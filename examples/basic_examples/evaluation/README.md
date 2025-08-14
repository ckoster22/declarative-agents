# Evaluation Example

This example demonstrates how to create **evaluation suites** for agents to ensure quality and reliability.

## Purpose

Shows how to:
- Create test suites for agent evaluation
- Define clear evaluation criteria
- Test agents against multiple scenarios
- Ensure consistent agent behavior
- Validate agent outputs

## Architecture

```
Evaluation Framework
├── SimpleGreetingAgent (agent being evaluated)
├── SimpleGreetingEvaluationAgent (evaluation orchestrator)
└── simple_greeting_suite.py (test cases and criteria)
```

## Files

- `simple_agent.yaml` - Agent being evaluated (greeting generator)
- `evaluation_agent.yaml` - Agent that performs evaluations
- `evals/simple_greeting_suite.py` - Test suite with test cases and criteria
- `README.md` - This documentation

## Key Concepts Demonstrated

1. **Test Suite Structure**: Organized test cases with expected outcomes
2. **Evaluation Criteria**: Clear, measurable criteria for success
3. **Keyword Validation**: Checking for expected content in outputs
4. **Scenario Coverage**: Testing different input types and edge cases
5. **Quality Assurance**: Systematic validation of agent behavior

## Test Cases

The evaluation suite includes:

### Formal Titles
- **Dr. Johnson**: Tests formal greeting with academic title
- **Mr. Williams**: Tests formal greeting with honorific
- **Ms. Davis**: Tests formal greeting with honorific
- **Professor Brown**: Tests formal greeting with academic title

### Informal Names
- **Alice**: Tests informal, friendly greeting
- **Bob**: Tests simple name handling

## Evaluation Criteria

1. **Name Inclusion**: Must include exact name from prompt
2. **Tone Appropriateness**: Formal for titles, informal for first names
3. **Length**: 1-2 sentences (appropriate length)
4. **Friendliness**: Welcoming and positive tone
5. **No Extra Content**: Clean output without explanations
6. **Keyword Presence**: Must contain expected keywords

## Usage

Run individual test:
```bash
python -m framework.cli run examples/basic_examples/evaluation/evaluation_agent.yaml "Dr. Johnson"
```

Run full evaluation suite:
```bash
python -m framework.cli eval examples/basic_examples/evaluation/evaluation_agent.yaml
```

## Expected Behavior

1. **Test Execution**: Evaluation agent calls greeting agent with test input
2. **Output Analysis**: Evaluates greeting against criteria
3. **Result Reporting**: Provides pass/fail status with reasoning
4. **Coverage**: Tests multiple scenarios and edge cases

## Framework Capabilities Used

- `agent_as_tool: true` - Agent composition for evaluation
- Test suite structure with test cases
- Evaluation criteria definition
- Keyword validation
- Systematic testing approach

## Benefits

- **Quality Assurance**: Ensures consistent agent behavior
- **Regression Testing**: Catches issues when agents are modified
- **Documentation**: Test cases serve as usage examples
- **Confidence**: Validates agent reliability before deployment

## Evaluation Best Practices

1. **Clear Criteria**: Define measurable, objective criteria
2. **Comprehensive Coverage**: Test various input types and edge cases
3. **Keyword Validation**: Check for expected content and tone
4. **Consistent Structure**: Use standardized test case format
5. **Maintainable**: Keep test suites updated with agent changes

## Extending the Example

- Add more test cases for edge cases
- Include negative test cases (invalid inputs)
- Add performance criteria (response time)
- Create evaluation suites for other agent types 