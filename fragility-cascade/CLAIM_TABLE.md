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
