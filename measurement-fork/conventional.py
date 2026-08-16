#!/usr/bin/env python3
"""
ARM 3 -- conventional design generator.

Encodes the design defaults a field would actually run. These are
NOT errors and are not written as errors. Each has a real reason:
state variables inside the boundary are accessible and repeatable;
single-point measurement is cheap; standardized items are comparable
across labs; a fixed reference makes results poolable.

The point of this arm is that it is competent. The gaps then show up
as gaps rather than as mistakes.

Swappable: any generator emitting probe() dicts can replace this one.

CC0-1.0. stdlib only.
"""
import json
import sys

from quantities import quantity, probe


def generate(spec):
    out = []
    n = 0

    for m in spec.get("currently_measured", []):
        n += 1
        out.append(probe(
            arm="conventional",
            pid="C%02d" % n,
            q=quantity(base=m, object_of="organism"),
            protocol=("measure %s at a single matched stimulus; "
                      "compare group means across the regime" % m),
            reads="level of %s in the organism at one point" % m,
            blind_to=("whether the level is a property of the organism "
                      "or of its relation to the environment; no gradient, "
                      "so a calibrated response and a degraded one return "
                      "the same number"),
        ))

    src = spec.get("test_items_source", "unknown")
    n += 1
    out.append(probe(
        arm="conventional",
        pid="C%02d" % n,
        q=quantity(base="task_performance", object_of="organism"),
        protocol=("standardized battery, items drawn from %s, "
                  "scored against a fixed reference" % src),
        reads="performance relative to the reference population",
        blind_to=("performance in the domain the organism actually "
                  "calibrated to; items come from one side only, so "
                  "domain mismatch reads as deficit"),
    ))

    reg = spec.get("regime")
    if reg:
        n += 1
        out.append(probe(
            arm="conventional",
            pid="C%02d" % n,
            q=quantity(base="outcome_endpoint", object_of="organism"),
            protocol=("follow hard endpoints across %s (%s); "
                      "dose-response on the exposure variable"
                      % (reg["variable"], reg["range"])),
            reads="endpoint incidence by exposure level",
            blind_to=("anything that improves while endpoints improve; "
                      "one column, so an allocation shift and a loss "
                      "look identical"),
        ))

    n += 1
    out.append(probe(
        arm="conventional",
        pid="C%02d" % n,
        q=quantity(base="self_report", object_of="organism"),
        protocol="validated questionnaire, present-day administration",
        reads="reported state at time of administration",
        blind_to=("recall is state-modulated; the reported history is "
                  "an instrument-level quantity reported as an "
                  "organism-level one"),
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
