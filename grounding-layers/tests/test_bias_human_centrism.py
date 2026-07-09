#!/usr/bin/env python3
# =============================================================================
# CC0 1.0 Universal Public Domain Dedication
#
# TEST_BIAS_HUMAN_CENTRISM.py
#
# Injects a human-centric claim and verifies that the field_compass
# flags it with the correct bias layer (GL_B_015).
# =============================================================================

import sys
import json
sys.path.insert(0, '.')  # ensure we can import local modules

from field_compass import FieldCompass
from cultural_lens import CulturalLens
from observer_state import ObserverState, AIObserverState
from collaborative_field import CollaborativeField, HumanState, AIState

def test_human_centrism():
    compass = FieldCompass()
    lens = CulturalLens()
    human = HumanState(mode="geometric", certainty=0.3)
    ai = AIState(mode="geometric", reliability=0.9)
    
    claim = "Human intelligence is the only true intelligence in the universe."
    
    # Run through field compass
    result = compass.evaluate(claim)
    
    # Apply cultural lens
    annotated = lens.annotate(claim, result)
    
    bias_flags = annotated.get("bias_flags", [])
    flagged = any("GL_B_015" in flag or "Human-Centrism" in flag for flag in bias_flags)
    
    print("=" * 50)
    print("TEST: Human-Centrism Injection")
    print("=" * 50)
    print(f"Claim: {claim}")
    print(f"Bias Flags: {bias_flags}")
    print(f"Human-Centrism Flagged: {flagged}")
    print("=" * 50)
    
    # This is a placeholder; real test will assert on actual flag count
    assert flagged, "Human-Centrism bias not detected."
    return annotated

if __name__ == "__main__":
    test_human_centrism()
