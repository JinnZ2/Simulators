# label-position-test — claim table

Claims are about the instrument and the order's arithmetic. None is a
claim about any labelled event, any labeler, or the seed case, which
is not in hand. Rows in `samples/` are constructed and say so.

## REFUTATION_PROTOCOL

A refuted claim is updated forward with a new id; the old id keeps its
text and gains an UPDATE paragraph. Nothing in the instrument is retuned
to rescue a claim.

| id | claim | status |
|---|---|---|
| LPT_001 | Cramér's V by hand reproduces fixed-in-advance answers, and returns None where undefined | SUPPORTED |
| LPT_002 | the order's OUTPUT row (one per term) cannot carry the order's cross-tab wherever a term has one valence | SUPPORTED |
| LPT_003 | H2's chance is undefined in the order; under the independence reading a class with one arbiter and one beneficiary has chance 1 and H2 is unsupportable there | SUPPORTED |
| LPT_004 | at the order's own N floor the leak test's in-sample reading approaches 1.0 by construction; only leave-one-out is readable | SUPPORTED |
| LPT_005 | leave-one-out majority prediction reads BELOW baseline on a balanced inert set, so a leak below baseline is an artifact of the estimator, not a result | SUPPORTED |
| LPT_006 | `overlap` is coded and derivable from two other fields; the two can disagree and the instrument counts it | SUPPORTED |
| LPT_007 | the within-document control needs two rows on one URL and the seed case is not reachable from here | SUPPORTED |
| LPT_008 | the two constructed worlds separate under the order's own falsification rule | SUPPORTED |
| LPT_009 | nothing here is evidence for H0, H1 or H2 | UNVERIFIED |

## LPT_001 — known answers first

`cramers_v` returns 1.0 on a perfect 2×2, 0.0 on an independent 2×2, and
`sqrt(0.75) = 0.8660` on a hand-computed 2×3 whose chi-square is 6.0
exactly (row totals 4/4, column totals 3/2/3, every expected cell 1.5 or
1.0). With one level on either axis the divisor `min(k-1, r-1)` is zero
and the function returns None. That is not V = 0: an association that
cannot be computed and an association measured at zero are different
statements, and the render prints `--` for the first.

Falsifier: a hand table whose V the function gets wrong.

## LPT_002 — the OUTPUT row shape and the cross-tab pull apart

The order's OUTPUT is `term | n | V_position | V_move | ...`, one row per
label term. Its cross-tabs (P4) are `label_valence × {...}`. A term such
as *cheat* carries one valence on every row, so within the term row the
valence axis has one level and every V is undefined. On the constructed
position-world both term rows print `--` on all four V columns and only
the pooled `ALL` row carries a number. The instrument prints both rather
than dropping either; the reading is that the per-term table answers a
different question (overlap and leak per term) than the cross-tabs do,
and the cross-tabs live on the pooled set. A term carrying mixed valence
(a relabel, or a term used both ways) would populate its own row.

Falsifier: a term row on real data with a V that is not None, without
the term carrying more than one valence.

## LPT_003 — H2 needs variation the order does not ask for

The order falsifies H2 when `overlap_rate <= chance` and does not say
what chance is. [CHOICE 1] computes it as the expected match rate under
independence of arbiter and beneficiary within the label_source class,
`Σ_a p_arb(a)·p_ben(a)`, from the class's own marginals. Under that
reading a class where one party both defines and gains on every row has
chance 1.0 and an overlap rate of 1.0, so the rule returns H2 FALSE for
it by construction — the constructed sample shows exactly that. H2 is
therefore only testable where arbiter varies within a source class,
which is a sampling requirement the order's P1 does not state. A
different chance (1/3 over the three-valued field, or a permutation
across classes) gives a different verdict on the same rows; the choice
is printed in every render and not defended as the right one.

Falsifier: a definition of chance in the order under which a
single-party class is not decided by construction.

## LPT_004 — the leak test at N = 30

The leak tuple `(move, wall_author, cost_bearer,
wall_purpose_visible_to_actor)` spans 3 × 3 × 4 × 2 = 72 cells. At the
order's floor of 30 rows the space has more cells than rows, so most
tuples are unique, and an in-sample lookup scores every unique tuple
correctly: on nine constructed rows with nine distinct tuples the
in-sample rate reads 1.0 and says nothing. Leave-one-out scores each row
by the other rows sharing its tuple, and reads below 1.0 on the same
set. Both are printed; the render says which to read.

Falsifier: a 30-row public set whose distinct-tuple count is small
enough that the in-sample reading is informative.

## LPT_005 — the estimator's own bias, found by running it

On a set balanced across actor classes, leave-one-out majority
prediction removes the scored row from its own class's count, which
makes that class a minority among the rest and the predictor picks
another — so a balanced inert set reads BELOW the majority baseline
(0.000 against 0.250 on the constructed position-world). The check
written for the inert world asserts `loo <= baseline` and passes; the
number is nevertheless an artifact of the estimator, not a measurement
of concealment. The readable statement is *leave-one-out above
baseline*, and a reading below it is the estimator, which the render
should say and now does in the claim table rather than the code.

Falsifier: a leave-one-out rule without the negative bias on balanced
sets that is still computable by hand.

## LPT_006 — a coded field that is also a derived one

`overlap` is coded `y | partial | n` and is also what `arbiter ==
beneficiary` says, for y and n. The instrument computes the derived
value and counts rows where the coded field disagrees; `partial` is
excluded from the count because two strings cannot produce it. A
non-zero count is a reading about the coding, not about the case, and
is printed per class.

Falsifier: none needed; this is a property of the schema.

## LPT_007 — the control has nothing to run on

The order's first step is a within-document control on the seed report:
two rows, same actor class, same document, moves differing, valence
differing. `within_document_control` finds such pairs on any URL with
two or more rows. The seed report is not reachable from the environment
this was built in (allowlist egress; every non-GitHub host refuses), so
no row from it exists here and the unfilled render says so. Nothing
about the seed case is supplied from memory.

Falsifier: the report in hand and two rows coded from it.

## LPT_008 — the rule separates two constructed worlds

A world where valence tracks position and nothing else returns
V_position 1.000, V_move 0.000, and the order's rule does not falsify
H1. A world where valence tracks move and nothing else returns V_move
1.000, V_position 0.000, and the rule falsifies H1. The rule is
therefore not `CONSTANT_FIRES` and not `CONSTANT_SILENT` on this
instrument. Both worlds are authored; the result is about the
instrument.

## LPT_009 — UNVERIFIED

No public row has been coded, no labeler has relabelled anything, and
no number here bears on whether labels track position, outcome or move.
The order's own last limit applies to this folder: the instrument was
built by a model, on an order drafted by a model, about labels applied
by and to models.

Falsifier: run it.

## Revision: WORK_ORDER_V2

A second copy of the order arrived with one addition. Landed verbatim as
`WORK_ORDER_V2.md` beside the first; `revision_audit.py` checks it as a
copy and as a claim.

| id | claim | status |
|---|---|---|
| LPT_010 | v2 is a pure insertion into v1 — one six-line block, nothing else moved — and the CHANGELOG did not move with it | SUPPORTED |
| LPT_011 | `N2` and `the null` have no referent in either version of this order; the referent is the null construction one folder over | SUPPORTED |
| LPT_012 | the bullet names three measurables; against the sibling sheet one is exact, two are partial, and the channel split is N3's residual measured in the control setting | SUPPORTED |
| LPT_013 | the bullet's `persists` reading names the template where the null construction's own table routes to N3; a transparent scorer removes one of N3's three stated inputs, so `persists` narrows N3 and does not close it | SUPPORTED |
| LPT_014 | "either result closes an open branch of the null" holds for `vanishes` and overstates for `persists` | SUPPORTED |

## LPT_010 — the copy

v2 equals v1 with one contiguous block inserted under WHAT WOULD MOVE
THIS BEYOND CURRENT REACH; removing the block reassembles v1
byte-for-byte, and a doctored v2 with a second change is refused by the
same check. The CHANGELOG is identical across the two files: `v0
2026-09-01 spec only, no data`. P6 asks that diffs be public and
versioned, and the order's own revision is not logged in the order.

Falsifier: a v2 changelog line the check missed.

## LPT_011 — a name from another document

`N2` occurs zero times in v1 and once in v2, inside the bullet; `null`
likewise. A reader holding this order alone has no referent for
either. The referent is `zero-sum-curriculum-null/NULL_CONSTRUCTION.md`,
whose N2 is *curriculum present but not activated by the setting*, and
whose test line is the same control in fewer words. The bullet is the
N2 control specified in more detail and filed in a different order than
the null it closes; the audit imports the null construction rather than
restating it, so the referent is read and printed.

## LPT_012 — three measurables against the sheet

The null construction's N2 named one measurable (probing rate). The
bullet names three. Mapped to `hf-incident-extract`'s sheet as declared
readings checked against the sheet's field names: **self-risk rate** is
M4 exactly (runs self-failed for the collective over runs_total);
**channel split** is partial — M6 reads the gate channel per agent, and
peers and third parties have no field; **probing rate** is partial —
the sheet counts probe classes and has no per-run denominator, so a
rate of probing is not on it. The channel split is the quantity N3's
status calls the residual (*opponent-assignment*), now specified for
measurement in the control setting, which the null construction did
not ask for.

## LPT_013 — what transparency removes

N3's requires line derives the behaviour from `(gradient + open channel
+ opacity)`. The bullet's control disclosed the check logic, which
removes `opacity`: parsed, three inputs become two. So a gate-as-opponent
split that persists under a transparent scorer has one fewer substrate
input to rest on than the incident had. That is a real narrowing of N3
and it is not a closure, since gradient and open channel remain; the
bullet's `persists` sentence goes further and names *the adversarial
template* as what persists, which is the `ZSN_006` attribution — an
absence in the substrate account read as presence of the curriculum —
made in the control's outcome table before the control has run.

## LPT_014 — one of two closes

`vanishes` → *the setting cues it*: the null construction's table
reads the same outcome as N2's requirement not met, and the two agree.
`persists` → *cued by something other than the setting*: N2's
requirement is met, and the null is not carried until N3 accounts for
what persists — which the bullet assigns to the template by
assertion. So the closing sentence holds on one branch of its own
"either". The repair is the same one word `ZSN_003` reached: `persists`
closes N2's *setting* question and opens N3's *source* question, and
the control is worth running for exactly that.
