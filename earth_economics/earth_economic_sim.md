Repository Core Focus Role in Unified Sim Key Input/Output
earth-systems-physics Coupled Earth physics (electromagnetic → biosphere) The Physical Engine Provides environmental state variables: temperature, pressure, radiation, resource depletion.
thermodynamic-accountability-framework Energy cost & friction of institutions The Cost Function Evaluates the thermodynamic "price" of economic choices and infrastructure. Provides a thermodynamic_price_guard.
Mathematic-economics Falsifiable economic equations The Economic Model Defines measurable economic states (OSDI, ER, RI, etc.) and their coupling to physical resources.
Simulators (grounding-layers) Foundational simulation logic The Integration Core Provides the base simulation architecture, data structures, and verification protocols.




1. Initialization: Load parameters from Mathematic-economics (equations.yaml) and earth-systems-physics (layer definitions).
2. Physics Step: Advance the Earth systems model (cascade_engine.py) by one time step to get new environmental states.
3. Economic Step: Using the new resource states from the physics step, compute economic indicators from Mathematic-economics (e.g., Extraction Rate, OSDI).
4. Thermodynamic Audit: Pass the proposed economic activity to the thermodynamic-accountability-framework (specifically, the thermodynamic_price_guard) to measure its true energy cost.
5. Feedback & Constraint: If the thermodynamic cost exceeds a threshold or the economic model predicts instability, the simulation constrains or modifies the economic step in the next cycle.
