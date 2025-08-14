import json

# Import the GPT-4o search helper located in the same examples package.
from .gpt4o_search_tool import GPT4OSearchTool
from datetime import datetime, timezone

# def get_current_topic_tool():
#     """Gets the current research topic from context. Returns None if no topic is set."""
#     # Mock implementation - in reality this would check session/context
#     return json.dumps({
#         "state_name": "needs_topic",
#         "topic": None
#     })


def user_input_tool(prompt_message: str):
    user_input = input(prompt_message + " ").strip()
    return json.dumps({"user_input": user_input})


# -----------------------------------------------------------------------------
# GPT-4o powered web-search tool
# -----------------------------------------------------------------------------


async def search_topic_context_tool(search_query: str) -> str:
    gpt4o_tool = GPT4OSearchTool(search_context_size="medium")
    search_summary, sources = await gpt4o_tool.search(search_query)

    payload = {
        "search_query": search_query,
        "search_summary": search_summary,
        "sources": sources,
    }

    return json.dumps(payload, ensure_ascii=False)


# -----------------------------------------------------------------------------
# Date & Time utility tool
# -----------------------------------------------------------------------------


def get_current_datetime_tool() -> str:
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    return json.dumps({"current_datetime": now})
