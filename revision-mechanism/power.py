#!/usr/bin/env python3
"""What the ask's sample size can and cannot deliver.

SOURCE_DROP.md asks for "One site pair, one domain." Comparison 2
predicts that a rate-mismatch threshold "should appear as a
DISCONTINUITY, not a slope."

This computes whether that is detectable at the asked-for n, and at
what n it becomes detectable. It uses no field data, touches no
community, and says nothing about any real site or any real body of
knowledge.

WHAT THIS FILE IS NOT
    It does not simulate a community, a tradition, a site, or a
    holder. There are no synthetic "sites" standing in for real ones.
    The only objects are two abstract functions -- a line and a step --
    and binomial sampling noise. Everything below is a statement about
    the DESIGN's arithmetic.

    The study itself cannot be run from here and this is not an
    attempt to run it. It requires fieldwork, collective consent, and
    a companion coding scheme (M1-M8) that is not in this repository
    and is not reconstructed.

THE RESULT IN ONE LINE
    A step and a slope through the same two endpoints are the same two
    points. n=2 cannot distinguish them at any per-site precision, and
    that is exact rather than statistical.

usage:  python3 power.py                # the report
        python3 power.py --selftest

CC0. stdlib only. Parses under Python 3.9. Deterministic given seeds.
"""

import math
import os
import random
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DROP = os.path.join(HERE, "SOURCE_DROP.md")

# ---- declared parameters. Every one a [CHOICE], none measured. ----
LO = 0.10        # held-obsolete rate well below the mismatch point
HI = 0.45        # held-obsolete rate well above it
BREAK = 1.0      # r = change rate / transmission cycle length
R_MIN, R_MAX = 0.2, 2.0
TRIALS = 400
SEED0 = 4242


def truth_step(r):
    """Comparison 2's prediction: a discontinuity."""
    return LO if r < BREAK else HI


def truth_slope(r):
    """The alternative it must be distinguished from, through the SAME
    endpoints -- otherwise the endpoints alone separate them and the
    shape is not what is being tested."""
    return LO + (HI - LO) * (r - R_MIN) / (R_MAX - R_MIN)


def sites(n):
    """n sites evenly spanning the rate ratio, endpoints included."""
    if n < 2:
        raise ValueError("a comparison takes at least two sites")
    if n == 2:
        return [R_MIN, R_MAX]
    return [R_MIN + (R_MAX - R_MIN) * i / (n - 1.0) for i in range(n)]


def observe(rs, truth, m_components, rng):
    """Held-obsolete rate per site: k of m components, binomial.

    m_components is the denominator the drop calls "the single most
    comparable number across sites" -- still-transmitted components at
    that site.
    """
    out = []
    for r in rs:
        p = truth(r)
        k = sum(1 for _ in range(m_components) if rng.random() < p)
        out.append(k / float(m_components))
    return out


def _sse(rs, ys, f):
    return sum((y - f(r)) ** 2 for r, y in zip(rs, ys))


def _fit_line(rs, ys):
    n = float(len(rs))
    mx, my = sum(rs) / n, sum(ys) / n
    den = sum((r - mx) ** 2 for r in rs)
    if den == 0:
        return lambda r: my
    b = sum((r - mx) * (y - my) for r, y in zip(rs, ys)) / den
    a = my - b * mx
    return lambda r: a + b * r


def _fit_step(rs, ys):
    lo = [y for r, y in zip(rs, ys) if r < BREAK]
    hi = [y for r, y in zip(rs, ys) if r >= BREAK]
    ml = sum(lo) / len(lo) if lo else 0.0
    mh = sum(hi) / len(hi) if hi else 0.0
    return lambda r: (ml if r < BREAK else mh)


def discriminates(n_sites, m_components, trials=TRIALS, seed=SEED0):
    """How often the better-fitting model is the one that generated it.

    Both models are fitted to each dataset and the lower SSE wins.
    Both have two free parameters, so the comparison is fair on
    parameter count and needs no penalty term.

    At n=2 both models pass exactly through both points, SSE is 0 for
    each, and the tie is broken by nothing. Reported as a tie rather
    than resolved.
    """
    rng = random.Random(seed)
    correct, ties = 0, 0
    for t in range(2 * trials):
        truth = truth_step if t % 2 == 0 else truth_slope
        rs = sites(n_sites)
        ys = observe(rs, truth, m_components, rng)
        s_step = _sse(rs, ys, _fit_step(rs, ys))
        s_line = _sse(rs, ys, _fit_line(rs, ys))
        if abs(s_step - s_line) < 1e-12:
            ties += 1
            continue
        picked = truth_step if s_step < s_line else truth_slope
        correct += 1 if picked is truth else 0
    n = 2 * trials
    return {
        "n_sites": n_sites, "m_components": m_components,
        "trials": n,
        "ties": ties, "tie_rate": ties / float(n),
        "decided": n - ties,
        "accuracy_on_decided": (correct / float(n - ties)
                                if n > ties else None),
        "accuracy_over_all": correct / float(n),
    }


def two_points_are_exact():
    """The n=2 result is arithmetic and does not need trials.

    Any two points (r1, y1), (r2, y2) with r1 < BREAK <= r2 are fitted
    exactly by BOTH a line and a step. Shown by construction over a
    grid of arbitrary pairs rather than asserted.
    """
    rng = random.Random(11)
    worst = 0.0
    for _ in range(500):
        rs = [R_MIN, R_MAX]
        ys = [rng.random(), rng.random()]
        worst = max(worst, _sse(rs, ys, _fit_step(rs, ys)),
                    _sse(rs, ys, _fit_line(rs, ys)))
    return {"pairs_tested": 500, "worst_sse_either_model": worst,
            "both_fit_exactly": worst < 1e-24,
            "why": "a line has two free parameters and a step has two. "
                   "Two points determine both exactly, so the residual "
                   "carries no information about which generated them. "
                   "No per-site precision changes this."}


def n_for(target, m_components, ns=(2, 3, 4, 5, 6, 8, 10, 12, 16, 20)):
    """Smallest site count reaching `target` accuracy on decided runs."""
    rows = []
    for n in ns:
        d = discriminates(n, m_components)
        rows.append(d)
        if d["accuracy_on_decided"] is not None \
                and d["accuracy_on_decided"] >= target \
                and d["tie_rate"] < 0.05:
            return {"n": n, "rows": rows, "found": True}
    return {"n": None, "rows": rows, "found": False}


# ---------------------------------------- what the ask supports

def comparisons():
    """The four comparisons against the asked-for sample size.

    Each is classified by what it needs, not by whether it is
    interesting. `n_sites` is the number of sites the comparison's own
    statistic requires; `at_pair` says whether one site pair delivers
    it.
    """
    return [
        {"id": 1, "name": "high-change vs low-change, same domain",
         "statistic": "presence/absence of named revision machinery",
         "kind": "CATEGORICAL", "n_sites_needed": 2, "at_pair": True,
         "note": "a presence/absence contrast on two sites is exactly "
                 "what a pair delivers. n=2 is the design, not a "
                 "limitation."},
        {"id": 2, "name": "fast-change vs slow-change",
         "statistic": "shape of held-obsolete rate against rate ratio",
         "kind": "SHAPE", "n_sites_needed": None, "at_pair": False,
         "note": "the prediction is a DISCONTINUITY rather than a "
                 "slope, which is a claim about shape. Two points are "
                 "fitted exactly by both shapes."},
        {"id": 3, "name": "component form, M3 vs M7",
         "statistic": "survival rate by component class, within site",
         "kind": "WITHIN_SITE", "n_sites_needed": 1, "at_pair": True,
         "note": "the denominator is COMPONENTS, not sites, so one "
                 "site with enough components carries it. Power comes "
                 "from M1-M8, which is not in this repository."},
        {"id": 4, "name": "written vs living, same domain and region",
         "statistic": "revision rate and held-obsolete rate by medium",
         "kind": "CROSS_MEDIUM", "n_sites_needed": 2, "at_pair": True,
         "note": "deliverable at a pair, and see the units problem in "
                 "CLAIM_TABLE RM_004: a revision in a written record "
                 "and a revision in a living system are not obviously "
                 "the same object."},
    ]


def _companion_scheme():
    """The scheme, IMPORTED from the companion study.

    It landed 2026-08-26. Imported rather than copied so the two
    cannot drift, and so this folder stops describing an absence that
    is no longer one.
    """
    p = os.path.join(ROOT, "transmission-decay")
    if not os.path.isdir(p):
        return None
    if p not in sys.path:
        sys.path.insert(0, p)
    import scheme as SC
    return SC


def m1_m8_dependency():
    """How much of the design keys off the companion coding scheme.

    Was: named and absent. RM_008's stated falsifier was "the
    companion study landing", and it landed.
    """
    txt = open(DROP, encoding="utf-8").read()
    SC = _companion_scheme()
    return {
        "scheme_named": "M1–M8" in txt or "M1-M8" in txt,
        "in_this_repo": SC is not None,
        "components": sorted(SC.COMPONENTS) if SC else [],
        "n_components": len(SC.COMPONENTS) if SC else 0,
        "source": ("transmission-decay.scheme.COMPONENTS, imported"
                   if SC else None),
        "comparison_3_terms_resolve": bool(
            SC and "M3" in SC.COMPONENTS and "M7" in SC.COMPONENTS),
        "reconstructed": False,
        "measures_keyed_to_it": [
            "STATUS (per component)",
            "REVISION PROVENANCE (per component)",
            "LATENCY (per component)",
            "HELD-OBSOLETE RATE (denominator is components)",
            "ROBUSTNESS FORM (per component)",
            "comparison 3 (M3 vs M7 by name)",
        ],
        "why_not_reconstructed": "a coding scheme is data. Inventing "
                                 "M1-M8 would have put a category "
                                 "system in the author's mouth and "
                                 "every number downstream would have "
                                 "been about the invention. It landed "
                                 "instead, and is imported.",
    }


# ------------------------------------------- the unassessed-component bias

def unassessed_bias(u_grid=(0.0, 0.1, 0.2, 0.3, 0.5), true_rate=0.35):
    """STATUS has five values and no state for "checked, still matches".

        held unchanged
        revised
        extended
        dropped
        held obsolete    still transmitted, no longer matches conditions

    `held obsolete` is checked-and-does-not-match. Nothing is
    checked-and-does-match, so a component nobody assessed and a
    component assessed as still fitting both land in `held unchanged`.

    Both sit in the held-obsolete rate's denominator -- "still-
    transmitted components" -- and only one can contribute to the
    numerator. So an unassessed fraction u biases the headline number
    LOW, and by a computable amount.
    """
    rows = []
    for u in u_grid:
        # of the still-transmitted set, a fraction u was never assessed.
        # Those cannot be coded held-obsolete even where they are.
        observed = true_rate * (1.0 - u)
        rows.append({"unassessed_share": u, "true_rate": true_rate,
                     "observed_rate": observed,
                     "understated_by": true_rate - observed,
                     "relative_error": (true_rate - observed) / true_rate})
    return {"rows": rows,
            "why": "the bias runs one way. An unassessed component "
                   "enters the denominator and cannot enter the "
                   "numerator, so the transmission system's own error "
                   "rate is reported lower than it is, by exactly the "
                   "unassessed share.",
            "repair": "a sixth STATUS value -- held unchanged, match "
                      "confirmed -- distinct from held unchanged, match "
                      "not assessed. Two states, currently one."}


# ------------------------------------------------------------- report

def wrap(t, w=68, ind="   "):
    out, cur = [], ind
    for word in t.split():
        if len(cur) + len(word) + 1 > w and cur.strip():
            out.append(cur.rstrip())
            cur = ind
        cur += word + " "
    if cur.strip():
        out.append(cur.rstrip())
    return out


def render():
    o = []
    o.append("REVISION MECHANISM -- what the ask's sample size delivers")
    o.append("")
    o += wrap("SOURCE_DROP.md asks for \"One site pair, one domain.\" "
              "This computes which of its four comparisons a pair "
              "carries. It uses no field data, touches no community, "
              "and says nothing about any real site or any real body of "
              "knowledge.", ind="")
    o.append("")
    o += wrap("THE STUDY IS NOT RUN HERE AND IS NOT SIMULATED. It "
              "requires fieldwork and collective consent, and its own "
              "ethics section says publishing a group's revision "
              "procedure without consent can damage the mechanism "
              "being studied. No synthetic site stands in for a real "
              "one anywhere below. The only objects are a line, a "
              "step, and binomial noise.", ind="")
    o.append("")

    o.append("0. THE COMPANION SCHEME")
    d = m1_m8_dependency()
    o.append("   M1-M8 named in the drop: %s" % d["scheme_named"])
    o.append("   present in this repository: %s" % d["in_this_repo"])
    o.append("   reconstructed: %s" % d["reconstructed"])
    if d["in_this_repo"]:
        o.append("   components: %s" % ", ".join(d["components"]))
        o.append("   source: %s" % d["source"])
        o.append("   comparison 3's M3 and M7 resolve: %s"
                 % d["comparison_3_terms_resolve"])
    o.append("   measures that key off it:")
    for m in d["measures_keyed_to_it"]:
        o.append("     - %s" % m)
    o += wrap(d["why_not_reconstructed"])
    o.append("")

    o.append("1. WHAT ONE SITE PAIR CARRIES")
    o.append("   %-3s %-42s %-14s %s"
             % ("#", "comparison", "kind", "at a pair"))
    for c in comparisons():
        o.append("   %-3d %-42s %-14s %s"
                 % (c["id"], c["name"][:42], c["kind"],
                    "yes" if c["at_pair"] else "NO"))
    o.append("")
    o += wrap("Three of four. The one that does not is comparison 2, "
              "and it is the one whose prediction is a THRESHOLD.")
    o.append("")

    o.append("2. WHY n=2 CANNOT SEE A DISCONTINUITY -- exact, not statistical")
    e = two_points_are_exact()
    o.append("   arbitrary pairs tested: %d" % e["pairs_tested"])
    o.append("   largest residual, either model: %.2e"
             % e["worst_sse_either_model"])
    o.append("   both fit exactly: %s" % e["both_fit_exactly"])
    o += wrap(e["why"])
    o.append("")

    o.append("3. THE SITE COUNT COMPARISON 2 REQUIRES")
    o.append("   accuracy at telling a step from a slope, by site count")
    o.append("   and by components measured per site (M)")
    o.append("")
    o.append("   %-5s %s" % ("n", "  ".join("M=%-3d" % m
                                            for m in (10, 30, 100))))
    for n in (2, 3, 4, 6, 8, 12, 20):
        cells = []
        for m in (10, 30, 100):
            r = discriminates(n, m, trials=200)
            cells.append("%-5s" % ("tie" if r["accuracy_on_decided"]
                                   is None else "%.2f"
                                   % r["accuracy_on_decided"]))
        o.append("   %-5d %s" % (n, "  ".join(cells)))
    o.append("")
    o += wrap("`tie` is not low power. At n=2 both models fit every "
              "dataset exactly, so nothing is decided at any M -- the "
              "row is empty rather than weak.")
    o += wrap("Reading across: comparison 2 becomes decidable at "
              "roughly four to six sites when about a hundred "
              "components are coded per site, and eight to "
              "twelve at thirty. At ten components per site, twenty "
              "sites still do not reach 0.9.")
    o.append("")

    o.append("4. AN ASYMMETRY IN THE HEADLINE NUMBER")
    u = unassessed_bias()
    o.append("   held-obsolete rate, true value %.2f"
             % u["rows"][0]["true_rate"])
    o.append("   %-18s %-14s %s"
             % ("unassessed share", "observed", "understated by"))
    for r in u["rows"]:
        o.append("   %-18.2f %-14.3f %.3f  (%.0f%%)"
                 % (r["unassessed_share"], r["observed_rate"],
                    r["understated_by"], 100 * r["relative_error"]))
    o += wrap(u["why"])
    o += wrap("WHAT WOULD CLOSE IT: " + u["repair"])
    return "\n".join(o)


def main(argv):
    if "--selftest" in argv:
        import selftest_power
        return selftest_power.run()
    print(render())
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
