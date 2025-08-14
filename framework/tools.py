"""
Tool integration utilities for the declarative agent framework.

This module handles the loading and integration of tools that can be used by agents,
including dynamic function imports, tool validation, and declarative agent-as-tool support.
"""

import importlib
import pathlib
from typing import List, Callable, Protocol, Optional, Awaitable, Callable as _Callable
import yaml

from agents import function_tool, FunctionTool

from framework.types import ToolSpecification
from framework.file_tools import read_file, append_to_file, get_temp_directory_info
from framework.user_tools import user_input_tool, get_current_datetime_tool
from framework.input_sources import InputSourceHandler
from framework.tool_context import set_current_context, get_current_context


class ToolFunction(Protocol):
    """Protocol for tool functions that can be wrapped by function_tool."""
    __name__: str
    def __call__(self, input: str = "", **kwargs) -> str: ...


# ---- Agent-as-tool callback registration ------------------------------------
from framework.context import AgentContext

_run_agent_as_tool_cb: Optional[_Callable[[str, str, Optional[AgentContext]], Awaitable[str]]] = None


def register_run_agent_as_tool(
    callback: _Callable[[str, str, Optional[AgentContext]], Awaitable[str]]
) -> None:
    """Register the function used to execute agents-as-tools.

    This indirection avoids import cycles between tools and agent loading.
    """
    global _run_agent_as_tool_cb
    _run_agent_as_tool_cb = callback


async def run_agent_as_tool(yaml_path: str, input_data: str, context: Optional[AgentContext] = None) -> str:
    if _run_agent_as_tool_cb is None:
        raise RuntimeError("run_agent_as_tool callback not registered")
    return await _run_agent_as_tool_cb(yaml_path, input_data, context)




class ToolLoader:
    """Loads and validates tools for agent use."""

    # Built-in framework tools
    _BUILTIN_TOOLS = {
        "read_file": read_file,
        "append_to_file": append_to_file,
        "user_input_tool": user_input_tool,
        "get_current_datetime_tool": get_current_datetime_tool,
        "get_temp_directory_info": get_temp_directory_info,
    
    }

    @staticmethod
    def get_builtin_tools() -> List[FunctionTool]:
        """Get all built-in framework tools as function_tool instances."""
        loaded_tools = []

        for tool_name, builtin_func in ToolLoader._BUILTIN_TOOLS.items():
            function_tool_instance = function_tool(func=builtin_func)  # type: ignore[call-overload]
            loaded_tools.append(function_tool_instance)

        return loaded_tools

    @staticmethod
    def validate_tools(tools: List[ToolSpecification]) -> None:
        """Validate that all tools can be imported and used."""
        for tool in tools:
            if tool.agent_as_tool:
                ToolLoader._validate_agent_as_tool(tool)
            elif tool.function in ToolLoader._BUILTIN_TOOLS:
                # Built-in tools are always valid
                pass
            else:
                ToolLoader._import_function_from_string(tool.function)

    @staticmethod
    def load_tools(tools: List[ToolSpecification]) -> List[FunctionTool]:
        """Load tools from specifications into function_tool instances."""
        loaded_tools = []

        for tool in tools:
            if tool.agent_as_tool:
                current_func: ToolFunction = ToolLoader._create_agent_tool_function(tool)
            elif tool.function in ToolLoader._BUILTIN_TOOLS:
                # Handle built-in framework tools
                current_func = ToolLoader._BUILTIN_TOOLS[tool.function]  # type: ignore[assignment]
            else:
                current_func = ToolLoader._import_function_from_string(tool.function)  # type: ignore[assignment]

            if tool.name != current_func.__name__:
                function_tool_instance = function_tool(
                    func=current_func, name_override=tool.name, description_override=tool.description
                )  # type: ignore[call-overload]
            else:
                function_tool_instance = function_tool(func=current_func)  # type: ignore[call-overload]

            loaded_tools.append(function_tool_instance)

        return loaded_tools

    @staticmethod
    def _validate_agent_as_tool(tool: ToolSpecification) -> None:
        """Validate an agent-as-tool specification."""
        if not tool.agent_yaml_path:
            raise ValueError(
                f"Tool {tool.name} has agent_as_tool=True but no agent_yaml_path specified"
            )

        # Check if YAML file exists
        import os

        if not os.path.exists(tool.agent_yaml_path):
            # Attempt to resolve the path relative to the declarative_experiment
            # root directory.  This allows YAML specs to reference sibling files
            # with shorter paths such as `examples/...`.
            fallback_path = (
                pathlib.Path(__file__).resolve().parent.parent / tool.agent_yaml_path
            )
            if fallback_path.exists():
                tool.agent_yaml_path = str(fallback_path)
            else:
                raise ValueError(f"Agent YAML file not found: {tool.agent_yaml_path}")

        # Validate the YAML file can be loaded
        try:
            with open(tool.agent_yaml_path, "r") as f:
                data = yaml.safe_load(f)
            if "agent" not in data:
                raise ValueError(
                    f"Agent YAML file {tool.agent_yaml_path} must contain 'agent' section"
                )
        except Exception as e:
            raise ValueError(
                f"Error loading agent YAML file {tool.agent_yaml_path}: {e}"
            )

    @staticmethod
    def _create_agent_tool_function(tool: ToolSpecification) -> Callable:
        """Create a function that runs an agent as a tool."""

        async def agent_tool_function(input: str = "") -> str:
            """Dynamically created agent tool function."""
            # Get current context from thread-local storage
            current_context = get_current_context()

            # Use input source handler to resolve input
            resolved_input = InputSourceHandler.resolve_input(
                tool, input, current_context
            )
            return await run_agent_as_tool(
                tool.agent_yaml_path, resolved_input, current_context
            )

        # Set function name and docstring
        agent_tool_function.__name__ = tool.name
        agent_tool_function.__doc__ = (
            tool.description or f"Agent tool that runs {tool.agent_yaml_path}"
        )

        return agent_tool_function

    @staticmethod
    def _import_function_from_string(function_path: str):
        """Import a function dynamically from a string like 'module.function_name'."""
        module_path, function_name = function_path.rsplit(".", 1)
        module = importlib.import_module(module_path)
        
        # Access function from module namespace
        module_dict = module.__dict__
        if function_name not in module_dict:
            raise AttributeError(f"Module '{module_path}' has no attribute '{function_name}'")
        return module_dict[function_name]
