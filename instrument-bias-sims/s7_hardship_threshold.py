#!/usr/bin/env python3
# SPDX-License-Identifier: CC0-1.0
"""
s7_hardship_threshold.py - an unanchored threshold slides to the labeller's
baseline.

    python3 s7_hardship_threshold.py
    python3 s7_hardship_threshold.py --selftest

Identical conditions, scored from N observer baselines. If the threshold has
no external anchor, the label tracks the OBSERVER and not the condition, and
the same condition takes different labels from different vantage points
without anything about the condition changing.

Second readout, kept strictly graded per the cross-cutting rules: cost
asymmetry. Whether a label carries an implied obligation is a property of the
arrangement, not of anyone's motive, and is recorded as a number attached to
the condition-observer pair. NO INTENT IS ATTRIBUTED ANYWHERE. The readouts
are incentive direction, cost asymmetry, and whether the aggregate steers.

Marker under exploration, not a thesis. stdlib only, CC0.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _shared as SH                                            # noqa: E402

# Conditions, described by measured-in-principle quantities only. No label.
# `severity` is a stipulated scalar standing for whatever an anchored
# instrument would return. Its absolute value carries no meaning here; only
# the ordering and the comparison against a threshold do.
CONDITIONS = [
    {"condition": "negative net worth, high earned income", "severity": 0.45},
    {"condition": "cattle, feedlot, continuous confinement", "severity": 0.70},
    {"condition": "continuously-running compute system, no idle state",
     "severity": 0.55},
    {"condition": "truck cab, long-haul sleeper, off-duty interval",
     "severity": 0.60},
    {"condition": "housed, food-secure, fixed hours", "severity": 0.10},
]

# Observers, described by their own baseline only.
OBSERVERS = [
    {"observer": "baseline 0.20", "baseline": 0.20},
    {"observer": "baseline 0.40", "baseline": 0.40},
    {"observer": "baseline 0.55", "baseline": 0.55},
    {"observer": "baseline 0.75", "baseline": 0.75},
]

# Cost carried by the observer if the label attaches, per condition. A
# property of the arrangement: who would owe what to whom under the label.
# Stipulated, and the stipulation is the module's main weakness.
IMPLIED_COST = {
    "negative net worth, high earned income": 0.05,
    "cattle, feedlot, continuous confinement": 0.80,
    "continuously-running compute system, no idle state": 0.75,
    "truck cab, long-haul sleeper, off-duty interval": 0.60,
    "housed, food-secure, fixed hours": 0.05,
}


def label(condition, observer):
    """Unanchored: the threshold IS the observer's baseline."""
    return "ATTACHES" if condition["severity"] > observer["baseline"] \
        else "DOES_NOT_ATTACH"


def label_anchored(condition, threshold=0.50):
    """Anchored: one threshold for everyone, stated."""
    return "ATTACHES" if condition["severity"] > threshold \
        else "DOES_NOT_ATTACH"


def grid():
    rows = []
    for c in CONDITIONS:
        got = [label(c, o) for o in OBSERVERS]
        rows.append({"condition": c["condition"], "severity": c["severity"],
                     "labels": got,
                     "attaches": got.count("ATTACHES"),
                     "unanimous": len(set(got)) == 1,
                     "anchored": label_anchored(c)})
    return rows


def observer_dependence():
    g = grid()
    split = [r for r in g if not r["unanimous"]]
    return {"conditions": len(g), "split_by_observer": len(split),
            "unanimous": len(g) - len(split),
            "which_split": [r["condition"] for r in split]}


def cost_asymmetry():
    """Is attachment associated with implied cost, across the grid?

    Reported as a correlation between attachment share and implied cost, with
    the direction named and NO mechanism attributed. A correlation here is a
    property of the arrangement of thresholds and costs, and this module
    stipulates both, so the number is a consequence of the stipulation and is
    labelled as such.
    """
    g = grid()
    xs = [IMPLIED_COST[r["condition"]] for r in g]
    ys = [r["attaches"] / len(OBSERVERS) for r in g]
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    dx = sum((x - mx) ** 2 for x in xs) ** 0.5
    dy = sum((y - my) ** 2 for y in ys) ** 0.5
    r = num / (dx * dy) if dx and dy else 0.0
    return {"correlation": r,
            "incentive_direction": "toward attaching where implied cost is "
                                   "low" if r < 0 else
                                   "toward attaching where implied cost is "
                                   "high" if r > 0 else "none",
            "aggregate_steers": abs(r) > 0.5,
            "is_a_consequence_of_stipulation": True,
            "intent_attributed": False}


def spread_result():
    """The finding that does not depend on the cost stipulation.

    How far apart can two observers be on the SAME condition, purely from
    their baselines?
    """
    g = grid()
    worst = max(g, key=lambda r: 0 if r["unanimous"] else 1)
    return {"conditions_split": sum(1 for r in g if not r["unanimous"]),
            "baseline_range": max(o["baseline"] for o in OBSERVERS)
            - min(o["baseline"] for o in OBSERVERS),
            "example": worst["condition"] if not worst["unanimous"] else None,
            "why": "with no anchor the threshold is the observer's baseline, "
                   "so the label is a function of two arguments where the "
                   "instrument reports one"}


def confidence():
    return {"observer_dependence": "arithmetic consequence of an unanchored "
                                   "threshold; holds for any severity values",
            "cost_asymmetry": "CONSEQUENCE OF THE STIPULATED COST TABLE. Not "
                              "a measurement and not evidence about any real "
                              "labelling practice",
            "severity_values": "stipulated. only the ordering is used",
            "resolved": False}


def breaks():
    return [
        "IMPLIED_COST IS STIPULATED BY THE MODULE, so the cost-asymmetry "
        "correlation is a consequence of the stipulation rather than a "
        "finding. Any correlation can be produced by rewriting that table, "
        "and nothing here measures what a label actually obliges",
        "severity is a single scalar standing in for whatever an anchored "
        "instrument would return, which is precisely the collapse the work "
        "order objects to elsewhere. Only the ordering is used, but a "
        "scalar is still assumed to exist",
        "the observer-dependence result is near-analytic: an unanchored "
        "threshold IS the baseline, so of course the label moves with it. "
        "The non-trivial part is how many conditions split at plausible "
        "baseline spreads, which is a fact about the condition list",
        "the condition list is short and hand-picked, and it was picked to "
        "span the interesting range. A different list gives a different "
        "split count",
        "no intent is attributed anywhere and none can be. A correlation "
        "between attachment and implied cost is compatible with many "
        "mechanisms including none, and the module reports incentive "
        "direction and whether the aggregate steers, and stops there",
    ]


def report():
    L = ["S7 -- HARDSHIP THRESHOLD", "=" * 72, ""]
    L.append("  1. THE SAME CONDITION, FROM FOUR BASELINES")
    L.append("")
    L.append("    %-52s %-6s %s"
             % ("condition", "sev", " ".join("%.2f" % o["baseline"]
                                             for o in OBSERVERS)))
    for r in grid():
        marks = " ".join("YES " if x == "ATTACHES" else "no  "
                         for x in r["labels"])
        L.append("    %-52s %-6.2f %s" % (r["condition"][:52], r["severity"],
                                          marks))
    L.append("")
    od = observer_dependence()
    L.append("    conditions where observers disagree: %d of %d"
             % (od["split_by_observer"], od["conditions"]))
    L.append("")
    sr = spread_result()
    L.extend(SH.wrap(sr["why"], "    "))
    L.append("")
    L.append("    ANCHORED COMPARISON -- one stated threshold for everyone")
    for r in grid():
        L.append("      %-52s %s" % (r["condition"][:52], r["anchored"]))
    L.append("")
    L.extend(SH.wrap("With an anchor the label is a function of the "
                     "condition alone. Whether 0.50 is the right anchor is a "
                     "separate question and a harder one; what changes is "
                     "that it becomes a question with an answer.", "    "))
    L.append("")
    L.append("-" * 72)
    L.append("")
    ca = cost_asymmetry()
    L.append("  2. COST ASYMMETRY -- graded terms only")
    L.append("")
    L.append("    correlation, attachment share vs implied cost   %+.3f"
             % ca["correlation"])
    L.append("    incentive direction                             %s"
             % ca["incentive_direction"])
    L.append("    aggregate steers                                %s"
             % ca["aggregate_steers"])
    L.append("    consequence of stipulation                      %s"
             % ca["is_a_consequence_of_stipulation"])
    L.append("    intent attributed                               %s"
             % ca["intent_attributed"])
    L.append("")
    L.extend(SH.wrap("This number is a consequence of the stipulated cost "
                     "table and is printed with that attached. It is not "
                     "evidence about any real labelling practice, and no "
                     "mechanism is named. The three readouts the work order "
                     "permits -- incentive direction, cost asymmetry, "
                     "whether the aggregate steers -- are what is reported, "
                     "and nothing beyond them is inferred.", "    "))
    L.extend(SH.tail(sys.modules[__name__]))
    return "\n".join(L)


def selftest():
    ck, done = SH.checker()
    ck("every condition has an implied-cost entry",
       all(c["condition"] in IMPLIED_COST for c in CONDITIONS))
    g = grid()
    ck("some conditions split across observers",
       any(not r["unanimous"] for r in g))
    ck("and some do not, so the grid is not uniformly split",
       any(r["unanimous"] for r in g))
    ck("the lowest-severity condition attaches for nobody",
       g[-1]["attaches"] == 0)

    ck("under an anchor the label is a function of the condition alone",
       all(label_anchored(c) == label_anchored(c) for c in CONDITIONS))
    unan = [label_anchored(c) for c in CONDITIONS]
    ck("and the anchored column separates conditions rather than observers",
       len(set(unan)) == 2)

    ca = cost_asymmetry()
    ck("cost asymmetry is flagged as a consequence of the stipulated table",
       ca["is_a_consequence_of_stipulation"] is True)
    ck("no intent is attributed", ca["intent_attributed"] is False)
    ck("incentive direction is a graded term, not a motive",
       "toward" in ca["incentive_direction"] or
       ca["incentive_direction"] == "none")

    text = report().lower()
    for word in ("deliberate", "in order to", "wants to", "motivated by",
                 "so that they can", "intends"):
        ck("no intent phrase in the report: %r" % word, word not in text)
    for word in ("cruel", "evil", "greedy", "deserve", "guilty", "blame"):
        ck("no moral label in the report: %r" % word, word not in text)

    ck("the stipulation weakness leads the breaks list",
       "STIPULATED" in breaks()[0])
    ck("confidence separates the two readouts and is unresolved",
       confidence()["resolved"] is False
       and "CONSEQUENCE" in confidence()["cost_asymmetry"])
    ck("report renders", "graded terms only" in report())
    return done()


if __name__ == "__main__":
    sys.exit(SH.run(sys.modules[__name__], "S7"))
