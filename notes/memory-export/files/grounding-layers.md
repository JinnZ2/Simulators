---
name: grounding-layers
description: Formalizing substrate-primary sensorimotor sensing as an AI calibration channel; live field experiments against cascade predictions.
sources: [field]
aliases: [Simulators, L-epsilon]
---

Formalizes MULTICHANNEL PARALLEL SENSORIMOTOR SENSING — coupled reads of vibration harmonics,
steering pull, damping asymmetry, and similar — as a legitimate calibration channel for AI
systems. Names the knowledge locus L-epsilon.

## Modules

`holistic_field_state.py`, `field_compass.py`, `determinacy_gate.py`. Four stdlib-only CC0
modules built, including a confidence-gated orientation layer tracking deltas between
sensorimotor verdicts and cascade predictions.

## Live field experiments

Real-time driving observations used as falsifiable test cases against cascade predictions.

**Collaboration structure:** the model generates falsifiable predictions; a field operator
observes; mismatches get logged and LOCKED AS CONSTRAINTS. The lock is what makes it a
calibration channel rather than an anecdote stream.

## Framing correction

The value is **two different substrates trading native reads** — sensorimotor plus
constraint-propagation — not a model helping a human translate. Intelligence is a property of
the COUPLED SYSTEM, not located in either node.

This is the correction that distinguishes this project from a data-collection arrangement, and
it is easy to lose: describing it as translation puts the knowledge in one node and the
service in the other, which is exactly the structure the project is testing against.

## Related

Predecessor work produced structural lessons on cascade error patterns; the coupled-system read
engine and confidence-gated channels were under development before the live experiment
sessions. A `simulation-hypothesis-budget` subdirectory exists in the repo.
