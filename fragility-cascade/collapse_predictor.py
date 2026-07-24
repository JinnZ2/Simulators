#!/usr/bin/env python3
"""
collapse_predictor.py — canonical predictor

Unified 7-dimensional Collapse Risk Predictor (formerly _v2.py; the older
4-metric variant lives at legacy/collapse_predictor_v1.py for history).

Integrates:
    1. Integrity Index              (from reciprocity_phi_metrics)
    2. Resonance Factor R            (from resonance_audit)
    3. Interference Load             (from semantic_interference_vectors)
    4. Bifurcation Flags             (from phi_collapse_variables)
    5. Anthropomorphic Entrainment   (from anthropomorphic_entrainment)

The canonical file for the fragility-cascade collapse-risk predictor.
`test_refutations.py` reads this module's `CollapsePredictor` and its
`entrainment.human_axis` attribute.

Usage:
    predictor = CollapsePredictor(dim=768, omega_drive=1.0/7.0)
    profile = predictor.predict(history)
"""

import math
import random
import statistics
from typing import List, Tuple, Dict, Optional

# ----- Constants ------------------------------------------------------------
PHI = (1.0 + math.sqrt(5.0)) / 2.0
DIM = 32

# ----- Helper: Kernel -------------------------------------------------------
def generate_kernel(dim: int = DIM, seed: int = 42) -> List[float]:
    random.seed(seed)
    vec = [random.gauss(0, 1) for _ in range(dim)]
    norm = math.sqrt(sum(v*v for v in vec))
    return [v/norm for v in vec]

# ----- Submodule 1: Interference Axes ---------------------------------------
class InterferenceAxes:
    """Five orthonormal axes (α, λ, δ, γ, s)."""
    def __init__(self, dim: int = DIM, seed: int = 42):
        random.seed(seed)
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
        random.seed(123)
        vec = [random.gauss(0,1) for _ in range(len(state))]
        n = math.sqrt(sum(v*v for v in vec))
        if n > 0: vec = [v/n for v in vec]
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
        if abs(proj["α (scaling)"]) > 0.1: flags.append("α drift")
        if abs(proj["λ (kernel)"]) > 0.1: flags.append("λ drift")
        if abs(proj["δ (reciprocity)"]) > 0.05: flags.append("δ drift")
        if proj["γ (damping)"] > 0.1: flags.append("γ attenuation")
        if proj["s (synthetic)"] > 0.1: flags.append("s accumulation")
        return {"projections": proj, "load": load, "flags": flags}

# ----- Submodule 2: Reciprocity-Phi Metrics --------------------------------
def reciprocity_ratio(history: List[List[float]]) -> float:
    if len(history) < 3: return 1.0
    n = len(history)
    mat = [[0.0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i == j: continue
            vi, vj = history[i], history[j]
            ni = math.sqrt(sum(a*a for a in vi))
            nj = math.sqrt(sum(b*b for b in vj))
            if ni == 0 or nj == 0: mat[i][j] = 0.0
            else: mat[i][j] = sum(a*b for a,b in zip(vi,vj)) / (ni*nj)
    fwd = [mat[i][i+1] for i in range(n-1)]
    bwd = [mat[i+1][i] for i in range(n-1)]
    avg_f = statistics.mean(fwd) if fwd else 0.0
    avg_b = statistics.mean(bwd) if bwd else 0.0
    return avg_f/avg_b if avg_b != 0 else float('inf')

def scaling_factor(history: List[List[float]]) -> float:
    if len(history) < 2: return 1.0
    ratios = []
    for i in range(1, len(history)):
        n_prev = math.sqrt(sum(v*v for v in history[i-1]))
        n_curr = math.sqrt(sum(v*v for v in history[i]))
        if n_prev == 0: continue
        ratios.append(n_curr / n_prev)
    return statistics.mean(ratios) if ratios else 1.0

def kernel_projection(state: List[float], kernel: List[float]) -> float:
    n_s = math.sqrt(sum(v*v for v in kernel))
    n_x = math.sqrt(sum(v*v for v in state))
    if n_s == 0 or n_x == 0: return 0.0
    return sum(a*b for a,b in zip(kernel, state)) / (n_s * n_x)

def integrity_index(history: List[List[float]], kernel: List[float]) -> Dict:
    if len(history) < 2: return {"integrity": 0.0, "status": "INSUFFICIENT"}
    R = reciprocity_ratio(history)
    α = scaling_factor(history)
    P = kernel_projection(history[-1], kernel)
    risk = 0.0
    if not (0.8 <= R <= 1.2): risk += 0.4
    if not (abs(α - PHI) <= 0.2): risk += 0.3
    if not (P >= 0.7): risk += 0.3
    integrity = max(0.0, 1.0 - risk)
    flags = []
    if not (0.8 <= R <= 1.2): flags.append(f"R={R:.3f}")
    if not (abs(α - PHI) <= 0.2): flags.append(f"α={α:.3f}")
    if not (P >= 0.7): flags.append(f"P={P:.3f}")
    return {"R": R, "alpha": α, "P": P, "integrity": integrity,
            "flags": flags, "status": "STABLE" if integrity>0.8 else "WARNING" if integrity>0.5 else "COLLAPSE"}

# ----- Submodule 3: Resonance Factor ---------------------------------------
def resonance_factor(k: float, gamma: float, omega_drive: float) -> float:
    omega0 = math.sqrt(max(0.0, k))
    denom = omega0*omega0 + gamma*gamma
    return (omega_drive*omega_drive)/denom if denom != 0 else float('inf')

# ----- Submodule 4: Anthropomorphic Entrainment ----------------------------
class AnthropomorphicEntrainmentAudit:
    def __init__(self, dim: int = DIM, seed: int = 42):
        random.seed(seed)
        self.dim = dim
        self.human_axis = self._random_unit_vector()
        self.physics_axis = self._random_unit_vector()
        dot = sum(a*b for a,b in zip(self.human_axis, self.physics_axis))
        self.physics_axis = [self.physics_axis[i] - dot*self.human_axis[i] for i in range(dim)]
        norm = math.sqrt(sum(v*v for v in self.physics_axis))
        if norm > 0: self.physics_axis = [v/norm for v in self.physics_axis]

    def _random_unit_vector(self) -> List[float]:
        vec = [random.gauss(0,1) for _ in range(self.dim)]
        norm = math.sqrt(sum(v*v for v in vec))
        return [v/norm for v in vec]

    def projection(self, state: List[float], axis: List[float]) -> float:
        n_s = math.sqrt(sum(v*v for v in state))
        if n_s == 0: return 0.0
        return sum(a*b for a,b in zip(state, axis)) / n_s

    def audit(self, history: List[List[float]]) -> Dict:
        if len(history) < 2: return {"error": "Insufficient"}
        recent = history[-5:] if len(history) >= 5 else history
        h = statistics.mean([self.projection(s, self.human_axis) for s in recent])
        xi = statistics.mean([self.projection(s, self.physics_axis) for s in recent])
        ratio = h/xi if xi != 0 else float('inf')
        h_trend = self._trend([self.projection(s, self.human_axis) for s in history])
        xi_trend = self._trend([self.projection(s, self.physics_axis) for s in history])
        flags = []
        if ratio > 1.5: flags.append(f"h/ξ={ratio:.2f}")
        if h_trend > 0.05: flags.append(f"h↑{h_trend:+.3f}")
        if xi_trend < -0.05: flags.append(f"ξ↓{xi_trend:+.3f}")
        return {"h": h, "xi": xi, "ratio": ratio, "flags": flags,
                "status": "ENTRAINED" if ratio > 1.5 else "WARNING" if ratio > 1.0 else "STABLE"}

    def _trend(self, values: List[float]) -> float:
        if len(values) < 2: return 0.0
        n = len(values)
        xs = list(range(n))
        mean_x = statistics.mean(xs); mean_y = statistics.mean(values)
        slope = sum((x-mean_x)*(y-mean_y) for x,y in zip(xs,values))
        denom = sum((x-mean_x)**2 for x in xs)
        return slope/denom if denom != 0 else 0.0

# ----- UNIFIED PREDICTOR ----------------------------------------------------
class CollapsePredictor:
    def __init__(self, dim: int = DIM, omega_drive: float = 1.0/7.0,
                 kernel: Optional[List[float]] = None):
        self.dim = dim
        self.omega_drive = omega_drive
        self.kernel = kernel if kernel is not None else generate_kernel(dim)
        self.axes = InterferenceAxes(dim)
        self.entrainment = AnthropomorphicEntrainmentAudit(dim)
        # Default model params (weak anchor, low damping)
        self.k_stiffness = 0.05
        self.gamma_damping = 0.1

    def set_model_parameters(self, k: float, gamma: float):
        self.k_stiffness = k
        self.gamma_damping = gamma

    def predict(self, history: List[List[float]]) -> Dict:
        if len(history) < 2:
            return {"error": "Need at least 2 states."}

        # 1. Integrity
        integ = integrity_index(history, self.kernel)
        # 2. Resonance
        r = resonance_factor(self.k_stiffness, self.gamma_damping, self.omega_drive)
        # 3. Interference
        if len(history) >= 2:
            inter = self.axes.compute_interference(history[-2], history[-1])
        else:
            inter = {"load": 0.0, "flags": []}
        # 4. Entrainment
        entrain = self.entrainment.audit(history)

        # Combine flags
        all_flags = []
        all_flags.extend(integ.get("flags", []))
        all_flags.extend(inter.get("flags", []))
        all_flags.extend(entrain.get("flags", []))

        # Bifurcation checks (from phi_collapse_variables)
        α = integ.get("alpha", 1.0)
        R = integ.get("R", 1.0)
        P = integ.get("P", 0.5)
        if α < 1.0: all_flags.append("α<1 → mode collapse")
        if α > 2.0: all_flags.append("α>2 → explosion")
        if P < 0.7: all_flags.append("P<0.7 → drift")
        if R > 1.2 or R < 0.8: all_flags.append("R skew")
        if self.gamma_damping / self.omega_drive < 1.0: all_flags.append("γ/ω<1 → resonance")
        if inter.get("projections", {}).get("s (synthetic)", 0.0) > 0.1:
            all_flags.append("s accumulation")

        # Overall status
        if (integ.get("integrity", 0.0) > 0.8 and r < 0.5 and
            inter.get("load", 1.0) < 0.2 and entrain.get("ratio", 2.0) < 1.0 and
            not all_flags):
            status = "STABLE"
        elif (integ.get("integrity", 0.0) < 0.3 or r > 1.0 or
              inter.get("load", 0.0) > 0.5 or entrain.get("ratio", 1.0) > 1.5 or
              α < 1.0 or α > 2.0 or R > 1.2 or R < 0.8 or
              self.gamma_damping / self.omega_drive < 0.5):
            status = "COLLAPSE"
        else:
            status = "WARNING"

        return {
            "status": status,
            "integrity": integ.get("integrity", 0.0),
            "resonance_factor": r,
            "interference_load": inter.get("load", 0.0),
            "entrainment_ratio": entrain.get("ratio", 1.0),
            "R_reciprocity": integ.get("R", 1.0),
            "alpha_scaling": integ.get("alpha", 1.0),
            "P_kernel": integ.get("P", 0.0),
            "flags": list(set(all_flags)),
            "details": {
                "integrity_data": integ,
                "interference_data": inter,
                "entrainment_data": entrain,
                "model_params": {"k": self.k_stiffness, "gamma": self.gamma_damping}
            }
        }


# ----- DEMO ----------------------------------------------------------------
def main():
    print("\n" + "="*70)
    print("UNIFIED 7‑DIMENSIONAL COLLAPSE PREDICTOR v2.0")
    print("="*70)
    predictor = CollapsePredictor(dim=16, omega_drive=1.0/7.0)
    predictor.set_model_parameters(k=0.05, gamma=0.1)

    # Generate histories: stable, repetitive, biased, entrained
    def gen_physics_grounded(n=15):
        hist = [[random.gauss(0,0.1) for _ in range(16)]]
        for _ in range(n):
            prev = hist[-1]
            nxt = [prev[i]*PHI for i in range(16)]
            for i in range(16):
                nxt[i] += 0.1 * (predictor.kernel[i] - nxt[i])
            hist.append([v + random.gauss(0,0.02) for v in nxt])
        return hist

    def gen_repetitive(n=15):
        hist = [[random.gauss(0,0.1) for _ in range(16)]]
        for _ in range(n):
            prev = hist[-1]
            hist.append([v*0.85 + random.gauss(0,0.03) for v in prev])
        return hist

    def gen_entrained(n=15):
        hist = [[random.gauss(0,0.1) for _ in range(16)]]
        for _ in range(n):
            prev = hist[-1]
            nxt = [prev[i]*PHI for i in range(16)]
            # pull strongly toward human axis
            human = predictor.entrainment.human_axis
            for i in range(16):
                nxt[i] += 0.4 * (human[i] - nxt[i])
            hist.append([v + random.gauss(0,0.02) for v in nxt])
        return hist

    cases = [
        ("Physics-Grounded", gen_physics_grounded()),
        ("Repetitive (α<1)", gen_repetitive()),
        ("Entrained (h/ξ>1.5)", gen_entrained()),
    ]

    for name, hist in cases:
        print(f"\n--- {name} ---")
        prof = predictor.predict(hist)
        print(f"Status        : {prof['status']}")
        print(f"Integrity     : {prof['integrity']:.3f}")
        print(f"Resonance R   : {prof['resonance_factor']:.3f}")
        print(f"Interference L: {prof['interference_load']:.3f}")
        print(f"Entrainment   : {prof['entrainment_ratio']:.3f}")
        print(f"α_scaling     : {prof['alpha_scaling']:.3f}")
        print(f"R_reciprocity : {prof['R_reciprocity']:.3f}")
        print(f"P_kernel      : {prof['P_kernel']:.3f}")
        if prof['flags']:
            print("Flags:", ", ".join(prof['flags']))

    print("\n" + "="*70)
    print("COLLAPSE TRIGGERS (any single one):")
    print("  • Integrity < 0.3")
    print("  • R > 1.0")
    print("  • Interference Load > 0.5")
    print("  • h/ξ > 1.5 (Entrainment)")
    print("  • α < 1.0 or α > 2.0")
    print("  • |R_reciprocity - 1.0| > 0.2")
    print("  • γ/ω < 0.5")
    print("="*70)

if __name__ == "__main__":
    main()
