initial_outline_generator_test_suite = [
    {
        "id": "outline_gen_1",
        "prompt": '{"research_topic": "The impact of artificial intelligence on healthcare delivery in the United States", "gathered_knowledge": [{"content": "AI applications in healthcare include diagnostic imaging, drug discovery, electronic health records, telemedicine, and predictive analytics. Key findings show improved diagnostic accuracy, reduced costs, and enhanced patient outcomes. Challenges include data privacy, regulatory compliance, and workforce displacement."}]}',
    },
    {
        "id": "outline_gen_2",
        "prompt": '{"research_topic": "The economic effects of renewable energy adoption in Germany", "gathered_knowledge": [{"content": "Germany\'s renewable energy transition (Energiewende) has created jobs in solar and wind sectors, reduced energy imports, and increased energy costs for consumers. The policy has driven technological innovation and positioned Germany as a leader in clean energy exports. However, grid stability and industrial competitiveness remain challenges."}]}',
    },
    {
        "id": "outline_gen_3",
        "prompt": '{"research_topic": "The psychological impacts of social media on adolescent mental health", "gathered_knowledge": [{"content": "Research shows correlations between excessive social media use and increased rates of anxiety, depression, and sleep disorders among teenagers. Platform design features like infinite scroll and push notifications contribute to addictive behaviors. Positive aspects include social connection and access to mental health resources."}]}',
    },
    {
        "id": "outline_gen_4",
        "prompt": '{"research_topic": "The evolution of cybersecurity threats in the banking sector", "gathered_knowledge": [{"content": "Banking cybersecurity has evolved from basic password protection to multi-factor authentication, AI-powered fraud detection, and blockchain security. Common threats include phishing, ransomware, and insider attacks. Financial institutions invest heavily in security infrastructure and regulatory compliance."}]}',
    },
    {
        "id": "outline_gen_5",
        "prompt": '{"research_topic": "The effectiveness of remote work policies on employee productivity", "gathered_knowledge": [{"content": "Studies show mixed results on remote work productivity, with some reporting 13-50% increases and others noting decreased collaboration and innovation. Factors affecting success include management practices, technology infrastructure, and employee characteristics. Hybrid models are emerging as popular compromises."}]}',
    },
    {
        "id": "outline_gen_6",
        "prompt": '{"research_topic": "The impact of climate change on global food security", "gathered_knowledge": [{"content": "Climate change affects food production through changing precipitation patterns, extreme weather events, and rising temperatures. Vulnerable regions include sub-Saharan Africa and South Asia. Adaptation strategies include drought-resistant crops, improved irrigation, and diversified farming systems. Food prices and availability are increasingly affected."}]}',
    },
    {
        "id": "outline_gen_7",
        "prompt": '{"research_topic": "The role of blockchain technology in supply chain management", "gathered_knowledge": [{"content": "Blockchain provides transparency, traceability, and immutable records in supply chains. Benefits include reduced fraud, improved food safety, and enhanced sustainability tracking. Challenges include scalability, energy consumption, and integration with existing systems. Major companies like Walmart and Maersk have implemented blockchain solutions."}]}',
    },
    {
        "id": "outline_gen_8",
        "prompt": '{"research_topic": "The development of autonomous vehicles and their impact on transportation", "gathered_knowledge": [{"content": "Autonomous vehicle technology ranges from Level 1 (driver assistance) to Level 5 (full automation). Current deployments focus on specific use cases like highway driving and ride-sharing. Impacts include potential reduction in traffic accidents, changes in urban planning, and job displacement for drivers. Regulatory frameworks are still evolving."}]}',
    },
    {
        "id": "outline_gen_9",
        "prompt": '{"research_topic": "The effectiveness of mindfulness meditation in treating anxiety disorders", "gathered_knowledge": [{"content": "Clinical studies show mindfulness-based interventions reduce anxiety symptoms by 20-30% on average. Mechanisms include improved emotional regulation, reduced rumination, and enhanced present-moment awareness. Mindfulness-Based Stress Reduction (MBSR) and Mindfulness-Based Cognitive Therapy (MBCT) are evidence-based approaches."}]}',
    },
    {
        "id": "outline_gen_10",
        "prompt": '{"research_topic": "The influence of social media algorithms on political polarization", "gathered_knowledge": [{"content": "Social media algorithms create echo chambers by showing users content similar to their past interactions. This can reinforce existing beliefs and reduce exposure to diverse viewpoints. Research indicates increased political polarization correlates with social media usage. Some platforms have implemented measures to promote diverse content."}]}',
    },
]

initial_outline_generator_criteria = """
**1. JSON Structure**: The output must be a valid JSON object with exactly two keys: 'state_name' and 'outline'.

**2. State Name**: The 'state_name' field must be exactly "ready_for_critique".

**3. Outline Count**: The 'outline' list must contain between 3 and 8 sections.

**4. Section Quality**: Each section must be:
   - A clear, descriptive title that relates to the research topic
   - Specific enough to guide content development
   - Different from other sections (no redundancy)
   - Appropriate for a comprehensive research report

**5. Logical Structure**: The outline must demonstrate logical flow:
   - Should typically start with an introduction or background section
   - Include substantive sections covering main findings/themes
   - Should typically end with a conclusion or summary section
   - Sections should build upon each other logically

**6. Comprehensiveness**: The outline must adequately cover the research topic:
   - Address the main aspects mentioned in the gathered knowledge
   - Provide sufficient breadth to cover the topic comprehensively
   - Not miss obvious major themes from the research data

**7. Professionalism**: Section titles must be professional and appropriate for an academic or business report format.
"""
