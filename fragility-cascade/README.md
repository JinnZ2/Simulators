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
