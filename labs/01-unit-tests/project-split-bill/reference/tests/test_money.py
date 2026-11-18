from decimal import Decimal

import pytest

from splitbill.money import format_amount, parse_amount, split


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        pytest.param("12", Decimal("12"), id="integer"),
        pytest.param("12.5", Decimal("12.5"), id="one-decimal"),
        pytest.param(" 12.50 ", Decimal("12.50"), id="spaces-around"),
    ],
)
def test_valid_amounts(text, expected):
    assert parse_amount(text) == expected


@pytest.mark.parametrize(
    "text",
    [
        pytest.param("12,50", id="comma"),
        pytest.param("12.345", id="three-decimals"),
        pytest.param("-5", id="negative"),
        pytest.param("1e3", id="exponent"),
        pytest.param("", id="empty"),
        pytest.param("ten", id="words"),
    ],
)
def test_invalid_amounts(text):
    with pytest.raises(ValueError, match="invalid amount"):
        parse_amount(text)


def test_zero_is_not_an_expense():
    with pytest.raises(ValueError, match="must be positive"):
        parse_amount("0.00")


@pytest.mark.parametrize(
    ("amount", "people", "expected"),
    [
        pytest.param("90.00", 3, ["30.00", "30.00", "30.00"], id="exact"),
        pytest.param("100.00", 3, ["33.34", "33.33", "33.33"], id="one-leftover-cent"),
        pytest.param("10.01", 3, ["3.34", "3.34", "3.33"], id="two-leftover-cents"),
        pytest.param("0.02", 3, ["0.01", "0.01", "0.00"], id="fewer-cents-than-people"),
        pytest.param("10.01", 1, ["10.01"], id="one-person"),
    ],
)
def test_shares_add_up_to_the_cent(amount, people, expected):
    shares = split(Decimal(amount), people)

    assert shares == [Decimal(share) for share in expected]
    assert sum(shares) == Decimal(amount)


def test_splitting_needs_someone():
    with pytest.raises(ValueError, match="at least one person"):
        split(Decimal("10.00"), 0)


@pytest.mark.parametrize(
    ("value", "text"),
    [
        pytest.param("12.5", "+12.50", id="owed"),
        pytest.param("-33.33", "-33.33", id="owes"),
        pytest.param("0.00", "0.00", id="settled"),
        pytest.param("-0.00", "0.00", id="negative-zero"),
    ],
)
def test_amounts_are_shown_with_sign_and_two_decimals(value, text):
    assert format_amount(Decimal(value)) == text
