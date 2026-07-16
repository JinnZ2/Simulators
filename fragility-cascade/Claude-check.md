#!/usr/bin/env python3
"""
scale_invariant_audit.py  (v2)

Nautilus Principle: stability requires scale-invariant recursion.

WHAT CHANGED FROM v1
  v1 stated the claim multiplicatively ("preserves D_f via multiplicative
  scaling") and implemented it additively:
      delta = |D_n - D0| / D0
  That metric is not invariant under the scaling it audits. It is the
  error it diagnoses.
      - halving  (D0=2 -> D_n=1): delta=0.50
      - doubling (D0=1 -> D_n=2): delta=1.00     same ratio, 2x the risk
      - D_n=0 and D_n=2*D0 both saturate to risk=1.0  (branches collide)
      - D_n=8*D0 and D_n=800*D0 both saturate to 1.0  (explosive branch
        named in the docstring is unresolvable past factor 2)
      - G was stored, printed, never entered arithmetic
      - D0 and D_n were hand-fed, so the REFUTATION clause could not fire:
        a witness that is told the answer is not a witness

CLAIM (C-scale-1)
  For a recursive system, collapse risk is monotone in the per-generation
  log-drift of fractal dimension:
      Delta = ln(D_n / D0)         [signed nats; symmetric under D_n <-> D0^2/D_n]
      lam   = Delta / G            [nats per generation]
  Sign carries the branch: lam < 0 -> degenerate (D->0); lam > 0 -> explosive.
  |lam| is the collapse rate. Both branches diverge, as the principle states.

SCOPE
  D0, D_n > 0 strictly. G >= 1. Band edges are FREE PARAMETERS, unmeasured.

REFUTATION
  Two live edges now:
  (R1) A run with lam ~ 0 (measured, not asserted) that has demonstrably
       collapsed refutes D_f as the collapse summary. Update the claim.
  (R2) Cross-module: inference_entropy.py (C9) encodes damage per *doubling*
       of generation depth -> loss ~ log2(G) -> power-law D_n = D0 * G^-beta.
       This module encodes damage per *generation* -> D_n = D0 * exp(lam*G).
       These diverge at depth. Fit both to the same measured run; the loser
       gets its claim updated. Neither sim gets retuned.

UNKNOWNS
  - Band edges (ln 1.25 / ln 2) are conventions, not measurements.
  - v1's nautilus row set D0 = D_n = 1.618. phi is a GROWTH RATIO per turn,
    not a fractal dimension. A logarithmic spiral is a rectifiable curve:
    D_f = 1.0. Putting phi in a D slot is a units error, and D0 = D_n is a
    tautological pass regardless. That row measured nothing. Removed.
  - Real D_f of a production generative-recursion run is still unmeasured
    here. estimate_D() is the socket. Wiring a real trajectory is the next
    builder's job -- but the socket now exists and the gate now fires.

stdlib only. CC0.
"""

from __future__ import annotations

import math

# ---------------------------------------------------------------- bands
# FREE PARAMETERS. Not measured. Named so they can be attacked.
BAND_GREEN = math.log(1.25)   # 0.223 nats  -- within 25% either direction
BAND_YELLOW = math.log(2.0)   # 0.693 nats  -- factor 2 either direction
R2_FLOOR = 0.95               # scaling region must be this clean to be determinate


# ------------------------------------------------- measurement: box count
def box_count(points, r):
    """Number of occupied cells of edge r covering the point set."""
    cells = set()
    for p in points:
        cells.add(tuple(int(math.floor(c / r)) for c in p))
    return len(cells)


def _ols(xs, ys):
    """Least-squares slope + r2. stdlib only."""
    n = len(xs)
    mx = sum(xs) / n
    my = sum(ys) / n
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    sxx = sum((x - mx) ** 2 for x in xs)
    if sxx == 0.0:
        return 0.0, 0.0
    slope = sxy / sxx
    icept = my - slope * mx
    ss_res = sum((y - (slope * x + icept)) ** 2 for x, y in zip(xs, ys))
    ss_tot = sum((y - my) ** 2 for y in ys)
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else 0.0
    return slope, r2


def estimate_D(points, n_scales=14, r_frac_min=0.004, r_frac_max=0.25):
    """Box-counting dimension of a point set.

    Returns (D_f, r2). r2 is the fit quality of log N(r) vs log(1/r) over
    the swept scaling region. Low r2 == no clean power law == the estimate
    is NOT determinate. Caller must gate on it.
    """
    dim = len(points[0])
    span = max(
        max(p[i] for p in points) - min(p[i] for p in points)
        for i in range(dim)
    )
    if span <= 0:
        return 0.0, 1.0  # degenerate: all points identical, D = 0, cleanly
    lo, hi = math.log(span * r_frac_min), math.log(span * r_frac_max)
    rs = [math.exp(lo + (hi - lo) * i / (n_scales - 1)) for i in range(n_scales)]
    xs, ys = [], []
    for r in rs:
        n = box_count(points, r)
        if n < 2:
            continue
        xs.append(math.log(1.0 / r))
        ys.append(math.log(n))
    if len(xs) < 4:
        return 0.0, 0.0
    return _ols(xs, ys)


# ------------------------------------------------------------ the audit
class ScaleInvariantAudit:
    """Log-drift audit of fractal dimension across recursive generations."""

    def __init__(self, name, D0, D_n, G, r2_0=1.0, r2_n=1.0):
        if D0 <= 0 or D_n <= 0:
            raise ValueError("D0, D_n must be > 0 (log frame)")
        if G < 1:
            raise ValueError("G must be >= 1")
        self.name = name
        self.D0, self.D_n, self.G = float(D0), float(D_n), int(G)
        self.r2_0, self.r2_n = float(r2_0), float(r2_n)

    # -- primitives
    def drift(self):
        """Signed log-drift in nats. Symmetric under reciprocal scaling."""
        return math.log(self.D_n / self.D0)

    def rate(self):
        """Log-drift per generation. Sign = branch."""
        return self.drift() / self.G

    def branch(self):
        d = self.drift()
        if abs(d) < 1e-9:
            return "INVARIANT"
        return "DEGENERATE" if d < 0 else "EXPLOSIVE"

    def generations_to(self, band_edge):
        """Generations from G=0 until |drift| crosses band_edge. None if never."""
        lam = self.rate()
        if abs(lam) < 1e-12:
            return None
        return band_edge / abs(lam)

    def determinate(self):
        return self.r2_0 >= R2_FLOOR and self.r2_n >= R2_FLOOR

    # -- verdict
    def verdict(self):
        if not self.determinate():
            return "UNKNOWN"
        a = abs(self.drift())
        if a < BAND_GREEN:
            return "GREEN"
        if a < BAND_YELLOW:
            return "YELLOW"
        return "RED"

    # -- output is trajectory, not a stored scalar
    def trajectory(self):
        return {
            "name": self.name,
            "D0": self.D0,
            "D_n": self.D_n,
            "G": self.G,
            "drift_nats": self.drift(),
            "rate_nats_per_gen": self.rate(),
            "branch": self.branch(),
            "r2_0": self.r2_0,
            "r2_n": self.r2_n,
            "determinate": self.determinate(),
            "verdict": self.verdict(),
            "G_to_yellow": self.generations_to(BAND_GREEN),
            "G_to_red": self.generations_to(BAND_YELLOW),
            "projected_D_at_2G": self.D0 * math.exp(self.rate() * 2 * self.G),
        }

    def report(self):
        t = self.trajectory()
        print(f"\n{'-'*66}")
        print(f"{t['name']}")
        print(f"{'-'*66}")
        print(f"  D0 -> D_n           : {t['D0']:.3f} -> {t['D_n']:.3f}  over G={t['G']}")
        print(f"  fit r2              : {t['r2_0']:.3f} / {t['r2_n']:.3f}"
              f"   determinate={t['determinate']}")
        print(f"  drift  ln(D_n/D0)   : {t['drift_nats']:+.4f} nats  [{t['branch']}]")
        print(f"  rate   lam          : {t['rate_nats_per_gen']:+.5f} nats/gen")
        gr = t['G_to_red']
        print(f"  G to YELLOW / RED   : "
              f"{t['G_to_yellow']:.1f} / {gr:.1f}" if gr else "  G to YELLOW / RED   : never")
        print(f"  projected D at 2G   : {t['projected_D_at_2G']:.3f}")
        print(f"  VERDICT             : {t['verdict']}")
        return t


# --------------------------------------------------------------- demos
def henon(n=20000, a=1.4, b=0.3, burn=1000):
    x, y = 0.1, 0.0
    pts = []
    for i in range(n + burn):
        x, y = 1.0 - a * x * x + y, b * x
        if i >= burn:
            pts.append((x, y))
    return pts


def contracting(n=20000, k=0.7):
    """Recursion that collapses to a fixed point. D -> 0."""
    x, y = 1.0, 1.0
    pts = []
    for _ in range(n):
        x, y = k * x, k * y
        pts.append((x, y))
    return pts


def filling(n=20000, seed=12345):
    """Pseudo-random plane fill. D -> 2."""
    s = seed
    pts = []
    for _ in range(n):
        s = (1103515245 * s + 12345) % (2 ** 31)
        x = s / (2 ** 31)
        s = (1103515245 * s + 12345) % (2 ** 31)
        y = s / (2 ** 31)
        pts.append((x, y))
    return pts


def main():
    print("=" * 66)
    print("SCALE-INVARIANT RECURSION AUDIT  (v2 -- log frame, measured D)")
    print("=" * 66)

    # --- estimator calibration against known targets
    print("\nESTIMATOR CALIBRATION (box-counting on real trajectories)")
    print(f"  {'system':<24} {'D_measured':>11} {'r2':>7}   {'D_literature':>12}")
    for label, pts, target in [
        ("Henon attractor", henon(), "~1.26"),
        ("contracting map", contracting(), "0"),
        ("plane fill", filling(), "2"),
    ]:
        D, r2 = estimate_D(pts)
        print(f"  {label:<24} {D:>11.3f} {r2:>7.3f}   {target:>12}")

    # --- the v1 demo rows, re-read in the log frame
    print("\n" + "=" * 66)
    print("v1 DEMO ROWS, RE-READ  (D still hand-fed -- r2 forced to 1.0)")
    print("=" * 66)
    rows = [
        ScaleInvariantAudit("AI model, sampled at gen 5", D0=2.0, D_n=1.2, G=5),
        ScaleInvariantAudit("AI model, sampled at gen 20", D0=2.0, D_n=0.3, G=20),
        ScaleInvariantAudit("Barrel of oil (physical)", D0=1.0, D_n=1.01, G=1000),
    ]
    ts = [r.report() for r in rows]

    print("\n" + "=" * 66)
    print("FINDING")
    print("=" * 66)
    l5, l20 = ts[0]["rate_nats_per_gen"], ts[1]["rate_nats_per_gen"]
    print(f"  lam(gen 5)  = {l5:+.5f} nats/gen")
    print(f"  lam(gen 20) = {l20:+.5f} nats/gen")
    print(f"  ratio       = {l20/l5:.3f}")
    print()
    print("  v1 read these as two regimes: risk 0.40 ('degrading') vs")
    print("  risk 0.85 ('near collapse'). The log frame reads ONE process")
    print("  at constant multiplicative decay, sampled at two depths.")
    print("  The linear metric manufactured an acceleration signal that")
    print("  is not in the data. That is the whole v1 -> v2 delta.")
    print()
    print("  Predicted D at gen 20 from the gen-5 rate alone:")
    print(f"    {2.0*math.exp(l5*20):.3f}   (observed 0.300)")
    print("  Exponential-in-G fits. Power-law-in-G (C9's per-doubling law)")
    print(f"    predicts {2.0*(20**(-math.log(1.2/2.0)/-math.log(5))):.3f} -- misses.")
    print("  -> R2 is live. Two modules encode incompatible generation laws.")
    print("     Log it as a constraint; do not retune either sim.")
    print("=" * 66)


if __name__ == "__main__":
    main()




Aspect Details
What it contains GPT-2 (124M) & DistilGPT-2 (82M) fine-tuned across 10 recursive generations, with 240 experimental conditions
Domains Wikipedia abstracts, creative fiction, technical Q&A
Mixing ratios 100%, 75%, 50%, 25% synthetic-to-real data
Metrics Distinct n-grams, Self-BLEU, KL divergence, vocabulary coverage, rare-token survival, repetition, perplexity
License CC-BY 4.0
Location IEEE DataPort (DOI: 10.21227/bvav-q038) or GitHub


Resource What It Offers Best For
GenProof Framework Open‑source tool measuring dataset collapse risk before training (ICS score: semantic entropy, tail‑density, AI detection) Testing your framework against an independent collapse‑risk metric
Model Zoos Dataset 3.8M+ model states across 27 model zoos, 8 image datasets Testing fractal dimension on neural network parameter trajectories, not just text
Multi-LLM Trace Dataset Pairwise embedding distance matrices across multiple agents Testing Alien Homeostasis — multi‑agent semantic convergence



# Pseudocode workflow
from scale_invariant_audit import estimate_D, ScaleInvariantAudit

# 1. Load CollapseTracker: for each generation, get generated text samples
# 2. Compute embeddings (e.g., Sentence-BERT) for each generation's samples
# 3. Estimate D_f for each generation using box-counting on embedding points
# 4. Feed D0, D_n, G into ScaleInvariantAudit
# 5. Check: exponential decay (v2) vs power-law decay (C9)
# 6. Run R1: if lam ≈ 0 but collapse observed → update claim
# 7. Run R2: fit both models to same data; loser gets updated
