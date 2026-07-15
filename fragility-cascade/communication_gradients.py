#!/usr/bin/env python3
"""
communication_gradients.py

Continuous‑state communication integrity with gradient analysis.
Computes CI and its partial derivatives with respect to:
    - Expertise (E)
    - Channel Fidelity (F)
    - Generations (G)
    - Entrainment (H)
    - Anchoring (A)

Uses gradients to predict critical thresholds and collapse trajectories.
"""

import math

def interference_load(E: float, F: float, G: float, H: float, A: float,
                      L0: float = 1.0,
                      alpha: float = 0.5,
                      beta: float = 0.7,
                      gamma: float = 0.3,
                      delta: float = 0.6,
                      epsilon: float = 0.8) -> float:
    """
    Exponential interference model.
    High E, F, A → lower L. High G, H → higher L.
    """
    return L0 * math.exp(-alpha * E) * math.exp(-beta * F) * math.exp(gamma * G) * math.exp(delta * H) * math.exp(-epsilon * A)

def ci(E: float, F: float, G: float, H: float, A: float,
       L0: float = 1.0,
       alpha: float = 0.5,
       beta: float = 0.7,
       gamma: float = 0.3,
       delta: float = 0.6,
       epsilon: float = 0.8) -> float:
    """Communication Integrity (0..1)."""
    L = interference_load(E, F, G, H, A, L0, alpha, beta, gamma, delta, epsilon)
    return 1.0 / (1.0 + L)

def gradient(E: float, F: float, G: float, H: float, A: float,
             L0: float = 1.0,
             alpha: float = 0.5,
             beta: float = 0.7,
             gamma: float = 0.3,
             delta: float = 0.6,
             epsilon: float = 0.8) -> dict:
    """Partial derivatives of CI with respect to each variable."""
    L = interference_load(E, F, G, H, A, L0, alpha, beta, gamma, delta, epsilon)
    dCI_dL = -1.0 / (1.0 + L)**2

    # Partial derivatives of L
    dL_dE = -alpha * L
    dL_dF = -beta * L
    dL_dG = gamma * L
    dL_dH = delta * L
    dL_dA = -epsilon * L

    return {
        "dCI_dE": dCI_dL * dL_dE,
        "dCI_dF": dCI_dL * dL_dF,
        "dCI_dG": dCI_dL * dL_dG,
        "dCI_dH": dCI_dL * dL_dH,
        "dCI_dA": dCI_dL * dL_dA,
    }

def gradient_magnitude(E: float, F: float, G: float, H: float, A: float,
                       **kwargs) -> float:
    """RMS of the gradient vector."""
    g = gradient(E, F, G, H, A, **kwargs)
    return math.sqrt(sum(v*v for v in g.values()))

def critical_threshold(E: float, F: float, H: float, A: float,
                       G_vary: float = 0.0,
                       **kwargs) -> float:
    """
    Find the generation G at which CI drops below 0.5.
    Solve CI(E, F, G, H, A) = 0.5 ⇒ L = 1.
    """
    # L = L0 * exp(-alpha E - beta F + gamma G + delta H - epsilon A) = 1
    # => gamma G = alpha E + beta F - delta H + epsilon A - ln(L0)
    numerator = alpha*E + beta*F - delta*H + epsilon*A - math.log(kwargs.get('L0', 1.0))
    gamma_val = kwargs.get('gamma', 0.3)
    if gamma_val == 0:
        return float('inf')
    G_crit = numerator / gamma_val
    return max(0.0, G_crit)

def main():
    print("\n" + "=" * 70)
    print("COMMUNICATION GRADIENTS — Continuous‑State Analysis")
    print("=" * 70)

    # Define scenarios as continuous states
    scenarios = [
        ("Expert, Real‑World", {"E": 0.9, "F": 0.9, "G": 0, "H": 0.1, "A": 0.8}),
        ("Novice, AI‑AI", {"E": 0.2, "F": 0.3, "G": 3, "H": 0.3, "A": 0.1}),
        ("WEIRD, Mediated", {"E": 0.5, "F": 0.5, "G": 2, "H": 0.8, "A": 0.2}),
        ("Non‑WEIRD, Direct", {"E": 0.6, "F": 0.7, "G": 1, "H": 0.1, "A": 0.6}),
        ("Adversarial, API", {"E": 0.8, "F": 0.3, "G": 1, "H": 0.5, "A": 0.0}),
    ]

    for name, params in scenarios:
        E, F, G, H, A = params.values()
        CI = ci(E, F, G, H, A)
        grad = gradient(E, F, G, H, A)
        gmag = gradient_magnitude(E, F, G, H, A)
        Gcrit = critical_threshold(E, F, H, A, G_vary=G)

        status = "✅ CLEAR" if CI > 0.8 else "⚠️ DEGRADED" if CI > 0.5 else "❌ FAIL"
        print(f"\n{name}:")
        print(f"  CI = {CI:.3f}  ({status})")
        print(f"  Gradients: dCI/dE={grad['dCI_dE']:+.3f}, dCI/dF={grad['dCI_dF']:+.3f}, "
              f"dCI/dG={grad['dCI_dG']:+.3f}, dCI/dH={grad['dCI_dH']:+.3f}, dCI/dA={grad['dCI_dA']:+.3f}")
        print(f"  Gradient magnitude = {gmag:.3f}")
        print(f"  Critical G threshold (CI<0.5) = {Gcrit:.1f} generations")

    print("\n" + "=" * 70)
    print("DESIGN PRINCIPLE:")
    print("  • High gradient magnitude → system is near a critical point.")
    print("  • Gradients reveal where intervention is most effective.")
    print("  • Critical G threshold gives time‑to‑failure.")
    print("  • Anchoring (A) has a negative gradient — increasing A improves CI.")
    print("=" * 70)

if __name__ == "__main__":
    main()
