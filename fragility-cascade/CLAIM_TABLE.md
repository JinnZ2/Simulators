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

Note: the pre-C11 duplicate of C12 (an earlier phrasing that sat above the "Revised" block) has been retired to Git history — the revised phrasing above is canonical.
