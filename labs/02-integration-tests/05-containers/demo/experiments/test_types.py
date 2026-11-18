"""Experiment 3: what each database does with a text in a number column. Run it on purpose:

    python -m pytest experiments/test_types.py
"""

import pytest


def test_age_must_be_a_number(contacts):
    with pytest.raises(Exception):  # each driver raises its own error class
        contacts.add("Beto", "veinte")
