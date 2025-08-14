# Basic Examples Collection

This collection provides **small, focused examples** that demonstrate individual framework capabilities in isolation. These examples serve as building blocks for understanding and creating more complex agent systems.

## Examples Overview

| Example | Purpose | Complexity | Key Capability |
|---------|---------|------------|----------------|
| [Agent-as-Tool](./agent_as_tool/) | Foundation pattern | Very Low | Agent composition |
| [Structured Output](./structured_output/) | Output validation | Low | JSON schema validation |
| [Context Passing](./context_passing/) | Data flow | Low | Agent communication |
| [State Machine](./state_machine/) | Workflow orchestration | Low | State transitions |
| [Tool Integration](./tool_integration/) | Custom tools | Low | Python function integration |
| [Reflection Loop](./reflection_loop/) | Iterative behavior | Medium | Question generation |
| [Evaluation](./evaluation/) | Quality assurance | Low | Test suites |
| [Input Schema](./input_schema/) | Input validation | Low | Input requirements |

## Learning Path

### 1. Start Here: Agent-as-Tool
**File**: `agent_as_tool/math_orchestrator_agent.yaml`
- **What it shows**: How one agent calls another as a tool
- **Key concept**: `agent_as_tool: true`
- **Why start here**: Foundation for all multi-agent systems

### 2. Structured Output
**File**: `structured_output/contact_form_agent.yaml`
- **What it shows**: JSON schema validation and error handling
- **Key concept**: `type: "structured_output"`
- **Why important**: Ensures reliable data exchange

### 3. Context Passing
**File**: `context_passing/context_orchestrator_agent.yaml`
- **What it shows**: How agents pass structured data between each other
- **Key concept**: JSON data flow between agents
- **Why important**: Essential for complex workflows

### 4. State Machine
**File**: `state_machine/order_processor_agent.yaml`
- **What it shows**: Simple workflow with state transitions
- **Key concept**: State-based decision making
- **Why important**: Foundation for complex workflows

### 5. Tool Integration
**File**: `tool_integration/tool_agent.yaml`
- **What it shows**: Custom Python functions as tools
- **Key concept**: `function` import paths
- **Why important**: Extends agent capabilities

### 6. Reflection Loop
**File**: `reflection_loop/reflection_orchestrator_agent.yaml`
- **What it shows**: Iterative question generation and analysis
- **Key concept**: Dynamic iteration based on completeness
- **Why important**: Adaptive, intelligent behavior

### 7. Evaluation
**File**: `evaluation/evaluation_agent.yaml`
- **What it shows**: Test suites for agent validation
- **Key concept**: Systematic quality assurance
- **Why important**: Ensures reliable agent behavior

### 8. Input Schema
**File**: `input_schema/input_validation_agent.yaml`
- **What it shows**: Input validation and requirements
- **Key concept**: `input_schema` definition
- **Why important**: Prevents errors and improves UX

## Quick Start

### Prerequisites
- Python 3.8+
- Framework dependencies installed
- Access to LLM models (qwen3-1.7b, qwen3-coder-30b)

### Running Examples

1. **Agent-as-Tool**:
   ```bash
   python3 -m framework.cli examples/basic_examples/agent_as_tool/math_orchestrator_agent.yaml "What is 15 * 23 + 7?"
   ```

2. **Structured Output**:
   ```bash
   python3 -m framework.cli examples/basic_examples/structured_output/contact_form_agent.yaml "Name: John Doe, Email: john@example.com, Phone: (555) 123-4567, Message: Hello, I would like to inquire about your services."
   ```

3. **Context Passing**:
   ```bash
   python3 -m framework.cli examples/basic_examples/context_passing/context_orchestrator_agent.yaml "The company reported 15% revenue growth in Q3, with strong performance in the technology sector."
   ```

4. **State Machine**:
   ```bash
   python3 -m framework.cli examples/basic_examples/state_machine/order_processor_agent.yaml "Order: 2 laptops at $999 each, Customer: John Doe, Email: john@example.com, Address: 123 Main St, Payment: Credit Card"
   ```

5. **Tool Integration**:
   ```bash
   python3 -m framework.cli examples/basic_examples/tool_integration/tool_agent.yaml "What's the weather in Tokyo?"
   ```

6. **Reflection Loop**:
   ```bash
   python3 -m framework.cli examples/basic_examples/reflection_loop/reflection_orchestrator_agent.yaml "I want to start a business."
   ```

7. **Evaluation**:
   ```bash
   python3 -m framework.cli examples/basic_examples/evaluation/evaluation_agent.yaml "Dr. Johnson"
   ```

8. **Input Schema**:
   ```bash
   python3 -m framework.cli examples/basic_examples/input_schema/input_validation_agent.yaml "Topic: Artificial Intelligence, Time Period: present, Output Format: summary"
   ```

## Framework Capabilities Demonstrated

### Core Patterns
- **Agent-as-Tool**: `agent_as_tool: true`, `agent_yaml_path`
- **Structured Output**: `type: "structured_output"`, `output_schema`
- **Tool Integration**: `function` import paths
- **Input Validation**: `input_schema`, `properties`, `enum`

### Data Types
- **Strings**: Basic text fields
- **Numbers**: Integer and float values
- **Booleans**: True/false flags
- **Arrays**: Lists of values
- **Objects**: Nested data structures
- **Enums**: Constrained value sets

### Workflow Patterns
- **Sequential**: Step-by-step execution
- **State Machine**: State-based transitions
- **Iterative**: Loop until completion
- **Conditional**: Decision-based branching

## Building Complex Systems

These examples can be combined to create more sophisticated systems:

1. **Start with Agent-as-Tool** for basic composition
2. **Add Structured Output** for reliable data exchange
3. **Use Context Passing** for multi-step workflows
4. **Implement State Machine** for complex orchestration
5. **Integrate Custom Tools** for specialized functionality
6. **Add Reflection Loops** for adaptive behavior
7. **Include Evaluation** for quality assurance
8. **Use Input Schemas** for validation

## Best Practices

### Agent Design
- **Single Responsibility**: Each agent has one clear purpose
- **Clear Interfaces**: Well-defined input/output schemas
- **Error Handling**: Graceful degradation for failures
- **Documentation**: Clear prompts and descriptions

### Workflow Design
- **Modularity**: Break complex tasks into smaller agents
- **Reusability**: Design agents for multiple use cases
- **Testability**: Create evaluation suites for validation
- **Maintainability**: Clear separation of concerns

### Tool Integration
- **Function Signatures**: Clear parameter names and types
- **Return Formats**: Consistent JSON output
- **Error Handling**: Graceful failure modes
- **Documentation**: Comprehensive docstrings

## Next Steps

After mastering these examples:

1. **Explore the deep_research example** to see how these patterns combine
2. **Create your own agents** using these patterns as templates
3. **Build evaluation suites** for your agents
4. **Experiment with different models** and configurations
5. **Contribute new examples** to the community

## Troubleshooting

### Common Issues
- **Import Errors**: Ensure Python paths are correct
- **Model Access**: Verify model availability and credentials
- **Schema Validation**: Check JSON structure matches schemas
- **Tool Integration**: Verify function import paths

### Getting Help
- Check individual example README files for specific guidance
- Review framework documentation for detailed explanations
- Examine the deep_research example for advanced patterns
- Create issues for bugs or request features

## Contributing

We welcome contributions to expand this collection:

1. **New Examples**: Create examples for missing capabilities
2. **Improvements**: Enhance existing examples with better patterns
3. **Documentation**: Improve README files and comments
4. **Tests**: Add evaluation suites for examples

Each example should:
- Demonstrate a single, clear capability
- Be small and focused
- Include comprehensive documentation
- Have clear usage examples
- Follow framework best practices
