"""Tests for the discount. The fixtures live in conftest.py."""


# Task 2 · A fixture that uses another fixture


def test_no_discount_one_cent_below_100(almost_discount):
    assert almost_discount.total() == 9_999


def test_the_discount_starts_at_exactly_100(almost_discount):
    almost_discount.add("sticker")

    assert almost_discount.total() == 9_000


def test_the_discount_is_10_percent_of_any_subtotal(almost_discount):
    almost_discount.add("voucher")  # two vouchers: 199.98

    assert almost_discount.discount() == 1_999
