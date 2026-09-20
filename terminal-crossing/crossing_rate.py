#!/usr/bin/env python3
"""
crossing_rate -- WO-3 step 2: the crossing-rate metric.

The order's useful conversion is the whole of this module: "Not 'is it
terminal' but WHAT IS THE CROSSING RATE, AND OVER WHAT HORIZON." A
binary with no instances is converted into a quantity with a scale.

The six falsifier conditions are PARSED out of WORK_ORDER.md at call
time and are never retyped here. Channel ids are derived mechanically
from the order's own bullets -- the first word after "no " -- so a
condition edited in the order moves the metric rather than leaving a
copy behind. Five stale copies of one gate across three drops is what
retyping costs in this tree (MF_019).

Three states per channel, not two. PRESENT and ABSENT_MEASURED are
measurements; UNSEARCHED is a silence. A channel nobody declared is
UNSEARCHED, so a system with an undeclared channel returns
NOT_ESTABLISHED and can never return TERMINAL by omission.

WHAT THIS IS NOT. Every rate in SYSTEMS is CONSTRUCTED. No repository,
no spacecraft and no black hole is measured here, and nothing in the
output is a statement about one. What the module establishes is that
the metric discriminates between the order's three asymptotes and that
its TERMINAL branch is reachable on a control -- reachability of a
verdict is not the existence of a system that earns it.

CC0. stdlib only. Parses under Python 3.9. ASCII.
"""

import collections
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ORDER = os.path.join(HERE, "WORK_ORDER.md")

CHOICES = [
    "[CHOICE 1] an undeclared channel is UNSEARCHED, never ABSENT_MEASURED "
    "-- a silence and a measured absence are different states",
    "[CHOICE 2] channel ids are derived mechanically from the order's own "
    "bullets (the first word after \"no \"), not assigned in this module",
    "[CHOICE 3] a horizon carries a value and a unit, or the token "
    "UNBOUNDED; a rate whose unit is outside the declared table returns "
    "UNIT_UNKNOWN rather than a silently converted number",
    "[CHOICE 4] a PRESENT channel with no declared rate contributes its "
    "completed count only; its rate stays None rather than defaulting to 0",
]

CHANNEL_STATES = ("PRESENT", "ABSENT_MEASURED", "UNSEARCHED")

# Declared unit table. A rate or horizon unit outside it is not converted.
SECONDS = {"second": 1.0, "day": 86400.0, "year": 31556952.0}
RATE_BASE = {"per_second": "second", "per_day": "day", "per_year": "year"}
UNBOUNDED = "UNBOUNDED"

TOTAL_STATES = (
    "COMPUTED",
    "UNBOUNDED_HORIZON",
    "NOT_ESTABLISHED",
    "UNIT_UNKNOWN",
)


# ---------------------------------------------------------------- parsing

_BULLET = re.compile(r"^-\s+no\s+([A-Za-z]+)")


def conditions(path=ORDER):
    """The order's falsifier conditions, parsed. [(channel_id, bullet)]."""
    with open(path, "rb") as fh:
        text = fh.read().decode("utf-8")
    lines = text.splitlines()
    start = None
    for i, line in enumerate(lines):
        if line.startswith("### Conditions"):
            start = i + 1
            break
    if start is None:
        raise ValueError("conditions section not located in %s" % path)
    out = []
    for line in lines[start:]:
        if line.startswith("#"):
            break
        m = _BULLET.match(line.strip())
        if m:
            out.append((m.group(1).lower(), line.strip()))
    if not out:
        raise ValueError("no conditions parsed from %s" % path)
    return out


def channel_ids(path=ORDER):
    return [c for c, _ in conditions(path)]


# ---------------------------------------------------------------- records

Channel = collections.namedtuple(
    "Channel", "channel state completed rate rate_unit basis")

System = collections.namedtuple(
    "System", "name horizon_value horizon_unit channels note")


def channel(cid, state, completed=0, rate=None, rate_unit=None, basis=""):
    if state not in CHANNEL_STATES:
        raise ValueError("state outside the declared set: %r" % (state,))
    return Channel(cid, state, completed, rate, rate_unit, basis)


def system(name, horizon_value, horizon_unit, decls, note=""):
    """Undeclared channels are filled as UNSEARCHED. [CHOICE 1]"""
    by_id = {}
    for ch in decls:
        by_id[ch.channel] = ch
    filled = collections.OrderedDict()
    for cid in channel_ids():
        if cid in by_id:
            filled[cid] = by_id[cid]
        else:
            filled[cid] = channel(cid, "UNSEARCHED", basis="not declared")
    for cid in by_id:
        if cid not in filled:
            raise ValueError("channel outside the order's conditions: %r" % cid)
    return System(name, horizon_value, horizon_unit, filled, note)


# ---------------------------------------------------------------- metric

def expected_crossings(rate, rate_unit, horizon_value, horizon_unit):
    """Expected crossings over the horizon, or None where not computable.

    None is returned for an absent rate, an unknown rate unit, an
    unbounded or absent horizon, and an unknown horizon unit. A rate
    MEASURED at zero returns 0.0, which is a different reading from
    None and is why the two are kept apart. [CHOICE 3][CHOICE 4]
    """
    if rate is None:
        return None
    if rate_unit not in RATE_BASE:
        return None
    if horizon_value is None or horizon_unit not in SECONDS:
        return None
    base = SECONDS[RATE_BASE[rate_unit]]
    return rate * (horizon_value * SECONDS[horizon_unit] / base)


def crossing_total(sysrec):
    """(state, value). value is None on every state but COMPUTED."""
    if any(c.state == "UNSEARCHED" for c in sysrec.channels.values()):
        return ("NOT_ESTABLISHED", None)
    if sysrec.horizon_unit == UNBOUNDED or sysrec.horizon_value is None:
        return ("UNBOUNDED_HORIZON", None)
    if sysrec.horizon_unit not in SECONDS:
        return ("UNIT_UNKNOWN", None)
    total = 0.0
    for c in sysrec.channels.values():
        if c.state != "PRESENT":
            continue
        total += float(c.completed)
        if c.rate is None:
            continue
        if c.rate_unit not in RATE_BASE:
            return ("UNIT_UNKNOWN", None)
        total += expected_crossings(
            c.rate, c.rate_unit, sysrec.horizon_value, sysrec.horizon_unit)
    return ("COMPUTED", total)


def verdict(sysrec):
    """TERMINAL / NOT_TERMINAL / NOT_ESTABLISHED."""
    states = [c.state for c in sysrec.channels.values()]
    if "PRESENT" in states:
        return "NOT_TERMINAL"
    if "UNSEARCHED" in states:
        return "NOT_ESTABLISHED"
    return "TERMINAL"


def shape(sysrec):
    """The arithmetic shape of the reading, for the step 2 discrimination."""
    state, value = crossing_total(sysrec)
    if state != "COMPUTED":
        return (state, None, None)
    completed = any(c.state == "PRESENT" and c.completed
                    for c in sysrec.channels.values())
    rated = any(c.state == "PRESENT" and c.rate is not None
                for c in sysrec.channels.values())
    return ("COMPUTED", completed, rated)


def discriminates(records):
    """Do the given systems return distinct arithmetic shapes?"""
    shapes = [shape(r) for r in records]
    return len(set(shapes)) == len(shapes)


# ------------------------------------------------------- constructed corpus

def _asymptotes():
    """The order's three closest candidates. Every rate CONSTRUCTED."""
    sealed = system(
        "sealed_repository", 1.0e4, "year",
        [channel("physical", "PRESENT", 0, 1.0e-6, "per_year",
                 "CONSTRUCTED leakage rate; the order states a rate, not a value"),
         channel("operator", "ABSENT_MEASURED", basis="after closure"),
         channel("shared", "ABSENT_MEASURED", basis="geological isolation"),
         channel("maintenance", "PRESENT", 1, basis="emplacement and closure"),
         channel("supply", "PRESENT", 1, basis="components arrived"),
         channel("disposal", "PRESENT", 1, basis="emplacement is the exit path")],
        "the order: a designed containment period and a leakage RATE")
    voyager = system(
        "voyager_post_transmission", None, UNBOUNDED,
        [channel("physical", "PRESENT", 1, basis="the craft left"),
         channel("operator", "ABSENT_MEASURED", basis="transmission ceased"),
         channel("shared", "ABSENT_MEASURED", basis="no shared bench"),
         channel("maintenance", "ABSENT_MEASURED", basis="unreachable"),
         channel("supply", "PRESENT", 1, basis="components arrived"),
         channel("disposal", "PRESENT", 1, basis="the trajectory is the exit")],
        "the order: horizon is the lifetime of the object, not decades")
    hole = system(
        "black_hole_interior", 1.0e6, "year",
        [channel("physical", "ABSENT_MEASURED", basis="past the horizon"),
         channel("operator", "ABSENT_MEASURED", basis="no operator"),
         channel("shared", "PRESENT", 0, 1.0e-6, "per_year",
                 "CONSTRUCTED Hawking rate; horizon truncated, also CONSTRUCTED"),
         channel("maintenance", "ABSENT_MEASURED", basis="no maintenance"),
         channel("supply", "ABSENT_MEASURED",
                 basis="declared reading: infall is outside the drawn boundary"),
         channel("disposal", "ABSENT_MEASURED", basis="no disposal path")],
        "the order: emits Hawking radiation eventually")
    return [sealed, voyager, hole]


def _control_terminal():
    """All six ABSENT_MEASURED. Shows the TERMINAL branch is reachable.

    CONSTRUCTED. Reachability of a verdict is not a claim that a system
    earning it exists; the order reports no instance and this control
    does not supply one.
    """
    return system(
        "control_all_absent", 1.0, "year",
        [channel(cid, "ABSENT_MEASURED", basis="CONSTRUCTED control")
         for cid in channel_ids()],
        "reachability control, not an instance")


def _control_undeclared():
    """Three channels declared, three left out. CONSTRUCTED."""
    return system(
        "control_partly_declared", 1.0, "year",
        [channel("physical", "ABSENT_MEASURED", basis="CONSTRUCTED control"),
         channel("operator", "ABSENT_MEASURED", basis="CONSTRUCTED control"),
         channel("shared", "ABSENT_MEASURED", basis="CONSTRUCTED control")],
        "three channels undeclared; UNSEARCHED is not ABSENT_MEASURED")


SYSTEMS = None


def corpus():
    global SYSTEMS
    if SYSTEMS is None:
        SYSTEMS = _asymptotes() + [_control_terminal(), _control_undeclared()]
    return SYSTEMS


# ---------------------------------------------------------------- render

def _fmt(value):
    if value is None:
        return "--"
    return "%.6f" % value


def render():
    out = []
    out.append("WO-3 CROSSING RATE -- the falsifier as a quantity")
    out.append("CONSTRUCTED rates. No repository, spacecraft or black hole "
               "is measured.")
    out.append("")
    for c in CHOICES:
        out.append(c)
    out.append("")

    conds = conditions()
    out.append("Falsifier conditions, parsed from WORK_ORDER.md (%d):" % len(conds))
    for cid, bullet in conds:
        out.append("  %-12s | %s" % (cid, bullet))
    out.append("")

    out.append("Channel states: %s" % ", ".join(CHANNEL_STATES))
    out.append("  an undeclared channel is UNSEARCHED, so a system carrying one")
    out.append("  returns NOT_ESTABLISHED and never TERMINAL by omission.")
    out.append("")

    out.append("Readings:")
    out.append("  %-26s %-16s %-18s %s"
               % ("system", "verdict", "total state", "expected crossings"))
    for rec in corpus():
        state, value = crossing_total(rec)
        out.append("  %-26s %-16s %-18s %s"
                   % (rec.name, verdict(rec), state, _fmt(value)))
    out.append("")

    asym = _asymptotes()
    out.append("Step 2 discrimination, on the order's three asymptotes:")
    for rec in asym:
        out.append("  %-26s shape=%s" % (rec.name, shape(rec)))
    out.append("  distinct shapes: %s" % discriminates(asym))
    zeros = [r.name for r in asym if crossing_total(r)[1] == 0.0]
    out.append("  asymptotes returning a total of zero: %d %s"
               % (len(zeros), zeros if zeros else ""))
    out.append("")

    out.append("Horizon carried per system:")
    for rec in corpus():
        if rec.horizon_unit == UNBOUNDED:
            h = UNBOUNDED
        else:
            h = "%g %s" % (rec.horizon_value, rec.horizon_unit)
        out.append("  %-26s %s" % (rec.name, h))
    return "\n".join(out)


def main(argv):
    if "--selftest" in argv:
        sys.stderr.write(
            "crossing_rate is a library and a render; the checks live in "
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
