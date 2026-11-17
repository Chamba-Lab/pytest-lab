"""Tests for passwords.py."""

import pytest

from passwords import COMMON, violations


# Task 1 · One parametrized test for the six rules (task 2 adds the last case)


@pytest.mark.parametrize(
    ("password", "expected"),
    [
        pytest.param("Short1A", ["too-short"], id="too-short"),
        pytest.param("NoDigitsHereAtAll", ["no-digit"], id="no-digit"),
        pytest.param("lowercase1234", ["no-upper"], id="no-upper"),
        pytest.param("UPPERCASE1234", ["no-lower"], id="no-lower"),
        pytest.param("Has Space1234", ["whitespace"], id="whitespace"),
        pytest.param("Password1234", ["common"], id="common"),
        pytest.param(
            "Tab\tSeparated12",
            ["whitespace"],
            id="tab-is-whitespace",
            marks=pytest.mark.xfail(reason="issue #7: tabs are not detected as whitespace"),
        ),
    ],
)
def test_each_rule(password, expected):
    assert violations(password) == expected


def test_a_strong_password_is_valid():
    assert violations("Correct7Horse") == []


# Task 3 · A custom marker


@pytest.mark.slow
def test_every_common_password_is_rejected():
    assert COMMON
    for password in sorted(COMMON):
        assert "common" in violations(password)
