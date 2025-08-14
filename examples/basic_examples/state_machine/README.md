# Basic State Machine Example

This example demonstrates a simple **state machine workflow** with clear state transitions and error handling.

## Purpose

Shows how to create agents that:
- Follow a defined sequence of states
- Make decisions based on tool outputs
- Handle errors gracefully
- Maintain workflow integrity

## Architecture

```
OrderProcessorAgent (State Machine Controller)
├── OrderValidatorAgent (State 1: Validation)
├── PaymentProcessorAgent (State 2: Payment)
└── OrderConfirmerAgent (State 3: Confirmation)
```

## State Machine Flow

```
INITIAL → VALIDATE → PAYMENT → CONFIRM → COMPLETE
   ↓         ↓         ↓         ↓
   |         |         |         |
   |         |         |         └── Success: Order confirmed
   |         |         └── Success: Payment processed
   |         └── Success: Order validated
   └── Start: Order received
```

## Files

- `order_processor_agent.yaml` - Main state machine orchestrator
- `order_validator_agent.yaml` - Validates order details
- `payment_processor_agent.yaml` - Processes payment
- `order_confirmer_agent.yaml` - Confirms order and generates summary
- `README.md` - This documentation

## Key Concepts Demonstrated

1. **State Transitions**: Clear progression through workflow states
2. **Decision Making**: Based on tool output examination
3. **Error Handling**: Stop workflow on validation/payment failures
4. **Data Flow**: Pass order data through each state
5. **Workflow Integrity**: Enforce sequential execution

## Usage

Test with valid order:
```bash
python -m framework.cli run examples/basic_examples/state_machine/order_processor_agent.yaml "Order: 2 laptops at $999 each, Customer: John Doe, Email: john@example.com, Address: 123 Main St, Payment: Credit Card"
```

## Expected Behavior

1. **Validation**: Checks order completeness and validity
2. **Payment**: Processes payment and generates transaction ID
3. **Confirmation**: Creates order confirmation with delivery estimate
4. **Completion**: Returns success message with order summary

## State Machine Rules

- **Sequential Execution**: States must be completed in order
- **Error Propagation**: Failures stop the workflow immediately
- **Data Continuity**: Order data flows through all states
- **State Inspection**: Each step examines previous tool output

## Framework Capabilities Used

- `agent_as_tool: true` - Agent composition
- `type: "structured_output"` - Reliable state data
- `output_schema` - State validation
- `boolean` - Success/failure indicators
- `enum` - Constrained status values
- State machine logic in prompts

## Benefits

- **Predictable Flow**: Clear state progression
- **Error Isolation**: Failures don't affect subsequent states
- **Maintainability**: Each state has single responsibility
- **Testability**: Individual states can be tested separately 