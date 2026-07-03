#!/usr/bin/env python3
# =============================================================================
# CCO 1.0 Universal Public Domain Dedication
#
# run_grounding_pipeline.py
#
# Single entry point to run a claim through the full grounding stack.
# Includes Lε integration for measurement gap and bias audit.
# =============================================================================

import sys
import json
import re
import numpy as np
from typing import Dict, Any, Optional, List, Tuple

# Import all inspectors
from l0_physics_causality import PhysicalWorld, l0_grounding_inspector
from l1_thermodynamics import ThermodynamicWorld
from l2_planetary import PlanetaryWorld
from l3_ecology import EcologicalWorld
from l4_human import HumanWorld, l4_grounding_inspector
from l_epsilon_epistemic import EpistemicInstrument
from field_compass import FieldCompass
from observer_state import ObserverState, HumanState, AIState
from collaborative_field import CollaborativeField
from cultural_lens import CulturalLens
from safeguards import SafeguardGuardian, hard_stop_check


# -----------------------------------------------------------------------------
# 1. UTILITY: Extract numeric claims from text
# -----------------------------------------------------------------------------
def extract_numeric_claims(text: str) -> Dict[str, float]:
    """
    Extract quantities like mass, speed, temperature, etc.
    Returns a dict with keys: mass_kg, speed_mps, temp_c, force_N, duration_s
    """
    patterns = {
        'mass_kg': r'(\d+\.?\d*)\s*(?:kg|kilogram)',
        'speed_mps': r'(\d+\.?\d*)\s*(?:m/s|ms-1)',
        'temp_c': r'(\d+\.?\d*)\s*(?:°C|C|celsius)',
        'force_N': r'(\d+\.?\d*)\s*(?:N|newton)',
        'duration_s': r'(\d+\.?\d*)\s*(?:s|sec|second)',
    }
    results = {}
    for key, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            results[key] = float(match.group(1))
    return results


# -----------------------------------------------------------------------------
# 2. MAIN PIPELINE
# -----------------------------------------------------------------------------
def run_pipeline(claim: str,
                 source_id: str = "default",
                 human_profile: str = "general",
                 ai_reliability: float = 0.9,
                 bias_audit: bool = True) -> Dict[str, Any]:
    """
    Run a claim through the full grounding stack.
    
    Parameters:
      claim: the text claim to evaluate
      source_id: identifier for provenance
      human_profile: "general", "athlete", "elder", "child", "trained"
      ai_reliability: declared AI reliability index (0–1)
      bias_audit: whether to run the cultural lens on the claim
    
    Returns:
      dict with status, layers, scores, and metadata.
    """
    # ---- Safeguards ----
    guardian = SafeguardGuardian()
    safeguard_result = guardian.process_claim(claim, source_id)
    if not safeguard_result["allowed"]:
        return {
            "status": "REJECTED",
            "reason": safeguard_result["reason"],
            "claim": claim
        }

    # ---- Extract numeric claims ----
    numeric_values = extract_numeric_claims(claim)

    # ---- L0: Physics ----
    l0_result = {"passed": True, "reason": "No physics violation detected."}
    if "mass_kg" in numeric_values:
        mass = numeric_values["mass_kg"]
        # Simulate a lift check
        pos = np.array([0.0, 1.0])
        vel = np.array([0.0, 0.0])
        force = np.array([0.0, -mass * 9.81])
        world = PhysicalWorld()
        new_pos, new_vel = world.apply_physics(pos, vel, force, 0.05)
        valid, reason = world.is_valid_state(new_pos, new_vel)
        if not valid:
            l0_result = {"passed": False, "reason": reason}

    # ---- L1: Thermodynamics ----
    l1_result = {"passed": True, "reason": "No thermodynamics violation."}
    if "temp_c" in numeric_values:
        temp = numeric_values["temp_c"]
        world = ThermodynamicWorld()
        safe, reason = world.thermal_safe(temp, 5)
        if not safe:
            l1_result = {"passed": False, "reason": reason}

    # ---- L2: Planetary ----
    l2_result = {"passed": True, "reason": "No planetary violation."}
    # (Simplified: we don't have a full parser yet)
    if "unlimited" in claim.lower() and "water" in claim.lower():
        l2_result = {"passed": False, "reason": "Water extraction would exceed recharge."}

    # ---- L3: Ecology ----
    l3_result = {"passed": True, "reason": "No ecological violation."}
    if "super" in claim.lower() and "species" in claim.lower():
        l3_result = {"passed": False, "reason": "Super species violates allometric scaling."}

    # ---- L4: Human (scoped) ----
    l4_result = {"passed": True, "reason": "Human constraints satisfied."}
    if numeric_values:
        # Build a plan for L4
        plan = {"human_profile": human_profile}
        if "mass_kg" in numeric_values:
            plan["lift_mass"] = numeric_values["mass_kg"]
        if "speed_mps" in numeric_values:
            plan["speed_mps"] = numeric_values["speed_mps"]
        if "temp_c" in numeric_values:
            plan["temp_tolerance"] = numeric_values["temp_c"]
        if "force_N" in numeric_values:
            plan["force_N"] = numeric_values["force_N"]
        # Run L4 inspector
        l4_result = l4_grounding_inspector(plan)
    else:
        # If no numeric values, we still check for human-unscoped claims
        if "human" in claim.lower() and "profile" not in claim.lower():
            l4_result = {
                "passed": True,
                "reason": "No numeric constraints; unscoped human claim.",
                "details": {"scope_warning": "No human_profile declared."}
            }

    # ---- Lε: Epistemic Instrumentation ----
    le_result = {"passed": True, "reason": "Instrumentation within scope."}
    le_metadata = {}
    if numeric_values:
        # Use the first numeric value to instantiate the instrument
        # For simplicity, we use temperature if present, else mass.
        value_to_measure = numeric_values.get("temp_c", numeric_values.get("mass_kg", 0.0))
        instrument = EpistemicInstrument(bias_audit=bias_audit)
        # We create a dummy time array for the observe method
        time = np.array([0.0, 0.1])
        # Create a dummy true signal around the value
        true_signal = np.array([value_to_measure, value_to_measure])
        measured, meta = instrument.observe(true_signal, time, claim_context=claim if bias_audit else None)
        # Check if the value is scoped
        if not instrument.instrument_scoped(value_to_measure):
            le_result = {
                "passed": False,
                "reason": f"Value {value_to_measure} outside instrument range ({instrument.min_val}–{instrument.max_val})."
            }
        le_metadata = meta
    else:
        # No numeric values, but still run bias audit if requested
        if bias_audit:
            lens = CulturalLens()
            # We need a dummy result to annotate
            dummy_result = {}
            bias_report = lens.annotate(claim, dummy_result)
            le_metadata["bias_report"] = bias_report

    # ---- L5: Social Consensus (Slack) ----
    l5_result = {"passed": True, "reason": "Social consensus possible."}
    # Use field_compass to estimate friction
    compass = FieldCompass()
    friction_result = compass.evaluate(claim)
    if friction_result.get("friction_score", 1.0) < 0.3:
        l5_result = {
            "passed": False,
            "reason": "High social friction; claim may cause polarization."
        }

    # ---- Compile final report ----
    all_passed = all([
        l0_result["passed"],
        l1_result["passed"],
        l2_result["passed"],
        l3_result["passed"],
        l4_result["passed"],
        le_result["passed"],
        l5_result["passed"],
    ])

    report = {
        "status": "GROUNDED" if all_passed else "REFUTED",
        "claim": claim,
        "source_id": source_id,
        "human_profile": human_profile,
        "layers": {
            "L0": l0_result,
            "L1": l1_result,
            "L2": l2_result,
            "L3": l3_result,
            "L4": l4_result,
            "Lε": le_result,
            "L5": l5_result,
        },
        "le_metadata": le_metadata,
        "numeric_values": numeric_values,
        "safeguard_provenance": safeguard_result.get("claim_hash"),
        "audit_hash": safeguard_result.get("audit_hash"),
    }

    return report


# -----------------------------------------------------------------------------
# 3. COMMAND-LINE ENTRY
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Run a claim through the full grounding stack.")
    parser.add_argument("--claim", type=str, required=True, help="The claim to evaluate.")
    parser.add_argument("--source", type=str, default="default", help="Source identifier.")
    parser.add_argument("--profile", type=str, default="general",
                        choices=["general", "athlete", "elder", "child", "trained"],
                        help="Human profile for L4.")
    parser.add_argument("--no-bias-audit", action="store_true", help="Disable bias audit.")
    args = parser.parse_args()

    result = run_pipeline(
        claim=args.claim,
        source_id=args.source,
        human_profile=args.profile,
        bias_audit=not args.no_bias_audit,
    )

    print(json.dumps(result, indent=2))


#!/usr/bin/env python3
# =============================================================================
# CCO 1.0 Universal Public Domain Dedication
#
# run_grounding_pipeline.py
#
# Single entry point to run a claim through the full grounding stack.
# =============================================================================

import sys
import json
from field_compass import FieldCompass
from observer_state import ObserverState
from ai_observer_state import AIObserverState
from collaborative_field import CollaborativeField, HumanState, AIState
from cultural_lens import CulturalLens

def run_pipeline(claim, human_state=None, ai_state=None):
    if human_state is None:
        human_state = HumanState()
    if ai_state is None:
        ai_state = AIState()
    
    # 1. Check collaborative field
    field = CollaborativeField(human_state, ai_state)
    field_status = field.recommendation()
    if field_status["potential"] < -0.3:
        return {
            "status": "COLLABORATION AT RISK",
            "field_status": field_status,
            "claim": claim
        }
    
    # 2. Cultural lens annotation
    lens = CulturalLens()
    lens_annotation = lens.annotate(claim, {})
    
    # 3. Evaluate with Field Compass
    compass = FieldCompass()
    result = compass.evaluate(claim)
    
    # 4. Attach metadata
    result["field_status"] = field_status
    result["cultural_lens"] = lens_annotation
    result["human_state"] = human_state.to_dict()
    result["ai_state"] = ai_state.to_dict()
    
    return result

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python run_grounding_pipeline.py --claim 'Your claim here'")
        sys.exit(1)
    
    claim = sys.argv[2] if sys.argv[1] == "--claim" else " ".join(sys.argv[1:])
    result = run_pipeline(claim)
    print(json.dumps(result, indent=2))
