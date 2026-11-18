"""Shared fixtures for the tests of cart.py."""

# --- Mutant hunt: leave this part as it is ---------------------------------
# When CART_MUTANT names a folder in tests/mutants/, that folder goes first on
# the import path, so `import cart` loads the mutant. It must run before the
# imports below.
import os
import sys
from pathlib import Path

_mutant = os.environ.get("CART_MUTANT")
if _mutant:
    sys.path.insert(0, str(Path(__file__).parent / "mutants" / _mutant))
# ---------------------------------------------------------------------------

import pytest  # noqa: E402

from cart import Cart, Catalog  # noqa: E402

PRICES = {"pen": 300, "book": 2500, "voucher": 9999, "sticker": 1}


@pytest.fixture
def catalog() -> Catalog:
    return Catalog(PRICES)


@pytest.fixture
def cart(catalog) -> Cart:
    return Cart(catalog)


@pytest.fixture
def almost_discount(cart) -> Cart:
    """A cart one cent below the discount: a voucher of 99.99."""
    cart.add("voucher")
    return cart
