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

from quantities import probe, quantity

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
            q=quantity(base=base, object_of="the design"),
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
            q=quantity(
                base="rename or decompose: %s" % q,
                object_of="the design"),
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
            q=quantity(
                base=("measure %s on a population that was never exposed"
                      % reg["variable"]),
                object_of="the design"),
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
