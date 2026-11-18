"""Your tests for splitbill.money. Add test_ledger.py and test_cli.py next to this file (see BRIEF.md).

The first test is an example of how to import the application; the rest of the suite is yours.
"""

from decimal import Decimal

from splitbill.money import parse_amount


def test_an_integer_amount_is_valid():
    assert parse_amount("12") == Decimal("12")
