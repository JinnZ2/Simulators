#!/usr/bin/env python3
"""
SECOND INSTRUMENT -- gap transfer across hosts.

Claim, from HANDOFF.md: an audit gap survives the end of the practice
carrying it and reattaches to a new intervention. TRACK THE GAP, NOT THE
INTERVENTION. This is the TIME DIMENSION of the radials, which measure
one boundary statically.

Prediction, from HANDOFF.md: do not look at the discredited practice --
it is already being fixed -- look at whatever inherited its POPULATION
and its ACCOUNTING HORIZON.

WHAT THIS DOES NOT DO
  There is no efficacy field on any host. Not for the discredited
  practice, not for the successor, not anywhere: no field records whether
  an intervention worked, helped, cured or succeeded, and
  test_boundary.py asserts that over the AST of this file. "Track the
  gap, not the intervention" is a property of the schema here rather than
  an instruction in a docstring -- an instrument holding an efficacy
  column is one somebody will sort by.

  The gap object is the unmeasured quantity and the accounting horizon
  that leaves it unmeasured. A host is a carrier of that gap and nothing
  else is recorded about it.

REACHABLE NEGATIVE
  A successor that MEASURES the gap did not inherit it -- the gap was
  closed, not transferred. `gap_measured` is three-valued so a successor
  nobody checked is not scored as having closed it.

CC0. Stdlib only. Parses under 3.9.
"""

import os
import sys

UNDECLARED = "UNDECLARED"
NOT_EVALUABLE = "NOT_EVALUABLE"

DIRECTIONS = ("PERMISSIVE", "RESTRICTIVE")

CHOICES = {
    9: ("Population inheritance test. Exact identity of the declared "
        "population, OR a declared overlap fraction on the successor at or "
        "above POPULATION_OVERLAP_FLOOR. Default floor 0.50, printed. A "
        "successor declaring neither is UNDECLARED, never NOT_INHERITED."),
    10: ("Horizon inheritance test. Identity of the declared accounting "
         "horizon in the SAME UNIT. A horizon declared in a different unit "
         "is NOT_EVALUABLE, not unequal -- two horizons in different units "
         "are not the same quantity and comparing them is the operation "
         "this instrument exists to catch."),
}

POPULATION_OVERLAP_FLOOR = 0.50


def choices_report():
    out = ["CHOICES -- gap_transfer", ""]
    for k in sorted(CHOICES):
        out.append("[CHOICE %d] %s" % (k, CHOICES[k]))
        out.append("")
    return "\n".join(out)


class RecordRefused(Exception):
    pass


def _absent(v):
    """A field is absent whether it is missing or explicitly UNDECLARED.

    Found by running, not by reading, and it bit twice in one build. In
    radials.r2_measurand_ownership an explicit UNDECLARED was REFUSED as a
    bad rung while a missing key passed. Here the error ran the other way
    and was worse: horizon_inherited compared two UNDECLARED strings, got
    equality, and reported the horizon as INHERITED -- which is how a
    record declaring no horizon at all reached SAME_GAP_BOTH_DIRECTIONS,
    the handoff's own sharpest reading, out of two blanks. One sentinel,
    two encodings, opposite failures; this helper is the single test.
    """
    return v is None or v == UNDECLARED


def _check_host(h):
    for k in h:
        if k in ("efficacy", "effectiveness", "helped", "cured", "success",
                 "improvement", "benefit"):
            raise RecordRefused(
                "host %r carries the field %r. This instrument tracks the "
                "gap, not the intervention; there is no column for how the "
                "intervention went." % (h.get("name"), k))
    d = h.get("direction", UNDECLARED)
    if d != UNDECLARED and d not in DIRECTIONS:
        raise RecordRefused("direction %r is not declared vocabulary"
                            % (d,))


# --------------------------------------------------------------- checks

def population_inherited(prev, nxt, floor=POPULATION_OVERLAP_FLOOR):
    """[CHOICE 9]."""
    a = prev.get("population", UNDECLARED)
    b = nxt.get("population", UNDECLARED)
    ov = nxt.get("population_overlap")
    if (_absent(a) or _absent(b)) and ov is None:
        return {"test": "population", "state": UNDECLARED,
                "inherited": None,
                "why": "neither an identity nor an overlap is declared"}
    if ov is not None:
        return {"test": "population", "state": "VALUE",
                "inherited": ov >= floor, "overlap": ov, "floor": floor,
                "route": "declared_overlap", "choice": 9}
    return {"test": "population", "state": "VALUE", "inherited": a == b,
            "route": "identity", "choice": 9}


def horizon_inherited(prev, nxt):
    """[CHOICE 10]. Units must match or the comparison is NOT_EVALUABLE."""
    ah, au = prev.get("accounting_horizon"), prev.get("horizon_unit")
    bh, bu = nxt.get("accounting_horizon"), nxt.get("horizon_unit")
    if _absent(ah) or _absent(bh):
        return {"test": "horizon", "state": UNDECLARED, "inherited": None,
                "missing": [n for n, v in (("prev.accounting_horizon", ah),
                                           ("next.accounting_horizon", bh))
                            if _absent(v)]}
    if _absent(au) or _absent(bu) or au != bu:
        return {"test": "horizon", "state": NOT_EVALUABLE, "inherited": None,
                "units": (au, bu),
                "why": ("the two horizons are not declared in the same "
                        "unit; they are not the same quantity"),
                "choice": 10}
    return {"test": "horizon", "state": "VALUE", "inherited": ah == bh,
            "horizon": (ah, bh), "unit": au, "choice": 10}


def gap_state(host):
    """Three-valued. A successor that MEASURES the gap closed it rather
    than inheriting it; a successor nobody checked is not scored as
    either."""
    v = host.get("gap_measured", UNDECLARED)
    if _absent(v):
        return {"state": UNDECLARED, "measured": None}
    if v not in (True, False):
        raise RecordRefused("gap_measured %r is not True, False or "
                            "UNDECLARED" % (v,))
    return {"state": "VALUE", "measured": v}


def transfer(prev, nxt, floor=POPULATION_OVERLAP_FLOOR):
    """One consecutive pair of hosts."""
    _check_host(prev)
    _check_host(nxt)
    pop = population_inherited(prev, nxt, floor=floor)
    hor = horizon_inherited(prev, nxt)
    gs = gap_state(nxt)

    if gs["measured"] is True:
        verdict = "GAP_CLOSED_NOT_TRANSFERRED"
    elif pop["state"] != "VALUE" or hor["state"] != "VALUE":
        verdict = NOT_EVALUABLE
    elif pop["inherited"] and hor["inherited"]:
        verdict = "CARRIER"
    elif pop["inherited"] or hor["inherited"]:
        verdict = "PARTIAL_CARRIER"
    else:
        verdict = "NOT_THE_CARRIER"

    partial_on = None
    if verdict == "PARTIAL_CARRIER":
        partial_on = "population" if pop["inherited"] else "horizon"

    da, db = prev.get("direction", UNDECLARED), nxt.get("direction",
                                                        UNDECLARED)
    if _absent(da) or _absent(db):
        flip = {"state": UNDECLARED, "reading": None}
    elif da != db and hor.get("inherited") is True:
        flip = {"state": "VALUE", "reading": "SAME_GAP_BOTH_DIRECTIONS",
                "from": da, "to": db,
                "why": ("the accounting horizon is unchanged and the "
                        "direction reversed: one horizon, two directions")}
    elif da != db:
        flip = {"state": "VALUE", "reading": "DIRECTION_CHANGED",
                "from": da, "to": db,
                "why": ("direction reversed, and the horizon is not shown "
                        "to be the same one")}
    else:
        flip = {"state": "VALUE", "reading": "SAME_DIRECTION",
                "from": da, "to": db}

    return {"from": prev.get("name"), "to": nxt.get("name"),
            "population": pop, "horizon": hor, "gap_in_successor": gs,
            "verdict": verdict, "partial_on": partial_on,
            "direction": flip}


def read(record, floor=POPULATION_OVERLAP_FLOOR):
    hosts = record.get("hosts") or []
    for h in hosts:
        _check_host(h)
    chain = [transfer(hosts[i], hosts[i + 1], floor=floor)
             for i in range(len(hosts) - 1)]
    return {"gap_id": record.get("gap_id"),
            "gap": record.get("gap"),
            "unit_of_the_missing_measurement":
                record.get("unit_of_the_missing_measurement", UNDECLARED),
            "provenance": record.get("provenance", "CONSTRUCTED"),
            "hosts": [h.get("name") for h in hosts],
            "transfers": chain,
            "carried_by": [t["to"] for t in chain if t["verdict"] == "CARRIER"],
            "both_directions": any(
                t["direction"].get("reading") == "SAME_GAP_BOTH_DIRECTIONS"
                for t in chain)}


def locate_carrier(prev, candidates, floor=POPULATION_OVERLAP_FLOOR):
    """The handoff's prediction made operative: given a host whose
    practice ended, return the candidates that inherited BOTH its
    population and its accounting horizon. Ranks nothing -- the
    candidates come back in the order given, with their two test results,
    and there is no score to sort by."""
    out = []
    for c in candidates:
        t = transfer(prev, c, floor=floor)
        out.append({"candidate": c.get("name"), "verdict": t["verdict"],
                    "population": t["population"]["state"],
                    "population_inherited": t["population"].get("inherited"),
                    "horizon": t["horizon"]["state"],
                    "horizon_inherited": t["horizon"].get("inherited")})
    return {"from": prev.get("name"), "candidates": out,
            "carriers": [o["candidate"] for o in out
                         if o["verdict"] == "CARRIER"],
            "ranks_nothing": True}


def radial_link(record):
    """The composition the handoff states: the radials measure one
    boundary statically, this measures the same boundary over time. Where
    a host declares a boundary rung, R2 -- measurand ownership -- is read
    per host, so the transferred quantity and the ownership of it are
    visible on one page. Nothing is combined."""
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    try:
        import radials
    finally:
        sys.path.pop(0)
    out = []
    for h in record.get("hosts") or []:
        r2 = radials.r2_measurand_ownership(h)
        out.append({"host": h.get("name"), "R2_state": r2["state"],
                    "R2_rung": r2.get("rung"), "R2_value": r2.get("value")})
    return {"gap_id": record.get("gap_id"), "per_host_R2": out,
            "note": ("R2 is read per host and never averaged across the "
                     "chain; a gap moving between two boundaries with "
                     "different ownership is two readings, not one")}


# --------------------------------------------------------------- render

def render(records, floor=POPULATION_OVERLAP_FLOOR):
    L = ["GAP TRANSFER ACROSS HOSTS", ""]
    L.append("Track the gap, not the intervention. No host in this schema "
             "carries an efficacy")
    L.append("field; the instrument cannot report how any intervention "
             "went, by construction.")
    L.append("population_overlap_floor=%g [CHOICE 9]" % floor)
    L.append("")
    for rec in records:
        r = read(rec, floor=floor)
        L.append("GAP  %s" % r["gap_id"])
        L.append("  what is unmeasured  %s" % r["gap"])
        L.append("  unit                %s"
                 % r["unit_of_the_missing_measurement"])
        L.append("  provenance          %s" % r["provenance"])
        L.append("  host chain          %s" % " -> ".join(r["hosts"]))
        L.append("")
        for t in r["transfers"]:
            L.append("  %s -> %s" % (t["from"], t["to"]))
            L.append("     population  %-14s inherited=%s"
                     % (t["population"]["state"],
                        t["population"].get("inherited")))
            L.append("     horizon     %-14s inherited=%s"
                     % (t["horizon"]["state"], t["horizon"].get("inherited")))
            L.append("     gap in successor  %s (measured=%s)"
                     % (t["gap_in_successor"]["state"],
                        t["gap_in_successor"]["measured"]))
            L.append("     VERDICT     %s%s"
                     % (t["verdict"],
                        "" if not t["partial_on"]
                        else " (on %s)" % t["partial_on"]))
            d = t["direction"]
            L.append("     direction   %s  %s -> %s"
                     % (d.get("reading") or d["state"], d.get("from"),
                        d.get("to")))
            if d.get("why"):
                L.append("       %s" % d["why"])
            L.append("")
        L.append("  carried by: %s" % (r["carried_by"] or "none"))
        L.append("  same gap running both directions: %s"
                 % r["both_directions"])
        rl = radial_link(rec)
        L.append("  R2 per host (time dimension of the radials):")
        for e in rl["per_host_R2"]:
            L.append("     %-34s %-12s %s"
                     % (e["host"], e["R2_state"], e["R2_rung"]))
        L.append("     %s" % rl["note"])
        L.append("")
    L.append("Every fact in these records is CARRIED from HANDOFF.md or "
             "CONSTRUCTED here, and")
    L.append("checked against nothing. Nothing in this file is a claim "
             "about any treatment,")
    L.append("prescriber, patient or policy.")
    return "\n".join(L)


def main(argv):
    if "--selftest" in argv:
        sys.stderr.write(
            "gap_transfer.py has no selftest. The checks live in "
            "test_boundary.py; run `python3 test_boundary.py`.\n")
        return 2
    if "--choices" in argv:
        print(choices_report())
        return 0
    here = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, here)
    try:
        import gap_cases
    finally:
        sys.path.pop(0)
    print(render(gap_cases.GAPS))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
