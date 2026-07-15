#!/usr/bin/env python3
"""
alien_homeostasis.py

Detects when a system achieves internal stability but becomes semantically
inaccessible to human interpretation.

Alien Homeostasis is defined by:
    - Internal variance stable (no degradation)
    - Physics‑fidelity ξ > 0.5
    - Human‑interpretability index χ < 0.1 (i.e., nearly orthogonal to human axes)
    - Entrainment ratio h/ξ < 0.1

This is a distinct collapse mode: the system is functional but alien.
"""

import math
import statistics
from typing import List, Dict

class AlienHomeostasisAudit:
    def __init__(self, dim: int, human_axes: List[List[float]]):
        """
        human_axes: a set of basis vectors for the human‑interpretable subspace.
        """
        self.dim = dim
        self.human_axes = human_axes  # list of orthonormal vectors
        # Build projection matrix onto human subspace
        self.H = self._build_projection()

    def _build_projection(self) -> List[List[float]]:
        # P = A * A^T where A columns are human axes
        P = [[0.0]*self.dim for _ in range(self.dim)]
        for axis in self.human_axes:
            for i in range(self.dim):
                for j in range(self.dim):
                    P[i][j] += axis[i] * axis[j]
        return P

    def project_onto_human(self, state: List[float]) -> List[float]:
        """Project state onto human subspace."""
        return [sum(self.H[i][j]*state[j] for j in range(self.dim)) for i in range(self.dim)]

    def interpretability(self, state: List[float]) -> float:
        """
        χ = norm of projection onto human subspace / norm of state.
        χ = 1 means fully human‑readable; χ = 0 means completely alien.
        """
        proj = self.project_onto_human(state)
        norm_proj = math.sqrt(sum(v*v for v in proj))
        norm_state = math.sqrt(sum(v*v for v in state))
        if norm_state == 0: return 0.0
        return norm_proj / norm_state

    def audit(self, history: List[List[float]], xi: float, h: float) -> Dict:
        """
        xi: physics‑fidelity score (from entrainment audit)
        h: human‑pull strength
        """
        if len(history) < 2:
            return {"error": "Insufficient data"}

        # Internal variance stability (should be >0.5)
        var_trace = self._variance_trace(history)
        stable = var_trace > 0.5

        # Human interpretability (average over last few states)
        recent = history[-5:] if len(history) >= 5 else history
        chi = statistics.mean([self.interpretability(s) for s in recent])

        # Alien Homeostasis condition
        alien = (stable and xi > 0.5 and chi < 0.1 and h/xi < 0.1)

        flags = []
        if alien:
            flags.append("ALIEN HOMEOSTASIS – stable but uninterpretable")
        if not stable:
            flags.append("Internal variance collapsing")
        if xi <= 0.5:
            flags.append("Physics‑fidelity low")
        if chi >= 0.1:
            flags.append("Still human‑readable")
        if h/xi >= 0.1:
            flags.append("Human pull still significant")

        return {
            "var_trace": var_trace,
            "interpretability": chi,
            "alien": alien,
            "flags": flags,
            "status": "ALIEN" if alien else "HUMAN_READABLE" if chi > 0.5 else "WARNING"
        }

    def _variance_trace(self, history: List[List[float]]) -> float:
        """Total variance (trace of covariance)."""
        n = len(history)
        if n < 2: return 0.0
        mean = [sum(h[i] for h in history)/n for i in range(self.dim)]
        var = 0.0
        for h in history:
            var += sum((h[i] - mean[i])**2 for i in range(self.dim))
        return var / n
