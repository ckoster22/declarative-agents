Minimal Context Passing Demo

This example shows how an orchestrator can inject a previous agent's output into another agent's input without re-emitting large payloads.

Flow:
- ContextProducer produces a structured object.
- Orchestrator stores it in context automatically and then calls ContextConsumer with:
  - `{ContextProducer.message}`
  - `{ContextProducer.meta.count}`
  - `{ContextProducer.output}` (entire output)

Run:
```bash
python -m framework.cli examples/basic_examples/context_passing/minimal_context_demo/minimal_context_orchestrator.yaml "start"
```

Expected behavior:
- Orchestrator first runs `run_producer` to populate context under `ContextProducer`.
- Then `run_consumer` is invoked with an input JSON where placeholders are resolved by the framework.
- The consumer echoes those values per its schema.

