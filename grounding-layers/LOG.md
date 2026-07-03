work from bottom to top on this page

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
