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

simple_greeting_criteria = [
    "The greeting includes the exact name provided in the prompt.",
    "Tone appropriateness: formal titles (Dr., Mr., Ms., Professor) receive formal greetings; first names receive informal, friendly greetings.",
    "Length: the greeting is 1–2 sentences.",
    "Friendliness: the greeting is welcoming and positive.",
    "No extra content: no explanations, markdown, or any text beyond the greeting.",
    "Keyword presence: contains expected keywords based on the test case.",
] 