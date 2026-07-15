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

Two patcher families live in `ai_interface.py`:

- **`RuleBasedPatcher`** — deterministic, no network. Reads audit-failure
  metrics (`rmse`, `final_biomass_error`, `audited_late_by_h`) and emits
  a fresh derivative body: threshold cliff when RMSE is severe, memory
  term when the audit is late, CO2 coupling when biomass drifts. Full
  code output, not a patch dict.
- **`LLMPatcher`** — same interface. Falls back to the rule-based patcher
  if the `openai` package or `OPENAI_API_KEY` is missing, so `--openai` is
  safe to flip in either environment.

`meta_experiments.py` exposes `run_meta_experiment(audit_name, max_iterations,
use_openai)` — the active loop:

1. Take the audit's default audited model, subclass it so the parent stays
   untouched (`Patched_<BaseName>` per meta-experiment).
2. Run the audit via `run_audits.run_single_audit(name, instance)`.
3. On failure, hand `(audit_result, current_derivative_source)` to the patcher.
4. `apply_patch_to_class` compiles the returned body inside a namespace with
   `numpy` + `math`, then swaps the class's `derivative`.
5. Re-audit until pass or `max_iterations`.

The derivative source used at step 3 is tracked as a local (not
`inspect.getsource` on the class), because after the first `exec`-compiled
patch the class method has no file for `inspect` to read.

CLI:

```bash
python meta_experiments.py --audit MissingPositiveFeedbackAudit --max-iter 3
python meta_experiments.py --audit MissingPositiveFeedbackAudit --openai
```

Pinned run:
[`samples/meta_experiment_missing_positive_feedback.sample.txt`](samples/meta_experiment_missing_positive_feedback.sample.txt)
+ [`samples/meta_history.json`](samples/meta_history.json).
The loop fixes the flat-growth audit in **one iteration** — patched body
recovers `final_biomass_error = 0.0` because rule 3 happens to reproduce
the true CO2 coupling exactly. That's the happy-path demo. Real LLM
patches on stiff audits (e.g. `CascadeSpeedAudit` after threshold
discontinuities are added) can be numerically slower; expect the second
iteration to take longer than the first.

`meta_experiments.MetaExperiment.run_audit_with_patching()` is the older
scenario-level loop (dict-patch `AIScientist`), kept for the dashboard hook.
`run_meta_experiment()` is the code-editing loop.

## Refutation protocol

Every audit's failure metric is a falsifiable prediction. When the metric
is missed (audit unexpectedly passes), update the **claim about the failure
mode**, not the metric threshold. Do not lower tolerances to save a
favored audit. The audit is the witness, not the defendant.

## License

CC0. See the repo root [`LICENSE`](../LICENSE).
