# Operational Cycle

The system follows a five-step cycle (plus a calibration interlock added in v2.0)
to evaluate a claim.

## Step 1 — Initial Claim Formulation
An AI agent instantiates a Claim object, explicitly defining its local context and
scope (temporal bounds, spatial bounds, locality context) to avoid binary,
universal truth assumptions.

## Step 2 — Proxy Traversal & Discovery
The agent queries the Vector Knowledge Graph. If no direct proxy is available, it
searches for **cascading proxies**:

```
Employee Burnout  →(proxy_of)→  Slack Response Velocity  →(proxy_of)→  Keystroke / Server Log Activity
```

Each hop is an edge in the VKG with its own coupling strength and evidence weight;
fidelity decays with cascade depth.

**v2.0 — proxy-validity recursion (Amendment 3):** every selected proxy must have
a resolvable `validity_claim_id` — the claim that *this proxy measures its target
variable*. That claim is itself evaluated through this cycle (bounded recursion:
validity claims may not recurse deeper than one level without human review). A
proxy whose validity claim falls below the deployment threshold is treated as
asserted, not established (Seltzer 2021).

**v2.0 — governance edges (Amendment 5):** traversal must check for incoming
`governs` edges on each proxy. A governed proxy may still inform the gradient in
research mode, but is excluded from any deployment-facing output unless the
governing constraint (consent, legal basis) is satisfied (Chowdhary et al. 2023).

## Step 3 — Metrological Evaluation & Instrumentation
The agent evaluates the quality of incoming data:

- **Signal-to-Noise Ratio calculation** — filters true shifts from random noise
  using the proxy's noise floor.
- **Bias Calibration** — adjusts for known systematic distortions in the
  measurement tool (the proxy's `systematic_bias` field).

**v2.0 — provenance weighting (Amendment 2):** metrological values are weighted by
their provenance (`measured` > `estimated` > `assumed`). A proxy whose
`systematic_bias_source` is `assumed` contributes its bias correction as a prior
with uncertainty, not a fixed offset — preventing circular updating (Kane 1997).

## Step 3.5 — Confidence Calibration (Amendment 1, added v2.0)

Raw fidelity gradients and evidence weights are **never** fed directly into the
update step. Knowledge-graph confidence research shows uncalibrated scores are
systematically overconfident (Tabacof & Costabello 2019; Safavi et al. 2020).

- Each proxy's `fidelity_gradient` is mapped through its calibration record
  (`platt_scaling`, `isotonic_regression`, or `temperature_scaling`) fitted on
  held-out verified outcomes, producing `calibrated_fidelity`.
- A proxy with `method: none` (uncalibrated) is flagged and its evidence weight
  is shrunk toward the prior by a conservative factor.
- Calibration quality itself is tracked via `expected_calibration_error`;
  degrading ECE triggers recalibration.

## Step 4 — Gradient Updating (Non-Binary Reasoning)
The framework updates the claim's confidence gradient using a continuous
probabilistic function over **calibrated** inputs:

```
confidence_new = f(confidence_prior, calibrated proxy evidence)
```

Reasoning happens in shades of grey, not black and white — evidence moves the
gradient; it does not flip a boolean.

## Step 5 — Unknown Variable & Hidden Proxy Search
The system monitors **residual variance** between predictions and observations.
If a set threshold is exceeded, it flags an unmapped variable and prepares
exploratory queries to isolate confounding factors or missing proxies in the
graph.

**v2.0 — identification gate (Amendment 4):** before any exploratory query's
results can update the gradient, the `hidden_variable_search.identification_gate`
must pass:

1. Record `residual_variance_observed` and the breached `threshold`.
2. Select an identification strategy — e.g., proxy-variable conditions
   (Miao, Geng & Tchetgen Tchetgen 2018), negative controls, or multi-cause
   estimation **with a fragility check** (D'Amour 2019).
3. List the `assumptions` explicitly. If identification fails, the gate stays
   `failed`: residual variance is reported as *unexplained ignorance* (raising
   `unknown_variable_risk_score`) rather than chased with unconstrained queries.
