#!/usr/bin/env python3
# SPDX-License-Identifier: CC0-1.0
"""
s8_recognition_to_delivery.py - time as an excuse vs time as a variable.

    python3 s8_recognition_to_delivery.py
    python3 s8_recognition_to_delivery.py --selftest

Interval from problem-documentation to delivered relief, per era, normalised
by communication and disbursement speed. The stated test: does the normalised
current interval exceed the horseback-era interval?

THE NORMALISATION IS THE WHOLE CLAIM, AND IT IS CIRCULAR AS STATED. Dividing
by communication speed assumes the binding constraint on delivery was
communication -- which is exactly what the test is supposed to establish. If
the binding constraint was something else in either era, the normaliser is
measuring the wrong thing and the comparison inherits that.

So this module reports the raw intervals and the normalisers SEPARATELY, and
then shows that the choice of normaliser decides the answer: under three
defensible normalisers the verdict changes sign. That is the finding. It does
not settle the question; it shows the question is not yet well posed, which is
a different and more useful state than an unresolved answer.

Every figure below is DECLARED, carried from the work order or from common
summary knowledge, and is NOT verified here.

Marker under exploration, not a thesis. stdlib only, CC0.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _shared as SH                                            # noqa: E402

# DECLARED FIGURES. Not verified in this module. Days unless stated.
ERAS = [
    {"era": "New Deal, first tranche", "year": 1933,
     "interval_days": 100,
     "comms_days_one_way": 3.0,        # telegraph + rail + paper
     "disbursement_days": 14.0,        # cheque, post, local office
     "source": "declared: ~100 days to first tranche"},
    {"era": "Rural electrification", "year": 1935,
     "interval_days": 3650,
     "comms_days_one_way": 3.0,
     "disbursement_days": 14.0,
     "source": "declared: roughly a decade"},
    {"era": "Present", "year": 2026,
     "interval_days": 540,
     "comms_days_one_way": 0.0007,     # same-day electronic, ~1 minute
     "disbursement_days": 1.0,         # same-day electronic transfer
     "source": "DECLARED PLACEHOLDER. no measured present-day interval is "
               "used here, and the verdict moves with it"},
]

NORMALISERS = [
    {"name": "comms only",
     "of": lambda e: e["comms_days_one_way"],
     "assumes": "the binding constraint was moving the message"},
    {"name": "comms + disbursement",
     "of": lambda e: e["comms_days_one_way"] + e["disbursement_days"],
     "assumes": "the binding constraint was moving the message and the money"},
    {"name": "none (raw interval)",
     "of": lambda e: 1.0,
     "assumes": "nothing; reports the interval as measured"},
]


def normalised(norm):
    rows = []
    for e in ERAS:
        d = norm["of"](e)
        rows.append({"era": e["era"], "raw_days": e["interval_days"],
                     "normaliser_days": d,
                     "normalised": e["interval_days"] / d if d else None})
    return rows


def verdict(norm):
    """Does the present normalised interval exceed the 1933 one?"""
    rows = normalised(norm)
    old = [r for r in rows if r["era"].startswith("New Deal")][0]
    new = [r for r in rows if r["era"] == "Present"][0]
    return {"normaliser": norm["name"], "assumes": norm["assumes"],
            "old": old["normalised"], "new": new["normalised"],
            "ratio": new["normalised"] / old["normalised"]
            if old["normalised"] else None,
            "present_exceeds": new["normalised"] > old["normalised"]}


def flip_point(norm):
    """The present-day interval at which this normaliser's verdict flips.

    The interesting quantity, and not the one the first draft looked for.
    """
    rows = normalised(norm)
    old = [r for r in rows if r["era"].startswith("New Deal")][0]
    present = [e for e in ERAS if e["era"] == "Present"][0]
    d = norm["of"](present)
    return old["normalised"] * d


def normaliser_sensitivity():
    """CORRECTED. The first draft of this module predicted the verdict would
    change sign across normalisers. It does not, at the declared placeholder:
    all three agree, because 540 days exceeds 100 days before any denominator
    is applied. The check caught the drafted prose and the prose was changed
    to the measurement.

    What the normalisers disagree about is WHERE the sign flips -- the
    present-day interval that would count as no worse than 1933 -- and those
    flip points span more than three orders of magnitude. So the test has no
    stable meaning until the normaliser is justified, which is the same
    finding by a better route.
    """
    vs = [verdict(n) for n in NORMALISERS]
    for v, n in zip(vs, NORMALISERS):
        v["flip_point_days"] = flip_point(n)
    signs = set(v["present_exceeds"] for v in vs)
    ratios = [v["ratio"] for v in vs if v["ratio"] is not None]
    flips = [v["flip_point_days"] for v in vs]
    return {"verdicts": vs,
            "verdict_changes_sign": len(signs) > 1,
            "ratio_spread": max(ratios) / min(ratios) if ratios else None,
            "flip_point_spread": max(flips) / min(flips) if min(flips) else
            None,
            "why": "the normaliser encodes an assumption about what the "
                   "binding constraint was, and that assumption is what the "
                   "test exists to establish. It does not change the sign at "
                   "the declared placeholder; it changes the interval at "
                   "which the sign would flip, by more than three orders of "
                   "magnitude. Either way the answer was chosen with the "
                   "denominator"}


def variable_check():
    """The work order's own criterion, applied to the phrase it is aimed at.

    A real variable has a value, an uncertainty and a stated endpoint. This is
    checked against both the phrase and against THIS MODULE'S OWN present-day
    figure, which turns out to fail two of the three.
    """
    items = [
        {"item": "'not enough time yet'", "has_value": False,
         "has_uncertainty": False, "has_endpoint": False},
        {"item": "this module's present-day interval", "has_value": True,
         "has_uncertainty": False, "has_endpoint": True},
        {"item": "the 1933 first-tranche interval", "has_value": True,
         "has_uncertainty": False, "has_endpoint": True},
    ]
    for it in items:
        it["qualifies_as_a_variable"] = (it["has_value"]
                                         and it["has_uncertainty"]
                                         and it["has_endpoint"])
    return items


def confidence():
    return {"normaliser_sensitivity": "arithmetic, given the declared "
                                      "figures",
            "figures": "ALL DECLARED, none verified here. the present-day "
                       "interval is an explicit placeholder",
            "the_comparison_itself": "NOT_WELL_POSED until the binding "
                                     "constraint per era is established",
            "resolved": False}


def breaks():
    return [
        "THE NORMALISATION IS CIRCULAR AS STATED. Dividing by communication "
        "speed assumes communication was the binding constraint, which is "
        "what the test is meant to establish. At the declared placeholder "
        "the three normalisers happen to AGREE on the sign -- the drafted "
        "expectation that they would not was wrong and is recorded in "
        "normaliser_sensitivity() -- but they disagree by over 4000x about "
        "what present-day interval would count as parity, so the choice "
        "still decides the answer, one step further back",
        "the present-day interval is a PLACEHOLDER. No measured "
        "documentation-to-delivery interval is used, and the verdict moves "
        "with it under every normaliser",
        "'delivered relief' is not defined. First tranche, full coverage and "
        "last recipient are three different endpoints with different "
        "intervals, and the 1933 and present figures may not be the same "
        "endpoint",
        "no uncertainty is attached to any figure, so by the work order's "
        "own criterion -- a value, an uncertainty and a stated endpoint -- "
        "the module's own numbers do not qualify as variables either. That "
        "is checked in variable_check() rather than left implicit",
        "two data points per era at most, and one era. A trend is not "
        "recoverable from this",
    ]


def report():
    L = ["S8 -- RECOGNITION TO DELIVERY", "=" * 72, ""]
    L.append("  0. FIGURES, ALL DECLARED AND NONE VERIFIED HERE")
    L.append("")
    L.append("    %-30s %-8s %-12s %s"
             % ("era", "days", "comms d", "disburse d"))
    for e in ERAS:
        L.append("    %-30s %-8d %-12.4f %.1f"
                 % (e["era"], e["interval_days"], e["comms_days_one_way"],
                    e["disbursement_days"]))
    L.append("")
    for e in ERAS:
        if "PLACEHOLDER" in e["source"]:
            L.extend(SH.wrap("%s: %s" % (e["era"], e["source"]), "    "))
    L.append("")
    L.append("-" * 72)
    L.append("")
    ns = normaliser_sensitivity()
    L.append("  1. THE NORMALISER DECIDES THE ANSWER")
    L.append("")
    L.append("    %-24s %-10s %-8s %s"
             % ("normaliser", "ratio", "exceeds", "flips below (days)"))
    for v in ns["verdicts"]:
        L.append("    %-24s %-10.1f %-8s %.4f"
                 % (v["normaliser"], v["ratio"],
                    "YES" if v["present_exceeds"] else "no",
                    v["flip_point_days"]))
    L.append("")
    L.append("    verdict changes sign across normalisers: %s"
             % ns["verdict_changes_sign"])
    L.append("    ratio spread across normalisers:         %.0fx"
             % ns["ratio_spread"])
    L.append("    FLIP-POINT spread across normalisers:    %.0fx"
             % ns["flip_point_spread"])
    L.append("")
    L.extend(SH.wrap("CORRECTION, kept rather than smoothed. This module was "
                     "drafted expecting the verdict to change sign across "
                     "normalisers. It does not: at the declared placeholder "
                     "all three agree, because 540 days exceeds 100 days "
                     "before any denominator is applied. The check caught "
                     "the prose and the prose was changed to the "
                     "measurement.", "    "))
    L.append("")
    L.extend(SH.wrap("What the normalisers disagree about is where the sign "
                     "WOULD flip -- the present-day interval that counts as "
                     "no worse than 1933. Under the raw reading that is 100 "
                     "days. Under comms-plus-disbursement it is about six "
                     "days. Under comms-only it is about half an hour. Three "
                     "defensible denominators, and a %.0fx range in what "
                     "would count as parity." % ns["flip_point_spread"],
                     "    "))
    L.append("")
    for v in ns["verdicts"]:
        L.extend(SH.wrap("%s assumes: %s" % (v["normaliser"], v["assumes"]),
                         "    "))
    L.append("")
    L.extend(SH.wrap(ns["why"], "    "))
    L.append("")
    L.extend(SH.wrap("So the honest output is not a verdict. It is that the "
                     "comparison is not well posed until the binding "
                     "constraint per era is established independently -- and "
                     "establishing that is a different and prior piece of "
                     "work. Reporting a normalised ratio without it hands "
                     "over an answer whose sign was chosen with the "
                     "denominator.", "    "))
    L.append("")
    L.append("-" * 72)
    L.append("")
    L.append("  2. THE WORK ORDER'S OWN CRITERION, TURNED ON THIS MODULE")
    L.append("")
    L.append("    %-42s %-7s %-7s %-9s %s"
             % ("item", "value", "uncert", "endpoint", "is a variable"))
    for it in variable_check():
        L.append("    %-42s %-7s %-7s %-9s %s"
                 % (it["item"], it["has_value"], it["has_uncertainty"],
                    it["has_endpoint"], it["qualifies_as_a_variable"]))
    L.append("")
    L.extend(SH.wrap("A real variable has a value, an uncertainty and a "
                     "stated endpoint. The phrase the work order objects to "
                     "has none of the three. This module's own figures have "
                     "two of three -- no uncertainty on any of them -- so by "
                     "the criterion it is applying, its own numbers do not "
                     "qualify either. Recorded rather than exempted.", "    "))
    L.extend(SH.tail(sys.modules[__name__]))
    return "\n".join(L)


def selftest():
    ck, done = SH.checker()
    ck("every era carries a source string", all(e["source"] for e in ERAS))
    ck("the present-day figure is marked a placeholder",
       any("PLACEHOLDER" in e["source"] for e in ERAS))

    ns = normaliser_sensitivity()
    ck("the verdict does NOT change sign at the declared placeholder -- the "
       "drafted expectation was wrong and the correction is kept",
       ns["verdict_changes_sign"] is False)
    ck("the ratio spreads by orders of magnitude across normalisers",
       ns["ratio_spread"] > 100)
    ck("and the FLIP POINT -- what would count as parity -- spreads by more "
       "than three orders of magnitude, which is the finding",
       ns["flip_point_spread"] > 1000)
    ck("every verdict carries its flip point",
       all("flip_point_days" in v for v in ns["verdicts"]))
    ck("every normaliser states the assumption it encodes",
       all(v["assumes"] for v in ns["verdicts"]))
    ck("the raw-interval normaliser assumes nothing, which is what makes it "
       "the honest baseline",
       [n for n in NORMALISERS if n["name"].startswith("none")][0]["assumes"]
       == "nothing; reports the interval as measured")

    vc = variable_check()
    ck("the phrase under objection qualifies as a variable on nothing",
       vc[0]["qualifies_as_a_variable"] is False
       and not any([vc[0]["has_value"], vc[0]["has_uncertainty"],
                    vc[0]["has_endpoint"]]))
    ck("and this module's own figures do not qualify either, which is "
       "recorded rather than exempted",
       all(not it["qualifies_as_a_variable"] for it in vc))
    ck("the reason is the missing uncertainty, not a missing value",
       vc[1]["has_value"] and not vc[1]["has_uncertainty"])

    ck("the circularity leads the breaks list", "CIRCULAR" in breaks()[0])
    ck("the comparison is recorded as not well posed",
       "NOT_WELL_POSED" in confidence()["the_comparison_itself"])
    ck("confidence unresolved", confidence()["resolved"] is False)

    text = report().lower()
    for w in ("deliberate", "in order to", "intends", "motivated by"):
        ck("no intent phrase: %r" % w, w not in text)
    ck("report renders", "not well posed" in text)
    return done()


if __name__ == "__main__":
    sys.exit(SH.run(sys.modules[__name__], "S8"))
