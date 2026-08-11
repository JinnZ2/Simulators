"""Phase 5 — synthetic ground-truth worlds.

Generate a latent target variable and an observable proxy under a KNOWN
instrument model (noise, bias, confounder leakage, alternative-cause
contamination). If the lab pipeline can't recover a known instrument, it must
not grade unknown ones.
"""
from __future__ import annotations
import numpy as np
from dataclasses import dataclass

@dataclass
class SyntheticWorld:
    """latent: true target. observed: proxy readings. The 'truth' dict is the
    answer key — estimation code must never see it."""
    latent: np.ndarray
    observed: np.ndarray
    truth: dict

def make_world(n: int = 2000, true_bias: float = 0.10, true_noise: float = 0.15,
               confounder_leak: float = 0.3, alt_cause_weight: float = 0.2,
               seed: int = 42) -> SyntheticWorld:
    """observed = latent + bias + confounder*leak + alt_cause*w + N(0, noise)"""
    rng = np.random.default_rng(seed)
    latent = rng.beta(2, 2, n)                     # true target in [0,1]
    confounder = rng.normal(0, 1, n)               # third variable moving both
    latent = np.clip(latent + 0.1 * confounder, 0, 1)
    alt_cause = rng.normal(0, 1, n)                # cause of observable bypassing target
    observed = (latent + true_bias + confounder_leak * confounder * 0.1
                + alt_cause_weight * alt_cause * 0.1
                + rng.normal(0, true_noise, n))
    return SyntheticWorld(latent=latent, observed=observed,
                          truth={"bias": true_bias, "noise": true_noise,
                                 "confounder_leak": confounder_leak,
                                 "alt_cause_weight": alt_cause_weight})

def estimate_instrument(world: SyntheticWorld) -> dict:
    """Recover instrument properties from observed-vs-verified-target pairs.

    In synthetic mode we are granted a small 'verified outcomes' holdout —
    mirroring reality, where a small set of ground-truth labels is what makes
    calibration possible at all."""
    n_holdout = max(50, len(world.latent) // 4)
    idx = np.arange(n_holdout)                      # holdout = first quarter
    err = world.observed[idx] - world.latent[idx]
    return {
        "estimated_bias": float(np.mean(err)),
        "estimated_noise": float(np.std(err)),
        "correlation_obs_latent": float(np.corrcoef(world.observed, world.latent)[0, 1]),
        "holdout_n": int(n_holdout),
    }

def recovery_score(world: SyntheticWorld, est: dict) -> dict:
    """Grade the pipeline against the answer key."""
    return {
        "bias_error": abs(est["estimated_bias"] - world.truth["bias"]),
        "noise_error": abs(est["estimated_noise"] - world.truth["noise"]),
        "passed": abs(est["estimated_bias"] - world.truth["bias"]) < 0.05 and
                  abs(est["estimated_noise"] - world.truth["noise"]) < 0.05,
    }
