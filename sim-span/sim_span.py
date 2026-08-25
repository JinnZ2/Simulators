#!/usr/bin/env python3
"""SIM-SPAN -- can a span-reporting rule manufacture a U?

Question. Can a span-reporting rule manufacture a U between reported sleep
duration and an outcome, when no U exists in true sleep?

Null (as specified). True sleep has a flat OR monotone relation to the
outcome. If a U appears on the reported axis, the reporting rule produced
it.

Mechanism under test. `span` is time in bed: true sleep plus time spent
awake during awakenings. A reporter who states span is stating a quantity
that mixes two independent variables. Bin an outcome by that mixture and
the two populations at the top of the axis -- long sleepers, and short
fragmented sleepers -- are averaged together.

stdlib only. CC0. Parses under Python 3.9. Phone-buildable.

    python3 sim_span.py                 # all three legs, then the sweeps
    python3 sim_span.py --leg mono      # one leg
    python3 sim_span.py --selftest
"""

import math
import random
import sys

# --------------------------------------------------------------------------
# [CHOICE] UNITS. The spec gives `wake_cost` in MINUTES per awakening and
# writes `span = true_sleep + frag * wake_cost`, with true_sleep in HOURS.
# Taken literally that adds minutes to hours -- mean frag 2 at 15 min/wake
# would add 30 HOURS to a night's sleep. Implemented dimensionally, with
# the conversion explicit. Recorded in RESULTS.md rather than silently
# fixed.
# --------------------------------------------------------------------------

MIN_PER_HOUR = 60.0

# [CHOICE] all invented; no value here is sourced from a sleep study.
SLEEP_MEAN, SLEEP_SD = 7.0, 1.1
SLEEP_LO, SLEEP_HI = 3.0, 11.0
FRAG_MEAN = 2.0
WAKE_MEAN = 15.0            # minutes per awakening
NOISE_SD = 1.0
MONO_SLOPE = -1.0           # outcome units per hour of true sleep
FRAG_SLOPE = 1.5            # outcome units per awakening
HALF_HOUR = 0.5
MIN_PER_BIN = 20            # bins thinner than this are dropped
INTERIOR = 0.10             # vertex must sit inside the middle 80% of range
# A U has to TURN. Convexity plus an interior vertex is not enough: a
# monotone rising curve fits a positive quadratic whose vertex sits just
# inside the left margin, and the first version of this detector scored
# those as Us. Both arms must rise by MARGIN times the residual scatter of
# the bin means about the fit -- a reasoning-gate G-RES pair, the feature
# against the instrument's own noise, with the margin named.
MARGIN = 2.0
# [CHOICE] where published U-shaped sleep-duration minima are reported to
# sit. Used only to ask WHERE a manufactured U lands, never to score one.
PUBLISHED_WINDOW = (6.0, 9.0)

LEGS = ("flat", "mono", "frag_driven")


# --------------------------------------------------------------------------
# population
# --------------------------------------------------------------------------

def _poisson(rng, lam):
    """Knuth. lam is small here, so the loop is short."""
    el, k, p = math.exp(-lam), 0, 1.0
    while True:
        p *= rng.random()
        if p <= el:
            return k
        k += 1


def agents(n, rng, frag_mean=FRAG_MEAN, wake_mean=WAKE_MEAN):
    """true_sleep, frag and wake_cost, drawn INDEPENDENTLY.

    Independence of frag and true_sleep is the spec's own stated
    assumption and is probably false of real sleepers. See RESULTS.md.
    """
    out = []
    for _ in range(n):
        ts = min(SLEEP_HI, max(SLEEP_LO, rng.gauss(SLEEP_MEAN, SLEEP_SD)))
        frag = _poisson(rng, frag_mean)
        # per-agent minutes awake per awakening, positive, right-skewed
        wc = wake_mean * math.exp(rng.gauss(0.0, 0.5)) / math.exp(0.125)
        out.append({"true_sleep": ts, "frag": frag, "wake_cost": wc})
    return out


def add_span(pop):
    for a in pop:
        a["span"] = a["true_sleep"] + a["frag"] * a["wake_cost"] / MIN_PER_HOUR
    return pop


def round_half(x, width=HALF_HOUR):
    """Nearest half hour, ties UP.

    [CHOICE] Python's round() is banker's rounding: round(7.25/0.5) is 14,
    not 15, so 7.25 h would report as 7.0. The spec says "rounded to the
    nearest half hour" and does not state a tie rule. Ties-up is chosen
    because it is what a reader assumes, and because a tie rule that
    alternates direction is a second reporting artifact inside the one
    being measured. Recorded in RESULTS.md.
    """
    return math.floor(x / width + 0.5) * width


def add_reported(pop, p, rng):
    """Fraction `p` report span; the rest report true sleep.

    [CHOICE] both are rounded to the half hour, so the two sub-populations
    land on one comparable axis. Rounding only the span-reporters would
    make `p` a rounding sweep as well as a mixture sweep.
    """
    for a in pop:
        a["reports_span"] = rng.random() < p
        raw = a["span"] if a["reports_span"] else a["true_sleep"]
        a["reported"] = round_half(raw)
    return pop


def add_outcome(pop, leg, rng):
    for a in pop:
        if leg == "flat":
            base = 0.0
        elif leg == "mono":
            base = MONO_SLOPE * a["true_sleep"]
        elif leg == "frag_driven":
            base = FRAG_SLOPE * a["frag"]
        else:
            raise ValueError("unknown leg: %s" % leg)
        a["outcome"] = base + rng.gauss(0.0, NOISE_SD)
    return pop


# --------------------------------------------------------------------------
# measurement
# --------------------------------------------------------------------------

def bin_means(pop, axis, width=HALF_HOUR, min_per_bin=MIN_PER_BIN):
    buckets = {}
    for a in pop:
        k = round_half(a[axis], width)
        buckets.setdefault(k, []).append(a["outcome"])
    xs, ys, ns = [], [], []
    for k in sorted(buckets):
        v = buckets[k]
        if len(v) < min_per_bin:
            continue
        xs.append(k)
        ys.append(sum(v) / float(len(v)))
        ns.append(len(v))
    return xs, ys, ns


def quad_fit(xs, ys):
    """Least squares y = a x^2 + b x + c. Unweighted, 3x3 by elimination.

    Unweighted because the spec says 'take mean outcome per bin, fit a
    quadratic' -- the bin mean is the datum. Sparse extreme bins are
    dropped by min_per_bin rather than down-weighted.
    """
    n = len(xs)
    if n < 3:
        return None
    s = [0.0] * 5
    t = [0.0] * 3
    for x, y in zip(xs, ys):
        xp = 1.0
        for i in range(5):
            s[i] += xp
            xp *= x
        t[0] += y
        t[1] += y * x
        t[2] += y * x * x
    m = [[s[2], s[1], s[0], t[0]],
         [s[3], s[2], s[1], t[1]],
         [s[4], s[3], s[2], t[2]]]
    # rows are [x^2, x, 1 | rhs] for the three moment equations
    m = [[m[0][0], m[0][1], m[0][2], m[0][3]],
         [m[1][0], m[1][1], m[1][2], m[1][3]],
         [m[2][0], m[2][1], m[2][2], m[2][3]]]
    for col in range(3):
        piv = max(range(col, 3), key=lambda r: abs(m[r][col]))
        if abs(m[piv][col]) < 1e-12:
            return None
        m[col], m[piv] = m[piv], m[col]
        pv = m[col][col]
        for j in range(col, 4):
            m[col][j] /= pv
        for r in range(3):
            if r != col and m[r][col] != 0.0:
                f = m[r][col]
                for j in range(col, 4):
                    m[r][j] -= f * m[col][j]
    return m[0][3], m[1][3], m[2][3]      # a, b, c


def read_axis(pop, axis):
    """Sign of the quadratic term and where the minimum sits."""
    xs, ys, ns = bin_means(pop, axis)
    fit = quad_fit(xs, ys)
    if fit is None:
        return {"axis": axis, "n_bins": len(xs), "a": None, "vertex": None,
                "is_u": False, "why": "fewer than 3 usable bins"}
    a, b, c = fit
    vertex = -b / (2.0 * a) if a != 0 else None
    lo, hi = min(xs), max(xs)
    span = hi - lo
    interior = (vertex is not None and span > 0
                and lo + INTERIOR * span < vertex < hi - INTERIOR * span)

    def f(x):
        return a * x * x + b * x + c

    resid = math.sqrt(sum((y - f(x)) ** 2 for x, y in zip(xs, ys))
                      / float(len(xs)))
    if vertex is None:
        left = right = 0.0
    else:
        left = f(lo) - f(vertex)
        right = f(hi) - f(vertex)
    turns = (interior and resid > 0
             and left > MARGIN * resid and right > MARGIN * resid)
    is_u = bool(a > 0 and turns)

    if a <= 0:
        why = "concave"
    elif not interior:
        why = "minimum outside the range"
    elif not turns:
        why = "convex, interior, but does not turn: arms %.2f/%.2f vs %.1fx scatter %.2f" % (
            left, right, MARGIN, resid)
    else:
        why = "U: turns on both arms"

    return {"axis": axis, "n_bins": len(xs), "a": a, "vertex": vertex,
            "lo": lo, "hi": hi, "interior": interior, "resid": resid,
            "left_rise": left, "right_rise": right,
            "is_u": is_u, "why": why}


def in_published_window(vertex):
    lo, hi = PUBLISHED_WINDOW
    return vertex is not None and lo <= vertex <= hi


def one_run(n, leg, p, seed, frag_mean=FRAG_MEAN, wake_mean=WAKE_MEAN):
    rng = random.Random(seed)
    pop = add_outcome(
        add_reported(add_span(agents(n, rng, frag_mean, wake_mean)), p, rng),
        leg, rng)
    return {"reported": read_axis(pop, "reported"),
            "true": read_axis(pop, "true_sleep"), "pop": pop}


def u_rate(n, leg, p, seeds, frag_mean=FRAG_MEAN, wake_mean=WAKE_MEAN):
    """Fraction of independent runs showing a U, on each axis.

    The rate across seeds IS the statistic. A single run's quadratic sign
    is a coin flip on noise; the control axis is run on the same seeds so
    the two rates are paired.
    """
    rep = tru = 0
    for s in range(seeds):
        r = one_run(n, leg, p, 1000 + s, frag_mean, wake_mean)
        rep += 1 if r["reported"]["is_u"] else 0
        tru += 1 if r["true"]["is_u"] else 0
    return rep / float(seeds), tru / float(seeds), seeds


# --------------------------------------------------------------------------
# WHERE the manufactured U lands
#
# The spec asks whether a U can be manufactured and where it appears and
# disappears. It can. The sharper question, which the spec does not ask
# and which this sim can answer, is whether it lands where the published
# one does. A U at the wrong place on the axis is not an explanation of a
# U at the right place.
# --------------------------------------------------------------------------

GRID_FRAG = (0.5, 1.0, 2.0, 3.0, 4.0, 6.0, 8.0, 12.0)
GRID_WAKE = (5.0, 10.0, 15.0, 20.0, 30.0, 45.0, 60.0, 90.0, 120.0)
GRID_P = (0.10, 0.25, 0.50, 0.75, 1.0)


def vertex_floor(leg="mono", n=20000, seed=1000):
    """Grid the three swept parameters; return every U and its vertex."""
    hits, tried = [], 0
    for fm in GRID_FRAG:
        for wm in GRID_WAKE:
            for p in GRID_P:
                tried += 1
                d = one_run(n, leg, p, seed, fm, wm)["reported"]
                if d["is_u"]:
                    hits.append({"vertex": d["vertex"], "frag": fm,
                                 "wake": wm, "p": p, "a": d["a"],
                                 "lo": d["lo"], "hi": d["hi"]})
    hits.sort(key=lambda h: h["vertex"])
    return {"tried": tried, "hits": hits,
            "floor": hits[0]["vertex"] if hits else None,
            "in_window": [h for h in hits if in_published_window(h["vertex"])]}


# --------------------------------------------------------------------------
# report
# --------------------------------------------------------------------------

N = 20000
SEEDS = 40


def leg_block(leg, n=N, seeds=SEEDS):
    print("LEG  %s" % leg)
    r = one_run(n, leg, 1.0, 1000)
    for k in ("reported", "true"):
        d = r[k]
        av = "%+.4f" % d["a"] if d["a"] is not None else "--"
        vx = "%.2f" % d["vertex"] if d["vertex"] is not None else "--"
        print("  %-9s bins %2d   a %-10s vertex %-7s %s"
              % (d["axis"], d["n_bins"], av, vx, d["why"]))
    rep, tru, ns = u_rate(n, leg, 1.0, seeds)
    print("  U rate over %d seeds:  reported %.2f   true %.2f" % (ns, rep, tru))
    print()
    return rep, tru


def sweep_p(leg, n=N, seeds=20):
    print("  sweep p (fraction reporting span), leg=%s" % leg)
    print("    %-6s %-12s %s" % ("p", "U rate rep", "U rate true"))
    out = []
    for p in (0.0, 0.25, 0.5, 0.75, 1.0):
        rep, tru, _ = u_rate(n, leg, p, seeds)
        print("    %-6.2f %-12.2f %.2f" % (p, rep, tru))
        out.append((p, rep, tru))
    print()
    return out


def sweep_frag(leg, n=N, seeds=20):
    print("  sweep mean frag, leg=%s, p=1.0" % leg)
    print("    %-6s %-12s %s" % ("frag", "U rate rep", "U rate true"))
    out = []
    for fm in (0.0, 0.5, 1.0, 2.0, 4.0, 8.0):
        rep, tru, _ = u_rate(n, leg, 1.0, seeds, frag_mean=fm)
        print("    %-6.1f %-12.2f %.2f" % (fm, rep, tru))
        out.append((fm, rep, tru))
    print()
    return out


def sweep_wake(leg, n=N, seeds=20):
    print("  sweep mean wake_cost (min), leg=%s, p=1.0" % leg)
    print("    %-6s %-12s %s" % ("wake", "U rate rep", "U rate true"))
    out = []
    for wm in (0.0, 5.0, 15.0, 30.0, 60.0, 120.0):
        rep, tru, _ = u_rate(n, leg, 1.0, seeds, wake_mean=wm)
        print("    %-6.0f %-12.2f %.2f" % (wm, rep, tru))
        out.append((wm, rep, tru))
    print()
    return out


def report():
    print("SIM-SPAN   can a span-reporting rule manufacture a U?")
    print("N=%d per run, %d seeds per rate, p=1.0 unless swept\n" % (N, SEEDS))
    rates = {}
    for leg in LEGS:
        rates[leg] = leg_block(leg)
    print("-" * 66)
    print("SWEEPS\n")
    for leg in LEGS:
        sweep_p(leg)
    sweep_frag("mono")
    sweep_wake("mono")
    print("-" * 66)
    print("WHERE THE MANUFACTURED U LANDS")
    print("  %d parameter combinations per leg (frag x wake x p)."
          % (len(GRID_FRAG) * len(GRID_WAKE) * len(GRID_P)))
    print("  A U at the wrong place on the axis does not explain a U at the")
    print("  right one, so the vertex is reported, not just the sign.\n")
    print("  %-13s %-8s %-16s %s"
          % ("leg", "U found", "in %.0f-%.0f h window" % PUBLISHED_WINDOW,
             "lowest vertex"))
    print("  " + "-" * 60)
    vfs = {}
    for leg in LEGS:
        vf = vertex_floor(leg)
        vfs[leg] = vf
        print("  %-13s %-8d %-16d %s"
              % (leg, len(vf["hits"]), len(vf["in_window"]),
                 ("%.2f h" % vf["floor"]) if vf["floor"] is not None else "--"))
    print()
    for leg in LEGS:
        vf = vfs[leg]
        if not vf["hits"]:
            continue
        print("  %s -- lowest three:" % leg)
        for h in vf["hits"][:3]:
            print("    v=%-7.2f frag=%-5.1f wake=%-5.0f p=%-5.2f a=%+.4f  "
                  "range %.1f-%.1f"
                  % (h["vertex"], h["frag"], h["wake"], h["p"], h["a"],
                     h["lo"], h["hi"]))
    print()
    print("-" * 66)
    print("FALSIFIER, as the spec states it")
    print("  'If no combination produces a U on the reported axis under the")
    print("   flat null, the reporting artifact cannot explain the published")
    print("   U on its own, and the finding survives this objection.'")
    print()
    print("  flat        U rate on reported: %.2f" % rates["flat"][0])
    print("  mono        U rate on reported: %.2f" % rates["mono"][0])
    print("  frag_driven U rate on reported: %.2f" % rates["frag_driven"][0])
    print()
    print("  The spec's NULL is 'flat OR monotone'. Its FALSIFIER is scoped")
    print("  to FLAT alone. Those are different sets, and the legs disagree,")
    print("  so which one is run decides the answer. See RESULTS.md.")
    return rates, vfs


# --------------------------------------------------------------------------

def selftest():
    fails = []

    # quad_fit against answers fixed in advance.
    xs = [-2.0, -1.0, 0.0, 1.0, 2.0]
    exact = [2.0 * x * x - 3.0 * x + 5.0 for x in xs]
    a, b, c = quad_fit(xs, exact)
    if abs(a - 2) > 1e-9 or abs(b + 3) > 1e-9 or abs(c - 5) > 1e-9:
        fails.append("quad_fit does not recover an exact parabola: "
                     "%.6f %.6f %.6f" % (a, b, c))
    lin = [3.0 * x + 1.0 for x in xs]
    a2, b2, c2 = quad_fit(xs, lin)
    if abs(a2) > 1e-9 or abs(b2 - 3) > 1e-9 or abs(c2 - 1) > 1e-9:
        fails.append("quad_fit invents curvature in a straight line: "
                     "a=%.3e" % a2)
    if quad_fit([1.0, 2.0], [1.0, 2.0]) is not None:
        fails.append("quad_fit fitted a quadratic to two points")

    # units: the conversion must be present, or span is nonsense.
    rng = random.Random(7)
    pop = add_span(agents(400, rng, frag_mean=2.0, wake_mean=15.0))
    excess = sum(a["span"] - a["true_sleep"] for a in pop) / len(pop)
    if not (0.1 < excess < 2.0):
        fails.append("mean span excess %.2f h is not a plausible amount of "
                     "time awake in bed; the unit conversion is wrong"
                     % excess)

    # p=0 must put every reporter on the true axis.
    rng = random.Random(9)
    pop = add_reported(add_span(agents(300, rng)), 0.0, rng)
    if any(a["reports_span"] for a in pop):
        fails.append("p=0 still produced span reporters")
    if any(abs(a["reported"] - round_half(a["true_sleep"])) > 1e-12
           for a in pop):
        fails.append("p=0 reported axis is not the true axis")

    # frag_mean=0 removes the mechanism entirely: span must equal true.
    rng = random.Random(11)
    pop = add_span(agents(300, rng, frag_mean=0.0))
    if any(abs(a["span"] - a["true_sleep"]) > 1e-12 for a in pop):
        fails.append("frag_mean=0 still moved span off true_sleep")

    # the detector must be able to say NO, or it is CONSTANT_FIRES.
    flat_rep, _flat_tru, _ = u_rate(4000, "flat", 1.0, 12)
    if flat_rep > 0.99:
        fails.append("the U detector fires on the flat leg at rate %.2f; it "
                     "cannot return a negative" % flat_rep)
    # ...and able to say YES, or it is CONSTANT_SILENT. At the spec's own
    # default frag/wake the mono leg does NOT fire -- the curvature is
    # there but the vertex sits outside the reported range -- so the
    # positive control has to be run where the mechanism is live. That
    # fact is a result, not a nuisance: see RESULTS.md.
    mono_rep, _mono_tru, _ = u_rate(8000, "mono", 1.0, 12, wake_mean=45.0)
    if mono_rep < 0.01:
        fails.append("the U detector never fires on the mono leg even at "
                     "wake_mean=45; it cannot return a positive")
    # and the default really must be quiet, or the line above is untrue
    d = one_run(20000, "mono", 1.0, 1000)["reported"]
    if d["is_u"]:
        fails.append("the mono leg now fires at the spec's default "
                     "frag/wake; RESULTS.md must be restated")

    # every manufactured U must land above the published window, or the
    # headline finding is refuted.
    vf = vertex_floor("mono", n=8000)
    if vf["in_window"]:
        fails.append("a manufactured U landed inside the published %.0f-%.0f h "
                     "window (%d combinations); the headline finding is "
                     "REFUTED and RESULTS.md must be rewritten"
                     % (PUBLISHED_WINDOW[0], PUBLISHED_WINDOW[1],
                        len(vf["in_window"])))
    if not vf["hits"]:
        fails.append("no combination produced a U at all; the sweep no "
                     "longer exercises the mechanism")

    # rounding
    for raw, want in ((7.24, 7.0), (7.25, 7.5), (7.75, 8.0), (6.9, 7.0)):
        if abs(round_half(raw) - want) > 1e-12:
            fails.append("round_half(%.2f) = %.2f, expected %.2f"
                         % (raw, round_half(raw), want))

    for f in fails:
        print("FAIL: " + f)
    print("SELFTEST %s (%d checks failed)"
          % ("PASS" if not fails else "FAIL", len(fails)))
    return 1 if fails else 0


def main(argv):
    if "--selftest" in argv:
        return selftest()
    if "--leg" in argv:
        leg = argv[argv.index("--leg") + 1]
        leg_block(leg)
        sweep_p(leg)
        return 0
    report()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
