"""Tests for weather.py. Replace each pytest.skip(...) with a real test (see the README).

When a test needs a fixture, add it as a parameter: def test_x(httpserver, client): ...
"""

import pytest

from weather import CityNotFound, Reading, WeatherClient, WeatherUnavailable


# Task 1 · A local test server


def test_reads_the_current_weather():
    pytest.skip("TODO task 1: the server expects the right request and answers with JSON")


# Task 2 · HTTP errors


def test_an_unknown_city_is_not_found():
    pytest.skip("TODO task 2: the server answers 404")


def test_a_server_error_means_unavailable():
    pytest.skip("TODO task 2: the server answers 500")


# Task 3 · Slow and down


def test_a_slow_service_times_out():
    pytest.skip("TODO task 3: the server takes longer than the client's timeout")


def test_a_service_that_is_down_is_unavailable():
    pytest.skip("TODO task 3: point a client at down_url")
