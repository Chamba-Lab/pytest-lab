"""Your tests for expenses.store. Add test_rates.py and test_importer.py next to this file (see BRIEF.md).

The first test is an example of how to import the application; the rest of the suite is yours.
"""

import sqlite3

import pytest

from expenses.store import ExpenseStore


@pytest.fixture
def store():
    conn = sqlite3.connect(":memory:")
    yield ExpenseStore(conn)
    conn.close()  # runs even when the test fails (lab 2.3)


def test_a_new_store_is_empty(store):
    assert store.expenses() == []
