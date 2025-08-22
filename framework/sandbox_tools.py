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
import os
import shutil
import subprocess
from uuid import uuid4


# Allow operators to override the sandbox image (e.g., pin to a digest) at deploy time
_DEFAULT_SANDBOX_IMAGE = "python:3.11-alpine"
_SANDBOX_IMAGE = os.environ.get("PY_SANDBOX_IMAGE", _DEFAULT_SANDBOX_IMAGE)

# Hard limits to minimize abuse and resource exhaustion
_MAX_CODE_BYTES = 64 * 1024  # Max size of code accepted from caller
_MAX_STDIO_BYTES = 64 * 1024  # Max captured bytes for both stdout and stderr

# Parameter guardrails
_MIN_TIMEOUT_SECONDS = 1
_MAX_TIMEOUT_SECONDS = 10
_MIN_MEMORY_MB = 32
_MAX_MEMORY_MB = 1024
_MIN_CPU_LIMIT = 0.1
_MAX_CPU_LIMIT = 2.0


def _clamp(value: float, lo: float, hi: float) -> float:
    if value < lo:
        return lo
    if value > hi:
        return hi
    return value


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

    # Fast-fail if the container runtime is not available
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

    # Enforce maximum code size to avoid host-side memory abuse
    code_bytes = code.encode("utf-8", errors="replace")
    if len(code_bytes) > _MAX_CODE_BYTES:
        return json.dumps(
            {
                "stdout": "",
                "stderr": "Code too large for sandbox",
                "exit_code": 413,
                "timed_out": False,
                "diagnostics": {
                    "max_code_bytes": _MAX_CODE_BYTES,
                },
            }
        )

    # Clamp resource parameters to conservative bounds
    safe_timeout = int(_clamp(int(timeout_seconds), _MIN_TIMEOUT_SECONDS, _MAX_TIMEOUT_SECONDS))
    safe_memory_mb = int(_clamp(int(memory_mb), _MIN_MEMORY_MB, _MAX_MEMORY_MB))
    safe_cpu_limit = float(_clamp(float(cpu_limit), _MIN_CPU_LIMIT, _MAX_CPU_LIMIT))

    container_name = f"py-sandbox-{uuid4().hex}"

    # Build a locked-down container invocation
    cmd = [
        "docker",
        "run",
        "--pull=never",
        "--log-driver=none",
        "--no-healthcheck",
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
        f"{safe_memory_mb}m",
        "--memory-swap",
        f"{safe_memory_mb}m",
        "--cpus",
        str(safe_cpu_limit),
        "--read-only",
        "--tmpfs",
        f"/tmp:rw,noexec,nosuid,nodev,size=64m",
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
        "PYTHONNOUSERSITE=1",
        "-e",
        "HOME=/tmp",
        _SANDBOX_IMAGE,
        "/bin/sh",
        "-lc",
        # Limit combined stdout/stderr to 64KiB each and keep file perms tight
        f"umask 077; cat >/tmp/main.py && python3 -I -B -S /tmp/main.py > /tmp/_o 2> /tmp/_e; head -c {_MAX_STDIO_BYTES} /tmp/_o; head -c {_MAX_STDIO_BYTES} /tmp/_e 1>&2",
    ]

    try:
        proc = subprocess.run(
            cmd,
            input=code_bytes,
            capture_output=True,
            timeout=safe_timeout,
        )
        return json.dumps(
            {
                "stdout": proc.stdout.decode("utf-8", errors="replace"),
                "stderr": proc.stderr.decode("utf-8", errors="replace"),
                "exit_code": int(proc.returncode),
                "timed_out": False,
                "diagnostics": {
                    "cpu_limit": safe_cpu_limit,
                    "memory_mb": safe_memory_mb,
                    "timeout_seconds": safe_timeout,
                },
            }
        )
    except subprocess.TimeoutExpired as e:
        # Best-effort cleanup; ignore return status
        subprocess.run(["docker", "rm", "-f", container_name], capture_output=True)
        stdout_text = e.stdout.decode("utf-8", errors="replace") if e.stdout else ""
        stderr_text = e.stderr.decode("utf-8", errors="replace") if e.stderr else ""
        return json.dumps(
            {
                "stdout": stdout_text,
                "stderr": stderr_text or "Execution timed out",
                "exit_code": 124,
                "timed_out": True,
                "diagnostics": {
                    "cpu_limit": safe_cpu_limit,
                    "memory_mb": safe_memory_mb,
                    "timeout_seconds": safe_timeout,
                },
            }
        )
    except Exception:
        # Best-effort cleanup; avoid surfacing internal details
        try:
            subprocess.run(["docker", "rm", "-f", container_name], capture_output=True)
        except Exception:
            pass
        return json.dumps(
            {
                "stdout": "",
                "stderr": "Sandbox execution failed",
                "exit_code": 1,
                "timed_out": False,
                "diagnostics": {
                    "cpu_limit": safe_cpu_limit,
                    "memory_mb": safe_memory_mb,
                    "timeout_seconds": safe_timeout,
                },
            }
        )

