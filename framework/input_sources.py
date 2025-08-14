"""
Input source handling for the declarative agent framework.

This module handles automatic input source resolution for agent tools,
including file contents and template formatting.
"""

from typing import Optional
from framework.types import ToolSpecification
from framework.context import AgentContext


class InputSourceHandler:
    """Handles different input sources for agent tools."""

    @staticmethod
    def resolve_input(
        tool: ToolSpecification,
        base_input: str = "",
        context: Optional[AgentContext] = None,
    ) -> str:
        return InputSourceHandler._get_template_input(tool, base_input, context)

    @staticmethod
    def _get_template_input(
        tool: ToolSpecification, base_input: str, context: Optional[AgentContext] = None
    ) -> str:
        return tool.input_template.format(input=base_input)
