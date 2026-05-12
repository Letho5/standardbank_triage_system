# Prompt Log — Definite Triage Engine
**Candidate:** Lethukuthula Mthiyane  
**Challenge:** Standard Bank Internship — Challenge 2  
**AI Tool:** Claude

---

You said: Hi Claude. I need your help building a project for a Standard Bank internship hiring challenge. I want us to work together properly — you explain everything before we write it, and I type it myself so I genuinely understand it. This is a ticket triage system for a bank. Please note this is South Africa, multilingual, and security matters. Can we start by you telling me what this system actually needs to do before we touch any code?

Claude responded: Before any code — good instinct. A triage system is the intake desk, not the treatment room. It reads every incoming message and decides three things: what is this about, how urgent is it, and who should handle it. The goal is that by the time a human agent opens a ticket, the hard thinking is already done. Category identified. Urgency assessed. Key details extracted. First response drafted. The agent just executes. Think of it like a hospital emergency room triage nurse — not the doctor who treats, but the person who decides who needs the trauma team right now and who can wait. Without that person, critical cases get buried under routine ones. That is the gap this system fills.

---

You said: Okay so when you say intake desk — are you saying this system doesn't actually solve the customer's problem?

Claude responded: Exactly right. It triages, it does not resolve. The system makes sure the right message reaches the right person at the right time. A fraud case reported at 2am gets flagged as critical before a human even wakes up. An angry customer who has been bounced between departments six times gets flagged as high urgency so they do not have to repeat themselves again. A compliment gets routed to the right branch manager so good work gets recognised. The resolution still happens — but it happens faster and to the right person because the intake was handled correctly.

---

You said: This system is for South Africa. Customers write in English, Afrikaans, IsiZulu — sometimes all three in one message. What risks does that introduce that a normal classifier would miss?

Claude responded: Three significant ones. First — code-switching is completely normal in South Africa but looks like noise to most classifiers. "Sawubona, I need help with my rekening" is not broken communication, it is how people naturally talk. A generic system might fail to classify it correctly simply because it does not recognise the mix. Second — SA-specific terms like load shedding, RICA, FICA, airtime, and debit orders have no direct equivalents in Western training data. A model might misread a load shedding complaint as a vague network issue and route it wrong. Third — urgency signals are culturally embedded. "It is what it is" sounds resigned and calm. In SA context it is a churn signal — the customer has given up. A generic classifier reads the calm tone and assigns low urgency. That is exactly the wrong call.

---

You said: So how do we handle all of that — do we train a new model?

Claude responded: No — and understanding why not is important. Training a new model for this context would take months, a large labelled dataset, and significant compute cost. What we do instead is engineer the system prompt carefully. We give the existing model a detailed brief before every customer message — the SA context, the cultural signals, the hard rules. The model already understands language broadly. We are filling in specific gaps and setting the rules for how to apply that understanding in this specific context. Prompt engineering, not model training. That is the practical approach for a system like this.

---

You said: Okay before we build — why are we using multiple files instead of one script? The challenge says a simple script is fine.

Claude responded: Simple script is fine means you do not need a web server or database. It does not mean one file is better. Each file having one job means when something breaks you know exactly where to look. When you want to iterate on the system prompt you open prompt.py and nothing else changes. If you ever need to switch from Anthropic to a different LLM provider you change engine.py only — the CLI, the display, the tests, none of them care. More importantly for tomorrow: in an interview, being able to say "this file does exactly one thing" is a much stronger answer than "everything is in here somewhere."

---

You said: I already cloned the challenge repo. I didn't create a new project. Does that change anything?

Claude responded: Yes — show me the directory listing and the requirements.txt before we plan anything. If the repo already has structure we do not know about, building on top of it blindly creates problems we will only discover later. I also need to see the README — the challenge specifies exact output schemas we have to match. We build to their spec, not ours.

---

You said: [shared directory and files] The requirements.txt only has python-dotenv. Anthropic is just commented out.

Claude responded: That needs to be fixed before we write a single line of code. The challenge says the submission must work with a single pip install -r requirements.txt. If a reviewer clones your repo and runs that command and anthropic is missing from the file, your submission fails before it starts — not because your code is wrong but because the requirements file is incomplete. We add anthropic and rich to it right now.

---

You said: What is rich and why do we need it?

Claude responded: Rich is a Python library for beautiful terminal output. It gives you coloured text, bordered panels, auto-aligned tables, and JSON syntax highlighting — things that would take hundreds of lines to build manually with raw print statements. For a triage system, the urgency level needs to be impossible to miss at a glance. Rich lets us make CRITICAL display in red and HIGH in amber without building a custom formatting engine. It is the difference between output that communicates instantly and output that requires reading.

---

You said: I looked at the sample tickets. TEST-003 is pure Afrikaans, TEST-006 mixes Zulu and English, TEST-010 is literally just angry emojis and load shedding. What does the system prompt need to handle all of those correctly?

Claude responded: At minimum six things. It needs to understand code-switching as normal, not broken. It needs SA-specific term definitions — load shedding, RICA, FICA, airtime, debit orders. It needs hard escalation triggers so ICASA and the Ombudsman always raise urgency immediately. It needs a bias guard so informal and non-English messages are never deprioritised. It needs a security rule so account numbers are never echoed back in responses. And it needs an explicit instruction for unknown inputs — what to do when a message matches nothing in the prompt. Without that last one the system handles the test cases by luck, not design.

---

You said: Okay I'm concerned about the prompt.py module. Is it supposed to have only the phrases that are in the test inputs?? What if I test it on something that is not on the prompt.py???

Claude responded: This is the most important question you have asked. The system prompt is not a lookup table. The listed SA phrases are cultural anchors — they correct gaps that might exist from training on mostly Western data. They are not an exhaustive dictionary. When a customer writes something completely new — unusual slang, a different language, one word, gibberish — the model applies everything it already knows about language plus the rules we have set. The SA phrases tell the model how to interpret the cultural layer on top of what it already knows. We should also add an explicit section to the prompt saying: for anything not listed, use your general language understanding and always return valid JSON. That makes the behaviour intentional rather than accidental.

---

You said: So we should add a section that says use your general understanding for anything not listed?

Claude responded: Yes — and it matters that we state it explicitly rather than assuming the model will figure it out. There is a real difference between a system that handles unknown inputs by luck and one that handles them by design. If it ever fails you can point to the rule and debug it, rather than wondering why it worked sometimes and not others. We add it now.

---

You said: Also — this is a South African bank. If the model was mostly trained on English, is it going to treat a Zulu message as less serious just because it sounds informal?

Claude responded: Yes — without an explicit instruction, that is exactly the risk. Models trained predominantly on formal English data can associate informal language and non-English languages with lower confidence, which can translate to lower urgency scores. A Zulu-speaking customer reporting fraud is not a lower priority than an English-speaking customer reporting the same thing. In a bank serving all South Africans, that kind of systematic bias is not just a technical problem — it is a service equity problem. The bias guard goes into the prompt as a hard rule: never downgrade urgency because the message is in Zulu, Afrikaans, Xhosa, or informal English. Informal is not unimportant.

---

You said: And security — the suggested response gets sent to the customer right? What if it has their full account number in it?

Claude responded: That is a compliance risk. If the suggested response echoes back a full account number and that message gets forwarded, logged, or screenshotted somewhere insecure, you have a data exposure event. We add a hard security rule to the prompt: never reproduce full account numbers or card numbers in the suggested response. If a number was mentioned, reference only the last four digits. So ACC-99123 becomes "your account ending 9123." That is the standard masking convention in banking communications and it needs to be in the prompt as a non-negotiable rule.

---

You said: When it comes to ICASA and the Banking Ombudsman — should the prompt suggest the model consider whether it is serious, or should it always escalate?

Claude responded: Always escalate. No consideration, no weighing up. The moment ICASA or the Banking Ombudsman or the Consumer Tribunal appears in a message, urgency goes to critical immediately. These are real regulatory bodies with real enforcement power. A customer mentioning them has already decided to escalate formally. Giving the model discretion to decide whether this particular mention is serious enough is exactly the wrong design. Hard rule, no exceptions.

---

You said: Okay let us build engine.py. I typed it but I want to understand the retry logic. Why exponential backoff specifically — why not just retry three times immediately?

Claude responded: When an API returns a rate limit error it means you sent too many requests too quickly and the service needs time to reset. Retrying immediately hits the same limit again immediately. Exponential backoff means each retry waits longer than the last — with a base of 2.0, attempt one waits 2 seconds, attempt two waits 4 seconds, attempt three waits 8 seconds. Progressive delays give the rate limit time to fully reset. This is the industry standard for API resilience and you will see it in production systems everywhere.

---

You said: And we have a _fallback function. Why return a structured object when things fail instead of just crashing?

Claude responded: Because in a production triage system, a crash means a customer message is lost. If the tool raises an unhandled exception, the ticket disappears — no record, no one knows it came in. A structured fallback means the ticket still exists with a flag saying triage failed, which an agent can pick up manually. The output is always valid. The underscore prefix on _fallback and _validate signals they are private to this module — not meant to be called from outside engine.py.

---

You said: python triage.py --message "my airtime is gone"
Traceback (most recent call last):
  File "triage.py", line 12, in module
    from engine import triage_message
ModuleNotFoundError: No module named 'anthropic'

I ran pip install -r requirements.txt already. It said requirement already satisfied.

Claude responded: The requirements.txt only had python-dotenv in it when you installed. "Requirement already satisfied" means python-dotenv was found — not anthropic. Anthropic was never actually in the file. Run pip show anthropic and it will come back not found. Install both missing packages directly and then update requirements.txt to include them. That file must list every dependency your code actually imports or the submission is broken for any reviewer who installs fresh.

---

You said: pip show anthropic
WARNING: Package(s) not found: anthropic

Okay so the file was just incomplete this whole time.

Claude responded: Exactly. And this is a useful debugging lesson — "requirement already satisfied" only tells you about packages that are already in the file. It says nothing about packages missing from the file entirely. The error was never in your code. The requirements file was incomplete. Install anthropic and rich, update the file, and this will not happen again.

---

You said: It worked. Output showed service, medium, negative, summary about airtime disappearing, no entities extracted, suggested response asking for a phone number. Is that right?

Claude responded: That is exactly right — and more impressive than it looks. Three words, no account number, no phone number, no location, no explicit emotion. The system read "airtime" as a telecoms service issue rather than billing because no charge was mentioned. It picked up implicit frustration from the brevity. It correctly found nothing to extract. And the suggested response asking for a phone number is what a real agent would do next — there is nothing to act on without an identifier. A three-word message produced a complete, valid, useful triage object.

---

You said: I ran all 10 sample tickets. TEST-003 came back and the suggested response was in Afrikaans. Did the prompt do that or did that happen on its own?

Claude responded: The prompt did that deliberately. The instruction says write the suggested response in the customer's primary language. TEST-003 was pure Afrikaans so the model detected that and responded in kind. That is the system meeting the customer where they are. Without that instruction in the prompt the response would have defaulted to English regardless of the customer's language.

---

You said: TEST-009 — stolen phone. The response said "account ending 9123" not the full ACC-99123. That was the security rule working?

Claude responded: Yes. The input contained ACC-99123 and the security rule says never reproduce full account numbers — last four digits only. The model masked it correctly under real test conditions with a real account number present in the input. That rule was not theoretical. It held.

---

You said: Okay the 10 passed. I want to add my own edge cases now. What would genuinely break this system that the samples do not cover?

Claude responded: Five gaps in the sample tickets. Empty input — the system should not make an API call for nothing and should not crash. Emoji-only — three angry emojis with no words should still return valid JSON. Afrikaans combined with a regulatory body mention — the samples test these separately, not together. The churn signal in a calm message — "it is what it is" sounds resigned but urgency must go high. And pure gibberish — random characters should return safe defaults, not raise an exception.

---

You said: I added all 5. 15/15 passed. But does 15/15 actually mean the system is correct or just that the structure is valid?

Claude responded: Important distinction. The test suite validates structure — every field exists, every value is from the allowed set. It does not validate semantics — whether the answer is actually right. You need to check the actual values manually. Does EXTRA-003 return urgency=critical AND language=afrikaans simultaneously? Does EXTRA-004 return urgency=high despite the calm tone? Those confirmations are what tell you the prompt's rules are working, not just that the JSON is valid.

---

You said: EXTRA-003 came back urgency=critical and lang=afrikaans. EXTRA-004 returned high urgency. Churn signal worked.

Claude responded: That is the prompt's rules working under real conditions. The Afrikaans escalation case confirmed two separate rules firing simultaneously — language detection and hard escalation trigger. The churn signal case confirmed that calm tone alone does not suppress urgency when a specific phrase triggers the rule. Those are the two most important validations in your edge case suite.

---

You said: Can you explain display.py to me properly. I typed it but I need to understand what each part is actually doing for the interview.

Claude responded: display.py has one job — take the dictionary from engine.py and make it readable in the terminal. No logic, no API calls, pure presentation. The rich library handles coloured text, bordered panels, and auto-aligned tables — things that would require hundreds of lines of manual ANSI code otherwise. The two colour dictionaries at the top map each urgency and sentiment value to a style string. The reason for dictionaries instead of if-elif blocks is readability and maintainability — one line to change a colour rather than hunting through a function. Every field is accessed using .get() rather than direct key access so a missing field shows a dash instead of crashing.

---

You said: Why .get() instead of just result["urgency"]?

Claude responded: Direct key access crashes if the key is missing — it raises a KeyError. .get() returns None instead of crashing. display.py is the last step before the user sees output. If it raises an exception the user sees a traceback instead of results. With .get() and default values a missing field shows a dash and the rest of the output still renders. Defensive programming in the presentation layer means a partial result is still useful rather than a complete failure.

---

You said: In engine.py the _validate function — why is it separate from the main function?

Claude responded: Single responsibility. triage_message has one job — call the API and get a response. _validate has one job — check that response is structurally correct. Combining them creates a function doing two different things that is harder to test and harder to change. If the validation rules ever need updating — a new field, different allowed values — you edit _validate without touching the API call logic. Separation also means you can test validation independently without mocking an API call.

---

You said: What does if __name__ == "__main__": do at the bottom of triage.py? I see it everywhere but I never fully understood it.

Claude responded: When Python runs a file directly — python triage.py — the variable __name__ is set to the string "__main__". When a file is imported as a module by another file, __name__ is set to the module name instead. So that condition means: only run this code when the file is executed directly, not when it is imported. Without it, if tests.py ever imported anything from triage.py the CLI would launch automatically on import. With it, imports are safe and the CLI only starts when you explicitly run the file.

---

You said: I'm trying to push to github and I got:

! [rejected] main -> main (non-fast-forward)
error: failed to push some refs
hint: Updates were rejected because the tip of your current branch is behind its remote counterpart.

Claude responded: The remote has a commit your local copy does not have. Most likely you made an edit directly on GitHub at some point — clicking the pencil icon to edit a file creates a commit on the remote that your local history does not know about. The histories have diverged. Run git pull origin main --rebase to pull the remote changes and replay your local commits on top of them cleanly.

---

You said: What does --rebase do and why use it over just git pull?

Claude responded: A plain git pull creates a merge commit — a new commit that says these two histories were joined here. Your log ends up with branching history even though only one person was working on the project. --rebase replays your local commits on top of the remote commits instead, keeping a clean linear history. For a solo project, rebase produces a cleaner git log. Being able to explain that distinction in an interview shows you understand what your tools actually do, not just which commands to type.

---

You said: interactive rebase in progress
CONFLICT (content): Merge conflict in README.md
both modified: README.md

Claude responded: The rebase found that both sides changed README.md and cannot decide which version to keep. In a rebase, "theirs" refers to your local commits being replayed — which is the README you want. Run these four in order: git checkout --theirs README.md, then git add README.md, then git rebase --continue, then git push. That tells git to take your local version, mark the conflict resolved, finish the rebase, and push.

---
You said: Okay let us push what we already have to our github repo
and after that give me a readme file for my github.

Claude responded: Before anything else — open your .gitignore and
confirm .env is listed. If your API key ends up on GitHub it gets
exposed publicly and Anthropic will revoke it. That is a
non-negotiable check before any push. Once the push is clean we
write the README around what is actually in the repo.

---

You said: (venv) PS C:\Users\Sinqobile\definite-triage> git push
Enumerating objects: 5, done.
Counting objects: 100% (5/5), done.
Delta compression using up to 4 threads
Compressing objects: 100% (3/3), done.
Writing objects: 100% (3/3), 573 bytes | 71.00 KiB/s, done.
Total 3 (delta 2), reused 0 (delta 0), pack-reused 0 (from 0)
remote: Resolving deltas: 100% (2/2), completed with 2 local objects.
To https://github.com/Letho5/standardbank_triage_system.git
   ebca2cc..5ef4f89  main -> main .Now give me the readme.

Claude responded: 
Open your existing README.md in VSCode and replace its entire contents with everything below. This is what reviewers will see when they land on your repo.

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
```
Sawubona, ngicela usizo. I-account yami i-blocked and I can't buy
bundles. I went to the store in Umlazi but they said I must call.
Angazi what to do anymore. My number is 0734567890.
```

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
  "suggested_response": "Sawubona! I'm sorry to hear about your blocked account and the frustration of not getting help. Let me assist you right away with unblocking your account so you can purchase bundles again."
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

Create a `.env` file in the project root:

```
ANTHROPIC_API_KEY=your_key_here
```

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

---

## What Makes the Prompt Work

The system prompt has six deliberate layers, each addressing a specific failure mode:

- **Role declaration** — anchors Claude as a South African banking triage engine
- **Cultural context** — fills in what training data misses: load shedding, RICA, FICA, SA slang, code-switching
- **Escalation triggers** — hardcoded overrides for ICASA, Ombudsman, Tribunal mentions, fraud language, ALL CAPS
- **Bias guard** — explicitly forbids downgrading urgency for informal, Zulu, Afrikaans, or short messages
- **Security rule** — full account and card numbers may never appear in the suggested response
- **Output schema** — strict JSON, no preamble, no markdown fences

> The bias guard is the most important section. Without it, models systematically deprioritise informal English and African-language messages — exactly the customers a South African bank needs to serve well.

---

## Error Handling

| Failure | Behaviour |
|---|---|
| Empty or whitespace-only input | Returns fallback immediately — no API call wasted |
| LLM returns invalid JSON | Retries up to 3 times with exponential backoff (2s, 4s, 8s) |
| API rate limit hit | Same retry pattern — gives the limit time to reset |
| API down or auth failure | Returns structured fallback with diagnostic detail |

Whatever happens, the output is always a valid JSON object.

---

## Test Coverage

**15 / 15 tests passing.**

Ten provided tickets cover the documented cases. Five additional edge cases stress the system:

- Empty input
- Emoji-only message
- Afrikaans with regulatory escalation
- Calm churn signal ("it is what it is")
- Gibberish

Each test verifies that every field contains a legal value from the allowed enum sets.

---

## Design Decisions

**Anthropic Claude over alternatives** — strong multilingual capability and reliable adherence to strict JSON output schemas in system prompts.

**Prompt engineering over fine-tuning** — iterable in seconds, version-controllable in git, no training cost.

**Validation after parsing** — coercing wrong enum values to safe defaults keeps the tool useful while the prompt is improved.

**Exponential backoff** — rate limits need time to reset. Progressive delays give the API breathing room.

---

## What I Would Add With More Time

- Mock-based unit tests that run without burning API tokens
- Expected-value assertions on sample tickets to catch prompt regressions
- Per-field confidence scores
- Explicit prompt versioning
- Async batch processing for high-volume queues

---

## Built With

Python 3 · Anthropic Claude API · Rich · python-dotenv

---

## A Note on AI Collaboration

This submission was built with Claude as a thinking partner. See `PROMPT_LOG.md` for the full collaboration log — the questions asked, the suggestions pushed back on, the iterations on the system prompt, and what was learned.
---

You said: Okay I might need us to be minimal but informative when
it comes to the readme. I want us to be simple but also well
documented.

Claude responded: Stripped it down to only what earns its place —
a tight problem statement, setup in five commands, a usage table,
the output schema, a structure table, and bullet points on key
design choices. Removed the padding. Every section had a reason
to be there.

---

You said: I don't just want it short but I want a winning readme
that will be easy to read and be informative also. Good
professional readme.

Claude responded: Rebuilt it with a confident opening, a real
example showing actual input and output so a reviewer immediately
sees what the system does, clean quick start, usage table, how it
works diagram, project structure, what makes the prompt work,
error handling table, test results, design decisions, and an
honest section on what would be improved with more time. The
example near the top was the key addition — show do not tell.

---

You said: I need to make edits in the readme. The how it works
is out of alignment. Also my name is Lethukuthula Mthiyane not
Sinqobile.

Claude responded: Two targeted fixes. The diagram needed to be
wrapped in a code block to preserve alignment on GitHub — outside
a code block GitHub collapses the spacing. And updated the author
name throughout to Lethukuthula Mthiyane.

You said: git push
fatal: unable to access: Could not resolve host: github.com

Then I ran it again immediately and it worked. What was that?

Claude responded: A momentary DNS failure — your machine temporarily could not resolve github.com to an IP address. These hiccups last a few seconds and resolve themselves. Nothing was wrong with your git setup or your code. Running the same command again a few seconds later is exactly the right response.

---

You said: Okay it pushed. All files are there and .env is not visible. What questions should I expect tomorrow about the system prompt?

Claude responded: Three categories. Design questions — why is the bias guard in the prompt rather than in post-processing code, why are escalation triggers hard rules rather than suggestions, what happens with a language you did not explicitly handle. Iteration questions — what did the first version look like and what changed, how did you know when the prompt was good enough. Tradeoff questions — what would you do differently with more time, what is the weakest part of this design. Know your answers to all of these before you walk in.

---

You said: What is the weakest part of this system honestly?

Claude responded: Two honest weaknesses. The test suite validates structure, not correctness — 15/15 passing tells you every response has valid fields and enum values, not that the categorisation is actually right. A test that asserts TEST-003 always returns fraud and afrikaans would catch prompt regressions. You do not have that. Second — every test run burns real API tokens. Mock-based tests that intercept the API call would let you run freely during development without cost. Those gaps are real and worth naming proactively in the interview rather than hoping the reviewer does not notice.

---

You said: If a senior engineer reviewed this code what would they actually say?

Claude responded: Three things. No logging — there is no record of what messages came in, what the model returned, or where failures happened. In production you need an audit trail. No configuration management — model name, retry count, and backoff factor are hardcoded. A config file would make those adjustable without editing source code. And no confidence scores — the output tells you the category and urgency but not how certain the model was. Low-confidence classifications that route incorrectly are silent failures. These are genuine gaps worth naming.

---

You said: What would you say if they ask me why I chose Anthropic over OpenAI?

Claude responded: Say this — Claude has strong multilingual capability across English, Afrikaans, and IsiZulu, and follows complex system prompts reliably. The entire architecture depends on the model returning strict JSON with no preamble, a behaviour verified through testing not assumed. If they push further — mention the architecture is provider-agnostic. Swapping to OpenAI means changing the API call in engine.py only. Everything else stays identical. That answer shows you made a deliberate choice and you understand the tradeoffs.

---

You said: If this went to production at a real South African bank what would actually need to change?

Claude responded: Five things minimum. Logging and auditing — every message, classification, and routing decision needs a record for compliance. A feedback loop — agents need to mark classifications as wrong so the prompt improves over time. Human-in-the-loop for low-confidence cases — when the model is uncertain, route to a human rather than guess. POPIA compliance for data handling — customer messages contain PII and need proper storage, access controls, and retention policies. And load testing — a production bank receives thousands of messages per hour and single-threaded sequential processing would not survive that volume.

---

You said: Last question — be honest, if you had to score what we built out of 10 as a submission for this internship, what would you give it?

Claude responded: Eight out of ten. The system prompt is thoughtful and layered — the bias guard and security rule show it was designed for its context, not copied from a template. The error handling covers real failure modes. The test suite goes beyond the provided samples with reasoned edge cases. The code is clean, separated, and explainable. What keeps it from nine or ten: no mock tests, no expected-value assertions on sample tickets, and no prompt version history. Name those gaps proactively tomorrow rather than waiting for the interviewer to find them. Naming your own weaknesses first is a sign of engineering maturity.

---

Claude is AI and can make mistakes. Please double-check responses.

