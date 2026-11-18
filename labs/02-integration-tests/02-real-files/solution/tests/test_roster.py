"""Tests for roster.py, against real files: data next to the tests and an expected report."""

from pathlib import Path

from roster import load_members, write_report

DATA = Path(__file__).parent / "data"  # the folder of this file, wherever pytest runs from


# Task 1 · Test data next to the tests


def test_loads_every_member_from_the_file():
    members = load_members(DATA / "members.csv")

    assert len(members) == 7
    assert members[0] == {"name": "José Pérez", "email": "jose@example.com", "city": "Lima"}


def test_a_quoted_name_keeps_its_comma():
    members = load_members(DATA / "members.csv")

    assert members[1] == {"name": "Quispe, Ñusta", "email": "nusta@example.com", "city": "Cusco"}


# Task 2 · The expected file


def test_the_report_matches_the_expected_file(tmp_path):
    output = tmp_path / "report.txt"

    write_report(load_members(DATA / "members.csv"), output)

    assert output.read_bytes() == (DATA / "expected_report.txt").read_bytes()


# Task 3 · Folders that do not exist, files that do


def test_the_report_creates_its_folders(tmp_path):
    output = tmp_path / "reports" / "2026" / "report.txt"

    write_report(load_members(DATA / "members.csv"), output)

    assert output.read_bytes() == (DATA / "expected_report.txt").read_bytes()


def test_writing_twice_leaves_one_report(tmp_path):
    output = tmp_path / "report.txt"
    members = load_members(DATA / "members.csv")

    write_report(members, output)
    write_report(members, output)

    assert output.read_bytes() == (DATA / "expected_report.txt").read_bytes()
