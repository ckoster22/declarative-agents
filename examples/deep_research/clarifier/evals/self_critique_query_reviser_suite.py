self_critique_query_reviser_test_suite = [
    {
        "id": "revise_climate_change",
        # The agent expects its input as a *single* string, so we embed the JSON payload
        # directly in the prompt field.
        "prompt": (
            '{"original_topic": "Impact of climate change on agriculture", '
            '"clarifying_questions_asked": ['
            '"Are you interested in a specific region?", '
            '"Do you want to focus on a specific time frame?"], '
            '"user_clarification_answer": '
            '"Yes, I\'d like to focus on Southeast Asia between 2020 and 2050."}'
        ),
        # Keywords that **must** appear in the agent\'s final_revised_query.
        "expected_keywords": ["Southeast Asia", "2020", "2050"],
    },
    {
        "id": "revise_remote_work",
        "prompt": (
            '{"original_topic": "Remote work policies and employee productivity", '
            '"clarifying_questions_asked": ['
            '"Which industry are you interested in?", '
            '"Do you want a particular time period?"], '
            '"user_clarification_answer": '
            '"The US tech sector for the year 2022."}'
        ),
        "expected_keywords": ["US tech sector", "2022"],
    },
    {
        "id": "revise_renewable_energy",
        "prompt": (
            '{"original_topic": "Renewable energy adoption in Germany", '
            '"clarifying_questions_asked": ['
            '"Which renewable technology are you most interested in?", '
            '"Do you want to focus on a particular period?"], '
            '"user_clarification_answer": '
            '"Please focus on solar power deployment from 2010 to 2025."}'
        ),
        "expected_keywords": ["Germany", "solar", "2010", "2025"],
    },
    {
        "id": "revise_ai_jobs",
        "prompt": (
            '{"original_topic": "Impact of AI on the job market", '
            '"clarifying_questions_asked": ['
            '"Are you examining a specific sector?", '
            '"Should we consider automation levels?"], '
            '"user_clarification_answer": '
            '"Yes. Focus on manufacturing jobs and the rise of automation over the last decade."}'
        ),
        "expected_keywords": ["manufacturing", "automation", "job market"],
    },
    {
        "id": "revise_vaccine_hesitancy",
        "prompt": (
            '{"original_topic": "Vaccine hesitancy trends", '
            '"clarifying_questions_asked": ['
            '"Which disease vaccine are we talking about?", '
            '"Do you want a specific demographic focus?"], '
            '"user_clarification_answer": '
            '"Investigate COVID-19 vaccine hesitancy among adults in the United States, especially the role of social media misinformation."}'
        ),
        "expected_keywords": [
            "COVID",
            "United States",
            "social media",
            "vaccine hesitancy",
        ],
    },
    {
        "id": "revise_urban_transport",
        "prompt": (
            '{"original_topic": "Urban transport innovations", '
            '"clarifying_questions_asked": ['
            '"Which city should we analyze?", '
            '"Are you interested in a specific technology?"], '
            '"user_clarification_answer": '
            '"Analyze smart-city public transport solutions implemented in London since 2015, with an emphasis on contactless payments."}'
        ),
        "expected_keywords": ["London", "smart city", "contactless payments", "2015"],
    },
    {
        "id": "revise_medieval_trade",
        "prompt": (
            '{"original_topic": "Medieval trade routes", '
            '"clarifying_questions_asked": ['
            '"Do you want European or Asian focus?", '
            '"Is there a specific century of interest?"], '
            '"user_clarification_answer": '
            '"Focus on the Silk Road trade network during the 13th century."}'
        ),
        "expected_keywords": ["Silk Road", "13th century", "trade"],
    },
    {
        "id": "revise_space_exploration",
        "prompt": (
            '{"original_topic": "Future of space exploration", '
            '"clarifying_questions_asked": ['
            '"Which celestial body or mission?", '
            '"Any specific timeframe?"], '
            '"user_clarification_answer": '
            '"Study planned Mars colonization initiatives leading up to the year 2030."}'
        ),
        "expected_keywords": ["Mars", "colonization", "2030"],
    },
    {
        "id": "revise_llm_advancements",
        "prompt": (
            '{"original_topic": "tell me about the latest advancements in LLMs within the past 30 days", '
            '"clarifying_questions_asked": ['
            '"Should the analysis focus on comparing specific models (e.g., Gemini vs. GPT-4.1) or provide a general overview of recent advancements?", '
            '"Do you want to highlight the impact of open-source model proliferation or emphasize cost reduction through distillation as key themes?", '
            '"Would you prefer a thematic breakdown (e.g., multimodal capabilities, reasoning improvements) or a comparative analysis of different LLMs?", '
            '"Should the report prioritize recent developments in multi-step reasoning or address broader trends like government initiatives and AI ethics?"], '
            '"user_clarification_answer": '
            '"1. no, I only want info on open weight models\nThe report should only be 3 sections long"}'
        ),
        "expected_keywords": ["open weight", "last 30 days"],
    },
    {
        "id": "revise_election_integrity",
        "prompt": (
            '{"original_topic": "Recently (June 2025) there have been potential breakthroughs into whether the 2024 US presidential election was rigged. I want you to be unbiased and look for the **facts** and not speculations. Imagine you are an investigative journalist and get to the bottom of this", '
            '"clarifying_questions_asked": ['
            "\"Do you want to focus on specific claims like Starlink or 'Stop the Steal'?\", "
            "\"Should the report compare foreign interference (Russia, China, Iran) with domestic misinformation (e.g., 'Stop the Steal')?\", "
            '"Would you prefer a comparative analysis of U.S. election integrity measures (e.g., CISA) versus historical precedents?", '
            '"Do you want to explore the role of cybersecurity agencies in countering disinformation?"], '
            '"user_clarification_answer": '
            '"1. I don\'t know. You decide. Follow the evidence and facts wherever it takes you.\n2. same answer\n3. no\n4. no"}'
        ),
        "expected_keywords": ["2024", "evidence", "facts"],
    },
    {
        "id": "revise_llm_benchmarks",
        "prompt": (
            '{"original_topic": "LLM benchmarks are extremely important that they are measuring the right thing, as too simplistic or narrow of a metric can be gamed and lead to models that maximize the metric but do not maximize the intent behind the metric. I want you to research the latest current and proposed LLM benchmarks that reliably track how \\"good\\" an LLM is. I want to know which metrics that, if gamed, means the LLMs are actually doing really well.", '
            '"clarifying_questions_asked": ['
            '"Do you want the report to prioritize benchmarks that emphasize real-world applicability over theoretical performance metrics?", '
            '"Should the analysis include comparisons between proposed metrics for fairness, diversity, or ethical considerations?", '
            '"Are you interested in exploring how recent advancements address the issue of metric gaming in LLM evaluations?", '
            '"Would you prefer focusing on specific aspects like coherence, creativity, or logical reasoning in benchmark selection?"], '
            '"user_clarification_answer": '
            '"1. yes\n2. no\n3. sure\n4. reasoning, coding, agentic use cases, deep thinking, writing"}'
        ),
        "expected_keywords": [
            "reasoning",
            "coding",
            "agentic",
            "deep thinking",
            "writing",
        ],
    },
    {
        "id": "revise_composting_guide",
        "prompt": (
            '{"original_topic": "how to compost at home", '
            '"clarifying_questions_asked": ['
            '"Do you prefer a traditional composting method or vermicomposting (worm bin) approach?", '
            '"What format do you want the instructions to be presented in? (e.g., step-by-step guide, video, infographic)", '
            '"Are there specific materials or waste types you need to include in your compost pile?", '
            '"Do you need tips for maintaining a healthy composting system or troubleshooting common issues?"], '
            '"user_clarification_answer": '
            '"1. traditional\n2. step by step\n3. sawdust, food scraps\n4. yes"}'
        ),
        "expected_keywords": ["traditional", "step by step", "sawdust", "food scraps"],
    },
]

self_critique_query_reviser_criteria = [
    "The agent output is a JSON object containing exactly three keys: 'initial_draft_query', 'critique', and 'final_revised_query'.",
    "Each of 'initial_draft_query', 'critique', and 'final_revised_query' is a non-empty string.",
    "Ordinarily, 'final_revised_query' differs from 'initial_draft_query', reflecting improvements raised in the critique; if identical, the critique justifies why no change was necessary.",
    "The 'final_revised_query' accurately captures the substantive intent expressed in BOTH 'original_topic' and 'user_clarification_answer', incorporating all meaningful constraints without adding or omitting material information.",
    "The 'final_revised_query' is not unduly influenced by wording or suggestions in 'clarifying_questions_asked' that were not accepted or acknowledged by the user.",
    "Unanswered clarifying questions leave no trace in the 'final_revised_query'.",
    "The 'final_revised_query' is clear, unambiguous, and concise (ideally a single sentence).",
    "The 'final_revised_query' integrates all salient details from 'user_clarification_answer' so it is ready for research without further clarification.",
]
