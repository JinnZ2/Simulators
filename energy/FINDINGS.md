# FINDINGS

Author audit of the `energy/` drop. Six findings, four survivals.
The report's headline claims are on trial here, not the sweep data
or the qualitative Instrument A vs B contrast.

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

---

## F4 — SIMPLE_POLE at α ≈ −1/λ² is epoch-dependent

- Wall is `1 + α·φ̂² = 0` → `φ̂² = -1/α`.
- `α = -1/λ²` only holds where `φ̂ ≈ λ` (exponential attractor).
- `φ̂` evolves → the wall **moves**.
- Classifier fixed a moving boundary to a static α.
- Score `0.9999` from 27 cells is over-reported precision.

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
2. **F1** — swap "14 orders lifted" for "the projection is exactly
   rank-deficient by construction (3 params → 2 observables); the
   rank-3 tomographic instrument is well-posed at `S_min = 2.09`."
3. **F3** — instrument `run_iteration6.py` to log `β(z)`, `G_eff`,
   and `f/H` step-by-step and check for the high-z runaway before
   quoting the `fs8 ≈ 8×` veto.
4. **F5** — inline the `S_min` normalization convention and the
   DESI-mock covariance used for the χ² surface in the README or
   in `modules/README.md`.
5. **F4** — recompute the singularity classifier along the actual
   `φ̂(N)` trajectory, not at the static attractor value.
6. **F6** — decide license posture; either request CC0 waiver from
   the module authors or add an explicit `LICENSE.MIT` inside
   `modules/` and note the repo carries a mixed license.
