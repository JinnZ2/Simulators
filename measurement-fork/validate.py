#!/usr/bin/env python3
"""
validate.py -- is the spec complete enough to fork on?

CC0-1.0. stdlib only.

Reconstructed from compare.py's call site:

    qs = validate.check(spec)
    if qs:  print("SPEC INCOMPLETE -- run validate.py first"); ...

so `check` returns a list of questions and an empty list means go. Fails
closed: an underspecified system produces no fork, because the fork's whole
output is a comparison and there is nothing to compare arms on.

The questions are questions, not error messages. A missing field here is
usually not an oversight -- it is a part of the design nobody has decided
yet, and the useful output is the decision that is still open.
"""

from __future__ import annotations

import json
import sys

REQUIRED = {
    "system_id": "What is this system called? One token, used to name the run.",
    "description": "One sentence: what is being measured, and about what?",
    "open_questions": (
        "What do you actually want to know? These drive the RESIDUAL cell, "
        "which is the point of the exercise -- with none declared, the fork "
        "can tell you what each arm reaches but not what nothing reaches."),
}

EXPECTED = {
    "currently_measured": (
        "What does the standard design measure today? Each entry becomes a "
        "conventional probe. Empty means the conventional arm has almost "
        "nothing to generate, which is worth knowing but is rarely true."),
    "provisioned": (
        "What does the environment provide, and on whose schedule? Each "
        "entry becomes a latency and a contingency-consistency probe. "
        "Without it the coupling arm cannot reach the loop-closing "
        "quantities at all."),
    "regime": (
        "What varies, and over what range? Needs {\"variable\": ..., "
        "\"range\": ...}. Drives the endpoint probe and the environment's "
        "own autocorrelation."),
    "boundary": (
        "Where does the organism end and the environment begin? Consequence "
        "delivery crosses this line, and which side a quantity sits on is "
        "the object_of field the whole comparator keys on."),
    "actors": (
        "Who is in the loop? A provisioning agent between organism and "
        "environment is a third actor, and quantities about it belong to "
        "neither of the other two."),
    "test_items_source": (
        "Where do the test items come from? If items are drawn from one "
        "side only, domain mismatch is scored as deficit and no arm can "
        "tell the difference without this being declared."),
}


def check(spec):
    """Returns a list of open questions. Empty list means the spec will fork."""
    questions = []

    for field, ask in REQUIRED.items():
        val = spec.get(field)
        if not val:
            questions.append("[required] %s -- %s" % (field, ask))

    for field, ask in EXPECTED.items():
        if field not in spec:
            questions.append("[expected] %s -- %s" % (field, ask))

    reg = spec.get("regime")
    if reg and not (isinstance(reg, dict)
                    and reg.get("variable") and reg.get("range")):
        questions.append(
            "[malformed] regime -- needs both 'variable' and 'range'. "
            "A regime with a variable and no range cannot be swept; a range "
            "with no variable does not say what is varying.")

    for field in ("currently_measured", "provisioned", "open_questions"):
        val = spec.get(field)
        if val is not None and not isinstance(val, list):
            questions.append(
                "[malformed] %s -- must be a list, got %s"
                % (field, type(val).__name__))

    return questions


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    with open(sys.argv[1]) as fh:
        spec = json.load(fh)
    questions = check(spec)
    if not questions:
        print("spec complete: %s" % spec.get("system_id"))
        return 0
    print("SPEC INCOMPLETE -- %d open:\n" % len(questions))
    for q in questions:
        print("  " + q)
    return 1


if __name__ == "__main__":
    sys.exit(main())
