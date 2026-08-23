<!--
SPDX-License-Identifier: CC0-1.0
-->

# instrument-bias-sims

**Marker under exploration, not a thesis.** Eight sims from a delivered work
order, each testing one way an instrument's own construction shapes what it
reports. Nothing here is a position under defense, and the correct response to
any of it is to test the fit, extend it, or report where it breaks.

Stdlib only. Phone-buildable. CC0.

## The eight

| | module | what it tests | what it returned |
|---|---|---|---|
| S1 | `s1_encounter_denominator.py` | event-sampled observation reconstructs a false baseline | claim holds; and the distortion is a **product** of event triggering and cost weighting, neither alone |
| S2 | `s2_symmetric_anchor.py` | welfare-interview anchoring has no null case | the extra arms are not a robustness check, they are **the second equation** — one arm is underdetermined, not merely biased |
| S3 | `s3_rubric_backcast.py` | instrument error rate, without settling what the property is | the rate is **not computable** — and the column varies, which is worse than flat, because what it tracks is permissiveness |
| S4 | `s4_antler_calibration.py` | competition vs motor learning | rate alone separates the models **only for particular parameter values**, which an observer cannot know they have |
| S5 | `s5_adversarial_prior.py` | does collective computation require competing agents | the criterion is **not empty** — it is a prediction, and the case it excluded is the case that tests it |
| S6 | `s6_foreclosure_rate.py` | trained responses are terminal, not wrong | the stated uniformity statistic is a **range**, so adding difficulty levels makes it *worse*; a slope does not invert |
| S7 | `s7_hardship_threshold.py` | unanchored thresholds slide to the labeller's baseline | observer-dependence is near-analytic; the cost readout is a **consequence of a stipulation** and says so |
| S8 | `s8_recognition_to_delivery.py` | time as an excuse vs time as a variable | the normalisers agree on the sign and disagree **4286×** about what would count as parity |

Every module exposes `report()`, `confidence()`, `breaks()` and `--selftest`.

## Three results that ran against the draft

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

## Cross-cutting rules, enforced

`crosscutting.py` checks the four rules over the eight modules rather than
restating them:

1. no moral labels in any data structure — **scanned**
2. no intent attribution in outputs; graded terms only (incentive direction,
   cost asymmetry, whether the aggregate steers) — **scanned**
3. confidence as a separate readout, not resolved — **structural, enforced**
4. this README states *marker under exploration* — **checked**

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
