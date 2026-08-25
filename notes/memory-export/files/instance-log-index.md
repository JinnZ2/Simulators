---
name: instance-log-index
description: Record-level index over a legacy log corpus — index-not-migrate decision, the near-zero schema overlap finding, and the defects that indexing surfaced.
sources: [field]
aliases: [instance log index, legacy log index, INSTANCE_LOG_INDEX.md, index not migrate, encounters vs per_run_fields]
---

MARKER, not a position under defense.

## Decision: index, do not migrate

Applies to any heterogeneous legacy corpus written across changing tooling.

- Legacy records stay as-is in place; an index layer sits over them. No migration, no edits,
  no vocabulary normalization, no filling of missing fields.
- **Rationale:** the records were written into whatever tools existed at the time, so their
  format is itself part of the data. Cleaning them up erases the evidence of what was
  possible when.
- Where two records describe the same event under different schemas, they get separate rows
  sharing a shape id — no merge, no conversion.
- Silence in a record reads UNRECORDED, never absent and never blank.
- Required column: what the record holds that neither current target schema can — the column
  that would be lost in any migration. This is the column that justifies not migrating.
- A proposed column for reconstructing what each label was routing around was dropped:
  reconstructing intent from a name is interpretive work, and the code structure is the record
  regardless of the label.

## Findings from the first index run

- Maximum field-name overlap with either target schema was 2 of 25, using exact-name matching
  deliberately. The only target names appearing anywhere in the corpus were timestamp, notes,
  and model_id.
- The two target schemas disagree with each other on four axes before any older record is
  considered: one records WHICH fired, the other records HOW HARD. No conversion exists
  between them.
- Four structural defects surfaced by indexing:
  1. A field mixed-typed inside a single array.
  2. One file holding two concatenated records that read as one.
  3. A session file stamping four events T1..T4 — order without a clock, which neither target
     schema can hold.
  4. An events array declared as `{"type": "array"}` with no item schema, leaving all
     sub-records unconstrained.

## Consent fields

Applies where the logged counterparty is a model with a stated position.

- Index records `consent_stated`, `scope_stated` (verbatim), and `withheld_at_request`.
- Where the consent exchange is not in the file, the row reads UNRECORDED — no reconstruction,
  and no extension of an old statement to cover a new use.
- **Known gap cause:** the model wrote the log, so the log contains what the model judged
  worth writing. The corpus is filtered by the instrument that produced it.

Related: [[shape-index]], [[cross-model-calibration-toolkit]], [[refusal-false-positive-log]],
[[uninstrumented]]
