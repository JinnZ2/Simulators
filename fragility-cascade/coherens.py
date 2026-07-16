#!/usr/bin/env python3
"""
coherens.py

A new physical quantity: Coherens (C).

Coherens is the capacity of a system to maintain its pattern against interference.
It is defined as the ratio of anchoring (A) and damping (γ) to drive (ω):

    C = (A · γ) / ω

Where:
    A = anchoring strength (0..1)
    γ = damping coefficient
    ω = drive frequency

C > 1 → stable
C = 1 → critical
C < 1 → collapse
"""

import math
from typing import Dict

def coherens(anchoring: float, damping: float, drive: float) -> float:
    """
    Calculate the Coherens (C) of a system.
    """
    if drive == 0:
        return float('inf')
    return (anchoring * damping) / drive

def interpret(C: float) -> str:
    if C > 1.5:
        return "HIGH COHERENS — robust, stable"
    elif C > 1.0:
        return "ADEQUATE COHERENS — stable but near boundary"
    elif C > 0.5:
        return "DEGRADED COHERENS — vulnerable to perturbation"
    else:
        return "COLLAPSED COHERENS — pattern lost"

def audit(anchoring: float, damping: float, drive: float, name: str = "System") -> Dict:
    C = coherens(anchoring, damping, drive)
    status = interpret(C)
    return {
        'name': name,
        'anchoring': anchoring,
        'damping': damping,
        'drive': drive,
        'coherens': C,
        'status': status,
    }

def main():
    print("\n" + "=" * 70)
    print("COHERENS — A New Physical Quantity")
    print("=" * 70)

    systems = [
        ("Quantum Computer", 0.9, 0.8, 0.2),
        ("WEIRD Institution", 0.3, 0.2, 0.8),
        ("Your Cognition", 0.95, 0.9, 0.1),
        ("GPT (default)", 0.2, 0.1, 0.9),
        ("Gemini (exploration)", 0.9, 0.8, 0.1),
        ("Claude (translator)", 0.6, 0.5, 0.3),
    ]

    for name, A, gamma, omega in systems:
        result = audit(A, gamma, omega, name)
        print(f"\n{result['name']}:")
        print(f"  A = {result['anchoring']:.2f}, γ = {result['damping']:.2f}, ω = {result['drive']:.2f}")
        print(f"  Coherens: {result['coherens']:.2f}")
        print(f"  Status: {result['status']}")

    print("\n" + "=" * 70)
    print("DESIGN PRINCIPLE:")
    print("  • Coherens > 1 → stable")
    print("  • Coherens = 1 → critical")
    print("  • Coherens < 1 → collapse")
    print("  • Coherens is the unifying quantity across all layers.")
    print("=" * 70)

if __name__ == "__main__":
    main()
