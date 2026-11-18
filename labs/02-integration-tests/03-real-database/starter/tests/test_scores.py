"""Tests for scores.py. Replace each pytest.skip(...) with a real test (see the README).

When a test needs a fixture, add it as a parameter: def test_x(db): ...
"""

import sqlite3

import pytest

from scores import add_score, history, record_match, top


# Task 1 · A new database for every test


def test_scores_are_saved_in_order():
    pytest.skip("TODO task 1: save two scores of a player and read them back with history()")


def test_negative_points_are_rejected():
    pytest.skip("TODO task 1: the database rejects a negative score")


# Task 2 · Data seeded in the database


def test_top_shows_the_best_score_of_each_player():
    pytest.skip("TODO task 2: top() over the seeded scores")


def test_a_name_with_an_apostrophe():
    pytest.skip("TODO task 2: save and read the scores of O'Higgins")


# Task 3 · All or nothing


def test_a_failed_match_saves_nothing():
    pytest.skip("TODO task 3: a match with one rejected score leaves the database as it was")
