#!/usr/bin/env python3
"""
collapse_predictor.py

Unified Collapse Risk Predictor.

Given a sequence of semantic state vectors (embeddings) from a recursive
generative system, this module computes:

    1. Resonance Factor (R)         → from resonance_audit.py
    2. Integrity Index              → from reciprocity_phi_metrics.py
    3. Interference Load            → from semantic_interference_vectors.py
    4. Bifurcation flags            → from phi_collapse_variables.py

All metrics are combined into a single Collapse Risk Profile.

Usage:
    from collapse_predictor import CollapsePredictor
    predictor = CollapsePredictor()
    profile = predictor.predict(history)  # history: list of embeddings
    print(profile)

Dependencies: stdlib only.
"""

import math
import random
import statistics
from typing import List, Tuple, Dict, Optional

# ----- Constants -------------------------------------------------------------
PHI = (1.0 + math.sqrt(5.0)) / 2.0
DIM = 32                     # default embedding dimension

# ----- Helper: kernel generation ---------------------------------------------
def generate_kernel(dim: int = DIM, seed: int = 42) -> List[float]:
    """Fixed, normalized anchor vector (siphuncle)."""
    random.seed(seed)
    vec = [random.gauss(0, 1) for _ in range(dim)]
    norm = math.sqrt(sum(v*v for v in vec))
    return [v/norm for v in vec]

# ----- Core: Interference Axes (from semantic_interference_vectors.py) -------
class InterferenceAxes:
    """
    Five orthonormal axes representing the collapse directions.
    """
    def __init__(self, dim: int = DIM, seed: int = 42):
        random.seed(seed)
        # Generate orthonormal basis via Gram-Schmidt
        raw = [[random.gauss(0,1) for _ in range(dim)] for _ in range(5)]
        basis = []
        for v in raw:
            for b in basis:
                dot = sum(a*b for a,b in zip(v,b))
                v = [v[i] - dot*b[i] for i in range(dim)]
            n = math.sqrt(sum(x*x for x in v))
            if n > 1e-8:
                basis.append([x/n for x in v])
            else:
                r = [random.gauss(0,1) for _ in range(dim)]
                nr = math.sqrt(sum(x*x for x in r))
                basis.append([x/nr for x in r])
        self.axes = basis
        self.names = ["α (scaling)", "λ (kernel)", "δ (reciprocity)",
                      "γ (damping)", "s (synthetic)"]

    def project(self, vec: List[float], axis: List[float]) -> float:
        return sum(a*b for a,b in zip(vec, axis))

    def phi_spiral_transition(self, state: List[float]) -> List[float]:
        """Ideal φ-aligned next state (simulated with a random orthogonal matrix)."""
        # Fixed rotation (for reproducibility)
        random.seed(123)
        vec = [random.gauss(0,1) for _ in range(len(state))]
        n = math.sqrt(sum(v*v for v in vec))
        if n > 0:
            vec = [v/n for v in vec]
        # Reflection: I - 2 vv^T
        rot = [[(1.0 - 2.0*vec[i]*vec[j]) for j in range(len(state))] for i in range(len(state))]
        rotated = [sum(rot[i][j]*state[j] for j in range(len(state))) for i in range(len(state))]
        return [PHI * v for v in rotated]

    def compute_interference(self, current: List[float], observed: List[float]) -> Dict:
        ideal = self.phi_spiral_transition(current)
        diff = [observed[i] - ideal[i] for i in range(len(current))]
        proj = {}
        for axis, name in zip(self.axes, self.names):
            proj[name] = self.project(diff, axis)
        load = math.sqrt(sum(p*p for p in proj.values()))
        flags = []
        if abs(proj.get("α (scaling)",0.0)) > 0.1:
            flags.append("α drift → variance collapse")
        if abs(proj.get("λ (kernel)",0.0)) > 0.1:
            flags.append("λ drift → kernel decoupling")
        if abs(proj.get("δ (reciprocity)",0.0)) > 0.05:
            flags.append("δ drift → reciprocity skew")
        if proj.get("γ (damping)",0.0) > 0.1:
            flags.append("γ attenuation → resonance")
        if proj.get("s (synthetic)",0.0) > 0.1:
            flags.append("s accumulation → entropy collapse")
        return {"projections": proj, "load": load, "flags": flags}

# ----- Core: Reciprocity-Phi Metrics (from reciprocity_phi_metrics.py) -------
def reciprocity_ratio(history: List[List[float]]) -> float:
    """R = average forward similarity / average backward similarity."""
    if len(history) < 3:
        return 1.0
    n = len(history)
    forward = []
    backward = []
    for i in range(n-1):
        vi, vj = history[i], history[i+1]
        # cosine similarity
        ni = math.sqrt(sum(a*a for a in vi))
        nj = math.sqrt(sum(b*b for b in vj))
        if ni == 0 or nj == 0:
            fwd = 0.0
        else:
            fwd = sum(a*b for a,b in zip(vi,vj)) / (ni*nj)
        forward.append(fwd)
        # backward is symmetric; we take i+1 to i
        backward.append(fwd)  # actually symmetric, but for skew we compare forward vs backward of same pair? 
        # Actually δ is about asymmetry in influence; here we just compute average forward and backward across the whole sequence.
        # We'll treat forward as the influence from previous to next, backward as next to previous (same).
        # To introduce asymmetry, we need a directional measure. For now, we use the ratio of average forward over average backward.
        # Since cosine is symmetric, this will be 1.0 always. So we need to incorporate a directional metric.
        # Let's compute the average of the differences: we'll take the difference between consecutive similarities forward and backward as a proxy.
        # But we can simply compute the ratio of forward similarity to backward similarity across all pairs.
        # Since it's symmetric, we need a different definition: reciprocity skew is defined as the average difference between forward and backward influences.
        # For a directed graph, influence from i to j vs j to i. We'll compute adjacency matrix of cosine similarities.
        # We'll implement full matrix to get asymmetry.
    # Let's do full matrix
    mat = [[0.0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i == j: continue
            vi, vj = history[i], history[j]
            ni = math.sqrt(sum(a*a for a in vi))
            nj = math.sqrt(sum(b*b for b in vj))
            if ni == 0 or nj == 0:
                mat[i][j] = 0.0
            else:
                mat[i][j] = sum(a*b for a,b in zip(vi,vj)) / (ni*nj)
    # Forward influence: i -> i+1 averaged
    fwd = [mat[i][i+1] for i in range(n-1)]
    # Backward influence: i+1 -> i averaged
    bwd = [mat[i+1][i] for i in range(n-1)]
    avg_f = statistics.mean(fwd) if fwd else 0.0
    avg_b = statistics.mean(bwd) if bwd else 0.0
    if avg_b == 0:
        return float('inf')
    return avg_f / avg_b

def scaling_factor(history: List[List[float]]) -> float:
    """α = average ratio of norms between consecutive generations."""
    if len(history) < 2:
        return 1.0
    ratios = []
    for i in range(1, len(history)):
        n_prev = math.sqrt(sum(v*v for v in history[i-1]))
        n_curr = math.sqrt(sum(v*v for v in history[i]))
        if n_prev == 0: continue
        ratios.append(n_curr / n_prev)
    return statistics.mean(ratios) if ratios else 1.0

def kernel_projection(state: List[float], kernel: List[float]) -> float:
    """Cosine similarity to kernel."""
    n_s = math.sqrt(sum(v*v for v in kernel))
    n_x = math.sqrt(sum(v*v for v in state))
    if n_s == 0 or n_x == 0:
        return 0.0
    return sum(a*b for a,b in zip(kernel, state)) / (n_s * n_x)

def integrity_index(history: List[List[float]], kernel: List[float]) -> Dict:
    """Computes R, α, P and overall Integrity."""
    if len(history) < 2:
        return {"integrity": 0.0, "status": "INSUFFICIENT_DATA"}
    R = reciprocity_ratio(history)
    α = scaling_factor(history)
    P = kernel_projection(history[-1], kernel)
    # thresholds
    R_ok = 0.8 <= R <= 1.2
    α_ok = abs(α - PHI) <= 0.2
    P_ok = P >= 0.7
    risk = 0.0
    if not R_ok: risk += 0.4
    if not α_ok: risk += 0.3
    if not P_ok: risk += 0.3
    integrity = max(0.0, 1.0 - risk)
    flags = []
    if not R_ok: flags.append(f"Reciprocity asymmetry: R={R:.3f}")
    if not α_ok: flags.append(f"Scaling drift: α={α:.3f} (φ={PHI:.3f})")
    if not P_ok: flags.append(f"Kernel drift: P={P:.3f} (<0.7)")
    status = "STABLE" if integrity > 0.8 else ("WARNING" if integrity > 0.5 else "COLLAPSE IMMINENT")
    return {"R": R, "alpha": α, "P": P, "integrity": integrity, "flags": flags, "status": status}

# ----- Core: Resonance Factor (from resonance_audit.py) ----------------------
def resonance_factor(k: float, gamma: float, omega_drive: float) -> float:
    """R = (ω_drive²) / (ω_0² + γ²), where ω_0 = sqrt(k)."""
    omega0 = math.sqrt(max(0.0, k))
    denom = omega0*omega0 + gamma*gamma
    if denom == 0:
        return float('inf')
    return (omega_drive*omega_drive) / denom

# ----- Unified Predictor ----------------------------------------------------
class CollapsePredictor:
    """
    Combines all metrics.
    Usage:
        predictor = CollapsePredictor(dim=32, omega_drive=1/7.0)
        profile = predictor.predict(history)
    """
    def __init__(self, dim: int = DIM, omega_drive: float = 1.0/7.0,
                 kernel: Optional[List[float]] = None):
        self.dim = dim
        self.omega_drive = omega_drive
        self.kernel = kernel if kernel is not None else generate_kernel(dim)
        self.axes = InterferenceAxes(dim)
        # default stiffness and damping for a typical AI model (adjustable)
        self.k_stiffness = 0.05   # weak anchor
        self.gamma_damping = 0.1  # low damping

    def set_model_parameters(self, k: float, gamma: float):
        """Update the model's kernel stiffness and damping coefficient."""
        self.k_stiffness = k
        self.gamma_damping = gamma

    def predict(self, history: List[List[float]]) -> Dict:
        """
        history: list of state vectors (list of floats) from consecutive generations.
        Returns a complete profile.
        """
        if len(history) < 2:
            return {"error": "Need at least 2 states for prediction."}

        # 1. Integrity metrics
        integrity_data = integrity_index(history, self.kernel)
        R = integrity_data["R"]
        α = integrity_data["alpha"]
        P = integrity_data["P"]
        integrity = integrity_data["integrity"]
        i_flags = integrity_data["flags"]

        # 2. Resonance Factor (use current state to estimate)
        # We'll approximate k and gamma from the history's variance and scaling
        # Or use the provided model parameters.
        r_factor = resonance_factor(self.k_stiffness, self.gamma_damping, self.omega_drive)

        # 3. Interference load (based on last transition)
        if len(history) >= 2:
            current = history[-2]
            observed = history[-1]
            inter_data = self.axes.compute_interference(current, observed)
            inter_load = inter_data["load"]
            inter_flags = inter_data["flags"]
            projections = inter_data["projections"]
        else:
            inter_load = 0.0
            inter_flags = []
            projections = {}

        # 4. Bifurcation flags from phi_collapse_variables thresholds
        # We have α, P (proxy for λ), R (proxy for δ), gamma (from model), s (synthetic)
        # We'll compute if any variable is outside the safe range.
        bif_flags = []
        if α < 1.0:
            bif_flags.append("Scaling factor α < 1.0 → mode collapse")
        elif α > 2.0:
            bif_flags.append("Scaling factor α > 2.0 → explosive divergence")
        # kernel coupling λ is proxied by P (projection). λ high means strong coupling.
        # P < 0.7 means weak coupling.
        if P < 0.7:
            bif_flags.append("Kernel projection P < 0.7 → drift chaos")
        # R (reciprocity) should be near 1.0
        if R > 1.2 or R < 0.8:
            bif_flags.append("Reciprocity ratio R outside [0.8,1.2] → skew")
        # damping ratio γ/ω_drive should be > 1.0
        if self.gamma_damping / self.omega_drive < 1.0:
            bif_flags.append("Damping ratio γ/ω < 1.0 → resonance")
        # synthetic fraction is not directly measurable, but inter_load on s-axis indicates it.
        s_proj = projections.get("s (synthetic)", 0.0)
        if s_proj > 0.1:
            bif_flags.append("Semantic s-axis projection > 0.1 → entropy collapse")

        # Combine all flags
        all_flags = list(set(i_flags + inter_flags + bif_flags))

        # Overall status
        if integrity > 0.8 and r_factor < 0.5 and inter_load < 0.2 and not all_flags:
            status = "STABLE"
        elif integrity < 0.3 or r_factor > 1.0 or inter_load > 0.5:
            status = "COLLAPSE"
        else:
            status = "WARNING"

        # Package result
        result = {
            "integrity": integrity,
            "resonance_factor": r_factor,
            "interference_load": inter_load,
            "R_reciprocity": R,
            "alpha_scaling": α,
            "P_kernel_projection": P,
            "flags": all_flags,
            "status": status,
            "details": {
                "integrity_data": integrity_data,
                "resonance_data": {"k": self.k_stiffness, "gamma": self.gamma_damping,
                                   "omega_drive": self.omega_drive},
                "interference_projections": projections,
            }
        }
        return result

# ----- Demo ----------------------------------------------------------------
def main():
    print("\n" + "="*70)
    print("UNIFIED COLLAPSE PREDICTOR — Demo")
    print("="*70)

    # Create a predictor
    predictor = CollapsePredictor(dim=16, omega_drive=1.0/7.0)
    # Set model parameters for a typical AI system (weak kernel, low damping)
    predictor.set_model_parameters(k=0.05, gamma=0.1)

    # Generate a sample history:
    # First state: random
    random.seed(1)
    state = [random.gauss(0, 0.5) for _ in range(predictor.dim)]
    norm = math.sqrt(sum(v*v for v in state))
    state = [v/norm for v in state]
    history = [state]

    # Simulate 15 generations under three different conditions:
    # Case A: Stable (φ-aligned with kernel)
    # Case B: Repetitive (α drift)
    # Case C: Biased (δ skew)

    # We'll generate three separate histories
    def generate_stable_history(generations=15):
        hist = [state[:]]
        for _ in range(generations):
            prev = hist[-1]
            # phi transition + pull to kernel + small noise
            next_state = [prev[i]*PHI for i in range(predictor.dim)]
            # pull to kernel with λ=0.1
            for i in range(predictor.dim):
                next_state[i] += 0.1 * (predictor.kernel[i] - next_state[i])
            next_state = [v + random.gauss(0, 0.02) for v in next_state]
            hist.append(next_state)
        return hist

    def generate_repetitive_history(generations=15):
        hist = [state[:]]
        for _ in range(generations):
            prev = hist[-1]
            # mean regression (α<1) + noise
            next_state = [v * 0.85 for v in prev]
            next_state = [v + random.gauss(0, 0.03) for v in next_state]
            hist.append(next_state)
        return hist

    def generate_biased_history(generations=15):
        hist = [state[:]]
        for _ in range(generations):
            prev = hist[-1]
            # φ scaling but with bias vector added
            next_state = [prev[i]*PHI for i in range(predictor.dim)]
            # add bias along delta axis
            bias = predictor.axes.axes[2]  # δ axis
            for i in range(predictor.dim):
                next_state[i] += 0.2 * bias[i]
            next_state = [v + random.gauss(0, 0.02) for v in next_state]
            hist.append(next_state)
        return hist

    histories = {
        "Stable": generate_stable_history(),
        "Repetitive (α<1)": generate_repetitive_history(),
        "Biased (δ≠0)": generate_biased_history(),
    }

    for name, hist in histories.items():
        print(f"\n--- {name} ---")
        profile = predictor.predict(hist)
        print(f"Status        : {profile['status']}")
        print(f"Integrity     : {profile['integrity']:.3f}")
        print(f"Resonance R   : {profile['resonance_factor']:.3f}")
        print(f"Interference L: {profile['interference_load']:.3f}")
        print(f"R_reciprocity : {profile['R_reciprocity']:.3f}")
        print(f"α_scaling     : {profile['alpha_scaling']:.3f}")
        print(f"P_kernel      : {profile['P_kernel_projection']:.3f}")
        if profile['flags']:
            print("Flags:")
            for f in profile['flags']:
                print(f"  - {f}")

    print("\n" + "="*70)
    print("INTERPRETATION:")
    print("  STABLE       : Integrity>0.8, R<0.5, L<0.2, no flags.")
    print("  WARNING      : One metric borderline.")
    print("  COLLAPSE     : Integrity<0.3 or R>1.0 or L>0.5.")
    print("="*70)

if __name__ == "__main__":
    main()
