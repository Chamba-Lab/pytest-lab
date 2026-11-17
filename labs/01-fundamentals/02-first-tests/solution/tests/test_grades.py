"""Tests for grades.py."""

import re

import pytest

from grades import average, passed, ranking


# Task 1 · The average


def test_average_of_several_grades():
    assert average([70, 85, 90]) == pytest.approx(245 / 3)


def test_average_of_decimal_grades():
    assert average([0.1, 0.2]) == pytest.approx(0.15)


# Task 2 · Errors


def test_average_of_no_grades_is_an_error():
    with pytest.raises(ValueError, match="must not be empty"):
        average([])


def test_grade_out_of_range_is_an_error():
    with pytest.raises(ValueError, match=re.escape("out of range [0, 100]")):
        average([90, 120])


# Task 3 · The boundary


def test_the_passing_grade_itself_passes():
    assert passed(60)
    assert not passed(59.9)


# Task 4 · Ties


def test_ties_are_in_alphabetical_order():
    students = {"zoe": 90, "beto": 95, "ana": 90}

    assert ranking(students) == ["beto", "ana", "zoe"]
