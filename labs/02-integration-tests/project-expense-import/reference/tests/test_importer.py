"""The importer with everything real: a CSV file, the SQLite store and the rates server."""

import shutil
from datetime import date
from decimal import Decimal
from pathlib import Path

import pytest

from expenses.importer import DuplicateImport, ImportFailed, import_file
from expenses.rates import RatesUnavailable
from expenses.store import Expense

DATA = Path(__file__).parent / "data"


def test_imports_every_row_converted_to_soles(store, rates, serve_rate):
    serve_rate("USD", "3.70")

    count = import_file(DATA / "trip.csv", store, rates)

    assert count == 4
    assert store.expenses() == [
        Expense(date(2026, 11, 2), "Hotel en Cusco", Decimal("32.00"), "USD", Decimal("118.40")),
        Expense(date(2026, 11, 2), "Café y pan", Decimal("18.50"), "PEN", Decimal("18.50")),
        # 1.25 × 3.70 = 4.625: a half cent rounds up
        Expense(date(2026, 11, 3), "Agua", Decimal("1.25"), "USD", Decimal("4.63")),
        Expense(date(2026, 11, 4), "Entrada a Machu Picchu", Decimal("152.00"), "PEN", Decimal("152.00")),
    ]


def test_asks_for_each_currency_only_once(httpserver, store, rates, serve_rate):
    serve_rate("USD", "3.70")

    import_file(DATA / "trip.csv", store, rates)  # two rows in USD

    assert len(httpserver.log) == 1


def test_soles_need_no_rate(httpserver, store, rates, csv_file):
    path = csv_file("2026-11-02,Menú,15.00,PEN", "2026-11-03,Combi,2.50,PEN")

    assert import_file(path, store, rates) == 2
    assert httpserver.log == []


def test_an_invalid_line_saves_nothing_and_says_which(store, rates, serve_rate, csv_file):
    serve_rate("USD", "3.70")
    path = csv_file("2026-11-02,Hotel,32.00,USD", "2026-11-03,Cena,12.345,PEN")

    with pytest.raises(ImportFailed, match=r"^line 3: invalid amount"):
        import_file(path, store, rates)
    assert store.expenses() == []


def test_a_failed_rate_saves_nothing(httpserver, store, rates, serve_rate, csv_file):
    serve_rate("USD", "3.70")
    httpserver.expect_request("/v1/rates/EUR").respond_with_data("internal error", status=500)
    path = csv_file("2026-11-02,Hotel,32.00,USD", "2026-11-03,Museo,10.00,EUR")

    with pytest.raises(RatesUnavailable):  # the importer lets the client's error through
        import_file(path, store, rates)
    assert store.expenses() == []


def test_a_failed_import_can_be_tried_again(httpserver, store, rates, serve_rate):
    httpserver.expect_oneshot_request("/v1/rates/USD").respond_with_data("busy", status=503)
    serve_rate("USD", "3.70")  # used after the one-shot answer

    with pytest.raises(RatesUnavailable):
        import_file(DATA / "trip.csv", store, rates)
    assert import_file(DATA / "trip.csv", store, rates) == 4


def test_the_same_file_twice_is_a_duplicate(store, rates, serve_rate):
    serve_rate("USD", "3.70")
    import_file(DATA / "trip.csv", store, rates)

    with pytest.raises(DuplicateImport):
        import_file(DATA / "trip.csv", store, rates)
    assert len(store.expenses()) == 4


def test_a_copy_with_another_name_is_a_duplicate(store, rates, serve_rate, tmp_path):
    serve_rate("USD", "3.70")
    copy = tmp_path / "trip-copy.csv"
    shutil.copy(DATA / "trip.csv", copy)
    import_file(DATA / "trip.csv", store, rates)

    with pytest.raises(DuplicateImport):
        import_file(copy, store, rates)
