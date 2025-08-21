"""
Containerized sandbox execution tools.

This module exposes a framework-level tool to run short Python code snippets
inside an isolated, resource-constrained sandbox. The sandbox has no network,
limited CPU and memory, a read-only root filesystem, and only a tmpfs-mounted
"/tmp" available for writing the code prior to execution.

The function returns a JSON string with stdout, stderr, exit_code, timed_out,
and diagnostics fields.
"""

from __future__ import annotations

import json
import shutil
import subprocess
from uuid import uuid4


_SANDBOX_IMAGE = "python:3.11-alpine"


def run_python_sandboxed(
    code: str,
    timeout_seconds: int = 5,
    memory_mb: int = 256,
    cpu_limit: float = 0.5,
) -> str:
    """
    Execute Python code inside a strongly sandboxed, containerized environment.

    Args:
        code: The Python code to execute.
        timeout_seconds: Max wall-clock seconds to allow before terminating.
        memory_mb: Memory limit for the sandbox in MiB.
        cpu_limit: CPU limit (e.g., 0.5 = half a CPU).

    Returns:
        A JSON string with keys: stdout, stderr, exit_code, timed_out, diagnostics.
    """

    if shutil.which("docker") is None:
        return json.dumps(
            {
                "stdout": "",
                "stderr": "Sandbox runtime not available",
                "exit_code": 127,
                "timed_out": False,
                "diagnostics": {
                    "hint": "Install and start the container runtime.",
                },
            }
        )

    container_name = f"py-sandbox-{uuid4().hex}"

    cmd = [
        "docker",
        "run",
        "--pull=never",
        "--log-driver=none",
        "--rm",
        "--name",
        container_name,
        "-i",
        "--network",
        "none",
        "--ipc",
        "none",
        "--pids-limit",
        "100",
        "--memory",
        f"{memory_mb}m",
        "--memory-swap",
        f"{memory_mb}m",
        "--cpus",
        str(cpu_limit),
        "--read-only",
        "--tmpfs",
        "/tmp:rw,size=64m",
        "-w",
        "/tmp",
        "--security-opt",
        "no-new-privileges",
        "--cap-drop",
        "ALL",
        "--ulimit",
        "nproc=100:100",
        "--ulimit",
        "nofile=128:128",
        "--user",
        "65534:65534",
        "-e",
        "PYTHONDONTWRITEBYTECODE=1",
        "-e",
        "PYTHONUNBUFFERED=1",
        "-e",
        "HOME=/tmp",
        _SANDBOX_IMAGE,
        "/bin/sh",
        "-lc",
        # Limit combined stdout/stderr to 64KiB each to avoid unbounded host-side capture
        "cat >/tmp/main.py && python3 /tmp/main.py > /tmp/_o 2> /tmp/_e; head -c 65536 /tmp/_o; head -c 65536 /tmp/_e 1>&2",
    ]

    try:
        proc = subprocess.run(
            cmd,
            input=code.encode("utf-8"),
            capture_output=True,
            timeout=timeout_seconds,
        )
        return json.dumps(
            {
                "stdout": proc.stdout.decode("utf-8", errors="replace"),
                "stderr": proc.stderr.decode("utf-8", errors="replace"),
                "exit_code": int(proc.returncode),
                "timed_out": False,
                "diagnostics": {
                    "cpu_limit": cpu_limit,
                    "memory_mb": memory_mb,
                    "timeout_seconds": timeout_seconds,
                },
            }
        )
    except subprocess.TimeoutExpired as e:
        # Best-effort cleanup; ignore return status
        subprocess.run(["docker", "rm", "-f", container_name], capture_output=True)
        stdout_text = (
            e.stdout.decode("utf-8", errors="replace") if e.stdout else ""
        )
        stderr_text = (
            e.stderr.decode("utf-8", errors="replace") if e.stderr else ""
        )
        return json.dumps(
            {
                "stdout": stdout_text,
                "stderr": stderr_text or "Execution timed out",
                "exit_code": 124,
                "timed_out": True,
                "diagnostics": {
                    "cpu_limit": cpu_limit,
                    "memory_mb": memory_mb,
                    "timeout_seconds": timeout_seconds,
                },
            }
        )


