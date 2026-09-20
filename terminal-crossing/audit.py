#!/usr/bin/env python3
"""
audit -- WO-3 step 1: attack the falsifier, and read the three failed
candidates against the conditions.

The order's step 1 is "name a medium the conditions do not cover. If one
exists, the conditions are incomplete and should be revised, not
defended." That is a request for an attack, so one is made -- and the
proposal is held in its own constant, never merged into the six parsed
from the order. A candidate seventh medium and a delivered condition are
different objects, and a module that appended one to the other would
report the order as carrying seven bullets.

The second half reads the order's three failed candidates against the six
channels. The order gives all three one verdict, FAILS, and names a
different reason for each; the metric in crossing_rate.py records a
channel and has no field for a reason, so what the mapping shows is which
of the two a reader keeps.

WHAT THIS IS NOT. Nothing here decides whether the proposed seventh
medium counts as a crossing under the order's own usage. Both readings
are stated and the item is carried UNRESOLVED.

CC0. stdlib only. Parses under Python 3.9. ASCII.
"""

import collections
import sys

import crossing_rate as cr

CHOICES = [
    "[CHOICE 5] the proposed seventh medium is held in a separate "
    "constant and is never merged into the six parsed from the order",
    "[CHOICE 6] each failed candidate carries a mechanism field of this "
    "audit's own reading; the order's single FAILS verdict is carried "
    "beside it rather than replaced",
]

# ---------------------------------------------------------- step 1

Medium = collections.namedtuple(
    "Medium", "name covered_by shieldable reading_a reading_b state")

PROPOSED_SEVENTH = Medium(
    name="gravitational coupling",
    covered_by=None,
    shieldable=False,
    reading_a=(
        "it is a channel: mass-energy inside the boundary is read "
        "outside it, so something goes out"),
    reading_b=(
        "it is not a crossing under the order's own usage: the order's "
        "examples are things that go out and come back, and nothing "
        "returns through this one"),
    state="UNRESOLVED",
)


def covered(medium, path=cr.ORDER):
    """Does any parsed condition name the proposed medium's channel?

    The order's third bullet enumerates power, thermal and acoustic. A
    coupling outside that list is not named by any of the six.
    """
    named = " ".join(text.lower() for _, text in cr.conditions(path))
    words = [w for w in medium.name.lower().split() if len(w) > 3]
    hits = [w for w in words if w in named]
    return hits


def falsifier_state(medium, path=cr.ORDER):
    """UNSATISFIED / UNSATISFIABLE_IF_COUNTED, with the split stated.

    The order reports no instance found, which is UNSATISFIED: the
    conditions are stated and nothing meets them. A medium that cannot be
    shielded at any expenditure is a different epistemic object -- the
    falsifier would then be UNSATISFIABLE, and no search closes it.
    """
    if covered(medium, path):
        return ("COVERED_BY_CONDITIONS", "the six name this channel")
    if medium.shieldable:
        return ("UNSATISFIED", "an uncovered channel that can be closed")
    return ("UNSATISFIABLE_IF_COUNTED",
            "an uncovered channel that no expenditure closes -- and "
            "whether it counts is " + medium.state)


# ------------------------------------------------- the three candidates

Candidate = collections.namedtuple(
    "Candidate", "name order_verdict mechanism channel quote")

CANDIDATES = [
    Candidate(
        "ab_test_recommendation_matchmaking", "FAILS",
        "DEFERRED_CONSEQUENCE", "operator",
        "the defect never appears in the test, only in the projections "
        "built on it"),
    Candidate(
        "throwaway_prototype", "FAILS",
        "EXTERNALISED", "supply+disposal",
        "it is not terminal, it is EXTERNALISING"),
    Candidate(
        "scratch_calculation_air_gap", "FAILS",
        "DESIGN_NOT_FACT", "operator",
        "Terminal-in-design, not terminal-in-fact"),
]


def mechanism_channel_map():
    """Do distinct mechanisms map to distinct channels? [CHOICE 6]"""
    by_channel = collections.OrderedDict()
    for c in CANDIDATES:
        by_channel.setdefault(c.channel, []).append(c.mechanism)
    collisions = [(ch, ms) for ch, ms in by_channel.items() if len(ms) > 1]
    return {
        "mechanisms": len(set(c.mechanism for c in CANDIDATES)),
        "channels": len(by_channel),
        "collisions": collisions,
    }


def conditions_unexercised(path=cr.ORDER):
    """Conditions no delivered candidate is mapped onto."""
    touched = set()
    for c in CANDIDATES:
        for part in c.channel.split("+"):
            touched.add(part)
    return [cid for cid in cr.channel_ids(path) if cid not in touched]


# ------------------------------------------------------- other markers

CONTAMINATION = {
    "state": "UNKNOWN",
    "order_line": "Recorded as UNKNOWN deliberately. Not resolved in "
                  "either direction.",
    "note": "a third state, kept apart from a measured zero and from a "
            "measured crossing",
}

SEARCH_STATUS = {
    "item": "step 4, an honest costing that declined",
    "order_line": "Two searches did not find one",
    "corpus": "NOT_STATED",
    "terms": "NOT_STATED",
    "reading": "an absence with no corpus and no terms bounding it",
}


# ---------------------------------------------------------------- render

def render():
    out = []
    out.append("WO-3 AUDIT -- step 1 attack, and the three candidates")
    out.append("The seventh medium is PROPOSED here and is not in the "
               "order's six.")
    out.append("")
    for c in CHOICES:
        out.append(c)
    out.append("")

    conds = cr.conditions()
    out.append("Step 1, attack on the falsifier:")
    out.append("  proposed medium : %s" % PROPOSED_SEVENTH.name)
    out.append("  named by the six: %s"
               % (covered(PROPOSED_SEVENTH) or "no"))
    out.append("  shieldable      : %s" % PROPOSED_SEVENTH.shieldable)
    state, why = falsifier_state(PROPOSED_SEVENTH)
    out.append("  falsifier state : %s" % state)
    out.append("    %s" % why)
    out.append("  reading A: %s" % PROPOSED_SEVENTH.reading_a)
    out.append("  reading B: %s" % PROPOSED_SEVENTH.reading_b)
    out.append("  carried   : %s, neither reading taken here"
               % PROPOSED_SEVENTH.state)
    out.append("")

    out.append("The order's three failed candidates:")
    out.append("  %-36s %-10s %-22s %s"
               % ("candidate", "verdict", "mechanism (read here)",
                  "channel"))
    for c in CANDIDATES:
        out.append("  %-36s %-10s %-22s %s"
                   % (c.name, c.order_verdict, c.mechanism, c.channel))
    m = mechanism_channel_map()
    out.append("  distinct mechanisms %d against distinct channels %d"
               % (m["mechanisms"], m["channels"]))
    for ch, ms in m["collisions"]:
        out.append("  channel %s carries %d mechanisms: %s"
                   % (ch, len(ms), ", ".join(ms)))
    out.append("  so the channel is not a function of the mechanism, and "
               "the metric records the channel.")
    out.append("")

    unex = conditions_unexercised()
    out.append("Conditions exercised by no delivered candidate: %d of %d"
               % (len(unex), len(conds)))
    for cid in unex:
        out.append("  %s" % cid)
    out.append("")

    out.append("Contamination marker: %s" % CONTAMINATION["state"])
    out.append("  %s" % CONTAMINATION["order_line"])
    out.append("  %s" % CONTAMINATION["note"])
    out.append("")

    out.append("Step 4 search: corpus %s, terms %s"
               % (SEARCH_STATUS["corpus"], SEARCH_STATUS["terms"]))
    out.append("  order line: %s" % SEARCH_STATUS["order_line"])
    out.append("  reading   : %s" % SEARCH_STATUS["reading"])
    return "\n".join(out)


def main(argv):
    if "--selftest" in argv:
        sys.stderr.write(
            "audit is a library and a render; the checks live in "
            "terminal-crossing/test_terminal.py -- run "
            "python3 terminal-crossing/test_terminal.py\n")
        return 2
    if "--choices" in argv:
        for c in CHOICES:
            print(c)
        return 0
    print(render())
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
