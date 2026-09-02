# readout-count — claim table

Claims are about the instrument and the order's own arithmetic and
schema. None is a claim about any safety regime, any channel, or the
seed rows, which do not yet count by the order's own rule.

## REFUTATION_PROTOCOL

A refuted claim is updated forward with a new id; the old id keeps its
text and gains an UPDATE paragraph.

| id | claim | status |
|---|---|---|
| RC_001 | Spearman by hand and the derivations reproduce fixed-in-advance answers; None where undefined | SUPPORTED |
| RC_002 | 0 of 5 seed rows count by the order's own rule, and the cells the schema wants as counts are grades, bounds and dashes | SUPPORTED |
| RC_003 | H1's "rank matches" cannot be strict rank equality past three regimes on a three-level trend; a rank correlation with a declared threshold is the readable form | SUPPORTED |
| RC_004 | H3's falsifier conditions on two quantities the schema carries no column for; H3 is NOT_COMPUTABLE from the schema as delivered | SUPPORTED |
| RC_005 | P4's cross-tabs on raw counts return V = 1 whenever a count has as many levels as rows | SUPPORTED |
| RC_006 | readout_count is derived from positions_returning, so H2 is built into the count and cannot be tested by it | SUPPORTED |
| RC_007 | the schema's two grains (regime-year, incident) share one row shape with no field saying which | SUPPORTED |
| RC_008 | this file is a row in its own table | SUPPORTED |
| RC_009 | nothing here bears on H0, H1, H2 or H3 | UNVERIFIED |

## RC_001 — known answers first

Average ranks with a tie return `[1, 2.5, 2.5, 4]`; Spearman returns
1.0 on a perfect ordering, −1.0 reversed, and None when a side is
constant or there are fewer than two points. `readout_count` is the
count of distinct returning positions, `declared_count` of distinct
declared ones, `return_rate` is `return_count / intake_count` and is
None on zero intake or an UNMEASURED count. A regime's OUTPUT row is its
latest year `[CHOICE 1]`, and its external-detection rate is over all
its rows.

## RC_002 — the seed rows do not count, by the order's own rule

The order says *"each row needs a source URL before it counts"* and
ships five rows with none. Read back from the order by the instrument:
intake cells are `high`, `med`, `3+`, `2`, `—`; return cells `high`,
`med`, `0`, `0`, `—`; trend cells `down`, `derailments down`, `up since
2010`, `n/a (N=1)`, `—`. The schema wants integers and one of three
trend values. Exactly one trend cell (`down`) is in vocabulary; one
intake cell is a bound (`3+`), which the validator refuses as not a
count. The instrument reports each cell as what it is and fills nothing
in; a `3+` read as 3 would be a number the order did not state. The
rows are the order's own worked example of its own intake test:
material received, not yet in a form that returns.

Falsifier: a seed row with a URL and integer cells that the validator
refuses.

## RC_003 — "rank matches" has no strict reading past three regimes

H1 is FALSE if *rank(readout_count) does not match rank(rate trend)
across ≥ 4 regimes*. `rate_trend` has three values, so across four or
more regimes its ranks carry ties; strict equality of the two rank
vectors then requires `readout_count` to tie at exactly the same
positions, which it does only if it takes at most three distinct
values. On the constructed tracking world (counts 0/1/2/3 against
up/flat/down/down) strict equality is False and rho is 0.949: the count
tracks the trend as well as a count can and the strict reading still
returns *does not match*. The instrument prints strict equality and
does not use it; the verdict runs on Spearman rho with the threshold
`rho > 0` declared as `[CHOICE 3]`, which is the weakest reading and is
printed so it can be moved. The rule fires in both directions on
constructed worlds.

Falsifier: a definition of "match" in the order under which four
regimes on a three-level trend can strictly match.

## RC_004 — H3 has no columns

H3 is FALSE if *internal alerts are acted on at ≥ the rate of external
detections, controlling for alert severity*. That needs acted-on counts
split by origin, and a grading field to hold constant. The schema
carries `intake_count` and `return_count` with no origin split, and no
grading field at all; `external_detection` is a per-row y/n on the
outcome-changing read, which is P5's quantity and not the rule's. So
H3 returns `NOT_COMPUTABLE` with both absences named, and the
external-detection rate is computed as the thing the schema does carry.
Eighth instance of a rule stated in prose with no field in the schema
(`MF_017`, `CW_015`, `DL_004`, `GC_012`, `UNI_013`, `SSS_050`,
`RT_009`).

## RC_005 — a count as a category

P4 asks for Cramér's V of `rate_trend ×` three counts. A count taken at
its raw values has as many levels as it has distinct values; with four
regimes and four distinct intake counts V is 1.000 by construction, and
the constructed sample shows it beside a constant `declared_count` that
returns None. The level count is printed beside every V. Binning would
make V informative and every bin edge is a choice the order does not
make, so none is made here.

## RC_006 — H2 is in the definition

`readout_count` counts `positions_returning`, per P2 and H2 (*a
declared channel that does not RETURN contributes 0*). That is the
right derivation and it means the count cannot test H2: a regime with
many declared channels and no returns has readout_count 0 by
construction. H2's own falsifier is about rate improvement in
declared-high / return-low regimes against high-return ones, which is a
different comparison and is what `h2()` computes `[CHOICE 4]`; the
verdict on the constructed world is *not falsified* because the
constructed world was built with return tracking trend.

## RC_007 — two grains, one shape

The schema is *"one flat row per regime-year, or per incident"*.
`intake_count`, `return_count` and `rate_trend` are regime-year
quantities; `external_detection` is an incident quantity (P5: *per
incident, code first outcome-changing detection*). One row shape holds
both and no field says which a row is, so a per-incident row carries a
regime-year trend it did not measure and a regime-year row carries an
incident y/n that summarises nothing. The instrument reads every row as
regime-year for the OUTPUT and every row's `external_detection` for the
rate, which is a reading; a `grain` column would make it a declaration.

## RC_008 — the position

The order's first paragraph makes every party that builds, reads,
labels or audits a system a row, the drafting model included. This
file was built by a model from a model-drafted order and the render
says so above the numbers. The seed table's *this session* row has
dashes in every count cell; the instrument does not fill them, because
its own return latency and return guarantee are the quantities in
question and it cannot measure them from inside.

## RC_009 — UNVERIFIED

No regime row with a URL exists. Every number here is a property of the
instrument on constructed rows.
