#!/usr/bin/env python3
"""Simple test script to verify the refactoring works."""

import os
import sys

# Enable mock LLM for testing
os.environ["USE_MOCK_LLM"] = "true"
os.environ["MOCK_LLM_RESPONSE"] = "Hello, this is a test response."

# Add workspace to path
sys.path.insert(0, "/workspace")

from framework.declarative_agents import AgentLoader
from framework.types import AgentType, FunctionToolSpec, StructuredOutputAgentDefinition


def test_tool_spec_discriminated_union():
    """Test that ToolSpecification discriminated union works."""
    print("Testing ToolSpecification discriminated union...")
    
    # Test FunctionToolSpec
    function_tool = FunctionToolSpec(
        name="test_tool",
        function="framework.file_tools.read_file",
        description="Test function tool"
    )
    assert function_tool.tool_type == "function"
    assert function_tool.function == "framework.file_tools.read_file"
    print("✓ FunctionToolSpec works")
    
    # Test AgentAsToolSpec
    from framework.types import AgentAsToolSpec
    agent_tool = AgentAsToolSpec(
        name="test_agent_tool",
        agent_yaml_path="examples/basic_examples/hello_world.yaml",
        description="Test agent tool"
    )
    assert agent_tool.tool_type == "agent"
    assert agent_tool.agent_yaml_path == "examples/basic_examples/hello_world.yaml"
    print("✓ AgentAsToolSpec works")
    
    print("✓ ToolSpecification discriminated union test passed\n")


def test_agent_definition_discriminated_union():
    """Test that AgentDefinition discriminated union works."""
    print("Testing AgentDefinition discriminated union...")
    
    from framework.types import StandardAgentDefinition, StructuredOutputAgentDefinition, OrchestratorAgentDefinition
    
    # Test StandardAgentDefinition
    standard = StandardAgentDefinition(
        name="test_agent",
        prompt="You are a test agent",
        agent_type=AgentType.AGENT
    )
    assert standard.agent_type in (AgentType.AGENT, AgentType.TOOL)
    print("✓ StandardAgentDefinition works")
    
    # Test StructuredOutputAgentDefinition
    from framework.types import StructuredOutputSchema
    structured = StructuredOutputAgentDefinition(
        name="test_structured",
        prompt="You are a structured output agent",
        output_schema=StructuredOutputSchema(properties={"result": {"type": "string"}}),
        formatter_model="qwen3-1.7b"
    )
    assert structured.agent_type == AgentType.STRUCTURED_OUTPUT
    assert len(structured.output_schema.properties) > 0
    print("✓ StructuredOutputAgentDefinition works")
    
    # Test OrchestratorAgentDefinition
    orchestrator = OrchestratorAgentDefinition(
        name="test_orchestrator",
        prompt="You are an orchestrator"
    )
    assert orchestrator.agent_type == AgentType.ORCHESTRATOR
    print("✓ OrchestratorAgentDefinition works")
    
    print("✓ AgentDefinition discriminated union test passed\n")


def test_strict_enum_validation():
    """Test that strict enum validation works."""
    print("Testing strict enum validation...")
    
    from framework.declarative_agents import AgentLoader
    
    # This should fail with strict validation
    try:
        invalid_data = {
            "agent": {
                "name": "test",
                "prompt": "test",
                "type": "invalid_type"  # Invalid agent type
            }
        }
        AgentLoader.load_from_dict(invalid_data)
        print("✗ Should have raised ValueError for invalid agent type")
        sys.exit(1)
    except ValueError as e:
        assert "Invalid agent type" in str(e)
        print("✓ Strict enum validation works (correctly rejects invalid types)")
    
    print("✓ Strict enum validation test passed\n")


def test_event_extraction():
    """Test that shared event extraction works."""
    print("Testing shared event extraction...")
    
    from framework.utils import extract_text_delta_from_event
    
    # Test event with delta attribute
    class MockEvent:
        def __init__(self):
            self.delta = "test delta"
    
    event1 = MockEvent()
    result = extract_text_delta_from_event(event1)
    assert result == "test delta"
    print("✓ Event with delta attribute works")
    
    # Test event with data.delta
    class MockData:
        def __init__(self):
            self.delta = "data delta"
    
    class MockEvent2:
        def __init__(self):
            self.data = MockData()
    
    event2 = MockEvent2()
    result = extract_text_delta_from_event(event2)
    assert result == "data delta"
    print("✓ Event with data.delta works")
    
    # Test event with no delta
    class MockEvent3:
        pass
    
    event3 = MockEvent3()
    result = extract_text_delta_from_event(event3)
    assert result is None
    print("✓ Event with no delta returns None")
    
    print("✓ Event extraction test passed\n")


def test_context_default():
    """Test that context uses empty default instead of None."""
    print("Testing context default...")
    
    from framework.tool_context import get_current_context
    
    context = get_current_context()
    assert context is not None
    assert hasattr(context, "agent_outputs")
    print("✓ Context default is not None")
    
    print("✓ Context default test passed\n")


if __name__ == "__main__":
    print("Running refactoring tests...\n")
    
    try:
        test_tool_spec_discriminated_union()
        test_agent_definition_discriminated_union()
        test_strict_enum_validation()
        test_event_extraction()
        test_context_default()
        
        print("=" * 50)
        print("All tests passed! ✓")
        print("=" * 50)
    except Exception as e:
        print(f"\n✗ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
