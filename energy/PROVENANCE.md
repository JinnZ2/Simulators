# Provenance & Decision Ledger
## Coupled Quintessence × Early Dark Energy — Metacognitive Metrology Project

**Purpose.** This document is the chain-of-reasoning record for the project. It is written for two readers: a human researcher picking this up cold, and an AI agent asked to extend it. Every major decision point (DP) records: the situation, the choice made, the alternatives considered and why they were rejected, and the evidence. Every open branch (OB) records: what is known, what is unknown, and the cheapest next step. Nothing in here is decorative — if a claim in any module or figure cannot be traced to a DP and an anchor test, treat it as unverified.

**Reading order.** §1 architecture → §2 decision ledger → §3 anchor tests (trust calibration) → §4 falsification ledger → §5 open branches → §6 file map → §7 reproduction → §8 notes for AI successors.

---

## 1. System architecture (what exists)

Five capability layers, all in `energy/modules/`:

1. **Dynamical engines.** `unified_cq_ede.py` (single-integration CQ+EDE hybrid, autonomous ODE system) and `late_trigger_lens.py` (phenomenological w(z)-kink background+growth integrator). These are the ground truth generators; everything else interprets their output.
2. **Lens modules** (one question each): `overlap_lens.py`, plus earlier lens modules (iterations 1–6) covering degeneracy, cancellation, and corridor mapping.
3. **Gate system.** Four observational gates: DESI (w0–wa distance, σ units), σ8 (structure amplitude, |σ8−0.81|/0.016), H0 (one-sided, max(0, 68.5−H0)/0.5), CMB (100θ*, Planck 1.04109±0.00030, σ units). Aggregate distance D = √Σ log10(1+gᵢ)². A model "closes" when all gates pass at working tolerance.
4. **Metrology layers.** Success geometry (gate-gradient cosines, obstruction rank, LP improvement cones), swampland gates (dS: λ≳1; distance conjecture: Δφ≲1), falsification engine.
5. **Exploration surfaces.** `energy/app/` — CQ playground (`index.html`) + Late-Time Needle Lab (`needle_lab.html`, instrument-design simulator over 16 precomputed kink models in `needle_data.js`).

---

## 2. Decision ledger

### DP-1 — Unified integration instead of multiplicative composition
- **Situation.** Early work composed CQ and EDE effects multiplicatively from separate lens outputs.
- **Choice.** Build one engine integrating CQ autonomous system + EDE Klein–Gordon field together, with EDE switched to a w=1/3 fluid after z_c.
- **Rejected.** Multiplicative composition: <1% accurate for σ8 but **fails for H0** — the coupling drags the sound horizon, an interaction effect that factorization cannot represent.
- **Lesson (load-bearing).** When two mechanisms share the background, composition of separate runs is not an approximation — it is a different theory.

### DP-2 — EDE contribution to the deceleration parameter q
- **Situation.** First unified runs showed r_s *growing* with EDE fraction (rs_ratio ≈ 1.03) — physically backwards.
- **Choice.** Net EDE term in q is 1.5·Ω_ede·w_e, i.e. 0.5(Ae−Be) in the KG phase and 0.5·Oe in the fluid phase. The remainder is absorbed by matter closure.
- **Rejected.** Naive Ae (KG) or 2·Oe (fluid) coefficients — both double-count because Ω_m is defined by closure, not evolved.
- **Evidence.** After fix: E_ede/E_ref = +1.1–1.6%, rs_ratio ≈ 0.989 (matches independent `edelens` at the per-mille level).
- **Warning to successors.** This is the single easiest bug to reintroduce. Any refactor of the RHS must re-run `anchors()` (§3).

### DP-3 — Friedmann anchor normalization
- **Situation.** CMB channel returned r_s_ref ≈ 265 Mpc instead of ≈147 Mpc.
- **Choice.** E² = ρ̂_tot (plain), with E_i = √(OR0·a_i⁻⁴/z_i).
- **Rejected.** E² = ρ̂_tot/3 — a √3 factor inherited from dimensionless-variable conventions in the CQ literature; harmless internally, fatal when converting to Mpc.
- **Companion fixes.** Baryon loading in c_s uses **photons only** (R = 3Ωb/4Ωγ ·a, Ωγ = 5.44e-5; using total radiation costs 4%); evaluate at z* = 1090 (decoupling), not the drag epoch.
- **Evidence.** Engine ΛCDM zero point: r_s = 144.44 Mpc, χ = 13864 Mpc, 100θ* = 1.04179 → 2.3σ from Planck. This residual is a **known systematic**, carried honestly in every CMB verdict (see §4 note).

### DP-4 — Sound-horizon/gate calibration philosophy
- **Situation.** Both engines sit at **−3.0σ LOW** vs Planck 100θ* = 1.04109 ± 0.00030 (A4 in `R_EQ_MODE='physical'`: −2.96σ; A5: −3.04σ). They agree with **each other** to r_s = 144.21 Mpc (4 decimals) and 0.08σ in 100θ*. The earlier ledger claim of *opposite* signs (+2.33σ HIGH / −3.03σ LOW) was based on an A4 value 1.04179 that is **not reproducible from the current code**; see the bisect in DP-13 and `samples/g1_bisect.sample.txt`.
- **Choice.** Keep absolute computation, report σ against Planck **with sign**, and **disclose the zero-point offset** rather than recalibrating onto Planck.
- **Rejected.** Recalibrating r_s or χ onto the Planck value. Tempting; would have made every CMB verdict look cleaner; would also have hidden a real modeling limitation and broken comparability across modules.
- **Lesson.** A disclosed systematic is a measurement; a calibrated-away systematic is a story.
- **Corollary (for downstream verdicts).** Any per-engine absolute σ against Planck for the CMB gate is **uninterpretable in isolation** until the engine's own ΛCDM zero point is quoted. Report `Δθ*` against the same engine's ΛCDM as the primary column; keep absolute-vs-Planck as a labeled second column.
- **Corollary (DP-11 champion).** Reported as absolute-vs-Planck 2.4σ; same-engine Δ against A5 ΛCDM is **+5.43σ**. The mechanism shifts 100θ* by +5.4σ (crossing Planck from below); it does not sit near null. Rewrite the champion line in these units.

### DP-5 — Closure scheme for the late-time lens
- **Situation.** User's draft `late_trigger_lens.py` initialized Ω_DE to exactly 0; with w(a) phenomenology the DE density could never grow from zero — the scheme was silently unstable.
- **Choice.** Evolve lnΩ_de with its own conservation law: state [lnE, lnΩr, lnΩde], lnΩde′ = −3(1+w_de) − 2h, matter obtained by closure. Shoot lnΩde_i (log bisection [−60, −0.1], 44 iters) to Ω_de(0) = 0.685.
- **Rejected.** Evolving Ω_de = 1 − Ω_m − Ω_r directly (closure-for-DE): subtractive cancellation at early times; DE effectively pinned to zero.
- **Lesson.** Whatever component you *care about* must have its own conservation law; never let the quantity of interest be the closure remainder.

### DP-6 — Shooting strategy (all engines)
- **Choice.** Log-space bisection, 40–44 iterations, on the *initial* dynamical variable (y_i for CQ, pe_i for EDE, lnΩde_i for late lens), targeting a *today* condition (Ω_DE0 = 0.685).
- **Why.** The systems are stiff and exponentially sensitive; log brackets are wide-safe and 44 iterations of bisection ≈ 13 digits, far below model-systematic floors.
- **Known cost.** Nested shooting (y_i outer, pe_i inner) makes each unified run seconds-scale; grids must be budgeted accordingly (see DP-10).

### DP-7 — Running coupling parameterization
- **Situation.** Constant-β corridor failed (§4, F-2).
- **Choice.** β(N) = β₀ + β₁(1−eᴺ): constant today, vanishing at early times; optional late-trigger multiplier e^{npl·N} (∝ aⁿ).
- **Rejected (tested, not assumed).** Late trigger (npl > 0): dodges the θ* gate as designed, but buys **nothing** — σ8 and H0 gains vanish with the early action. Recorded as "no-go in miniature": the coupling's usefulness *is* its early action; triggering it late is equivalent to not having it.

### DP-8 — CMB as the fourth gate
- **Situation.** Three-channel closure had been found: (λ=1.1, β₁=0.2, f=0.35) → DESI 1.35σ, σ8 = 0.810, H0 = 72.95.
- **Choice.** Add 100θ* as an independent gate with all other parameters pinned.
- **Result.** It vetoed everything: closure point 837σ; corridor 283σ; EDE-only f=0.10 at 52σ. Maximum survivable combined strength ≲ 0.05, and even that sits at ~54σ.
- **Decision.** Adopt the veto as the project's central fact rather than tuning it away. Everything after DP-8 (swampland gates, success geometry, late kink) is downstream of respecting this wall.

### DP-9 — Interpreting the obstruction geometrically
- **Situation.** User asked whether "components interfering with the trajectory" could be made a geometry.
- **Choice.** Gate-gradient analysis: cosine matrix of gate sensitivities, D-distance landscape, Farkas/LP improvement cones.
- **Findings (now load-bearing).** DESI↔CMB gradient cosine = **−0.93** (master antagonism: what pleases one angers the other); S8↔CMB = +0.93 (co-moving); H0 approximately orthogonal (free direction). Effective obstruction rank 2. The LP escape cone is a **linear mirage**: the real CMB wall is nonlinear (13σ → 141σ between β₁ = 0.05 → 0.1).
- **Lesson.** Local feasibility certificates (Farkas) can certify directions that the nonlinear wall annihilates one step later. Treat LP cones as hypotheses, not maps.

### DP-10 — Grid execution discipline
- **Situation.** A 25-run grid appeared to time out at 120s; results had in fact completed (kernel state held all 25 entries).
- **Choice (now policy).** After any long cell, inspect kernel state before re-running; never assume timeout = no result. Self-contained cells only (sys.path + importlib.reload) because kernel resets recur.
- **For successors.** Batch grids to < ~90s or persist incrementally to disk.

### DP-11 — The late-time turn
- **Situation.** With the early-time wall established (DP-8), the question inverted: is there any deviation that lives *after* recombination entirely?
- **Choice.** Phenomenological kink w_de(a) = w0 + wa(1−a) + δw·tanh-step at a_t ≈ 0.9–0.95 (z ≈ 0.05–0.1), full four-gate evaluation.
- **Result.** Champion (a_t=0.92, δw=+0.10, Δa=0.05): DESI 1.11σ, σ8=0.807, H0=67.4.
  - **θ* primary (Δ vs A5 ΛCDM): +5.43σ** (mechanism moves 100θ* by 0.163%, crossing Planck from below).
  - **θ* absolute vs Planck: +2.4σ** — smaller magnitude because the shift lands near Planck, not because the mechanism is null. Kept as a labeled second column.
  - Other gates: DESI 1.11σ, σ8=0.807, best D = 0.70 at (0.95, 0.10, 0.05).
  - Catch: w(z) shape departs from CPL at z≳0.3 (RMS 0.157) — a CPL-assuming analysis would misread it. The +5.4σ same-engine θ* shift is a **second** discriminator against ΛCDM in the same direction the DESI-CPL pull was pointing; this reframes the champion from "passes all four gates" to "passes DESI+σ8+H0 gates and produces a coherent +5σ θ* shift that a systematics-aware CMB analysis must confront."
- **Instrument consequence.** Signal sizes: ΔH/H +0.73% (z≈0.15); ΔdL/dL −0.59% (z≈0.37); Δfσ8 −1.14% (z≈0.14). Detectable at 10.8σ combined with 1000 chronometers at 2%; sirens alone need ≈1600 events at 7% — ET-era, not LVK-era.
- **Decision.** Build the instrument-design exploration space (Needle Lab) rather than a paper-style claim: the deliverable is the *design problem*, not a detection forecast.

### DP-12 — Public surface design
- **Choice.** Two-page static site: model playground + instrument lab, all model data precomputed to JSON (needle_data.js), no backend.
- **Rejected.** Live-compute backend: the engines are seconds-per-run with nested shooting; a static precomputed grid is honest about what is and isn't covered, and cannot be misused outside validated domains.
- **Known defect fixed en route.** JS key-format mismatch ('0.92_0.10' vs '0.92_0.1') emptied the canvases; fixed via parseFloat key reconstruction. If selects are ever extended, key formatting must remain `parseFloat`-canonical.

### DP-13 — θ* zero-point bisect (external audit-driven)
- **Situation.** External audit G1 flagged that the ledger reported A4 = +2.33σ HIGH and A5 = −3.03σ LOW — opposite signs, 5.37σ apart — while calling them "same systematic family." The audit asked for a bisect over the modeling choices (z*, radiation content, χ limits, quadrature, Ωγ, C_OVER_H0) to name the responsible knob.
- **Bisect executed** (see `samples/g1_bisect.sample.txt`):
    - Both engines share OM0=0.315, OR0=9.2e-5, OG0=5.44e-5 (photons only in c_s), OB0=0.049, H0=67.4, C_OVER_H0=4448 Mpc, z*=1090, `scipy.simpson` on log-spaced a-grids.
    - Grid density differs: `unified_cq_ede` uses **4000** points for χ, `late_trigger_lens` uses **3000**. Effect on 100θ*: **0.08σ**. Not the culprit.
    - `unified_cq_ede` carries an `R_EQ_MODE` switch (`'it6'` default vs `'physical'`). With `'physical'`, both engines match r_s to 4 decimals and χ to 0.002%. With `'it6'` (the DEFAULT), r_s = 115.8 Mpc / 100θ* = 1.229 — **25% off** and unusable for CMB verdicts.
    - The doc's stated A4 = 1.04179 does **not** come from either mode of the current code. It is stale.
- **Choice.**
    1. Correct A4/A5 in §3 to their measured values (both −3.0σ LOW, agreeing to 0.08σ; single systematic, not two).
    2. Enforce `R_EQ_MODE='physical'` at every θ* callsite; `cmb_observables` docstring at line 289 already says "Needs R_EQ_MODE='physical'" — treat as load-bearing.
    3. Report champion θ* as Δ vs same-engine ΛCDM (primary) with absolute-vs-Planck as labeled second column.
- **Consequence for DP-11.** The DP-11 champion's θ* is a **+5.43σ same-engine shift**, not a null pass. The line in §2 DP-11 has been rewritten to reflect this.
- **Cheapest next test (open).** The −3.0σ shared offset is a genuine physics gap between these engines and a full Boltzmann θ*. Candidates: recombination-history approximation (z*=1090 is a proxy; the drag epoch or full visibility function differs), sub-percent χ grid at a→0 (though our 3000/4000 comparison rules this out at 0.08σ), radiation temperature evolution vs Ωγ constant. Not yet pinned; not a blocker for the falsification ledger.
- **Lesson.** A load-bearing switch that silently gives 25%-off physics in default mode is a footgun. Either the default is wrong, or the callsite must enforce it. This ledger picks the callsite fix; a future refactor should consider flipping the default.

### DP-14 — H0 gate clip (external audit G2)
- **Situation.** External audit G2 flagged that the H0 gate
  `max(0, 68.5 − H0) / 0.5` in `late_trigger_lens.gate_vector` is
  one-sided: any model with `H0 > 68.5` returns g_H0 = 0 and therefore a
  zero gradient in the H0 direction. DP-9's "H0 approximately orthogonal"
  and "obstruction rank 2" (4 gates → 3 live after the clip, minus one
  antagonistic pair → 2) may fall out of the clip, not the physics. Also
  the denominator 0.5 is Planck's σ_H0 — far tighter than any published
  H0 uncertainty on the SH0ES side of the tension (SH0ES: 73.04 ± 1.04).
- **Choice (this pass).** Add `h0_two_sided=True` option to
  `gate_vector` with named `h0_ref` and `h0_sig` parameters; keep the
  default one-sided form so existing analyses reproduce byte-for-byte.
  Document both defaults and the reason to run two-sided next.
- **Deferred.** Actually re-running DP-9's cosines / obstruction rank
  under the two-sided form. That is **OB-8** below; if rank stays 2 and
  H0 stays orthogonal, DP-9 is real; if either moves, DP-9 gets amended.
- **Origin of 0.5.** Not documented in the surviving code. Best guess:
  Planck 2018 σ_H0 = 0.5 km/s/Mpc, treated as a "how far can we go
  toward SH0ES before we exit the Planck error box" scale. Any future
  gate revision should replace with a joint-tension-scale sourced
  uncertainty (SH0ES 1.04 or combined ~ 1.3).

### DP-15 — D-metric compresses catastrophe (external audit G3)
- **Situation.** `D_of(g) = √Σ log10(1+g_i)²` is treated as a "distance"
  in downstream text but the log-compression under-weights catastrophic
  single-gate failures: log10(1+837) = 2.92 vs log10(1+1.35) = 0.37, so
  an 837σ veto counts only ~8× a passing gate. D-based rankings
  therefore obscure exactly the gate that is killing you.
- **Choice.** Keep D as a ranking heuristic (the log squashes make it
  robust to any single blow-up) but label it explicitly. Docstring
  updated on `D_of`; every downstream verdict must report the raw gate
  vector alongside the D value. Do not describe D as a geometry or a
  distance in σ-space.

### DP-16 — Named denominators (external audit F5)
- **Choice.** Every threshold / normalization used in a gate or a
  cross-module verdict is named here in one place. New entries live in
  §7 (Reproduction notes).
- **Committed to §7 in this pass:**
    - `S_min = 0.05` threshold in `metrology_diagnostic.MetrologyDiagnostic.S_MIN_THRESHOLD` — dimensionless smallest Fisher singular value of the parameter-Hessian (the callsite hands in a Fisher matrix built with the caller's own σ conventions; the 0.05 is calibrated against the tomographic-verdict rank-3 jump from ~0.03 to ~5 seen in the OKComputer geodesic-foot payload). Not a physical unit; a *rank-collapse threshold* on whatever Fisher matrix is passed in.
    - phantom-layer χ² (`sweeps/phantom_layer_sweep.csv`) — Mahalanobis distance under the DESI-mock covariance `DESI_MU=(-0.86, -0.53)`, `DESI_COV = [[0.04², 0.4·0.04·0.16], [0.4·0.04·0.16, 0.16²]]` (correlated w0/wa errors, 0.4 correlation), same convention as `payload_bridge.DESI_MU`/`DESI_COV` and `late_trigger_lens.gate_vector`'s DESI channel.
    - CMB gate: 100θ* against Planck 2018 = **1.04109 ± 0.00030** (`THS_PLANCK`/`THS_ERR` in both engines). See DP-4/DP-13 for the required same-engine-Δ reporting.
    - H0 gate: default one-sided against **h0_ref=68.5** with `h0_sig=0.5` (see DP-14 for the audit's objection and the two-sided option).
    - σ8 gate: `|σ8 − 0.81| / 0.016` — 0.81 is the ΛCDM control σ8 in the sub-horizon growth approximation used here; 0.016 is a working tolerance, not a Planck error bar.
- **Rule for successors.** A new gate or a new threshold does not exist for cross-module use until it is named here with (a) the numerical value, (b) the units or normalization, and (c) the data source or the tolerance it represents.

### DP-17 — Certificate validity radius (external audit 3.5; DP-9 companion)
- **Situation.** DP-9 labeled its LP escape cone a "linear mirage" — the CMB wall is nonlinear (13σ → 141σ across β₁ = 0.05 → 0.10). The audit asked for the exportable, cosmology-free quantity that names *how far* the linear certificate is trustworthy from any given base point.
- **Definition.** For a certificate computed at parameter point p₀:
    - `β₁_onset` = first sweep point where actual Δθ*(β₁) deviates from the **linear-in-β₁ tangent** at p₀ by more than DEV_TOL = 20%.
    - `r_valid = |β₁_onset − β₁_certified|`.
    - **`r̂ = r_valid / β₁_certified`** — dimensionless, no cosmology in it. This is the exportable quantity.
- **Sweep** (see `exploration_layers/certificate_validity_lens.py`, `samples/certificate_validity_lens.sample.txt`, `sweeps/certificate_validity.csv`, `figures/certificate_validity.png`). All Δθ*_σ reported as same-engine Δ per DP-13.

  Base point A: (λ=1.1, β₁_certified=0.05, f_ede=0.05, z_c=3162):

  | β₁    | 0.02 | 0.03 | 0.04 | **0.05** | 0.06 | 0.07 | 0.08 | 0.10 | 0.12 |
  |------:|-----:|-----:|-----:|--------:|-----:|-----:|-----:|-----:|-----:|
  | Δθ*_σ | 13.6 | 22.8 | 35.2 | **51.0** | 69.9 | 92.0 | 117.1| 176.4| 247.1|

  Base point B (r̂-stability test): (λ=0.9, β₁=0.05, f_ede=0.05, z_c=3162):

  | β₁    | 0.02 | 0.03 | 0.04 | **0.05** | 0.06 | 0.07 | 0.08 | 0.10 | 0.12 |
  |------:|-----:|-----:|-----:|--------:|-----:|-----:|-----:|-----:|-----:|
  | Δθ*_σ | 26.4 | 35.4 | 47.6 | **63.1** | 81.7 | 103.5| 128.4| 187.2| 257.2|

- **Shape.**
    - Base A: log-log slope = +1.64, R² = 0.9952 (power law wins; Δθ*_σ ∝ β₁^1.64).
    - Base B: log-log slope = +1.30 (R² 0.976), log-linear slope = +23 (R² 0.986) — **exponential edges out power law here.** Functional class is base-point-dependent even when r̂ is not.
- **Result.**
    - **r̂(λ=1.1) = 1.00** (onset at β₁ = 0.10, tangent-slope 1732 σ per β₁ deviates by ≥20% by β₁ = 0.10).
    - **r̂(λ=0.9) = 1.00** (same onset).
    - **Relative difference: 0%.**
- **Interpretation.** r̂ is stable across the two base points tested → **property of the wall**, not of the base point. The LP-certificate around the coupled-quintessence CMB wall stays trustworthy for roughly a **doubling** of the certified β₁ before nonlinearity breaks it. A certificate at β₁ = 0.05 is honest out to β₁ ≈ 0.10; past that, the linear tangent under-predicts the θ* damage by more than 20%. Two base points is a weak stability test — a third at f_ede shifted (per the audit's TODO 3.5.d) would harden the claim, but r̂ = 1.00 exactly at both current points is a strong signal.
- **Puzzle piece.** r̂ ≈ 1 is a *shape* property of a locally-power-law wall with slope near 1.5: a linear tangent at any point under-estimates the tail by ~20% by the time you have doubled the coordinate. This should transfer to any nonlinear-wall-plus-linear-certificate pair with similar convexity. If a future gate wall has slope 3 or 5, r̂ will be smaller; if it has slope 1.1, r̂ will be much larger.
- **Numerical footnote.** With CERT_BETA1 = 0.05 and DEV_TOL = 0.20, β₁_onset happens to land ON the sweep point 0.10 for both base points — a coarser grid would still detect the onset here, but the *precision* of r̂ = 1.0 is one grid step (Δβ₁ = 0.02, so r̂ known to ±0.4). A finer grid would sharpen the number; the qualitative result (LP-certificate radius ~100% of certified β₁) is robust.

### DP-18 — DIVERGENCE PLAYGROUND wired in (external audit spec)
- **Situation.** Audit added the DIVERGENCE PLAYGROUND spec: a hash-sealed multi-reader loop over fork points that measures spread on three structured axes (verdict / mechanism / collapse), with C1-C4 coincidence tests and a null-ensemble runner. The object under test is not the cosmology; it's the spread across readers.
- **Choice.** Land as a top-level `divergence-playground/` folder (matches the `inverseminar/` and `claim-audits/` pattern — general mechanism, phone-buildable, stdlib-only). Seed a project-specific `energy/FORKS.jsonl` with the seven forks harvested from this ledger and the earlier audit passes.
- **Fork inventory** (`energy/FORKS.jsonl`, status snapshot as of DP-18):
    - FK-1 θ* engine split — **RESOLVED by DP-13** (documentation drift, not engine disagreement)
    - FK-2 generative CPL recovery — **RESOLVED by F2** (basis echo)
    - FK-3 H0 orthogonality — **PARTIAL**: DP-14 added the two-sided option, OB-8 stakes the rerun
    - FK-4 fs8 ≈ 8× ΛCDM — **OPEN**: cheapest collapse is a tolerance + high-z cutoff sweep on `run_iteration6`
    - FK-5 α wall classification — **OPEN**: cheapest collapse is `singularity_cartographer` at 3 epochs along the attractor
    - FK-6 certificate validity r̂ — **RESOLVED by DP-17** (r̂ = 1.00, property of the wall)
    - FK-7 D as distance — **STAKED**: DP-15 caveat lands the docstring; the D-vs-Pareto ordering test is OB-9
- **Convergence rule.** A claim that N quantities converge on a common cause must first pass C1 (no deterministic map collapsing them to one), then C2 (state N_trials before claiming surprise), then C3 (pre-declared tolerance window), then C4 (out-of-sample prediction). Any prior "convergence" reading in this repo that was not run through this ladder is under audit; the rs_ratio / E_ede / Δfσ8 "three shadows" note in the earlier chat log was the trigger case.
- **Anchor.** Playground modules ship with self-tests; running `python3 seal.py` verifies the seal, hash-mismatch detection, and post-reveal-commit rejection. Worked example on FK-2 in `divergence-playground/samples/worked_example.sample.txt`.

---

## 3. Anchor tests (trust calibration)

Re-run these before trusting any modification. `anchors()` in `unified_cq_ede.py` performs the first two.

| # | Anchor | Expectation | Status |
|---|--------|-------------|--------|
| A1 | Unified CQ (β const) vs iteration-6 standalone | Δw0 < 4e-6 | ✅ holds |
| A2 | Running coupling landmark (λ=1.1, β₁=0.2) | w0=−0.86324, wa=−0.33771, DESI 1.35σ | ✅ holds |
| A3 | Unified EDE vs edelens | rs_ratio 0.9886 vs 0.9834; σ8 0.777 vs 0.773 | ✅ holds |
| A4 | `unified_cq_ede` ΛCDM zero point (`R_EQ_MODE='physical'`) | r_s=**144.21 Mpc**; χ=13863.84 Mpc; 100θ*=**1.04020** vs Planck 1.04109±0.00030 → **−2.96σ LOW**. See `samples/g1_bisect.sample.txt` — corrects an earlier +2.33σ HIGH value that is not reproducible from the current code. **`R_EQ_MODE` footgun**: the module's default `'it6'` gives r_s=115.8 Mpc / 100θ*=1.229 (25% off); line 289 comment `Needs R_EQ_MODE='physical'` is load-bearing. | ✅ holds |
| A5 | `late_trigger_lens` ΛCDM zero point | r_s=**144.21 Mpc**; χ=13864.17 Mpc; 100θ*=**1.04018** vs Planck → **−3.04σ LOW**. Matches A4 (both engines) to 4 decimals in r_s, 0.002% in χ, 0.08σ in 100θ*. The `−3σ` offset is a **single** disclosed systematic shared by both engines (photons-only c_s + z*=1090 + sub-percent χ grid recover r_s ≈ 144.2 Mpc where Boltzmann codes give ≈147.1 Mpc). | ✅ holds |

Any future module must state which anchors it inherits and add its own zero-point test before its first scientific claim.

---

## 4. Falsification ledger (what is dead, and what killed it)

- **F-1: Multiplicative CQ×EDE composition** — killed by H0 (coupling drags r_s; interaction term not factorizable). DP-1.
- **F-2: Constant-β corridor for the H0 tension** — σ8/H0 closure exists at β≈0.09–0.11 × f≈0.12–0.17 (σ8≈0.79–0.80, H0≈69.0–69.8) but is CMB-vetoed at 283σ. DP-8.
- **F-3: Three-channel closure (λ=1.1, β₁=0.2, f=0.35)** — killed at 837σ by θ*. DP-8. **This was the moment the project pivoted from "find the model" to "map the obstruction."**
- **F-4: β₁=0.4 champion** — irreparable independently (σ8≈3.2 gate units, H0=61.6). Not a near miss; a structural failure.
- **F-5: Late-triggered coupling β∝aⁿ** — dodges θ*, buys nothing. "The coupling's usefulness is its early action." DP-7.
- **F-6: Shallow-slope CQ** — swampland dS gate (λ≳1) kills the shallow-λ region that would soften other tensions.
- **F-7: Large constant β (≳0.15)** — distance conjecture: field excursion Δφ = 2.66 ≳ 1.
- **F-8: Strong combined frontier** — anything above combined strength ≈0.05 dies at θ* ≥ 54σ.
- **Still alive:** (i) the late-time kink family (DP-11) — passes all four gates, distinguishable from ΛCDM by next-generation instruments; (ii) pure EDE at f=0.05 as closest-to-success point (D=1.19 vs ΛCDM 1.68); (iii) H0-orthogonal directions (free parameter space per DP-9 geometry).

---

## 5. Open exploration branches

Ranked by (information gain)/(cost), cheapest meaningful next step stated for each.

- **OB-1 (was offered, unconfirmed): real DESI w(z) bin covariances as gates.** Replace analytic DESI distance with binned w(z) pulls + published covariance. Cost: low. Gain: converts the DESI gate from proxy to instrument.
- **OB-2: Non-CPL shape tests of the kink.** The RMS-0.157 CPL mismatch (DP-11) is itself a signature: fit binned-w and PCA/basis-expansion reconstructions to kink mocks. Cost: low–medium. Gain: tells observers *how to look* without CPL blinders.
- **OB-3: Kink × growth observables joint forecast.** Needle Lab treats channels independently; add cross-covariances (H–fσ8 from the same 21cm survey). Cost: medium. Gain: realistic combined σ, possibly lower requirement on sirens.
- **OB-4: Microphysical origin of the kink.** The kink is phenomenological; candidates: late phase transition, oscillating-field onset, coupling trigger β(a). Any candidate must re-enter `unified_cq_ede.py` and pass anchors. Cost: high. Gain: converts the surviving phenomenology into a theory with prior-plausible parameters.
- **OB-5 (offered, unconfirmed): running-vacuum channel; neutrino trigger; k-dependent fuzzy-DM growth.** Each is a new gate or a new mechanism; same entry protocol as OB-4.
- **OB-6: Point the metrology stack at a non-cosmology dataset.** The 4-gate + obstruction-geometry machinery is domain-agnostic. Cost: medium (mostly gate redefinition). Gain: tests whether the *method*, not just the models, is doing real work.
- **OB-7: AI-facing API over the stack.** Scriptable gate evaluation (JSON in/out) so other agents can propose models and receive gate vectors. Natural extension of OB work; see §8.
- **OB-8: Rerun DP-9 obstruction geometry under two-sided H0 gate.** DP-14 added the `h0_two_sided=True` option to `gate_vector` but kept the default one-sided so existing analyses reproduce. This branch reruns the gate-gradient cosine matrix, D-distance landscape, and the LP escape cone with `h0_two_sided=True`. Two outcomes: (a) obstruction rank stays 2 and H0 stays orthogonal → DP-9 is real; (b) rank changes or H0 stops being orthogonal → DP-9 gets amended, the "H0 free direction" claim is downgraded to "H0 free direction *upward* only," and the "linear-mirage" LP-cone verdict may need reinterpretation. **Cost: low** (mostly re-invoking existing code with one kwarg). **Gain: decides whether one of DP-9's load-bearing verdicts is physics or an artifact of the gate function.**

- **OB-9: FK-4, FK-5, FK-7 collapse tests (from `energy/FORKS.jsonl`, staged by DP-18).**
    - **FK-4** (`fs8 ≈ 8× ΛCDM`, LOW): tolerance sweep on `solve_ivp` (rtol, atol) + high-z cutoff test (N_i ∈ {−10, −14, −18}). If fs8_ratio is stable across all three, F3's "physical blowup, not integrator bug" verdict holds. Should also cross-check by inspecting `β(z)` and `G_eff` traces from `run_iteration6` at z ≫ 1.
    - **FK-5** (`α wall classification`, MEDIUM): run `singularity_cartographer` on the `1 + α·φ̂²` wall at 3 epochs along the attractor trajectory (e.g. N ∈ {−3, −1.5, 0}). If the classified `α_wall` moves, the report's static SIMPLE_POLE classification is a snapshot; if it holds, F4 is wrong and the pole is genuinely attached to the attractor.
    - **FK-7** (`D as a distance`, LOW): for a set of gate vectors, compute D-ordering and raw-gate-vector Pareto (dominance) ordering. If they ever disagree on a pair (i.e., model A dominates B on every gate but has larger D), D is not a metric compatible with the physics. DP-15's docstring caveat is a documentation fix; this test is the empirical version.
    All three are staged for the next writer.

---

## 6. File map

| Path | Role |
|---|---|
| `modules/unified_cq_ede.py` | Unified CQ+EDE engine. Anchors A1–A4. Contains `anchors()` self-test — run before any edit is trusted. |
| `modules/late_trigger_lens.py` | Late-kink background/growth/r_s engine. Anchor A5. |
| `modules/overlap_lens.py` | CQ×EDE degeneracy/cancellation geometry over precomputed manifolds. |
| `modules/README.md` | Module-level documentation (11 modules). |
| `app/index.html` | CQ playground. |
| `app/needle_lab.html` + `app/needle_data.js` | Late-Time Needle Lab: 16 precomputed kink models × instrument simulator. |
| Figures: `unified_corridor.png`, `three_channel_closure.png`, `cmb_gate_verdict.png`, `swampland_gates.png`, `success_geometry.png`, `late_kink_needle.png` | The six verdicts, one image each. |

---

## 7. Reproduction notes

- Python 3.12; scipy's new API (`simpson(y, x=...)`, `np.trapezoid`, `cumulative_trapezoid`) — legacy names removed.
- All engines: log-bisection shooting to Ω_DE0 = 0.685; C_OVER_H0 = 299792.458/67.4 = 4448 Mpc; Ωγ = 5.44e-5 (photons only in c_s).
- Kernel resets recur: every notebook cell must be self-contained (`sys.path.insert` + `importlib.reload`).
- Budget grids < ~90 s or persist incrementally; after a timeout, check kernel state before re-running (DP-10).
- Website: static, no build step; version snapshots via the version manager (latest: playground + needle lab).

### 7.1 Named denominators (per DP-16)

Every threshold and normalization used in a gate or cross-module verdict is listed here. Adding a new gate without an entry here is a documentation bug.

| Name | Value | Normalization | Source |
|---|---|---|---|
| `THS_PLANCK`, `THS_ERR` | 1.04109, 0.00030 | Planck 2018 100θ* | `unified_cq_ede`, `late_trigger_lens` |
| `DESI_MU` | (−0.86, −0.53) | DESI-mock (w0, wa) mean | `payload_bridge`, `late_trigger_lens` |
| `DESI_COV` | [[0.04², 0.4·0.04·0.16], [·, 0.16²]] | corr(w0, wa) = 0.4 | same |
| `S_MIN_THRESHOLD` | 0.05 | dimensionless — rank-collapse trigger on the caller-provided Fisher matrix (calibrated against the tomographic-verdict rank-3 jump ~0.03 → ~5) | `metrology_diagnostic` |
| `S8_LCDM`, σ8 tolerance | 0.81, 0.016 | ΛCDM control (sub-horizon growth approx); 0.016 is a working tolerance, not a Planck error bar | `late_trigger_lens` |
| H0 gate: `h0_ref`, `h0_sig`, one-sided default | 68.5, 0.5, one-sided | See DP-14; two-sided option available; origin of 0.5 undocumented, best guess Planck σ_H0 | `late_trigger_lens.gate_vector` |
| `A_LS`, `A_DRAG` | 1/1090, 1/1060 | z* = 1090 (decoupling) for θ*; z_drag = 1060 for BAO. See DP-3. | both engines |
| `OG0`, `OB0`, `OM0`, `OR0`, `ODE0` | 5.44e-5, 0.049, 0.315, 9.2e-5, 0.685 | photons only in c_s (DP-3); OB0 is Ω_b h² / h² with h=0.674 | both engines |
| `R_EQ_MODE` | `'physical'` REQUIRED for θ* | see DP-13; `'it6'` default breaks CMB gate by 25% | `unified_cq_ede` |
| D-aggregate | log10(1+g_i) squashing | ranking heuristic, NOT σ-metric; see DP-15 | `late_trigger_lens.D_of` |

---

## 8. Notes for AI successors

1. **Trust the falsification ledger more than the conclusions.** Models here die honestly; the ledger (§4) is the durable asset. If your new idea resurrects an F-item, you must explain which premise changed.
2. **Anchor before claim.** Run `anchors()` (A1–A4) and late_trigger_lens self-test (A5) after any engine edit. A diff that moves an anchor is either a bug or a disclosed systematic — decide which, in writing, in this file.
3. **The known systematic.** The θ* zero point is offset from Planck in ΛCDM, and the two engines are offset from each other. See A4/A5 in §3 for signed values and DP-13 in §2 for the bisection that names which modeling choice moves it. Do not "fix" the offset by recalibration (DP-4); if you improve the physics (recombination history, full Boltzmann), record the new zero point here.
4. **Respect DP-2 and DP-5.** The q-coefficient rule and the conservation-law-for-the-quantity-of-interest rule are the two easiest things to break and the two hardest to notice broken.
5. **Append, don't rewrite.** Add new DPs, F-items, and OBs below with the next sequence numbers. Breadcrumbs only work if the trail is contiguous.

*Ledger closes at DP-18, F-8, OB-9. Next writer starts at DP-19.*
