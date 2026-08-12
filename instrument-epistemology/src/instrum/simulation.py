"""Phase 6 — forward-simulated physics validation."""
from __future__ import annotations
import numpy as np
from dataclasses import dataclass

@dataclass
class SimulationResult:
    injected: float
    recovered: float
    recovery_error: float
    passed: bool
    detail: dict

def inject_and_recover(true_value: float, chain_fidelity: float,
                       noise: float, model_bias: float, n: int = 4000,
                       tol: float = 0.1, seed: int = 17) -> SimulationResult:
    rng = np.random.default_rng(seed)
    observed = true_value * chain_fidelity + model_bias + rng.normal(0, noise, n)
    recovered = float(np.mean(observed))
    err = abs(recovered - true_value) / max(abs(true_value), 1e-9)
    return SimulationResult(injected=true_value, recovered=round(recovered, 4),
                            recovery_error=round(err, 4), passed=err < tol,
                            detail={"chain_fidelity": chain_fidelity,
                                    "model_bias": model_bias, "noise": noise,
                                    "note": "unmodelled fidelity loss+bias appears as systematic error"})
