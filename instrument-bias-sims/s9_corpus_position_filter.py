#!/usr/bin/env python3
# SPDX-License-Identifier: CC0-1.0
"""
s9_corpus_position_filter.py - a corpus samples observer positions
non-uniformly, with nothing doing the filtering.

    python3 s9_corpus_position_filter.py
    python3 s9_corpus_position_filter.py --selftest

Training corpora are assembled from written text. Writing is done from a
position. The position has properties. So the corpus samples positions
non-uniformly -- and no agent selects on position anywhere in the chain.

NOT A CLAIM ABOUT CONTENT. Facts get recorded eventually, by visitors. The
category at issue is INTERRELATION: how components couple under non-delivery,
non-availability and non-substitution. That forms under residence and does not
survive extraction into a paper written from a supplied position.

WHAT THIS MODULE ADDS TO THE SPEC, and it is the part that is not analytic.
The spec's reason -- "because those two conditions are anti-correlated with
writing" -- needs the JOINT structure, not the two marginals. At zero coupling
between the position axes, the suppression of a two-condition category is
EXACTLY the product of its two marginal suppressions: no interaction, nothing
to explain. Everything above that product is supplied by the coupling, and the
module measures how much coupling is needed before interrelation becomes the
most-suppressed category. It does not always win.

Graded terms only: sampling density, correlation direction, cost asymmetry,
whether the aggregate steers. Nothing here requires anyone to have wanted it.

Marker under exploration, not a thesis. stdlib only, CC0.
"""

import math
import random
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _shared as SH                                            # noqa: E402

# ---------------------------------------------------------------- B0 AGENTS
# Declared before any equation, per the folder rule adopted in S4. An agent
# with an empty capability list is a VISIBLE BLANK.

AGENTS = [
    {"agent": "observer",
     "capabilities": ["occupies a position", "holds knowledge",
                      "may write"]},
    {"agent": "corpus_assembler",
     "capabilities": ["collects written text", "deduplicates"]},
    {"agent": "model",
     "capabilities": ["trained on the corpus", "scores relevance"]},
    {"agent": "filtering_agent",
     "capabilities": []},
]

BLANK_IS_THE_POINT = {
    "agent": "filtering_agent",
    "why_blank": "no agent selects on position anywhere in this model. The "
                 "corpus_assembler cannot see position; the observer is not "
                 "excluded from anything; the model reads what it was given. "
                 "The non-uniformity is a consequence of a cost gradient and "
                 "a population structure, and it needs nobody to have wanted "
                 "it",
    "why_it_matters": "the file is named ...position_filter and there is no "
                      "filter in it. Under the folder rule that has to render "
                      "as a [BLANK] rather than be argued in prose, because "
                      "the absence is the finding",
}


def agent_table():
    return [{"agent": a["agent"],
             "capabilities": a["capabilities"] or ["[BLANK]"],
             "is_blank": not a["capabilities"]} for a in AGENTS]


# ------------------------------------------------------- POSITION VARIABLES
# Each axis runs 0..1. The direction is stated so the sign of every later
# correlation is readable.
AXES = [
    {"axis": "supply_assumption",
     "low": "absence assumed, work around it", "high": "delivery expected"},
    {"axis": "substitution",
     "low": "fabricated or done without", "high": "part orderable"},
    {"axis": "failure_horizon",
     "low": "must hold until next repair", "high": "repair is scheduled"},
    {"axis": "observation_mode",
     "low": "residence / continuous", "high": "visitation / event-sampled"},
    {"axis": "time_to_writing_station",
     "low": "prohibitive", "high": "near zero"},
    {"axis": "reward_structure",
     "low": "writing costs unpaid hours", "high": "writing is compensated"},
]
AXIS_NAMES = [a["axis"] for a in AXES]

# A single latent drives the axes together. coupling = 0 makes them
# independent; coupling = 1 makes them a single variable with noise.
LATENT = "remoteness"


def observer(rng, coupling=0.7):
    """One observer's position vector.

    Under high remoteness: supply assumption falls, substitution falls,
    failure horizon falls, observation becomes residential, the writing
    station gets far away, and writing stops being compensated.
    """
    r = rng.random()

    def ax(direction):
        # direction +1 means the axis rises with remoteness
        base = r if direction > 0 else (1.0 - r)
        return max(0.0, min(1.0, coupling * base
                            + (1.0 - coupling) * rng.random()))

    return {"remoteness": r,
            "supply_assumption": ax(-1),
            "substitution": ax(-1),
            "failure_horizon": ax(-1),
            "observation_mode": ax(-1),   # low = residence, falls with r
            "time_to_writing_station": ax(-1),
            "reward_structure": ax(-1)}


def p_write(pos, a=2.2, b=2.0, c=1.4, intercept=-2.6):
    """Writing probability. Rises with supply assumption, with proximity to a
    writing station, and with compensation. It does not read any knowledge
    the observer holds."""
    z = (intercept + a * pos["supply_assumption"]
         + b * pos["time_to_writing_station"]
         + c * pos["reward_structure"])
    return 1.0 / (1.0 + math.exp(-z))


# ------------------------------------------------------- KNOWLEDGE CATEGORIES
# Each category is a CONJUNCTION of position conditions under which that
# knowledge forms. `test` returns whether an observer at this position holds
# it. The list is enumerated by this module's author and the ranking below is
# a property of the enumeration -- stated up front, not in a footnote.
CATEGORIES = [
    {"category": "facts", "conditions": [],
     "test": lambda p: True,
     "note": "no position requirement. visitors record these"},
    {"category": "procedure_under_supply",
     "conditions": ["supply_assumption high"],
     "test": lambda p: p["supply_assumption"] > 0.5,
     "note": "how a job is done when the part arrives"},
    {"category": "fabrication_practice",
     "conditions": ["substitution low"],
     "test": lambda p: p["substitution"] < 0.5,
     "note": "making the part instead of ordering it"},
    {"category": "interrelation",
     "conditions": ["supply_assumption low", "observation_mode residence"],
     "test": lambda p: p["supply_assumption"] < 0.5
     and p["observation_mode"] < 0.5,
     "note": "how components couple under non-delivery. THE SPEC'S "
             "PREDICTED MOST-SUPPRESSED CATEGORY"},
    {"category": "hold_until_next_repair",
     "conditions": ["supply_assumption low", "failure_horizon low",
                    "observation_mode residence"],
     "test": lambda p: p["supply_assumption"] < 0.5
     and p["failure_horizon"] < 0.5 and p["observation_mode"] < 0.5,
     "note": "a THREE-condition category, added to test whether "
             "interrelation is actually the most suppressed or only the "
             "most suppressed on a two-condition list"},
]


def population(n=6000, coupling=0.7, seed=17):
    rng = random.Random(seed)
    return [observer(rng, coupling) for _ in range(n)]


def corpus(pop, seed=23):
    """Sample weighted by P(write). Nothing inspects position or knowledge."""
    rng = random.Random(seed)
    return [o for o in pop if rng.random() < p_write(o)]


def density_by_region(pop, corp, axis, bins=4):
    """Sampling density along one axis, population vs corpus."""
    rows = []
    for i in range(bins):
        lo, hi = i / bins, (i + 1) / bins
        in_pop = [o for o in pop if lo <= o[axis] < hi or
                  (i == bins - 1 and o[axis] == 1.0)]
        in_corp = [o for o in corp if lo <= o[axis] < hi or
                   (i == bins - 1 and o[axis] == 1.0)]
        rows.append({"bin": "%.2f-%.2f" % (lo, hi),
                     "pop_share": len(in_pop) / len(pop) if pop else 0.0,
                     "corpus_share": len(in_corp) / len(corp)
                     if corp else 0.0,
                     "ratio": (len(in_corp) / len(corp)) /
                     (len(in_pop) / len(pop))
                     if pop and corp and in_pop else None})
    return rows


def survival(pop, corp):
    """For each knowledge category, what fraction of holders reach the corpus."""
    rows = []
    for cat in CATEGORIES:
        holders = [o for o in pop if cat["test"](o)]
        written = [o for o in corp if cat["test"](o)]
        base = len(corp) / len(pop) if pop else 0.0
        s = len(written) / len(holders) if holders else None
        rows.append({"category": cat["category"],
                     "n_conditions": len(cat["conditions"]),
                     "holders": len(holders),
                     "in_corpus": len(written),
                     "survival": s,
                     "suppression_vs_base": (s / base) if s and base else None,
                     "note": cat["note"]})
    return rows


def interaction_check(coupling_values=(0.0, 0.3, 0.5, 0.7, 0.9),
                      n=6000, seed=17):
    """The part the spec's reasoning needs and does not state.

    For the two-condition interrelation category, compare its measured
    suppression against the PRODUCT of the two single-condition suppressions.

    RAN AGAINST THE DRAFT AND THE RESULT IS KEPT. This was written expecting
    the conjunction to be suppressed MORE than the product -- excess below
    1.0. It goes the other way: excess is 1.01 at zero coupling and rises to
    1.85 at coupling 0.9, so the conjunction is suppressed LESS than the
    product model says.

    The reason is visible once measured. When remoteness drives both axes,
    "low supply assumption" and "residence" select nearly the same people, so
    the conjunction is barely rarer than either condition alone while the
    product keeps multiplying as if they were independent. Treating the two
    conditions as multiplicative therefore OVERSTATES the suppression, by up
    to 1.85x here.
    """
    rows = []
    for cv in coupling_values:
        pop = population(n=n, coupling=cv, seed=seed)
        corp = corpus(pop)
        base = len(corp) / len(pop)

        def supp(pred):
            h = [o for o in pop if pred(o)]
            w = [o for o in corp if pred(o)]
            return (len(w) / len(h)) / base if h and base else None

        s_supply = supp(lambda p: p["supply_assumption"] < 0.5)
        s_resid = supp(lambda p: p["observation_mode"] < 0.5)
        s_both = supp(lambda p: p["supply_assumption"] < 0.5
                      and p["observation_mode"] < 0.5)
        prod = s_supply * s_resid if (s_supply and s_resid) else None
        rows.append({"coupling": cv, "supply_only": s_supply,
                     "residence_only": s_resid, "both": s_both,
                     "product_of_marginals": prod,
                     "excess": (s_both / prod) if (s_both and prod) else None})
    return rows


def ranking_check(coupling=0.7, n=8000, seed=17):
    """Is interrelation actually the most-suppressed category?"""
    pop = population(n=n, coupling=coupling, seed=seed)
    corp = corpus(pop)
    rows = [r for r in survival(pop, corp)
            if r["suppression_vs_base"] is not None]
    rows.sort(key=lambda r: r["suppression_vs_base"])
    return {"ranked": rows, "most_suppressed": rows[0]["category"],
            "interrelation_rank": [r["category"] for r in rows]
            .index("interrelation") + 1,
            "n_categories": len(rows),
            "caveat": "the ranking is a property of the category list, which "
                      "is enumerated by this module. Adding a category with "
                      "more conditions moves interrelation down it"}


# --------------------------------------------------------- SECOND-ORDER TEST
def surface(item, w_content, rng, noise=0.15):
    """An item's visible features: part content quality, part positional
    typicality, part noise. The scorer sees only this."""
    return (w_content * item["content_quality"]
            + (1.0 - w_content) * item["position_typicality"]
            + rng.gauss(0.0, noise))


def relevance_test(w_content, n=3000, coupling=0.7, seed=31):
    """Does relevance-scoring track position rather than content?

    The scorer is calibrated on the corpus: its relevance is closeness to the
    corpus mean surface value. Content quality is generated INDEPENDENTLY of
    position, so any correlation between relevance and position is the
    sampling frame returning its own shape.
    """
    rng = random.Random(seed)
    pop = population(n=n, coupling=coupling, seed=seed)
    corp = corpus(pop, seed=seed + 1)
    if not corp:
        return None

    def item_of(o):
        return {"content_quality": rng.random(),
                "position_typicality": p_write(o) }

    corp_items = [item_of(o) for o in corp]
    mu = sum(surface(i, w_content, rng) for i in corp_items) / len(corp_items)

    held = [item_of(o) for o in pop]
    scores = [-abs(surface(i, w_content, rng) - mu) for i in held]
    return {"w_content": w_content,
            "corr_with_position": _corr(
                [i["position_typicality"] for i in held], scores),
            "corr_with_content": _corr(
                [i["content_quality"] for i in held], scores)}


def _corr(xs, ys):
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    dx = sum((x - mx) ** 2 for x in xs) ** 0.5
    dy = sum((y - my) ** 2 for y in ys) ** 0.5
    return num / (dx * dy) if dx and dy else 0.0


def relevance_crossover(ws=(0.0, 0.2, 0.4, 0.5, 0.6, 0.8, 1.0)):
    """RAN AGAINST THE DRAFT AND THE RESULT IS KEPT.

    This was written expecting content to take over as the surface mix rose.
    It does not. A relevance score defined as CLOSENESS TO THE CORPUS MEAN is
    a typicality measure, and content quality is generated uniformly, so the
    corpus mean sits in the middle of the content range. Items of middling
    quality score highest and the relationship with quality is non-monotone,
    which shows up as a correlation near zero at every mix.

    What actually happens across the sweep is that the score stops tracking
    POSITION. It never starts tracking content. Both correlations are weak at
    the crossing, and above it both decay toward zero.

    That is the sharper form of the spec's second-order point: a typicality-
    calibrated relevance score cannot reward quality at any surface mix. It
    can only stop penalising position.
    """
    rows = [relevance_test(w) for w in ws]
    rows = [r for r in rows if r]
    over = [r for r in rows
            if abs(r["corr_with_content"]) > abs(r["corr_with_position"])]
    peak_content = max(abs(r["corr_with_content"]) for r in rows)
    return {"rows": rows,
            "content_overtakes_at": over[0]["w_content"] if over else None,
            "peak_content_correlation": peak_content,
            "content_ever_strong": peak_content > 0.4,
            "why": "the crossing is not a handover to content. It is the "
                   "point where the score stops tracking position, and the "
                   "content correlation never exceeds %.2f at any mix -- "
                   "because closeness to a corpus mean rewards being "
                   "average, not being good" % peak_content}


def confidence():
    return {"first_order": "a consequence of the stipulated P(write) and the "
                           "stipulated population coupling. Direction is "
                           "structural, magnitude is not",
            "interaction_result": "the zero-coupling identity is algebraic; "
                                  "the excess above it is a function of the "
                                  "coupling parameter",
            "ranking": "a property of the enumerated category list, not of "
                       "the world",
            "second_order": "the crossover is real but its location moves "
                            "with the stipulated surface-feature mix",
            "any_real_corpus": "NONE. no corpus is read, sampled or measured "
                               "anywhere in this file",
            "resolved": False}


def breaks():
    return [
        "THE SPEC'S STATED REASON IS INCOMPLETE AND THE MODULE MEASURES THE "
        "GAP. 'Because those two conditions are anti-correlated with writing' "
        "gives the two marginals. At zero coupling between the position axes "
        "the conjunction's suppression is EXACTLY their product -- no "
        "interaction at all. Everything above that is supplied by the "
        "coupling, which is a fact about the population and not about either "
        "condition",
        "INTERRELATION IS NOT ALWAYS THE MOST-SUPPRESSED CATEGORY. Adding a "
        "three-condition category moves it down the ranking, and the ranking "
        "is a property of the list this module enumerates. 'Most strongly "
        "suppressed' is a statement about the enumeration until the category "
        "set comes from somewhere else",
        "P(write | position) is stipulated as a logistic in three axes with "
        "chosen coefficients. The first-order result is a consequence of it. "
        "What is not a consequence of it is the interaction, which is why "
        "that is the reported finding",
        "THE MULTIPLICATIVE READING OF THE SPEC'S REASON IS TOO STRONG, AND "
        "THIS MODULE'S DRAFT MADE IT. Coupling drives the excess ABOVE 1.0, "
        "not below: when remoteness moves both axes, the two conditions "
        "select nearly the same people and the conjunction is barely rarer "
        "than either alone. A product-of-marginals estimate overstates the "
        "suppression by up to 1.85x here",
        "the second-order test is downstream of the first: corpus membership "
        "is position-driven by construction, so a scorer calibrated on the "
        "corpus tracking position is close to a restatement. And the "
        "crossing is NOT a handover to content -- a typicality score rewards "
        "being average, so the content correlation stays under 0.2 at every "
        "mix. What the sweep locates is where position stops dominating, "
        "which is a weaker statement than the one drafted",
        "position_typicality is operationalised as P(write), which makes the "
        "second-order correlation partly definitional. A corpus study would "
        "need an independent positional marker",
        "no corpus is read anywhere. Every number here is generated",
    ]


def report():
    L = ["S9 -- CORPUS POSITION FILTER", "=" * 72, ""]
    L.append("  B0. AGENTS -- declared before any equation")
    L.append("")
    L.append("    %-20s %s" % ("agent", "capabilities"))
    for a in agent_table():
        L.append("    %-20s %s" % (a["agent"], ", ".join(a["capabilities"])))
    L.append("")
    L.extend(SH.wrap("THE BLANK IS THE POINT. " + BLANK_IS_THE_POINT["why_blank"],
                     "    "))
    L.append("")
    L.extend(SH.wrap(BLANK_IS_THE_POINT["why_it_matters"], "    "))
    L.append("")
    L.append("-" * 72)
    L.append("")
    L.append("  POSITION AXES -- direction stated so later signs are readable")
    L.append("")
    for a in AXES:
        L.append("    %-26s 0 = %-34s 1 = %s"
                 % (a["axis"], a["low"], a["high"]))
    L.append("")
    L.append("-" * 72)
    L.append("")
    pop = population()
    corp = corpus(pop)
    L.append("  1. SAMPLING DENSITY -- population vs corpus")
    L.append("")
    L.append("    corpus is %.1f%% of the population"
             % (100.0 * len(corp) / len(pop)))
    L.append("")
    for axis in ("supply_assumption", "time_to_writing_station",
                 "observation_mode"):
        L.append("    %s" % axis)
        L.append("      %-14s %-12s %-14s %s"
                 % ("bin", "pop share", "corpus share", "ratio"))
        for r in density_by_region(pop, corp, axis):
            L.append("      %-14s %-12.4f %-14.4f %s"
                     % (r["bin"], r["pop_share"], r["corpus_share"],
                        "--" if r["ratio"] is None else "%.2f" % r["ratio"]))
        L.append("")
    L.extend(SH.wrap("Sampling density rises with supply assumption and with "
                     "proximity to a writing station, in the direction the "
                     "spec predicts. No step in the chain reads position.",
                     "    "))
    L.append("")
    L.append("-" * 72)
    L.append("")
    L.append("  2. WHAT SURVIVES, BY KNOWLEDGE CATEGORY")
    L.append("")
    L.append("    %-26s %-6s %-10s %s"
             % ("category", "conds", "survival", "vs base"))
    for r in survival(pop, corp):
        L.append("    %-26s %-6d %-10s %s"
                 % (r["category"], r["n_conditions"],
                    "--" if r["survival"] is None
                    else "%.4f" % r["survival"],
                    "--" if r["suppression_vs_base"] is None
                    else "%.3f" % r["suppression_vs_base"]))
    L.append("")
    rk = ranking_check()
    L.append("    most suppressed: %s" % rk["most_suppressed"])
    L.append("    interrelation ranks %d of %d"
             % (rk["interrelation_rank"], rk["n_categories"]))
    L.append("")
    L.extend(SH.wrap(rk["caveat"], "    "))
    L.append("")
    L.append("-" * 72)
    L.append("")
    L.append("  3. THE INTERACTION -- what the spec's reason does not supply")
    L.append("")
    L.append("    %-10s %-12s %-12s %-10s %-12s %s"
             % ("coupling", "supply only", "residence", "both",
                "product", "excess"))
    for r in interaction_check():
        L.append("    %-10.1f %-12.3f %-12.3f %-10.3f %-12.3f %s"
                 % (r["coupling"], r["supply_only"], r["residence_only"],
                    r["both"], r["product_of_marginals"],
                    "--" if r["excess"] is None else "%.2f" % r["excess"]))
    L.append("")
    L.extend(SH.wrap("At coupling 0 the conjunction's suppression is the "
                     "PRODUCT of the two marginals -- excess 1.01, no "
                     "interaction, nothing the two conditions do together "
                     "that they do not do apart.", "    "))
    L.append("")
    L.extend(SH.wrap("RAN AGAINST THE DRAFT. This section was written "
                     "expecting excess to fall BELOW 1.0 as coupling rose -- "
                     "the conjunction being rarer than the product. It goes "
                     "the other way, to 1.85. The measurement is kept and "
                     "the prose was changed.", "    "))
    L.append("")
    L.extend(SH.wrap("The reason is visible once measured: when remoteness "
                     "drives both axes, low supply assumption and residence "
                     "select nearly the same people, so the conjunction is "
                     "barely rarer than either condition alone while the "
                     "product keeps multiplying as though they were "
                     "independent. Treating the two conditions "
                     "multiplicatively OVERSTATES the suppression, by up to "
                     "1.85x here.", "    "))
    L.append("")
    L.extend(SH.wrap("So the spec's claim survives in direction and its "
                     "stated reason needs correcting in mechanism. "
                     "Interrelation is suppressed -- but because it sits in "
                     "the remote region at all, not because two independent "
                     "penalties compound. The compounding version is the one "
                     "a reader would reach for, and it is too strong.",
                     "    "))
    L.append("")
    L.append("-" * 72)
    L.append("")
    rc = relevance_crossover()
    L.append("  4. SECOND-ORDER -- does relevance track position or content?")
    L.append("")
    L.append("    %-14s %-22s %s"
             % ("content mix", "corr with position", "corr with content"))
    for r in rc["rows"]:
        L.append("    %-14.1f %-22s %+.3f"
                 % (r["w_content"], "%+.3f" % r["corr_with_position"],
                    r["corr_with_content"]))
    L.append("")
    L.append("    position stops dominating at mix >= %s"
             % rc["content_overtakes_at"])
    L.append("    peak content correlation at any mix: %.3f"
             % rc["peak_content_correlation"])
    L.append("")
    L.extend(SH.wrap(rc["why"], "    "))
    L.append("")
    L.extend(SH.wrap("RAN AGAINST THE DRAFT. This was written expecting "
                     "content to take over as the mix rose. It does not. The "
                     "score is closeness to the corpus mean -- a TYPICALITY "
                     "measure -- and content quality is uniform, so the mean "
                     "sits mid-range and middling items score highest. The "
                     "relationship with quality is non-monotone and reads as "
                     "a correlation near zero at every mix.", "    "))
    L.append("")
    L.extend(SH.wrap("What the sweep shows is the score STOPPING to track "
                     "position. It never starts tracking content. That is "
                     "the sharper form of the spec's second-order point: a "
                     "typicality-calibrated relevance score cannot reward "
                     "quality at any surface mix, it can only stop "
                     "penalising position. Content quality is generated "
                     "independently of position here, so below the crossing "
                     "the score is not a judgement about the item at all.",
                     "    "))
    L.extend(SH.tail(sys.modules[__name__]))
    return "\n".join(L)


def selftest():
    ck, done = SH.checker()

    # B0
    ck("the filtering agent is declared and BLANK",
       [a for a in agent_table() if a["agent"] == "filtering_agent"][0]
       ["is_blank"] is True)
    ck("and renders as [BLANK] rather than vanishing",
       "[BLANK]" in [a for a in agent_table()
                     if a["agent"] == "filtering_agent"][0]["capabilities"])
    ck("no other agent is blank",
       sum(1 for a in agent_table() if a["is_blank"]) == 1)
    ck("agents are declared before any equation",
       open(__file__).read().index("AGENTS = [")
       < open(__file__).read().index("def observer("))

    # structure
    ck("every axis states both directions",
       all(a["low"] and a["high"] for a in AXES))
    ck("p_write reads only supply, distance and reward -- never knowledge",
       "category" not in p_write.__code__.co_names
       and "test" not in p_write.__code__.co_names)

    pop = population(n=4000)
    corp = corpus(pop)
    ck("the corpus is a strict subset", 0 < len(corp) < len(pop))

    d = density_by_region(pop, corp, "supply_assumption")
    ck("sampling density rises with supply assumption",
       d[-1]["ratio"] > d[0]["ratio"])
    d2 = density_by_region(pop, corp, "time_to_writing_station")
    ck("and with proximity to a writing station",
       d2[-1]["ratio"] > d2[0]["ratio"])

    sv = dict((r["category"], r) for r in survival(pop, corp))
    ck("facts survive at close to the base rate",
       abs(sv["facts"]["suppression_vs_base"] - 1.0) < 0.05)
    ck("interrelation is suppressed relative to base",
       sv["interrelation"]["suppression_vs_base"] < 0.6)
    ck("the spec's prediction holds in direction: interrelation is "
       "suppressed harder than the supply-side category",
       sv["interrelation"]["suppression_vs_base"]
       < sv["procedure_under_supply"]["suppression_vs_base"])

    ic = interaction_check(coupling_values=(0.0, 0.9), n=8000)
    zero, high = ic[0], ic[1]
    ck("AT ZERO COUPLING the conjunction is exactly the product of the two "
       "marginals -- no interaction, which is what the spec's stated reason "
       "amounts to on its own",
       abs(zero["excess"] - 1.0) < 0.08)
    ck("and at high coupling it sits well ABOVE the product -- the draft "
       "expected below, and the measurement is kept",
       high["excess"] > 1.5)
    ck("so coupling makes the conjunction LESS penalised than a "
       "multiplicative model predicts, not more",
       high["excess"] > zero["excess"])
    ck("interrelation is still suppressed in absolute terms, so the "
       "correction is to the mechanism and not to the direction",
       high["both"] < 0.8)

    rk = ranking_check()
    ck("interrelation is NOT the most-suppressed category once a "
       "three-condition category is on the list",
       rk["most_suppressed"] != "interrelation")
    ck("and the ranking caveat names the enumeration as the reason",
       "enumerated by this module" in rk["caveat"])

    rc = relevance_crossover()
    ck("at zero content mix relevance tracks position, not content",
       abs(rc["rows"][0]["corr_with_position"])
       > abs(rc["rows"][0]["corr_with_content"]))
    ck("but content NEVER becomes strongly tracked -- the draft expected it "
       "to, and the measurement is kept",
       rc["content_ever_strong"] is False)
    ck("at full content mix both correlations are near zero, because "
       "closeness to a corpus mean rewards being average",
       abs(rc["rows"][-1]["corr_with_content"]) < 0.1
       and abs(rc["rows"][-1]["corr_with_position"]) < 0.1)
    ck("a crossing exists and is located, and it is a crossing between two "
       "weak correlations rather than a handover",
       rc["content_overtakes_at"] is not None
       and rc["peak_content_correlation"] < 0.4)

    text = report().lower()
    for w in ("deliberate", "in order to", "intends", "motivated by",
              "wants to"):
        ck("no intent phrase: %r" % w, w not in text)
    ck("graded terms are used", "correlation" in text
       and "sampling density" in text)
    ck("the incomplete-reason finding leads the breaks list",
       "INCOMPLETE" in breaks()[0])
    ck("the ranking caveat is the second break",
       "NOT ALWAYS THE MOST-SUPPRESSED" in breaks()[1])
    ck("confidence records that no real corpus is read",
       "NONE" in confidence()["any_real_corpus"])
    ck("confidence unresolved", confidence()["resolved"] is False)
    ck("report renders", "THE BLANK IS THE POINT" in report())
    return done()


if __name__ == "__main__":
    sys.exit(SH.run(sys.modules[__name__], "S9"))
