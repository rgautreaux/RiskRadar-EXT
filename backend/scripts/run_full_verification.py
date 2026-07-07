"""Run full backend verification in one command.

This script runs:
1) pytest suite
2) standalone scraper/database/summary smoke test in mock-summary mode

Usage (from repository root):
    python backend/scripts/run_full_verification.py
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path
import argparse


def _run(command: list[str], cwd: Path) -> int:
    print(f"\n$ {' '.join(command)}")
    result = subprocess.run(command, cwd=str(cwd), check=False)
    return result.returncode


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

    steps = [
        (
            "Run pytest suite",
            [python_exe, "-m", "pytest"],
            backend_dir,
        ),
        (
            "Run standalone smoke test with mock summary",
            [python_exe, "test_scrape_and_summarize.py", "--mock-summary"],
            backend_dir,
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
            (
                "Run normalization guardrails",
                guardrail_cmd,
                backend_dir,
            )
        )

    for label, command, cwd in steps:
        print(f"\n== {label} ==")
        code = _run(command, cwd)
        if code != 0:
            print(f"FAILED: {label} (exit code {code})")
            return code

    print("\nPASS: Full backend verification completed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
