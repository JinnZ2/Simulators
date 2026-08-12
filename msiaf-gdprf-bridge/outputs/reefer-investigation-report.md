# MSIAF x GDPRF Investigation Report — Reefer Run-Off-Road

**Case:** Reefer run-off-road onto soft shoulder after debris avoidance

## Link Determinations

| Link | Pathway | Posterior | Cascade fidelity | Gate |
|---|---|---|---|---|
| L1 | D4 -> D2 | 0.744 | 0.837 | not_triggered |
| L2 | D2 -> D1 | 0.590 | 0.348 | not_triggered |
| L3 | D3 hazard + D2 stale feed | 0.751 | 0.819 | not_triggered |
| L4 | D1 micro-delay at the moment of the incident | 0.611 | 0.500 | failed |

## Systemic Determination

- Chain (conjunctive) confidence: **0.202**
- Weakest-link bound: **0.590**
- Bound divergence: 0.389 (residual variance trigger fired)
- Max unknown-variable risk: 0.500

## Decision Point

**ESCALATE** — residual variance trigger with unpassed identification gate; human must adjudicate unexplained ignorance

## Human Translation Layer Output

> The systemic determination — financial penalty structure (D4) driving dispatch pressure (D2), degrading driver physiology (D1), meeting an uncommunicated infrastructure hazard (D3) — is **supported at chain confidence 0.20** (weakest link: D2 -> D1 at 0.59). The moment-of-incident reconstruction link remains model-based and uncalibrated, and its identification gate failed: the exact contribution of fatigue to the overcorrection is recorded as **unexplained ignorance**, not asserted. Per the decision policy, this determination is **escalate**. residual variance trigger with unpassed identification gate; human must adjudicate unexplained ignorance.