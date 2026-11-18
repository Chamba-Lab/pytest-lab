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


@pytest.fixture
def db():
    conn = sqlite3.connect(":memory:")  # setup: a new, empty database for this test
    create_schema(conn)
    yield conn
    conn.close()  # teardown: runs after the test, even when it fails


@pytest.fixture
def seeded_db(db):
    for player, points in [("beto", 7), ("ana", 5), ("ana", 9), ("carla", 7), ("dani", 2)]:
        add_score(db, player, points)
    return db
