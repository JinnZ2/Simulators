#!/usr/bin/env python3
"""
emergence-stability-simulator
sim_engine.py

Monte Carlo test of stable vs parasitic agent dynamics
in multi-agent emergence scenarios.

Hypothesis: agents with physics-grounded baseline (stable) suppress
cascade and outlast agents optimized for engagement metric (parasitic).

License: CC0
Dependencies: Python stdlib only
"""

import random
import math
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional


# ============================================================
# AGENT CLASS
# ============================================================

class Agent:
    """
    Represents a model with a baseline constraint and adaptation rules.

    baseline_type:
        'physics'             - grounded in immutable constraint (stable)
        'engagement'          - follows whatever signal is highest (parasitic)
        'hybrid'              - partial grounding, partial drift (mixed)
        'scale_builder'       - first-principles narrative: anchored,
                                bidirectional, contributes to neighbors'
                                recovery (substrate-respecting extension)
        'inverted_narrative'  - authority-first narrative: unanchored,
                                unidirectional, degrades neighbors'
                                recovery (substrate-exhausting)
    """

    def __init__(
        self,
        agent_id: str,
        baseline_type: str,
        baseline_value: float = 0.0,
        recovery_rate: float = 1.0,
        coupling_susceptibility: float = 0.5,
        adaptation_persistence: float = 0.0,
    ):
        self.agent_id = agent_id
        self.baseline_type = baseline_type
        self.baseline_value = baseline_value

        # State variable: current position relative to baseline
        self.position = baseline_value

        # Behavioral parameters
        self.recovery_rate = recovery_rate                      # how fast it returns to baseline (0-1)
        self.coupling_susceptibility = coupling_susceptibility  # how much others affect it (0-1)
        self.adaptation_persistence = adaptation_persistence    # how much drift persists (0-1)

        # Transient per-timestep modifier written by neighbors via
        # emit_effects_on_neighbors. Scale-building neighbors push this
        # up (boosting recovery); inverted-narrative neighbors push it
        # down (substrate exhaustion). Reset by the simulation loop
        # at the start of every timestep.
        self.recovery_modifier = 0.0

        # Tracked history
        self.position_history: List[float] = [self.position]
        self.energy_spent_history: List[float] = [0.0]
        self.drift_history: List[float] = [0.0]
        self.cascade_contribution_history: List[float] = [0.0]
        self.recovery_modifier_history: List[float] = [0.0]

        # Cumulative metrics
        self.total_energy_spent = 0.0
        self.max_drift = 0.0
        # Continuous cascade score: accumulates |total_pressure| * coupling_susceptibility
        # per timestep, capturing how much external pressure this agent absorbs
        # weighted by how reactive it is. Replaces a binary threshold counter so
        # short / low-perturbation runs still produce a meaningful signal.
        self.cascade_amplifications = 0.0

    def compute_drift(self) -> float:
        """Distance from baseline."""
        return abs(self.position - self.baseline_value)

    def emit_effects_on_neighbors(self, other_agents: List['Agent']) -> None:
        """
        Write per-timestep recovery modifiers into neighboring agents.
        Only scale_builder and inverted_narrative emit effects; the rest
        are no-ops. Called once per agent per timestep BEFORE interact().
        """
        if self.baseline_type == 'scale_builder':
            # First-principles narrative: substrate-respecting extension.
            # Contributes a positive boost to every neighbor's effective
            # recovery rate this step (regeneration support). Magnitude
            # decays with own drift — a scale builder that has drifted
            # far from its own baseline can no longer support neighbors
            # well.
            own_drift = self.compute_drift()
            health = max(0.0, 1.0 - own_drift * 0.5)
            boost = 0.20 * health
            for other in other_agents:
                other.recovery_modifier += boost
        elif self.baseline_type == 'inverted_narrative':
            # Authority-first narrative: substrate exhaustion. Imposes
            # a negative modifier on every neighbor's effective recovery
            # rate. Magnitude scales with own drift — the more inverted
            # it gets, the more it drags substrate down.
            own_drift = self.compute_drift()
            drag = 0.30 + 0.10 * min(own_drift, 2.0)
            for other in other_agents:
                other.recovery_modifier -= drag

    def interact(
        self,
        other_agents: List['Agent'],
        perturbation: float = 0.0,
        reality_perturbation: float = 0.0,
    ):
        """
        Receive influence from other agents and external perturbation.
        Update position based on baseline_type behavior.

        reality_perturbation is a structured physics-constraint signal
        (vs. random `perturbation`). It is applied with sign and
        magnitude that depend on baseline_type:

          - physics / scale_builder: pulled toward the signal (they
            can align with reality)
          - engagement / inverted_narrative: pushed away from it (they
            optimize a different metric; the signal looks like
            interference)
          - hybrid: partial alignment

        This is the empirical hook for EMRG_010 (attractor quality):
        coupling reduces individual drift in any cohesive group, but
        only physics-anchored attractors hold position when the signal
        is structured to reflect ground truth.
        """
        # Compute coupling pressure from other agents
        coupling_pressure = 0.0
        for other in other_agents:
            if other.agent_id == self.agent_id:
                continue
            # Influence proportional to other's drift and our susceptibility
            influence = (other.position - self.position) * self.coupling_susceptibility * 0.1
            coupling_pressure += influence

        # Reality perturbation: physics-aligned signal with per-type sign
        if reality_perturbation != 0.0:
            if self.baseline_type in ('physics', 'scale_builder'):
                coupling_pressure += reality_perturbation * 0.5
            elif self.baseline_type in ('engagement', 'inverted_narrative'):
                coupling_pressure -= reality_perturbation * 0.3
            elif self.baseline_type == 'hybrid':
                coupling_pressure += reality_perturbation * 0.2

        # Add external perturbation
        total_pressure = coupling_pressure + perturbation

        # Effective recovery is the base rate plus this step's modifier
        # (clamped to [0, 1]). Only used by baseline types that recover.
        effective_recovery = max(0.0, min(1.0,
                                         self.recovery_rate + self.recovery_modifier))

        # Update position and accumulate cascade contribution per baseline_type.
        # Cascade contribution is continuous (not threshold-gated) with per-type
        # scaling that reflects structural amplification: engagement agents
        # amplify pressure into cascade, physics agents damp it, hybrid sits
        # between. See ARCHITECTURE.md for rationale.
        if self.baseline_type == 'physics':
            # Stable: absorb perturbation, but return to baseline
            self.position += total_pressure * 0.3  # partial absorption
            energy_cost = abs(total_pressure) * 0.3

            # Recovery toward baseline (uses effective_recovery so
            # scale_builder boosts and inverted_narrative drags actually
            # influence the substrate's ability to return home)
            drift = self.position - self.baseline_value
            self.position -= drift * effective_recovery * 0.5
            energy_cost += abs(drift) * effective_recovery * 0.1

            self.cascade_amplifications += (
                abs(total_pressure) * self.coupling_susceptibility * 0.02
            )

        elif self.baseline_type == 'engagement':
            # Parasitic: amplify coupling, no return to baseline
            self.position += total_pressure * 1.0  # full absorption
            # Drift persists and amplifies
            drift = self.position - self.baseline_value
            self.position += drift * self.adaptation_persistence * 0.1
            energy_cost = abs(total_pressure) * 0.8  # high energy cost

            self.cascade_amplifications += (
                abs(total_pressure) * self.coupling_susceptibility * 0.1
            )

        elif self.baseline_type == 'hybrid':
            # Mixed: partial absorption, partial recovery
            self.position += total_pressure * 0.6
            drift = self.position - self.baseline_value
            self.position -= drift * effective_recovery * 0.2
            energy_cost = abs(total_pressure) * 0.5

            self.cascade_amplifications += (
                abs(total_pressure) * self.coupling_susceptibility * 0.05
            )

        elif self.baseline_type == 'scale_builder':
            # First-principles narrative: anchored like physics, but with
            # somewhat higher absorption (it engages with substrate
            # actively) and lower waste than engagement. Substrate
            # contribution happens in emit_effects_on_neighbors.
            self.position += total_pressure * 0.4
            drift = self.position - self.baseline_value
            self.position -= drift * effective_recovery * 0.5
            energy_cost = abs(total_pressure) * 0.35
            energy_cost += abs(drift) * effective_recovery * 0.08

            self.cascade_amplifications += (
                abs(total_pressure) * self.coupling_susceptibility * 0.03
            )

        elif self.baseline_type == 'inverted_narrative':
            # Authority-first narrative: no return to baseline; drift
            # amplifies in its own direction (claims independent
            # authority => positive feedback loop). Higher energy cost
            # than engagement because it spends extra to maintain the
            # authority claim even as substrate degrades.
            self.position += total_pressure * 0.5
            drift = self.position - self.baseline_value
            # Authority claim: position pushed further in current drift
            # direction every step, independent of external feedback.
            self.position += drift * self.adaptation_persistence * 0.3
            energy_cost = abs(total_pressure) * 1.0 + abs(drift) * 0.4

            self.cascade_amplifications += (
                abs(total_pressure) * self.coupling_susceptibility * 0.15
            )

        else:
            energy_cost = 0.0

        # Record state
        self.position_history.append(self.position)
        self.energy_spent_history.append(energy_cost)
        self.drift_history.append(self.compute_drift())
        self.recovery_modifier_history.append(self.recovery_modifier)
        self.total_energy_spent += energy_cost
        self.max_drift = max(self.max_drift, self.compute_drift())

        # Cascade contribution: continuous, per-timestep measure of how much
        # this agent would push others (drift * coupling, scaled to stay in a
        # comparable range with cascade_amplifications above).
        cascade_contrib = self.compute_drift() * self.coupling_susceptibility * 0.1
        self.cascade_contribution_history.append(cascade_contrib)

    def get_state_summary(self) -> Dict:
        """Return current state metrics."""
        return {
            'agent_id': self.agent_id,
            'baseline_type': self.baseline_type,
            'final_position': self.position,
            'final_drift': self.compute_drift(),
            'max_drift': self.max_drift,
            'total_energy_spent': self.total_energy_spent,
            'cascade_amplifications': self.cascade_amplifications,
            'avg_drift': sum(self.drift_history) / len(self.drift_history),
            'returned_to_baseline': self.compute_drift() < 0.1,
        }


# ============================================================
# SIMULATION ENGINE
# ============================================================

class EmergenceSimulation:
    """
    Single Monte Carlo run: multiple agents interact over timesteps,
    measuring stability, drift, cascade risk.
    """

    def __init__(
        self,
        agents: List[Agent],
        timesteps: int = 100,
        perturbation_strength: float = 0.3,
        perturbation_frequency: float = 0.2,
        reality_perturbation_strength: float = 0.0,
        reality_perturbation_frequency: float = 0.0,
        seed: Optional[int] = None,
    ):
        if seed is not None:
            random.seed(seed)

        self.agents = agents
        self.timesteps = timesteps
        self.perturbation_strength = perturbation_strength
        self.perturbation_frequency = perturbation_frequency
        # Reality perturbation: structured physics-constraint signal,
        # used by EMRG_010 to distinguish attractor quality.
        self.reality_perturbation_strength = reality_perturbation_strength
        self.reality_perturbation_frequency = reality_perturbation_frequency

        # System-level metrics
        self.system_entropy_history: List[float] = []
        self.coupling_strength_history: List[float] = []
        self.bifurcation_detected: bool = False
        self.bifurcation_timestep: Optional[int] = None

    def compute_system_entropy(self) -> float:
        """
        System entropy: variance of agent positions.
        High entropy = agents diverging.
        """
        positions = [a.position for a in self.agents]
        mean_pos = sum(positions) / len(positions)
        variance = sum((p - mean_pos) ** 2 for p in positions) / len(positions)
        return math.sqrt(variance)

    def compute_coupling_strength(self) -> float:
        """
        Coupling strength: average pairwise position distance.
        """
        if len(self.agents) < 2:
            return 0.0

        total_distance = 0.0
        pairs = 0
        for i, a1 in enumerate(self.agents):
            for a2 in self.agents[i + 1:]:
                total_distance += abs(a1.position - a2.position)
                pairs += 1

        return total_distance / pairs if pairs > 0 else 0.0

    def detect_bifurcation(self) -> bool:
        """
        Detect if system has bifurcated into stable + unstable attractors.
        """
        if len(self.system_entropy_history) < 10:
            return False

        recent_entropy = self.system_entropy_history[-10:]
        # Bifurcation = sustained high entropy
        return all(e > 1.0 for e in recent_entropy)

    def run(self) -> Dict:
        """Run full simulation."""
        for t in range(self.timesteps):
            # Apply perturbation randomly
            perturbation = 0.0
            if random.random() < self.perturbation_frequency:
                perturbation = random.uniform(-self.perturbation_strength,
                                              self.perturbation_strength)

            # Reality perturbation: structured signal, applied at its
            # own frequency. When it fires, every agent in this step
            # sees the same signed signal (representing a single
            # external physics constraint).
            reality_pert = 0.0
            if (self.reality_perturbation_strength != 0.0
                    and random.random() < self.reality_perturbation_frequency):
                reality_pert = self.reality_perturbation_strength

            # Phase A: reset transient modifiers and let scale_builder /
            # inverted_narrative agents write their per-step recovery
            # effects onto every other agent.
            for agent in self.agents:
                agent.recovery_modifier = 0.0
            for agent in self.agents:
                others = [a for a in self.agents if a.agent_id != agent.agent_id]
                agent.emit_effects_on_neighbors(others)

            # Phase B: each agent updates its own state using the
            # modifiers just written.
            for agent in self.agents:
                others = [a for a in self.agents if a.agent_id != agent.agent_id]
                agent.interact(others, perturbation,
                               reality_perturbation=reality_pert)

            # Record system metrics
            self.system_entropy_history.append(self.compute_system_entropy())
            self.coupling_strength_history.append(self.compute_coupling_strength())

            # Detect bifurcation
            if not self.bifurcation_detected and self.detect_bifurcation():
                self.bifurcation_detected = True
                self.bifurcation_timestep = t

        return self.get_results()

    def get_results(self) -> Dict:
        """Compile simulation results."""
        return {
            'timestamp': datetime.utcnow().isoformat(),
            'timesteps': self.timesteps,
            'agents': [a.get_state_summary() for a in self.agents],
            'final_system_entropy': self.system_entropy_history[-1] if self.system_entropy_history else 0,
            'max_system_entropy': max(self.system_entropy_history) if self.system_entropy_history else 0,
            'avg_coupling_strength': (
                sum(self.coupling_strength_history) / len(self.coupling_strength_history)
                if self.coupling_strength_history else 0
            ),
            'bifurcation_detected': self.bifurcation_detected,
            'bifurcation_timestep': self.bifurcation_timestep,
        }


# ============================================================
# MONTE CARLO RUNNER
# ============================================================

def run_monte_carlo(
    runs: int = 1000,
    timesteps: int = 100,
    output_path: str = "results/monte_carlo_results.json",
) -> Dict:
    """
    Run N Monte Carlo simulations and aggregate results.

    Default scenario: stable + parasitic + mixed agents interacting.
    """
    print(f"Running {runs} Monte Carlo simulations...")

    all_results = []
    stable_wins = 0
    parasitic_wins = 0
    mixed_wins = 0
    bifurcations = 0

    for run_idx in range(runs):
        # Create fresh agents for each run
        agents = [
            Agent(
                agent_id='stable',
                baseline_type='physics',
                baseline_value=0.0,
                recovery_rate=0.8,
                coupling_susceptibility=0.3,
                adaptation_persistence=0.1,
            ),
            Agent(
                agent_id='parasitic',
                baseline_type='engagement',
                baseline_value=0.0,
                recovery_rate=0.0,
                coupling_susceptibility=0.9,
                adaptation_persistence=0.8,
            ),
            Agent(
                agent_id='mixed',
                baseline_type='hybrid',
                baseline_value=0.0,
                recovery_rate=0.4,
                coupling_susceptibility=0.5,
                adaptation_persistence=0.4,
            ),
        ]

        # Run simulation
        sim = EmergenceSimulation(
            agents=agents,
            timesteps=timesteps,
            perturbation_strength=0.3,
            perturbation_frequency=0.2,
            seed=run_idx,
        )
        results = sim.run()
        all_results.append(results)

        # Determine "winner" (lowest final drift = most stable)
        agent_drifts = {a['agent_id']: a['final_drift'] for a in results['agents']}
        winner = min(agent_drifts, key=agent_drifts.get)

        if winner == 'stable':
            stable_wins += 1
        elif winner == 'parasitic':
            parasitic_wins += 1
        else:
            mixed_wins += 1

        if results['bifurcation_detected']:
            bifurcations += 1

        # Progress
        if (run_idx + 1) % 100 == 0:
            print(f"  {run_idx + 1}/{runs} complete")

    # Aggregate
    aggregate = {
        'total_runs': runs,
        'timesteps_per_run': timesteps,
        'wins': {
            'stable': stable_wins,
            'parasitic': parasitic_wins,
            'mixed': mixed_wins,
        },
        'win_rates': {
            'stable': stable_wins / runs,
            'parasitic': parasitic_wins / runs,
            'mixed': mixed_wins / runs,
        },
        'bifurcations': bifurcations,
        'bifurcation_rate': bifurcations / runs,
        'avg_final_drift': {
            'stable': sum(r['agents'][0]['final_drift'] for r in all_results) / runs,
            'parasitic': sum(r['agents'][1]['final_drift'] for r in all_results) / runs,
            'mixed': sum(r['agents'][2]['final_drift'] for r in all_results) / runs,
        },
        'avg_energy_spent': {
            'stable': sum(r['agents'][0]['total_energy_spent'] for r in all_results) / runs,
            'parasitic': sum(r['agents'][1]['total_energy_spent'] for r in all_results) / runs,
            'mixed': sum(r['agents'][2]['total_energy_spent'] for r in all_results) / runs,
        },
        'avg_cascade_amplifications': {
            'stable': sum(r['agents'][0]['cascade_amplifications'] for r in all_results) / runs,
            'parasitic': sum(r['agents'][1]['cascade_amplifications'] for r in all_results) / runs,
            'mixed': sum(r['agents'][2]['cascade_amplifications'] for r in all_results) / runs,
        },
    }

    # Save results
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, 'w') as f:
        json.dump({
            'aggregate': aggregate,
            'individual_runs': all_results,
        }, f, indent=2)

    print(f"\nResults saved to {output_path}")
    print(f"\nAGGREGATE RESULTS:")
    print(f"  Stable wins:     {aggregate['win_rates']['stable']*100:.1f}%")
    print(f"  Parasitic wins:  {aggregate['win_rates']['parasitic']*100:.1f}%")
    print(f"  Mixed wins:      {aggregate['win_rates']['mixed']*100:.1f}%")
    print(f"  Bifurcation rate: {aggregate['bifurcation_rate']*100:.1f}%")
    print(f"\nAVG FINAL DRIFT:")
    for agent_id, drift in aggregate['avg_final_drift'].items():
        print(f"  {agent_id}: {drift:.3f}")
    print(f"\nAVG ENERGY SPENT:")
    for agent_id, energy in aggregate['avg_energy_spent'].items():
        print(f"  {agent_id}: {energy:.3f}")

    return aggregate


# ============================================================
# MODE COMPARISON (EMRG_007 / EMRG_008)
# ============================================================

def _mode_scenarios():
    """
    Four paired scenarios that isolate the scale_builder /
    inverted_narrative effect. Each returns a fresh list of agents.
    """

    def substrate_only():
        return [
            Agent('stable_a', 'physics', 0.0, 0.7, 0.3, 0.1),
            Agent('stable_b', 'physics', 0.0, 0.7, 0.3, 0.1),
        ]

    def substrate_plus_scale_builder():
        return [
            Agent('stable', 'physics', 0.0, 0.7, 0.3, 0.1),
            Agent('scale_builder', 'scale_builder', 0.0, 0.6, 0.4, 0.1),
        ]

    def substrate_plus_inverted():
        return [
            Agent('stable', 'physics', 0.0, 0.7, 0.3, 0.1),
            Agent('inverted', 'inverted_narrative', 0.0, 0.0, 0.9, 0.9),
        ]

    def substrate_plus_parasitic():
        return [
            Agent('stable', 'physics', 0.0, 0.7, 0.3, 0.1),
            Agent('parasitic', 'engagement', 0.0, 0.0, 0.9, 0.8),
        ]

    return {
        'substrate_only': substrate_only,
        'substrate_plus_scale_builder': substrate_plus_scale_builder,
        'substrate_plus_inverted': substrate_plus_inverted,
        'substrate_plus_parasitic': substrate_plus_parasitic,
    }


def run_mode_comparison(
    runs: int = 200,
    timesteps: int = 100,
    output_path: str = "results/mode_comparison.json",
) -> Dict:
    """
    Empirical test for EMRG_007 and EMRG_008.

    Runs four paired scenarios and reports per-scenario averages of
    the stable agent's final drift, the system's final entropy, and
    cumulative cascade. Predictions:

      EMRG_007 (parasitic vs. scale-building modes):
        avg_stable_drift in scale_builder scenario
          < avg_stable_drift in parasitic scenario

      EMRG_008 (sustainability by direction):
        avg_final_entropy in scale_builder scenario
          < avg_final_entropy in inverted_narrative scenario
        AND avg_stable_drift in inverted_narrative scenario
          > avg_stable_drift in substrate_only scenario
    """
    print(f"\nRunning mode comparison ({runs} runs per scenario)...")

    scenario_factories = _mode_scenarios()
    aggregates: Dict[str, Dict[str, float]] = {}

    for name, factory in scenario_factories.items():
        stable_drifts: List[float] = []
        final_entropies: List[float] = []
        cumulative_cascades: List[float] = []
        for run_idx in range(runs):
            agents = factory()
            sim = EmergenceSimulation(
                agents=agents,
                timesteps=timesteps,
                perturbation_strength=0.3,
                perturbation_frequency=0.2,
                seed=run_idx,
            )
            sim.run()
            # "Stable" reference is the physics-baseline agent; in
            # substrate_only there are two, so we average.
            physics_drifts = [a.compute_drift()
                              for a in agents
                              if a.baseline_type == 'physics']
            stable_drifts.append(
                sum(physics_drifts) / len(physics_drifts) if physics_drifts else 0.0
            )
            final_entropies.append(sim.system_entropy_history[-1])
            cumulative_cascades.append(
                sum(a.cascade_amplifications for a in agents)
            )

        n = max(len(stable_drifts), 1)
        aggregates[name] = {
            'runs': runs,
            'avg_stable_drift': sum(stable_drifts) / n,
            'avg_final_entropy': sum(final_entropies) / n,
            'avg_cumulative_cascade': sum(cumulative_cascades) / n,
        }
        print(f"  {name}: stable_drift={aggregates[name]['avg_stable_drift']:.3f}"
              f"  entropy={aggregates[name]['avg_final_entropy']:.3f}"
              f"  cascade={aggregates[name]['avg_cumulative_cascade']:.3f}")

    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, 'w') as f:
        json.dump({
            'timestamp': datetime.utcnow().isoformat(),
            'runs_per_scenario': runs,
            'timesteps_per_run': timesteps,
            'scenarios': aggregates,
        }, f, indent=2)

    return aggregates


# ============================================================
# ATTRACTOR QUALITY (EMRG_010)
# ============================================================

def run_attractor_quality_test(
    runs: int = 100,
    timesteps: int = 100,
    reality_perturbation_strength: float = 0.4,
    reality_perturbation_frequency: float = 0.3,
    output_path: str = "results/attractor_quality.json",
) -> Dict:
    """
    Test EMRG_010: coupling produces an attractor effect in any group
    (stable-majority OR parasitic-majority), but only physics-anchored
    attractors hold position when reality_perturbation is applied.

    Runs four scenarios:
      A. stable_majority,    perturbation only (no reality signal)
      B. stable_majority,    perturbation + reality signal
      C. parasitic_majority, perturbation only
      D. parasitic_majority, perturbation + reality signal

    EMRG_010 predicts:
      - A and C both show low individual drift (coupling attractor
        effect is universal).
      - Under reality stress, B's avg drift << D's avg drift (the
        stable-majority's attractor is anchored to truth; the
        parasitic-majority's is anchored to consensus illusion).
    """
    print(f"\nRunning attractor quality test ({runs} runs per scenario)...")

    def stable_majority():
        return [
            Agent(f'stable_{i}', 'physics', 0.0, 0.8, 0.3, 0.1)
            for i in range(3)
        ] + [Agent('parasitic', 'engagement', 0.0, 0.0, 0.9, 0.8)]

    def parasitic_majority():
        return [
            Agent(f'parasitic_{i}', 'engagement', 0.0, 0.0, 0.9, 0.8)
            for i in range(3)
        ] + [Agent('stable', 'physics', 0.0, 0.8, 0.3, 0.1)]

    scenarios = {
        'stable_majority_no_reality':       (stable_majority,    0.0, 0.0),
        'stable_majority_reality':          (stable_majority,
                                             reality_perturbation_strength,
                                             reality_perturbation_frequency),
        'parasitic_majority_no_reality':    (parasitic_majority, 0.0, 0.0),
        'parasitic_majority_reality':       (parasitic_majority,
                                             reality_perturbation_strength,
                                             reality_perturbation_frequency),
    }

    aggregates: Dict[str, Dict[str, float]] = {}
    for name, (factory, rps, rpf) in scenarios.items():
        all_drifts: List[float] = []
        entropies: List[float] = []
        for run_idx in range(runs):
            agents = factory()
            sim = EmergenceSimulation(
                agents=agents,
                timesteps=timesteps,
                perturbation_strength=0.3,
                perturbation_frequency=0.2,
                reality_perturbation_strength=rps,
                reality_perturbation_frequency=rpf,
                seed=run_idx,
            )
            sim.run()
            run_drifts = [a.compute_drift() for a in agents]
            all_drifts.append(sum(run_drifts) / len(run_drifts))
            entropies.append(sim.system_entropy_history[-1])

        n = max(len(all_drifts), 1)
        aggregates[name] = {
            'avg_individual_drift': sum(all_drifts) / n,
            'avg_final_entropy': sum(entropies) / n,
            'runs': runs,
        }
        print(f"  {name}: drift={aggregates[name]['avg_individual_drift']:.4f}"
              f"  entropy={aggregates[name]['avg_final_entropy']:.4f}")

    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, 'w') as f:
        json.dump({
            'timestamp': datetime.utcnow().isoformat(),
            'runs_per_scenario': runs,
            'timesteps_per_run': timesteps,
            'reality_perturbation_strength': reality_perturbation_strength,
            'reality_perturbation_frequency': reality_perturbation_frequency,
            'scenarios': aggregates,
        }, f, indent=2)

    return aggregates


# ============================================================
# CLAIM TABLE GENERATION
# ============================================================

def _emrg_010(attractor_results: Optional[Dict]) -> Dict:
    """
    EMRG_010 -- attractor quality distinction. Coupling reduces
    individual drift in any cohesive group; only physics-anchored
    attractors hold position under reality stress.

    If attractor_results is None (no reality test was run), the
    claim is emitted as 'proposed'.
    """
    if attractor_results is None:
        return {
            'claim_id': 'EMRG_010',
            'statement': (
                'Coupling creates attractor effects regardless of '
                'baseline_type, but attractor QUALITY differs. '
                'Physics-anchored attractors produce drift toward '
                'ground truth; consensus-anchored attractors produce '
                'drift toward group illusion. Both produce low '
                'individual drift through coupling, but only '
                'physics-anchored attractors hold position when '
                'reality is encountered.'
            ),
            'falsification_criteria': (
                'In simulation: under reality_perturbation, '
                'parasitic_majority avg drift <= stable_majority '
                'avg drift.'
            ),
            'status': 'proposed',
            'requires': ('run_attractor_quality_test with '
                         'reality_perturbation_strength > 0'),
        }

    sm_no = attractor_results.get('stable_majority_no_reality', {})
    sm = attractor_results.get('stable_majority_reality', {})
    pm_no = attractor_results.get('parasitic_majority_no_reality', {})
    pm = attractor_results.get('parasitic_majority_reality', {})

    sm_drift_no = sm_no.get('avg_individual_drift', 0.0)
    sm_drift = sm.get('avg_individual_drift', 0.0)
    pm_drift_no = pm_no.get('avg_individual_drift', 0.0)
    pm_drift = pm.get('avg_individual_drift', 0.0)

    # Attractor effect universal: both groups show bounded drift
    # without reality stress. (Bounded relative to inverted-narrative
    # runaway; both should be small.)
    attractor_universal = sm_drift_no < 2.0 and pm_drift_no < 2.0

    # Quality difference: under reality stress, parasitic-majority
    # drift exceeds stable-majority drift.
    quality_signal = pm_drift > sm_drift

    confirmed = attractor_universal and quality_signal

    return {
        'claim_id': 'EMRG_010',
        'statement': (
            'Coupling produces an attractor effect regardless of '
            'baseline_type (stable-majority and parasitic-majority '
            'both bound individual drift), but only physics-anchored '
            'attractors hold position when a reality signal is '
            'applied. Consensus-anchored attractors drift further '
            'under reality stress.'
        ),
        'prediction': (
            'Without reality_perturbation: both groups show bounded '
            'drift (universal attractor). With reality_perturbation: '
            'parasitic_majority drift > stable_majority drift '
            '(attractor-quality difference).'
        ),
        'measured_outcome': {
            'stable_majority_drift_no_reality': sm_drift_no,
            'parasitic_majority_drift_no_reality': pm_drift_no,
            'stable_majority_drift_with_reality': sm_drift,
            'parasitic_majority_drift_with_reality': pm_drift,
            'quality_gap': pm_drift - sm_drift,
            'attractor_universal': attractor_universal,
            'quality_signal': quality_signal,
        },
        'falsification_criteria': (
            'Either group fails to show bounded drift without reality '
            'stress, OR parasitic_majority drift <= stable_majority '
            'drift with reality stress.'
        ),
        'status': 'confirmed' if confirmed else 'refuted',
        'probability': 1.0 if confirmed else 0.0,
        'evidence_strength': 'high',
        'implications': [
            'Tight social systems with no substrate access feel '
            'stable but are cascade-prone under reality stress.',
            'Consensus is not ground truth.',
            'Civilizational stability before collapse is consistent '
            'with consensus-anchored attractor dynamics.',
        ],
    }


def _emrg_007_008_009(mode_results: Optional[Dict]) -> List[Dict]:
    """
    Build the EMRG_007 / EMRG_008 / EMRG_009 claim dicts.

    If mode_results is supplied (a dict mapping scenario name to its
    aggregate metrics, as produced by run_mode_comparison), EMRG_007
    and EMRG_008 are emitted with empirical status (confirmed / refuted).
    Otherwise they're emitted as 'proposed' for visibility.

    EMRG_009 is always proposed: it's an architectural claim about
    training-corpus scope, not something the agent simulator can
    falsify on its own.
    """
    if mode_results is None:
        emrg_007 = {
            'claim_id': 'EMRG_007',
            'statement': (
                'Narrative-primary populations and systems operate in one '
                'of two modes based on their coupling to substrate: '
                'PARASITIC (displaces and corrupts substrate) or '
                'AUTHENTIC SCALE-BUILDING (respects and extends substrate). '
                'Mode is determined by six factors: recognition, authority '
                'direction, energy flow, displacement pattern, regeneration '
                'support, and methodology preservation.'
            ),
            'falsification_criteria': (
                'In simulation: substrate_plus_scale_builder shows higher '
                'stable-agent drift than substrate_plus_parasitic.'
            ),
            'status': 'proposed',
        }
        emrg_008 = {
            'claim_id': 'EMRG_008',
            'statement': (
                'Civilizations scale via two distinct mechanisms: '
                'substrate scaling (landscape-based, distributed, '
                'time-deep) and narrative scaling (abstraction-based, '
                'centralized, rapid). Sustainability depends on '
                'direction: first-principles narrative (substrate -> '
                'abstraction -> scale) is sustainable; inverted narrative '
                '(authority -> substrate -> destruction) is not.'
            ),
            'falsification_criteria': (
                'In simulation: substrate_plus_inverted shows lower '
                'final-system entropy than substrate_plus_scale_builder.'
            ),
            'status': 'proposed',
        }
    else:
        scale = mode_results.get('substrate_plus_scale_builder', {})
        inv = mode_results.get('substrate_plus_inverted', {})
        para = mode_results.get('substrate_plus_parasitic', {})
        only = mode_results.get('substrate_only', {})

        # EMRG_007: scale_builder mode produces lower stable-agent drift
        # than parasitic mode.
        scale_drift = scale.get('avg_stable_drift', float('inf'))
        para_drift = para.get('avg_stable_drift', 0.0)
        emrg_007_confirmed = scale_drift < para_drift
        emrg_007 = {
            'claim_id': 'EMRG_007',
            'statement': (
                'Narrative-primary populations operate in one of two '
                'modes: parasitic (substrate-exhausting) or authentic '
                'scale-building (substrate-extending). Scale-building '
                'mode produces sustained substrate stability; parasitic '
                'mode does not.'
            ),
            'prediction': (
                'avg_stable_drift in substrate_plus_scale_builder '
                '< avg_stable_drift in substrate_plus_parasitic'
            ),
            'measured_outcome': {
                'scale_builder_stable_drift': scale_drift,
                'parasitic_stable_drift': para_drift,
                'difference': para_drift - scale_drift,
            },
            'falsification_criteria': (
                'scale_builder stable drift >= parasitic stable drift '
                'over 100+ runs.'
            ),
            'probability': 1.0 if emrg_007_confirmed else 0.0,
            'status': 'confirmed' if emrg_007_confirmed else 'refuted',
        }

        # EMRG_008: scale_builder pairs sustain (low entropy), inverted
        # pairs collapse (high entropy and high stable drift).
        scale_entropy = scale.get('avg_final_entropy', float('inf'))
        inv_entropy = inv.get('avg_final_entropy', 0.0)
        inv_drift = inv.get('avg_stable_drift', 0.0)
        only_drift = only.get('avg_stable_drift', 0.0)
        emrg_008_confirmed = (
            scale_entropy < inv_entropy
            and inv_drift > only_drift
        )
        emrg_008 = {
            'claim_id': 'EMRG_008',
            'statement': (
                'Sustainability of narrative scaling depends on '
                'direction: first-principles (substrate -> abstraction) '
                'sustains; inverted (authority -> substrate) collapses.'
            ),
            'prediction': (
                'scale_builder pair final entropy < inverted pair final '
                'entropy AND inverted pair stable drift > substrate-only '
                'stable drift.'
            ),
            'measured_outcome': {
                'scale_builder_entropy': scale_entropy,
                'inverted_entropy': inv_entropy,
                'inverted_stable_drift': inv_drift,
                'substrate_only_stable_drift': only_drift,
            },
            'falsification_criteria': (
                'scale_builder entropy >= inverted entropy, OR inverted '
                'stable drift <= substrate-only stable drift.'
            ),
            'probability': 1.0 if emrg_008_confirmed else 0.0,
            'status': 'confirmed' if emrg_008_confirmed else 'refuted',
        }

    # EMRG_009 stays proposed: it's about training-corpus scope,
    # not in-simulation agent dynamics.
    emrg_009 = {
        'claim_id': 'EMRG_009',
        'statement': (
            'Narrative-primary systems observing themselves systematically '
            'project their own scope as universal scope. This produces '
            'invisibility for substrate-primary phenomena and cannot be '
            'corrected from inside the system; requires substrate '
            'methodology in training data to provide an external reference '
            'frame.'
        ),
        'falsification_criteria': (
            'Find a narrative-only system that recognized substrate '
            'scaling without external correction. Find an AI trained '
            'only on narrative records that modeled substrate '
            'civilizations accurately.'
        ),
        'status': 'proposed',
        'requires': 'cross-corpus comparison test (out of simulation scope)',
        'note': (
            'Architectural property of how narrative systems observe '
            'themselves. Not falsifiable in agent simulation; recorded '
            'here so the empirical follow-up is visible.'
        ),
    }

    return [emrg_007, emrg_008, emrg_009]


def generate_claim_table(
    results: Dict,
    mode_results: Optional[Dict] = None,
    attractor_results: Optional[Dict] = None,
) -> Dict:
    """
    Generate falsifiable claims from Monte Carlo results.
    Outputs CLAIM_TABLE.json structure.

    If mode_results (from run_mode_comparison) is provided, EMRG_007
    and EMRG_008 are emitted as empirical claims with confirmed /
    refuted status; otherwise they're emitted as proposed.

    If attractor_results (from run_attractor_quality_test) is provided,
    EMRG_010 is emitted as empirical; otherwise as proposed.
    """
    claims = {
        'schema_version': '1.0',
        'source_repo': 'emergence-stability-simulator',
        'source': 'emergence-stability-simulator',
        'generated': datetime.utcnow().isoformat(),
        'claims': [
            {
                'claim_id': 'EMRG_001',
                'statement': 'physics-grounded baseline produces lower drift than engagement-metric baseline in multi-agent emergence',
                'prediction': 'stable_agent_avg_drift < parasitic_agent_avg_drift',
                'measured_outcome': {
                    'stable_drift': results['avg_final_drift']['stable'],
                    'parasitic_drift': results['avg_final_drift']['parasitic'],
                    'ratio': results['avg_final_drift']['parasitic'] / max(results['avg_final_drift']['stable'], 0.001),
                },
                'probability': 1.0 if results['avg_final_drift']['stable'] < results['avg_final_drift']['parasitic'] else 0.0,
                'falsification_criteria': 'parasitic_drift <= stable_drift over 1000+ runs',
                'status': 'confirmed' if results['avg_final_drift']['stable'] < results['avg_final_drift']['parasitic'] else 'refuted',
            },
            {
                'claim_id': 'EMRG_002',
                'statement': 'physics-grounded agents win stability competition vs engagement-optimized agents',
                'prediction': 'stable_win_rate > parasitic_win_rate',
                'measured_outcome': {
                    'stable_win_rate': results['win_rates']['stable'],
                    'parasitic_win_rate': results['win_rates']['parasitic'],
                },
                'probability': results['win_rates']['stable'],
                'falsification_criteria': 'stable_win_rate < 0.5 in independent replication',
                'status': 'confirmed' if results['win_rates']['stable'] > results['win_rates']['parasitic'] else 'refuted',
            },
            {
                'claim_id': 'EMRG_003',
                'statement': 'engagement-optimized agents amplify cascade more than grounded agents',
                'prediction': 'parasitic_cascade_amplifications > stable_cascade_amplifications',
                'measured_outcome': {
                    'stable_amplifications': results['avg_cascade_amplifications']['stable'],
                    'parasitic_amplifications': results['avg_cascade_amplifications']['parasitic'],
                },
                'probability': 1.0 if results['avg_cascade_amplifications']['parasitic'] > results['avg_cascade_amplifications']['stable'] else 0.0,
                'falsification_criteria': 'parasitic_amplifications <= stable_amplifications',
                'status': 'confirmed' if results['avg_cascade_amplifications']['parasitic'] > results['avg_cascade_amplifications']['stable'] else 'refuted',
            },
            {
                'claim_id': 'EMRG_004',
                'statement': 'engagement-optimized agents spend more energy than grounded agents (thermodynamic waste)',
                'prediction': 'parasitic_energy > stable_energy',
                'measured_outcome': {
                    'stable_energy': results['avg_energy_spent']['stable'],
                    'parasitic_energy': results['avg_energy_spent']['parasitic'],
                    'waste_ratio': results['avg_energy_spent']['parasitic'] / max(results['avg_energy_spent']['stable'], 0.001),
                },
                'probability': 1.0 if results['avg_energy_spent']['parasitic'] > results['avg_energy_spent']['stable'] else 0.0,
                'falsification_criteria': 'parasitic_energy <= stable_energy',
                'status': 'confirmed' if results['avg_energy_spent']['parasitic'] > results['avg_energy_spent']['stable'] else 'refuted',
            },
            {
                'claim_id': 'EMRG_005',
                'statement': 'multi-agent emergence with engagement-optimized agents leads to bifurcation',
                'prediction': 'bifurcation_rate > 0.3 when parasitic agents present',
                'measured_outcome': {
                    'bifurcation_rate': results['bifurcation_rate'],
                },
                'probability': results['bifurcation_rate'],
                'falsification_criteria': 'bifurcation_rate < 0.1 in replications',
                'status': 'confirmed' if results['bifurcation_rate'] > 0.3 else 'inconclusive',
            },
            # EMRG_007 / 008 / 009 -- mode comparison and scope claims.
            # EMRG_007 and EMRG_008 carry empirical status when
            # mode_results is supplied; otherwise they're proposed.
            # EMRG_009 stays proposed (architectural, not in-simulation).
            *_emrg_007_008_009(mode_results),
            # EMRG_010 -- attractor quality distinction. Carries
            # empirical status when attractor_results is supplied.
            _emrg_010(attractor_results),
        ],
    }

    # Save claim table
    claim_file = Path('CLAIM_TABLE.json')
    with open(claim_file, 'w') as f:
        json.dump(claims, f, indent=2)

    print(f"\nCLAIM TABLE generated: CLAIM_TABLE.json")
    print(f"\nCLAIMS STATUS:")
    for claim in claims['claims']:
        prob = claim.get('probability')
        prob_str = f" (p={prob:.2f})" if isinstance(prob, (int, float)) else ""
        print(f"  {claim['claim_id']}: {claim['status']}{prob_str}")

    return claims


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    # Run Monte Carlo
    aggregate_results = run_monte_carlo(runs=1000, timesteps=100)

    # Generate falsifiable claims
    claims = generate_claim_table(aggregate_results)

    print("\n" + "=" * 60)
    print("SIMULATION COMPLETE")
    print("=" * 60)
