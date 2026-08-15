# CLAIM_TABLE — aperiodic-order-sim-stack

Claims made by the drop (`SIM_STACK_REPORT.txt`) and by the audit
(`README.md`), each with the measurement that would refute it.

`who` follows the [`claim-audits/`](../claim-audits/) convention:
**D** = the drop's own claim, **A** = an audit claim added here.

## REFUTATION_PROTOCOL

The generators were not shipped, so no claim below can be settled by
rerunning the original sims. Each falsifier is therefore written as a
*new* run someone with the generators can perform. Two rules, matching
the repo's standing practice:

1. A failed check updates the **claim**, not the estimator. If a
   falsifier fires, the entry is rewritten to what the new measurement
   says. Nothing here is retuned to preserve a prior.
2. Absence of a detected feature is never entered as evidence of a
   difference unless a positive control has shown the method detects
   that feature when it is present. `AOS_005` exists because the drop
   broke this rule.

---

## AOS_001 — the two shipped dimension estimators disagree in sign

**who:** A &nbsp;·&nbsp; **status:** SUPPORTED

Box counting gives `D_f(AB) − D_f(Cascade) = +0.334` (plateau fit) and
`+0.240` (global fit). The sandbox estimator, on the same five point
sets in the same drop, gives `−0.247` (global) and `−0.023` (plateau).
The report publishes only the box-counting family and does not mention
the disagreement.

**Falsifier:** produce the sandbox numbers from the report, or show the
sandbox figures were generated from different point sets than the
box-counting figures. Either would dissolve the contradiction.

**Evidence:** `figures/sim_b_boxcount.png`,
`figures/sim_b_boxcount_local.png`, `figures/sim_b_sandbox.png`,
`figures/sim_b_sandbox_local.png`, compared against
`SIM_STACK_REPORT.txt`.

---

## AOS_002 — the sandbox estimator fails its own 1D control

**who:** A &nbsp;·&nbsp; **status:** SUPPORTED

The Line point set has an exactly known `D_f = 1.000`. The sandbox
estimator returns `1.913` (global) and `1.844` (plateau) — an error
larger than the effect under study. Box counting returns `1.000`.

This is the reason to keep the box-counting result and discard the
sandbox one. It is stated here because the report does not state it.

**Falsifier:** show the sandbox Line panel was computed on a set that is
not one-dimensional, or that its axis is a different quantity than
`log M(r)` vs `log r`. Absent that, the estimator is wrong on a set
whose answer is known.

**Evidence:** `figures/sim_b_sandbox.png` and
`figures/sim_b_sandbox_local.png`, Line panels — the local slope
oscillates around 1.8–2.0 across the whole radius range, so the failure
is not a bad fit window.

---

## AOS_003 — the decisive gap is largely inside the artifact budget

**who:** A &nbsp;·&nbsp; **status:** SUPPORTED

Sample size (12,000 → 1,024) moves box-counting `D_f` by up to 0.137 on
probes whose true dimension is fixed. Box-ladder commensurability moves
it by a further 0.115 on a known fractal at fixed N. Combined worst case
0.252, against a reported separation of 0.334.

The budget is an **upper** bound (worst case per source, signs assumed
to align); the residual 0.082 is a **lower** bound on structure. That
residual still exceeds the report's own 0.021 matched-N baseline by 4×.

**Falsifier:** rerun SIM-B with Ammann-Beenker subsampled to 1,024
points and a Poisson control also at 1,024 in the Cascade's bounding
box. If `D_f(AB@1024) − D_f(Cascade@1024)` stays near 0.334, this claim
is refuted and the drop's magnitude stands.

**Evidence:** `finite_n_control.py`,
`samples/finite_n_control.sample.txt`; point counts read from
`figures/sim_b_point_sets.png`; saturation ceilings visible in
`figures/sim_b_boxcount.png`.

---

## AOS_004 — direction survives; magnitude does not

**who:** A &nbsp;·&nbsp; **status:** SUPPORTED

The Cascade's box-counting dimension is lower than Ammann-Beenker's by
more than the artifact budget can explain. The specific value 0.334, and
the word "decisive," are not supported at that precision.

**Falsifier:** the matched-N rerun in `AOS_003`. A result inside the
0.021 baseline refutes the direction as well as the magnitude; a result
near 0.334 refutes the magnitude half of this claim.

---

## AOS_005 — SIM-C's null is entered as positive evidence

**who:** A &nbsp;·&nbsp; **status:** SUPPORTED

SIM-C's own section reports no correspondence and no sharp threshold —
a null. The OVERALL CONCLUSION lists it as evidence of "different
threshold behavior." No positive control establishes that the method
detects a threshold when one is present.

The knee is separately weak: comparable curvature peaks at
f ≈ 0.45/0.55/0.65/0.70/0.80/0.90, and f = 0.65 falls on a local
*minimum* of the splitting curve.

**Falsifier:** run the same knee detector on a tight-binding model with
a threshold inserted by construction at a known `f`. If the detector
recovers it inside the scatter, the method has been validated and this
claim weakens to the knee-robustness half.

**Evidence:** `SIM_STACK_REPORT.txt` SIM-C section vs OVERALL
CONCLUSION; `figures/sim_c_threshold_sweep.png`.

---

## AOS_006 — no Bragg peaks are visible in the shipped S(k) figure

**who:** A &nbsp;·&nbsp; **status:** SUPPORTED

The report reads Ammann-Beenker as showing "sharp Bragg peaks." The
shipped `S(k)` map shows one bright spot at the origin — the
forward-scattering peak every finite point set has — on a linear color
scale that flattens everything else to black. The eight-fold star is not
visible. The quoted peak/floor ratio of 5537 is approximately
`S(0)/floor`.

Partially offsetting, and stated as such: the radial profile does show
genuine oscillatory structure in AB out to |k| ≈ 20 against a Cascade
that is flat at ≈ 1. AB is not an uncorrelated set.

**Falsifier:** re-plot `S(k)` on a log color scale with `k = 0` masked.
If eight-fold peaks appear, this claim is refuted and the report's
reading stands. This is the cheapest outstanding check in the drop.

**Evidence:** `figures/sim_a_structure_factor.png`.

---

## AOS_007 — the α exponent difference is confounded by the forward peak

**who:** A &nbsp;·&nbsp; **status:** UNVERIFIED

`α_AB = −1.529` vs `α_C = −0.069` is measured on a radial profile whose
dynamic range is dominated by `S(0) ≈ 11,500`. Whether the fit window
excludes the forward peak cannot be determined from the figure, so this
is flagged as a gap rather than a defect.

`UNVERIFIED` here means what it means in
[`claim-audits/`](../claim-audits/): a gap, not a negative verdict.

**Falsifier:** publish the fit range. If it starts well above the
forward peak's shoulder, the exponents are clean and this entry closes.

---

## AOS_008 — the report's substantive direction is probably correct

**who:** D &nbsp;·&nbsp; **status:** PLAUSIBLE, WEAKLY EVIDENCED

Quasiperiodic tilings and branching cascades most likely are distinct
classes of aperiodic order. Nothing in this audit argues otherwise.
The objection throughout is to the strength of the shipped evidence and
to the omission of the disagreeing estimator — not to the conclusion.

**Falsifier:** the `AOS_003` matched-N rerun, plus the `AOS_006`
re-plot. If both come back supporting the drop, the conclusion is
established and this table's audit claims collapse to a note about
reporting practice.
