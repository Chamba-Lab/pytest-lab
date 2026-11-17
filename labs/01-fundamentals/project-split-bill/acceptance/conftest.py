"""Runs any implementation of splitbill as a separate process (black box).

By default it runs the reference: `python -m splitbill` with reference/src on the
import path. To check your own implementation, set SPLITBILL_CMD to the command
that starts it, for example:

    SPLITBILL_CMD="python -m splitbill"   (with your package importable)
    SPLITBILL_CMD="node mine/cli.js"
"""

import os
import shlex
import subprocess
import sys
from pathlib import Path

import pytest

REFERENCE_SRC = Path(__file__).resolve().parent.parent / "reference" / "src"


def command() -> tuple[list[str], dict[str, str]]:
    env = dict(os.environ)
    custom = os.environ.get("SPLITBILL_CMD")
    if custom:
        return shlex.split(custom, posix=os.name != "nt"), env
    env["PYTHONPATH"] = os.pathsep.join(filter(None, [str(REFERENCE_SRC), env.get("PYTHONPATH")]))
    return [sys.executable, "-m", "splitbill"], env


@pytest.fixture
def splitbill(tmp_path):
    """splitbill(command, csv_text) runs the CLI on a temporary CSV file and returns the result."""

    def run(subcommand: str, csv_text: str | None = None, *, encoding: str = "utf-8",
            file_name: str = "expenses.csv") -> subprocess.CompletedProcess[str]:
        path = tmp_path / file_name
        if csv_text is not None:
            path.write_text(csv_text, encoding=encoding)
        base, env = command()
        return subprocess.run([*base, subcommand, str(path)], env=env, capture_output=True,
                              text=True, encoding="utf-8", errors="replace", timeout=30)

    return run
