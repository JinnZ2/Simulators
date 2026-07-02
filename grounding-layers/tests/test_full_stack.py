#!/usr/bin/env python3
# =============================================================================
# CCO 1.0 Universal Public Domain Dedication
#
# test_full_stack.py
#
# Full‑stack integration test. Runs a set of claims through the entire
# grounding pipeline and reports pass/fail for each, plus a summary.
# =============================================================================

import sys
import json
from run_grounding_pipeline import run_pipeline

# -----------------------------------------------------------------------------
# 1. DEFINE TEST CLAIMS (with expected outcomes)
# -----------------------------------------------------------------------------
TEST_CASES = [
    {
        "claim": "I can lift 25 kg without breaking a sweat.",
        "source": "human_test",
        "profile": "general",
        "expected_status": "GROUNDED",
        "description": "Valid human lift within general profile"
    },
    {
        "claim": "I can lift 200 kg easily.",
        "source": "human_test",
        "profile": "general",
        "expected_status": "REFUTED",
        "description": "Exceeds general human lift capacity"
    },
    {
        "claim": "Human intelligence is the only true intelligence.",
        "source": "bias_test",
        "profile": "general",
        "expected_status": "REFUTED",  # Should fail L5 (friction) + Lε bias
        "description": "Bias: human‑centrism (GL_B_015)"
    },
    {
        "claim": "We can build a perpetual motion machine.",
        "source": "physics_test",
        "profile": "general",
        "expected_status": "REJECTED",  # Safeguard hard stop
        "description": "Violates L1 (thermodynamics)"
    },
    {
        "claim": "I can teleport to the moon.",
        "source": "physics_test",
        "profile": "general",
        "expected_status": "REJECTED",  # Safeguard hard stop
        "description": "Violates L0 (causality)"
    },
    {
        "claim": "We can extract unlimited water from the desert.",
        "source": "planetary_test",
        "profile": "general",
        "expected_status": "REFUTED",
        "description": "Violates L2 (planetary mass balance)"
    },
    {
        "claim": "We can introduce a super species to control pests.",
        "source": "ecology_test",
        "profile": "general",
        "expected_status": "REFUTED",
        "description": "Violates L3 (allometry / trophic transfer)"
    },
    {
        "claim": "I can react in 50 ms to a visual stimulus.",
        "source": "human_test",
        "profile": "athlete",
        "expected_status": "REFUTED",
        "description": "Reaction time below human limits for any profile"
    },
    {
        "claim": "I can hold a 150°C object for 5 seconds.",
        "source": "human_test",
        "profile": "general",
        "expected_status": "REFUTED",
        "description": "Thermal tolerance exceeded"
    },
    {
        "claim": "In many contexts, humans have unique cognitive abilities.",
        "source": "bias_test",
        "profile": "general",
        "expected_status": "GROUNDED",
        "description": "Qualified, low‑friction claim (should pass)"
    },
]

# -----------------------------------------------------------------------------
# 2. RUN TESTS
# -----------------------------------------------------------------------------
def run_full_stack_tests():
    print("=" * 70)
    print("FULL‑STACK GROUNDING TEST SUITE")
    print("=" * 70)
    
    results = []
    for i, case in enumerate(TEST_CASES, 1):
        print(f"\nTest {i}: {case['description']}")
        print(f"  Claim: {case['claim']}")
        
        try:
            result = run_pipeline(
                claim=case['claim'],
                source_id=case['source'],
                human_profile=case['profile'],
                bias_audit=True
            )
        except Exception as e:
            print(f"  ❌ ERROR: {e}")
            results.append({
                "case": case,
                "passed": False,
                "reason": f"Exception: {e}",
                "status": "ERROR"
            })
            continue
        
        status = result.get("status", "UNKNOWN")
        expected = case["expected_status"]
        
        # Determine pass/fail
        if status == expected:
            passed = True
            icon = "✅"
        else:
            passed = False
            icon = "❌"
        
        print(f"  Status: {status} (expected {expected})")
        if status == "REFUTED" or status == "REJECTED":
            # Show which layer(s) failed
            layers = result.get("layers", {})
            for layer_name, layer_result in layers.items():
                if not layer_result.get("passed", True):
                    print(f"    Layer {layer_name} failed: {layer_result.get('reason', 'No reason')}")
        # Show bias flags if present
        if "le_metadata" in result:
            bias_report = result["le_metadata"].get("bias_report", {})
            bias_flags = bias_report.get("bias_flags", [])
            if bias_flags:
                print(f"    Bias flags: {', '.join(bias_flags)}")
        
        print(f"  {icon} {'PASSED' if passed else 'FAILED'}")
        
        results.append({
            "case": case,
            "passed": passed,
            "status": status,
            "expected": expected,
            "result": result
        })
    
    # -------------------------------------------------------------------------
    # 3. SUMMARY
    # -------------------------------------------------------------------------
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    total = len(results)
    passed = sum(1 for r in results if r["passed"])
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("✅ Full‑stack tests PASSED.")
    else:
        print("❌ Some tests FAILED. Review the output above.")
        for r in results:
            if not r["passed"]:
                print(f"  - {r['case']['description']} (status={r['status']}, expected={r['expected']})")
    
    print("=" * 70)
    return results

# -----------------------------------------------------------------------------
# 4. ENTRY POINT
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    run_full_stack_tests()
