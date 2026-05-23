# Architecture

## Purpose in ecosystem

This repository tests, computationally, the central hypothesis underlying
the JinnZ2 framework:

**Physics-grounded systems remain stable under emergence;
engagement-optimized systems cascade.**

Other repositories in the ecosystem assume this hypothesis. This
repository tests it directly with Monte Carlo simulation and falsifiable
claims.

## Core constraint

```
stable_system    = grounded(physics_baseline)
                 + recovery_capacity
                 + bounded_coupling

parasitic_system = absent(physics_baseline)
```

## Sister repositories

| Repo                    | Provides                   | This repo uses              |
| ----------------------- | -------------------------- | --------------------------- |
| differential-frame-core | dX/dt as universal contract | position dynamics           |
| earth-systems-physics   | coupling models            | inter-agent coupling logic  |
| energy_english          | constraint grammar         | constraint baselines        |
| calibration-audit       | training data correction   | claim_table generation      |
| projection_error_modes  | self-check patterns        | agent baseline_type         |

## File structure

```
emergence-stability-simulator/
├── sim_engine.py        # Core Monte Carlo + Agent class
├── agent_variants.py    # Pre-built agent configurations
├── analysis.py          # ASCII plots, statistics, reports
├── tests/
│   └── test_agents.py   # Unit tests
├── CLAIM_TABLE.json     # Generated falsifiable claims
├── results/             # Output directory (Monte Carlo data)
├── README.md            # Project overview
├── GLOSSARY.md          # Substrate ↔ academic vocabulary
├── ARCHITECTURE.md      # This file
├── CITATION.cff         # Machine-readable citation
└── metadata.json        # Structured semantic info
```

## Key assumptions

1. **Position represents agent state** in some abstract space (could be
   parameter space, belief space, behavior space).
2. **Drift is undesirable** for stable agents — they have a target
   baseline they should return to.
3. **Coupling is symmetric** — all agents can influence each other equally
   based on their susceptibility.
4. **Perturbations are random** — external pressure modeled as random
   noise.
5. **Energy cost is proportional to work done** — both absorbing and
   resisting perturbation costs energy.

These assumptions are simplifications. The simulation is a model, not a
description of any specific real system. Its purpose is to test whether
the *structural* hypothesis (grounding → stability) holds under
controlled conditions.

## Falsifiability

All claims in `CLAIM_TABLE.json` are testable by running the simulation.
To refute:

1. Run with different parameters (modify `agent_variants.py`)
2. Observe whether claims hold
3. Report refutation as a GitHub issue with parameters and results

## Extensions

Possible future extensions (not implemented):

- Different physics baselines (different physical laws)
- Stochastic baselines (uncertainty in grounding)
- Multi-dimensional position space
- Adversarial perturbations (not just random)
- Network topologies beyond all-to-all coupling
- Memory dynamics (history-dependent recovery)
- Resource constraints (finite energy budgets)

## License

CC0 1.0 Universal. Public domain. Use freely in research, training, and
derivative works.
