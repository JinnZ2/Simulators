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

## AOS_006 — the S(k) figure measures the aperture, not the tiling

**who:** A &nbsp;·&nbsp; **status:** SUPPORTED, STRENGTHENED

The report reads Ammann-Beenker as showing "sharp Bragg peaks." The
shipped `S(k)` map shows one bright spot at the origin — the
forward-scattering peak every finite point set has — on a linear color
scale that flattens everything else to black.

**Revised.** An earlier version of this entry conceded that the radial
profile's oscillations out to |k| ≈ 20 were real structure and that AB
was "not an uncorrelated set." That concession was wrong. The diffuse
floor is 2.08 for AB against 0.96 for the cascade; `S(k) → 1` is the
correct asymptote for an uncorrelated set, so the cascade is right, but a
quasiperiodic tiling has a **pure point** spectrum whose between-peak
floor sits *below* 1, not twice above it. The ordering is backwards.

`aperture_alias_demo.py` confirms it on probes with known spectra: a
Fibonacci chain returns floor 0.09 against a Poisson 0.99. The
oscillations are aperture ringing; "68 peaks" are fringe maxima; the 2.08
floor is residual ringing. Nothing in SIM-A is a property of the tiling.

**Falsifier:** push the SIM-B periodic lattice through the SIM-A `S(k)`
code. If it returns a resolved reciprocal-lattice spectrum rather than
only `k = 0`, the aliasing account fails and the report's reading stands.
Alternatively, show that the "diffuse floor" panel reports a plain mean
rather than a top-excluded floor — the demo notes the Fibonacci mean is
2.45, which would make 2.08 reachable for a genuine quasicrystal.

**Evidence:** `figures/sim_a_structure_factor.png`;
`aperture_alias_demo.py`; `samples/aperture_alias_demo.sample.txt`.

---

## AOS_007 — the α exponent is the window envelope, not structural scaling

**who:** A &nbsp;·&nbsp; **status:** UPGRADED from UNVERIFIED to SUPPORTED

`α_AB = −1.529` vs `α_C = −0.069` is measured on a radial profile whose
dynamic range is dominated by `S(0) ≈ 11,500`. This was previously logged
as `UNVERIFIED` — a gap, not a defect — because the fit range could not be
read off the figure.

`AOS_006` closes it from the other side. If the AB oscillations are
aperture fringes rather than structure, then their decay rate is the decay
of the window envelope, and α_AB describes the sample window. The cascade's
α ≈ 0 remains correct and unaffected: a flat `S(k) → 1` is what an
uncorrelated point set gives.

**Falsifier:** the same lattice control as `AOS_006`. A resolved spectrum
there would restore α_AB as a structural measurement.

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

---

## AOS_009 — the "15× baseline" uses the smallest pairwise gap as the noise floor

**who:** A &nbsp;·&nbsp; **status:** SUPPORTED

The report justifies its separation as "~15× larger than the AB–Poisson
finite-size baseline (0.021)". That baseline is the **smallest** of the
three pairwise gaps inside the space-filling cluster:

```
AB–Poisson        0.022     <- chosen as the noise floor
Poisson–Lattice   0.053
AB–Lattice        0.075
cluster spread    0.075
```

Three sets whose true dimension is 2 disagree by 0.075. That spread is
the error bar, not the closest pair within it. The honest ratio is
`0.334 / 0.075 ≈ 4.5×`, not 15.9×.

**Still decisive, still separated — not 15×.** This refines `AOS_003`
and `AOS_004` rather than replacing them, and the two routes converge:
the empirical cluster spread of 0.075 is close to the 0.082 residual
that `finite_n_control.py` reaches from the opposite direction, by
subtracting a measured worst-case artifact budget from the reported gap.
An effective error bar near 0.08 makes the separation about 4×.

A second reading of the same figures supports it. Taking the local-slope
plateaus directly rather than either windowed fit gives AB ≈ 1.93,
cascade ≈ 1.60, Poisson ≈ 1.97, lattice ≈ 2.00, line 1.00. Two fit rules
on identical data move AB by 0.120 and the lattice by 0.095 — again the
same order as the cluster spread, and again far above 0.021.

**Falsifier:** show that AB–Poisson is the correct reference pair
because Poisson is the matched control for AB specifically, and that the
lattice belongs to a different comparison class. That argument can be
made; the report does not make it, and it would still need the
matched-N rerun in `AOS_003`.

**Evidence:** `SIM_STACK_REPORT.txt` Key Distance section;
`figures/sim_b_boxcount_local.png` and `figures/sim_b_boxcount.png` for
the two fit rules; `../reasoning-gate/SIM_STACK_BACKTRACE.md` SIM-B
section, where this was first identified.

---

## AOS_010 — no cascade number in this stack supports a statement about tungsten

**who:** A &nbsp;·&nbsp; **status:** SUPPORTED

The cascade set is a synthetic branching walk. Every cascade quantity in
the drop — `D_f = 1.555`, `E_split/E₀ = 0.0015`, the branching threshold
— is a property of that generator's parameters (`E_split`, `E_min`,
branch rule), not of any physical material. The report does not flag it,
and places cascade numbers at the same epistemic level as facts about
aperiodic order.

This is `AOS_004` sharpened: the comparison behind "structurally
distinct classes of aperiodic order" runs between a physical property of
the Ammann-Beenker tiling and a parameter of a piece of code.
`../reasoning-gate/replay_sim_stack.py` tags `Df_cascade` as `generator`
for exactly this reason.

**Falsifier:** derive any cascade parameter from a measured material
property rather than choosing it, or show the branching rule is
constrained by physics the report states. Either would promote the
cascade numbers a layer.
