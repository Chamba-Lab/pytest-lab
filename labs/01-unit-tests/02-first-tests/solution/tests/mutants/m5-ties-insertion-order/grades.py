# MUTANT m5-ties-insertion-order: ranking() leaves ties in insertion order instead of alphabetical order.
"""Course grades on a 0-100 scale. This module is finished: the lab is about testing it."""

PASSING_GRADE = 60


def average(grades: list[float]) -> float:
    """Arithmetic mean of the grades."""
    if not grades:
        raise ValueError("grades must not be empty")
    for grade in grades:
        _check_range(grade)
    return sum(grades) / len(grades)


def passed(grade: float, passing: float = PASSING_GRADE) -> bool:
    """True when the grade reaches the passing grade (the passing grade itself passes)."""
    _check_range(grade)
    return grade >= passing


def ranking(students: dict[str, float]) -> list[str]:
    """Names from the best grade to the worst; ties in alphabetical order."""
    return sorted(students, key=lambda name: -students[name])


def _check_range(grade: float) -> None:
    if not 0 <= grade <= 100:
        raise ValueError(f"grade out of range [0, 100]: {grade}")
