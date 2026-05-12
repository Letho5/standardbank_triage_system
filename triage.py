# triage.py
# CLI entry point for Definite — Standard Bank Ticket Triage Engine.
# Usage:
#   python triage.py --message "my airtime is gone"
#   python triage.py --file test_inputs/sample_tickets.json
#   python triage.py --message "..." --json
#   echo "help me" | python triage.py

import sys
import json
import argparse
from engine import triage_message
from display import print_result, print_json, console


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="triage",
        description="Definite — Ticket Triage Engine for Standard Bank SA",
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--message", "-m",
        type=str,
        help="A customer message string passed directly on the command line.",
    )
    group.add_argument(
        "--file", "-f",
        type=str,
        help="Path to a JSON file containing an array of ticket objects (sample_tickets.json format).",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output raw JSON only — no formatting. Useful for piping into other tools.",
    )
    return parser


def run_single(message: str, as_json: bool) -> None:
    """Triage a single message and display the result."""
    result = triage_message(message)
    if as_json:
        print_json(result)
    else:
        print_result(result, message=message)


def run_batch(filepath: str, as_json: bool) -> None:
    """
    Triage all tickets in a JSON file.
    Expects an array of objects with at least a 'message' field.
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            tickets = json.load(f)
    except FileNotFoundError:
        console.print(f"[bold red]Error:[/bold red] File not found: {filepath}")
        sys.exit(1)
    except json.JSONDecodeError:
        console.print(f"[bold red]Error:[/bold red] {filepath} is not valid JSON.")
        sys.exit(1)

    if not isinstance(tickets, list):
        console.print("[bold red]Error:[/bold red] Expected a JSON array of ticket objects.")
        sys.exit(1)

    for i, ticket in enumerate(tickets, start=1):
        ticket_id  = ticket.get("id", f"#{i}")
        message    = ticket.get("message", "")

        if not as_json:
            console.rule(f"[dim]Ticket {ticket_id}[/dim]")

        if not message.strip():
            console.print(f"[yellow]Skipping {ticket_id} — empty message.[/yellow]")
            continue

        result = triage_message(message)

        if as_json:
            print_json(result)
        else:
            print_result(result, message=message)

    if not as_json:
        console.rule("[dim]End of batch[/dim]")


def main():
    parser = build_parser()
    args = parser.parse_args()

    # Check if input is being piped via stdin
    if not sys.stdin.isatty() and not args.message and not args.file:
        message = sys.stdin.read().strip()
        run_single(message, args.json)

    elif args.message:
        run_single(args.message, args.json)

    elif args.file:
        run_batch(args.file, args.json)

    else:
        parser.print_help()
        sys.exit(0)


if __name__ == "__main__":
    main()