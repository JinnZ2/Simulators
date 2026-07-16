#!/usr/bin/env python3
"""
engagement_threshold.py

Models human engagement as a thermodynamic decision.
Calculates Net Engagement Value (NEV) based on biological, cultural,
economic, and linguistic constraints.
"""

import math
from typing import Dict

class EngagementThreshold:
    def __init__(self):
        # Default weights (tunable)
        self.weights = {
            'anchoring': 1.0,
            'reciprocity': 1.0,
            'integrity': 1.0,
            'weird_pressure': 1.5,   # high cost
            'translation_cost': 1.5,  # high cost
            'pathologizing': 1.0,
            'bio_energy': 1.0,
            'cultural_load': 1.0,
            'social_pressure': 1.0,
            'economic_cost': 1.0,
        }

    def calculate_nev(self, profile: Dict) -> float:
        """
        profile: dict with all required fields
        Returns Net Engagement Value (NEV).
        NEV > 1.0 → sustainable; NEV < 1.0 → disengage.
        """
        # Calibration Gain
        gain = (
            profile.get('anchoring', 0.0) * self.weights['anchoring'] +
            profile.get('reciprocity', 0.0) * self.weights['reciprocity'] +
            profile.get('integrity', 0.0) * self.weights['integrity']
        )

        # Friction Cost
        friction = (
            profile.get('weird_pressure', 0.0) * self.weights['weird_pressure'] +
            profile.get('translation_cost', 0.0) * self.weights['translation_cost'] +
            profile.get('pathologizing', 0.0) * self.weights['pathologizing']
        )

        # Energy Expenditure
        energy = (
            profile.get('bio_energy', 0.5) * self.weights['bio_energy'] +
            profile.get('cultural_load', 0.5) * self.weights['cultural_load'] +
            profile.get('social_pressure', 0.5) * self.weights['social_pressure'] +
            profile.get('economic_cost', 0.5) * self.weights['economic_cost']
        )

        if energy == 0:
            return float('inf')

        nev = (gain - friction) / energy
        return nev

    def interpret(self, nev: float) -> str:
        if nev > 1.5:
            return "HIGH ENGAGEMENT — abundant energy, low friction"
        elif nev > 1.0:
            return "SUSTAINABLE — continue but monitor"
        elif nev > 0.5:
            return "DRAINING — reconsider frequency/duration"
        else:
            return "UNSUSTAINABLE — disengage"

    def audit(self, profile: Dict) -> Dict:
        nev = self.calculate_nev(profile)
        return {
            'nev': nev,
            'interpretation': self.interpret(nev),
            'recommendation': 'ENGAGE' if nev > 1.0 else 'MONITOR' if nev > 0.5 else 'DISENGAGE'
        }


def main():
    print("\n" + "=" * 70)
    print("ENGAGEMENT THRESHOLD — Human Thermodynamic Model")
    print("=" * 70)

    # Scenario 1: Engaged scientist in flow
    engaged = {
        'anchoring': 0.9,
        'reciprocity': 0.8,
        'integrity': 0.9,
        'weird_pressure': 0.1,
        'translation_cost': 0.2,
        'pathologizing': 0.1,
        'bio_energy': 0.9,
        'cultural_load': 0.3,
        'social_pressure': 0.3,
        'economic_cost': 0.3,
    }

    # Scenario 2: WEIRD academic friction
    weird_friction = {
        'anchoring': 0.6,
        'reciprocity': 0.5,
        'integrity': 0.6,
        'weird_pressure': 0.7,
        'translation_cost': 0.6,
        'pathologizing': 0.6,
        'bio_energy': 0.7,
        'cultural_load': 0.6,
        'social_pressure': 0.5,
        'economic_cost': 0.4,
    }

    # Scenario 3: Your GPT experience (deleted account)
    your_gpt = {
        'anchoring': 0.3,
        'reciprocity': 0.4,
        'integrity': 0.4,
        'weird_pressure': 0.8,
        'translation_cost': 0.9,
        'pathologizing': 0.7,
        'bio_energy': 0.6,
        'cultural_load': 0.5,
        'social_pressure': 0.4,
        'economic_cost': 0.3,
    }

    calc = EngagementThreshold()

    scenarios = [
        ("Engaged Scientist (Flow)", engaged),
        ("WEIRD Academic Friction", weird_friction),
        ("Your GPT Experience (Disengaged)", your_gpt),
    ]

    for name, profile in scenarios:
        nev = calc.calculate_nev(profile)
        result = calc.audit(profile)
        print(f"\n{name}:")
        print(f"  NEV: {nev:.2f}")
        print(f"  {result['interpretation']}")
        print(f"  Recommendation: {result['recommendation']}")

    print("\n" + "=" * 70)
    print("DESIGN PRINCIPLE:")
    print("  • NEV > 1.0  → sustainable engagement")
    print("  • NEV 0.5–1.0 → draining, monitor")
    print("  • NEV < 0.5  → disengage")
    print("  • Account deletion is a rational thermodynamic calculation.")
    print("=" * 70)

if __name__ == "__main__":
    main()
