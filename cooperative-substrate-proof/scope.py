#!/usr/bin/env python3
"""scope.py -- the C1-C4 coding pass. Imported by P1..P5; runs standalone.

A competition-dominant observation is ADMISSIBLE as evidence about a
system only when four scope conditions hold JOINTLY:

    C1 time-scoped   window short against the coupling-formation rate
    C2 outcome-bound win condition externally imposed
    C3 narrow metric a single scalar is scored
    C4 enclosed      fixed resource set, no exit

Each condition on a coded case is one of three values. UNCODED is not
ABSENT: a case nobody coded on C3 has not been shown to lack a narrow
metric, and reading it as ABSENT would mark the case OUT_OF_SCOPE on a
silence. So the pass returns three states, never two:

    ADMISSIBLE      all four PRESENT
    OUT_OF_SCOPE    at least one ABSENT   (names which)
    UNDETERMINED    none ABSENT, at least one UNCODED (names which)

[CHOICE 1] C1 is derivable from P5's two clocks: C1 is PRESENT when the
scoring window is shorter than the coupling-formation time. That is the
one condition with an instrument in this folder; C2-C4 are hand codes.

Refuses --selftest (checks live in selftest.py).
"""
import json
import sys

CONDS = ("C1", "C2", "C3", "C4")
GLOSS = {
    "C1": "time-scoped: window short vs coupling-formation rate",
    "C2": "outcome-bound: win condition externally imposed",
    "C3": "narrow metric: single scalar",
    "C4": "enclosed: fixed resource set, no exit",
}
VALUES = ("PRESENT", "ABSENT", "UNCODED")
STATES = ("ADMISSIBLE", "OUT_OF_SCOPE", "UNDETERMINED", "MALFORMED")


def code_case(case):
    """Return {state, absent, uncoded, name}. A case is a dict with a
    `name` and a `conds` dict over C1..C4; a missing key is UNCODED, a
    value outside VALUES makes the case MALFORMED (typed, not raised)."""
    if not isinstance(case, dict):
        return {"state": "MALFORMED", "reason": "case is not a dict", "name": None}
    conds = case.get("conds") or {}
    absent, uncoded, bad = [], [], []
    for c in CONDS:
        v = conds.get(c, "UNCODED")
        if v not in VALUES:
            bad.append("%s=%r" % (c, v))
        elif v == "ABSENT":
            absent.append(c)
        elif v == "UNCODED":
            uncoded.append(c)
    name = case.get("name")
    if bad:
        return {"state": "MALFORMED", "reason": "value outside VALUES: " + ", ".join(bad), "name": name}
    if absent:
        state = "OUT_OF_SCOPE"
    elif uncoded:
        state = "UNDETERMINED"
    else:
        state = "ADMISSIBLE"
    return {"state": state, "absent": absent, "uncoded": uncoded, "name": name}


def c1_from_clocks(t_scored_s, t_coupling_s):
    """[CHOICE 1] C1 from two clocks. PRESENT when the scoring window is
    shorter than the time a coupling takes to form; ABSENT when it is not;
    UNCODED when either clock is undeclared. None is an absent quantity."""
    if t_scored_s is None or t_coupling_s is None:
        return "UNCODED"
    if t_coupling_s <= 0 or t_scored_s <= 0:
        return "UNCODED"
    return "PRESENT" if t_scored_s < t_coupling_s else "ABSENT"


def code_corpus(cases):
    """Coding pass over a list of cases. Counts kept apart per state; a
    zero is printed, never dropped."""
    out = {s: [] for s in STATES}
    for c in cases:
        r = code_case(c)
        out[r["state"]].append(r)
    return out


def render(coded):
    lines = ["scope coding pass  (C1..C4; three values per condition)"]
    for c in CONDS:
        lines.append("  %s  %s" % (c, GLOSS[c]))
    for s in STATES:
        lines.append("%-13s %d" % (s, len(coded[s])))
        for r in coded[s]:
            detail = ""
            if r["state"] == "OUT_OF_SCOPE":
                detail = "absent=" + ",".join(r["absent"])
            elif r["state"] == "UNDETERMINED":
                detail = "uncoded=" + ",".join(r["uncoded"])
            elif r["state"] == "MALFORMED":
                detail = r["reason"]
            lines.append("    %-32s %s" % (r["name"], detail))
    lines.append("[CHOICE 1] C1 derivable from P5 clocks (t_scored < t_coupling); C2-C4 hand codes")
    return "\n".join(lines)


CONSTRUCTED = [
    {"name": "CONSTRUCTED bounded tournament", "conds": {"C1": "PRESENT", "C2": "PRESENT", "C3": "PRESENT", "C4": "PRESENT"}},
    {"name": "CONSTRUCTED open field, exit free", "conds": {"C1": "PRESENT", "C2": "PRESENT", "C3": "PRESENT", "C4": "ABSENT"}},
    {"name": "CONSTRUCTED metric uncoded", "conds": {"C1": "PRESENT", "C2": "PRESENT", "C4": "PRESENT"}},
]


def main(argv):
    if "--selftest" in argv:
        sys.stderr.write("scope.py holds no checks; run python3 selftest.py\n")
        return 2
    if "--cases" in argv:
        path = argv[argv.index("--cases") + 1]
        with open(path) as f:
            cases = [json.loads(l) for l in f if l.strip()]
    else:
        cases = CONSTRUCTED
        print("corpus: CONSTRUCTED (three cases authored in this file; no study coded)")
    print(render(code_corpus(cases)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
