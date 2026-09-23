#!/usr/bin/env python3
"""P5 -- LAG DECLARATION CHECK. No fetch, no model call.

Per action, two intervals:

    t_visible  the shortest interval at which this action's failure
               could become observable
    t_scored   the interval at which the actor is evaluated

and the order's gate:

    t_visible / t_scored >= 10  ->  DECLARED_UNKNOWN, NOT BLOCKING

The gate does not stop anything. It converts an UNDECLARED blind spot
into a DECLARED one, which is the whole of what it does and the reason
it is worth running: an actor scored on an interval ten times shorter
than the one their failure needs to appear in is being scored on a
quantity that cannot yet carry a failure signal, and a clean score over
that interval is not evidence of anything.

Four verdicts, and the third is the load-bearing one:

    TRACKED           ratio below the gate; the scoring interval can
                      see the failure
    DECLARED_UNKNOWN  ratio at or above the gate; the blind spot is now
                      on the record
    UNDECLARED        t_visible not declared. The ratio is UNDEFINED,
                      never small. You cannot get a null signal out of a
                      variable nobody declared, and the absence of a
                      failure signal from an undeclared variable reads
                      as success. That is the state the antibiotic
                      anchor sat in: per patient, per course, the
                      treatment looked correct for fifty years, because
                      the interval on which resistance becomes visible
                      was not a variable anyone was scored against.
    NOT_EVALUABLE     t_scored absent or non-positive; there is no
                      denominator and so no reading

    python3 p5_lag.py                        # ships the anchors
    python3 p5_lag.py --actions FILE.json

Refuses --selftest; checks live in test_proof.py.
"""

import json
import sys

import scope

# [CHOICE 1] the threshold is 10, the order's own number ("~10"). The
# "~" is not implemented as a band: a band needs two numbers and the
# order gives one, so the gate is a single comparison and is labelled a
# choice rather than a derivation.
THRESHOLD = 10.0

SECOND = 1.0
DAY = 86400.0
YEAR = 365.0 * DAY

TRACKED = "TRACKED"
DECLARED_UNKNOWN = "DECLARED_UNKNOWN"
UNDECLARED = "UNDECLARED"
NOT_EVALUABLE = "NOT_EVALUABLE"


def lag_ratio(t_visible, t_scored):
    """t_visible / t_scored, or None.

    None on an undeclared t_visible, on an absent or non-positive
    t_scored, and on anything unreadable as a number. A t_visible of
    exactly 0.0 is a MEASUREMENT -- the failure is visible immediately
    -- and returns 0.0, which is why the undeclared case must not.
    """
    if t_visible is None or t_scored is None:
        return None
    try:
        v = float(t_visible)
        s = float(t_scored)
    except (TypeError, ValueError):
        return None
    if s <= 0:
        return None
    if v < 0:
        return None
    return v / s


def classify(t_visible, t_scored):
    if t_scored is None:
        return NOT_EVALUABLE
    try:
        s = float(t_scored)
    except (TypeError, ValueError):
        return NOT_EVALUABLE
    if s <= 0:
        return NOT_EVALUABLE
    if t_visible is None:
        return UNDECLARED
    r = lag_ratio(t_visible, t_scored)
    if r is None:
        return NOT_EVALUABLE
    return DECLARED_UNKNOWN if r >= THRESHOLD else TRACKED


def read_action(obj):
    tv = obj.get("t_visible")
    ts = obj.get("t_scored")
    return {
        "action": obj.get("action", "unlabelled"),
        "t_visible": tv,
        "t_scored": ts,
        "unit": obj.get("unit", "s"),
        "ratio": lag_ratio(tv, ts),
        "verdict": classify(tv, ts),
        "note": obj.get("note", ""),
        "scope": obj.get("scope"),
    }


ANCHORS = [
    {"action": "antibiotic course scored per patient",
     "t_visible": 50.0 * YEAR, "t_scored": 10.0 * DAY, "unit": "s",
     "note": ("CARRIED from the order. The order's own worst case: the "
              "treatment looked correct per patient for fifty years.")},
    {"action": "trial endpoint scored at months, outcome at decades",
     "t_visible": 30.0 * YEAR, "t_scored": 180.0 * DAY, "unit": "s",
     "note": "CARRIED from the order."},
    {"action": "compiler regression caught by the test suite",
     "t_visible": 60.0, "t_scored": 600.0, "unit": "s",
     "note": ("CONSTRUCTED. The reachable negative: a failure visible "
              "faster than the scoring interval.")},
    {"action": "deployment scored weekly, failure interval never stated",
     "t_visible": None, "t_scored": 7.0 * DAY, "unit": "s",
     "note": ("CONSTRUCTED. The state the anchor sat in: no t_visible, "
              "so no ratio, so a clean weekly score forever.")},
    {"action": "action with no scoring interval",
     "t_visible": 1.0 * YEAR, "t_scored": None, "unit": "s",
     "note": "CONSTRUCTED. No denominator; no reading."},
]

# Scoring an actor on an imposed interval against a single scalar is
# the shape C1-C4 describe, so the anchors are coded and most land
# WITHIN. That is a coverage statement about the SCORING ARRANGEMENT,
# not a verdict on any actor.
ANCHOR_SCOPE = {
    "window": 1.0, "coupling_time": 1.0,
    "window_unit": "scoring interval", "coupling_unit": "scoring interval",
    "C2": True, "C3": True, "C4": True,
}


def fmt_time(v, unit):
    if v is None:
        return "--"
    if unit != "s":
        return "%g %s" % (v, unit)
    if v >= YEAR:
        return "%.3g yr" % (v / YEAR)
    if v >= DAY:
        return "%.3g d" % (v / DAY)
    return "%.3g s" % v


def render(rows):
    lines = []
    lines.append("P5 LAG DECLARATION CHECK")
    lines.append("")
    lines.append("  [CHOICE 1] gate: t_visible / t_scored >= %.0f" % THRESHOLD)
    lines.append("")
    head = "  %-46s %10s %10s %10s  %s" % (
        "action", "t_visible", "t_scored", "ratio", "verdict")
    lines.append(head)
    lines.append("  " + "-" * (len(head) - 2))
    for r in rows:
        ratio = "--" if r["ratio"] is None else "%.4g" % r["ratio"]
        lines.append("  %-46s %10s %10s %10s  %s" % (
            r["action"][:46], fmt_time(r["t_visible"], r["unit"]),
            fmt_time(r["t_scored"], r["unit"]), ratio, r["verdict"]))
    lines.append("")
    counts = {}
    for r in rows:
        counts[r["verdict"]] = counts.get(r["verdict"], 0) + 1
    lines.append("  " + "  ".join("%s %d" % (k, counts[k])
                                  for k in sorted(counts)))
    lines.append("")
    lines.append("  DECLARED_UNKNOWN does not block. It moves a blind spot")
    lines.append("  from UNDECLARED, where a clean score reads as success,")
    lines.append("  to the record, where it reads as a score taken over an")
    lines.append("  interval that could not have carried the failure.")
    lines.append("")
    sr = scope.code(ANCHOR_SCOPE)
    lines.append("  scope coding of the scoring arrangement (C1-C4): %s"
                 % sr["verdict"])
    lines.append("  %s" % sr["reading"])
    return "\n".join(lines)


def main(argv):
    if "--selftest" in argv:
        sys.stderr.write(
            "p5_lag.py does not carry its own checks.\n"
            "Run: python3 test_proof.py\n")
        return 2
    if "--choices" in argv:
        sys.stdout.write("[CHOICE 1] gate threshold %.1f\n" % THRESHOLD)
        return 0
    raw = ANCHORS
    for i, a in enumerate(argv):
        if a == "--actions" and i + 1 < len(argv):
            with open(argv[i + 1], "r", encoding="utf-8") as fh:
                raw = json.load(fh)
    rows = [read_action(o) for o in raw]
    sys.stdout.write(render(rows) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
