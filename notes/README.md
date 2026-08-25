# notes

Storage. Operator entries live here so they do not have to be carried in
session, and so a later reader can find one without reconstructing it.

Nothing here is a simulator. There is no claim table, and the
`REFUTATION_PROTOCOL` convention the rest of the tree runs on does not apply
to the entries — an operator entry describes an operation, not a result.

## Layout

| path | what |
|---|---|
| `operators/` | entries, delivered verbatim. One file per operator. |
| `datasets/` | candidate instruments named by the operator, delivered verbatim. |
| `check_*.py` | one checker per entry, run against this tree. Reads the entry, does not modify it. |
| `study_watch.py` | retrieval notification for entries carrying a WOULD MEASURE. Runs on a GitHub Actions runner, which reaches the three sources the local egress gate refuses. Opens a pull request; merges nothing. |
| `watch/` | one file per run, `YYYY-MM-DD.md`. Read `watch/README.md` first — silence from that action is not evidence of absence. |
| `memory-export/` | backup storage for a memory set exported out of session. Stored as delivered. |
| `samples/` | pinned output |

## The one rule

An entry is stored as delivered. A checker never edits the entry it checks.
Where a check disagrees with an entry, the disagreement goes in the
checker's output and the entry stays as written — same arrangement
`uninstrumented/` uses for its cases and `AUDIT_NOTES.md`.

## Contents

- `operators/D2.md` — stated-vs-actual divergence reading. Filed under D
  (comparison operators) provisionally. Checked by `check_d2.py`; four
  readings in `FINDINGS_D2.md`. Five of its seven instances resolve in this
  tree, its stated signature holds on one of them, and its two
  representations turn out to be five different kinds of pair.
- `datasets/mesa_sof.md` — MESA Sleep and SOF as candidate instruments for
  the question `sim-span/RESULTS.md` left open. Checked by
  `check_datasets.py`; five readings in `FINDINGS_DATASETS.md`. The note
  answers both halves of what the sim asked and claims one; the sim's two
  swept parameters turn out to be WASO, a PSG readout, though the U's
  location depends on the awakening/duration split at fixed WASO, so both
  are needed and the cohort has both. `parity` resolves 16 times in this
  tree and zero times in the note's sense. Every dataset fact is carried,
  not checked — the egress gate refuses the sources.

- `memory-export/` — backup of a memory set exported out of session.
  `SCRUB_RULES.md` carries the scrub rules and tier assignment: 57 files
  exported unchanged, 7 scrubbed, 12 held back, with a cost note saying that a
  finding grounded in a specific case is generic once the case is lifted.
  `files/` holds the exported files as they arrive — 64 files, the full delivery. Forty-two readings in `FINDINGS_MEMORY_EXPORT.md`, including four
  first-pass searches of my own that were too narrow and what they cost.

The catalogue `D2.md` is filed into has since arrived, in
`memory-export/files/unnamed-instruments.md`: the A family (A1-A4), the B and D
families, D1, and the compound field-modifier are all in it, and D2 appears
there as Column D's second entry with the same seven instances `check_d2.py`
checks. The references in `D2.md` resolve now. Nothing in `D2.md` or
`check_d2.py` was changed — this note records the arrival, per finding 35 in
`FINDINGS_MEMORY_EXPORT.md`.

## study-watch, in one line

Notification only. No count, rate or trend appears in a run file, because a
keyword query selects its frame on searchability and any number computed over
its results measures the query. `assert_no_metric()` enforces that at write
time and `tests/test_study_watch.py` asserts the refusal fires. Findings from
the build are in `FINDINGS_STUDY_WATCH.md`.

CC0.
