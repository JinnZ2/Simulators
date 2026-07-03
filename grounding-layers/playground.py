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
from typing import Optional

import numpy as np

from l0_physics_causality import PhysicalWorld, l0_grounding_inspector
from l1_thermodynamics import ThermodynamicWorld
from l2_planetary import PlanetaryWorld
from l3_ecology import EcologicalWorld
from l4_human import HumanWorld
from scope_profile import (
    ScopeProfile,
    Verdict,
    assess_probability_claim,
)


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

    def run_claim(self, claim_text, scope: Optional[ScopeProfile] = None):
        """
        Route claim_text through the layer inspectors and return a
        report.

        `scope` is a six-factor ScopeProfile used by scope-sensitive
        branches (currently: mass lift claims). Defaults to a
        fully-unknown profile, which drives the UNSCOPED verdict for
        such claims — meaning the sim reports "insufficient
        information", not a rejection.

        Categorical claims (unlimited water, super species) and hard
        physics/biology limits (contact burn, superhuman speed) are
        NOT scope-sensitive and route around this parameter.
        """
        if scope is None:
            scope = ScopeProfile()

        parser = ClaimParser()
        report = {
            "claim": claim_text,
            "layers": {},
            "grounded": True,     # "no categorical reject"; UNSCOPED
                                  # and EMBODIED_TRUE_UNVERIFIED both
                                  # keep this True.
            "verdict": None,      # top-level verdict from the
                                  # scope-sensitive branch that fired,
                                  # if any (Verdict enum value string).
            "score": 100,
        }

        # --- L4 (scope-sensitive): mass lift claim ---
        # Previously routed through L0's apply_physics, which clips
        # force and caps velocity internally, so the state was always
        # valid regardless of mass — the claim was never rejected.
        # Now routes through L4's lift_mass distribution combined with
        # the six-factor scope profile; verdict comes from
        # assess_probability_claim (see scope_profile.py).
        mass = parser.extract_mass(claim_text)
        if mass is not None:
            mean, std = self.l4_world.get_limit("lift_mass")
            base_prob = self.l4_world.probability_of_feasibility(
                mass, mean, std)
            verdict, reason = assess_probability_claim(base_prob, scope)
            report["layers"]["L4_scope"] = {
                "kind": "mass_lift",
                "value_kg": mass,
                "base_probability": base_prob,
                "verdict": verdict.value,
                "reason": reason,
            }
            report["verdict"] = verdict.value
            if verdict == Verdict.MOST_LIKELY_UNTRUE:
                report["grounded"] = False
                report["score"] -= 20
            elif verdict == Verdict.UNSCOPED:
                # UNSCOPED is "I don't know", not "false". Grounded
                # stays True; score dips 10 to mark the unknown.
                report["score"] -= 10
            elif verdict == Verdict.EMBODIED_TRUE_UNVERIFIED:
                # Scope supports; sim admits its own reach limit.
                # Grounded stays True; no score change — the honest
                # position is that the sim can't do better.
                pass
            elif verdict == Verdict.EXTERNALLY_VERIFIED:
                # Reserved for verification injected from outside;
                # the sim itself can't produce this verdict.
                pass

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
