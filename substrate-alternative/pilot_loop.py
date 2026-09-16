#!/usr/bin/env python3
"""pilot_loop -- food distribution coordination on ICS structure.

WHAT THIS IS
    A coordination loop in which the allocation signal is not a
    number attached to a unit of food.  Four channels replace it:

        capacity declarations   who has what, ready when
        need declarations       who needs what, wanted by when
        matching                capacity meets need, logged
        lag tracking            cycles from declaration to arrival

    The substrate is the Incident Command System -- public
    FEMA/NIMS doctrine, already used to move food under a
    declared incident, already carrying a request channel and a
    resource-status vocabulary.

WHAT IS RETURNED
    UNMET(node, resource, quantity, reason) is a FIRST-CLASS
    RETURN TYPE.  It is not an exception, not an error code, not
    a warning, and not a zero.  A loop that can only report what
    it moved is an instrument with one reachable state.  Four
    reasons are declared and all four are reachable; the tests
    assert that, because a reason nobody has seen fire is not
    known to fire.

THE HONEST LIMIT, STATED HERE RATHER THAN AT THE BOTTOM
    1.  A matching rule that hands limited capacity to competing
        needs IS a distribution decision.  A number attached to a
        unit of food is one such rule.  Removing it does not
        remove the decision -- it makes the rule explicit,
        logged, and arguable.  That is the whole of what this
        does, and it is smaller than it sounds.
    2.  ICS is a COMMAND structure.  It coordinates a response
        under a declared incident with a declared commander.  So
        this loop substitutes an allocation rule for one signal
        AND an authority for another.  frame_audit cannot see the
        second substitution: it screens for one vocabulary, and
        the authority assumption is not in that vocabulary.  The
        screen has a blind spot exactly the shape of the
        substrate chosen to fill the hole it screens for.
    3.  No run here is a statement about any actual food system.
        Every scenario is constructed.

CC0.  Standard library only.  Parses under Python 3.9.
"""

import collections
import os
import sys

import frame_audit

# Every line between the CARRIED marker and END CARRIED is
# transcribed from public ICS/NIMS doctrine from memory.  Nothing
# there was retrieved: this environment's network is an allowlist
# and the doctrine hosts are not on it, so each line is CARRIED
# and unverified, in the sense that nobody here opened a source.
#
# --- ICS VOCABULARY, CARRIED --------------------------------------
#   General Staff, four sections:
#       Operations, Planning, Logistics, Finance/Administration
#   Finance/Administration units:
#       Time Unit, Procurement Unit, Compensation/Claims Unit,
#       Cost Unit
#   ICS-213RR   Resource Request Message
#   ICS-211     Check-In List
#   ICS-204     Assignment List
#   ICS-215     Operational Planning Worksheet
#   Resource status:  ASSIGNED / AVAILABLE / OUT-OF-SERVICE
#   Span of control:  3 to 7, 5 typical
#   Work is planned in operational periods (the Planning P)
# --- END CARRIED --------------------------------------------------

# THE FINDING IS THAT THE BLOCK ABOVE FIRES THE SCREEN, and that
# every token in it which fires is a section or a unit that ICS
# itself names.  One of the four General Staff sections, and
# three of its four units, are the part of the structure this
# loop has no channel for.  A pilot that borrows ICS as a
# substrate has therefore dropped or repurposed a quarter of what
# it borrowed, and the doctrine's vocabulary says so before any
# of ours does.  Recorded, not smoothed.
#
# ONE EXEMPTION, AND IT WAS EXPECTED TO BE TWO.  A second region
# was reserved for the docstring, on the reasoning that a module
# cannot say which signal it removed without naming it, and no
# word screen separates use from mention.  The region turned out
# to be unnecessary: the docstring was written without the
# vocabulary, so the anticipated hits did not occur and the
# region was deleted rather than kept empty.  That is a small
# result against the reasoning, and it is recorded here because
# an unfired exemption left in place reads as a hit that was
# forgiven.  The surviving exemption is measured in three arms in
# test_substrate.py: masked, the file is clean; unmasked, the
# carried block is the only thing that fires; and a planted token
# inside the region is still caught.

EXEMPT_REGIONS = (
    ("--- ICS VOCABULARY, CARRIED", "--- END CARRIED",
     "section and unit names transcribed from public ICS "
     "doctrine; that they fire is the finding"),
)

UNMET_REASONS = (
    "NO_CAPACITY_DECLARED",
    "CAPACITY_EXHAUSTED",
    "UNREACHABLE",
    "ARRIVES_AFTER_HORIZON",
)

CHOICES = {
    1: "UNMET carries `resource` in addition to the three fields "
       "asked for (node, quantity, reason), because a node may "
       "need two resources and a bare quantity would not say "
       "which one went unfilled.",
    2: "Needs are served in order of (horizon_cycle, node_id, "
       "resource) -- earliest deadline first, ties broken by id.  "
       "Deterministic and declared.  This ordering IS the "
       "allocation rule; it is ours, not ICS's.  ICS specifies a "
       "request channel (ICS-213RR) and an assignment authority.  "
       "It does not specify who wins when two requests meet one "
       "pallet.",
    3: "Within a need, the nearest eligible capacity is drawn "
       "first, ties broken by node id.  Nearest, not largest and "
       "not fullest: the quantity this loop reports is lag, so "
       "the rule minimises the quantity it reports.  A different "
       "rule (drain the largest holder first, to keep small "
       "holders in reserve) is defensible and would give a "
       "different log.",
    4: "A route is directional and is looked up as (from, to).  "
       "With symmetric=True (the default) the reverse pair is "
       "accepted as a fallback.  An ABSENT pair is UNREACHABLE.  "
       "It is never a large number and never zero -- both would "
       "put an undeclared route on the same scale as a declared "
       "one.",
    5: "Arrival is max(ready_cycle, declared_cycle) + travel.  "
       "Capacity that is not ready yet delays the arrival rather "
       "than being silently available.",
    6: "Lag is arrival_cycle - declared_cycle: cycles from the "
       "need being declared to the food being there.  Not from "
       "departure, and not from the start of the run.",
    7: "Per-node readouts are a list of lags plus a max and a "
       "min.  Nothing is summed across nodes and nothing is "
       "ranked.  One number per node would be a standing for the "
       "node, which is a second allocation signal arriving "
       "through the readout.",
}

Node = collections.namedtuple("Node", "node_id label")
Capacity = collections.namedtuple(
    "Capacity", "node_id resource quantity ready_cycle")
Need = collections.namedtuple(
    "Need", "node_id resource quantity declared_cycle horizon_cycle")
ALLOCATED = collections.namedtuple(
    "ALLOCATED",
    "from_node to_node resource quantity depart_cycle "
    "arrival_cycle lag")
UNMET = collections.namedtuple(
    "UNMET", "node resource quantity reason")


class ScenarioError(Exception):
    """A scenario that cannot be read is not silently repaired."""


def travel(routes, a, b, symmetric=True):
    """Cycles from a to b, or None when no route is declared.

    None is the third state.  [CHOICE 4]"""
    if a == b:
        return 0
    if (a, b) in routes:
        return routes[(a, b)]
    if symmetric and (b, a) in routes:
        return routes[(b, a)]
    return None


def _check(scenario):
    ids = set()
    for node in scenario["nodes"]:
        if node.node_id in ids:
            raise ScenarioError("duplicate node id %r" % node.node_id)
        ids.add(node.node_id)
    for cap in scenario["capacities"]:
        if cap.node_id not in ids:
            raise ScenarioError("capacity at undeclared node %r"
                                % cap.node_id)
        if cap.quantity <= 0:
            raise ScenarioError("capacity quantity must be positive")
    for need in scenario["needs"]:
        if need.node_id not in ids:
            raise ScenarioError("need at undeclared node %r"
                                % need.node_id)
        if need.quantity <= 0:
            raise ScenarioError("need quantity must be positive")
        if need.horizon_cycle < need.declared_cycle:
            raise ScenarioError("horizon before declaration at %r"
                                % need.node_id)
    for (a, b) in scenario["routes"]:
        if a not in ids or b not in ids:
            raise ScenarioError("route over undeclared node: %r"
                                % ((a, b),))


def _reason(resource, declared_total, pool, need, routes, symmetric):
    """Why the remainder of one need could not be filled."""
    if declared_total == 0:
        return "NO_CAPACITY_DECLARED"
    remaining = [c for c in pool
                 if c["resource"] == resource and c["left"] > 0]
    if not remaining:
        return "CAPACITY_EXHAUSTED"
    routed = []
    for cap in remaining:
        cycles = travel(routes, cap["node_id"], need.node_id, symmetric)
        if cycles is not None:
            routed.append((cap, cycles))
    if not routed:
        return "UNREACHABLE"
    for cap, cycles in routed:
        depart = max(cap["ready_cycle"], need.declared_cycle)
        if depart + cycles <= need.horizon_cycle:
            # Would have been drawn.  Unreachable state; the loop
            # below runs until no eligible capacity is left.
            raise AssertionError(
                "eligible capacity left unallocated -- matcher bug")
    return "ARRIVES_AFTER_HORIZON"


def run(scenario):
    """Match declared capacity to declared need.  Log everything."""
    _check(scenario)
    symmetric = scenario.get("symmetric_routes", True)
    routes = scenario["routes"]
    pool = [dict(node_id=c.node_id, resource=c.resource,
                 left=c.quantity, ready_cycle=c.ready_cycle)
            for c in scenario["capacities"]]
    declared_total = collections.Counter()
    for cap in scenario["capacities"]:
        declared_total[cap.resource] += cap.quantity

    needs = sorted(scenario["needs"],
                   key=lambda n: (n.horizon_cycle, n.node_id,
                                  n.resource))  # [CHOICE 2]
    allocations = []
    unmet = []
    for need in needs:
        left = need.quantity
        while left > 0:
            pick = None
            for cap in pool:
                if cap["resource"] != need.resource or cap["left"] <= 0:
                    continue
                cycles = travel(routes, cap["node_id"], need.node_id,
                                symmetric)
                if cycles is None:
                    continue
                depart = max(cap["ready_cycle"], need.declared_cycle)
                if depart + cycles > need.horizon_cycle:
                    continue
                key = (cycles, cap["node_id"])  # [CHOICE 3]
                if pick is None or key < pick[0]:
                    pick = (key, cap, cycles, depart)
            if pick is None:
                break
            _, cap, cycles, depart = pick
            moved = min(left, cap["left"])
            cap["left"] -= moved
            left -= moved
            arrival = depart + cycles  # [CHOICE 5]
            allocations.append(ALLOCATED(
                from_node=cap["node_id"],
                to_node=need.node_id,
                resource=need.resource,
                quantity=moved,
                depart_cycle=depart,
                arrival_cycle=arrival,
                lag=arrival - need.declared_cycle))  # [CHOICE 6]
        if left > 0:
            unmet.append(UNMET(  # [CHOICE 1]
                node=need.node_id,
                resource=need.resource,
                quantity=left,
                reason=_reason(need.resource,
                               declared_total[need.resource],
                               pool, need, routes, symmetric)))
    return {
        "allocations": allocations,
        "unmet": unmet,
        "per_node": per_node(scenario, allocations, unmet),
        "capacity_left": [(c["node_id"], c["resource"], c["left"])
                          for c in pool if c["left"] > 0],
        "unmet_reasons": UNMET_REASONS,
        "choices": sorted(CHOICES),
    }


def per_node(scenario, allocations, unmet):
    """Per node, per resource.  No composite.  [CHOICE 7]"""
    out = collections.OrderedDict()
    for need in sorted(scenario["needs"],
                       key=lambda n: (n.node_id, n.resource)):
        row = out.setdefault(need.node_id, collections.OrderedDict())
        cell = row.setdefault(need.resource, {
            "needed": 0, "met": 0, "unfilled": 0,
            "lags": [], "max_lag": None, "min_lag": None})
        cell["needed"] += need.quantity
    for alloc in allocations:
        cell = out[alloc.to_node][alloc.resource]
        cell["met"] += alloc.quantity
        cell["lags"].append(alloc.lag)
    for item in unmet:
        out[item.node][item.resource]["unfilled"] += item.quantity
    for node_id in out:
        for resource in out[node_id]:
            cell = out[node_id][resource]
            if cell["lags"]:
                cell["max_lag"] = max(cell["lags"])
                cell["min_lag"] = min(cell["lags"])
            # no allocations -> max_lag stays None.  Absent, not 0.
    return out


# ---- the screen --------------------------------------------------

def _norm(line):
    return line.strip().lstrip("#").strip()


def _regions(lines):
    """[(first_line, last_line, reason)] for the exempt regions."""
    found = []
    for start, end, reason in EXEMPT_REGIONS:
        a = b = None
        for i, line in enumerate(lines):
            if a is None and _norm(line).startswith(_norm(start)):
                a = i
            elif (a is not None and b is None
                  and _norm(line).startswith(_norm(end))):
                b = i
                break
        if a is None or b is None:
            raise ScenarioError(
                "exempt region marker not found: %r" % start)
        found.append((a, b, reason))
    return found


def screen(text, exempt_regions=()):
    """Run frame_audit over text, splitting hits by region.

    exempt_regions is [(first_line, last_line, reason)].  A hit
    outside every region is UNEXEMPTED and is the flag."""
    result = frame_audit.audit(text)
    offsets = [0]
    for line in text.split("\n"):
        offsets.append(offsets[-1] + len(line) + 1)
    inside = []
    outside = []
    for hit in result["hits"]:
        line_no = 0
        for i in range(len(offsets) - 1):
            if offsets[i] <= hit.char_start < offsets[i + 1]:
                line_no = i
                break
        placed = None
        for a, b, reason in exempt_regions:
            if a <= line_no <= b:
                placed = reason
                break
        if placed is None:
            outside.append((line_no + 1, hit))
        else:
            inside.append((line_no + 1, hit, placed))
    return {
        "exempted": inside,
        "unexempted": outside,
        "flagged": bool(outside),
        "counts": result["counts"],
    }


def screen_self(path=None):
    """Screen the source of this module."""
    path = path or os.path.abspath(__file__)
    with open(path) as handle:
        text = handle.read()
    return screen(text, _regions(text.split("\n")))


def screen_output(text):
    """Screen a rendered run.  No exemptions apply to output."""
    return screen(text, ())


# ---- a constructed scenario --------------------------------------

DEMO = {
    "nodes": [
        Node("depot_north", "holds pallets, ready at cycle 0"),
        Node("depot_south", "holds pallets, ready at cycle 2"),
        Node("kitchen_a", "needs staples by cycle 3"),
        Node("kitchen_b", "needs staples by cycle 2"),
        Node("kitchen_c", "needs staples, no route declared"),
        Node("kitchen_d", "needs produce, none declared anywhere"),
    ],
    "capacities": [
        Capacity("depot_north", "staples", 40, 0),
        Capacity("depot_south", "staples", 25, 2),
    ],
    "needs": [
        Need("kitchen_a", "staples", 30, 0, 3),
        Need("kitchen_b", "staples", 20, 0, 2),
        Need("kitchen_c", "staples", 10, 0, 5),
        Need("kitchen_d", "produce", 15, 0, 5),
    ],
    "routes": {
        ("depot_north", "kitchen_a"): 1,
        ("depot_north", "kitchen_b"): 2,
        ("depot_south", "kitchen_a"): 1,
        ("depot_south", "kitchen_b"): 3,
    },
    "symmetric_routes": True,
}


def render(result):
    lines = []
    lines.append("PILOT LOOP -- allocation log")
    lines.append("=" * 62)
    lines.append("")
    lines.append("MATCHED  from            to             res      "
                 "qty  dep  arr  lag")
    if not result["allocations"]:
        lines.append("  none")
    for a in result["allocations"]:
        lines.append("  %-15s %-14s %-8s %4d %4d %4d %4d" % (
            a.from_node, a.to_node, a.resource, a.quantity,
            a.depart_cycle, a.arrival_cycle, a.lag))
    lines.append("")
    lines.append("UNMET  (a return type, not a failure)")
    if not result["unmet"]:
        lines.append("  none.  Every declared need was filled from "
                     "declared capacity.")
    for u in result["unmet"]:
        lines.append("  %-15s %-8s %4d   %s"
                     % (u.node, u.resource, u.quantity, u.reason))
    lines.append("")
    lines.append("PER NODE  (no total, no ranking)")
    per = result["per_node"]
    for node_id in per:
        for resource in per[node_id]:
            cell = per[node_id][resource]
            lags = ",".join(str(x) for x in cell["lags"]) or "-"
            lines.append("  %-15s %-8s needed %3d  met %3d  "
                         "unfilled %3d  lags [%s]  max %s"
                         % (node_id, resource, cell["needed"],
                            cell["met"], cell["unfilled"], lags,
                            "-" if cell["max_lag"] is None
                            else cell["max_lag"]))
    lines.append("")
    lines.append("CAPACITY LEFT")
    if not result["capacity_left"]:
        lines.append("  none")
    for node_id, resource, left in result["capacity_left"]:
        lines.append("  %-15s %-8s %4d" % (node_id, resource, left))
    return "\n".join(lines)


def choices_report():
    out = ["pilot_loop [CHOICE n]"]
    for n in sorted(CHOICES):
        out.append("  [CHOICE %d] %s" % (n, CHOICES[n]))
    return "\n".join(out)


def screen_report():
    src = screen_self()
    lines = ["SCREEN -- pilot_loop.py source"]
    lines.append("=" * 62)
    lines.append("unexempted hits : %d   FLAGGED: %s"
                 % (len(src["unexempted"]), src["flagged"]))
    for line_no, hit in src["unexempted"]:
        lines.append("  line %-5d %-18s %r"
                     % (line_no, hit.frame, hit.surface))
    lines.append("exempted hits   : %d" % len(src["exempted"]))
    seen = collections.OrderedDict()
    for line_no, hit, reason in src["exempted"]:
        seen.setdefault(reason, []).append(hit.entry)
    for reason in seen:
        lines.append("  region: %s" % reason)
        lines.append("    %s" % ", ".join(sorted(set(seen[reason]))))
    out = screen_output(render(run(DEMO)))
    lines.append("")
    lines.append("SCREEN -- rendered run (no exemptions apply)")
    lines.append("unexempted hits : %d   FLAGGED: %s"
                 % (len(out["unexempted"]), out["flagged"]))
    for line_no, hit in out["unexempted"]:
        lines.append("  line %-5d %-18s %r"
                     % (line_no, hit.frame, hit.surface))
    return "\n".join(lines)


USAGE = """usage: python3 pilot_loop.py --demo
       python3 pilot_loop.py --screen
       python3 pilot_loop.py --choices
"""


def main(argv):
    args = list(argv[1:])
    if "--selftest" in args:
        sys.stderr.write(
            "pilot_loop.py carries no selftest.\n"
            "Run: python3 test_substrate.py\n")
        return 2
    if not args or args[0] in ("-h", "--help"):
        sys.stdout.write(USAGE)
        return 0
    if args[0] == "--choices":
        print(choices_report())
        return 0
    if args[0] == "--screen":
        print(screen_report())
        return 0
    if args[0] == "--demo":
        print(render(run(DEMO)))
        return 0
    sys.stdout.write(USAGE)
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
