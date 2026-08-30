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
#       UNASSIGNED and the exact fragmentation is refused.
#
# What survives that refusal is a LOWER BOUND on fragmentation, and it
# is enough to settle the spec's claim: the chain crosses the CA/US
# boundary in the delivered text, so at least two EAP authorities apply,
# so no single entity's plan spans the chain. The exact seam count is a
# different, unanswerable-here question.

import os
import sys

UNASSIGNED = "UNASSIGNED"

# The five owner categories the spec names, verbatim. Used only to state
# that the spec ASSERTS mixed ownership; no node is assigned to one.
OWNER_CATEGORIES = ("USACE", "USBR", "PUD", "BC Hydro", "private")

# The node list, transcribed from SOURCE_DROP.md section 1. A node's
# `jurisdiction` is set ONLY where the delivered text tags it; the
# three upper nodes carry "(CA)" and nothing else does, so everything
# else is US by the section headers ("US:", "Snake:", "Lower:") which
# are themselves in the delivered text. `owner` is UNASSIGNED for every
# node -- see the header.
NODES = [
    # (name, reach, jurisdiction-as-delivered, owner)
    ("Mica",             "Upper", "CA", UNASSIGNED),
    ("Revelstoke",       "Upper", "CA", UNASSIGNED),
    ("Keenleyside",      "Upper", "CA", UNASSIGNED),
    ("Grand Coulee",     "US",    "US", UNASSIGNED),
    ("Chief Joseph",     "US",    "US", UNASSIGNED),
    ("Wells",            "US",    "US", UNASSIGNED),
    ("Rocky Reach",      "US",    "US", UNASSIGNED),
    ("Rock Island",      "US",    "US", UNASSIGNED),
    ("Wanapum",          "US",    "US", UNASSIGNED),
    ("Priest Rapids",    "US",    "US", UNASSIGNED),
    ("Lower Granite",    "Snake", "US", UNASSIGNED),
    ("Little Goose",     "Snake", "US", UNASSIGNED),
    ("Lower Monumental", "Snake", "US", UNASSIGNED),
    ("Ice Harbor",       "Snake", "US", UNASSIGNED),
    ("McNary",           "Lower", "US", UNASSIGNED),
    ("John Day",         "Lower", "US", UNASSIGNED),
    ("The Dalles",       "Lower", "US", UNASSIGNED),
    ("Bonneville",       "Lower", "US", UNASSIGNED),
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


def spanning_bound():
    """A LOWER BOUND on the number of distinct EAP authorities over the
    chain, computed only from what the delivered text states.

    The bound is the number of distinct jurisdictions, because an EAP
    authority cannot cross a national boundary: a US federal owner's
    plan does not extend into BC Hydro's Canadian projects, and vice
    versa. That much is in the text (the CA tags). The spec asserts a
    finer split -- five owner categories -- but does not say which node
    is which, so the finer count is not computed."""
    juris = jurisdictions()
    return {
        "distinct_jurisdictions_in_text": len(juris),
        "jurisdictions": juris,
        "authorities_lower_bound": len(juris),
        "owner_categories_asserted_by_spec": len(OWNER_CATEGORIES),
        "owner_categories": list(OWNER_CATEGORIES),
        "per_node_owner_known": len(owners_assigned()),
        "n_nodes": len(NODES),
        "exact_seam_count": UNASSIGNED,
        "exact_seam_reason":
            "per-node ownership is public fact not in the delivered "
            "text; NID and project memoranda refuse CONNECT here, and it "
            "is not supplied from memory into a dam-safety artifact",
    }


def no_plan_spans():
    """The spec's own conclusion, and whether the delivered text settles
    it.

    'mixed ownership means no entity's plan spans the chain.' It is
    settled iff the authorities lower bound exceeds one -- and it does,
    from the CA/US split alone, before any per-node ownership is
    supplied. The finding is ROBUST to the missing data: no assignment
    of the 18 nodes to the 5 categories can reduce the jurisdiction
    count below the 2 the text already carries."""
    b = spanning_bound()
    settled = b["authorities_lower_bound"] > 1
    return {
        "no_single_plan_spans_chain": settled,
        "settled_by": "the CA/US boundary in the delivered node list",
        "robust_to_missing_ownership": True,
        "robust_because":
            "assigning the 18 nodes to owners can only RAISE the "
            "authority count above the jurisdiction floor, never lower "
            "it; the floor of 2 is already > 1",
        "authorities_lower_bound": b["authorities_lower_bound"],
    }


def render():
    out = []
    w = out.append
    b = spanning_bound()
    s = no_plan_spans()
    w("EAP COVERAGE -- the one governance claim computable from the")
    w("delivered text, without HEC-RAS, data, or invented ownership")
    w("")
    w("The spec: \"mixed ownership means no entity's plan spans the")
    w("chain. Record it as data, not commentary.\" This is that record.")
    w("")
    w("NODES (transcribed from SOURCE_DROP.md section 1):")
    w("  %d dam nodes; the estuary is a reach, not a node." % b["n_nodes"])
    last = None
    line = "  "
    for name, reach, juris, owner in NODES:
        if reach != last:
            if last is not None:
                w(line.rstrip())
            line = "  %-7s " % (reach + ":")
            last = reach
        line += "%s [%s]  " % (name, juris)
    w(line.rstrip())
    w("")
    w("OWNERSHIP, as the delivered text supports it:")
    w("  distinct jurisdictions in the text:   %d  %s" % (
        b["distinct_jurisdictions_in_text"], b["jurisdictions"]))
    w("  owner categories the spec asserts:    %d  %s" % (
        b["owner_categories_asserted_by_spec"], b["owner_categories"]))
    w("  per-node owner known here:            %d of %d" % (
        b["per_node_owner_known"], b["n_nodes"]))
    w("  exact number of EAP seams:            %s" % b["exact_seam_count"])
    w("    %s" % b["exact_seam_reason"])
    w("")
    w("THE SPEC'S CONCLUSION, and whether the text settles it:")
    w("  no single entity's plan spans the chain:  %s"
      % s["no_single_plan_spans_chain"])
    w("  settled by:  %s" % s["settled_by"])
    w("  authorities, lower bound:  %d" % s["authorities_lower_bound"])
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
