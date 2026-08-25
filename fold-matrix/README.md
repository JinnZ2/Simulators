# fold-matrix

Work order 8, delivered verbatim in `WORK_ORDER.md`. One term, one grid,
not one number.

| file | |
|---|---|
| `WORK_ORDER.md` | the order as delivered |
| `fold_matrix.py` | the grid and every rule in it. `--selftest` |
| `terms/` | the four S6 fixtures, as data |
| `PREDICTIONS_WO8.md` | S2's prediction, registered before the fixtures |
| `CLAIM_TABLE.md` | `FM_001..009` |
| `samples/` | one pinned run of each |

```
fold_matrix.py run [TERM_ID ...]
fold_matrix.py --selftest
```

## The arm this extends is not here

The order opens *"the downward arm already has a reading"*. There is no
folded-term instrument in this repository: `severed`, `still_acting` and
*deepest still-acting term* return zero hits across the tree before this
folder. Seventh instance of the stated-thing-with-no-artifact shape, and
the largest — the prior six were a missing field or a missing test.

So the grid holds both arms and **nothing is reconstructed**. H1's levels
−2 and −3 are what the factor physically rests on, this repository has
measured neither, and they carry `ABSENT` rather than a plausible
reading.

## What the fixtures produced

All four behave as S6 requires: H1's downward levels resolve and its
level-0 clock is **derived** (3.0 y ÷ a coupling of 0.8815 **measured by
perturbation**, not asserted); H2 returns `NOT_EVALUABLE` with all three
scope fields named; H3 refuses the comparison as *"nothing was
compared"*; H4 emits both clocks and picks neither.

**And H1 exposed a defect in the instrument.** The first clock check
counted distinct values, so H1 read as a mismatch — level −1 assumes 3.0
years and level 0 derives 3.403 from it. That is **one horizon and its own
derivative**, not two in conflict. The false positive runs toward the
finding, since S5 says a horizon disagreement *is* the finding, so an
over-firing check manufactures them and every derivation chain in the
claim registry would produce one. Repaired with `derived_from`: derived
clocks are still emitted, with what they came from, and only the
disagreement count excludes them.

## The empty cell that has two causes

S2 requires `value_string` per upward cell and says empty is normal. On
H1 level +1 it is empty for a reason the four basis values cannot record:
`Disclaimer!A3` states the goal — *"to support organizations to estimate
their GHG emissions"* — and, **in the same cell**, that the secretariat
*"makes no representations as to the accuracy, completeness, suitability
or validity of any information on this Spreadsheet"*.

That is not `ABSENT`, since a goal is stated, and it is not ordinary
`ASSERTED` either. A relation claimed at adoption with no value string
and a relation the source **refuses** to claim are different facts
arriving at the same empty cell. Carried as `source_disclaims` beside the
basis and printed with the quote, rather than by adding a fifth value to
a delivered vocabulary.

## Refusals that are structural

`NOT_EVALUABLE` is unrankable in code, not by convention: `score()`
raises on it — and raises on an evaluable term too, because there is no
score in this instrument at all. `upward_tally()` excludes refused terms
and names them, so a refusal never enters a count as a zero.

One distinction S3 does not make and the check does: a scope field
**present but declared unknown** is missing too, reported apart from an
omission. `horizon: "unknown"` is honest and still does not let a ratio be
compared, but a gap in the record and a measurement nobody has call for
different next steps.

## Wired, not retyped

`boundary` and `horizon` are two of `declared-frame`'s three CORE fields
and are read out of it at import, asserted in the selftest, so the two
folders cannot drift. `with_respect_to` is S3's addition and asks a
different question — declared-frame asks what is inside the accounting,
S3 asks what the ratio is taken against.

S4's neutral reading is a **declared field**. No string operation turns
*efficiency* into *joules out per joule in, at the cell surface,
instantaneous*; producing one would be inventing a measurement, so a
flagged term without one reports `NOT_SUPPLIED`.

## The exemption

`SSS_049` retired scan 4's exemption and kept its three-arm harness for a
real case. This is one: S3's efficiency class is
*efficient / optimal / better / faster*, and **`better` is on
`no_severity`'s list** while the other three are not.
`DELIVERED_VOCABULARY = ("better",)` — one token, measured three ways,
with a fourth check asserting the list is length one so a widening turns
red.

39 selftest checks. Stdlib only, parses under Python 3.9. CC0.
