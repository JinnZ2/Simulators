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
# Run default Monte Carlo (1000 runs, 100 timesteps each)
python3 sim_engine.py

# Generate report
python3 analysis.py

# Run tests
python3 -m unittest tests.test_agents
```

## Outputs

- `results/monte_carlo_results.json` — raw simulation data
- `CLAIM_TABLE.json` — falsifiable claims with probabilities
- `results/full_report.txt` — ASCII analysis report

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
