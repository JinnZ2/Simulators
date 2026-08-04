# FINDINGS

Author audit of the `energy/` drop. Six findings, four survivals.
The report's headline claims are on trial here, not the sweep data
or the qualitative Instrument A vs B contrast.

> **Read [`PROVENANCE.md`](PROVENANCE.md) alongside this file.** It
> is the author's own decision ledger (12 DPs, 8 falsification
> entries, 7 open branches, 5 anchor tests) and it independently
> reproduces several findings below:
>
> - **F-2 in PROVENANCE = F3 here:** constant-β corridor CMB-vetoed
>   at 283σ; β₁=0.4 champion killed with σ8≈3.2 gate units
>   (matches the R-D lens prediction `growth_ratio = 3.249`, see
>   [`exploration_layers/reaction_diffusion_lens.py`](exploration_layers/reaction_diffusion_lens.py)).
> - **F-5 in PROVENANCE = R-D lens prediction:** late-triggered
>   β(a) = β₀·aⁿ "dodges θ* but buys nothing" — the coupling's
>   usefulness IS its early action. Consistent with the finding
>   that the mechanism is autocatalytic accumulation over the
>   matter era, not the late-time value.
> - **DP-4 = F5 here:** "A disclosed systematic is a measurement;
>   a calibrated-away systematic is a story." The author holds a
>   known 2.3σ θ* offset in every CMB verdict rather than
>   recalibrating it away.
> - **DP-11 late-time kink = "still alive" branch:** the phenomeno-
>   logical w_DE kink at a_t=0.92–0.95 passes all four gates;
>   [`app/needle_lab.html`](app/needle_lab.html) is the
>   instrument-design surface for measuring it.
>
> Where PROVENANCE and this file diverge in language they converge
> in verdict. Read them together.

---

## F1 — the "14 orders of magnitude" is not a measurement

Fisher eigenvalue `1.6e-14` is not a measurement.

- 3 params (`λ, β, α`) → 2 observables (`w₀, wₐ`).
- Rank deficiency is **structural**: true eigenvalue = 0.
- float64 noise floor ≈ `247.7 × 2.2e-16 ≈ 5e-14`.
- `1.6e-14` sits below it. "14 orders" is unquantifiable.

**Fix.** Report null-space dimension, not a ratio. Instrument B's
`2.09` is the only real number here.

---

## F2 — the generative module recovering CPL is guaranteed, not found

If `z/(1+z)` is in the numpy basis library AND residuals were taken
against a `w₀–wₐ`-projected instrument, the projection basis IS the
regression basis.

**Fix.** Rerun with `z/(1+z)` REMOVED from the library. If it
reconstructs the form from other primitives, claim stands.
Otherwise it's an echo.

### Test result (see `samples/f2_echo_test.sample.txt`)

The target inside `payload_bridge.main()` is constructed as
`w_desi = w0 + wa * (1 - 1/(1+z)) = w0 + wa * z/(1+z)` — CPL by
definition. The basis library ships `z/(1+z)` twice: once as
`"z*inv(1+z)"`, once labeled `"(1-a) [CPL-like]"`.

| basis                             | proposed missing term                          | std reduction |
|-----------------------------------|------------------------------------------------|---------------|
| **original** (z/(1+z) present)    | `-0.353·z·inv(1+z) − 0.043·exp(−2z)`           | **94.7%**     |
| **excised** (z/(1+z) removed)     | `-0.214·log(1+z) − 0.060·exp(−z)`              | 76.6%         |

Removing the primitive changes both the functional form (log(1+z)
diverges where z/(1+z) saturates — different asymptote at high z)
and the fit quality. Multiple survivors correlate `|>0.99|` with the
residual on this z-range (inv +0.996, exp −0.994, log −0.994,
even plain z at −0.96), so the greedy pick is not stable under basis
substitution.

**F2 CONFIRMED.** The "first term IS the CPL wₐ form" phrasing
described the regressor's basis, not the physics. The generative
module returned its own seed.

---

## F3 — fs8 ≈ 8× ΛCDM is not a tension, it's a blowup

- fs8 is constrained at the ~5–10% level.
- `G_eff = 1 + 2β²` cannot reach 8× growth at any β that survives
  CMB/BBN early-coupling bounds.
- Check integrator stability before calling it physics.
- **Suspect:** runaway in `β(z) = β₀ + β₁·z/(1+z)` at high z, where
  `z/(1+z) → 1` and the coupling never turns off.

### Lens: reaction-diffusion (see [`exploration_layers/reaction_diffusion_lens.py`](exploration_layers/reaction_diffusion_lens.py))

The growth equation is a reaction with rate
`R(N) = 1.5·Ω_m·(1 + 2β²)` and damping `F(N) = 2 − q`. Reading β(z)
as an autocatalytic term that never removes itself gives the total
growth ratio to ΛCDM at fixed background:

| β₀, β₁      | growth_ratio | β(today) contribution |
|-------------|-------------:|-----------------------|
| (0, 0)      | 1.000        | 0 (baseline)          |
| (0, 0.20)   | 1.356        | 0                     |
| (0, 0.40)   | **3.249**    | 0                     |
| (0, 0.60)   | 12.455       | 0                     |

**F3 refined, not overturned.** The 8× is **not** integrator
instability — it is the mechanism the parameterization prescribes.
`β(today) ≈ 0` so `p(N=0)` matches ΛCDM, but the growth compounded
over the matter era where β(z) saturated near `β₀ + β₁`. The
R-D name for the mechanism: autocatalytic reaction whose catalyst
is never removed. Any physical β(z) must decay at high z;
`β₀ + β₁·z/(1+z)` cannot. Iteration-6's "champion" is genuinely
killed by the growth channel — the loop stayed open for the right
reason.

---

## F4 — SIMPLE_POLE at α ≈ −1/λ² is epoch-dependent

- Wall is `1 + α·φ̂² = 0` → `φ̂² = -1/α`.
- `α = -1/λ²` only holds where `φ̂ ≈ λ` (exponential attractor).
- `φ̂` evolves → the wall **moves**.
- Classifier fixed a moving boundary to a static α.
- Score `0.9999` from 27 cells is over-reported precision.

### Lens: RG flow (see [`exploration_layers/rg_flow_lens.py`](exploration_layers/rg_flow_lens.py))

Fixed points of the (x, y) autonomous subsystem at (λ=1.10, β=0):

| x     | y     | Ω_φ   | w_φ    | class    | eigenvalues        |
|-------|-------|-------|--------|----------|---------------------|
| 0.000 | 0.000 | 0.000 |  0.000 | SADDLE   | ±1.50               |
| 1.000 | 0.000 | 1.000 | +1.000 | REPELLER | +1.65, +3.00        |
| 0.449 | 0.893 | 1.000 | −0.597 | ATTRACTOR| −1.79, −2.40        |

At the field-dominated attractor, `x* = 0.449 ≠ 0`, so
`φ̂(N) = φ̂_i + √6·x*·(N − N_i)` grows linearly along the flow. The
apparent wall `α_wall(N) = −1/φ̂(N)²` then moves:

| N     | φ̂       | α_wall     |
|-------|---------|------------|
| −6.00 | 0.0010  | −1 × 10⁶   |
| −3.00 | 0.0030  | −1.1 × 10⁵ |
| −1.50 | 0.1372  | −53.14     |
|  0.00 | 1.2347  | −0.656     |

**F4 CONFIRMED.** `α_wall` spans **1.5 × 10⁶** across the matter
era. The report's static value `α = −1/λ² = −0.826` is crossed at
exactly **one epoch** (N ≈ −0.10, φ̂ ≈ 1.14). Fixing this snapshot
as if it were a coupling constant is the F4 error: the wall is a
trajectory, not a coupling.

---

## F5 — undefined / unreproducible thresholds

- `S_min = 0.05` — threshold on WHAT normalization?
- phantom_layer χ² — against WHICH dataset + covariance?

Neither is in the README. Both gate the verdicts.

---

## F6 — license collision

- `modules/` = MIT (per-file headers).
- Repository root LICENSE = CC0.

A CC0 repo carrying MIT per-file headers is not CC0. The `energy/`
folder README notes the split in its Provenance section, but this
mixed-license state is a real ambiguity that should be resolved
upstream (module authors either waive to CC0 or the repo declares a
per-folder license map).

---

## §8 — "N ≈ 4 distinguishable cosmologies" is a transition reading

Not in the original F1-F6 list, but the percolation lens
([`exploration_layers/percolation_lens.py`](exploration_layers/percolation_lens.py))
raises this as a companion finding on the report's §8. Building a
graph on the 48 manifold nodes with edges at observable-space
distance ≤ θ (using `σ_w0=0.04, σ_wa=0.16, σ_fs8=0.02`):

| θ (σ) | n_components | giant_fraction |
|------:|-------------:|---------------:|
|  0.50 |           24 |          0.333 |
|  0.70 |           10 |          0.479 |
|  1.00 |            2 |          0.667 |
|  1.50 |            1 |          1.000 |

The report picked θ = 1σ. The percolation transition
(`giant_fraction` crossing 0.5) sits between θ = 0.7 and θ = 1.0 —
the report threshold is **on the transition**, not on a plateau.
This means the "N ≈ 4" count is not a robust readout of the geometry;
it is a transition-region readout that will jump under modest
covariance rescaling. The geometry is stable, the number attached
to it is not.

## What survives

- ✓ **Instrument A/B contrast** — the qualitative result (projection
  blind, tomography not) is sound and does not depend on the bogus
  "14 orders" number. F1 refines the framing without killing it.
- ✓ **Shooting to Ω_φ,0 = 0.685** — standard, fine.
- ✓ **Sweep CSVs are data.** They stand independent of the
  interpretation layer built on them.
- ✓ **"Loop stays open by design"** — correct posture, wrongly
  applied to a candidate that F3 says was never alive.

---

## Cheapest next moves, in order

1. **F2 — done.** See table above and the sample. The claim of a
   CPL-shaped discovery collapses.
2. **F3 — done, sharpened.** See the R-D lens above and the sample.
   The 8× is real physics of a pathological parameterization, not
   an integrator bug. The finding stands and now has a mechanism.
3. **F4 — done, confirmed.** See the RG lens above and the sample.
   The α-wall spans 6 orders of magnitude across the flow; the
   report's static classification captured one snapshot of a moving
   boundary.
4. **§8 — done, weakened.** See the percolation lens above. The
   "N ≈ 4" count sits on the percolation transition; the geometry
   is stable but the count attached to it is not.
5. **F1** — swap "14 orders lifted" for "the projection is exactly
   rank-deficient by construction (3 params → 2 observables); the
   rank-3 tomographic instrument is well-posed at `S_min = 2.09`."
6. **F5** — inline the `S_min` normalization convention and the
   DESI-mock covariance used for the χ² surface in the README or
   in `modules/README.md`.
7. **F6** — decide license posture; either request CC0 waiver from
   the module authors or add an explicit `LICENSE.MIT` inside
   `modules/` and note the repo carries a mixed license.

## Exploration-layer pattern

The above lenses live in
[`exploration_layers/`](exploration_layers/README.md) and follow a
simple rule: **when a wall is named, look for the same wall in
another field's language and land a reading in that language.**
Three families landed here (reaction-diffusion, percolation, RG
flow); nothing stops more from arriving. The lens returns numbers
and shape, not a verdict — it can strengthen a finding (F3 kept its
teeth), confirm it (F4 got a quantitative number for the wall's
motion), or weaken it (percolation reframed §8's count). What
matters is that the reading exists in language the original framing
could not have produced.
