# research-stability-audit

**Public domain. CC0. Falsifiable claims. Stdlib only.**

A framework for testing claims about research stability and AI model
degradation. Not "here's what we know" — "here's how to test what we
claim to know."

## What this is

Six preset falsifiable claims with measurement methods, thresholds,
time windows, and cascade-risk thresholds — covering reproducibility
crisis, retraction lag, field-specific decay rates, AI model
degradation, substrate transmission collapse, and the
methodology-vs-narrative survival differential.

Plus a small framework (`ResearchClaim`, `ResearchStabilityAudit`,
`ResearchPaper`, `ResearchDataset`) so you can plug measurements in
and have bifurcation / cascade-risk computed for you.

## What this is not

- Not a conclusion about what's true in any specific field
- Not a substitute for empirical replication studies
- Not a model — a *framework for testing* claims about research stability

## How to run

```bash
# Register the preset claims and write CLAIM_TABLE.json + CROSS_REFERENCES.json
python3 research_stability_audit.py
```

## Outputs

- `CLAIM_TABLE.json` — six falsifiable claims, ready for measurement
- `CROSS_REFERENCES.json` — mapping to `emergence-stability-simulator`
  claims (same physics at different scales)

## Cross-reference to emergence-stability-simulator

This audit's claims map onto the agent-level claims in
`emergence-stability-simulator`:

| Research claim       | Agent-level analog | Shared principle |
|----------------------|--------------------|------------------|
| `AI_DEGRAD_001`      | `EMRG_003`, `EMRG_004` | Ungrounded systems amplify pressure and waste energy |
| `RES_REPRO_001`      | `EMRG_001`, `EMRG_002` | Physics-grounded baselines drift less |
| `BIF_ONSET_001`      | `EMRG_005`, `EMRG_006` | Grounded minority can dominate via attractor effect |
| `CASCADE_METHOD_001` | `EMRG_001`, `EMRG_006` | Falsifiable methodology is the field-level baseline |

AI model degradation, research irreproducibility, and emergent cascade
are instances of the same structural pattern: systems without a
grounded baseline drift and amplify; systems with one damp.

## Sources

Documented in `NOTES.md` and the `sources` field of each claim.
Headline numbers:

- 40-60% real research failure rate vs 0-5% formal retraction rate
- 91% of ML models degrade within one year (Nature 2025)
- Citation half-life: 3-5 years in fast-moving fields
- Knowledge transmission collapse: <1 generation in skilled trades

## License

CC0 1.0 Universal (public domain).
