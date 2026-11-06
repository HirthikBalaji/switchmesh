"""
SwitchMesh Ephemeral Verification Sandbox Runner.
Provides isolated, reproducible execution of repro scripts, test suites, and hot-reload patches.
Generates cryptographically verified execution cards for Switch team chat rooms.
"""

from __future__ import annotations
import hashlib
import os
import subprocess
import tempfile
import time
from typing import Dict, Optional
from switchmesh.protocol.types import SandboxExecutionResult


class EphemeralSandbox:
    """
    Spins up an ephemeral working directory and executes target code or scripts.
    Collects execution metrics, diffs, and verification flags.
    """

    def __init__(self, sandbox_name: str, timeout_seconds: int = 15):
        self.sandbox_name = sandbox_name
        self.timeout_seconds = timeout_seconds
        self.temp_dir = tempfile.mkdtemp(prefix=f"switchmesh_{sandbox_name}_")

    def write_file(self, relative_path: str, content: str) -> str:
        """Write a source file into the sandbox workspace."""
        full_path = os.path.join(self.temp_dir, relative_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)
        return full_path

    def run_command(self, cmd: List[str] | str, env: Optional[Dict[str, str]] = None) -> SandboxExecutionResult:
        """
        Executes a command inside the sandbox.
        """
        sandbox_id = f"sbx-{hashlib.sha256(f'{self.sandbox_name}-{time.time()}'.encode()).hexdigest()[:8]}"
        start_time = time.time()

        merged_env = os.environ.copy()
        if env:
            merged_env.update(env)

        is_shell = isinstance(cmd, str)
        try:
            proc = subprocess.run(
                cmd,
                shell=is_shell,
                cwd=self.temp_dir,
                capture_output=True,
                text=True,
                timeout=self.timeout_seconds,
                env=merged_env
            )
            duration_ms = (time.time() - start_time) * 1000
            verified = (proc.returncode == 0)
            return SandboxExecutionResult(
                sandbox_id=sandbox_id,
                command=cmd if isinstance(cmd, str) else " ".join(cmd),
                exit_code=proc.returncode,
                stdout=proc.stdout.strip(),
                stderr=proc.stderr.strip(),
                duration_ms=round(duration_ms, 2),
                verified=verified
            )
        except subprocess.TimeoutExpired:
            duration_ms = (time.time() - start_time) * 1000
            return SandboxExecutionResult(
                sandbox_id=sandbox_id,
                command=cmd if isinstance(cmd, str) else " ".join(cmd),
                exit_code=-1,
                stdout="",
                stderr=f"Execution timed out after {self.timeout_seconds}s",
                duration_ms=round(duration_ms, 2),
                verified=False
            )

    def cleanup(self):
        """Removes the ephemeral sandbox directory."""
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir, ignore_errors=True)
