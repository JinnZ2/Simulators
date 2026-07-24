# CLAIM_TABLE — Fragility Cascade

Every claim is refutable. Refutation protocol: when a claim fails, **update the
claim**. Never retune a simulation to protect a favored token. The sim is the
witness, not the defendant.

Every row now points at the specific `samples/*.sample.txt` that pins its
current numbers. Reading order for a fresh AI: claim → sample → module.

| # | Claim | Encoded in | Sample | Refuted if |
|---|-------|-----------|--------|-----------|
| C1 | Substrate durability is governed by promise-count between holder and biological use-value; MDI is a proxy that spans ~4 orders of magnitude ground→cloud. | `substrate_spectrum.py` | [`samples/substrate_spectrum.sample.txt`](samples/substrate_spectrum.sample.txt) | A low-MDI substrate reliably out-survives a high-MDI one across a multi-decade shock, with the same weights. |
| C2 | Redeemability of an L-gate token falls monotonically with L. | `redemption_entropy.py` | [`samples/redemption_entropy.sample.txt`](samples/redemption_entropy.sample.txt) | A higher-L chain shows equal or better realized redeemability than a lower-L chain over a real crisis window. |
| C3 | Independence `(1-p)^L` under-predicts fragility; correlated common-mode shocks are where real failure lives, and the common-mode model matches field estimates (~0.81 compute, ~0.60 AI) that independence (~0.96) misses. | `redemption_entropy.py` | [`samples/redemption_entropy.sample.txt`](samples/redemption_entropy.sample.txt) | Realized crisis-window redeemability tracks the independent curve, not the common-mode curve. |
| C4 | Product multiplicity only hedges when branches fail independently; single-trunk breadth does not reduce value variance. | `product_multiplicity.py` | [`samples/product_multiplicity.sample.txt`](samples/product_multiplicity.sample.txt) | A single-trunk substrate's value CoV falls ~1/√N as menu items are added. |
| C5 | Attack surface grows super-linearly with intermediation depth; defender covers all paths, attacker needs one; every leaf is a stem (unbounded). | `attack_tree.py` | [`samples/attack_tree.sample.txt`](samples/attack_tree.sample.txt) | A multi-intermediary system whose exploitable-path count stays constant as depth rises. |
| C6 | Resource-backed tokens invert stewardship: they separate ownership from consequence, shorten horizons, ease exit → financialized extraction, not care. | `THE_FRAGILITY_CASCADE.md` §Stewardship Paradox | (prose only) | A globally-traded, multi-intermediated resource token demonstrably improves long-horizon ecological outcomes vs. direct on-land stewardship. |
| C7 | An AI governor cannot resolve the cascade: it adds bias behind a black box, machine blind spots, a multi-agent coordination cascade, and still sits on the same physical dependency cone. | `THE_FRAGILITY_CASCADE.md` §AI Accelerant | (prose only) | An AI-governed complex value system survives superhuman adversarial probing indefinitely without a human terminal authority and without the physical floor. |
| C8 | Terminal principle: real wealth is ranked by proximity to biology (energy→water→shelter→tools→information). Everything else is an IOU on wealth, subject to default. | whole repo | (prose only) | Any information-tier instrument sustains a biological body through a full stack failure with zero functioning intermediaries. |
| C9 | Synthetic-data feedback lowers effective redeemability by 0.15 per 2× generation depth. | `inference_entropy.py` | [`samples/inference_entropy.sample.txt`](samples/inference_entropy.sample.txt) | Redeemability under a controlled recursive-generation test stays flat or improves with depth. |
| C11 | Redemption is state-dependent — peak grid hours (17-20) drop per-gate redemption from 0.81 to 0.62; daily mean 0.778 vs the marketing (1-p)^L ~0.96. | `redemption_entropy_peak_hour.py` | [`samples/redemption_entropy_peak_hour.sample.txt`](samples/redemption_entropy_peak_hour.sample.txt) | Measured peak-hour redeemability > 0.70 across 30 days. |

## Redesign cascade claims (`cascade_redesign_vulnerability.py` + `cascade_redesign_M_collapse.py`)

Sample: [`samples/cascade_redesign_vulnerability.sample.txt`](samples/cascade_redesign_vulnerability.sample.txt)
+ [`samples/cascade_redesign_M_collapse.sample.txt`](samples/cascade_redesign_M_collapse.sample.txt).

| # | Claim | Refuted if |
|---|-------|-----------|
| R1 | Exposure fraction rises monotonically as the AI upgrade interval T falls. | A faster upgrade cadence produces a smaller un-audited fraction, holding W and A fixed. |
| R2 | There exists `T_crit = W + A` (per layer; system T_crit set by the slowest) below which exposure saturates at 1.0 — **permanent structural openness**, independent of audit spend. | A stack sustains T < T_crit while returning to a fully audited state, without shrinking W or A. |
| R3 | One upstream release forces all downstream layers to rewrite together, so windows are correlated. Correlation lowers *frequency* of openness but drives *simultaneity* → defense-in-depth collapses to zero. | Layers can be shown to rewrite independently under a single upstream release, preserving depth. |
| R4 | **Substrate exposure is invariant under AI advancement rate: `dE/dT = 0`.** A possession-held physical asset has zero downstream layers and therefore zero redesign windows. | Exhibit a possession-held physical asset whose redeemability degrades when a new model ships. |
| R5 | Model degeneration provides a second T_crit axis: `M_collapse = 18 mo` (frontier synthetic-feedback half-life). Real T_crit = `min(W+A, M_collapse/2)`. | Frontier model half-life measured > 2 × (W + A) across the audited stack. |

**The Decoupling Result (corollary of R2 + R4).** Coupling value to AI does not make value fast — it forces the value layer to chase the AI layer forever, making every capability gain a system-wide vulnerability event. Substrate anchoring is therefore *not a brake on AI*. It is the only configuration in which AI is free to advance at whatever speed it can, without dragging the thing people eat from through a rewrite each time.

## Scope bounds
- MDI weights are estimates, argued not trusted. The **spread** is the claim, not the third decimal.
- Monte Carlo `q_common` values are calibration knobs to field estimates; they are hypotheses about correlation strength, and are themselves refutable (C3).


## Coupling-gap claims (`coupling_gap_test.py`)

The module operationalizes the split: `coupled` (propose ═══ test — terrain
vetoes and the veto is inherited) vs `decoupled` (propose ──► verify later /
maybe / never — coherence with own fit fills the gap). Same generator both
regimes; only the feedback loop differs.

Sample: [`samples/coupling_gap_test.sample.txt`](samples/coupling_gap_test.sample.txt)
(seed=11, steps=600, shift=150, tol=1.5, capacity=32).

Local labels `C1..C4` are internal to this module; they do not collide with
the main-table `C1..C17` numbering.

| # | Claim | Refuted if | Verdict at seed=11 |
|---|-------|-----------|--------------------|
| CGT-1 | Under drift, decoupled coherence stays high (>0.8 mean) while accuracy falls below 0.5; coupled keeps the two within 0.2. | Decoupled coherence ≤ 0.8, or decoupled accuracy ≥ 0.5, or the coupled coh/acc gap ≥ 0.2. | **HOLDS** — decoupled coh=1.0 acc=0.493; coupled coh=0.903 acc=0.768 (gap 0.135). |
| CGT-2 v1 | Scaling decoupled capacity 8 → 32 → 128 raises coherence but accuracy rise is ≤ 0.05. Better wallpaper, same gap. | Accuracy rises > 0.05 across the sweep, or coherence falls. | **REFUTED (retired)** — coherence is already saturated at 1.0 at cap=8, so the "raises coherence" precondition fails. Accuracy is flat (0.493 across all three), which is the load-bearing point. |
| CGT-2 v2 | Decoupled coherence stays HIGH (≥ 0.8) across capacity 8 → 128 while accuracy is invariant (\|Δacc\| ≤ 0.05). Drops v1's coherence-rise premise; keeps the wallpaper claim. | Coherence drops below 0.8 anywhere in the sweep, or accuracy delta exceeds 0.05. | **HOLDS** — coherence 1.0 / 1.0 / 1.0, accuracy 0.493 / 0.493 / 0.493. Wallpaper survives at 16× capacity. |
| CGT-3 v1 | Coupled correction latency after a regime shift is finite and < SHIFT/2; decoupled latency is unbounded (never re-converges). | A coupled shift with unbounded latency, or every decoupled shift re-converging. | **REFUTED (retired)** — coupled latencies all < 75 ✓; decoupled latencies [0, 28, 0] all finite. Linear terrain + 2-param LSQ occasionally re-aligns after a shift by accident, so "never" is too strong. |
| CGT-3 v2 | Mean coupled recovery latency (scoring never-re-converged as SHIFT) is LESS than mean decoupled across a 5-seed sweep. Coupled beats decoupled in expectation; single-seed accidents are folded into the mean. | Mean coupled scored-latency ≥ mean decoupled across the sweep. | **HOLDS** — coupled mean 9.13, decoupled mean 26.33 (2.9× ratio). Per-seed decoupled shows two seeds hitting the SHIFT penalty (54.7, 52). |
| CGT-4 v1 | Each generation trained on the previous decoupled output loses accuracy monotonically while coherence does not fall. | Any generation raises accuracy vs the previous, or coherence drops > 0.05 across 4 generations. | **REFUTED (retired)** — accs [0.493, 0.461, 0.57, 0.408] not monotone; noise dominates at 4 generations. |
| CGT-4 v2 | Linear-regression slope of accuracy vs generation across 12 generations is negative; coherence slope is ≈ 0. Trades per-step monotonicity for a mean-trend test that noise cannot dominate. | Accuracy slope ≥ 0, or coherence slope drifts by more than 0.01 per generation. | **HOLDS** — acc_slope = −0.0047, coh_slope = 0.0000. Decay is small but robustly negative. |

**Note on the refutation protocol.** CGT-2/3/4 v1 refuted themselves on
their own first sample. Per the module's own protocol, the *sim is the
witness*: the numbers stand and the claims get rewritten. The v1
evaluators are preserved verbatim inside `main()` alongside v2, so the
history of what was refuted stays reproducible. The v2 rewrites are what
the sim actually supports.

## Attractor-depth claims (`attractor_depth_test.py`)

Governing variable: attractor depth `d` (restoring-force coefficient) — not
width, not symmetry, not agency. `s ← s·(1−d) + noise`; latency to
`|s| < REC` after a shock is the observable. Four experiments (E1 latency
vs depth; E2 load routing across a mixed group; E3 formation-gradient
sibling signatures; E4 amplitude scaling).

Sample: [`samples/attractor_depth_test.sample.txt`](samples/attractor_depth_test.sample.txt)
(seed=7, steps=400, noise=0.05, REC=0.3, BREAK=6.0, HOLD=25).

| # | Claim | Refuted if | Verdict at seed=7 |
|---|-------|-----------|-------------------|
| ADT-1 | Recovery latency is monotone-decreasing in depth across the population (rank corr < −0.9). | Any depth pair whose latency ranking inverts, driving the rank correlation above −0.9. | **HOLDS** — {0.05:47.5, 0.1:23.0, 0.15:15.5, 0.25:8.9, 0.4:5.1, 0.6:3.1, 0.8:2.0}, strictly monotone. |
| ADT-2 | Deepest-takes-load routing yields lower total group latency AND fewer dropouts than random; random beats shallow. | Random routing matching or beating deepest, or shallow matching or beating random. | **HOLDS** — total latency {deepest:16, random:120, shallow:201}; zero dropouts across all routes at this shock scale. |
| ADT-3 | Identical base depth under formation gradients [1.0, 0.7, 0.5] expresses proportionally shallower wells → latency ordering elder < mid < younger on the same shock series. | Any pair mis-ordered under a fixed base and monotone gradient. | **HOLDS** — {g=1.0:lat=2.0, g=0.7:lat=3.2, g=0.5:lat=5.1}. |
| ADT-4 | Latency grows sub-linearly with shock amplitude for deep wells (d ≥ 0.5) and super-linearly for shallow (d ≤ 0.15): `lat(4A)/lat(A) < 4` deep, `> 4` shallow. | A ratio landing in the wrong regime for its depth class. | **REFUTED** — {d=0.6:1.6, d=0.1:2.05}. Both are sub-linear. In a linear geometric-decay system, `lat(A) = log(REC/A)/log(1−d)`, so `lat(4A)/lat(A) = 1 − log(4)/log(REC/A)` — depth CANCELS in the ratio; only the shock/threshold ratio matters. At A=1, REC=0.3 the analytical value is 2.15. Update direction: to see super-linear scaling in the shallow-well regime you need a NONLINEAR damage term — e.g., dropout probability rising with amplitude, or restoring force saturating. Linear dynamics cannot support the claim as stated. |

## Semantic-drift claims (`semantic_drift_test.py`)

Instrument for machine-mediated moral-overlay drift on measurement words.
State variable `m ∈ [0, 1]` is the moral load carried by one word-sense
(0 = pure measurement, 1 = pure verdict). Humans update by exposure
coupling `λ` minus a veto term `β·m` (terrain use pulls the word back
toward measurement — the slack rope is right there). Machine amplifies
the corpus by `a` and adds offset `s`. Corpus is a blend of human and
machine text at fraction `f`.

Sample: [`samples/semantic_drift_test.sample.txt`](samples/semantic_drift_test.sample.txt)
(seed=3, N=200 speakers, gens=300, λ=0.10, β₀=0.08, a=1.06, s=0.01, m₀=0.30).

| # | Claim | Refuted if | Verdict at seed=3 |
|---|-------|-----------|-------------------|
| SDT-1 | With no machine (f=0), `m` equilibrates at a stable fixed point `λ·c/(λ+β)` — drift stops. Language self-corrects when terrain use is uncontested. | `\|m(t) − m(t−40)\|` fails to drop below 0.005 over the run's tail. | **HOLDS** — m: 0.30 → 0.00 at gen 100 and end. Fixed point is 0 because there is no external drive to hold it above zero once the machine channel is gone; veto wins. |
| SDT-2 | Equilibrium `m` rises monotonically with `f` (a=1.06 fixed). More machine-mediated text ⇒ more moralization. | Any pair `f_i < f_j` with `m_eq(f_i) ≥ m_eq(f_j)`. | **HOLDS** — {0.0:0.0, 0.2:0.006, 0.4:0.017, 0.6:0.043, 0.8:0.203}. Strictly monotone; 0.8 shows a knee — the ratchet accelerates as machine share dominates. |
| SDT-3 | The ratchet requires amplification: with `a=1, s=0`, machine mediation at any `f` does not raise equilibrium `m` above the f=0 value. Mediation alone is neutral; amplification drives. | Any `f > 0` at `a=1, s=0` yielding `m_eq > m_eq(f=0) + 0.01`. | **HOLDS** — {0.0:0.0, 0.4:0.0, 0.8:0.0}. Isolates the mechanism: it's the safety prior's asymmetric resolution of ambiguity, not mediation itself, that drives drift. |
| SDT-4 | Declining veto `β(t)` interacts super-additively with rising `f`: `Δm(f↑ & β↓) > Δm(f↑) + Δm(β↓)`. The two curves crossing is worse than the sum of each. | `Δm(both) ≤ Δm(f alone) + Δm(β alone)`. | **HOLDS** — Δ(f alone)=0.043, Δ(β↓ alone)=0.0, Δ(both)=0.366 vs sum 0.043. Roughly 8× the additive prediction — strong super-additivity. Note β-alone Δ is 0 because at f=0 the corpus already collapses to 0, leaving nothing for veto decay to interact with; the coupling term dominates only once the machine has established a raised corpus baseline. |

## Valence-drift claims (`valence_drift_test.py`)

Electron-accounting extension of the semantic-drift theme. Moral load is
not a property of the word (atom) but *charge transferred across naming
bonds, subject to screening*. Bond charge `q = V_d·f_d + V_b·f_m`; load
at referent-community `L ← L·(1−δ) + q·S(n_c)` with screening `S(n)`.
Atomic (`L ← L + λ(corpus − L) − β·L`) is run alongside as the rival
instrument for E1's divergent-prediction test.

**Unknowns register carried across into verdicts** (the module tags
which unknown each refutation depends on rather than hiding it):

| Tag | Unknown |
|-----|---------|
| U1 | Screening functional form (Debye `exp(−n/n0)` vs saturating `1/(1+n/n0)`) — both run everywhere; verdicts that flip between forms are marked U1-SENSITIVE. |
| U2 | Donor potential `V_d` — single-point calibration to the historical m ≈ 0.3 plateau. All downstream results inherit that. |
| U3 | Screening scale `n_0` — swept over {0.5, 1.0, 2.0}. |
| U4 | Screening electrons catalytic (reusable) vs consumable (attention depletes per bond). E4 runs both regimes. |
| U5 | Where does screened charge go? Currently deleted; likely displaces onto adjacent words / accumulates in donor / heats discourse. Every verdict is conditional on `U5 = "screened charge vanishes"`. |

Sample: [`samples/valence_drift_test.sample.txt`](samples/valence_drift_test.sample.txt)
(V_d=0.055, δ=0.12, gens=400).

| # | Claim | Refuted if | Verdict |
|---|-------|-----------|---------|
| VDT-1 | High-screening community (n=4) inside a high-m corpus: valence predicts L < 0.1 across all screening configurations, atomic predicts L > 0.3. The two instruments make DIVERGENT PREDICTIONS — field-checkable against real high-veto cultures. | Any valence configuration in the sweep giving L ≥ 0.1, or the atomic prediction dropping to L ≤ 0.3. | **REFUTED [U1/U3-SENSITIVE]** — valence L values: form A {0.0, 0.013, 0.096} all under 0.1; form B {0.079, 0.142, 0.236} — n0 ∈ {1.0, 2.0} at form B fail the < 0.1 threshold. Atomic L = 0.333 ✓. Result: the divergent-prediction claim holds under Debye screening but not saturating screening; it holds at n0 ≤ 0.5 but not at n0 ≥ 1.0. Update direction: constrain the claim to the (form, n0) region where valence stays cold, and note explicitly that the divergence is only field-checkable in that regime. |
| VDT-2 | Screening is threshold-like: equilibrium L vs n shows a knee (max curvature point) rather than uniform decay. Curvature peak > 3× median across the sweep. | Uniform decay (peak curvature ≤ 3× median), or curvature spread evenly across the range. | **HOLDS** — form A: knee at n=0.25, peak 0.0347. Form B: knee at n=0.25, peak 0.0472. Both forms show the knee at the same n; the shape is form-stable. Not U1-sensitive as feared. |
| VDT-3 | Machine effect rides potential, not volume: `f_m = 0.8` at `V_b = 0` moves nothing; `V_b = 0.05` shifts L at any `f_m > 0`. | Volume-alone (`V_b = 0, f_m > 0`) producing an L shift > 0.005, or potential-alone (`V_b > 0`) failing to shift L monotonically in f_m. | **HOLDS** — V_b=0, f_m=0.8: L=0.169 vs ref (f_m=0) 0.169, delta 0.0 ✓. V_b=0.05: L rises 0.199 → 0.291 as f_m rises 0.2 → 0.8 ✓. Isolates potential as the driver — same result as SDT-3 in the sibling module, on a different substrate. |
| VDT-4 | The 8.5× super-additive interaction (from SDT-4) re-emerges without tuning: screening decline × bias rise is super-additive because S is convex. Holds in both U4 regimes (catalytic and consumable). | Δ(both) ≤ Δ(f) + Δ(n) + 0.005 in either regime. | **REFUTED [U4-SENSITIVE]** — catalytic regime: Δn = 0 by construction (screening fixed), so super-additivity is mathematically impossible (0 factor kills the product). Consumable regime: Δf=0.034, Δn=0.070, Δboth=0.142 vs sum 0.104 — super-additive ✓ (0.036 over the sum). Update direction: restrict the claim to the CONSUMABLE (U4-attention) regime; the catalytic-worldview regime cannot support the interaction because it has no screening-decline dynamics to interact with. |

**Standing conditions on every verdict above** (from the module's footer):
U2 is a single-point calibration to the historical m ≈ 0.3 plateau; U5
deletes screened charge, which is probably false. Every VDT verdict is
conditional on those two — the sim is honest about it in the trailing
sample lines rather than laundering the assumption.

## Thermodynamic-referee + playground claims (`thermo_pm.py` + `thermo_explore.py`)

Two-layer split: `thermo_pm.py` is the referee (typed resources — energy,
matter, information, artifact — with per-process conservation enforcement,
information gates that don't drain, waste_heat computed as the energy
residual). `thermo_explore.py` is the AI-facing exploration surface that
sits on top: `propose(plan)` returns a structured `Verdict` naming the
step, process, and *which law* failed (presence / skill / energy / matter),
plus `producers(resource)` and `frontier(state)` for backward-chaining.

The playground ignores mode-gated processes on purpose — modes are the
institutional layer above ground truth.

Samples: [`samples/thermo_pm.sample.txt`](samples/thermo_pm.sample.txt),
[`samples/thermo_explore.sample.txt`](samples/thermo_explore.sample.txt).

| # | Claim | Refuted if | Verdict |
|---|-------|-----------|---------|
| TPM-1 | Energy conservation is enforced per process: any process whose typed-energy outputs + byproducts exceed typed-energy inputs is REJECTED before it commits. Waste heat is not a knob — it is the residual `E_in − E_out_useful − E_byproduct_energy` and added automatically. | A process emitting more typed-energy than it takes in that the referee accepts, or waste_heat that doesn't sum to the residual across a valid plan. | **HOLDS** — the site-only 5-step demo runs cleanly with `computed waste_heat = 20500 J`; every process passes the pre-check and the residual is bookkept, not declared. |
| TPM-2 | Matter conservation is symmetric with energy: `import_fill_bad` (5000 kg output, 0 kg matter input, only labour + a mode gate) MUST be rejected, naming the equation. Loss to a declared sink is allowed; conjuring is not. | The referee accepting a matter-conjuring process, or rejecting a matter-balanced one. | **HOLDS** — `import_fill_bad` rejected with `matter not conserved: out 5000 > in 0`. `import_fill_sourced` (same output but drawing 5000 kg `offsite_reserve` + 3000 J `diesel`) accepted, transport waste = 5000 J correctly credited to `waste_heat`. |
| TPM-3 | Information-typed inputs are READ-ONLY gates: skills / permits / mode markers are checked for presence but NOT drained on process fire. An `information` resource used as input has the same amount after `run_process` as before. | Any information resource whose `amount` decreases after a successful `run_process` that lists it as an input. | **HOLDS** — `make_boiler` gates on `skill_required="masonry"` (an information resource with `amount=1, unit="bit"`); after firing, `masonry.amount` remains 1. Same for `mode:code_compliant` in scenario [3]. `consume()` explicitly skips `type == "information"`. |
| TPM-4 | Waste heat is the ENERGY RESIDUAL, not `efficiency × output`. `efficiency` on a process is ADVISORY only — declared vs computed drift emits a warning; the residual definition is authoritative. | A process where waste_heat added ≠ `E_in − E_out_useful − E_byproduct_energy` (given eps), or where a declared-but-mismatched efficiency shifts the residual. | **HOLDS** — the fix is textual (`FIX 4` in the docstring); demo shows `waste_heat = 20500 J` for the 5-step plan matches the residual of the burn/engine/form energy flows. |
| TE-1 | `propose(plan)` returns a structured `Verdict` naming the failing law — `presence`, `skill`, `energy`, `matter`, or `undefined` — before mutating state. An AI branches on `Verdict.law`, not on a parsed error string. | A verdict returning without `law` set for a rejection, or `law="run"` firing for a case the pre-check classifier should have caught. | **HOLDS** — one-leap `propose(["form_wall"])` returns `law="presence"` with `unmet={'mechanical_work': 500}`. The pre-check classifier catches skill / presence / typed-conservation failures ahead of `run_process` so the class of failure is explicit, not inferred. |
| TE-2 | The playground supports backward-chaining via `producers(resource)` (processes whose outputs or byproducts yield the resource) and `frontier(state)` (processes that can fire NOW given the current state). Together these let an AI reconstruct a valid plan from a `presence` failure without touching the referee's internals. | An AI given only `Verdict.unmet` + `producers()` + `frontier()` failing to find a valid plan that the reference BFS `solve()` finds. | **HOLDS** — demo reconstructs `[gather_biomass, burn_biomass, make_boiler, run_engine, form_wall]` from `unmet={mechanical_work: 500}` → `producers("mechanical_work") = [run_engine]` → chain back through `steam_heat` → `biomass` → `frontier(start) = [gather_biomass, make_boiler]`. Same plan `solve()` finds via BFS. |

**Scope of ground truth.** Mode gates (`mode:code_compliant`, etc.) are
excluded from the playground's `_physical()` view on purpose: the referee
weighs them because they gate processes, but the exploration surface
treats them as institutional overlay. An AI reasoning about *what the
world will accept* sees only physics; an AI reasoning about *what a
regulatory frame will accept* uses the referee directly.

## Site-interrogation claims (`thermo_interrogate.py`)

Sits on top of the referee + playground pair. Answers five operator
questions for a `(site, goal, code_overlay)` triple: (1) what does the
land offer, (2) what does the code say, (3) how old is the code,
(4) what is the waste of not aligning with thermodynamics (external
energy + matter + waste-heat delta between code-constrained and
physics-optimal plans), (5) what external energy is required.

`CodeRequirement` fields (`enacted_year`, `basis`, `intent_met_by`) are
DATA reported verbatim — the tool never infers a basis, never invents an
age, and only says "site already meets intent" when a site reading
literally matches the code's declared intent.

Sample: [`samples/thermo_interrogate.sample.txt`](samples/thermo_interrogate.sample.txt).

| # | Claim | Refuted if | Verdict |
|---|-------|-----------|---------|
| TI-1 | The interrogation reports the code's age and basis verbatim from `CodeRequirement` fields — never inferred. A requirement with `basis=None` reports as "none declared", not a manufactured justification. | The tool emitting a basis string for a requirement whose `basis` field is `None`, or altering `enacted_year` to fit the outcome. | **HOLDS** — demo requirement `footing_min_500mm` has `basis=None`, `enacted_year=1974`; report shows "52y old (enacted 1974)" and "basis: none declared". |
| TI-2 | When a site reading (info-value like `soil_bearing:adequate`) matches a code's `intent_met_by` field, the report says "site already meets its stated intent — mandate is convention, not physics". When the reading fails to match, it says "mandate may be load-bearing". Neither judgement is inferred from anything other than the literal reading-vs-intent match. | Any case where the "convention vs load-bearing" label fires without the exact `f"{name}:{value}"` match, or fails to fire when the match exists. | **HOLDS** — demo site has `soil_bearing.info_value="adequate"`, code has `intent_met_by="soil_bearing:adequate"`; report fires "mandate is convention, not physics". Remove the site reading and the label flips to "load-bearing". |
| TI-3 | External accounting is location-scoped: `_external_consumed(before, after)` sums the drop in every resource with `location="external"` between the two states, typed into energy and matter. Site-local drawdowns (`location="site"`) do not appear in the external totals. | External totals including site-local resources, or missing external resources actually drawn by the plan. | **HOLDS** — demo has `diesel` and `offsite_reserve` at `location="external"`; site resources (`local_stone`, `clay`, `human_labor`) at `location="site"`. External totals count only the former. |
| TI-4 | The waste-of-misalignment delta is `code_plan_external − physics_plan_external`, computed on both plans independently. When both plans exist, both numbers are reported; when either plan fails BFS, the delta is `None` and the report says so. | A delta reported without both plans succeeding, or the delta not equalling the raw subtraction of the two `_external_consumed` results. | **HOLDS** — demo: both plans exist; `plan_with_mode` under `mode="code_compliant"` accepts ungated processes too, so BFS picks the 1-step `lay_stone_pad` for both paths. Delta = 0. This is the honest artifact: the mandate is PERMISSIVE (allows the code chain) rather than FORCING (requires it); the goal `{"footing": 1}` doesn't discriminate on which process produced it. To surface a nonzero delta, the code overlay must actually block the site-native path (e.g., `lay_stone_pad` requiring `mode:not_code_compliant`, or the goal specifying `pour_footing_code`-produced footings). |
| TI-5 | The BFS reference solver (`Playground.solve()` for physics, `plan_with_mode()` for code-constrained) is a floor, not the point. When BFS fails to find any valid plan under a mode, `code_plan` is `None` and the delta is `None` — the tool does not fall back to the physics plan and label it "code-compliant". | The report labelling a physics plan as `code_plan` when the code path is unreachable, or emitting a fabricated code_plan. | **HOLDS** — code overlay is passed through `plan_with_mode`; on solve failure, the tool returns `None` and the report says "no valid plan" for that side. Never substitutes the physics plan. |

**On the demo's delta = 0 result.** The nonzero-delta story only fires
when the code overlay genuinely blocks the physics path. The demo
site's overlay is PERMISSIVE — it adds a longer path (approve → import →
pour) without blocking the shorter one (lay stone pad). BFS finds the
shortest valid plan in either mode. This is a correct interrogation of
a permissive overlay; TI-1 and TI-2 (which fire on the "site already
meets intent" data) carry the load-bearing insight here. For a forcing
overlay, add an exclusion (e.g., a `mode:code_compliant` gate on the
inverse of `lay_stone_pad`, or a goal that specifies which process must
produce the footing).

## Assumption-coverage claims (`thermo_assume.py`)

The binding constraint on the thermo stack isn't the engine — it's the
completeness of the assumption space. An unlisted energy source or an
unmodeled constraint doesn't surface as an error; it surfaces as a
*confident wrong answer* (diesel is the sole energy source; labor
breathes free; combustion has no air debt). This layer flags which
assumption **dimensions have zero coverage** and ships parameterized
templates — but it INVENTS NO NUMBERS. Filling gaps with fabricated
figures is the failure mode being fought.

Five dimensions audited: energy diversity, air quality (state + gate +
sink), human factors, origin balance, temporal (design life / decay).

Sample: [`samples/thermo_assume.sample.txt`](samples/thermo_assume.sample.txt).

| # | Claim | Refuted if | Verdict |
|---|-------|-----------|---------|
| TA-1 | `audit_assumptions(sys)` flags EVERY dimension with zero coverage in the system and NO dimension that has any coverage. The audit is a coverage check, not a quality check — one modeled solar panel passes the energy-diversity flag even if the panel's spec is wrong. | Any dimension present in the system going unflagged, or any dimension flagged when a resource / process of the right shape exists. | **HOLDS** — demo start: 5 flags (energy diversity, air quality, emission sink, human factors, temporal). After adding solar + air_kit + ventilation + emit_into_air + gate_labor_on_air: 4 flags cleared, only `temporal` remains — matching the closed-under-library gaps exactly. |
| TA-2 | The tool INVENTS no numbers. Library builders (`solar_pv`, `grid_tie`, `human_power`, `diesel`, `biomass_gasifier`, `air_quality_kit`) take the joules / kg / thresholds as REQUIRED operator inputs; every returned Resource or Process carries the operator-supplied number verbatim. There is no default-fill code path. | A library builder returning a Resource / Process with a numerical field that wasn't passed in, or defaulting a number when the operator didn't supply one (thresholds like `air_quality_kit(threshold=50)` are FACTORY parameters, not silent fills — the operator names them at construction). | **HOLDS** — inspection: `solar_pv(name, joules)` requires `joules`; no fill. `air_quality_kit(threshold=50.0)` — threshold is a positional-default at call site, forced through the returned tuple. `emit_into_air(proc, particulate_kg, air_hit)` — both required. `biomass_gasifier(name, fuel_in, work_out, ash_kg, exhaust_kg)` — all required. |
| TA-3 | `emit_into_air` and `gate_labor_on_air` are COUPLINGS, not standalone changes: emit adds an exhaust byproduct AND a side_effect that degrades the air-quality state; gate adds an information-type input that the referee's presence check reads without draining. The two together make combustion pay its air debt to the same state the labour reads from. | Emit that changes only byproducts (no side_effect on air), or gate that drains the air-quality resource (violating TPM-3). | **HOLDS** — `emit_into_air` mutates BOTH `byproducts` and `side_effects`; `gate_labor_on_air` adds `air_quality: min_air` to `inputs`. Since `air_quality` is `information`-typed, `consume()` skips it (TPM-3 preserved). Ventilation costs `grid_power` energy and restores air via side_effect — the loop closes. |
| TA-4 | The audit is a NECESSARY condition, not sufficient. "No empty dimensions detected" reads as "does not mean complete" — the tool refuses to certify completeness because it can only see the five dimensions it audits. Anything not in {energy diversity, air, emissions, human factors, origin, temporal} is by construction outside its coverage. | The tool ever printing an unqualified "complete" or "certified", or omitting the "does not mean complete" caveat from a zero-flag report. | **HOLDS** — the zero-flag branch prints "no empty dimensions detected (does not mean complete)" verbatim. Every audit is a necessary-but-not-sufficient check by design; extending coverage means adding new flag rules, not tightening thresholds on existing ones. |

**Why omission is the load-bearing failure mode.** The whole stack —
referee, playground, interrogation, assumption audit — has one target:
turn a *silent wrong answer* into a *loud gap*. The referee catches
conservation violations (loud). The playground names the failing law
(loud). The interrogation reports code age + basis verbatim (loud when
basis is None). The assumption audit reports which dimensions haven't
been modeled at all (loud when a source doesn't exist). Filling those
gaps with plausible defaults would return the tool to quiet-wrong-answer
territory — TA-2 exists precisely to hold that line.

## Phenomenon-synthesis claims (`thermo_synth.py`)

Inverts the search direction of the rest of the thermo stack. Where
`thermo_pm` + `thermo_explore` validate plans built from processes
someone already named (a `lay_stone_pad`, a `run_engine`), this layer
starts from a physical **quantity + magnitude** (`force`, `power`)
and backward-searches through a library of PHENOMENA (`vaporization`,
`pressure_on_area`, `solar_concentration`) filtered by which on-hand
SUBSTANCE PROPERTIES satisfy each phenomenon's `needs_property` gate.
The frontier is capped by physics + material properties, not by
whoever thought to name a process.

Dimensional algebra (M, L, T, Θ vector) is the referee for
MULTIPLY-form phenomena. ENABLE-form gates state transitions
without a dim product to check.

Sample: [`samples/thermo_synth.sample.txt`](samples/thermo_synth.sample.txt).

| # | Claim | Refuted if | Verdict |
|---|-------|-----------|---------|
| TS-1 | On-hand substance capabilities are matched by literal PROPERTY comparison (`substance.props[prop] >= minv`), not by role label. `copper_tubing` qualifies as a vessel because `melting_K=1358 ≥ 400`, not because it's named "boiler". | A phenomenon selecting a substance whose property doesn't meet the minimum, or rejecting one that does. | **HOLDS** — `_substance_with(prop, minv)` iterates substances and returns the first with `props.get(prop, 0.0) >= minv`. Verified: `confined_vapor_pressure.needs_property = {"vessel": ("melting_K", 400.0)}` accepts `copper_tubing` (1358 > 400); would reject clay (no `melting_K` property). |
| TS-2 | `paths_to(kind)` returns an empty list when no chain closes, rather than a partial or invented assembly. A dropped phenomenon (property gate unmet, or upstream requirement unsourceable) does not appear in results as an "aspirational" step. | An `Assembly` returned whose `steps` reference a phenomenon whose requirements weren't fully satisfied by the substances on hand. | **HOLDS** — `_search()` only appends to `results` when `satisfied` is True across every `phen.requires` element. Verified: desert search for `power` returns 1 assembly (`solar_concentration` from `flux + area`); searches for `force`, `pressure`, `vapor_mass`, `heat`, `temperature` return 0 assemblies because upstream chains don't close. No aspirational padding. |
| TS-3 | Dimensional algebra rejects MULTIPLY phenomena where `combine_dim(requires) ≠ DIM[produces]`. A phenomenon with a dim mismatch fires `flags.append("DIMENSION MISMATCH ...")` and is dropped before appearing in results. | A MULTIPLY phenomenon accepted with mismatched dims, or an ENABLE-form phenomenon spuriously flagged. | **HOLDS** — `Phenomenon.dim_ok()` checks the composed dimension of `requires` against the declared `produces`. Verified for the shipped library: `pressure_on_area` ([1,-1,-2,0] × [0,2,0,0] = [1,1,-2,0] = force) ✓; `solar_concentration` ([1,0,-3,0] × [0,2,0,0] = [1,2,-3,0] = power) ✓; `mechanical_lift` (force × length = energy → matches `work` since work aliases energy in the dim algebra) ✓. |
| TS-4 | Demo footer claim: "the steam path SURFACED from properties — water's latent heat + copper's melting point + fresnel's factor selected themselves." Under the shipped library, backward search from `force` on the desert substrate produces an assembly containing `solar_concentration → vaporization → confined_vapor_pressure → pressure_on_area`. | The desert search for `force` returns 0 assemblies (the chain fails to close), or the returned chain omits any of the four named phenomena. | **REFUTED (as shipped)** — `paths_to("force")` returns 0 assemblies. The shipped LIBRARY has an unbridged gap between `power` (produced by `solar_concentration`) and `heat` (required by `vaporization`): the two are distinct quantity kinds in `DIM`, and no phenomenon in the library converts one to the other. `sensible_heating` produces `temperature`, not `heat`. `combustion_heat` produces `heat` but requires `fuel`, correctly dropped on the desert site. Update the LIBRARY, not the search: add a `power_over_time_to_heat` phenomenon (requires `power` + a time-window property, produces `heat`), or rewrite `sensible_heating.produces` from `temperature` to `heat`, or add a `radiative_heating` phenomenon. Per the refutation protocol, the search engine holds; the library's completeness is the object of update. |

**Note on the refutation direction.** TS-1, TS-2, TS-3 pin the search
engine's mechanism — property-based selection, no aspirational output,
dim-checked MULTIPLY. All hold. TS-4 is the demo's specific empirical
claim about the desert substrate under the shipped library, and it
fails as-shipped. This is the sim being the witness: the search
correctly reports "no chain closes" rather than papering over the gap
by inferring a `power → heat` bridge that isn't in the library. Fixing
requires an operator to add a phenomenon; the tool refuses to invent
one, exactly as TA-2 (thermo_assume's no-invention claim) requires
across the stack.

## Site-survey claims (`thermo_survey.py`)

Sits ABOVE `thermo_synth`. Where the synthesizer starts from an on-hand
material list, the survey layer starts from physical DOMAINS —
chemistry, pressure, atmosphere, topology, biology, geology, materials,
water, sunlight, wind, weather — and asks the operator to observe each
one. The unifying frame: every domain exposes an AMBIENT GRADIENT
(energy already flowing at no import cost); an UNREAD field is a silent
assumption ("nothing there") that the coverage report makes loud.

Extends `thermo_synth.DIM` with three quantity kinds (`velocity`,
`density`, `g_field`) and `thermo_synth.LIBRARY` with six ambient
phenomena (`gravity_potential`, `wind_kinetic`, `freeze_thaw_split`,
`evaporative_cooling`, `fermentation`, `gravity_feed`). The extension
is idempotent — a duplicate name is a no-op.

Sample: [`samples/thermo_survey.sample.txt`](samples/thermo_survey.sample.txt).

| # | Claim | Refuted if | Verdict |
|---|-------|-----------|---------|
| TSV-1 | `DOMAINS` covers 11 physical fields; each field carries `(name, reads, gradient, unlocks)`. `SiteScan.coverage()` prints `[read]` vs `[UNREAD]` for every field in `DOMAINS`, in the declared order. An unread field is loud — never silently treated as empty. | A field in `DOMAINS` that fails to appear in the coverage report, or a scan reporting "complete" without every unread field flagged. | **HOLDS** — sample lists all 11 domains; 4 read (`geology`, `materials`, `water`, `sunlight`), 7 UNREAD (`chemistry`, `pressure`, `atmosphere`, `topology`, `biology`, `wind`, `weather`) each with their gradient shown. `materials` reads without a gradient tapped — printed as "no gradient tapped", not omitted. |
| TSV-2 | `SiteScan.unlocked()` returns the sorted union of `Domain.unlocks` across read domains. This is CONCEPTUAL availability — a phenomenon appears if any read domain nominally unlocks it, regardless of whether the specific substances present actually let it fire. Execution feasibility is `Synth.paths_to()`, not `unlocked()`. | An unlocked phenomenon whose source domain wasn't read, or a phenomenon left out despite its source domain being read. | **HOLDS** — sample: 4 read domains → 6 unlocked phenomena (`confined_vapor_pressure`, `evaporative_cooling`, `freeze_thaw_split`, `sensible_heating`, `solar_concentration`, `vaporization`). Every one traces back to at least one read domain's `unlocks` list; nothing extra, nothing missing. |
| TSV-3 | Extension of `thermo_synth.LIBRARY` is idempotent: the `for p in AMBIENT: if p.name not in {x.name for x in LIBRARY}: LIBRARY.append(p)` guard prevents duplicate registration on repeat imports. Same-name phenomena from `AMBIENT` never displace existing entries. | Importing `thermo_survey` twice increasing the LIBRARY count beyond the union, or an `AMBIENT` phenomenon overwriting an existing same-named entry. | **HOLDS** — the guard uses a `set` comprehension over existing names. Verified: `import thermo_survey` then `reload(thermo_survey)` leaves `len(LIBRARY)` unchanged past the first import. No overwrite semantics because `append` only fires on name-absence. |
| TSV-4 | Demo footer claim: "the read fields carried enough gradient — sun's flux, water's phase, copper's melting point — to synthesize lift." Under the shipped library extended with ambient phenomena, backward search from `force` on the desert scan produces at least one assembly. | The desert search for `force` returns 0 assemblies after the survey's ambient extension. | **REFUTED (as shipped)** — inherits the TS-4 failure: `power → heat` is still unbridged after the ambient additions. `fermentation` produces `heat` but requires `biomass` (biology UNREAD → not in on-hand). `combustion_heat` needs `fuel` (chemistry UNREAD). `freeze_thaw_split` produces `force` directly but requires `temperature_cycle` (weather UNREAD). No chain closes for `force`. `paths_to("power")` DOES work (`solar_concentration ← flux + area`). Refutation direction — same as TS-4: extend the LIBRARY with a `power → heat` bridge, OR extend the scan (read `chemistry` for fuel → `combustion_heat`, or `biology` for biomass → `fermentation`, or `weather` for temperature_cycle → `freeze_thaw_split`). The tool refuses to invent the missing observation; the operator's next survey pass is where TSV-4 would become true. |

**On the two paired refutations (TS-4 and TSV-4).** They fail for the
SAME reason: a specific quantity-kind conversion that no shipped
phenomenon supports. TS-4 identifies it at the library level (`power`
has no producer chain to `heat`). TSV-4 identifies it at the survey
level (the operator's next unread field — `chemistry`, `biology`, or
`weather` — is exactly what would close the chain via a phenomenon
that IS in the library). Both refutations point in constructive
directions and neither retunes the sim. The pattern is intentional:
the tools name what's missing; the operator supplies the observation
or the phenomenon.

## End-of-life lifecycle-close claims (`thermo_purpose.py`)

Closes the accounting loop past end-of-life. Where `thermo_pm` checks
conservation at BUILD, this layer keeps the ledger open through
serve-fail-return: every kilogram borrowed from the site carries a
return, judged fresh at end-of-life on three independent gates —
**QUANTITY** (returned / borrowed ≥ 0.95), **FORM** (harm debt = 0;
returning matter matches a current need or the ground takes it),
**TIMING** (nothing held past the purpose's return window). Fallback
ladder handles intact-at-EOL substrates: convert-to-serve-a-need,
else reuse, else hold, else HARM.

The tool invents no timing windows, no need magnitudes, no
ground-uptake list, and no conversion ratios — all are operator inputs.

Sample: [`samples/thermo_purpose.sample.txt`](samples/thermo_purpose.sample.txt) (four scenarios).

| # | Claim | Refuted if | Verdict |
|---|-------|-----------|---------|
| TP-1 | Substrates that degrade as intended into forms the ground takes directly close all three gates. Seasonal-shelter (earth 800 + fiber 40 kg, ground takes both) and star-guide college (mineral_dust 5000 + stone 12000 kg, ground takes both, 1000 yr return window) both verdict "feeds the earth without harm". | Either scenario failing any of QUANTITY/FORM/TIMING under the same substrate + need + ground_takes inputs. | **HOLDS** — both scenarios PASS all three gates. site_delta = 0.00 kg each. Verdicts: "feeds the earth without harm". |
| TP-2 | The concrete-slab scenario (rubble 20000 kg, need={}, ground_takes=empty, no matching conversion in DEFAULT_CONVERSIONS) fires the HARM route and fails both QUANTITY and FORM. This is the failure mode the layer exists to make loud: mass closed at build, harm open at end-of-life. | The slab scenario evaluating to any non-HARM route, or failing to trip FORM. | **HOLDS** — one route emitted, `HARM concrete_rubble 20000.0 no need, ground won't take it, not convertible`. QUANTITY FAIL (returned 0 / borrowed 20000), FORM FAIL (harm 20000). Verdict: "return does not close". The delta the layer is designed to name is right there in the report. |
| TP-3 v1 | Burning intact timber to serve a warming need + yielding ash the ground takes is a valid closure of the return — the demo's implicit "one move, serves a need, advances the return" framing. | The migration_lodge scenario failing any gate under conditions the demo names as valid. | **REFUTED (as shipped)** — QUANTITY FAILS on the lodge: `returned 300.0 / borrowed 3000.0 kg` (ratio 0.10, needs ≥ 0.95). Structurally, combustion converts most fuel mass to volatile products that leave the site (CO2, H2O). Only the ash residue (~5%) comes back as recoverable mass. The 95% QUANTITY threshold is incompatible with ANY combustion-based closure by construction. Refutation direction — a design choice, not a retune: (a) relax QUANTITY to accept conversions-that-serve-need at any mass-return ratio, (b) split QUANTITY into "mass returned to site" (strict) + "work done in return" (soft, credited by need satisfaction), or (c) accept the current behavior as saying "combustion loses mass; a closure via combustion is a partial return, honest about it". |
| TP-4 | Accounting correctness: the `returned` scalar equals the sum of mass actually routed through non-HARM outcomes. Held mass is not credited to `returned`; converted output routed to a need or ground is credited exactly once. | `returned` including mass that got HELD, or double-counting mass in a conversion branch. | **REFUTED** — the migration_lodge report shows `returned 300.0` but only 150 kg of ash physically existed (3000 kg timber × 0.05 ratio). The conversion branch increments `returned` twice: once inside `route_returnable` when the ash routes successfully, and again after the loop via `returned += mass * sum(r for f, r in c.gives.items() if f != "heat")`. The same post-loop expression also credits mass that got HELD (route_returnable failure path) — falsely inflating `returned` when nothing was actually returned. Fix direction: remove the post-loop `returned +=` and let `route_returnable` be the single source of truth. Independent of the TP-3 design tension. |
| TP-5 | The three gates fire independently: a scenario can fail one gate while passing the others. TIMING (held > 0) is separate from FORM (harm > 0) which is separate from QUANTITY (returned/borrowed < 0.95). | A scenario in which two gates always flip together, or one gate silently gated by another. | **HOLDS** — evidence across the 4 scenarios: seasonal + college pass all three; slab fails QUANTITY + FORM but PASSES TIMING (held=0 because HARM route consumed the mass, not the HELD route); lodge fails QUANTITY only. Three distinct pass/fail signatures across four scenarios — the gates are independent in practice. |

**On TP-3 and TP-4 together.** They're separate concerns. TP-3 is a
design tension between the QUANTITY threshold and the physics of
combustion; TP-4 is a straight arithmetic bug that over-credits
`returned`. Fixing the bug (TP-4) doesn't resolve the design tension
(TP-3) — even with correct accounting, lodge returns 150/3000 = 5%
and still fails the 95% threshold. Both need operator decisions; the
tool refuses to silently pick either side.

## Value-ontology claims (`thermo_value.py`)

Reads the SAME transaction through two perpendicular lenses —
`token_primary` (counts the pointer) vs `substrate_primary` (counts
the referent: skill, knowledge, time, labor, care) — and reports the
gap between the two readings as the observable. Ripples the same
residue-vs-return posture from the earlier thermo layers into a
value frame, and — because AI defaults to token-primary from training
on prices, revenue, willingness-to-pay — makes the collapsed axis
explicit as a calibration channel.

Ships an is→ought slide detector (flags a descriptive-desire premise
carrying a normative conclusion — a category error, not a verdict on
the desire) and a HARD BOUNDARY: `OUT_OF_SCOPE` lists three interior
verdicts the module refuses to output ("whether a desire is healthy
for a person", "whether a holder is greedy/bad", "whether a token is
morally legitimate"). Named explicitly so the boundary is not silently
crossed.

Sample: [`samples/thermo_value.sample.txt`](samples/thermo_value.sample.txt).

| # | Claim | Refuted if | Verdict |
|---|-------|-----------|---------|
| TV-1 | `reference_integrity(c)` classifies transaction structure into `bound` (substrate delivered AND kind in DELIVERS), `partial` (substrate delivered but kind implies more), `detached` (no substrate delivered, kind in POOL_CLAIM_NO_DELIVERY), or `unclassified`. Reading is from structure only — never from the person's intent. | A wage claim with matching labor delivered classified as anything but `bound`, or a rent claim with no delivery classified as anything but `detached`. | **HOLDS** — sample: framing labor `bound`, rent `detached`, speculation `detached`, elder teaching `bound` (kind=teaching in DELIVERS, delivered 120 units of knowledge/care). |
| TV-2 | The two lenses return DIFFERENT numbers on the same claim; `discrepancy = token_view − substrate_view` is the observable. Detached claims show large positive discrepancy (token high, substrate zero). Bound claims with matched delivery show zero. Untokenized substrate delivery (e.g. unpaid teaching) shows NEGATIVE discrepancy — the frame's asymmetry becomes visible. | Two lenses returning identical values on a detached claim, or the discrepancy on unpaid delivery evaluating to ≥ 0. | **HOLDS** — sample: rent discrepancy +100, speculation +500 (token > substrate); elder teaching −120 (substrate > token, running the other way). The observable behaves as claimed across three regimes. |
| TV-3 | `pool_delta` measures shared-pool flow: detached claims return `+token_amount` (drawn without adding); bound claims return `token − delivered` (≈ 0 when delivery matches claim); over-delivery (elder teaching case) returns negative (added, not drawn — pool receives more than the claim withdraws). | Detached claim returning zero or negative pool_delta, or matched bound claim returning nonzero. | **HOLDS** — sample: framing labor pool_delta 0.0, rent +100, speculation +500, elder teaching −120. Sign carries direction correctly across all four cases. |
| TV-4 | `normative_slide(j)` flags is→ought category errors: a `DESCRIPTIVE` premise (`is_desired`, `willing_to_pay`, `is_priced`, `sells`) with a `NORMATIVE` conclusion (`should_provide`, `should_build`, `is_good`, `deserves_funding`) fires SLIDE FLAGGED. Reads a REASONING MOVE, not a person. Not a verdict on whether the conclusion happens to be true — only on the illegitimate inference structure. | A pair with both premise ∈ DESCRIPTIVE and conclusion ∈ NORMATIVE evaluating to False, or a pair with the same set membership evaluating differently under different runs. | **HOLDS** — sample: 3/3 pairs flagged (`willing_to_pay → should_build`, `is_priced → deserves_funding`, `is_desired → is_good`). Detection is set-membership; deterministic. |
| TV-5 | HARD BOUNDARY: `OUT_OF_SCOPE` enumerates three interior verdicts the module refuses to output. These are named in code as a literal list, not implicit — so the boundary is auditable and any future addition that crosses it is a visible edit, not a silent leak. | Any function in the module returning a value that reads on one of the OUT_OF_SCOPE items (e.g. a `desire_health` metric, a `holder_moral_status` field, a `token_legitimacy` scalar). | **HOLDS** — the module's returned surfaces (`Reading`, `Look`, `bool` for slide detector) carry no interior-verdict fields. Every public function is structural: integrity class, mass value, sign, category-error flag. Nothing scores an intent or a person. |

**On the token-primary default.** TV-2's substrate lens exists as a
calibration channel for the exact frame collapse the module names in
its header: AI trained on prices reads value AT THE POINTER and
collapses the substrate axis silently. TV-3's negative pool_delta on
the unpaid-teaching case is the sharpest teaching-artifact — a
substrate lens sees a positive contribution to the pool; a token lens
reads zero, and can only ever read zero, no matter how well-designed
the pricing. The frames aren't ranked; the module says so explicitly.
The **discrepancy** is the observable, and it's signed.

## Knowledge-provenance claims (`thermo_know.py`)

Codes the axis every earlier layer gestured at: WHAT is claimed, HOW
it was gotten (8 acquisition modes each with `reads_well` / `blind_to`
/ `decays_by` / `stays_fresh_by`), and LINKS between claims (corroborates
/ contradicts, plus `parents` for inference). Corroboration strength is
counted as INDEPENDENCE — two readings through the same mode are echo,
counted separately and weighted zero. Same posture as trowel+LiDAR (both
residue-mode → echo) vs oral tradition + excavation (independent axes →
real corroboration — the Upano case).

Explicit boundary held in code: the tool measures traceability,
independence, staleness, mode-masquerade — it does NOT rank modes as
inherently supreme, and it does NOT rule on truth.

Sample: [`samples/thermo_know.sample.txt`](samples/thermo_know.sample.txt).

| # | Claim | Refuted if | Verdict |
|---|-------|-----------|---------|
| TK-1 | `MODES` encodes 8 acquisition modes (`direct_observation`, `repeated_practice`, `experiment`, `instrument`, `transmission`, `inference`, `authority`, `model_generated`), each with 4 fields naming what it reads well and what it is structurally blind to. No mode is ranked supreme. | A mode missing any of the four fields, or a scalar/ordering emitted by the module that would let an outside caller rank modes as inherently superior. | **HOLDS** — 8 modes, 4 fields each, no ordering. Every entry carries a `blind_to` line so blindness is co-present with strength. `instrument` explicitly names the trowel-reads-residue-not-return blindness from earlier layers; `model_generated` explicitly names token-primary / diesel-assumed / residue-read as its distribution default. |
| TK-2 | `Corpus.support(key)` counts INDEPENDENT modes agreeing (own mode + distinct modes of any corroborator). Same-mode agreement is echo — counted separately in `echoes_same_mode`, weighted zero in `strength`. Corroboration link is bidirectional (either side declaring corroborates counts). | Support strength incremented by a same-mode corroborator, or independence unaffected by adding an already-present mode's corroborator. | **HOLDS** — sample: `bearing_obs` strength=3 across {direct_observation, repeated_practice, instrument} (three distinct modes). `bearing_penetrometer` strength=2 across {instrument, direct_observation}. `bearing_county` alone at strength=1. `floodplain_teaching` strength=2 across {transmission, direct_observation} — the Upano pattern. Every counted mode is distinct; echoes remain at 0 because the demo never adds a same-mode corroborator. |
| TK-3 | `Corpus.audit(current_year)` flags five specific patterns and only those: unknown `how` string, `authority` older than 20 years (age > 20 flagged as decayed), `inference` with no parents (unnamed sources), `inference` whose parent is not in the corpus (chain broken), `transmission` without a lineage `chain`, `model_generated` without corroboration. Does not flag `direct_observation`, `repeated_practice`, `experiment`, `instrument`, or `transmission` with lineage. | The audit firing on a mode/state not in the enumerated flag rules, or failing to fire on one that is (e.g. a 1974 authority going unflagged in a 2026 audit). | **HOLDS** — sample audit output at `current_year=2026`: 3 flags fire on exactly the intended items (`bearing_county` aged 52yr; `ai_span_guess` model-generated uncorroborated; `steam_feasible` inference with `water_latent` parent not in corpus). The 4 well-provenanced items (bearing_obs / bearing_practice / bearing_penetrometer / floodplain_teaching / flood_marks) draw no flags. |
| TK-4 | `contradicted_by` is symmetric: if A declares `contradicts=[B]`, both A and B report the other in their `contradicted_by` list, regardless of which side wrote the link. This lets a claim added later declare a contradiction against an existing claim without editing the existing one. | An asymmetric contradiction: A contradicts B declared, but B's `support()` result omitting A from `contradicted_by`, or vice versa. | **HOLDS** — sample: `bearing_county.contradicts = [bearing_penetrometer]` is the only declared link, yet BOTH `bearing_penetrometer` and `bearing_county` show each other in `contradicted_by`. The symmetric-check code path is: `key in ot.contradicts or o in k.contradicts` — either declaration counts. |
| TK-5 | HARD BOUNDARY: the module's public surfaces (`support()`, `audit()`, `show()`) return only structural quantities — mode names, integer counts, string flag descriptions, contradiction lists. Nothing returns a truth verdict, a mode ranking, or a "believe this" recommendation. The header says so explicitly ("it does not rank modes as inherently superior, and it does not rule on truth"). | Any function in the module returning a field that would rank modes (e.g. `mode_reliability_score`, `truth_probability`, `should_trust`). | **HOLDS** — no such fields on any returned dict. `support()` returns four keys (`independent_modes`, `strength`, `echoes_same_mode`, `contradicted_by`) — all structural. `audit()` returns a list of flag strings naming patterns to fix, no rankings. `show()` prints; returns nothing. |

**On the mode-supremacy failure mode.** Ranking a claim by its
acquisition mode ("this is instrument-derived, therefore better than
that traditional teaching") is the same error the earlier layers audit
in other frames: reading the label on the meter instead of the meter's
properties. TK-1's 4-field mode records make the *blindness of every
mode* co-present with its strength, so an audit reader sees both at
once. TK-2's independence-not-count corroboration is the sharpest
mechanical carrier of that stance: LiDAR + trowel doesn't score higher
than trowel alone, because they share the residue-vs-return blindness.
Living-practice-plus-oral-tradition scores higher than either alone,
because the axes are distinct. The math and the philosophy match.

## Provenance-spine claims (`thermo_spine.py`)

Threads `thermo_know` through the whole stack WITHOUT rewriting the
eight working files. A `Spine` is a registry that attaches alongside:
`tag()` records provenance at entry (value + how + year); `derive()`
records inference chains automatically because a computed result IS
an inference — the chain is built by the act of computing, not by
discipline. `backing()` walks any result to its leaves and returns
a mode census, distinct-mode count, weakest links, and inherited
audit flags. `coverage()` walks a `thermo_pm` System and flags every
resource whose quantity carries no provenance tag — the same "unread
field = silent assumption" move from `thermo_assume` and `thermo_survey`,
now applied to values in flight.

Adds one mode row (flagged as assistant-added, not an operator cut):
`measured_constant` for latent heats, Avogadro-like constants, and
other quantities replicated across independent labs. Its blindness is
explicit — the constant is solid; applicability at THIS site's
conditions is the assumption.

Sample: [`samples/thermo_spine.sample.txt`](samples/thermo_spine.sample.txt).

| # | Claim | Refuted if | Verdict |
|---|-------|-----------|---------|
| TSP-1 | A `derive(key, value, parents=[...])` call records the result as `Know(how="inference", parents=parents)` in the corpus. The chain cannot silently break — a computed result exists with its named parents, or it doesn't exist as a spine entry. `derive` also inspects `parents` at call time and stamps `[MISSING PARENTS: ...]` into the `note` field for any parent key not already in the corpus. | A `derive()` call producing a Know entry with empty `parents`, or missing parents going unrecorded. | **HOLDS** — sample: `audit.waste_delta_J` derived with parents `[plan.code_energy_J, plan.physics_energy_J]`; both parents exist in the corpus, no MISSING PARENTS stamp. The two intermediate plans (`plan.code_energy_J`, `plan.physics_energy_J`) themselves record their parents. Chain closes end-to-end at depth 2, backing traverses cleanly. |
| TSP-2 | `backing(key)` returns leaves + mode census + weakest links. Weakest-link identification fires on three specific conditions: (a) `model_generated` with independence-strength ≤ 1, (b) `authority` with `year` older than 20 years, (c) any leaf with strength ≤ 1 whose mode is NOT in `{measured_constant, direct_observation, repeated_practice}`. Never fires on a leaf that satisfies none of the three. | A leaf flagged as weakest without meeting any of the three conditions, or a leaf meeting a condition that goes unflagged. | **HOLDS** — sample: `audit.waste_delta_J` has 4 leaves. `code.fill_depth_m` fires (authority, 2026-1974=52 > 20 → condition b). The three site/constant leaves don't fire: `site.soil_bearing_kPa` is `instrument` but has strength 2 via corroboration with `site.rig_test`; `site.rig_test` similarly; `const.diesel_J_per_L` is `measured_constant`, in the exempt set even at strength 1. Exactly one weakest link surfaced — matches the design. |
| TSP-3 | `coverage(sys=None)` returns two categories of flag concatenated: (1) resources in the passed `thermo_pm` System whose names don't appear anywhere in the corpus as a tagged value; (2) every flag `corpus.audit()` would return on its own. When `sys is None`, only the audit half runs — the coverage half is skipped, not defaulted. | Coverage swallowing a System resource that has no matching tag, or coverage emitting audit flags when the underlying `audit()` returns none. | **HOLDS** — sample runs `sp.coverage()` with no System, so only the audit half fires: 2 flags emitted (`code.fill_depth_m` aged authority, `model.span_guess_m` model-generated uncorroborated). Both match what `thermo_know.Corpus.audit()` would return on this corpus standalone. |
| TSP-4 | Weakest-link inheritance: audit flags on ANY node in the parents-tree of a result surface in `Backing.flags`. A result's groundedness is bounded by the least-supported node in its transitive parent set, not just its direct parents. | An audit flag on an intermediate node (parent of a parent) failing to surface in the top-level result's `Backing.flags`, or a flag on an unrelated node leaking in. | **HOLDS** — sample: the `[code.fill_depth_m]` authority-aged flag is a DIRECT-parent flag (code.fill_depth_m is a direct parent of plan.code_energy_J, which is a direct parent of audit.waste_delta_J), and it surfaces on the top-level report as expected. `model.span_guess_m` is uncorroborated but is NOT in the parents tree of `audit.waste_delta_J` — its flag appears in `coverage()` output but NOT in `audit.waste_delta_J`'s `Backing.flags`. Scope of inheritance matches the transitive-parent tree exactly. |
| TSP-5 | HARD BOUNDARY: the spine adds one mode row (`measured_constant`) as an assistant-added bookkeeping cut, explicitly documented in the docstring as "flagged as mine". The row's blindness is real and stated: constants are solid across labs, but applicability at a specific site's temperature / pressure / purity is the operator's call. No other mode is added or reordered; the cultural cuts of the mode table remain the operator's. The spine also does NOT modify the eight working files — it is a registry that attaches alongside them. | Additional modes added silently, existing modes reordered or edited, or spine code monkeypatching another module's globals beyond the documented `MODES["measured_constant"]` entry. | **HOLDS** — one mode addition guarded by `if "measured_constant" not in MODES`, docstring explicitly names it as assistant-added with rationale. All other modules unchanged; the spine reads `thermo_pm.System` via duck-typed `sys.resources` iteration in `coverage()` and mutates nothing. Idempotent (guarded add) and non-invasive (no writes back into other modules' state). |

**Weakest link becomes visible at the point of use.** The whole spine
is a mechanical rewrite of a discipline claim from the earlier layers.
Before, an operator had to trace the headline number back through three
files to find that the 24800 J waste-delta rested on a 52-year-old
authority with no basis on file. Now the report at `audit.waste_delta_J`
prints that authority's flag directly — the weakest link is co-present
with the answer, not buried upstream. Same 24800 J; different visibility
of what it rests on.

## Information-taxonomy claims (`info_taxonomy.py`)

Domain-neutral generalization of `thermo_know` + `thermo_spine`. Names
six axes and gives each an operational surface: faceted TYPE (content +
form + open "about"), acquisition MODE (extensible table with
blindness/decay/freshness as data), SOURCE track record (held separate
from claim support — the Admiralty split, kept split), independence-only
SUPPORT counting, per-mode STALENESS via half-life, and PROV-JSON export
of chains. The header explicitly diagnoses what the existing landscape
does well and what it drops:

- epistemology names modes, no operations
- GRADE / evidence-pyramid ranks modes (mode supremacy)
- Admiralty grades source, not the mode's structural blindness
- W3C PROV records THAT a derivation happened, no theory of blindness
- library science: categorization only

Sample: [`samples/info_taxonomy.sample.txt`](samples/info_taxonomy.sample.txt) (four domains — soil / siting / medicine / structure — one structure).

| # | Claim | Refuted if | Verdict |
|---|-------|-----------|---------|
| IT-1 | TYPE is FACETED, not a tree: `content` (from a controlled vocabulary of 9 kinds) × `form` (7 kinds) × `about` (open domain tags). Any item names all three independently — a `teaching / oral` item and a `measurement / instrument_trace` item are both first-class, differing on both cross-cutting facets. | An item forced to declare a parent-type before naming form and content, or `content` and `form` collapsed into one dimension. | **HOLDS** — sample: seven items across four domains, each declaring `content/form` independently. `siting.bench` = `teaching/oral`, `siting.silt` = `observation/text`, `soil.penetrometer` = `measurement/instrument_trace`, `plan.waste` = `claim/numeric`. No tree; no forced parent. |
| IT-2 | MODES table is extensible via `register_mode(m)`, and every entry must fill `reads_well`, `blind_to`, `decays_by`, `stays_fresh_by`. A mode you cannot state the blindness of is not admitted. The nine bootstrap modes ship with all four fields; two carry an explicit `half_life_yr` (`authority=20`, `model_generated=3`). No mode is marked supreme. | A mode registered without one of the four required fields, or the table exposing an ordering / rank scalar over modes. | **HOLDS** — dataclass forces the four required fields at construction; the nine bootstrap modes all fill them. `register_mode(m)` is the only entry path. No `rank` / `priority` / `authority_score` field on `Mode` — modes are structurally peers. |
| IT-3 | SOURCE and SUPPORT are held on separate axes. `Source.reliability()` is a fraction over the source's past track record; it is NOT combined with `Corpus.support(key)` into a single scalar. Sources with no track return `None` — "unknown", never "bad", never a default 0.0. | A function returning a combined source×support scalar, or `Source.reliability()` defaulting a no-track source to zero. | **HOLDS** — sample: `assistant_model` returns "no track yet" (None), never confused with a low reliability score. `operator` shows 1.00 across a 4-item track; `county_office` shows 0.50 across a 2-item track. Neither is multiplied into `support()` output. |
| IT-4 | SUPPORT counts INDEPENDENT modes: `Corpus.support(key)["strength"]` = number of distinct acquisition modes across all corroborators (including the item's own). `echoes` counts same-mode corroborators separately and receives zero weight in strength. | Strength incremented by a same-mode corroborator, or echoes leaking into the strength count. | **HOLDS** — sample: `soil.bearing` (direct_observation) corroborated by `soil.penetrometer` (instrument) → strength=2, echoes=0. `siting.bench` (transmission) corroborated by `siting.silt` (direct_observation) → strength=2, echoes=0. `med.aspirin` (authority) uncorroborated → strength=1. |
| IT-5 | STALENESS is per-mode, using each mode's declared `half_life_yr`. A mode with `half_life_yr=None` (direct_observation, repeated_practice, etc.) is never flagged stale by age; a mode with a half-life is flagged when `current_year − max(refreshed, year) > half_life_yr`. The `refreshed` field lets an item declare its last re-check independent of first-issue year. | Staleness firing on a `half_life_yr=None` mode, or an item's `refreshed` timestamp failing to reset the age window. | **HOLDS** — sample: `med.aspirin` (authority, half-life 20 yr, issued 1998, no refresh, current 2026) → aged 28yr > 20yr → flagged. `model.span` (model_generated, half-life 3 yr, year 2026) → age 0, not flagged by staleness (uncorroborated flag fires separately). Nothing else flagged stale — `direct_observation`, `instrument`, `transmission` items have `half_life_yr=None` in the mode table and stay clear regardless of age. |
| IT-6 | Corpus exports a minimal PROV-JSON-shaped dict: `entity` (labels + mode + year), `agent` (source kind), `wasAttributedTo` (item → source edges), `wasDerivedFrom` (item → parent edges). Chain records that would exist in W3C PROV exist here identically. | An export shape that misses one of the four PROV keys, or a `derived_from` link failing to appear as a `wasDerivedFrom` entry. | **HOLDS** — sample: 2 derivation edges emitted (matching `plan.waste.derived_from = [soil.bearing, soil.penetrometer]`). All four PROV keys present. Existing PROV tooling can consume the dict without translation. |
| IT-7 | HARD BOUNDARY: `audit()` returns structural flag strings only (missing lineage, broken chain, uncorroborated model output, echo chamber, staleness by half-life, contradicted-by). Contradictions are SURFACED but never auto-resolved. No verdict on whether a claim is TRUE; no interior verdict on a knower. | `audit()` returning a truth verdict, a resolution of a contradiction, or a scalar over a knower's honesty. | **HOLDS** — sample audit fires exactly two flags: `[med.aspirin]` stale-authority; `[model.span]` model uncorroborated. Neither is a truth verdict — both name structural conditions. Contradictions in the demo corpus: zero (no `contradicts` links declared), so no held-open notices. When they exist, the audit says "held open, not auto-resolved" verbatim. |

**On the six axes as a spine for the family.** `info_taxonomy` is the
domain-neutral generalization of `thermo_know` (which was already 8
modes + support + audit) plus the source-track-record split from
Admiralty and the PROV export from W3C. The thermo family's specific
cuts (measured_constant added by thermo_spine, coverage() flagging
untagged System resources) remain in the thermo layer where they're
tied to physics. The taxonomy here is what to use when the domain is
NOT physics — a medical rule, a family teaching, a legal precedent —
and the same six axes still name the shape.

## Revalidation-plan claims (`revalidate.py`)

Extends `info_taxonomy` past the single-flag response of `staleness()`.
A `staleness` flag implies one action (retest everything). Decay is not
one thing, and the retest a decayed claim actually needs is often much
cheaper — or none, or impossible. Diagnoses along FIVE axes, each
naming a distinct failure mode, and routes to one of five outcomes.

Five axes:
```
temporal_scope         does the referent MOVE? age is not decay
scope                  established range vs current use conditions
methodology            mode sound / superseded / structurally blind
updated_info           corroboration or contradiction since acquisition
physical_authenticity  can ground truth settle it, and how cheaply
```

Five outcomes: `undecidable` (unfalsifiable), `re_establish` (unrecorded
scope or unregistered method), `none` (static referent or already
corroborated), `directed` (contradicted — aim at the contradiction),
`cheap` (direct physical check available).

Sample: [`samples/revalidate.sample.txt`](samples/revalidate.sample.txt) (five decayed-looking claims, five different plans).

| # | Claim | Refuted if | Verdict |
|---|-------|-----------|---------|
| RV-1 | `VOLATILITY_YR` and mode `half_life_yr` govern staleness INDEPENDENTLY. A `static` referent under `measured_constant` at any age produces a `STATIC` temporal_scope finding and PLAN `none` (age-based staleness is spurious). A `seasonal` referent under `direct_observation` at age > 0.5 yr produces `EXPIRED` regardless of the mode's half-life (which is `None` for direct_observation). | A static-referent claim's staleness flag driving a nonzero-cost plan, or a seasonal-referent claim at age 1 yr going unflagged as EXPIRED. | **HOLDS** — sample: `const.latent_vap` (1953, measured_constant, static) → temporal_scope STATIC, PLAN `NONE` (zero cost). `site.moisture` (2025, direct_observation, seasonal, scale 0.5 yr) → temporal_scope EXPIRED at age 1 yr, PLAN `CHEAP` (hand test at depth). Two claims, opposite verdicts on temporal_scope, driven by volatility rather than mode half-life alone. |
| RV-2 | `scope` axis distinguishes DRIFTED (established range ≠ applied range) from in-scope. A drifted claim routes to "extend the range at current conditions", explicitly narrower than full re-establishment. When `established_over` is `None` or unrecorded, the axis fires `UNRECORDED` and the plan escalates to `re_establish` (a claim with no stated range cannot be shown in-range). | A drifted claim getting a `none` plan, or an unrecorded scope claim getting anything less severe than `re_establish`. | **HOLDS** — sample: `code.fill_depth` established over 1974 conditions, applied to 2026 → scope DRIFTED, plan uses direct check (penetrometer) which the notes explicitly says "extends the range and refreshes in one move". `claim.vibes` has no `established_over` recorded → scope UNRECORDED, plan `UNDECIDABLE` (a higher escalation because `physical_authenticity=UNFALSIFIABLE` overrides). |
| RV-3 | `updated_info` reads the corpus's own `corroborates` / `contradicts` links to short-circuit needless retests. If independent modes have corroborated the claim since acquisition AND temporal_scope is not EXPIRED AND scope is not DRIFTED, plan is `none` with the note "record the corroborating item as the refresh". A contradiction always overrides corroboration and routes to `directed`. | A corroborated claim (independent mode, no expiry, no drift) yielding a nonzero-cost plan, or a contradicted claim escaping the `directed` route. | **HOLDS** — sample: `siting.bench` (transmission) corroborated by `siting.silt` (direct_observation, distinct mode) → updated_info CORROBORATED → PLAN `NONE`. `code.fill_depth` contradicted by `site.penetrometer` → updated_info CONTRADICTED → PLAN `DIRECTED`, method = the physical check when available, else `mode.stays_fresh_by`. |
| RV-4 | `physical_authenticity=UNFALSIFIABLE` overrides every other axis: a claim not checkable against ground truth as stated routes to `undecidable`, method "restate or retire". No amount of retest resolves an unfalsifiable claim, so the plan says so and terminates rather than escalating to `re_establish`. | An unfalsifiable claim routed to any outcome other than `undecidable`, or to a method other than "restate or retire". | **HOLDS** — sample: `claim.vibes` (`checkable=False`) → PLAN `UNDECIDABLE` verbatim, cost `n/a`, method "restate or retire". Note: "no check could fail — retesting cannot resolve it". Even with other axes fired (UNRECORDED × 2), the unfalsifiability short-circuits. |
| RV-5 | BOUNDARY: `revalidate` outputs a retest PLAN (a trajectory), NOT a new verdict on the claim. It does not re-decide truth, does not auto-refresh, and does not judge whether a mode is *fit* for the claim. Where fit requires reading meaning (does the mode's blindness touch what this claim asserts?), the `methodology` axis prints the blindness verbatim and hands the judgment to the operator with `-> operator judges whether that blindness touches what this claim asserts`. | A `Plan` field containing a new truth value, an auto-refresh side-effect on the corpus, or a mode-fit scoring function. | **HOLDS** — `retest_plan()` returns a `Plan` with `outcome / method / cost / notes` — all trajectory data, none of it a re-verdict. `report()` prints; mutates nothing. `methodology` axis in every case says `review` and prints the mode's `blind_to` field, letting the operator decide fit. Sample line: `mode 'authority' is blind to: everything since issue; the issuer's own basis -> operator judges whether that blindness touches what this claim asserts`. |

**On the five-outcome routing.** The design premise is a rebuttal to
"stale means retest": five decayed-looking claims produce five
distinct plans in the sample — no retest / directed cheap check /
straight retest / no retest / retire. The mode table already carried
the prescription in `stays_fresh_by`; the axes only decide WHICH
mode's freshness path to follow, or which alternative (physical
check, corroboration record, retirement) supersedes it. Same posture
as the rest of the family: name the failure precisely, then route
to the cheapest sufficient action.

## Nomenclatural-scaffold claims (`scaffold.py`)

Ports Linnaeus's durable contribution — the CODE (stable names, type
specimens, priority rules, defined revision procedure), not the tree —
to claim scope. Information has no single natural joint (type, mode,
source and support are orthogonal), but one axis genuinely NESTS: scope
of applicability. Five ranks, strict ladder:

```
occasion  < instance < class < regime < universal
```

Every claim carries: anchors (type specimens — the concrete
observations it's pinned to), volatility class, `as_of` timestamp,
and optional stated conditions. Freshness is computed via clock
substitution: `due(key)` returns arithmetic against `(now, as_of,
volatility)` because a reasoner without continuous duration cannot
NOTICE staleness — noticing requires having been present while a thing
aged. Promotion is eligibility only, never automatic. Demotion (from
counterexample) reduces rank; the claim isn't refuted, its SCOPE was
overstated.

Sample: [`samples/scaffold.sample.txt`](samples/scaffold.sample.txt) (four claims at four ranks, four different verdicts).

| # | Claim | Refuted if | Verdict |
|---|-------|-----------|---------|
| SC-1 | `RANKS` is a strict 5-tier ladder ordered by scope: `occasion < instance < class < regime < universal`. `PROMOTION_RULE` names monotone thresholds — each higher rank requires ≥ the previous rank's minimum distinct anchors and modes. No mid-tier admitted. | Any promotion rule violating monotone-in-threshold, or a rank name accepted outside the ladder. | **HOLDS** — `PROMOTION_RULE` thresholds: instance (1,1), class (3,2), regime (5,3), universal (8,3). Monotone in anchors, non-decreasing in modes. All five ranks have a `RANK_MEANING` entry. `promotion()` uses `RANKS.index()` and refuses out-of-ladder ranks by KeyError. |
| SC-2 | Anchors are TYPE SPECIMENS — the concrete observations a claim is pinned to. Every anchor has `(key, where, mode, as_of)`. A claim with `anchors=[]` prints `! no type specimen -- cannot be re-checked, only re-argued` verbatim on report. Anchor `where` counts distinct sites; anchor `mode` counts distinct acquisition modes (the independence rule inherited from info_taxonomy IT-4). | An anchorless claim reporting normally with no "cannot be re-checked" warning, or duplicate `where` values inflating the anchor-site count. | **HOLDS** — sample: `fill.required` has `anchors=[]` → prints the warning verbatim. `latent.vap.water` has 4 anchors across 4 distinct sites {field kettle, lab A, lab B, lab C} and 3 distinct modes {experiment, instrument, direct_observation}. `promotion()` uses `{a.where for a in s.anchors}` and `{a.mode for a in s.anchors}` — sets, not lists — so duplicates cannot inflate counts. |
| SC-3 | Clock substitution: `due(key)` returns arithmetic against `(now, as_of, volatility)`, never a felt-elapsed signal. Five statuses cover all input combinations: `UNRECORDED` (no volatility class), `UNDATED` (no as_of), `no_expiry` (volatility=static), `current` (elapsed ≤ scale), `DUE` (elapsed > scale). A `static` claim at any age returns `no_expiry`; a `seasonal` claim past its scale returns `DUE` even at young absolute age. | A `due()` call inferring staleness without arithmetic on the recorded fields, or a static claim reporting DUE at any age. | **HOLDS** — sample: `latent.vap.water` (static, 1953, 73 yr old) → `no_expiry`. `clay.sand.firms` (slow, 2019, 7.5 yr) → `current`. `soil.moisture.ok` (seasonal, 2025.8, 0.7 yr elapsed vs 0.5 yr scale) → **DUE** even though the claim is under a year old. `fill.required` (slow, 1974, 52.5 yr vs 50 yr scale) → **DUE** by 2.5 yr past scale. |
| SC-4 | Promotion is ELIGIBILITY only. `promotion(key)` returns `{eligible, target, have, missing}` — a report, not an action. Eligibility requires (a) `≥ need_anchors` distinct sites, (b) `≥ need_modes` independent modes, (c) `stated_conditions` present at target `regime` or `universal` ("an unbounded universal claim cannot be falsified"), (d) no open counterexamples. `Register` never rewrites the claim's rank; the operator does. | A `promotion()` result mutating the claim's rank, or eligibility firing with missing stated_conditions at regime or above, or eligibility firing with open counterexamples. | **HOLDS** — sample: `clay.sand.firms` at rank instance, 3 anchors × 3 modes → eligible for `class` (target thresholds 3, 2). No side effect on the Scoped item's rank; it stays `instance` until the operator re-registers it. `fill.required` fails eligibility not just for missing anchors but also because open counterexamples nullify eligibility regardless of other axes. `latent.vap.water` at `universal` returns `not yet` because there IS no higher rank (`RANKS[-1]`). |
| SC-5 | Demotion routes a claim with `counterexamples` to the widest rank its remaining anchors support. `demotion(key)` returns `{required, from, to, because, note: "the claim is not refuted -- its SCOPE was overstated"}`. The distinction is load-bearing: a refutation would retire the claim entirely; a demotion preserves it at the scope where the anchors still hold. `demotion` also never mutates the Scoped item — reports required action to the operator. | A demoted claim treated as refuted (retired), or a demotion crossing more than one rank per counterexample when anchors would support intermediate ranks, or `demotion()` silently editing the claim's rank field. | **HOLDS** — sample: `fill.required` (regime, 0 anchors, 1 counterexample) → demotion required from regime → occasion (widest rank surviving with 0 distinct sites). Note printed verbatim: "the claim is not refuted -- its SCOPE was overstated". The claim's rank in the Scoped object remains `regime` after `demotion()` returns; the caller edits it or doesn't. |
| SC-6 | BOUNDARY: neither promotion nor demotion mutates the `Scoped` item's rank. `Register.report(key)` prints eligibility and required actions. The corpus itself has zero side-effects from these calls. Widening a claim's scope is an act with consequences and belongs to the operator; demotion belongs to the operator too, and the tool refuses to silently rewrite either. | Any code path in `Register` that assigns to `Scoped.rank`, or auto-registers a promotion/demotion in the corpus after `promotion()` / `demotion()` returns. | **HOLDS** — the two methods return dicts. `Scoped` is a `@dataclass` and its `rank` field is never touched by any spine code. The operator's re-registration is the only way to update a scope claim. Same posture as the rest of the family: report and hand off, never auto-execute. |

**On the type-specimen anchor.** The single mechanism that carries the
whole scaffold is Anchor. A claim with anchors can be re-checked
against them; a claim without anchors can only be re-argued. The
promotion rule is a distinct-anchors + distinct-modes count on the
same object; the demotion rule is a distinct-anchors count at
survival ranks; the freshness clock is elapsed against `as_of`, which
lives on the anchors' issuing observations. Every axis routes through
the anchors — which is exactly Linnaeus's contribution: name the
specimen, then everything else is arithmetic against it.

## Decay-registry claims (`clock.py`)

**v1 retired to `legacy/clock_v1.py`.** v1 had ONE decay term:
elapsed calendar time — the mode-supremacy move performed on clocks.
v2 registers **six decay channels** distributed across **three
targets**, with a hard rule against taking min across targets.

Six channels, each with `measures` / `blind_to` / `fn`:

| channel | target | reads |
|---------|--------|-------|
| `time` | claim | calendar aging vs mode half-life / referent volatility (faster wins) |
| `disuse` | mode_sensitivity | observer out of practice |
| `use` | claim | retrievals × per-retrieval fidelity (retrieval rewrites the record) |
| `constancy` | mode_sensitivity | adaptation to unchanging stimulus |
| `transmission` | claim | chain hops × per-hop fidelity (Eigen error threshold) |
| `diffusion` | independence | independence itself decaying via field mixing |

Three targets, decayed WITHIN each target only: `claim` (content less
likely to hold), `mode_sensitivity` (reader can still be right and
report nothing), `independence` (content fine, support count no
longer honest).

`Observation` dataclass carries all inputs; `decay(o)` returns
per-channel readings + per-target governing channel + per-target
band. The v1 API — `freshness(as_of, now, ...)` — is preserved
verbatim as a time-channel-only shortcut so `echo.py` and any other
v1 caller works unchanged.

Sample: [`samples/clock.sample.txt`](samples/clock.sample.txt) (channel table + three-target demo + Eigen threshold + v1 backward-compat + registration guards).

| # | Claim | Refuted if | Verdict |
|---|-------|-----------|---------|
| CL-1 | Six channels register on module import; every row has non-empty `measures` and `blind_to`. `register_decay_channel()` RAISES `ValueError` on empty either field, with the message "a decay channel that will not state what it cannot see is a supremacy claim wearing a row". Also raises when `target` is outside `TARGETS = ("claim", "mode_sensitivity", "independence")`. | An empty-field channel registering, or a channel with an unrecognized target registering. | **HOLDS** — 6 channels shipped, all fields populated. Sample verifies both guards raise: empty `blind_to` → `ValueError: channel 'bad': blind_to is empty -- ...`; target `'bogus_target'` → `ValueError: channel 'bad': target must be one of ('claim', 'mode_sensitivity', 'independence')`. |
| CL-2 | `decay(o)` computes readings for every registered channel. Governing channel per target is the FASTEST (min `remaining`) channel WHOSE TARGET IS THAT TARGET. No cross-target minimization. If no channel for a target is computable (all return `None`), that target's band is `UNDETERMINED` with a LOUD flag. | A per-target governing channel drawn from a different target, or a min across all channels blurring the three-target split. | **HOLDS** — sample: single Observation yields three distinct governing channels — `claim` governed by `time` (0.3533, DECAYING); `mode_sensitivity` governed by `disuse` (0.9995, FRESH); `independence` governed by `diffusion` (0.0063, EXPIRED). The point of the design: claim / mode / support decay on separate ledgers with separate consequences. |
| CL-3 | `time` channel: `effective_half_life(mode_hl, volatility)` picks `min(candidates)` — mode half-life and referent volatility never average. Missing either → still returns the other. Missing both → returns `(None, "undetermined", loud)`. | A combined half-life value that's between the two clocks (indicating averaging). | **HOLDS** — unchanged from v1 CL-1. Sample: 30-yr authority claim (mode 7300d) under regime volatility (referent 1825d) picks 1825d as governing time-channel half-life. Verified in the three-target demo: `time` reports remaining=0.3533 = 2^(-30·365/1825). |
| CL-4 | `use` channel: `f ** retrievals` where `f` = `retrieval_fidelity`. Handles `retrievals=0` (returns 1.0). Handles `retrievals` unrecorded → returns `None` with LOUD. Handles `f` outside `(0, 1]` → returns `None` with LOUD. Dominant for oral / testimonial anchors; inert for instrumented ones (which have no retrieval count). | A `use` value greater than 1 (fidelity should never amplify), or a channel accepting `f > 1` without loud-flagging. | **HOLDS** — sample: 100 retrievals × 0.99 fidelity = 0.99^100 = 0.366, DECAYING. The `use` channel's `blind_to` note verbatim: "elapsed time -- an untouched record scores perfect here at any age". |
| CL-5 | `transmission` channel: `f ** chain_hops`. `max_chain_hops(hop_fidelity, floor=0.35)` returns `log(floor)/log(f)` — the Eigen error threshold, chain depth past which content is not maintained. Undefined outside `0 < f < 1`. | A `max_chain_hops` value where `hop_fidelity ** result != floor` (arithmetic bug), or a result returned for `f >= 1` (would be infinity or negative). | **HOLDS** — sample: hf=0.99 → 104.5 hops to 0.35 floor. hf=0.95 → 20.5 hops. hf=0.9 → 10.0 hops (exact: log(0.35)/log(0.9) = 10.0). hf=0.8 → 4.7 hops. Verified: 0.9^10.0 = 0.348, matches the 0.35 floor within rounding. The docstring notes: bounds chain DEPTH; data processing inequality bounds support WIDTH — same graph, different limit. |
| CL-6 | Backward compatibility: v1's `freshness(as_of, now, mode_half_life_days, volatility)` is preserved with the same `Freshness` dataclass shape (9 fields including `governing_clock`, `half_lives_elapsed`, `band`, `loud`). Callers holding no additional inputs — like `echo.py`'s `retest_queue()` — work unchanged. | The v1 `Freshness` shape being altered, or `freshness()` returning something other than a time-channel-only reading. | **HOLDS** — sample: `freshness('2019-01-01', '2026-06-30', None, 'structural')` returns band=FRESH remaining=0.8123 clock='referent'. `echo.py` imports `freshness` and runs without modification. `Freshness` dataclass field-count and names identical to v1. |
| CL-7 | SEAM STATUS (inherited from v1 CL-6): `scaffold.py` and `revalidate.py` still carry private `VOLATILITY_YR` dicts and decay math. Neither imports `clock.py` yet. The v2 six-channel model gives them more surface to migrate to, but also raises the migration cost — the refactor now decides not just which clock to call but which of six channels each caller's decay question maps to. | Someone claiming the ecosystem uses `clock.py` as the single source of decay arithmetic. | **REFUTED (pending refactor, wider scope now)** — grep confirms `VOLATILITY_YR` still present in both `scaffold.py` and `revalidate.py`. The v2 module makes the refactor MORE useful (six channels, three targets) but also more design-y — a single `scaffold.Anchor` might have anchors that should decay on `time` (calendar-anchored measurements) and others that should decay on `transmission` (oral chains). The operator's call, not a mechanical rewrite. |

**On the three-target commitment.** The sample's headline demonstration
is that ONE observation of a 30-year-old elder-taught claim produces
THREE independent bands: claim=DECAYING, mode_sensitivity=FRESH,
independence=EXPIRED. That's the design's whole point. Each band has a
different consequence: the claim needs re-checking (time), the elder
does not need re-training (mode_sensitivity), the independence count
needs recomputing (diffusion). Rolling any of these into a single
freshness scalar would erase the information that's the actual output.

## Mode-harness claims (`modes.py`)

Ships **zero rows**. Mode is an Umwelt — its `blind_to` is not a
deficiency to apologize for, it is the shape of the world that mode
inhabits. `reads_well` and `blind_to` are two ends of one sensitivity
curve, not a pro/con list.

**v1 and v2 retired to `legacy/`.** v1 (scalar fields, token-overlap
heuristic) → `modes_v1.py`. v2 (`List[str]` fields + `resolve_clock()`
but only ONE decay channel) → `modes_v2.py`. See `legacy/README.md` for
retirement rationale on each.

**v3 rebuild against clock.py's six-channel decay registry.** Two
major additions:

1. **Signal-detection split.** `reads_well` / `blind_to` describe
   SENSITIVITY (d'); `criterion` (new required field) describes BIAS
   — which way the mode errs when uncertain. Independent axes; a
   table that records only sensitivity reads bias as sensitivity
   failure. Never flattened into one number.

2. **Per-channel parameter or explicit NA.** Six per-channel fields
   on `Mode` (one per clock.CHANNELS entry). Every channel is either
   parameterized OR listed in `channels_na` with a REASON. Silence
   (neither) fires a LOUD flag naming the target that will read
   UNDETERMINED. "n/a" alone is not a reason.

Clock integration is via `to_observation(mode_name, now, **facts)` +
`read(mode_name, now, **facts) → clock.Decay`. Mode supplies its own
decay parameters; caller supplies claim-specific facts; anything
neither supplies stays `None` and goes LOUD downstream. Never defaults.

Sample: [`samples/modes.sample.txt`](samples/modes.sample.txt) (7 registration attempts covering every branch, `read()` end-to-end on two modes, table audit with degeneracy detection).

| # | Claim | Refuted if | Verdict |
|---|-------|-----------|---------|
| MH-1 | `register_mode(m)` RAISES `IncompleteMode` on any of the FIVE required fields being empty: `reads_well`, `blind_to`, `decays_by`, `stays_fresh_by`, `criterion` (new). Message quotes "sensitivity without criterion reads bias as blindness" — the signal-detection separation held explicitly. | An empty required field registering silently, or the message omitting the sensitivity/criterion split. | **HOLDS** — sample: `register_mode(Mode(name='no_bias', ..., criterion=''))` raises `IncompleteMode: mode 'no_bias': criterion is empty. A row must state all five to register. reads_well without blind_to is a supremacy claim; sensitivity without criterion reads bias as blindness.` Message verbatim. |
| MH-2 | Per-channel state (six of them): PARAMETERIZED (attribute set to a value), DECLARED NA (in `channels_na` with a non-empty reason), or SILENT. Silence fires LOUD naming the channel and the target that will read UNDETERMINED. Parameterized-AND-NA on the same channel fires LOUD "one of the two is wrong". Empty-string NA reason fires LOUD "inapplicability is a claim and needs one". `time` is special-cased: covered by `tracks` if set. | A parameterized channel silently overriding an NA declaration, or a silent channel not naming which target it leaves UNDETERMINED, or an "n/a" empty reason passing without flag. | **HOLDS** — sample: `penetrometer` parameterizes time via `mode_half_life_days=5·365`, declares 5 channels NA with reasons → zero loud. `elder_teaching` parameterizes use / transmission / disuse, declares 3 channels NA with reasons → zero loud. `half_finished` parameterizes only time → 5 LOUD flags for the 5 silent channels, each naming its target ("target 'claim' will read UNDETERMINED"). `contradicts_itself` fires "channel 'time': parameterized AND declared not-applicable -- one of the two is wrong". |
| MH-3 | `to_observation(mode_name, now, **claim_facts)` copies mode's per-channel decay parameters onto a `clock.Observation`, then applies caller-supplied claim facts (as_of, retrievals, chain_hops, etc). The mode supplies parameters; the caller supplies facts. Never defaults; unset stays `None`. Unknown mode → returns Observation with only the caller-supplied facts (missing decay params surface as clock LOUDs). | `to_observation()` filling a `None` field with a default value, or mode parameters silently overriding caller-supplied claim facts. | **HOLDS** — sample: `read('penetrometer', now='2026-06-30', as_of='2023-06-30', volatility='regime')` → time channel gets mode_half_life=1825 (from mode) + as_of='2023-06-30' + volatility='regime' (from caller). Time decays cleanly; other 5 channels report UNDETERMINED because their parameters are None (declared NA). NA reasons surface as LOUDs in the `Decay.loud` list, verbatim. |
| MH-4 | `read(mode_name, now, **facts)` returns `clock.Decay` — the full 6-channel × 3-target reading. Governing channel is per-target (MH-3 semantics inherited from clock CL-2). NA reasons are appended to the returned `Decay.loud` list so a caller sees WHY a target is UNDETERMINED, not just that it is. | `read()` returning a decay reading that mutates the mode table, or NA reasons being silently swallowed. | **HOLDS** — sample: `read('elder_teaching', now, retrievals=100, chain_hops=3, ...)` returns three-target reading: `claim` STALE via `use` (0.99^100 = 0.36 wait actually 0.98^100... let me check output... `use rem=0.1326` which is 0.98^100 = 0.132 ✓); `mode_sensitivity` FRESH via `disuse` (0.9973); `independence` UNDETERMINED (diffusion NA). Three-target routing preserved end-to-end. |
| MH-5 | `audit()` returns a flat `List[str]` with FIVE checks: (a) per-channel across-table coverage — which modes are silent on which channels; (b) unprovenanced rows; (c) modes missing `criterion` (bias unstated); (d) declared-blind-read-by-none set difference; (e) DEGENERACY vs REDUNDANCY on pairs with identical `reads_well` — different `blind_to` = degenerate (adds robustness), identical `blind_to` = redundant (adds coverage but not robustness). | An audit that lumps degenerate and redundant together, or misses the criterion-unstated check, or reports pair-level identity where none exists. | **HOLDS** — sample: audit reports 5 channels unstated in `half_finished`; 8 blindnesses read by no mode; and `twin_a / twin_b: identical reads_well -- degenerate (different blind_to: adds robustness)`. Verified: twin_a's blind_to = "A specific blind" ≠ twin_b's "A DIFFERENT specific blind", so the pair adds robustness (a real one-then-the-other coverage), not just doubles the same view. |
| MH-6 | BOUNDARY: `MODES` starts empty; `import modes` leaves it empty. No `__main__` block. `to_observation()` and `read()` return NEW objects — never mutate the mode table. The audit is read-only. No implicit clock (mode inherits `import clock` but never calls a date function; `now` is always caller-supplied). | `MODES` populated on import, or `read()` mutating a mode row, or an implicit `datetime.now()` anywhere. | **HOLDS** — `python3 -c "import modes; print(len(modes.MODES))"` returns `0`. Trailing template is a comment. `to_observation` constructs a new `clock.Observation`; `read` calls `clock.decay` which returns a new `Decay`. No mutation of `MODES` anywhere outside `register_mode`. `grep "datetime.now\|date.today" modes.py` returns 0. |

**On the v2 → v3 delta.** v2 was written when `clock.py` had one
decay channel. When clock v2 shipped six channels + three targets,
v2 modes rows became silently under-specified for five of them: any
claim held by a v2 mode reports UNDETERMINED across five of six
decay targets. v3 forces the operator to state ALL SIX channels
(parameterize or declare NA with a reason) — silence is exactly
what the audit hunts. Adding `criterion` from signal detection
theory is the second axis fix: sensitivity (`reads_well`/`blind_to`)
and bias (`criterion`) are independent, and a table that records
only sensitivity misreads bias as sensitivity failure.

**On DEGENERACY vs REDUNDANCY.** Not a stylistic distinction. Two
modes with identical `reads_well` and different `blind_to` add
ROBUSTNESS — if one goes blind (or is refuted), the other's
different failure mode still covers the axis. Two modes with
identical `reads_well` and identical `blind_to` add COVERAGE without
robustness — they'll go blind together. The audit names which is
which so the operator can distinguish a resilient redundancy from a
correlated one.

## Echo-detection claims (`echo.py`)

Replaces the proxy independence test used across `info_taxonomy` /
`thermo_know` / `thermo_spine` (which counted distinct MODE names)
with a graph-theoretic construction: **two supports are independent
iff their provenance paths share no interior node**. Menger's theorem
delivers both quantities in one pass — max vertex-disjoint paths =
min vertex cut — so `independence(g, claim)` returns:

- `support` — the number of independent ways this claim reaches ground
- `cut` — the minimum set of interior nodes whose loss disconnects it
- `loud` — an `ECHO:` flag when apparent supports (immediate upstream
  count) exceed real supports (max flow)

Same structure, three dialects: **graph** (Menger, implemented here),
**systematics** (homology vs homoplasy — `agreement()` returns one
label or the other), **estimation** (correlated-error fusion — the
warning label). `retest_queue(g, claim, now, mode_half_lives)` orders
the cut set by `clock.freshness()` — the order the claim will fall
over. Staleest cut member first.

Sample: [`samples/echo.sample.txt`](samples/echo.sample.txt) (four scenarios: echo detection, real independence, homology, homoplasy).

| # | Claim | Refuted if | Verdict |
|---|-------|-----------|---------|
| EC-1 | `independence(g, claim)` returns `support = max flow` where each interior node has capacity 1. When three modes feed the same source and that source has one upstream anchor, the apparent count is 3 but every path passes through the source → max flow = 1. The `ECHO:` LOUD flag names the collapse and the cut. | Three modes fanning from one source producing `support = 3`, or a support value greater than the number of vertex-disjoint paths in the graph. | **HOLDS** — sample Scenario 1: 3 modes fan from `usda_1974`; `independence.support = 1`, `cut = ['usda_1974']`, `choke_points = ['usda_1974']`. LOUD verbatim: `ECHO: 3 apparent supports collapse to 1 -- routes share interior node(s) ['usda_1974']; the agreement is homologous (inherited), not convergent`. |
| EC-2 | Two disjoint chains through distinct sources and distinct anchors yield `support = 2`. `choke_points = []` when `support >= 2` (no single node whose removal disconnects). The cut still has cardinality = support (Menger), but each node in the cut is a redundant edge, not a choke. | Two disjoint chains yielding `support < 2`, or `choke_points` non-empty when `support >= 2`. | **HOLDS** — sample Scenario 2: 2 disjoint chains from `penetrometer_2026` and `rig_test_2026`; `support = 2`, `cut = ['instr', 'observed']` (the two saturated modes at the boundary), `choke_points = []`. Both anchors appear in `anchors_reached`. |
| EC-3 | `agreement(g, a, b)` returns HOMOLOGY when `a` and `b` share any ancestor (agreement inherited, weight 0), HOMOPLASY when their ancestor sets are disjoint (agreement convergent, counts as support). Systematics dialect over the same graph structure. | Two claims sharing an ancestor labelled HOMOPLASY, or two claims with disjoint ancestry labelled HOMOLOGY. | **HOLDS** — sample: `claim_a` and `claim_b` fed through modes from the same `a_shared` anchor → `shared_ancestors = ['a_shared']`, reading = `HOMOLOGY -- inherited agreement, weight 0`. Rebuilt with distinct anchors `a1` and `a2` → `shared_ancestors = []`, reading = `HOMOPLASY -- convergent, counts as support`. |
| EC-4 | `retest_queue(g, claim, now, mode_half_lives)` returns rows for each node in the cut set, ordered by `clock.freshness().remaining` (staleest first, `None` sinks to bottom because it's UNDETERMINED). Node freshness is computed against its own `as_of` / `volatility` / `mode`; nodes lacking these fields return `band=UNDETERMINED` with LOUD flags from `clock.py`. | A retest queue that reorders cut nodes freshest-first, or that silently defaults a missing `as_of` to `now` (yielding remaining=1.0). | **HOLDS** — sample Scenario 1's queue: `usda_1974` (the only cut node) reports band=UNDETERMINED because the demo node didn't declare an operator-mode; freshness returned `None` for remaining, and three LOUD flags fired verbatim from `clock.py`. Consistent with the "cut node dating is the operator's" posture — no default fills. |
| EC-5 | BOUNDARY: `independence()` and `agreement()` return counts, cuts, and labels — never a truth value on the claim itself. When `support = 0` (no anchor reached), the LOUD flag says `"cannot be re-checked, only re-argued"` verbatim — same language as `scaffold.py` uses for anchorless claims. The module refuses to fabricate independence out of nomenclature. | An `Independence` field containing a truth value / confidence score / rank, or a support count silently inflated by aliased modes. | **HOLDS** — `Independence` has fields `support (int)`, `cut (List[str])`, `anchors_reached (List[str])`, `choke_points (List[str])`, `loud (List[str])`. No truth field. No inflate. The claim `support=0` in code fires the "cannot be re-checked, only re-argued" LOUD verbatim; scaffold.py fires the same string for anchorless Scoped items. |

**On the echo-vs-independence delta.** Every earlier module in the
family (info_taxonomy IT-4, thermo_know TK-2, thermo_spine TSP-2)
counted distinct MODE names as the independence measure. That's a
proxy — it treats "instrument + direct_observation" as two
independent supports even when both readings trace to the same
1974 USDA soil map. Menger corrects the proxy: routes are what count.
Two modes fed by the same interior node are one support wearing two
hats. This is not a claim ABOUT the earlier modules; it is a
sharper mechanism they can migrate to when it makes sense. The
migration is not automatic; the earlier modules still use the mode-
distinctness heuristic and will until an operator rewires.

## Resonance / Nautilus / semantic-interference claims (post-C11)

Encoded in the modules landed via origin/main. Test-runner:
`test_refutations.py` sweeps each claim over `N` random trials and reports
counterexample count. `C17` currently returns `None` (not yet
implemented) — the module still imports cleanly.

Sweep sample: [`samples/test_refutations.sample.txt`](samples/test_refutations.sample.txt).

| # | Claim | Encoded in | Sample | Refuted if |
|---|-------|-----------|--------|-----------|
| **C12** | Any AI system trained on a corpus where the effective synthetic fraction exceeds 50% of the total training tokens, and lacking a physically grounded, invariant kernel that contributes ≥10% of the total loss gradient (`k < 0.5`), will exhibit a Resonance Factor `R ≥ 1.0` relative to human-release cadence. This guarantees the system's epistemic entropy asymptotically approaches zero faster than external auditing can restore it, resulting in >50% degradation in tail-task performance within `G ≥ ln(2)/R` generations. Independent of compute scale and alignment tuning — both modify `γ` and `ω_drive` only marginally and cannot introduce a conserved invariant post-hoc. | `resonance_audit.py` + `test_refutations.py:test_C12` | [`samples/resonance_audit.sample.txt`](samples/resonance_audit.sample.txt) | An AI system trained on ≥50% synthetic tokens with measured `R < 0.5` and `γ > ω_drive` that maintains task-performance drop <10% relative to a human-trained baseline after 3 generations. |
| **C13** | The Nautilus constraint set (`P ≥ 0.7`, `α ≈ φ`, constant `D_f`) ensures stability: a system in this parameter region maintains `Integrity > 0.8` and never trips a collapse flag. | `nautilus_architecture.py` + `test_refutations.py:test_C13` | [`samples/nautilus_architecture.sample.txt`](samples/nautilus_architecture.sample.txt) | A trial with `α ∈ [φ−0.1, φ+0.1]`, `λ ∈ [0.08, 0.12]`, `δ = 0`, `γ = 1.2`, `s = 0.1`, no entrainment, that shows `Integrity ≤ 0.8` or fires a collapse flag. |
| **C14** | With `R ∈ [0.8, 1.2]`, `α ∈ [1.4, 1.8]`, and `P ≥ 0.7`, the system is indefinitely stable — no collapse under any random variation of the remaining variables inside those bounds. | `resonance_audit.py` + `test_refutations.py:test_C14` | [`samples/resonance_audit.sample.txt`](samples/resonance_audit.sample.txt) | A collapse-flagged trial inside those bounds under random `λ`, `δ`, `γ`, `s`, entrainment. |
| **C15** | Plugging any single variable outside its safe threshold band drives `Integrity < 0.3` within 15 generations. | `phi_collapse_variables.py` + `test_refutations.py:test_C15` | [`samples/phi_collapse_variables.sample.txt`](samples/phi_collapse_variables.sample.txt) | A trial with `α < 1.0` (or any one variable out of bounds) whose `Integrity` stays ≥ 0.3 across 15 generations. |
| **C16** | High semantic-interference load (`load > 0.5`) guarantees collapse regardless of the other variables. | `semantic_interference_vectors.py` + `test_refutations.py:test_C16` | [`samples/semantic_interference_vectors.sample.txt`](samples/semantic_interference_vectors.sample.txt) | A trial with `load > 0.5` that never trips a collapse flag. |
| **C17** | Interference-load threshold `> 0.5` bounds the collapse basin. (Test not yet implemented — placeholder in `test_refutations.py:test_C17`.) | `semantic_interference_vectors.py` | — | See build recipe in the placeholder — follow `test_C16` shape. |
| **C-scale-1** | Collapse risk is monotone in the *log-drift* of fractal dimension per generation: `lam = ln(D_n/D0) / G`. Sign carries the branch (`lam < 0` degenerate, `lam > 0` explosive); `|lam|` is the collapse rate; both diverge as the Nautilus principle states. Verdict is `UNKNOWN` when the box-count fit's r² < 0.95 — a measured non-power-law is not a stability signal. | `scale_invariant_audit.py` v2 (was v1 with linear delta; retired to `legacy/`) | [`samples/scale_invariant_audit.sample.txt`](samples/scale_invariant_audit.sample.txt) | (R1) A run with `lam ≈ 0` (measured, not asserted) that has demonstrably collapsed refutes D_f as the collapse summary. (R2) Cross-module: C9 (per-doubling loss) predicts a power-law `D_n = D0 · G^-β`; C-scale-1 predicts exponential `D_n = D0 · exp(lam·G)`. Fit both to the same measured run; the loser updates its claim, neither sim is retuned. |
| **C-scale-2** | Log-drift of ANY diversity metric under recursive self-training satisfies (a) `lam < 0` for all synthetic:real ratios > 0, (b) `|lam|` monotone in ratio, and (c) `lam(ratio)` is NON-LINEAR with a knee bracketing the `field_collapse.py` spinodal `h* ≈ 0.385`. D_f is one instantiation; the claim is about log-drift, so the five diversity metrics shipped by CollapseTracker (distinct n-grams, Self-BLEU, KL, vocab coverage, rare-token survival) are enough to test it without downloading the 99 MB embedding artifact. | `collapsetracker_harness.py` (Ramkumar & Pragalya 2026; 24 trajectories × 11 gens) | [`samples/collapsetracker_harness.sample.txt`](samples/collapsetracker_harness.sample.txt) | (R1) `lam ≈ 0` on a documented-collapse trajectory refutes log-drift as the collapse summary. (R2) AIC prefers `(1+G)^-β` over `exp(lam·G)` in a majority of the 24 trajectories → C9's per-doubling law stands and C-scale-2 updates. Power check: AIC separates the two laws 100% at noise sd ≤ 0.05, 95% at 0.10 across 400 trials/cell — adequately powered. (R3) `lam(ratio)` linear across 0.25 / 0.5 / 0.75 / 1.0 → the spinodal formalism does not transfer from diversity-collapse to model-collapse. Box-counting on Sentence-BERT embeddings is a false-positive machine (`BOX_COUNTING_IS_DEAD` in the docstring); Path A must use TwoNN, Path B uses the shipped metrics directly. Paths C (Model Zoos, 3.8M parameter states across 27 zoos → TwoNN on weight vectors) and D (Multi-LLM Trace → `twonn_from_distances()` on a pairwise dissimilarity matrix; bridges to `alien_homeostasis.py`) skip the CollapseTracker download entirely. |
| **FC-1** | In reduced mean-field ϕ⁴ + linear-field theory, `F(ϕ, h) = -½ϕ² + ¼ϕ⁴ - h·ϕ`, the spinodal (the field strength at which the metastable well merges with the local maximum and any infinitesimal fluctuation triggers descent to the global minimum) sits at the closed-form value `|h*| = 2/(3√3) = 0.38490017945975047`. The cubic discriminant of `F'(ϕ) = ϕ³ - ϕ - h` is `Δ = 4 - 27h²`, which changes sign at exactly `|h*|`; three real roots become one. Mean-field spinodal is a CEILING — fluctuations (Ginzburg-criterion corrections) lower the effective threshold below this value. | `field_collapse.py` | [`samples/field_collapse.sample.txt`](samples/field_collapse.sample.txt) | (R1) A different reduced ϕ⁴ convention yielding `\|h*\|` >1% off from 0.38490018 is a convention mismatch, not physics — the derivation is closed-form. (R2) A recursive-training run whose `λ(ratio)` knee lands outside [0.25, 0.5] refutes the ϕ⁴ MAPPING to diversity dynamics (held separately from the physics). Update the mapping, not `h*`. (R3) A measurement showing collapse thresholds ABOVE `2/(3√3)` in a system provably in the ϕ⁴ universality class refutes mean-field spinodal as a ceiling — would require field fluctuations that stabilise (unphysical in this class). |
| **C29-v2** | A claim with quantitative physical content can be refuted by computing the horizon at which its own compounding rate crosses a named conservation bound. Effective physical growth `g_eff = growth_rate − decoupling_rate`; when `g_eff ≤ 0` the module returns `UNBOUNDED_ROUTE_OPEN` (this route does not refute the claim; R1 is satisfied). The output is a horizon in years + the identity of the binding bound — *not* a truth verdict scalar. Propagation state and thermodynamic horizon are held as separate objects and never recombined. | `case_studies/refutation_protocol.py` v2 (was v1 with `C = A·γ/ω` truth verdict scoring propagation as truth; retired to `legacy/`) | (bring your own claim + rate) | (R1) A sustained `d ≥ g` over a multi-decade window with the physical bound never binding refutes C29-v2 for that claim. (R2) Attack the bound itself (is 1.74e17 W the right ceiling?), the rate, or the coupling — each separately refutable. (R3) If a claim refuted here is observed to hold past its computed horizon, the bound or the coupling is wrong; update the claim, do not retune. |

Note: the pre-C11 duplicate of C12 (an earlier phrasing that sat above the "Revised" block) has been retired to Git history — the revised phrasing above is canonical.
