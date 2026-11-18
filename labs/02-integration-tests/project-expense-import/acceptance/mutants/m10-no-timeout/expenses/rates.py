"""A client for the exchange rate service: how many soles (PEN) one unit of a currency is worth."""

from decimal import Decimal

import requests


class UnknownCurrency(Exception):
    """The service does not know the currency (HTTP 404)."""


class RatesUnavailable(Exception):
    """The service could not answer: an error on its side, too slow, or not reachable."""


class RatesClient:
    def __init__(self, base_url: str, timeout: float = 2.0):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def rate_to_pen(self, currency: str) -> Decimal:
        """GET /v1/rates/<currency>; the answer is {"currency": "USD", "rate_to_pen": "3.75"}."""
        try:
            response = requests.get(f"{self.base_url}/v1/rates/{currency}")
        except (requests.Timeout, requests.ConnectionError) as error:
            raise RatesUnavailable(f"no rate for {currency}: {error}") from error
        if response.status_code == 404:
            raise UnknownCurrency(currency)
        if response.status_code != 200:
            raise RatesUnavailable(f"the rates service answered {response.status_code}")
        return Decimal(response.json()["rate_to_pen"])
