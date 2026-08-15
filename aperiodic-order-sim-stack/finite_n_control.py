"""
finite_n_control.py — the estimator controls the SIM-B drop did not run.

WHY THIS FILE EXISTS
--------------------
`SIM_STACK_REPORT.txt` calls SIM-B decisive on one number:

    |D_f(Ammann-Beenker) - D_f(Cascade)| = 0.334

and validates it against a stated finite-size baseline:

    |D_f(Ammann-Beenker) - D_f(Poisson)| = 0.021

But `figures/sim_b_point_sets.png` shows the two comparisons were not run
at the same sample size. Ammann-Beenker, Poisson, Lattice and Line each
carry ~12,000 points. Cascade carries 1,024 — about 12x fewer. The
baseline is matched-N; the decisive difference is not.

That matters because box counting on a finite point set saturates. Once
the box is small enough that almost every occupied box holds exactly one
point, N(s) stops growing and the log-log slope rolls over to zero. The
ceiling is the point count itself, and `figures/sim_b_boxcount.png` shows
it directly: the Cascade curve flattens at log N = 3.0 (= 1024), every
other curve flattens at log N = 4.08 (= 12,000). A sparser set has a
shorter scaling window, and a shorter window read through a plateau-finding
estimator can land somewhere else on the curve entirely.

So before "the dimensions separate" can stand, one question needs a
number: how much D_f does the estimator move on point sets whose true
dimension is KNOWN and does not depend on N?

WHAT THIS MEASURES
------------------
Three probes with exactly known dimensions, each run at both sample sizes:

  Poisson      true D_f = 2         the drop's own finite-size reference
  Line         true D_f = 1         estimator sanity check
  Cantor dust  true D_f = log4/log3 the class the Cascade is claimed to be
                                    in — genuinely sub-dimensional

Any movement between the two sample sizes is pure artifact, because the
truth is constant in N. The dust is additionally run under two box
ladders, because a second confound turned up while building this: when
the ladder's ratio is commensurate with the set's own scaling ratio, the
recovered dimension is materially different from when it is not.

WHAT THIS DOES NOT DO
---------------------
It does not reproduce the Ammann-Beenker tiling or the branching cascade —
the drop shipped results, not generators. It cannot recover the true
Cascade dimension. It can only size the artifact budget that has to come
off the top before a residual is called geometry.

Standard library only. Deterministic under a fixed seed.
"""

from __future__ import annotations

import math
import random
from typing import Iterable, Sequence

Point = tuple[float, float]

# Sample sizes read off figures/sim_b_point_sets.png panel titles.
N_DENSE = 12_000  # Ammann-Beenker, Poisson, Lattice, Line
N_SPARSE = 1_024  # Cascade

SEED = 20260815

REPORTED_GAP = 0.334      # |D_f(AB) - D_f(Cascade)| from SIM_STACK_REPORT.txt
REPORTED_BASELINE = 0.021  # |D_f(AB) - D_f(Poisson)|, matched-N


# ---------------------------------------------------------------------------
# probes — true dimension known, and independent of N
# ---------------------------------------------------------------------------

def poisson(n: int, rng: random.Random) -> list[Point]:
    """Uniform random points in the unit square. True D_f = 2 for all n."""
    return [(rng.random(), rng.random()) for _ in range(n)]


def line(n: int, rng: random.Random) -> list[Point]:
    """Points on the unit diagonal. True D_f = 1 for all n."""
    return [(t, t) for t in (rng.random() for _ in range(n))]


def cantor_dust(n: int, rng: random.Random, levels: int = 14) -> list[Point]:
    """
    2D Cantor dust: middle thirds removed on both axes, so each level keeps
    4 of 9 subsquares. Exact D_f = log(4)/log(3) = 1.2619.

    Placement is CONTINUOUS — after descending `levels` levels the point is
    scattered uniformly inside the surviving cell rather than pinned to its
    corner. That detail is load-bearing. Pinning points to corners makes the
    set a finite lattice of 4^levels discrete sites, so below the finest
    level every point is isolated, occupied-box count saturates early, and
    the recovered dimension reads 1.05 against a true 1.26. The set has not
    changed; only whether the sample resolves it has. That is the same
    failure this module exists to measure, met on the way in.
    """
    pts: list[Point] = []
    for _ in range(n):
        x = y = 0.0
        scale = 1.0
        for _ in range(levels):
            scale /= 3.0
            x += rng.choice((0.0, 2.0)) * scale
            y += rng.choice((0.0, 2.0)) * scale
        pts.append((x + rng.random() * scale, y + rng.random() * scale))
    return pts


# ---------------------------------------------------------------------------
# box counting
# ---------------------------------------------------------------------------

def normalize(points: Sequence[Point]) -> list[Point]:
    """Map into [0,1]^2 preserving aspect ratio (scale by the larger extent)."""
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    x0, y0 = min(xs), min(ys)
    extent = max(max(xs) - x0, max(ys) - y0)
    if extent <= 0:
        raise ValueError("degenerate point set: zero extent")
    return [((p[0] - x0) / extent, (p[1] - y0) / extent) for p in points]


def occupied_boxes(points: Iterable[Point], s: float) -> int:
    """Count distinct boxes of side s holding at least one point."""
    inv = 1.0 / s
    return len({(int(x * inv), int(y * inv)) for x, y in points})


def box_curve(points: Sequence[Point], base: float = 2.0,
              n_scales: int = 16) -> list[tuple[float, float]]:
    """Return [(log(1/s), log N(s))] over a geometric ladder of box sizes."""
    pts = normalize(points)
    return [
        (math.log(base ** i), math.log(occupied_boxes(pts, base ** -i)))
        for i in range(1, n_scales + 1)
    ]


def _fit(xs: Sequence[float], ys: Sequence[float]) -> tuple[float, float]:
    """Least-squares slope and r^2."""
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    sxx = sum((x - mx) ** 2 for x in xs)
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    syy = sum((y - my) ** 2 for y in ys)
    return (sxy / sxx if sxx else 0.0,
            (sxy * sxy) / (sxx * syy) if sxx and syy else 0.0)


def dimension(points: Sequence[Point], base: float = 2.0) -> dict[str, float]:
    """
    Box-counting dimension over the unsaturated part of the log-log curve.

    Saturation guard: points at or above 95% of log(N_points) are dropped
    before fitting. Past that ceiling the curve is flat because boxes have
    run out of points to hold, not because the set has run out of structure —
    and a flat run fits a straight line beautifully, so an unguarded
    max-r^2 plateau finder will park itself in the dead zone and report a
    dimension near zero.
    """
    curve = box_curve(points, base=base)
    ceiling = 0.95 * math.log(len(points))
    live = [(x, y) for x, y in curve if y < ceiling]
    if len(live) < 3:
        raise ValueError("sample too small to support a fit below saturation")

    slope, r2 = _fit([p[0] for p in live], [p[1] for p in live])
    return {"d_f": slope, "r2": r2, "scales": float(len(live))}


# ---------------------------------------------------------------------------
# the control
# ---------------------------------------------------------------------------

def run(generator, label: str, truth: float, base: float = 2.0) -> float:
    """Run one probe at both sample sizes. Returns the finite-N artifact."""
    dense = dimension(generator(N_DENSE, random.Random(SEED)), base=base)
    sparse = dimension(generator(N_SPARSE, random.Random(SEED + 1)), base=base)
    gap = dense["d_f"] - sparse["d_f"]

    print(f"\n{label}   true D_f = {truth:.4f}   ladder = base {base:g}")
    print(f"  N = {N_DENSE:>6,}   D_f = {dense['d_f']:.3f}   "
          f"r2 = {dense['r2']:.4f}   {int(dense['scales'])} live scales")
    print(f"  N = {N_SPARSE:>6,}   D_f = {sparse['d_f']:.3f}   "
          f"r2 = {sparse['r2']:.4f}   {int(sparse['scales'])} live scales")
    print(f"  finite-N shift (dense - sparse) = {gap:+.3f}")
    return gap


def main() -> None:
    dust_truth = math.log(4) / math.log(3)

    print("=" * 74)
    print("FINITE-N CONTROL FOR SIM-B")
    print("=" * 74)
    print("How much D_f does the estimator move between 12,000 and 1,024")
    print("points, on sets whose true dimension does not depend on N?")

    poisson_gap = run(poisson, "Poisson (space-filling)", 2.0)
    line_gap = run(line, "Line (1D sanity check)", 1.0)
    dust_gap_2 = run(cantor_dust, "Cantor dust", dust_truth, base=2.0)
    dust_gap_3 = run(cantor_dust, "Cantor dust", dust_truth, base=3.0)

    # Ladder confound, measured at the dense sample size only, so it is not
    # entangled with the finite-N shift above.
    dust_b2 = dimension(cantor_dust(N_DENSE, random.Random(SEED)), base=2.0)
    dust_b3 = dimension(cantor_dust(N_DENSE, random.Random(SEED)), base=3.0)
    ladder_gap = dust_b2["d_f"] - dust_b3["d_f"]

    finite_n = max(abs(poisson_gap), abs(line_gap),
                   abs(dust_gap_2), abs(dust_gap_3))
    budget = finite_n + abs(ladder_gap)

    print("\n" + "=" * 74)
    print("READING")
    print("=" * 74)
    print(f"  SIM-B reported  |D_f(AB) - D_f(Cascade)|  = {REPORTED_GAP:.3f}")
    print(f"  SIM-B baseline  |D_f(AB) - D_f(Poisson)|  = {REPORTED_BASELINE:.3f}"
          "   (matched-N)")
    print()
    print("  Artifact 1 — unmatched sample size. Largest shift across the")
    print(f"  three known-truth probes when N drops 12x: {finite_n:.3f}")
    print(f"    Poisson {poisson_gap:+.3f}   Line {line_gap:+.3f}   "
          f"dust(base2) {dust_gap_2:+.3f}   dust(base3) {dust_gap_3:+.3f}")
    print()
    print("  Artifact 2 — box-ladder commensurability. The same 12,000-point")
    print("  Cantor dust, same estimator, only the ladder ratio changed:")
    print(f"    base 2 (incommensurate) D_f = {dust_b2['d_f']:.3f}   "
          f"error {dust_b2['d_f'] - dust_truth:+.3f}")
    print(f"    base 3 (commensurate)   D_f = {dust_b3['d_f']:.3f}   "
          f"error {dust_b3['d_f'] - dust_truth:+.3f}")
    print(f"    ladder shift = {abs(ladder_gap):.3f}")
    print()
    print(f"  Combined artifact budget: {budget:.3f} against a reported")
    print(f"  separation of {REPORTED_GAP:.3f} — roughly "
          f"{100.0 * budget / REPORTED_GAP:.0f}% of it.")
    print()
    print("  Read the budget as an UPPER bound, not an expected error: it adds")
    print("  the worst observed shift from each artifact, and the two need not")
    print("  align in sign on any real point set. The residual below is")
    print("  correspondingly a LOWER bound on how much is structure.")
    print()

    if budget >= REPORTED_GAP:
        print("  The budget covers the reported gap. SIM-B's separation is not")
        print("  established by the shipped numbers.")
    else:
        print(f"  A residual of {REPORTED_GAP - budget:.3f} survives the budget,")
        print(f"  still well above the {REPORTED_BASELINE:.3f} matched-N baseline.")
        print("  SIM-B's DIRECTION survives: the Cascade does read lower, and")
        print("  not only because it is sparser. Its MAGNITUDE does not — the")
        print("  0.334 figure is quoted to a precision the method does not")
        print("  support, and 'decisive' is doing more work than it has earned.")

    print()
    print("  What would settle it: rerun SIM-B with Ammann-Beenker subsampled")
    print("  to 1,024 points, and with a Poisson control also at 1,024 in the")
    print("  Cascade's own bounding box. Both are cheap. Neither was run.")
    print()
    print("  This control cannot recover the true Cascade dimension, and does")
    print("  not claim to. It sizes the artifact, nothing more.")


if __name__ == "__main__":
    main()
