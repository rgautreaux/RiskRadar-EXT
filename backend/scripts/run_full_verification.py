"""Run full backend verification in one command.

This script runs:
1) pytest suite
2) standalone scraper/database/summary smoke test in mock-summary mode

Usage (from repository root):
    python backend/scripts/run_full_verification.py
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path
import argparse
from typing import NamedTuple


def _run(command: list[str], cwd: Path) -> int:
    print(f"\n$ {' '.join(command)}")
    result = subprocess.run(command, cwd=str(cwd), check=False)
    return result.returncode


class VerificationStep(NamedTuple):
    label: str
    command: list[str]
    cwd: Path
    env: dict[str, str] | None = None


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run full backend verification flow.")
    parser.add_argument(
        "--include-normalization-guardrails",
        action="store_true",
        help="Run normalization dry-run guardrails after tests and smoke test.",
    )
    parser.add_argument(
        "--strict-normalization",
        action="store_true",
        help="Fail if normalization reconciliation mismatches are detected.",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    repo_root = Path(__file__).resolve().parents[2]
    backend_dir = repo_root / "backend"
    python_exe = sys.executable

    print("== RiskRadar backend full verification ==")
    print(f"Python: {python_exe}")
    print(f"Repo:   {repo_root}")

    pythonpath_parts = [str(repo_root), str(backend_dir)]
    existing_pythonpath = os.environ.get("PYTHONPATH")
    if existing_pythonpath:
        pythonpath_parts.append(existing_pythonpath)
    verification_env = os.environ.copy()
    verification_env["PYTHONPATH"] = os.pathsep.join(pythonpath_parts)

    steps: list[VerificationStep] = [
        VerificationStep(
            "Run pytest suite",
            [python_exe, "-m", "pytest"],
            backend_dir,
        ),
        VerificationStep(
            "Run standalone smoke test with mock summary",
            [python_exe, "test_scrape_and_summarize.py", "--mock-summary"],
            backend_dir,
            verification_env,
        ),
    ]

    if args.include_normalization_guardrails:
        guardrail_cmd = [
            python_exe,
            "scripts/verify_normalization_guardrails.py",
        ]
        if args.strict_normalization:
            guardrail_cmd.append("--strict")
        guardrail_cmd.append("--allow-missing-tables")

        steps.append(
            VerificationStep(
                "Run normalization guardrails",
                guardrail_cmd,
                backend_dir,
            )
        )

    for step in steps:
        label = step.label
        command = step.command
        cwd = step.cwd
        print(f"\n== {label} ==")
        code = _run(command, cwd) if step.env is None else subprocess.run(command, cwd=str(cwd), check=False, env=step.env).returncode
        if code != 0:
            print(f"FAILED: {label} (exit code {code})")
            return code

    print("\nPASS: Full backend verification completed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
