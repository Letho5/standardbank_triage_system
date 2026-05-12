# display.py
# Formats and prints the triage result to the terminal.
# Uses the rich library for colour-coded, readable output.

import json
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box
from rich.text import Text

console = Console()

# Colour mapping for urgency levels
URGENCY_COLOURS = {
    "critical": "bold red",
    "high":     "bold yellow",
    "medium":   "bold blue",
    "low":      "dim white",
}

# Colour mapping for sentiment
SENTIMENT_COLOURS = {
    "angry":    "bold red",
    "negative": "yellow",
    "neutral":  "white",
    "positive": "bold green",
}


def print_result(result: dict, message: str = None) -> None:
    """
    Print a fully formatted triage result to the terminal.
    """

    urgency   = result.get("urgency", "medium")
    sentiment = result.get("sentiment", "neutral")
    category  = result.get("category", "other")
    language  = result.get("language_detected", "other")
    summary   = result.get("summary", "")
    entities  = result.get("key_entities", {})
    response  = result.get("suggested_response", "")
    error     = result.get("_error")

    # Print the original message if provided
    if message:
        console.print(
            Panel(message, title="[dim]Incoming message[/dim]", border_style="dim", expand=False)
        )

    # Alert banner if there was a triage error
    if error:
        console.print(f"\n[bold red]⚠ Triage error:[/bold red] {result.get('_error_detail', '')}\n")

    # Urgency header — the most important signal, shown first
    urgency_colour = URGENCY_COLOURS.get(urgency, "white")
    console.print(f"\n[{urgency_colour}]▶ URGENCY: {urgency.upper()}[/{urgency_colour}]")

    # Core classification table
    table = Table(box=box.SIMPLE, show_header=False, padding=(0, 2))
    table.add_column("Field", style="dim", width=20)
    table.add_column("Value")

    table.add_row("Category",  category)
    table.add_row("Sentiment", Text(sentiment, style=SENTIMENT_COLOURS.get(sentiment, "white")))
    table.add_row("Language",  language)
    table.add_row("Summary",   summary)

    console.print(table)

    # Entities section
    console.print("[dim]── Extracted entities ──────────────────────────[/dim]")
    for key, value in entities.items():
        label = key.replace("_", " ").title()
        val_display = str(value) if value else "[dim]none[/dim]"
        console.print(f"  [dim]{label:<16}[/dim] {val_display}")

    # Suggested response
    console.print(
        Panel(
            response,
            title="[green]Suggested first response[/green]",
            border_style="green",
        )
    )


def print_json(result: dict) -> None:
    """
    Print the raw JSON output — used when --json flag is passed.
    """
    # Remove internal error fields before printing clean output
    clean = {k: v for k, v in result.items() if not k.startswith("_")}
    console.print_json(json.dumps(clean, indent=2))