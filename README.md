# Challenge 2: Build an LLM-Powered Tool

## The Scenario

Your team needs a **Customer Support Ticket Triage System**. It takes raw, unstructured customer messages and produces structured output that can be fed into a ticketing system.

Your job: **build a working CLI tool that does this.**

---

A working MVP that handles the basic cases is better than a perfect system that doesn't run.

---

## Requirements

### Input
Your tool must accept a customer message as text input (via CLI argument, stdin, or a simple file).

### Output
For each message, produce a **JSON object** with:

```json
{
  "category": "billing | network | service | fraud | other",
  "urgency": "low | medium | high | critical",
  "sentiment": "positive | neutral | negative | angry",
  "language_detected": "english | afrikaans | zulu | xhosa | mixed | other",
  "summary": "One sentence summary of the issue (max 50 words)",
  "key_entities": {
    "account_number": "extracted or null",
    "phone_number": "extracted or null",
    "amount": "extracted or null",
    "location": "extracted or null"
  },
  "suggested_response": "A brief, empathetic first-response to the customer (2-3 sentences)"
}
```

### Functional Requirements

1. **Must use an LLM API** — Any provider is fine (OpenAI, Anthropic, Groq, Ollama, etc.). Free tiers are acceptable.
2. **Must handle these cases:**
   - Standard English complaints
   - Messages with South African slang ("eish", "shame", "just now", "load shedding")
   - Mixed-language messages (English + Afrikaans/Zulu phrases)
   - Angry/abusive messages (should still produce valid output)
   - Very short messages ("my airtime is gone")
   - Very long, rambling messages
3. **Must include error handling:**
   - What happens if the LLM returns invalid JSON?
   - What happens if the API is down or rate-limited?
   - What happens if the input is empty or nonsensical?
4. **Must include a test suite** — At least 5 test cases that demonstrate your tool works. Use the provided sample tickets as a starting point.

### Non-Functional Requirements

- Must run from the command line
- Must have a README with setup instructions
- Must work with a single `pip install` + API key setup
- Code should be readable (comments where needed, clear function names)

---

## Provided Test Inputs

See `test_inputs/sample_tickets.json` for 10 sample messages to test against. Your tool should handle ALL of these correctly.

You should also create your own additional test cases.

---

## What We're Evaluating

| Criteria | What we're looking for |
|----------|----------------------|
| Does it work? | Runs, produces valid JSON output for all test cases |
| Output quality | Correct categorisation, accurate summaries, appropriate responses |
| Error handling | Graceful behaviour when things go wrong (bad input, API failures, invalid responses) |
| Prompt design | Thoughtful, iterated prompt engineering — not just "classify this text" |
| Code quality | Readable, documented, sensible structure |
| Prompt log | How did you iterate on your solution? How did you test and refine? |

> Remember: you'll walk us through your submission in an interview. Make sure you can explain your prompt design decisions and demonstrate your tool live.

---

## Tips

- Start with the simplest possible version that works, then improve
- Your prompt design is the most important part — iterate on it
- Test with the provided samples EARLY, not at the end
- Handle the LLM returning garbage gracefully (it will happen)
- You don't need a fancy UI — a CLI script is perfect
- If you can't get an API key, using Ollama locally is fine

---

## Constraints

- **No web frameworks required** — a simple Python script is fine
- **No database required** — process one message at a time
- **Budget:** Use free-tier APIs only. Don't spend money on this.
- **Language:** Python preferred, but any language is acceptable.

---

## Bonus (Not Required)

- Batch processing (handle multiple tickets from a file)
- Confidence scores for categorization
- Retry logic with exponential backoff
- Prompt versioning (show how you iterated on your prompts)
- Unit tests that mock the LLM API
