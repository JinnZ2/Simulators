# SPEC_GPT.md

provenance: GPT, 2026-11-10. Pasted by Kavik into the work order of 2026-11-10 and
filed here verbatim (recovered from the session transcript; nothing edited, the
non-ASCII characters are the delivery's own). Everything below the line is the spec.

---

Relational Systems Experimental Playground

Python laboratory for equation substitution, boundary exploration, and context-dependent model discovery

1. Research objective

Develop a Python playground that allows mathematical equations, system matrices, boundary conditions, and control variables to be independently substituted, modified, and compared.

The playground must not assume that one model applies universally.

Instead, it investigates which mathematical formulations produce usable descriptions of particular systems under particular conditions.

Candidate systems include:

* Slime molds
* Forests and ecological networks
* Biological organisms
* Artificial intelligence systems
* Distributed and self-organizing systems
* Hypothetical or abstract dynamical systems

These are experimental domains, not intelligence rankings.

2. Foundational architecture

Separate the laboratory into six independently configurable layers.

A. System definition

Describes the system being investigated.

Variables:

* State variables
* Internal organization
* Energy inputs and outputs
* Material exchanges
* Information exchanges
* Environmental dependencies
* Characteristic timescales

The system definition must permit multiple competing boundary definitions.

B. Relational matrix

Describes relationships among system components and their environment.

Candidate relationship classes:

* Energy transfer
* Matter transfer
* Information transfer
* Causal interaction
* Structural dependency
* Feedback
* Regulatory interaction
* Unknown relationship

Relationships must be directional where appropriate. Reciprocity must not be assumed.

C. Boundary matrix

Describes the selected system boundary as an experimental variable.

Variables:

* Boundary location
* Boundary thickness
* Permeability
* Exchange rates
* Boundary mobility
* Included relationships
* Excluded relationships
* Boundary uncertainty

The boundary may be fixed, moving, distributed, or dynamically generated.

D. Control matrix

Describes experimental interventions.

Variables:

* Held constant
* Independently varied
* Coupled variables
* Perturbation magnitude
* Perturbation duration
* Recovery conditions
* Measurement frequency
* Instrument sensitivity

Boundary selection and control selection must be independently configurable.

E. Continuity matrix

Maintains the distinction between:

1. System continuity.
2. Configuration continuity.
3. Transition dynamics.
4. Recovery and reorganization.
5. Persistence under changing conditions.

A system must be permitted to reorganize without automatically being classified as having ceased to exist.

F. Uncertainty matrix

Tracks uncertainty independently for every measured or modeled variable.

Required statuses:

* MEASURED
* ESTIMATED
* INFERRED
* ASSUMED
* UNKNOWN
* NOT MEASURED
* EXCLUDED BY DESIGN

Every value must have provenance and, where possible, a numerical uncertainty interval.

Unknown values must never silently become zero.

⸻

3. Equation substitution engine

This is the central feature.

The playground must permit equations to be replaced without rewriting the experimental infrastructure.

Use a common interface:

MODEL(state, environment, relationships, controls, parameters)

Each equation module returns:

* Predicted state changes.
* Energy changes, when applicable.
* Relationship changes.
* Boundary behavior.
* Configuration changes.
* Model-specific uncertainty.

Candidate equation families:

A. Linear systems

[
\dot{x}=Ax+Bu
]

Useful for investigating:

* Stability
* Coupling
* Controllability
* Sensitivity
* Response to perturbation

B. Nonlinear dynamical systems

[
\dot{x}=f(x,u,e,\theta)
]

Useful for:

* Threshold behavior
* Nonlinear feedback
* Multiple stable configurations
* Bifurcations
* Regime changes

C. Network dynamics

[
\dot{x}i=f_i(x_i,\sum_j A{ij}g(x_j))
]

Useful for:

* Distributed organization
* Network dependencies
* Local versus global behavior
* Emergent coordination

D. Energy-constrained systems

[
\frac{dE}{dt}=P_{\mathrm{in}}-P_{\mathrm{out}}-P_{\mathrm{diss}}
]

Useful for:

* Energy availability
* Persistence costs
* Dissipation
* Operational limits

E. Boundary-dependent systems

[
\dot{x}=f(x,e,B(t),u)
]

Where (B(t)) describes a potentially changing boundary.

Useful for:

* Permeability
* Boundary movement
* Interface behavior
* Exchange dependencies

F. Stochastic systems

[
dx=f(x,t)dt+G(x,t)dW_t
]

Useful for:

* Environmental variability
* Uncertainty propagation
* Perturbation sensitivity
* Probabilistic transitions

These are candidate model families, not assumptions that every system follows every equation.

⸻

4. Boundary experimentation

The playground should allow multiple boundary definitions to operate on the same underlying experimental system.

For example:

Experiment A:

* System = AI software.

Experiment B:

* System = functioning computational installation.

Experiment C:

* System = computational infrastructure and its operational dependencies.

Experiment D:

* System = extended material and energy supply network.

Each experiment uses the same underlying observations where applicable, but changes the selected system boundary.

The laboratory then compares:

* Which dependencies become internal?
* Which remain external?
* Which relationships disappear from the model?
* Which new relationships become visible?
* Does the predicted behavior change?
* Does the definition of continuity change?
* Does uncertainty increase or decrease?

Importantly, changing the boundary must not change the underlying physical observations.

⸻

5. Experimental matrix

The experimental runner should support factorial combinations of:

Dimension	Experimental variation
Equation	Linear, nonlinear, network, stochastic
Boundary	Fixed, moving, distributed
Control	Fixed, varied, perturbed
Environment	Stable, variable, changing
Energy	Abundant, constrained, intermittent
Relationships	Dense, sparse, directional
Continuity	Structural, functional, reorganizational
Uncertainty	Low, high, heterogeneous
Timescale	Short, intermediate, long

The combinations should be configurable rather than requiring every possible combination.

This permits targeted experimentation without creating an unnecessarily large search space.

⸻

6. Boundary-edge investigation

The boundary should have its own measurement engine.

Measure:

* Exchange rates across the boundary.
* Changes in permeability.
* Accumulation or depletion near interfaces.
* Local instability.
* Changes in coupling strength.
* Changes in organizational structure.
* Transition thresholds.
* Hysteresis.
* Recovery after perturbation.

Distinguish interior, interface, and exterior measurements.

Do not assume the boundary is a geometrically thin surface. Some systems have diffuse or distributed interfaces.

An important experimental question:

Do the most informative changes occur in the system’s interior, at its interface, or in the relationships connecting it to its surroundings?

⸻

7. Model usability determination

The laboratory must not produce a universal winner or intelligence ranking.

Instead, it should generate a context-dependent applicability record for each equation.

Criterion	Question
Applicability	Under what conditions does the model work?
Predictive adequacy	Does it predict observations within stated uncertainty?
Stability	Does it remain useful under perturbation?
Sensitivity	Which parameters dominate its behavior?
Boundary dependence	How sensitive are results to boundary selection?
Energy consistency	Does it respect relevant physical constraints?
Observability	Can its required variables be measured?
Identifiability	Can competing parameter explanations be distinguished?
Computational cost	What resources does the model require?
Failure region	Where does its approximation cease to hold?

A model can be useful in one context and unsuitable in another.

Two models may also be simultaneously useful at different scales.

A model’s failure region must be retained as experimental information rather than discarded as noise.

⸻

8. Experimental outputs

Every run should generate:

1. Configuration record.
2. Equation identifier and version.
3. Boundary specification.
4. Control specification.
5. Parameter values.
6. Initial conditions.
7. Observations and predictions.
8. Uncertainty propagation.
9. Perturbation response.
10. Continuity and transition measurements.
11. Applicability region.
12. Known limitations.

Results should be reproducible using the original configuration and random seed.

⸻

9. Suggested Python project structure

relational-playground/
│
├── README.md
├── pyproject.toml
│
├── playground/
│   ├── system.py
│   ├── environment.py
│   ├── relationships.py
│   ├── boundaries.py
│   ├── controls.py
│   ├── continuity.py
│   ├── uncertainty.py
│   │
│   ├── equations/
│   │   ├── base.py
│   │   ├── linear.py
│   │   ├── nonlinear.py
│   │   ├── network.py
│   │   ├── energy.py
│   │   ├── boundary.py
│   │   └── stochastic.py
│   │
│   ├── experiments/
│   │   ├── runner.py
│   │   ├── perturbation.py
│   │   ├── sensitivity.py
│   │   ├── parameter_sweep.py
│   │   └── comparison.py
│   │
│   ├── analysis/
│   │   ├── applicability.py
│   │   ├── transitions.py
│   │   ├── identifiability.py
│   │   └── model_limits.py
│   │
│   └── reporting/
│       ├── results.py
│       └── provenance.py
│
├── experiments/
│   ├── boundary_variation/
│   ├── continuity/
│   ├── energy_constraints/
│   ├── relationship_dynamics/
│   └── model_comparison/
│
└── tests/
    ├── test_equations.py
    ├── test_boundaries.py
    ├── test_controls.py
    ├── test_uncertainty.py
    ├── test_continuity.py
    └── test_reproducibility.py

10. Implementation constraints

Initial implementation:

* Python standard library.
* No runtime network dependencies.
* Replaceable equation modules.
* Deterministic test fixtures.
* Explicit random seeds.
* No implicit defaults that convert unknowns into known values.
* No automatic model ranking.
* No automatic selection of system boundaries.
* No automatic exclusion of inconvenient observations.

Optional numerical libraries can be introduced later through adapters.

The initial laboratory should prioritize experimental integrity over computational sophistication.

⸻

11. Initial experimental sequence

Phase 1 — Establish the instrument

Build the system representation, relationship matrix, boundary matrix, control matrix, and uncertainty tracking.

Phase 2 — Equation substitution

Implement linear, nonlinear, network, and energy-balance models.

Verify that equations can be exchanged without changing the experiment runner.

Phase 3 — Boundary perturbation

Run identical systems with different boundary definitions.

Compare dependency classifications and resulting model behavior.

Phase 4 — Dynamic organization

Introduce changing boundaries, configuration transitions, and system continuity measurements.

Phase 5 — Context-dependent applicability

Determine which mathematical formulations remain useful under different physical and environmental conditions.

Phase 6 — Cross-system investigation

Apply the same experimental infrastructure to slime molds, forests, biological systems, and AI.

Do not assume that identical mathematical descriptions imply identical mechanisms.

⸻

12. Central research questions

The playground should ultimately investigate:

1. Can a system be described without assuming a fixed boundary?
2. Which relationships are necessary for particular forms of organization?
3. How does changing the boundary alter the apparent independence of a system?
4. Can system continuity persist through configuration discontinuity?
5. Where do different mathematical formulations become useful or cease to be useful?
6. Are there common mathematical structures across otherwise different physical systems?
7. Which observed similarities are genuine and which result from experimental selection?
8. Can uncertainty in boundary selection be propagated into uncertainty in model applicability?
9. Do boundary regions exhibit behaviors that cannot be predicted from interior measurements alone?
10. Can multiple competing models remain valid within different regions of the same experimental space?

13. Governing principle

The playground is an instrument for discovering applicability, not an instrument for confirming a predetermined ontology.

It must preserve:

* Multiple valid descriptions.
* Competing equations.
* Unresolved relationships.
* Context-dependent results.
* Boundary uncertainty.
* Failed predictions.
* Unexpected transitions.

The intended result is not one universal equation for intelligence or organization. It is an experimentally grounded map of where different equations, matrices, and system descriptions produce useful models, under what conditions, and with what uncertainty.
