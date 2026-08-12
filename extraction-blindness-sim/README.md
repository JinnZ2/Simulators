# extraction-blindness-sim

An optimizer does not act on the world. It acts on an observation of
the world. This folder measures what happens in the gap.

**The mechanism under test:** an optimizer whose sensors cannot detect
cumulative degradation reads the absence of an error signal as
confirmation of safety, and will drive a regenerating substrate past
its tipping point while reporting nominal.

That is a falsifiable statement, and `run_experiments.py` measures it.
In the pinned fishery run the optimizer's own reported safety exceeds
true substrate health by **0.5630** at its worst, and the stock
collapses at **step 7** while the controller still reports safety
0.3728 against true health 0.1755.

Stdlib only. Deterministic. `python3 run_experiments.py`.

---

## The three blindness modes

Each is a *structural* property of the measurement apparatus, not a
noise term. None of them go away with more samples. All three are
one-sided: they report the substrate as healthier than it is, never
worse — a property asserted by a test, because it is what makes the
failure mode systematically toward overshoot rather than toward
excessive caution.

**Frame blindness** — the system boundary is drawn around the
extraction yield. State outside the boundary is not measured badly; it
is absent from the observation entirely. Externalities cannot be
mispriced because they never arrive to be priced.

**Model-dependence masking** — a reported quantity at rung M2/M3 is a
model output, not a reading. Outside the bridge model's training
domain the report regresses toward the model's prior rather than
tracking the physical state, so a degrading substrate keeps reporting
near-nominal. Rungs follow the M0–M3 ladder in
`../instrument-epistemology/`. Includes the confirmed
MIR-in-high-clay saturation failure.

**Temporal aliasing** — the decision loop runs faster than the
substrate relaxes. Trend is estimated over a window short relative to
relaxation, against a noise floor; a slow true trend is statistically
indistinguishable from zero over that window. No fudge factor — the
aliasing is emergent from window length, noise floor, and true slope.

---

## Layout

| File | What |
|---|---|
| `substrate.py` | Regenerating stock with depensation and recovery hysteresis |
| `blindness.py` | The three operators plus a composable `BlindnessStack` |
| `indicators.py` | Decay-velocity leading indicators (fishery + soil panels) |
| `boundaries.py` | Hard extraction boundaries — graduated, override-only |
| `throughput.py` | Regenerative Throughput: five competing formulations, two trigger policies |
| `optimizer.py` | The extractive loop and its `reported_safety` output |
| `profiles.py` | Fishery and soil domains, `[SPEC]` vs `[MODEL]` constants marked |
| `run_experiments.py` | Six experiments, one per claim |
| `schemas/` | Telemetry + blindness-audit JSON Schema, verbatim from the source |
| `tests/test_all.py` | Module self-tests plus cross-module invariants |

Every module also runs its own self-test: `python3 substrate.py`, etc.

```bash
python3 run_experiments.py     # the six experiments
python3 tests/test_all.py      # 9 tests, no pytest needed
python3 -m pytest tests/ -q    # or with pytest
```

---

## Results

Full evidence in [`CLAIM_TABLE.md`](CLAIM_TABLE.md), pinned output in
[`samples/experiments.sample.txt`](samples/experiments.sample.txt).

| Claim | Result |
|---|---|
| **EBS_001** blind optimizer reports safety while collapsing | SUPPORTED — gap 0.5630, collapse step 7 |
| **EBS_002** indicators fire before collapse | SUPPORTED — lead 6 (fishery), 24 (soil) |
| **EBS_003** threshold placement dominates authority | SUPPORTED — advisory 1.0000 vs override 0.3107 |
| **EBS_004a** RT as written is inverted vs its own governance rule | SUPPORTED |
| **EBS_004b** additive caloric term masks depletion | SUPPORTED — Version B +0.5167 while carbon falls 30% |
| **EBS_005** fixed RT threshold both false-alarms and misses | SUPPORTED |
| **EBS_006** aliasing is decisive only where the trend steers | SUPPORTED — 0.8798 vs 0.0000 in that regime |

Two of these are worth reading closely because they came out against
the obvious expectation.

### EBS_003 — the hard boundary underperformed the advisory signal

The intuition is that a non-negotiable override must beat a signal that
can be traded away. It did not. The advisory indicators ended at
**1.0000** of pristine; the hard boundaries ended at **0.3107** while
permitting **4.3× more total extraction**.

The boundaries were not broken. They did exactly what they were told.
The specification writes the fishery biomass floor at 50% of B_MSY —
which is **25% of pristine** — while depensation begins at **40% of
pristine**. The floor sits below the threshold it exists to defend, so
the override permits maximal extraction right down to a line already
inside the irreversible regime, then holds the system there and
reports compliance.

Authority applied after the irreversible point is authority over
nothing. Where a threshold sits dominates what power it carries.

### EBS_006 — aliasing is inert unless something acts on the trend

Temporal aliasing initially showed no effect at all. The reason turned
out to be structural: in the first version of `optimizer.py` the
perceived trend fed only `reported_safety`, which is an output, never
an input to the extraction decision. Blindness in a channel no
decision depends on cannot change an outcome.

Adding a `trend_responsive` controller made the mechanism measurable,
and the result is sharp in exactly one of three regimes:

| regime | outcome delta |
|---|---|
| trend not in the control loop | 0.0000 — cosmetic |
| trend steers, no effort ratchet | **+0.8798** — decisive |
| trend steers, ratchet defending a target | 0.0000 — the ratchet dominates |

Clear vision ends at 0.8798 of pristine; the same controller with an
aliased trend ends at 0.0000. But any effort ratchet defending a fixed
yield target overwhelms the trend backoff and collapses the substrate
whether or not it can see.

---

## Contradictions in the source, reproduced not repaired

The source specification supplies mutually exclusive definitions of
Regenerative Throughput and does not reconcile them. `throughput.py`
implements each **as written** rather than picking a house style, so
the disagreement is measurable. Where they diverge in *sign* is the
part that matters for governance.

**Four contradictions the source's own audit identified:**

1. Two mutually exclusive `RT_soil` equations (ratio form vs. additive
   form). Both implemented; neither endorsed.
2. SOC floor depth given as 10 cm in one place and 20 cm in another,
   while the boundary text says 30 cm. `boundaries.py` uses the 30 cm
   integrated value and flags the ambiguity.
3. The fixed `RT < 0.95` trigger is uncalibrated — demonstrated in
   EBS_005 to produce both a false alarm and a missed detection.
4. The caloric term is added after the ratio rather than debited from
   the humified pool — demonstrated in EBS_004b to invert the sign of
   the reported change.

**One the source's audit did not catch:**

5. **The RT metric is inverted relative to its own governance rule.**
   The rule says that when RT falls below its floor the operator must
   "reduce extraction or invest more heavily in restoration". Under
   `RT = Output / (Regen + Reinvest)` as written, both of those
   *lower* RT (0.9130 → 0.7825 and 0.8077). Under
   `RT = (Regen + Reinvest) / Output` both raise it, and `RT > 1`
   carries the natural meaning "regeneration exceeds extraction".
   Found while implementing the control logic against the equation.

These are recorded as open questions in `CLAIM_TABLE.md`, not silently
resolved. Deciding between the RT_soil forms needs field data
correlating each against the SOC floor; deciding the depth needs a
sliding-window integration across 0–10 / 10–20 / 20–30 cm to find
which layer fails first.

---

## What this does not model

Stated plainly because the limitations bound what the results mean.

- **Derived state variables are not independently simulated.** Mean
  trophic level, F:B ratio, qCO2 and the rest are deterministic
  functions of stock depletion. The *ordering* of threshold crossings
  is therefore partly assumed rather than derived. This is the largest
  caveat on EBS_002's lead times.
- **The substrate is deterministic.** No recruitment variability. A
  stochastic substrate would turn EBS_001 and EBS_002 from single
  trajectories into distributions, which is their honest form.
- **`[MODEL]` constants are scaffolding.** `profiles.py` marks every
  constant `[SPEC]` (from the source, a claim about the world) or
  `[MODEL]` (chosen to make the simulation run). The `[MODEL]` ones
  are the first thing to change when better numbers exist.
- **No economics.** No prices, discount rates, or agents. Extraction
  pressure is a fixed target plus an effort ratchet, not a market.
- **One substrate per run.** No spatial structure, no fleet
  heterogeneity, no cross-substrate substitution.

---

## Calibration note

Two targets were initially mis-sized in a way worth recording, because
it is the same error the sim is about.

"120% of F_MSY" was first computed against the textbook logistic
`r*K/4`. But depensation drags the substrate's *true* peak
regeneration well below that (0.0666 vs 0.1000 at these constants), so
the intended 20% overshoot was silently a **1.97× overshoot** and wiped
the stock out in 3 steps. Both profiles now size their targets against
`Substrate.peak_regeneration()`, computed numerically from the actual
stock–recruitment curve.

A model-derived reference point taken for a physical one, producing a
much larger intervention than intended, is precisely the
model-dependence masking failure in `blindness.py`. It is recorded
here rather than quietly fixed.

---

## Repo positioning

Stdlib only. No `numpy`. Same genre as `sustained-activation-gate/` and
`incentive-blindspot-sim/` — a coupled-dynamics simulator with a claim
table and a refutation protocol.

**Provenance.** Built from a design conversation covering optimization
frameworks operating as extractive loops, worked through an AI-optimised
purse-seine fishery and an AI-optimised arable soil. Landed **minus the
narrative** at the user's instruction: the predation metaphor and the
rhetorical framing are dropped, and the mechanism, the numbers, the
equations, the instrument-verification findings, the JSON schemas and
the self-audit are kept.

### Cross-repo connections

- **`instrument-epistemology/`** — the direct parent. Its M0–M3
  model-dependence ladder, transduction chains and observational
  blindness maps are the vocabulary `blindness.py` implements. That
  folder grades instruments; this one puts a graded instrument in a
  control loop and measures what the loop then does.
- **`proxy-investigation-lab/`** — grades proxies and measures Goodhart
  pressure. EBS_005's absolute-vs-relative trigger is the same
  argument at the threshold layer: a fixed cut-off applied across
  substrates with different baselines is not a measurement.
- **`climate-modeling/`** — its load-bearing target is
  **cascade-speed blindness**: smooth, memoryless, Gaussian-driven
  models systematically underestimate how fast collapse arrives.
  EBS_001 is that claim with the model inside the controller rather
  than beside it.
- **`thermal-sensor-degradation-audit/`** —
  `corruption(trend) = corruption(measurement) × corruption(framework)`.
  A sensor degrading *during* the event it records is the same
  structure as a bridge model regressing to its prior as the substrate
  leaves the training domain.
- **`sustained-activation-gate/`** — bistability and hysteresis as a
  tilted double well. `Substrate`'s depensation-plus-hysteresis is the
  same shape in a resource-stock coordinate.
- **`null-harness/`** — a gate must beat a known-null before you trust
  it. The test asserting blindness is never pessimistic is that
  discipline applied to the blindness operators themselves.
- **`gdprf-framework/`** — blindness-adjusted confidence updates. The
  `reported_safety` metric here is the ungoverned version: confidence
  computed from observation alone, with no blindness adjustment. That
  is the failure GDPRF's audit layer exists to prevent.

CC0.
