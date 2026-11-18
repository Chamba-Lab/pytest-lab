"""The command line, called in-process through main(), with a temporary file and captured output.

The exit codes are part of the contract, so they are written as literals (2), not as the
constant the code uses: a test that compares with the same constant changes along with it.
"""

import pytest

from splitbill.cli import main


@pytest.fixture
def csv_file(tmp_path):
    def write(*rows: str, encoding: str = "utf-8"):
        path = tmp_path / "expenses.csv"
        path.write_text("\n".join(["payer,amount,participants", *rows]) + "\n", encoding=encoding)
        return path

    return write


def test_balances_one_line_per_person_sorted_by_name(csv_file, capsys):
    exit_code = main(["balances", str(csv_file("caro,30,ana;caro", "ana,10,ana;beto"))])

    assert exit_code == 0
    assert capsys.readouterr().out.splitlines() == ["ana -10.00", "beto -5.00", "caro +15.00"]


def test_settle_prints_the_transfers(csv_file, capsys):
    exit_code = main(["settle", str(csv_file("ana,90,ana;beto;caro"))])

    assert exit_code == 0
    assert capsys.readouterr().out.splitlines() == ["beto -> ana: 30.00", "caro -> ana: 30.00"]


def test_an_invalid_row_is_an_input_error_on_stderr(csv_file, capsys):
    exit_code = main(["balances", str(csv_file("ana,10,ana", "beto,10,50,beto"))])

    output = capsys.readouterr()
    assert exit_code == 2
    assert output.out == ""
    assert output.err.startswith("error: line 3: expected 3 columns, got 4")


def test_a_missing_file_is_an_input_error(tmp_path, capsys):
    exit_code = main(["balances", str(tmp_path / "nowhere.csv")])

    assert exit_code == 2
    assert "file not found" in capsys.readouterr().err


def test_a_file_saved_by_excel_with_a_bom_is_accepted(csv_file, capsys):
    exit_code = main(["balances", str(csv_file("ana,10,ana;beto", encoding="utf-8-sig"))])

    assert exit_code == 0
    assert capsys.readouterr().out.splitlines() == ["ana +5.00", "beto -5.00"]


def test_an_unknown_command_is_a_usage_error(capsys):
    with pytest.raises(SystemExit) as stop:
        main(["average", "expenses.csv"])

    assert stop.value.code == 2
    assert "invalid choice" in capsys.readouterr().err
