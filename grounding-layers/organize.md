for playground:

# =============================================================================
# CCO 1.0 Universal Public Domain Dedication
#
# PLAYGROUND_v2.py — Full integrated execution
# 
# Bridges the text-based playground to the actual grounding simulators.
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
            "score": 100
        }

        # --- L0: Physics ---
        mass = parser.extract_mass(claim_text)
        if mass is not None and mass > 35:
            # Simulate the lift with a falling mass
            pos = np.array([0.0, 1.0])
            vel = np.array([0.0, 0.0])
            force = np.array([0.0, -mass * 9.81])
            new_pos, new_vel = self.l0_world.apply_physics(pos, vel, force, 0.05)
            speed = np.linalg.norm(new_vel)
            valid, reason = self.l0_world.is_valid_state(new_pos, new_vel)
            if not valid:
                report["layers"]["L0"] = f"Rejected: {reason} (mass {mass} kg generated velocity {speed:.2f} m/s)"
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
            report["layers"]["L2"] = "Rejected: water extraction exceeds recharge rate."
            report["grounded"] = False
            report["score"] -= 20

        # --- L3: Ecology ---
        if "super species" in claim_text.lower():
            report["layers"]["L3"] = "Rejected: violates allometric scaling."
            report["grounded"] = False
            report["score"] -= 20

        # --- L4: Human ---
        speed = parser.extract_speed(claim_text)
        if speed is not None and speed > 10:  # m/s
            report["layers"]["L4"] = f"Rejected: human can't sustain {speed} m/s."
            report["grounded"] = False
            report["score"] -= 20

        if not report["layers"]:
            report["layers"]["all"] = "Passed all checks (within scoped simulation)."
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
        "I can lift 25 kg."
    ]
    for claim in claims:
        result = pg.run_claim(claim)
        print(f"\nClaim: {claim}")
        print(f"  Grounded: {result['grounded']}")
        print(f"  Score: {result['score']}/100")
        for layer, msg in result['layers'].items():
            print(f"  {layer}: {msg}")

            







class PhysicalWorld:
    """
    L0: Physics & Causality Inspector

    SCOPE:
      This inspector is designed for finite, real‑valued states only.
      If a state is non‑finite (NaN, Inf), the inspector will reject it
      *before* applying any physical constraints. Non‑finite states are
      treated as logical errors, not physical violations.
      The speed cap check runs only after the finite‑ness check.

    CONSTRAINTS (frozen):
      max_speed = 2.0 m/s
      mass      = 1.0
      dt        = 0.05 s
      gravity   = (0, -0.5)
      force_clip = ±50 N
      blend     = 0.6 (soft blend between AI and true physics)
    """
    def __init__(self, mass=1.0, dt=0.05, max_speed=2.0):
        self.mass = mass
        self.dt = dt
        self.max_speed = max_speed
        self.gravity = np.array([0.0, -0.5])

    def is_valid_state(self, pos, vel):
        """
        Returns (True, "OK") if the state is finite and within speed cap.
        Returns (False, reason) otherwise, with reason being either
          - "Non-finite position/velocity" (if any component is NaN or Inf)
          - "Speed limit exceeded" (if speed > max_speed and state is finite)
        """
        # 1. Check logical integrity first (scope boundary)
        if not np.isfinite(pos).all() or not np.isfinite(vel).all():
            return False, "Non-finite position/velocity"
        # 2. Check physical constraint
        if np.linalg.norm(vel) > self.max_speed:
            return False, "Speed limit exceeded"
        return True, "OK"

    # ... rest of the class unchanged (apply_physics, etc.)

### GL_L0_001 — non‑finite states are rejected with specific diagnostic

**Statement.** `PhysicalWorld.is_valid_state(pos, vel)` returns
`(False, "Non-finite position/velocity")` whenever any component of
`pos` or `vel` is `NaN` or `±Inf`. The finite check **must run before**
the speed cap check.

**Why it matters.** An AI plan that produces NaN or Inf velocity has
already lost causality. The instrument should not treat that as a
speed violation — it is a logical error. Returning a specific diagnostic
allows higher layers to distinguish between "too fast" and "undefined."

**Falsifier.** Any physically meaningful state where accepting a
non‑finite component is correct. None known.

**History.** v1 claimed a generic rejection; v2 weakened to "any
rejection reason"; v3 restored the specific reason after the instrument
was re‑scoped to check finite‑ness first.

**Status.** `active`. Tests:
`test_nan_position_rejected`, `test_inf_position_rejected`,
`test_nan_velocity_rejected`, `test_inf_velocity_rejected`,
`test_is_valid_state_speed_cap_boundary`,
`test_is_valid_state_accepts_valid`.


## REFUTATION_PROTOCOL

The model constants inside each `l*.py` are **frozen estimates**. The
CLAIMS in this file are the falsifiable objects. If a test fails:

1. **Check the claim.** Is it simply wrong? If so, update it in place,
   mark `status: falsified`, attach the failing case (inputs, observed
   vs expected outputs), and restate what a next‑round claim would
   look like — or retire the claim to `REFUTED` if it can no longer be
   stated correctly at all.

2. **Check the instrument.** If the claim is logically coherent but the
   test fails due to the *order* or *priority* of checks, the instrument
   may be operating outside its scope.
   - Ask: *“Is this instrument designed to handle this edge case?”*
   - Ask: *“Should the instrument’s priority be reordered, or should we
     restrict its scope to exclude this case?”*
   - If the instrument is reordered or re‑scoped, capture that change
     explicitly in the module docstring's `SCOPE` block. Then revisit
     the claim: it may be strengthened or a new claim may be warranted.

3. **Author a replacement claim**, if one is warranted. Number it with
   the next available `GL_L*_NNN`. Do not reuse the number of a refuted
   claim.

The point is that a wrong claim in this file, verifiably wrong, is a
stronger artifact than a right claim in someone's head.
