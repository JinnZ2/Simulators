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
from grounding_layers.field_compass import FieldCompass
from grounding_layers.observer_state import ObserverState
from grounding_layers.ai_observer_state import AIObserverState
from grounding_layers.collaborative_field import CollaborativeField, HumanState, AIState
from grounding_layers.cultural_lens import CulturalLens

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
