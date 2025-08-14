# Declarative Agent Framework

A framework for creating and orchestrating AI agents through YAML configuration files, enabling complex multi-agent workflows with structured output and multiple communication patterns.

## Features

- **Declarative Agent Configuration**: Define agents entirely through YAML files
- **Structured Output**: Automatic JSON schema validation and parsing
- **Multiple Communication Patterns**: Support for different ways agents can communicate
- **Orchestrator Agents**: Agents that coordinate other agents using tools
- **Declarative Tool Specification**: Define tools in YAML with automatic validation
- **Fail-Fast Validation**: All configuration is validated at startup time

## Quick Start

### Simple Agent

Create an agent YAML file:

```yaml
# yamls/hello_world.yaml
agent:
  name: "MyAgent"
  prompt: "You are a helpful assistant."

model:
  name: "qwen3-30b-a3b@q8_0"
  temperature: 0.7
  max_tokens: 1000

output_schema:
  type: "object"
  properties:
    response:
      type: "string"
      description: "The response to the user"
    confidence:
      type: "number"
      description: "Confidence score from 0-1"
```

Run it:

```bash
python -m framework.cli examples/basic_examples/hello_world.yaml "Hello, how are you?"
```

Environment setup:

- Set `OPENAI_BASE_URL` and `OPENAI_API_KEY` as needed. Defaults target LM Studio at `http://localhost:1234/v1`.
  - Example (LM Studio): `OPENAI_BASE_URL=http://localhost:1234/v1` and any dummy `OPENAI_API_KEY`.
  - Example (OpenAI): `OPENAI_BASE_URL=https://api.openai.com/v1` and a real `OPENAI_API_KEY`.

### Agent with Tools

Define tools declaratively in YAML:

```yaml
# yamls/orchestrator_agent_declarative_tools.yaml
agent:
  name: "OrchestratorAgent"
  prompt: |
    You are an orchestrator agent. Use your tools to coordinate other agents.
    
    WORKFLOW:
    1. call_description_agent(topic)
    2. format_story_input(description_result)
    3. call_story_agent(formatted_input)

model:
  name: "qwen3-30b-a3b@q8_0"
  temperature: 0.1

tools:
  - name: "call_description_agent"
    function: "orchestrator_tools.call_description_agent"
    description: "Call the description agent with a topic"
  - name: "call_story_agent"
    function: "orchestrator_tools.call_story_agent"
    description: "Call the story agent with formatted input"
  - name: "format_story_input"
    function: "orchestrator_tools.format_story_input"
    description: "Format description output for story agent input"
```

## Configuration Reference

### Agent Configuration

```yaml
agent:
  name: "AgentName"              # Required: Agent identifier
  prompt: "System instructions"   # Required: Agent's system prompt

model:                           # Optional: Model configuration
  name: "qwen3-30b-a3b@q8_0"    # Model name
  temperature: 0.7               # Temperature (0.0-1.0)
  top_p: 0.95                   # Top-p sampling
  max_tokens: 1000              # Maximum tokens

output_schema:                   # Optional: Structured output schema
  type: "object"
  properties:
    field_name:
      type: "string"
      description: "Field description"

input_schema:                    # Optional: Input context requirements
  required_context:
    - "previous_agent_name"

tools:                           # Optional: Tool specifications
  - name: "tool_name"
    function: "module.function_name"
    description: "Tool description"
```

### Tool Specification

Tools are defined declaratively in YAML and validated at startup:

```yaml
tools:
  - name: "my_tool"                          # Tool name
    function: "my_module.my_function"        # Python function path
    description: "What this tool does"       # Optional description

  - name: "call_other_agent"                 # Agent-as-tool
    agent_as_tool: true
    agent_yaml_path: "examples/path/to/other_agent.yaml"
    input_template: "{input}"                 # Formats input to the agent
```

**Key Benefits:**
- **Startup Validation**: All tools are validated when loading the YAML
- **Fail-Fast**: Invalid tools cause immediate failure, not runtime errors
- **Startup Tool Validation**: Tools are validated during load to reduce runtime errors
- **Explicit Dependencies**: Tool functions must exist at startup time

### Example Tool Functions

```python
# orchestrator_tools.py
async def call_description_agent(topic: str) -> str:
    """Call the description agent with a topic."""
    from framework.declarative_agents import AgentLoader
    spec = AgentLoader.load_from_file("examples/structured_examples/workflows/description_agent.yaml")
    result = await spec.run(topic)
    return json.dumps(result)

async def format_story_input(description_json: str) -> str:
    """Format description output for story agent."""
    data = json.loads(description_json)
    return f"Write a story about: {data['description']}. Main character: {data['mainCharacterName']}"
```

## Communication Patterns

### 1. Sequential Text Mode
Simple text-based communication between agents:

```yaml
workflow:
  name: "Sequential Workflow"
  initial_input: "artificial intelligence"
  communication_mode: "chat_history"
  agents:
    - name: "description_step"
      agent_file: "examples/structured_examples/workflows/description_agent.yaml"
    - name: "story_step"
      agent_file: "examples/structured_examples/workflows/story_agent.yaml"
      input_from: "description_step"
```

### 2. Context Injection Mode
Structured data sharing with full JSON context:

```yaml
workflow:
  name: "Context Workflow"
  initial_input: "artificial intelligence"
  communication_mode: "context"
  agents:
    - name: "context_description_step"
      agent_file: "examples/structured_examples/workflows/context_description_agent.yaml"
    - name: "context_story_step"
      agent_file: "examples/structured_examples/workflows/context_story_agent.yaml"
      input_from: "context_description_step"
```

### 3. Declarative Orchestrator
Agents that coordinate other agents using tools:

```yaml
# The orchestrator agent uses tools to call other agents
agent:
  name: "OrchestratorAgent"
  prompt: |
    You coordinate other agents using tools.
    Call call_description_agent, then format_story_input, then call_story_agent.

tools:
  - name: "call_description_agent"
    function: "orchestrator_tools.call_description_agent"
  - name: "call_story_agent"
    function: "orchestrator_tools.call_story_agent"
  - name: "format_story_input"
    function: "orchestrator_tools.format_story_input"
```

## Validation and Error Handling

The framework emphasizes fail-fast validation and clear errors:

### Startup Validation
- **Required Fields**: All required YAML fields are validated
- **Tool Imports**: All tool functions must be importable
- **Schema Validation**: Output schemas are validated for correctness

### Runtime Behavior
- **Clear Exceptions**: Meaningful exceptions are raised on misconfiguration
- **Guaranteed Imports (post-validate)**: Tools are validated at startup to reduce runtime surprises
- **Explicit Failures**: Invalid configuration causes immediate startup failure

### Example Error Messages

```bash
# Missing required field
ValueError: Agent section must contain 'name' field

# Invalid tool function
ModuleNotFoundError: No module named 'nonexistent_module'

# Missing tool field
ValueError: Tool 'my_tool' missing required 'function' field
```



## Architecture

The framework is built around these key principles:

1. **Declarative Configuration**: Everything is specified in YAML
2. **Startup Validation**: All errors are caught at startup time
3. **Type Safety**: Strong typing with union types for valid states
4. **Clear Errors**: Defensive checks with explicit exceptions
5. **Fail-Fast**: Invalid configuration causes immediate failure

This approach ensures that if the agent loads successfully, it will run without configuration-related errors. 