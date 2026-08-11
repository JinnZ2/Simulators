# GDPRF — Gradient-Driven Proxy Reasoning Framework

A framework that enables AI agents to construct and refine complex claims by
linking abstract concepts to concrete, observable **proxies** — reasoning in
continuous confidence gradients rather than binary true/false logic.

> Claims like *"employee morale is low"* or *"economic growth is slowing"* cannot
> be verified directly. They must be distilled into physical, empirical, or
> data-driven proxies.

## Repository Contents

### Docs
- [`docs/architecture.md`](docs/architecture.md) — core modules and rationale
- [`docs/operational-cycle.md`](docs/operational-cycle.md) — the five-step evaluation cycle
- [`docs/human-translation-layer.md`](docs/human-translation-layer.md) — explainability: confidence mapping, causal chains, scope clarification
- [`docs/amendments-v2.md`](docs/amendments-v2.md) — v2.0 spec amendments grounded in the literature self-assessment
- [`docs/provenance.md`](docs/provenance.md) — tamper-evident lineage ledger for every belief update
- [`docs/spec-v3.md`](docs/spec-v3.md) — v3.0 consolidation: instrument-aware schemas, blindness-adjusted updates, action proposals
- [`docs/decision-points.md`](docs/decision-points.md) — governed thresholds turning gradients into actions

### Schemas (JSON)
- [`schemas/claim.schema.json`](schemas/claim.schema.json) — Claim / Hypothesis object
- [`schemas/proxy.schema.json`](schemas/proxy.schema.json) — Proxy node object
- [`schemas/edge.schema.json`](schemas/edge.schema.json) — Vector Knowledge Graph edge object

### Examples
- [`examples/burnout-claim.example.json`](examples/burnout-claim.example.json) — a worked cascading-proxy example (burnout → Slack response velocity → server log activity)

### Reference Implementation (Python)
- [`src/gdprf/engine.py`](src/gdprf/engine.py) — operational cycle steps 3, 3.5, 4, 5 (calibration, provenance-weighted metrology, log-odds gradient update, identification gate)
- [`src/gdprf/provenance.py`](src/gdprf/provenance.py) — W3C PROV-inspired, hash-chained audit ledger
- [`src/gdprf/decisions.py`](src/gdprf/decisions.py) — decision-point policy (DEPLOY / RESEARCH / HOLD / ESCALATE / ABORT)
- [`src/run_example.py`](src/run_example.py) — end-to-end run of the bundled example
- [`tests/test_engine.py`](tests/test_engine.py) — 14-test suite (`python3 -m pytest tests/ -q`)

### Research
- [`research/literature-review.md`](research/literature-review.md) — academic grounding (and complications) for each framework pillar, with source CSVs
- [`research/framework-assessment.md`](research/framework-assessment.md) — self-test: the framework's own five-step cycle applied to its six core claims, with posteriors

## The Core Idea

| Binary reasoning | GDPRF gradient reasoning |
|---|---|
| Claim is true or false | Claim carries a continuous confidence gradient (0.0–1.0) and variance margin |
| Abstract traits treated as directly knowable | Abstract traits mapped to observable proxy metrics with metrological quality scores |
| Universal claims | Every claim is scoped (temporal, spatial, locality context) |
| Hidden variables ignored | Residual variance monitored; threshold breach triggers hidden-proxy search |

## Core Objects (Quick Reference)

**Claim** — the hypothesis under evaluation: ID, domain, statement, scope,
confidence gradient, variance margin, assigned proxies, unknown-variable risk score.

**Proxy** — a measurable stand-in for an unobservable variable: target variable,
observable metric, metrology (precision, noise floor, systematic bias), fidelity
gradient, physical grounding chain, vector embedding.

**Edge** — a typed relationship in the Vector Knowledge Graph: `causal`,
`correlated`, `confounding`, or `proxy_of`, with coupling strength, evidence
weight, and update timestamp.

## Operational Cycle (Summary)

1. **Claim formulation** — instantiate a scoped Claim object (no universal truths).
2. **Proxy traversal & discovery** — query the VKG; cascade through indirect
   proxies when no direct one exists.
3. **Metrological evaluation** — signal-to-noise filtering and bias calibration
   of incoming measurements.
4. **Gradient Bayesian update** — continuous probabilistic confidence revision:
   `confidence_new = f(confidence_prior, proxy evidence)`.
5. **Unknown-variable search** — monitor residual variance; on threshold breach,
   launch exploratory queries for confounders or missing proxies.

The **Human Translation Layer** then renders the high-dimensional system state as
readable narrative with explicit scope and causal-chain traceability.

## Status

**v3.0** — instrument-epistemology consolidation: measurand decomposition,
transduction chains, traceability pyramids, M0–M3 model-dependence rungs, and
blindness maps are first-class schema objects; the engine performs
blindness-adjusted gradient updates; the Action Proposal Engine converts
Phase-7 limitations into upgrade tasks. Schemas are not backward compatible
with v2.x. See [`docs/spec-v3.md`](docs/spec-v3.md).

Earlier: v2.1 reference implementation (engine, provenance, decision points);
v2.0 amendments from the literature self-assessment.

Open threads:
- Formal definition of the gradient update function `f` (Bayesian conjugate
  families vs. learned update)
- VKG storage/indexing strategy for vector embeddings
- Threshold policy for the unknown-variable risk score
- Validation test suite for the schemas
