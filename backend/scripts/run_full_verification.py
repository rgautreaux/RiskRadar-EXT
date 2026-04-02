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


def _run(command: list[str], cwd: Path) -> int:
    print(f"\n$ {' '.join(command)}")
    result = subprocess.run(command, cwd=str(cwd), check=False)
    return result.returncode


def main() -> int:
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
