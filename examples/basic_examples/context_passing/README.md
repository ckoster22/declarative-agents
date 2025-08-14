# Context Passing Example

This example demonstrates how agents pass structured data between each other in a workflow.

## Purpose

Shows how to:
- Extract and structure data in one agent
- Pass complete context to another agent
- Maintain data integrity across agent boundaries
- Coordinate multi-step workflows with data flow

## Architecture

```
ContextOrchestratorAgent
├── DataCollectorAgent (extracts structured data)
└── DataAnalyzerAgent (receives and analyzes data)
```

## Files

- `context_orchestrator_agent.yaml` - Main orchestrator that coordinates the workflow
- `data_collector_agent.yaml` - Agent that extracts and structures data
- `data_analyzer_agent.yaml` - Agent that receives structured data and analyzes it
- `README.md` - This documentation

## Key Concepts Demonstrated

1. **Data Extraction**: Converting unstructured input to structured format
2. **Context Passing**: Passing complete JSON data between agents
3. **Structured Communication**: Using JSON schemas for reliable data transfer
4. **Workflow Coordination**: Orchestrating multi-step processes

## Usage

Run with sample data:
```bash
python -m framework.cli run examples/basic_examples/context_passing/context_orchestrator_agent.yaml "The company reported 15% revenue growth in Q3, with strong performance in the technology sector. Customer satisfaction scores improved to 4.2/5.0, and employee retention rates reached 92%."
```

## Expected Behavior

1. **Data Collection**: Extracts topic, facts, sentiment, and confidence
2. **Data Analysis**: Receives structured data and provides insights
3. **Final Output**: Presents both collected data and analysis results

## Data Flow

```
User Input → DataCollector → Structured JSON → DataAnalyzer → Analysis Results
```

## Framework Capabilities Used

- `agent_as_tool: true` - Agent composition
- `type: "structured_output"` - Reliable JSON output
- `output_schema` - Data structure validation
- `input_template` - Parameter passing
- `enum` - Constrained field values
- `array` - List data structures

## Benefits

- **Data Integrity**: Structured schemas ensure reliable data transfer
- **Modularity**: Each agent has a single responsibility
- **Reusability**: Agents can be used in different workflows
- **Maintainability**: Clear separation of concerns 