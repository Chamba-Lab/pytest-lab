"""The same tests, on SQLite and on PostgreSQL (see the `contacts` fixture in conftest.py)."""


def test_search_finds_part_of_a_name(contacts):
    contacts.add("Ana Torres", 31)
    contacts.add("Luis Rojas", 28)

    assert contacts.search("Torres") == ["Ana Torres"]


def test_search_ignores_case(contacts):
    contacts.add("Ana Torres", 31)

    assert contacts.search("ana") == ["Ana Torres"]


def test_each_test_starts_empty(contacts):
    assert contacts.search("") == []
