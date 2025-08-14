# Agent-as-Tool Example

This example demonstrates the fundamental **agent-as-tool** pattern, where one agent calls another agent as a tool.

## Architecture

```
MathOrchestratorAgent
└── CalculatorAgent (called as tool)
```

## Files

- `math_orchestrator_agent.yaml` - Main orchestrator that coordinates the workflow
- `calculator_agent.yaml` - Specialized agent that performs calculations
- `README.md` - This documentation

## Key Concepts Demonstrated

1. **Agent-as-Tool Pattern**: Using `agent_as_tool: true` to call other agents
2. **Tool Specification**: Defining tools with YAML paths and input templates
3. **Structured Output**: Calculator agent uses JSON schema for reliable output
4. **Simple Orchestration**: Basic workflow coordination

## Usage

Run the orchestrator with a math problem:

```bash
python -m framework.cli run examples/basic_examples/agent_as_tool/math_orchestrator_agent.yaml "What is 15 * 23 + 7?"
```

## Expected Behavior

1. Orchestrator receives the math problem
2. Orchestrator calls calculator agent with the expression "15 * 23 + 7"
3. Calculator agent returns structured JSON with result
4. Orchestrator presents the result in user-friendly format

## Framework Capabilities Used

- `agent_as_tool: true` - Core agent composition pattern
- `agent_yaml_path` - Loading agents from YAML files
- `input_template` - Parameter passing between agents
- `type: "structured_output"` - Reliable JSON output
- `output_schema` - Output validation and structure 