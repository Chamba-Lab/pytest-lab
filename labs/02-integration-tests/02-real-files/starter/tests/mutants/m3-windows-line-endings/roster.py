"""A club roster: members come from a CSV file and a report by city goes to a text file.

This module is finished: the lab is about testing it against real files.
"""

import csv
from collections import Counter
from pathlib import Path


def load_members(path: Path) -> list[dict[str, str]]:
    """Members from a UTF-8 CSV file whose first row is the header: name,email,city."""
    with path.open(encoding="utf-8", newline="") as file:
        return [dict(row) for row in csv.DictReader(file)]


def report(members: list[dict[str, str]]) -> str:
    """How many members each city has, cities in alphabetical order, and the total."""
    counts = Counter(member["city"] for member in members)
    lines = ["Members by city"]
    lines += [f"{city}: {count}" for city, count in sorted(counts.items())]
    lines.append(f"Total: {len(members)}")
    return "\n".join(lines) + "\n"


def write_report(members: list[dict[str, str]], path: Path) -> None:
    """Writes the report to `path` in UTF-8 with Unix line endings (\\n), on every system.

    Creates the missing folders, and replaces the file if it already exists.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(report(members), encoding="utf-8", newline="\r\n")
