#!/usr/bin/env python3
"""
inference_entropy.py

C9: Synthetic-data feedback lowers effective redeemability by 0.15 per 2×
generation depth, independent of grid uptime. Models the depreciation of a
compute token due to recursive self-consumption (Shumailov et al., Nature 2024).
"""

import math

# Base redeemability from redemption_entropy.py (compute = 0.81)
BASE_REDEEM = 0.81

# Entropy decay per doubling of generation depth
DECAY_PER_DOUBLING = 0.15

def effective_redeemability(generations):
    """
    generations: number of recursive generation steps (0 = human-trained)
    Returns effective redeemability after synthetic feedback.
    """
    if generations <= 0:
        return BASE_REDEEM
    # Decay scales with log2(generations+1) to avoid singularity
    depth_factor = math.log2(generations + 1)
    decay = DECAY_PER_DOUBLING * depth_factor
    return max(0.0, BASE_REDEEM - decay)

def hallucination_entropy(generations):
    """
    Returns a dimensionless entropy measure (0..1). 0 = no hallucination,
    1 = total collapse. Scales as (1 - effective_redeemability).
    """
    return 1.0 - effective_redeemability(generations)

def main():
    print("=" * 60)
    print("INFERENCE ENTROPY — C9")
    print("=" * 60)
    print(f"Base redeemability (compute): {BASE_REDEEM:.3f}")
    print(f"Decay per 2× generation depth: {DECAY_PER_DOUBLING:.2f}")
    print("-" * 60)
    print(f"{'Generations':>12} | {'Redeemability':>14} | {'Entropy':>10} | {'Status'}")
    print("-" * 60)

    for gen in [0, 1, 2, 3, 4, 5, 8, 10, 15, 20]:
        r = effective_redeemability(gen)
        h = hallucination_entropy(gen)
        if r < 0.5:
            status = "⚠️ COLLAPSE ZONE"
        elif r < 0.7:
            status = "DEGRADED"
        else:
            status = "INTACT"
        print(f"{gen:>12} | {r:>14.3f} | {h:>10.3f} | {status}")

    print("-" * 60)
    print("REFUTATION:")
    print("  If a frontier model at generation 5 has redeemability > 0.65,")
    print("  C9 is falsified. Measure from real inference logs.")
    print("=" * 60)

if __name__ == "__main__":
    main()
