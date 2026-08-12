# GDPRF v3.0 — Specification Consolidation

v3.0 consolidates the instrument-epistemology work into the core spec. Every
claim and proxy is now instrument-aware: measurands, transduction chains,
traceability pyramids, model-dependence rungs, and blindness maps are first-class
schema objects, and the update engine accounts for them mathematically.

## Schema Changes

### Claim (v3.0)
New required fields:
- `target_measurand` — the unobservable true state the claim is about
- `grounding_status` — `measured` / `estimated` / `assumed` (claim-level rollup)
- `model_dependence_rung` — M0/M1/M2/M3 of the claim's reported quantity

### Proxy (v3.0)
Replaces the flat v2.0 proxy with an instrument-grade node:
- `target_measurand` + `observable_indication` + `bridge_model` (with
  `model_dependence_rung`, `calibration_source`, `uncertainty_source`)
- `transduction_chain` — phenomenon → interaction → transducer →
  signal_conditioning → digitization → indication; per-link fidelity and grade
- `traceability_pyramid` — `primary_standard_exists`,
  `calibration_chain_status` (`intact`/`expired`/`convention_only`/`broken`),
  `si_unit_link`
- `blindness_map` — `null_states`, `alias_states`, `saturation_limit`,
  `gate_cutoffs`, `frame_biases`
- `epistemic_mask_score` — P(Blind): probability the proxy is in a blindness
  state for the current claim context
- v2.0 fields retained: `calibration`, `validity_claim_id`, `metrology`

## Enhancement 1 — Blindness-Adjusted Gradient Updates

Implemented in `engine.py` as `gradient_update_masked`:

```
Likelihood_adjusted(D|H) = (1 - P(Blind)) · P(D|H) + P(Blind) · P(Uninformative)
```

Concretely: each evidence pair (fidelity, coupling) is scaled by
`(1 - epistemic_mask_score)` before the log-odds update. Consequences:

- A **fully blind** observation (mask → 1) yields **zero information gain** —
  the posterior does not move in either direction.
- A blind "no signal" reading does **not** push the posterior toward zero —
  absence of signal is no longer misread as evidence of absence.
- Partial masks scale gain smoothly without ever reversing sign.

Additionally, `effective_fidelity_v3` composes:
`calibrated_fidelity × transduction_chain_fidelity × traceability_factor`
where the traceability factor is 1.0 (intact) / 0.9 (expired) / 0.8
(convention_only) / 0.6 (broken).

## Enhancement 2 — Action Proposal Engine

New module `gdprf.actions`. Phase-7 limitations are no longer just reported —
they generate upgrade tasks:

| Gap detected | Action proposed |
|---|---|
| Expired/broken calibration chain | `SCHEDULE_CALIBRATION` |
| Convention-only traceability (no primary standard) | `COMMISSION_EXPERIMENT` (standards infrastructure) |
| Uncalibrated proxy (`method: none`) | `COMMISSION_EXPERIMENT` (validation holdout) |
| Null/gate blind states | `TRIANGULATION_CALL` (physically distinct instrument) |
| Frame biases | `REQUEST_SENSOR_PLACEMENT` |
| Assumed transduction links | `COMMISSION_EXPERIMENT` (per-link) |
| Unknown-variable risk > 0.45 | `HUMAN_REVIEW` |

Each proposal carries target aspect, rationale, expected grounding upgrade,
priority, and cost class — machine-readable for multi-agent task queues.

## Model-Dependence Ladder Mandates (now enforced in schema)

| Rung | Uncertainty dominated by | Mandate |
|---|---|---|
| M0 | Instrument physics | Report raw metric without inference |
| M1 | Reference standard quality | Require intact traceability chain |
| M2 | Empirical model transferability | Disclose training data (sample size, location) |
| M3 | Inverse-problem assumptions & priors | Bound prior distributions; note non-uniqueness |

## Worked Example

[`../examples/biomass-claim.example.json`](../examples/biomass-claim.example.json)
— an M2 ecology claim (forest biomass via airborne LiDAR) with full
transduction chain, convention-only traceability, a five-category blindness map,
and mask score 0.25. Validates against all v3.0 schemas.
