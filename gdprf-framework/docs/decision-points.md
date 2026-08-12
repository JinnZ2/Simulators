# Decision Points

A confidence gradient is not a decision. **Decision points** are explicit
thresholds where the system must act — and the gradient-plus-ignorance state
determines which action is permitted.

## Actions

| Action | Meaning |
|---|---|
| `DEPLOY` | Claim may drive deployment-facing output |
| `RESEARCH` | Keep gathering evidence; research-mode only |
| `HOLD` | Insufficient evidence either way |
| `ESCALATE` | Human review required |
| `ABORT` | Governance violation or failed gate — stop this branch |

## Decision Logic (in order of precedence)

1. **Governance** — any assigned proxy under an unsatisfied `governs` edge →
   `ABORT` for deployment (research-mode inference unaffected).
2. **Identification gate** — triggered hidden-variable search with a
   failed/pending gate → `ESCALATE`: a human adjudicates unexplained ignorance.
3. **Calibration floor** — `DEPLOY` requires calibrated proxies with
   `expected_calibration_error` below the policy floor; otherwise drop to
   `RESEARCH` even at high confidence.
4. **Bands** — confidence × unknown-variable risk:

```
conf >= deploy_confidence AND uvr <= max_unknown_risk_for_deploy   -> DEPLOY
conf >= deploy_confidence AND uvr >  escalate_unknown_risk         -> ESCALATE   ← confident AND ignorant
conf >= deploy_confidence AND uvr in between                       -> RESEARCH
research_confidence <= conf < deploy_confidence                    -> RESEARCH
conf < research_confidence                                         -> HOLD
```

The **confident-and-ignorant → ESCALATE** rule is the load-bearing one: a high
confidence gradient paired with a high unknown-variable risk score means the
model is sure of itself inside a map it knows is incomplete. That state never
deploys silently.

## Policy as Configuration

Thresholds are not constants in the engine — they are a `DecisionPolicy`
deployment choice, tuned per domain and recorded in the provenance ledger as the
`agent` context of each `decision_point` record. A medical deployment and a
logistics deployment will (and should) set different bands; both must log which
policy decided.

```python
from gdprf.decisions import DecisionPolicy, evaluate
policy = DecisionPolicy(deploy_confidence=0.85, max_unknown_risk_for_deploy=0.25)
dp = evaluate(claim, proxies, edges, policy)
```

## Worked Result

On the bundled example: posterior 0.77 (research band) — but the latency proxy is
under an unsatisfied `governs` edge (employee-consent policy), so the decision is
**ABORT-for-deployment** with research-mode inference preserved. This is the
Amendment-5 machinery working as designed: technically valid evidence,
deployability blocked until consent is satisfied.
