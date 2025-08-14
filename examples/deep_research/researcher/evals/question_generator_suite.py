question_generator_test_suite = [
    {
        "id": "gen_q_1",
        "prompt": "The economic impact of renewable energy adoption in Germany.",
    },
    {
        "id": "gen_q_2",
        "prompt": "The psychological effects of social media on adolescents.",
    },
    {
        "id": "gen_q_3",
        "prompt": "The history and evolution of the CRISPR-Cas9 gene-editing technology.",
    },
    {
        "id": "gen_q_4",
        "prompt": "A comparative analysis of urban planning strategies in Singapore and Tokyo.",
    },
    {
        "id": "gen_q_5",
        "prompt": "The role of artificial intelligence in diagnosing diseases from medical imaging.",
    },
    {
        "id": "gen_q_6",
        "prompt": "The causes and consequences of the decline of bee populations worldwide.",
    },
    {
        "id": "gen_q_7",
        "prompt": "The influence of ancient Roman architecture on modern building design.",
    },
    {
        "id": "gen_q_8",
        "prompt": "An analysis of supply chain vulnerabilities exposed by the COVID-19 pandemic.",
    },
    {
        "id": "gen_q_9",
        "prompt": "The effectiveness of various carbon capture technologies in mitigating climate change.",
    },
    {
        "id": "gen_q_10",
        "prompt": "The cultural significance of the Silk Road in connecting Eastern and Western civilizations.",
    },
]

question_generator_criteria = """
**1. JSON Structure**: The output must be a valid JSON object with exactly one key 'questions' containing a list of strings.
**2. Question Count**: The 'questions' list must contain exactly 3 questions.
**3. Question Quality**: Each question must be:
   - Relevant to the research topic provided in the prompt
   - Clear and specific enough to guide focused research
   - Different from each other to ensure comprehensive coverage
   - Phrased as answerable research questions that would help gather information about the topic
**4. No Extra Fields**: The JSON output should contain only the 'questions' field, no other fields like 'state_name' or metadata.
"""
