"""Tests for roster.py. Replace each pytest.skip(...) with a real test (see the README).

The data for the tests is already in tests/data/: members.csv and expected_report.txt.
"""

import pytest

from roster import load_members, write_report


# Task 1 · Test data next to the tests


def test_loads_every_member_from_the_file():
    pytest.skip("TODO task 1: load tests/data/members.csv; check how many members and the first one")


def test_a_quoted_name_keeps_its_comma():
    pytest.skip("TODO task 1: the second member's name has a comma inside quotes")


# Task 2 · The expected file


def test_the_report_matches_the_expected_file():
    pytest.skip("TODO task 2: write the report to a temporary file and compare it with expected_report.txt")


# Task 3 · Folders that do not exist, files that do


def test_the_report_creates_its_folders():
    pytest.skip("TODO task 3: write the report inside folders that do not exist yet")


def test_writing_twice_leaves_one_report():
    pytest.skip("TODO task 3: write the report twice to the same file")
