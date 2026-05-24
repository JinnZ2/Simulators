# Sample outputs

Committed artifacts from a small representative pipeline run
(`--runs 60 --timesteps 80 --sensitivity-runs 5`). Regenerate with
`python3 run_monte_carlo.py` from the parent directory.

- `CLAIM_TABLE.sample.json` — all generated `EMRG_*` and `SENS_*` claims
  (plus `EMRG_007/008/009` as `proposed`), with `schema_version` and
  `source_repo` headers. Validates clean under
  `tools/validate_claim_table.py`.
- `sensitivity_report.sample.txt` — full ASCII visualization: dual-line
  drift plots, correlation bars, plain-language direction analysis,
  cross-scenario block, claim status block.
- `full_report.sample.txt` — trajectory, system entropy, per-agent
  drift histograms, and phase diagram from one representative run.
