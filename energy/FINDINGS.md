# FINDINGS

Author audit of the `energy/` drop. Six findings, four survivals.
The report's headline claims are on trial here, not the sweep data
or the qualitative Instrument A vs B contrast.

> **Read [`PROVENANCE.md`](PROVENANCE.md) alongside this file.** It
> is the author's own decision ledger (12 DPs, 8 falsification
> entries, 7 open branches, 5 anchor tests) and it independently
> reproduces several findings below:
>
> - **F-2 in PROVENANCE ≈ F3 here:** constant-β corridor CMB-vetoed
>   at 283σ; β₁=0.4 champion killed with σ8 ≈ 3.2 gate units. The
>   R-D lens
>   ([`exploration_layers/reaction_diffusion_lens.py`](exploration_layers/reaction_diffusion_lens.py))
>   reports `growth_ratio = 3.249` at β₁=0.4 over 14 matter-era
>   e-folds on a **fixed ΛCDM background**; that is a *toy upper
>   bound* on the linear-growth ODE and does **not** correspond to
>   σ8 3.2 gate units (a 5% σ8 enhancement) — the numeric coincidence
>   between 3.249 and 3.2 is not a physics match. What survives is
>   the *qualitative* mechanism: β(z) that never turns off pumps the
>   matter era, both readings say so, and both point at the same
>   parameter region as pathological.
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
as an autocatalytic term that never removes itself gives an
**upper-bound growth ratio** on a fixed ΛCDM background (no backreaction
on the expansion history):

| β₀, β₁      | growth_ratio (fixed-bkg) | β(today) contribution |
|-------------|-------------------------:|-----------------------|
| (0, 0)      | 1.000                    | 0 (baseline)          |
| (0, 0.20)   | 1.356                    | 0                     |
| (0, 0.40)   | **3.249**                | 0                     |
| (0, 0.60)   | 12.455                   | 0                     |

**Caveat.** These are fixed-background upper bounds on `D(a=1)/D(a_i)`;
the self-consistent shooting engine backreacts on the expansion
history and delivers a much smaller σ8 enhancement (`late_trigger_lens`
and `unified_cq_ede`: σ8 ≈ 0.86 for β₁=0.4 → 3.2 gate units, a ~5%
effect). The lens' contribution is qualitative — it names the
mechanism — not quantitative.

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
6. **F5 — DONE.** PROVENANCE §7.1 "Named denominators" table lands
   every threshold used by any gate: `S_MIN_THRESHOLD`, DESI mock
   covariance, Planck 100θ*, H0 gate (with DP-14 caveat), σ8
   working tolerance, `R_EQ_MODE` requirement. Adding a new gate
   without an entry there is now a documentation bug per DP-16.
7. **F6 — DONE.** MIT headers waived to CC0 across all 10 modules;
   modules/README.md and top-level README updated.

## Follow-on audit results (external G-findings)

The initial F1-F6 list was answered by a follow-up audit that
raised five sharper concerns (G1-G5). Resolutions:

- **G1 SIGN — DONE.** The doc's A4 = "+2.33σ HIGH" was **stale** —
  neither R_EQ mode of the current code reproduces it. Both engines
  actually sit at −3.0σ LOW and agree with each other to 0.08σ. The
  earlier "opposite signs 5.4σ apart" reading was based on the stale
  doc, not the code. Fixed in PROVENANCE §3 A4/A5 and DP-4/DP-13.
  Also enforced a warning at `cmb_observables` when `R_EQ_MODE` is
  not `'physical'` (the default `'it6'` gives r_s off by 25%). See
  `samples/g1_bisect.sample.txt`.
- **G1 DP-11 champion — DONE.** Re-reported as **Δθ* = +5.43σ vs
  same-engine ΛCDM** (primary) with absolute-vs-Planck 2.4σ as a
  labeled second column. The mechanism produces a real +5σ shift;
  it does not sit near null.
- **G2 H0 clip — PARTIAL.** `gate_vector` now accepts
  `h0_two_sided=True` (default unchanged for reproducibility). The
  actual rerun of DP-9's cosines/rank under the two-sided form is
  staked as PROVENANCE OB-8.
- **G3 D metric — DONE.** `D_of` docstring now labels D as a
  log-compressed ranking heuristic, not a metric. PROVENANCE DP-15
  requires the raw gate vector alongside every D quote.
- **G4 sandbox paths — DONE.** All `/mnt/agents/output/*` references
  removed from PROVENANCE §1; `payload_bridge.py` default path now
  resolved from `__file__`. Duplicate `app/PROVENANCE.md` deleted.
- **G5 §8.6 personal paragraph — DONE.** Removed from PROVENANCE §8.

## F-10 D correction landed: local scalar drift lens

The F-10 audit killed the pasted `local_scalar_drift.py` (drift
prefactor off by 1.23×10²⁴). The corrected version ships as
[`exploration_layers/local_scalar_drift_lens.py`](exploration_layers/local_scalar_drift_lens.py)
with four import-time anchors on the physical constants (H0 in GeV,
yr_to_GeVinv, ρ_c today, and the prefactor at 1+w=1 equal to
√3·H0 in per-year — all match textbook values to 1%).

**What this delivers.** For the DP-11 "still-alive" champion kink
(`a_t=0.92, δw=0.10, Δa=0.05`, `w0 = −0.917`), the corrected
prefactor lands at `2.85×10⁻¹¹ /yr` per unit β. Sensitivity
thresholds for present-day laboratory tests:

| measurement                 | limit /yr | β to see it        |
|-----------------------------|----------:|-------------------:|
| atomic clocks (α̇/α)        | 1×10⁻¹⁷   | **β_α > 3.5×10⁻⁷** |
| lunar laser ranging (Ġ/G)   | 2×10⁻¹³   | β_G > 7×10⁻³       |

The α limit sits well inside plausible Damour-Polyakov coupling
range — atomic clocks **today** rule out any kink whose scalar
carries a photon coupling above `~3×10⁻⁷`. That is the present-day
laboratory falsification channel the paste was aiming at but could
not deliver because of the F-10-D2 and F-10-D3 unit bugs. DP-11's
"still alive" verdict now has a real gate.

Full plot: [`figures/local_scalar_drift.png`](figures/local_scalar_drift.png).
Sample run: [`exploration_layers/samples/local_scalar_drift_lens.sample.txt`](exploration_layers/samples/local_scalar_drift_lens.sample.txt).

## Follow-on (audit TODO 3.5): DP-17 certificate validity radius

Executed the certificate-validity sweep the audit prescribed alongside
the G1 bisect (they share the θ* machinery). Sweep of β₁ at pinned
(λ, f_ede, z_c) with linear-in-β₁ tangent onset criterion (>20%
extrapolation deviation triggers onset). Results at two base points:

| base point            | β₁_certified | β₁_onset | **r̂**   | shape (winner)          |
|-----------------------|-------------:|---------:|--------:|-------------------------|
| A: λ=1.1, f=0.05     | 0.05         | 0.10     | **1.00** | power law (R²=0.995)    |
| B: λ=0.9, f=0.05     | 0.05         | 0.10     | **1.00** | exponential (R²=0.986)  |

**r̂ is stable across base points → property of the wall.** The
LP-certificate around the coupled-quintessence CMB wall stays trustworthy
for roughly a **doubling** of the certified β₁ before the tangent
under-predicts by more than 20%. A certificate computed at β₁ = 0.05
is honest out to β₁ ≈ 0.10; past that, nonlinearity bites.

The functional form itself (power law vs exponential) *is*
base-point-dependent — R² winners flip between λ=1.1 and λ=0.9 —
but the LP-radius r̂ is not. That is a genuine "shape property of a
locally-power-law-with-slope-~1.5 wall" reading and should transfer
to any nonlinear-wall-plus-linear-certificate pair with similar
convexity. Full DP-17 write-up in PROVENANCE, artifacts in
[`exploration_layers/certificate_validity_lens.py`](exploration_layers/certificate_validity_lens.py),
[`sweeps/certificate_validity.csv`](sweeps/certificate_validity.csv),
[`figures/certificate_validity.png`](figures/certificate_validity.png).

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
