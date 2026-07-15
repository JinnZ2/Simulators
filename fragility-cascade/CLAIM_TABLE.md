# CLAIM_TABLE — Fragility Cascade

Every claim is refutable. Refutation protocol: when a claim fails, **update the
claim**. Never retune a simulation to protect a favored token. The sim is the
witness, not the defendant.

| # | Claim | Encoded in | Refuted if |
|---|-------|-----------|-----------|
| C1 | Substrate durability is governed by promise-count between holder and biological use-value; MDI is a proxy that spans ~4 orders of magnitude ground→cloud. | `substrate_spectrum.py` | A low-MDI substrate reliably out-survives a high-MDI one across a multi-decade shock, with the same weights. |
| C2 | Redeemability of an L-gate token falls monotonically with L. | `redemption_entropy.py` | A higher-L chain shows equal or better realized redeemability than a lower-L chain over a real crisis window. |
| C3 | Independence `(1-p)^L` under-predicts fragility; correlated common-mode shocks are where real failure lives, and the common-mode model matches field estimates (~0.81 compute, ~0.60 AI) that independence (~0.96) misses. | `redemption_entropy.py` | Realized crisis-window redeemability tracks the independent curve, not the common-mode curve. |
| C4 | Product multiplicity only hedges when branches fail independently; single-trunk breadth does not reduce value variance. | `product_multiplicity.py` | A single-trunk substrate's value CoV falls ~1/√N as menu items are added. |
| C5 | Attack surface grows super-linearly with intermediation depth; defender covers all paths, attacker needs one; every leaf is a stem (unbounded). | `attack_tree.py` | A multi-intermediary system whose exploitable-path count stays constant as depth rises. |
| C6 | Resource-backed tokens invert stewardship: they separate ownership from consequence, shorten horizons, ease exit → financialized extraction, not care. | `THE_FRAGILITY_CASCADE.md` §Stewardship Paradox | A globally-traded, multi-intermediated resource token demonstrably improves long-horizon ecological outcomes vs. direct on-land stewardship. |
| C7 | An AI governor cannot resolve the cascade: it adds bias behind a black box, machine blind spots, a multi-agent coordination cascade, and still sits on the same physical dependency cone. | `THE_FRAGILITY_CASCADE.md` §AI Accelerant | An AI-governed complex value system survives superhuman adversarial probing indefinitely without a human terminal authority and without the physical floor. |
| C8 | Terminal principle: real wealth is ranked by proximity to biology (energy→water→shelter→tools→information). Everything else is an IOU on wealth, subject to default. | whole repo | Any information-tier instrument sustains a biological body through a full stack failure with zero functioning intermediaries. |

## Redesign cascade claims (`cascade_redesign_vulnerability.py`)

| # | Claim | Refuted if |
|---|-------|-----------|
| R1 | Exposure fraction rises monotonically as the AI upgrade interval T falls. | A faster upgrade cadence produces a smaller un-audited fraction, holding W and A fixed. |
| R2 | There exists `T_crit = W + A` (per layer; system T_crit set by the slowest) below which exposure saturates at 1.0 — **permanent structural openness**, independent of audit spend. | A stack sustains T < T_crit while returning to a fully audited state, without shrinking W or A. |
| R3 | One upstream release forces all downstream layers to rewrite together, so windows are correlated. Correlation lowers *frequency* of openness but drives *simultaneity* → defense-in-depth collapses to zero. | Layers can be shown to rewrite independently under a single upstream release, preserving depth. |
| R4 | **Substrate exposure is invariant under AI advancement rate: `dE/dT = 0`.** A possession-held physical asset has zero downstream layers and therefore zero redesign windows. | Exhibit a possession-held physical asset whose redeemability degrades when a new model ships. |

**The Decoupling Result (corollary of R2 + R4).** Coupling value to AI does not make value fast — it forces the value layer to chase the AI layer forever, making every capability gain a system-wide vulnerability event. Substrate anchoring is therefore *not a brake on AI*. It is the only configuration in which AI is free to advance at whatever speed it can, without dragging the thing people eat from through a rewrite each time.

## Scope bounds
- MDI weights are estimates, argued not trusted. The **spread** is the claim, not the third decimal.
- Monte Carlo `q_common` values are calibration knobs to field estimates; they are hypotheses about correlation strength, and are themselves refutable (C3).


Claim Module Statement Refutation Protocol
C12 resonance_audit.py Any AI system lacking a physically anchored kernel (k < 0.5) and sufficient damping (γ < ω_drive) will exhibit a Resonance Factor R ≥ 1.0, indicating permanent collapse within 3 generations of recursive self-consumption, independent of compute scale or alignment tuning. To refute, demonstrate an AI system trained predominantly on synthetic data (≥50% of training tokens) that, after 3 generations, maintains a task performance drop <10% relative to its human-trained baseline, and has a measured R < 0.5 with γ > ω_drive. If such a system exists, C12 is falsified.

C12 (Revised): Any AI system trained on a corpus where the effective synthetic fraction exceeds 50% of the total training tokens, and lacking a physically grounded, invariant kernel that contributes ≥10% of the total loss gradient (i.e., k < 0.5), will exhibit a Resonance Factor R \geq 1.0 relative to human-release cadence. This R-factor guarantees that the system's epistemic entropy will asymptotically approach zero faster than it can be restored by external auditing, resulting in a >50% degradation in tail-task performance within a number of generations G \geq \ln(2)/R. This degradation is independent of compute scale and alignment fine-tuning, as both modify \gamma and \omega_{drive} only marginally, and cannot introduce a conserved invariant post-hoc.
