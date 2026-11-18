"""Command line: `python -m splitbill balances|settle <file.csv>`."""

import argparse
import sys
from pathlib import Path

from .ledger import InputError, balances, read_expenses, settle
from .money import format_amount

EXIT_INPUT_ERROR = 2  # same code argparse uses for usage errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="splitbill", description="Split shared expenses fairly, to the cent.")
    commands = parser.add_subparsers(dest="command", required=True)
    for name, help_text in (
        ("balances", "what each person is owed (+) or owes (-)"),
        ("settle", "the transfers that settle every balance"),
    ):
        command = commands.add_parser(name, help=help_text)
        command.add_argument("file", type=Path, help="CSV file with the columns payer,amount,participants")
    args = parser.parse_args(argv)

    try:
        text = args.file.read_text(encoding="utf-8")  # utf-8-sig also accepts the BOM that Excel writes
    except FileNotFoundError:
        print(f"error: file not found: {args.file}", file=sys.stderr)
        return EXIT_INPUT_ERROR
    try:
        expenses = read_expenses(text.splitlines())
    except InputError as error:
        print(f"error: {error}", file=sys.stderr)
        return EXIT_INPUT_ERROR

    result = balances(expenses)
    if args.command == "balances":
        for name, value in result.items():
            print(f"{name} {format_amount(value)}")
    else:
        for transfer in settle(result):
            print(f"{transfer.debtor} -> {transfer.creditor}: {transfer.amount:.2f}")
    return 0
