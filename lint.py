#!/usr/bin/env python3
"""
Lint script for the enview project using ruff.
Run this script to check code quality and formatting.
"""

import subprocess
import sys
from pathlib import Path


def run_command(cmd, description):
    """Run a command and return success status."""
    print(f"\n{description}...")
    print(f"Running: {' '.join(cmd)}")

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)

    return result.returncode == 0


def main():
    """Run all linting checks."""
    project_root = Path(__file__).parent
    success = True

    # Check code style and errors with ruff
    if not run_command(
        ["ruff", "check", str(project_root)], "Checking code style and errors"
    ):
        success = False

    # Check import sorting
    if not run_command(
        ["ruff", "check", "--select", "I", "--diff", str(project_root)],
        "Checking import sorting",
    ):
        success = False

    # Check formatting
    if not run_command(
        ["ruff", "format", "--check", str(project_root)], "Checking code formatting"
    ):
        success = False

    if success:
        print("\n✅ All checks passed!")
    else:
        print("\n❌ Some checks failed. Run 'ruff check --fix .' to auto-fix issues.")
        sys.exit(1)


if __name__ == "__main__":
    main()
