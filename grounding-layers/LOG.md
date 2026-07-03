work from bottom to top on this page

# Reasoning Log: Probabilistic L1–L4 Conditioning

**Date:** 2026-07-02  
**Context:** After establishing a probabilistic L0 (physics likelihood), we extend the same approach upward through thermodynamics (L1), planetary mass balance (L2), ecological homeostasis (L3), and biomechanical constraints (L4). Each layer adds a log-likelihood term for the AI’s proposal, conditioning on the physical plausibility from below.  
**Status:** Design reasoning complete. Implementation stages proposed. L5 (pluralistic human constructs) will follow after this block.

---

## 1. General pattern

Every layer Ln (n ≥ 1) receives:
- The AI’s proposed plan (which may include trajectories, resource draws, or population manipulations).
- The physical likelihood (or trajectory sample) from L0.
- Any relevant outputs from intermediate layers.

It returns:
- A **conditional log-likelihood** `log p(proposal | Ln constraints, lower-layer states)`.
- Optionally, a corrected state estimate (the mode) for visualisation / enforcement.

The layers are designed to be **additive**: the total log-probability of a proposal across L0–L4 is the sum of the layer-specific terms (assuming conditional independence of violations given the lower-layer states). This is a product-of-experts structure.

Implementation can follow the same pattern as `ProbabilisticWorld`:

- A class for each layer with frozen constants and noise/deviation parameters.
- A `log_likelihood(...)` method.
- A thin inspector function that iterates over time steps (if dynamic) and accumulates the score.

---

## 2. L1 – Thermodynamics & Entropy

**Constraints (from README):**
- 2nd law: entropy generation must be non-negative on average.
- Battery depletion, Carnot ceiling (efficiency ≤ 1 – T_cold/T_hot).
- Energy books must close (no perpetual motion).

**Probabilistic treatment:**
- Entropy generation per step: compute `ΔS = (heat_in / T_hot) – (heat_out / T_cold)`. Expectation over noise can be modelled as a Gaussian around zero, with a sharp penalty if the mean falls significantly below zero.
- Carnot ceiling: proposed work extraction vs. maximum. Penalise with a logistic barrier: `log p ∝ –softplus(scale * (work – max_work))`.
- Battery depletion: track stored energy; if the proposal draws more energy than available, apply a heavy-tailed cost (e.g., negative log-likelihood grows quadratically beyond capacity).

**Key observation:**
L1 operates on energy flows and heat reservoirs. If the proposal is a trajectory of forces and velocities, we can compute work, heat dissipation, and entropy from the physical state (already available from L0). So L1’s `log_likelihood` can take the L0 physical states (or just the proposed forces/velocities) and add its own thermal accounting.

**Stage:**  
Add a `ThermodynamicsAuditor` class with `log_likelihood(pos, vel, force, battery_state, reservoir_temps)` that returns a scalar. The `__main__` demo can be extended to include a simple battery and two thermal reservoirs.

---

## 3. L2 – Planetary Mass Balance

**Constraints:**
- Finite pools: water, soil, minerals, carbon.
- Heat budget (radiative balance).

**Probabilistic treatment:**
- The proposal likely involves resource extraction/consumption rates. For each resource, model a log-probability that proposed consumption exceeds available stock: `log p(consumption) ∝ –(consumption / stock)^2` or a similar logistic penalty as stock approaches zero.
- Heat budget: if the plan emits waste heat, compare to radiative cooling capacity. Soft penalty for exceeding the planetary energy balance.
- Noise parameters represent measurement uncertainty in global inventories.

**Scope:**  
This layer will often act on aggregate quantities over a plan’s entire horizon, not per-timestep. The inspector can sum resource uses and evaluate a final score. Alternatively, it can penalise the *cumulative* overdraft.

**Implementation idea:**  
`PlanetaryMassAuditor` takes a proposed extraction schedule (e.g., kg/year of lithium, gigatonnes of CO₂) and returns a log-likelihood. It may also call L0 to ensure that the plan’s energy demands (e.g., mining energy) are physically plausible – thus, it conditions on the physical likelihood.

---

## 4. L3 – Ecological Homeostasis

**Constraints:**
- Allometric scaling laws.
- Lotka-Volterra dynamics (predator-prey oscillations bounded).
- ~10% trophic transfer efficiency.
- Extinction cascades (thresholds on population sizes).

**Probabilistic treatment:**
- Given a proposed intervention (e.g., harvest rates, habitat destruction), the auditor runs a simplified ecosystem model (maybe a few species) and compares predicted population trajectories to viability thresholds.
- For each species, probability of persistence can be modelled as a soft function of minimum population size over time. Extinction cascade risk: if one keystone species drops below a critical level, add a large penalty.
- Log-likelihood can be the joint probability that all populations remain above viable levels, assuming stochastic demographic/environmental noise.

**Important nuance:**  
L3’s model itself is uncertain (Lε again). The auditor can incorporate structural uncertainty by having multiple possible ecosystem models and marginalising over them, but for the first pass, a single deterministic model with process noise suffices.

**Implementation:**  
`EcologicalHomeostasisAuditor` with `log_likelihood(intervention_schedule)` that runs a Lotka-Volterra simulation and returns a score based on minimum population thresholds.

---

## 5. L4 – Biomechanical Sensorimotor

**Constraints:**
- Joint limits, grip strength, neural latency (~50–200 ms).
- Thermal tolerance (e.g., core temperature ≤ 40°C).
- Sustained power output ≤ 200 W (human baseline).

**Probabilistic treatment:**
- These are agent-specific constraints that can be applied to the physical trajectory from L0. The L0 inspector already works on a point mass; L4 can check if the required joint torques, reaction times, and metabolic power exceed human capabilities.
- For example, given a velocity profile, compute required limb accelerations; if they imply joint angles beyond anatomical limits, penalise.
- Thermal tolerance: a simple two-compartment heat model. If core temperature drifts beyond bounds, add penalty.
- Neural latency: if the AI’s proposed control loop requires reaction faster than a threshold, penalise heavily (since it violates sensorimotor reality).

**Implementation:**  
`BiomechanicalAuditor` that takes the agent’s trajectory (pos, vel, forces) and a set of body parameters, then returns a log-likelihood based on feasible effort, power, and thermal profiles.

---

## 6. Integration and stacking

Once each layer has its own `log_likelihood` method, a master inspector can iterate over the plan and accumulate:



# Reasoning Log: Probabilistic L0 Foundation

**Date:** 2026-07-02  
**Context:** Conversation on evolving L0 from deterministic hard-gate to a probability matrix, prompted by the insight that a binary inspector is brittle and that Lε already models the measurement-truth gap.  
**Status:** Reasoning complete; next step is staged implementation.

---

## 1. Why Probabilistic?

The existing L0 inspector makes binary reject/accept decisions based on hard thresholds (speed ≤ 2.0 m/s, finite-state check, energy conservation). This has two weaknesses:

- **Over-rejection** – Valid proposals with tiny numerical noise or sensor error are flagged as violations.
- **False confidence** – A proposal that passes exactly on the boundary is treated as fully valid, ignoring that it sits at the edge of feasibility.

Since Lε already acknowledges that all observations are mediated by imperfect instruments, the physical layer’s enforcement should reflect that uncertainty. A probabilistic L0 produces a **plausibility score** (log-likelihood) rather than a pass/fail flag. This makes the entire stack:

- **Graceful under noise** – small errors reduce likelihood but don’t cause immediate rejection.
- **Ready for Bayesian stacking** – higher layers can condition on the physical likelihood, turning the pyramid into a hierarchical probabilistic filter.
- **Auditable** – frozen constants extend to noise parameters; refutable claims become statistical (e.g., “a violation of energy conservation by more than 3σ reduces log-likelihood by at least X dB”).

---

## 2. What “Probability Matrix” Means Here

In the context of L0, a probability matrix is a **transition density**:  
`p( next_pos, next_vel | current_pos, current_vel, applied_force, physics_params, noise_params )`

The inspector no longer selects a single “corrected” state. Instead, it evaluates the **likelihood** of the AI’s proposed next state under true physics plus measurement noise. The most probable state (the mode) can still be used for correction if needed, but the primary output becomes a **trajectory log-probability**.

---

## 3. Design Constraints (Preserving Audit-Grade Integrity)

- **Frozen constants**: physical constants (mass, dt, max_speed) remain frozen. Noise standard deviations (`pos_sigma`, `vel_sigma`, `energy_sigma`, `accel_sigma`) become additional frozen estimates.
- **Scope**: the probabilistic inspector extends `PhysicalWorld`, leaving the original deterministic one intact for backward compatibility and test continuity.
- **Claims**: new claims (`GL_L0_P001`…) will pin the statistical behavior, e.g., “Given a teleport of 1 m, log-likelihood drops by >20 units.”
- **Lε alignment**: the noise parameters are part of the instrument model (Lε). They can be tied to a specific sensor configuration declared in the Lε simulator later.
- **No hard rejections**: a proposal is not “rejected” inside L0. It accumulates a score. Rejection thresholds, if desired, move to a higher-level orchestration layer that aggregates scores from L0…L5.

---

## 4. Implementation Stages (Context-Friendly)

### Stage 4.1 – Soften existing constraints (minimal diff)
Replace the hard `is_valid_state` checks inside a new subclass `ProbabilisticWorld` with Gaussian log-likelihoods for position continuity, velocity smoothness, and energy conservation, plus a smooth logistic barrier for the speed limit. The inspector loop becomes a **log-probability accumulator**.

### Stage 4.2 – Probabilistic inspector function
A new `l0_probabilistic_inspector` that returns `(corrected_traj, log_probs)` – where `log_probs[i]` is the log-likelihood of the AI’s state at step `i` given physics and noise. The corrected trajectory is the mode (true physics) blended as before for visualisation.

### Stage 4.3 – Claims and tests
Add `GL_L0_P001` through `P004` to CLAIMS.md, freezing noise constants and asserting log-likelihood thresholds for known hallucination patterns. Write audit tests (e.g., teleport by 1 m yields logp decrease > X). These tests will live in `tests/test_l0_probabilistic.py`.

### Stage 4.4 – Visualisation update
The `__main__` demo still runs, but instead of binary violation flags, we plot the log-probability trace and highlight where scores plummet.

---

## 5. How This Cascades Upward

With a probabilistic L0:
- **L1** receives a likelihood-weighted set of possible microstates, not a single trajectory. The entropy generation check becomes an expectation.
- **L2** can ask: “Given the probability that the physical plan exceeds mass limits, what is the risk of resource depletion?”
- **L5** finally sees a **Bayesian risk** of physical infeasibility, enabling culturally-aware decisions that still respect the hard floors.
- The entire stack becomes a **hierarchical Bayesian model**, which is the natural way to combine hard constraints with measurement noise.

---

## 6. Open Questions (for later)

- Should the speed-limit barrier be logistic or a soft-box prior? Both are options; the logistic is smoother and easier to differentiate if we ever want gradient-based planning.
- How to propagate uncertainty through L3’s ecological model? Likely via Monte Carlo sampling from the physical posterior.
- At what total log-likelihood does the system trigger an audit alarm? This is a policy decision best left to the orchestration layer.

---

## 7. Immediate Next Action

1. Draft `probabilistic_world.py` (or extend `l0_physics_causality.py` with the new subclass) using the sketched `log_likelihood` method.
2. Write a short demo script that runs the same AI hallucination through the probabilistic inspector and prints the per-step log-probabilities.
3. Once stable, freeze noise constants and document in CLAIMS.md.

---

*This log is a living document; update it as implementation reveals new edge cases or constraints.*
