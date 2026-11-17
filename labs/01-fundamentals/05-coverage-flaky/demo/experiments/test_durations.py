"""Three tests with different speeds, to find the slow one with --durations."""

import time


def test_fast():
    assert sum(range(100)) == 4950


def test_a_bit_slow():
    time.sleep(0.2)


def test_slow():
    time.sleep(0.6)
