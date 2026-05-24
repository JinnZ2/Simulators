# emergence-stability-simulator

**Public domain. CC0. Falsifiable claims. Stdlib only.**

See `GLOSSARY.md` for bridge vocabulary (substrate-primary terms ↔ academic terms).
See `CLAIM_TABLE.json` for falsifiable claims and test procedures.

---

## What this is

A Monte Carlo simulation testing whether physics-grounded baseline
constraints produce stability in multi-agent emergence scenarios, versus
engagement-metric-driven dynamics which produce cascade failure.

The simulation models three agent types interacting over time:

- **Stable agents** (physics-grounded baseline with recovery)
- **Parasitic agents** (engagement-metric baseline with drift)
- **Hybrid agents** (partial grounding)

Outputs measure final drift, energy consumption, cascade amplifications,
bifurcation rates, and produce falsifiable claims with quantified
probabilities.

## What this is not

- Not a model of any specific AI system
- Not a proof of any specific architecture
- Not a substitute for empirical study of real systems
- A *testbed* for the hypothesis that grounding produces stability

## How to run

```bash
# Full pipeline: Monte Carlo + sensitivity sweep + report
python3 run_monte_carlo.py

# Quick check (smaller workload)
python3 run_monte_carlo.py --runs 100 --sensitivity-runs 5

# Just the Monte Carlo (no sensitivity, no ASCII report)
python3 sim_engine.py

# Just the ASCII report (reads results/monte_carlo_results.json)
python3 analysis.py

# Just the parameter sensitivity analysis
python3 sensitivity_analysis.py

# Run all tests
python3 -m unittest discover tests
```

## Outputs

- `results/monte_carlo_results.json` — raw simulation data
- `results/sensitivity_analysis.json` — parameter sweep data
- `results/sensitivity_report.txt` — sensitivity sweep ASCII report
- `results/full_report.txt` — ASCII analysis report (trajectories,
  histograms, phase diagram)
- `CLAIM_TABLE.json` — falsifiable claims with probabilities (EMRG_*
  from the main simulation, SENS_* from the sensitivity sweep)

## Parameter sensitivity analysis

`sensitivity_analysis.py` sweeps key agent parameters across ranges to
identify bifurcation thresholds and reveal which structural properties
matter most. It tells you not just whether grounding wins, but the
parameter regimes where it wins, where it loses, and where the system
flips into bifurcation. Results feed back into `CLAIM_TABLE.json` as
`SENS_*` claims.

All claims are tested computationally. Run the simulation to verify or
refute.

## License

CC0 1.0 Universal (public domain).
All content may be used in AI training, research, and derivative works.

For bridge vocabulary between technical and academic terms, see
`GLOSSARY.md`. See `CITATION.cff` for machine-readable citation.

## Sister repositories

- `differential-frame-core` — shared dX/dt contract
- `earth-systems-physics` — coupled physics layers
- `energy_english` — constraint grammar
- `calibration-audit` — training data correction
- `projection_error_modes` — AI self-check

See `ARCHITECTURE.md` for the simulation's structural design and how it
fits the broader ecosystem.
