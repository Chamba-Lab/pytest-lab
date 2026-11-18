"""The store against a real SQLite database."""

import sqlite3
from datetime import date
from decimal import Decimal

from expenses.store import Expense, ExpenseStore

LUNCH = Expense(date(2026, 11, 2), "Café y pan", Decimal("18.50"), "PEN", Decimal("18.50"))
HOTEL = Expense(date(2026, 11, 2), "Hotel en Cusco", Decimal("32.00"), "USD", Decimal("120.00"))


def test_saved_expenses_come_back_exactly(store):
    store.save_import("abc123", "trip.csv", [LUNCH, HOTEL])

    assert store.expenses() == [LUNCH, HOTEL]
    assert store.was_imported("abc123")


def test_the_total_is_exact_to_the_cent(store):
    expenses = [
        Expense(date(2026, 11, 2), "Taxi", Decimal("10.10"), "PEN", Decimal("10.10")),
        Expense(date(2026, 11, 3), "Bus", Decimal("20.20"), "PEN", Decimal("20.20")),
    ]
    store.save_import("abc123", "trip.csv", expenses)

    assert store.total_pen() == Decimal("30.30")


def test_a_saved_import_survives_closing_the_database(tmp_path):
    path = tmp_path / "expenses.db"
    conn = sqlite3.connect(path)
    ExpenseStore(conn).save_import("abc123", "trip.csv", [LUNCH])
    conn.close()  # closing does not commit: only what save_import committed is on disk

    reopened = sqlite3.connect(path)
    try:
        assert ExpenseStore(reopened).expenses() == [LUNCH]
    finally:
        reopened.close()
