#!/usr/bin/env python3
"""
budget.py - what a Planck-resolution simulation of the observable universe
would cost, and which of those numbers mean anything.

    python3 budget.py            # full report
    python3 budget.py --selftest

Three layers, kept apart on purpose:

  ARITHMETIC     counts and energy floors computed in our own physics, about
                 a simulator embedded in our own physics. A consistent
                 calculation -- NOT a measurement of anything. The constants
                 are measured and used at their own scale; three interpretive
                 steps are not, and are named in --sources: Planck length as
                 a cell (~15.8 decades below the shortest length ever
                 probed), Planck time as a tick (~22.3 decades below the
                 shortest interval ever resolved), and kT ln2 per cell-step.
                 Relabelled from DECIDABLE after the delivered LADDER.md;
                 see ladder_audit.py. No number moved.
  VOID           the ratio "energy required / energy available to a simulator"
                 when the simulator is in a parent universe. Both operands must
                 be properties of ONE object; they are not. Refused, not
                 estimated. (reasoning-gate G-DIM)
  DOMINANT KNOB  the resolution assumption, which is doing more work than any
                 physics in the argument and is never defended.

The headline is not the big number. It is that the big number is a property of
an unargued resolution choice, and that the volume-based count everyone quotes
is wrong by ~60 orders of magnitude against the holographic bound.

stdlib only. CC0.
"""

import argparse
import math
import sys

# --- constants. CODATA 2018 unless noted. ----------------------------------

C = 299792458.0                 # m/s, exact
HBAR = 1.054571817e-34          # J s
KB = 1.380649e-23               # J/K, exact
G = 6.67430e-11                 # m^3 kg^-1 s^-2

L_PLANCK = 1.616255e-35         # m
T_PLANCK = 5.391247e-44         # s
E_PLANCK = 1.956e9              # J

# observable universe. Planck 2018 / standard cosmology.
R_OBS = 4.4e26                  # m, comoving radius (~46.5 Gly)
AGE = 4.35e17                   # s (13.787 Gyr)
T_CMB = 2.725                   # K
RHO_CRIT = 8.5e-27              # kg/m^3
LN2 = math.log(2.0)

SOURCES = {
    "L_PLANCK": "CODATA 2018",
    "T_PLANCK": "CODATA 2018",
    "R_OBS": "comoving radius of the observable universe, ~46.5 Gly",
    "AGE": "13.787 Gyr, Planck 2018",
    "T_CMB": "2.725 K -- the coldest available heat sink INSIDE this universe",
    "RHO_CRIT": "critical density, flat universe",
}


def sci(x, sig=3):
    if x == 0:
        return "0"
    e = int(math.floor(math.log10(abs(x))))
    m = round(x / (10.0 ** e), sig - 1)
    if abs(m) >= 10.0:          # rounding can push the mantissa over the top
        m /= 10.0
        e += 1
    elif abs(m) < 1.0:          # or under the bottom
        m *= 10.0
        e -= 1
    return "%.*fe%+d" % (sig - 1, m, e)


# --- layer 1: ARITHMETIC ---------------------------------------------------

def counts():
    """Planck cells in the observable universe over its history."""
    volume = (4.0 / 3.0) * math.pi * R_OBS ** 3
    n_vol = volume / L_PLANCK ** 3
    n_time = AGE / T_PLANCK
    return {
        "volume_m3": volume,
        "n_planck_volumes": n_vol,
        "n_planck_times": n_time,
        "n_spacetime_cells": n_vol * n_time,
    }


def holographic():
    """Bekenstein-Hawking / holographic bound: information goes as AREA."""
    area = 4.0 * math.pi * R_OBS ** 2
    bits = area / (4.0 * L_PLANCK ** 2) / LN2   # S/k_B in nats -> bits
    return {"area_m2": area, "max_bits": bits}


def universe_energy():
    """Total mass-energy at CRITICAL density over the comoving volume.

    Convention matters and is stated: this counts ALL components (matter,
    dark matter, dark energy) at rho_crit, giving ~3e54 kg. The commonly
    quoted ~1.5e53 kg counts matter only (Omega_m ~ 0.31). The choice moves
    the ratios below by ~1.3 orders of magnitude out of ~150 and changes no
    conclusion, but it is a choice.
    """
    volume = (4.0 / 3.0) * math.pi * R_OBS ** 3
    mass = RHO_CRIT * volume
    return mass * C ** 2


def landauer_energy(n_bit_ops, temp=T_CMB):
    """Floor for n IRREVERSIBLE bit operations against a bath at temp."""
    return n_bit_ops * KB * temp * LN2


def margolus_levitin_energy(n_ops, seconds):
    """A system of energy E performs at most 2E/(pi hbar) ops per second."""
    return n_ops * math.pi * HBAR / (2.0 * seconds)


def bremermann_rate(energy):
    """Ops per second available to a system of the given energy."""
    return 2.0 * energy / (math.pi * HBAR)


# --- layer 2: VOID ---------------------------------------------------------

class FrameError(Exception):
    pass


def cross_frame_ratio(required_J, available_J, same_frame):
    """Refuses unless both operands are properties of one physical frame.

    reasoning-gate G-DIM: a ratio needs both operands to be properties of ONE
    object. 'Energy our physics says the job costs' over 'energy a parent
    universe has' are properties of two different objects with two different
    sets of constants. The number would compute; it would not mean anything.
    """
    if not same_frame:
        raise FrameError(
            "VOID RATIO. numerator is computed from OUR hbar, k_B, T_CMB and "
            "l_Planck; denominator would be a property of a parent universe "
            "whose constants are unknown and need not match. Nothing licenses "
            "dividing one by the other. State the frame or do not form the "
            "ratio.")
    return required_J / available_J


# --- layer 3: THE KNOB -----------------------------------------------------

def resolution_sweep(lengths):
    """Cost scales as (l_Planck / L)^4 -- three space dims plus time.

    This is the whole argument's sensitivity. Nothing in the simulation
    hypothesis requires Planck resolution; it is assumed.
    """
    base = counts()["n_spacetime_cells"]
    out = []
    for name, L in lengths:
        dt = L / C
        n_v = ((4.0 / 3.0) * math.pi * R_OBS ** 3) / L ** 3
        n_t = AGE / dt
        cells = n_v * n_t
        out.append({"scale": name, "length_m": L, "cells": cells,
                    "cheaper_by": base / cells,
                    "landauer_J": landauer_energy(cells)})
    return out


# --- the one thing that is decidable without a parent frame ---------------

def self_simulation_possible(state_bits, overhead_bits=1):
    """Can a system simulate ITSELF at full fidelity, inside itself?

    Needs >= state_bits to represent the simulated copy, PLUS at least one bit
    of machinery distinguishing copy from original, inside a system that has
    state_bits total. Requires state_bits + overhead <= state_bits.

    Independent of any parent universe's constants, which is why it is the
    only conclusion here that survives layer 2.
    """
    # NOTE: do NOT decide this by computing state_bits + overhead_bits and
    # comparing. At 1e123 bits, float addition gives x + 1 == x exactly, and
    # the impossibility silently becomes "possible". The claim is exact, so
    # the test must be exact: you need MORE than you have iff overhead > 0.
    # Caught by this module's own selftest; kept as a worked instance of
    # arithmetic losing an argument that holds symbolically.
    need_exceeds = overhead_bits > 0
    return {"have_bits": state_bits,
            "need_bits": "%s + %s" % (state_bits, overhead_bits),
            "float_addition_loses_it": (state_bits + overhead_bits
                                        == state_bits),
            "possible": not need_exceeds}


# --- report ----------------------------------------------------------------

def report():
    L = []
    A = L.append
    c = counts()
    h = holographic()
    U = universe_energy()

    A("SIMULATION-HYPOTHESIS ENERGY BUDGET")
    A("=" * 72)
    A("")
    A("LAYER 1 -- ARITHMETIC (our physics, simulator embedded in our "
      "physics)")
    A("  A consistent calculation, not a measurement. Three interpretive")
    A("  steps carry the extrapolation -- see ladder_audit.py.")
    A("")
    A("  observable universe volume        %s m^3" % sci(c["volume_m3"]))
    A("  Planck volumes in it              %s" % sci(c["n_planck_volumes"]))
    A("  Planck times since t=0            %s" % sci(c["n_planck_times"]))
    A("  spacetime cells to step           %s" % sci(c["n_spacetime_cells"]))
    A("")
    A("  universe's own mass-energy        %s J" % sci(U))
    A("    (all components at rho_crit. matter-only is ~20x smaller;")
    A("     the choice moves the ratios by ~1.3 decades out of ~150.)")
    A("")
    e_land = landauer_energy(c["n_spacetime_cells"])
    e_ml = margolus_levitin_energy(c["n_spacetime_cells"], AGE)
    A("  ENERGY FLOORS, one bit-op per cell:")
    A("    Landauer  (k_B T ln2, T = %.3f K)   %s J" % (T_CMB, sci(e_land)))
    A("      = %s x the universe's mass-energy" % sci(e_land / U))
    A("    Margolus-Levitin (rate over %s s) %s J" % (sci(AGE), sci(e_ml)))
    A("      = %s x the universe's mass-energy" % sci(e_ml / U))
    A("")
    A("  Both floors assume the simulator sits in a universe with our")
    A("  constants and our CMB as its heat sink. That is the ONLY reading")
    A("  under which these numbers are about anything -- see LAYER 2.")
    A("")
    A("-" * 72)
    A("")
    A("  THE VOLUME COUNT IS THE WRONG COUNT.")
    A("")
    A("  holographic bound on the observable universe:")
    A("    horizon area                    %s m^2" % sci(h["area_m2"]))
    A("    max information in it           %s bits" % sci(h["max_bits"]))
    A("    Planck-VOLUME count             %s" % sci(c["n_planck_volumes"]))
    A("    volume count exceeds the bound by  %s" %
      sci(c["n_planck_volumes"] / h["max_bits"]))
    A("")
    A("  A region's information content goes as its AREA, not its volume.")
    A("  Every 'simulate every Planck volume' estimate overcounts the state")
    A("  by ~%d orders of magnitude before any energy is assigned to it."
      % round(math.log10(c["n_planck_volumes"] / h["max_bits"])))
    A("")
    n_holo_ops = h["max_bits"] * c["n_planck_times"]
    A("  redone on the holographic state, one update per Planck time:")
    A("    bit-operations                  %s" % sci(n_holo_ops))
    A("    Landauer floor                  %s J  (%s x universe)"
      % (sci(landauer_energy(n_holo_ops)),
         sci(landauer_energy(n_holo_ops) / U)))
    A("    Margolus-Levitin floor          %s J  (%s x universe)"
      % (sci(margolus_levitin_energy(n_holo_ops, AGE)),
         sci(margolus_levitin_energy(n_holo_ops, AGE) / U)))
    A("")
    A("  Still astronomically above the universe's own energy. The")
    A("  correction changes the exponent, not the conclusion, for the")
    A("  embedded-simulator reading.")
    A("")
    A("=" * 72)
    A("")
    A("LAYER 2 -- VOID (the ratio everyone actually wants)")
    A("")
    A("  'Could a simulator afford this?' requires:")
    A("      energy the job costs   /   energy the simulator has")
    A("")
    try:
        cross_frame_ratio(e_land, 1.0e100, same_frame=False)
        A("  ...computed. THIS LINE SHOULD BE UNREACHABLE.")
    except FrameError as exc:
        A("  REFUSED:")
        for line in str(exc).split(". "):
            if line.strip():
                A("    %s." % line.strip().rstrip("."))
    A("")
    A("  The numerator in LAYER 1 is built from OUR hbar, k_B, T_CMB and")
    A("  l_Planck. A parent universe running us need not share any of them.")
    A("  Its Planck length, its thermodynamics, its available energy and")
    A("  whether it even has a Landauer limit are all unconstrained by")
    A("  anything measurable from inside here.")
    A("")
    A("  So LAYER 1 is not an argument against the simulation hypothesis.")
    A("  It is a measurement of one specific thing: whether THIS universe")
    A("  could host a full-resolution simulation of itself. It could not,")
    A("  by ~150 orders of magnitude.")
    A("")
    A("=" * 72)
    A("")
    A("LAYER 3 -- THE KNOB THAT DOES THE WORK")
    A("")
    A("  Cost scales as (l_Planck / L)^4. Nothing in the hypothesis requires")
    A("  Planck resolution; it is assumed, and it is the assumption the whole")
    A("  number rests on.")
    A("")
    A("  %-22s %-12s %-12s %s" % ("resolution", "cells", "cheaper by",
                                  "Landauer J"))
    for r in resolution_sweep([
            ("Planck", L_PLANCK),
            ("proton radius", 8.4e-16),
            ("Bohr radius", 5.29e-11),
            ("visible light", 5.5e-7),
            ("1 mm", 1.0e-3),
            ("1 km", 1.0e3)]):
        A("  %-22s %-12s %-12s %s"
          % (r["scale"], sci(r["cells"], 2), sci(r["cheaper_by"], 2),
             sci(r["landauer_J"], 2)))
    A("")
    A("  The rule is L^-4: every factor of 10 in resolution is a factor of")
    A("  10^4 in cost. Planck to proton radius is ~19 decades of length and")
    A("  ~79 of cost; Planck to visible light is ~114 decades of cost.")
    A("  An argument whose conclusion moves by 10^114 under a parameter")
    A("  nobody has defended is a statement about that parameter.")
    A("")
    A("  And the resolution only has to beat what is MEASURED, not what")
    A("  exists. No experiment has resolved anything near l_Planck; the")
    A("  shortest length probed is ~10^-19 m at collider energies.")
    A("")
    A("=" * 72)
    A("")
    A("THE ONE CONCLUSION THAT SURVIVES LAYER 2")
    A("")
    s = self_simulation_possible(h["max_bits"])
    A("  Can a system simulate ITSELF at full fidelity, inside itself?")
    A("    bits available                  %s" % sci(s["have_bits"]))
    A("    bits needed (copy + 1 marker)   %s + 1" % sci(s["have_bits"]))
    A("    possible                        %s" % s["possible"])
    A("")
    A("    (decided exactly, not by addition: at this magnitude float")
    A("     arithmetic gives x + 1 == x, which is %s here, and would"
      % s["float_addition_loses_it"])
    A("     report the impossibility as possible. caught by selftest.)")
    A("")
    A("  This needs no parent-universe constants, which is why it is the only")
    A("  result here that is not frame-dependent. A full-fidelity self-")
    A("  simulation is impossible for any system whatsoever, at any scale,")
    A("  under any physics, because the copy plus the machinery distinguishing")
    A("  it from the original does not fit inside the original.")
    A("")
    A("  Everything else in this file is contingent on a frame nobody can")
    A("  measure from in here.")
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

    c = counts()
    h = holographic()

    ck("planck volume count in the expected decade",
       1e184 < c["n_planck_volumes"] < 1e186)
    ck("planck time count in the expected decade",
       1e60 < c["n_planck_times"] < 1e62)
    ck("holographic bound near 10^123",
       1e122 < h["max_bits"] < 1e124)
    ck("volume count exceeds holographic bound",
       c["n_planck_volumes"] > h["max_bits"])
    ck("overcount is 55-70 orders of magnitude",
       55 < math.log10(c["n_planck_volumes"] / h["max_bits"]) < 70)

    ck("landauer scales linearly",
       abs(landauer_energy(2e10) - 2 * landauer_energy(1e10)) < 1e-6 *
       landauer_energy(2e10))
    ck("landauer is positive and tiny per bit",
       0 < landauer_energy(1) < 1e-22)
    ck("ML bound falls as the deadline lengthens",
       margolus_levitin_energy(1e50, 1e18) <
       margolus_levitin_energy(1e50, 1e17))
    ck("bremermann inverts ML",
       abs(bremermann_rate(margolus_levitin_energy(1e40, 1.0)) - 1e40)
       < 1e30)

    try:
        cross_frame_ratio(1.0, 1.0, same_frame=False)
        ck("cross-frame ratio refused", False)
    except FrameError:
        ck("cross-frame ratio refused", True)
    ck("same-frame ratio allowed",
       cross_frame_ratio(10.0, 2.0, same_frame=True) == 5.0)

    sw = resolution_sweep([("a", L_PLANCK), ("b", L_PLANCK * 10)])
    ck("cost falls as the 4th power of resolution",
       abs(sw[0]["cells"] / sw[1]["cells"] - 1e4) / 1e4 < 0.01)

    ck("self-simulation impossible at any size",
       not self_simulation_possible(1e123)["possible"])
    ck("self-simulation impossible for a small system too",
       not self_simulation_possible(8)["possible"])

    ck("report renders", "VOID" in report())
    print("%d/%d checks passed" % (k - f, k))
    return 1 if f else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--sources", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if a.sources:
        for k, v in sorted(SOURCES.items()):
            print("  %-12s %s" % (k, v))
        return 0
    print(report())
    return 0


if __name__ == "__main__":
    sys.exit(main())
