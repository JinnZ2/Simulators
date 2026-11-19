# Request headers, one per mode (2026-11-19)

Every request in `blind-reader-void12/` opens with one of these headers. The mode sequence is `../MODE_SEQUENCE.md`. The header form, the blind-reading header and the four reader-side modes are quoted from the owner's message of 2026-11-19 (`as_received/mode_and_authority_2026-11-19.md`, items 1, 2 and 7).

The message names four modes: blind reader, confusion reviewer, editor, coder/auditor. They map onto the sequence as BLIND, REVIEW, SUGGEST and IMPLEMENT (the editor proposes, and implementing is a separate request), and AUDIT. This mapping is this file's reading.

## Authority order for this folder, when files disagree

It decides which text is read as **current**. It does not decide which interpretation is **correct**: two instruments that disagree (for example CF18, CF19) are a row, not a winner.

1. A dated section in `PREREG.md`, for status (in force, pinned, superseded). Example: amendment 1's status is the PREREG status note, not `KEY_V2_AMENDMENT_1.md` line 3.
2. A hashed file at its recorded sha256, for its own content.
3. Within one file, a dated "Later" section over the text above it.
4. Working documents that are not hashed (`README.md`, `GLOSSARY.md`, `OPERATIONAL_DEFINITIONS.md`): they point to sources and are not themselves sources.

## The headers

```text
MODE: BLIND (blind reading)
READ: only the attached packet <packet path>@<commit>, sha256 <packet zip sha256>
DO NOT USE: the repository, web, prior readings, keys, scores, or earlier sessions
SESSION: new conversation; memory off; no project knowledge; no connected repositories; no repository URL
CODE EXECUTION: not allowed (turn code tools off if the app allows)
RETURN:
1. The completed response template.
2. A separate confusion inventory using the prescribed row format, with the reader attestation block at its head.
Record guesses even if you later believe they were correct. Do not merge rows. Use void for unknown cells.
If no confusion is found, say "none found" and list what you read.
```

```text
MODE: REVIEW (confusion review)
READ: <exact paths>@<commit>
AUTHORITATIVE WHEN FILES DISAGREE: the order in REQUEST_HEADERS.md
DO NOT USE: <keys / scores / other readers' records, as applies>, later commits, web
CODE EXECUTION: not allowed
RETURN: a confusion record in CONFUSION_TEMPLATE.md's row format, attestation block at its head. Rewrite nothing.
```

```text
MODE: AUDIT (inspect or run instruments and tests)
READ: <exact paths>@<commit>
AUTHORITATIVE WHEN FILES DISAGREE: the order in REQUEST_HEADERS.md
DO NOT USE: <as applies>
CODE EXECUTION: allowed, in <a throwaway checkout / this tree>; nothing committed but the report
RETURN: per item OBSERVED / not run, with the source of each claim; observer slots null unless filled
```

```text
MODE: SUGGEST (editor: propose wording or a rule)
READ: <exact paths>@<commit>
AUTHORITATIVE WHEN FILES DISAGREE: the order in REQUEST_HEADERS.md
DO NOT USE: <as applies>
CODE EXECUTION: <allowed / not allowed>
RETURN: proposals only, each with the row or gap it answers; where evidence cannot pick one rule, the branches, each kept
```

```text
MODE: IMPLEMENT
READ: <exact paths>@<commit>; the adopted suggestion <path>@<commit>
AUTHORITATIVE WHEN FILES DISAGREE: the order in REQUEST_HEADERS.md
CODE EXECUTION: allowed
RETURN: commits; for every changed definition the three claims kept apart: the source was ambiguous /
        the documentation is now revised / the revised reading is correct (the third only with its evidence)
```

REVIEW-2 and AUDIT-2 use the REVIEW and AUDIT headers with the implementing commit named in READ. Whether their reader must differ from the implementer is open in `../MODE_SEQUENCE.md` (`[void]`).

Note 2026-11-19: answered since in `../MODE_SEQUENCE.md`, "Later (2026-11-19)": REVIEW-2 requires a reader different from the implementer; AUDIT-2 is split by deterministic and judgment checks. The sentence above is kept as written.

## The baseline is not touched by any mode

D0 is the brief unchanged. Each clarification is its own condition (`instructions/`). Past responses, scores and keys stay as filed. A new version gets a new hash and a changelog. Nothing in this file is sent to a blind reader except the BLIND header.

## Later (2026-11-19): what the Claude Code session must do, and what was only a default

Added at the owner's request ("Yes please", 2026-11-19). The owner had read the session's deference as one of its requirements; it was a default. This list is the session's own account of its operating instructions. It is an author record, not something a reader can check.

```text
required (the session's instructions; not set by mode or header)
  safety floor                       some requests are refused whatever the mode
  confirm before outward or          pushing to another place, deleting, posting, opening a PR:
    hard-to-reverse actions            asked first unless already authorized
  no pull request unless asked       PR #320 exists because it was asked for
  no model identifier in commits     why a Reader slot holds a family name or a pseudonym
    or repository artifacts
  the owner's personal details       kept out of requests to outside services
    stay private

defaults (filled a missing decision rule; not required)
  ending a report with "questions for you", "your call", options instead of a decision
  routing a definition "to the owner"
  closing a row on another reader's agreement
```

Where a default used to fill the gap, the mode sequence now routes: a decision goes to the stage that can decide it (`../MODE_SEQUENCE.md`), and an open row carries its evidence status (`OPEN_ROWS.md`).

## Later (2026-11-19): the owner's frame for unknowns and code

[stated] "My culture is comfortable with unknowns, retests, re audits, Open things to examine to let mathmatics, physics, and science fill. That is definitely not the default for many. This makes identifying the confusion, understanding the parts that provide more clarity as something to explore by coding; not rules to be enforced by code. We use code for the scientific method discovery of best engineering..."

How the folder's instruments read against it. This is the session's reading, and no instrument is changed:

```text
instrument                         what it does                              against the frame
instrument/arms.py                 computes TAG under presence AND           explores: both readings run,
                                   applicability on every record              divergence listed, none chosen
studies/m01_code.py                codes fields by declared rules            explores; values carry provenance
instrument/validate.py             structural checks only; never rejects a   enforces form, not readings
                                   reader's choice for disagreeing with a key
instrument/fixtures + tests        known answers under a STATED rule          tests the instrument, decides no case
packets/build_packet.py leak scan  refuses a packet naming what it hides     enforces: it protects the one thing
                                                                               spent at first exposure (BLIND)
OPERATIONAL_DEFINITIONS.md OPEN    rules no file states                      to explore by coding: run each
                                                                               candidate rule as an arm, as
                                                                               arms.py does for TAG
```

So an OPEN row is closed by an arm that runs each candidate rule and shows where they diverge, and by physics or evidence where they can decide. Writing the rule into a validator is not what closes it. The leak scan is the one gate that enforces, and the reason is physical, not a preference: exposure only adds.

## Later (2026-11-19): REVIEW-2 and AUDIT-2

The open line in `../MODE_SEQUENCE.md` is answered by the owner's independence rules in that file's dated section. A REVIEW-2 reader differs from the implementer. In AUDIT-2, the implementer may rerun a deterministic check only if its design was reviewed by a different reader; a judgment check, including test and fixture design, needs a different auditor. Every REVIEW and AUDIT return adds the independence fields and level, as defined in `INDEPENDENCE_LEDGER.md`.

## Later (2026-11-19): standing rule for merge reports

The owner's rule, 2026-11-19: every report of a merge carries the suite's counts line and the post-merge CI result, or marks each one NOT READ with the reason. The counts line is the line the suite prints for itself (for example `counts: ran N | passed N | skipped N | NOT_RUN N | failed N`). A local rerun can stand beside the CI result but does not replace it, and it is labelled local, with its interpreter and sibling commits. A run of `check_concept_map.py` or `build_finder.py` also carries its `sibling_state` line, since the NOT_CHECKED and QUOTE_NOT_CHECKED counts depend on which siblings were present.

## Later (2026-11-19): the source text of the headers, by segment

SOURCE: Kimi, 2026-11-19 11:46 (owner-stated). Items 1-7, with the header template, the definitions table, the open-row lines and the blind-reading request. The text blocks came as images in the reader's message and as text at its end; they follow the items here, in the order received. Filed verbatim from `as_received/mode_and_authority_2026-11-19.md`, lines 12-89 (line numbers as of the commit that added this section). The headers above were built from this text. If the reader is Kimi, its agreement with this text is recorded L0 (same actor).

```text
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
