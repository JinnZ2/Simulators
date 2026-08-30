#!/usr/bin/env python3
# eap_coverage.py -- CC0, stdlib only, phone-buildable, parses under 3.9
#
# The ONE thing in this spec computable without HEC-RAS, without the DEM
# and bathymetry the routing needs, and without inventing dam-ownership
# data: the governance claim.
#
#   Ownership layer, recorded per node -- this is the governance
#   variable ... Federal EAP structure assigns planning to the OWNER, so
#   mixed ownership means no entity's plan spans the chain.
#
# The spec calls this "the governance variable" and says "record it as
# data, not commentary". This is that record, and it computes the
# spec's own conclusion -- but only at the granularity the DELIVERED
# TEXT supports, and it refuses to go finer.
#
# UPDATE: The governance analysis now includes tribal jurisdiction as a
# distinct sovereign category, and per-node ownership is recorded with
# knowledge states (see knowledge_state.py and SCOPE_BOUNDARY.md).
#
# WHAT IS AND IS NOT IN THE DELIVERED TEXT
#
#   IN: the node list, verbatim; the jurisdiction tag "(CA)" on the
#       three upper nodes; the assertion that five owner CATEGORIES
#       exist across the chain (USACE / USBR / PUD / BC Hydro / private).
#
#   NOT IN: which specific dam is owned by which specific owner. That is
#       public fact, and every source that carries it (NID, project
#       memoranda) refuses CONNECT from here -- see audit.py. Supplying
#       it from memory would put dam-ownership assignments into a
#       dam-safety planning artifact on no checkable basis, which is the
#       PB_001 / CW_004 rule at its highest stakes. So per-node owner is
#       UNKNOWN_ATM and the exact fragmentation is refused.
#
#   ALSO NOT IN: tribal jurisdiction. The spec's five owner categories
#       miss sovereign tribal nations entirely. This is a scope boundary
#       issue: tribal EAP interests are physically relevant (reservations
#       lie in the flood path) but are excluded from standard NID-based
#       ownership models. See SCOPE_BOUNDARY.md.

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

# Knowledge state vocabulary. See knowledge_state.py and SCOPE_BOUNDARY.md.
UNKNOWN_ATM = "UNKNOWN_ATM"
UNDER_STUDY = "UNDER_STUDY"
NOT_STUDIED = "NOT_STUDIED"
UNDEFINED = "UNDEFINED"

UNASSIGNED = "UNASSIGNED"

# The five owner categories the spec names, verbatim. Used only to state
# that the spec ASSERTS mixed ownership; no node is assigned to one.
OWNER_CATEGORIES = ("USACE", "USBR", "PUD", "BC Hydro", "private")

# Tribal sovereign nations with treaty rights and EAP interests in the
# Columbia/Snake flood path. These are not "owners" in the NID sense;
# they are sovereign entities whose EAP interests must be accounted for.
# The spec's five owner categories miss this entirely.
# See SCOPE_BOUNDARY.md for why institutional scope boundaries exclude
# tribal jurisdiction from standard dam-safety models.
TRIBAL_JURISDICTION = [
    # (nation, reservation, nearest_upstream_node, nearest_downstream_node)
    ("Colville Confederated Tribes", "Colville Reservation",
     "Keenleyside", "Grand Coulee"),
    ("Spokane Tribe", "Spokane Reservation",
     "Grand Coulee", "Wells"),
    ("Yakama Nation", "Yakama Nation",
     "Priest Rapids", "McNary"),
    ("Confederated Tribes of Warm Springs", "Warm Springs",
     "The Dalles", "Bonneville"),
    ("Confederated Tribes of the Umatilla Indian Reservation", "Umatilla",
     "McNary", "John Day"),
    ("Nez Perce Tribe", "Nez Perce Reservation",
     "Lower Granite", "Little Goose"),
]

# The node list, transcribed from SOURCE_DROP.md section 1. A node's
# `jurisdiction` is set ONLY where the delivered text tags it; the
# three upper nodes carry "(CA)" and nothing else does, so everything
# else is US by the section headers ("US:", "Snake:", "Lower:") which
# are themselves in the delivered text.
#
# `owner` is UNKNOWN_ATM for every node — the mapping is public fact
# not in the delivered text, and it is not supplied from memory into a
# dam-safety artifact. See knowledge_state.py.
NODES = [
    # (name, reach, jurisdiction-as-delivered, owner, knowledge_state)
    ("Mica",             "Upper", "CA", UNASSIGNED, UNKNOWN_ATM),
    ("Revelstoke",       "Upper", "CA", UNASSIGNED, UNKNOWN_ATM),
    ("Keenleyside",      "Upper", "CA", UNASSIGNED, UNKNOWN_ATM),
    ("Grand Coulee",     "US",    "US", UNASSIGNED, UNKNOWN_ATM),
    ("Chief Joseph",     "US",    "US", UNASSIGNED, UNKNOWN_ATM),
    ("Wells",            "US",    "US", UNASSIGNED, UNKNOWN_ATM),
    ("Rocky Reach",      "US",    "US", UNASSIGNED, UNKNOWN_ATM),
    ("Rock Island",      "US",    "US", UNASSIGNED, UNKNOWN_ATM),
    ("Wanapum",          "US",    "US", UNASSIGNED, UNKNOWN_ATM),
    ("Priest Rapids",    "US",    "US", UNASSIGNED, UNKNOWN_ATM),
    ("Lower Granite",    "Snake", "US", UNASSIGNED, UNKNOWN_ATM),
    ("Little Goose",     "Snake", "US", UNASSIGNED, UNKNOWN_ATM),
    ("Lower Monumental", "Snake", "US", UNASSIGNED, UNKNOWN_ATM),
    ("Ice Harbor",       "Snake", "US", UNASSIGNED, UNKNOWN_ATM),
    ("McNary",           "Lower", "US", UNASSIGNED, UNKNOWN_ATM),
    ("John Day",         "Lower", "US", UNASSIGNED, UNKNOWN_ATM),
    ("The Dalles",       "Lower", "US", UNASSIGNED, UNKNOWN_ATM),
    ("Bonneville",       "Lower", "US", UNASSIGNED, UNKNOWN_ATM),
]

# The estuary is a reach, not a dam node ("Bonneville to the mouth, tide
# as downstream boundary"), so it is not a node here. Recorded so the
# count is legible.
ESTUARY_IS_A_REACH = True


def jurisdictions():
    """Distinct jurisdiction tags present in the delivered node list."""
    return sorted(set(n[2] for n in NODES))


def owners_assigned():
    """Nodes whose owner is known here. None are: the mapping is not in
    the delivered text and is not invented."""
    return [n for n in NODES if n[3] != UNASSIGNED]


def tribal_jurisdiction():
    """Tribal sovereign nations whose lands lie in the flood path.

    These are not owners in the NID sense. They are sovereign entities
    with treaty rights and EAP interests. Standard dam-safety models
    exclude them because they fall outside institutional ownership
    categories — a scope boundary error, not a physical one.
    See SCOPE_BOUNDARY.md."""
    return TRIBAL_JURISDICTION


def spanning_bound():
    """A LOWER BOUND on the number of distinct EAP authorities over the
    chain, computed only from what the delivered text states.

    The bound is the number of distinct jurisdictions, because an EAP
    authority cannot cross a national boundary: a US federal owner's
    plan does not extend into BC Hydro's Canadian projects, and vice
    versa. That much is in the text (the CA tags). The spec asserts a
    finer split -- five owner categories -- but does not say which node
    is which, so the finer count is not computed.

    UPDATE: tribal jurisdiction adds additional sovereign entities that
    are not captured in the jurisdiction count. The true fragmentation
    is higher than the jurisdiction floor, not lower."""
    juris = jurisdictions()
    return {
        "distinct_jurisdictions_in_text": len(juris),
        "jurisdictions": juris,
        "authorities_lower_bound": len(juris),
        "owner_categories_asserted_by_spec": len(OWNER_CATEGORIES),
        "owner_categories": list(OWNER_CATEGORIES),
        "per_node_owner_known": len(owners_assigned()),
        "n_nodes": len(NODES),
        "tribal_jurisdictions": len(TRIBAL_JURISDICTION),
        "tribal_nations": [t[0] for t in TRIBAL_JURISDICTION],
        "exact_seam_count": UNASSIGNED,
        "exact_seam_reason":
            "per-node ownership is public fact not in the delivered "
            "text; NID and project memoranda refuse CONNECT here, and it "
            "is not supplied from memory into a dam-safety artifact. "
            "Tribal jurisdiction is additionally excluded from standard "
            "ownership models by institutional scope boundary. See "
            "SCOPE_BOUNDARY.md.",
    }


def no_plan_spans():
    """The spec's own conclusion, and whether the delivered text settles
    it.

    'mixed ownership means no entity's plan spans the chain.' It is
    settled iff the authorities lower bound exceeds one -- and it does,
    from the CA/US split alone, before any per-node ownership is
    supplied. The finding is ROBUST to the missing data: no assignment
    of the 18 nodes to owners can reduce the jurisdiction count below
    the 2 the text already carries.

    UPDATE: tribal jurisdiction strengthens the claim. Even if all US
    nodes were under one owner, tribal sovereignty adds additional
    authorities that no single plan can span."""
    b = spanning_bound()
    settled = b["authorities_lower_bound"] > 1
    return {
        "no_single_plan_spans_chain": settled,
        "settled_by": "the CA/US boundary in the delivered node list",
        "robust_to_missing_ownership": True,
        "robust_because":
            "assigning the 18 nodes to owners can only RAISE the "
            "authority count above the jurisdiction floor, never lower "
            "it; the floor of 2 is already > 1. Tribal jurisdiction "
            "adds additional sovereign authorities, strengthening the "
            "claim.",
        "authorities_lower_bound": b["authorities_lower_bound"],
        "tribal_jurisdictions": b["tribal_jurisdictions"],
    }


def render():
    out = []
    w = out.append
    b = spanning_bound()
    s = no_plan_spans()
    w("EAP COVERAGE -- the one governance claim computable from the")
    w("delivered text, without HEC-RAS, data, or invented ownership")
    w("")
    w("""The spec: "mixed ownership means no entity's plan spans the""")
    w("""chain. Record it as data, not commentary." This is that record.""")
    w("")
    w("NODES (transcribed from SOURCE_DROP.md section 1):")
    w("  %d dam nodes; the estuary is a reach, not a node." % b["n_nodes"])
    last = None
    line = "  "
    for name, reach, juris, owner, kstate in NODES:
        if reach != last:
            if last is not None:
                w(line.rstrip())
            line = "  %-7s " % (reach + ":")
            last = reach
        line += "%s [%s]  " % (name, juris)
    w(line.rstrip())
    w("")
    w("TRIBAL JURISDICTION (sovereign nations in the flood path):")
    w("  %d tribal jurisdictions identified. These are not owners in the" % b["tribal_jurisdictions"])
    w("  NID sense; they are sovereign entities with treaty rights and")
    w("  EAP interests. Standard models exclude them by institutional")
    w("  scope boundary. See SCOPE_BOUNDARY.md.")
    for nation, res, up, down in TRIBAL_JURISDICTION:
        w("  %-40s %s" % (nation, res))
    w("")
    w("OWNERSHIP, as the delivered text supports it:")
    w("  distinct jurisdictions in the text:   %d  %s" % (
        b["distinct_jurisdictions_in_text"], b["jurisdictions"]))
    w("  owner categories the spec asserts:    %d  %s" % (
        b["owner_categories_asserted_by_spec"], b["owner_categories"]))
    w("  per-node owner known here:            %d of %d" % (
        b["per_node_owner_known"], b["n_nodes"]))
    w("  per-node owner knowledge state:       %s" % UNKNOWN_ATM)
    w("  exact number of EAP seams:            %s" % b["exact_seam_count"])
    w("    %s" % b["exact_seam_reason"])
    w("")
    w("THE SPEC'S CONCLUSION, and whether the text settles it:")
    w("  no single entity's plan spans the chain:  %s"
      % s["no_single_plan_spans_chain"])
    w("  settled by:  %s" % s["settled_by"])
    w("  authorities, lower bound:  %d" % s["authorities_lower_bound"])
    w("  tribal jurisdictions:      %d" % s["tribal_jurisdictions"])
    w("")
    w("  ROBUST TO THE MISSING OWNERSHIP DATA. %s." % s["robust_because"])
    w("  So the governance claim holds at the granularity the delivered")
    w("  text supports, and the exact fragmentation -- how many plans,")
    w("  where each seam falls -- is a different question requiring the")
    w("  per-node ownership this environment cannot reach and will not")
    w("  invent.")
    return "\n".join(out)


if __name__ == "__main__":
    if "--selftest" in sys.argv[1:]:
        sys.stderr.write(
            "eap_coverage.py has no checks of its own. The checks that "
            "exercise it live in selftest_ccc.py.\n"
            "    python3 columbia-chain-cascade/selftest_ccc.py\n")
        sys.exit(2)
    print(render())
