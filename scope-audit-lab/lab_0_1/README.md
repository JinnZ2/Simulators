# Scope Audit Lab — Prototype 0.1

A preference-free, standard-library Python instrument for recording mathematical models,
their declared scope, controlled experiments, discrepancies, and unresolved questions.

**Design constraint:** this tool records evidence and relationships. It does not decide
that a model is correct, incorrect, universally valid, or invalid. A discrepancy is a
recorded observation requiring characterization, not an automatic conclusion.

## Requirements
- Python 3.10+
- Standard library only
- No network access
- No external solver required

## Quick start
```bash
python -m unittest discover -s tests -v
python -m scope_audit_lab demo --out demo_output.jsonl
python -m scope_audit_lab validate demo_output.jsonl
```

The demo creates synthetic illustrative data, not empirical findings.

## Record types
- `model`: purpose, target quantity, declared scope, assumptions, dependencies, units, unknowns, representation, provenance.
- `experiment`: question, conditions, changed factors, control, planned comparisons, status.
- `observation`: predicted and observed values, uncertainty, method, conditions, residuals when calculable.
- `audit_event`: recorded evidence, unresolved questions, proposed next tests; no automatic verdict.

Records are appended as JSON Lines. Model revisions should receive new IDs; prior observations are not overwritten.

## Interpretation boundary
The tool does not automatically attribute a discrepancy to scope mismatch, measurement error,
numerical error, implementation defect, omitted dependency, invalid assumption, stochastic
variation, or an unmodeled process. Those remain candidate explanations to be tested.

## Not implemented in 0.1
Dimensional-analysis plugins, dependency graph algorithms, compression adapters, statistical
diagnostics, uncertainty propagation, domain-specific solvers, and cryptographic log chaining.
