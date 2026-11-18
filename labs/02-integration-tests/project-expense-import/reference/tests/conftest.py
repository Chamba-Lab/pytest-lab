"""Fixtures shared by the reference suite: a real SQLite database, a real HTTP server and CSV files."""

import sqlite3

import pytest

from expenses.rates import RatesClient
from expenses.store import ExpenseStore


@pytest.fixture(scope="session")
def httpserver_listen_address():
    return ("127.0.0.1", 0)  # localhost first tries IPv6 on Windows: half a second per request (lab 2.4)


@pytest.fixture
def store():
    conn = sqlite3.connect(":memory:")
    yield ExpenseStore(conn)
    conn.close()


@pytest.fixture
def rates(httpserver):
    return RatesClient(httpserver.url_for("/"), timeout=0.5)


@pytest.fixture
def serve_rate(httpserver):
    """serve_rate("USD", "3.75") makes the test server answer the rate of that currency."""

    def serve(currency, rate_to_pen):
        httpserver.expect_request(f"/v1/rates/{currency}").respond_with_json(
            {"currency": currency, "rate_to_pen": rate_to_pen}
        )

    return serve


@pytest.fixture
def csv_file(tmp_path):
    """csv_file(rows) writes a UTF-8 CSV with the header and returns its path."""

    def write(*rows, name="expenses.csv"):
        path = tmp_path / name
        path.write_text("\n".join(["date,description,amount,currency", *rows]) + "\n", encoding="utf-8")
        return path

    return write
