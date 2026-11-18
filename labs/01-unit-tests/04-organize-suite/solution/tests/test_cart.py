"""Tests for adding products to the cart. The fixtures live in conftest.py."""

import pytest


# Task 1 · The same preparation, written once


def test_adding_a_product_twice_adds_up(cart):
    cart.add("pen")
    cart.add("pen", 2)

    assert cart.items == {"pen": 3}


def test_an_unknown_product_is_rejected(cart):
    with pytest.raises(ValueError, match="unknown product"):
        cart.add("guitar")


def test_a_quantity_below_one_is_rejected(cart):
    with pytest.raises(ValueError, match="at least 1"):
        cart.add("pen", 0)


# Task 3 · A slow test, marked


@pytest.mark.slow
def test_many_additions_add_up(cart):
    for _ in range(2_000_000):
        cart.add("pen")

    assert cart.subtotal() == 2_000_000 * 300
