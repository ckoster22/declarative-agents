# Input Schema Example

This example demonstrates **input validation** using input schemas to ensure agents receive properly structured data.

## Purpose

Shows how to:
- Define required input fields and their types
- Validate input against schemas
- Handle missing or invalid input gracefully
- Provide clear feedback on input requirements
- Ensure reliable agent behavior through input validation

## Architecture

```
InputValidationAgent
├── Input Schema (defines required fields and types)
├── Input Validation (checks input against schema)
└── Structured Output (provides validation results and analysis)
```

## Files

- `input_validation_agent.yaml` - Agent with input schema validation
- `README.md` - This documentation

## Key Concepts Demonstrated

1. **Input Schema Definition**: Specifying required fields and types
2. **Enum Validation**: Constraining values to specific options
3. **Required vs Optional Fields**: Distinguishing mandatory from optional input
4. **Validation Feedback**: Providing clear error messages
5. **Graceful Degradation**: Handling incomplete input appropriately

## Input Schema Structure

### Required Fields
- **topic**: String - The main topic or subject for analysis
- **time_period**: Enum - Must be "past", "present", or "future"
- **output_format**: Enum - Must be "summary", "detailed", or "brief"

### Optional Fields
- **additional_context**: String - Any additional context or requirements

## Usage Examples

### Valid Input
```bash
python -m framework.cli run examples/basic_examples/input_schema/input_validation_agent.yaml "Topic: Artificial Intelligence, Time Period: present, Output Format: summary, Additional Context: Focus on recent developments in 2024"
```

### Invalid Input (Missing Fields)
```bash
python -m framework.cli run examples/basic_examples/input_schema/input_validation_agent.yaml "Topic: Climate Change"
```

### Invalid Input (Wrong Enum Values)
```bash
python -m framework.cli run examples/basic_examples/input_schema/input_validation_agent.yaml "Topic: Renewable Energy, Time Period: yesterday, Output Format: long"
```

## Expected Behavior

### Valid Input
1. **Validation**: Input passes all schema checks
2. **Analysis**: Agent provides analysis based on requirements
3. **Output**: Structured response with validation status and analysis

### Invalid Input
1. **Validation**: Input fails schema validation
2. **Error Reporting**: Clear identification of missing/invalid fields
3. **Guidance**: Suggestions for correcting the input
4. **Graceful Handling**: Agent continues with available information

## Framework Capabilities Used

- `input_schema` - Input validation definition
- `properties` - Field definitions with types and descriptions
- `enum` - Constrained value validation
- `required` - Mandatory field specification
- `type: "structured_output"` - Reliable output format
- `output_schema` - Structured response validation

## Benefits

- **Input Reliability**: Ensures agents receive properly structured data
- **Error Prevention**: Catches input issues before processing
- **User Guidance**: Provides clear feedback on input requirements
- **Consistent Behavior**: Agents behave predictably with valid input
- **Maintainability**: Clear input requirements are documented

## Input Schema Best Practices

1. **Clear Descriptions**: Provide helpful descriptions for each field
2. **Appropriate Constraints**: Use enums for limited choice sets
3. **Required vs Optional**: Distinguish mandatory from optional fields
4. **Validation Messages**: Provide clear error messages
5. **Graceful Handling**: Handle invalid input without crashing

## Use Cases

- **Form Processing**: Validating user form submissions
- **API Input**: Ensuring API endpoints receive valid data
- **Workflow Orchestration**: Validating data between workflow steps
- **Data Processing**: Ensuring data quality before analysis
- **User Interfaces**: Providing real-time input validation feedback 