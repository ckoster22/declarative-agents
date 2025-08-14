"""
Async-safe context storage for tool execution.

Replaces thread-local storage with contextvars so that each asyncio Task
propagates its own agent execution context correctly.
"""

from __future__ import annotations

from contextvars import ContextVar
from typing import Optional

from framework.context import AgentContext


_current_context: ContextVar[Optional[AgentContext]] = ContextVar(
    "_current_context", default=None
)


def set_current_context(context: Optional[AgentContext]) -> None:
    """Set the current context for tool execution for this task."""
    _current_context.set(context)


def get_current_context() -> Optional[AgentContext]:
    """Get the current context for tool execution for this task."""
    return _current_context.get()


