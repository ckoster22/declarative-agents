"""
Base types and enums for the declarative agent framework.

This module contains the lowest volatility components: core types, enums,
and base models that define the fundamental structure of the framework.
"""

from enum import Enum
from typing import Dict, List, Union, Any
from pydantic import BaseModel, Field
from pydantic import ConfigDict, field_validator, model_validator
from config import BIG_MODEL, SMALL_MODEL, Model


class AgentType(str, Enum):
    """Types of agents in the system."""

    AGENT = "agent"
    TOOL = "tool"
    ORCHESTRATOR = "orchestrator"
    STRUCTURED_OUTPUT = "structured_output"


class FieldType(str, Enum):
    """JSON schema field types."""

    STRING = "string"
    INTEGER = "integer"
    NUMBER = "number"
    BOOLEAN = "boolean"
    ARRAY = "array"


class CommunicationMode(str, Enum):
    """Communication modes for workflow execution."""

    CHAT_HISTORY = "chat_history"
    CONTEXT = "context"


class AgentConfiguration(BaseModel):
    """Configuration for agent model settings."""

    model_config = ConfigDict(extra="forbid", validate_assignment=True, strict=True)

    name: str = BIG_MODEL
    temperature: float = 0.6
    top_p: float = 0.95
    # Do *not* impose a default token limit; let the underlying SDK/model decide.
    max_tokens: int | None = None

    @field_validator("temperature")
    @classmethod
    def _validate_temperature(cls, value: float) -> float:
        if not (0.0 <= value <= 2.0):
            raise ValueError("temperature must be between 0.0 and 2.0 inclusive")
        return value

    @field_validator("top_p")
    @classmethod
    def _validate_top_p(cls, value: float) -> float:
        if not (0.0 <= value <= 1.0):
            raise ValueError("top_p must be between 0.0 and 1.0 inclusive")
        return value

    @field_validator("max_tokens")
    @classmethod
    def _validate_max_tokens(cls, value: int | None) -> int | None:
        if value is not None and value <= 0:
            raise ValueError("max_tokens must be a positive integer when provided")
        return value


class ToolSpecification(BaseModel):
    """Specification for a tool that can be used by an agent."""

    model_config = ConfigDict(extra="forbid", validate_assignment=True, strict=True)

    name: str = Field(description="Name of the tool")
    function: str = Field(
        default="",
        description="Import path to the function (e.g., 'module.function_name')",
    )
    description: str = Field(
        default="", description="Description of what the tool does"
    )
    agent_as_tool: bool = Field(
        default=False,
        description="Whether this tool should invoke an agent from a YAML file",
    )
    agent_yaml_path: str = Field(
        default="",
        description="Path to the agent YAML file (required when agent_as_tool=True)",
    )
    input_template: str = Field(
        default="{input}",
        description=(
            "Template for agent input. Supports {input} and context placeholders like "
            "{AgentName}, {AgentName.output}, or nested {AgentName.key.subkey}. Values are JSON-encoded."
        ),
    )

    @model_validator(mode="after")
    def _validate_tool_invariants(self) -> "ToolSpecification":
        # If agent_as_tool is true, agent_yaml_path must be provided
        if self.agent_as_tool:
            if not self.agent_yaml_path:
                raise ValueError(
                    f"Tool '{self.name}': agent_yaml_path is required when agent_as_tool=True"
                )
            # If invoking an agent, function path should generally be empty to avoid confusion
            if self.function:
                raise ValueError(
                    f"Tool '{self.name}': function must be empty when agent_as_tool=True"
                )
        else:
            # Standard function tool must specify a function import path or a built-in name.
            # We intentionally allow non-dotted names here to support framework built-ins
            # (validated later by ToolLoader), while still requiring a non-empty value.
            if not self.function:
                raise ValueError(
                    f"Tool '{self.name}': function import path or built-in name is required when agent_as_tool=False"
                )
            # agent_yaml_path should not be set for a function tool
            if self.agent_yaml_path:
                raise ValueError(
                    f"Tool '{self.name}': agent_yaml_path must be empty when agent_as_tool=False"
                )
        return self


class OutputSchema(BaseModel):
    """Schema definition for structured output."""

    model_config = ConfigDict(extra="forbid", validate_assignment=True, strict=True)

    # Allow optional JSON Schema "type" for compatibility with YAMLs that include it.
    # When present, it must be "object" since we only support object-like outputs.
    type: str | None = Field(
        default=None,
        description="Optional JSON Schema type. If provided, must be 'object'.",
    )

    properties: Dict[str, Any] = Field(
        default_factory=dict, description="Properties of the output schema"
    )
    required: List[str] = Field(default_factory=list, description="Required properties")

    @field_validator("type")
    @classmethod
    def _validate_type(cls, value: str | None) -> str | None:
        if value is None:
            return value
        if value != "object":
            raise ValueError("OutputSchema.type must be 'object' when provided")
        return value

    @model_validator(mode="after")
    def _validate_required_subset(self) -> "OutputSchema":
        if self.required:
            missing = [key for key in self.required if key not in self.properties]
            if missing:
                raise ValueError(
                    f"OutputSchema.required contains keys not present in properties: {missing}"
                )
        return self


class InputSchema(BaseModel):
    """Schema definition for input requirements."""

    model_config = ConfigDict(extra="forbid", validate_assignment=True, strict=True)

    required_context: List[str] = Field(
        default_factory=list, description="Required context from other agents"
    )
    properties: Dict[str, Union[str, int, float, bool, list, dict]] = Field(
        default_factory=dict, description="Input properties"
    )

    @field_validator("required_context")
    @classmethod
    def _validate_unique_context(cls, value: List[str]) -> List[str]:
        if len(value) != len(set(value)):
            raise ValueError("InputSchema.required_context must not contain duplicates")
        return value


class AgentDefinition(BaseModel):
    """Complete agent definition from YAML."""

    model_config = ConfigDict(extra="forbid", validate_assignment=True, strict=True)

    name: str = Field(description="Name of the agent")
    prompt: str = Field(description="Prompt template for the agent")
    model: AgentConfiguration = Field(default_factory=AgentConfiguration)
    output_schema: OutputSchema = Field(
        default_factory=lambda: OutputSchema(properties={})
    )
    input_schema: InputSchema = Field(default_factory=InputSchema)
    tools: List[ToolSpecification] = Field(default_factory=list)
    agent_type: AgentType = Field(
        default=AgentType.AGENT, description="Type of agent to create"
    )
    formatter_model: Model = Field(
        default=SMALL_MODEL,
        description="Model name for formatter in structured output agents",
    )
    print_think_tokens: bool = Field(
        default=True, description="Whether to print think tokens during streaming"
    )
    max_iterations: int | None = Field(
        default=None,
        description="Override the maximum number of iterations (thought/tool cycles) allowed for this agent. If None, the underlying Runner default is used.",
    )

    @field_validator("name")
    @classmethod
    def _validate_name(cls, value: str) -> str:
        if not value or not value.strip():
            raise ValueError("agent.name must be a non-empty string")
        return value

    @field_validator("prompt")
    @classmethod
    def _validate_prompt(cls, value: str) -> str:
        if not value or not value.strip():
            raise ValueError("agent.prompt must be a non-empty string")
        return value

    @field_validator("max_iterations")
    @classmethod
    def _validate_max_iterations(cls, value: int | None) -> int | None:
        if value is not None and value <= 0:
            raise ValueError("max_iterations must be a positive integer when provided")
        return value

    @model_validator(mode="after")
    def _validate_agent_invariants(self) -> "AgentDefinition":
        # Structured output agents must declare an output schema
        if self.agent_type == AgentType.STRUCTURED_OUTPUT:
            if not self.output_schema.properties:
                raise ValueError(
                    "Structured output agents require a non-empty output_schema.properties"
                )
            if not self.formatter_model or not self.formatter_model.strip():
                raise ValueError(
                    "Structured output agents require a non-empty formatter_model"
                )
        return self
