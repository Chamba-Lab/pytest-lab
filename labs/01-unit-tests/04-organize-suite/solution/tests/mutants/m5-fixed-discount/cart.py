"""Shopping cart. This module is finished: the lab is about testing it.

Prices are whole cents (2500 means 25.00), so every total is exact.
"""

DISCOUNT_FROM = 10_000  # from a subtotal of 100.00 on...
DISCOUNT_PERCENT = 10  # ...the cart gets 10% off


class Catalog:
    """The price of each product, in cents."""

    def __init__(self, prices: dict[str, int]):
        self._prices = dict(prices)

    def price(self, product: str) -> int:
        if product not in self._prices:
            raise ValueError(f"unknown product: {product}")
        return self._prices[product]


class Cart:
    def __init__(self, catalog: Catalog):
        self.catalog = catalog
        self.items: dict[str, int] = {}

    def add(self, product: str, quantity: int = 1) -> None:
        """Adds units of a product. Unknown products and quantities below 1 are rejected."""
        if quantity < 1:
            raise ValueError(f"quantity must be at least 1: {quantity}")
        self.catalog.price(product)  # raises ValueError for an unknown product
        self.items[product] = self.items.get(product, 0) + quantity

    def subtotal(self) -> int:
        return sum(self.catalog.price(product) * quantity for product, quantity in self.items.items())

    def discount(self) -> int:
        """10% of the subtotal, rounded down to the cent, once the subtotal reaches 100.00."""
        subtotal = self.subtotal()
        if subtotal >= DISCOUNT_FROM:
            return DISCOUNT_FROM * DISCOUNT_PERCENT // 100
        return 0

    def total(self) -> int:
        return self.subtotal() - self.discount()
