"""Two tests that share a list."""

CART = []  # module-level state: every test in this file sees the same list


def test_adding_an_item():
    CART.append("book")
    assert CART == ["book"]


def test_the_cart_has_one_item():
    assert len(CART) == 1
