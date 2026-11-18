"""Tests for scores.py, against a real SQLite database. The fixtures are in conftest.py."""

import sqlite3

import pytest

from scores import add_score, history, record_match, top


# Task 1 · A new database for every test


def test_scores_are_saved_in_order(db):
    add_score(db, "ana", 10)
    add_score(db, "ana", 4)

    assert history(db, "ana") == [10, 4]


def test_negative_points_are_rejected(db):
    with pytest.raises(sqlite3.IntegrityError):
        add_score(db, "ana", -1)


# Task 2 · Data seeded in the database


def test_top_shows_the_best_score_of_each_player(seeded_db):
    assert top(seeded_db) == [("ana", 9), ("beto", 7), ("carla", 7)]


def test_a_name_with_an_apostrophe(db):
    add_score(db, "O'Higgins", 4)

    assert history(db, "O'Higgins") == [4]


# Task 3 · All or nothing


def test_a_failed_match_saves_nothing(db):
    with pytest.raises(sqlite3.IntegrityError):
        record_match(db, {"ana": 10, "beto": -1})

    assert top(db) == []
