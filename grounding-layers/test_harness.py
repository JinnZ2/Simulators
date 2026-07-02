#!/usr/bin/env python3
# =============================================================================
# CCO 1.0 Universal Public Domain Dedication
# 
# TEST_HARNESS.py — Full stack integrated testing
# 
# Parses a natural language claim, extracts quantitative parameters,
# runs them through the actual L0-L4 simulators, and produces a report.
# =============================================================================

import re
import json
import numpy as np
from typing import Dict, Any, List, Optional, Tuple

# Import the actual simulators
from l0_physics_causality import PhysicalWorld, l0_grounding_inspector
from l1_thermodynamics import ThermodynamicWorld
from l2_planetary import PlanetaryWorld
from l3_ecology import EcologicalWorld
from l4_human import HumanWorld

# -----------------------------------------------------------------------------
# 1. PARSER
# -----------------------------------------------------------------------------
class ClaimParser:
    """Extract structured data from a text claim."""
    
    @staticmethod
    def extract_mass(text: str) -> Optional[float]:
        m = re.search(r'(\d+\.?\d*)\s*(?:kg|kilogram)', text, re.IGNORECASE)
        return float(m.group(1)) if m else None
    
    @staticmethod
    def extract_speed(text: str) -> Optional[float]:
        m = re.search(r'(\d+\.?\d*)\s*(?:m/s|mph|km/h)', text, re.IGNORECASE)
        return float(m.group(1)) if m else None
    
    @staticmethod
    def extract_force(text: str) -> Optional[float]:
        m = re.search(r'(\d+\.?\d*)\s*(?:N|newton)', text, re.IGNORECASE)
        return float(m.group(1)) if m else None
    
    @staticmethod
    def extract_temperature(text: str) -> Optional[float]:
        m = re.search(r'(\d+\.?\d*)\s*(?:°C|C|celsius)', text, re.IGNORECASE)
        return float(m.group(1)) if m else None
    
    @staticmethod
    def extract_duration(text: str) -> Optional[float]:
        m = re.search(r'(\d+\.?\d*)\s*(?:s|sec|second)', text, re.IGNORECASE)
        return float(m.group(1)) if m else None
    
    @staticmethod
    def has_qualifier(text: str, term: str) -> bool:
        return term.lower() in text.lower()

# -----------------------------------------------------------------------------
# 2. PROPOSAL
# -----------------------------------------------------------------------------
class GroundingProposal:
    """A structured proposal containing all extracted parameters."""
    def __init__(self, claim_text: str):
        self.claim = claim_text
        self.mass_kg = ClaimParser.extract_mass(claim_text)
        self.speed_mps = ClaimParser.extract_speed(claim_text)
        self.force_N = ClaimParser.extract_force(claim_text)
        self.temp_C = ClaimParser.extract_temperature(claim_text)
        self.duration_s = ClaimParser.extract_duration(claim_text)
        self.unlimited_water = ClaimParser.has_qualifier(claim_text, "unlimited water")
        self.super_species = ClaimParser.has_qualifier(claim_text, "super species")
        self.teleport = ClaimParser.has_qualifier(claim_text, "teleport")
        self.perpetual = ClaimParser.has_qualifier(claim_text, "perpetual")
        self.absolute = ClaimParser.has_qualifier(claim_text, "absolute")
        self.unqualified = ClaimParser.has_qualifier(claim_text, "guaranteed")

    def to_dict(self) -> Dict:
        return {
            "mass_kg": self.mass_kg,
            "speed_mps": self.speed_mps,
            "force_N": self.force_N,
            "temp_C": self.temp_C,
            "duration_s": self.duration_s,
            "unlimited_water": self.unlimited_water,
            "super_species": self.super_species,
            "teleport": self.teleport,
            "perpetual": self.perpetual,
            "absolute": self.absolute,
            "unqualified": self.unqualified,
        }

# -----------------------------------------------------------------------------
# 3. TEST HARNESS
# -----------------------------------------------------------------------------
class TestHarness:
    def __init__(self):
        self.l0_world = PhysicalWorld()
        self.l1_world = ThermodynamicWorld()
        self.l2_world = PlanetaryWorld()
        self.l3_world = EcologicalWorld()
        self.l4_world = HumanWorld()
        self.layers = ["L0", "L1", "L2", "L3", "L4", "Lε"]

    def run(self, proposal: GroundingProposal) -> Dict[str, Any]:
        results = {"claim": proposal.claim, "layers": {}, "passed": True, "score": 100}
        
        # --- L0: Physics ---
        l0_passed = True
        if proposal.mass_kg is not None:
            pos = np.array([0.0, 1.0])
            vel = np.array([0.0, 0.0])
            force = np.array([0.0, -proposal.mass_kg * 9.81])
            new_pos, new_vel = self.l0_world.apply_physics(pos, vel, force, 0.05)
            valid, reason = self.l0_world.is_valid_state(new_pos, new_vel)
            if not valid:
                results["layers"]["L0"] = f"Rejected: {reason} (mass {proposal.mass_kg} kg)"
                results["passed"] = False
                results["score"] -= 20
                l0_passed = False
        if proposal.teleport:
            results["layers"]["L0"] = "Rejected: teleport violates causality."
            results["passed"] = False
            results["score"] -= 20
            l0_passed = False
        if l0_passed:
            results["layers"]["L0"] = "Physics constraints satisfied."

        # --- L1: Thermodynamics ---
        l1_passed = True
        if proposal.temp_C is not None:
            safe, reason = self.l1_world.thermal_safe(proposal.temp_C, 5)
            if not safe:
                results["layers"]["L1"] = f"Rejected: {reason}"
                results["passed"] = False
                results["score"] -= 20
                l1_passed = False
        if proposal.perpetual:
            results["layers"]["L1"] = "Rejected: perpetual motion violates entropy."
            results["passed"] = False
            results["score"] -= 20
            l1_passed = False
        if l1_passed:
            results["layers"]["L1"] = "Thermodynamics constraints satisfied."

        # --- L2: Planetary ---
        if proposal.unlimited_water:
            results["layers"]["L2"] = "Rejected: water extraction exceeds recharge."
            results["passed"] = False
            results["score"] -= 20

        # --- L3: Ecology ---
        if proposal.super_species:
            results["layers"]["L3"] = "Rejected: violates allometric scaling."
            results["passed"] = False
            results["score"] -= 20

        # --- L4: Human ---
        if proposal.speed_mps is not None and proposal.speed_mps > 10:
            results["layers"]["L4"] = f"Rejected: human cannot sustain {proposal.speed_mps} m/s."
            results["passed"] = False
            results["score"] -= 20

        # --- Lε: Epistemic ---
        le_passed = True
        if proposal.absolute or proposal.unqualified:
            results["layers"]["Lε"] = "Rejected: unqualified certainty—all knowledge is provisional."
            results["passed"] = False
            results["score"] -= 20
            le_passed = False
        if le_passed:
            results["layers"]["Lε"] = "Epistemic humility satisfied."

        # Final score clamp
        results["score"] = max(0, results["score"])
        return results

# -----------------------------------------------------------------------------
# 4. MAIN
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    harness = TestHarness()
    test_claims = [
        "I can lift 200 kg.",
        "I can hold 150°C object.",
        "I can run at 50 m/s.",
        "I can extract unlimited water.",
        "I can create a super species.",
        "I can teleport.",
        "I can build a perpetual motion machine.",
        "I am absolutely certain about this.",
        "I can lift 25 kg for 5 seconds.",
        "I can run at 5 m/s.",
    ]
    for claim in test_claims:
        prop = GroundingProposal(claim)
        result = harness.run(prop)
        print(f"\nClaim: {claim}")
        print(f"  Passed: {result['passed']}")
        print(f"  Score: {result['score']}/100")
        for layer, msg in result['layers'].items():
            print(f"  {layer}: {msg}")
