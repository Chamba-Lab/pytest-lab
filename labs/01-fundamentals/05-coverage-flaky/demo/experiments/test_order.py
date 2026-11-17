"""Two tests that share state. They pass together and fail apart."""

CART = []  # module-level state: every test in this file sees the same list


def test_adding_an_item():
    CART.append("book")
    assert CART == ["book"]


def test_the_cart_has_one_item():
    assert len(CART) == 1  # true only if the test above ran first
