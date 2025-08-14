from __future__ import annotations

import asyncio
import importlib.util
import logging
from pathlib import Path
import sys
from types import ModuleType
import json
import re
from typing import Dict, List, Optional, Tuple, Any

from pydantic import BaseModel, Field
from rich.console import Console
from rich.table import Table
from rich.text import Text

from framework.declarative_agents import (
    Agent,
    Runner,
    OpenAIChatCompletionsModel,
    ModelSettings,
    AgentSpecification,
    AgentLoader,
)
from framework.types import AgentType
from framework.utils import ThinkTagFilter
from config import get_external_client


def _extract_text_delta_from_event(event: object) -> Optional[str]:
    """Best-effort extraction of textual delta from a streamed event.

    Keeps exception handling scoped and minimal while accommodating multiple
    possible event shapes produced by different SDKs.
    """
    # Case 1: Direct string delta on the event
    try:
        ev_delta = event.delta  # type: ignore[attr-defined]
        if isinstance(ev_delta, str):
            return ev_delta
    except Exception:
        pass

    # Case 2: Event carries a data payload we can parse
    try:
        data_obj = event.data  # type: ignore[attr-defined]
    except Exception:
        data_obj = None

    if isinstance(data_obj, str):
        s = data_obj.strip()
        if s.startswith("data:"):
            s = s[5:].strip()
        if s and s != "[DONE]":
            # Try JSON line shape first
            try:
                obj = json.loads(s)
                for choice in obj.get("choices", []):
                    content = (
                        choice.get("delta", {}).get("content")
                        or choice.get("message", {}).get("content")
                    )
                    if isinstance(content, str) and content:
                        return content
            except Exception:
                # Conservative regex fall-back for a single content field
                m = re.search(r'"content"\s*:\s*"(.*?)"', s)
                if m:
                    return m.group(1)

    # Case 3: Structured data object with a delta attribute
    if data_obj is not None:
        try:
            data_delta = data_obj.delta  # type: ignore[attr-defined]
            if isinstance(data_delta, str):
                return data_delta
        except Exception:
            pass

    return None

"""
Evaluation utilities for the declarative agent framework.

This module provides a lightweight abstraction to support the `--eval` flag:

    python -m framework.cli path/to/agent.yaml --eval

Convention:

1. Each agent YAML lives somewhere in the repo (e.g. `.../clarifier_agent.yaml`).
2. A sibling directory named `evals/` sits next to that YAML. Python files inside
   it define one or more test suites.
3. A test-suite file must expose exactly one list whose variable name ends with
   `_test_suite` and exactly one string whose variable name ends with `_criteria`.

The framework discovers these variables reflectively and evaluates the agent
against each case using an AI-judge pattern.
"""

console = Console()

logger = logging.getLogger(__name__)
_EVAL_LOGGING_CONFIGURED: bool = False

# --- Models -----------------------------------------------------------------


class EvaluationResult(BaseModel):
    """Schema returned by the judge formatter."""

    passed: bool = Field(
        description="True if the agent's output meets all criteria, False otherwise."
    )
    reasoning: str = Field(
        description="Explanation referencing the specific criteria that were met or failed."
    )


# --- Helper functions -------------------------------------------------------

from config import BIG_MODEL, big_model_settings, Model

_QWEN_MODEL_NAME: Model = BIG_MODEL
_QWEN_MODEL_SETTINGS: ModelSettings = big_model_settings

_client = get_external_client()
if _client is None:
    logger.warning(
        "LM Studio client not detected – evaluations that rely on external LLMs will fail"
    )

# Lazily-constructed global judge agents so we don't spawn them repeatedly
_judge_agent: Optional[Agent] = None
_judge_formatter_agent: Optional[Agent] = None


def _configure_evaluation_logging(logs_dir: Path) -> None:
    """Ensure evaluation logs go to both stdout and a rotating file.

    The configuration is idempotent; repeated calls will be no-ops.
    """
    global _EVAL_LOGGING_CONFIGURED
    if _EVAL_LOGGING_CONFIGURED:
        return

    logs_dir.mkdir(parents=True, exist_ok=True)

    logger.setLevel(logging.INFO)
    logger.propagate = False

    formatter = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # File handler
    file_handler = logging.FileHandler(logs_dir / "evaluation.log", mode="a", encoding="utf-8")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    # Stream handler to stdout
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    _EVAL_LOGGING_CONFIGURED = True


def _get_judge_agents() -> Tuple[Agent, Agent]:
    """Create (or return cached) judge + formatter agents."""

    global _judge_agent, _judge_formatter_agent

    if _judge_agent and _judge_formatter_agent:
        return _judge_agent, _judge_formatter_agent

    judge_instructions = """
You are a meticulous and impartial AI evaluator. Your task is to assess the output of another AI agent based on a given set of criteria.

You will be provided with:
1.  The `agent_output` that the agent produced.
2.  The `evaluation_criteria` that you must strictly follow to determine if the test passes or fails.
3.  The `test_case` details for context.

CRITICAL RULE: Your decision about whether the test passes or fails MUST be based *exclusively* on the `evaluation_criteria`. The `test_case` (including the original `prompt`) is provided for context only. Do NOT infer the agent's expected behavior from the `prompt`; use only the `evaluation_criteria`.

Your process is to:
1.  **Understand the Goal**: Read the `evaluation_criteria` carefully to understand what constitutes a "pass".
2.  **Analyze the Output**: Scrutinize the `agent_output` and compare it against the rules in the `evaluation_criteria`.
3.  **Make a Decision**: Based *only* on the `evaluation_criteria`, decide if the `agent_output` passes the test.
4.  **Formulate Reasoning**: In the `reasoning` field, explain *why* the test passed or failed by referencing the specific rule(s) from the `evaluation_criteria` that were met or not met.
5.  **Set Final Verdict**: Set the `passed` field to `true` if the test passed, and `false` if it failed.

You may use <think> tags to reason about the query before producing your final output. Your final output must be a single, valid JSON object with 'passed' (boolean) and 'reasoning' (string) fields.
"""

    _judge_agent = Agent(
        name="EvaluationJudgeAgent",
        instructions=judge_instructions,
        model=OpenAIChatCompletionsModel(model=_QWEN_MODEL_NAME, openai_client=_client),
        model_settings=_QWEN_MODEL_SETTINGS,
    )

    _judge_formatter_agent = Agent(
        name="EvaluationJudgeFormatterAgent",
        instructions=(
            "You are a formatter agent. Your task is to convert the user's input text into a valid JSON "
            "object conforming to the EvaluationResult schema. The schema requires a 'passed' field (boolean) "
            "and a 'reasoning' field (string). Your output MUST be ONLY the JSON object."
        ),
        model=OpenAIChatCompletionsModel(model=_QWEN_MODEL_NAME, openai_client=_client),
        model_settings=_QWEN_MODEL_SETTINGS,
        output_type=EvaluationResult,
    )

    return _judge_agent, _judge_formatter_agent


# ---------------------------------------------------------------------------
# Evaluation helpers
# ---------------------------------------------------------------------------


async def evaluate_agent_against_suite(
    agent_spec: AgentSpecification,
    test_suite: List[Dict[str, Any]],
    evaluation_criteria: str,
) -> None:
    """Run a test suite against an agent specification and print a summary.

    If the YAML defines `type: "structured_output"` we invoke the full two-step
    `StructuredOutputAgent` chain so the formatter model guarantees valid JSON.
    Otherwise we fall back to the original direct-agent execution path.
    """

    judge_agent, judge_formatter_agent = _get_judge_agents()

    use_structured_output = (
        agent_spec.definition.agent_type == AgentType.STRUCTURED_OUTPUT
    )

    # Non-structured agents are materialised once and reused across cases – this
    # mirrors the original implementation.
    direct_agent: Optional[Agent] = None
    if not use_structured_output:
        direct_agent = agent_spec.create_agent()

    target_agent_name = (
        agent_spec.definition.name
        if use_structured_output
        else direct_agent.name if direct_agent is not None else "unknown"
    )

    # Create logs directory once at the start and configure logging sinks
    logs_dir = Path("evaluation_logs") / target_agent_name
    _configure_evaluation_logging(logs_dir)

    logger.info("--- Starting Evaluation for: %s ---", target_agent_name)
    pass_count = 0
    total_count = len(test_suite)

    # Data structures to track UI state and logs
    case_rows: List[Dict[str, str]] = []

    for idx, test_case in enumerate(test_suite, start=1):
        test_id: str = test_case.get("id", f"case_{idx}")
        agent_input: str = test_case.get("prompt", "")

        parsed_output = None

        if use_structured_output:
            # ----------------------------------------------------------
            # Use the full StructuredOutputAgent chain so that the
            # formatter model produces clean, parseable JSON.
            # ----------------------------------------------------------
            try:
                result_model = await agent_spec.structured_output_agent.run(
                    agent_input,
                )
                # Convert the Pydantic model into a regular dict so that
                # downstream code (judge prompt) can embed it easily.
                parsed_output = result_model.model_dump()
            except Exception as e:
                logger.exception("Error running StructuredOutputAgent: %s", e)
                parsed_output = None
        else:
            # ----------------------------------------------------------
            # Legacy path – run the single agent directly with streaming.
            # This mirrors the live streaming used by non-eval runs so
            # think tokens are surfaced to stdout and captured in logs.
            # ----------------------------------------------------------
            assert direct_agent is not None  # Mypy guard

            # Build kwargs for Runner.run_streamed to honour max_iterations if specified
            max_turns = 10
            if agent_spec.definition.max_iterations is not None:
                max_turns = agent_spec.definition.max_iterations

            streamed = Runner.run_streamed(
                starting_agent=direct_agent,
                input=agent_input,
                max_turns=max_turns,
            )

            think_filter = ThinkTagFilter()
            should_print_think = bool(agent_spec.definition.print_think_tokens)

            raw_chunks: list[str] = []
            visible_chunks: list[str] = []

            async for event in streamed.stream_events():
                text_delta = _extract_text_delta_from_event(event)
                if text_delta is None:
                    continue

                raw_chunks.append(text_delta)
                if should_print_think:
                    print(text_delta, end="", flush=True)
                    visible_chunks.append(text_delta)
                else:
                    chunk = think_filter.filter_token(text_delta)
                    if chunk:
                        print(chunk, end="", flush=True)
                        visible_chunks.append(chunk)

            # Ensure newline after stream
            print()

            # Persist both raw and visible streams into the evaluation log
            raw_stream = "".join(raw_chunks)
            visible_stream = "".join(visible_chunks)
            if raw_stream:
                logger.info("Raw stream output (including <think>):\n%s", raw_stream)
            if visible_stream and visible_stream != raw_stream:
                logger.info("Visible stream output (after think filtering):\n%s", visible_stream)

            # Use the schema-derived model decided at spec load time
            agent_stream = streamed
            if agent_spec.output_model is not None:
                parsed_output = agent_stream.final_output_as(agent_spec.output_model)

        if parsed_output is None:
            case_rows.append({"id": test_id, "result": "FAIL"})
            logger.debug("Raw output was: %s", agent_stream.final_output)
            continue

        # 2. AI Judge phase ------------------------------------------------
        # 2. Ask the AI judge to decide pass/fail
        judge_prompt = f"""The current date is June 2025.

Please evaluate the following agent output for logical correctness.
The output has already been validated as *parsable*. You only need to check the content against the criteria.

**Original Prompt:**\n```\n{agent_input}\n```\n\n**Agent's Parsed Output (as JSON):**\n```json\n{parsed_output}\n```\n\n**Evaluation Criteria:**\n```\n{evaluation_criteria}\n```\n\n**Test Case Details (for context):**\n```json\n{test_case}\n```"""

        # Stream judge output to stdout and log file
        judge_streamed = Runner.run_streamed(
            starting_agent=judge_agent,
            input=judge_prompt,
        )

        judge_raw_chunks: list[str] = []
        async for event in judge_streamed.stream_events():
            text_delta = _extract_text_delta_from_event(event)
            if text_delta is None:
                continue
            print(text_delta, end="", flush=True)
            judge_raw_chunks.append(text_delta)
        print()
        if judge_raw_chunks:
            logger.info("Judge raw stream output (token-by-token):\n%s", "".join(judge_raw_chunks))

        judge_output_text = str(judge_streamed.final_output)

        # Stream formatter output as well
        formatter_streamed = Runner.run_streamed(
            starting_agent=judge_formatter_agent,
            input=judge_output_text,
        )

        formatter_raw_chunks: list[str] = []
        async for event in formatter_streamed.stream_events():
            text_delta = _extract_text_delta_from_event(event)
            if text_delta is None:
                continue
            print(text_delta, end="", flush=True)
            formatter_raw_chunks.append(text_delta)
        print()
        if formatter_raw_chunks:
            logger.info(
                "Judge formatter raw stream output (token-by-token):\n%s",
                "".join(formatter_raw_chunks),
            )

        eval_result = formatter_streamed.final_output_as(EvaluationResult)

        if eval_result is None:
            case_rows.append({"id": test_id, "result": "FAIL"})
            logger.warning(
                "[FAIL] %s – judge formatter could not parse result; raw: %s",
                test_id,
                formatter_streamed.final_output,
            )
            continue

        if eval_result.passed:
            pass_count += 1
            case_rows.append({"id": test_id, "result": "PASS"})
            logger.info("[PASS] Test ID: %s", test_id)
        else:
            case_rows.append({"id": test_id, "result": "FAIL"})
            logger.warning("[FAIL] Test ID: %s", test_id)

        logger.info("Judge reasoning: %s\n", eval_result.reasoning)

    # Summary
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Test ID", width=30, no_wrap=True)
    table.add_column("Result", justify="right", width=10)
    for row in case_rows:
        result_text = Text(row["result"])
        if row["result"] == "PASS":
            result_text.stylize("bold green")
        else:
            result_text.stylize("bold red")
        table.add_row(row["id"], result_text)
    
    console.print(table)
    
    pass_rate = (pass_count / total_count) * 100 if total_count > 0 else 0
    logger.info(
        "--- Evaluation Summary — Passed: %s / %s (%.2f%%) ---",
        pass_count,
        total_count,
        pass_rate,
    )


# --- Discovery helpers ------------------------------------------------------


def _load_eval_module(yaml_path: str) -> ModuleType:
    """Locate and import the *first* Python module inside the sibling `evals/` directory."""

    yaml_file = Path(yaml_path).resolve()
    evals_dir = yaml_file.parent / "evals"

    if not evals_dir.is_dir():
        raise FileNotFoundError(
            f"No `evals/` directory found next to {yaml_file}. Expected at {evals_dir}"
        )

    # Pick the first .py file alphabetically
    py_files = sorted(p for p in evals_dir.iterdir() if p.suffix == ".py")
    if not py_files:
        raise FileNotFoundError(f"No Python eval files found in {evals_dir}")

    # --- Improved selection logic -----------------------------------
    # Prefer a test-suite file whose stem (filename without extension)
    # matches the *agent* name so that multiple agents in the same
    # directory can coexist with their own eval suites.
    #
    # Heuristic:
    #   1. Strip the trailing "_agent" from the YAML filename (if any).
    #   2. Look for a .py file whose stem *starts with* that base token.
    #   3. If multiple match, pick the first alphabetically.
    #   4. If none match, fall back to previous behaviour (first file).

    base_token = yaml_file.stem.replace("_agent", "")
    matching = [p for p in py_files if p.stem.startswith(base_token)]
    target = sorted(matching)[0] if matching else py_files[0]

    spec = importlib.util.spec_from_file_location(target.stem, target)
    if spec is None or spec.loader is None:  # pragma: no cover – unlikely
        raise ImportError(f"Failed to import evaluation module from {target}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # type: ignore[arg-type]
    return module


def _extract_suite_and_criteria(module: ModuleType) -> Tuple[List[Dict[str, Any]], str]:
    """Extract the test suite list and criteria string from the module via naming convention."""

    test_suite: Optional[List[Dict[str, Any]]] = None
    criteria: Optional[str] = None

    for attr_name, attr_val in vars(module).items():
        if attr_name.endswith("_test_suite") and isinstance(attr_val, list):
            test_suite = attr_val
        elif attr_name.endswith("_criteria") and isinstance(attr_val, str):
            criteria = attr_val

    if test_suite is None or criteria is None:
        raise AttributeError(
            "Evaluation module must define variables ending with `_test_suite` (list) "
            "and `_criteria` (str)."
        )

    return test_suite, criteria


# --- Public entrypoint ------------------------------------------------------


async def run_evaluation_from_yaml(yaml_path: str) -> None:
    """Discover and execute the evaluation associated with a YAML agent spec."""

    # 1. Load the agent specification (we need the full spec now)
    agent_spec = AgentLoader.load_from_file(yaml_path)

    # 2. Locate evaluation suite
    eval_module = _load_eval_module(yaml_path)
    test_suite, evaluation_criteria = _extract_suite_and_criteria(eval_module)

    # 3. Execute evaluation using the spec (handles structured agents)
    await evaluate_agent_against_suite(agent_spec, test_suite, evaluation_criteria)


# Handy synchronous wrapper (for potential future CLI integration)


def run_evaluation_sync(yaml_path: str) -> None:
    """Blocking wrapper around `run_evaluation_from_yaml` for convenience."""

    asyncio.run(run_evaluation_from_yaml(yaml_path))
