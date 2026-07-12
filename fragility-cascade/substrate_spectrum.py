"""
substrate_spectrum.py
---------------------
The substrate hierarchy as a scored model, plus the Monetary Durability Index.

CC0. stdlib only. Phone-buildable.

Core claim (falsifiable): a value substrate's durability is governed by how many
promises sit between the holder and biological use-value. Every property below is
a proxy for that promise count. MDI collapses them into one number.

    MDI = (possession_independence * product_multiplicity * gate_trust)
          / (obsolescence_rate * cone_depth * gate_count)

Refutation protocol: if a substrate scores low MDI but demonstrably survives
across a multi-decade shock better than a high-MDI substrate, the WEIGHTS or the
FACTOR SET are wrong. Update the claim. Do not retune to save a favored token.
"""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Substrate:
    name: str
    tier: int                    # 1 ground .. 4 clouds
    possession_independence: float  # 0..1  can you hold it with ~zero counterparties
    product_multiplicity: float     # >=1   independently-useful products one unit spawns
    gate_trust: float               # 0..1  per-gate reliability you can actually verify
    obsolescence_rate: float        # >0    fractional real-utility decay per year
    cone_depth: int                 # layers you depend on but cannot seize
    gate_count: int                 # independent "no" points between you and redemption

    def mdi(self) -> float:
        num = self.possession_independence * self.product_multiplicity * self.gate_trust
        den = self.obsolescence_rate * max(self.cone_depth, 1) * max(self.gate_count, 1)
        return num / den if den else float("inf")


# Reference table. Numbers are estimates, meant to be argued with, not trusted.
LEDGER = [
    #                       tier  poss  mult   trust  obsol cone gates
    Substrate("gold",          1, 0.98,   3.0,  0.99, 0.001,  1,   1),
    Substrate("oil",           1, 0.90,  40.0,  0.98, 0.02,   2,   1),
    Substrate("grain",         1, 0.85,   6.0,  0.95, 0.30,   2,   1),  # stores poorly -> high obsol
    Substrate("compute_token", 2, 0.05,   1.2,  0.90, 0.45,   8,   4),
    Substrate("ai_token",      3, 0.03,   1.05, 0.85, 0.90,  10,   6),
    Substrate("sovereign_bond",4, 0.02,   1.0,  0.75, 0.10,  12,   9),
    Substrate("resource_token",4, 0.02,   1.1,  0.70, 0.15,  14,  11),
]


def report():
    rows = sorted(LEDGER, key=lambda s: s.mdi(), reverse=True)
    w = max(len(s.name) for s in rows)
    print(f"{'substrate':<{w}}  tier   MDI       gates  cone  obsol/yr")
    print("-" * (w + 40))
    for s in rows:
        print(f"{s.name:<{w}}   T{s.tier}   {s.mdi():8.3f}   {s.gate_count:>3}   "
              f"{s.cone_depth:>3}    {s.obsolescence_rate:5.3f}")
    print("\nprinciple: abstraction is leverage; leverage is fragility.")
    print("MDI spans ~4 orders of magnitude ground -> cloud. That spread IS the claim.")


if __name__ == "__main__":
    report()
