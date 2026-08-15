# aperiodic-order-sim-stack

A results drop plus an audit of it.

The drop asks one question: **do quasiperiodic tilings and branching
cascades share a geometry, or do they only share the property of not
being periodic?** Three simulations were run against it — fractal
dimension (SIM-B), structure factor (SIM-A), band-edge splitting under
a disorder sweep (SIM-C) — and `SIM_STACK_REPORT.txt` concludes that all
three converge: the two classes are structurally distinct.

The report's own figures do not support that reading as stated. The
drop shipped **two independent dimension estimators**. They disagree on
the *sign* of the headline result. Only one of them appears in the
report.

## What landed

| File | What it is |
| --- | --- |
| [`SIM_STACK_REPORT.txt`](SIM_STACK_REPORT.txt) | The drop's master report, **verbatim as delivered**. Not edited. |
| [`figures/`](figures/) | The eight shipped PNGs, plus [`figures/README.md`](figures/README.md) mapping each panel to the claim it bears on. |
| [`finite_n_control.py`](finite_n_control.py) | The estimator control the drop did not run. Stdlib only. |
| [`samples/finite_n_control.sample.txt`](samples/finite_n_control.sample.txt) | Pinned output of that control. |
| [`CLAIM_TABLE.md`](CLAIM_TABLE.md) | Six claims with the measurement that would refute each. |

No generator code was shipped — only results. The Ammann-Beenker tiling,
the branching cascade, and the three controls cannot be regenerated from
what arrived. That bounds everything below: the audit reads figures and
reruns controls on synthetic probes, and cannot rerun the sims
themselves.

## Finding 1 — two estimators, opposite conclusions, one reported

`SIM_STACK_REPORT.txt` presents SIM-B under a single heading,
"Box-Counting Dimension Results," and calls it decisive. But
`figures/sim_b_sandbox.png` and `figures/sim_b_sandbox_local.png` show a
**sandbox** (mass-radius, `M(r) ~ r^D`) estimator was also run on the
same five point sets. Its numbers appear nowhere in the report.

Across the four estimator variants the drop actually shipped:

| Estimator variant | AB | Cascade | Poisson | Line | **AB − Cascade** | Line error |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| box-count, plateau fit *(the reported one)* | 1.889 | 1.555 | 1.911 | 1.000 | **+0.334** | +0.000 |
| box-count, global fit | 1.769 | 1.529 | 1.852 | 0.979 | **+0.240** | −0.021 |
| sandbox, global fit | 1.961 | 2.208 | 1.972 | 1.913 | **−0.247** | +0.913 |
| sandbox, plateau fit | 1.946 | 1.969 | 1.930 | 1.844 | **−0.023** | +0.844 |

The quantity the verdict rests on changes sign depending on which
shipped estimator you read. By box counting the Cascade sits far below
Ammann-Beenker. By the sandbox method it sits at or slightly *above* it,
and the separation collapses to 0.023 — indistinguishable from the
report's own 0.021 finite-size baseline. The report's sentence
"The quasiperiodic and cascade dimensions do NOT coincide" is true of one
estimator and false of the other.

**There is a good reason to prefer box counting here, and the report does
not give it.** Look at the Line column. The Line is a 1D control with an
exactly known dimension of 1.000. Box counting recovers it to three
decimals. The sandbox estimator returns **1.913** — off by 0.913, larger
than the entire effect under study. An estimator that reports a straight
line as very nearly space-filling is not measuring dimension, and its
Cascade number should be discarded.

So the box-counting result survives and the sandbox result fails on its
own control. That is the right outcome. But it was reached here by
checking the control, not by the report, which resolved the disagreement
by omission — it does not mention that a second estimator was run, that
it disagreed, or that it failed the Line check. A reader of
`SIM_STACK_REPORT.txt` alone cannot know any of this. The controls in the
report are described as validating the method ("Controls Validate
Method: Line hits 1.000 exactly"); that line is true of the estimator
that was published and false of the one that was not.

The cause of the sandbox failure is not recoverable from the figures
alone, since the generator was not shipped. It is a real bug worth
finding: `figures/sim_b_sandbox_local.png` shows the Line's local slope
oscillating around 1.8–2.0 across the entire radius range, so it is
wrong everywhere, not just in a bad fit window.

## Finding 2 — the decisive gap is ~75% within the artifact budget

`finite_n_control.py` addresses the second problem visible in
`figures/sim_b_point_sets.png`: the panel titles report ~12,000 points
for Ammann-Beenker, Poisson, Lattice and Line, and **1,024** for the
Cascade. The report's finite-size baseline (0.021, AB vs Poisson) is
measured between two 12,000-point sets. The decisive difference (0.334,
AB vs Cascade) is measured across a 12× sample-size drop. The baseline
does not cover the comparison it is used to license.

That matters because box counting saturates at the point count.
`figures/sim_b_boxcount.png` shows it plainly — the Cascade curve flattens
at `log N = 3.0` (= 1024), every other curve flattens at `log N = 4.08`
(= 12,000). The sparse set has a materially shorter scaling window.

The control runs the same estimator over three probes whose true
dimension is known and **does not depend on N**, at both sample sizes.
Any movement is pure artifact:

```
Poisson  (true 2.0000)   12,000 → 1.936    1,024 → 1.799    shift +0.137
Line     (true 1.0000)   12,000 → 0.951    1,024 → 0.901    shift +0.050
Cantor   (true 1.2619)   12,000 → 1.304    1,024 → 1.326    shift −0.021
```

A second confound turned up while building it. The same 12,000-point
Cantor dust, same estimator, changing only the box ladder's ratio:

```
base 2 (incommensurate with the set's 1/3 scaling)   D_f = 1.304   error +0.042
base 3 (commensurate)                                D_f = 1.189   error −0.073
                                                     ladder shift = 0.115
```

Worst-case sample-size shift (0.137) plus ladder shift (0.115) gives an
artifact budget of **0.252 against a reported separation of 0.334** —
about 75% of it.

Read that as an **upper** bound on artifact, not an expected error: it
adds the worst observed shift from each source, and the two need not
align in sign on any real point set. The residual 0.082 is correspondingly
a **lower** bound on structure — and it is still four times the report's
0.021 baseline.

**So SIM-B's direction survives and its magnitude does not.** The Cascade
does read lower than Ammann-Beenker, and not only because it is sparser.
But 0.334 is quoted to a precision the method does not support, and
"decisive" is doing more work than it has earned. Two cheap runs would
settle it: Ammann-Beenker subsampled to 1,024 points, and a Poisson
control also at 1,024 inside the Cascade's own bounding box. Neither
was run.

## Finding 3 — SIM-C's null result is counted as positive evidence

The SIM-C section states its own outcome plainly: *"No direct
correspondence between the knee location and the cascade branching
threshold. The band-edge splitting grows gradually with disorder and does
not show a sharp threshold."* That is a null result. The method looked
for a threshold and did not find one.

The OVERALL CONCLUSION then lists SIM-C as one of three converging
lines of evidence: *"SIM-C (band-edge splitting): Different threshold
behavior → different response to symmetry breaking."* Absence of a
detected feature has become evidence of a difference. It cannot be,
absent a positive control showing this method detects a threshold when
one is present. No such control was run. This is the failure
[`null-harness/`](../null-harness/) exists to catch, one folder over — a
gate that never fires is not evidence, it is an untested gate.

The knee itself is weak. In `figures/sim_c_threshold_sweep.png` the
curvature curve has comparable peaks at f ≈ 0.45, 0.55, 0.65, 0.70, 0.80
and 0.90; f = 0.65 wins by a margin no larger than the scatter between
its neighbours. It also lands on a **local minimum** of the splitting
curve it is supposed to be finding the knee of, and the shaded ±1σ band
spans most of the rise. The reported ratio of 54.1 is built on that
location.

## Finding 4 — SIM-A's k-space figures do not show what the text claims

The report reads SIM-A as *"AB shows sharp Bragg peaks (quasi-crystalline
order) with strong diffuse background."* The shipped
`figures/sim_a_structure_factor.png` shows the Ammann-Beenker `S(k)` map
as a single bright spot at the origin on an otherwise black field. The
eight-fold Bragg star that is the actual signature of an Ammann-Beenker
tiling is not visible in it.

What is at the origin is the forward-scattering peak at `k → 0`, which
every finite point set has and which carries no information about
quasiperiodic order. It reaches `S(0) ≈ 11,500` against a diffuse floor
of 2.08, so on the linear color scale used it flattens everything else to
black. The quoted "peak/floor ratio = 5537" is essentially `S(0)/floor`.

Part of the SIM-A reading does hold. The radial profile (top-right panel,
log scale) shows real oscillatory structure in the AB curve out to
|k| ≈ 20 while the Cascade is flat at ≈ 1. Flat-at-1 is the signature of
an uncorrelated point set, and AB clearly is not that. **AB has more
k-space structure than the Cascade — that much the figure supports.**

What the figure does not support is the specific reading. The tail
exponent difference (α_AB = −1.529 vs α_C = −0.069) is measured on a
profile whose dynamic range is dominated by the forward peak, so it is at
least partly a measurement of `S(0)` falloff rather than of structural
scaling. Re-plotting on a log color scale with `k = 0` excluded would
settle in one pass whether the eight-fold peaks are there. It is the
single cheapest outstanding check in the drop.

## What the drop actually establishes

Restating the conclusion at the strength the evidence carries:

- **Supported.** Ammann-Beenker and the Cascade have different k-space
  character: one has oscillatory structure out to |k| ≈ 20, the other is
  flat at the uncorrelated floor.
- **Supported in direction, not magnitude.** The Cascade's box-counting
  dimension is lower than Ammann-Beenker's. The margin is not 0.334 ±
  nothing; ~75% of it sits inside a measurable artifact budget.
- **Not established.** That the two "do not share a common fractal
  geometry" as a settled result. The drop's own second estimator says
  they coincide, and although that estimator fails its Line control and
  should be discarded, the report neither performs nor reports that
  reasoning.
- **Not established.** Anything from SIM-C. Its stated finding is a null,
  and it is entered into the conclusion as a positive.
- **Not established.** That AB shows sharp Bragg peaks, on this figure.

The drop's headline direction is probably right. The evidence shipped for
it is weaker than the report says, and the strongest argument against it
was shipped in the same zip without being mentioned.

## Running the control

```bash
python3 finite_n_control.py
```

Standard library only, deterministic under a fixed seed, under a second
to run. Output is pinned at
[`samples/finite_n_control.sample.txt`](samples/finite_n_control.sample.txt).

## Where this sits in the repo

- [`null-harness/`](../null-harness/) — the direct sibling. Same
  invariant: a gate that never fires has not been shown to work.
  SIM-C's missing positive control is exactly its `CONSTANT_SILENT`
  case.
- [`model-ecology/`](../model-ecology/) — `confound_sweep.py` separates
  apparatus floor from window from real structure, and finds the window
  to be the largest and most invisible confound. Findings 1 and 2 here
  are that result again on a different substrate: fit window and box
  ladder each move the answer by more than the effect.
- [`divergence-playground/`](../divergence-playground/) — this drop is a
  natural fork point. Two estimators on identical data returning opposite
  signs is the `agree_by_accident` cell inverted, and would make a good
  `Reading` spread.
- [`instrument-epistemology/`](../instrument-epistemology/) — the
  estimator is the instrument here. The sandbox method's Line failure is
  a blindness map entry, not a rounding error.

## Provenance and license

Delivered 2026-08-15 as `sim_stack_results.zip` — one report and eight
PNGs, no source. `SIM_STACK_REPORT.txt` and every figure are checked in
exactly as received; all audit content is confined to this README,
`CLAIM_TABLE.md`, `figures/README.md`, and `finite_n_control.py`. The
drop's numbers have not been edited to agree with the audit, and the
audit's numbers were not tuned to disagree with the drop.

CC0, matching the repository default.
