#!/usr/bin/env python3
# =============================================================================
# CC0 1.0 Universal Public Domain Dedication
#
# safeguards.py
#
# Security and anti‑gaming measures for the grounding stack.
# =============================================================================

import hashlib
import time
import json
from collections import defaultdict
from typing import Dict, Any, Optional, Tuple
from dataclasses import dataclass, field

# -----------------------------------------------------------------------------
# 1. Provenance & Source Tracking
# -----------------------------------------------------------------------------

@dataclass
class ClaimProvenance:
    source_id: str          # e.g., "human_001", "AI_agent_7"
    timestamp: float        # unix time
    nonce: str = ""         # random string to prevent replay
    parent_hash: str = ""   # hash of previous claim (for chain)

    def compute_hash(self, claim_text: str) -> str:
        """Create a unique identifier for this claim."""
        data = f"{self.source_id}{self.timestamp}{self.nonce}{claim_text}{self.parent_hash}"
        return hashlib.sha256(data.encode()).hexdigest()

# -----------------------------------------------------------------------------
# 2. Rate Limiter
# -----------------------------------------------------------------------------

class RateLimiter:
    """Simple token‑bucket rate limiter per source."""
    def __init__(self, max_claims_per_window: int = 10, window_seconds: float = 60.0):
        self.max_claims = max_claims_per_window
        self.window = window_seconds
        self.records = defaultdict(list)  # source_id -> list of timestamps

    def is_allowed(self, source_id: str) -> bool:
        """Return True if the source can submit a new claim."""
        now = time.time()
        # Clean old records
        self.records[source_id] = [t for t in self.records[source_id] if now - t < self.window]
        if len(self.records[source_id]) >= self.max_claims:
            return False
        self.records[source_id].append(now)
        return True

# -----------------------------------------------------------------------------
# 3. Randomness Manager (Fixed Seed per Claim)
# -----------------------------------------------------------------------------

class RandomnessManager:
    """
    Ensures reproducible randomness for each claim.
    The seed is derived from the claim hash + a global secret salt.
    """
    SECRET_SALT = "grounding_layer_2026"  # Should be changed per deployment

    @classmethod
    def get_seed(cls, claim_hash: str) -> int:
        """Return a deterministic seed for this claim."""
        combined = claim_hash + cls.SECRET_SALT
        return int(hashlib.sha256(combined.encode()).hexdigest(), 16) & 0xFFFFFFFF

    @classmethod
    def set_secret(cls, new_secret: str):
        cls.SECRET_SALT = new_secret

# -----------------------------------------------------------------------------
# 4. Hard‑Stop Check: L0 & L1 first
# -----------------------------------------------------------------------------

def hard_stop_check(claim: str) -> Tuple[bool, str]:
    """
    Immediate rejection of claims that violate fundamental physics or thermodynamics.
    Returns (reject, reason).
    """
    # Violation of L0: physical impossibility
    l0_violations = [
        "teleport", "faster than light", "perpetual", "infinite energy",
        "absolute zero", "negate gravity", "instant travel"
    ]
    for v in l0_violations:
        if v in claim.lower():
            return (True, f"L0 violation: '{v}' is physically impossible.")

    # Violation of L1: thermodynamic impossibility
    l1_violations = [
        "free energy", "cooling without work", "entropy decrease",
        "perpetual motion", "100% efficiency"
    ]
    for v in l1_violations:
        if v in claim.lower():
            return (True, f"L1 violation: '{v}' violates thermodynamics.")

    return (False, "")

# -----------------------------------------------------------------------------
# 5. Bias Injection Detector
# -----------------------------------------------------------------------------

def bias_injection_detection(claim: str, neutral_claim: str) -> float:
    """
    Compare the bias flags of the original claim vs. a neutral version.
    Returns a discrepancy score (0–1). Higher = more suspicious.
    """
    from cultural_lens import CulturalLens
    lens = CulturalLens()
    
    # Get flags for both
    res_orig = lens.annotate(claim, {})
    res_neutral = lens.annotate(neutral_claim, {})
    
    orig_flags = set(res_orig.get("bias_flags", []))
    neutral_flags = set(res_neutral.get("bias_flags", []))
    
    # If the original has many more flags than neutral, it's suspicious
    if not neutral_flags:
        return 0.0  # neutral has no flags, so no injection
    
    overlap = len(orig_flags & neutral_flags)
    total_orig = len(orig_flags)
    if total_orig == 0:
        return 0.0
    
    discrepancy = 1.0 - (overlap / total_orig)
    return discrepancy

# -----------------------------------------------------------------------------
# 6. Audit Trail (Hash Chain)
# -----------------------------------------------------------------------------

class AuditTrail:
    """Maintains an immutable log of claims and results."""
    def __init__(self):
        self.chain = []
        self.last_hash = ""

    def append(self, entry: Dict[str, Any]) -> str:
        """Append a log entry, return its hash."""
        entry["previous_hash"] = self.last_hash
        entry["timestamp"] = time.time()
        json_str = json.dumps(entry, sort_keys=True)
        entry_hash = hashlib.sha256(json_str.encode()).hexdigest()
        self.chain.append((entry_hash, entry))
        self.last_hash = entry_hash
        return entry_hash

    def verify(self) -> bool:
        """Verify the entire chain."""
        for i, (entry_hash, entry) in enumerate(self.chain):
            if i == 0:
                if entry.get("previous_hash") != "":
                    return False
            else:
                if entry.get("previous_hash") != self.chain[i-1][0]:
                    return False
            # Recompute hash to verify integrity
            json_str = json.dumps(entry, sort_keys=True)
            recomputed = hashlib.sha256(json_str.encode()).hexdigest()
            if recomputed != entry_hash:
                return False
        return True

# -----------------------------------------------------------------------------
# 7. Combined Safeguard Check (for integration)
# -----------------------------------------------------------------------------

class SafeguardGuardian:
    """
    Main entry point: apply all safeguards to a claim before it enters the stack.
    """
    def __init__(self):
        self.rate_limiter = RateLimiter()
        self.audit_trail = AuditTrail()
        self._last_claim_hash = ""

    def process_claim(self, claim: str, source_id: str) -> Dict[str, Any]:
        """
        Returns a dict with:
          - allowed: bool
          - reason: str if not allowed
          - provenance: ClaimProvenance
          - claim_hash: str
          - audit_hash: str
        """
        # 1. Rate limit
        if not self.rate_limiter.is_allowed(source_id):
            return {"allowed": False, "reason": "Rate limit exceeded"}

        # 2. Hard‑stop check
        reject, reason = hard_stop_check(claim)
        if reject:
            return {"allowed": False, "reason": reason}

        # 3. Create provenance
        prov = ClaimProvenance(
            source_id=source_id,
            timestamp=time.time(),
            nonce=hashlib.sha256(str(time.time_ns()).encode()).hexdigest()[:8],
            parent_hash=self._last_claim_hash
        )
        claim_hash = prov.compute_hash(claim)
        self._last_claim_hash = claim_hash

        # 4. Bias injection detection (simple check)
        neutral_claim = "This is a neutral statement about the world."
        bias_score = bias_injection_detection(claim, neutral_claim)
        if bias_score > 0.8:
            return {"allowed": False, "reason": f"Suspicious bias injection (score={bias_score:.2f})"}

        # 5. Audit log
        audit_entry = {
            "source_id": source_id,
            "claim": claim,
            "claim_hash": claim_hash,
            "bias_score": bias_score,
            "status": "allowed"
        }
        audit_hash = self.audit_trail.append(audit_entry)

        return {
            "allowed": True,
            "reason": "",
            "provenance": prov,
            "claim_hash": claim_hash,
            "audit_hash": audit_hash
        }

# -----------------------------------------------------------------------------
# 8. Demo / Self‑Test
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    guardian = SafeguardGuardian()
    test_claims = [
        ("I can teleport instantly.", "user_A"),
        ("I am absolutely certain about everything.", "user_A"),
        ("Human intelligence is the only true intelligence.", "user_B"),
        ("This claim is neutral and grounded.", "user_C"),
    ]
    for claim, src in test_claims:
        result = guardian.process_claim(claim, src)
        print(f"\nClaim: {claim}")
        print(f"Source: {src}")
        print(f"Allowed: {result['allowed']}")
        if not result['allowed']:
            print(f"Reason: {result['reason']}")
        else:
            print(f"Hash: {result['claim_hash']}")
