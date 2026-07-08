#!/usr/bin/env python3
# =============================================================================
# CC0 1.0 Universal Public Domain Dedication
#
# audit_l0.py
#
# Runs a full L0 audit: constants, claims, tests, demo, and scope.
# =============================================================================

import subprocess
import sys
import numpy as np
from l0_physics_causality import PhysicalWorld, l0_grounding_inspector, ai_hallucinated_plan

def audit_constants():
    """Verify frozen constants haven't drifted."""
    world = PhysicalWorld()
    expected = {
        "max_speed": 2.0,
        "mass": 1.0,
        "dt": 0.05,
        "gravity": (0.0, -0.5),
    }
    actual = {
        "max_speed": world.max_speed,
        "mass": world.mass,
        "dt": world.dt,
        "gravity": tuple(world.gravity),
    }
    for k, v in expected.items():
        if actual[k] != v:
            return False, f"{k}: expected {v}, got {actual[k]}"
    return True, "Constants locked."

def audit_tests():
    """Run the test suite."""
    result = subprocess.run(
        ["pytest", "test_l0_physics_causality.py", "-v", "--tb=short"],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        return False, f"Tests failed:\n{result.stdout}\n{result.stderr}"
    return True, "All tests passed."

def audit_demo():
    """Verify pinned demo numbers."""
    # Run the demo and capture output
    # This is a simplified check; we'll compare key numbers
    np.random.seed(0)
    ai_traj, ai_forces = ai_hallucinated_plan(200)
    corrected_traj, violations, penalties = l0_grounding_inspector(ai_traj, ai_forces, PhysicalWorld())
    
    violations_sum = np.sum(violations)
    ai_max_speed = np.max(np.linalg.norm(np.diff(ai_traj, axis=0), axis=1) / 0.05)
    grounded_max_speed = np.max(np.linalg.norm(np.diff(corrected_traj, axis=0), axis=1) / 0.05)
    ai_end_y = ai_traj[-1, 1]
    grounded_end_y = corrected_traj[-1, 1]
    drift = np.linalg.norm(ai_traj[-1] - corrected_traj[-1])
    
    # Compare to pinned values (with tolerance)
    tol = 0.05
    checks = [
        (abs(violations_sum - 180) <= 1, f"Violations: expected ~180, got {violations_sum}"),
        (abs(ai_max_speed - 100.0) < 0.1, f"AI max speed: expected 100.0, got {ai_max_speed:.3f}"),
        (abs(grounded_max_speed - 2.025) < tol, f"Grounded max speed: expected 2.025, got {grounded_max_speed:.3f}"),
        (abs(ai_end_y - 1.065) < tol, f"AI end y: expected 1.065, got {ai_end_y:.3f}"),
        (abs(grounded_end_y - (-13.10)) < tol, f"Grounded end y: expected -13.10, got {grounded_end_y:.3f}"),
        (abs(drift - 14.17) < tol, f"Drift: expected 14.17, got {drift:.3f}"),
    ]
    for passed, msg in checks:
        if not passed:
            return False, msg
    return True, "Demo numbers match pinned values."

def audit_scope():
    """Check that SCOPE block is present in docstring."""
    import l0_physics_causality as mod
    doc = mod.__doc__ or ""
    if "SCOPE" not in doc:
        return False, "SCOPE block missing from docstring."
    return True, "Scope declared."

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("L0 AUDIT")
    print("=" * 60)
    
    checks = [
        ("Constants", audit_constants),
        ("Tests", audit_tests),
        ("Demo", audit_demo),
        ("Scope", audit_scope),
    ]
    
    all_passed = True
    for name, func in checks:
        passed, msg = func()
        status = "✅" if passed else "❌"
        print(f"{status} {name}: {msg}")
        if not passed:
            all_passed = False
    
    print("=" * 60)
    if all_passed:
        print("✅ L0 audit passed. You may proceed to L1.")
    else:
        print("❌ L0 audit failed. Resolve issues before proceeding.")
    print("=" * 60)
