"""
Agent specifications and execution for the declarative agent framework.

This module handles the creation and execution of agents from YAML specifications,
including proper streaming and structured output support.
"""

from dataclasses import dataclass
from inspect import signature
from typing import Dict, List, Optional, Sequence, Type, TypedDict, Union

import yaml

# __init__.py for declarative_agents package
from agents import Agent, FunctionTool, ModelSettings, OpenAIChatCompletionsModel, Runner, RunResult
from pydantic import BaseModel

from config import SMALL_MODEL, get_external_client
from framework.context import AgentContext, AgentOutput, ContextFormatter
from framework.models import ModelFactory
from framework.specialized_agents import StructuredOutputAgent
from framework.tool_context import set_current_context
from framework.tools import ToolLoader
from framework.types import (
    AgentAsToolSpec,
    AgentDefinition,
    AgentType,
    FunctionToolSpec,
    InputSchema,
    OrchestratorAgentDefinition,
    OutputSchema,
    StandardAgentDefinition,
    StructuredOutputAgentDefinition,
    StructuredOutputSchema,
    ToolSpecification,
)
from framework.utils import ThinkTagFilter, clean_agent_output, extract_text_delta_from_event, remove_think_tags

# --- Begin restored custom agent framework classes ---


@dataclass
class AgentKwargs:
    """Type-safe container for Agent constructor arguments."""

    name: str
    instructions: str
    model: OpenAIChatCompletionsModel
    model_settings: ModelSettings
    tools: Sequence[FunctionTool]
    output_type: Optional[Type[BaseModel]] = None
    max_iterations: Optional[int] = None


class YamlData(TypedDict):
    """Type-safe structure for YAML configuration data."""

    agent: Dict[str, Union[str, int, float, bool, list, dict]]
    model: Optional[Dict[str, Union[str, int, float]]]
    tools: Optional[List[Dict[str, Union[str, bool]]]]
    output_schema: Optional[Dict[str, Union[str, dict]]]
    input_schema: Optional[Dict[str, Union[str, list]]]
    max_iterations: Optional[int]


class AgentData(TypedDict):
    """Type-safe structure for agent data within YAML."""

    name: str
    prompt: str
    type: Optional[str]
    formatter_model: Optional[str]
    print_think_tokens: Optional[bool]
    max_iterations: Optional[int]


class AgentSpecification:
    """Agent specification loaded from YAML with execution capabilities."""

    def __init__(self, definition: AgentDefinition):
        self.definition = definition
        self.output_model: Optional[Type[BaseModel]] = self._create_output_model()
        self.structured_output_agent = None

        # Validate tools at initialization
        if self.definition.tools:
            ToolLoader.validate_tools(self.definition.tools)

        # Pre-create structured output agent if needed
        # Type narrowing: agent_type == STRUCTURED_OUTPUT guarantees StructuredOutputAgentDefinition
        if self.definition.agent_type == AgentType.STRUCTURED_OUTPUT:
            # For structured output agents, output_model is guaranteed to be non-None
            # because StructuredOutputSchema requires non-empty properties
            if self.output_model is None:
                raise ValueError("StructuredOutputAgent requires an output_schema to be defined")
            self.structured_output_agent = self._create_structured_output_agent()

    def _create_output_model(self) -> Optional[Type[BaseModel]]:
        """Create output model from schema if present."""
        if self.definition.output_schema.properties:
            return ModelFactory.create_output_model_from_schema(
                self.definition.output_schema, f"{self.definition.name}Output"
            )
        return None

    def _create_structured_output_agent(self) -> StructuredOutputAgent:
        """Create a StructuredOutputAgent instance."""
        # Create the thinker agent with tools
        client = get_external_client()
        if client is None:
            raise ValueError("Failed to get LM Studio client. Check if LM Studio server is running.")

        model_settings = ModelSettings(
            temperature=self.definition.model.temperature,
            top_p=self.definition.model.top_p,
            max_tokens=self.definition.model.max_tokens,
        )

        # Add tools if they exist
        tools: Sequence[FunctionTool] = []
        if self.definition.tools:
            tools = ToolLoader.load_tools(self.definition.tools)

        agent_kwargs = AgentKwargs(
            name=self.definition.name,
            instructions=self.definition.prompt,
            model=OpenAIChatCompletionsModel(model=self.definition.model.name, openai_client=client),
            model_settings=model_settings,
            tools=tools,
        )

        thinker_agent = Agent(
            name=agent_kwargs.name,
            instructions=agent_kwargs.instructions,
            model=agent_kwargs.model,
            model_settings=agent_kwargs.model_settings,
            tools=list(agent_kwargs.tools),
        )

        # output_model is guaranteed to be non-None for StructuredOutputAgentDefinition
        # because StructuredOutputSchema requires non-empty properties
        assert self.output_model is not None, "output_model cannot be None for StructuredOutputAgent"

        # Ensure the thinker agent respects the YAML flag for think-token printing
        thinker_agent.print_think_tokens = self.definition.print_think_tokens  # type: ignore[attr-defined]

        # Type narrowing: agent_type == STRUCTURED_OUTPUT guarantees StructuredOutputAgentDefinition
        if self.definition.agent_type != AgentType.STRUCTURED_OUTPUT:
            raise ValueError(f"Expected StructuredOutputAgentDefinition, got agent_type: {self.definition.agent_type}")
        
        # Type narrowing: definition is StructuredOutputAgentDefinition
        structured_def: StructuredOutputAgentDefinition = self.definition  # type: ignore[assignment]

        return StructuredOutputAgent(
            thinker_agent=thinker_agent,
            output_model=self.output_model,
            formatter_model_name=structured_def.formatter_model,
            max_iterations=structured_def.max_iterations,
        )

    def create_agent(self) -> Agent:
        """Create an Agent instance with proper configuration."""
        client = get_external_client()
        if client is None:
            raise ValueError("Failed to get LM Studio client. Check if LM Studio server is running.")

        model_settings = ModelSettings(
            temperature=self.definition.model.temperature,
            top_p=self.definition.model.top_p,
            max_tokens=self.definition.model.max_tokens,
        )

        # Add tools if they exist
        tools: Sequence[FunctionTool] = []
        if self.definition.tools:
            tools = ToolLoader.load_tools(self.definition.tools)

        # Optional: pass max_iterations if supported by the underlying Agent class
        max_iterations: Optional[int] = None
        if self.definition.max_iterations is not None:
            if "max_iterations" in signature(Agent).parameters:
                max_iterations = self.definition.max_iterations

        agent_kwargs = AgentKwargs(
            name=self.definition.name,
            instructions=self.definition.prompt,
            model=OpenAIChatCompletionsModel(model=self.definition.model.name, openai_client=client),
            model_settings=model_settings,
            tools=tools,
            output_type=self.output_model,
            max_iterations=max_iterations,
        )

        agent = Agent(
            name=agent_kwargs.name,
            instructions=agent_kwargs.instructions,
            model=agent_kwargs.model,
            model_settings=agent_kwargs.model_settings,
            tools=list(agent_kwargs.tools),
            output_type=agent_kwargs.output_type,
        )
        # Configure agent to print think tokens
        # Note: This assumes the Agent class supports this attribute directly
        agent.print_think_tokens = self.definition.print_think_tokens
        return agent

    async def run(
        self,
        input_data: str = "",
        context: Optional[AgentContext] = None,
        agent_type: AgentType = AgentType.ORCHESTRATOR,
    ) -> AgentOutput:
        """Execute the agent with proper streaming and context handling."""
        full_input = self._prepare_input(input_data, context)

        # Use structured output agent if configured
        # Type narrowing: agent_type == STRUCTURED_OUTPUT guarantees StructuredOutputAgentDefinition
        if self.definition.agent_type == AgentType.STRUCTURED_OUTPUT:
            if not self.structured_output_agent:
                raise ValueError("StructuredOutputAgent not properly initialized")

            # Set context for tool execution
            set_current_context(context)

            # Run the structured output agent
            result = await self.structured_output_agent.run(full_input)
            return result.model_dump()

        # Regular agent execution
        agent = self.create_agent()

        # Set context for tool execution
        set_current_context(context)

        # Build kwargs for Runner.run allowing optional max_iterations
        max_turns = 10
        if self.definition.max_iterations is not None:
            max_turns = self.definition.max_iterations

        # Stream tokens live to stdout while capturing the final result
        streamed = Runner.run_streamed(
            starting_agent=agent,
            input=full_input,
            max_turns=max_turns,
        )

        # Stream semantic events and print message chunks
        think_filter = ThinkTagFilter()
        should_print_think = bool(self.definition.print_think_tokens)
        async for event in streamed.stream_events():
            text_delta = extract_text_delta_from_event(event)
            if text_delta is None:
                continue

            if should_print_think:
                print(text_delta, end="", flush=True)
            else:
                chunk = think_filter.filter_token(text_delta)
                if chunk:
                    print(chunk, end="", flush=True)

        # Ensure a newline before returning the final result
        print()

        return self._extract_output(streamed)

    def _prepare_input(self, input_data: str, context: Optional[AgentContext]) -> str:
        """Prepare the full input including context if available."""
        if context:
            context_input = ContextFormatter.prepare_context_input(
                context, self.definition.input_schema, self.definition.name
            )
            if context_input:
                return f"{context_input}\n\nTask: {input_data}" if input_data else context_input

        return input_data

    def _extract_output(self, result: RunResult) -> AgentOutput:
        """Extract output from stream result with automatic think tag removal."""
        if self.output_model:
            structured_output = result.final_output_as(self.output_model)
            if structured_output:
                # Clean the structured output by removing think tags from string values
                cleaned_output = clean_agent_output(structured_output.model_dump())
                return cleaned_output
            else:
                # Clean the raw output before returning
                raw_output = remove_think_tags(str(result.final_output))
                return {"raw_output": raw_output}
        else:
            # Clean the final output before returning
            raw_output = remove_think_tags(str(result.final_output))
            return raw_output


class AgentLoader:
    """Loads agent specifications from YAML files."""

    @staticmethod
    def load_from_file(yaml_path: str) -> AgentSpecification:
        """Load an agent specification from a YAML file."""
        with open(yaml_path, "r") as f:
            data = yaml.safe_load(f)

        # Enforce top-level YAML structure to fail-fast on unknown keys
        if not isinstance(data, dict):
            raise ValueError("YAML root must be a mapping (object)")

        allowed_top_keys = {"agent", "model", "tools", "output_schema", "input_schema", "max_iterations"}
        unknown_top = set(data.keys()) - allowed_top_keys
        if unknown_top:
            raise ValueError(
                f"Unknown top-level keys in YAML: {sorted(unknown_top)}. Allowed keys: {sorted(allowed_top_keys)}"
            )

        return AgentLoader.load_from_dict(data)

    @staticmethod
    def load_from_dict(
        data: YamlData,
    ) -> AgentSpecification:
        """Load an agent specification from a dictionary.

        The YAML format allows certain keys (model, tools, input_schema, output_schema)
        to live at the top-level, separate from the `agent:` block.  This method
        now merges those sections back into the AgentDefinition so that features
        such as tool usage continue to function.
        """
        if "agent" not in data:
            raise ValueError("YAML must contain 'agent' section")

        # Copy to avoid mutating the caller's data and validate keys
        if not isinstance(data["agent"], dict):
            raise ValueError("'agent' section must be a mapping (object)")
        agent_data = dict(data["agent"])  # type: ignore[arg-type]

        allowed_agent_keys = {
            "name",
            "prompt",
            "type",
            "formatter_model",
            "print_think_tokens",
            "max_iterations",
        }
        unknown_agent = set(agent_data.keys()) - allowed_agent_keys
        if unknown_agent:
            raise ValueError(
                f"Unknown keys under 'agent': {sorted(unknown_agent)}. Allowed keys: {sorted(allowed_agent_keys)}"
            )

        # Map the YAML `type` field (string) ➜ enum value expected by pydantic
        # Strict validation: fail fast on invalid agent types
        agent_type_str = agent_data.pop("type", AgentType.AGENT.value)
        try:
            agent_type = AgentType(agent_type_str)
        except ValueError as e:
            raise ValueError(f"Invalid agent type '{agent_type_str}'. Valid types: {[t.value for t in AgentType]}") from e

        # Gather optional top-level sections with explicit type checks
        model_config = data.get("model", {})
        if not isinstance(model_config, dict):
            raise ValueError("Top-level 'model' must be a mapping (object)")
        output_schema_cfg = data.get("output_schema", {})
        if not isinstance(output_schema_cfg, dict):
            raise ValueError("Top-level 'output_schema' must be a mapping (object)")
        input_schema_cfg = data.get("input_schema", {})
        if not isinstance(input_schema_cfg, dict):
            raise ValueError("Top-level 'input_schema' must be a mapping (object)")
        tools_cfg = data.get("tools", [])
        if not isinstance(tools_cfg, list):
            raise ValueError("Top-level 'tools' must be a list")

        # Build tools as discriminated unions
        tools: List[ToolSpecification] = []
        for tool_dict in tools_cfg:
            if tool_dict.get("agent_as_tool", False):
                tool = AgentAsToolSpec(
                    name=str(tool_dict["name"]),
                    agent_yaml_path=str(tool_dict.get("agent_yaml_path", "")),
                    description=str(tool_dict.get("description", "")),
                    input_template=str(tool_dict.get("input_template", "{input}")),
                )
            else:
                tool = FunctionToolSpec(
                    name=str(tool_dict["name"]),
                    function=str(tool_dict.get("function", "")),
                    description=str(tool_dict.get("description", "")),
                    input_template=str(tool_dict.get("input_template", "{input}")),
                )
            tools.append(tool)

        # Build the appropriate discriminated union type based on agent_type
        # StructuredOutputSchema will validate non-empty properties, so no need to check here
        if agent_type == AgentType.STRUCTURED_OUTPUT:
            definition: AgentDefinition = StructuredOutputAgentDefinition(
                name=str(agent_data["name"]),
                prompt=str(agent_data["prompt"]),
                model=model_config,  # type: ignore[arg-type]
                output_schema=StructuredOutputSchema(**output_schema_cfg),  # type: ignore[arg-type]
                input_schema=InputSchema(**input_schema_cfg),  # type: ignore[arg-type]
                tools=tools,
                formatter_model=str(agent_data.get("formatter_model", SMALL_MODEL)),
                print_think_tokens=bool(agent_data.get("print_think_tokens", True)),
                max_iterations=agent_data.get("max_iterations", data.get("max_iterations")),  # type: ignore[arg-type]
            )
        elif agent_type == AgentType.ORCHESTRATOR:
            definition = OrchestratorAgentDefinition(
                name=str(agent_data["name"]),
                prompt=str(agent_data["prompt"]),
                model=model_config,  # type: ignore[arg-type]
                output_schema=OutputSchema(**output_schema_cfg),  # type: ignore[arg-type]
                input_schema=InputSchema(**input_schema_cfg),  # type: ignore[arg-type]
                tools=tools,
                print_think_tokens=bool(agent_data.get("print_think_tokens", True)),
                max_iterations=agent_data.get("max_iterations", data.get("max_iterations")),  # type: ignore[arg-type]
            )
        else:
            definition = StandardAgentDefinition(
                name=str(agent_data["name"]),
                prompt=str(agent_data["prompt"]),
                agent_type=agent_type,  # type: ignore[arg-type]
                model=model_config,  # type: ignore[arg-type]
                output_schema=OutputSchema(**output_schema_cfg),  # type: ignore[arg-type]
                input_schema=InputSchema(**input_schema_cfg),  # type: ignore[arg-type]
                tools=tools,
                print_think_tokens=bool(agent_data.get("print_think_tokens", True)),
                max_iterations=agent_data.get("max_iterations", data.get("max_iterations")),  # type: ignore[arg-type]
            )

        return AgentSpecification(definition)


async def run_agent_from_yaml(
    yaml_path: str, input_data: str = "", agent_type: AgentType = AgentType.ORCHESTRATOR
) -> str:
    """Load and run an agent from a YAML file with token streaming."""
    agent_spec = AgentLoader.load_from_file(yaml_path)

    # Create a context for the agent execution
    context = AgentContext()
    result = await agent_spec.run(input_data, context=context, agent_type=agent_type)
    return str(result)


# --- End restored custom agent framework classes ---
