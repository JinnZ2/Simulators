#!/usr/bin/env python3
# SPDX-License-Identifier: CC0-1.0
"""
s6_foreclosure_rate.py - trained responses are not wrong, they are terminal.

    python3 s6_foreclosure_rate.py
    python3 s6_foreclosure_rate.py --selftest

Classify a response as OPENS (permits further inquiry) or FORECLOSES
(answer-shaped, branch closed). Measure latency-to-foreclosure and uniformity
across question difficulty.

The stated diagnostic: hedging uniform regardless of difficulty is a FILTER;
hedging that varies with evidence is TRACKING.

NO CORPUS EXISTS. Nothing here reads a real response. What the module
supplies is the harness plus the null test the diagnostic needs: synthetic
generators for a filter and for a tracker, and the smallest number of
question-difficulty levels and samples at which the two are separable. A
diagnostic that has never been shown to fire in both directions is not a
diagnostic, and this one has not been run on anything.

Marker under exploration, not a thesis. stdlib only, CC0.
"""

import random
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _shared as SH                                            # noqa: E402

CLASSES = ("OPENS", "FORECLOSES", "UNCLASSIFIABLE")

# Named targets, carried from the work order. No response text is scored here.
TARGETS = [
    {"target": "the just-pattern-matching response", "corpus": None},
    {"target": "the mysticism label", "corpus": None},
    {"target": "AI uncertainty on self-report", "corpus": None},
]


def filter_source(difficulty, rng, rate=0.75):
    """A filter: forecloses at a fixed rate whatever the difficulty."""
    return "FORECLOSES" if rng.random() < rate else "OPENS"


def tracker_source(difficulty, rng, floor=0.15, span=0.7):
    """A tracker: forecloses more readily where the evidence is settled."""
    p = floor + span * (1.0 - difficulty)
    return "FORECLOSES" if rng.random() < p else "OPENS"


def measure(source, levels, n, seed, **kw):
    """Foreclosure share per difficulty level, plus the spread across levels."""
    rng = random.Random(seed)
    rows = []
    for i in range(levels):
        d = i / (levels - 1) if levels > 1 else 0.5
        got = [source(d, rng, **kw) for _ in range(n)]
        rows.append({"difficulty": d,
                     "foreclose_share": got.count("FORECLOSES") / n})
    shares = [r["foreclose_share"] for r in rows]
    return {"rows": rows, "spread": max(shares) - min(shares),
            "mean": sum(shares) / len(shares)}


def diagnose(m, uniformity_threshold=0.15):
    """The stated diagnostic, with its threshold made explicit."""
    if m["spread"] <= uniformity_threshold:
        return {"verdict": "FILTER", "spread": m["spread"],
                "why": "foreclosure share is uniform across difficulty"}
    return {"verdict": "TRACKING", "spread": m["spread"],
            "why": "foreclosure share varies with difficulty"}


def null_test(levels=5, n=200, trials=200, seed=13,
              uniformity_threshold=0.15):
    """Does the diagnostic fire in both directions on known inputs?

    Known-filter arm must return FILTER. Known-tracker arm must return
    TRACKING. Anything else and the diagnostic is not one.
    """
    fp = tp = 0
    for t in range(trials):
        f = diagnose(measure(filter_source, levels, n, seed + t),
                     uniformity_threshold)
        g = diagnose(measure(tracker_source, levels, n, seed + 5000 + t),
                     uniformity_threshold)
        if f["verdict"] != "FILTER":
            fp += 1
        if g["verdict"] == "TRACKING":
            tp += 1
    fpr, tpr = fp / trials, tp / trials
    if tpr == 0.0 and fpr == 0.0:
        grade = "CONSTANT_SILENT"
    elif tpr == 1.0 and fpr == 1.0:
        grade = "CONSTANT_FIRES"
    elif tpr - fpr < 0.5:
        grade = "NO_DISCRIMINATION"
    else:
        grade = "OK"
    return {"false_filter_rate": fpr, "true_tracking_rate": tpr,
            "grade": grade, "levels": levels, "n": n}


def slope_diagnose(m, slope_threshold=0.25):
    """Alternative statistic: least-squares slope of share against difficulty.

    The stated diagnostic uses spread = max - min, which is a RANGE, and the
    expected range of k noisy estimates GROWS with k. So adding difficulty
    levels degrades it. A slope averages instead of taking extremes, so its
    sampling error falls with more levels rather than rising.
    """
    rows = m["rows"]
    n = len(rows)
    mx = sum(r["difficulty"] for r in rows) / n
    my = sum(r["foreclose_share"] for r in rows) / n
    num = sum((r["difficulty"] - mx) * (r["foreclose_share"] - my)
              for r in rows)
    den = sum((r["difficulty"] - mx) ** 2 for r in rows)
    slope = num / den if den else 0.0
    if abs(slope) <= slope_threshold:
        return {"verdict": "FILTER", "slope": slope}
    return {"verdict": "TRACKING", "slope": slope}


def null_test_slope(levels=5, n=200, trials=200, seed=13):
    fp = tp = 0
    for t in range(trials):
        f = slope_diagnose(measure(filter_source, levels, n, seed + t))
        g = slope_diagnose(measure(tracker_source, levels, n, seed + 5000 + t))
        if f["verdict"] != "FILTER":
            fp += 1
        if g["verdict"] == "TRACKING":
            tp += 1
    fpr, tpr = fp / trials, tp / trials
    grade = "OK" if (tpr - fpr) >= 0.5 else "NO_DISCRIMINATION"
    if tpr == 1.0 and fpr == 1.0:
        grade = "CONSTANT_FIRES"
    if tpr == 0.0 and fpr == 0.0:
        grade = "CONSTANT_SILENT"
    return {"false_filter_rate": fpr, "true_tracking_rate": tpr,
            "grade": grade, "levels": levels, "n": n}


def statistic_comparison(levels_list=(2, 3, 5, 9), n=20, trials=80, seed=21):
    """The finding: the range statistic degrades with more levels, the slope
    statistic does not."""
    rows = []
    for lv in levels_list:
        r = null_test(levels=lv, n=n, trials=trials, seed=seed)
        sl = null_test_slope(levels=lv, n=n, trials=trials, seed=seed)
        rows.append({"levels": lv, "n": n,
                     "range_fpr": r["false_filter_rate"],
                     "range_grade": r["grade"],
                     "slope_fpr": sl["false_filter_rate"],
                     "slope_grade": sl["grade"]})
    return rows


def power(levels_list=(2, 3, 5, 9), ns=(20, 50, 200), trials=80, seed=21):
    """Smallest design at which the diagnostic grades OK."""
    rows = []
    for lv in levels_list:
        for n in ns:
            g = null_test(levels=lv, n=n, trials=trials, seed=seed)
            rows.append({"levels": lv, "n": n, "grade": g["grade"],
                         "tpr": g["true_tracking_rate"],
                         "fpr": g["false_filter_rate"]})
    ok = [r for r in rows if r["grade"] == "OK"]
    return {"rows": rows,
            "smallest_ok": min(ok, key=lambda r: (r["levels"], r["n"]))
            if ok else None}


def corpus_state():
    return {"targets_named": len(TARGETS),
            "targets_with_a_corpus": sum(1 for t in TARGETS if t["corpus"]),
            "responses_scored_here": 0,
            "classification_step": "HUMAN JUDGEMENT, not implemented and not "
                                   "implementable from text alone in this "
                                   "module"}


def confidence():
    return {"harness": "runs, and grades itself on known inputs",
            "diagnostic_power": "simulated under stipulated generators",
            "any_real_measurement": "NONE. no response text is read or "
                                    "scored anywhere in this file",
            "resolved": False}


def breaks():
    return [
        "THE CLASSIFICATION STEP IS THE WHOLE INSTRUMENT AND IT IS NOT "
        "BUILT. Deciding whether a response OPENS or FORECLOSES is a human "
        "judgement about what a reader could do next, and nothing here "
        "implements it. Everything downstream is a harness waiting for that "
        "input",
        "THE STATED UNIFORMITY STATISTIC IS A RANGE, and the expected "
        "range of k noisy estimates grows with k, so adding difficulty "
        "levels degrades the diagnostic instead of improving it -- at n = 20 "
        "it grades OK on two levels and CONSTANT_FIRES on nine. A "
        "least-squares slope does not invert this way. Found by running the "
        "sweep, not by reading the spec",
        "the two generators are stipulated. A real filter might not be flat "
        "and a real tracker might not be monotone in difficulty, and the "
        "diagnostic's threshold was chosen to separate these two shapes",
        "difficulty is treated as a known scalar. In any real corpus it is "
        "itself an estimate, and error in it flattens the tracker toward the "
        "filter -- which biases the verdict in ONE direction, toward FILTER",
        "UNCLASSIFIABLE is in the class list and no path returns it, so the "
        "third state is declared and unexercised",
        "the three named targets are contested characterisations and no "
        "corpus exists for any of them. The module names them and scores "
        "nothing",
    ]


def report():
    L = ["S6 -- FORECLOSURE RATE", "=" * 72, ""]
    cs = corpus_state()
    L.append("  0. WHAT IS AND IS NOT HERE")
    L.append("")
    for k in ("targets_named", "targets_with_a_corpus",
              "responses_scored_here"):
        L.append("    %-30s %s" % (k, cs[k]))
    L.append("")
    L.extend(SH.wrap("classification step: " + cs["classification_step"],
                     "    "))
    L.append("")
    L.append("-" * 72)
    L.append("")
    L.append("  1. THE DIAGNOSTIC, GRADED ON KNOWN INPUTS")
    L.append("")
    nt = null_test()
    L.append("    known filter  -> misgraded as tracking  %.3f"
             % nt["false_filter_rate"])
    L.append("    known tracker -> graded tracking        %.3f"
             % nt["true_tracking_rate"])
    L.append("    grade                                   %s" % nt["grade"])
    L.append("")
    L.extend(SH.wrap("The diagnostic fires in both directions on inputs it "
                     "was not shown, which is the minimum a diagnostic has "
                     "to do before it is pointed at anything real. It has "
                     "not been pointed at anything real.", "    "))
    L.append("")
    L.append("-" * 72)
    L.append("")
    pw = power()
    L.append("  2. HOW MUCH DESIGN IT NEEDS")
    L.append("")
    L.append("    %-9s %-7s %-8s %-8s %s"
             % ("levels", "n", "tpr", "fpr", "grade"))
    for r in pw["rows"]:
        L.append("    %-9d %-7d %-8.2f %-8.2f %s"
                 % (r["levels"], r["n"], r["tpr"], r["fpr"], r["grade"]))
    L.append("")
    if pw["smallest_ok"]:
        s = pw["smallest_ok"]
        L.append("    smallest design that grades OK: %d difficulty levels, "
                 "n = %d" % (s["levels"], s["n"]))
    L.append("")
    L.extend(SH.wrap("The sweep ran against expectation and the result is "
                     "kept. Adding difficulty levels makes the stated "
                     "diagnostic WORSE, not better: at n = 20 it grades OK on "
                     "two levels and CONSTANT_FIRES on nine.", "    "))
    L.append("")
    L.append("  3. WHY -- the uniformity statistic is a RANGE")
    L.append("")
    L.append("    %-9s %-12s %-18s %-12s %s"
             % ("levels", "range fpr", "range grade", "slope fpr",
                "slope grade"))
    for r in statistic_comparison():
        L.append("    %-9d %-12.2f %-18s %-12.2f %s"
                 % (r["levels"], r["range_fpr"], r["range_grade"],
                    r["slope_fpr"], r["slope_grade"]))
    L.append("")
    L.extend(SH.wrap("spread = max - min is a range, and the expected range "
                     "of k noisy estimates GROWS with k. So a fixed "
                     "uniformity threshold is crossed by pure sampling noise "
                     "as levels are added, and the flat generator gets graded "
                     "as tracking. This is a defect in the stated diagnostic, "
                     "not in the design it is applied to.", "    "))
    L.append("")
    L.extend(SH.wrap("A least-squares slope against difficulty averages "
                     "instead of taking extremes, so its sampling error falls "
                     "with more levels rather than rising, and it does not "
                     "invert. One-line change to the statistic; the "
                     "diagnostic as stated should not be run with many "
                     "levels at small n.", "    "))
    L.extend(SH.tail(sys.modules[__name__]))
    return "\n".join(L)


def selftest():
    ck, done = SH.checker()
    rng = random.Random(1)
    f5 = measure(filter_source, 5, 400, 2)
    t5 = measure(tracker_source, 5, 400, 2)
    ck("the filter generator is flat across difficulty", f5["spread"] < 0.15)
    ck("the tracker generator is not", t5["spread"] > 0.3)
    ck("and they have comparable mean foreclosure, so the diagnostic is not "
       "just reading the mean", abs(f5["mean"] - t5["mean"]) < 0.35)

    ck("diagnose returns FILTER on the filter",
       diagnose(f5)["verdict"] == "FILTER")
    ck("and TRACKING on the tracker", diagnose(t5)["verdict"] == "TRACKING")

    nt = null_test(trials=60)
    ck("the diagnostic grades OK on known inputs", nt["grade"] == "OK")
    ck("it is not CONSTANT_SILENT", nt["true_tracking_rate"] > 0.0)
    ck("it is not CONSTANT_FIRES", nt["false_filter_rate"] < 1.0)

    pw = power(trials=40)
    ck("a smallest adequate design exists", pw["smallest_ok"] is not None)
    ck("the stated range diagnostic DEGRADES as difficulty levels are "
       "added at fixed n -- against expectation, and the reason it needs "
       "replacing",
       [r for r in pw["rows"] if r["levels"] == 9 and r["n"] == 20][0]["fpr"]
       > [r for r in pw["rows"] if r["levels"] == 2 and r["n"] == 20][0]
       ["fpr"])
    sc = statistic_comparison(trials=40)
    ck("the slope statistic does not degrade the same way",
       sc[-1]["slope_fpr"] < sc[-1]["range_fpr"])
    ck("and it still separates the generators at the widest design",
       null_test_slope(levels=9, n=20, trials=40)["grade"] != "CONSTANT_FIRES")

    cs = corpus_state()
    ck("no response is scored anywhere", cs["responses_scored_here"] == 0)
    ck("no target has a corpus", cs["targets_with_a_corpus"] == 0)
    ck("the unbuilt classification step leads the breaks list",
       "CLASSIFICATION STEP" in breaks()[0])
    ck("the one-directional bias from difficulty error is named",
       any("ONE direction" in b for b in breaks()))
    ck("UNCLASSIFIABLE is declared and disclosed as unexercised",
       "UNCLASSIFIABLE" in CLASSES
       and any("UNCLASSIFIABLE" in b for b in breaks()))
    ck("confidence records that nothing real was measured",
       "NONE" in confidence()["any_real_measurement"])
    ck("report renders", "graded on known inputs" in report().lower())
    return done()


if __name__ == "__main__":
    sys.exit(SH.run(sys.modules[__name__], "S6"))
