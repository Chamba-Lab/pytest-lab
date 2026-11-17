"""Your tests for passwords.py. The tasks are in the README."""

import pytest

from passwords import COMMON, violations


# Three tests that only differ in their data: task 1 turns them into one.


def test_too_short():
    assert violations("Short1A") == ["too-short"]


def test_no_digit():
    assert violations("NoDigitsHereAtAll") == ["no-digit"]


def test_no_upper():
    assert violations("lowercase1234") == ["no-upper"]


def test_each_rule():
    pytest.skip("TODO task 1: one parametrized test for the six rules, with readable ids")


def test_a_strong_password_is_valid():
    assert violations("Correct7Horse") == []


def test_every_common_password_is_rejected():
    assert COMMON
    for password in sorted(COMMON):
        assert "common" in violations(password)
