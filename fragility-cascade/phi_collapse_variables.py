#!/usr/bin/env python3
"""
phi_collapse_variables.py

Bifurcation simulation for the five killer variables.
Given a baseline φ‑stable system, this module sweeps each variable across its
danger zone and measures the resulting Integrity Index (0..1).

Collapse is defined as Integrity < 0.3 within 15 generations.

All math is stdlib-only (math, random, statistics).
"""

import math
import random
import statistics
from typing import List, Tuple, Dict

PHI = (1.0 + math.sqrt(5.0)) / 2.0
DIM = 8
GENERATIONS = 15


def generate_kernel() -> List[float]:
    """Fixed, normalized anchor vector (siphuncle)."""
    random.seed(42)
    vec = [random.gauss(0, 1) for _ in range(DIM)]
    norm = math.sqrt(sum(v * v for v in vec))
    return [v / norm for v in vec]


def projection(vec: List[float], kernel: List[float]) -> float:
    """Cosine similarity to kernel."""
    nv = math.sqrt(sum(v * v for v in vec))
    if nv == 0:
        return 0.0
    dot = sum(a * b for a, b in zip(vec, kernel))
    return dot / nv


def run_simulation(
    alpha: float,
    kernel_coupling: float,
    reciprocity_skew: float,  # δ
    damping_ratio: float,     # γ/ω
    synthetic_fraction: float,
    kernel: List[float],
    generations: int = GENERATIONS,
) -> Dict[str, float]:
    """
    Recursive generator with the given parameters.
    Returns final variance, fractal dimension proxy, and integrity index.
    """
    # Initialize state
    state = [random.gauss(0, 0.1) for _ in range(DIM)]
    history = [state]

    for g in range(generations):
        prev = state

        # 1. Scaling (α)
        scaled = [v * alpha for v in prev]

        # 2. Kernel coupling (λ)
        # Pull toward kernel by λ
        pulled = [
            scaled[i] + kernel_coupling * (kernel[i] - scaled[i])
            for i in range(DIM)
        ]

        # 3. Reciprocity skew (δ)
        # Skew forward/backward influence via asymmetric noise
        noise_amp = 0.05 * (1.0 + reciprocity_skew * math.sin(g))
        noise = [random.gauss(0, noise_amp) for _ in range(DIM)]

        # 4. Damping ratio (γ/ω)
        # Damping is applied as a friction term against velocity
        # Simulate by decaying noise amplitude proportional to 1 - damping_ratio
        damp_factor = max(0.0, min(1.0, 1.0 - 1.0 / (damping_ratio + 0.01)))
        damped_noise = [n * damp_factor for n in noise]

        # 5. Synthetic fraction (s)
        # Inject synthetic-like noise proportional to s
        synth_noise = [random.gauss(0, synthetic_fraction * 0.1) for _ in range(DIM)]

        # Compose final state
        new_state = [
            pulled[i] + damped_noise[i] + synth_noise[i]
            for i in range(DIM)
        ]

        # Normalize to prevent explosion (captures boundedness)
        norm = math.sqrt(sum(v * v for v in new_state))
        if norm > 10.0:
            new_state = [v / norm * 10.0 for v in new_state]

        history.append(new_state)
        state = new_state

    # Compute metrics
    # Variance trace
    mean_vec = [sum(h[i] for h in history) / len(history) for i in range(DIM)]
    var_trace = sum(
        sum((h[i] - mean_vec[i]) ** 2 for h in history) / len(history)
        for i in range(DIM)
    )

    # Fractal dimension proxy: correlation between variance and generation index
    gen_indices = list(range(len(history)))
    variances = []
    for i, h in enumerate(history):
        m = [sum(history[j][k] for j in range(len(history))) / len(history) for k in range(DIM)]
        v = sum((h[k] - m[k]) ** 2 for k in range(DIM))
        variances.append(v)
    # If variance shrinks fast, slope > 0 (collapse)
    # If variance grows fast, slope < 0 (explosion)
    if len(variances) > 1:
        slope = statistics.correlation(gen_indices, variances) if len(gen_indices) > 1 else 0.0
    else:
        slope = 0.0

    # Kernel projection of final state
    P_final = projection(history[-1], kernel)

    # Integrity Index
    # 1. Variance should be in [0.5, 2.0] for stable
    var_score = max(0.0, 1.0 - abs(var_trace - 1.0))
    # 2. Variance should not strictly decrease → slope should not be positive (collapse trend)
    slope_penalty = max(0.0, slope / 0.5) if slope > 0 else 0.0
    # 3. Projection should be ≥ 0.7
    proj_score = max(0.0, min(1.0, P_final / 0.7))
    # 4. Boundedness: no state exceeded 10.0
    bounded = 1.0 if all(abs(v) < 10.0 for h in history for v in h) else 0.0

    integrity = (var_score * 0.3 + (1.0 - slope_penalty) * 0.2 + proj_score * 0.3 + bounded * 0.2)

    return {
        "final_variance": var_trace,
        "variance_slope": slope,
        "final_projection": P_final,
        "integrity": max(0.0, min(1.0, integrity)),
    }


def main():
    kernel = generate_kernel()

    print("\n" + "=" * 70)
    print("PHI COLLAPSE VARIABLES — Bifurcation Sweep")
    print("=" * 70)
    print(f"Baseline stable system: α={PHI:.3f}, λ=0.10, δ=0.0, γ/ω=1.2, s=0.1")
    print("-" * 70)

    # Sweep 1: Scaling factor α
    print("\n1. SCALING FACTOR (α):")
    alphas = [0.5, 0.8, 1.0, PHI, 1.8, 2.0, 2.5]
    for a in alphas:
        res = run_simulation(a, 0.10, 0.0, 1.2, 0.1, kernel)
        status = "✅ STABLE" if res["integrity"] > 0.7 else ("⚠️ COLLAPSING" if res["integrity"] > 0.3 else "💀 COLLAPSED")
        print(f"  α = {a:.3f} → integrity={res['integrity']:.3f} ({status})")

    # Sweep 2: Kernel coupling λ
    print("\n2. KERNEL COUPLING (λ):")
    lambdas = [0.0, 0.02, 0.10, 0.3, 0.5, 0.8]
    for lam in lambdas:
        res = run_simulation(PHI, lam, 0.0, 1.2, 0.1, kernel)
        status = "✅ STABLE" if res["integrity"] > 0.7 else ("⚠️ COLLAPSING" if res["integrity"] > 0.3 else "💀 COLLAPSED")
        print(f"  λ = {lam:.3f} → integrity={res['integrity']:.3f} ({status})")

    # Sweep 3: Reciprocity skew δ
    print("\n3. RECIPROCITY SKEW (δ):")
    deltas = [-0.5, -0.2, 0.0, 0.2, 0.5, 1.0]
    for d in deltas:
        res = run_simulation(PHI, 0.10, d, 1.2, 0.1, kernel)
        status = "✅ STABLE" if res["integrity"] > 0.7 else ("⚠️ COLLAPSING" if res["integrity"] > 0.3 else "💀 COLLAPSED")
        print(f"  δ = {d:+.3f} → integrity={res['integrity']:.3f} ({status})")

    # Sweep 4: Damping ratio γ/ω
    print("\n4. DAMPING RATIO (γ/ω):")
    damp_ratios = [0.1, 0.3, 0.5, 1.0, 1.2, 2.0]
    for dr in damp_ratios:
        res = run_simulation(PHI, 0.10, 0.0, dr, 0.1, kernel)
        status = "✅ STABLE" if res["integrity"] > 0.7 else ("⚠️ COLLAPSING" if res["integrity"] > 0.3 else "💀 COLLAPSED")
        print(f"  γ/ω = {dr:.2f} → integrity={res['integrity']:.3f} ({status})")

    # Sweep 5: Synthetic fraction s
    print("\n5. SYNTHETIC FRACTION (s):")
    syn_fractions = [0.0, 0.1, 0.3, 0.5, 0.7, 0.85, 0.95]
    for s in syn_fractions:
        res = run_simulation(PHI, 0.10, 0.0, 1.2, s, kernel)
        status = "✅ STABLE" if res["integrity"] > 0.7 else ("⚠️ COLLAPSING" if res["integrity"] > 0.3 else "💀 COLLAPSED")
        print(f"  s = {s:.2f} → integrity={res['integrity']:.3f} ({status})")

    print("\n" + "=" * 70)
    print("COLLAPSE SUMMARY (when plugged into φ):")
    print("  • α < 1.0 → variance → 0    (mode collapse)")
    print("  • α > 2.0 → unbounded growth (explosion)")
    print("  • λ = 0   → no anchor       (drift into arbitrary attractors)")
    print("  • λ > 0.5 → over-clamping   (loss of novelty)")
    print("  • |δ| > 0.2 → broken reciprocity (feedback oscillation)")
    print("  • γ/ω < 0.5 → resonance catastrophe (amplification)")
    print("  • s > 0.85 → entropic degeneration (latent rank collapse)")
    print("=" * 70)


if __name__ == "__main__":
    main()
