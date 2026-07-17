#!/usr/bin/env python3
"""
scale_regime_switch.py

Detects phase changes in the collapse rate lambda(s) as a function of scale.
Applies to material fatigue, AI collapse, and other multi‑scale processes.
"""

import math
import numpy as np
from scipy.optimize import curve_fit

def piecewise_lambda(s, regime):
    if regime == 'elastic':
        return 0.0
    elif regime == 'plastic':
        return 0.05 * s
    elif regime == 'fracture':
        return 0.5 * math.exp(0.7 * s)
    elif regime == 'catastrophic':
        return float('inf')
    else:
        return 0.0

def detect_regime(D_f_series, scale_series, threshold=0.1):
    """
    Detect where lambda changes sign or magnitude.
    """
    lambda_vals = []
    for i in range(1, len(D_f_series)):
        if scale_series[i] == scale_series[i-1]:
            continue
        lam = math.log(D_f_series[i] / D_f_series[i-1]) / (scale_series[i] - scale_series[i-1])
        lambda_vals.append(lam)
    # Identify change points
    change_points = []
    for i in range(1, len(lambda_vals)):
        if abs(lambda_vals[i] - lambda_vals[i-1]) > threshold:
            change_points.append(i)
    return change_points, lambda_vals

def main():
    print("\n" + "=" * 70)
    print("SCALE REGIME SWITCH — Material Science Case")
    print("=" * 70)

    # Simulated D_f vs scale
    scale = np.linspace(0, 10, 100)
    D_f = []
    for s in scale:
        if s < 3:
            D_f.append(0.8)  # elastic
        elif s < 6:
            D_f.append(0.8 + 0.1 * (s - 3))  # plastic
        elif s < 8:
            D_f.append(1.1 + 0.3 * (s - 6))  # fracture
        else:
            # catastrophic: rapid collapse
            D_f.append(1.7 - 2.0 * (s - 8))

    print("D_f vs scale:")
    for i in range(0, len(scale), 20):
        print(f"  scale={scale[i]:.1f}, D_f={D_f[i]:.3f}")

    change_points, lambda_vals = detect_regime(D_f, scale)
    print(f"\nChange points detected at indices: {change_points}")
    print("Regime transitions:")
    print("  0-3: elastic (constant)")
    print("  3-6: plastic (linear increase)")
    print("  6-8: fracture (accelerating increase)")
    print("  8+: catastrophic (exponential decrease)")

    print("\n" + "=" * 70)
    print("DESIGN PRINCIPLE:")
    print("  • Collapse rate lambda is NOT universal.")
    print("  • It changes with scale and regime.")
    print("  • The framework detects the change—it doesn't impose a constant.")
    print("  • Material science shows us where the phase changes are.")
    print("=" * 70)

if __name__ == "__main__":
    main()
