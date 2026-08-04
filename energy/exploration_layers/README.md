# exploration_layers

**When you hit a wall, put more than one physics against it.**

Each finding in [`../FINDINGS.md`](../FINDINGS.md) is a wall. A wall
named in one field's language usually has a name in another field's
language too, and the second reading often catches what the first
missed — different math, different failure modes surfaced, same shape.

Three lenses landed here, each attached to a specific finding. Each
returns **numbers and shape**, not a verdict (same posture as
`../../rigidification-sensor/harm.py`).

> **Convergent discovery.** The author's v2 drop shipped their own
> three-lens scan as [`../modules/theory_space_lenses.py`](../modules/theory_space_lenses.py)
> — same R-D / percolation / Fisher-curvature triad, developed
> independently on their side. The two implementations reached the
> β₁ ≈ 0.2–0.3 pathology from different directions:
>
> - `theory_space_lenses.py.survival_report()` — "UNIVERSAL
>   PATHOLOGY: growth kink, graph fragmentation peak (8.75σ), and
>   Fisher rank collapse all at β₁≈0.2–0.3."
> - `reaction_diffusion_lens.py` — `growth_ratio = 3.249` at β₁=0.4,
>   compounding to 12.5 at β₁=0.6.
>
> Both name the same wall; the modules stand as sibling readings.

## Landed

| lens                          | wall                              | reading                                                                                        |
|-------------------------------|-----------------------------------|------------------------------------------------------------------------------------------------|
| `reaction_diffusion_lens.py`  | F3 — running-coupling "blowup"    | growing-mode exponent `p(N)` and Damköhler analog `Da(N)` along the trajectory; total growth ratio to ΛCDM |
| `percolation_lens.py`         | §8 — "N ≈ 4 distinguishable"      | giant-component fraction vs threshold θ on the observable-space graph                          |
| `rg_flow_lens.py`             | F4 — moving `α = −1/φ̂²` boundary | fixed points of the (x, y) autonomous system, classification, and `α_wall(N)` along the flow  |

## What each lens said

### F3 (R-D lens): the growth channel is autocatalytic, not buggy

The growth equation for δ_m in e-folds is a reaction with rate
`R(N) = 1.5·Ω_m(N)·(1 + 2β(N)²)` and damping `F(N) = 2 − q(N)`.
Reading `β(z) = β₀ + β₁·z/(1+z)` — the coupling that never turns off:

```
label                       growth_ratio    p(N=0)   p_lcdm(N=0)    Da_max
LCDM control      (0,0)            1.000     0.175         0.175     0.665
F3 iteration-6    (0,0.20)         1.356     0.175         0.175     0.714
F3 iteration-6    (0,0.40)         3.249     0.175         0.175     0.868
large runaway     (0,0.60)        12.455     0.175         0.175     1.126
```

The 8× fs8 anomaly is **not integrator instability** — it's the
mechanism the parameterization prescribes. `β` today is ≈ 0
(`p(N=0)` unchanged from ΛCDM), but the growth compounded over the
14 e-folds of matter era where β(z) saturated near `β₀ + β₁`. The
R-D framing gives the name: an autocatalytic reaction whose catalyst
is never removed. Any physical coupling parameterization must decay
at high z; `β₀ + β₁·z/(1+z)` cannot.

**F3 refined:** the "8×" is a real prediction of a pathological
parameterization, not a bug. Iteration-6's "champion" is genuinely
killed by the growth channel — the loop stayed open for the right
reason.

### Packing (percolation lens): θ=1σ sits on the transition

Building a graph on the 48 manifold-graph nodes where nodes within
observable-space distance θ (using `σ_w0=0.04, σ_wa=0.16, σ_fs8=0.02`)
are connected:

```
  theta   n_comp   giant_frac   mean_size
   0.50       24        0.333        2.00
   0.70       10        0.479        4.80    <- report threshold neighborhood
   1.00        2        0.667       24.00
   1.50        1        1.000       48.00
```

The percolation transition (giant fraction crossing 0.5) sits between
θ=0.7 and θ=1.0 — **exactly where the report picked its threshold.**
This means the "N ≈ 4 distinguishable cosmologies" count is not a
plateau reading; it is a transition reading. A modest covariance
rescaling would jump the count sharply. The geometry is stable; the
number attached to it is not.

### F4 (RG lens): the wall spans 6 orders of magnitude along the flow

Fixed points of the (x, y) subsystem at λ=1.10, β=0:

```
        x        y    Om_phi    w_phi        class    eigenvalues
    0.000    0.000     0.000    0.000       SADDLE   ±1.50
    1.000    0.000     1.000    1.000     REPELLER   +1.65, +3.00
    0.449    0.893     1.000   -0.597    ATTRACTOR   -1.79, -2.40   <- field-dominated
```

At the attractor, x* = 0.449 is nonzero — so `φ̂(N)` grows linearly at
slope √6·x* ≈ 1.1 per e-fold. The apparent wall
`α_wall(N) = −1/φ̂(N)²` moves with it:

```
      N   phi_hat   alpha_wall
  -6.00    0.0010      −1e+06
  -3.00    0.0030    −1.13e+05
  -1.50    0.1372      −53.14
   0.00    1.2347       −0.656
```

`α_wall` spans **1.5 × 10⁶** across the matter era. The report's
static value `α = −1/λ² = −0.826` is crossed at exactly **one epoch**
(N ≈ −0.10). Fixing this snapshot as if it were a coupling constant
is the F4 error: the wall is a trajectory, not a coupling.

**F4 confirmed** with a sharp number: the singularity classifier's
`SIMPLE_POLE at α ≈ −0.826` corresponds to `φ̂ ≈ 1.14` at one
particular e-fold. Everywhere else, the wall is elsewhere.

## The pattern

For any new wall the repo hits, the same three-move template:

1. Name the wall (F#) and its native framing.
2. Point at families whose math might transfer — pattern recognition
   across fields, not commitment to a formalism.
3. Land one lens per family that returns numbers and shape (no
   verdict). Attach it to the finding.

The lenses are *readings*, not proofs. They can strengthen a finding
(F3, F4 above), weaken it (percolation weakened §8's "N=4" from a
result to a transition-region readout), or leave it neutral. What
matters is that the reading exists in language the original framing
would not have produced.

## Sample outputs

- [`samples/reaction_diffusion_lens.sample.txt`](samples/reaction_diffusion_lens.sample.txt)
- [`samples/percolation_lens.sample.txt`](samples/percolation_lens.sample.txt)
- [`samples/rg_flow_lens.sample.txt`](samples/rg_flow_lens.sample.txt)

## Dependencies

`numpy` + `scipy` (same as `../modules/`). `percolation_lens.py` is
pure stdlib (union-find + JSON).
