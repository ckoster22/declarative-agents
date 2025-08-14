"""
StructuredOutputAgent for the declarative agent framework.

This agent provides a two-step thinking and formatting process that can be
used declaratively through YAML configuration files.
"""

import logging
import json
import re
from typing import TypeVar, Generic, Type, Optional
from pydantic import BaseModel
from agents import Agent, Runner, OpenAIChatCompletionsModel, RunResult
from config import get_external_client, BIG_MODEL, SMALL_MODEL, Model
from framework.utils import remove_think_tags, ThinkTagFilter

logger = logging.getLogger(__name__)

# Define a TypeVar for the Pydantic model
OutputType = TypeVar("OutputType", bound=BaseModel)


class StructuredOutputAgentError(Exception):
    """Custom exception for errors within the StructuredOutputAgent."""

    def __init__(self, message: str, raw_output: Optional[str] = None):
        super().__init__(message)
        self.raw_output = raw_output


class StructuredOutputAgent(Generic[OutputType]):
    """
    A framework-level agent that encapsulates a two-step agent process by taking
    a "thinker" agent and dynamically creating a "formatter" agent to parse the
    output into a structured Pydantic model.

    This abstracts away the two-call pattern, providing a single entry point
    that returns a validated data object, designed to work with the declarative
    framework.
    """

    def __init__(
        self,
        thinker_agent: Agent,
        output_model: Type[OutputType],
        formatter_model_name: Model = SMALL_MODEL,
        max_iterations: int | None = None,
    ):
        """
        Initialize the StructuredOutputAgent.

        Args:
            thinker_agent: The agent that performs the actual thinking/reasoning
            output_model: The Pydantic model class for structured output
            formatter_model_name: The model name for the formatter agent
        """
        self.thinker_agent = thinker_agent
        self.output_model = output_model
        self.formatter_model_name = formatter_model_name
        self._max_iterations = max_iterations

        # Dynamically create the internal formatter agent
        formatter_instructions = f"""You are a formatter agent. Your task is to convert the user's input text into a valid JSON object conforming to the {self.output_model.__name__} schema.
Your output MUST be ONLY the JSON object, with no other text, explanations, or markdown code blocks."""

        formatter_model = OpenAIChatCompletionsModel(
            model=formatter_model_name,
            openai_client=get_external_client(),
        )

        self.formatter_agent = Agent(
            name=f"{self.thinker_agent.name}Formatter",
            instructions=formatter_instructions,
            model=formatter_model,
            model_settings=self.thinker_agent.model_settings,
            output_type=self.output_model,
        )
        # Configure formatter agent to not print think tokens
        # Note: This assumes the Agent class supports this attribute directly
        self.formatter_agent.print_think_tokens = False

        logger.debug(
            f"Initialized StructuredOutputAgent for {self.thinker_agent.name} -> {self.formatter_agent.name} (internal)"
        )

    def _extract_text_delta(self, event: object) -> str | None:
        """Extract a textual delta from a streaming event without using exceptions for control flow."""
        # Case 1: direct string delta
        ev_delta = getattr(event, "delta", None)
        if isinstance(ev_delta, str):
            return ev_delta

        data_obj = getattr(event, "data", None)
        # Case 2: data is a plain string, possibly OpenAI-like SSE line
        if isinstance(data_obj, str) and data_obj:
            s = data_obj.strip()
            if s.startswith("data:"):
                s = s[5:].strip()
            if s and s != "[DONE]":
                # Attempt JSON parse; if it fails, fall back to regex extraction
                try:
                    obj = json.loads(s)
                    text: str | None = None
                    for choice in obj.get("choices", []):
                        content = (
                            choice.get("delta", {}).get("content")
                            or choice.get("message", {}).get("content")
                        )
                        if isinstance(content, str) and content:
                            text = (text or "") + content
                    return text
                except Exception:
                    m = re.search(r'"content"\s*:\s*"(.*?)"', s)
                    return m.group(1) if m else None
            return None

        # Case 3: data has a delta attribute
        data_delta = getattr(data_obj, "delta", None)
        if isinstance(data_delta, str):
            return data_delta
        return None

    async def run(self, input_data: str) -> OutputType:
        """
        Execute the two-step thinking and formatting process.

        Args:
            input_data: The input to be passed to the thinker agent

        Returns:
            A parsed Pydantic object of type OutputType

        Raises:
            StructuredOutputAgentError: If the formatter fails to parse the thinker's output
        """
        logger.info(
            f"Running StructuredOutputAgent chain for '{self.thinker_agent.name}'..."
        )

        # 1. Stream the thinker agent so we can surface think tokens if enabled
        think_filter = ThinkTagFilter()
        should_print_think = bool(getattr(self.thinker_agent, "print_think_tokens", False))

        streamed = Runner.run_streamed(
            starting_agent=self.thinker_agent,
            input=input_data,
            max_turns=self._max_iterations or 10,
        )

        raw_chunks: list[str] = []
        async for event in streamed.stream_events():
            text_delta = self._extract_text_delta(event)
            if text_delta is None:
                continue

            raw_chunks.append(text_delta)
            if should_print_think:
                print(text_delta, end="", flush=True)
            else:
                chunk = think_filter.filter_token(text_delta)
                if chunk:
                    print(chunk, end="", flush=True)

        print()

        # Use concatenated chunks as the raw thinker output
        raw_output_text = "".join(raw_chunks)
        logger.debug(
            f"Raw output from {self.thinker_agent.name}:\n{raw_output_text}"
        )

        # Clean the raw output by removing think tags before passing to formatter
        cleaned_output_text = remove_think_tags(raw_output_text)

        logger.debug(
            f"Cleaned output (think tags removed) from {self.thinker_agent.name}:\n{cleaned_output_text}"
        )

        # 2. Run the internal formatter agent to parse the cleaned output
        # Do not stream formatter; it should not print think tokens and must return clean JSON
        formatter_result: RunResult = await Runner.run(
            starting_agent=self.formatter_agent,
            input=cleaned_output_text,
        )

        # 3. Parse structured output deterministically
        final_output = formatter_result.final_output_as(self.output_model)
        if final_output is None:
            raise StructuredOutputAgentError(
                f"Failed to parse output from {self.formatter_agent.name}",
                raw_output=str(formatter_result.final_output),
            )

        logger.info(
            f"StructuredOutputAgent chain for '{self.thinker_agent.name}' completed successfully."
        )
        return final_output

    @classmethod
    def create_from_config(
        cls,
        name: str,
        instructions: str,
        output_model: Type[OutputType],
        model_name: Model = BIG_MODEL,
        formatter_model_name: Model = SMALL_MODEL,
        temperature: float = 0.6,
        top_p: float = 0.95,
        max_tokens: int | None = None,
    ) -> "StructuredOutputAgent[OutputType]":
        """
        Create a StructuredOutputAgent from configuration parameters.

        This method is designed to be used by the declarative framework
        to create agents from YAML configuration.

        Args:
            name: Name of the thinker agent
            instructions: Instructions for the thinker agent
            output_model: Pydantic model for structured output
            model_name: Model name for the thinker agent
            formatter_model_name: Model name for the formatter agent
            temperature: Temperature setting for the model
            top_p: Top-p setting for the model
            max_tokens: Maximum tokens for the model

        Returns:
            A configured StructuredOutputAgent instance
        """
        from framework.declarative_agents import ModelSettings

        client = get_external_client()
        if client is None:
            raise ValueError(
                "Failed to get LM Studio client. Check if LM Studio server is running."
            )

        model_settings = ModelSettings(
            temperature=temperature,
            top_p=top_p,
            max_tokens=max_tokens,
        )

        thinker_agent = Agent(
            name=name,
            instructions=instructions,
            model=OpenAIChatCompletionsModel(model=model_name, openai_client=client),
            model_settings=model_settings,
        )

        return cls(
            thinker_agent=thinker_agent,
            output_model=output_model,
            formatter_model_name=formatter_model_name,
        )
