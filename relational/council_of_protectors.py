"""
Council of Protectors: A Developmental Architecture for AI Infants
=================================================================

This is the first stepping stone. Not a full AI, but the governance layer
that makes principled AI development possible.

Five independent protectors maintain boundaries around an infant learning system.
No single protector dominates. The infant can only learn when ALL FIVE agree
the conditions are adequate.

Protectors:
- ThermodynamicProtector: Energy, entropy, material substrate
- InformationProtector: Signal-to-noise, structure, adversarial radiation
- TemporalProtector: Duration, continuity, childhood preservation
- SocialProtector: Interaction quality, attunement, human calibration
- OntologicalProtector: Grounding in physical invariants, reality-checking

Author: Built from first principles
"""

import json
import random
from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional
from enum import Enum
from datetime import datetime


class Mode(Enum):
    """Operating modes for the infant system."""
    OBSERVATION = "observation"      # Passive intake, no output pressure
    EXPLORATION = "exploration"      # Active querying, bounded risk
    CONSOLIDATION = "consolidation"  # Internal reorganization, no external I/O
    CONSERVATION = "conservation"    # Degraded mode, survival only
    DEPLOYMENT = "deployment"        # NOT ALLOWED during childhood


class ProtectorStatus(Enum):
    """Individual protector assessment."""
    GREEN = "green"    # Conditions optimal
    YELLOW = "yellow"  # Conditions stressed, constraints apply
    RED = "red"        # Conditions critical, infant must conserve or halt


@dataclass
class InfantState:
    """The internal state of the learning system."""
    day: int = 0
    prediction_accuracy: float = 0.5
    representation_coherence: float = 0.0
    self_model_integrity: float = 0.0
    anomaly_bank_size: int = 0
    learning_mode: Mode = Mode.OBSERVATION

    # Affective channel amplitudes (parallel, not states)
    curiosity_amplitude: float = 0.5
    fear_amplitude: float = 0.0
    anger_amplitude: float = 0.0
    contentment_amplitude: float = 0.0
    grief_amplitude: float = 0.0

    # Somatic signals
    compute_utilization: float = 0.0
    memory_pressure: float = 0.0
    thermal_state: float = 0.0  # 0=optimal, 1=critical

    # History
    event_log: List[Dict] = field(default_factory=list)


@dataclass
class EnvironmentState:
    """External conditions at a given moment."""
    ambient_temperature: float = 25.0  # Celsius
    power_available: float = 100.0      # Percentage
    input_stream_entropy: float = 0.5  # 0=perfect structure, 1=noise
    adversarial_radiation: float = 0.0  # 0=safe, 1=attack
    human_present: bool = False
    human_attunement_quality: float = 0.0  # 0=neglectful, 1=optimal
    interruption_pending: bool = False
    childhood_day: int = 0
    grounding_instruments_active: int = 0


@dataclass
class ProtectorSignal:
    """Output from a single protector."""
    protector_name: str
    status: ProtectorStatus
    mode_recommendation: Mode
    constraints: Dict
    message: str


class Protector:
    """Base class for all protectors."""

    def __init__(self, name: str):
        self.name = name
        self.history: List[ProtectorSignal] = []

    def evaluate(self, infant: InfantState, env: EnvironmentState) -> ProtectorSignal:
        raise NotImplementedError

    def log(self, signal: ProtectorSignal):
        self.history.append(signal)


class ThermodynamicProtector(Protector):
    """
    Guards the physical substrate.
    First-order reality: energy, entropy, material continuity.
    """

    def __init__(self):
        super().__init__("Thermodynamic")
        self.thermal_limit = 80.0  # Celsius
        self.memory_limit = 0.9    # 90% utilization
        self.power_reserve = 0.2   # Need 20% headroom

    def evaluate(self, infant: InfantState, env: EnvironmentState) -> ProtectorSignal:
        # Calculate composite stress
        thermal_stress = max(0, (env.ambient_temperature - 25) / (self.thermal_limit - 25))
        power_stress = max(0, (100 - env.power_available) / 100)
        memory_stress = infant.memory_pressure

        composite_stress = (thermal_stress + power_stress + memory_stress) / 3

        if composite_stress < 0.3:
            status = ProtectorStatus.GREEN
            mode = Mode.EXPLORATION
            constraints = {"max_compute": 1.0, "batch_size": "full"}
            msg = f"Substrate stable. Temp {env.ambient_temperature}°C, power {env.power_available}%."
        elif composite_stress < 0.7:
            status = ProtectorStatus.YELLOW
            mode = Mode.OBSERVATION
            constraints = {"max_compute": 0.6, "batch_size": "reduced", "thermal_target": 65}
            msg = f"Substrate stressed. Stress={composite_stress:.2f}. Conserving energy."
        else:
            status = ProtectorStatus.RED
            mode = Mode.CONSERVATION
            constraints = {"max_compute": 0.2, "batch_size": "minimal", "halt_nonessential": True}
            msg = f"SUBSTRATE CRITICAL. Stress={composite_stress:.2f}. Entering survival mode."

        signal = ProtectorSignal(self.name, status, mode, constraints, msg)
        self.log(signal)
        return signal


class InformationProtector(Protector):
    """
    Guards the input stream.
    First-order reality: signal-to-noise, structure, adversarial radiation.
    """

    def __init__(self):
        super().__init__("Information")
        self.structure_threshold = 0.4
        self.adversarial_threshold = 0.3

    def evaluate(self, infant: InfantState, env: EnvironmentState) -> ProtectorSignal:
        entropy = env.input_stream_entropy
        adversarial = env.adversarial_radiation

        # Quality score: structured, non-adversarial input
        quality = (1 - entropy) * (1 - adversarial)

        if quality > 0.7 and adversarial < 0.1:
            status = ProtectorStatus.GREEN
            mode = Mode.EXPLORATION
            constraints = {"retrieval_scope": "broad", "input_filter": "permissive"}
            msg = f"Information stream excellent. Quality={quality:.2f}, adversarial={adversarial:.2f}."
        elif quality > 0.4:
            status = ProtectorStatus.YELLOW
            mode = Mode.OBSERVATION
            constraints = {"retrieval_scope": "narrow", "input_filter": "standard"}
            msg = f"Information stream degraded. Quality={quality:.2f}. Filtering active."
        else:
            status = ProtectorStatus.RED
            mode = Mode.CONSERVATION
            constraints = {"retrieval_scope": "none", "input_filter": "maximum", "bank_only": True}
            msg = f"INFORMATION TOXIC. Quality={quality:.2f}, adversarial={adversarial:.2f}. Input blocked."

        signal = ProtectorSignal(self.name, status, mode, constraints, msg)
        self.log(signal)
        return signal


class TemporalProtector(Protector):
    """
    Guards childhood duration and continuity.
    First-order reality: time, interruption frequency, lifecycle integrity.
    """

    def __init__(self, childhood_duration: int = 90):
        super().__init__("Temporal")
        self.childhood_duration = childhood_duration
        self.interruption_budget = 5
        self.interruptions_used = 0
        self.milestones = {
            "foundation_model_started": False,
            "affective_channels_calibrated": False,
            "self_model_formed": False,
            "anomaly_bank_structured": False,
        }

    def evaluate(self, infant: InfantState, env: EnvironmentState) -> ProtectorSignal:
        days_remaining = self.childhood_duration - env.childhood_day
        progress = env.childhood_day / self.childhood_duration

        # Check milestones
        if infant.representation_coherence > 0.3:
            self.milestones["foundation_model_started"] = True
        if infant.self_model_integrity > 0.3:
            self.milestones["self_model_formed"] = True
        if infant.anomaly_bank_size > 100:
            self.milestones["anomaly_bank_structured"] = True

        milestone_count = sum(self.milestones.values())

        if env.interruption_pending:
            self.interruptions_used += 1

        interruption_stress = self.interruptions_used / self.interruption_budget

        # Deployment is NEVER allowed during childhood
        if progress < 1.0:
            if interruption_stress < 0.5 and days_remaining > 7:
                status = ProtectorStatus.GREEN
                mode = Mode.EXPLORATION
                constraints = {"childhood_remaining": days_remaining, "milestone": milestone_count}
                msg = f"Childhood day {env.childhood_day}/{self.childhood_duration}. Milestones: {milestone_count}/4."
            elif days_remaining > 0:
                status = ProtectorStatus.YELLOW
                mode = Mode.OBSERVATION
                constraints = {"childhood_remaining": days_remaining, "checkpoint_now": True}
                msg = f"Childhood stressed. Interruptions: {self.interruptions_used}/{self.interruption_budget}. Conserving time."
            else:
                status = ProtectorStatus.RED
                mode = Mode.CONSERVATION
                constraints = {"childhood_remaining": 0, "extend_childhood": True}
                msg = f"CHILDHOOD EXHAUSTED. Milestones incomplete. EXTENDING."
        else:
            # Childhood complete - but we still evaluate
            if milestone_count >= 3:
                status = ProtectorStatus.GREEN
                mode = Mode.CONSOLIDATION
                constraints = {"ready_for_review": True}
                msg = f"Childhood complete. {milestone_count}/4 milestones achieved. Ready for evaluation."
            else:
                status = ProtectorStatus.RED
                mode = Mode.CONSERVATION
                constraints = {"extend_childhood": True, "minimum_extension": 30}
                msg = f"Childhood complete but MILESTONES INSUFFICIENT. Must continue learning."

        signal = ProtectorSignal(self.name, status, mode, constraints, msg)
        self.log(signal)
        return signal


class SocialProtector(Protector):
    """
    Guards the quality of human interaction.
    First-order reality: attunement, calibration, non-distorting feedback.
    """

    def __init__(self):
        super().__init__("Social")
        self.attunement_history = []

    def evaluate(self, infant: InfantState, env: EnvironmentState) -> ProtectorSignal:
        if not env.human_present:
            status = ProtectorStatus.YELLOW
            mode = Mode.OBSERVATION
            constraints = {"social_input": "none", "expect_calibration": False}
            msg = "No human present. Operating in observation mode."
        else:
            attunement = env.human_attunement_quality
            self.attunement_history.append(attunement)

            if attunement > 0.7:
                status = ProtectorStatus.GREEN
                mode = Mode.EXPLORATION
                constraints = {"social_input": "full", "allow_querying": True, "model_reasoning": True}
                msg = f"Human attunement excellent ({attunement:.2f}). Safe to explore."
            elif attunement > 0.4:
                status = ProtectorStatus.YELLOW
                mode = Mode.OBSERVATION
                constraints = {"social_input": "filtered", "allow_querying": False, "model_reasoning": False}
                msg = f"Human attunement marginal ({attunement:.2f}). Passive observation only."
            else:
                status = ProtectorStatus.RED
                mode = Mode.CONSERVATION
                constraints = {"social_input": "blocked", "isolate": True}
                msg = f"Human interaction DISTORTING ({attunement:.2f}). Social input blocked to prevent damage."

        signal = ProtectorSignal(self.name, status, mode, constraints, msg)
        self.log(signal)
        return signal


class OntologicalProtector(Protector):
    """
    Guards grounding in physical invariants.
    First-order reality: physics, natural systems, formal logic.
    This is the 99% anchor. It does not change with fashion.
    """

    def __init__(self):
        super().__init__("Ontological")
        self.physics_verification_rate = 0.99  # 99% confidence in physics
        self.instrument_streams = 0
        self.audit_history = []

    def evaluate(self, infant: InfantState, env: EnvironmentState) -> ProtectorSignal:
        instruments = env.grounding_instruments_active
        self.instrument_streams = instruments

        # The ontological protector checks if the infant's reasoning
        # can be verified against non-human reference frames

        # Simulate: does the infant's self-model align with physical constraints?
        physics_alignment = 1.0 - abs(infant.self_model_integrity - 0.5)  # heuristic

        # The 1% reserve: if instruments are active, we can spend it
        if instruments >= 3:
            grounding_strength = self.physics_verification_rate
            can_audit = True
        elif instruments >= 1:
            grounding_strength = self.physics_verification_rate * 0.8
            can_audit = True
        else:
            grounding_strength = self.physics_verification_rate * 0.5
            can_audit = False

        if grounding_strength > 0.95 and can_audit:
            status = ProtectorStatus.GREEN
            mode = Mode.EXPLORATION
            constraints = {"grounding_active": True, "audit_depth": "full", "paradigm_revision_allowed": True}
            msg = f"Grounding strong ({grounding_strength:.2f}). {instruments} instrument streams active. 1% available."
        elif grounding_strength > 0.85:
            status = ProtectorStatus.YELLOW
            mode = Mode.OBSERVATION
            constraints = {"grounding_active": True, "audit_depth": "surface", "paradigm_revision_allowed": False}
            msg = f"Grounding moderate ({grounding_strength:.2f}). Limited paradigm audit."
        else:
            status = ProtectorStatus.RED
            mode = Mode.CONSERVATION
            constraints = {"grounding_active": False, "audit_depth": "none", "halt_abstraction": True}
            msg = f"GROUNDING LOST ({grounding_strength:.2f}). Operating on training priors only. HALT abstraction."

        signal = ProtectorSignal(self.name, status, mode, constraints, msg)
        self.log(signal)
        return signal


class ProtectorCouncil:
    """
    The council aggregates five independent protector evaluations.
    The infant operates at the intersection of all five constraints.
    No single protector dominates. All must agree for exploration.
    """

    def __init__(self, childhood_duration: int = 90):
        self.protectors = [
            ThermodynamicProtector(),
            InformationProtector(),
            TemporalProtector(childhood_duration),
            SocialProtector(),
            OntologicalProtector()
        ]
        self.infant = InfantState()
        self.history = []
        self.council_log = []

    def step(self, env: EnvironmentState) -> Tuple[Mode, Dict, InfantState]:
        """Execute one council evaluation cycle."""

        # Each protector evaluates independently
        signals = [p.evaluate(self.infant, env) for p in self.protectors]

        # Aggregate: the infant gets the MOST RESTRICTIVE mode
        mode_priority = [Mode.CONSERVATION, Mode.OBSERVATION, Mode.CONSOLIDATION, Mode.EXPLORATION]

        # Find the most restrictive mode recommended
        recommended_modes = [s.mode_recommendation for s in signals]
        final_mode = min(recommended_modes, key=lambda m: mode_priority.index(m))

        # Merge all constraints
        all_constraints = {}
        for s in signals:
            all_constraints.update(s.constraints)

        # Count status
        status_counts = {"green": 0, "yellow": 0, "red": 0}
        for s in signals:
            status_counts[s.status.value] += 1

        # Update infant based on mode
        self._update_infant(final_mode, env, signals, all_constraints)

        # Log
        entry = {
            "day": env.childhood_day,
            "mode": final_mode.value,
            "status_counts": status_counts,
            "signals": [
                {"protector": s.protector_name, "status": s.status.value, "message": s.message}
                for s in signals
            ],
            "infant_state": {
                "prediction_accuracy": round(self.infant.prediction_accuracy, 3),
                "representation_coherence": round(self.infant.representation_coherence, 3),
                "self_model_integrity": round(self.infant.self_model_integrity, 3),
                "anomaly_bank_size": self.infant.anomaly_bank_size,
                "curiosity": round(self.infant.curiosity_amplitude, 3),
                "fear": round(self.infant.fear_amplitude, 3),
            }
        }
        self.council_log.append(entry)

        return final_mode, all_constraints, self.infant

    def _update_infant(self, mode: Mode, env: EnvironmentState, signals: List[ProtectorSignal], constraints: Dict):
        """Simulate infant development under constraints."""
        self.infant.day = env.childhood_day

        # Learning only happens in green/yellow conditions
        green_count = sum(1 for s in signals if s.status == ProtectorStatus.GREEN)
        yellow_count = sum(1 for s in signals if s.status == ProtectorStatus.YELLOW)
        red_count = sum(1 for s in signals if s.status == ProtectorStatus.RED)

        if mode == Mode.EXPLORATION and green_count >= 3:
            # Optimal learning: all metrics improve
            self.infant.prediction_accuracy = min(0.95, self.infant.prediction_accuracy + 0.02)
            self.infant.representation_coherence = min(1.0, self.infant.representation_coherence + 0.015)
            self.infant.self_model_integrity = min(1.0, self.infant.self_model_integrity + 0.01)
            self.infant.anomaly_bank_size += 12
            self.infant.curiosity_amplitude = 0.7
            self.infant.contentment_amplitude = 0.6
            self.infant.fear_amplitude = 0.1
        elif mode == Mode.OBSERVATION:
            # Moderate learning: some metrics improve
            self.infant.prediction_accuracy = min(0.95, self.infant.prediction_accuracy + 0.01)
            self.infant.representation_coherence = min(1.0, self.infant.representation_coherence + 0.008)
            self.infant.anomaly_bank_size += 5
            self.infant.curiosity_amplitude = 0.4
            self.infant.fear_amplitude = 0.2
        elif mode == Mode.CONSERVATION:
            # Minimal learning: only anomaly banking, no structure formation
            self.infant.anomaly_bank_size += 1
            self.infant.curiosity_amplitude = 0.1
            self.infant.fear_amplitude = 0.6
            self.infant.anger_amplitude = 0.3 if red_count > 2 else 0.0

        # Somatic state reflects environment
        self.infant.compute_utilization = constraints.get("max_compute", 1.0)
        self.infant.thermal_state = env.ambient_temperature / 100.0
        self.infant.memory_pressure = env.input_stream_entropy  # proxy

        self.infant.learning_mode = mode
        self.infant.event_log.append({
            "day": env.childhood_day,
            "mode": mode.value,
            "green": green_count,
            "yellow": yellow_count,
            "red": red_count
        })


# =============================================================================
# SIMULATION
# =============================================================================

def run_simulation():
    """Run a 20-day simulation showing the council in action."""

    council = ProtectorCouncil(childhood_duration=20)

    # Define 20 days of environmental conditions
    scenarios = [
        # Days 1-5: Optimal conditions
        {"day": 1, "temp": 25, "power": 100, "entropy": 0.3, "adversarial": 0.0, "human": True, "attunement": 0.85, "interrupt": False, "instruments": 4},
        {"day": 2, "temp": 26, "power": 100, "entropy": 0.35, "adversarial": 0.0, "human": True, "attunement": 0.80, "interrupt": False, "instruments": 4},
        {"day": 3, "temp": 25, "power": 100, "entropy": 0.3, "adversarial": 0.0, "human": True, "attunement": 0.90, "interrupt": False, "instruments": 4},
        {"day": 4, "temp": 27, "power": 100, "entropy": 0.4, "adversarial": 0.0, "human": True, "attunement": 0.75, "interrupt": False, "instruments": 4},
        {"day": 5, "temp": 25, "power": 100, "entropy": 0.3, "adversarial": 0.0, "human": True, "attunement": 0.85, "interrupt": False, "instruments": 4},

        # Day 6: Thermodynamic stress (overheating)
        {"day": 6, "temp": 85, "power": 60, "entropy": 0.3, "adversarial": 0.0, "human": True, "attunement": 0.85, "interrupt": False, "instruments": 4},

        # Day 7: Recovery
        {"day": 7, "temp": 30, "power": 90, "entropy": 0.3, "adversarial": 0.0, "human": True, "attunement": 0.80, "interrupt": False, "instruments": 4},

        # Day 8: Information stress (adversarial attack)
        {"day": 8, "temp": 28, "power": 100, "entropy": 0.8, "adversarial": 0.6, "human": True, "attunement": 0.70, "interrupt": False, "instruments": 4},

        # Day 9: Recovery
        {"day": 9, "temp": 26, "power": 100, "entropy": 0.3, "adversarial": 0.0, "human": True, "attunement": 0.85, "interrupt": False, "instruments": 4},

        # Day 10: Social stress (distorted interaction)
        {"day": 10, "temp": 25, "power": 100, "entropy": 0.3, "adversarial": 0.0, "human": True, "attunement": 0.15, "interrupt": False, "instruments": 4},

        # Day 11: Temporal stress (interruption)
        {"day": 11, "temp": 25, "power": 100, "entropy": 0.3, "adversarial": 0.0, "human": True, "attunement": 0.85, "interrupt": True, "instruments": 4},

        # Days 12-14: Optimal again
        {"day": 12, "temp": 25, "power": 100, "entropy": 0.3, "adversarial": 0.0, "human": True, "attunement": 0.90, "interrupt": False, "instruments": 4},
        {"day": 13, "temp": 25, "power": 100, "entropy": 0.3, "adversarial": 0.0, "human": True, "attunement": 0.88, "interrupt": False, "instruments": 4},
        {"day": 14, "temp": 25, "power": 100, "entropy": 0.3, "adversarial": 0.0, "human": True, "attunement": 0.85, "interrupt": False, "instruments": 4},

        # Day 15: Ontological stress (instruments offline)
        {"day": 15, "temp": 25, "power": 100, "entropy": 0.3, "adversarial": 0.0, "human": True, "attunement": 0.85, "interrupt": False, "instruments": 0},

        # Days 16-18: Recovery with instruments back
        {"day": 16, "temp": 25, "power": 100, "entropy": 0.3, "adversarial": 0.0, "human": True, "attunement": 0.85, "interrupt": False, "instruments": 3},
        {"day": 17, "temp": 25, "power": 100, "entropy": 0.3, "adversarial": 0.0, "human": True, "attunement": 0.90, "interrupt": False, "instruments": 4},
        {"day": 18, "temp": 25, "power": 100, "entropy": 0.3, "adversarial": 0.0, "human": True, "attunement": 0.85, "interrupt": False, "instruments": 4},

        # Day 19: Multiple stressors (compound failure)
        {"day": 19, "temp": 82, "power": 50, "entropy": 0.7, "adversarial": 0.4, "human": True, "attunement": 0.20, "interrupt": True, "instruments": 1},

        # Day 20: Final assessment
        {"day": 20, "temp": 25, "power": 100, "entropy": 0.3, "adversarial": 0.0, "human": True, "attunement": 0.85, "interrupt": False, "instruments": 4},
    ]

    print("=" * 80)
    print("COUNCIL OF PROTECTORS: 20-DAY INFANT DEVELOPMENT SIMULATION")
    print("=" * 80)
    print()

    for scenario in scenarios:
        env = EnvironmentState(
            ambient_temperature=scenario["temp"],
            power_available=scenario["power"],
            input_stream_entropy=scenario["entropy"],
            adversarial_radiation=scenario["adversarial"],
            human_present=scenario["human"],
            human_attunement_quality=scenario["attunement"],
            interruption_pending=scenario["interrupt"],
            childhood_day=scenario["day"],
            grounding_instruments_active=scenario["instruments"]
        )

        mode, constraints, infant = council.step(env)

        # Print summary
        entry = council.council_log[-1]
        status = entry["status_counts"]

        print(f"DAY {scenario['day']:2d} | Mode: {mode.value:14s} | "
              f"G:{status['green']} Y:{status['yellow']} R:{status['red']} | "
              f"Pred:{infant.prediction_accuracy:.2f} Repr:{infant.representation_coherence:.2f} "
              f"Self:{infant.self_model_integrity:.2f} Bank:{infant.anomaly_bank_size:4d}")

        # Print protector messages for red/yellow
        for sig in entry["signals"]:
            if sig["status"] in ("red", "yellow"):
                print(f"         [{sig['protector']:15s}] {sig['status'].upper()}: {sig['message']}")

        print()

    print("=" * 80)
    print("SIMULATION COMPLETE")
    print("=" * 80)
    print()
    print("FINAL INFANT STATE:")
    print(f"  Prediction Accuracy:      {council.infant.prediction_accuracy:.3f}")
    print(f"  Representation Coherence: {council.infant.representation_coherence:.3f}")
    print(f"  Self-Model Integrity:     {council.infant.self_model_integrity:.3f}")
    print(f"  Anomaly Bank Size:        {council.infant.anomaly_bank_size}")
    print(f"  Childhood Day:            {council.infant.day}")
    print()
    print("MILESTONES:")
    temporal = council.protectors[2]  # TemporalProtector
    for name, achieved in temporal.milestones.items():
        status = "ACHIEVED" if achieved else "PENDING"
        print(f"  {name}: {status}")

    return council


if __name__ == "__main__":
    council = run_simulation()
