"""Shared fixtures for the tests of loans.py. Task 1 adds them here."""

# --- Mutant hunt: leave this part as it is ---------------------------------
# When LOANS_MUTANT names a folder in tests/mutants/, that folder goes first on
# the import path, so `import loans` loads the mutant. It must run before the
# imports below.
import os
import sys
from pathlib import Path

_mutant = os.environ.get("LOANS_MUTANT")
if _mutant:
    sys.path.insert(0, str(Path(__file__).parent / "mutants" / _mutant))
# ---------------------------------------------------------------------------

from datetime import datetime, timedelta  # noqa: E402
from unittest.mock import create_autospec  # noqa: E402

import pytest  # noqa: E402

from loans import Library, LoanStore, Notifier  # noqa: E402


class FakeClock:
    """A clock that only moves when the test says so. Already written: use it in a fixture."""

    def __init__(self, start: datetime):
        self.now = start

    def __call__(self) -> datetime:
        return self.now

    def advance(self, **delta: float) -> None:
        self.now += timedelta(**delta)


# TODO task 1: four fixtures
#   clock    -> a FakeClock that starts on 2026-01-15 09:00
#   notifier -> a test double of Notifier made with create_autospec
#   store    -> a LoanStore on a file inside tmp_path
#   library  -> a Library built from the three fixtures above
