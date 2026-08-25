# memory-export

Backup storage for a memory set exported out of session. Same rule as
`notes/operators/`: files are stored as delivered, and nothing here edits what
it stores. Readings go in `notes/FINDINGS_MEMORY_EXPORT.md`.

Most of these are markers, specs and gap lists, and several say so in their own
first line. Not all — `diversity-collapse-model` reports a CLAIM_TABLE and
states the refutation protocol applies to it.

## Layout

| path | what |
|---|---|
| `SCRUB_RULES.md` | scrub rules and tier assignment for the export. 57 tier 1, 7 tier 2, 12 tier 3. |
| `files/` | the exported files, one per file, stored as delivered. |

## Arrival state

| tier | named in the manifest | landed |
|---|---|---|
| 1 — exported unchanged | 57 | 35 |
| 2 — scrubbed and exported | 7 | 7 |
| 3 — held back | 12 | 0, and none expected |

Tier 2 is complete. Tier 3 is held back by the manifest's own decision — its
absence is a choice recorded upstream, not a gap here.

Tier is inferred, not carried: the manifest labels no file individually, so a
file is filed tier 1 when it was exported and is not in the tier-2 table.

## The cost

`SCRUB_RULES.md` names three files that pay most for the scrub, and all three
have landed. The reasoning is intact; the standing behind it is not carried.
That was the trade taken deliberately, and re-attaching the names is not a
repair. Detail in finding 10.

CC0.
