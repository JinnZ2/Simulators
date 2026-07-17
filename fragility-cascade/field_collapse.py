#!/usr/bin/env python3
"""
field_collapse.py

Where does the h* = 0.385 that `collapsetracker_harness.py` cites come from?

It is the SPINODAL of a reduced mean-field phi^4 + linear-field theory:

    F(phi, h) = -1/2 * phi^2 + 1/4 * phi^4 - h * phi        (reduced units)

Stationary points solve  -phi + phi^3 - h = 0.
Below the mean-field critical point the potential has two minima. As |h|
rises, one of them shrinks; at |h*| it collides with the local maximum
between the wells and disappears. Beyond that field strength there is no
metastable well left -- ANY infinitesimal fluctuation slides straight down
into the global minimum. That is the mean-field limit of stability.

Simultaneously d/dphi F = 0 and d^2/dphi^2 F = 0:
    -phi + phi^3 - h = 0
    -1 + 3 phi^2 = 0     ->   phi_s = +/- 1/sqrt(3)
    h_s = -phi_s + phi_s^3 = -+2 / (3 sqrt(3))

|h*| = 2 / (3 * sqrt(3)) = 0.38490017945975047...

That is the closed form. This module writes it out, checks it numerically,
and exposes SPINODAL_H_STAR so no downstream module has to hardcode it.

CLAIM (FC-1)
  In reduced mean-field phi^4 + linear-field theory, the spinodal sits at
  |h*| = 2/(3*sqrt(3)) = 0.38490017945975047. This is a CEILING on any
  measured collapse threshold in a system whose diversity order parameter
  is well-modelled by that universality class: fluctuations and
  nucleation lower the effective threshold below the mean-field value
  (Ginzburg criterion). Below-h* collapses are expected; above-h*
  survival refutes the mapping.

SCOPE
  Landau-Ginzburg phi^4 with no spatial / fluctuation / asymmetry terms.
  Reduced units: the -1/2 phi^2 + 1/4 phi^4 shape is what makes the
  number 0.3849 concrete. In raw units F = -a phi^2 + b phi^4 - h phi
  the same derivation gives |h*| = (2 a / 3) * sqrt(a / (3 b)); reduce
  to a = 1/2, b = 1/4 and this collapses to 2/(3 sqrt(3)).
  This module is a physics claim ABOUT the potential. Whether recursive
  training sits in this universality class is a MAPPING claim held
  separately -- see MAPPING below, and the P3 test in the harness.

MAPPING TO C-scale-2 (held separate from the physics)
  phi   ~  diversity retention order parameter (>0 = diverse well,
                                                <0 = collapsed well)
  h     ~  synthetic-fraction driver on the recursive-training loop
           (h=0 pure real, h large pushes toward the collapsed well)
  h*    ~  predicted knee in lambda(ratio) that P3 in
           collapsetracker_harness.py brackets against the measurement
           grid 0.25 / 0.5 / 0.75 / 1.0. P3 falsifies THIS mapping (not
           C-scale-2) if the measured knee lands outside [0.25, 0.5].

REFUTATION
  (R1) Repeat the derivation in a different phi^4 convention and get a
       h* value more than 1% off from 0.38490018. Convention mismatch,
       not physics -- the closed form is exact.
  (R2) A recursive-training run whose lambda(ratio) knee falls outside
       [0.25, 0.5] refutes the phi^4 mapping. Update the MAPPING; do
       not retune h*. The number is a physics constant, not a fit.
  (R3) A measurement that shows collapse thresholds ABOVE 2/(3 sqrt(3))
       in a system provably in the phi^4 universality class refutes
       mean-field spinodal as a ceiling. Would require field
       fluctuations that stabilise -- unphysical in this class.

UNKNOWNS
  - The MAPPING is the load-bearing unknown. Whether recursive-training
    diversity is well-modelled by phi^4 (vs. phi^6, asymmetric,
    fluctuation-dressed, or off-mean-field entirely) is genuinely open.
  - Ginzburg-criterion corrections lower h* below the mean-field value.
    This module does NOT compute them. The number here is the ceiling.

stdlib only. CC0.
"""

from __future__ import annotations

import math


# ------------------------------------------ closed-form spinodal (reduced)
# F(phi, h) = -1/2 phi^2 + 1/4 phi^4 - h phi
# spinodal:  F'  = F'' = 0  simultaneously
#   phi_s = 1/sqrt(3)
#   h_s   = 2 / (3 sqrt(3))
PHI_STAR = 1.0 / math.sqrt(3.0)
SPINODAL_H_STAR = 2.0 / (3.0 * math.sqrt(3.0))  # 0.38490017945975047


# ---------------------------------------------------- raw potential shape
def landau_potential(phi: float, h: float) -> float:
    """F(phi, h) = -1/2 phi^2 + 1/4 phi^4 - h phi   (reduced units)."""
    return -0.5 * phi * phi + 0.25 * phi ** 4 - h * phi


def dF_dphi(phi: float, h: float) -> float:
    """Force. Zeros are stationary points of F."""
    return -phi + phi ** 3 - h


def d2F_dphi2(phi: float, h: float) -> float:
    """Curvature. Zero coincident with dF/dphi=0 marks the spinodal."""
    return -1.0 + 3.0 * phi * phi


# ---------------------------------------- numerical cross-check of |h*|
def cubic_discriminant(h: float) -> float:
    """Discriminant of  dF/dphi = phi^3 - phi - h = 0.

    For x^3 + p x + q = 0 with p=-1, q=-h:  Delta = -4 p^3 - 27 q^2
        Delta > 0 : three real roots  (two wells + a local max)
        Delta = 0 : double root       (metastable well merges with local max)
        Delta < 0 : one real root     (only the global-minimum well survives)
    Setting Delta = 0 gives  h^2 = 4/27, i.e. |h*| = 2/(3 sqrt(3)).
    """
    return 4.0 - 27.0 * h * h


def n_real_roots(h: float) -> int:
    d = cubic_discriminant(h)
    if d > 1e-12:
        return 3
    if d < -1e-12:
        return 1
    return 2  # double root at the spinodal


def find_spinodal_numeric(bracket=(0.0, 1.0), tol=1e-15) -> float:
    """Bisection on the discriminant. Returns |h*| independently of the
    closed form, as a check that the algebra was not fudged."""
    a, b = bracket
    da = cubic_discriminant(a)
    for _ in range(200):
        m = 0.5 * (a + b)
        dm = cubic_discriminant(m)
        if da * dm <= 0.0:
            b = m
        else:
            a = m
            da = dm
        if (b - a) < tol:
            break
    return 0.5 * (a + b)


def ginzburg_note() -> str:
    return ("mean-field spinodal is a CEILING. Fluctuations (Ginzburg-"
            "criterion corrections) lower the effective threshold below "
            "|h*| = 0.3849. This module does not compute them.")


# --------------------------------------------------------------- main
def main():
    print("=" * 70)
    print("field_collapse.py -- mean-field phi^4 spinodal (FC-1)")
    print("=" * 70)
    print()
    print("Reduced potential:  F(phi, h) = -1/2 phi^2 + 1/4 phi^4 - h phi")
    print()
    print("Spinodal is where the metastable minimum coalesces with the")
    print("local maximum. Solve dF/dphi = 0 AND d2F/dphi2 = 0 together:")
    print()
    print("   -phi + phi^3 - h = 0")
    print("   -1 + 3 phi^2   = 0     ->   phi_s = 1/sqrt(3)")
    print("   h_s = -phi_s + phi_s^3 = -2 / (3 sqrt(3))")
    print()
    print(f"   phi_s   = 1/sqrt(3)     = {PHI_STAR:.17f}")
    print(f"   |h*|    = 2/(3 sqrt(3)) = {SPINODAL_H_STAR:.17f}")
    print()

    h_num = find_spinodal_numeric()
    print("Numerical cross-check (bisect the cubic discriminant of F'):")
    print(f"   |h*|  (numeric) = {h_num:.15f}")
    print(f"   |closed - numeric| = "
          f"{abs(SPINODAL_H_STAR - h_num):.2e}   (should be < 1e-14)")
    print()

    print("Real-root count of  dF/dphi = phi^3 - phi - h = 0  vs h:")
    print(f"   {'h':>10}  {'discriminant':>13}  {'#roots':>7}   geometry")
    for h in (0.0,
              SPINODAL_H_STAR / 2,
              SPINODAL_H_STAR - 1e-6,
              SPINODAL_H_STAR,
              SPINODAL_H_STAR + 1e-6,
              1.5 * SPINODAL_H_STAR):
        d = cubic_discriminant(h)
        n = n_real_roots(h)
        geo = {3: "two wells + hump",
               2: "spinodal: metastable well merges with hump",
               1: "one well left; the other has vanished"}[n]
        print(f"   {h:>10.7f}  {d:>13.6e}  {n:>7d}   {geo}")
    print()

    print("USED BY:")
    print("   collapsetracker_harness.py imports SPINODAL_H_STAR from here.")
    print("   The P3 knee test in the harness brackets the CollapseTracker")
    print("   grid (0.25 / 0.5 / 0.75 / 1.0) against |h*| = 0.3849 and")
    print("   fails if the measured knee sits outside [0.25, 0.5].")
    print()
    print("NOTE:", ginzburg_note())
    print("=" * 70)


if __name__ == "__main__":
    main()
