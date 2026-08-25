# memory-export

Backup storage for a memory set exported out of session. Same rule as
`notes/operators/`: files are stored as delivered, and nothing here edits what
it stores. Readings go in `notes/FINDINGS_MEMORY_EXPORT.md`.

Most of these are markers, specs and gap lists, and 19 of them say so in their
own first line. `files/ecosystem-conventions.md` carries the ecosystem-wide
reading protocol they are written under — read it before reading the rest, and
before reading `FINDINGS_MEMORY_EXPORT.md`, which is written under it. Not all — `diversity-collapse-model` reports a CLAIM_TABLE and
states the refutation protocol applies to it.

## Layout

| path | what |
|---|---|
| `SCRUB_RULES.md` | scrub rules and tier assignment for the export. 57 tier 1, 7 tier 2, 12 tier 3. |
| `files/` | the exported files, one per file, stored as delivered. |

## Arrival state

**Complete: 64 files stored, against a manifest stating 63.** The off-by-one
is recorded in finding 42 and not resolved — the export does not enumerate its
own contents, so there is no list to diff against.

All 46 cross-reference names resolve; the link graph closes with none dangling.

The manifest was revised after delivery finished. The version this folder was
built against split the export into tier 1 "exported unchanged (57 files)" and
tier 2 "scrubbed and exported (7 files)". The final version replaces both with
a single **tier 1 and 2, condensed, scrubbed and exported (63 files)**, and
states that **no file was exported unchanged** — every one was rewritten, with
material reorganized where the original order obscured the argument.

So the 57/7 split this folder tracked per batch never described the delivery,
and the per-file tier assignments inferred here were inferences about a
distinction that does not exist. Detail in finding 41.

Tier 3 remains 12 files held back by the manifest's own decision, not a gap
here.

`SCRUB_RULES.md` holds the final version. The superseded one is in this
folder's git history, first stored at the top of the branch.

## Scrub exemption, from `median-case-calibration` onward

The operator directed that later files be **exempt from the manifest's
person/place/occupation rules, to keep the memory dump intact**. So from
`median-case-calibration` on, `SCRUB_RULES.md` no longer describes what is in
`files/`.

Concretely, that file carries occupational detail, equipment, operating
conditions and a scale figure of the kind the manifest lists as categorically
removed. It is stored as delivered and was not scrubbed here.

This is recorded so a later reader does not read the difference as a scrub
failure, and does not use `SCRUB_RULES.md` as an index of what the folder can
contain. The manifest still describes the seven tier-2 files accurately; it no
longer describes the folder.

## The cost

`SCRUB_RULES.md` names three files that pay most for the scrub, and all three
have landed. The reasoning is intact; the standing behind it is not carried.
That was the trade taken deliberately, and re-attaching the names is not a
repair. Detail in finding 10.

CC0.
