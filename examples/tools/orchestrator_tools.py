"""
Tools for the orchestrator agent to call other agents and manage workflows.
"""

import json
from framework.declarative_agents import AgentLoader


async def call_description_agent(topic: str) -> str:
    spec = AgentLoader.load_from_file(
        "examples/structured_examples/workflows/description_agent.yaml"
    )
    result = await spec.run(topic)
    if isinstance(result, dict):
        return json.dumps(result)
    return json.dumps({"description": str(result), "mainCharacterName": "Unknown"})


async def call_story_agent(formatted_input: str) -> str:
    spec = AgentLoader.load_from_file(
        "examples/structured_examples/workflows/story_agent.yaml"
    )
    result = await spec.run(formatted_input)
    if isinstance(result, dict):
        return json.dumps(result)
    return json.dumps({"outline": "Story outline", "story": str(result)})


def format_story_input(description_json: str) -> str:
    try:
        data = json.loads(description_json)
        description = data.get("description", "No description")
        character_name = data.get("mainCharacterName", "Unknown")
        return (
            "Write a story based on this description: {description}. "
            "Use this character name: {character_name}"
        ).format(description=description, character_name=character_name)
    except json.JSONDecodeError:
        return f"Write a story based on: {description_json}"
