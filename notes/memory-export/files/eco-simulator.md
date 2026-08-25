---
name: eco-simulator
description: Multi-agent institutional simulation — stakeholder metabolism, policy friction, compliance drag as thermodynamic cost.
sources: [field]
aliases: [EcoSimulator, eco_simulator]
---

CC0. Models institutional and social systems as ENERGY FLOWS above the physical substrate
layer.

## Three structural components

- **Stakeholder Agent Cluster** — agents initialized with explicit incentives, constraints,
  and operational agendas
- **Friction Engine** — rules-based matrix calculating transaction drag, coordination
  overhead, and entropy for every policy transition
- **Stress-Test Sandbox** — high-frequency simulation loop exposing bottlenecks before
  physical resources are committed

## Three paradigms integrated

- **IRM** (Influence-Reaction Model): agents influence the environment; the environment reacts
  based on physical laws; cell-based controllers assign environmental state limits
- **EMuReL** (Environmental-impact Multi-agent RL): agents estimate the environmental impact of
  peers' actions, forcing comparison of personal gain against collective cost
- **ABM**: integrates sociology, economics, environmental science; models coordination of
  capital across institutional bodies with internal memory modules

## Closed-loop feedback

agent ignores environmental impact -> constraint degrades available capital -> conflict
resolution triggers -> entropy event logged

## Relationship to thermo_pm

EcoSimulator sits ON TOP OF [[thermo-pm]]. thermo_pm produces physical ground truth;
EcoSimulator models what institutions ADD as overhead. Intended interface: EcoSimulator queries
the thermo_pm waste delta as a friction-cost input.

That layering is the point — institutional overhead is only legible as a quantity once there
is a physical floor to measure it against.
