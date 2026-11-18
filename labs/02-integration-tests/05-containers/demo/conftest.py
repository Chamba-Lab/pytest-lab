"""Fixtures for tests/ and experiments/: each test runs twice, on SQLite and on PostgreSQL in a container."""

import sqlite3

import pytest

from contacts import SCHEMA, Contacts

POSTGRES_IMAGE = "postgres:18.7-alpine"


def docker_is_running() -> bool:
    try:
        import docker  # installed with testcontainers

        docker.from_env().ping()
    except Exception:  # not installed, not running, or not reachable
        return False
    return True


@pytest.fixture(scope="session")
def postgres_url():
    """Starts one PostgreSQL container for the whole run and removes it at the end."""
    postgres = pytest.importorskip("testcontainers.community.postgres", reason="install demo/requirements.txt")
    if not docker_is_running():
        pytest.skip("Docker is not running")
    with postgres.PostgresContainer(POSTGRES_IMAGE, driver=None) as container:
        yield container.get_connection_url()


@pytest.fixture(params=["sqlite", "postgres"])
def contacts(request):
    if request.param == "sqlite":
        conn = sqlite3.connect(":memory:")
        conn.execute(SCHEMA)
        yield Contacts(conn, placeholder="?")
        conn.close()
    else:
        psycopg = pytest.importorskip("psycopg", reason="install demo/requirements.txt")
        with psycopg.connect(request.getfixturevalue("postgres_url")) as conn:
            conn.execute(SCHEMA)
            yield Contacts(conn, placeholder="%s")
            conn.rollback()  # nothing was committed: the table and its rows disappear
