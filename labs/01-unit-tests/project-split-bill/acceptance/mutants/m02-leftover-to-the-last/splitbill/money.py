"""Money: parse amounts and split them into shares that add up to the cent."""

import re
from decimal import Decimal

CENT = Decimal("0.01")
_AMOUNT = re.compile(r"\d+(\.\d{1,2})?")


def parse_amount(text: str) -> Decimal:
    """A positive amount with at most two decimals and a dot: '12', '12.5', '12.50'."""
    text = text.strip()
    if not _AMOUNT.fullmatch(text):
        raise ValueError(f"invalid amount {text!r} (use digits and a dot, at most 2 decimals)")
    amount = Decimal(text)
    if amount <= 0:
        raise ValueError(f"amount must be positive: {text!r}")
    return amount


def split(amount: Decimal, people: int) -> list[Decimal]:
    """Equal shares, in cents, that add up exactly to `amount`.

    The cents that do not divide evenly go one each to the first shares, so
    split(Decimal("100.00"), 3) == [Decimal("33.34"), Decimal("33.33"), Decimal("33.33")].
    """
    if people < 1:
        raise ValueError("at least one person is needed to split an amount")
    cents = int(amount * 100)
    base, leftover = divmod(cents, people)
    return [Decimal(base + (1 if index >= people - leftover else 0)) * CENT for index in range(people)]


def format_amount(value: Decimal) -> str:
    """'+12.50' when owed, '-12.50' when owing, '0.00' when settled."""
    return "0.00" if value == 0 else f"{value:+.2f}"
