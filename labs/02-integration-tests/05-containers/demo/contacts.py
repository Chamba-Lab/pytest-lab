"""Contacts kept in a SQL database. Finished: the lab runs the same tests on SQLite and on PostgreSQL.

Contacts receives an open connection (sqlite3 or psycopg) and the placeholder its
driver uses for parameters: sqlite3 writes `?`, psycopg writes `%s`.
"""

SCHEMA = "CREATE TABLE contacts (name TEXT NOT NULL, age INTEGER NOT NULL)"


class Contacts:
    def __init__(self, conn, placeholder: str = "?"):
        self.conn = conn
        self.p = placeholder

    def add(self, name: str, age: int) -> None:
        self.conn.execute(f"INSERT INTO contacts (name, age) VALUES ({self.p}, {self.p})", (name, age))

    def search(self, text: str) -> list[str]:
        """Names that contain `text`, ignoring upper and lower case, in alphabetical order."""
        rows = self.conn.execute(
            f"SELECT name FROM contacts WHERE lower(name) LIKE lower({self.p}) ORDER BY name",
            (f"%{text}%",),
        )
        return [name for (name,) in rows]
