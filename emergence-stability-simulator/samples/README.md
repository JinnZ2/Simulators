# Sample outputs

Committed artifacts from a small representative pipeline run
(`--runs 60 --timesteps 80 --sensitivity-runs 5 --mode-runs 60
 --attractor-runs 60 --balance-runs-per-cell 2`). Regenerate with
`python3 run_monte_carlo.py` from the parent directory.

- `CLAIM_TABLE.sample.json` — all 19 generated claims with
  `schema_version` and `source_repo` headers. EMRG_011 / 012 / 014
  confirmed; EMRG_013 / 015 explicitly REFUTED with `refutation_basis`
  and pointers to `CASE_STUDY_NARRATIVE_INSTINCT.md`. Validates clean
  under `tools/validate_claim_table.py`.
- `mode_comparison.sample.json` — per-scenario averages for the four
  paired scenarios used by EMRG_007 / EMRG_008. The numbers for
  `substrate_plus_inverted` are huge by design — inverted_narrative
  is a positive-feedback runaway.
- `attractor_quality.sample.json` — four scenarios used by EMRG_010
  (stable_majority / parasitic_majority × with / without
  `reality_perturbation`). Quality gap appears under reality stress.
- `balance_threshold.sample.json` — ratio sweep, extraction sweep,
  2D sustainability surface (with threshold curve), scale_builder
  amplification (both sustainable and unsustainable regimes,
  surfacing the artifact behind the refuted EMRG_013), disruption
  resilience (also an artifact under refutation), multi-community
  reach (artifact behind the refuted EMRG_015), historical overlay.
- `substrate_substitution.sample.txt` — output of
  `tools/substrate_substitution.py` applied to this CLAIM_TABLE.
  Side-by-side grass/grasshopper substitution for every claim that
  uses the substrate/narrative vocabulary. Methodology enforcement;
  see `tools/substrate_substitution_toolkit.py` for the seven-category
  programmatic surface.
- `sensitivity_report.sample.txt` — full ASCII visualization: dual-line
  drift plots, correlation bars, plain-language direction analysis,
  cross-scenario block, claim status block.
- `full_report.sample.txt` — trajectory, system entropy, per-agent
  drift histograms, and phase diagram from one representative run.
