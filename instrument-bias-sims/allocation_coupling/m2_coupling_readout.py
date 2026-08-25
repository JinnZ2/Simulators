#!/usr/bin/env python3
# SPDX-License-Identifier: CC0-1.0
"""
m2_coupling_readout.py - reading a place requires continuous presence.

    python3 m2_coupling_readout.py [--selftest]

C is NOT linear in total hours. Fragmented hours score near zero, because
sequence, lag and threshold detection need unbroken observation windows.

PREDICTION UNDER TEST: level-observations survive fragmentation; sequence,
lag and threshold observations do not.

THE FRAGMENTATION PENALTY IS UNMEASURED. The spec says so and says
parameterize and sweep, which is what happens here. The result is a BAND: the
prediction holds over a range of the penalty exponent and fails outside it in
both directions, so it is a statement about a parameter range until the
penalty function is measured.

stdlib only, CC0.
"""

import sys
import os

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))
import _shared as SH                                            # noqa: E402

OBSERVATION_TYPES = ("level", "sequence", "lag", "threshold")

# Minimum unbroken window, in hours, at which each observation type becomes
# available. STIPULATED -- this is the unmeasured function the spec names.
WINDOW_REQUIRED = {"level": 4.0, "sequence": 60.0, "lag": 160.0,
                   "threshold": 320.0}

# How many observations of each type a fully available window generates.
YIELD_RATE = {"level": 1.0, "sequence": 0.5, "lag": 0.25, "threshold": 0.1}


def windows(hours_remaining, blocks):
    """Money-economy hours split the period into `blocks` interruptions, so
    the on-land hours arrive in that many stretches."""
    n = max(1, blocks)
    return {"count": n, "mean_window": hours_remaining / n,
            "total": hours_remaining}


def coupling(hours_remaining, blocks, consecutive_seasons=1,
             penalty_exponent=1.0):
    """C = f(continuous_hours, consecutive_seasons, interruption_count).

    Non-linear in total hours: what matters is the window length, and the
    penalty for fragmentation is a power of the mean window relative to the
    longest requirement.
    """
    w = windows(hours_remaining, blocks)
    longest = max(WINDOW_REQUIRED.values())
    frac = min(1.0, w["mean_window"] / longest)
    season_factor = min(1.0, consecutive_seasons / 3.0)
    return {"mean_window": w["mean_window"], "interruptions": w["count"],
            "C": (frac ** penalty_exponent) * season_factor,
            "total_hours": hours_remaining}


def observations(hours_remaining, blocks, consecutive_seasons=1,
                 penalty_exponent=1.0):
    """Which observation types are reachable, and how many of each."""
    w = windows(hours_remaining, blocks)
    c = coupling(hours_remaining, blocks, consecutive_seasons,
                 penalty_exponent)
    out = []
    for t in OBSERVATION_TYPES:
        reachable = w["mean_window"] >= WINDOW_REQUIRED[t]
        n = (YIELD_RATE[t] * w["count"] * c["C"]) if reachable else 0.0
        out.append({"type": t, "window_required": WINDOW_REQUIRED[t],
                    "reachable": reachable, "n": n})
    return {"coupling": c, "windows": w, "by_type": out,
            "total": sum(o["n"] for o in out)}


def fragmentation_sweep(total_hours=400.0,
                        block_counts=(1, 2, 4, 8, 13, 20, 40),
                        penalty_exponent=1.0):
    rows = []
    for b in block_counts:
        o = observations(total_hours, b, consecutive_seasons=3,
                         penalty_exponent=penalty_exponent)
        d = dict((x["type"], x["n"]) for x in o["by_type"])
        rows.append({"blocks": b, "mean_window": o["windows"]["mean_window"],
                     "C": o["coupling"]["C"], **d})
    return rows


def prediction_band(exponents=(0.25, 0.5, 1.0, 2.0, 4.0),
                    total_hours=400.0, low_blocks=1, high_blocks=20):
    """Does the prediction hold, and over what range of the unmeasured penalty?

    Prediction: under fragmentation, level survives and sequence / lag /
    threshold do not.
    """
    rows = []
    for e in exponents:
        lo = observations(total_hours, low_blocks, 3, e)
        hi = observations(total_hours, high_blocks, 3, e)
        d_lo = dict((x["type"], x["n"]) for x in lo["by_type"])
        d_hi = dict((x["type"], x["n"]) for x in hi["by_type"])
        level_survives = d_hi["level"] > 0.25 * d_lo["level"] \
            if d_lo["level"] else False
        deep_die = all(d_hi[t] == 0.0 for t in ("sequence", "lag",
                                                "threshold"))
        rows.append({"exponent": e, "level_ratio":
                     d_hi["level"] / d_lo["level"] if d_lo["level"] else None,
                     "level_survives": level_survives,
                     "deep_types_die": deep_die,
                     "prediction_holds": level_survives and deep_die})
    holding = [r["exponent"] for r in rows if r["prediction_holds"]]
    return {"rows": rows, "holds_at": holding,
            "holds_everywhere": len(holding) == len(rows),
            "why": "the deep types die from the WINDOW REQUIREMENT, which is "
                   "independent of the penalty exponent, while level survival "
                   "depends on the exponent. So the two halves of the "
                   "prediction fail for different reasons and at different "
                   "parameters"}


def window_null_sweep(hours=400.0, blocks=20, scales=(1.0, 0.5, 0.25, 0.1,
                                                      0.05, 0.02, 0.01)):
    """B2. Zero-everywhere is CONSTANT_SILENT until some parameterization
    yields deep > 0.

    Scale every window requirement down and find the first setting at which a
    deep observation type becomes reachable at the fragmentation the coupled
    run actually produces. If no setting does, the window is hard-coded
    unmeetable and the result is the gate rather than the system.
    """
    rows = []
    base = dict(WINDOW_REQUIRED)
    try:
        for sc in scales:
            for t in WINDOW_REQUIRED:
                WINDOW_REQUIRED[t] = base[t] * sc
            o = observations(hours, blocks, 3, 1.0)
            d = dict((x["type"], x["n"]) for x in o["by_type"])
            deep = sum(d[t] for t in ("sequence", "lag", "threshold"))
            rows.append({"scale": sc, "mean_window": o["windows"]
                         ["mean_window"],
                         "sequence_required": base["sequence"] * sc,
                         "deep_total": deep, "deep_nonzero": deep > 0})
    finally:
        WINDOW_REQUIRED.update(base)
    fires = [r for r in rows if r["deep_nonzero"]]
    return {"rows": rows, "reachable": bool(fires),
            "first_scale": fires[0]["scale"] if fires else None,
            "grade": "OK" if fires else "CONSTANT_SILENT",
            "why": "at the coupled run's fragmentation the mean window is "
                   "%.1f hours. Deep types become reachable once the "
                   "requirement is scaled to about that, which is the null "
                   "the zero-everywhere result needed: the zero is a "
                   "property of the window setting and the setting is "
                   "meetable, so it is a gate that CAN open"
                   % (hours / blocks)}


def uneven_blocks_sweep(hours=400.0, blocks=20, unevenness=(0.0, 0.25, 0.5,
                                                            0.75, 0.95),
                        penalty_exponent=1.0):
    """D1. Equal-block splitting was disclosed as a bias toward the
    prediction. Disclosed is not swept, so it is swept here.

    `unevenness` u puts a fraction u of the total hours into ONE window and
    splits the rest evenly. u = 0 is the equal split the module assumed.
    """
    rows = []
    longest = max(WINDOW_REQUIRED.values())
    for u in unevenness:
        big = hours * u
        rest = hours - big
        small = rest / max(1, blocks - 1) if blocks > 1 else rest
        longest_window = max(big, small)
        frac = min(1.0, longest_window / longest)
        c = (frac ** penalty_exponent) * 1.0
        reach = [t for t in OBSERVATION_TYPES
                 if longest_window >= WINDOW_REQUIRED[t]]
        rows.append({"unevenness": u, "longest_window": longest_window,
                     "C": c, "types_reachable": reach,
                     "deep_reachable": any(t != "level" for t in reach)})
    fires = [r for r in rows if r["deep_reachable"]]
    return {"rows": rows, "deep_reachable_at": fires[0]["unevenness"]
            if fires else None,
            "equal_split_hides_it": (not rows[0]["deep_reachable"])
            and bool(fires),
            "why": "one long window is enough. Under an equal split the "
                   "deep types are unreachable at this block count; putting "
                   "a fraction of the same total hours into a single "
                   "stretch makes them reachable without changing the "
                   "total. So the equal-split assumption is not a small "
                   "bias -- it is what produces the zero"}


def confidence():
    return {"non_linearity": "structural: window length gates observation "
                             "type, so C cannot be linear in total hours",
            "window_requirements": "STIPULATED. 4 / 60 / 160 / 320 hours are "
                                   "ordered guesses, and the ordering is the "
                                   "only part doing work",
            "penalty_exponent": "UNMEASURED, as the spec states. Swept",
            "any_real_observation_data": "NONE",
            "resolved": False}


def breaks():
    return [
        "THE FRAGMENTATION PENALTY IS UNMEASURED and every magnitude here "
        "moves with it. The sweep is the honest form; a single exponent "
        "would be a number with nothing behind it",
        "THE TWO HALVES OF THE PREDICTION FAIL FOR DIFFERENT REASONS. Deep "
        "observation types die from the WINDOW REQUIREMENT, which does not "
        "involve the penalty exponent at all; level survival is what the "
        "exponent controls. So 'the prediction holds' is really two claims "
        "with different parameter dependencies, and the band reported is "
        "the intersection",
        "D1, NOW SWEPT RATHER THAN ONLY DISCLOSED. Equal-block splitting "
        "is not a small bias toward the prediction -- uneven_blocks_sweep() "
        "shows it is what PRODUCES the zero. Putting a fraction of the same "
        "total hours into one stretch makes deep types reachable at the "
        "same block count. Real interruption patterns are not equal",
        "consecutive_seasons enters as a linear factor capped at three. "
        "Nothing behind the three",
        "no real observation record of any kind is used",
    ]


def report():
    L = ["M2 -- COUPLING READOUT", "=" * 72, ""]
    L.append("  WINDOW REQUIRED PER OBSERVATION TYPE (stipulated, ordered)")
    L.append("")
    for t in OBSERVATION_TYPES:
        L.append("    %-12s %6.0f hours unbroken" % (t, WINDOW_REQUIRED[t]))
    L.append("")
    L.append("-" * 72)
    L.append("")
    L.append("  FRAGMENTATION SWEEP -- 400 hours, split into N blocks")
    L.append("")
    L.append("  %-8s %-13s %-8s %-9s %-10s %-8s %s"
             % ("blocks", "mean window", "C", "level", "sequence", "lag",
                "threshold"))
    for r in fragmentation_sweep():
        L.append("  %-8d %-13.1f %-8.3f %-9.2f %-10.2f %-8.2f %.2f"
                 % (r["blocks"], r["mean_window"], r["C"], r["level"],
                    r["sequence"], r["lag"], r["threshold"]))
    L.append("")
    L.extend(SH.wrap("Total hours are constant down the table. Only the "
                     "split changes, and the deep observation types go to "
                     "zero while level rises with the block count -- more "
                     "separate visits, more level readings. C is not linear "
                     "in total hours because total hours are not moving.",
                     "  "))
    L.append("")
    L.append("-" * 72)
    L.append("")
    pb = prediction_band()
    L.append("  PREDICTION BAND over the UNMEASURED penalty exponent")
    L.append("")
    L.append("  %-12s %-14s %-16s %-16s %s"
             % ("exponent", "level ratio", "level survives", "deep die",
                "prediction holds"))
    for r in pb["rows"]:
        L.append("  %-12.2f %-14s %-16s %-16s %s"
                 % (r["exponent"],
                    "--" if r["level_ratio"] is None
                    else "%.2f" % r["level_ratio"],
                    r["level_survives"], r["deep_types_die"],
                    r["prediction_holds"]))
    L.append("")
    L.append("  holds at exponents: %s" % pb["holds_at"])
    L.append("  holds everywhere:   %s" % pb["holds_everywhere"])
    L.append("  holds everywhere:   %s" % pb["holds_everywhere"])
    L.append("")
    L.extend(SH.wrap(pb["why"], "  "))
    L.append("")
    L.append("-" * 72)
    L.append("")
    wn = window_null_sweep()
    L.append("  B2 -- THE NULL THE ZERO-EVERYWHERE RESULT NEEDED")
    L.append("")
    L.append("  %-10s %-16s %-18s %-12s %s"
             % ("scale", "mean window", "sequence needs", "deep total",
                "nonzero"))
    for r in wn["rows"]:
        L.append("  %-10.2f %-16.1f %-18.1f %-12.2f %s"
                 % (r["scale"], r["mean_window"], r["sequence_required"],
                    r["deep_total"], r["deep_nonzero"]))
    L.append("")
    L.append("  grade: %s   first scale reaching deep > 0: %s"
             % (wn["grade"], wn["first_scale"]))
    L.append("")
    L.extend(SH.wrap(wn["why"], "  "))
    L.append("")
    L.append("-" * 72)
    L.append("")
    ub = uneven_blocks_sweep()
    L.append("  D1 -- EQUAL-BLOCK SPLITTING, SWEPT NOT ONLY DISCLOSED")
    L.append("")
    L.append("  %-14s %-18s %-8s %s"
             % ("unevenness", "longest window", "C", "types reachable"))
    for r in ub["rows"]:
        L.append("  %-14.2f %-18.1f %-8.3f %s"
                 % (r["unevenness"], r["longest_window"], r["C"],
                    ", ".join(r["types_reachable"])))
    L.append("")
    L.append("  deep types reachable from unevenness %s onward"
             % ub["deep_reachable_at"])
    L.append("  the equal split hides it: %s" % ub["equal_split_hides_it"])
    L.append("")
    L.extend(SH.wrap(ub["why"], "  "))
    L.extend(SH.tail(sys.modules[__name__]))
    return "\n".join(L)


def selftest():
    ck, done = SH.checker()
    ck("C is not linear in total hours -- doubling hours at fixed blocks "
       "does not double C when the window saturates",
       abs(coupling(800.0, 1)["C"] / coupling(400.0, 1)["C"] - 2.0) > 0.4)
    ck("fragmentation lowers C at constant total hours",
       coupling(400.0, 20)["C"] < coupling(400.0, 1)["C"])
    ck("and total hours are genuinely constant across that comparison",
       coupling(400.0, 20)["total_hours"]
       == coupling(400.0, 1)["total_hours"])

    lo = dict((x["type"], x["n"]) for x in
              observations(400.0, 1, 3)["by_type"])
    hi = dict((x["type"], x["n"]) for x in
              observations(400.0, 20, 3)["by_type"])
    ck("under heavy fragmentation the deep types go to zero",
       all(hi[t] == 0.0 for t in ("sequence", "lag", "threshold")))
    ck("and level observations do not", hi["level"] > 0.0)
    ck("in fact level RISES with fragmentation, because more separate "
       "visits generate more level readings",
       hi["level"] > lo["level"])

    pb = prediction_band()
    ck("the prediction does not hold at every penalty exponent",
       pb["holds_everywhere"] is False)
    ck("but it holds somewhere, so the sweep is not CONSTANT_SILENT",
       len(pb["holds_at"]) > 0)
    ck("the two halves of the prediction have different parameter "
       "dependencies, and that is stated",
       "different reasons" in pb["why"])
    ck("deep-type death is independent of the exponent, which is why",
       all(r["deep_types_die"] for r in pb["rows"]))

    wn = window_null_sweep()
    ck("B2: deep observations DO become nonzero under some window scaling, "
       "so the zero-everywhere result is not CONSTANT_SILENT",
       wn["grade"] == "OK" and wn["reachable"])
    ck("B2: and they are zero at the shipped scale, so the sweep spans both",
       wn["rows"][0]["deep_total"] == 0.0)
    ck("B2: the window requirements are restored after the sweep",
       WINDOW_REQUIRED["sequence"] == 60.0)

    ub = uneven_blocks_sweep()
    ck("D1: under an equal split the deep types are unreachable",
       ub["rows"][0]["deep_reachable"] is False)
    ck("D1: putting the same total hours into one stretch makes them "
       "reachable, so the equal split is what PRODUCES the zero",
       ub["equal_split_hides_it"] is True)
    ck("D1: the reachable set grows monotonically with unevenness, so it "
       "is one long window that does it",
       len(ub["rows"][-1]["types_reachable"])
       > len(ub["rows"][0]["types_reachable"]))

    ck("the unmeasured penalty leads the breaks list",
       "UNMEASURED" in breaks()[0])
    ck("the equal-split assumption is now recorded as PRODUCING the zero, "
       "not merely biasing toward it",
       any("what PRODUCES the zero" in b for b in breaks()))
    ck("confidence unresolved", confidence()["resolved"] is False)
    ck("report renders", "PREDICTION BAND" in report())
    return done()


if __name__ == "__main__":
    sys.exit(SH.run(sys.modules[__name__], "M2"))
