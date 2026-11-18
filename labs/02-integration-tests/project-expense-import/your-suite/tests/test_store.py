"""Your tests for expenses.store. Add test_rates.py and test_importer.py next to this file (see BRIEF.md).

The first test is an example of how to import the application; the rest of the suite is yours.
"""

import sqlite3

from expenses.store import ExpenseStore


def test_a_new_store_is_empty():
    conn = sqlite3.connect(":memory:")

    assert ExpenseStore(conn).expenses() == []

    conn.close()
