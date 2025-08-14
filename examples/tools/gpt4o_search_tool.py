import re
from openai import OpenAI
from typing import Tuple, List, TypedDict


class Source(TypedDict):
    title: str
    url: str


class GPT4OSearchTool:
    """Simple wrapper around the GPT-4o *search-preview* endpoint.

    The goal is to have a very small, dependency-free helper that returns
    the raw text produced by the model **plus** a list of sources (title & URL) so
    that downstream agents can cite or reference them.
    """

    def __init__(self, search_context_size: str = "low"):
        self.client = OpenAI()
        self.search_context_size = search_context_size

    # ---------------------------------------------------------------------
    # Private helpers
    # ---------------------------------------------------------------------
    def _extract_sources_from_content(self, content: str) -> List[Source]:
        """Fallback regex extraction for sources when tool_calls are absent."""
        # Regex to find markdown links: [text](url)
        matches = re.findall(r"\[([^\]]+)\]\(([^)]+)\)", content)

        sources: List[Source] = []
        seen_urls: set[str] = set()

        for title, url in matches:
            if url not in seen_urls:
                sources.append({"title": title, "url": url})
                seen_urls.add(url)

        return sources

    # ---------------------------------------------------------------------
    # Public API
    # ---------------------------------------------------------------------
    async def search(self, query: str) -> Tuple[str, List[Source]]:
        """Perform a web search using the GPT-4o *search-preview* model.

        Args:
            query: The search query.

        Returns:
            Tuple of `(content, sources)` where `content` is the raw assistant
            message text and `sources` is a list of `{title, url}` dicts.
        """
        completion = self.client.chat.completions.create(
            model="gpt-4o-search-preview",
            messages=[{"role": "user", "content": query}],
            web_search_options={"search_context_size": self.search_context_size},
        )

        content: str = completion.choices[0].message.content or ""
        sources: List[Source] = []

        # First, try to get sources from tool_calls (the "official" way)
        if completion.choices[0].message.tool_calls:
            for tool_call in completion.choices[0].message.tool_calls:
                if tool_call.type == "search_results" and tool_call.search_results:
                    for source in tool_call.search_results:
                        sources.append(source.model_dump(exclude_none=True))

        # If no sources extracted, fall back to regex extraction from the text.
        if not sources:
            sources = self._extract_sources_from_content(content)

        return content, sources
