"""
redemption_entropy.py
--------------------
How redeemable is a token, period by period, given a chain of L gates that can
each say "no"?

The naive model treats gates as independent: P(redeem) = (1 - p)**L. That is too
kind. It predicts compute (L=4, p=0.01) redeems 96% of the time. The document's
lived estimate is ~81%. The gap is CORRELATION: one grid outage, one provider
policy change, one supply shock takes down many gates at once. That common-mode
term is where the fragility actually lives.

This module runs both models so the gap is visible and falsifiable.

    independent:   each gate fails iid with prob p
    common-mode:   with prob q, a shared shock knocks out the whole chain,
                   AND each surviving gate still fails independently with prob p

Falsifiable prediction:
  1. mean redeemability falls monotonically with gate count L
  2. common-mode model predicts LOWER mean and HIGHER blackout frequency than
     independent, and it is the common-mode numbers that match field estimates
  3. variance grows with L -> the token behaves like a lottery on uptime, not a
     store of value

Refute by: showing a high-L token whose realized redeemability over a real crisis
window matches the independent (1-p)**L curve rather than the common-mode curve.

CC0. stdlib only.
"""

import random
from dataclasses import dataclass


@dataclass
class Chain:
    name: str
    gates: int          # L
    p_gate: float       # independent per-gate failure prob per period
    q_common: float     # common-mode (correlated) shock prob per period

    def independent_period(self, rng) -> int:
        """1 if every gate holds under independence assumption, else 0."""
        for _ in range(self.gates):
            if rng.random() < self.p_gate:
                return 0
        return 1

    def commonmode_period(self, rng) -> int:
        """1 if no shared shock AND every gate independently holds."""
        if rng.random() < self.q_common:
            return 0
        return self.independent_period(rng)


def simulate(chain: Chain, periods=100_000, seed=0):
    rng = random.Random(seed)
    ind = [chain.independent_period(rng) for _ in range(periods)]
    rng = random.Random(seed)  # same seed, fair comparison
    com = [chain.commonmode_period(rng) for _ in range(periods)]
    return {
        "name": chain.name,
        "L": chain.gates,
        "indep_mean": sum(ind) / periods,
        "common_mean": sum(com) / periods,
        "common_blackout_pct": 100 * (1 - sum(com) / periods),
    }


CHAINS = [
    Chain("oil (possession)", gates=1, p_gate=0.001, q_common=0.0002),
    Chain("compute_token",    gates=4, p_gate=0.010, q_common=0.150),
    Chain("ai_token",         gates=6, p_gate=0.020, q_common=0.320),
    Chain("resource_token",   gates=11, p_gate=0.020, q_common=0.400),
]


def report():
    print(f"{'chain':<18} L   indep   common  blackout%")
    print("-" * 52)
    for c in CHAINS:
        r = simulate(c)
        print(f"{r['name']:<18}{r['L']:>2}   {r['indep_mean']:.3f}   "
              f"{r['common_mean']:.3f}    {r['common_blackout_pct']:5.1f}")
    print("\nRead the gap between indep and common: that column is the lie in every")
    print("'99.9% uptime' promise. Independence is the marketing model. Correlation")
    print("is the physics. A barrel in your hand has L=1 and no shared shock.")


if __name__ == "__main__":
    report()
