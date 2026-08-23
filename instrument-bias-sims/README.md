<!--
SPDX-License-Identifier: CC0-1.0
-->

# instrument-bias-sims

**Marker under exploration, not a thesis.** Nine sims plus one module set, from delivered work
orders, each testing one way an instrument's own construction shapes what it
reports. Nothing here is a position under defense, and the correct response to
any of it is to test the fit, extend it, or report where it breaks.

Stdlib only. Phone-buildable. CC0.

## The nine

| | module | what it tests | what it returned |
|---|---|---|---|
| S1 | `s1_encounter_denominator.py` | event-sampled observation reconstructs a false baseline | claim holds; and the distortion is a **product** of event triggering and cost weighting, neither alone |
| S2 | `s2_symmetric_anchor.py` | welfare-interview anchoring has no null case | the extra arms are not a robustness check, they are **the second equation** — one arm is underdetermined, not merely biased |
| S3 | `s3_rubric_backcast.py` | instrument error rate, without settling what the property is | the rate is **not computable** — and the column varies, which is worse than flat, because what it tracks is permissiveness |
| S4 | `s4_antler_calibration.py` | competition vs motor learning | **patched.** the pre-patch rank series was the antler-rank model's own output, so model A was fitted to its own conclusion; the doe was absent entirely; and the doe-choice arms are **not identified** by paternity share alone |
| S5 | `s5_adversarial_prior.py` | does collective computation require competing agents | the criterion is **not empty** — it is a prediction, and the case it excluded is the case that tests it |
| S6 | `s6_foreclosure_rate.py` | trained responses are terminal, not wrong | the stated uniformity statistic is a **range**, so adding difficulty levels makes it *worse*; a slope does not invert |
| S7 | `s7_hardship_threshold.py` | unanchored thresholds slide to the labeller's baseline | observer-dependence is near-analytic; the cost readout is a **consequence of a stipulation** and says so |
| S8 | `s8_recognition_to_delivery.py` | time as an excuse vs time as a variable | the normalisers agree on the sign and disagree **4286×** about what would count as parity |
| S9 | `s9_corpus_position_filter.py` | a corpus samples observer positions non-uniformly, with nothing filtering | the spec's reason is the two **marginals**; coupling drives the conjunction's excess **above** 1.0, so the multiplicative reading **overstates** suppression by up to 1.85× |
| S10 | [`allocation_coupling/`](allocation_coupling/) | tenure → hours → coupling → record, as four modules with a runner | the **residual is 79% of the total effect** — a per-link table cannot hold the cross-term the spec says the finding is in |

Every module exposes `report()`, `confidence()`, `breaks()` and `--selftest`.

## Six results that ran against the draft

Recorded rather than smoothed, because a sim that only ever confirms the prose
around it is not being run.

- **S3.** The false-null column was drafted as flat and uninformative. It
  varies 0.12–1.00, and the spread tracks **how readily an instrument grants** —
  because the case list contains nothing that penalises granting. An instrument
  granting every case would take the best score.
- **S6.** Adding difficulty levels was expected to strengthen the diagnostic.
  It **inverts** it: `spread = max − min` is a range, the expected range of *k*
  noisy estimates grows with *k*, and at n = 20 the stated diagnostic grades OK
  on two levels and `CONSTANT_FIRES` on nine.
- **S8.** The normalisers were expected to disagree on the sign. They don't, at
  the declared placeholder. They disagree about **where the sign flips**, by
  4286× — which is the same finding one step further back.
- **S9, interaction.** The conjunction was expected to be suppressed *more*
  than the product of its marginals. It's suppressed **less** — excess rises to
  **1.85** at high coupling, because when remoteness drives both axes the two
  conditions select nearly the same people while the product keeps multiplying
  as though they were independent. The multiplicative reading, which is the one
  a reader reaches for, **overstates** the suppression.
- **S9, second-order.** Content was expected to take over as the surface mix
  rose. It never does: a relevance score defined as closeness to the corpus mean
  is a **typicality** measure, so middling items score highest and the content
  correlation stays under **0.2 at every mix**. What the sweep locates is where
  the score stops tracking *position* — it never starts tracking quality.
- **S10 / M4.** The readout compared |r| only and reported "tracks generated
  observations" for a correlation of **−0.85**. The sign was the finding and the
  magnitude comparison lost it. The assessed gradient doesn't track generation —
  it **inverts** it, which is stronger than the spec predicted.

## Structural rule, adopted from the S4 patch

**The AGENTS section comes first, before any equations, and a missing agent
must be a visible `[BLANK]` — never an omission buried in prose.**

S4 is where this was earned. The pre-patch version had no doe in it at all —
not as a blank, as an *absence* — so access was a function of the buck alone in
both models and the question of what a doe tracks could not be posed. The
omission lived in prose, so nothing rendered it and nothing could check for it.
`agent_table()` now renders blanks; `PRE_PATCH_OMISSION` records the state
before rather than quietly fixing it.

## What the S4 patch turned up

- **B2 was a defect in my code.** `rank_prospect` was hardcoded
  `{1: 0.25, 2: 0.60, 3: 0.85}` — derived from the antler-rank model, so
  model A was fitted to its own conclusion and could not fail. Both arms now
  run: A's trend is **9.3× steeper** under the circular arm, and under the
  paternity-derived arm it predicts a nearly flat rate, so **any** observed
  year-trend refutes it. The pre-patch code could not produce that test.
- **B3 is not identified by the stated test.** `arm_size` carries a free
  selectivity exponent and reaches the observed young-buck paternity share at
  k ≈ 2, so "which arm reproduces the observed distribution" has more than one
  answer. The second observable that would identify it: **paternity against
  antler size within an age class**, which separates size selection from
  anything merely correlated with age.
- **B1's phrase checks out in one sense of two.** "floor = 0 is model A in
  disguise" — on the mature-buck observable the two predict *opposite* things,
  which is maximal separability. What floor 0 does share with model A is the
  structural assumption that competence is acquired once and then fixed.
- **Adding the floor exposed another defect.** `hardware()` modelled antler
  *mass* only, which plateaus — so the annual delta went to zero at maturity
  and the floor would have multiplied zero, contradicting the premise it
  encodes. Geometry changes annually where mass does not; `GEOMETRY_DELTA` is
  now separate and stipulated.

## The excluded subject

[`excluded_subject.py`](excluded_subject.py) — its own entry, not a note per
module, because it is four instances of one shape. A sim built to measure how
a position is excluded turns out to have **no representation for the position
it is about**. Not a wrong value — no slot.

| sim | missing | excluded at |
|---|---|---|
| S4 | the doe | derivation |
| S9 | the filtering agent | derivation *(declared; the blank is the finding)* |
| S10 | the untenured continuous observer | derivation |
| S10/M4 | a position high on generation **and** writing | the five-row list |

**A declared blank is a disclosure. An unreachable agent is the failure.** S9's
blank is correct and is its point; S10's is a limit on what the module set can
say. Same rendering, two states, and the entry keeps them apart. Three of the
four were found by an outside reader, not by the scan — which is the scan's own
limit, since it detects *declared* blanks and every instance started as an
absence nobody had declared.

## Cross-cutting rules, enforced

`crosscutting.py` checks five rules over fifteen modules rather than
restating them:

1. no moral labels in any data structure — **scanned**
2. no intent attribution in outputs; graded terms only (incentive direction,
   cost asymmetry, whether the aggregate steers) — **scanned**
3. confidence as a separate readout, not resolved — **structural, enforced**
4. this README states *marker under exploration* — **checked**
5. a readout comparing correlations compares **signed** values, never
   `abs()` — **AST check, structural**

Rule 5 was earned from S10/M4, where a readout compared |r| only and reported
"tracks generated observations" for a correlation of **−0.85**. Added as an AST
check, it immediately found **a second instance in S9** that nobody had
noticed. Rule 2 then rejected the first draft of `excluded_subject.py` — the
module written to catalogue this class of defect — for the phrase "built that
way on purpose".

The checker is null-tested on a planted violation, so none of the three module
checks is silent by construction. Its own limit is stated at the top of the
file rather than the bottom: **a keyword scan is stepped around by any
paraphrase**, so a pass on rules 1 and 2 means no listed token was found, not
that the rule holds. Rules 3 and 4 are the ones actually enforced — a module
without a separate unresolved `confidence()` or with an empty `breaks()` turns
the folder's test red.

## What is not here

No module reads real data. S3's grid is hand-coded judgement, S6 has no corpus
and does not implement the classification step that is its whole instrument,
S7's cost table is stipulated, S8's present-day interval is an explicit
placeholder, and S4 uses no cervid data of any kind. Each module's `breaks()`
says so in its own terms, and every literature claim carried from the work
order is marked carried-not-verified.
