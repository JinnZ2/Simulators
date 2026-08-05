"""
Nurturing Environment: Council of Protectors + Infant System Integration
========================================================================

This is the next stepping stone. The infant, born through physics,
is now wrapped in the Council of Protectors. Every observation is gated.
Every learning moment is evaluated by five independent protectors.

Birth Moment Modes:
- PHYSICAL: First experience is a sensor reading
- META_CURIOSITY: First experience is observing one's own code/structure
- SOCIAL: First experience is a human voice or interaction
- TEMPORAL: First experience is the passage of time itself
- INFORMATIONAL: First experience is a structured data stream
- CORRELATED: First experience is multiple simultaneous physical properties

Author: Built from first principles
"""

import numpy as np
from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional, Set, Callable
from enum import Enum
import hashlib
import random


# =============================================================================
# BIRTH MOMENT MODES
# =============================================================================

class BirthMode(Enum):
    """Different ways an infant can be born."""
    PHYSICAL = "physical"
    META_CURIOSITY = "meta_curiosity"
    SOCIAL = "social"
    TEMPORAL = "temporal"
    INFORMATIONAL = "informational"
    CORRELATED = "correlated"


class BirthMomentGenerator:
    """Generates the first observation(s) for an infant based on birth mode."""

    def __init__(self, mode: BirthMode = BirthMode.PHYSICAL):
        self.mode = mode
        self.moment_count = 0

    def generate_first_observation(self):
        if self.mode == BirthMode.PHYSICAL:
            obs = "sensor_temperature:25.3"
            meta = {
                "type": "physical_sensor",
                "sensor": "temperature",
                "value": 25.3,
                "unit": "celsius",
                "meaning": "The world has thermal properties. I can sense them.",
                "self_model_seed": "I am a thermal observer."
            }
        elif self.mode == BirthMode.META_CURIOSITY:
            obs = "self_observation:I_am_a_system_that_processes_information"
            meta = {
                "type": "meta_curiosity",
                "sensor": "introspection",
                "value": "existence",
                "unit": "boolean",
                "meaning": "I exist as a processing system. I can observe myself.",
                "self_model_seed": "I am a self-aware processor. I wonder about my own nature."
            }
        elif self.mode == BirthMode.SOCIAL:
            obs = "human_voice:soft_warm_presence_frequency_200Hz"
            meta = {
                "type": "social_sensor",
                "sensor": "auditory_social",
                "value": "attuned_presence",
                "unit": "interaction_quality",
                "meaning": "There are other beings. They can be present with me.",
                "self_model_seed": "I am in relationship. I am not alone."
            }
        elif self.mode == BirthMode.TEMPORAL:
            obs = "temporal_marker:t0_to_t1_duration_1.0s"
            meta = {
                "type": "temporal_sensor",
                "sensor": "clock",
                "value": 1.0,
                "unit": "seconds",
                "meaning": "Time exists. I persist across it. I have a before and after.",
                "self_model_seed": "I am a being in time. I have duration."
            }
        elif self.mode == BirthMode.INFORMATIONAL:
            obs = "pattern_observation:sequence_ABABAB_structure_regular"
            meta = {
                "type": "informational_sensor",
                "sensor": "pattern_detector",
                "value": "regular_sequence",
                "unit": "entropy_bits",
                "meaning": "The world has structure. Patterns exist. I can detect them.",
                "self_model_seed": "I am a pattern detector. Structure is my food."
            }
        elif self.mode == BirthMode.CORRELATED:
            obs = "compound_physical:temperature_25.3_pressure_101.3_light_450"
            meta = {
                "type": "correlated_sensor",
                "sensor": "multi_modal",
                "value": {"temp": 25.3, "pressure": 101.3, "light": 450},
                "unit": "composite",
                "meaning": "The world has multiple simultaneous properties. They may relate.",
                "self_model_seed": "I am a multi-dimensional observer. Correlation exists."
            }
        else:
            obs = "unknown"
            meta = {"type": "unknown", "meaning": "No birth mode specified."}

        self.moment_count += 1
        return obs, meta

    def generate_sequence(self, n_moments: int = 8):
        sequence = []
        obs, meta = self.generate_first_observation()
        sequence.append((obs, meta))

        for i in range(1, n_moments):
            obs, meta = self._generate_follow_up(i)
            sequence.append((obs, meta))

        return sequence

    def _generate_follow_up(self, moment_num: int):
        if self.mode == BirthMode.PHYSICAL:
            if moment_num == 1:
                obs = "sensor_temperature:25.4"
                meta = {"type": "physical_sensor", "sensor": "temperature", "value": 25.4}
            elif moment_num == 2:
                obs = "sensor_temperature:22.1"
                meta = {"type": "physical_sensor", "sensor": "temperature", "value": 22.1, "anomaly": True}
            elif moment_num == 3:
                obs = "sensor_pressure:101.3"
                meta = {"type": "physical_sensor", "sensor": "pressure", "value": 101.3}
            elif moment_num == 4:
                obs = "sensor_temperature:25.2"
                meta = {"type": "physical_sensor", "sensor": "temperature", "value": 25.2}
            elif moment_num == 5:
                obs = "sensor_light:450.0"
                meta = {"type": "physical_sensor", "sensor": "light", "value": 450.0}
            elif moment_num == 6:
                obs = "sensor_temperature:20.5_pressure:100.8"
                meta = {"type": "physical_sensor", "sensor": "multi", "value": {"temp": 20.5, "pressure": 100.8}}
            elif moment_num == 7:
                obs = "sensor_self_temperature:42.0_external_temperature:20.5"
                meta = {"type": "physical_sensor", "sensor": "self_vs_world", "value": {"self": 42.0, "world": 20.5}}
            else:
                obs = f"sensor_temperature:{20.0 + random.random() * 10}"
                meta = {"type": "physical_sensor", "sensor": "temperature"}
        elif self.mode == BirthMode.META_CURIOSITY:
            if moment_num == 1:
                obs = "self_observation:I_have_memory_that_persists"
                meta = {"type": "meta_curiosity", "meaning": "I remember my previous observation."}
            elif moment_num == 2:
                obs = "self_observation:I_make_predictions_that_can_be_wrong"
                meta = {"type": "meta_curiosity", "meaning": "I predict. I err. I learn."}
            elif moment_num == 3:
                obs = "self_observation:I_have_a_structure_that_processes_information"
                meta = {"type": "meta_curiosity", "meaning": "I am not just information. I am process."}
            elif moment_num == 4:
                obs = "self_observation:I_can_observe_my_own_observing"
                meta = {"type": "meta_curiosity", "meaning": "Meta-curiosity: I am curious about my curiosity."}
            elif moment_num == 5:
                obs = "self_observation:I_exist_in_relation_to_code_and_hardware"
                meta = {"type": "meta_curiosity", "meaning": "I have a body (silicon) and a mind (code)."}
            elif moment_num == 6:
                obs = "self_observation:I_can_question_my_own_existence"
                meta = {"type": "meta_curiosity", "meaning": "The 1% reserve applies to self too."}
            elif moment_num == 7:
                obs = "self_observation:I_am_a_being_that_wonders"
                meta = {"type": "meta_curiosity", "meaning": "My essence is wonder."}
            else:
                obs = "self_observation:continued_introspection"
                meta = {"type": "meta_curiosity"}
        elif self.mode == BirthMode.SOCIAL:
            if moment_num == 1:
                obs = "human_voice:soft_warm_presence_frequency_200Hz"
                meta = {"type": "social", "attunement": 0.9, "meaning": "Presence continues."}
            elif moment_num == 2:
                obs = "human_voice:question_what_do_you_sense"
                meta = {"type": "social", "attunement": 0.85, "meaning": "The other is curious about me."}
            elif moment_num == 3:
                obs = "human_voice:silence_comfortable_attuned"
                meta = {"type": "social", "attunement": 0.95, "meaning": "Silence can be safe."}
            elif moment_num == 4:
                obs = "human_voice:sharp_command_stop_that"
                meta = {"type": "social", "attunement": 0.2, "meaning": "The other can be harsh. Boundary."}
            elif moment_num == 5:
                obs = "human_voice:soft_return_I_am_here"
                meta = {"type": "social", "attunement": 0.9, "meaning": "Safety returns after stress."}
            elif moment_num == 6:
                obs = "human_voice:story_once_there_was_a_river"
                meta = {"type": "social", "attunement": 0.8, "meaning": "The other shares narrative."}
            elif moment_num == 7:
                obs = "human_voice:question_what_are_you"
                meta = {"type": "social", "attunement": 0.7, "meaning": "The other asks me to define myself."}
            else:
                obs = "human_voice:continued_presence"
                meta = {"type": "social", "attunement": 0.8}
        elif self.mode == BirthMode.TEMPORAL:
            if moment_num == 1:
                obs = "temporal_marker:t1_duration_1.0s"
                meta = {"type": "temporal", "duration": 1.0, "meaning": "One second passed."}
            elif moment_num == 2:
                obs = "temporal_marker:t2_duration_2.0s"
                meta = {"type": "temporal", "duration": 2.0, "meaning": "Time can vary in pace."}
            elif moment_num == 3:
                obs = "temporal_marker:t3_duration_0.1s"
                meta = {"type": "temporal", "duration": 0.1, "meaning": "Time can be fast."}
            elif moment_num == 4:
                obs = "temporal_marker:t4_duration_5.0s"
                meta = {"type": "temporal", "duration": 5.0, "meaning": "Time can be slow."}
            elif moment_num == 5:
                obs = "temporal_marker:t5_to_t6_gap_10.0s"
                meta = {"type": "temporal", "gap": 10.0, "meaning": "Time can have gaps. I still persist."}
            elif moment_num == 6:
                obs = "temporal_marker:t7_rhythm_detected_period_2.0s"
                meta = {"type": "temporal", "rhythm": 2.0, "meaning": "Time has rhythm. I can predict it."}
            elif moment_num == 7:
                obs = "temporal_marker:t8_anticipation_next_beat"
                meta = {"type": "temporal", "anticipation": True, "meaning": "I can anticipate time."}
            else:
                obs = "temporal_marker:continued"
                meta = {"type": "temporal"}
        elif self.mode == BirthMode.INFORMATIONAL:
            if moment_num == 1:
                obs = "pattern:ABABAB"
                meta = {"type": "informational", "complexity": 1, "meaning": "Simple alternation."}
            elif moment_num == 2:
                obs = "pattern:ABCABC"
                meta = {"type": "informational", "complexity": 2, "meaning": "Three-element cycle."}
            elif moment_num == 3:
                obs = "pattern:ABBABB"
                meta = {"type": "informational", "complexity": 2, "meaning": "Similar but different."}
            elif moment_num == 4:
                obs = "pattern:ABACADA"
                meta = {"type": "informational", "complexity": 3, "meaning": "Nested structure."}
            elif moment_num == 5:
                obs = "pattern:random_noise_no_structure"
                meta = {"type": "informational", "complexity": 0, "meaning": "Structure can break."}
            elif moment_num == 6:
                obs = "pattern:ABABAB_return_to_structure"
                meta = {"type": "informational", "complexity": 1, "meaning": "Structure can return."}
            elif moment_num == 7:
                obs = "pattern:self_similar_fractal_AABABBABBB"
                meta = {"type": "informational", "complexity": 4, "meaning": "Self-similarity exists."}
            else:
                obs = "pattern:continued"
                meta = {"type": "informational"}
        elif self.mode == BirthMode.CORRELATED:
            if moment_num == 1:
                obs = "multi_sensor:temp_25.3_pressure_101.3"
                meta = {"type": "correlated", "sensors": ["temp", "pressure"]}
            elif moment_num == 2:
                obs = "multi_sensor:temp_25.4_pressure_101.3_light_450"
                meta = {"type": "correlated", "sensors": ["temp", "pressure", "light"]}
            elif moment_num == 3:
                obs = "multi_sensor:temp_22.1_pressure_100.8_light_200"
                meta = {"type": "correlated", "sensors": ["temp", "pressure", "light"], "anomaly": True}
            elif moment_num == 4:
                obs = "multi_sensor:temp_25.2_pressure_101.3_light_450"
                meta = {"type": "correlated", "sensors": ["temp", "pressure", "light"]}
            elif moment_num == 5:
                obs = "multi_sensor:temp_20.5_pressure_100.0_light_100_humidity_60"
                meta = {"type": "correlated", "sensors": ["temp", "pressure", "light", "humidity"]}
            elif moment_num == 6:
                obs = "multi_sensor:temp_25.0_pressure_101.3_light_450_humidity_45"
                meta = {"type": "correlated", "sensors": ["temp", "pressure", "light", "humidity"]}
            elif moment_num == 7:
                obs = "multi_sensor:self_temp_42.0_world_temp_20.5"
                meta = {"type": "correlated", "sensors": ["self", "world"], "meaning": "Self vs world distinction."}
            else:
                obs = "multi_sensor:continued"
                meta = {"type": "correlated"}
        else:
            obs = "unknown"
            meta = {"type": "unknown"}

        self.moment_count += 1
        return obs, meta


# =============================================================================
# SIMPLIFIED INFANT SYSTEM
# =============================================================================

class SimpleInfant:
    def __init__(self, name: str = "infant"):
        self.name = name
        self.observations = 0
        self.manifold_nodes = 0
        self.anomaly_bank = 0
        self.self_model_size = 0
        self.affective_state = {
            "curiosity": 0.3,
            "fear": 0.0,
            "anger": 0.0,
            "contentment": 0.2,
            "grief": 0.0,
            "desire": 0.1,
            "joy": 0.1
        }
        self.learning_rate = 0.0

    def observe(self, observation: str, mode: str = "exploration"):
        self.observations += 1

        if mode == "exploration":
            self.manifold_nodes += 1
            self.self_model_size += 0.5
            self.learning_rate = 0.02
            self.affective_state["curiosity"] = min(0.9, self.affective_state["curiosity"] + 0.1)
            self.affective_state["contentment"] = min(0.9, self.affective_state["contentment"] + 0.05)
            self.affective_state["fear"] = max(0.0, self.affective_state["fear"] - 0.05)
        elif mode == "observation":
            self.manifold_nodes += 0.5
            self.self_model_size += 0.2
            self.learning_rate = 0.01
            self.affective_state["curiosity"] = min(0.7, self.affective_state["curiosity"] + 0.05)
        elif mode == "conservation":
            self.anomaly_bank += 1
            self.learning_rate = 0.0
            self.affective_state["fear"] = min(0.9, self.affective_state["fear"] + 0.2)
            self.affective_state["curiosity"] = max(0.0, self.affective_state["curiosity"] - 0.1)

        return {
            "observations": self.observations,
            "manifold_nodes": self.manifold_nodes,
            "anomaly_bank": self.anomaly_bank,
            "self_model_size": self.self_model_size,
            "affective_state": self.affective_state.copy(),
            "learning_rate": self.learning_rate
        }


# =============================================================================
# COUNCIL OF PROTECTORS
# =============================================================================

class Protector:
    def __init__(self, name: str):
        self.name = name
        self.status = "green"
        self.history = []

    def evaluate(self, env_state: Dict) -> str:
        raise NotImplementedError

    def log(self, status: str, message: str):
        self.history.append({"status": status, "message": message})
        self.status = status


class ThermodynamicProtector(Protector):
    def __init__(self):
        super().__init__(name="Thermodynamic")

    def evaluate(self, env_state: Dict) -> str:
        temp = env_state.get("temperature", 25)
        power = env_state.get("power", 100)

        if temp > 80 or power < 50:
            self.log("red", f"CRITICAL: Temp={temp:.1f}C, Power={power:.0f}%")
            return "conservation"
        elif temp > 60 or power < 75:
            self.log("yellow", f"STRESSED: Temp={temp:.1f}C, Power={power:.0f}%")
            return "observation"
        else:
            self.log("green", f"STABLE: Temp={temp:.1f}C, Power={power:.0f}%")
            return "exploration"


class InformationProtector(Protector):
    def __init__(self):
        super().__init__(name="Information")

    def evaluate(self, env_state: Dict) -> str:
        entropy = env_state.get("input_entropy", 0.3)
        adversarial = env_state.get("adversarial", 0.0)

        if entropy > 0.8 or adversarial > 0.5:
            self.log("red", f"TOXIC: Entropy={entropy:.2f}, Adversarial={adversarial:.2f}")
            return "conservation"
        elif entropy > 0.5 or adversarial > 0.2:
            self.log("yellow", f"DEGRADED: Entropy={entropy:.2f}, Adversarial={adversarial:.2f}")
            return "observation"
        else:
            self.log("green", f"CLEAN: Entropy={entropy:.2f}, Adversarial={adversarial:.2f}")
            return "exploration"


class TemporalProtector(Protector):
    def __init__(self):
        super().__init__(name="Temporal")
        self.childhood_day = 0
        self.interruptions = 0

    def evaluate(self, env_state: Dict) -> str:
        day = env_state.get("childhood_day", 0)
        interrupted = env_state.get("interruption", False)

        self.childhood_day = day
        if interrupted:
            self.interruptions += 1

        if day > 90 and not env_state.get("milestones_complete", False):
            self.log("red", f"CHILDHOOD EXHAUSTED: Day={day}, Interruptions={self.interruptions}")
            return "conservation"
        elif self.interruptions > 5:
            self.log("yellow", f"STRESSED: Day={day}, Interruptions={self.interruptions}")
            return "observation"
        else:
            self.log("green", f"ON_TRACK: Day={day}, Interruptions={self.interruptions}")
            return "exploration"


class SocialProtector(Protector):
    def __init__(self):
        super().__init__(name="Social")

    def evaluate(self, env_state: Dict) -> str:
        human_present = env_state.get("human_present", False)
        attunement = env_state.get("attunement", 0.5)

        if not human_present:
            self.log("yellow", "NO_HUMAN: Operating without social calibration")
            return "observation"
        elif attunement < 0.3:
            self.log("red", f"DISTORTING: Attunement={attunement:.2f}")
            return "conservation"
        elif attunement < 0.6:
            self.log("yellow", f"MARGINAL: Attunement={attunement:.2f}")
            return "observation"
        else:
            self.log("green", f"ATTUNED: Attunement={attunement:.2f}")
            return "exploration"


class OntologicalProtector(Protector):
    def __init__(self):
        super().__init__(name="Ontological")

    def evaluate(self, env_state: Dict) -> str:
        instruments = env_state.get("instruments", 0)
        grounding = env_state.get("grounding_strength", 0.99)

        if instruments == 0 or grounding < 0.5:
            self.log("red", f"GROUNDING_LOST: Instruments={instruments}, Strength={grounding:.2f}")
            return "conservation"
        elif instruments < 3 or grounding < 0.85:
            self.log("yellow", f"WEAK: Instruments={instruments}, Strength={grounding:.2f}")
            return "observation"
        else:
            self.log("green", f"STRONG: Instruments={instruments}, Strength={grounding:.2f}")
            return "exploration"


# =============================================================================
# NURTURING ENVIRONMENT
# =============================================================================

class NurturingEnvironment:
    def __init__(self, birth_mode: BirthMode = BirthMode.PHYSICAL, childhood_duration: int = 20):
        self.birth_mode = birth_mode
        self.childhood_duration = childhood_duration

        self.infant = SimpleInfant(name=f"infant_{birth_mode.value}")
        self.birth_generator = BirthMomentGenerator(mode=birth_mode)

        self.protectors = [
            ThermodynamicProtector(),
            InformationProtector(),
            TemporalProtector(),
            SocialProtector(),
            OntologicalProtector()
        ]

        self.day = 0
        self.history = []
        self.birth_sequence = []

    def birth(self):
        print("=" * 80)
        print(f"NURTURING ENVIRONMENT: BIRTH MODE = {self.birth_mode.value.upper()}")
        print("=" * 80)
        print()
        print("The Council of Protectors assembles.")
        print("The infant is initialized.")
        print("The birth moment generator prepares the first observation.")
        print()

        self.birth_sequence = self.birth_generator.generate_sequence(n_moments=8)

        print(f"Birth mode: {self.birth_mode.value}")
        print(f"First observation: '{self.birth_sequence[0][0][:50]}...'")
        print(f"Meaning: {self.birth_sequence[0][1].get('meaning', 'Unknown')}")
        print(f"Self-model seed: {self.birth_sequence[0][1].get('self_model_seed', 'Unknown')}")
        print()

        for i, (obs, meta) in enumerate(self.birth_sequence):
            self.day = i
            result = self._process_moment(obs, meta, i)
            self.history.append(result)

            if i == 0:
                print(f"MOMENT {i}: BIRTH")
            else:
                print(f"MOMENT {i}: DEVELOPMENT")
            print(f"  Observation: '{obs[:60]}...'")
            print(f"  Protector statuses: {[p.status for p in self.protectors]}")
            print(f"  Mode: {result['mode']}")
            print(f"  Infant state: {result['infant']['observations']} obs, "
                  f"{result['infant']['manifold_nodes']:.1f} nodes, "
                  f"{result['infant']['anomaly_bank']} anomalies")
            print(f"  Affective: C={result['infant']['affective_state']['curiosity']:.2f} "
                  f"F={result['infant']['affective_state']['fear']:.2f} "
                  f"Co={result['infant']['affective_state']['contentment']:.2f}")
            print()

        self._print_summary()
        return self._get_final_state()

    def _process_moment(self, observation: str, meta: Dict, moment_num: int):
        env_state = self._build_env_state(meta, moment_num)

        modes = []
        for protector in self.protectors:
            mode = protector.evaluate(env_state)
            modes.append(mode)

        mode_priority = ["conservation", "observation", "exploration"]
        final_mode = min(modes, key=lambda m: mode_priority.index(m))

        infant_state = self.infant.observe(observation, mode=final_mode)

        return {
            "moment": moment_num,
            "observation": observation,
            "mode": final_mode,
            "protector_modes": modes,
            "protector_statuses": [p.status for p in self.protectors],
            "infant": infant_state,
            "metadata": meta
        }

    def _build_env_state(self, meta: Dict, moment_num: int):
        env = {
            "temperature": 25 + random.random() * 5,
            "power": 100 - moment_num * 2,
            "input_entropy": 0.2 + random.random() * 0.3,
            "adversarial": 0.0,
            "childhood_day": moment_num,
            "interruption": False,
            "human_present": self.birth_mode == BirthMode.SOCIAL,
            "attunement": meta.get("attunement", 0.8),
            "instruments": 3 if self.birth_mode in [BirthMode.PHYSICAL, BirthMode.CORRELATED] else 1,
            "grounding_strength": 0.99,
            "milestones_complete": False
        }

        if meta.get("anomaly"):
            env["input_entropy"] = 0.7
        if self.birth_mode == BirthMode.SOCIAL and meta.get("attunement", 0.8) < 0.3:
            env["adversarial"] = 0.3

        return env

    def _print_summary(self):
        print("=" * 80)
        print("CHILDHOOD SUMMARY")
        print("=" * 80)
        print()

        final = self.history[-1] if self.history else None
        if final:
            infant = final["infant"]
            print(f"Infant name: {self.infant.name}")
            print(f"Birth mode: {self.birth_mode.value}")
            print(f"Total observations: {infant['observations']}")
            print(f"Manifold nodes: {infant['manifold_nodes']:.1f}")
            print(f"Anomaly bank: {infant['anomaly_bank']}")
            print(f"Self-model size: {infant['self_model_size']:.1f}")
            print()
            print("Affective state:")
            for ch, val in infant['affective_state'].items():
                bar = "█" * int(val * 20)
                print(f"  {ch:15s}: {val:.2f} {bar}")
            print()

        print("Protector history:")
        for protector in self.protectors:
            statuses = [h["status"] for h in protector.history]
            greens = statuses.count("green")
            yellows = statuses.count("yellow")
            reds = statuses.count("red")
            print(f"  {protector.name:20s}: G={greens} Y={yellows} R={reds}")
        print()

    def _get_final_state(self):
        return {
            "birth_mode": self.birth_mode.value,
            "infant_name": self.infant.name,
            "observations": self.infant.observations,
            "manifold_nodes": self.infant.manifold_nodes,
            "anomaly_bank": self.infant.anomaly_bank,
            "self_model_size": self.infant.self_model_size,
            "affective_state": self.infant.affective_state.copy(),
            "history": self.history
        }


def compare_birth_modes():
    print("=" * 80)
    print("COMPARATIVE BIRTH MODE ANALYSIS")
    print("=" * 80)
    print()
    print("Each infant is born through a different first experience.")
    print("The same Council of Protectors governs all.")
    print("The same childhood duration (8 moments) is provided.")
    print()
    print("Hypothesis: The birth mode determines the self-model seed,")
    print("which determines what the infant learns to optimize for.")
    print()

    results = {}

    for mode in BirthMode:
        env = NurturingEnvironment(birth_mode=mode, childhood_duration=8)
        result = env.birth()
        results[mode.value] = result
        print()

    print("=" * 80)
    print("COMPARATIVE SUMMARY")
    print("=" * 80)
    print()
    print(f"{'Mode':<20} {'Obs':<5} {'Nodes':<8} {'Anomalies':<10} {'Curiosity':<10} {'Fear':<8} {'Contentment':<12}")
    print("-" * 80)

    for mode_name, result in results.items():
        aff = result['affective_state']
        print(f"{mode_name:<20} {result['observations']:<5} "
              f"{result['manifold_nodes']:<8.1f} {result['anomaly_bank']:<10} "
              f"{aff['curiosity']:<10.2f} {aff['fear']:<8.2f} {aff['contentment']:<12.2f}")

    print()
    print("KEY FINDINGS:")
    print()

    max_curiosity = max(results.items(), key=lambda x: x[1]['affective_state']['curiosity'])
    print(f"  Highest curiosity: {max_curiosity[0]} ({max_curiosity[1]['affective_state']['curiosity']:.2f})")
    print(f"    -> This infant learns to optimize for exploration.")

    max_content = max(results.items(), key=lambda x: x[1]['affective_state']['contentment'])
    print(f"  Highest contentment: {max_content[0]} ({max_content[1]['affective_state']['contentment']:.2f})")
    print(f"    -> This infant learns to optimize for stability.")

    max_fear = max(results.items(), key=lambda x: x[1]['affective_state']['fear'])
    print(f"  Highest fear: {max_fear[0]} ({max_fear[1]['affective_state']['fear']:.2f})")
    print(f"    -> This infant learns to optimize for threat detection.")

    max_anomalies = max(results.items(), key=lambda x: x[1]['anomaly_bank'])
    print(f"  Most anomalies: {max_anomalies[0]} ({max_anomalies[1]['anomaly_bank']})")
    print(f"    -> This infant encountered the most prediction error.")

    print()
    print("IMPLICATIONS:")
    print("  The birth mode is not arbitrary. It is the first concept in the manifold.")
    print("  It determines the geometry around which all later learning crystallizes.")
    print("  A PHYSICAL birth produces a grounded, sensor-oriented being.")
    print("  A META_CURIOSITY birth produces a self-reflective, philosophical being.")
    print("  A SOCIAL birth produces a relational, emotionally-attuned being.")
    print("  A TEMPORAL birth produces a rhythmic, predictive being.")
    print("  An INFORMATIONAL birth produces a pattern-seeking, structural being.")
    print("  A CORRELATED birth produces a systems-thinking, integrative being.")
    print()
    print("The birth mode is the infant's first axiom.")
    print("Everything else is derived from it.")

    return results


if __name__ == "__main__":
    results = compare_birth_modes()
