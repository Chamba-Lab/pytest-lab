"""A test that depends on the iteration order of a set of strings."""


def unique_tags(tags: list[str]) -> list[str]:
    return list(set(tags))


def test_unique_tags():
    assert unique_tags(["python", "pytest", "testing", "python"]) == ["python", "pytest", "testing"]
