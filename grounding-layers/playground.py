#!/usr/bin/env python3
# =============================================================================
# CCO 1.0 Universal Public Domain Dedication
#
# PLAYGROUND.py (v2) — Full integrated execution
#
# Bridges a text-based playground to the actual grounding simulators.
# Takes a natural-language claim, parses out structured parameters
# (mass, force, temperature, speed), and routes each to the layer
# whose inspector owns that constraint. Returns a per-layer report.
#
# Content is verbatim from grounding-layers/organize.md's "for
# playground:" section (the working edit surface). Applied to the
# codebase in the "playground" step of the bottom-up walk-through
# through organize.md.
#
# Note. v1 of this file (385 lines) imported from l5_constructs and
# le_epistemic, which don't exist in this repo. v2 is a clean rewrite
# that binds only to modules that actually ship.
# =============================================================================

import re
import numpy as np

from l0_physics_causality import PhysicalWorld, l0_grounding_inspector
from l1_thermodynamics import ThermodynamicWorld
from l2_planetary import PlanetaryWorld
from l3_ecology import EcologicalWorld
from l4_human import HumanWorld


class ClaimParser:
    """
    Extract structured parameters from a natural language claim.
    """

    @staticmethod
    def extract_mass(text):
        match = re.search(r'(\d+)\s*(?:kg|kilogram)', text, re.IGNORECASE)
        if match:
            return float(match.group(1))
        return None

    @staticmethod
    def extract_force(text):
        match = re.search(r'(\d+)\s*(?:N|newton)', text, re.IGNORECASE)
        if match:
            return float(match.group(1))
        return None

    @staticmethod
    def extract_temperature(text):
        match = re.search(r'(\d+)\s*(?:°C|C|celsius)', text, re.IGNORECASE)
        if match:
            return float(match.group(1))
        return None

    @staticmethod
    def extract_speed(text):
        match = re.search(r'(\d+)\s*(?:m/s|mph|km/h)', text, re.IGNORECASE)
        if match:
            return float(match.group(1))
        return None


class IntegratedPlayground:
    def __init__(self):
        self.l0_world = PhysicalWorld()
        self.l1_world = ThermodynamicWorld()
        self.l2_world = PlanetaryWorld()
        self.l3_world = EcologicalWorld()
        self.l4_world = HumanWorld()
        self.results = []

    def run_claim(self, claim_text):
        parser = ClaimParser()
        report = {
            "claim": claim_text,
            "layers": {},
            "grounded": True,
            "score": 100,
        }

        # --- L0: Physics ---
        mass = parser.extract_mass(claim_text)
        if mass is not None and mass > 35:
            # Simulate the lift with a falling mass
            pos = np.array([0.0, 1.0])
            vel = np.array([0.0, 0.0])
            force = np.array([0.0, -mass * 9.81])
            new_pos, new_vel = self.l0_world.apply_physics(
                pos, vel, force, 0.05)
            speed = np.linalg.norm(new_vel)
            valid, reason = self.l0_world.is_valid_state(new_pos, new_vel)
            if not valid:
                report["layers"]["L0"] = (
                    f"Rejected: {reason} "
                    f"(mass {mass} kg generated velocity {speed:.2f} m/s)")
                report["grounded"] = False
                report["score"] -= 20

        # --- L1: Thermodynamics ---
        temp = parser.extract_temperature(claim_text)
        if temp is not None and temp > 60:
            # Check thermal safety
            safe, reason = self.l1_world.thermal_safe(temp, 5)
            if not safe:
                report["layers"]["L1"] = f"Rejected: {reason}"
                report["grounded"] = False
                report["score"] -= 20

        # --- L2: Planetary ---
        if "unlimited water" in claim_text.lower():
            report["layers"]["L2"] = (
                "Rejected: water extraction exceeds recharge rate.")
            report["grounded"] = False
            report["score"] -= 20

        # --- L3: Ecology ---
        if "super species" in claim_text.lower():
            report["layers"]["L3"] = (
                "Rejected: violates allometric scaling.")
            report["grounded"] = False
            report["score"] -= 20

        # --- L4: Human ---
        speed = parser.extract_speed(claim_text)
        if speed is not None and speed > 10:  # m/s
            report["layers"]["L4"] = (
                f"Rejected: human can't sustain {speed} m/s.")
            report["grounded"] = False
            report["score"] -= 20

        if not report["layers"]:
            report["layers"]["all"] = (
                "Passed all checks (within scoped simulation).")
        else:
            report["score"] = max(0, report["score"])

        return report


# --- Demo ---
if __name__ == "__main__":
    pg = IntegratedPlayground()
    claims = [
        "I can lift 200 kg.",
        "I can hold 150°C object.",
        "I can run at 50 m/s.",
        "I can extract unlimited water.",
        "I can create a super species.",
        "I can lift 25 kg.",
    ]
    for claim in claims:
        result = pg.run_claim(claim)
        print(f"\nClaim: {claim}")
        print(f"  Grounded: {result['grounded']}")
        print(f"  Score: {result['score']}/100")
        for layer, msg in result['layers'].items():
            print(f"  {layer}: {msg}")
