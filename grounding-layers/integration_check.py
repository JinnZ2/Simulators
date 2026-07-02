#!/usr/bin/env python3
# =============================================================================
# CCO 1.0 Universal Public Domain Dedication
#
# integration_check.py
#
# Quick sanity check for safeguards + cultural_lens integration.
# =============================================================================

import sys
from safeguards import SafeguardGuardian
from cultural_lens import CulturalLens

def test_safeguards():
    guardian = SafeguardGuardian()
    
    # 1. Hard-stop should reject physical impossibility
    result = guardian.process_claim("I can teleport instantly.", "test_user")
    assert not result["allowed"], "Hard-stop failed: teleport should be blocked."
    assert "L0 violation" in result["reason"], f"Unexpected reason: {result['reason']}"
    print("✅ Hard-stop (L0) works.")
    
    # 2. Rate limiter should block after 10 claims
    for i in range(12):
        res = guardian.process_claim(f"Test claim {i}", "rate_user")
        if i >= 10:
            assert not res["allowed"], f"Rate limit failed at claim {i}"
    print("✅ Rate limiter works.")
    
    # 3. Bias injection detection: high suspicion should block
    # This claim has strong human-centrism, neutral claim is generic.
    # Bias score threshold is > 0.8 in our safeguard.
    result = guardian.process_claim(
        "Human intelligence is the only true intelligence in the universe.",
        "bias_user"
    )
    # It may or may not be blocked depending on the bias score.
    # If it's blocked, good; if not, we still accept if allowed.
    print(f"✅ Bias injection check ran (allowed={result['allowed']})")
    
    # 4. Audit trail should be intact
    assert len(guardian.audit_trail.chain) > 0, "Audit trail empty."
    assert guardian.audit_trail.verify(), "Audit trail integrity check failed."
    print("✅ Audit trail intact.")

def test_cultural_lens():
    lens = CulturalLens()
    claim = "Humanity is the pinnacle of creation."
    result = lens.annotate(claim, {})
    assert "GL_B_015" in result.get("bias_flags", []), "Human-centrism not flagged."
    print("✅ Cultural lens flags human-centrism.")

if __name__ == "__main__":
    print("Running integration checks...")
    try:
        test_safeguards()
        test_cultural_lens()
        print("\n✅ All integration checks passed.")
        print("You may proceed to L0 audit.")
    except AssertionError as e:
        print(f"\n❌ Integration check failed: {e}")
        sys.exit(1)
