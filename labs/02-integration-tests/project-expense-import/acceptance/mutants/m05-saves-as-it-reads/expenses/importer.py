"""Imports a CSV file of expenses into the store, with every amount converted to soles (PEN).

An import is all or nothing: if a line is invalid or the rates service fails, nothing
is saved, and the same file can be imported again once the problem is fixed.
"""

import csv
import hashlib
import re
from datetime import date
from decimal import ROUND_HALF_UP, Decimal
from pathlib import Path

from expenses.rates import RatesClient
from expenses.store import Expense, ExpenseStore

HEADER = ["date", "description", "amount", "currency"]
AMOUNT = re.compile(r"\d+(\.\d{1,2})?")
CURRENCY = re.compile(r"[A-Z]{3}")
CENT = Decimal("0.01")


class ImportFailed(Exception):
    """The file cannot be imported. For a problem in the file, the message starts with `line N:`."""


class DuplicateImport(ImportFailed):
    """A file with exactly the same content was already imported."""


def to_soles(amount: Decimal, rate: Decimal) -> Decimal:
    """amount × rate, rounded to the cent; a half cent rounds up."""
    return (amount * rate).quantize(CENT, rounding=ROUND_HALF_UP)


def read_rows(text: str) -> list[tuple[date, str, Decimal, str]]:
    """The rows of the CSV, checked line by line. Blank lines are skipped."""
    reader = csv.reader(text.splitlines())
    if next(reader, None) != HEADER:
        raise ImportFailed("line 1: the header must be date,description,amount,currency")
    rows = []
    for number, fields in enumerate(reader, start=2):
        if not fields:
            continue
        if len(fields) != 4:
            raise ImportFailed(f"line {number}: expected 4 columns, got {len(fields)}")
        day, description, amount, currency = (field.strip() for field in fields)
        try:
            spent_on = date.fromisoformat(day)
        except ValueError:
            raise ImportFailed(f"line {number}: invalid date {day!r}") from None
        if not AMOUNT.fullmatch(amount) or Decimal(amount) == 0:
            raise ImportFailed(f"line {number}: invalid amount {amount!r}")
        if not CURRENCY.fullmatch(currency):
            raise ImportFailed(f"line {number}: invalid currency {currency!r}")
        rows.append((spent_on, description, Decimal(amount), currency))
    return rows


def import_file(path: Path, store: ExpenseStore, rates: RatesClient) -> int:
    """Imports the expenses of a UTF-8 CSV file and returns how many were saved."""
    content = path.read_bytes()
    fingerprint = hashlib.sha256(content).hexdigest()
    if store.was_imported(fingerprint):
        raise DuplicateImport(f"{path.name} was already imported")
    store.conn.execute("INSERT INTO imports (fingerprint, file_name) VALUES (?, ?)", (fingerprint, path.name))
    rate_of = {"PEN": Decimal(1)}
    count = 0
    lines = content.decode("utf-8").splitlines()
    for number in range(2, len(lines) + 1):
        one_line = "\n".join(lines[:1] + [""] * (number - 2) + [lines[number - 1]])  # keeps the line number
        for spent_on, description, amount, currency in read_rows(one_line):
            if currency not in rate_of:
                rate_of[currency] = rates.rate_to_pen(currency)
            pen = to_soles(amount, rate_of[currency])
            store.conn.execute(
                "INSERT INTO expenses (spent_on, description, amount, currency, amount_pen, fingerprint)"
                " VALUES (?, ?, ?, ?, ?, ?)",
                (spent_on.isoformat(), description, str(amount), currency, str(pen), fingerprint),
            )
            store.conn.commit()
            count += 1
    return count
