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

### Interaction, engagement, and cross-frame audits

Landed after the C12-C17 batch. Move the audit from substrate integrity to
the interaction layer — what happens between the AI and the user, and what
happens between an audit and an incentive.

| file | what it computes |
|------|------------------|
| `coherens.py` | Coherens `C = (A + γ) / ω` — capacity of a system to hold its pattern against interference; stable iff `C > 1`. |
| `bacterial_herding.py` | photosynthetic-bacteria herding model mapped to Coherens: predator pressure = drive, herding = damping. |
| `survival_spirals.py` | coherence preservation under extreme constraint — the shape of last-resort coherence. |
| `engagement_threshold.py` | Net Engagement Value across biological / cultural / economic / linguistic constraints. |
| `friction_calibration_ratio.py` | FCR > 1 flags a net-loss interaction. |
| `interaction_audit.py` | audits agent-interlocutor interaction quality; classifies regime and predicts stability. |
| `weird_gatekeeper.py` | detects when a WEIRD frame is being forced on non-WEIRD cognition. |
| `explorer.py` | interactive sweep / phase-map / trajectory / stable-region search over the coupled collapse system. |
| `additional.md` | language and framing notes for the interaction-layer modules. |

### Additional axes on the original models

| file | what it adds | claim |
|------|--------------|-------|
| `cascade_redesign_M_collapse.py` | second T_crit axis: model degeneration half-life `M_collapse = 18 mo`; real T_crit is `min(W+A, M_collapse/2)`. When frontier synthetic-data feedback shortens M_collapse below 2 × (W+A), the model-degeneration axis pulls T_crit lower than the layer-stack axis. Standalone; does not replace `cascade_redesign_vulnerability.py`. | C9 / R-family |
| `redemption_entropy_peak_hour.py` | state-dependent per-gate redemption: peak grid hours (17-20, ~4/day) drop redeemability to 0.62 vs off-peak 0.81; daily average 0.778. Encodes C11 (state-dependent correlation). Standalone; does not replace `redemption_entropy.py`. | C11 |

## Run

```
python3 substrate_spectrum.py
python3 redemption_entropy.py
python3 product_multiplicity.py
python3 attack_tree.py
```

Or run the whole folder and get a report card:

```
python3 run_all.py                     # dumps samples/run_all_report.json
python3 run_all.py --timeout 30
```

`run_all.py` subprocesses every module's `__main__` demo (bounded wall time,
isolated imports), records exit code + wall time + first/last stdout line,
and writes a machine-readable report. Exit code is the count of non-OK
modules — usable in CI. `explorer.py` is skipped (interactive).

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
