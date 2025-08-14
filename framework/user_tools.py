"""
User interaction tools for the declarative agent framework.

This module provides tools for agents to interact with users,
including prompting for input and handling user responses.
"""

import json
import logging
from datetime import datetime, timezone

logger = logging.getLogger(__name__)


def user_input_tool(prompt_message: str) -> str:
    user_input = input(prompt_message + " ").strip()
    logger.debug("User input received: %s...", user_input[:50])
    return json.dumps({"user_input": user_input})


def get_current_datetime_tool() -> str:
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    logger.debug("Generated current datetime: %s", now)
    return json.dumps({"current_datetime": now})
