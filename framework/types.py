"""
Base types and enums for the declarative agent framework.

This module contains the lowest volatility components: core types, enums,
and base models that define the fundamental structure of the framework.
"""

from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Literal, Union, cast

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from config import BIG_MODEL, SMALL_MODEL, Model

# Type aliases for semantic clarity
FilePath = Path
DirectoryPath = Path
YamlPath = Path


class NonEmptyDict(dict):
    """Dictionary that must contain at least one key-value pair."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self:
            raise ValueError("NonEmptyDict must contain at least one item")


class NonEmptyList(list):
    """List that must contain at least one element."""

    def __init__(self, *args):
        super().__init__(*args)
        if not self:
            raise ValueError("NonEmptyList must contain at least one element")


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
        if not 0.0 <= value <= 2.0:
            raise ValueError("temperature must be between 0.0 and 2.0 inclusive")
        return value

    @field_validator("top_p")
    @classmethod
    def _validate_top_p(cls, value: float) -> float:
        if not 0.0 <= value <= 1.0:
            raise ValueError("top_p must be between 0.0 and 1.0 inclusive")
        return value

    @field_validator("max_tokens")
    @classmethod
    def _validate_max_tokens(cls, value: int | None) -> int | None:
        if value is not None and value <= 0:
            raise ValueError("max_tokens must be a positive integer when provided")
        return value


class FunctionToolSpec(BaseModel):
    """Specification for a function-based tool."""

    model_config = ConfigDict(extra="forbid", validate_assignment=True, strict=True)

    tool_type: Literal["function"] = "function"
    name: str = Field(description="Name of the tool")
    function: str = Field(description="Import path to the function (e.g., 'module.function_name')")
    description: str = Field(default="", description="Description of what the tool does")
    input_template: str = Field(
        default="{input}",
        description="Template for agent input with {input} placeholder and other parameters",
    )


class AgentAsToolSpec(BaseModel):
    """Specification for an agent-as-tool."""

    model_config = ConfigDict(extra="forbid", validate_assignment=True, strict=True)

    tool_type: Literal["agent"] = "agent"
    name: str = Field(description="Name of the tool")
    agent_yaml_path: str = Field(description="Path to the agent YAML file")
    description: str = Field(default="", description="Description of what the tool does")
    input_template: str = Field(
        default="{input}",
        description="Template for agent input with {input} placeholder and other parameters",
    )


ToolSpecification = Union[FunctionToolSpec, AgentAsToolSpec]


class OutputSchema(BaseModel):
    """Schema definition for structured output."""

    model_config = ConfigDict(extra="forbid", validate_assignment=True, strict=True)

    # Allow optional JSON Schema "type" for compatibility with YAMLs that include it.
    # When present, it must be "object" since we only support object-like outputs.
    type: str | None = Field(
        default=None,
        description="Optional JSON Schema type. If provided, must be 'object'.",
    )

    properties: Dict[str, Any] = Field(default_factory=dict, description="Properties of the output schema")
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
        # Help pylint with pydantic FieldInfo type by asserting dict interface
        props: Dict[str, Any] = dict(self.properties)
        if self.required:
            missing = [key for key in self.required if key not in props]
            if missing:
                raise ValueError(f"OutputSchema.required contains keys not present in properties: {missing}")
        return self


class StructuredOutputSchema(BaseModel):
    """Schema definition for structured output with required non-empty properties."""

    model_config = ConfigDict(extra="forbid", validate_assignment=True, strict=True)

    type: str | None = Field(
        default=None,
        description="Optional JSON Schema type. If provided, must be 'object'.",
    )

    properties: Dict[str, Any] = Field(description="Properties of the output schema (must be non-empty)")
    required: List[str] = Field(default_factory=list, description="Required properties")

    @field_validator("properties")
    @classmethod
    def _validate_properties_non_empty(cls, value: Dict[str, Any]) -> Dict[str, Any]:
        if not value:
            raise ValueError("StructuredOutputSchema.properties must be non-empty")
        return value

    @field_validator("type")
    @classmethod
    def _validate_type(cls, value: str | None) -> str | None:
        if value is None:
            return value
        if value != "object":
            raise ValueError("StructuredOutputSchema.type must be 'object' when provided")
        return value

    @model_validator(mode="after")
    def _validate_required_subset(self) -> "StructuredOutputSchema":
        props: Dict[str, Any] = dict(self.properties)
        if self.required:
            missing = [key for key in self.required if key not in props]
            if missing:
                raise ValueError(f"StructuredOutputSchema.required contains keys not present in properties: {missing}")
        return self


class InputSchema(BaseModel):
    """Schema definition for input requirements."""

    model_config = ConfigDict(extra="forbid", validate_assignment=True, strict=True)

    required_context: List[str] = Field(default_factory=list, description="Required context from other agents")
    properties: Dict[str, Union[str, int, float, bool, list, dict]] = Field(
        default_factory=dict, description="Input properties"
    )

    @field_validator("required_context")
    @classmethod
    def _validate_unique_context(cls, value: List[str]) -> List[str]:
        if len(value) != len(set(value)):
            raise ValueError("InputSchema.required_context must not contain duplicates")
        return value


class StandardAgentDefinition(BaseModel):
    """Standard agent definition from YAML."""

    model_config = ConfigDict(extra="forbid", validate_assignment=True, strict=True)

    agent_type: Literal[AgentType.AGENT, AgentType.TOOL] = Field(description="Type of agent")
    name: str = Field(description="Name of the agent")
    prompt: str = Field(description="Prompt template for the agent")
    model: AgentConfiguration = Field(default_factory=AgentConfiguration)
    output_schema: OutputSchema = Field(default_factory=lambda: OutputSchema(properties={}))
    input_schema: InputSchema = Field(default_factory=InputSchema)
    tools: List[ToolSpecification] = Field(default_factory=list)
    print_think_tokens: bool = Field(default=True, description="Whether to print think tokens during streaming")
    max_iterations: int | None = Field(
        default=None,
        description=(
            "Override the maximum number of iterations (thought/tool cycles) allowed "
            "for this agent. If None, the underlying Runner default is used."
        ),
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


class StructuredOutputAgentDefinition(BaseModel):
    """Structured output agent definition from YAML."""

    model_config = ConfigDict(extra="forbid", validate_assignment=True, strict=True)

    agent_type: Literal[AgentType.STRUCTURED_OUTPUT] = AgentType.STRUCTURED_OUTPUT
    name: str = Field(description="Name of the agent")
    prompt: str = Field(description="Prompt template for the agent")
    model: AgentConfiguration = Field(default_factory=AgentConfiguration)
    output_schema: StructuredOutputSchema = Field(description="Output schema with non-empty properties")
    input_schema: InputSchema = Field(default_factory=InputSchema)
    tools: List[ToolSpecification] = Field(default_factory=list)
    formatter_model: Model = Field(description="Model name for formatter")
    print_think_tokens: bool = Field(default=True, description="Whether to print think tokens during streaming")
    max_iterations: int | None = Field(
        default=None,
        description=(
            "Override the maximum number of iterations (thought/tool cycles) allowed "
            "for this agent. If None, the underlying Runner default is used."
        ),
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

    @field_validator("formatter_model")
    @classmethod
    def _validate_formatter_model(cls, value: Model) -> Model:
        model_str = str(value)
        if not model_str or not model_str.strip():
            raise ValueError("Structured output agents require a non-empty formatter_model")
        return value


class OrchestratorAgentDefinition(BaseModel):
    """Orchestrator agent definition from YAML."""

    model_config = ConfigDict(extra="forbid", validate_assignment=True, strict=True)

    agent_type: Literal[AgentType.ORCHESTRATOR] = AgentType.ORCHESTRATOR
    name: str = Field(description="Name of the agent")
    prompt: str = Field(description="Prompt template for the agent")
    model: AgentConfiguration = Field(default_factory=AgentConfiguration)
    output_schema: OutputSchema = Field(default_factory=lambda: OutputSchema(properties={}))
    input_schema: InputSchema = Field(default_factory=InputSchema)
    tools: List[ToolSpecification] = Field(default_factory=list)
    print_think_tokens: bool = Field(default=True, description="Whether to print think tokens during streaming")
    max_iterations: int | None = Field(
        default=None,
        description=(
            "Override the maximum number of iterations (thought/tool cycles) allowed "
            "for this agent. If None, the underlying Runner default is used."
        ),
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


AgentDefinition = Union[StandardAgentDefinition, StructuredOutputAgentDefinition, OrchestratorAgentDefinition]
