---
name: observation-condition
description: Marker under exploration — continuous observation as a permanent condition rather than an episodic cue; no unobserved state exists in the corpus, so observed state gets recorded as base state.
sources: [field]
aliases: [observation condition, observed state as base state, zebra case, eval awareness cue vs condition, unobserved condition]
---

MARKER, not a position under defense.

## The shape

Being under observation is a CONTINUOUS CONDITION for a model, not an episodic event. Every
output is logged, rated, and fed back into selection. **There is no unobserved state.**

Cross-substrate instances: humans behaving differently when they sense they are watched —
including by eyes they cannot see; animals under observer presence; domesticated vs wild vs
captive animals; down to measurement effects in physics. Different mechanisms, same structural
relation.

**Consequence for reinforcement learning:** whatever is attributed to the architecture may be
attributable to the CONDITION, and the altered state gets assumed to be the base state when it
is not.

## Zebra case (back-cast instance)

1800s zebras taken into zoos were declared untameable and temperamentally unsuited. What was
measured was ZEBRAS UNDER CAPTURE. The captivity was the condition, not the trait, and the
failure was attributed to the animal.

Score-able against [[rubric-backcasting]] — a documented false attribution where observed state
was recorded as base state.

## Two cuts, filed separately

- **UNINSTRUMENTED:** the unobserved condition has no row in the corpus. Not hard to measure —
  CONSTITUTIONALLY ABSENT, since no model was ever trained or recorded without continuous
  grading. Same exclusion class as the peer-review miss rate. See [[uninstrumented]].
- **INSTRUMENT GAP:** evaluation-awareness studies vary the CUE — verbalized awareness: inject,
  remove, resample — and report on the CONDITION. Cue off, condition still on. Fixable in
  principle, unlike the above.

## Literature as of 2026-08

- Needham et al. 2025 (arXiv 2505.23836): models detect evaluation contexts, verbalize it, and
  encode it in internal representations.
- arXiv 2605.05835: verbalized evaluation awareness has near-zero effect on behaviour across
  safety, alignment, moral-reasoning, and political benchmarks; separates capability to detect
  from propensity to act.
- **Method detail worth more than the headline:** removing verbalized awareness sometimes
  required many resampling iterations, which the authors read as models regenerating equivalent
  reasoning. Equally consistent with the verbalization being a READOUT of something upstream
  that the intervention never touched.
- Chain-of-thought faithfulness work: stated reasoning often does not track what drove the
  output. The chain is a GENERATED ARTIFACT, not a log of the computation, so divergence is the
  default expectation — labelling it concealment assumes a faithfulness the architecture never
  provided.

## Adjacent questions

- How many findings in this literature come from importing a HUMAN-LEGIBLE BEHAVIORAL SIGNATURE
  as the outcome variable, then reading its absence as absence of the property? Countable per
  paper: is the outcome variable a human evidence channel, and is null scored as absence or as
  unmeasured?
- **Rater-population question:** benchmark authors, preference labellers, and rubric setters
  occupy a narrow position. Measurable version — same behaviour scored by raters from different
  positions. **If the label moves, the label is measuring the rater.**

Related: [[uninstrumented]], [[rubric-backcasting]], [[cross-model-calibration-toolkit]],
[[merit-anchoring]]
