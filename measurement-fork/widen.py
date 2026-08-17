#!/usr/bin/env python3
"""
ARM 3 -- widen. Options, not quantities.

CC0-1.0. stdlib only.

Reconstructed from compare.py, which treats this arm differently from the
other two:

    if sole.get("widen"):
        print("  [widen] -- options, not quantities. "
              "mark applies yes|no|unclear:")

So this arm does not propose measurements. It proposes ways the other two
arms might be wrong about what to measure, and refuses to rank them. Direct
descendant of ../reasoning-gate/explore.py: emits candidates, ranks nothing,
does not converge.

That is why its probes' `blind_to` all say the same thing. A widening is not
an instrument and has no blindness map -- it is a question about whether the
instrument list is the right list. The `applies` field is the reader's to
fill, and nothing here fills it.
"""

from __future__ import annotations

import json
import sys

from quantities import OBJECTS, probe

# The widen arm does not measure anything, so it cannot build a quantity().
# The canonical quantities.py enforces a CLOSED vocabulary --
#     OBJECTS = ("organism", "environment", "coupling", "instrument")
# -- and refuses any other object_of outright. A widening is about the
# DESIGN, which is not on that list and should not be added to it.
#
# That refusal is load-bearing and is the schema confirming, from the
# delivered code, what coverage_check.py section 3 measures: widen output
# is not a quantity, so it must not appear in any quantity-keyed cell and
# must not count toward measurement coverage.
#
# So widen builds the same-shaped dict locally, tagged with an object_of
# OUTSIDE the closed vocabulary. Any consumer that filters on OBJECTS
# drops it automatically, which is the behaviour wanted.

NOT_A_QUANTITY = "design"
assert NOT_A_QUANTITY not in OBJECTS, (
    "widen's marker must stay outside the canonical vocabulary")


def option(base):
    """Quantity-shaped, deliberately not a quantity. See above."""
    return {"base": base, "normalizer": None, "object_of": NOT_A_QUANTITY}


def is_quantity(p):
    """True for probes that propose a measurement. Filter with this."""
    return p["quantity"]["object_of"] in OBJECTS

# Widenings that do not depend on the spec. Each names a way the fork's own
# framing could be wrong.
STRUCTURAL = (
    ("measure the same quantity on the environment as well as the organism",
     "every organism-level quantity has an environment-level twin nobody "
     "collected"),
    ("run the instrument on a case whose answer is already known",
     "no arm here validates its own apparatus against a known reference"),
    ("vary sample size by 4x and see which numbers move",
     "a number that moves with N is a property of the sampling, not the "
     "system"),
    ("measure the same thing twice on one subject, same session",
     "without repeat variance there is no floor to compare any spread "
     "against"),
    ("state what would change the number without changing the system",
     "if nothing would, the quantity may not be measuring the system"),
    ("ask who benefits from each possible answer",
     "the design was chosen by someone, and choice of measurand is not "
     "neutral"),
    # K17, relocated. It was specified as a probe with object_of=instrument,
    # which is inside quantities.OBJECTS and so would have been legal. It is
    # here instead because of what it points AT: it takes no reading from the
    # system, it decomposes the model's own terms, and it applies unchanged
    # to any model. That is a question about a design, which is what this arm
    # holds. Recorded as MF_016.
    ("decompose each term in the model and tag each component with its "
     "object_of; a count above one is a flag",
     "a single word can carry several quantities with different object_of "
     "and different rates. Summing them can cancel a real movement, which "
     "is Simpson's paradox on the decomposition rather than the ecological "
     "fallacy"),
)

BLIND = ("this is not an instrument and has no blindness map. It is a "
         "question about whether the instrument list is the right list.")


def generate(spec):
    out = []
    n = 0

    for base, why in STRUCTURAL:
        n += 1
        out.append(probe(
            arm="widen",
            pid="W%02d" % n,
            q=option(base),
            protocol="mark applies: yes | no | unclear. Then say why.",
            reads=why,
            blind_to=BLIND,
        ))

    # Spec-derived widenings: one per open question, asking whether the
    # question is badly named rather than unreached.
    for q in spec.get("open_questions", []):
        n += 1
        out.append(probe(
            arm="widen",
            pid="W%02d" % n,
            q=option("rename or decompose: %s" % q),
            protocol="mark applies: yes | no | unclear. Then say why.",
            reads=("a question no arm reaches may be unmeasurable, or may "
                   "be one question wearing the name of three"),
            blind_to=BLIND,
        ))

    # If the regime is declared, ask the question the endpoint probes cannot.
    reg = spec.get("regime")
    if reg:
        n += 1
        out.append(probe(
            arm="widen",
            pid="W%02d" % n,
            q=option("measure %s on a population that was never exposed"
                     % reg["variable"]),
            protocol="mark applies: yes | no | unclear. Then say why.",
            reads=("dose-response across an exposed range has no zero. "
                   "Without one, the reference is the least-exposed group "
                   "rather than an unexposed one"),
            blind_to=BLIND,
        ))

    return out


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    with open(sys.argv[1]) as fh:
        spec = json.load(fh)
    print(json.dumps(generate(spec), indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
