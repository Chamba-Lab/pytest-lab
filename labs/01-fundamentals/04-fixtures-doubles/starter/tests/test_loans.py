"""Tests for loans.py. Replace each pytest.skip(...) with a real test (see the README).

When a test needs a fixture, add it as a parameter: def test_x(library, clock): ...
"""

import pytest

from loans import LoanStore


# Task 1 · Fixtures and a temporary file


def test_a_loan_is_saved_to_the_file():
    pytest.skip("TODO task 1: lend a book, then read the file with a new LoanStore")


def test_a_book_cannot_be_lent_twice():
    pytest.skip("TODO task 1: lending the same book twice raises ValueError")


# Task 2 · A clock the test controls


def test_a_loan_is_not_overdue_on_its_last_day():
    pytest.skip("TODO task 2: 14 days later the loan is not overdue yet")


def test_a_loan_is_overdue_after_its_last_day():
    pytest.skip("TODO task 2: one second after that, it is")


# Task 3 · A test double for the notifier


def test_reminders_go_only_to_late_members():
    pytest.skip("TODO task 3: one late loan, one on time; check what the notifier received")


# Task 4 · Environment variables with monkeypatch


def test_the_loan_period_comes_from_the_environment():
    pytest.skip("TODO task 4: with LOAN_DAYS=7, a loan is overdue after 8 days")
