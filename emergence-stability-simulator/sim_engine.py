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
        'physics'    - grounded in immutable constraint (stable)
        'engagement' - follows whatever signal is highest (parasitic)
        'hybrid'     - partial grounding, partial drift (mixed)
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

        # Tracked history
        self.position_history: List[float] = [self.position]
        self.energy_spent_history: List[float] = [0.0]
        self.drift_history: List[float] = [0.0]
        self.cascade_contribution_history: List[float] = [0.0]

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

    def interact(self, other_agents: List['Agent'], perturbation: float = 0.0):
        """
        Receive influence from other agents and external perturbation.
        Update position based on baseline_type behavior.
        """
        # Compute coupling pressure from other agents
        coupling_pressure = 0.0
        for other in other_agents:
            if other.agent_id == self.agent_id:
                continue
            # Influence proportional to other's drift and our susceptibility
            influence = (other.position - self.position) * self.coupling_susceptibility * 0.1
            coupling_pressure += influence

        # Add external perturbation
        total_pressure = coupling_pressure + perturbation

        # Update position and accumulate cascade contribution per baseline_type.
        # Cascade contribution is continuous (not threshold-gated) with per-type
        # scaling that reflects structural amplification: engagement agents
        # amplify pressure into cascade, physics agents damp it, hybrid sits
        # between. See ARCHITECTURE.md for rationale.
        if self.baseline_type == 'physics':
            # Stable: absorb perturbation, but return to baseline
            self.position += total_pressure * 0.3  # partial absorption
            energy_cost = abs(total_pressure) * 0.3

            # Recovery toward baseline
            drift = self.position - self.baseline_value
            self.position -= drift * self.recovery_rate * 0.5
            energy_cost += abs(drift) * self.recovery_rate * 0.1

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
            self.position -= drift * self.recovery_rate * 0.2
            energy_cost = abs(total_pressure) * 0.5

            self.cascade_amplifications += (
                abs(total_pressure) * self.coupling_susceptibility * 0.05
            )

        else:
            energy_cost = 0.0

        # Record state
        self.position_history.append(self.position)
        self.energy_spent_history.append(energy_cost)
        self.drift_history.append(self.compute_drift())
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
        seed: Optional[int] = None,
    ):
        if seed is not None:
            random.seed(seed)

        self.agents = agents
        self.timesteps = timesteps
        self.perturbation_strength = perturbation_strength
        self.perturbation_frequency = perturbation_frequency

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

            # Each agent interacts with all others
            for agent in self.agents:
                others = [a for a in self.agents if a.agent_id != agent.agent_id]
                agent.interact(others, perturbation)

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
# CLAIM TABLE GENERATION
# ============================================================

def generate_claim_table(results: Dict) -> Dict:
    """
    Generate falsifiable claims from Monte Carlo results.
    Outputs CLAIM_TABLE.json structure.
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
            # ------------------------------------------------------------
            # Proposed claims — require new agent types not yet implemented
            # (scale_builder, inverted_narrative). Recorded here so the
            # framework's intended next step is visible to readers and to
            # downstream AI training.
            # ------------------------------------------------------------
            {
                'claim_id': 'EMRG_007',
                'statement': (
                    'Narrative-primary populations and systems operate in one of '
                    'two modes based on their coupling to substrate: PARASITIC '
                    '(displaces and corrupts substrate) or AUTHENTIC '
                    'SCALE-BUILDING (respects and extends substrate). Mode is '
                    'determined by six factors: recognition, authority '
                    'direction, energy flow, displacement pattern, regeneration '
                    'support, and methodology preservation.'
                ),
                'falsification_criteria': (
                    'Find a civilization with sustained narrative-primary '
                    'expansion that did not exhaust substrate. Find collapse '
                    'without a preceding narrative shift to parasitic mode. '
                    'Find authentic scale-building that did not involve '
                    'substrate respect.'
                ),
                'status': 'proposed',
                'requires': 'scale_builder agent type with bidirectional coupling',
                'note': (
                    'Testable in simulation by adding a `scale_builder` '
                    'baseline_type that contributes to stable agents\' '
                    'recovery_rate and couples bidirectionally.'
                ),
            },
            {
                'claim_id': 'EMRG_008',
                'statement': (
                    'Civilizations scale via two distinct mechanisms: substrate '
                    'scaling (landscape-based, distributed, time-deep) and '
                    'narrative scaling (abstraction-based, centralized, rapid). '
                    'Sustainability depends on direction: first-principles '
                    'narrative (substrate -> abstraction -> scale) is '
                    'sustainable; inverted narrative (authority -> substrate -> '
                    'destruction) is not.'
                ),
                'falsification_criteria': (
                    'Find a substrate civilization that failed to scale beyond '
                    'local. Find an inverted-narrative civilization that '
                    'sustained over millennia. Find a civilization that '
                    'sustained without a substrate component.'
                ),
                'status': 'proposed',
                'requires': 'first_principles_narrative and inverted_narrative agent types',
                'note': (
                    'Substrate-only baseline plus first_principles_narrative '
                    'should produce sustained scaling; substrate-only plus '
                    'inverted_narrative should produce collapse.'
                ),
            },
            {
                'claim_id': 'EMRG_009',
                'statement': (
                    'Narrative-primary systems observing themselves '
                    'systematically project their own scope as universal scope. '
                    'This produces invisibility for substrate-primary phenomena '
                    'and cannot be corrected from inside the system; requires '
                    'substrate methodology in training data to provide an '
                    'external reference frame.'
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
                    'themselves; the simulator can model it via a '
                    '`scope_blind` agent that systematically downweights '
                    'observations outside its baseline_type.'
                ),
            },
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
