"""Your fixtures go here. The first one is already written (see BRIEF.md)."""

import pytest


@pytest.fixture(scope="session")
def httpserver_listen_address():
    return ("127.0.0.1", 0)  # localhost first tries IPv6 on Windows: half a second per request (lab 2.4)
