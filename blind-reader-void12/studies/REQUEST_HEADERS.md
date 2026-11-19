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

## The baseline is not touched by any mode

D0 is the brief unchanged. Each clarification is its own condition (`instructions/`). Past responses, scores and keys stay as filed. A new version gets a new hash and a changelog. Nothing in this file is sent to a blind reader except the BLIND header.
