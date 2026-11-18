from decimal import Decimal

import pytest

from splitbill.ledger import Expense, InputError, Transfer, balances, read_expenses, settle

HEADER = "payer,amount,participants"


def expenses(*rows: str) -> list[Expense]:
    return read_expenses([HEADER, *rows])


def amounts(**values: str) -> dict[str, Decimal]:
    return {name: Decimal(value) for name, value in values.items()}


# Reading the file


def test_reads_payer_amount_and_participants():
    assert expenses("ana, 90.00 , ana; beto ;caro") == [
        Expense("ana", Decimal("90.00"), ("ana", "beto", "caro")),
    ]


def test_blank_lines_are_ignored():
    assert len(expenses("ana,10,ana", "", "  ", "beto,5,beto")) == 2


def test_the_header_is_required():
    with pytest.raises(InputError, match="line 1: the header must be"):
        read_expenses(["ana,10,ana"])


@pytest.mark.parametrize(
    ("row", "message"),
    [
        pytest.param("ana,10", "line 2: expected 3 columns, got 2", id="missing-column"),
        pytest.param(",10,ana", "line 2: the payer is empty", id="no-payer"),
        pytest.param("ana,10.505,ana", "line 2: invalid amount '10.505'", id="three-decimals"),
        pytest.param("ana,0,ana", "line 2: amount must be positive", id="zero"),
        pytest.param("ana,10, ; ", "line 2: no participants", id="no-participants"),
        pytest.param("ana,10,ana;beto;ana", "line 2: a participant appears twice", id="duplicate"),
    ],
)
def test_invalid_rows_say_which_line(row, message):
    with pytest.raises(InputError) as error:
        expenses(row)

    assert str(error.value).startswith(message)


def test_the_line_number_counts_the_header_and_blank_lines():
    with pytest.raises(InputError, match="^line 4:"):
        expenses("ana,10,ana", "", "ana,ten,ana")


# Balances


def test_the_payer_is_owed_what_the_others_consumed():
    assert balances(expenses("ana,90.00,ana;beto;caro")) == amounts(ana="60.00", beto="-30.00", caro="-30.00")


def test_the_leftover_cent_goes_to_the_first_name_in_alphabetical_order():
    assert balances(expenses("beto,100.00,caro;beto;ana")) == amounts(ana="-33.34", beto="66.67", caro="-33.33")


def test_a_payer_who_did_not_take_part_is_owed_everything():
    assert balances(expenses("ana,25.50,beto")) == amounts(ana="25.50", beto="-25.50")


@pytest.mark.parametrize(
    "rows",
    [
        pytest.param(["ana,100.00,ana;beto;caro"], id="thirds"),
        pytest.param(["ana,10.01,ana;beto;caro", "beto,0.05,ana;caro;dani;eva"], id="odd-cents"),
        pytest.param(["ana,0.01,ana;beto", "beto,0.01,ana;beto", "caro,99.99,ana;beto;caro"], id="tiny-amounts"),
    ],
)
def test_balances_add_up_to_exactly_zero(rows):
    assert sum(balances(expenses(*rows)).values()) == 0


# Settling


def test_one_transfer_per_debtor_when_one_person_paid_everything():
    result = settle(amounts(ana="60.00", beto="-30.00", caro="-30.00"))

    assert result == [
        Transfer("beto", "ana", Decimal("30.00")),
        Transfer("caro", "ana", Decimal("30.00")),
    ]


def test_the_largest_debtor_pays_the_largest_creditor_first():
    # The largest debtor (dani) is not the first in alphabetical order, and neither is
    # the largest creditor (beto): otherwise "pick the first name" would pass too.
    result = settle(amounts(ana="10.00", beto="50.00", caro="-15.00", dani="-45.00"))

    assert result[0] == Transfer("dani", "beto", Decimal("45.00"))


def test_transfers_bring_every_balance_to_zero():
    balance = balances(expenses("ana,100.00,ana;beto;caro;dani", "beto,33.33,caro;dani", "eva,7.77,ana;eva"))
    remaining = dict(balance)

    transfers = settle(balance)
    for transfer in transfers:
        remaining[transfer.debtor] += transfer.amount
        remaining[transfer.creditor] -= transfer.amount

    assert all(value == 0 for value in remaining.values())
    assert len(transfers) <= len(balance) - 1


def test_nothing_to_settle_when_everyone_is_even():
    assert settle(amounts(ana="0.00", beto="0.00")) == []
