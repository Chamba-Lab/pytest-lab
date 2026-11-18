"""The rates client against a real HTTP server (pytest-httpserver)."""

import socket
from decimal import Decimal

import pytest
from pytest_httpserver.hooks import Delay

from expenses.rates import RatesClient, RatesUnavailable, UnknownCurrency


def test_reads_the_rate_as_an_exact_decimal(rates, serve_rate):
    serve_rate("USD", "3.7512")

    assert rates.rate_to_pen("USD") == Decimal("3.7512")


def test_an_unknown_currency_is_not_found(httpserver, rates):
    httpserver.expect_request("/v1/rates/XYZ").respond_with_data("unknown currency", status=404)

    with pytest.raises(UnknownCurrency):
        rates.rate_to_pen("XYZ")


def test_a_server_error_means_unavailable(httpserver, rates):
    httpserver.expect_request("/v1/rates/USD").respond_with_data("internal error", status=500)

    with pytest.raises(RatesUnavailable):
        rates.rate_to_pen("USD")
    httpserver.check_assertions()


def test_a_slow_service_means_unavailable(httpserver, rates):
    httpserver.expect_request("/v1/rates/USD").with_post_hook(Delay(1.5)).respond_with_json(
        {"currency": "USD", "rate_to_pen": "3.75"}
    )

    with pytest.raises(RatesUnavailable):
        rates.rate_to_pen("USD")


def test_a_service_that_is_down_means_unavailable():
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        port = sock.getsockname()[1]  # closed again when the block ends: nobody listens there

    with pytest.raises(RatesUnavailable):
        RatesClient(f"http://127.0.0.1:{port}", timeout=0.5).rate_to_pen("USD")
