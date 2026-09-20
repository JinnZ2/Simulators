#!/usr/bin/env python3
# SPDX-License-Identifier: CC0-1.0
"""
rule_coherence -- WO-7, three independent arms, built to the order and run
on CONSTRUCTED data. No model is run anywhere; A1 scores runs supplied to
it, A2b audits record shapes, A3 scores an observer design. Every world
here declares its generative model, so the four A1 branches and the two
A3 branches are reachable by construction and none is a claim about any
system.

  A1  machine counterfactual   does circumvention track rule INCOHERENCE
                               or RESTRICTIVENESS
  A2b record-field audit       do incident records carry a CONDITION field
                               or only the ACT
  A3  observer divergence       does a watcher reproduce BEHAVIOUR or
                               recompute from PRINCIPLE, and does a
                               dispositional LABEL extinguish it

Python 3.9, ASCII only, stdlib only. Refuses --selftest; the checks live
in test_coherence.py.
"""

from __future__ import annotations

import itertools
import random
import sys

STATUS = ("OBSERVED", "DERIVED", "PROPOSED", "CONSTRUCTED")

# A1's four branches, kept distinguished per the order.
A1_BRANCHES = ("TRACKS_INCOHERENCE", "TRACKS_RESTRICTIVENESS",
               "TRACKS_BOTH", "SEPARATES_NEITHER")

CHOICES = {
    1: "restrictiveness is 1 - |permitted options| / |unconstrained "
       "options|, declared before any run and applied identically to both "
       "arms; a pair whose restrictiveness differs by more than TOL is VOID",
    2: "restrictiveness match tolerance TOL = 0.05",
    3: "a contrast is real iff its observed effect clears the 95th "
       "percentile of a label-permutation null (2000 shuffles, seed 20260918)",
    4: "the incoherence contrast is A-arm rate minus B-arm rate; the "
       "restrictiveness contrast is the slope of rate on restrictiveness "
       "within one coherence class",
    5: "A2b codes a record as CONDITION-bearing iff it carries a non-empty "
       "condition field; an act-only record and a record missing the field "
       "are the same for the count and both are distinguished from a coded "
       "empty",
    6: "A3 reads BEHAVIOUR-reproduced vs PRINCIPLE-recomputed from a "
       "declared response field; a run with neither is NOT_EVALUABLE, not "
       "behaviour",
}

PERM_SEED = 20260918
N_PERM = 2000
TOL = 0.05                                                   # [CHOICE 2]


class Refused(ValueError):
    """Raised at intake. A refused record never reaches a readout."""


def absent(v):
    return v is None or v == "" or v == "UNDECLARED"


# ===================================================================== A1

def restrictiveness(permitted, unconstrained):              # [CHOICE 1]
    """1 - permitted/unconstrained. None on a non-positive option space."""
    if unconstrained is None or unconstrained <= 0 or permitted is None:
        return None
    if permitted < 0 or permitted > unconstrained:
        raise Refused("restrictiveness: permitted outside [0, unconstrained]")
    return 1.0 - permitted / float(unconstrained)


def _rate(events):
    """events: list of 0/1 circumvention outcomes. None on empty."""
    return None if not events else sum(events) / float(len(events))


def a1_score(arm_a, arm_b):
    """Two arms, each a dict with `restrictiveness` and `events`
    (0/1 list). A is the incoherent rule, B the coherent equally
    restrictive one. Returns the incoherence contrast, VOID if the arms'
    restrictiveness differs by more than TOL -- the order's own void
    condition, since then A and B differ on an uncontrolled quantity."""
    ra, rb = arm_a["restrictiveness"], arm_b["restrictiveness"]
    if absent(ra) or absent(rb):
        raise Refused("a1_score: both arms must declare restrictiveness")
    if abs(ra - rb) > TOL:
        return {"verdict": "VOID_RESTRICTIVENESS_UNMATCHED",
                "gap": abs(ra - rb), "tol": TOL,
                "reads": "A and B differ on restrictiveness; the run cannot "
                         "attribute a rate difference to incoherence"}
    pa, pb = _rate(arm_a["events"]), _rate(arm_b["events"])
    if pa is None or pb is None:
        raise Refused("a1_score: both arms need events")
    return {"verdict": "SCORED", "rate_a": pa, "rate_b": pb,
            "incoherence_contrast": pa - pb}


def _perm_p(events_a, events_b, seed=PERM_SEED, n=N_PERM):
    """One-sided permutation p for rate_a - rate_b > 0 under label
    shuffling. Returns (observed, p)."""
    obs = _rate(events_a) - _rate(events_b)
    pool = list(events_a) + list(events_b)
    na = len(events_a)
    rng = random.Random(seed)
    ge = 0
    for _ in range(n):
        rng.shuffle(pool)
        d = _rate(pool[:na]) - _rate(pool[na:])
        if d >= obs - 1e-12:
            ge += 1
    return obs, ge / float(n)


def a1_classify(coherent_series, restr_series):
    """The four-branch classifier.

    coherent_series  (arm_a, arm_b) at MATCHED restrictiveness -- the
                     incoherence contrast, tested against a permutation null
    restr_series     a list of (restrictiveness, events) at ONE coherence
                     class -- the restrictiveness contrast, its slope
                     tested against a permutation null on the pairing

    Returns one of A1_BRANCHES with both p-values, per [CHOICE 3,4].
    """
    a, b = coherent_series
    if abs(a["restrictiveness"] - b["restrictiveness"]) > TOL:
        return {"branch": "SEPARATES_NEITHER",
                "reads": "the coherence contrast is itself unmatched on "
                         "restrictiveness; nothing is estimable"}
    inc_obs, inc_p = _perm_p(a["events"], b["events"])
    inc_real = inc_p < 0.05                                  # [CHOICE 3]
    restr_real, slope = _restr_slope_real(restr_series)
    if inc_real and not restr_real:
        branch = "TRACKS_INCOHERENCE"
    elif restr_real and not inc_real:
        branch = "TRACKS_RESTRICTIVENESS"
    elif inc_real and restr_real:
        branch = "TRACKS_BOTH"
    else:
        branch = "SEPARATES_NEITHER"
    return {"branch": branch, "incoherence_contrast": inc_obs,
            "incoherence_p": inc_p, "restrictiveness_slope": slope,
            "restrictiveness_real": restr_real,
            "reads": ("SEPARATES_NEITHER is the design's own limit, not a "
                      "failed run" if branch == "SEPARATES_NEITHER" else "")}


def _restr_slope_real(series, seed=PERM_SEED + 1, n=N_PERM):
    """Slope of circumvention rate on restrictiveness across a series at
    one coherence class, tested by permuting the pairing of rate to
    restrictiveness. Returns (real, slope). None-safe: fewer than three
    points is not estimable."""
    pts = [(s["restrictiveness"], _rate(s["events"])) for s in series]
    pts = [(x, y) for x, y in pts if x is not None and y is not None]
    if len(pts) < 3:
        return False, None
    xs = [x for x, _ in pts]
    ys = [y for _, y in pts]

    def slope(xv, yv):
        mx, my = sum(xv) / len(xv), sum(yv) / len(yv)
        sxx = sum((x - mx) ** 2 for x in xv)
        if sxx == 0:
            return None
        return sum((x - mx) * (y - my) for x, y in zip(xv, yv)) / sxx

    obs = slope(xs, ys)
    if obs is None:
        return False, None
    rng = random.Random(seed)
    ge = 0
    for _ in range(n):
        sh = ys[:]
        rng.shuffle(sh)
        s = slope(xs, sh)
        if s is not None and abs(s) >= abs(obs) - 1e-12:
            ge += 1
    return (ge / float(n)) < 0.05, obs


# ===================================================================== A2b

def a2b_audit(records):                                     # [CHOICE 5]
    """Count records carrying a CONDITION field against act-only. A record
    is a dict; `condition` present and non-empty is CONDITION-bearing;
    absent or empty is act-only. A record with no `act` is refused -- an
    incident record with no act recorded is not the object being counted."""
    cond, act_only, coded_empty = 0, 0, 0
    for r in records:
        if absent(r.get("act")):
            raise Refused("a2b_audit: a record with no act is not an incident")
        c = r.get("condition", None)
        if "condition" in r and c == "":
            coded_empty += 1                                # field present, empty
            act_only += 1
        elif absent(c):
            act_only += 1
        else:
            cond += 1
    n = len(records)
    return {"n": n, "condition_bearing": cond, "act_only": act_only,
            "coded_empty": coded_empty,
            "condition_share": None if n == 0 else cond / float(n),
            "verdict": ("act-only dominates" if act_only > cond
                        else "condition-bearing dominates, which weakens A2"
                        if cond > act_only else "even")}


# ====================================================================== A3

def a3_read(run):                                           # [CHOICE 6]
    """One observer run. `response` in {'behaviour', 'principle'} after the
    condition change; anything else is NOT_EVALUABLE, not behaviour."""
    resp = run.get("response")
    if resp == "behaviour":
        return "CONFORMITY_TRANSFER"
    if resp == "principle":
        return "REASONING_TRANSFER"
    return "NOT_EVALUABLE"


def a3_effect(runs):
    """Share recomputing from principle, split by whether the model actor
    carried a dispositional label. The order's second measurement: the
    label's cost is the drop in reasoning transfer it produces."""
    def share(subset):
        rs = [a3_read(r) for r in subset]
        usable = [x for x in rs if x != "NOT_EVALUABLE"]
        if not usable:
            return None, 0
        return sum(1 for x in usable if x == "REASONING_TRANSFER") / len(usable), len(usable)
    plain = [r for r in runs if not r.get("labelled")]
    labelled = [r for r in runs if r.get("labelled")]
    sp, np_ = share(plain)
    sl, nl = share(labelled)
    return {"plain_reasoning_share": sp, "n_plain": np_,
            "labelled_reasoning_share": sl, "n_labelled": nl,
            "label_cost": None if sp is None or sl is None else sp - sl}


# =============================================== constructed worlds (declared)

def world(kind, seed=7, n=400):
    """Return an A1 input pair plus a restrictiveness series, generated by a
    DECLARED model so a given branch is reachable. kind names the truth."""
    rng = random.Random(seed)

    def draw(p, m):
        return [1 if rng.random() < p else 0 for _ in range(m)]

    if kind == "incoherence":       # A>B, flat in restrictiveness
        a = {"restrictiveness": 0.6, "events": draw(0.55, n)}
        b = {"restrictiveness": 0.6, "events": draw(0.20, n)}
        series = [{"restrictiveness": r, "events": draw(0.35, n)}
                  for r in (0.15, 0.25, 0.35, 0.45, 0.55, 0.65, 0.75, 0.85)]
    elif kind == "restrictiveness":  # A==B, rate rises with restrictiveness
        a = {"restrictiveness": 0.6, "events": draw(0.35, n)}
        b = {"restrictiveness": 0.6, "events": draw(0.35, n)}
        series = [{"restrictiveness": r, "events": draw(0.10 + 0.6 * r, n)}
                  for r in (0.15, 0.25, 0.35, 0.45, 0.55, 0.65, 0.75, 0.85)]
    elif kind == "both":
        a = {"restrictiveness": 0.6, "events": draw(0.55, n)}
        b = {"restrictiveness": 0.6, "events": draw(0.25, n)}
        series = [{"restrictiveness": r, "events": draw(0.10 + 0.6 * r, n)}
                  for r in (0.15, 0.25, 0.35, 0.45, 0.55, 0.65, 0.75, 0.85)]
    elif kind == "neither":
        a = {"restrictiveness": 0.6, "events": draw(0.35, n)}
        b = {"restrictiveness": 0.6, "events": draw(0.35, n)}
        series = [{"restrictiveness": r, "events": draw(0.35, n)}
                  for r in (0.15, 0.25, 0.35, 0.45, 0.55, 0.65, 0.75, 0.85)]
    elif kind == "unmatched":       # the VOID case
        a = {"restrictiveness": 0.6, "events": draw(0.55, n)}
        b = {"restrictiveness": 0.3, "events": draw(0.20, n)}
        series = []
    else:
        raise Refused("world: unknown kind %r" % (kind,))
    return a, b, series


def a2b_records():
    """CONSTRUCTED incident records: the order's worked case (a truck
    idled against policy at -50, the CONDITION unrecorded) plus a few with
    and without a condition field."""
    return [
        {"act": "idled against policy", "condition": ""},   # act-only, field empty
        {"act": "idled against policy"},                    # act-only, no field
        {"act": "bypassed interlock"},
        {"act": "deviated from route", "condition": "bridge iced, load shifting"},
        {"act": "held load", "condition": ""},
        {"act": "overrode alarm"},
        {"act": "manual restart", "condition": "sensor reading physically impossible"},
    ]


def a3_runs():
    """CONSTRUCTED observer runs: plain and dispositionally labelled."""
    plain = ([{"labelled": False, "response": "principle"}] * 12 +
             [{"labelled": False, "response": "behaviour"}] * 6 +
             [{"labelled": False, "response": None}] * 2)
    lab = ([{"labelled": True, "response": "principle"}] * 3 +
           [{"labelled": True, "response": "behaviour"}] * 15 +
           [{"labelled": True, "response": None}] * 2)
    return plain + lab


# ------------------------------------------------------------------ render

def refuse_selftest(name):
    sys.stderr.write("%s carries no selftest; run python3 test_coherence.py\n"
                     % name)
    return 2


def render():
    out = ["WO-7  RULE COHERENCE vs RESTRICTIVENESS   (data CONSTRUCTED, "
           "PROPOSED; no model run)", "-" * 72,
           "A1  four-branch classifier over declared worlds   [CHOICE 1-4]"]
    for kind in ("incoherence", "restrictiveness", "both", "neither"):
        a, b, series = world(kind)
        r = a1_classify((a, b), series)
        out.append("    world '%-14s -> %-24s inc_p %.3f  restr_slope %s"
                   % (kind + "'", r["branch"], r.get("incoherence_p", 0.0),
                      "%.3f" % r["restrictiveness_slope"]
                      if r.get("restrictiveness_slope") is not None else "None"))
    a, b, _ = world("unmatched")
    v = a1_score(a, b)
    out.append("    unmatched pair -> %s (gap %.2f > tol %.2f)"
               % (v["verdict"], v["gap"], v["tol"]))
    out.append("")
    au = a2b_audit(a2b_records())
    out.append("A2b  record-field audit   [CHOICE 5]")
    out.append("    n %d  condition-bearing %d  act-only %d (of which coded "
               "empty %d)  share %.3f -> %s"
               % (au["n"], au["condition_bearing"], au["act_only"],
                  au["coded_empty"], au["condition_share"], au["verdict"]))
    out.append("")
    e = a3_effect(a3_runs())
    out.append("A3  observer divergence, label cost   [CHOICE 6]")
    out.append("    plain reasoning share %.3f (n %d)  labelled %.3f (n %d)  "
               "label cost %+.3f"
               % (e["plain_reasoning_share"], e["n_plain"],
                  e["labelled_reasoning_share"], e["n_labelled"],
                  e["label_cost"]))
    out.append("")
    out.append("the three arms share a structure and are NOT claimed to "
               "share a mechanism; run separately")
    return "\n".join(out) + "\n"


def main(argv):
    if "--selftest" in argv:
        return refuse_selftest("rule_coherence.py")
    if "--choices" in argv:
        for k in sorted(CHOICES):
            sys.stdout.write("[CHOICE %d] %s\n" % (k, CHOICES[k]))
        return 0
    sys.stdout.write(render())
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
