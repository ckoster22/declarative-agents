"""
Utility functions for the declarative agent framework.

This module provides common utilities used across the framework,
including think tag removal for cleaner agent outputs.
"""

import json
import re
from typing import Optional, Union, cast, overload


def remove_think_tags(text: str) -> str:
    if not text:
        return text

    # Remove <think>...</think> blocks (case-insensitive, multiline)
    think_pattern = re.compile(r"<think>.*?</think>", re.DOTALL | re.IGNORECASE)
    cleaned_text = re.sub(think_pattern, "", text)

    # Remove any stray opening/closing think tags that may remain
    cleaned_text = re.sub(r"</?think>", "", cleaned_text, flags=re.IGNORECASE)

    # Clean up excessive whitespace but preserve single spaces
    cleaned_text = re.sub(r"\n\s*\n", "\n\n", cleaned_text)  # Normalize multiple line breaks
    cleaned_text = re.sub(r" +", " ", cleaned_text)  # Normalize multiple spaces to single spaces
    cleaned_text = cleaned_text.replace("\\n", " ")  # Remove escaped newlines

    return cleaned_text.strip()


def _is_str(value: object) -> bool:
    """Type guard: check if value is a string."""
    return hasattr(value, "strip") and hasattr(value, "lower") and not hasattr(value, "keys")


def _is_dict(value: object) -> bool:
    """Type guard: check if value is a dict."""
    return hasattr(value, "keys") and hasattr(value, "__getitem__") and hasattr(value, "items")


@overload
def clean_agent_output(output: str) -> str: ...


@overload
def clean_agent_output(output: dict) -> dict: ...


def clean_agent_output(output: Union[str, dict]) -> Union[str, dict]:
    """Clean agent output by removing think tags from string values."""
    if _is_str(output):
        return remove_think_tags(cast(str, output))
    elif _is_dict(output):
        cleaned_output: dict = {}
        output_dict = cast(dict, output)
        for key, value in output_dict.items():
            if _is_str(value):
                cleaned_output[key] = remove_think_tags(cast(str, value))
            else:
                cleaned_output[key] = value
        return cleaned_output
    else:
        return output


def is_think_tag_token(token: str) -> bool:
    if not token:
        return False

    token_lower = token.lower()
    return "<think>" in token_lower or "</think>" in token_lower


def extract_text_delta_from_event(event: object) -> Optional[str]:
    """Extract a textual delta from a streaming event without using exceptions for control flow.

    This function handles multiple possible event shapes produced by different SDKs:
    - Direct string delta on the event (event.delta)
    - Data payload that is a plain string (possibly OpenAI-like SSE line)
    - Structured data object with a delta attribute (event.data.delta)

    Args:
        event: The streaming event object

    Returns:
        The extracted text delta string, or None if no text delta could be extracted
    """
    # Case 1: Direct string delta on the event
    ev_delta = getattr(event, "delta", None)
    if ev_delta is not None and _is_str(ev_delta):
        return cast(str, ev_delta)

    # Case 2: Event carries a data payload
    data_obj = getattr(event, "data", None)

    # Case 2a: data is a plain string, possibly OpenAI-like SSE line
    if data_obj is not None and _is_str(data_obj):
        data_str = cast(str, data_obj)
        if data_str:
            s = data_str.strip()
            if s.startswith("data:"):
                s = s[5:].strip()
            if s and s != "[DONE]":
                # Attempt JSON parse; if it fails, fall back to regex extraction
                try:
                    obj = json.loads(s)
                    text: Optional[str] = None
                    for choice in obj.get("choices", []):
                        content = choice.get("delta", {}).get("content") or choice.get("message", {}).get("content")
                        if content is not None and _is_str(content):
                            content_str = cast(str, content)
                            if content_str:
                                text = (text or "") + content_str
                    return text
                except Exception:
                    m = re.search(r'"content"\s*:\s*"(.*?)"', s)
                    return m.group(1) if m else None
        return None

    # Case 3: data has a delta attribute
    if data_obj is not None:
        data_delta = getattr(data_obj, "delta", None)
        if data_delta is not None and _is_str(data_delta):
            return cast(str, data_delta)

    return None


class ThinkTagFilter:
    def __init__(self):
        self.inside_think_tag = False
        self.buffer = ""

    def filter_token(self, token: str) -> str:
        if not token:
            return token

        self.buffer += token

        if self.inside_think_tag:
            if "</think>" in self.buffer.lower():
                end_think_pos = self.buffer.lower().find("</think>")
                remaining = self.buffer[end_think_pos + 8 :].lstrip()
                self.buffer = ""
                self.inside_think_tag = False
                if remaining:
                    return self.filter_token(remaining)
                else:
                    return ""
            else:
                self.buffer = ""
                return ""

        if "<think>" in self.buffer.lower():
            think_pos = self.buffer.lower().find("<think>")
            before_think = self.buffer[:think_pos].rstrip()
            self.buffer = self.buffer[think_pos + 7 :]
            self.inside_think_tag = True
            return before_think

        result = self.buffer
        self.buffer = ""
        return result

    def reset(self):
        self.inside_think_tag = False
        self.buffer = ""
