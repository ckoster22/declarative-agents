"""
Evaluation utilities for the declarative agent framework.

This module provides a lightweight abstraction to support the `--eval` flag:

    python -m framework.cli path/to/agent.yaml --eval

Convention:

1. Each agent YAML lives somewhere in the repo (e.g. `.../clarifier_agent.yaml`).
2. A sibling directory named `evals/` sits next to that YAML. Python files inside
   it define one or more test suites.
3. A test-suite file must expose exactly one list whose variable name ends with
   `_test_suite` and exactly one list/tuple of strings whose variable name ends with `_criteria`.

The framework discovers these variables reflectively and evaluates the agent
against each case using an AI-judge pattern.
"""

from __future__ import annotations

import asyncio
import importlib.util
from pathlib import Path
from types import ModuleType
from typing import Any, Dict, List, Tuple, cast

from agents import trace

from framework.declarative_agents import AgentLoader, AgentSpecification
from framework.evaluation_orchestrator import EvaluationOrchestrator

async def evaluate_agent_against_suite(
    agent_spec: AgentSpecification,
    test_suite: List[Dict[str, Any]],
    evaluation_criteria: List[str],
) -> None:
    """Run a test suite against an agent specification and print a summary.

    This is a convenience wrapper around EvaluationOrchestrator for backward compatibility.
    """
    orchestrator = EvaluationOrchestrator(agent_spec)
    await orchestrator.evaluate_against_suite(test_suite, evaluation_criteria)


# --- Discovery helpers ------------------------------------------------------


def _load_eval_module(yaml_path: str) -> ModuleType:
    """Locate and import the *first* Python module inside the sibling `evals/` directory."""

    yaml_file = Path(yaml_path).resolve()
    evals_dir = yaml_file.parent / "evals"

    if not evals_dir.is_dir():
        raise FileNotFoundError(f"No `evals/` directory found next to {yaml_file}. Expected at {evals_dir}")

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


def _is_list(value: object) -> bool:
    """Type guard: check if value is a list."""
    return hasattr(value, "__iter__") and hasattr(value, "__len__") and not hasattr(value, "keys")


def _is_list_or_tuple(value: object) -> bool:
    """Type guard: check if value is a list or tuple."""
    return _is_list(value) or (hasattr(value, "__iter__") and hasattr(value, "__len__") and hasattr(value, "__getitem__"))


def _extract_suite_and_criteria(module: ModuleType) -> Tuple[List[Dict[str, Any]], List[str]]:
    """Extract the test suite list and criteria list from the module via naming convention.

    The criteria must be a list/tuple of strings.
    """

    test_suite: Optional[List[Dict[str, Any]]] = None
    criteria: Optional[List[str]] = None

    for attr_name, attr_val in vars(module).items():
        if attr_name.endswith("_test_suite") and _is_list(attr_val):
            test_suite = cast(List[Dict[str, Any]], attr_val)
        elif attr_name.endswith("_criteria") and _is_list_or_tuple(attr_val):
            criteria = [str(c) for c in cast(List[Any], attr_val)]

    if test_suite is None or criteria is None:
        raise AttributeError(
            "Evaluation module must define variables ending with `_test_suite` (list) "
            "and `_criteria` (list | tuple of strings)."
        )

    return test_suite, criteria




# --- Public entrypoint ------------------------------------------------------


async def run_evaluation_from_yaml(yaml_path: str) -> None:
    """Discover and execute the evaluation associated with a YAML agent spec."""

    with trace(f"AI Judge Evaluation Suite — {yaml_path}"):
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
