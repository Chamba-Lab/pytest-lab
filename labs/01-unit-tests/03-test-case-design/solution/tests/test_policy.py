"""Tests for passwords.py."""

import pytest

from passwords import COMMON, violations


# Task 1 · One case per rule: each password breaks only that rule


@pytest.mark.parametrize(
    ("password", "expected"),
    [
        pytest.param("Short1A", ["too-short"], id="too-short"),
        pytest.param("NoDigitsHereAtAll", ["no-digit"], id="no-digit"),
        pytest.param("lowercase1234", ["no-upper"], id="no-upper"),
        pytest.param("UPPERCASE1234", ["no-lower"], id="no-lower"),
        pytest.param("Has Space1234", ["whitespace"], id="whitespace"),
        pytest.param("Password1234", ["common"], id="common"),
    ],
)
def test_each_rule(password, expected):
    assert violations(password) == expected


# Task 2 · Both sides of the length limit (10 characters)


@pytest.mark.parametrize(
    ("password", "expected"),
    [
        pytest.param("Abcdefg12", ["too-short"], id="9-chars"),
        pytest.param("Abcdefg123", [], id="10-chars"),
    ],
)
def test_length_limit(password, expected):
    assert violations(password) == expected


# Given: the valid class and the list of common passwords


def test_a_strong_password_is_valid():
    assert violations("Correct7Horse") == []


def test_every_common_password_is_rejected():
    assert COMMON
    for password in sorted(COMMON):
        assert "common" in violations(password)
