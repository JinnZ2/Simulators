# climate-modeling

**Two layers.** Level-1 is the actual simulation model (grass, cascade grass,
future migration and extinction models). Level-2 is *experiments about
experiments*: an audit taxonomy that probes what a modeler's own
simplifications systematically miss.

The whole point of the level-2 layer is to catch **cascade-speed blindness** —
the pattern where a smooth, memoryless, Gaussian-driven model predicts collapse
in fifty years and reality does it in five. Every audit is a controlled
experiment where the true system is known (we built it), a simplified model is
run in parallel, and the discrepancy names a specific failure mode.

Non-stdlib. Requires `numpy` + `scipy` (see `requirements.txt`); the dashboard
adds `streamlit`. Same exemption pattern as `play-sims/` — declared up front.

## Layout

```
climate-modeling/
├── config.py                  parameter registry
├── forcing.py                 six forcing generators (diurnal, ramp, trend,
│                              stochastic, fat-tailed, aggregated wrapper)
├── models/
│   ├── base.py                BaseModel with solve_ivp integrator
│   ├── grass.py               plain carbon-balance grass
│   └── cascade_grass.py       threshold + feedback + memory (the true system)
├── audits/
│   ├── base_audit.py          BaseAudit interface
│   ├── phase_change.py        built
│   ├── stationarity.py        built
│   ├── missing_feedback.py    built
│   ├── omitted_variable.py    built
│   ├── data_aggregation.py    built
│   ├── cascade_speed.py       built (the flagship)
│   ├── frontier_stubs.py      ten stubs with build recipes
│   └── audit_registry.py      BUILT_AUDITS + FRONTIER_AUDITS
├── ai_interface.py            AIScientist (dummy + openai path)
├── meta_experiments.py        AI-patching loop
├── run_audits.py              entry point
├── AUDIT_TAXONOMY.md          the sixteen failure modes
└── samples/                   captured audit report
```

## Run

```bash
pip install -r requirements.txt
python run_audits.py
```

Prints a report card and writes JSON to `samples/audit_report.json`.

## What's built vs frontier

**Six built audits** run end-to-end from the same `BaseAudit` interface:

- `PhaseChangeAudit` — smooth curve blind to a true respiration cliff.
- `StationarityAudit` — model calibrated on stationary window, forcing trends.
- `MissingFeedbackAudit` — grass-only ignores soil-plant coupling.
- `OmittedVariableAudit` — hidden moisture cycle drives residuals.
- `DataAggregationAudit` — daily-mean-fitted parameters bias hourly predictions.
- `CascadeSpeedAudit` — the flagship: threshold + feedback + memory + fat tails.

**Ten frontier stubs** each raise `NotImplementedError` with a full build
recipe in the class docstring (true system class, audit model, forcing
generator, failure metric). Same pattern as
`sustained-activation-gate/`'s `explore_theta_vs_restore` before it was
built. Promoting a stub to a live audit is a documented five-step
procedure in [`AUDIT_TAXONOMY.md`](AUDIT_TAXONOMY.md).

## AI-patching loop

`ai_interface.py` ships with a rule-based stub AI that recognises each
built audit and proposes a structural patch on failure (add threshold, add
feedback, recalibrate on richer data, adjust `Q10`). Swap `backend="openai"`
to route through an LLM; the prompt template is spelled out in
`_build_prompt`.

`meta_experiments.MetaExperiment.run_audit_with_patching()` runs an audit,
asks the AI for a patch on failure, records the patch, re-runs. Bounded by
`max_iterations`. Failed patches are recorded in `history`, not silently
discarded — the diagnostic point of the loop is which failure modes an
LLM's structural suggestions can actually repair.

## Refutation protocol

Every audit's failure metric is a falsifiable prediction. When the metric
is missed (audit unexpectedly passes), update the **claim about the failure
mode**, not the metric threshold. Do not lower tolerances to save a
favored audit. The audit is the witness, not the defendant.

## License

CC0. See the repo root [`LICENSE`](../LICENSE).
