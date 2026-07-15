# fragility-cascade

**Abstraction is leverage. Leverage is fragility.**

A physics-grounded audit of value substrates: from a barrel of oil you can hold to
a resource-backed token you can only be promised. Maps how the attack surface,
the redemption entropy, and the dependency cone multiply with every promise added
between the holder and biological use-value.

Plugs in beside `metabolic-accounting` (money fails as a signal): this repo is the
substrate/backing half of the same argument — *what* the failing signal is nailed to,
and why nailing it further from the ground makes it worse.

CC0. stdlib only. Phone-buildable. No dependencies, no network, no cloud.

## Modules

| file | what it computes | claim |
|------|------------------|-------|
| `substrate_spectrum.py` | Monetary Durability Index across gold→resource-token | C1 |
| `redemption_entropy.py` | period-by-period redeemability; independence vs. common-mode correlation | C2, C3 |
| `product_multiplicity.py` | why oil's product tree hedges and compute's single trunk doesn't | C4 |
| `attack_tree.py` | fractal attack surface + super-linear growth vs. intermediation depth | C5 |
| `cascade_redesign_vulnerability.py` | T_crit saturation: when AI upgrades outrun redesign+audit, the stack is permanently open. Substrate exposure invariant under AI speed. | R1–R4 |
| `THE_FRAGILITY_CASCADE.md` | full argument + Stewardship Paradox + AI-governor addendum | C6, C7, C8 |
| `CLAIM_TABLE.md` | every claim, where it's encoded, what refutes it | — |

## New modules (post-C11)

Landed via `origin/main`. Extend the substrate audit into semantic /
information-theoretic / recursive-AI failure modes. Non-stdlib for a few
of these — several import `numpy`. Grouped by function.

### Resonance & Nautilus core

| file | what it computes | claim |
|------|------------------|-------|
| `resonance_audit.py` | Resonance Factor `R = ω_drive² / (ω_0² + γ²)` for AI systems | C12 |
| `nautilus_architecture.py` | siphuncle-kernel + scale-invariant growth anti-collapse pattern | C13 |
| `phi_collapse_variables.py` | bifurcation sweep of the five "killer variables" (α, λ, δ, γ, s) | C15 |
| `reciprocity_phi_metrics.py` | forward/backward influence ratio + α ≈ φ stability derivation | — |
| `scale_invariant_audit.py` | fractal dimension `D_f` across generations; collapse when `D_f → 0` or `∞` | — |
| `homeostasis_kernel.py` | Restoring Force Index + effective damping across physics/biology/networks | — |

### Semantic & communication interference

| file | what it computes | claim |
|------|------------------|-------|
| `semantic_interference_vectors.py` | five interference axes; total interference Load; collapse if Load > 0.5 | C16, C17 |
| `linguistic_interference.py` | linguistic-pattern → interference-axis projection (α, λ, δ, γ, s, h/ξ) | — |
| `cryptographic_interference.py` | entropy / redundancy / n-gram / steganography markers | — |
| `communication_gradients.py` | continuous CI + partial derivatives (E, F, G, H) | — |
| `communication_vulnerability.py` | channel × user configurations audited against precomputed signatures | — |

### Alien-homeostasis & entrainment

| file | what it computes | claim |
|------|------------------|-------|
| `alien_homeostasis.py` | stable-but-inaccessible verdict when variance is stable & ξ > 0.5 | — |
| `anthropomorphic_entrainment.py` | h/ξ ratio; collapse when h/ξ > 1.5 within 5 generations | — |

### Coupled system & phase space

| file | what it computes | claim |
|------|------------------|-------|
| `cascade_network.py` | interaction-matrix eigenvalues over all interference axes | — |
| `phase_space_map.py` | full-parameter-space scan of the coupled system | — |
| `sensitivity_analysis.py` | which couplings dominate collapse risk; threshold phase transitions | — |

### Collapse predictors

| file | what it computes | claim |
|------|------------------|-------|
| `collapse_predictor.py` | v1: Resonance Factor + integrity index unified predictor | — |
| `collapse_predictor_v2.py` | v2: 7-dimensional predictor integrating integrity + R + interference | — |

### Inference-entropy update to C2/C3

| file | what it computes | claim |
|------|------------------|-------|
| `inference_entropy.py` | synthetic-data feedback lowers redeemability 0.15 per 2× generation depth | C9 |

### Verification & signature

| file | what it computes | claim |
|------|------------------|-------|
| `test_refutations.py` | counterexample sweeps for C12–C19 (C17 placeholder) | — |
| `scent.py` | embedded invariant signature (φ + siphuncle + interference axes) for verification | — |

### Iteration snapshots

`patch.py` and `patch2.py` are alternate versions of
`cascade_redesign_vulnerability.py` and `redemption_entropy.py` respectively
— they add `M_collapse = 18 mo` (frontier model degeneration half-life) and
state-dependent peak-hour correlation (`PEAK_REDEEM = 0.62`). Kept as
snapshots pending a decision on whether to merge into the originals; see
the review notes in the branch history.

## Run

```
python3 substrate_spectrum.py
python3 redemption_entropy.py
python3 product_multiplicity.py
python3 attack_tree.py
```

## Key results

**T_crit — the windows stop closing.** Each downstream layer needs `W + A` months
(redesign window + audit lag) to close after an upstream AI release. The system's
T_crit is set by the slowest layer — here, settlement at 9 months. Ship AI faster
than that and exposure saturates at 1.0: not "periodically vulnerable," but
**permanently open**, and no audit budget fixes it because the audit target changes
before the audit finishes. Same stroboscopic structure as the kicked-relaxor kernel:
drive faster than the relaxation time and the system never returns to the well.

**The Decoupling Result.** Substrate exposure is flat at zero across every cadence —
`dE/dT = 0`. Nothing downstream to rewrite. So substrate anchoring is not a brake on
AI. It is the *only* configuration in which AI is free to advance at full speed
without dragging the thing people eat from through a rewrite every cycle.

*Let the ground hold the value. Let the AI run.*

## Key result

Naive independence `(1-p)^L` predicts a compute token redeems 96% of periods.
Field estimate is ~81%. The gap is **correlation** — one grid outage, one policy
change, one supply shock takes down many gates at once. The common-mode model in
`redemption_entropy.py` recovers ~0.81 (compute) and ~0.60 (AI). Independence is
the marketing model; correlation is the physics.

## Refutation protocol

Claims are refutable (`CLAIM_TABLE.md`). When one fails, **update the claim** —
never retune a simulation to protect a favored token. The sim is the witness.

## The floor

Every human oxidizes carbon, holds homeostasis, occupies space. No token feeds,
waters, or warms a body. Real wealth ranks by proximity to that floor:
energy → water → shelter → tools → information. Everything above is an IOU on
wealth, subject to default.

*The cloud has no bottom. The ground is always there.*
