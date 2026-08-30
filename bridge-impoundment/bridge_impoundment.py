#!/usr/bin/env python3
# bridge_impoundment.py -- CC0, stdlib only, phone-buildable,
# parses under 3.9
#
# The drop names this file as the gap's expected deliverable. What is
# built here is the SCAFFOLD its structure supports without data, not
# the study: the parameter schema (every parameter carries a knowledge
# state and names what would move it), the three-state clog flag, the
# initiator interface contract, the mass-balance arithmetic, and both
# falsifier evaluators. NO real bridge appears anywhere in this file.
# The NBI, USGS and HEC-RAS inputs the study needs are named UNMEASURED
# per cell; a chain-level number produced here would read as a claim
# about real spans over real towns, which is the columbia-chain-cascade
# refusal (CCC_005) at the bridge scale.
#
# THE SIGN CAVEAT, ENFORCED RATHER THAN QUOTED: the drop's rule is that
# the successive-bridge protective finding (upstream structure shields
# downstream structure, standing-structure case) must not be carried
# into the release scenario. Here that is structural -- no function on
# the release path takes a shielding or reduction parameter, asserted
# over the signatures by the selftest, and the protective finding is
# representable only as a StandingStructureRecord whose one method
# refuses to emit into an initiator.

import sys

KNOWLEDGE_STATES = ("MEASURED", "UNDER_STUDY", "NOT_STUDIED",
                    "UNMEASURED", "CONSTRUCTED")

# carried from the drop's cited clogging literature (WRR 2025,
# Belgium/Germany 2021 floods); carried, not verified -- egress
# refuses the publisher (see audit.py EGRESS).
CLOG_SPACING_M = 10.0


def param(name, value, knowledge_state, moves_it):
    """A parameter cell. Refuses a value with no knowledge state and a
    state with no named mover -- the drop's own deliverable condition
    ('every parameter carries a knowledge state and names what would
    move it') as a constructor rule rather than a review item."""
    if knowledge_state not in KNOWLEDGE_STATES:
        raise ValueError("knowledge_state outside the closed "
                         "vocabulary: %r" % (knowledge_state,))
    if not moves_it or not str(moves_it).strip():
        raise ValueError("a parameter needs what would move it; "
                         "%r arrived without" % (name,))
    if value is not None and knowledge_state == "UNMEASURED":
        raise ValueError("%r carries a value marked UNMEASURED -- "
                         "one of the two is not true" % (name,))
    return {"name": name, "value": value,
            "knowledge_state": knowledge_state, "moves_it": moves_it}


# ---------------------------------------------------------- clog flag

def clog_flag(pier_spacing_m):
    """Three states, never two: FLAG at or under the carried threshold,
    CLEAR above it, UNMEASURED when the spacing is not known -- an
    unknown spacing is not a clear span."""
    if pier_spacing_m is None:
        return "UNMEASURED"
    if pier_spacing_m <= 0:
        raise ValueError("a pier spacing of %r m is not a span"
                         % (pier_spacing_m,))
    return "FLAG" if pier_spacing_m <= CLOG_SPACING_M else "CLEAR"


# ------------------------------------------------ initiator interface

# The CCC_007 comparability requirement, made checkable at the design
# layer: every initiator writes ONLY these keys. A breach hydrograph
# and a bridge-release hydrograph are interface-comparable iff their
# key sets are identical. Showing comparability ON THE ENGINE remains
# the routing run this environment cannot perform; what is checkable
# here is that nothing bridge-specific leaks into the downstream
# interface.

INITIATOR_KEYS = ("peak_flow", "time_to_peak", "volume", "debris_load",
                  "provenance")


def initiator(peak_flow, time_to_peak, volume, debris_load, provenance):
    return {"peak_flow": peak_flow, "time_to_peak": time_to_peak,
            "volume": volume, "debris_load": debris_load,
            "provenance": provenance}


def same_interface(a, b):
    return set(a.keys()) == set(b.keys()) == set(INITIATOR_KEYS)


class StandingStructureRecord(object):
    """The successive-bridge protective finding lives here and nowhere
    else: a record of the standing-structure, sustained-flow case. It
    has no path into an initiator -- asking for one raises, which is
    the drop's SIGN CAVEAT as a code path instead of a caution."""

    def __init__(self, reduction_fraction, basis):
        self.reduction_fraction = reduction_fraction
        self.basis = basis
        self.case = "standing-structure, sustained flow"

    def to_initiator(self):
        raise TypeError(
            "the protective finding is measured for the standing-"
            "structure case only and does not enter the release "
            "scenario (SIGN CAVEAT, SOURCE_DROP.md). Testing the "
            "release case is the gap.")


# ------------------------------------------------ mass-balance layer

def impoundment_arithmetic(inflow_rate, accumulation_time,
                           release_time):
    """Conservation only, no hydraulics: a clogged span that stores
    inflow for accumulation_time and releases the stored volume over
    release_time has peak-outflow gain = accumulation_time /
    release_time. Gain exceeds one exactly when the release is faster
    than the accumulation -- which is what a span giving way is. This
    is a property of storage-and-release, not of any bridge."""
    if min(inflow_rate, accumulation_time, release_time) <= 0:
        raise ValueError("all three terms are positive durations/rates")
    stored = inflow_rate * accumulation_time
    release_rate = stored / release_time
    return {"stored_volume": stored,
            "release_peak": release_rate,
            "gain": release_rate / inflow_rate,
            "gain_exceeds_one": release_time < accumulation_time}


def debris_budget(debris_in, structure_contribution):
    """The released debris load is the arriving load plus the span's
    own -- at or above unity by construction, with equality only when
    the structure contributes nothing."""
    if debris_in < 0 or structure_contribution < 0:
        raise ValueError("loads are non-negative")
    out = debris_in + structure_contribution
    return {"debris_out": out,
            "load_gain": (out / debris_in) if debris_in > 0 else None,
            "gain_at_least_one": out >= debris_in}


# ------------------------------------------------------- falsifiers

def falsifier(spacings, max_backwater, min_downstream_crest,
              breach_set_shifted):
    """The drop's primary falsifier, three-valued throughout. Returns
    GAP_CLOSES / GAP_STANDS / UNMEASURED. None anywhere means the
    input is not known, and an unknown input never closes a gap."""
    flags = [clog_flag(s) for s in spacings]
    if "UNMEASURED" in flags or not flags:
        return "UNMEASURED"
    if "FLAG" not in flags:
        return "GAP_CLOSES"  # no span at or under the threshold
    if max_backwater is None or min_downstream_crest is None \
            or breach_set_shifted is None:
        return "UNMEASURED"
    if max_backwater < min_downstream_crest and not breach_set_shifted:
        return "GAP_CLOSES"
    return "GAP_STANDS"


def coupling_falsifier(debris_supplies, clog_forming_threshold):
    """The secondary falsifier: supply below the clog-forming threshold
    at every flagged bridge drops the loop term -- and tests the
    coupling to the (absent) Gaps 2 and 14 directly."""
    if clog_forming_threshold is None or not debris_supplies \
            or any(s is None for s in debris_supplies):
        return "UNMEASURED"
    if all(s < clog_forming_threshold for s in debris_supplies):
        return "LOOP_TERM_DROPS"
    return "LOOP_TERM_STANDS"


# ---------------------------------------------------------- report

def chain_state():
    """What this module can say about the actual Columbia/Snake chain:
    nothing, per cell, honestly. Every input the study needs is
    UNMEASURED here, with the mover named."""
    return [
        param("pier_spacing_per_bridge", None, "UNMEASURED",
              "the NBI inventory pass (method step 1)"),
        param("debris_supply_per_bridge", None, "UNMEASURED",
              "coupling to the rim-slope and post-fire sources "
              "(method step 2; Gaps 14 and 2, absent from this tree)"),
        param("backwater_envelope", None, "UNMEASURED",
              "HEC-RAS obstruction routines (method steps 3-4)"),
        param("release_hydrograph", None, "UNMEASURED",
              "the failure-mode model (method step 5)"),
        param("breach_set_delta", None, "UNMEASURED",
              "the routing run (method step 7)"),
    ]


def render():
    out = []
    w = out.append
    w("BRIDGE IMPOUNDMENT -- SCAFFOLD STATE")
    w("")
    w("No real bridge appears in this module. The chain-level cells:")
    for p in chain_state():
        w("  %-26s %-11s <- %s" % (p["name"], p["knowledge_state"],
                                   p["moves_it"]))
    w("")
    w("clog_flag states: FLAG / CLEAR / UNMEASURED (threshold %.1f m,"
      % CLOG_SPACING_M)
    w("carried from the cited literature, not verified here)")
    demo = impoundment_arithmetic(1.0, 6.0, 1.0)
    w("storage-and-release arithmetic (constructed units): gain %.1f"
      % demo["gain"])
    w("  gain exceeds one iff release is faster than accumulation: %s"
      % demo["gain_exceeds_one"])
    b = initiator(1.0, 1.0, 1.0, 1.0, "breach")
    r = initiator(1.0, 1.0, 1.0, 1.0, "bridge-release")
    w("initiator interface identical across provenances: %s"
      % same_interface(b, r))
    w("the protective finding has no path into an initiator: enforced")
    w("")
    w("primary falsifier on the chain: %s"
      % falsifier([None], None, None, None))
    w("(an unknown input never closes a gap)")
    return "\n".join(out)


if __name__ == "__main__":
    if "--selftest" in sys.argv[1:]:
        sys.stderr.write(
            "bridge_impoundment.py has no checks of its own. The "
            "checks that exercise it live in selftest_bi.py.\n"
            "    python3 bridge-impoundment/selftest_bi.py\n")
        sys.exit(2)
    print(render())
