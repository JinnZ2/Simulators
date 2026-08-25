# fold-matrix

Work order 8, delivered verbatim in `WORK_ORDER.md`. One term, one grid,
not one number.

| file | |
|---|---|
| `WORK_ORDER.md` | the order as first delivered |
| `WORK_ORDER_V2.md` | the revision, verbatim. Supersedes it; both kept |
| `fold_matrix.py` | the grid and every rule in it. `--selftest` |
| `terms/` | the four S6 fixtures, as data |
| `PREDICTIONS_WO8.md` | S2's v1 prediction |
| `PREDICTIONS_WO8_V2.md` | the revised prediction, and what is not blind about it |
| `CLAIM_TABLE.md` | `FM_001..018` |
| `samples/` | one pinned run of each |

```
fold_matrix.py run [TERM_ID ...]
fold_matrix.py --selftest
```

## The revision, and what it recovered

`WORK_ORDER_V2.md` supersedes the first order; both are kept unedited so
the difference is diffable. Two changes: **S1a is entirely new**, and
**`value_string` becomes three independently ABSENT-able fields** where
it was one free-text string.

**The fixed format recovers information the free-text field destroyed,
and that is the revision's result.** Under v1 every upward cell here read
`empty`. Under the triple, `Disclaimer!A3` — *"in order to raise
awareness and to promote climate action"* — states a **direction** and no
size:

| level | sign | magnitude | unit |
|---|---|---|---|
| +1 | ABSENT | ABSENT | ABSENT |
| **+2** | **+** | ABSENT | ABSENT |
| +3 | ABSENT | ABSENT | ABSENT |

*Sign yes, magnitude no, unit no* is the ordinary shape of a purpose
claim, and one field recorded it as identical to a cell nobody wrote
anything in. Across the tally: `sign` ABSENT on 3 of 4, `magnitude` and
`unit` on 4 of 4.

The v1 form is **refused, not coerced**. An empty string cannot say which
of the three is missing, so mapping it to all-three-absent would assert
something the v1 data never recorded. All four fixtures were migrated by
hand.

## S1a: the floor is what was calculated, not what exists

*"Joules are not the floor unless joules were calculated."* H1's grid
names four downward levels and the workbook computes at exactly one:

| level | quantity | unit | computed |
|---|---|---|---|
| 0 | emissions | kg CO2e | **yes** — entered kWh × the factor |
| −1 | generation mix shares | fraction | no — the factor arrives as a constant |
| −2 | marginal plant heat rate | MJ/kWh | no |
| −3 | CO2e per unit fuel energy | kg CO2e/MJ | no |

**Downward stop level 0, `unmeasured_span` 3 levels.** Every level below
the stop names a real quantity with a real unit and the chain runs
through all of them; a naive reading would put the floor at −3 and the
span at zero.

`computed` is a **declared field** and `validate()` refuses a
`quantified` block without it. A reader filling it in from the physics —
*there is obviously a heat rate, so put one here* — is exactly the reader
the rule is written against, and the schema stops them at load.

The span **understates by construction**: it counts what the grid names,
and a grid that stops early reports a smaller span than the world has.

**The `FM_016` fix makes that readable instead of disclosed.**
`enumeration_basis` is declared per term — `document_named` /
`physical_traced` / `author_read` / `UNREAD` — and **never inferred**: a
grid loaded without it *declares* UNREAD rather than getting one assigned
from how well traced its levels look. That is `FM_013`'s refusal again,
sharper here, because a plausible level list is exactly what an author
produces from general knowledge without tracing anything. H1 declares
`author_read`, which is the unflattering answer and the true one: the
workbook names none of those levels.

**And the emitted number is renamed.** `unmeasured_span: 3` reads as a
measurement of the world; **`unmeasured_span_min: 3` reads as a floor**,
which is what it is. Before the amendment the honest reading lived in a
`note` string where nothing downstream could see it — the same shape as a
workbook stating a relationship in prose that no cell maintains, which is
the object scan 4 exists to find.

**Cross-document comparison now requires a matching basis.** H1 is
`author_read` and H4 is `document_named`, so the 3-vs-0 contrast this
README used to report is **refused**: both floors are emitted and the
difference is not computed. A selftest check reads the module's own
source and asserts no subtraction of two `span_min` values appears in it.
`FM_016` is corrected in place rather than defended.

`plan_exists` / `practice_tracks_plan` is its own column and the code
cannot merge it into `basis` — asserted in the selftest.
`practice_tracks_plan` defaults to **UNREAD**, never to `no`: a plan
nobody checked and a plan practice departs from are different findings.

## Zero is not absent

S7 says empty emits as empty, never as zero. The converse needs saying
too: **`magnitude: 0` is a claim** — the proxy is stated to move the goal
not at all — and `ABSENT` is the absence of one. The most confusable pair
in the format, kept apart and pinned both ways.

## What is not blind

`Disclaimer!A3` was already read in this session during the v1 run, so
P3 and P4 are **not blind predictions about that text**. They are
registered because the format is new and the split had not been computed.
`PREDICTIONS_WO8_V2.md` says so in full. What would be blind is the same
format on a workbook nobody here has opened, and `SSS_053` is why there
is not one.

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

74 selftest checks. Stdlib only, parses under Python 3.9. CC0.
