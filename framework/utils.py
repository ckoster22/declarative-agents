"""
Utility functions for the declarative agent framework.

This module provides common utilities used across the framework,
including think tag removal for cleaner agent outputs.
"""

import re
from typing import Union


def remove_think_tags(text: str) -> str:
    if not text:
        return text

    # Remove <think>...</think> blocks (case-insensitive, multiline)
    think_pattern = re.compile(r"<think>.*?</think>", re.DOTALL | re.IGNORECASE)
    cleaned_text = re.sub(think_pattern, "", text)

    # Remove any stray opening/closing think tags that may remain
    cleaned_text = re.sub(r"</?think>", "", cleaned_text, flags=re.IGNORECASE)

    # Clean up excessive whitespace but preserve single spaces
    cleaned_text = re.sub(
        r"\n\s*\n", "\n\n", cleaned_text
    )  # Normalize multiple line breaks
    cleaned_text = re.sub(
        r" +", " ", cleaned_text
    )  # Normalize multiple spaces to single spaces
    cleaned_text = cleaned_text.replace("\\n", " ")  # Remove escaped newlines

    return cleaned_text.strip()


def clean_agent_output(output: Union[str, dict]) -> Union[str, dict]:
    if isinstance(output, str):
        return remove_think_tags(output)
    elif isinstance(output, dict):
        cleaned_output = {}
        for key, value in output.items():
            if isinstance(value, str):
                cleaned_output[key] = remove_think_tags(value)
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
