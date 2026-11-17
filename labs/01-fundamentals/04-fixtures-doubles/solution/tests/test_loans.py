"""Tests for loans.py. The fixtures (library, store, clock, notifier) live in conftest.py."""

import pytest

from loans import LoanStore


# Task 1 · Fixtures and a temporary file


def test_a_loan_is_saved_to_the_file(library, tmp_path):
    library.lend("Dune", "ana")

    reopened = LoanStore(tmp_path / "loans.json")
    assert reopened.load() == [{"book": "Dune", "member": "ana", "since": "2026-01-15T09:00:00"}]


def test_a_book_cannot_be_lent_twice(library):
    library.lend("Dune", "ana")

    with pytest.raises(ValueError, match="already lent"):
        library.lend("Dune", "beto")


# Task 2 · A clock the test controls


def test_a_loan_is_not_overdue_on_its_last_day(library, clock):
    library.lend("Dune", "ana")
    clock.advance(days=14)

    assert library.overdue() == []


def test_a_loan_is_overdue_after_its_last_day(library, clock):
    library.lend("Dune", "ana")
    clock.advance(days=14, seconds=1)

    assert [loan["book"] for loan in library.overdue()] == ["Dune"]


# Task 3 · A test double for the notifier


def test_reminders_go_only_to_late_members(library, clock, notifier):
    library.lend("Dune", "ana")
    clock.advance(days=10)
    library.lend("Emma", "beto")
    clock.advance(days=5)  # Dune: 15 days (late), Emma: 5 days

    sent = library.send_reminders()

    assert sent == 1
    notifier.send.assert_called_once_with("ana", "Please return 'Dune'")


# Task 4 · Environment variables with monkeypatch


def test_the_loan_period_comes_from_the_environment(library, clock, monkeypatch):
    monkeypatch.setenv("LOAN_DAYS", "7")
    library.lend("Dune", "ana")
    clock.advance(days=8)

    assert [loan["book"] for loan in library.overdue()] == ["Dune"]
