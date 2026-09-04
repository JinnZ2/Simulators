#!/usr/bin/env python3
"""P5 -- lag declaration check. No fetch. Two parts, per the v2 order:

  5.1  the P1 precondition set is an INPUT CONSTRAINT, consumed before
       the action, not a report produced after it. An action carrying an
       empty precondition set is flagged (P1's own falsifier: no
       published result has one).
  5.2  per action, t_visible / t_scored, with the >= 10 gate:

         t_visible = shortest interval at which this action's failure
                     could become observable
         t_scored  = interval at which the actor is evaluated

The gate does not block; it CONVERTS an undeclared blind spot into a
declared one. The third state is the order's own "silence is not
safety": a variable with no declared t_visible has an UNDEFINED ratio,
not a small one -- you cannot get a null signal from a variable you
never declared, and absence of a failure signal reads as success. So
UNDECLARED is kept apart from DECLARED_UNKNOWN and from TRACKED.

[CHOICE 1] the ratio threshold is 10, the order's number.
Refuses --selftest (checks live in selftest_v2.py).
"""

import json
import sys

THRESHOLD = 10.0                      # [CHOICE 1] the order's ratio

# Anchors from the order, in seconds. The antibiotic case is the order's
# own worst-case delay structure; the same-window case is its opposite.
DECADE_S = 10 * 365.25 * 24 * 3600.0
MONTH_S = 30 * 24 * 3600.0

ANCHORS = [
    {"name": "antibiotic prescribing (per-patient)", "t_visible_s": 5 * DECADE_S,
     "t_scored_s": 6 * MONTH_S, "requires_compliance": False,
     "preconditions": ["susceptibility assay", "prior efficacy trials", "the standing resistance baseline"]},
    {"name": "same-window action (failure visible within the score window)",
     "t_visible_s": MONTH_S, "t_scored_s": 6 * MONTH_S, "requires_compliance": False,
     "preconditions": ["the measured endpoint"]},
    {"name": "undeclared-variable action", "t_visible_s": None,
     "t_scored_s": 6 * MONTH_S, "requires_compliance": True, "preconditions": []},
]

VERDICTS = ("TRACKED", "DECLARED_UNKNOWN", "UNDECLARED")


def ratio(action):
    """t_visible / t_scored, or None when t_visible is not declared. None
    is the absence of a quantity, not a value of it."""
    tv, ts = action.get("t_visible_s"), action.get("t_scored_s")
    if tv is None:
        return None
    if not ts or ts <= 0:
        return None
    return tv / ts


def gate(action, threshold=THRESHOLD):
    """Three states, kept apart. UNDECLARED is the order's 'silence is
    not safety': no declared t_visible means the ratio cannot be formed,
    which is not the same as a ratio below the threshold."""
    r = ratio(action)
    if action.get("t_visible_s") is None:
        return {"verdict": "UNDECLARED", "ratio": None,
                "reason": "t_visible not declared; a null signal cannot come from an undeclared variable"}
    if r is None:
        return {"verdict": "UNDECLARED", "ratio": None, "reason": "t_scored missing or non-positive"}
    if r >= threshold:
        return {"verdict": "DECLARED_UNKNOWN", "ratio": r,
                "reason": "failure interval is >= %g x the score interval; declared, so trackable" % threshold}
    return {"verdict": "TRACKED", "ratio": r, "reason": "failure could be seen within the score window"}


def precondition_constraint(action):
    """5.1: the precondition set constrains the action before it runs. An
    empty set is flagged -- P1's falsifier is a result with an empty
    precondition set, and none is known."""
    pre = action.get("preconditions")
    if pre is None:
        return {"state": "NOT_ENUMERATED", "n": None,
                "note": "the P1 record was not run before the action; 5.1 requires it as input, not as a later report"}
    if len(pre) == 0:
        return {"state": "EMPTY_SET_FLAGGED", "n": 0,
                "note": "an empty precondition set is P1's own falsifier; treat as unenumerated, not as no dependencies"}
    return {"state": "ENUMERATED", "n": len(pre), "note": "%d preconditions declared before the action" % len(pre)}


def compliance_pairing(action):
    """The order's pairing: does the move require anyone's COMPLIANCE to
    work (an arbitrary system, as opposed to a physical one), crossed
    with how long until its failure could be seen. A 2x2 cell, recorded,
    not scored."""
    g = gate(action)
    lag = g["verdict"]
    comp = "compliance_required" if action.get("requires_compliance") else "no_compliance_required"
    return {"compliance": comp, "lag": lag, "cell": (comp, lag)}


def evaluate(action, threshold=THRESHOLD):
    return {"name": action["name"], "gate": gate(action, threshold),
            "precondition": precondition_constraint(action), "compliance": compliance_pairing(action)}


def render(actions=None, threshold=THRESHOLD):
    actions = actions if actions is not None else ANCHORS
    L = ["P5 lag declaration check [CHOICE 1 threshold %g]" % threshold]
    L.append("5.1 precondition set is an input constraint, not a later report")
    L.append("5.2 t_visible / t_scored, >= threshold -> DECLARED_UNKNOWN; no t_visible -> UNDECLARED (not a small ratio)")
    for a in actions:
        e = evaluate(a, threshold)
        r = e["gate"]["ratio"]
        L.append("  %-46s ratio %-10s %-16s preconditions %-16s compliance %s" % (
            e["name"][:46], ("%.1f" % r) if r is not None else "undefined",
            e["gate"]["verdict"], e["precondition"]["state"], e["compliance"]["cell"]))
    L.append("the antibiotic anchor: failure visible at decades, scored at months, ratio >> 10, DECLARED_UNKNOWN")
    L.append("the undeclared-variable action: ratio undefined, UNDECLARED -- the state the order says silence hides")
    return "\n".join(L)


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if "--selftest" in argv:
        print("p5_lag has no selftest; run selftest_v2.py", file=sys.stderr)
        return 2
    if "--json" in argv:
        print(json.dumps([evaluate(a) for a in ANCHORS], indent=1, default=str))
        return 0
    print(render())
    return 0


if __name__ == "__main__":
    sys.exit(main())
