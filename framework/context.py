"""
Context management for the declarative agent framework.

This module handles the context that flows between agents in workflows,
allowing agents to access outputs from previous agents in the chain.
"""

import json
from typing import Dict, Union, Optional
from pydantic import BaseModel, Field

from framework.types import InputSchema

# Type alias for agent output
AgentOutput = Union[Dict[str, Union[str, int, float, bool]], str]


class AgentContext(BaseModel):
    """Context object that stores outputs from previous agents."""

    agent_outputs: Dict[str, AgentOutput] = Field(default_factory=dict)

    def add_output(self, agent_name: str, output: AgentOutput) -> None:
        self.agent_outputs[agent_name] = output

    def get_output(self, agent_name: str) -> Optional[AgentOutput]:
        return self.agent_outputs.get(agent_name)

    def has_output(self, agent_name: str) -> bool:
        return agent_name in self.agent_outputs


class ContextFormatter:
    """Formats context data for agent consumption."""

    @staticmethod
    def format_output_for_chat_history(output: AgentOutput, agent_name: str) -> str:
        if isinstance(output, dict):
            formatted_parts = [f"Output from {agent_name}:"]
            for key, value in output.items():
                formatted_parts.append(f"  {key}: {value}")
            return "\n".join(formatted_parts)
        else:
            return f"Output from {agent_name}: {output}"

    @staticmethod
    def prepare_context_input(
        context: AgentContext, input_schema: InputSchema, agent_name: str
    ) -> str:
        if not context.agent_outputs:
            return ""

        context_parts = [f"Available context for {agent_name}:"]

        if input_schema.required_context:
            for required_agent in input_schema.required_context:
                if context.has_output(required_agent):
                    output = context.get_output(required_agent)
                    context_parts.append(f"\nFrom {required_agent}:")
                    if isinstance(output, dict):
                        context_parts.append(json.dumps(output, indent=2))
                    else:
                        context_parts.append(str(output))
        else:
            for agent_name, output in context.agent_outputs.items():
                context_parts.append(f"\nFrom {agent_name}:")
                if isinstance(output, dict):
                    context_parts.append(json.dumps(output, indent=2))
                else:
                    context_parts.append(str(output))

        return "\n".join(context_parts)
