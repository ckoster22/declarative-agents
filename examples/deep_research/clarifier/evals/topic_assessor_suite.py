topic_assessor_test_suite = [
    {"id": "vague_1", "prompt": "AI", "expected_assessment": "NEEDS_CLARIFICATION"},
    {
        "id": "vague_2",
        "prompt": "The future of technology",
        "expected_assessment": "NEEDS_CLARIFICATION",
    },
    {
        "id": "vague_3",
        "prompt": "Compare the performance of the GPT-4-Turbo and Llama 3 70B models on the MMLU benchmark. The analysis must focus on three specific metrics: overall accuracy score, performance in the STEM category, and performance in the humanities category.",
        "expected_assessment": "NEEDS_CLARIFICATION",
    },
    {
        "id": "vague_4",
        "prompt": "What were the primary causes of the 2008 financial crisis? The analysis must focus specifically on the roles of subprime mortgage-backed securities and credit default swaps in the collapse of Lehman Brothers, excluding broader factors.",
        "expected_assessment": "NEEDS_CLARIFICATION",
    },
    {
        "id": "vague_5",
        "prompt": "Create a summary of the key findings from the research paper 'Attention Is All You Need' by Vaswani et al. (2017). The summary must explain the Transformer architecture and the concept of self-attention.",
        "expected_assessment": "NEEDS_CLARIFICATION",
    },
    # --- Truly clear, verbose, and specific prompts that should NOT need clarification ---
    {
        "id": "clear_1",
        "prompt": "Generate a comparative analysis report on the architectural differences between Google's Transformer model (as described in 'Attention Is All You Need') and Meta's Llama 3 70B model. The report must be structured into three main sections: 1) A detailed breakdown of the self-attention mechanism in the original Transformer, including multi-head attention and positional encodings. 2) An analysis of the architectural modifications in Llama 3, specifically focusing on Grouped Query Attention (GQA), Rotary Position Embeddings (RoPE), and the SwiGLU activation function. 3) A concluding section summarizing how these modifications in Llama 3 aim to improve computational efficiency and model performance for large-scale inference compared to the original Transformer design. The final output should be a markdown document of approximately 800-1000 words.",
        "expected_assessment": "NO_CLARIFICATION_NEEDED",
    },
    {
        "id": "clear_2",
        "prompt": "Create a detailed case study on the collapse of Lehman Brothers during the 2008 financial crisis. The analysis must be limited to the period from January 1, 2008, to September 15, 2008. The study should investigate three specific factors: 1) The role of their holdings in subprime mortgage-backed securities, quantifying the notional value and rating of these assets as of Q2 2008. 2) The impact of their exposure to credit default swaps (CDS) as both a seller and buyer of protection. 3) An examination of the firm's failed attempts to secure capital from either the U.S. government or private buyers (like Barclays and Bank of America) in the final week before bankruptcy. The report should not discuss the broader market contagion or the subsequent government bailouts of other institutions.",
        "expected_assessment": "NO_CLARIFICATION_NEEDED",
    },
    {
        "id": "clear_3",
        "prompt": "Analyze the theme of 'the corrupting influence of power' in George Orwell's 'Animal Farm'. The analysis must be structured as follows: First, trace the character arc of Napoleon, identifying three key events that mark his transition from a revolutionary leader to a dictator. Second, compare and contrast the Seven Commandments at the beginning of the revolution with their final, altered state. Third, discuss how the character of Squealer is used as a propaganda tool to maintain Napoleon's power, providing two specific examples of his rhetorical techniques. The final essay should be 500-600 words.",
        "expected_assessment": "NO_CLARIFICATION_NEEDED",
    },
    {
        "id": "clear_4",
        "prompt": "Provide a technical explanation of the CRISPR-Cas9 gene-editing system. The explanation must be written for an undergraduate audience with a basic understanding of molecular biology. It needs to cover: 1) The function of the Cas9 protein as a nuclease. 2) The role of the guide RNA (gRNA) in targeting a specific DNA sequence. 3) The process of DNA cleavage and the two primary cellular repair mechanisms that follow: Non-Homologous End Joining (NHEJ) and Homology Directed Repair (HDR). The explanation should conclude by describing how HDR can be exploited to insert a new DNA sequence at the target site.",
        "expected_assessment": "NO_CLARIFICATION_NEEDED",
    },
    {
        "id": "clear_5",
        "prompt": "Conduct a market analysis of the global electric vehicle (EV) battery market for the 2023 calendar year. The report must be structured to compare the market share, technology, and strategic partnerships of the top three manufacturers by gigawatt-hour (GWh) production volume: CATL, BYD, and LG Energy Solution. For each manufacturer, the analysis must detail: 1) Total GWh produced in 2023. 2) Their primary battery chemistries (e.g., LFP vs. NMC). 3) Their key automotive clients. The report should conclude with a summary table comparing these three metrics for the specified companies.",
        "expected_assessment": "NO_CLARIFICATION_NEEDED",
    },
]

topic_assessor_criteria = """
**Assessment Accuracy**: The 'assessment' field in the JSON output must exactly match the `expected_assessment` from the test case details.
"""
