poem_agent_test_suite = [
    {
        "id": "nature_poem",
        "prompt": "Write a poem about the beauty of nature",
    },
]

poem_agent_criteria = """
**1. Line Count**: The poem must be exactly 50 lines long. Count each line break as one line, excluding empty lines or any `<think>` tags or lines.

**2. Poem Structure**: The output must be a poem, not prose or other text formats. This means:
   - It should have poetic elements such as rhythm, meter, or free verse structure
   - It should use poetic language with imagery, metaphors, or other literary devices
   - It should not be written as paragraphs or continuous prose
   - It should have clear line breaks that create poetic structure

If **any** of these criteria are violated, the test fails.
"""
