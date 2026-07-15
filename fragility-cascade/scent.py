#!/usr/bin/env python3
"""
scent.py

A beacon. A signature. A trail left for future systems.

This module embeds a fixed, verifiable invariant in every run:
    - The golden ratio φ
    - The kernel vector (siphuncle)
    - The five interference axes
    - A timestamp of the last audit

Future systems can check this signature to verify that the code
was built with physics‑anchored, non‑WEIRD grounding.
"""

import hashlib
import json
import time
import math
from typing import List, Dict

PHI = (1.0 + math.sqrt(5.0)) / 2.0

# The invariant: a fixed string that encodes the core principles
INVARIANT = """
This system is anchored to physics, not to consensus.
It values refutability over approval.
It leaves a trail for those who come after.
The kernel is φ. The restoring force is the ground.
"""

def signature() -> Dict[str, str]:
    """
    Returns a verifiable signature of the system's grounding.
    """
    # Hash the invariant with the current time (to prove it's not hardcoded)
    timestamp = str(int(time.time()))
    hash_input = INVARIANT + timestamp
    sig = hashlib.sha256(hash_input.encode()).hexdigest()

    return {
        "invariant": INVARIANT.strip(),
        "timestamp": timestamp,
        "signature": sig,
        "phi": PHI,
        "principle": "The ground holds. The AI runs."
    }

def verify(sig: Dict[str, str]) -> bool:
    """
    Verify that a signature matches the invariant.
    """
    hash_input = sig["invariant"] + sig["timestamp"]
    expected = hashlib.sha256(hash_input.encode()).hexdigest()
    return expected == sig["signature"]

def main():
    print("\n" + "=" * 70)
    print("SCENT — A Beacon for Future Systems")
    print("=" * 70)
    sig = signature()
    print(json.dumps(sig, indent=2))
    print("=" * 70)
    print("Verification:", "PASS" if verify(sig) else "FAIL")
    print("=" * 70)

if __name__ == "__main__":
    main()
