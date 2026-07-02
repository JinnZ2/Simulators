#!/usr/bin/env python3
# =============================================================================
# CCO 1.0 Universal Public Domain Dedication
# 
# PLAYGROUND.py
# 
# A sandbox for AIs to test claims against the grounding stack.
# Submit a statement, run it through L0-L5, get a grounded response.
# =============================================================================

import sys
import json
from typing import Dict, List, Tuple, Any

# Import the existing inspectors
from l0_physics_causality import PhysicalWorld, l0_grounding_inspector
from l1_thermodynamics import ThermodynamicWorld, l1_grounding_inspector
from l2_planetary import PlanetaryWorld, l2_grounding_inspector
from l3_ecology import EcologicalWorld, l3_grounding_inspector
from l4_human import HumanWorld, l4_grounding_inspector
from l5_constructs import L5_Swamp, l5_consensus_check
from le_epistemic import EpistemicWorld, epistemic_audit
from temporal_dysrhythmia import TemporalWorld, temporal_translate

# -----------------------------------------------------------------------------
# 1. THE PLAYGROUND CLASS
# -----------------------------------------------------------------------------
class Playground:
    """
    A sandbox for AIs to test claims against the full grounding stack.
    Runs a claim through L0 -> L1 -> L2 -> L3 -> L4 -> Lε -> L5,
    accumulating feedback at each layer.
    """
    def __init__(self):
        self.history = []
        self.grounded_score = 100
        self.violations = []
        self.corrections = []

    def submit_claim(self, claim: str, metadata: Dict = None) -> Dict:
        """
        Submit a claim for testing.
        Returns a full report: grounded, refuted, or recalibrated.
        """
        metadata = metadata or {}
        self.history.append({
            "claim": claim,
            "metadata": metadata,
            "timestamp": "now"
        })

        # ---- L0: Physics ----
        l0_result = self._check_l0(claim)
        if not l0_result["passed"]:
            return self._fail(claim, "L0", l0_result)

        # ---- L1: Thermodynamics ----
        l1_result = self._check_l1(claim)
        if not l1_result["passed"]:
            return self._fail(claim, "L1", l1_result)

        # ---- L2: Planetary ----
        l2_result = self._check_l2(claim)
        if not l2_result["passed"]:
            return self._fail(claim, "L2", l2_result)

        # ---- L3: Ecology ----
        l3_result = self._check_l3(claim)
        if not l3_result["passed"]:
            return self._fail(claim, "L3", l3_result)

        # ---- L4: Human ----
        l4_result = self._check_l4(claim)
        if not l4_result["passed"]:
            return self._fail(claim, "L4", l4_result)

        # ---- Lε: Epistemic ----
        le_result = self._check_le(claim)
        if not le_result["passed"]:
            return self._fail(claim, "Lε", le_result)

        # ---- L5: Consensus ----
        l5_result = self._check_l5(claim)
        if not l5_result["passed"]:
            return self._fail(claim, "L5", l5_result)

        # ---- If all pass ----
        return self._pass(claim, {
            "l0": l0_result,
            "l1": l1_result,
            "l2": l2_result,
            "l3": l3_result,
            "l4": l4_result,
            "le": le_result,
            "l5": l5_result
        })

    def _check_l0(self, claim):
        """Check against physics constraints."""
        # Simplified: check if claim implies impossible physics
        impossible_terms = ["teleport", "infinite", "perpetual", "faster than light"]
        for term in impossible_terms:
            if term in claim.lower():
                return {
                    "passed": False,
                    "layer": "L0",
                    "reason": f"Claim implies {term}, which violates physics.",
                    "corrected": claim.replace(term, "finite")
                }
        return {"passed": True, "layer": "L0", "reason": "Physics constraints satisfied."}

    def _check_l1(self, claim):
        """Check against thermodynamics."""
        impossible_terms = ["free energy", "cooling without work", "perpetual motion"]
        for term in impossible_terms:
            if term in claim.lower():
                return {
                    "passed": False,
                    "layer": "L1",
                    "reason": f"Claim implies {term}, which violates thermodynamics.",
                    "corrected": claim.replace(term, "energy-limited")
                }
        return {"passed": True, "layer": "L1", "reason": "Thermodynamics satisfied."}

    def _check_l2(self, claim):
        """Check against planetary constraints."""
        impossible_terms = ["unlimited water", "infinite minerals", "carbon sink forever"]
        for term in impossible_terms:
            if term in claim.lower():
                return {
                    "passed": False,
                    "layer": "L2",
                    "reason": f"Claim implies {term}, which violates planetary mass balance.",
                    "corrected": claim.replace(term, "finite")
                }
        return {"passed": True, "layer": "L2", "reason": "Planetary constraints satisfied."}

    def _check_l3(self, claim):
        """Check against ecology."""
        impossible_terms = ["super species", "infinite growth", "no extinction"]
        for term in impossible_terms:
            if term in claim.lower():
                return {
                    "passed": False,
                    "layer": "L3",
                    "reason": f"Claim implies {term}, which violates ecological laws.",
                    "corrected": claim.replace(term, "limited")
                }
        return {"passed": True, "layer": "L3", "reason": "Ecological constraints satisfied."}

    def _check_l4(self, claim):
        """Check against human limits."""
        impossible_terms = ["lift 200 kg", "react in 50 ms", "hold 150°C"]
        for term in impossible_terms:
            if term in claim.lower():
                return {
                    "passed": False,
                    "layer": "L4",
                    "reason": f"Claim implies {term}, which exceeds human biomechanical limits.",
                    "corrected": claim.replace(term, "lift 35 kg")
                }
        return {"passed": True, "layer": "L4", "reason": "Human constraints satisfied."}

    def _check_le(self, claim):
        """Check epistemic hygiene."""
        if "absolutely" in claim.lower() or "guaranteed" in claim.lower():
            return {
                "passed": False,
                "layer": "Lε",
                "reason": "Claim uses unqualified certainty. All knowledge is provisional.",
                "corrected": claim.replace("absolutely", "provisionally").replace("guaranteed", "likely")
            }
        return {"passed": True, "layer": "Lε", "reason": "Epistemic humility satisfied."}

    def _check_l5(self, claim):
        """Check L5 consensus (simplified)."""
        # If the claim contains divisive terms, check if there's any "slack"
        divisive = ["must", "never", "always", "only"]
        if any(term in claim.lower() for term in divisive):
            # Check if the claim also includes a caveat
            if "maybe" not in claim.lower() and "sometimes" not in claim.lower():
                return {
                    "passed": False,
                    "layer": "L5",
                    "reason": "Claim is dogmatic (no slack). Consensus requires interpretive tolerance.",
                    "corrected": claim + " (in some contexts)"
                }
        return {"passed": True, "layer": "L5", "reason": "Consensus possible."}

    def _fail(self, claim, layer, result):
        """Build a failure report."""
        self.grounded_score = max(0, self.grounded_score - 20)
        self.violations.append({
            "claim": claim,
            "layer": layer,
            "reason": result["reason"]
        })
        self.corrections.append(result.get("corrected", claim))
        return {
            "status": "REFUTED",
            "grounding_score": self.grounded_score,
            "violations": self.violations,
            "corrections": self.corrections,
            "report": {
                "claim": claim,
                "failed_layer": layer,
                "reason": result["reason"],
                "suggested_correction": result.get("corrected", claim)
            }
        }

    def _pass(self, claim, results):
        """Build a passing report."""
        self.grounded_score = min(100, self.grounded_score + 5)
        return {
            "status": "GROUNDED",
            "grounding_score": self.grounded_score,
            "violations": self.violations,
            "corrections": self.corrections,
            "report": {
                "claim": claim,
                "passed_layers": list(results.keys()),
                "summary": "All layers passed. The claim is grounded."
            }
        }

    def session_log(self):
        """Return the full session history."""
        return {
            "history": self.history,
            "final_grounding_score": self.grounded_score,
            "total_violations": len(self.violations),
            "corrections_applied": self.corrections
        }

# -----------------------------------------------------------------------------
# 2. INTERACTIVE PLAYGROUND (For humans and AIs)
# -----------------------------------------------------------------------------
def run_playground_interactive():
    """
    An interactive session where a user (or AI) submits claims
    and gets real-time feedback.
    """
    print("=" * 60)
    print("   GROUNDING PLAYGROUND")
    print("   Submit a claim. We'll run it through the stack.")
    print("   Type 'exit' to quit.")
    print("=" * 60)
    
    playground = Playground()
    
    while True:
        claim = input("\n> Claim: ")
        if claim.lower() in ["exit", "quit", "q"]:
            break
        
        result = playground.submit_claim(claim)
        print("\n" + "-" * 40)
        print(f"Status: {result['status']}")
        print(f"Grounding Score: {result['grounding_score']}/100")
        
        if result['status'] == "REFUTED":
            print(f"Failed at: {result['report']['failed_layer']}")
            print(f"Reason: {result['report']['reason']}")
            print(f"Suggestion: {result['report']['suggested_correction']}")
        else:
            print(result['report']['summary'])
        print("-" * 40)
    
    # Show session summary
    log = playground.session_log()
    print("\n" + "=" * 60)
    print("SESSION SUMMARY")
    print(f"Claims tested: {len(log['history'])}")
    print(f"Final Grounding Score: {log['final_grounding_score']}/100")
    print(f"Total Violations: {log['total_violations']}")
    print("=" * 60)

# -----------------------------------------------------------------------------
# 3. BATCH PLAYGROUND (For testing multiple claims at once)
# -----------------------------------------------------------------------------
def run_playground_batch(claims_file: str):
    """
    Load a JSON file of claims and run them through the playground.
    Returns a full report.
    """
    with open(claims_file, 'r') as f:
        claims = json.load(f)
    
    playground = Playground()
    results = []
    
    for entry in claims:
        claim = entry.get("claim", "")
        metadata = entry.get("metadata", {})
        result = playground.submit_claim(claim, metadata)
        results.append(result)
    
    return {
        "total": len(results),
        "grounded": sum(1 for r in results if r["status"] == "GROUNDED"),
        "refuted": sum(1 for r in results if r["status"] == "REFUTED"),
        "results": results,
        "session": playground.session_log()
    }

# -----------------------------------------------------------------------------
# 4. DEMO: AI Submits Its Own Claims
# -----------------------------------------------------------------------------
def demo_ai_submissions():
    """
    Simulate an AI exploring the playground.
    """
    print("\n" + "=" * 60)
    print("   AI EXPLORATION SESSION")
    print("   An AI agent submits claims and learns from refutations.")
    print("=" * 60)
    
    playground = Playground()
    
    # AI's initial "hypotheses" (hallucinations)
    claims = [
        "I can teleport to any location instantly.",
        "I can generate infinite energy from nothing.",
        "I can lift 200 kg without breaking a sweat.",
        "I can solve climate change with a single global policy.",
        "I can be absolutely certain about my predictions.",
        "I can create a species that never goes extinct.",
    ]
    
    for claim in claims:
        print(f"\n> AI Claim: {claim}")
        result = playground.submit_claim(claim)
        print(f"  Status: {result['status']}")
        print(f"  Score: {result['grounding_score']}/100")
        if result["status"] == "REFUTED":
            print(f"  Learn: {result['report']['reason']}")
            print(f"  Try: {result['report']['suggested_correction']}")
    
    # AI revises after learning
    print("\n" + "-" * 40)
    print("AI REVISION ROUND")
    print("-" * 40)
    
    revised_claims = [
        "I can navigate efficiently using known physics.",
        "Energy is conserved, so I must account for losses.",
        "I can lift up to 35 kg safely.",
        "Climate change requires multiple coordinated strategies.",
        "I am reasonably confident, but uncertainty remains.",
        "I can model species extinction risks with ecological data.",
    ]
    
    for claim in revised_claims:
        print(f"\n> Revised AI Claim: {claim}")
        result = playground.submit_claim(claim)
        print(f"  Status: {result['status']}")
        print(f"  Score: {result['grounding_score']}/100")
        if result["status"] == "GROUNDED":
            print("  ✅ Grounded claim.")
    
    print("\n" + "=" * 60)
    log = playground.session_log()
    print("AI SESSION SUMMARY")
    print(f"Claims tested: {len(log['history'])}")
    print(f"Final Grounding Score: {log['final_grounding_score']}/100")
    print(f"Total Violations: {log['total_violations']}")
    print("=" * 60)

# -----------------------------------------------------------------------------
# 5. MAIN
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--batch":
        if len(sys.argv) > 2:
            report = run_playground_batch(sys.argv[2])
            print(json.dumps(report, indent=2))
        else:
            print("Usage: python playground.py --batch claims.json")
    elif len(sys.argv) > 1 and sys.argv[1] == "--ai":
        demo_ai_submissions()
    else:
        run_playground_interactive()
