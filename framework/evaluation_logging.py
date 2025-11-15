"""
Logging configuration for evaluation module.

This module handles the setup of logging sinks for evaluation runs,
separating logging concerns from evaluation orchestration logic.
"""

import logging
import sys
from pathlib import Path


_EVAL_LOGGING_CONFIGURED: bool = False


def configure_evaluation_logging(logs_dir: Path) -> None:
    """Ensure evaluation logs go to both stdout and a rotating file.

    The configuration is idempotent; repeated calls will be no-ops.

    Args:
        logs_dir: Directory where evaluation logs should be written
    """
    global _EVAL_LOGGING_CONFIGURED
    if _EVAL_LOGGING_CONFIGURED:
        return

    logger = logging.getLogger(__name__.split(".")[0] + ".evaluation")
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
