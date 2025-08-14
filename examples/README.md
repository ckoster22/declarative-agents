# Examples Directory

This directory contains various examples demonstrating different agent patterns and workflows.

## Directory Structure

### `/basic_examples/` - Simple Standalone Agents
- `hello_world.yaml` - Basic hello world agent
- `note_taking_agent.yaml` - File-based note taking agent
- `poem_agent.yaml` - Single agent poem generator

### `/basic_examples/poem_workflow/` - Multi-Agent Poem Generation
- `poem_orchestrator_agent.yaml` - Main orchestrator
- `poem_outline_agent.yaml` - Generates poem outline
- `poem_composer_agent.yaml` - Composes final poem

### `/structured_examples/standalone/` - Standalone Structured Agents
- `context_description_agent.yaml` - Context-aware description agent
- `context_story_agent.yaml` - Context-aware story agent

### `/structured_examples/workflows/` - Multi-Agent Workflows
- `orchestrator_agent.yaml` - Basic description→story orchestrator
- `structured_orchestrator_agent.yaml` - Structured description→story orchestrator
- `orchestrator_agent_declarative_tools.yaml` - Declarative tools orchestrator
- `description_agent.yaml` - Description sub-agent
- `story_agent.yaml` - Story sub-agent
- `structured_description_agent.yaml` - Structured description sub-agent
- `structured_story_agent.yaml` - Structured story sub-agent

### `/tools/` - Supporting Tool Files
- `orchestrator_tools.py` - Tools for basic orchestrator
- `structured_orchestrator_tools.py` - Tools for structured orchestrator
- `gpt4o_search_tool.py` - GPT-4o search functionality
- `clarifier_tools.py` - Clarification tools

### `/standalone/` - Other Standalone Examples
- `thinking_agent_example.yaml` - Thinking agent with structured output

### `/deep_research/` - Advanced Research Workflow
- This directory contains a multi-stage research workflow that demonstrates advanced agentic patterns. See the `deep_research/README.md` for more details.

## Status

### ✅ Working Examples (Tested and Verified)
- **Standalone Agents:**
  - `/basic_examples/hello_world.yaml` ✅ - Simple hello world agent
  - `/basic_examples/poem_agent.yaml` ✅ - Single agent poem generator (50 lines)
  - `/structured_examples/standalone/context_description_agent.yaml` ✅ - Context-aware description agent
  - `/standalone/thinking_agent_example.yaml` ✅ - Thinking agent with structured output

- **Multi-Agent Workflows:**
  - `/basic_examples/poem_workflow/poem_orchestrator_agent.yaml` ⚠️ - Poem workflow (orchestrator + 2 sub-agents) - *Known quirk: may repeat lines in output at higher temperatures; reduce temperature or tighten prompts to mitigate.*
  - `/structured_examples/workflows/structured_orchestrator_agent.yaml` ✅ - Structured description→story workflow

- **Supporting Tools:**
  - All tool files in `/tools/` with corrected paths ✅

### ❌ Broken Examples
- ~~`structured_examples/two_agent_workflow.yaml`~~ - **REMOVED** - Referenced non-existent file paths (`declarative_experiment/yamls/description_agent.yaml` and `declarative_experiment/yamls/story_agent.yaml`)

### ⚠️ Examples with Minor Issues
- `/basic_examples/poem_workflow/poem_orchestrator_agent.yaml` - Works but has line repetition in the final output (lines 31-50 repeat lines 26-30)

## Usage

### Standalone Agents
```bash
python -m framework.cli examples/basic_examples/hello_world.yaml "Hello"
python -m framework.cli examples/basic_examples/poem_agent.yaml "nature"
python -m framework.cli examples/structured_examples/standalone/context_description_agent.yaml "artificial intelligence"
python -m framework.cli examples/standalone/thinking_agent_example.yaml "a robot that learns to love"
```

### Multi-Agent Workflows
```bash
python -m framework.cli examples/basic_examples/poem_workflow/poem_orchestrator_agent.yaml "nature"
python -m framework.cli examples/structured_examples/workflows/orchestrator_agent.yaml "artificial intelligence"
python -m framework.cli examples/structured_examples/workflows/structured_orchestrator_agent.yaml "artificial intelligence"
python -m framework.cli examples/structured_examples/workflows/orchestrator_agent_declarative_tools.yaml "artificial intelligence"
```
