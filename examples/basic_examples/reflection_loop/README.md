# Simple Reflection Loop Example

This example demonstrates an **iterative reflection loop** where an agent analyzes information and generates follow-up questions until completeness is achieved.

## Purpose

Shows how to create agents that:
- Analyze information completeness
- Generate targeted follow-up questions
- Iterate until sufficient information is gathered
- Provide reasoning for decisions

## Architecture

```
ReflectionOrchestratorAgent
└── ReflectionAgent (analyzes and generates questions)
```

## Reflection Loop Flow

```
Initial Information → Reflection Analysis → Questions? → User Answers → Combined Info → Reflection Analysis → Complete?
    ↓                                                                                                    ↑
    └────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Files

- `reflection_orchestrator_agent.yaml` - Main orchestrator that manages the reflection loop
- `reflection_agent.yaml` - Agent that analyzes information and generates questions
- `README.md` - This documentation

## Key Concepts Demonstrated

1. **Iterative Analysis**: Repeatedly analyze information until complete
2. **Question Generation**: Generate targeted follow-up questions
3. **Information Accumulation**: Combine original and new information
4. **Completion Detection**: Stop when no more questions are needed
5. **Reasoning Transparency**: Provide explanations for decisions

## Usage

Test with incomplete information:
```bash
python -m framework.cli run examples/basic_examples/reflection_loop/reflection_orchestrator_agent.yaml "I want to start a business."
```

Test with more complete information:
```bash
python -m framework.cli run examples/basic_examples/reflection_loop/reflection_orchestrator_agent.yaml "I want to start a tech consulting business in San Francisco, targeting small businesses, with $50k initial investment, and I have 5 years of software development experience."
```

## Expected Behavior

1. **Initial Analysis**: Reflection agent assesses information completeness
2. **Question Generation**: If incomplete, generates specific follow-up questions
3. **User Interaction**: Orchestrator presents questions and waits for answers
4. **Iteration**: Combines information and re-analyzes
5. **Completion**: Stops when information is deemed complete

## Reflection Agent Output

The reflection agent returns:
- **information_quality**: "complete", "incomplete", or "ambiguous"
- **reasoning**: Explanation of the assessment
- **follow_up_questions**: Array of questions (empty if complete)
- **confidence**: Confidence level in the assessment

## Framework Capabilities Used

- `agent_as_tool: true` - Agent composition
- `type: "structured_output"` - Reliable JSON output
- `output_schema` - Structured response validation
- `enum` - Constrained quality assessment values
- `array` - Dynamic question lists
- Iterative workflow logic

## Benefits

- **Adaptive**: Adjusts questions based on current information
- **Efficient**: Focuses on gaps rather than asking everything
- **Transparent**: Provides reasoning for decisions
- **Flexible**: Can handle various types of information gathering

## Use Cases

- **Requirements Gathering**: Software development requirements
- **Research Planning**: Academic or business research
- **Problem Diagnosis**: Technical or business problems
- **Goal Setting**: Personal or organizational planning
- **Interview Processes**: Structured information collection 