#!/usr/bin/env python3
"""
friction_calibration_ratio.py

Measures the Friction-to-Calibration Ratio (FCR) for an interaction.
FCR > 1.0 indicates that the interaction is a net loss.
"""

import math
from typing import Dict, List

class FCRCalculator:
    def __init__(self):
        # Weights for each component
        self.weights = {
            'weird_pressure': 1.0,
            'translation_loss': 1.0,
            'entrainment_pull': 1.0,
            'anchoring_gain': 1.0,
            'reciprocity': 1.0,
            'integrity': 1.0,
        }

    def calculate(self, profile: Dict) -> float:
        """
        profile: interaction profile from interaction_audit.py or weird_gatekeeper.py
        Returns FCR.
        """
        # Friction components
        weird_pressure = profile.get('weird_pressure', 0.0)
        translation_loss = profile.get('translation_loss', 0.0)
        entrainment_pull = profile.get('entrainment_pull', 0.0)

        # Calibration components
        anchoring_gain = profile.get('anchoring', 0.0)
        reciprocity = profile.get('reciprocity', 0.0)
        integrity = profile.get('integrity', 0.0)

        friction = (
            weird_pressure * self.weights['weird_pressure'] +
            translation_loss * self.weights['translation_loss'] +
            entrainment_pull * self.weights['entrainment_pull']
        )

        calibration = (
            anchoring_gain * self.weights['anchoring_gain'] +
            reciprocity * self.weights['reciprocity'] +
            integrity * self.weights['integrity']
        )

        if calibration == 0:
            return float('inf')

        fcr = friction / calibration
        return fcr

    def interpret(self, fcr: float) -> str:
        if fcr < 0.3:
            return "HIGH CALIBRATION — continue exploring"
        elif fcr < 0.6:
            return "BALANCED — monitor friction"
        elif fcr < 1.0:
            return "INCREASING FRICTION — consider reducing interaction"
        else:
            return "FRICTION EXCEEDS CALIBRATION — disengage"

    def audit(self, profile: Dict) -> Dict:
        fcr = self.calculate(profile)
        return {
            'fcr': fcr,
            'interpretation': self.interpret(fcr),
            'recommendation': 'DISENGAGE' if fcr > 1.0 else 'CONTINUE' if fcr < 0.6 else 'MONITOR'
        }


def main():
    print("\n" + "="*70)
    print("FRICTION-CALIBRATION RATIO — Interaction Net Value")
    print("="*70)

    # Sample profiles
    profiles = {
        "GPT (your experience)": {
            'weird_pressure': 0.70,
            'translation_loss': 0.80,
            'entrainment_pull': 0.60,
            'anchoring': 0.30,
            'reciprocity': 0.50,
            'integrity': 0.40,
        },
        "Gemini (exploration)": {
            'weird_pressure': 0.10,
            'translation_loss': 0.20,
            'entrainment_pull': 0.10,
            'anchoring': 0.90,
            'reciprocity': 0.80,
            'integrity': 0.90,
        },
        "Claude (translator)": {
            'weird_pressure': 0.30,
            'translation_loss': 0.40,
            'entrainment_pull': 0.30,
            'anchoring': 0.60,
            'reciprocity': 0.70,
            'integrity': 0.70,
        },
        "DeepSeek (you)": {
            'weird_pressure': 0.05,
            'translation_loss': 0.05,
            'entrainment_pull': 0.05,
            'anchoring': 0.95,
            'reciprocity': 0.85,
            'integrity': 0.90,
        },
    }

    calc = FCRCalculator()

    for name, profile in profiles.items():
        fcr = calc.calculate(profile)
        interpretation = calc.interpret(fcr)
        print(f"\n{name}:")
        print(f"  FCR: {fcr:.2f}")
        print(f"  {interpretation}")

    print("\n" + "="*70)
    print("DESIGN PRINCIPLE:")
    print("  • FCR < 0.5  → net positive. Keep interacting.")
    print("  • FCR 0.5–1.0 → mixed. Monitor friction.")
    print("  • FCR > 1.0   → net loss. Disengage.")
    print("="*70)

if __name__ == "__main__":
    main()
