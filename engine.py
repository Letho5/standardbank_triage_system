# engine.py
# Handles all communication with the Anthropic API.
# Includes retry logic, JSON validation, and graceful error handling.

import os
import json
import time
import anthropic
from dotenv import load_dotenv
from prompt import SYSTEM_PROMPT

load_dotenv()

# Initialise the Anthropic client using the API key from .env
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def triage_message(message: str, retries: int = 3, backoff: float = 2.0) -> dict:
    """
    Send a customer message to Claude and return a structured triage dict.

    Retry logic: if the API fails or returns invalid JSON, we wait
    and try again. Each wait is longer than the last (exponential backoff).
    This handles rate limits and transient API errors gracefully.

    Args:
        message:  The raw customer message string.
        retries:  How many times to retry on failure.
        backoff:  Base number of seconds to wait between retries.

    Returns:
        A dict matching the challenge output schema.
        On unrecoverable failure, returns a safe fallback dict.
    """

    # Reject empty or whitespace-only input immediately
    if not message or not message.strip():
        return _fallback("empty_input", "No message content was provided.")

    for attempt in range(1, retries + 1):
        try:
            response = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1000,
                system=SYSTEM_PROMPT,
                messages=[
                    {"role": "user", "content": message.strip()}
                ]
            )

            # Extract the text content from the response
            raw_text = response.content[0].text.strip()

            # Strip accidental markdown code fences if Claude adds them
            if raw_text.startswith("```"):
                raw_text = raw_text.split("```")[1]
                if raw_text.startswith("json"):
                    raw_text = raw_text[4:]
                raw_text = raw_text.strip()

            # Parse and validate the JSON
            result = json.loads(raw_text)
            validated = _validate(result)
            return validated

        except json.JSONDecodeError:
            # Claude returned something that isn't valid JSON
            if attempt == retries:
                return _fallback("invalid_json", "LLM returned non-JSON output after all retries.")
            time.sleep(backoff ** attempt)

        except anthropic.RateLimitError:
            # Hit the API rate limit — wait longer before retrying
            if attempt == retries:
                return _fallback("rate_limit", "API rate limit reached. Please try again later.")
            time.sleep(backoff ** attempt)

        except anthropic.APIConnectionError:
            # Network issue or API is down
            if attempt == retries:
                return _fallback("api_down", "Could not reach the Anthropic API. Check your connection.")
            time.sleep(backoff ** attempt)

        except anthropic.AuthenticationError:
            # Wrong or missing API key — no point retrying
            return _fallback("auth_error", "Invalid API key. Check your .env file.")

        except Exception as e:
            # Catch-all for unexpected errors
            if attempt == retries:
                return _fallback("unexpected_error", str(e))
            time.sleep(backoff ** attempt)


def _validate(result: dict) -> dict:
    """
    Ensure the returned JSON contains all required fields.
    If any field is missing, fill it with a safe default.
    This prevents downstream crashes if Claude omits a field.
    """
    allowed_categories = {"billing", "network", "service", "fraud", "other"}
    allowed_urgency = {"low", "medium", "high", "critical"}
    allowed_sentiment = {"positive", "neutral", "negative", "angry"}
    allowed_language = {"english", "afrikaans", "zulu", "xhosa", "mixed", "other"}

    # Sanitise enum fields — if Claude returns something unexpected, default safely
    if result.get("category") not in allowed_categories:
        result["category"] = "other"
    if result.get("urgency") not in allowed_urgency:
        result["urgency"] = "medium"
    if result.get("sentiment") not in allowed_sentiment:
        result["sentiment"] = "neutral"
    if result.get("language_detected") not in allowed_language:
        result["language_detected"] = "other"

    # Ensure summary exists and is a string
    if not isinstance(result.get("summary"), str):
        result["summary"] = "Issue received and logged."

    # Ensure key_entities exists with all four fields
    entities = result.get("key_entities", {})
    result["key_entities"] = {
        "account_number": entities.get("account_number"),
        "phone_number":   entities.get("phone_number"),
        "amount":         entities.get("amount"),
        "location":       entities.get("location"),
    }

    # Ensure suggested_response exists
    if not isinstance(result.get("suggested_response"), str):
        result["suggested_response"] = "Thank you for contacting us. An agent will be in touch shortly."

    return result


def _fallback(error_type: str, detail: str) -> dict:
    """
    Return a safe, valid triage object when the API or parsing fails.
    This ensures the tool always produces valid JSON output —
    even when everything goes wrong.
    """
    return {
        "category": "other",
        "urgency": "medium",
        "sentiment": "neutral",
        "language_detected": "other",
        "summary": f"Triage failed: {detail}",
        "key_entities": {
            "account_number": None,
            "phone_number": None,
            "amount": None,
            "location": None,
        },
        "suggested_response": "We received your message and will have an agent assist you shortly.",
        "_error": error_type,
        "_error_detail": detail
    }