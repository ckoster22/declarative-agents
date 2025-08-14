"""
Declarative Agent Framework

A framework for creating and executing agents from YAML specifications
with proper volatility-based decomposition.
"""

from typing import List, Callable
from framework.types import (
    AgentType,
    FieldType,
    CommunicationMode,
    AgentConfiguration,
    ToolSpecification,
    OutputSchema,
    InputSchema,
    AgentDefinition,
)

from framework.context import (
    AgentContext,
    ContextFormatter,
)

from framework.models import (
    ModelFactory,
)

from framework.tools import (
    ToolLoader,
)
from framework.agent_runner import run_agent_as_tool
from framework.tool_context import (
    set_current_context,
    get_current_context,
)
from agents import FunctionTool

from framework.input_sources import (
    InputSourceHandler,
)

from framework.file_tools import (
    read_file,
    append_to_file,
    get_temp_directory_info,
)

from framework.user_tools import (
    user_input_tool,
    get_current_datetime_tool,
)

from framework.declarative_agents import (
    AgentSpecification,
    AgentLoader,
    run_agent_from_yaml,
)



from framework.utils import (
    remove_think_tags,
    clean_agent_output,
    is_think_tag_token,
    ThinkTagFilter,
)

# Legacy compatibility layer
# Legacy class names for backward compatibility
AgentSpec = AgentSpecification

# Legacy function names for backward compatibility
load_agent_from_file = AgentLoader.load_from_file
create_output_model_from_schema = ModelFactory.create_output_model_from_schema
format_output_for_chat_history = ContextFormatter.format_output_for_chat_history
prepare_context_input = ContextFormatter.prepare_context_input
import_function_from_string = ToolLoader._import_function_from_string


# Legacy tool functions for backward compatibility
def validate_tools_spec(tools_spec) -> None:
    tool_specs = [ToolSpecification(**tool) for tool in tools_spec]
    ToolLoader.validate_tools(tool_specs)


def get_tools_from_yaml_spec(tools_spec) -> List[FunctionTool]:
    tool_specs = [ToolSpecification(**tool) for tool in tools_spec]
    return ToolLoader.load_tools(tool_specs)


def get_tools_for_agent(tools_spec) -> List[FunctionTool]:
    tool_specs = [ToolSpecification(**tool) for tool in tools_spec]
    return ToolLoader.load_tools(tool_specs)


__all__ = [
    # Types
    "AgentType",
    "FieldType",
    "CommunicationMode",
    "AgentConfiguration",
    "ToolSpecification",
    "OutputSchema",
    "InputSchema",
    "AgentDefinition",
    # Legacy compatibility
    "AgentSpec",
    "load_agent_from_file",
    "create_output_model_from_schema",
    "format_output_for_chat_history",
    "prepare_context_input",
    "import_function_from_string",
    "validate_tools_spec",
    "get_tools_from_yaml_spec",
    "get_tools_for_agent",
    # Context
    "AgentContext",
    "ContextFormatter",
    # Models
    "ModelFactory",
    # Tools
    "ToolLoader",
    "run_agent_as_tool",
    "set_current_context",
    "get_current_context",

    # Input Sources
    "InputSourceHandler",
    # File Tools
    "read_file",
    "append_to_file",
    "get_temp_directory_info",
    # User Tools
    "user_input_tool",
    "get_current_datetime_tool",
    # Agents
    "AgentSpecification",
    "AgentLoader",
    "run_agent_from_yaml",
    # Utilities
    "remove_think_tags",
    "clean_agent_output",
    "is_think_tag_token",
    "ThinkTagFilter",
]
