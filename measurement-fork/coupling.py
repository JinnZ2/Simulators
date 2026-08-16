#!/usr/bin/env python3
"""
ARM 2 -- coupling generator.

Rule it runs on: when a quantity is a RELATION between organism and
environment, the standard instrument reads one side and reports the
result as a property of the organism. This arm generates the missing
side, and the ratio.

Emits probes whose object_of is 'coupling' or 'environment' wherever
the conventional arm would have said 'organism'.

CC0-1.0. stdlib only.
"""
import json
import sys

from quantities import quantity, probe


def generate(spec):
    out = []
    n = 0

    for p in spec.get("provisioned", []):
        n += 1
        out.append(probe(
            arm="coupling",
            pid="K%02d" % n,
            q=quantity(base="latency", object_of="coupling",
                       normalizer=None),
            protocol=("time from the actor's act to the consequence "
                      "arriving, for: %s. Distribution, not mean." % p),
            reads="how tightly the loop can close",
            blind_to="whether the actor's own sensors were used to read it",
        ))

        n += 1
        out.append(probe(
            arm="coupling",
            pid="K%02d" % n,
            q=quantity(base="contingency_consistency", object_of="coupling"),
            protocol=("same act, repeated; measure variance in the "
                      "consequence returned, for: %s" % p),
            reads="whether the mapping is learnable at all",
            blind_to="magnitude of consequence; only its reliability",
        ))

    n += 1
    out.append(probe(
        arm="coupling",
        pid="K%02d" % n,
        q=quantity(base="response_magnitude", object_of="coupling",
                   normalizer="perturbation_size"),
        protocol=("small periodic contingency breaks; record response "
                  "magnitude divided by objective perturbation size. "
                  "The RATIO is the readout, not the response."),
        reads="accumulated calibration error",
        blind_to=("nothing about absolute response level; deliberately "
                  "discards it"),
    ))

    n += 1
    out.append(probe(
        arm="coupling",
        pid="K%02d" % n,
        q=quantity(base="confidence", object_of="coupling",
                   normalizer="accuracy"),
        protocol=("elicit predicted outcome AND stated confidence before "
                  "each trial; score both separately. Report the gap."),
        reads=("decoupling of confidence from validity -- rises silently "
               "while every state variable reads nominal"),
        blind_to="cases where the actor cannot report confidence",
    ))

    n += 1
    out.append(probe(
        arm="coupling",
        pid="K%02d" % n,
        q=quantity(base="response_magnitude", object_of="organism",
                   normalizer="stimulus_severity"),
        protocol=("graded severity series, 4+ levels. Fit the slope. "
                  "A single matched stimulus cannot run this."),
        reads=("discrimination gradient. Calibrated = graded. "
               "Degraded = flat."),
        blind_to="which mechanism produced a given slope, absent history",
    ))

    src = spec.get("test_items_source", "unknown")
    n += 1
    out.append(probe(
        arm="coupling",
        pid="K%02d" % n,
        q=quantity(base="task_performance", object_of="coupling",
                   normalizer="domain_match"),
        protocol=("BIDIRECTIONAL: both groups take items from BOTH "
                  "domains (currently items come from %s only). "
                  "Read the interaction, not the main effect. "
                  "Allocation predicts crossover; deficit predicts one "
                  "group wins both." % src),
        reads="whether apparent deficit is domain mismatch",
        blind_to="absolute capability; only the interaction",
    ))

    reg = spec.get("regime")
    if reg:
        n += 1
        out.append(probe(
            arm="coupling",
            pid="K%02d" % n,
            q=quantity(base="autocorrelation", object_of="environment"),
            protocol=("measure the environment's own variance structure "
                      "over %s -- autocorrelation, not event count. "
                      "Severe-but-predictable and mild-but-unpredictable "
                      "are different regimes that current instruments "
                      "score the same." % reg["variable"]),
            reads="what the organism was calibrating TO",
            blind_to="the organism entirely; this measures the surround",
        ))

    n += 1
    out.append(probe(
        arm="coupling",
        pid="K%02d" % n,
        q=quantity(base="allocation", object_of="organism",
                   normalizer="total_budget"),
        protocol=("measure peripheral response AND classification "
                  "performance in the SAME subjects, same session. "
                  "Allocation predicts they move opposite. "
                  "Damage predicts they move together."),
        reads="whether a drop in one column is a shift or a loss",
        blind_to="the budget itself; only its distribution",
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
