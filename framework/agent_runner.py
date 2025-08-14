from __future__ import annotations

from typing import Optional

from framework.declarative_agents import AgentLoader, AgentType
from framework.tools import register_run_agent_as_tool
from framework.utils import remove_think_tags
from framework.context import AgentContext


async def run_agent_as_tool(yaml_path: str, input_data: str, context: Optional[AgentContext] = None) -> str:
    """Load and run an agent from a YAML file as a tool.

    Returns a plain string with think tags removed.
    """
    agent_spec = AgentLoader.load_from_file(yaml_path)
    result = await agent_spec.run(input_data, context=context, agent_type=AgentType.TOOL)
    return remove_think_tags(str(result))


# Register callback at import time (top-level import; no lazy behavior)
register_run_agent_as_tool(run_agent_as_tool)


