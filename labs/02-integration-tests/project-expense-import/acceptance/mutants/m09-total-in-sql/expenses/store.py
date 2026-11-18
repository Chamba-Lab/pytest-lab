"""Expenses kept in SQLite. Amounts are stored as text so they come back as exact Decimals."""

import sqlite3
from dataclasses import dataclass
from datetime import date
from decimal import Decimal

SCHEMA = """
CREATE TABLE IF NOT EXISTS imports (
    fingerprint TEXT PRIMARY KEY,
    file_name TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS expenses (
    spent_on TEXT NOT NULL,
    description TEXT NOT NULL,
    amount TEXT NOT NULL,
    currency TEXT NOT NULL,
    amount_pen TEXT NOT NULL,
    fingerprint TEXT NOT NULL REFERENCES imports (fingerprint)
);
"""


@dataclass(frozen=True)
class Expense:
    spent_on: date
    description: str
    amount: Decimal
    currency: str
    amount_pen: Decimal


class ExpenseStore:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn
        conn.executescript(SCHEMA)

    def was_imported(self, fingerprint: str) -> bool:
        row = self.conn.execute("SELECT 1 FROM imports WHERE fingerprint = ?", (fingerprint,)).fetchone()
        return row is not None

    def save_import(self, fingerprint: str, file_name: str, expenses: list[Expense]) -> None:
        """Saves the import and all its expenses in one transaction: all of them, or none."""
        with self.conn:
            self.conn.execute("INSERT INTO imports (fingerprint, file_name) VALUES (?, ?)", (fingerprint, file_name))
            self.conn.executemany(
                "INSERT INTO expenses (spent_on, description, amount, currency, amount_pen, fingerprint)"
                " VALUES (?, ?, ?, ?, ?, ?)",
                [
                    (e.spent_on.isoformat(), e.description, str(e.amount), e.currency, str(e.amount_pen), fingerprint)
                    for e in expenses
                ],
            )

    def expenses(self) -> list[Expense]:
        """Every expense, in the order it was saved."""
        rows = self.conn.execute(
            "SELECT spent_on, description, amount, currency, amount_pen FROM expenses ORDER BY rowid"
        )
        return [
            Expense(date.fromisoformat(day), description, Decimal(amount), currency, Decimal(pen))
            for day, description, amount, currency, pen in rows
        ]

    def total_pen(self) -> Decimal:
        """The sum of every expense in soles, exact to the cent."""
        (total,) = self.conn.execute("SELECT COALESCE(SUM(amount_pen), 0) FROM expenses").fetchone()
        return Decimal(str(total))
