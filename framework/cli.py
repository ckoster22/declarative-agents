"""
Command line interface for the declarative agent framework.

This module provides the main entry point for running agents and workflows
from the command line with proper argument parsing and execution.
"""

import argparse
import asyncio
from framework.declarative_agents import run_agent_from_yaml


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run declarative agents from YAML files"
    )
    parser.add_argument("yaml_file", help="Path to the YAML file")
    parser.add_argument("input", nargs="?", default="", help="Input text for the agent")
    parser.add_argument(
        "--eval",
        action="store_true",
        help="Run evaluation suite for the specified agent YAML",
    )
    return parser


async def run_command(args: argparse.Namespace) -> str:
    print("\n=== STARTING DECLARATIVE AGENT ===")

    if args.eval:
        from framework.evaluation import run_evaluation_from_yaml

        await run_evaluation_from_yaml(args.yaml_file)
        return "Evaluation complete"

    result = await run_agent_from_yaml(args.yaml_file, args.input)

    print("\n\n=== FINAL RESULT ===")
    print(result)

    return result


def main():
    parser = create_parser()
    args = parser.parse_args()

    asyncio.run(run_command(args))


if __name__ == "__main__":
    main()
