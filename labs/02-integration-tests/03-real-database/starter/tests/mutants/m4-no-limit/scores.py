"""A game leaderboard kept in a SQLite database.

This module is finished: the lab is about testing it against a real database. Every
function receives an open connection, so a test can hand it a database of its own.
"""

import sqlite3

SCHEMA = """
CREATE TABLE IF NOT EXISTS scores (
    player TEXT NOT NULL,
    points INTEGER NOT NULL CHECK (points >= 0)
)
"""


def create_schema(conn: sqlite3.Connection) -> None:
    conn.execute(SCHEMA)


def add_score(conn: sqlite3.Connection, player: str, points: int) -> None:
    """Saves one score. The database rejects negative points with sqlite3.IntegrityError."""
    with conn:
        conn.execute("INSERT INTO scores (player, points) VALUES (?, ?)", (player, points))


def history(conn: sqlite3.Connection, player: str) -> list[int]:
    """Every score of a player, in the order they were saved."""
    rows = conn.execute("SELECT points FROM scores WHERE player = ? ORDER BY rowid", (player,))
    return [points for (points,) in rows]


def top(conn: sqlite3.Connection, n: int = 3) -> list[tuple[str, int]]:
    """The n players with the best single score, highest first; ties in alphabetical order."""
    rows = conn.execute(
        "SELECT player, MAX(points) AS best FROM scores"
        " GROUP BY player ORDER BY best DESC, player",
    )
    return rows.fetchall()


def record_match(conn: sqlite3.Connection, results: dict[str, int]) -> None:
    """Saves the score of every player in a match, all or nothing: if one is rejected, none is saved."""
    with conn:
        conn.executemany("INSERT INTO scores (player, points) VALUES (?, ?)", results.items())
