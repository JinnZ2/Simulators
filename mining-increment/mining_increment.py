#!/usr/bin/env python3
# mining_increment.py -- CC0, stdlib only, phone-buildable,
# parses under 3.9
#
# The drop names this file as the gap's expected deliverable. Built
# here is the SCAFFOLD its structure supports without data: the
# interface equation, the transfer gate, the stock/flow separation,
# the two subsidence time functions with their stated properties
# checked, and both falsifier evaluators. NO real mine, watershed, or
# reservoir appears in this file; every chain-level cell is UNMEASURED
# with its mover named -- a basin number produced here would read as a
# claim about real watersheds, the CCC_005 refusal again.
#
# The parameter schema is IMPORTED from the sibling gap's scaffold
# rather than copied -- both drops state the identical deliverable
# condition ("every parameter carries a knowledge state and names what
# would move it"), so there is one constructor for it in the tree.
#
# TWO RULES FROM THE DELIVERED PROSE, ENFORCED AS STRUCTURE:
#   the TRANSFER CAVEAT -- a coal-basin parameter applied to a basin
#   whose transfer is not established returns UNDEFINED, as a code
#   path (method step 2: "mark the imported parameter UNDEFINED
#   rather than applying it");
#   the STOCK/FLOW SEPARATION -- the storage-side and flow-side
#   quantities of the water-balance link are distinct named fields in
#   one record, and no function here returns a single scalar for the
#   pair (method step 4: "do not let a subsurface storage change and
#   a surface flow change share a variable name").

import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.append(os.path.join(ROOT, "bridge-impoundment"))
from bridge_impoundment import KNOWLEDGE_STATES, param  # noqa: E402,F401


# ------------------------------------------------- transfer gate

class ImportedParam(object):
    """A parameter imported from a study basin. Applying it to a
    target basin yields its value only where transfer is established
    for that basin; anywhere else it yields the string UNDEFINED --
    the caveat as a return value, not a caution."""

    def __init__(self, name, value, study_basin, basis):
        self.name = name
        self.value = value
        self.study_basin = study_basin
        self.basis = basis
        self.transfer = {}  # target basin -> True/False, established

    def establish_transfer(self, target_basin, established, basis):
        if not basis or not str(basis).strip():
            raise ValueError("establishing or refuting transfer takes "
                             "a basis")
        self.transfer[target_basin] = bool(established)

    def apply_to(self, target_basin):
        if target_basin == self.study_basin:
            return self.value
        if self.transfer.get(target_basin) is True:
            return self.value
        return "UNDEFINED"


# the two carried porosity deltas, entered against their study basin;
# carried, not verified -- publisher hosts refuse (audit.py EGRESS)
POROSITY_NON_FISSURE = ImportedParam(
    "surface_porosity_delta_non_fissure", 0.0742,
    "coal-basin (China/Pakistan)",
    "carried from the drop's table, Land Degradation & Development "
    "2025")
POROSITY_FISSURE = ImportedParam(
    "surface_porosity_delta_fissure", 0.1925,
    "coal-basin (China/Pakistan)",
    "carried from the drop's table, same row family")


# ------------------------------------------ stock/flow separation

def water_balance_link(storage_side, flow_side, basis):
    """The named intermediate of method step 4. Two distinct fields,
    both required (None is legal and means unmeasured on that side --
    which is a different statement from the sides sharing a name)."""
    if not basis or not str(basis).strip():
        raise ValueError("the link carries its basis")
    return {"storage_side_infiltration_capacity_delta": storage_side,
            "flow_side_runoff_coefficient_delta": flow_side,
            "basis": basis}


# ------------------------------------------------- the interface

def pool_effective(pool_natural, increment_fraction):
    """The contributing_inflow interface equation, as delivered:
    pool_effective = pool_natural * (1 + increment_fraction)."""
    if pool_natural < 0:
        raise ValueError("a pool level is non-negative")
    if increment_fraction == "UNDEFINED":
        return "UNDEFINED"
    return pool_natural * (1.0 + increment_fraction)


def rim_flag(aquifer_exposed):
    """The failure-concentration condition, three states: a parcel
    with the aquifer exposed FLAGs as a candidate displacement-wave
    source; not exposed CLEARs; unknown is UNMEASURED."""
    if aquifer_exposed is None:
        return "UNMEASURED"
    return "FLAG" if aquifer_exposed else "CLEAR"


# ---------------------------------------- subsidence time functions

def knothe(t, w0, c):
    """The confirmed anchor form: W(t) = W0 * (1 - e^(-c t))."""
    if t < 0 or w0 < 0 or c <= 0:
        raise ValueError("t, W0 non-negative; c positive")
    return w0 * (1.0 - math.exp(-c * t))


def mmf(t, w0, a, b):
    """The alternative form as supplied, carried with UNVERIFIED
    attribution per the drop's provenance flag -- anchor on knothe();
    this stays available for the comparison its family is used for."""
    if t < 0 or w0 < 0 or a <= 0 or b <= 0:
        raise ValueError("t, W0 non-negative; a, b positive")
    if t == 0:
        return 0.0
    return w0 * (t ** b) / (a + t ** b)


def shared_properties(w0=3.0, horizon=1e9):
    """The drop states both forms share W(0) = 0 and the asymptote
    W0. Checked by arithmetic rather than quoted."""
    k0, m0 = knothe(0.0, w0, 0.3), mmf(0.0, w0, 2.0, 1.5)
    k_inf = knothe(horizon, w0, 0.3)
    m_inf = mmf(horizon, w0, 2.0, 1.5)
    return {"both_zero_at_zero": k0 == 0.0 and m0 == 0.0,
            "both_approach_w0":
                abs(k_inf - w0) < 1e-6 and abs(m_inf - w0) < 1e-6}


def strain_integral(strain_profile):
    """S = integral of mean vertical strain over depth; trapezoid on
    (depth, strain) pairs. Dimensionally length, as the drop says."""
    if len(strain_profile) < 2:
        raise ValueError("an integral takes at least two points")
    s = 0.0
    for (h1, e1), (h2, e2) in zip(strain_profile, strain_profile[1:]):
        if h2 <= h1:
            raise ValueError("depths increase")
        s += 0.5 * (e1 + e2) * (h2 - h1)
    return s


# ------------------------------------------------------- falsifiers

def falsifier(increments, rim_intersections):
    """Primary: every tributary increment below 1% AND no mined
    parcel intersecting a rim slope closes the gap. Three-valued; an
    unknown never closes."""
    if not increments or any(i is None for i in increments) \
            or any(r is None for r in rim_intersections):
        return "UNMEASURED"
    if any(i == "UNDEFINED" for i in increments):
        return "UNMEASURED"  # an UNDEFINED import is not a low value
    if all(i < 0.01 for i in increments) \
            and not any(rim_intersections):
        return "GAP_CLOSES"
    return "GAP_STANDS"


def transfer_falsifier(imported_params, target_basin):
    """Secondary, and the first in this family with THREE outcomes by
    the drop's own text: transfer refuted everywhere -> the imports
    revert to UNDEFINED and the gap NARROWS to a measurement problem
    (what IS the delta for this rock); any established -> the gap
    stands on the imported side; nothing yet established or refuted
    -> UNMEASURED."""
    states = [p.transfer.get(target_basin) for p in imported_params]
    if all(s is False for s in states):
        return "GAP_NARROWS"
    if any(s is True for s in states):
        return "GAP_STANDS"
    return "UNMEASURED"


# ---------------------------------------------------------- report

def chain_state():
    return [
        param("mine_inventory", None, "UNMEASURED",
              "the MRDS pass plus state permits (method step 1)"),
        param("transfer_established", None, "UNMEASURED",
              "host-rock comparison against the coal-basin studies "
              "(method step 2)"),
        param("subsidence_extent", None, "UNMEASURED",
              "InSAR over mined parcels (method step 3)"),
        param("runoff_coefficient_delta", None, "UNMEASURED",
              "the water balance through the named link "
              "(method step 4)"),
        param("increment_fraction_per_tributary", None, "UNMEASURED",
              "the interface conversion (method step 5)"),
        param("rim_slope_candidates", None, "UNMEASURED",
              "mined parcels against rim slopes, aquifer exposure "
              "flagged (method step 6)"),
    ]


def render():
    out = []
    w = out.append
    w("MINING INCREMENT -- SCAFFOLD STATE")
    w("")
    w("No real mine, watershed, or reservoir appears in this module.")
    w("Chain-level cells:")
    for p in chain_state():
        w("  %-34s %-11s <- %s" % (p["name"], p["knowledge_state"],
                                   p["moves_it"]))
    w("")
    w("transfer gate: the carried coal-basin porosity deltas applied")
    w("to an unestablished basin return %r and %r"
      % (POROSITY_NON_FISSURE.apply_to("columbia-snake"),
         POROSITY_FISSURE.apply_to("columbia-snake")))
    sp = shared_properties()
    w("subsidence forms share W(0)=0 and the W0 asymptote (computed):")
    w("  %s / %s" % (sp["both_zero_at_zero"], sp["both_approach_w0"]))
    w("the anchor is knothe(); mmf() is carried with UNVERIFIED")
    w("attribution per the drop's own provenance flag")
    lk = water_balance_link(None, None, "unmeasured on both sides")
    w("stock/flow link fields: %s"
      % ", ".join(k for k in lk if k != "basis"))
    w("")
    w("primary falsifier on the chain: %s" % falsifier([None], [None]))
    w("transfer falsifier on the chain: %s"
      % transfer_falsifier([POROSITY_NON_FISSURE, POROSITY_FISSURE],
                           "columbia-snake"))
    w("(an unknown input never closes a gap; a refuted transfer")
    w("narrows it rather than closing it)")
    return "\n".join(out)


if __name__ == "__main__":
    if "--selftest" in sys.argv[1:]:
        sys.stderr.write(
            "mining_increment.py has no checks of its own. The checks "
            "that exercise it live in selftest_mi.py.\n"
            "    python3 mining-increment/selftest_mi.py\n")
        sys.exit(2)
    print(render())
