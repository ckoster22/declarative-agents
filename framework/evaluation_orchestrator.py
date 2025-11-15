"""
Evaluation orchestrator for the declarative agent framework.

This module provides the EvaluationOrchestrator class that encapsulates
the evaluation logic, separating orchestration concerns from discovery
and logging setup.
"""

import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from agents import Agent, Runner
from pydantic import BaseModel, Field
from rich.console import Console
from rich.table import Table
from rich.text import Text

from config import BIG_MODEL, Model, big_model_settings, get_external_client
from framework.declarative_agents import AgentSpecification, ModelSettings, OpenAIChatCompletionsModel
from framework.evaluation_logging import configure_evaluation_logging
from framework.types import AgentType
from framework.utils import ThinkTagFilter, extract_text_delta_from_event

console = Console()
logger = logging.getLogger(__name__)

# --- Models -----------------------------------------------------------------


class EvaluationResult(BaseModel):
    """Schema returned by the judge formatter."""

    passed: bool = Field(description="True if the agent's output meets all criteria, False otherwise.")
    reasoning: str = Field(description="Explanation referencing the specific criteria that were met or failed.")


# --- Evaluation Orchestrator -----------------------------------------------


class EvaluationOrchestrator:
    """Orchestrates the evaluation of agents against test suites."""

    def __init__(self, agent_spec: AgentSpecification):
        """Initialize the orchestrator with an agent specification."""
        from framework.types import AgentType

        self.agent_spec = agent_spec
        # Type narrowing: use agent_type discriminator instead of isinstance
        self.use_structured_output = agent_spec.definition.agent_type == AgentType.STRUCTURED_OUTPUT
        self.direct_agent: Optional[Agent] = None

        # Initialize direct agent if not using structured output
        if not self.use_structured_output:
            self.direct_agent = agent_spec.create_agent()

        # Determine target agent name
        self.target_agent_name = (
            agent_spec.definition.name
            if self.use_structured_output
            else self.direct_agent.name if self.direct_agent is not None else "unknown"
        )

        # Configure logging
        logs_dir = Path("evaluation_logs") / self.target_agent_name
        configure_evaluation_logging(logs_dir)

    async def evaluate_against_suite(
        self,
        test_suite: List[Dict[str, Any]],
        evaluation_criteria: List[str],
    ) -> None:
        """Run a test suite against the agent specification and print a summary.

        The judge evaluates the agent output independently against each criterion.
        """
        logger.info("--- Starting Evaluation for: %s ---", self.target_agent_name)
        pass_count = 0
        total_count = len(test_suite)

        # Data structures to track UI state and logs
        case_rows: List[Dict[str, str]] = []

        for idx, test_case in enumerate(test_suite, start=1):
            test_id: str = test_case.get("id", f"case_{idx}")
            agent_input: str = test_case.get("prompt", "")

            parsed_output = await self._run_agent_for_test_case(agent_input, test_case)

            if parsed_output is None:
                case_rows.append({"id": test_id, "result": "FAIL", "criteria": "0/0"})
                logger.debug("No parseable output produced by the agent; skipping judge phase.")
                continue

            # Judge per criterion independently
            criteria_list = [str(c).strip() for c in (evaluation_criteria or []) if str(c).strip()]
            if not criteria_list:
                case_rows.append({"id": test_id, "result": "FAIL", "criteria": "0/0"})
                logger.warning("[FAIL] %s – empty criteria list provided; cannot judge.", test_id)
                continue

            per_criterion_results = await self._judge_output(parsed_output, agent_input, test_case, criteria_list)

            # Aggregate: overall pass only if all criteria passed
            overall_pass = all(r.passed for r in per_criterion_results) if per_criterion_results else False
            passed_count = sum(1 for r in per_criterion_results if r.passed)
            total_criteria = len(per_criterion_results)
            failed_indices = [str(i + 1) for i, r in enumerate(per_criterion_results) if not r.passed]
            criteria_summary = f"{passed_count}/{total_criteria}" + (
                f" (failed: {', '.join(failed_indices)})" if failed_indices else ""
            )

            if overall_pass:
                pass_count += 1
                case_rows.append({"id": test_id, "result": "PASS", "criteria": criteria_summary})
                logger.info("[PASS] Test ID: %s (all %s criteria passed)", test_id, len(per_criterion_results))
            else:
                case_rows.append({"id": test_id, "result": "FAIL", "criteria": criteria_summary})
                logger.warning("[FAIL] Test ID: %s (failed criteria: %s)", test_id, ", ".join(failed_indices) or "n/a")

        self._print_summary_table(case_rows, pass_count, total_count)

    async def _run_agent_for_test_case(
        self, agent_input: str, test_case: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Run the agent for a test case and return parsed output."""
        if self.use_structured_output:
            try:
                result_model = await self.agent_spec.structured_output_agent.run(agent_input)
                return result_model.model_dump()
            except Exception as e:
                logger.exception("Error running StructuredOutputAgent: %s", e)
                return None
        else:
            assert self.direct_agent is not None

            max_turns = 10
            if self.agent_spec.definition.max_iterations is not None:
                max_turns = self.agent_spec.definition.max_iterations

            streamed = Runner.run_streamed(
                starting_agent=self.direct_agent,
                input=agent_input,
                max_turns=max_turns,
            )

            think_filter = ThinkTagFilter()
            should_print_think = bool(self.agent_spec.definition.print_think_tokens)

            raw_chunks: list[str] = []
            visible_chunks: list[str] = []

            async for event in streamed.stream_events():
                text_delta = extract_text_delta_from_event(event)
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

            print()

            # Persist both raw and visible streams into the evaluation log
            raw_stream = "".join(raw_chunks)
            visible_stream = "".join(visible_chunks)
            if raw_stream:
                logger.info("Raw stream output (including <think>):\n%s", raw_stream)
            if visible_stream and visible_stream != raw_stream:
                logger.info("Visible stream output (after think filtering):\n%s", visible_stream)

            if self.agent_spec.output_model is not None:
                return streamed.final_output_as(self.agent_spec.output_model)
            return None

    async def _judge_output(
        self,
        parsed_output: Dict[str, Any],
        agent_input: str,
        test_case: Dict[str, Any],
        criteria_list: List[str],
    ) -> List[EvaluationResult]:
        """Judge the output against each criterion independently."""
        per_criterion_results: List[EvaluationResult] = []

        for crit_index, single_criterion in enumerate(criteria_list, start=1):
            judge_agent, judge_formatter_agent = self._build_fresh_judge_agents()
            judge_prompt = f"""The current date is June 2025.

Please evaluate the following agent output for logical correctness.
The output has already been validated as parsable. You only need to check the content against the single evaluation criterion below.

Evaluation Criterion:\n```\n{single_criterion}\n```

**Original Prompt:**\n```\n{agent_input}\n```\n\n**Agent's Parsed Output (as JSON):**\n```json\n{parsed_output}\n```\n\n**Test Case Details (for context):**\n```json\n{test_case}\n```"""

            # Stream judge output to stdout and log file
            judge_streamed = Runner.run_streamed(
                starting_agent=judge_agent,
                input=judge_prompt,
            )

            judge_raw_chunks: list[str] = []
            async for event in judge_streamed.stream_events():
                text_delta = extract_text_delta_from_event(event)
                if text_delta is None:
                    continue
                print(text_delta, end="", flush=True)
                judge_raw_chunks.append(text_delta)
            print()
            if judge_raw_chunks:
                logger.info(
                    "Judge raw stream output for criterion %s (token-by-token):\n%s",
                    crit_index,
                    "".join(judge_raw_chunks),
                )

            judge_output_text = str(judge_streamed.final_output)

            # Stream formatter output as well
            formatter_streamed = Runner.run_streamed(
                starting_agent=judge_formatter_agent,
                input=judge_output_text,
            )

            formatter_raw_chunks: list[str] = []
            async for event in formatter_streamed.stream_events():
                text_delta = extract_text_delta_from_event(event)
                if text_delta is None:
                    continue
                print(text_delta, end="", flush=True)
                formatter_raw_chunks.append(text_delta)
            print()
            if formatter_raw_chunks:
                logger.info(
                    "Judge formatter raw stream output for criterion %s (token-by-token):\n%s",
                    crit_index,
                    "".join(formatter_raw_chunks),
                )

            eval_result = formatter_streamed.final_output_as(EvaluationResult)

            if eval_result is None:
                logger.warning(
                    "[FAIL] %s – judge formatter could not parse result for criterion %s; raw: %s",
                    test_case.get("id", "unknown"),
                    crit_index,
                    formatter_streamed.final_output,
                )
                per_criterion_results.append(
                    EvaluationResult(passed=False, reasoning="Formatter could not parse result")
                )
            else:
                per_criterion_results.append(eval_result)
                level = logging.INFO if eval_result.passed else logging.WARNING
                logger.log(level, "Criterion %s passed: %s", crit_index, eval_result.passed)
                logger.info("Criterion %s reasoning: %s", crit_index, eval_result.reasoning)

        return per_criterion_results

    def _build_fresh_judge_agents(self) -> Tuple[Agent, Agent]:
        """Construct fresh judge and formatter agents to ensure independence per criterion."""
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

        client = get_external_client()
        if client is None:
            raise RuntimeError("External client not available for judge agents")

        _QWEN_MODEL_NAME: Model = BIG_MODEL
        _QWEN_MODEL_SETTINGS: ModelSettings = big_model_settings

        judge = Agent(
            name="EvaluationJudgeAgent",
            instructions=judge_instructions,
            model=OpenAIChatCompletionsModel(model=_QWEN_MODEL_NAME, openai_client=client),
            model_settings=_QWEN_MODEL_SETTINGS,
        )

        formatter = Agent(
            name="EvaluationJudgeFormatterAgent",
            instructions=(
                "You are a formatter agent. Your task is to convert the user's input text into a valid JSON "
                "object conforming to the EvaluationResult schema. The schema requires a 'passed' field (boolean) "
                "and a 'reasoning' field (string). Your output MUST be ONLY the JSON object."
            ),
            model=OpenAIChatCompletionsModel(model=_QWEN_MODEL_NAME, openai_client=client),
            model_settings=_QWEN_MODEL_SETTINGS,
            output_type=EvaluationResult,
        )

        return judge, formatter

    def _print_summary_table(self, case_rows: List[Dict[str, str]], pass_count: int, total_count: int) -> None:
        """Print the evaluation summary table."""
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Test ID", width=30, no_wrap=True)
        table.add_column("Result", justify="right", width=10)
        table.add_column("Criteria", justify="left", width=30)
        for row in case_rows:
            result_text = Text(row["result"])
            if row["result"] == "PASS":
                result_text.stylize("bold green")
            else:
                result_text.stylize("bold red")
            table.add_row(row["id"], result_text, row.get("criteria", ""))

        console.print(table)

        pass_rate = (pass_count / total_count) * 100 if total_count > 0 else 0
        logger.info(
            "--- Evaluation Summary — Passed: %s / %s (%.2f%%) ---",
            pass_count,
            total_count,
            pass_rate,
        )
