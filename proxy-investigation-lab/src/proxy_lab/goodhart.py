"""Goodhart red-team harness — what happens to a proxy once it is USED for decisions.

"When a measure becomes a target, it ceases to be a good measure." The harness
simulates strategic agents who learn that the proxy drives a decision, then adapt
their behavior to move the observable WITHOUT moving the target. We measure:

  - gaming_latency: how quickly behavior shifts after the metric becomes a target
  - fidelity_collapse: proxy-outcome correlation before vs. after gaming
  - detection_surface: what residual signal still distinguishes gaming from truth
"""
from __future__ import annotations
import numpy as np
from dataclasses import dataclass

@dataclass
class GoodhartResult:
    baseline_correlation: float
    gamed_correlation: float
    fidelity_collapse: float          # baseline - gamed
    gaming_latency_periods: int       # periods until observable decouples
    detection_surface: dict           # residual signals that still separate gamers

def red_team(n: int = 3000, periods: int = 12, adapt_rate: float = 0.35,
             seed: int = 99) -> GoodhartResult:
    """Agents have a true latent state and an observable. In period 0 the
    observable is honest. From period 1 the proxy is a decision target and
    agents inflate the observable directly (cheaper than improving the latent)."""
    rng = np.random.default_rng(seed)
    latent0 = rng.beta(2, 2, n)
    skill = rng.normal(0, 1, n)                 # heterogeneous gaming ability
    base_corr, game_corr = None, None
    latency = periods
    for t in range(periods):
        pressure = min(1.0, adapt_rate * t)     # learned adaptation over time
        inflation = pressure * np.clip(0.3 + 0.2 * skill, 0, None)
        observed = np.clip(latent0 + inflation + rng.normal(0, 0.1, n), 0, 1.5)
        latent = np.clip(latent0 + 0.05 * t * 0.1 + rng.normal(0, 0.02, n), 0, 1)  # drifts slowly
        c = float(np.corrcoef(observed, latent)[0, 1])
        if t == 0:
            base_corr = c
        if base_corr and latency == periods and c < 0.7 * base_corr:
            latency = t
        if t == periods - 1:
            game_corr = c
    # detection surface: gamers inflate variance and break the slope at the top end
    top = observed > np.quantile(observed, 0.9)
    detection = {
        "variance_ratio_top_decile": float(np.var(observed[top]) / max(np.var(observed), 1e-9)),
        "slope_top_vs_bottom": float(
            np.polyfit(latent[~top], observed[~top], 1)[0]
            - np.polyfit(latent[top], observed[top], 1)[0]),
        "interpretation": "gaming flattens the observed-vs-latent slope at the top of the "
                          "distribution and inflates top-decile variance — audit there first",
    }
    return GoodhartResult(baseline_correlation=round(base_corr, 4),
                          gamed_correlation=round(game_corr, 4),
                          fidelity_collapse=round(base_corr - game_corr, 4),
                          gaming_latency_periods=int(latency),
                          detection_surface=detection)
