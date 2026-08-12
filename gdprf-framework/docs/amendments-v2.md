# Spec Amendments v2.0 — Grounded in Framework Self-Assessment

These amendments implement the recommendations from
[`../research/framework-assessment.md`](../research/framework-assessment.md),
which tested GDPRF's six core claims against retrieved academic literature.

| # | Amendment | Motivating finding | Literature anchor | Implementation |
|---|-----------|--------------------|-------------------|----------------|
| 1 | **Calibration module** (new step 3.5) | Claim C4 scored 0.38 — VKG confidences can't be taken at face value | Tabacof & Costabello 2019; Safavi et al. 2020 | `calibration` object in `proxy.schema.json`; update engine consumes `calibrated_fidelity` only |
| 2 | **Bias provenance** | Bias values are usually estimated, not measured | Kane 1997; Magnusson & Ellison 2008 | `metrology.provenance` with `measured`/`estimated`/`assumed` per field; provenance-weighted correction in step 3 |
| 3 | **Proxy-validity recursion** | Proxies silently redefine constructs; validity is a claim, not a fact | Seltzer 2021; Knox et al. 2022 | `validity_claim_id` required on every proxy; bounded recursion in step 2 |
| 4 | **Identification gate** (step 5) | Residual-variance triggers chase noise without identification | Miao et al. 2018; D'Amour 2019 | `hidden_variable_search` object in `claim.schema.json`; gate must pass before gradient updates |
| 5 | **Governance edge type** | Telemetry proxies face consent/deployability constraints | Chowdhary et al. 2023 | `governs` added to `relationship_type` enum in `edge.schema.json`; traversal check in step 2 |

## Schema Compatibility

v2.0 is **not** backward compatible:

- `proxy` objects now require `calibration`, `validity_claim_id`, and
  `metrology.provenance`.
- `claim` objects gain optional `hidden_variable_search` (required only after a
  step-5 trigger).
- `edge` objects accept the new `governs` enum value.

The worked example has been updated to v2.0:
[`../examples/burnout-claim.example.json`](../examples/burnout-claim.example.json)
