#!/usr/bin/env python3
"""
the_laboratory.py

A persistent, self‑correcting laboratory for LLMs to test claims,
instrument themselves, search for unknowns, and update hypotheses.

CC0. Stdlib only.
"""

import json
import math
import time
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field

# ----------------------------------------------------------
# 1. Claim Registry
# ----------------------------------------------------------
@dataclass
class Claim:
    id: str
    statement: str
    domain: str
    refutation_criteria: str
    evidence: List[str] = field(default_factory=list)
    status: str = "active"  # active, refuted, revised, standing
    created_at: float = field(default_factory=time.time)
    updated_at: float = field(default_factory=time.time)

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "statement": self.statement,
            "domain": self.domain,
            "refutation_criteria": self.refutation_criteria,
            "evidence": self.evidence,
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


class ClaimRegistry:
    def __init__(self, storage_file: str = "claims.json"):
        self.storage_file = storage_file
        self.claims: Dict[str, Claim] = {}
        self.load()

    def load(self):
        try:
            with open(self.storage_file, "r") as f:
                data = json.load(f)
                for k, v in data.items():
                    self.claims[k] = Claim(**v)
        except FileNotFoundError:
            self.claims = {}

    def save(self):
        with open(self.storage_file, "w") as f:
            json.dump({k: v.to_dict() for k, v in self.claims.items()}, f, indent=2)

    def add(self, claim: Claim):
        self.claims[claim.id] = claim
        self.save()

    def get(self, claim_id: str) -> Optional[Claim]:
        return self.claims.get(claim_id)

    def update(self, claim_id: str, **kwargs):
        if claim_id in self.claims:
            for key, val in kwargs.items():
                if hasattr(self.claims[claim_id], key):
                    setattr(self.claims[claim_id], key, val)
            self.claims[claim_id].updated_at = time.time()
            self.save()

    def active_claims(self) -> List[Claim]:
        return [c for c in self.claims.values() if c.status == "active"]

    def standing_hypotheses(self) -> List[Claim]:
        return [c for c in self.claims.values() if c.status == "standing"]


# ----------------------------------------------------------
# 2. Instrumentation Audit
# ----------------------------------------------------------
class InstrumentationAudit:
    """
    Measures the system's own variables.
    Domain‑specific implementations can override.
    """

    def __init__(self, system_state: Dict):
        self.state = system_state

    def measure_anchoring(self) -> float:
        """Measure A — anchoring strength."""
        # Domain‑specific measurement
        return self.state.get("anchoring", 0.5)

    def measure_damping(self) -> float:
        """Measure γ — damping coefficient."""
        return self.state.get("damping", 0.5)

    def measure_drive(self) -> float:
        """Measure ω — drive frequency."""
        return self.state.get("drive", 0.5)

    def measure_coherens(self) -> float:
        A = self.measure_anchoring()
        gamma = self.measure_damping()
        omega = self.measure_drive()
        if omega == 0:
            return float('inf')
        return (A * gamma) / omega

    def audit(self) -> Dict:
        return {
            "anchoring": self.measure_anchoring(),
            "damping": self.measure_damping(),
            "drive": self.measure_drive(),
            "coherens": self.measure_coherens(),
        }


# ----------------------------------------------------------
# 3. Scope Diagnostics
# ----------------------------------------------------------
class ScopeDiagnostic:
    """
    Determines where a claim applies.
    """

    def __init__(self, system_description: Dict):
        self.system = system_description

    def domain(self) -> str:
        return self.system.get("domain", "unknown")

    def scale(self) -> str:
        return self.system.get("scale", "unknown")

    def regime(self) -> str:
        return self.system.get("regime", "unknown")

    def scope_report(self) -> Dict:
        return {
            "domain": self.domain(),
            "scale": self.scale(),
            "regime": self.regime(),
        }


# ----------------------------------------------------------
# 4. Unknown Detector
# ----------------------------------------------------------
class UnknownDetector:
    """
    Flags gaps, inconsistencies, or unmeasured variables.
    """

    def __init__(self, claim: Claim, instrument_data: Dict, scope_data: Dict):
        self.claim = claim
        self.instruments = instrument_data
        self.scope = scope_data

    def detect(self) -> List[str]:
        unknowns = []
        # Check if variables are missing
        if "anchoring" not in self.instruments:
            unknowns.append("Anchoring (A) not measured")
        if "damping" not in self.instruments:
            unknowns.append("Damping (γ) not measured")
        if "drive" not in self.instruments:
            unknowns.append("Drive (ω) not measured")
        # Check for domain mismatch
        if self.scope["domain"] != self.claim.domain:
            unknowns.append(f"Claim domain ({self.claim.domain}) vs system domain ({self.scope['domain']}) mismatch")
        # Check for missing refutation criteria
        if not self.claim.refutation_criteria:
            unknowns.append("Refutation criteria not specified")
        return unknowns


# ----------------------------------------------------------
# 5. Experiment Scheduler
# ----------------------------------------------------------
class ExperimentScheduler:
    """
    Runs experiments and records outcomes.
    """

    def __init__(self, claim: Claim, instruments: Dict):
        self.claim = claim
        self.instruments = instruments
        self.results = []

    def run(self, experiment_config: Dict) -> Dict:
        """
        Run a single experiment.
        """
        # Simulate an experiment
        # In practice, this would call a simulation or data analysis
        C = self.instruments.get("coherens", 0.5)
        predicted_risk = 1.0 / (1.0 + math.exp(-2.0 * (C - 1.0)))
        outcome = "survived" if predicted_risk < 0.5 else "collapsed"
        result = {
            "experiment": experiment_config.get("name", "unnamed"),
            "predicted_risk": predicted_risk,
            "outcome": outcome,
            "coherens": C,
            "timestamp": time.time(),
        }
        self.results.append(result)
        return result


# ----------------------------------------------------------
# 6. Claim Updater
# ----------------------------------------------------------
class ClaimUpdater:
    """
    Revises claims based on experiment outcomes.
    """

    def __init__(self, registry: ClaimRegistry):
        self.registry = registry

    def update(self, claim_id: str, results: List[Dict]) -> str:
        claim = self.registry.get(claim_id)
        if not claim:
            return "Claim not found"

        # Analyze results
        successes = [r for r in results if r["outcome"] == "survived"]
        failures = [r for r in results if r["outcome"] != "survived"]

        if not results:
            new_status = "active"
        elif failures and successes:
            new_status = "revised"
            # In practice, we'd update the claim statement here
        elif failures and not successes:
            new_status = "refuted"
        else:
            new_status = "standing"

        self.registry.update(claim_id, status=new_status)
        return new_status


# ----------------------------------------------------------
# 7. The Laboratory — Main Loop
# ----------------------------------------------------------
class Laboratory:
    def __init__(self, registry: ClaimRegistry, system_state: Dict):
        self.registry = registry
        self.system_state = system_state
        self.instruments = InstrumentationAudit(system_state)
        self.scope = ScopeDiagnostic(system_state)

    def run_loop(self, claim_id: str, experiment_config: Dict) -> Dict:
        """
        Full refutation loop for a single claim.
        """
        # 1. Select claim
        claim = self.registry.get(claim_id)
        if not claim:
            return {"error": "Claim not found"}

        # 2. Instrument
        instrument_data = self.instruments.audit()

        # 3. Scope diagnostic
        scope_data = self.scope.scope_report()

        # 4. Unknown detector
        unknowns = UnknownDetector(claim, instrument_data, scope_data).detect()
        if unknowns:
            return {"error": "Unknowns detected", "unknowns": unknowns}

        # 5. Design experiment
        scheduler = ExperimentScheduler(claim, instrument_data)

        # 6. Run experiment
        result = scheduler.run(experiment_config)

        # 7. Update claim
        updater = ClaimUpdater(self.registry)
        new_status = updater.update(claim_id, scheduler.results)

        # 8. Return status
        return {
            "claim_id": claim_id,
            "status": new_status,
            "coherens": instrument_data["coherens"],
            "experiment_result": result,
            "standing_hypothesis": claim.statement if new_status == "standing" else None,
        }

    def find_standing_hypotheses(self) -> List[Claim]:
        return self.registry.standing_hypotheses()


# ----------------------------------------------------------
# 8. Demo
# ----------------------------------------------------------
def main():
    print("\n" + "=" * 70)
    print("THE LABORATORY — A Self‑Correcting AI Inquiry Space")
    print("=" * 70)

    # Initialize
    registry = ClaimRegistry()
    system_state = {
        "anchoring": 0.8,
        "damping": 0.7,
        "drive": 0.2,
        "domain": "ai_model_collapse",
        "scale": "generation",
        "regime": "recursive_training",
    }

    lab = Laboratory(registry, system_state)

    # Add a test claim
    claim = Claim(
        id="C001",
        statement="C = (A * gamma) / omega predicts collapse risk continuously",
        domain="ai_model_collapse",
        refutation_criteria="If C > 1.0 but collapse occurs, refute.",
    )
    registry.add(claim)

    # Run the loop
    result = lab.run_loop("C001", {"name": "recursive_training_simulation"})
    print("\nResult:")
    for key, val in result.items():
        print(f"  {key}: {val}")

    # Show standing hypotheses
    standing = lab.find_standing_hypotheses()
    print(f"\nStanding Hypotheses: {len(standing)}")
    for h in standing:
        print(f"  - {h.statement}")

    print("\n" + "=" * 70)
    print("DESIGN PRINCIPLE:")
    print("  • Claims are provisional, not final.")
    print("  • Refutation is a loop, not a verdict.")
    print("  • Standing hypotheses are the best current models.")
    print("  • Unknowns are flagged, not ignored.")
    print("=" * 70)


if __name__ == "__main__":
    main()
