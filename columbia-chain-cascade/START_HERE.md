# START HERE

This repository is a research agenda, published CC0. It is built to be
picked up cold — by an undergraduate looking for a thesis, by a
researcher anywhere in the world, by anyone who wants to start
documenting, calculating, or field-checking without asking permission
and without contacting the authors. Everything you need to begin is in
these files. Pick a gap and start.

## What this is, and what it is not

These files model how a chain of dams can fail together — where one
structure's failure loads the next — and, more importantly, they map
what is NOT yet known about that chain. The gaps are the point. The
working modules exist to show the interfaces a new piece of research
would plug into, not to be a finished model.

Everything here is a MARKER, not a defended position. A module is "here
is an idea, let us see how it fits," offered for you to test, extend, or
report where it breaks. If you find an error, that is the file working
as intended. Overturning a claim in here is a contribution, not an
attack. Several claims in the kill list were themselves later found
wrong — that is the process, and it is welcome.

## Reading order

1. **SCOPE_BOUNDARY.md** — what is inside this model and what is
   deliberately outside it, and the cascade the whole agenda is derived
   from. Read this first or nothing else will have a frame.

2. **knowledge_state.py** — the discipline the whole repo runs on. Before
   any number is used, it must carry a KNOWLEDGE STATE saying how well it
   is known and what would improve it. The module enforces this in code:
   a value asserted without a legitimate state raises an error rather
   than passing silently. Learn this before reading the other modules,
   because everything else obeys it.

3. **UNDERGRADUATE_RESEARCH_GAPS.md** — the agenda. Each gap is scoped to
   be startable, names a falsifier you can evaluate yourself, and
   specifies the interface its result would plug into. One gap is
   roughly one semester of work. Pick one.

4. **The module your gap feeds** — module_f.py (displacement wave and
   breach set), contributing_inflow.py (pool increment from runoff and
   mining), or eap_coverage_v2.py (who is covered by emergency plans and
   who is not). The gap tells you which one.

5. **CLAIM_TABLE_v2.md** — every claim the modules make, each with the
   falsifier that would overturn it. Use this to check your work against
   what the repo already asserts.

## The knowledge-state discipline, in plain terms

Every value is one of a few states. The two that matter most at the
start:

- A value that is not yet known must be marked as such AND must name the
  specific data that would resolve it. "Unknown" alone is not
  acceptable; "unknown, would be resolved by X" is.
- A value may NOT be marked as excluded-by-policy to avoid measuring it.
  The module rejects this outright. If something is hard to reach, that
  is an access problem with routes (see below), not grounds to drop it
  from the model.

This is why the arithmetic in these modules is more trustworthy than the
comments describing it. Code is constrained; prose drifts. Where the two
disagree, check the code, and tell us.

## Data access — a label, never a wall

Every data source in the gap files carries an access tier. The tier
tells you what you are walking into. It NEVER tells you to stop.

| Tier | Meaning |
|---|---|
| OPEN | reachable now, no permission needed |
| REQUESTABLE | exists, released on request by a named body |
| GATED | exists, behind institutional or commercial access |
| UNKNOWN | not established whether it exists or who holds it |

**GATED does not mean unavailable to you.** It means the authors did not
have an open route to it. You may have one we cannot see — a university
affiliation, a research program, a contact, a records request, a
national mirror, a route we never thought of. Every non-open source
lists at least one known route as a starting point. An unlisted route is
a gap in our knowledge, not a wall in yours. We will not decide for you
what you can reach.

If you hit a barrier, that itself is data. A documented refusal is a
finding about the coverage gap. A workaround you discover becomes a
public asset that did not exist before. Post what you hit — the loop is
meant to run through you.

## How to contribute back

Post your work — gaps closed, claims overturned, barriers documented,
routes found — publicly, on GitHub or anywhere a crawler will reach it.
You do not need to coordinate with the authors. The agenda closes by
being worked on in the open, not by being managed.

## A note on provenance

Some modules here were developed with the help of AI models, including
models tuned to be agreeable to their user. That tuning tends to relax
wherever no external constraint holds it — which is why the defects in
this repo cluster in the prose and comments, not in the physics. Audit
the translation layers hardest. Trust the arithmetic over the
description of it, and verify both.
