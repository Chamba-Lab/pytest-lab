"""Expenses, balances and the transfers that settle them."""

import csv
from collections.abc import Iterable
from dataclasses import dataclass
from decimal import Decimal

from .money import parse_amount, split

HEADER = ["payer", "amount", "participants"]
ZERO = Decimal("0.00")


@dataclass(frozen=True)
class Expense:
    payer: str
    amount: Decimal
    participants: tuple[str, ...]


@dataclass(frozen=True)
class Transfer:
    debtor: str
    creditor: str
    amount: Decimal


class InputError(ValueError):
    """A problem in the input, with the line where it happened."""


def read_expenses(lines: Iterable[str]) -> list[Expense]:
    """Reads CSV lines: a header, then payer,amount,participants (names separated by ';')."""
    reader = csv.reader(lines)
    header = next(reader, None)
    if header is None or [column.strip() for column in header] != HEADER:
        raise InputError("line 1: the header must be: payer,amount,participants")
    expenses = []
    for number, row in enumerate(reader, start=2):
        if not any(cell.strip() for cell in row):
            continue  # blank line
        if len(row) != 3:
            raise InputError(f"line {number}: expected 3 columns, got {len(row)}")
        payer = row[0].strip()
        if not payer:
            raise InputError(f"line {number}: the payer is empty")
        try:
            amount = parse_amount(row[1])
        except ValueError as error:
            raise InputError(f"line {number}: {error}") from None
        participants = tuple(name.strip() for name in row[2].split(";") if name.strip())
        if not participants:
            raise InputError(f"line {number}: no participants")
        if len(set(participants)) != len(participants):
            raise InputError(f"line {number}: a participant appears twice")
        expenses.append(Expense(payer, amount, participants))
    return expenses


def balances(expenses: Iterable[Expense]) -> dict[str, Decimal]:
    """What each person paid minus what they owe, by name. Positive: is owed money."""
    totals: dict[str, Decimal] = {}
    for expense in expenses:
        totals[expense.payer] = totals.get(expense.payer, ZERO) + expense.amount
        shares = split(expense.amount, len(expense.participants))
        for name, share in zip(sorted(expense.participants), shares):
            totals[name] = totals.get(name, ZERO) - share
    return dict(sorted(totals.items()))


def settle(balance: dict[str, Decimal]) -> list[Transfer]:
    """Transfers that bring every balance to zero.

    The largest debtor pays the largest creditor, again and again; ties go in
    alphabetical order. It needs at most (people - 1) transfers.
    """
    debts = {name: -value for name, value in balance.items() if value < 0}
    credits = {name: value for name, value in balance.items() if value > 0}
    transfers = []
    while debts and credits:
        debtor = max(sorted(debts), key=debts.__getitem__)
        creditor = max(sorted(credits), key=credits.__getitem__)
        amount = min(debts[debtor], credits[creditor])
        transfers.append(Transfer(debtor, creditor, amount))
        debts[debtor] -= amount
        credits[creditor] -= amount
        if debts[debtor] == 0:
            del debts[debtor]
        if credits[creditor] == 0:
            del credits[creditor]
    return transfers
