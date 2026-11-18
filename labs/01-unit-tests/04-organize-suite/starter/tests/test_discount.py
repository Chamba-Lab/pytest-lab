"""Tests for the discount. Replace each pytest.skip(...) with a real test (see the README).

When a test needs a fixture, add it as a parameter: def test_x(almost_discount): ...
"""

import pytest


def test_no_discount_one_cent_below_100():
    pytest.skip("TODO task 2: a cart of 99.99 pays 99.99")


def test_the_discount_starts_at_exactly_100():
    pytest.skip("TODO task 2: one more cent and the cart pays 90.00")


def test_the_discount_is_10_percent_of_any_subtotal():
    pytest.skip("TODO task 2: the discount of a bigger cart")
