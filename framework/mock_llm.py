"""
Mock AsyncOpenAI client for testing in environments without LLM servers.

This module provides a mock implementation that supports streaming responses
and can be toggled via the USE_MOCK_LLM environment variable.
"""

import asyncio
import json
import os
from typing import AsyncIterator, Dict, List, Optional, Union

from agents import AsyncOpenAI


class MockAsyncOpenAI(AsyncOpenAI):
    """Mock AsyncOpenAI client that supports streaming responses."""

    def __init__(self, base_url: str = "", api_key: str = ""):
        """Initialize the mock client."""
        super().__init__(base_url=base_url, api_key=api_key)
        self._response_config: Optional[str] = os.getenv("MOCK_LLM_RESPONSE", None)

    async def chat(
        self,
        messages: List[Dict[str, str]],
        model: str = "",
        stream: bool = False,
        **kwargs,
    ) -> Union[Dict, AsyncIterator]:
        """Mock chat completion that supports streaming."""
        response_text = self._get_mock_response(messages)

        if stream:
            return self._stream_response(response_text)
        else:
            return self._non_stream_response(response_text, model)

    def _get_mock_response(self, messages: List[Dict[str, str]]) -> str:
        """Get mock response text, optionally from environment variable."""
        if self._response_config:
            return self._response_config

        # Default mock response
        last_message = messages[-1].get("content", "") if messages else ""
        return f"Mock response to: {last_message[:50]}..."

    def _stream_response(self, text: str) -> AsyncIterator:
        """Yield streaming events in the format expected by the agents library."""

        async def _generate():
            # Simulate token-by-token streaming
            tokens = text.split()
            for i, token in enumerate(tokens):
                # Create event-like object with delta attribute
                event = type(
                    "MockEvent",
                    (),
                    {
                        "delta": token + (" " if i < len(tokens) - 1 else ""),
                        "data": None,
                    },
                )()
                yield event

        return _generate()

    def _non_stream_response(self, text: str, model: str) -> Dict:
        """Return a non-streaming response."""
        return {
            "choices": [
                {
                    "message": {"content": text, "role": "assistant"},
                    "finish_reason": "stop",
                }
            ],
            "model": model,
            "usage": {"prompt_tokens": 10, "completion_tokens": len(text.split()), "total_tokens": 10 + len(text.split())},
        }

    async def chat_completions_create(
        self,
        messages: List[Dict[str, str]],
        model: str = "",
        stream: bool = False,
        **kwargs,
    ) -> Union[Dict, AsyncIterator]:
        """Alias for chat method to match AsyncOpenAI interface."""
        return await self.chat(messages=messages, model=model, stream=stream, **kwargs)


def create_mock_client() -> MockAsyncOpenAI:
    """Create a mock AsyncOpenAI client instance."""
    return MockAsyncOpenAI(base_url="http://mock", api_key="mock_key")
