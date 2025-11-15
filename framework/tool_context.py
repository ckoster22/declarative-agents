"""
Async-safe context storage for tool execution.

Replaces thread-local storage with contextvars so that each asyncio Task
propagates its own agent execution context correctly.
"""

from __future__ import annotations

from contextvars import ContextVar
from typing import Optional

from framework.context import AgentContext

# Use empty context as default instead of None to avoid needless None checks
_empty_context = AgentContext()
_current_context: ContextVar[AgentContext] = ContextVar("_current_context", default=_empty_context)


def set_current_context(context: Optional[AgentContext]) -> None:
    """Set the current context for tool execution for this task."""
    _current_context.set(context if context is not None else _empty_context)


def get_current_context() -> AgentContext:
    """Get the current context for tool execution for this task."""
    return _current_context.get()
