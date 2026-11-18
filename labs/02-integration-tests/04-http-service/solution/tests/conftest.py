"""Shared fixtures for the tests of weather.py. Task 1 adds the client here."""

# --- Mutant hunt: leave this part as it is ---------------------------------
# When WEATHER_MUTANT names a folder in tests/mutants/, that folder goes first on
# the import path, so `import weather` loads the mutant. It must run before the
# imports below.
import os
import sys
from pathlib import Path

_mutant = os.environ.get("WEATHER_MUTANT")
if _mutant:
    sys.path.insert(0, str(Path(__file__).parent / "mutants" / _mutant))
# ---------------------------------------------------------------------------

import socket  # noqa: E402

import pytest  # noqa: E402

from weather import WeatherClient  # noqa: E402


@pytest.fixture(scope="session")
def httpserver_listen_address():
    """The test server listens on 127.0.0.1, on any free port. Already written: see the README."""
    return ("127.0.0.1", 0)


@pytest.fixture
def client(httpserver):
    return WeatherClient(httpserver.url_for("/"), api_key="test-key-not-secret", timeout=0.5)


@pytest.fixture
def down_url():
    """The URL of a port where nothing is listening. Already written: use it in task 3."""
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))  # the system picks a free port...
        port = sock.getsockname()[1]
    return f"http://127.0.0.1:{port}"  # ...and closing the socket leaves it with nobody listening
