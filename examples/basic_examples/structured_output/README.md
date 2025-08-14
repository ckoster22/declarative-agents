# Structured Output with Validation Example

This example demonstrates **structured output** with JSON schema validation and error handling.

## Purpose

Shows how to create agents that:
- Enforce strict output formats
- Validate data according to business rules
- Handle validation errors gracefully
- Provide reliable, consistent outputs

## Files

- `contact_form_agent.yaml` - Agent that processes contact forms with validation
- `README.md` - This documentation

## Key Concepts Demonstrated

1. **Structured Output**: Using `type: "structured_output"` for JSON validation
2. **Output Schema**: Defining required fields and data types
3. **Validation Logic**: Business rules for data validation
4. **Error Handling**: Returning validation errors in structured format

## Usage

Test with valid input:
```bash
python -m framework.cli run examples/basic_examples/structured_output/contact_form_agent.yaml "Name: John Doe, Email: john@example.com, Phone: (555) 123-4567, Message: Hello, I would like to inquire about your services."
```

Test with invalid input:
```bash
python -m framework.cli run examples/basic_examples/structured_output/contact_form_agent.yaml "Name: J, Email: invalid-email, Phone: 123, Message: Too short"
```

## Expected Behavior

**Valid Input**: Returns JSON with extracted data and empty validation_errors array
**Invalid Input**: Returns JSON with extracted data and validation_errors array containing error messages

## Framework Capabilities Used

- `type: "structured_output"` - Enables JSON schema validation
- `output_schema` - Defines required structure and validation rules
- `properties` - Field definitions with types and descriptions
- `required` - Enforces mandatory fields
- `items` - Array validation for error messages

## Validation Rules

- **Name**: 2-50 characters
- **Email**: Valid email format
- **Phone**: 10-15 digits (allows formatting)
- **Message**: 10-500 characters
- **All fields**: Required 