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
        # Fast-path: if the template is the default or only references {input}
        template = tool.input_template or "{input}"

        # Pattern matches placeholders like {input}, {AgentA}, {AgentA.output}, {AgentA.some.nested.key}
        # It intentionally requires the first character after '{' to be a letter or underscore
        # so that JSON braces (e.g., { "key": ... }) are not treated as placeholders.
        placeholder_pattern = re.compile(r"\{([A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z0-9_]+)*)\}")

        def _lookup_placeholder(path: str) -> str:
            # Built-in {input}
            if path == "input":
                return base_input

            if not context or not context.agent_outputs:
                # No context available; leave placeholder unchanged
                return "{" + path + "}"

            # Support top-level agent name and optional nested keys via dot notation
            parts = path.split(".")
            agent_name = parts[0]
            if agent_name not in context.agent_outputs:
                return "{" + path + "}"

            value: object = context.agent_outputs.get(agent_name)

            # Interpret a special segment name 'output' as an alias to the agent's full output.
            # For dict outputs, 'output' simply returns the entire dict.
            # For string outputs, it's identical to the raw string.
            # Any additional segments beyond 'output' are resolved as dict keys if possible.
            start_index = 1
            if len(parts) >= 2 and parts[1] == "output":
                start_index = 2

            # Resolve remaining path segments into nested dicts
            for segment in parts[start_index:]:
                if isinstance(value, dict) and segment in value:
                    value = value[segment]
                else:
                    return "{" + path + "}"

            # Final serialization: always JSON-encode so templates can form valid JSON safely
            try:
                return json.dumps(value, ensure_ascii=False)
            except Exception:
                return str(value)
        # Replace all placeholders
        def _replacer(match: re.Match[str]) -> str:
            keypath = match.group(1)
            try:
                return _lookup_placeholder(keypath)
            except Exception:
                # Defensive: in case any unexpected error occurs, keep the original token
                return match.group(0)

        return placeholder_pattern.sub(_replacer, template)
