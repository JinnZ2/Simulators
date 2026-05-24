# Sample outputs

Committed artifacts from a small representative pipeline run
(`--runs 60 --timesteps 80 --sensitivity-runs 5 --mode-runs 60`).
Regenerate with `python3 run_monte_carlo.py` from the parent directory.

- `CLAIM_TABLE.sample.json` — all generated `EMRG_*` and `SENS_*` claims
  with `schema_version` and `source_repo` headers. EMRG_007 and
  EMRG_008 carry empirical status (`confirmed`/`refuted`) backed by the
  mode comparison; EMRG_009 stays `proposed` (architectural, out of
  simulation scope). Validates clean under
  `tools/validate_claim_table.py`.
- `mode_comparison.sample.json` — per-scenario averages for the four
  paired scenarios (substrate_only, substrate_plus_scale_builder,
  substrate_plus_inverted, substrate_plus_parasitic). The numbers
  for `substrate_plus_inverted` are very large by design — the
  inverted_narrative agent is a positive-feedback runaway that
  drags substrate into multi-order-of-magnitude divergence.
- `sensitivity_report.sample.txt` — full ASCII visualization: dual-line
  drift plots, correlation bars, plain-language direction analysis,
  cross-scenario block, claim status block.
- `full_report.sample.txt` — trajectory, system entropy, per-agent
  drift histograms, and phase diagram from one representative run.
