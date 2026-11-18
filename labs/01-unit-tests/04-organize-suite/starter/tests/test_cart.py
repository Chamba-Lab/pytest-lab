"""Tests for adding products to the cart. The tasks are in the README.

These three tests work, but each one repeats the same preparation (task 1).
"""

import pytest

from cart import Cart, Catalog

PRICES = {"pen": 300, "book": 2500, "voucher": 9999, "sticker": 1}


def test_adding_a_product_twice_adds_up():
    cart = Cart(Catalog(PRICES))
    cart.add("pen")
    cart.add("pen", 2)

    assert cart.items == {"pen": 3}


def test_an_unknown_product_is_rejected():
    cart = Cart(Catalog(PRICES))

    with pytest.raises(ValueError, match="unknown product"):
        cart.add("guitar")


def test_a_quantity_below_one_is_rejected():
    cart = Cart(Catalog(PRICES))

    with pytest.raises(ValueError, match="at least 1"):
        cart.add("pen", 0)


def test_many_additions_add_up():
    cart = Cart(Catalog(PRICES))
    for _ in range(2_000_000):
        cart.add("pen")

    assert cart.subtotal() == 2_000_000 * 300
