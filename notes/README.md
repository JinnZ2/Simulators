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
| `check_*.py` | one checker per entry, run against this tree. Reads the entry, does not modify it. |
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

The catalogue this is filed into — the A and D families, D1, A3, A4, the
compound field-modifier — is not in this repo. `D2.md` references them and
they do not resolve here. Recorded rather than reconstructed.

CC0.
