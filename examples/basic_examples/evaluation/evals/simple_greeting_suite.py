simple_greeting_test_suite = [
    {
        "id": "formal_title",
        "prompt": "Dr. Johnson",
        "expected_keywords": ["Dr. Johnson", "pleasure", "acquaintance", "Good day"],
    },
    {
        "id": "informal_name",
        "prompt": "Alice",
        "expected_keywords": ["Alice", "Hello", "Hi", "great", "welcome"],
    },
    {
        "id": "mr_title",
        "prompt": "Mr. Williams",
        "expected_keywords": ["Mr. Williams", "pleasure", "Good day", "acquaintance"],
    },
    {
        "id": "ms_title",
        "prompt": "Ms. Davis",
        "expected_keywords": ["Ms. Davis", "pleasure", "Good day", "acquaintance"],
    },
    {
        "id": "simple_name",
        "prompt": "Bob",
        "expected_keywords": ["Bob", "Hello", "Hi", "great", "welcome"],
    },
    {
        "id": "professor_title",
        "prompt": "Professor Brown",
        "expected_keywords": ["Professor Brown", "pleasure", "Good day", "acquaintance"],
    },
]

simple_greeting_criteria = """
**1. Name Inclusion**: The greeting must include the exact name provided in the prompt.
**2. Tone Appropriateness**: 
    - Formal titles (Dr., Mr., Ms., Professor) should receive formal greetings
    - First names should receive informal, friendly greetings
**3. Length**: Greeting should be 1-2 sentences (not too short, not too long).
**4. Friendliness**: Greeting should be welcoming and positive.
**5. No Extra Content**: Should not include explanations, markdown, or extra text beyond the greeting.
**6. Keyword Presence**: Must contain expected keywords based on the test case.

If **any** rule above is violated, the test fails.
""" 