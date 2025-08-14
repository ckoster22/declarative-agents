# Local LLM Agentic Flows Guide

## Table of Contents
- [Troubleshooting](#troubleshooting)
- [Architecture Guidance](#architecture-guidance)
- [Declarative Agent Philosophy](#declarative-agent-philosophy)
- [Experimenter's Mindset](#experimenters-mindset)
- [Model Configuration](#model-configuration)

## Troubleshooting

### Token Output Issues
- **Problem**: Token output ends prematurely
- **Solution**: Check the `max_tokens` setting. Increase it or remove it entirely to allow for complete responses

### Tool Call Issues
- **Problem**: Tool calls aren't being made
- **Solution**: Verify the agent type and expectations. Structured-output agents run a two-step chain (thinker → formatter). Tools are available to the thinker step, not the formatter. If you need tool use, set the agent's `type` to `structured_output` only when you require validated JSON; otherwise use `agent`.

## Architecture Guidance

### Agentic Techniques

#### 1. Prompt Chaining
- **Definition**: Multiple sequential calls to LLMs where each call builds on the previous output
- **Use Cases**: 
  - Iteratively refining content quality
  - Consolidating information from multiple sources
  - Expanding brief outlines into detailed content
  - Breaking complex tasks into manageable steps
- **Benefits**: Allows for progressive improvement and complex multi-step reasoning
- **Implementation**: Use workflow specifications to chain agents together

#### 2. LLM as a Judge
- **Definition**: Using an LLM to evaluate outputs and inform subsequent decisions
- **Use Cases**:
  - Double-checking work for accuracy and completeness
  - Identifying course corrections early in the process
  - Quality assurance and validation
  - A/B testing between different approaches
- **Benefits**: Catches errors sooner and provides objective evaluation
- **Implementation**: Create specialized judge agents with clear evaluation criteria

#### 3. Reflection
- **Definition**: Periodically assessing progress and direction in long processes
- **Use Cases**:
  - Avoiding tunnel vision in complex tasks
  - Ensuring alignment with overall goals
  - Identifying when to pivot or adjust strategy
  - Maintaining awareness of the "big picture"
- **Benefits**: Prevents getting lost in details and keeps focus on objectives
- **Implementation**: Schedule reflection checkpoints in workflows or use dedicated reflection agents

#### 4. Problem Decomposition
- **Definition**: Breaking complex problems into smaller, more manageable sub-problems
- **When to Use**: When an LLM is struggling with a complex task despite prompt improvements
- **Strategy**:
  - Identify the core components of the problem
  - Create specialized agents for each sub-problem
  - Use an orchestrator to coordinate the solution assembly
  - Chain solutions together to build the final result
- **Benefits**: 
  - Improves reliability and consistency
  - Makes debugging easier (isolate failures to specific sub-problems)
  - Allows for specialized optimization of each component
  - Reduces cognitive load on individual agents
- **Implementation**: Design workflow specifications that break tasks into discrete steps with clear inputs/outputs

### Agent Design Principles

#### 1. Prefer Small, Focused Agents
- Create small agents with small prompts that do one thing really well
- Avoid overly complex prompts that try to do too much
- Each agent should have a single, clear responsibility

#### 2. Orchestrator Pattern
- Use an orchestrator agent that operates at a higher elevation (in terms of abstraction layers)
- The orchestrator delegates specialized tasks to specialized agents
- This creates a clear separation of concerns and better maintainability

#### 3. Agent Isolation
- Specialized agents shouldn't know about other specialized agents
- Think of them as agnostic microservices
- They do one thing well and it's up to the orchestrator to coordinate invocations

#### 4. Visual Communication
- Consider including simple mermaid diagrams in orchestrator prompts
- Mermaid syntax is a very concise and unambiguous way to communicate:
  - Tool calls
  - Ordering
  - Loops
  - Conditional flows

### Model Selection Strategy

#### Size vs. Performance Trade-offs
- Prefer smaller models (fewer parameters) over larger models
- Only move to larger models when the smaller model is giving diminishing returns on results
- Start with the smallest viable model and scale up as needed

### Development Approach

#### Iterative Design
- Approach agentic architecture iteratively and experimentally
- Start with one agent
- If you're not getting the desired results, create a simple orchestrator agent that invokes one or two specialist agents
- Don't overshoot the number of agents

#### Complexity Management
- Always take a step back and ask "Am I making this too complicated?"
- Prefer simplicity over complexity
- If a solution feels overly complex, it probably is

## Declarative Agent Philosophy

### Core Principles

The declarative agent framework (`@/framework`) is built around the principle that **configuration should be separate from implementation**. This philosophy enables rapid experimentation and iteration by treating agents as data rather than code.

#### 1. YAML-First Design
- Agent behavior is defined in YAML files, not Python code
- Prompts, model settings, tools, and output schemas are declarative
- Changes to agent behavior require no code modifications
- Version control becomes easier with human-readable configurations

#### 2. Framework Architecture
The framework provides several key abstractions:

- **AgentSpecification**: Loads and validates YAML definitions
- **StructuredOutputAgent**: Two-step thinking and formatting process
- **ToolLoader**: Dynamic tool integration with validation
- **WorkflowSpecification**: Multi-agent orchestration
- **EventBus**: Real-time token streaming and event handling

#### 3. Volatility-Based Decomposition
The framework follows a volatility-based architecture:
- **Low volatility**: Core types, enums, and base models
- **Medium volatility**: Agent specifications and tool integrations
- **High volatility**: Prompts, model configurations, and experiment parameters

This separation allows stable framework code to support rapidly changing experimental configurations.

#### 4. Streaming and Observability
- Real-time token streaming with think tag filtering
- Rich console output with live updates during execution
- Comprehensive logging for post-experiment analysis
- Event-driven architecture for extensibility

### Framework Workflow

1. **Load**: YAML files are parsed into `AgentDefinition` objects
2. **Validate**: Tools, schemas, and configurations are validated
3. **Execute**: Agents run with proper streaming and context handling
4. **Observe**: Real-time feedback and comprehensive logging
5. **Iterate**: Modify YAML and repeat

This workflow enables the rapid experimentation cycle that's essential for effective agentic AI development.

## Experimenter's Mindset

### Scientific Method Approach

Effective agentic AI development requires a systematic, scientific approach. Treat each experiment as a hypothesis test with clear methodology and documentation.

#### 1. Observe
- **Current State**: What is the agent currently doing?
- **Pain Points**: Where are the failures or inefficiencies?
- **Success Patterns**: What's working well?
- **Token Usage**: Monitor consumption and efficiency
- **Output Quality**: Assess relevance, accuracy, and completeness

#### 2. Hypothesize
- **Root Cause Analysis**: Why is the current behavior occurring?
- **Improvement Theories**: What changes might help?
- **Risk Assessment**: What could go wrong with proposed changes?
- **Success Criteria**: How will you measure improvement?

#### 3. Design Validation Experiments
- **A/B Testing**: Compare current vs. proposed configurations
- **Edge Case Testing**: Identify failure modes
- **Performance Metrics**: Define measurable success criteria
- **Control Groups**: Maintain baseline for comparison

#### 4. Experiment
- **Small Changes**: Make incremental modifications
- **Isolated Testing**: Test one variable at a time
- **Reproducible Setup**: Ensure experiments can be repeated
- **Documentation**: Record all parameters and conditions

#### 5. Record and Analyze
- **Detailed Notes**: Document observations, hypotheses, and results
- **Metrics Collection**: Track performance indicators
- **Failure Analysis**: Understand why experiments failed
- **Pattern Recognition**: Identify recurring issues or successes

#### 6. Iterate and Repeat
- **Learn from Failures**: Use negative results to refine hypotheses
- **Scale Successes**: Expand on what works
- **Continuous Improvement**: Never stop experimenting
- **Knowledge Accumulation**: Build a body of evidence

### Experimental Best Practices

#### Documentation Standards
- **Experiment Logs**: Date, hypothesis, changes, results
- **Configuration Snapshots**: Save YAML files for each experiment
- **Performance Metrics**: Token usage, response time, quality scores
- **Failure Cases**: Document what didn't work and why

#### Iteration Strategy
- **Start Simple**: Begin with minimal viable agents
- **Add Complexity Gradually**: Introduce features one at a time
- **Regression Testing**: Ensure new changes don't break existing functionality
- **Cross-Validation**: Test hypotheses across different scenarios

#### Knowledge Management
- **Pattern Library**: Document successful agent patterns
- **Anti-Patterns**: Record what doesn't work
- **Model Performance Database**: Track which models work best for which tasks
- **Tool Effectiveness**: Document which tools provide the most value

### Mindset Principles

1. **Embrace Failure**: Every failed experiment is valuable data
2. **Question Assumptions**: Regularly challenge your beliefs about what works
3. **Measure Everything**: Don't rely on intuition alone
4. **Share Knowledge**: Document and share findings with the community
5. **Stay Curious**: Always ask "what if?" and "why?"

## Model Configuration

#### Qwen3-1.7B
- **Model**: `qwen3-1.7b`
- **Temperature**: `0.6`
- **Top P**: `0.95`
- **Use Case**: Good starting point for most tasks, efficient for simple agents

#### Qwen3-30B-A3B
- **Model**: `qwen3-30b-a3b`
- **Temperature**: `0.6`
- **Top P**: `0.95`
- **Use Case**: Higher performance for complex reasoning tasks, use when smaller models show diminishing returns

### Configuration Notes
- Both models use the same temperature and top_p settings for consistency
- Temperature of 0.6 provides a good balance between creativity and consistency
- Top P of 0.95 allows for some variety while maintaining quality
- Both Qwen3 models may produce `<think>` tags during reasoning
- The framework automatically filters think tokens from streamed output and removes think tags in final outputs

## Best Practices Summary

1. **Start Simple**: Begin with a single agent and add complexity only when needed
2. **Use Orchestrators**: Delegate specialized tasks to focused agents
3. **Keep Agents Isolated**: Each agent should be self-contained and unaware of others
4. **Monitor Token Limits**: Ensure `max_tokens` is appropriate for your use case
5. **Verify Agent Types**: Use `agent` type for tool calls, `structured_output` for other purposes
6. **Prefer Smaller Models**: Scale up only when necessary
7. **Document with Diagrams**: Use mermaid diagrams for complex workflows
8. **Question Complexity**: Regularly ask if you're overcomplicating the solution 