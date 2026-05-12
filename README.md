# Definite

> An LLM-powered triage engine that turns raw customer support messages into structured tickets — built for South Africa's multilingual banking and telecoms reality.

Standard Bank Internship Challenge 2 · Submitted by Lethukuthula Mthiyane

---

## The Problem

When a customer messages a bank, that message arrives raw — three words or three paragraphs, in any of South Africa's official languages, often code-switched, sometimes furious. A human agent currently has to read every single one, decide what it's about, judge how urgent it is, and route it to the right team. Critical cases get buried under routine ones. Angry customers wait while their message sits in a queue.

Definite is the first brain that reads every incoming message before a human touches it. By the time an agent opens a ticket, the category is identified, the urgency is assessed, the key details are extracted, and a warm first response is already drafted in the customer's language.

It does not replace human empathy. It makes sure that empathy reaches the right person at the right time.

---

## Example

**Input:**
Sawubona, ngicela usizo. I-account yami i-blocked and I can't buy
bundles. I went to the store in Umlazi but they said I must call.
Angazi what to do anymore. My number is 0734567890.

**Output:**
```json
{
  "category": "service",
  "urgency": "high",
  "sentiment": "negative",
  "language_detected": "mixed",
  "summary": "Customer's account is blocked preventing bundle purchases, unable to get help from Umlazi store or call centre.",
  "key_entities": {
    "account_number": null,
    "phone_number": "0734567890",
    "amount": null,
    "location": "Umlazi"
  },
  "suggested_response": "Sawubona! I'm sorry to hear about your blocked account and the frustration with getting help. Let me assist you right away with unblocking your account so you can purchase bundles again."
}
```

Notice the response opens in Zulu — meeting the customer where they are.

---

## Quick Start

```bash
git clone https://github.com/Letho5/standardbank_triage_system.git
cd standardbank_triage_system

python -m venv venv
venv\Scripts\activate         # Windows
source venv/bin/activate      # macOS / Linux

pip install -r requirements.txt
```

Create a `.env` file in the project root with your Anthropic API key:
ANTHROPIC_API_KEY=your_key_here

That's it. You're ready to triage.

---

## Usage

| Command | What it does |
|---|---|
| `python triage.py --message "..."` | Triage a single message |
| `python triage.py --file test_inputs/sample_tickets.json` | Process a batch of tickets |
| `echo "..." \| python triage.py` | Read message from stdin |
| `python triage.py --message "..." --json` | Output raw JSON for piping |
| `python tests.py` | Run the full test suite (15 cases) |

---
## How It Works

```
┌──────────────────┐     ┌─────────────────┐     ┌──────────────────┐
│  Raw customer    │ ──▶ │  System prompt  │ ──▶ │  Validated JSON  │
│     message      │     │   + Claude API  │     │     ticket       │
└──────────────────┘     └─────────────────┘     └──────────────────┘
                                                          │
                                                          ▼
                                                 ┌──────────────────┐
                                                 │  Rich terminal   │
                                                 │     output       │
                                                 └──────────────────┘
```

Each module has one responsibility:

| File | Responsibility |
|---|---|
| `prompt.py` | System prompt — SA context, urgency rules, output schema, bias guards |
| `engine.py` | Anthropic API call, exponential backoff retry, JSON validation, fallback handling |
| `display.py` | Terminal output formatting with `rich` — colour-coded urgency, structured panels |
| `triage.py` | CLI entry point — argparse, stdin handling, batch dispatch |
| `tests.py` | 10 provided sample tickets + 5 edge cases — validates every output structurally |

Swapping LLM providers means changing one file. Adding a new output format means changing one file. The prompt is iterable in seconds without risk to the API logic.

---

## What Makes the Prompt Work

The system prompt has six deliberate layers, each addressing a specific failure mode:

- **Role declaration** — anchors Claude as a South African banking triage engine
- **Cultural context** — fills in what training data misses ("just now" doesn't mean now, "eish" signals frustration, load shedding is not the customer's fault)
- **Escalation triggers** — hardcoded overrides for ICASA, Ombudsman, Tribunal mentions, fraud language, ALL CAPS
- **Bias guard** — explicitly forbids downgrading urgency for informal, Zulu, Afrikaans, or short messages
- **Security rule** — full account and card numbers may never appear in the suggested response
- **Output schema** — strict JSON, no preamble, no markdown fences

> The bias guard is the most important section. Without it, models systematically deprioritise informal English and African-language messages — exactly the customers a South African bank needs to serve well.

---

## Error Handling

The tool handles four documented failure modes without ever crashing:

| Failure | Behaviour |
|---|---|
| Empty or whitespace-only input | Returns a fallback immediately — no API call wasted |
| LLM returns invalid JSON | Retries up to 3 times with exponential backoff (2s, 4s, 8s) |
| API rate limit hit | Same retry pattern — gives the limit time to reset |
| API down or auth failure | Returns a structured fallback with diagnostic detail |

Whatever happens, the output is always a valid JSON object that downstream systems can consume.

---

## Test Coverage

**15 / 15 tests passing.**

Ten provided tickets cover the documented cases — billing, network, fraud, service, compliments, and rambling messages. Five additional edge cases stress the system:

- Empty input
- Emoji-only message
- Afrikaans with regulatory escalation
- Calm churn signal ("it is what it is")
- Gibberish

Each test verifies that every field in the output contains a legal value from the allowed enum sets.

---

## Design Decisions

**Anthropic Claude over alternatives.** Strong multilingual capability across English, Afrikaans, and IsiZulu, and reliable adherence to strict JSON output schemas in system prompts.

**Prompt engineering over fine-tuning.** A well-designed prompt is iterable in seconds and version-controllable. Fine-tuning would be more accurate but vastly more expensive to maintain.

**Validation after parsing.** The model occasionally returns slightly wrong enum values. Coercing to safe defaults rather than crashing keeps the tool useful while the prompt is improved.

**Three-retry exponential backoff.** Rate limits need time to reset. Progressive backoff gives the API breathing room.


## Built With

Python 3 · Anthropic Claude API · Rich · python-dotenv

---

## A note on AI collaboration

This submission was built with Claude as a thinking partner. See `PROMPT_LOG.md` for the full collaboration log — the questions I asked, the suggestions I pushed back on, the iterations on the system prompt, and what I learned.