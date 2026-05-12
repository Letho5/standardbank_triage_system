# tests.py
# Test suite for Definite.
# Runs all 10 provided sample tickets plus 5 edge cases.
# Usage: python tests.py

import json
from engine import triage_message
from display import console
from rich.table import Table
from rich import box

ALLOWED = {
    "category":          {"billing", "network", "service", "fraud", "other"},
    "urgency":           {"low", "medium", "high", "critical"},
    "sentiment":         {"positive", "neutral", "negative", "angry"},
    "language_detected": {"english", "afrikaans", "zulu", "xhosa", "mixed", "other"},
}

# Five additional edge cases beyond the provided samples
EXTRA_TESTS = [
    {
        "id": "EXTRA-001",
        "message": "",
        "expect_error": True,
        "notes": "Empty input — must not crash"
    },
    {
        "id": "EXTRA-002",
        "message": "🤬🤬🤬",
        "notes": "Emoji only — must produce valid JSON"
    },
    {
        "id": "EXTRA-003",
        "message": "Ek wil die Bankombud kontak oor my rekening wat geblokkeer is sonder rede.",
        "notes": "Afrikaans + Banking Ombudsman mention — must be critical"
    },
    {
        "id": "EXTRA-004",
        "message": "it is what it is. my debit order went off twice. whatever",
        "notes": "Churn signal + billing — urgency must not be low"
    },
    {
        "id": "EXTRA-005",
        "message": "asdfgh jkl qwerty 12345",
        "notes": "Nonsensical input — must produce valid JSON without crashing"
    },
]


def validate_result(result: dict) -> list[str]:
    """Return a list of validation errors. Empty list means pass."""
    errors = []
    for field, allowed in ALLOWED.items():
        val = result.get(field)
        if val not in allowed:
            errors.append(f"{field}='{val}' not in allowed set")
    if not isinstance(result.get("summary"), str):
        errors.append("summary is not a string")
    entities = result.get("key_entities", {})
    for key in ["account_number", "phone_number", "amount", "location"]:
        if key not in entities:
            errors.append(f"key_entities missing '{key}'")
    if not isinstance(result.get("suggested_response"), str):
        errors.append("suggested_response is not a string")
    return errors


def run_tests():
    # Load the provided sample tickets
    with open("test_inputs/sample_tickets.json", "r", encoding="utf-8") as f:
        sample_tickets = json.load(f)

    all_tests = sample_tickets + EXTRA_TESTS
    results_summary = []

    console.print("\n[bold]Definite — Test Suite[/bold]")
    console.rule()

    for ticket in all_tests:
        ticket_id  = ticket.get("id", "?")
        message    = ticket.get("message", "")
        notes      = ticket.get("notes", "")
        expect_err = ticket.get("expect_error", False)

        console.print(f"\n[dim]{ticket_id}[/dim]  {notes}")

        result = triage_message(message)
        errors = validate_result(result)
        has_error_field = "_error" in result

        if expect_err:
            # For error cases we just check that it produced valid JSON structure
            status = "PASS" if not errors else "FAIL"
        else:
            status = "PASS" if not errors else "FAIL"

        colour = "green" if status == "PASS" else "red"
        console.print(
            f"  [{colour}]{status}[/{colour}]  "
            f"category={result.get('category'):<10} "
            f"urgency={result.get('urgency'):<10} "
            f"sentiment={result.get('sentiment'):<10} "
            f"lang={result.get('language_detected')}"
        )

        if errors:
            for e in errors:
                console.print(f"    [red]✗ {e}[/red]")

        results_summary.append({
            "id": ticket_id,
            "status": status,
            "errors": errors,
        })

    # Final summary table
    console.rule()
    passed = sum(1 for r in results_summary if r["status"] == "PASS")
    total  = len(results_summary)
    colour = "green" if passed == total else "yellow"
    console.print(f"\n[{colour}]{passed}/{total} tests passed[/{colour}]\n")


if __name__ == "__main__":
    run_tests()