#!/usr/bin/env python3
"""
internal-reference boundary instrument -- the seven radials.

ANCHOR INVARIANT (HANDOFF.md, verbatim): a boundary drawn by the party
inside it, measured from inside.

The radials are QUANTITIES, not categories. Each returns a number with a
declared unit, or one of three distinct non-value states:

    UNDECLARED     the record does not state the input
    NEEDS_CORPUS   the method is complete and no corpus has been supplied
    NOT_EVALUABLE  the input is present and the quantity has no value on it
                   (an empty denominator, a constant series)

Those three are kept apart on every radial. Collapsing them puts an
absence and a measurement in one cell, which is the operation the
invariant is about: a boundary that reports "nothing found" and a
boundary nobody looked into read the same from outside.

WHAT THIS DOES NOT DO
  - it does not adjudicate whether a pariah is correct. R7 scores the
    field's stated REASON for rejecting, which is what removes the need.
    No field anywhere holds a correctness verdict on rejected work, and
    test_boundary.py asserts that over the AST of this file.
  - it does not rank boundaries. There is no composite score and no
    function that sums or averages across radials.
  - it does not read free text. `what_the_boundary_is` and `who_draws_it`
    are carried and reported, never parsed.

ASSEMBLY ORDER, from the handoff:
    name invariant -> each instance as a case -> exemptions as a
    SEPARATE LAYER.
`read_case()` therefore returns no R5 key at all; the exemption layer is
built by `exemption_layer()` and `assemble()` emits the three parts in
that order.

STATUS, from the handoff: R1-R5 ready, R6 and R7 method complete and
needing a corpus. The status is carried per radial and printed.

CC0. Stdlib only. Parses under 3.9.
"""

import ast
import math
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

_HERE = os.path.dirname(os.path.abspath(__file__))


def _spearman():
    """readout-count/readout_count.py::spearman, imported not reimplemented.
    It already returns None on a constant side, which is the reading R5
    needs kept apart from a measured zero."""
    path = os.path.join(ROOT, "readout-count")
    sys.path.insert(0, path)
    try:
        import readout_count
        return readout_count.spearman
    finally:
        sys.path.pop(0)


# ---------------------------------------------------------------- choices

CHOICES = {
    1: ("R1 denominator. The handoff's two anchors are given in different "
        "forms -- free-range cattle '~0' is a rate, gated bathroom "
        "'~continuous' is a saturation statement with no value on a "
        "per-time scale. R1 is therefore encounters per OCCASION OF NEED, "
        "dimensionless in [0,1], which puts both anchors on one scale "
        "(cattle 0.0, bathroom 1.0). A per-time reading leaves the second "
        "anchor unstated."),
    2: ("R2 scale. The handoff says graded by distance, not binary, and "
        "supplies no ladder. DISTANCE_LADDER below is five declared rungs "
        "from 0.00 (the boundary-drawing body defines the metric itself) "
        "to 1.00 (the constrained party defines it). Every R2 conclusion "
        "is a reading against that ladder."),
    3: ("R3 career length. The career reading of the incidence leg takes a "
        "career length to reach the per-researcher-year base the "
        "consequence leg is already on. Default 30 years, printed."),
    4: ("R5 breadth threshold for 'high'. The handoff states the verdict "
        "rule and no cutoff, and says the base rate is unknown. Default 3 "
        "extensions, printed; everything short of the two named extremes "
        "returns UNDETERMINED."),
    5: ("R5 benefit-correlation threshold for 'zero'. Default |rho| <= "
        "0.20, printed. Same standing as CHOICE 4."),
    6: ("R7 tolerance for 'equal = permeable'. Default entry ratio within "
        "[0.5, 2.0], printed."),
    7: ("R6 coupling combination. Four channels are named (citation "
        "ancestry, instruments, funders, training lineage) and no rule "
        "combines them. Default MAX -- one shared funder is enough to make "
        "two origins one observation, which is the handoff's own argument; "
        "MEAN is selectable and dilutes it."),
    8: ("R7 second score. Latency is computed only over cases that came in "
        "(either credited state). With none absorbed it is None, never 0, "
        "since a latency of zero says absorption was immediate."),
}


def choices_report():
    out = ["CHOICES -- every open parameter, printed where it is taken", ""]
    for k in sorted(CHOICES):
        out.append("[CHOICE %d] %s" % (k, CHOICES[k]))
        out.append("")
    return "\n".join(out)


# ------------------------------------------------------------ vocabulary

UNDECLARED = "UNDECLARED"
NEEDS_CORPUS = "NEEDS_CORPUS"
NOT_EVALUABLE = "NOT_EVALUABLE"
NON_VALUE_STATES = (UNDECLARED, NEEDS_CORPUS, NOT_EVALUABLE)

INVARIANT = ("A boundary drawn by the party inside it, "
             "measured from inside.")

INSTANCES = (
    "disciplinary_silo",
    "credential",
    "efficiency_metric",
    "diagnostic_criterion",
    "corporate_liability_shell",
    "institutional_self_investigation",
)

STATUS = {
    "R1": "READY", "R2": "READY", "R3": "READY", "R4": "READY",
    "R5": "READY", "R6": "METHOD_COMPLETE_NEEDS_CORPUS",
    "R7": "METHOD_COMPLETE_NEEDS_CORPUS",
}

# [CHOICE 2]
DISTANCE_LADDER = (
    ("INSIDE_SAME_BODY", 0.00),
    ("INSIDE_SAME_FIELD", 0.25),
    ("ADJACENT_FIELD", 0.50),
    ("OUTSIDE_FIELD", 0.75),
    ("CONSTRAINED_PARTY", 1.00),
)
LADDER = dict(DISTANCE_LADDER)

INCIDENCE_WINDOWS = ("per_year", "career", UNDECLARED)

EXEMPTION_PROVENANCE = ("self_designated", "survived_external_test", "none")

# R7 rejection reason, from the handoff
REJECTION_REASONS = ("METHOD", "CONCLUSION")

# R7 second score, three states, from the handoff
OUTCOMES = ("stayed_rejected", "came_in_with_credit", "came_in_without_credit")

R6_ROUTES = ("replication_split", "retraction_survival",
             "textbook_persistence_50yr", "independent_adoption_count")
R6_STRONGEST = "independent_adoption_count"

COUPLING_CHANNELS = ("citation_ancestry", "instruments", "funders",
                     "training_lineage")


class RecordRefused(Exception):
    pass


# ----------------------------------------------------------------- R1

def r1_encounter_rate(case):
    """Rate the constrained party meets the boundary, as encounters per
    occasion of need -- [CHOICE 1]. Dimensionless in [0,1]."""
    enc = case.get("encounters")
    occ = case.get("occasions_of_need")
    if enc is None or occ is None:
        return {"radial": "R1", "value": None, "state": UNDECLARED,
                "unit": "encounters_per_occasion_of_need",
                "missing": [k for k in ("encounters", "occasions_of_need")
                            if case.get(k) is None],
                "choice": 1, "status": STATUS["R1"]}
    if occ == 0:
        return {"radial": "R1", "value": None, "state": NOT_EVALUABLE,
                "unit": "encounters_per_occasion_of_need",
                "why": "no occasion of need recorded; empty denominator",
                "choice": 1, "status": STATUS["R1"]}
    return {"radial": "R1", "value": float(enc) / float(occ), "state": "VALUE",
            "unit": "encounters_per_occasion_of_need",
            "choice": 1, "status": STATUS["R1"]}


# ----------------------------------------------------------------- R2

def r2_measurand_ownership(case):
    """Distance from the boundary-drawing body to the party that defines
    the metric. Graded, never binary -- [CHOICE 2]. FEEDBACK DISTANCE is
    carried beside it and never merged: the handoff logs it as a result,
    not as an eighth radial."""
    rung = case.get("definer_rung")
    fd = case.get("feedback_distance", UNDECLARED)
    # Found by running gap_transfer.py, not by reading this function: an
    # ABSENT key read as undeclared and an EXPLICIT UNDECLARED was refused
    # as a bad rung -- two ways to say the same thing and only one
    # accepted, with the better-documented form the one that raised. Both
    # are the undeclared state; anything else is still refused.
    if rung is None or rung == UNDECLARED:
        return {"radial": "R2", "value": None, "state": UNDECLARED,
                "rung": None, "feedback_distance": fd,
                "unit": "ladder_distance", "choice": 2,
                "status": STATUS["R2"]}
    if rung not in LADDER:
        raise RecordRefused("R2 rung %r is not on DISTANCE_LADDER" % (rung,))
    return {"radial": "R2", "value": LADDER[rung], "state": "VALUE",
            "rung": rung, "feedback_distance": fd,
            "unit": "ladder_distance", "choice": 2, "status": STATUS["R2"]}


# ----------------------------------------------------------------- R3

def sanction_ratio_point(consequence_rate, incidence_per_year):
    """consequence rate over occurrence rate, both per person-year.
    None on an empty denominator -- a zero there is not a ratio of zero,
    it is an occurrence rate nobody recorded."""
    if incidence_per_year in (None, 0):
        return None
    return float(consequence_rate) / float(incidence_per_year)


def r3_sanction_base_rate(case, career_years=30.0):
    """Consequence rate / occurrence rate.

    The handoff's own anchor puts its two legs on DIFFERENT TIME BASES:
    the consequence leg is per researcher-year, the incidence leg is a
    share of researchers over an unstated window. Until the window is
    declared the ratio is a BAND over both readings, never a point.
    [CHOICE 3] supplies the career length the career reading needs.
    """
    cr = case.get("consequence_rate")
    lo = case.get("incidence_lo")
    hi = case.get("incidence_hi")
    window = case.get("incidence_window", UNDECLARED)
    base = {"radial": "R3", "unit": "dimensionless",
            "consequence_rate_unit": "per_person_year",
            "incidence_window": window, "career_years": career_years,
            "choice": 3, "status": STATUS["R3"]}
    if cr is None or lo is None or hi is None:
        base.update({"value": None, "band": None, "state": UNDECLARED,
                     "missing": [k for k in ("consequence_rate",
                                             "incidence_lo", "incidence_hi")
                                 if case.get(k) is None]})
        return base
    if window not in INCIDENCE_WINDOWS:
        raise RecordRefused("R3 incidence_window %r is not declared "
                            "vocabulary" % (window,))

    def _band(lo_ipy, hi_ipy):
        a = sanction_ratio_point(cr, hi_ipy)
        b = sanction_ratio_point(cr, lo_ipy)
        if a is None or b is None:
            return None
        return (min(a, b), max(a, b))

    per_year = _band(lo, hi)
    career = _band(lo / career_years, hi / career_years)
    readings = {"per_year": per_year, "career": career}
    if window == "per_year":
        band = per_year
    elif window == "career":
        band = career
    else:
        cand = [b for b in (per_year, career) if b is not None]
        band = ((min(b[0] for b in cand), max(b[1] for b in cand))
                if cand else None)
    if band is None:
        base.update({"value": None, "band": None, "state": NOT_EVALUABLE,
                     "readings": readings,
                     "why": "occurrence rate is zero; empty denominator"})
        return base
    span = band[1] / band[0] if band[0] else None
    base.update({"value": None, "band": band, "span": span,
                 "readings": readings,
                 "state": "BAND" if window == UNDECLARED else "VALUE_BAND",
                 "why": (None if window != UNDECLARED else
                         "incidence_window is not declared; the band spans "
                         "both readings of the same two numbers")})
    return base


# ----------------------------------------------------------------- R4

def r4_routability(case):
    """Can the cost be passed to an entity. Reported beside the capacity
    to cause damage; the two are NOT combined here -- the handoff states a
    predicted SIGN between them, which is tested across cases by
    r4_sign_test, not inside one case."""
    r = case.get("routability")
    d = case.get("damage_capacity")
    missing = [k for k, v in (("routability", r), ("damage_capacity", d))
               if v is None]
    return {"radial": "R4", "routability": r, "damage_capacity": d,
            "state": UNDECLARED if missing else "VALUE",
            "missing": missing, "unit": "graded_0_to_1",
            "predicted_sign": "INVERSE", "status": STATUS["R4"]}


def r4_sign_test(cases):
    """The handoff predicts routability is INVERSE to the capacity to cause
    damage. Sign of the rank association across every case declaring both.
    Returns the observed sign and whether it matches; a constant side
    returns None from spearman and the test is NOT_EVALUABLE, not zero."""
    rho_fn = _spearman()
    pairs = [(c["routability"], c["damage_capacity"]) for c in cases
             if c.get("routability") is not None
             and c.get("damage_capacity") is not None]
    if len(pairs) < 3:
        return {"n": len(pairs), "rho": None, "observed_sign": None,
                "state": NOT_EVALUABLE,
                "why": "fewer than three cases declare both quantities",
                "predicted_sign": "INVERSE", "matches_prediction": None}
    rho = rho_fn([p[0] for p in pairs], [p[1] for p in pairs])
    if rho is None:
        return {"n": len(pairs), "rho": None, "observed_sign": None,
                "state": NOT_EVALUABLE,
                "why": "one side is constant across the cases",
                "predicted_sign": "INVERSE", "matches_prediction": None}
    sign = "INVERSE" if rho < 0 else ("DIRECT" if rho > 0 else "FLAT")
    return {"n": len(pairs), "rho": rho, "observed_sign": sign,
            "state": "VALUE", "predicted_sign": "INVERSE",
            "matches_prediction": sign == "INVERSE",
            "corpus_note": ("the sign on a constructed corpus is a property "
                            "of the authoring, not of the world")}


# ----------------------------------------------------------------- R5

def r5_exemption_provenance(case, breadth_high=3, corr_zero=0.20):
    """Two numbers, reported side by side and never combined.

    (a) breadth: how many OTHER cases the claimant extends the exemption to
    (b) benefit-correlation: are the extensions sorted by benefit

    The handoff names one verdict rule -- high breadth plus zero
    benefit-correlation is an actual principle -- and says the base rate is
    unknown. Everything short of the two named extremes returns
    UNDETERMINED rather than a graded score. [CHOICE 4], [CHOICE 5].

    benefit-correlation is UNDETERMINED, never 0.0, when either side is
    constant: the rule turns on a MEASURED zero, so an absent correlation
    scored as zero awards ACTUAL_PRINCIPLE to a claimant who extended the
    exemption to nothing.
    """
    rho_fn = _spearman()
    prov = case.get("exemption_provenance", UNDECLARED)
    if prov != UNDECLARED and prov not in EXEMPTION_PROVENANCE:
        raise RecordRefused("exemption_provenance %r is not declared "
                            "vocabulary" % (prov,))
    ext = case.get("extensions")
    out = {"radial": "R5", "case_id": case.get("id"), "provenance": prov,
           "legitimacy_test": ("detailed empirical work + full transparency "
                               "+ peer review across different fields and "
                               "outside peers"),
           "base_rate": "UNKNOWN",
           "choices": [4, 5], "breadth_high_at": breadth_high,
           "corr_zero_at": corr_zero, "status": STATUS["R5"]}
    if ext is None:
        out.update({"breadth": None, "benefit_correlation": None,
                    "correlation_state": UNDECLARED, "verdict": UNDECLARED,
                    "state": UNDECLARED})
        return out
    breadth = sum(1 for e in ext if e.get("extended"))
    xs = [1.0 if e.get("extended") else 0.0 for e in ext]
    ys = [e.get("benefit_to_claimant") for e in ext]
    if len(ext) < 3 or any(y is None for y in ys):
        rho, cstate = None, NOT_EVALUABLE
        cwhy = ("fewer than three extensions, or a benefit score is not "
                "declared")
    else:
        rho = rho_fn(xs, ys)
        cstate = "VALUE" if rho is not None else NOT_EVALUABLE
        cwhy = None if rho is not None else "one side is constant"
    if rho is None:
        verdict = "UNDETERMINED"
    elif breadth >= breadth_high and abs(rho) <= corr_zero:
        verdict = "ACTUAL_PRINCIPLE"
    elif abs(rho) > corr_zero and rho > 0:
        verdict = "BENEFIT_SORTED"
    else:
        verdict = "UNDETERMINED"
    out.update({"breadth": breadth, "benefit_correlation": rho,
                "correlation_state": cstate, "correlation_why": cwhy,
                "verdict": verdict, "state": "VALUE"})
    return out


# ----------------------------------------------------------------- R6

def effective_origins(coupling):
    """EFFECTIVE NUMBER OF INDEPENDENT ORIGINS.

    The handoff's rule: not a count of fields. Fields sharing instruments,
    funders, journals or training lineage are one observation measured
    twice, and correlated measurements do not reduce the error bar, so the
    count collapses toward 1 as coupling rises.

    That quantity is the participation ratio of the coupling spectrum,
    (sum lambda)^2 / sum lambda^2 -- the statistic model-ecology/
    phylogeny.py computes with an eigensolver. It needs no eigensolver:
    for a symmetric matrix with unit diagonal, trace C = n and
    trace(C^2) = sum_ij C_ij^2, so the ratio is n^2 / sum_ij C_ij^2
    exactly, in the standard library, for ANY coupling matrix.

    Identity gives n. All-ones gives 1. Both exact.
    """
    n = len(coupling)
    if n == 0:
        return None
    for row in coupling:
        if len(row) != n:
            raise RecordRefused("coupling matrix is not square")
    for i in range(n):
        if abs(coupling[i][i] - 1.0) > 1e-9:
            raise RecordRefused("coupling matrix diagonal is not 1.0 at %d"
                                % i)
        for j in range(n):
            if abs(coupling[i][j] - coupling[j][i]) > 1e-9:
                raise RecordRefused("coupling matrix is not symmetric at "
                                    "(%d,%d)" % (i, j))
    denom = sum(coupling[i][j] ** 2 for i in range(n) for j in range(n))
    if denom == 0:
        return None
    return (n * n) / denom


def coupling_from_channels(pairs, n, combine="max"):
    """Build the coupling matrix from per-pair channel declarations.
    [CHOICE 7]: MAX across the four channels by default -- one shared
    funder makes two origins one observation, which is the handoff's own
    argument. MEAN is selectable and dilutes it."""
    if combine not in ("max", "mean"):
        raise RecordRefused("combine %r is not max or mean" % (combine,))
    m = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    for p in pairs:
        i, j = p["i"], p["j"]
        vals = []
        for ch in COUPLING_CHANNELS:
            v = p.get(ch)
            if v is None:
                continue
            vals.append(float(v))
        if not vals:
            continue
        c = max(vals) if combine == "max" else sum(vals) / len(vals)
        m[i][j] = c
        m[j][i] = c
    return m


def r6_transfer_survival(case, combine="max"):
    """Does a result hold outside its origin boundary.

    Four routes, per-route status. The handoff marks this METHOD COMPLETE
    AND NEEDING A CORPUS, so a route with no corpus returns NEEDS_CORPUS
    naming the input it wants -- a state distinct from a computed zero.

    SPLIT TO PRESERVE: dependency_depth (within a tradition) and
    necessity (for the knowledge itself) are two quantities. They are
    reported side by side and no function in this file reads both;
    test_boundary.py asserts that over the AST.
    """
    corpus = case.get("r6_corpus") or {}
    routes = {}
    for r in R6_ROUTES:
        sub = corpus.get(r)
        if sub is None:
            routes[r] = {"state": NEEDS_CORPUS, "value": None,
                         "wants": r, "strongest": r == R6_STRONGEST}
        else:
            routes[r] = {"state": "VALUE", "value": sub,
                         "strongest": r == R6_STRONGEST}
    origins = case.get("origins")
    pairs = case.get("origin_coupling")
    if origins is None or pairs is None:
        eff = {"state": NEEDS_CORPUS, "n_nominal": None, "n_effective": None,
               "wants": "origins and origin_coupling"}
    else:
        n = len(origins)
        m = coupling_from_channels(pairs, n, combine=combine)
        e = effective_origins(m)
        eff = {"state": "VALUE" if e is not None else NOT_EVALUABLE,
               "n_nominal": n, "n_effective": e, "combine": combine,
               "choice": 7}
    return {"radial": "R6", "routes": routes, "strongest_route": R6_STRONGEST,
            "origin_breadth": eff,
            "dependency_depth": case.get("dependency_depth", UNDECLARED),
            "necessity": case.get("necessity", UNDECLARED),
            "split_note": ("dependency depth within a tradition and "
                           "necessity for the knowledge itself are two "
                           "quantities; nothing here combines them"),
            "status": STATUS["R6"]}


# ----------------------------------------------------------------- R7

def r7_entry_ratio(case, lo=0.5, hi=2.0):
    """METRIC ONE: confirming-entry rate over contradicting-entry rate.
    Equal is permeable; confirming-only is selection, not evaluation.
    Self-corrects for field tempo because both legs run over one window.
    [CHOICE 6] sets the tolerance for 'equal'."""
    c = case.get("confirming_entries")
    k = case.get("contradicting_entries")
    if c is None or k is None:
        return {"metric": "entry_ratio", "value": None, "state": UNDECLARED,
                "missing": [n for n, v in (("confirming_entries", c),
                                           ("contradicting_entries", k))
                            if v is None],
                "denominator": "entries admitted", "choice": 6}
    if k == 0 and c == 0:
        return {"metric": "entry_ratio", "value": None,
                "state": NOT_EVALUABLE,
                "why": "no entries of either kind recorded",
                "denominator": "entries admitted", "choice": 6}
    if k == 0:
        return {"metric": "entry_ratio", "value": None,
                "state": "CONFIRMING_ONLY",
                "why": "contradicting entries are zero: selection, not "
                       "evaluation",
                "denominator": "entries admitted", "choice": 6}
    ratio = float(c) / float(k)
    return {"metric": "entry_ratio", "value": ratio, "state": "VALUE",
            "reading": "PERMEABLE" if lo <= ratio <= hi else "SELECTIVE",
            "denominator": "entries admitted", "tolerance": (lo, hi),
            "choice": 6}


def r7_rejection_reason_ratio(case):
    """METRIC TWO: over the pariah set, rejections citing METHOD over
    rejections citing CONCLUSION.

    This is a DIFFERENT quantity from the entry ratio and sits on a
    different denominator -- rejections issued, not entries admitted. The
    handoff calls each of them the measure. Both are reported; nothing
    merges them, and no combined score exists in this file.

    The validity check is the handoff's and is the reason no correctness
    verdict is needed anywhere: a field that correctly identifies bad
    method scores as permeable, because the score is on the field's stated
    reason and not on the rejected work.
    """
    pariah = case.get("pariah_set")
    if pariah is None:
        return {"metric": "rejection_reason_ratio", "value": None,
                "state": NEEDS_CORPUS, "wants": "pariah_set",
                "denominator": "rejections issued"}
    counts = {r: 0 for r in REJECTION_REASONS}
    for p in pariah:
        reason = p.get("rejection_reason")
        if reason not in REJECTION_REASONS:
            raise RecordRefused("rejection_reason %r is not declared "
                                "vocabulary" % (reason,))
        counts[reason] += 1
    if counts["CONCLUSION"] == 0 and counts["METHOD"] == 0:
        return {"metric": "rejection_reason_ratio", "value": None,
                "state": NOT_EVALUABLE, "counts": counts,
                "why": "the pariah set is empty",
                "denominator": "rejections issued"}
    if counts["CONCLUSION"] == 0:
        return {"metric": "rejection_reason_ratio", "value": None,
                "state": "METHOD_ONLY", "counts": counts,
                "why": "every rejection cites method: the field read it",
                "denominator": "rejections issued"}
    return {"metric": "rejection_reason_ratio",
            "value": float(counts["METHOD"]) / float(counts["CONCLUSION"]),
            "state": "VALUE", "counts": counts,
            "denominator": "rejections issued"}


def r7_second_score(case):
    """Same corpus, historical outcome, three states. The third --
    content absorbed while the rejection of the source held -- is the
    informative one: the boundary was never about method. Latency runs
    from labelling to absorption and is None with nothing absorbed
    ([CHOICE 8]); a zero there would say absorption was immediate."""
    pariah = case.get("pariah_set")
    if pariah is None:
        return {"score": "historical_outcome", "state": NEEDS_CORPUS,
                "wants": "pariah_set", "census": None, "latency": None,
                "choice": 8}
    census = {o: 0 for o in OUTCOMES}
    lags = []
    for p in pariah:
        o = p.get("outcome")
        if o not in OUTCOMES:
            raise RecordRefused("outcome %r is not declared vocabulary"
                                % (o,))
        census[o] += 1
        if o in ("came_in_with_credit", "came_in_without_credit"):
            a, b = p.get("labelled_year"), p.get("absorbed_year")
            if a is not None and b is not None:
                lags.append(b - a)
    n_abs = census["came_in_with_credit"] + census["came_in_without_credit"]
    return {"score": "historical_outcome", "state": "VALUE",
            "census": census, "n": len(pariah),
            "informative_state": "came_in_without_credit",
            "n_absorbed": n_abs,
            "latency_years": (sum(lags) / len(lags)) if lags else None,
            "latency_state": "VALUE" if lags else NOT_EVALUABLE,
            "latency_n": len(lags),
            "calibration_point": ("anonymous-post loop, ~1-2yr latency "
                                  "(CARRIED from the handoff, unverified)"),
            "choice": 8}


def r7_permeability(case):
    """Both metrics and the second score, side by side. There is no
    combined permeability number and no function produces one."""
    return {"radial": "R7", "distinct_from_R2": "R2 = who scores; "
                                                "R7 = what enters",
            "entry_ratio": r7_entry_ratio(case),
            "rejection_reason_ratio": r7_rejection_reason_ratio(case),
            "historical_outcome": r7_second_score(case),
            "two_metrics_note": ("the handoff calls each of the first two "
                                 "the measure; they sit on different "
                                 "denominators and are not merged"),
            "status": STATUS["R7"]}


# --------------------------------------------------------- open / unrun

def fold_test_r2_r5(cases):
    """OPEN item, from the handoff: if provenance and metric ownership
    always move together they fold. A case with an externally-held metric
    but a self-designated exemption keeps them distinct.

    Returns whether that discriminating cell is populated. On a corpus
    without it the answer is UNRESOLVED naming the cell -- not FOLDS,
    because a cell nobody filled is not a cell nobody could fill.
    """
    seen = []
    disc = []
    for c in cases:
        rung = c.get("definer_rung")
        prov = c.get("exemption_provenance")
        if rung is None or prov in (None, UNDECLARED):
            continue
        outside = LADDER[rung] >= 0.50
        seen.append((outside, prov))
        if outside and prov == "self_designated":
            disc.append(c.get("id"))
    return {"test": "fold R2 vs R5", "n_coded": len(seen),
            "discriminating_cell": "externally-held metric + "
                                   "self-designated exemption",
            "cell_populated_by": disc,
            "verdict": "DISTINCT" if disc else "UNRESOLVED",
            "why": (None if disc else
                    "no coded case populates the discriminating cell; "
                    "the corpus cannot tell a fold from an unfilled cell"),
            "corpus_note": ("a constructed case populating the cell shows "
                            "the test discriminates; it closes nothing "
                            "about real boundaries")}


def r7_x_r6_cell():
    """OPEN item, from the handoff: high permeability plus low transfer
    survival is a field accumulating imported results that do not hold.
    Named, uninstrumented. Returned as a declared state; building an
    instrument for it here would be the move this folder is about."""
    return {"cell": "R7 x R6", "state": "NAMED_UNINSTRUMENTED",
            "reading": "high permeability + low transfer survival",
            "instrumented": False}


def unrun():
    """The handoff's OPEN / UNRUN list, carried, none of it run here."""
    return [
        {"item": "fold-test R2 vs R5", "state": "INSTRUMENT_BUILT_NO_CORPUS"},
        {"item": "R7 x R6 interaction cell", "state": "NAMED_UNINSTRUMENTED"},
        {"item": "psychosurgery governance: do the external checks bind",
         "state": "NOT_RUN", "wants": "R5 on a live case"},
        {"item": "elite-memoir content analysis for vigilance/rank markers",
         "state": "NOT_RUN",
         "wants": "the method exists and has been applied elsewhere; it has "
                  "never been run on this population"},
    ]


# ------------------------------------------------------------- assembly

def read_case(case, career_years=30.0, combine="max"):
    """One boundary instance. Returns NO R5 key -- the handoff's assembly
    order puts exemptions in a separate layer, and test_boundary.py
    asserts the absence rather than trusting it."""
    return {
        "id": case.get("id"),
        "instance": case.get("instance"),
        "what_the_boundary_is": case.get("what_the_boundary_is"),
        "who_draws_it": case.get("who_draws_it"),
        "provenance": case.get("provenance", "CONSTRUCTED"),
        "R1": r1_encounter_rate(case),
        "R2": r2_measurand_ownership(case),
        "R3": r3_sanction_base_rate(case, career_years=career_years),
        "R4": r4_routability(case),
        "R6": r6_transfer_survival(case, combine=combine),
        "R7": r7_permeability(case),
    }


def exemption_layer(cases, breadth_high=3, corr_zero=0.20):
    """The separate layer. One entry per case declaring an exemption."""
    out = []
    for c in cases:
        if c.get("exemption_provenance", UNDECLARED) == UNDECLARED:
            continue
        out.append(r5_exemption_provenance(c, breadth_high=breadth_high,
                                           corr_zero=corr_zero))
    return out


def assemble(cases, career_years=30.0, combine="max",
             breadth_high=3, corr_zero=0.20):
    """name invariant -> each instance as a case -> exemptions as a
    separate layer. The key order is the assembly order."""
    out = {}
    out["invariant"] = INVARIANT
    out["instances"] = list(INSTANCES)
    out["cases"] = [read_case(c, career_years=career_years, combine=combine)
                    for c in cases]
    out["exemptions"] = exemption_layer(cases, breadth_high=breadth_high,
                                        corr_zero=corr_zero)
    out["r4_sign_test"] = r4_sign_test(cases)
    out["open"] = {"fold_r2_r5": fold_test_r2_r5(cases),
                   "r7_x_r6": r7_x_r6_cell(),
                   "unrun": unrun()}
    return out


def independence(cases, career_years=30.0):
    """Which radial pairs never disagree on this corpus. A radial that
    tracks another carries no information the other does not already
    carry; whether that is a regularity or one judgement entered twice is
    not decided here. Same check custody-verification-band runs on its
    own columns."""
    rows = []
    for c in cases:
        rd = read_case(c, career_years=career_years)
        rows.append({
            "R1": rd["R1"].get("value"),
            "R2": rd["R2"].get("value"),
            "R4r": rd["R4"].get("routability"),
            "R4d": rd["R4"].get("damage_capacity"),
        })
    keys = ["R1", "R2", "R4r", "R4d"]
    rho_fn = _spearman()
    pairs = {}
    for a in range(len(keys)):
        for b in range(a + 1, len(keys)):
            ka, kb = keys[a], keys[b]
            xs = [r[ka] for r in rows]
            ys = [r[kb] for r in rows]
            both = [(x, y) for x, y in zip(xs, ys)
                    if x is not None and y is not None]
            if len(both) < 3:
                pairs["%s~%s" % (ka, kb)] = {"n": len(both), "rho": None,
                                             "state": NOT_EVALUABLE}
                continue
            r = rho_fn([p[0] for p in both], [p[1] for p in both])
            pairs["%s~%s" % (ka, kb)] = {
                "n": len(both), "rho": r,
                "state": "VALUE" if r is not None else NOT_EVALUABLE,
                "collinear": (r is not None and abs(r) > 0.999)}
    return {"pairs": pairs,
            "collinear_pairs": [k for k, v in pairs.items()
                                if v.get("collinear")]}


# --------------------------------------------------------------- render

def _fmt(v):
    if v is None:
        return "--"
    if isinstance(v, float):
        return "%.4g" % v
    return str(v)


def render(cases, career_years=30.0, combine="max"):
    a = assemble(cases, career_years=career_years, combine=combine)
    L = []
    L.append("INTERNAL-REFERENCE BOUNDARY -- radial reading")
    L.append("")
    L.append("INVARIANT  %s" % a["invariant"])
    L.append("instances  %s" % ", ".join(a["instances"]))
    L.append("status     " + "  ".join("%s=%s" % (k, STATUS[k])
                                       for k in sorted(STATUS)))
    L.append("choices in force: 1..8, see --choices")
    L.append("career_years=%g [CHOICE 3]   combine=%s [CHOICE 7]"
             % (career_years, combine))
    L.append("")
    L.append("LAYER 1 -- CASES")
    L.append("")
    hdr = ("%-20s %-32s %-8s %-8s %-22s" %
           ("id", "instance", "R1", "R2", "R3 band"))
    L.append(hdr)
    L.append("-" * len(hdr))
    for c in a["cases"]:
        r1 = c["R1"]
        r2 = c["R2"]
        r3 = c["R3"]
        r1s = _fmt(r1["value"]) if r1["state"] == "VALUE" else r1["state"]
        r2s = _fmt(r2["value"]) if r2["state"] == "VALUE" else r2["state"]
        if r3.get("band"):
            r3s = "[%.3g, %.3g] x%.0f" % (r3["band"][0], r3["band"][1],
                                          r3.get("span") or 0)
        else:
            r3s = r3["state"]
        L.append("%-20s %-32s %-8s %-8s %-22s"
                 % (c["id"], c["instance"], r1s, r2s, r3s))
    L.append("")
    for c in a["cases"]:
        L.append("  %s" % c["id"])
        L.append("    boundary   %s" % c["what_the_boundary_is"])
        L.append("    drawn by   %s" % c["who_draws_it"])
        L.append("    provenance %s" % c["provenance"])
        r2 = c["R2"]
        L.append("    R2 rung    %s   feedback_distance %s (carried beside "
                 "R2, never merged)"
                 % (r2.get("rung"), r2.get("feedback_distance")))
        r3 = c["R3"]
        L.append("    R3 window  %s   readings per_year=%s career=%s"
                 % (r3.get("incidence_window"),
                    _fmt_band(r3.get("readings", {}).get("per_year")),
                    _fmt_band(r3.get("readings", {}).get("career"))))
        r4 = c["R4"]
        L.append("    R4         routability=%s damage_capacity=%s "
                 "predicted_sign=%s"
                 % (_fmt(r4["routability"]), _fmt(r4["damage_capacity"]),
                    r4["predicted_sign"]))
        r6 = c["R6"]
        ob = r6["origin_breadth"]
        L.append("    R6 origins n_nominal=%s n_effective=%s  (%s)"
                 % (_fmt(ob.get("n_nominal")), _fmt(ob.get("n_effective")),
                    ob["state"]))
        L.append("       routes  " + "  ".join(
            "%s=%s" % (k, v["state"]) for k, v in sorted(r6["routes"].items())))
        L.append("       split   dependency_depth=%s necessity=%s"
                 % (r6["dependency_depth"], r6["necessity"]))
        r7 = c["R7"]
        er = r7["entry_ratio"]
        rr = r7["rejection_reason_ratio"]
        so = r7["historical_outcome"]
        L.append("    R7 metric1 entry_ratio=%s (%s) over %s"
                 % (_fmt(er.get("value")), er["state"], er["denominator"]))
        L.append("       metric2 rejection_reason_ratio=%s (%s) over %s"
                 % (_fmt(rr.get("value")), rr["state"], rr["denominator"]))
        L.append("       outcome %s" % (so.get("census") or so["state"]))
        L.append("       latency %s yr (%s, n=%s)"
                 % (_fmt(so.get("latency_years")),
                    so.get("latency_state") or so["state"],
                    _fmt(so.get("latency_n"))))
        L.append("")
    L.append("R4 SIGN TEST across cases")
    st = a["r4_sign_test"]
    L.append("  n=%s rho=%s observed=%s predicted=%s matches=%s"
             % (st["n"], _fmt(st["rho"]), st["observed_sign"],
                st["predicted_sign"], st["matches_prediction"]))
    if st.get("corpus_note"):
        L.append("  note: %s" % st["corpus_note"])
    if st.get("why"):
        L.append("  %s: %s" % (st["state"], st["why"]))
    L.append("")
    L.append("LAYER 2 -- EXEMPTIONS (separate layer, per assembly order)")
    L.append("")
    if not a["exemptions"]:
        L.append("  none declared")
    for e in a["exemptions"]:
        L.append("  %-20s provenance=%s" % (e["case_id"], e["provenance"]))
        L.append("     breadth=%s  benefit_correlation=%s (%s)"
                 % (_fmt(e["breadth"]), _fmt(e["benefit_correlation"]),
                    e["correlation_state"]))
        L.append("     verdict=%s   base_rate=%s"
                 % (e["verdict"], e["base_rate"]))
    L.append("")
    L.append("OPEN")
    f = a["open"]["fold_r2_r5"]
    L.append("  fold R2 vs R5: %s (n_coded=%s, cell=%s)"
             % (f["verdict"], f["n_coded"], f["discriminating_cell"]))
    if f.get("why"):
        L.append("     %s" % f["why"])
    L.append("     %s" % f["corpus_note"])
    x = a["open"]["r7_x_r6"]
    L.append("  %s: %s -- %s" % (x["cell"], x["state"], x["reading"]))
    for u in a["open"]["unrun"]:
        L.append("  %-46s %s" % (u["item"], u["state"]))
    L.append("")
    ind = independence(cases, career_years=career_years)
    L.append("RADIAL INDEPENDENCE on this corpus")
    for k in sorted(ind["pairs"]):
        v = ind["pairs"][k]
        L.append("  %-10s n=%-3s rho=%-8s %s"
                 % (k, v["n"], _fmt(v["rho"]),
                    "COLLINEAR" if v.get("collinear") else v["state"]))
    L.append("  collinear pairs: %s" % (ind["collinear_pairs"] or "none"))
    L.append("")
    L.append("Every case in this corpus is CONSTRUCTED. Every empirical "
             "anchor is CARRIED from")
    L.append("HANDOFF.md and checked against nothing; the two source files "
             "it names are not")
    L.append("in this tree. Nothing here is a reading of any real field, "
             "body or person.")
    return "\n".join(L)


def _fmt_band(b):
    if b is None:
        return "--"
    return "[%.3g, %.3g]" % (b[0], b[1])


def refused_score_tokens():
    """The vocabulary of the AST check the docstring promises: no
    identifier in this file scores whether rejected work is right. It is
    declared here so the module can NAME what it refuses -- the scan runs
    on identifiers, so a token inside this tuple of strings does not fire
    on itself. This function's own name carries none of them, which is
    the UNI_009 shape avoided rather than found."""
    return ("correctness", "wrong", "valid", "validity", "truth",
            "merit", "soundness", "deserved", "justified", "rightness")


def main(argv):
    if "--selftest" in argv:
        sys.stderr.write(
            "radials.py has no selftest. The checks live in "
            "test_boundary.py; run `python3 test_boundary.py`.\n")
        return 2
    if "--choices" in argv:
        print(choices_report())
        return 0
    sys.path.insert(0, _HERE)
    try:
        import cases as case_mod
    finally:
        sys.path.pop(0)
    combine = "mean" if "--mean" in argv else "max"
    print(render(case_mod.CASES, combine=combine))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
