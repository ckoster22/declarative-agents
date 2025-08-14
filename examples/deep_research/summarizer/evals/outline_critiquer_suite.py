outline_critiquer_test_suite = [
    {
        "id": "critique_weak_outline_1",
        "prompt": '{"research_topic": "The impact of artificial intelligence on healthcare delivery in the United States", "initial_outline": ["AI", "Healthcare", "Benefits", "Problems", "End"], "gathered_knowledge": [{"content": "AI applications in healthcare include diagnostic imaging, drug discovery, electronic health records, telemedicine, and predictive analytics. Key findings show improved diagnostic accuracy, reduced costs, and enhanced patient outcomes. Challenges include data privacy, regulatory compliance, and workforce displacement. Major implementations include IBM Watson, Google DeepMind, and various FDA-approved AI diagnostic tools."}]}',
    },
    {
        "id": "critique_good_outline_1",
        "prompt": '{"research_topic": "The economic effects of renewable energy adoption in Germany", "initial_outline": ["Introduction to Germany\'s Renewable Energy Transition", "Economic Benefits: Job Creation and Export Growth", "Economic Challenges: Energy Costs and Grid Stability", "Impact on Industrial Competitiveness", "Conclusion and Future Outlook"], "gathered_knowledge": [{"content": "Germany\'s renewable energy transition (Energiewende) has created jobs in solar and wind sectors, reduced energy imports, and increased energy costs for consumers. The policy has driven technological innovation and positioned Germany as a leader in clean energy exports. However, grid stability and industrial competitiveness remain challenges."}]}',
    },
    {
        "id": "critique_redundant_outline_1",
        "prompt": '{"research_topic": "The psychological impacts of social media on adolescent mental health", "initial_outline": ["Social Media and Mental Health", "Effects on Teenagers", "Psychological Impacts", "Mental Health Issues", "Social Media Problems", "Teen Psychology"], "gathered_knowledge": [{"content": "Research shows correlations between excessive social media use and increased rates of anxiety, depression, and sleep disorders among teenagers. Platform design features like infinite scroll and push notifications contribute to addictive behaviors. Positive aspects include social connection and access to mental health resources."}]}',
    },
    {
        "id": "critique_missing_sections_1",
        "prompt": '{"research_topic": "The evolution of cybersecurity threats in the banking sector", "initial_outline": ["Introduction", "Common Threats", "Conclusion"], "gathered_knowledge": [{"content": "Banking cybersecurity has evolved from basic password protection to multi-factor authentication, AI-powered fraud detection, and blockchain security. Common threats include phishing, ransomware, and insider attacks. Financial institutions invest heavily in security infrastructure and regulatory compliance. Historical evolution shows progression from physical security to digital threats."}]}',
    },
    {
        "id": "critique_user_specified_structure_1",
        "prompt": '{"research_topic": "The effectiveness of remote work policies on employee productivity", "user_requirement": "Please structure this as a three-section report focusing on productivity metrics, challenges, and recommendations.", "initial_outline": ["Introduction", "Benefits of Remote Work", "Productivity Studies", "Management Challenges", "Technology Infrastructure", "Employee Characteristics", "Hybrid Models", "Conclusion"], "gathered_knowledge": [{"content": "Studies show mixed results on remote work productivity, with some reporting 13-50% increases and others noting decreased collaboration and innovation. Factors affecting success include management practices, technology infrastructure, and employee characteristics. Hybrid models are emerging as popular compromises."}]}',
    },
    {
        "id": "critique_comprehensive_outline_1",
        "prompt": '{"research_topic": "The impact of climate change on global food security", "initial_outline": ["Climate Change Overview", "Effects on Agricultural Production", "Regional Vulnerabilities", "Adaptation Strategies", "Economic and Social Impacts", "Policy Recommendations", "Conclusion"], "gathered_knowledge": [{"content": "Climate change affects food production through changing precipitation patterns, extreme weather events, and rising temperatures. Vulnerable regions include sub-Saharan Africa and South Asia. Adaptation strategies include drought-resistant crops, improved irrigation, and diversified farming systems. Food prices and availability are increasingly affected."}]}',
    },
    {
        "id": "critique_technical_outline_1",
        "prompt": '{"research_topic": "The role of blockchain technology in supply chain management", "initial_outline": ["Blockchain Technology", "Supply Chain Applications", "Benefits and Challenges", "Implementation Examples"], "gathered_knowledge": [{"content": "Blockchain provides transparency, traceability, and immutable records in supply chains. Benefits include reduced fraud, improved food safety, and enhanced sustainability tracking. Challenges include scalability, energy consumption, and integration with existing systems. Major companies like Walmart and Maersk have implemented blockchain solutions."}]}',
    },
    {
        "id": "critique_empty_outline_1",
        "prompt": '{"research_topic": "The development of autonomous vehicles and their impact on transportation", "initial_outline": [], "gathered_knowledge": [{"content": "Autonomous vehicle technology ranges from Level 1 (driver assistance) to Level 5 (full automation). Current deployments focus on specific use cases like highway driving and ride-sharing. Impacts include potential reduction in traffic accidents, changes in urban planning, and job displacement for drivers. Regulatory frameworks are still evolving."}]}',
    },
    {
        "id": "critique_medical_outline_1",
        "prompt": '{"research_topic": "The effectiveness of mindfulness meditation in treating anxiety disorders", "initial_outline": ["Introduction to Mindfulness", "Research on Anxiety Treatment", "Clinical Applications", "Mechanisms of Action", "Limitations and Considerations", "Conclusion"], "gathered_knowledge": [{"content": "Clinical studies show mindfulness-based interventions reduce anxiety symptoms by 20-30% on average. Mechanisms include improved emotional regulation, reduced rumination, and enhanced present-moment awareness. Mindfulness-Based Stress Reduction (MBSR) and Mindfulness-Based Cognitive Therapy (MBCT) are evidence-based approaches."}]}',
    },
    {
        "id": "critique_social_media_outline_1",
        "prompt": '{"research_topic": "The influence of social media algorithms on political polarization", "initial_outline": ["Social Media Basics", "Algorithm Functionality", "Political Effects", "Echo Chambers", "Polarization Trends", "Platform Responses", "Future Implications"], "gathered_knowledge": [{"content": "Social media algorithms create echo chambers by showing users content similar to their past interactions. This can reinforce existing beliefs and reduce exposure to diverse viewpoints. Research indicates increased political polarization correlates with social media usage. Some platforms have implemented measures to promote diverse content."}]}',
    },
]

outline_critiquer_criteria = """
**1. JSON Structure**: The output must be a valid JSON object with exactly two keys: 'state_name' and 'revised_outline'.

**2. State Name**: The 'state_name' field must be exactly "ready_for_expansion".

**3. Section Count**: The 'revised_outline' list must contain between 3 and 8 sections.

**4. Improvement Over Initial**: The revised outline must show clear improvement over the initial outline:
   - Eliminate redundancy (merge similar sections)
   - Fix unclear or vague section titles
   - Add missing sections that are important for the topic
   - Improve logical flow and structure

**5. User Requirement Adherence**: If the user has specified structural requirements (e.g., "three-section report"), the revised outline MUST honor those requirements exactly.

**6. Comprehensive Coverage**: The outline must adequately address all major themes present in the gathered knowledge:
   - No significant aspects from the research should be missing
   - All main findings should be addressable within the outline structure

**7. Logical Flow**: The revised outline must demonstrate clear logical progression:
   - Sections should build upon each other
   - Introduction → main content → conclusion structure when appropriate
   - No illogical ordering of sections

**8. Professional Quality**: Section titles must be:
   - Clear and descriptive
   - Professional and appropriate for academic/business reports
   - Specific enough to guide content development
   - Free of redundancy or overlap

**9. Handling Edge Cases**: The agent must handle special cases appropriately:
   - Empty initial outlines should result in a complete new outline
   - Severely flawed outlines should be substantially restructured
   - Good outlines should receive minor improvements or be kept largely intact
"""
