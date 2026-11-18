"""Your tests for grades.py. Replace each pytest.skip(...) with a real test (see the README)."""

import pytest

from grades import average, passed, ranking


# Task 1 · The average


def test_average_of_several_grades():
    pytest.skip("TODO task 1: average([70, 85, 90])")


def test_average_of_decimal_grades():
    pytest.skip("TODO task 1: average([0.1, 0.2]) is 0.15")


# Task 2 · Errors


def test_average_of_no_grades_is_an_error():
    pytest.skip("TODO task 2: average([]) raises ValueError")


def test_grade_out_of_range_is_an_error():
    pytest.skip("TODO task 2: a grade above 100 raises ValueError with the right message")


# Task 3 · The boundary


def test_the_passing_grade_itself_passes():
    pytest.skip("TODO task 3: 60 passes, just below 60 does not")


# Task 4 · Ties


def test_ties_are_in_alphabetical_order():
    pytest.skip("TODO task 4: students with the same grade come in alphabetical order")
