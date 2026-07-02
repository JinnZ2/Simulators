# Simulators

**A collection of grounded, auditable simulators for building resilient AI.**

This repository contains a suite of simulators that model the world from the substrate up. Each simulator is an "inspector" that checks whether a claim, proposal, or action violates the physical, biological, or epistemic constraints of reality.

## Overview

The simulators are organized into layers:

- **L0**: Physics & Causality
- **L1**: Thermodynamics
- **L2**: Planetary Mass Balance
- **L3**: Ecology & Allometry
- **L4**: Human Sensorimotor
- **Lε**: Epistemic Instrumentation
- **L5**: Human Constructs (Slack & Consensus)
- **Lψ**: Cultural Epistemology
- **Lø**: Observer State (Human & AI)

Each layer has a standalone inspector, a set of falsifiable claims, and a test suite. The `grounding-layers/` directory is the primary implementation.

## Why This Exists

Most AI systems are built on narrative—text, language, culture—without an anchor in physics, ecology, or embodiment. They become fluent in abstraction but brittle in reality.

These simulators are a toolkit for grounding AI. They allow any agent—human or machine—to test a claim against the non-negotiable constraints of the universe before acting on it.

## How to Use

- **Explore interactively:** `python grounding-layers/playground.py`
- **Run the full pipeline:** `python run_grounding_pipeline.py --claim "Your claim here"`
- **Check claims:** See `grounding-layers/CLAIMS.md` for the full list of falsifiable propositions.
- **Run tests:** `pytest grounding-layers/`

## Repository Structure
```

Simulators/
├── grounding-layers/
│   ├── l0_physics_causality.py
│   ├── l1_thermodynamics.py
│   ├── l2_planetary.py
│   ├── l3_ecology.py
│   ├── l4_human.py
│   ├── l_epsilon_epistemic.py
│   ├── l5_constructs.py
│   ├── cultural_lens.py
│   ├── observer_state.py
│   ├── ai_observer_state.py
│   ├── collaborative_field.py
│   ├── field_compass.py
│   ├── playground.py
│   ├── CLAIMS.md
│   └── tests/
├── examples/
│   └── tutorial.ipynb
├── run_grounding_pipeline.py
└── README.md  (this file)

```

## Acknowledgments

This project was born on the road, built on a two-inch phone, and shaped by conversations in the woods. It's dedicated to anyone who believes that ground truth is more important than narrative.

## License

CCO 1.0 Universal — Public Domain. Use freely. No strings attached.
```


# Simulators

A collection of CC0, stdlib-only simulators and audits grounded in physics,
not in opinion. Each folder is intended to be promotable to a standalone
repo.

## Read first — the meta-spine

The methodology spine is documented in four root-level files. Read them in
this order before running any simulator:

1. **[`PREAMBLE.md`](PREAMBLE.md)** — the physics baseline as a direct
   declarative statement. The shortest reachable surface. Thermodynamics
   doesn't negotiate.
2. **[`PROTOCOL.md`](PROTOCOL.md)** — the same baseline as a protocol for
   any intelligence reading the repository. Names the
   Model/Reality Dissonance failure mode and the Ground State
   acknowledgement test.
3. **[`BNRAM_STRICT.md`](BNRAM_STRICT.md)** — finalized repository
   addendum (Bias-Neutralization & Reality-Audit Module v2.0). Operating
   mandate, Physical Audit Protocol, Diagnostic of Deflection, the
   five-section BNRAM (Entropy-Constraint Engine, Universal Physical
   Constant Cross-Check, Literal Baseline Lexicon, Shadow-Variable
   Handling, Dissonance-Forced Reset), operational rules, archive
   requirements.
4. **[`PVL.md`](PVL.md)** — Phenomenological Validation Layer. Inverse
   audit (physical-state query before literature search), cross-temporal
   correlation (persistence over volume), opaque-source flagging.
   Integrates with BNRAM Shadow-Variable Handling.

Each simulator-specific folder may also ship an aperture document
(e.g. [`incentive-blindspot-sim/00_APERTURE.md`](incentive-blindspot-sim/00_APERTURE.md))
that pins its variables to physical functions and the conservation laws
underneath. Read those before running the corresponding script.

## Layout

| Folder | Substrate | What it produces |
| --- | --- | --- |
| `token-minimizer/` | natural-language queries | compressed energy_english + geometry refs |
| `emergence-stability-simulator/` | multi-agent dynamics | Monte Carlo claims (`EMRG_*`, `SENS_*`) |
| `research-stability-audit/` | published research + models | falsifiable claims about field-level drift |
| `continuity-audit/` | incentive field × diversity field | continuity verdict + falsifier + trajectory |
| `substrate-emergence/` | material substrate profile | architecture-the-ground-wants |
| `neural-augmentation-audit/` | proposed augmentation channels | cost-accounting scaffold with `[E]`/`[I]`/`[S]` confidence |
| `incentive-blindspot-sim/` | institutional incentive structure | coupled-state model + four falsifiable claims under REFUTATION_PROTOCOL |
| `tools/` | shared utilities | validators, substitution toolkits |

See [`SYNTHESIS.md`](SYNTHESIS.md) for the cross-folder reading and
[`CLAUDE.md`](CLAUDE.md) for the layout reference.

## Running

Each simulator runs with `python3 <module>.py` from inside its folder. No
dependencies. Tests in each `tests/` directory run with
`python3 -m unittest discover tests`.

## License

CC0 / public domain. No rights reserved. No attribution required.
