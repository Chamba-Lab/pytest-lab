"""A client for a weather service over HTTP.

This module is finished: the lab is about testing it against a real HTTP server.
The base URL, the API key and the timeout come from outside, so a test can point
the client to a server of its own.
"""

from dataclasses import dataclass

import requests


class CityNotFound(Exception):
    """The service does not know the city (HTTP 404)."""


class WeatherUnavailable(Exception):
    """The service could not answer: an error on its side, too slow, or not reachable."""


@dataclass(frozen=True)
class Reading:
    city: str
    celsius: float


class WeatherClient:
    def __init__(self, base_url: str, api_key: str, timeout: float = 2.0):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.timeout = timeout

    def current(self, city: str) -> Reading:
        """GET /v1/current?city=<city> with the X-Api-Key header; the answer is {"city": ..., "temp_c": ...}."""
        response = requests.get(
            f"{self.base_url}/v1/current",
            params={"city": city},
            headers={"X-Api-Key": self.api_key},
            timeout=self.timeout,
        )
        if response.status_code == 404:
            raise CityNotFound(city)
        if response.status_code != 200:
            raise WeatherUnavailable(f"the service answered {response.status_code}")
        data = response.json()
        return Reading(city=data["city"], celsius=data["temp_c"])
