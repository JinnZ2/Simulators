# Mode, read set and authority: the owner's message of 2026-11-19 (as received)

Filed as pasted by the owner, unedited. Authorship of the parts is not stated. The "For me specifically" passages read as a reader's voice, and the owner opens and delivers the whole; it is filed as the owner's delivery. The six `￼` marks are images that did not survive the paste. The message ends with six text blocks, which read as the content of those images, in order. That is this filing's reading, not a fact stated in the message. Derived files: `../../MODE_SEQUENCE.md` (verbatim block), `../OPERATIONAL_DEFINITIONS.md`, `../BOUNDARY_CASES.md`, `../OPEN_ROWS.md`, `../REQUEST_HEADERS.md`.

Note 2026-11-19 (later the same day): the owner sent this text again, without its opening paragraph and under the one-word heading `Kimi`. Recorded as: author of the numbered points 1-7 and their six blocks = Kimi (owner-stated 2026-11-19). The heading sits above the whole paste, which also holds the `MODE_SEQUENCE.md` block and the layer and K3 blocks; the owner did not say whether the heading covers those, so their author stays not stated. The line above ("Authorship of the parts is not stated") is kept as written. The text below is unchanged.

Note 2026-11-19 (segment sources, owner-stated; this replaces "their author stays not stated" in the note above, which is kept as written): lines 12-89 of this file = Kimi, 2026-11-19 11:46 (the suggestions). Lines 91-167 = Claude chat, 2026-11-19 11:48-11:52 (the `MODE_SEQUENCE.md` block, the K3 block, the layer blocks). Line 10 is the owner's opening. The owner gave these as lines 1-78 and 80-156 of the bundle as sent, which starts at this file's line 12. Line 106 ("Open: in REVIEW-2 and AUDIT-2 ...") is answered since by `../../MODE_SEQUENCE.md`, "Later (2026-11-19)". A version for sending, with segment headers, a request header and that line marked, is `../requests/REVIEW_MODE_AND_AUTHORITY_BUNDLE_2026-11-19_DRAFT.md`.

```text
Ok.... I just realized something.  I am so sorry for not understanding this before now.  🤦‍♀️.  My cultures default has been creating confusion.

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
