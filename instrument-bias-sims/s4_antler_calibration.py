#!/usr/bin/env python3
# SPDX-License-Identifier: CC0-1.0
"""
s4_antler_calibration.py - competition vs motor-learning, separated by
prediction.

    python3 s4_antler_calibration.py
    python3 s4_antler_calibration.py --selftest

Yearling bucks carry an annual hardware change: mass, moment of inertia and
geometry all move between seasons. Two models predict sparring engagement
from different quantities.

  A  competition   engagement rate proportional to expected doe access
  B  calibration   engagement rate proportional to antler NOVELTY, decaying
                   as the motor model converges, and independent of rank
                   prospects

The two are NOT separable on engagement rate alone, which is what the
literature measures. They separate on a cohort x year interaction: model B
predicts a MOTOR deficit at equal antler mass in year two for animals that
did not spar in year one, and model A predicts a social deficit instead.

Prior art carried from the work order and NOT verified here: the fawn-play
motor-training hypothesis is validated in this taxon (play peaks at three
weeks or less, cerebellar timing), and has not been extended to yearling
sparring.

Marker under exploration, not a thesis. stdlib only, CC0.
"""

import random
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _shared as SH                                            # noqa: E402

COHORTS = ("wild", "supplemented_no_year_one")


def hardware(year):
    """Antler mass in arbitrary units. The annual change is the driver."""
    return {1: 1.0, 2: 2.2, 3: 3.1}.get(year, 3.5)


def novelty(year, prior_years_sparred):
    """How far the carried hardware is from anything the animal has a motor
    model for. Falls as seasons accumulate, and does not fall for an animal
    that carried the change without using it."""
    delta = abs(hardware(year) - hardware(year - 1)) if year > 1 else 1.0
    convergence = 0.55 ** prior_years_sparred
    return delta * convergence


def engage_A(rank_prospect, novelty_unused, rng, noise=0.05):
    """Competition: rate tracks expected access, novelty irrelevant."""
    return max(0.0, rank_prospect + rng.gauss(0.0, noise))


def engage_B(rank_prospect_unused, nov, rng, noise=0.05):
    """Calibration: rate tracks novelty, rank irrelevant."""
    return max(0.0, nov + rng.gauss(0.0, noise))


def motor_error(prior_years_sparred, mass, base=0.45, per_season=0.55):
    """Model B's distinguishing prediction: control error at a given mass
    falls with seasons of sparring practice, not with seasons of carrying."""
    return base * (per_season ** prior_years_sparred) * (mass / 2.2)


def social_deficit(prior_years_sparred, base=0.40, per_season=0.5):
    """Model A's distinguishing prediction: the deficit is in rank, not in
    control."""
    return base * (per_season ** prior_years_sparred)


def engagement_only(n=400, seed=3):
    """The measurement the literature makes. Both models fit it."""
    rng = random.Random(seed)
    rows = []
    for year in (1, 2, 3):
        rank = {1: 0.25, 2: 0.60, 3: 0.85}[year]
        nov = novelty(year, prior_years_sparred=year - 1)
        a = sum(engage_A(rank, nov, rng) for _ in range(n)) / n
        b = sum(engage_B(rank, nov, rng) for _ in range(n)) / n
        rows.append({"year": year, "rank_prospect": rank, "novelty": nov,
                     "A_rate": a, "B_rate": b})
    return rows


def cohort_experiment(n=400, seed=9):
    """The measurement that separates them.

    Year two, matched antler mass, two cohorts. Wild animals sparred in year
    one; supplemented/rehab animals did not.
    """
    rng = random.Random(seed)
    out = []
    for cohort in COHORTS:
        prior = 1 if cohort == "wild" else 0
        me = sum(motor_error(prior, hardware(2)) + rng.gauss(0, 0.02)
                 for _ in range(n)) / n
        sd = sum(social_deficit(prior) + rng.gauss(0, 0.02)
                 for _ in range(n)) / n
        out.append({"cohort": cohort, "prior_years_sparred": prior,
                    "antler_mass": hardware(2),
                    "motor_error": me, "social_deficit": sd})
    wild = [r for r in out if r["cohort"] == "wild"][0]
    supp = [r for r in out if r["cohort"] != "wild"][0]
    return {"rows": out,
            "motor_gap": supp["motor_error"] - wild["motor_error"],
            "social_gap": supp["social_deficit"] - wild["social_deficit"],
            "A_predicts": "social gap, no motor gap",
            "B_predicts": "motor gap at equal mass, no necessary social gap"}


def separability(rows):
    """Can engagement rate alone tell the models apart?"""
    import statistics
    a = [r["A_rate"] for r in rows]
    b = [r["B_rate"] for r in rows]
    # both rise or both fall? the sign of the trend is what an observer reads
    return {"A_trend": a[-1] - a[0], "B_trend": b[-1] - b[0],
            "same_sign": (a[-1] - a[0]) * (b[-1] - b[0]) > 0,
            "A_spread": max(a) - min(a), "B_spread": max(b) - min(b),
            "separable_on_rate_alone": (a[-1] - a[0]) * (b[-1] - b[0]) <= 0}


def confidence():
    return {"model_separation": "structural: the two models are functions of "
                                "different variables, so a design varying "
                                "one at fixed other separates them",
            "parameter_values": "all stipulated. novelty decay, motor-error "
                                "base and per-season factors are round "
                                "numbers, not measurements",
            "prior_art_claim": "CARRIED FROM THE WORK ORDER, not verified "
                               "here",
            "resolved": False}


def breaks():
    return [
        "the cohort contrast is confounded. 'supplemented / rehab, no "
        "year-one testing' selects animals that differ in nutrition, "
        "handling, disease history and human exposure, any of which moves "
        "motor error. The design needs the deficit to be specific to the "
        "practice variable and nothing here establishes that",
        "the sim puts the separation in by construction: engage_A ignores "
        "novelty and engage_B ignores rank, so of course a design varying "
        "one at fixed other separates them. What the module shows is that "
        "the EXISTING measurement -- engagement rate over years -- does not, "
        "which is the part worth having",
        "motor_error decays with seasons SPARRED and not with seasons "
        "CARRIED. That is model B's content and it is assumed here rather "
        "than derived; if carrying alone calibrates, both cohorts converge "
        "and the design returns nothing",
        "no cervid data of any kind is used in this file",
        "the fawn-play prior art is carried from the work order unverified, "
        "and the whole design leans on it being real",
    ]


def report():
    L = ["S4 -- ANTLER CALIBRATION", "=" * 72, ""]
    rows = engagement_only()
    sep = separability(rows)
    L.append("  1. WHAT THE EXISTING MEASUREMENT CANNOT DO")
    L.append("")
    L.append("    %-6s %-14s %-10s %-10s %s"
             % ("year", "rank prospect", "novelty", "A rate", "B rate"))
    for r in rows:
        L.append("    %-6d %-14.2f %-10.3f %-10.3f %.3f"
                 % (r["year"], r["rank_prospect"], r["novelty"],
                    r["A_rate"], r["B_rate"]))
    L.append("")
    L.append("    A trend %+.3f   B trend %+.3f   same sign %s"
             % (sep["A_trend"], sep["B_trend"], sep["same_sign"]))
    L.append("    separable on rate alone: %s"
             % sep["separable_on_rate_alone"])
    L.append("")
    L.extend(SH.wrap("Here the trends happen to run opposite ways, which is "
                     "the ONE case where rate alone would separate them -- "
                     "and it depends entirely on the stipulated novelty decay "
                     "outpacing the stipulated rank rise. Move either "
                     "constant and the signs agree. So rate alone separates "
                     "the models only for particular parameter values, which "
                     "means an observer reading a real rate series cannot "
                     "know whether it does.", "    "))
    L.append("")
    L.append("-" * 72)
    L.append("")
    ce = cohort_experiment()
    L.append("  2. THE MEASUREMENT THAT DOES -- year two, matched mass")
    L.append("")
    L.append("    %-28s %-8s %-8s %-14s %s"
             % ("cohort", "prior", "mass", "motor error", "social deficit"))
    for r in ce["rows"]:
        L.append("    %-28s %-8d %-8.1f %-14.3f %.3f"
                 % (r["cohort"], r["prior_years_sparred"], r["antler_mass"],
                    r["motor_error"], r["social_deficit"]))
    L.append("")
    L.append("    motor gap  %+.3f" % ce["motor_gap"])
    L.append("    social gap %+.3f" % ce["social_gap"])
    L.append("")
    L.append("    A predicts: %s" % ce["A_predicts"])
    L.append("    B predicts: %s" % ce["B_predicts"])
    L.append("")
    L.extend(SH.wrap("Both gaps are non-zero in this sim because both "
                     "mechanisms were switched on. On real animals they are "
                     "measured separately -- a control-error assay at matched "
                     "mass, and a rank assay -- and the models disagree about "
                     "which one carries the deficit. That disagreement is the "
                     "experiment.", "    "))
    L.extend(SH.tail(sys.modules[__name__]))
    return "\n".join(L)


def selftest():
    ck, done = SH.checker()
    ck("novelty falls as seasons of sparring accumulate",
       novelty(3, 2) < novelty(2, 1))
    ck("novelty does NOT fall for an animal that carried without sparring",
       novelty(2, 0) > novelty(2, 1))

    rng = random.Random(1)
    ck("model A ignores novelty",
       abs(engage_A(0.5, 0.0, random.Random(1))
           - engage_A(0.5, 99.0, random.Random(1))) < 1e-9)
    ck("model B ignores rank",
       abs(engage_B(0.0, 0.5, random.Random(1))
           - engage_B(99.0, 0.5, random.Random(1))) < 1e-9)

    ce = cohort_experiment()
    ck("the no-year-one cohort carries the larger motor error at equal mass",
       ce["motor_gap"] > 0.05)
    ck("antler mass is matched across cohorts, so the motor gap is not a "
       "mass effect",
       len({r["antler_mass"] for r in ce["rows"]}) == 1)
    ck("the two models predict different things, which is what makes the "
       "design an experiment", ce["A_predicts"] != ce["B_predicts"])

    ck("motor error falls with seasons SPARRED",
       motor_error(1, 2.2) < motor_error(0, 2.2))
    ck("and rises with mass at fixed practice",
       motor_error(0, 3.1) > motor_error(0, 2.2))

    sep = separability(engagement_only())
    ck("the rate-only separability verdict is computed, not asserted",
       isinstance(sep["separable_on_rate_alone"], bool))

    ck("the cohort confound leads the breaks list",
       "confounded" in breaks()[0])
    ck("the built-in separation is disclosed rather than claimed as a result",
       any("by construction" in b for b in breaks()))
    ck("prior art is marked carried-not-verified",
       "not verified" in confidence()["prior_art_claim"].lower())
    ck("confidence unresolved", confidence()["resolved"] is False)
    ck("report renders", "matched mass" in report())
    return done()


if __name__ == "__main__":
    sys.exit(SH.run(sys.modules[__name__], "S4"))
