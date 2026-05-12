# Reflection — Definite Triage Engine
**Candidate:** Lethukuthula Mthiyane

---

Honestly, going into this I underestimated how much thinking goes 
into a system prompt. I thought it would be straightforward — 
define categories, list some rules, done. But once I started 
testing against the sample tickets I realised how many edge cases 
I had not thought about. A Zulu message getting deprioritised 
because it sounds informal. A customer mentioning ICASA being 
treated like a normal complaint. Those are not small gaps.

Where I got stuck was a ModuleNotFoundError that had me confused 
because pip said everything was installed. Turned out requirements.txt 
was incomplete — anthropic was never actually in it. Simple fix 
but it cost me time because I was looking in the wrong place.

I also hit a git conflict on push that I had not dealt with before. 
I worked through it but it reminded me that the non-technical parts 
of a project can eat your time just as much as the code.

If I had more time I would write tests that do not need the API 
to run — right now every test burns tokens. I would also version 
the system prompt properly so I can track what changed when 
something breaks.

What I took away from this is that AI is only as useful as the 
questions you ask it. The moments where I stopped and questioned 
something — why exponential backoff, what happens with unknown 
inputs, what is the security risk in the response field — those 
produced better outcomes than just accepting suggestions. Asking 
better questions is a skill I will keep working on.
