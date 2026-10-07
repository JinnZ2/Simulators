#!/usr/bin/env python3
"""P5 -- lag declaration check. Per action, two clocks:

    t_visible  shortest interval at which THIS system's failure could
               become observable
    t_scored   interval at which the actor is evaluated

    ratio = t_visible / t_scored
    ratio >= 10  [CHOICE 10, the dispatch's ~10]  -> DECLARED_UNKNOWN

The gate does not block the action. It converts an UNDECLARED blind
spot into a DECLARED one: the failure could not be seen inside the
score window, and now that is on the record.

THREE STATES, never two. An action with no declared t_visible has an
UNDEFINED ratio, not a small one: you cannot get a null signal from a
variable you never declared, and a missing failure signal reads as
success. So UNDECLARED is kept apart from both TRACKED and
DECLARED_UNKNOWN. A zero or negative t_scored is likewise UNDECLARED.

MEDICINE, the worst case the dispatch names: trial endpoints are months,
real outcomes decades; antibiotic resistance looked correct per patient
for fifty years. The anchors below are those two sentences as numbers.

C1 COUPLING. scope.C1 (time-scoped) is PRESENT when t_scored is shorter
than the coupling-formation time. An action carrying t_coupling_s gets
its C1 code from scope.c1_from_clocks -- P5's clocks ARE the C1 coder.

Refuses --selftest (checks live in selftest.py).
"""
import json
import sys

import scope

THRESHOLD = 10.0                       # [CHOICE 10]
STATES = ("TRACKED", "DECLARED_UNKNOWN", "UNDECLARED")
YEAR = 365.25 * 24 * 3600.0
MONTH = 30 * 24 * 3600.0
WEEK = 7 * 24 * 3600.0

ANCHORS = [
    {"name": "antibiotic course, scored per patient", "t_visible_s": 50 * YEAR, "t_scored_s": 2 * WEEK,
     "t_coupling_s": 50 * YEAR, "note": "resistance visible at population scale over decades; the patient is scored at course end"},
    {"name": "drug trial, months endpoint, decades outcome", "t_visible_s": 20 * YEAR, "t_scored_s": 6 * MONTH,
     "t_coupling_s": 20 * YEAR, "note": "the dispatch's medicine worst case"},
    {"name": "same-window action", "t_visible_s": 1 * MONTH, "t_scored_s": 6 * MONTH,
     "t_coupling_s": 1 * MONTH, "note": "failure visible inside the score window"},
    {"name": "undeclared t_visible", "t_visible_s": None, "t_scored_s": 6 * MONTH,
     "t_coupling_s": None, "note": "nobody declared when a failure could be seen"},
]


def ratio(action):
    tv, ts = action.get("t_visible_s"), action.get("t_scored_s")
    if tv is None or ts is None or ts <= 0 or tv < 0:
        return None
    return tv / ts


def gate(action, threshold=THRESHOLD):
    r = ratio(action)
    if r is None:
        state = "UNDECLARED"
    elif r >= threshold:
        state = "DECLARED_UNKNOWN"
    else:
        state = "TRACKED"
    return {"name": action.get("name"), "ratio": r, "state": state,
            "C1": scope.c1_from_clocks(action.get("t_scored_s"), action.get("t_coupling_s"))}


def render(results, threshold=THRESHOLD):
    lines = ["P5 lag declaration  [CHOICE 10] threshold %.0f   (gate declares; it does not block)" % threshold,
             "  %-46s %-12s %-17s C1" % ("action", "ratio", "state")]
    for r in results:
        lines.append("  %-46s %-12s %-17s %s" % (r["name"], "undefined" if r["ratio"] is None else "%.1f" % r["ratio"], r["state"], r["C1"]))
    counts = {s: sum(1 for r in results if r["state"] == s) for s in STATES}
    lines.append("  " + "  ".join("%s %d" % (s, counts[s]) for s in STATES))
    lines.append("  UNDECLARED is an absent quantity, not a small ratio; C1 read from t_scored < t_coupling")
    return "\n".join(lines)


def main(argv):
    if "--selftest" in argv:
        sys.stderr.write("p5_lag_declaration.py holds no checks; run python3 selftest.py\n")
        return 2
    if "--actions" in argv:
        with open(argv[argv.index("--actions") + 1]) as f:
            actions = [json.loads(l) for l in f if l.strip()]
    else:
        actions = ANCHORS
        print("actions: ANCHORS (the dispatch's medicine sentences as numbers; no real trial coded)")
    print(render([gate(a) for a in actions]))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
