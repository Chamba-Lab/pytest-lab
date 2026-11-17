"""Acceptance criteria of BRIEF.md, checked from the outside: only the command line,
its output and its exit code. Each test names the criterion it checks (A1…A9).
"""

from decimal import Decimal

import pytest

HEADER = "payer,amount,participants\n"


def lines(result) -> list[str]:
    return result.stdout.splitlines()


def balances_from(result) -> dict[str, Decimal]:
    return {name: Decimal(value) for name, value in (line.split(" ") for line in lines(result))}


def test_a1_balances_of_a_shared_dinner(splitbill):
    result = splitbill("balances", HEADER + "ana,90.00,ana;beto;caro\nbeto,30.00,beto;caro\n")

    assert result.returncode == 0
    assert lines(result) == ["ana +60.00", "beto -15.00", "caro -45.00"]


def test_a2_the_leftover_cent_goes_to_the_first_name_in_alphabetical_order(splitbill):
    result = splitbill("balances", HEADER + "beto,100.00,caro;beto;ana\n")

    assert lines(result) == ["ana -33.34", "beto +66.67", "caro -33.33"]


@pytest.mark.parametrize(
    "rows",
    [
        pytest.param("ana,100.00,ana;beto;caro\n", id="thirds"),
        pytest.param("ana,10.01,ana;beto;caro\nbeto,0.05,ana;caro;dani;eva\n", id="odd-cents"),
        pytest.param("ana,0.01,ana;beto\nbeto,0.01,ana;beto\ncaro,99.99,ana;beto;caro\n", id="tiny-amounts"),
        pytest.param("".join(f"p{n},{n}.{n:02d},p1;p2;p3;p4;p5;p6;p7\n" for n in range(1, 30)), id="many-rows"),
    ],
)
def test_a3_the_balances_add_up_to_exactly_zero(splitbill, rows):
    result = splitbill("balances", HEADER + rows)

    assert result.returncode == 0
    assert sum(balances_from(result).values()) == 0


def test_a4_settling_brings_everyone_to_zero_with_few_transfers(splitbill):
    expenses = HEADER + "ana,100.00,ana;beto;caro;dani\nbeto,33.33,caro;dani\neva,7.77,ana;eva\n"
    balance = balances_from(splitbill("balances", expenses))

    result = splitbill("settle", expenses)

    assert result.returncode == 0
    for line in lines(result):
        people, amount = line.split(": ")
        debtor, creditor = people.split(" -> ")
        balance[debtor] += Decimal(amount)
        balance[creditor] -= Decimal(amount)
    assert all(value == 0 for value in balance.values())
    assert len(lines(result)) <= len(balance) - 1


@pytest.mark.parametrize(
    ("row", "message"),
    [
        pytest.param("ana,10,50,ana", "line 3", id="comma-in-amount"),
        pytest.param("ana,10.505,ana", "line 3", id="three-decimals"),
        pytest.param("ana,-5,ana", "line 3", id="negative"),
        pytest.param("ana,10,", "line 3", id="no-participants"),
    ],
)
def test_a5_invalid_input_is_rejected_with_its_line(splitbill, row, message):
    result = splitbill("balances", HEADER + "beto,5,beto\n" + row + "\n")

    assert result.returncode == 2
    assert result.stdout == ""
    assert message in result.stderr


def test_a6_a_missing_file_is_an_error(splitbill):
    result = splitbill("balances", None, file_name="nowhere.csv")

    assert result.returncode == 2
    assert result.stdout == ""
    assert result.stderr.strip() != ""


def test_a7_an_unknown_command_is_a_usage_error(splitbill):
    result = splitbill("average", HEADER + "ana,10,ana\n")

    assert result.returncode == 2
    assert result.stdout == ""


def test_a8_names_with_accents_come_out_intact(splitbill):
    result = splitbill("balances", HEADER + "maría,20.00,maría;josé\n")

    assert lines(result) == ["josé -10.00", "maría +10.00"]


def test_a9_a_file_saved_by_excel_with_a_bom_is_accepted(splitbill):
    result = splitbill("balances", HEADER + "ana,10,ana;beto\n", encoding="utf-8-sig")

    assert result.returncode == 0
    assert lines(result) == ["ana +5.00", "beto -5.00"]
