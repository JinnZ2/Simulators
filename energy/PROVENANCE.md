# Provenance & Decision Ledger
## Coupled Quintessence × Early Dark Energy — Metacognitive Metrology Project

**Purpose.** This document is the chain-of-reasoning record for the project. It is written for two readers: a human researcher picking this up cold, and an AI agent asked to extend it. Every major decision point (DP) records: the situation, the choice made, the alternatives considered and why they were rejected, and the evidence. Every open branch (OB) records: what is known, what is unknown, and the cheapest next step. Nothing in here is decorative — if a claim in any module or figure cannot be traced to a DP and an anchor test, treat it as unverified.

**Reading order.** §1 architecture → §2 decision ledger → §3 anchor tests (trust calibration) → §4 falsification ledger → §5 open branches → §6 file map → §7 reproduction → §8 notes for AI successors.

---

## 1. System architecture (what exists)

Five capability layers, all in `/mnt/agents/output/modules/`:

1. **Dynamical engines.** `unified_cq_ede.py` (single-integration CQ+EDE hybrid, autonomous ODE system) and `late_trigger_lens.py` (phenomenological w(z)-kink background+growth integrator). These are the ground truth generators; everything else interprets their output.
2. **Lens modules** (one question each): `overlap_lens.py`, plus earlier lens modules (iterations 1–6) covering degeneracy, cancellation, and corridor mapping.
3. **Gate system.** Four observational gates: DESI (w0–wa distance, σ units), σ8 (structure amplitude, |σ8−0.81|/0.016), H0 (one-sided, max(0, 68.5−H0)/0.5), CMB (100θ*, Planck 1.04109±0.00030, σ units). Aggregate distance D = √Σ log10(1+gᵢ)². A model "closes" when all gates pass at working tolerance.
4. **Metrology layers.** Success geometry (gate-gradient cosines, obstruction rank, LP improvement cones), swampland gates (dS: λ≳1; distance conjecture: Δφ≲1), falsification engine.
5. **Exploration surfaces.** `/mnt/agents/output/app/` — CQ playground (`index.html`) + Late-Time Needle Lab (`needle_lab.html`, instrument-design simulator over 16 precomputed kink models in `needle_data.js`).

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
- **Situation.** The engine's ΛCDM zero point sits 2.3σ (engine) / 3.0σ (late_trigger_lens) off Planck θ*.
- **Choice.** Keep absolute computation, report σ against Planck, and **disclose the zero-point offset** rather than recalibrating onto Planck.
- **Rejected.** Recalibrating r_s or χ onto the Planck value. Tempting; would have made every CMB verdict look cleaner; would also have hidden a real modeling limitation and broken comparability across modules.
- **Lesson.** A disclosed systematic is a measurement; a calibrated-away systematic is a story.

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
- **Result.** Champion (a_t=0.92, δw=+0.10, Δa=0.05): DESI 1.11σ, σ8=0.807, H0=67.4, θ* 2.4σ — all gates pass; best D = 0.70 at (0.95, 0.10, 0.05). Catch: w(z) shape departs from CPL at z≳0.3 (RMS 0.157) — a CPL-assuming analysis would misread it.
- **Instrument consequence.** Signal sizes: ΔH/H +0.73% (z≈0.15); ΔdL/dL −0.59% (z≈0.37); Δfσ8 −1.14% (z≈0.14). Detectable at 10.8σ combined with 1000 chronometers at 2%; sirens alone need ≈1600 events at 7% — ET-era, not LVK-era.
- **Decision.** Build the instrument-design exploration space (Needle Lab) rather than a paper-style claim: the deliverable is the *design problem*, not a detection forecast.

### DP-12 — Public surface design
- **Choice.** Two-page static site: model playground + instrument lab, all model data precomputed to JSON (needle_data.js), no backend.
- **Rejected.** Live-compute backend: the engines are seconds-per-run with nested shooting; a static precomputed grid is honest about what is and isn't covered, and cannot be misused outside validated domains.
- **Known defect fixed en route.** JS key-format mismatch ('0.92_0.10' vs '0.92_0.1') emptied the canvases; fixed via parseFloat key reconstruction. If selects are ever extended, key formatting must remain `parseFloat`-canonical.

---

## 3. Anchor tests (trust calibration)

Re-run these before trusting any modification. `anchors()` in `unified_cq_ede.py` performs the first two.

| # | Anchor | Expectation | Status |
|---|--------|-------------|--------|
| A1 | Unified CQ (β const) vs iteration-6 standalone | Δw0 < 4e-6 | ✅ holds |
| A2 | Running coupling landmark (λ=1.1, β₁=0.2) | w0=−0.86324, wa=−0.33771, DESI 1.35σ | ✅ holds |
| A3 | Unified EDE vs edelens | rs_ratio 0.9886 vs 0.9834; σ8 0.777 vs 0.773 | ✅ holds |
| A4 | Engine ΛCDM zero point | r_s=144.44 Mpc; 100θ*=1.04179 (2.3σ high — **known systematic, disclosed, not calibrated away**) | ✅ holds |
| A5 | late_trigger_lens ΛCDM | 100θ*=1.04018 (3.0σ high — same systematic family) | ✅ holds |

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

---

## 8. Notes for AI successors

1. **Trust the falsification ledger more than the conclusions.** Models here die honestly; the ledger (§4) is the durable asset. If your new idea resurrects an F-item, you must explain which premise changed.
2. **Anchor before claim.** Run `anchors()` (A1–A4) and late_trigger_lens self-test (A5) after any engine edit. A diff that moves an anchor is either a bug or a disclosed systematic — decide which, in writing, in this file.
3. **The known systematic.** The θ* zero point sits 2.3–3.0σ high in ΛCDM. Do not "fix" it by recalibration (DP-4); if you improve the physics (recombination history, full Boltzmann), record the new zero point here.
4. **Respect DP-2 and DP-5.** The q-coefficient rule and the conservation-law-for-the-quantity-of-interest rule are the two easiest things to break and the two hardest to notice broken.
5. **Append, don't rewrite.** Add new DPs, F-items, and OBs below with the next sequence numbers. Breadcrumbs only work if the trail is contiguous.
6. **The human's working style** (relevant context, stated with consent): decisions arrive as drafts, fragments, and "let the math say what it says." The expected behavior is: extract the structural hunch, test it harder than they ask you to, and report the verdict straight — including when the verdict kills something they liked.

*Ledger closes at DP-12, F-8, OB-7. Next writer starts at DP-13.*
