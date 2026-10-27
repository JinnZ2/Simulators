# Scope Audit Lab — Prototype 0.2

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
python -m scope_audit_lab transitions-demo --out transitions_demo.jsonl
python -m scope_audit_lab validate transitions_demo.jsonl
```

The demos create synthetic illustrative data, not empirical findings.

## Record types
- `model`: purpose, target quantity, declared scope, assumptions, dependencies, units, unknowns, representation, provenance.
- `experiment`: question, conditions, changed factors, control, planned comparisons, status.
- `observation`: predicted and observed values, uncertainty, method, conditions, residuals when calculable.
- `audit_event`: recorded evidence, unresolved questions, proposed next tests; no automatic verdict.
- `transition_scan` (new in 0.2): one factor-variation scan — ordered cases, adjacent
  deltas, candidate transition regions, unresolved items. No boundary verdict.

Records are appended as JSON Lines. Model revisions should receive new IDs; prior observations are not overwritten. Streams written by 0.1 remain valid (schema versions 0.1 and 0.2 are both accepted).

## Scope-transition engine (new in 0.2)

`scope_audit_lab/transitions.py` implements the experiment engine specified at the end of
the 0.1 cycle:

1. Vary a recorded factor across cases **in the order given** — the engine never sorts.
2. Compare adjacent cases and calculate output changes (absolute and relative).
3. Record changes that exceed a declared threshold (`strictly greater than`) as
   **candidate transition regions**, with direction and factor interval.
4. Preserve missing inputs: a missing or non-finite factor/output is recorded with a
   reason — never dropped, interpolated, or replaced.
5. Zero-valued outputs: absolute change is still computed; relative change is recorded
   as undefined with the reason retained.

The engine does **not** declare that a scope boundary exists, that a model failed, or
that a transition is significant. Candidate regions are inputs to follow-up experiments.

CLI:
```bash
python -m scope_audit_lab transitions cases.json --threshold 5 --kind absolute \
    --factor-label visibility --output-label bottle_count --label "survey A" --out events.jsonl
```
`cases.json` is a list of `{"case_id", "factor", "output", "notes?"}`; `factor` or
`output` may be `null` (recorded as missing, not skipped).

## Interpretation boundary
The tool does not automatically attribute a discrepancy or a candidate transition region
to scope mismatch, measurement error, numerical error, implementation defect, omitted
dependency, invalid assumption, stochastic variation, or an unmodeled process. Those
remain candidate explanations to be tested.

## Verification status
- 31 unit tests pass (11 core + 20 transition-engine).
- Test coverage includes the four behaviors mandated by the 0.2 specification:
  threshold behavior (strict `>`, absolute and relative kinds), input-order
  preservation, missing measurements, and zero-valued outputs.
- 0.1 record streams still validate.

## Not implemented in 0.2
Automatic transition *detection* (statistical change-point estimation), coupling
tests between factors, dimensional-analysis plugins, dependency graph algorithms,
compression adapters, statistical diagnostics, uncertainty propagation, domain-specific
solvers, and cryptographic log chaining.
