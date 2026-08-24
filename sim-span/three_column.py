#!/usr/bin/env python3
"""The three-column test from NOTES_INSTRUMENT.md, run against the sim.

The note proposes:

    reported hours minus measured sleep, regressed on awakening count and
    awakening duration. If the gap grows with fragmentation, G-SPAN is
    confirmed on real people.

Three things about that are checkable here, because `sim_span.py` knows
the truth it is generating.

    1. The stated form is ADDITIVE and the quantity is a PRODUCT.
       gap = frag * wake_cost by construction, so `gap ~ count + duration`
       is misspecified. Fit the product.

    2. The test does more than confirm or deny. Under a mixture where a
       fraction p report span, E[gap | product] = p * product exactly, so
       THE SLOPE IS AN ESTIMATOR OF p -- the one quantity RESULTS.md said
       nobody reports.

    3. The note's "one flag" is load-bearing on that estimate rather than
       a nice-to-have. A self-report is a person's USUAL; a single night
       is one draw. Regressing on one night's fragmentation is
       errors-in-variables in the PREDICTOR, which attenuates.

stdlib only. CC0. Parses under Python 3.9.

    python3 three_column.py
    python3 three_column.py --selftest
"""

import math
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import sim_span as S  # noqa: E402


def ols(ys, cols):
    """Least squares with an intercept. Returns (beta, r_squared).

    beta[0] is the intercept; beta[i+1] is the coefficient on cols[i].
    Gaussian elimination on the normal equations; no numpy.
    """
    n, k = len(ys), len(cols) + 1
    if n <= k:
        return None, float("nan")
    rows = [[1.0] + [c[i] for c in cols] for i in range(n)]
    a = [[sum(rows[i][x] * rows[i][y] for i in range(n)) for y in range(k)]
         + [sum(rows[i][x] * ys[i] for i in range(n))] for x in range(k)]
    for c in range(k):
        piv = max(range(c, k), key=lambda r: abs(a[r][c]))
        if abs(a[piv][c]) < 1e-14:
            return None, float("nan")
        a[c], a[piv] = a[piv], a[c]
        pv = a[c][c]
        for j in range(c, k + 1):
            a[c][j] /= pv
        for r in range(k):
            if r != c and a[r][c] != 0.0:
                f = a[r][c]
                for j in range(c, k + 1):
                    a[r][j] -= f * a[c][j]
    beta = [a[i][k] for i in range(k)]
    ybar = sum(ys) / n
    sst = sum((y - ybar) ** 2 for y in ys)
    fit = [sum(beta[x] * rows[i][x] for x in range(k)) for i in range(n)]
    sse = sum((ys[i] - fit[i]) ** 2 for i in range(n))
    return beta, (1.0 - sse / sst) if sst > 0 else float("nan")


def ols_coef(which):
    """Known-answer handle. Exact fits, so the answer is fixed in advance."""
    xs = [0.0, 1.0, 2.0, 3.0, 4.0]
    if which == "slope":
        return round(ols([2.0 + 3.0 * x for x in xs], [xs])[0][1], 12)
    if which == "intercept":
        return round(ols([2.0 + 3.0 * x for x in xs], [xs])[0][0], 12)
    if which == "flat":
        return round(ols([5.0 for _x in xs], [xs])[0][1], 12)
    raise ValueError(which)


# --------------------------------------------------------------------------
# 1 & 2 -- one night per person, the sim's own population
# --------------------------------------------------------------------------

def three_column(p, n=20000, seed=4242):
    rng = random.Random(seed)
    pop = S.add_reported(S.add_span(S.agents(n, rng)), p, rng)
    gap = [a["reported"] - a["true_sleep"] for a in pop]
    product = [a["frag"] * a["wake_cost"] / 60.0 for a in pop]
    count = [float(a["frag"]) for a in pop]
    dur = [a["wake_cost"] / 60.0 for a in pop]
    bp, rp = ols(gap, [product])
    ba, ra = ols(gap, [count, dur])
    return {"p": p, "slope": bp[1], "intercept": bp[0], "r2_product": rp,
            "b_count": ba[1], "b_dur": ba[2], "r2_additive": ra}


# --------------------------------------------------------------------------
# 3 -- the note's flag, as a number
#
# A person has a USUAL sleep and a USUAL fragmentation, and reports the
# usual. Each observed night is a draw around it. Averaging k nights of
# the predictor is the whole of what the seven days buy.
# --------------------------------------------------------------------------

WITHIN_SD = 0.7          # [CHOICE] night-to-night sd of true sleep, hours
FRAG_BETWEEN_SD = 1.2    # [CHOICE] between-person sd of usual awakenings


def nightly(p, nights, n=20000, seed=99):
    rng = random.Random(seed)
    gaps, preds = [], []
    for _ in range(n):
        ts_mean = min(S.SLEEP_HI, max(S.SLEEP_LO,
                                      rng.gauss(S.SLEEP_MEAN, S.SLEEP_SD)))
        frag_mean = max(0.05, rng.gauss(S.FRAG_MEAN, FRAG_BETWEEN_SD))
        wc = S.WAKE_MEAN * math.exp(rng.gauss(0.0, 0.5)) / math.exp(0.125)
        usual_span = ts_mean + frag_mean * wc / 60.0
        raw = usual_span if rng.random() < p else ts_mean
        reported = S.round_half(raw)
        sleep_obs, prod_obs = [], []
        for _ in range(nights):
            ts = min(S.SLEEP_HI, max(S.SLEEP_LO, rng.gauss(ts_mean, WITHIN_SD)))
            fr = S._poisson(rng, frag_mean)
            sleep_obs.append(ts)
            prod_obs.append(fr * wc / 60.0)
        gaps.append(reported - sum(sleep_obs) / len(sleep_obs))
        preds.append(sum(prod_obs) / len(prod_obs))
    beta, r2 = ols(gaps, [preds])
    return {"p": p, "nights": nights, "slope": beta[1], "r2": r2,
            "recovered": beta[1] / p if p else float("nan")}


# --------------------------------------------------------------------------

def report():
    print("THE THREE-COLUMN TEST, run against the sim that proposed it\n")

    print("1  the stated form is additive; the quantity is a product")
    print("   gap = frag * wake_cost by construction, so `gap ~ count +")
    print("   duration` cannot represent it. Both fitted, same data:\n")
    print("   %-8s | %-9s %-10s %-8s | %-9s %-9s %s"
          % ("true p", "slope", "intercept", "R2", "b_count", "b_dur", "R2"))
    print("   " + "-" * 68)
    rows = [three_column(p) for p in (0.0, 0.25, 0.5, 0.75, 1.0)]
    for r in rows:
        print("   %-8.2f | %-9.4f %-10.4f %-8.4f | %-+9.4f %-+9.4f %.4f"
              % (r["p"], r["slope"], r["intercept"], r["r2_product"],
                 r["b_count"], r["b_dur"], r["r2_additive"]))
    print()
    print("   At p=1.0 the product form explains %.3f and the additive form"
          % rows[-1]["r2_product"])
    print("   %.3f of the variance. The additive coefficients scale with p"
          % rows[-1]["r2_additive"])
    print("   and neither of them IS p.")
    print()

    print("2  the slope of the product form estimates p")
    err = max(abs(r["slope"] - r["p"]) for r in rows)
    print("   max error across the five levels: %.4f" % err)
    print("   intercept stays at zero throughout, as it must if the")
    print("   true-reporters contribute a gap of zero.")
    print()
    print("   E[gap | product] = p * product exactly: a span-reporter's gap")
    print("   IS their WASO and a true-reporter's is zero, so the mixture's")
    print("   conditional mean is p times the product. The test does not")
    print("   only confirm or deny -- it MEASURES the quantity RESULTS.md")
    print("   said nobody reports.")
    print()

    print("3  the note's 'one flag' is worth a factor of two")
    print("   A self-report is a person's USUAL. A single night is one draw.")
    print("   Regressing on one night's fragmentation is errors-in-variables")
    print("   in the PREDICTOR, which attenuates toward zero.\n")
    print("   %-8s %-12s %-12s %-12s %s"
          % ("true p", "1 night", "7 nights", "1-night", "7-night"))
    print("   " + "-" * 62)
    for p in (0.25, 0.50, 0.75, 1.00):
        a, b = nightly(p, 1), nightly(p, 7)
        print("   %-8.2f %-12.4f %-12.4f %-12s %s"
              % (p, a["slope"], b["slope"],
                 "%.0f%% of p" % (100 * a["recovered"]),
                 "%.0f%% of p" % (100 * b["recovered"])))
    print()
    print("   One night recovers about HALF of p. Seven recover most of it.")
    print("   The note offers the seven days as something you can 'also")
    print("   check'; they are load-bearing on the headline number, and a")
    print("   single-night design would report p at half its value.")
    print()


def selftest():
    fails = []

    # ols against answers fixed in advance
    if abs(ols_coef("slope") - 3.0) > 1e-9:
        fails.append("ols does not recover an exact slope: %r"
                     % ols_coef("slope"))
    if abs(ols_coef("intercept") - 2.0) > 1e-9:
        fails.append("ols does not recover an exact intercept: %r"
                     % ols_coef("intercept"))
    if abs(ols_coef("flat")) > 1e-9:
        fails.append("ols invents a slope in constant data: %r"
                     % ols_coef("flat"))
    if ols([1.0, 2.0], [[1.0, 2.0]])[0] is not None:
        fails.append("ols fitted two parameters to two points")

    # finding 2: the slope must track p, or it is not an estimator.
    rows = [three_column(p, n=8000) for p in (0.0, 0.5, 1.0)]
    err = max(abs(r["slope"] - r["p"]) for r in rows)
    if err > 0.05:
        fails.append("the slope no longer estimates p (max error %.4f); "
                     "finding 2 must be restated" % err)
    # ...and it must be able to return zero, or it is CONSTANT_FIRES.
    if abs(rows[0]["slope"]) > 0.05:
        fails.append("the slope is non-zero at p=0 (%.4f); it cannot return "
                     "a negative result" % rows[0]["slope"])

    # finding 1: the product form must beat the additive one at p=1.
    top = three_column(1.0, n=8000)
    if not top["r2_product"] > top["r2_additive"]:
        fails.append("the additive form now fits at least as well "
                     "(%.4f vs %.4f); finding 1 must be restated"
                     % (top["r2_additive"], top["r2_product"]))

    # finding 3: one night must attenuate, or the flag is not load-bearing.
    one, seven = nightly(1.0, 1, n=6000), nightly(1.0, 7, n=6000)
    if not one["slope"] < seven["slope"] - 0.1:
        fails.append("averaging nights no longer recovers slope (1: %.4f, "
                     "7: %.4f); finding 3 must be restated"
                     % (one["slope"], seven["slope"]))
    if one["recovered"] > 0.75:
        fails.append("one night now recovers %.0f%% of p; the 'factor of "
                     "two' must be restated" % (100 * one["recovered"]))

    for f in fails:
        print("FAIL: " + f)
    print("SELFTEST %s (%d checks failed)"
          % ("PASS" if not fails else "FAIL", len(fails)))
    return 1 if fails else 0


def main(argv):
    if "--selftest" in argv:
        return selftest()
    report()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
