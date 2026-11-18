"""Shared fixtures for the tests of loans.py."""

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
    """A clock that only moves when the test says so."""

    def __init__(self, start: datetime):
        self.now = start

    def __call__(self) -> datetime:
        return self.now

    def advance(self, **delta: float) -> None:
        self.now += timedelta(**delta)


@pytest.fixture
def clock() -> FakeClock:
    return FakeClock(datetime(2026, 1, 15, 9, 0))


@pytest.fixture
def notifier():
    return create_autospec(Notifier, instance=True)


@pytest.fixture
def store(tmp_path) -> LoanStore:
    return LoanStore(tmp_path / "loans.json")


@pytest.fixture
def library(store, clock, notifier) -> Library:
    return Library(store, clock, notifier)
