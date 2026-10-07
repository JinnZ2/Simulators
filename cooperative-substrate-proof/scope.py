#!/usr/bin/env python3
"""Scope conditions C1-C4, the coding pass the order requires over any
study corpus, called by P1-P5 so the conditions are IN the parts rather
than beside them.

    C1 time-scoped   observation window short vs the coupling-formation rate
    C2 outcome-bound win condition externally imposed
    C3 narrow metric a single scalar
    C4 enclosed      fixed resource set, no exit

The four are CONJUNCTIVE, which is the order's word "jointly": a
competition-dominant observation requires all four. The return is a
domain-of-validity statement and nothing else --

    WITHIN_COMPETITIVE_FRAME  all four hold; the frame covers this
                              observation
    OUTSIDE_FRAME_SCOPE       at least one fails, named; the frame does
                              not cover this observation, which is not
                              the same as the observation being void
    UNDECLARED                at least one condition was not coded,
                              named; never defaulted in either direction

There is no member meaning "the competitive frame is wrong" and none
meaning some other frame is preferable. That is the framing's coverage
/ values cut made structural rather than promised.

Refuses --selftest; checks live in test_proof.py.
"""

import sys

CONDITIONS = ("C1", "C2", "C3", "C4")

GLOSS = {
    "C1": "time-scoped: observation window short vs coupling-formation rate",
    "C2": "outcome-bound: win condition externally imposed",
    "C3": "narrow metric: a single scalar",
    "C4": "enclosed: fixed resource set, no exit",
}

# [CHOICE 1] C1 is the one condition stated as a rate comparison rather
# than as a fact about the study design, so it needs a rule. It holds
# when the observation window is no longer than the time a coupling
# takes to form: within such a window a coupling that would have
# changed the outcome cannot appear, so the window cannot see one. The
# margin is 1.0 -- equality holds. Both quantities must carry the same
# unit; a mismatch is UNDECLARED, not a ratio.
C1_MARGIN = 1.0

UNDECLARED = "UNDECLARED"
WITHIN = "WITHIN_COMPETITIVE_FRAME"
OUTSIDE = "OUTSIDE_FRAME_SCOPE"


class ScopeInputError(ValueError):
    """Raised on a coding whose fields cannot be read at all."""


def c1_time_scoped(window, coupling_time, unit_window=None, unit_coupling=None):
    """Return True / False / None. None is UNDECLARED, never False.

    A missing quantity, a non-positive coupling time, or two quantities
    in different units all return None. Reading a missing window as a
    short one would put every uncoded study inside the frame, which is
    the direction the whole artifact is about.
    """
    if window is None or coupling_time is None:
        return None
    if unit_window is not None and unit_coupling is not None:
        if unit_window != unit_coupling:
            return None
    try:
        w = float(window)
        c = float(coupling_time)
    except (TypeError, ValueError):
        return None
    if c <= 0:
        return None
    return (w / c) <= C1_MARGIN


def _tri(value):
    """Coerce a declared condition to True / False / None."""
    if value is None:
        return None
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        v = value.strip().lower()
        if v in ("yes", "true", "y"):
            return True
        if v in ("no", "false", "n"):
            return False
        if v in ("", "undeclared", "unknown", "not stated"):
            return None
        raise ScopeInputError("unreadable condition value: %r" % (value,))
    raise ScopeInputError("unreadable condition value: %r" % (value,))


def code(coding):
    """Run the C1-C4 pass over one coding dict.

    Recognised keys: C1 (or the pair window / coupling_time), C2, C3, C4.
    Returns a dict carrying the per-condition tri-state, the verdict, and
    the named failing or undeclared conditions. Nothing is inferred from
    a silence.
    """
    if not isinstance(coding, dict):
        raise ScopeInputError("coding must be a dict")
    out = {}
    if "C1" in coding:
        out["C1"] = _tri(coding.get("C1"))
    else:
        out["C1"] = c1_time_scoped(
            coding.get("window"),
            coding.get("coupling_time"),
            coding.get("window_unit"),
            coding.get("coupling_unit"),
        )
    for key in ("C2", "C3", "C4"):
        out[key] = _tri(coding.get(key))

    undeclared = [k for k in CONDITIONS if out[k] is None]
    failed = [k for k in CONDITIONS if out[k] is False]
    if undeclared:
        verdict = UNDECLARED
    elif failed:
        verdict = OUTSIDE
    else:
        verdict = WITHIN
    return {
        "conditions": out,
        "verdict": verdict,
        "undeclared": undeclared,
        "failed": failed,
        "reading": reading(verdict, undeclared, failed),
    }


def reading(verdict, undeclared, failed):
    """One line, stating coverage and nothing else."""
    if verdict == UNDECLARED:
        return ("scope not established: " + ", ".join(undeclared)
                + " not coded. Neither inside nor outside the frame.")
    if verdict == OUTSIDE:
        return ("outside the competitive frame's coverage: "
                + ", ".join(failed) + " does not hold. The frame does not"
                " cover this observation; the observation stands.")
    return ("inside the competitive frame's coverage: C1-C4 all hold.")


def render(codings):
    """Table for a list of (label, coding) pairs."""
    lines = []
    lines.append("SCOPE CONDITIONS C1-C4 (conjunctive)")
    lines.append("")
    for key in CONDITIONS:
        lines.append("  %s  %s" % (key, GLOSS[key]))
    lines.append("")
    lines.append("  [CHOICE 1] C1 holds when window / coupling_time <= %.1f"
                 % C1_MARGIN)
    lines.append("")
    head = "  %-28s %-4s %-4s %-4s %-4s  %s" % (
        "label", "C1", "C2", "C3", "C4", "verdict")
    lines.append(head)
    lines.append("  " + "-" * (len(head) - 2))
    for label, coding in codings:
        r = code(coding)
        cells = []
        for key in CONDITIONS:
            v = r["conditions"][key]
            cells.append("--" if v is None else ("yes" if v else "no"))
        lines.append("  %-28s %-4s %-4s %-4s %-4s  %s"
                     % (label, cells[0], cells[1], cells[2], cells[3],
                        r["verdict"]))
    lines.append("")
    lines.append("  A verdict is a statement about coverage. No frame is")
    lines.append("  ranked here and none is ranked anywhere in this folder.")
    return "\n".join(lines)


DEMO = [
    ("tournament (constructed)", {
        "window": 1.0, "coupling_time": 30.0,
        "window_unit": "day", "coupling_unit": "day",
        "C2": True, "C3": True, "C4": True}),
    ("open field (constructed)", {
        "window": 365.0, "coupling_time": 30.0,
        "window_unit": "day", "coupling_unit": "day",
        "C2": False, "C3": False, "C4": False}),
    ("uncoded study (constructed)", {
        "C2": True, "C3": True}),
]


def main(argv):
    if "--selftest" in argv:
        sys.stderr.write(
            "scope.py does not carry its own checks.\n"
            "Run: python3 test_proof.py\n")
        return 2
    if "--choices" in argv:
        sys.stdout.write("[CHOICE 1] C1 margin = %.1f (scope.py)\n" % C1_MARGIN)
        return 0
    sys.stdout.write(render(DEMO) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
