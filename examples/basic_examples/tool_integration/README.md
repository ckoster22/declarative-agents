# Tool Integration Example

This example demonstrates how to integrate **custom Python tools** with agents in the framework.

## Purpose

Shows how to:
- Create custom Python functions as tools
- Integrate tools with agents via function imports
- Handle tool parameters and return values
- Build agents that leverage external functionality

## Architecture

```
ToolIntegrationAgent
├── weather_lookup_tool (Custom Python function)
├── currency_converter_tool (Custom Python function)
└── text_analyzer_tool (Custom Python function)
```

## Files

- `tool_agent.yaml` - Agent that uses custom tools
- `custom_tools.py` - Python module containing custom tool functions
- `README.md` - This documentation

## Key Concepts Demonstrated

1. **Custom Tool Creation**: Python functions as tools
2. **Function Import**: Using `function` field with import paths
3. **Parameter Handling**: Tools with multiple parameters
4. **Return Value Processing**: JSON responses from tools
5. **Tool Selection**: Agent logic for choosing appropriate tools

## Available Tools

### Weather Lookup Tool
- **Function**: `weather_lookup_tool(city: str)`
- **Purpose**: Get weather information for cities
- **Supported Cities**: New York, London, Tokyo, Sydney, Paris
- **Returns**: Temperature, condition, humidity, timestamp

### Currency Converter Tool
- **Function**: `currency_converter_tool(amount: float, from_currency: str, to_currency: str)`
- **Purpose**: Convert between currencies
- **Supported Currencies**: USD, EUR, GBP, JPY, CAD
- **Returns**: Converted amount, exchange rate, timestamp

### Text Analyzer Tool
- **Function**: `text_analyzer_tool(text: str)`
- **Purpose**: Analyze text statistics and sentiment
- **Features**: Word count, sentence count, sentiment analysis
- **Returns**: Statistics, sentiment, timestamp

## Usage

Test weather lookup:
```bash
python -m framework.cli run examples/basic_examples/tool_integration/tool_agent.yaml "What's the weather in Tokyo?"
```

Test currency conversion:
```bash
python -m framework.cli run examples/basic_examples/tool_integration/tool_agent.yaml "Convert 100 USD to EUR"
```

Test text analysis:
```bash
python -m framework.cli run examples/basic_examples/tool_integration/tool_agent.yaml "Analyze this text: I love this amazing product! It's wonderful and makes me happy."
```

## Expected Behavior

1. **Tool Selection**: Agent identifies which tool to use
2. **Parameter Extraction**: Extracts required parameters from user input
3. **Tool Execution**: Calls the appropriate Python function
4. **Result Presentation**: Formats tool output for user

## Framework Capabilities Used

- `function` - Import path to Python functions
- Tool parameter handling
- JSON return value processing
- Tool selection logic in prompts
- Error handling for unsupported inputs

## Benefits

- **Extensibility**: Easy to add new tools
- **Reusability**: Tools can be used by multiple agents
- **Reliability**: Python functions provide consistent behavior
- **Maintainability**: Clear separation between tools and agent logic

## Tool Development Guidelines

1. **Function Signature**: Use clear parameter names and types
2. **Return Format**: Return JSON strings for structured data
3. **Error Handling**: Handle edge cases gracefully
4. **Documentation**: Include docstrings for tool functions
5. **Testing**: Test tools independently before integration 