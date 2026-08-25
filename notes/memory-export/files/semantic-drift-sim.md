---
name: semantic-drift-sim
description: Semantic/valence drift simulation thread and its unknowns register — screening-electron measurement priorities.
sources: [field]
aliases: [valence_drift_test.py, semantic_drift_test.py]
---

Semantic drift simulation producing `valence_drift_test.py` with an explicit unknowns register.

Two unconstrained parameters identified as immediate measurement priorities:

1. Whether screening electrons are catalytic or consumable
2. The functional form of screening

Both are load-bearing: the simulation's behaviour over long runs depends on which branch is
true, and neither is currently constrained by measurement.
