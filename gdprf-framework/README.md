# gdprf-framework

GDPRF — **Gradient-Driven Proxy Reasoning Framework**. Reasoning in
continuous confidence gradients instead of binary true/false, by
linking unverifiable abstract claims to concrete observable
**proxies** with explicit metrology.

`PACKAGE_README.md` is the upstream framework introduction — start
there for the substance. This file covers repo positioning, what
actually runs, and cross-references.

## The one-line version

Claims like *"employee morale is low"* cannot be verified directly.
They must be distilled into proxies — and every proxy is an
instrument with precision, bias, and a noise floor, not a fact. GDPRF
makes that chain explicit and carries the uncertainty through to a
governed decision.

| Binary reasoning | GDPRF |
|---|---|
| Claim is true or false | Continuous confidence gradient + variance margin |
| Abstract traits directly knowable | Traits mapped to proxies with metrological quality scores |
| Universal claims | Every claim scoped (temporal, spatial, locality) |
| Hidden variables ignored | Residual variance monitored; breach triggers hidden-proxy search |

## What runs

```bash
python3 src/run_example.py     # end-to-end worked example
python3 -m pytest tests/ -q    # 23 tests
```

Verified on landing: **23/23 green**. The worked example
(`examples/burnout-claim.example.json`, a cascading burnout →
Slack response velocity → server log activity chain) produces:

```
prior 0.68 -> posterior 0.7696
cascade fidelity: 0.464
gate: not_triggered — no action
DECISION: ABORT — deployment blocked by governance constraint(s)
blocked by: ['proxy ...0001 under unsatisfied governs edge']
provenance ledger: 8 records, chain valid: True
```

Worth noting what that output *does*: the posterior went **up**
(0.68 → 0.77) and the system still refused to deploy, because a
governance edge was unsatisfied. Rising confidence does not buy
authority — that separation is the point of the decision layer.

## Layout

| Path | What |
|---|---|
| `docs/architecture.md` | Core modules and rationale |
| `docs/operational-cycle.md` | The five-step evaluation cycle |
| `docs/human-translation-layer.md` | Explainability: confidence mapping, causal chains, scope |
| `docs/amendments-v2.md` | v2.0 amendments grounded in the literature self-assessment |
| `docs/provenance.md` | Tamper-evident lineage ledger for every belief update |
| `docs/spec-v3.md` | v3.0 consolidation — instrument-aware schemas, blindness-adjusted updates |
| `docs/decision-points.md` | Governed thresholds turning gradients into actions |
| `schemas/*.json` | Claim / Proxy / Edge JSON Schema |
| `src/gdprf/engine.py` | Cycle steps 3, 3.5, 4, 5 (calibration, metrology, log-odds update, identification gate) |
| `src/gdprf/provenance.py` | W3C PROV-inspired hash-chained audit ledger |
| `src/gdprf/decisions.py` | DEPLOY / RESEARCH / HOLD / ESCALATE / ABORT policy |
| `research/literature-review.md` | Academic grounding *and complications* per pillar, with source CSVs |
| `research/framework-assessment.md` | The framework's own cycle applied to its six core claims |

That last one is the load-bearing move: **the framework runs itself
through its own five-step cycle and publishes the posteriors.** Same
shape as `divergence-playground/` seeding `FORKS.jsonl` from its own
ledger, or `equivalence-field/`'s `seed_claims()` holding the
module's own claims as first-class objects in its own spine.

## Version status

**v3.0** — measurand decomposition, transduction chains, traceability
pyramids, M0–M3 model-dependence rungs, and blindness maps are
first-class schema objects; the engine performs blindness-adjusted
gradient updates. **Schemas are not backward compatible with v2.x.**

The v3 instrument-epistemology vocabulary is implemented in the
sibling `../instrument-epistemology/` folder — that repo is where the
M0–M3 rungs and blindness maps were worked out against real
scientific instruments.

## Repo positioning

**Stdlib-only at runtime.** The single non-stdlib dependency is
`jsonschema`, used by exactly one test (`test_engine_v3.py::
test_v3_example_validates`) to validate the shipped example against
the v3 schema. Everything else — engine, provenance, decisions,
`run_example.py` — is pure stdlib. Without `jsonschema` you get
22 pass / 1 error rather than 23 pass.

No `CLAIMS.md` / `REFUTATION_PROTOCOL` file, but
`research/framework-assessment.md` is functionally that: six core
claims with posteriors, tested by the framework's own machinery.

## The family

This folder is one of four landed together, plus the earlier MSIAF
drop. They compose:

```
msiaf-framework/            the incident-analysis frame (D1-D4 cascade)
        │
        ├── msiaf-gdprf-bridge/     expresses MSIAF findings as GDPRF claims
        │
gdprf-framework/            ← you are here: the gradient reasoning engine
        │
        ├── proxy-investigation-lab/    tests the proxies GDPRF consumes
        │
        └── instrument-epistemology/    applies the same method to
                                        scientific instruments themselves
```

GDPRF *consumes* calibrated, provenanced proxy objects. The lab
*produces* them. The bridge *feeds* MSIAF determinations in.

## Cross-repo resonances

- **`divergence-playground/`** — hash-sealed `Reading` objects that
  cannot be revised after the fact. GDPRF's hash-chained provenance
  ledger is the same tamper-evidence discipline applied to belief
  updates instead of reader commitments.
- **`energy/PROVENANCE.md`** — a hand-maintained decision ledger
  (12 DPs, 8 falsification entries). GDPRF automates that shape.
- **`grounding-layers/`** — "any layer above L0 is bounded by every
  layer below it." GDPRF's cascade fidelity (0.464 in the worked
  example) is the same bounding argument as a running product.
- **`model-ecology/`** — asks "what is the domain of validity of this
  framework?" rather than "which model predicts best?" GDPRF's
  mandatory claim scoping is that question enforced at the schema
  level.

## Open threads (upstream)

- Formal definition of the gradient update function `f` (Bayesian
  conjugate families vs. learned update)
- VKG storage/indexing strategy for vector embeddings
- Threshold policy for the unknown-variable risk score
- Validation test suite for the schemas

## Provenance

Source drop: **OKComputer_Create_Another_Repo**
(`a21bf9b3-...zip`). An earlier zip (`40c116ad-...`) contained a
docs-only v2 subset of this folder; the later zip supersedes it
entirely (adds `src/`, `tests/`, `research/`, and the v3 spec), so
only the later version is landed. Files are byte-identical to the
drop apart from the upstream `README.md` → `PACKAGE_README.md`
rename.

CC0.
