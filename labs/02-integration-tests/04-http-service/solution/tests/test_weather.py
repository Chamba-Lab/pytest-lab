"""Tests for weather.py, against a real HTTP server on this machine (pytest-httpserver)."""

import pytest
from pytest_httpserver.hooks import Delay

from weather import CityNotFound, Reading, WeatherClient, WeatherUnavailable


# Task 1 · A local test server


def test_reads_the_current_weather(httpserver, client):
    httpserver.expect_request(
        "/v1/current", query_string={"city": "Lima"}, headers={"X-Api-Key": client.api_key}
    ).respond_with_json({"city": "Lima", "temp_c": 19.5})

    assert client.current("Lima") == Reading(city="Lima", celsius=19.5)


# Task 2 · HTTP errors


def test_an_unknown_city_is_not_found(httpserver, client):
    httpserver.expect_request("/v1/current").respond_with_data("unknown city", status=404)

    with pytest.raises(CityNotFound):
        client.current("Atlantis")


def test_a_server_error_means_unavailable(httpserver, client):
    httpserver.expect_request("/v1/current").respond_with_data("internal error", status=500)

    with pytest.raises(WeatherUnavailable):
        client.current("Lima")
    httpserver.check_assertions()  # fails if the request matched no expectation


# Task 3 · Slow and down


def test_a_slow_service_times_out(httpserver, client):
    httpserver.expect_request("/v1/current").with_post_hook(Delay(1.5)).respond_with_json(
        {"city": "Lima", "temp_c": 19.5}
    )

    with pytest.raises(WeatherUnavailable):
        client.current("Lima")


def test_a_service_that_is_down_is_unavailable(down_url):
    client = WeatherClient(down_url, api_key="test-key-not-secret", timeout=0.5)

    with pytest.raises(WeatherUnavailable):
        client.current("Lima")
