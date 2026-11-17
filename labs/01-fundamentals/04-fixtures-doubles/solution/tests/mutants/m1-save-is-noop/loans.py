# MUTANT m1-save-is-noop: save() writes nothing: loans are lost.
"""Library loans. This module is finished: the lab is about testing it.

Library does not create what it depends on: it receives a store (a JSON file),
a clock (a function that returns "now") and a notifier. That is what makes it
testable: a test can hand it a temporary file, a fake clock and a test double.
"""

import json
import os
from collections.abc import Callable
from datetime import datetime, timedelta
from pathlib import Path
from typing import Protocol

DEFAULT_LOAN_DAYS = 14


class Notifier(Protocol):
    def send(self, member: str, message: str) -> None: ...


class LoanStore:
    """Loans kept in a JSON file."""

    def __init__(self, path: Path):
        self.path = path

    def load(self) -> list[dict]:
        if not self.path.exists():
            return []
        return json.loads(self.path.read_text(encoding="utf-8"))

    def save(self, loans: list[dict]) -> None:
        pass


class Library:
    def __init__(self, store: LoanStore, clock: Callable[[], datetime], notifier: Notifier):
        self.store = store
        self.clock = clock
        self.notifier = notifier

    def loan_days(self) -> int:
        """Days a member can keep a book: LOAN_DAYS from the environment, or 14."""
        return int(os.environ.get("LOAN_DAYS", DEFAULT_LOAN_DAYS))

    def lend(self, book: str, member: str) -> None:
        loans = self.store.load()
        if any(loan["book"] == book for loan in loans):
            raise ValueError(f"already lent: {book}")
        loans.append({"book": book, "member": member, "since": self.clock().isoformat()})
        self.store.save(loans)

    def overdue(self) -> list[dict]:
        """Loans kept longer than the loan period (the last day itself is not late)."""
        limit = timedelta(days=self.loan_days())
        now = self.clock()
        return [loan for loan in self.store.load() if now - datetime.fromisoformat(loan["since"]) > limit]

    def send_reminders(self) -> int:
        """Sends one reminder per overdue loan and returns how many were sent."""
        late = self.overdue()
        for loan in late:
            self.notifier.send(loan["member"], f"Please return '{loan['book']}'")
        return len(late)
