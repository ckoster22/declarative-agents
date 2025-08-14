"""
Tools for the structured output orchestrator agent to call other structured output agents.
"""

import json


from framework import AgentLoader


async def call_structured_description_agent(topic: str) -> str:
    """
    Call the structured description agent with a topic and return the structured result as JSON.

    Args:
        topic: The topic to generate a description for

    Returns:
        JSON string containing the structured description output
    """
    # Load and run the structured description agent
    agent_spec = AgentLoader.load_from_file("examples/structured_examples/workflows/structured_description_agent.yaml")
    result = await agent_spec.run(topic)

    # The result should already be structured due to the StructuredOutputAgent
    if isinstance(result, dict):
        return json.dumps(result)
    else:
        return json.dumps(
            {"error": "Failed to get structured output", "raw_result": str(result)}
        )


async def call_structured_story_agent(description_json: str) -> str:
    """
    Call the structured story agent with formatted input and return the structured result as JSON.

    Args:
        description_json: JSON string containing description data from the description agent

    Returns:
        JSON string containing the structured story output
    """
    # Parse the description JSON to create a formatted input
    try:
        description_data = json.loads(description_json)

        # Format the input for the story agent
        formatted_input = f"""Based on the following details, write a story:

Description: {description_data.get('description', 'No description provided')}
Main Character: {description_data.get('mainCharacterName', 'Unknown')}
Theme: {description_data.get('theme', 'General')}
Setting: {description_data.get('setting', 'Unspecified')}

Please create a compelling story that incorporates all these elements."""

        # Load and run the structured story agent
        agent_spec = AgentLoader.load_from_file("examples/structured_examples/workflows/structured_story_agent.yaml")
        result = await agent_spec.run(formatted_input)

        # The result should already be structured due to the StructuredOutputAgent
        if isinstance(result, dict):
            return json.dumps(result)
        else:
            return json.dumps(
                {"error": "Failed to get structured output", "raw_result": str(result)}
            )

    except json.JSONDecodeError:
        return json.dumps({"error": "Invalid JSON input", "input": description_json})
    except Exception as e:
        return json.dumps({"error": str(e), "input": description_json})


def format_final_output(description_json: str, story_json: str) -> str:
    """
    Format the final output by combining results from both agents.

    Args:
        description_json: JSON string from description agent
        story_json: JSON string from story agent

    Returns:
        JSON string containing the combined, formatted output
    """
    try:
        description_data = json.loads(description_json)
        story_data = json.loads(story_json)

        combined_output = {
            "character_info": {
                "name": description_data.get("mainCharacterName", "Unknown"),
                "description": description_data.get("description", "No description"),
                "theme": description_data.get("theme", "General"),
                "setting": description_data.get("setting", "Unspecified"),
            },
            "story_info": {
                "outline": story_data.get("outline", "No outline provided"),
                "story": story_data.get("story", "No story provided"),
                "word_count": story_data.get("wordCount", 0),
                "genre": story_data.get("genre", "Unknown"),
                "mood": story_data.get("mood", "Neutral"),
            },
            "summary": f"Created a {story_data.get('genre', 'story')} story about {description_data.get('mainCharacterName', 'a character')} with approximately {story_data.get('wordCount', 0)} words.",
        }

        return json.dumps(combined_output, indent=2)

    except json.JSONDecodeError as e:
        return json.dumps(
            {
                "error": f"JSON decode error: {str(e)}",
                "description_json": description_json,
                "story_json": story_json,
            }
        )
    except Exception as e:
        return json.dumps(
            {
                "error": str(e),
                "description_json": description_json,
                "story_json": story_json,
            }
        )
