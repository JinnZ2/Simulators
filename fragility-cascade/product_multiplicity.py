"""
product_multiplicity.py
-----------------------
Why a barrel of oil is intrinsically hedged and a compute-hour is not.

A barrel spawns a TREE of physically distinct products (fuels, plastics, solvents,
asphalt, pharma feedstock). When one branch's demand collapses, the barrel is
redirected. The branches fail INDEPENDENTLY, so total value has low variance.

A compute-hour spawns a wide range of digital services, but they all ride the same
trunk: same silicon, same API gateway, same grid, same Terms of Service. The
branches are near-perfectly CORRELATED. One trunk shock and every branch goes to
zero together. Wide menu, single point of failure.

Model: total value = sum of branch values. Each branch value = base * shock.
Independent branches -> variance shrinks ~1/N (diversification).
Single-trunk branches -> shared shock -> variance does NOT shrink with N.

Falsifiable claim: multiplicity only hedges when branches are decorrelated.
Counting menu items (breadth) without measuring branch correlation overstates
resilience. Refute by finding a single-trunk substrate whose value variance falls
like 1/N as you add menu items.

CC0. stdlib only.
"""

import random
from statistics import mean, pstdev


def total_value(n_branches, correlation, rng, trials=20_000):
    """
    correlation in [0,1]:
      0 -> each branch gets its own independent shock (oil-like)
      1 -> all branches share one shock (compute-like)
    Returns coefficient of variation (std/mean) of total value across trials.
    """
    totals = []
    for _ in range(trials):
        shared = rng.gauss(1.0, 0.4)
        t = 0.0
        for _ in range(n_branches):
            own = rng.gauss(1.0, 0.4)
            shock = correlation * shared + (1 - correlation) * own
            t += max(shock, 0.0)          # demand can't go negative
        totals.append(t)
    m = mean(totals)
    return pstdev(totals) / m if m else float("inf")


def report():
    rng = random.Random(1)
    print("branches   oil-like CoV (corr=0)   compute-like CoV (corr=1)")
    print("-" * 60)
    for n in (1, 2, 5, 10, 20):
        oil = total_value(n, 0.0, rng)
        cmp = total_value(n, 1.0, rng)
        print(f"{n:>6}          {oil:6.3f}                 {cmp:6.3f}")
    print("\nOil-like column falls ~1/sqrt(N): real diversification, an intrinsic")
    print("hedge baked into the substrate. Compute-like column is flat: adding menu")
    print("items buys you nothing, because they all die on the same trunk shock.")
    print("Product multiplicity is only a hedge if the branches can fail apart.")


if __name__ == "__main__":
    report()
