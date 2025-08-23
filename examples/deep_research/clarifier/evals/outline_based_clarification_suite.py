outline_based_clarification_test_suite = [
    {
        "id": "clarify_vague_1",
        "prompt": "AI",
    },
    {
        "id": "clarify_vague_2",
        "prompt": "The future of technology",
    },
    {
        "id": "clarify_vague_3",
        "prompt": "climate change effects",
    },
    {
        "id": "clarify_vague_4",
        "prompt": "Analyze the impact of remote work policies on employee productivity in the US tech sector during 2022.",
    },
    {
        "id": "clarify_vague_5",
        "prompt": "A report on the historical development of the Python programming language from 1991 to 2020.",
    },
    {
        "id": "clarify_vague_6",
        "prompt": "tell me how to care for and maintain end grain cutting boards",
    },
    {
        "id": "clarify_vague_7",
        "prompt": """Topic: The current date is June 29th, 2025. Will nebraska have a budget shortfall this year? How is nebraska doing economically?

Recent Search Context:
```
Nebraska has recently made significant strides in addressing its budgetary challenges and fostering economic growth.

**State Budget Developments**

In May 2025, Governor Jim Pillen signed the 2025-2027 biennial budget into law, effectively closing a projected $432 million shortfall. The budget emphasizes fiscal restraint and includes line-item vetoes to ensure balanced spending. Notable vetoes include reducing the Supreme Court’s budget increase to align with the University of Nebraska's rate, utilizing existing agency funds for Fire Marshal salary and health insurance increases, and cutting an $18 million appropriation for recreational upgrades at Lake McConaughy. ([governor.nebraska.gov](https://governor.nebraska.gov/governor-pillen-signs-budget-announces-line-item-vetos?utm_source=openai))

Earlier in February 2025, the Nebraska Economic Forecasting Advisory Board revised revenue projections, adding approximately $165 million in potential new revenue over the next two fiscal years. This adjustment, primarily due to anticipated increases in corporate tax collections, helped reduce the budget shortfall to just under $200 million. ([nebraskaexaminer.com](https://nebraskaexaminer.com/2025/02/28/new-nebraska-economic-forecast-spurs-cautious-optimism-shrinks-state-budget-shortfall/?utm_source=openai))

**Economic Developments**

The state's economy is experiencing cautious optimism. The Nebraska Business Forecast Council projects modest employment growth of 0.7% in 2025, with acceleration to 0.9% in 2026. Job growth is expected in the services industry, including business services, health care, and leisure and hospitality, as well as in construction and nondurable goods manufacturing. However, growth may be limited in retail, wholesale trade, durable goods manufacturing, and the public sector. ([news.unl.edu](https://news.unl.edu/article/nebraska-expected-to-see-fragile-growth-in-high-interest-economy?utm_source=openai))

Agriculture remains a strong pillar of Nebraska's economy. Farm income was about $8 billion in 2024, nearly a record, and is expected to stabilize around $7 billion in 2025 and 2026. This stability is attributed to strong crop and livestock prices and rising production, despite a projected decrease in crop insurance payments. ([news.unl.edu](https://news.unl.edu/article/nebraska-expected-to-see-fragile-growth-in-high-interest-economy?utm_source=openai))

**Major Infrastructure Projects**

Several significant infrastructure projects are underway, contributing to economic development:

- **Sustainable Beef Processing Plant**: In May 2025, a $400 million beef processing plant began operations in North Platte. The facility processes 1,500 head of cattle per day and is expected to employ 850 people by the end of 2025. Most of its products supply Walmart stores in the central U.S. ([en.wikipedia.org](https://en.wikipedia.org/wiki/Sustainable_Beef?utm_source=openai))

- **Mutual of Omaha Headquarters Tower**: Construction is progressing on a 44-story office skyscraper in downtown Omaha, set to be the tallest building in Nebraska upon completion in 2026. The tower will serve as the headquarters for Mutual of Omaha Insurance Company. ([en.wikipedia.org](https://en.wikipedia.org/wiki/Mutual_of_Omaha_Headquarters_Tower?utm_source=openai))

- **Eppley Airfield Upgrade**: A nearly $1 billion upgrade is planned for Omaha's Eppley Airfield, with completion expected by 2028. The project includes a new glass-domed entrance, expanded boarding gates, and additional amenities, aiming to accommodate increasing passenger traffic. ([apnews.com](https://apnews.com/article/309940e9e5037c810b014da4ab5e9d73?utm_source=openai))

These developments reflect Nebraska's commitment to fiscal responsibility and economic growth through strategic investments and infrastructure improvements.


## Nebraska's Economic and Infrastructure Updates:
- [Nearly $1 billion upgrade planned at the airport in Omaha, Nebraska](https://apnews.com/article/309940e9e5037c810b014da4ab5e9d73?utm_source=openai)
- [Nebraska Gov. Pillen reveals plan for education funding](https://apnews.com/article/17e8dfce2fc2580f13c9eb5f27baac69?utm_source=openai)
- [Nebraska GOP governor, lawmakers unveil tax-slashing plan](https://apnews.com/article/b54213714d294efbbd721058b054ed57?utm_source=openai) 
""",
    },
    {
        "id": "clarify_clear_1",
        "prompt": "Compare the performance of the GPT-4-Turbo and Llama 3 70B models on the MMLU benchmark. The analysis must focus on three specific metrics: overall accuracy score, performance in the STEM category, and performance in the humanities category.",
    },
    {
        "id": "clarify_clear_2",
        "prompt": "What were the primary causes of the 2008 financial crisis? The analysis must focus specifically on the roles of subprime mortgage-backed securities and credit default swaps in the collapse of Lehman Brothers, excluding broader factors.",
    },
    {
        "id": "clarify_clear_3",
        "prompt": "Create a summary of the key findings from the research paper 'Attention Is All You Need' by Vaswani et al. (2017). The summary must explain the Transformer architecture and the concept of self-attention.",
    },
    {
        "id": "clarify_clear_4",
        "prompt": "Analyze the use of the 'green light' as a symbol in F. Scott Fitzgerald's 'The Great Gatsby'. The analysis should discuss its representation of Gatsby's hopes for the future and its connection to Daisy Buchanan.",
    },
    {
        "id": "clarify_clear_5",
        "prompt": "Explain the mechanism of action for mRNA vaccines, specifically the BNT162b2 vaccine against SARS-CoV-2. The explanation must detail how the lipid nanoparticle delivers mRNA to host cells and the resulting immune response.",
    },
]

outline_based_clarification_criteria = [
    "The 'questions' list in the JSON output contains between 1 and 4 questions.",
    "For each question: it is relevant to the prompt and clearly phrased.",
    "For each question: it is a clarifying question (typically closed-ended; begins with phrases like 'Are you', 'Do you', 'Would you', 'Which of these', 'Should the focus be').",
    "Wh-questions ('What', 'How', 'Why', 'When', 'Where') are not allowed unless they clearly ask for user preferences or choices (e.g., 'What level of detail do you want?', 'Which specific aspects interest you most?', 'How technical should the explanation be?').",
    "Questions are useful for narrowing research scope and avoid redundancy across multiple questions.",
]
