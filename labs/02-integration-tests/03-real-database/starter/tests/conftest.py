"""Shared fixtures for the tests of scores.py. Tasks 1 and 2 add them here."""

# --- Mutant hunt: leave this part as it is ---------------------------------
# When SCORES_MUTANT names a folder in tests/mutants/, that folder goes first on
# the import path, so `import scores` loads the mutant. It must run before the
# imports below.
import os
import sys
from pathlib import Path

_mutant = os.environ.get("SCORES_MUTANT")
if _mutant:
    sys.path.insert(0, str(Path(__file__).parent / "mutants" / _mutant))
# ---------------------------------------------------------------------------

import sqlite3  # noqa: E402

import pytest  # noqa: E402

from scores import add_score, create_schema  # noqa: E402


# TODO task 1: a fixture `db` that gives each test a new, empty database in memory
#   with the schema created, and closes the connection after the test.
# TODO task 2: a fixture `seeded_db` that adds the README's five scores to `db`.
