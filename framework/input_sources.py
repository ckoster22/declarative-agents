"""
Input source handling for the declarative agent framework.

This module handles automatic input source resolution for agent tools,
including file contents and template formatting.
"""

from typing import Optional
from framework.types import ToolSpecification
from framework.context import AgentContext
import json
import re


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
        template = tool.input_template or "{input}"

        # Pattern: {input}, {Agent}, {Agent.output}, {Agent.key.subkey}
        placeholder_pattern = re.compile(r"\{([A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z0-9_]+)*)\}")

        # Detect if the entire template is exactly one placeholder
        full_match = placeholder_pattern.fullmatch(template)
        single_placeholder_entire_template: bool = full_match is not None
        full_placeholder_path: str | None = full_match.group(1) if full_match else None

        def _resolve_object_for_path(path: str) -> object:
            if path == "input":
                return base_input
            if not context or not context.agent_outputs:
                return "{" + path + "}"
            parts = path.split(".")
            agent_name = parts[0]
            if agent_name not in context.agent_outputs:
                return "{" + path + "}"
            value: object = context.agent_outputs.get(agent_name)
            start_index = 1
            if len(parts) >= 2 and parts[1] == "output":
                start_index = 2
            for segment in parts[start_index:]:
                if isinstance(value, dict) and segment in value:
                    value = value[segment]
                else:
                    return "{" + path + "}"
            return value

        def _encode(value: object) -> str:
            try:
                return json.dumps(value, ensure_ascii=False)
            except Exception:
                return str(value)

        def _replacer(match: re.Match[str]) -> str:
            keypath = match.group(1)
            value_obj = _resolve_object_for_path(keypath)

            # If the whole template is exactly one placeholder and the resolved value is a plain string,
            # return the raw string (not JSON-quoted) so tools that expect plain text get it.
            if single_placeholder_entire_template and full_placeholder_path == keypath and isinstance(value_obj, str):
                return value_obj

            return _encode(value_obj)

        return placeholder_pattern.sub(_replacer, template)
