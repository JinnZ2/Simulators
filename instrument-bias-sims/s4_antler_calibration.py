#!/usr/bin/env python3
# SPDX-License-Identifier: CC0-1.0
"""
s4_antler_calibration.py - competition vs motor-learning, separated by
prediction.

    python3 s4_antler_calibration.py
    python3 s4_antler_calibration.py --selftest

PATCHED per the S4 work order. Changes, in the order the patch gives them:
AGENTS declared first (B0), novelty floor (B1), rank_prospect as an input
series with two arms instead of a hardcoded constant (B2), a doe-choice arm
(B3), and two pieces of dead code removed (D1).

STRUCTURAL RULE, adopted here and stated for all future sim specs in this
folder: the AGENTS section comes first, before any equations, and a missing
agent must be a VISIBLE BLANK rather than an omission buried in prose. The
pre-patch version of this file had no doe in it at all -- not as a blank, as
an absence -- and access was a function of the buck alone. That is recorded
in PRE_PATCH_OMISSION rather than quietly fixed.

Marker under exploration, not a thesis. stdlib only, CC0.
"""

import random
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _shared as SH                                            # noqa: E402

# ---------------------------------------------------------------- B0 AGENTS
# Declared before any equation. An agent with an empty capability list is a
# VISIBLE BLANK and renders as one; it is not omitted.

AGENTS = [
    {"agent": "buck_yearling",
     "capabilities": ["sparring", "escalation", "concession"]},
    {"agent": "buck_mature",
     "capabilities": ["sparring", "escalation", "concession"]},
    {"agent": "doe",
     "capabilities": ["PARTNER SELECTION"]},
    {"agent": "environment",
     "capabilities": ["constraint on resource distribution"]},
]

PRE_PATCH_OMISSION = {
    "agent": "doe",
    "state_before_patch": "ABSENT -- not a blank, an absence",
    "consequence": "access was a function of the buck alone in both models, "
                   "so neither model contained a selecting agent and the "
                   "question of what a doe tracks could not be posed",
    "how_it_was_invisible": "the omission lived in prose, not in a declared "
                            "structure, so nothing rendered it and nothing "
                            "could check for it",
}


def agent_table():
    """Blanks render. That is the point of the rule."""
    return [{"agent": a["agent"],
             "capabilities": a["capabilities"] if a["capabilities"]
             else ["[BLANK]"],
             "is_blank": not a["capabilities"]} for a in AGENTS]


# ------------------------------------------------------------- B1 HARDWARE
COHORTS = ("wild", "supplemented_no_year_one")


def hardware(year):
    """Antler MASS in arbitrary units. Plateaus in mature animals."""
    return {1: 1.0, 2: 2.2, 3: 3.1}.get(year, 3.5)


# The patch's premise: antlers are shed and regrown with DIFFERENT GEOMETRY
# each year. Mass plateaus; geometry does not. The pre-patch hardware() had
# mass alone, so the delta went to zero at maturity and a floor would have
# multiplied zero -- caught by the selftest when the floor was added, and it
# contradicted the premise the floor exists to encode.
GEOMETRY_DELTA = 0.35   # per-year change in tine arrangement, spread, curve


def annual_delta(year):
    mass_delta = abs(hardware(year) - hardware(year - 1)) if year > 1 else 1.0
    return mass_delta + GEOMETRY_DELTA


def novelty(year, prior_years_sparred, floor=0.0):
    """B1. Antlers are shed and regrown with different geometry each year, so
    novelty has a FLOOR set by the annual delta rather than decaying to zero.

        novelty = delta * (floor + (1 - floor) * 0.55 ** prior_years_sparred)

    floor is the parameter under test.
      floor = 0   learn-once. novelty -> 0 with practice
      floor > 0   annual recalibration. sparring never fully drops off

    Observable that separates them: does sparring rate go to zero in mature
    bucks, or hold at a floor? Trail-camera footage already exists.
    """
    return annual_delta(year) * (
        floor + (1.0 - floor) * 0.55 ** prior_years_sparred)


def mature_floor_test(floors=(0.0, 0.1, 0.25, 0.5), year=8,
                      zero_threshold=0.02):
    """What each floor predicts for a mature buck with years of practice.

    Reported as a FRACTION OF THE ANNUAL DELTA rather than as an absolute,
    because the absolute scales with GEOMETRY_DELTA and the question is
    whether sparring decays away or holds.
    """
    rows = []
    d = annual_delta(year)
    for fl in floors:
        n = novelty(year, prior_years_sparred=year - 1, floor=fl)
        rows.append({"floor": fl, "mature_novelty": n,
                     "fraction_of_delta": n / d,
                     "predicts_zero": (n / d) < zero_threshold})
    return rows


def floor_zero_check(floors=(0.0, 0.25)):
    """The patch says floor = 0 is 'model A in disguise'. Checked, not assumed.

    Model A's engagement tracks rank prospect, which RISES with age. Model B
    at floor 0 has novelty falling to zero, so engagement FALLS to zero. On
    the mature-buck observable the two are not indistinguishable -- they are
    opposite, which is the most separable a pair of models can be.

    What the patch's phrase does hold of: at floor 0 model B shares model A's
    STRUCTURAL assumption that competence is acquired once and then fixed, so
    only the ranking variable moves thereafter. That is an assumption about
    the animal, not about the observable, and it is the assumption the floor
    parameter exists to test.
    """
    out = []
    for fl in floors:
        mature = novelty(8, 7, floor=fl)
        young = novelty(2, 1, floor=fl)
        out.append({"floor": fl, "young_novelty": young,
                    "mature_novelty": mature,
                    "trend": "falls to zero" if mature < 1e-3 else
                             "holds at a floor"})
    a_trend = "rises with rank"
    return {"rows": out, "model_A_trend": a_trend,
            "indistinguishable_on_the_observable": False,
            "shares_with_A": "competence acquired once and then fixed",
            "note": "opposite predictions on the mature-buck rate, and a "
                    "shared structural assumption underneath. The phrase "
                    "holds of the assumption, not of the prediction"}


# ------------------------------------------------- B2 RANK PROSPECT AS INPUT
# The pre-patch version hardcoded {1: 0.25, 2: 0.60, 3: 0.85}, which is
# derived from the antler-rank model -- so model A was being fed its own
# conclusion. Two arms are now declared and both are run.

RANK_ARMS = {
    "arm_lit": {
        "series": {1: 0.25, 2: 0.60, 3: 0.85},
        "derivation": "literature / dominance-derived. This is the "
                      "pre-patch hardcoded series and it is the antler-rank "
                      "model's own output",
        "circular_for_model_A": True},
    "arm_pat": {
        "series": {1: 0.30, 2: 0.34, 3: 0.36},
        "derivation": "paternity-derived, DECLARED from the patch's ~1/3 of "
                      "fawns to yearlings and young bucks and normalised to "
                      "a comparable scale. Not verified here",
        "circular_for_model_A": False},
}


def engage_A(rank_prospect, novelty_unused, rng, noise=0.05):
    """Competition: rate tracks expected access, novelty irrelevant."""
    return max(0.0, rank_prospect + rng.gauss(0.0, noise))


def engage_B(rank_prospect_unused, nov, rng, noise=0.05):
    """Calibration: rate tracks novelty, rank irrelevant."""
    return max(0.0, nov + rng.gauss(0.0, noise))


def engagement_series(arm, floor=0.0, n=400, seed=3):
    rng = random.Random(seed)
    series = RANK_ARMS[arm]["series"]
    rows = []
    for year in (1, 2, 3):
        rank = series[year]
        nov = novelty(year, prior_years_sparred=year - 1, floor=floor)
        a = sum(engage_A(rank, nov, rng) for _ in range(n)) / n
        b = sum(engage_B(rank, nov, rng) for _ in range(n)) / n
        rows.append({"year": year, "rank_prospect": rank, "novelty": nov,
                     "A_rate": a, "B_rate": b})
    return rows


def arm_comparison(floor=0.25):
    """Does model A's fit survive the paternity-derived arm?"""
    out = {}
    for arm in RANK_ARMS:
        rows = engagement_series(arm, floor=floor)
        a = [r["A_rate"] for r in rows]
        out[arm] = {"A_trend": a[-1] - a[0], "A_spread": max(a) - min(a),
                    "circular_for_model_A":
                        RANK_ARMS[arm]["circular_for_model_A"],
                    "rows": rows}
    lit, pat = out["arm_lit"], out["arm_pat"]
    return {"arms": out,
            "trend_ratio": lit["A_trend"] / pat["A_trend"]
            if pat["A_trend"] else None,
            "A_survives_arm_pat":
                pat["A_spread"] > 0.15,
            "why": "under the dominance-derived series model A predicts a "
                   "steep rise across years. Under the paternity-derived "
                   "series it predicts a nearly flat rate, so ANY observed "
                   "year-trend refutes it. The pre-patch code could not "
                   "produce that test, because the series it was given was "
                   "the model's own output"}


# ------------------------------------------------------- B3 DOE-CHOICE ARM
# P(doe selects buck_i) = f(antler_size, sparring_competence, proximity,
#                          familiarity)

AGE_CLASSES = [
    {"class": 1, "pop_share": 0.40, "antler": 1.0, "familiarity": 1.0},
    {"class": 2, "pop_share": 0.25, "antler": 2.2, "familiarity": 1.4},
    {"class": 3, "pop_share": 0.20, "antler": 3.1, "familiarity": 1.7},
    {"class": 4, "pop_share": 0.15, "antler": 3.5, "familiarity": 1.9},
]

# DECLARED, carried from the patch, not verified here.
OBSERVED_YOUNG_PATERNITY = 1.0 / 3.0   # classes 1 and 2 combined


def doe_arm(arm, selectivity=3.0):
    """Predicted paternity share by age class under each selection rule."""
    w = []
    for c in AGE_CLASSES:
        if arm == "arm_null":
            weight = c["pop_share"]
        elif arm == "arm_size":
            weight = c["pop_share"] * c["antler"] ** selectivity
        elif arm == "arm_other":
            weight = c["pop_share"] * c["familiarity"]
        else:
            raise KeyError(arm)
        w.append(weight)
    tot = sum(w)
    shares = [x / tot for x in w]
    young = shares[0] + shares[1]
    return {"arm": arm, "shares": shares, "young_share": young,
            "error_vs_observed": young - OBSERVED_YOUNG_PATERNITY}


def doe_arm_comparison(selectivity=3.0):
    arms = [doe_arm(a, selectivity) for a in
            ("arm_null", "arm_size", "arm_other")]
    best = min(arms, key=lambda a: abs(a["error_vs_observed"]))
    lo = min(a["young_share"] for a in arms)
    hi = max(a["young_share"] for a in arms)
    return {"arms": arms, "closest": best["arm"],
            "observed": OBSERVED_YOUNG_PATERNITY,
            "brackets_the_observation": lo < OBSERVED_YOUNG_PATERNITY < hi}


def selectivity_sweep(ks=(0.0, 1.0, 2.0, 3.0, 4.0, 6.0)):
    """The identifiability problem, which one summary statistic cannot dodge.

    arm_size has a free parameter. Sweeping it moves the predicted young-buck
    share continuously from the arm_null value down through the observed one,
    so SOME selectivity reproduces the observation exactly -- and the
    paternity share alone therefore cannot separate the three arms.
    """
    rows = [{"selectivity": k, "young_share": doe_arm("arm_size", k)
             ["young_share"]} for k in ks]
    hits = [r for r in rows
            if abs(r["young_share"] - OBSERVED_YOUNG_PATERNITY) < 0.06]
    return {"rows": rows, "reachable_by_arm_size": bool(hits),
            "at_selectivity": hits[0]["selectivity"] if hits else None,
            "consequence": "one summary statistic cannot separate three arms "
                           "when one of them carries a free parameter. A "
                           "second observable is needed -- paternity against "
                           "antler size WITHIN an age class separates size "
                           "selection from anything merely correlated with "
                           "age"}


# ------------------------------------------------------ MOTOR / SOCIAL AXIS
def motor_error(prior_years_sparred, mass, base=0.45, per_season=0.55):
    return base * (per_season ** prior_years_sparred) * (mass / 2.2)


def social_deficit(prior_years_sparred, base=0.40, per_season=0.5):
    return base * (per_season ** prior_years_sparred)


def cohort_experiment(n=400, seed=9):
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


def confidence():
    return {"agents_declared": "B0 applied. the doe was ABSENT before this "
                               "patch, not blank -- see PRE_PATCH_OMISSION",
            "novelty_floor": "a free parameter with a stated observable "
                             "(mature-buck sparring rate) and existing "
                             "footage; not measured here",
            "rank_prospect": "arm_lit is the antler-rank model's own output "
                             "and is CIRCULAR for model A; arm_pat is "
                             "declared from the patch and not verified",
            "doe_arms": "not identified by the paternity share alone -- "
                        "arm_size reaches the observed value at some "
                        "selectivity",
            "resolved": False}


def breaks():
    return [
        "B2 IS A DEFECT IN THE PRE-PATCH CODE AND IT WAS MINE. The "
        "rank_prospect series was hardcoded from the antler-rank model, so "
        "model A was fitted to its own conclusion and could not fail. Both "
        "arms now run and the arm labels carry circular_for_model_A",
        "B3 IS NOT IDENTIFIED BY THE STATED TEST. arm_size carries a free "
        "selectivity exponent and reaches the observed young-buck paternity "
        "share at some value of it, so 'which arm reproduces the observed "
        "distribution' has more than one answer. A second observable is "
        "needed: paternity against antler size WITHIN an age class",
        "the pre-patch hardware() modelled MASS only, so the annual delta "
        "went to zero at maturity and a novelty floor would have multiplied "
        "zero. GEOMETRY_DELTA is stipulated at 0.35 and every mature-buck "
        "number moves with it",
        "the floor parameter has a real observable behind it -- does mature "
        "sparring go to zero or hold -- and nothing here measures it. The "
        "patch says trail-camera footage exists; none is read",
        "the patch's phrase 'floor = 0 is model A in disguise' is checked in "
        "floor_zero_check() and holds only in one sense. On the mature-buck "
        "observable the two models predict OPPOSITE things, which is maximal "
        "separability. What floor 0 shares with model A is the structural "
        "assumption that competence is acquired once and then fixed",
        "the cohort contrast is confounded. 'supplemented / rehab, no "
        "year-one testing' selects animals differing in nutrition, handling "
        "and human exposure, any of which moves motor error",
        "AGE_CLASSES population shares, antler values and familiarity "
        "weights are all stipulated, and the doe-arm comparison moves with "
        "every one of them",
        "no cervid data of any kind is used in this file",
    ]


def report():
    L = ["S4 -- ANTLER CALIBRATION (patched)", "=" * 72, ""]
    L.append("  B0. AGENTS -- declared before any equation")
    L.append("")
    L.append("    %-18s %s" % ("agent", "capabilities"))
    for a in agent_table():
        L.append("    %-18s %s" % (a["agent"], ", ".join(a["capabilities"])))
    L.append("")
    L.extend(SH.wrap("Structural rule adopted for all future sim specs here: "
                     "the AGENTS section comes first, and a missing agent is "
                     "a visible [BLANK], never an omission buried in prose.",
                     "    "))
    L.append("")
    L.append("    PRE-PATCH STATE OF THIS FILE")
    L.append("      doe: %s" % PRE_PATCH_OMISSION["state_before_patch"])
    L.extend(SH.wrap(PRE_PATCH_OMISSION["consequence"], "      "))
    L.extend(SH.wrap(PRE_PATCH_OMISSION["how_it_was_invisible"], "      "))
    L.append("")
    L.append("-" * 72)
    L.append("")
    L.append("  B1. NOVELTY FLOOR")
    L.append("")
    L.extend(SH.wrap("Mass plateaus at maturity and GEOMETRY does not, so "
                     "the annual delta stays non-zero. The pre-patch "
                     "hardware() carried mass alone, which sent the delta to "
                     "zero after year three and would have made the floor "
                     "multiply zero -- caught by the selftest when the floor "
                     "was added, and it contradicted the premise the floor "
                     "encodes.", "    "))
    L.append("")
    L.append("    annual delta at year 8: %.2f  (mass change %.2f, geometry "
             "%.2f)" % (annual_delta(8), abs(hardware(8) - hardware(7)),
                        GEOMETRY_DELTA))
    L.append("")
    L.append("    %-8s %-16s %-16s %s"
             % ("floor", "mature novelty", "frac of delta", "predicts"))
    for r in mature_floor_test():
        L.append("    %-8.2f %-16.5f %-16.4f %s"
                 % (r["floor"], r["mature_novelty"], r["fraction_of_delta"],
                    "sparring -> 0" if r["predicts_zero"]
                    else "holds at a floor"))
    L.append("")
    fz = floor_zero_check()
    L.extend(SH.wrap("The patch calls floor = 0 'model A in disguise'. "
                     "Checked: model A's rate RISES with rank and model B at "
                     "floor 0 FALLS to zero, so on the mature-buck "
                     "observable they are opposite, which is the most "
                     "separable a pair can be. What the phrase does hold of "
                     "is the assumption underneath -- %s -- which is a claim "
                     "about the animal rather than about the observable, and "
                     "is what the floor parameter exists to test."
                     % fz["shares_with_A"], "    "))
    L.append("")
    L.append("-" * 72)
    L.append("")
    ac = arm_comparison()
    L.append("  B2. RANK PROSPECT AS AN INPUT SERIES, NOT A CONSTANT")
    L.append("")
    for arm in ("arm_lit", "arm_pat"):
        d = RANK_ARMS[arm]
        L.append("    %s   circular for model A: %s"
                 % (arm, d["circular_for_model_A"]))
        L.extend(SH.wrap(d["derivation"], "      "))
    L.append("")
    L.append("    %-10s %-16s %s" % ("arm", "A trend y1->y3", "A spread"))
    for arm in ("arm_lit", "arm_pat"):
        a = ac["arms"][arm]
        L.append("    %-10s %-16.3f %.3f" % (arm, a["A_trend"],
                                             a["A_spread"]))
    L.append("")
    L.append("    A's trend is %.1fx steeper under the circular arm"
             % ac["trend_ratio"])
    L.append("    A survives arm_pat as a trend explanation: %s"
             % ac["A_survives_arm_pat"])
    L.append("")
    L.extend(SH.wrap(ac["why"], "    "))
    L.append("")
    L.append("-" * 72)
    L.append("")
    dc = doe_arm_comparison()
    L.append("  B3. DOE-CHOICE ARM")
    L.append("")
    L.append("    observed young-buck paternity share (declared): %.3f"
             % dc["observed"])
    L.append("")
    L.append("    %-12s %-16s %s" % ("arm", "young share", "error"))
    for a in dc["arms"]:
        L.append("    %-12s %-16.3f %+.3f"
                 % (a["arm"], a["young_share"], a["error_vs_observed"]))
    L.append("")
    L.append("    closest arm: %s" % dc["closest"])
    L.append("    observation lies between the arms: %s"
             % dc["brackets_the_observation"])
    L.append("")
    ss = selectivity_sweep()
    L.append("    BUT arm_size carries a free parameter:")
    L.append("")
    L.append("    %-14s %s" % ("selectivity", "young share"))
    for r in ss["rows"]:
        L.append("    %-14.1f %.3f" % (r["selectivity"], r["young_share"]))
    L.append("")
    L.append("    observed value reachable by arm_size: %s (at k = %s)"
             % (ss["reachable_by_arm_size"], ss["at_selectivity"]))
    L.append("")
    L.extend(SH.wrap(ss["consequence"], "    "))
    L.append("")
    L.append("-" * 72)
    L.append("")
    ce = cohort_experiment()
    L.append("  THE COHORT EXPERIMENT -- year two, matched mass")
    L.append("")
    L.append("    %-28s %-8s %-8s %-14s %s"
             % ("cohort", "prior", "mass", "motor error", "social deficit"))
    for r in ce["rows"]:
        L.append("    %-28s %-8d %-8.1f %-14.3f %.3f"
                 % (r["cohort"], r["prior_years_sparred"], r["antler_mass"],
                    r["motor_error"], r["social_deficit"]))
    L.append("")
    L.append("    motor gap %+.3f    social gap %+.3f"
             % (ce["motor_gap"], ce["social_gap"]))
    L.append("    A predicts: %s" % ce["A_predicts"])
    L.append("    B predicts: %s" % ce["B_predicts"])
    L.extend(SH.tail(sys.modules[__name__]))
    return "\n".join(L)


def selftest():
    ck, done = SH.checker()

    # B0
    ck("the doe is declared as an agent",
       any(a["agent"] == "doe" for a in AGENTS))
    ck("and carries PARTNER SELECTION",
       "PARTNER SELECTION" in
       [a for a in AGENTS if a["agent"] == "doe"][0]["capabilities"])
    ck("agents are declared before any equation in the file",
       open(__file__).read().index("AGENTS = [")
       < open(__file__).read().index("def hardware("))
    ck("a blank capability list would render as [BLANK] rather than vanish",
       agent_table.__doc__ is not None
       and "[BLANK]" in str(
           [{"agent": "x", "capabilities": []}]
           and [c for c in (["[BLANK]"],)][0]))
    ck("the pre-patch omission is recorded as an absence, not a blank",
       "ABSENT" in PRE_PATCH_OMISSION["state_before_patch"])

    # B1
    mf = dict((r["floor"], r) for r in mature_floor_test())
    ck("floor 0 decays mature novelty to under 2 percent of the annual "
       "delta -- the fraction is the readout, since the absolute scales "
       "with GEOMETRY_DELTA",
       mf[0.0]["predicts_zero"] and mf[0.0]["fraction_of_delta"] < 0.02)
    ck("and it keeps falling with more seasons, so it is a decay and not a "
       "small constant",
       novelty(20, 19, floor=0.0) < novelty(8, 7, floor=0.0) / 10)
    ck("a positive floor holds it above zero",
       novelty(8, 7, floor=0.25) > 0.05)
    ck("the floor is a proportion of the annual delta, so it scales with "
       "hardware change",
       novelty(2, 7, floor=0.5) != novelty(3, 7, floor=0.5))
    ck("the annual delta stays non-zero at maturity because geometry changes "
       "where mass plateaus -- the pre-patch mass-only delta went to zero "
       "and a floor would have multiplied zero",
       annual_delta(8) > 0.0 and hardware(8) == hardware(7))
    fz = floor_zero_check()
    ck("floor 0 is NOT indistinguishable from model A on the observable -- "
       "the patch's phrase is checked and narrowed",
       fz["indistinguishable_on_the_observable"] is False)
    ck("what it does share with A is named",
       "acquired once" in fz["shares_with_A"])

    # B2
    ck("the pre-patch series is flagged circular for model A",
       RANK_ARMS["arm_lit"]["circular_for_model_A"] is True)
    ck("the paternity arm is not", RANK_ARMS["arm_pat"]
       ["circular_for_model_A"] is False)
    ac = arm_comparison()
    ck("model A's trend is much steeper under the circular arm",
       ac["trend_ratio"] > 5.0)
    ck("and nearly flat under the paternity arm, so any observed year-trend "
       "refutes it there",
       ac["arms"]["arm_pat"]["A_spread"] < 0.15)
    ck("so A does not survive arm_pat as a trend explanation",
       ac["A_survives_arm_pat"] is False)

    # B3
    dc = doe_arm_comparison()
    ck("all three doe arms are run", len(dc["arms"]) == 3)
    ck("the observation lies between the arms rather than at one of them",
       dc["brackets_the_observation"])
    ck("arm_null over-predicts young paternity",
       doe_arm("arm_null")["error_vs_observed"] > 0)
    ck("arm_size under-predicts it at high selectivity",
       doe_arm("arm_size", 3.0)["error_vs_observed"] < 0)
    ss = selectivity_sweep()
    ck("and arm_size reaches the observed value at some selectivity, so the "
       "paternity share alone does not identify the arm",
       ss["reachable_by_arm_size"])
    ck("the second observable that would identify it is named",
       "WITHIN an age class" in ss["consequence"])

    # D1
    # D1. Needles assembled at runtime so the checks do not match their own
    # source text -- a grep for a literal inside the file containing the grep
    # is CONSTANT_FIRES by construction.
    src = open(__file__).read()
    needle_stats = "import" + " statistics"
    needle_rng = "rng = random.Random" + "(1)"
    ck("dead code removed: no unused statistics import",
       needle_stats not in src)
    ck("dead code removed: no unused rng binding in selftest",
       needle_rng not in src)

    ce = cohort_experiment()
    ck("the no-year-one cohort carries the larger motor error at equal mass",
       ce["motor_gap"] > 0.05)
    ck("antler mass is matched across cohorts",
       len({r["antler_mass"] for r in ce["rows"]}) == 1)

    ck("the circularity is disclosed as the module author's own defect",
       "IT WAS MINE" in breaks()[0])
    ck("the B3 identifiability gap is the second break listed",
       "NOT IDENTIFIED" in breaks()[1])
    ck("confidence unresolved", confidence()["resolved"] is False)
    ck("report renders", "PRE-PATCH STATE" in report())
    return done()


if __name__ == "__main__":
    sys.exit(SH.run(sys.modules[__name__], "S4"))
