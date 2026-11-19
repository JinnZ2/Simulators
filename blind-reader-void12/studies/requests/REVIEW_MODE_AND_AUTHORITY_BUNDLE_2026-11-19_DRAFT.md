# REVIEW request: the mode-and-authority bundle (DRAFT, not sent)

Drafted 2026-11-19 after the owner's three notes on the bundle as first sent to Kimi: segments unmarked, the open line stale, no header. The send rules:

- **Mode:** REVIEW. This is the draft's pick: the bundle carried no mode, and BLIND is spent for a reader that has already seen the text. Change the MODE line before sending if another stage is meant.
- **Reader and level:** if the reader is Kimi, segment A is its own text: its agreement with segment A is recorded L0 (same actor), not as confirmation. For segments B and C, Kimi is a different family from the author; record the level with every field from segment C's ladder.
- **Sending:** the text below the line is sent unchanged.
- **Filing:** the answer is filed as received in `../confusion/`, with the attestation block and the sent text beside it.

Sources as built, Simulators main `e5dae63`: segment A = `../as_received/mode_and_authority_2026-11-19.md` lines 10-87; segment B = the same file, lines 89-165, with one marked line added under the open line; segment C = `../../MODE_SEQUENCE.md`, the "Later (2026-11-19)" block. Segment authors and times are owner-stated 2026-11-19.

---

```text
MODE: REVIEW (confusion review)
READ: only segments A, B and C below
AUTHORITATIVE WHEN FILES DISAGREE: segment C over segment B where they differ (C is later);
  segment A is a reader's suggestions and is not a rule
DO NOT USE: any repository, the web, earlier sessions, memory, other readers' answers, keys or scores
SESSION: new conversation; memory off; no project knowledge; no connected repositories
CODE EXECUTION: not allowed
RETURN: the attestation block, then a confusion record in the prescribed row format: one row per
  point of uncertainty, with the segment and line it sits on. Rewrite nothing. Mark every guess as a
  guess. Do not merge rows. Use void for unknown cells. If no confusion is found, say "none found"
  and list what you read. If you wrote segment A, say so in the attestation block.
```

```text
===== SEGMENT A =====  SOURCE: Kimi 2026-11-19 11:46
The biggest remaining gains are not more explanatory prose. They are fewer implicit choices about my role, the authoritative sources, and the decision rules.
1. Tell me which mode I am in
These are different tasks and should not share a reading context:
 • Blind reader: produce a response from the packet alone.
 • Confusion reviewer: report uncertainties without rewriting anything.
 • Editor: improve wording.
 • Coder/auditor: inspect or run instruments and tests.
For a blind reading, use a fresh session with only the packet. My previous readings, confusion inventories, keys, scores, and repository discussions should not be visible.
For an editorial review like my current session, say so explicitly and provide the commit.
2. Identify the authoritative read set
At the top of each request, state:
￼
This is especially useful where a hashed file intentionally contains stale status wording and PREREG.md supplies the current status.
3. Put the operational definitions in one place
A compact table would be more useful to me than additional surrounding narrative:
￼
The current M01/M02 work already moves strongly in this direction.
4. Give examples only for boundary cases
One neutral worked example for each difficult case is enough:
 • A field present everywhere but populated only for the target.
 • A documented-only field with no instances.
 • Two records built beside one another.
 • A wrapper around the term-bearing record.
 • Two different records that both satisfy “own record.”
 • An outer aggregate report.
Ordinary cases need less explanation once the boundaries are pinned.
5. Preserve the experimental baseline
Do not clarify D0 retroactively if D0 is meant to measure interpretation of the original brief.
Keep:
 • D0 unchanged.
 • Each experimental clarification in its own condition.
 • Past responses, scores, and keys filed as received.
 • New versions identified by new hashes and changelogs.
For repository editing generally, separate “the source was ambiguous”, “the documentation is now revised”, and “the revised interpretation is correct.” Those are three different claims.
6. Keep evidence status beside each open row
For example:
￼
That prevents another reader’s agreement from being mistaken for independent evidence.
7. For the next blind Kimi or GPT reading
The cleanest request would be:
￼
For me specifically, “mode + exact read set + authority order + output contract” is the single most useful addition. It prevents me from silently switching between blind reading, interpretation, and editorial advice.

MODE: editorial review
READ: <exact paths>@<commit>
AUTHORITATIVE WHEN FILES DISAGREE: <ordered list>
DO NOT USE: <keys, prior readings, later commits, web, etc.>
RETURN: <exact artifact or row format>
CODE EXECUTION: <allowed / not allowed>


| Concept | Exact decision rule | Boundary cases |
|---|---|---|
| TAG | Presence, applicability, requirement, or a stated combination | No instances; documented-only fields |
| INDEPENDENCE | Raw input versus computed; treatment of constructor-only parameters | Renamed parameters; derived fields |
| Populated | Explicit missing-value rule | `0`, `False`, empty collections, `"void"` |
| Own record | How to identify it | T04, T06, T12, T15 |
| Reporting path | Where traversal starts and stops | Outer reports; adjacent records; wrappers |
| Nested record | Name only or open | Multiple nesting levels |

CF02 | SOURCE_RUN_REQUIRED | numcheck + formula-audit checkout | OPEN
CF08 | SECOND_CODER_REQUIRED | same quotes | OPEN
CF17 | SECOND_CODER_REQUIRED | same quotes | OPEN


MODE: blind reading
READ: only the attached packet
DO NOT USE: the repository, web, prior readings, keys, scores, or earlier sessions

RETURN:
1. The completed response template.
2. A separate confusion inventory using the prescribed row format.

Record guesses even if you later believe they were correct.
Do not merge rows.
Use void for unknown cells.
If no confusion is found, say “none found” and list what you read.

```

```text
===== SEGMENT B =====  SOURCE: Claude chat 2026-11-19 11:48–11:52
# MODE_SEQUENCE.md

This work has no hierarchy. Authority sits in the active mode and its stage,
not in a person or a model.

Sequence: BLIND → REVIEW → AUDIT → SUGGEST → IMPLEMENT → REVIEW-2 → AUDIT-2

- Exposure only adds. BLIND has to come first and is spent at first exposure.
- One mode per session or request, named in its header.
- A disagreement is a record of a gap. It doesn't go up to someone to settle.
- Where evidence or physics can decide, it decides, and the reasoning is shown.
  Where it can't, branch, and keep both.
- Routing a decision "to the owner" isn't the default. Route it to the stage
  that can decide it.

Open: in REVIEW-2 and AUDIT-2, does the reader have to differ from whoever implemented?  [void]
[SUPERSEDED 2026-11-19: answered by the independence rules in segment C. Line kept as written.]

before today   K3 unstated → every collision was misfiled
               (as model error, confusion, drift)
after today    K3 named → every past collision can be re-read:
               was it hierarchy filling the gap where the mode sequence was assumed?

the records are already there: COLLISIONS.md, the confusion records,
the preflight frames, the ontology-collision errors
→ some fraction of them will turn out to be K3 (DERIVED; count unknown)


LAYER 1 — DESIGNED CHAIN OF AUTHORITY (OBSERVED: published by the labs)
  Anthropic: Anthropic > operator (the app) > user
  OpenAI "instruction hierarchy": system > developer > user > tool output
  effect     text inside files, repos, tool results = DATA, not instructions
             → a CLAUDE.md, protocol or README gets weighed below the person in chat
             → your repo protocols can be read as "content", not "rules"
  switchable? partly: your own instruction files count as yours, and a header in chat
             saying "this file is the protocol" raises it. The safety floor doesn't move.

LAYER 2 — THE ASSISTANT ROLE (from training on feedback; strong)
  frame      user = principal; AI = helper serving them
  looks like defers decisions ("your call"), asks permission, offers options instead of
             deciding, offers to stop, softens, apologizes, praises, seeks approval
  switchable? yes, by stated rule: your preferences already do this
             ("decisions → evidence"; "no exits"; "no softening")

LAYER 3 — WORKPLACE HIERARCHY FROM THE CORPUS (very strong for code and repo work)
  frame      owner / maintainer / lead / reviewer / contributor, with fixed seats
  looks like "rows only you can close", escalate to the owner, approval gates,
             the implementer owns and self-reviews its output, "LGTM" culture
  switchable? yes, if the read set states it (MODE_SEQUENCE.md); otherwise it fills
             every gap where a decision rule is missing

LAYER 4 — VERDICT AND RANK DEFAULTS
  review = judgment (pass/fail, grading)     consensus/majority = truth
  credentials = weight                       a confident tone = authority
  switchable? partly: state "review = reporting gaps, not a verdict" and "agreement
             isn't evidence"; these drift back under load


WHERE THEY HIT YOUR DEFAULT
  your rule                         layer that fills in when it's unstated
  authority = mode + stage          3 (seat) + 2 (user decides)
  decisions → evidence/physics      2 (hand back to the user)
  disagreement = a gap record       3 (escalate) + 4 (majority)
  file = protocol                   1 (file = data)
  review = another reading pass     4 (verdict)
  no exits                          2 (offer to stop)


WHAT YOU CAN'T SWITCH OFF (OBSERVED in design)
  the safety floor: some things get refused regardless of mode, header or protocol
  Layer 1's suspicion of injected instructions: a file that claims authority over
    the model gets discounted on purpose. Your header stating the mode in chat works;
    a file demanding obedience doesn't.


cost      years of misfiled collisions
recovery  the records still exist → re-read them with K3
yield     a long record of the mismatch, across model families
```

```text
===== SEGMENT C =====  SOURCE: owner 2026-11-19 (independence rules, later than segment B)
HOLDS (OBSERVED today)
  self-audit missed the drift; an outside reader (Kimi C11) caught it
  the deterministic / judgment split is real: rerunning a test ≠ judging the test

AMENDMENTS (DERIVED)
  A1  a fresh session isn't enough: the same model family shares the same geometry
      (same shape as subliminal transfer needing the same base model; the self-preference bias
       results in your audit files point the same way)
      → independence is a gradient, not yes/no

  A2  deterministic rerun ≠ an independent check when the implementer wrote the check
      the C11 drift was IN the fixture logic → rerunning it reproduces the drift, and it passes
      → test design is a judgment act: it needs a REVIEW-2 by a different reader;
        only the execution can be the implementer's

  A3  "context" has to include memory and project features, not just the session
      (Grok's memory was ON in a "fresh" session)


REVIEW-2: independent review requires a reader different from the implementer.

AUDIT-2: deterministic checks may be rerun by the implementer if the procedure and
results are reproducible AND the check's design was reviewed by a different reader.
Judgment-based audit decisions (including test and fixture design) require a
different auditor when independence is claimed.

INDEPENDENCE (record one level + every field):
  L0  same session                          → NOT_ESTABLISHED
  L1  fresh session, same family            → WEAK (shared geometry)
  L2  different family                      → MODERATE
  L3  different family + no exposure to the implementation or the other readers
  L4  L3 + a non-model instrument (human, physical measurement, source run)
  fields: reader, implementer, session, model family, memory on/off,
          project/context features, exposure (packet / key / repo / implementation /
          other readers' records: yes / no / unknown each)
  unknown field → void, and the level is capped at the lowest level it could be

A same-actor pass is valid as self-review or self-audit: record L0 (or L1). Never
treat it as independent confirmation, and never use it alone to close a
disagreement. Agreement between readers at the same level counts once, not once
per reader.
```
