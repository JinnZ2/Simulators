#!/usr/bin/env python3
"""
multiscale.py - the same budget when resolution is not uniform.

    python3 multiscale.py
    python3 multiscale.py --selftest

budget.py assumes one resolution everywhere. Real simulations never do that:
adaptive mesh refinement, level-of-detail, lazy evaluation. A simulation
hypothesis that assumed uniform Planck resolution would be assuming the most
expensive architecture anyone has ever built, for no stated reason.

Cost per level is the L^-4 law weighted by the volume fraction at that level,
with the timestep tied to the cell (dt = L/c), so coarse regions step slower:

    cells_i = f_i * V * T * c / L_i^4

Total is the sum, and it is DOMINATED BY THE FINEST LEVEL times the fraction
of volume that needs it. That product is what the whole argument turns on, and
neither factor is constrained by anything measurable from inside.

Imports budget.py for constants and does not modify it. stdlib only. CC0.
"""

import argparse
import math
import os
import sys
from collections import OrderedDict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import budget as B                                              # noqa: E402

# --- densities, for deriving volume fractions honestly ---------------------

RHO_CRIT = B.RHO_CRIT               # 8.5e-27 kg/m^3
OMEGA_B = 0.0490                    # baryon fraction, Planck 2018
RHO_BARYON = OMEGA_B * RHO_CRIT     # ~4.2e-28 kg/m^3
RHO_NUCLEAR = 2.3e17                # kg/m^3, inside a nucleon
RHO_CONDENSED = 1.0e3               # kg/m^3, water/rock
RHO_ISM = 1.7e-21                   # kg/m^3, ~1 H atom per cm^3

V_OBS = (4.0 / 3.0) * math.pi * B.R_OBS ** 3
T_OBS = B.AGE


def volume_fraction(rho_local):
    """What fraction of the volume sits at a given local density?

    Mass is conserved: f = rho_mean / rho_local. Crude and correct to an order
    of magnitude, which is all any of this needs.
    """
    return RHO_BARYON / rho_local


def cells_at_level(fraction, length):
    """f * V * T * c / L^4 -- the L^-4 law with an adaptive timestep."""
    return fraction * V_OBS * T_OBS * B.C / length ** 4


def stack_cost(levels):
    """levels: [(name, fraction, length)]. Returns per-level and total."""
    rows = []
    total = 0.0
    for name, f, L in levels:
        n = cells_at_level(f, L)
        rows.append({"level": name, "fraction": f, "length_m": L, "cells": n})
        total += n
    for r in rows:
        r["share"] = r["cells"] / total if total else 0.0
    return {"levels": rows, "total_cells": total,
            "landauer_J": B.landauer_energy(total),
            "dominant": max(rows, key=lambda r: r["cells"])["level"]}


# --- architectures. each is a CHOICE. none is argued for by the hypothesis. -

def architectures():
    f_nuc = volume_fraction(RHO_NUCLEAR)
    f_con = volume_fraction(RHO_CONDENSED)
    f_ism = volume_fraction(RHO_ISM)
    return OrderedDict([
        ("uniform_planck", [
            ("everything", 1.0, B.L_PLANCK)]),
        ("planck_in_nucleons", [
            ("nucleon interiors", f_nuc, B.L_PLANCK),
            ("everywhere else", 1.0, 5.29e-11)]),
        ("atomic_in_matter", [
            ("condensed matter", f_con, 5.29e-11),
            ("diffuse gas", f_ism, 1.0e-2),
            ("everywhere else", 1.0, 1.0)]),
        ("coarse_with_fine_patches", [
            ("labs and detectors", 1e-40, B.L_PLANCK),
            ("condensed matter", f_con, 5.29e-11),
            ("everywhere else", 1.0, 1.0e3)]),
    ])


# --- the lazy limit --------------------------------------------------------

def observation_events():
    """Order-of-magnitude count of everything ever actually measured.

    The floor a render-on-observation architecture would pay if consistency
    were free. It is not free -- see consistency_cost().
    """
    humans_ever = 1.1e11
    seconds_per_life = 2.2e9              # ~70 yr
    photoreceptors = 1.2e8                # rods + cones, one retina pair
    events_per_second = 10.0              # flicker-fusion scale
    human = humans_ever * seconds_per_life * photoreceptors * events_per_second
    # instruments: be generous by many orders and it changes nothing
    instrumental = 1e30
    return {"human_photon_events": human,
            "instrumental_allowance": instrumental,
            "total": human + instrumental}


def consistency_cost():
    """The term that makes lazy evaluation not obviously cheap.

    Rendering on observation is only sound if what is rendered stays
    consistent with everything that could be checked later -- every record,
    every correlation, every delayed-choice measurement. Nobody has a bound
    on that, and it is not in any number above.

    Returned as an explicit UNMEASURED rather than estimated at zero, which is
    what quoting the event count alone would do.
    """
    return {"state": "UNMEASURED",
            "why": "no published bound on maintaining global consistency "
                   "under lazy evaluation with retrospective checkability",
            "estimated_here": None}


# --- report ----------------------------------------------------------------

def report():
    L = []
    A = L.append
    arch = architectures()
    costs = OrderedDict((k, stack_cost(v)) for k, v in arch.items())
    base = costs["uniform_planck"]["total_cells"]

    A("MULTI-SCALE RESOLUTION BUDGET")
    A("=" * 72)
    A("")
    A("  Cost per level: f_i * V * T * c / L_i^4")
    A("  (the L^-4 law, weighted by volume fraction, timestep dt = L/c)")
    A("")
    A("  VOLUME FRACTIONS, derived from densities not assumed:")
    A("    baryon mean density        %s kg/m^3" % B.sci(RHO_BARYON))
    for nm, r in (("nuclear (inside nucleons)", RHO_NUCLEAR),
                  ("condensed matter", RHO_CONDENSED),
                  ("diffuse ISM", RHO_ISM)):
        A("    fraction at %-26s %s" % (nm, B.sci(volume_fraction(r))))
    A("")
    A("-" * 72)
    A("")
    for name, c in costs.items():
        A("  %s" % name.upper().replace("_", " "))
        A("    %-24s %-11s %-11s %-11s %s"
          % ("level", "fraction", "length m", "cells", "share"))
        for r in c["levels"]:
            A("    %-24s %-11s %-11s %-11s %.3f"
              % (r["level"], B.sci(r["fraction"], 2), B.sci(r["length_m"], 2),
                 B.sci(r["cells"], 2), r["share"]))
        A("    %-24s %55s" % ("TOTAL", B.sci(c["total_cells"], 3) + " cells"))
        A("    %-24s %55s" % ("Landauer floor",
                              B.sci(c["landauer_J"], 3) + " J"))
        A("    %-24s %55s" % ("vs uniform Planck",
                              B.sci(c["total_cells"] / base, 2) + " x"))
        A("    dominant level: %s" % c["dominant"])
        A("")
    A("-" * 72)
    A("")
    A("  EVERY ARCHITECTURE IS DOMINATED BY ONE LEVEL:")
    A("    the finest resolution, times the volume fraction needing it.")
    A("    Neither factor is constrained by anything measurable from inside.")
    A("")
    obs = observation_events()
    A("  THE LAZY LIMIT -- render only what is measured")
    A("    human photon-absorption events, all people ever   %s"
      % B.sci(obs["human_photon_events"]))
    A("    instrumental allowance (generous by many decades) %s"
      % B.sci(obs["instrumental_allowance"]))
    A("    total measurement events                          %s"
      % B.sci(obs["total"]))
    A("    Landauer floor on that                            %s J"
      % B.sci(B.landauer_energy(obs["total"])))
    A("    vs uniform Planck                                 %s x"
      % B.sci(obs["total"] / base, 2))
    A("")
    e_lazy = B.landauer_energy(obs["total"])
    A("    For scale: %s J is about %.0f MJ -- %.1f kWh, or the chemical"
      % (B.sci(e_lazy, 3), e_lazy / 1e6, e_lazy / 3.6e6))
    A("    energy in roughly %.1f litre of gasoline (~34 MJ/L)."
      % (e_lazy / 3.4e7))
    A("    The Landauer floor on rendering every observation ever made, by")
    A("    everyone who has ever lived, is about a litre of fuel.")
    A("    That is what the architecture assumption is worth.")
    A("")
    cc = consistency_cost()
    A("    CONSISTENCY COST: %s" % cc["state"])
    A("      %s" % cc["why"])
    A("      not estimated here, and not set to zero. quoting the event")
    A("      count alone would set it to zero silently.")
    A("")
    A("=" * 72)
    A("")
    A("  THE SPREAD IS THE RESULT")
    A("")
    lo = obs["total"]
    A("    most expensive architecture   %s cells" % B.sci(base, 3))
    A("    cheapest floor considered     %s events" % B.sci(lo, 3))
    A("    span                          %s decades"
      % round(math.log10(base / lo)))
    A("")
    A("    budget.py found the answer moves 10^114 under ONE undefended")
    A("    parameter. Allowing multiple scales, it moves %d decades under an"
      % round(math.log10(base / lo)))
    A("    undefended ARCHITECTURE.")
    A("")
    A("    So 'the energy cost of simulating the universe' is not an")
    A("    underdetermined quantity. It is not a well-posed one until the")
    A("    level stack is specified, and no version of the hypothesis")
    A("    specifies it.")
    A("")
    A("    What survives unchanged: budget.py's SHB_005. No system simulates")
    A("    itself at full fidelity at any resolution, because the argument is")
    A("    about state capacity and not about cost.")
    return "\n".join(L)


# --- selftest --------------------------------------------------------------

def selftest():
    f = k = 0

    def ck(label, cond):
        nonlocal f, k
        k += 1
        if not cond:
            f += 1
            print("FAIL %s" % label)

    uni = stack_cost([("all", 1.0, B.L_PLANCK)])
    ck("uniform Planck reproduces budget.py's cell count",
       abs(uni["total_cells"] / B.counts()["n_spacetime_cells"] - 1.0) < 0.02)

    ck("L^-4 law holds across a decade",
       abs(cells_at_level(1.0, 1e-10) / cells_at_level(1.0, 1e-9) - 1e4)
       / 1e4 < 0.01)
    ck("cost is linear in volume fraction",
       abs(cells_at_level(0.5, 1e-10) / cells_at_level(1.0, 1e-10) - 0.5)
       < 1e-9)

    ck("nuclear volume fraction is ~1e-45",
       1e-46 < volume_fraction(RHO_NUCLEAR) < 1e-44)
    ck("condensed fraction is ~1e-31",
       1e-32 < volume_fraction(RHO_CONDENSED) < 1e-30)
    ck("denser means rarer", volume_fraction(RHO_NUCLEAR)
       < volume_fraction(RHO_CONDENSED) < volume_fraction(RHO_ISM))

    costs = {k2: stack_cost(v) for k2, v in architectures().items()}
    ck("uniform Planck is the most expensive",
       costs["uniform_planck"]["total_cells"]
       == max(c["total_cells"] for c in costs.values()))
    ck("every architecture is dominated by one level",
       all(max(r["share"] for r in c["levels"]) > 0.5
           for c in costs.values()))
    ck("refining a fraction of volume is cheaper than refining all of it",
       costs["planck_in_nucleons"]["total_cells"]
       < costs["uniform_planck"]["total_cells"])

    ck("shares sum to one",
       all(abs(sum(r["share"] for r in c["levels"]) - 1.0) < 1e-9
           for c in costs.values()))

    obs = observation_events()
    ck("observation count is astronomically below uniform Planck",
       obs["total"] < 1e-100 * costs["uniform_planck"]["total_cells"])
    ck("consistency cost is UNMEASURED, not zero",
       consistency_cost()["estimated_here"] is None
       and consistency_cost()["state"] == "UNMEASURED")

    ck("report renders", "SPREAD IS THE RESULT" in report())
    print("%d/%d checks passed" % (k - f, k))
    return 1 if f else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    print(report())
    return 0


if __name__ == "__main__":
    sys.exit(main())
