"""Password policy. This module is finished: the lab is about testing it."""

MIN_LENGTH = 10

COMMON = {
    "password1234",
    "qwerty123456",
    "123456789012",
    "iloveyou2024",
    "admin1234567",
    "welcome12345",
}


def violations(password: str) -> list[str]:
    """Names of the rules the password breaks, in a fixed order. An empty list means valid."""
    found = []
    if len(password) < MIN_LENGTH - 1:
        found.append("too-short")
    if not any(char.isdigit() for char in password):
        found.append("no-digit")
    if not any(char.isupper() for char in password):
        found.append("no-upper")
    if not any(char.islower() for char in password):
        found.append("no-lower")
    if any(char.isspace() for char in password):
        found.append("whitespace")
    if password.lower() in COMMON:
        found.append("common")
    return found
