#!/usr/bin/env python3
# pipeline.py -- CC0, stdlib only, phone-buildable, parses under 3.9
#
# The spec's post-processing pipeline, built as specified. The spec says
# this half is "stdlib, phone-buildable"; the router (2D unsteady solve)
# is "the only non-phone term". So:
#
#   THE ROUTER OUTPUT IS AN INPUT. This file never runs a hydraulic
#   solver. It consumes a time-resolved depth field -- the thing the
#   router emits -- and derives observable-indicator rules from it. Here
#   that field is SYNTHETIC (see ensembles.py), constructed to exercise
#   the pipeline; nothing in this folder is a claim about any real
#   community, drainage, road, or household.
#
# The pipeline is faithful to the spec's steps 1-6. Where the spec
# leaves a boundary case undefined (a tie in wetting time, a run where
# neither landmark wets), the choice is marked [CHOICE] and the
# consequence is in AUDIT_NOTES / audit.py.

import os
import sys

INF = float("inf")


# ----------------------------------------------------------- step 1

class Landmark(object):
    """A thing a resident can see. `visible_when` is a depth at which the
    water is observable at that feature (over a deck, at girders, at a
    known mark) -- not a gauge reading."""
    def __init__(self, lid, visible_when, is_route=False):
        self.id = lid
        self.visible_when = float(visible_when)
        self.is_route = bool(is_route)


# A "field" here is the router output at the granularity the pipeline
# consumes: field[run_id][landmark_id] = depth time series (one depth per
# timestep). Faithful to the spec's depth(x,y,t) via t_wet below, without
# pretending to a full 2D solve this environment cannot produce.


# ----------------------------------------------------------- step 2

def t_wet(field, lm, run):
    """First timestep at which depth at the landmark crosses its
    visibility threshold. INF if it never does. Exactly the spec's
    def."""
    series = field[run][lm.id]
    for t, d in enumerate(series):
        if d >= lm.visible_when:
            return t
    return INF


# ----------------------------------------------------------- step 3

def _sign(x):
    if x > 0:
        return 1
    if x < 0:
        return -1
    return 0


# [CHOICE] A run in which NEITHER landmark wets (both INF) carries no
# ordering information -- INF - INF is undefined. The spec's sign()/
# all_same() do not say. Such runs are EXCLUDED from a pair's stability
# check rather than counted as agreement or as a flip. Excluding them is
# the honest reading (no information), and the consequence is recorded.
def _ordering(field, A, B, runs):
    signs = []
    used = []
    for r in runs:
        ta, tb = t_wet(field, A, r), t_wet(field, B, r)
        if ta == INF and tb == INF:
            continue                      # no ordering information
        signs.append(_sign(ta - tb))
        used.append(r)
    return signs, used


def stable_pairs(landmarks, field, runs):
    """Pairs whose wetting ORDER holds across every informative run.

    The spec: 'a rule is only usable if the ORDER holds across the
    ensemble ... if all_same(order)'. Strict: a single flip drops the
    pair. A tie (sign 0) is a distinct value from -1/+1, so a pair that
    is A-before-B in some runs and A-with-B in others is dropped too --
    see audit.py OIR_003 on why that is the safe direction to err."""
    out = []
    for i in range(len(landmarks)):
        for j in range(i + 1, len(landmarks)):
            A, B = landmarks[i], landmarks[j]
            signs, used = _ordering(field, A, B, runs)
            if not signs:
                continue                  # no informative run for this pair
            if len(set(signs)) == 1:
                consensus = signs[0]
                # order it so the earlier-wetting landmark is first
                if consensus <= 0:
                    out.append((A, B, used))
                else:
                    out.append((B, A, used))
    return out


# ----------------------------------------------------------- step 4

def _percentile(xs, p):
    if not xs:
        return None
    s = sorted(xs)
    if len(s) == 1:
        return s[0]
    k = (len(s) - 1) * (p / 100.0)
    lo = int(k)
    hi = min(lo + 1, len(s) - 1)
    frac = k - lo
    return s[lo] * (1 - frac) + s[hi] * frac


def lead(A, B, field, runs):
    """Lead-time band from A (earlier) to B (later). Deltas over runs
    where BOTH wet -- the spec's `if both_wet`. `min`/`p10` are the
    plan-against-the-short-end anchors; the card never uses the median.

    NOTE: the both-wet filter drops runs where B wets and A does not
    (a miss) and where A wets and B does not (a false alarm). The miss
    case is caught by step 3 (it flips the sign); the false-alarm case
    is NOT -- see reliability() and audit.py OIR_002."""
    deltas = []
    for r in runs:
        ta, tb = t_wet(field, A, r), t_wet(field, B, r)
        if ta == INF or tb == INF:
            continue
        deltas.append(tb - ta)
    if not deltas:
        return None
    return {"min": min(deltas), "p10": _percentile(deltas, 10),
            "p50": _percentile(deltas, 50), "p90": _percentile(deltas, 90),
            "n_both_wet": len(deltas)}


def reliability(trigger, hazard, field, runs):
    """The two error rates the lead band does not carry.

    A card says 'IF trigger wet THEN hazard coming'. Its failures:
      MISS         hazard wets, trigger dry   -- fatal, no warning
      FALSE_ALARM  trigger wets, hazard dry   -- cry-wolf, erodes trust

    Step 3 drops a pair on any miss (the sign flips), so a kept trigger
    has miss_rate ~ 0 by construction. It does NOT drop on a false alarm
    (a dry hazard reads as trigger-before-hazard, the SAME sign as a true
    positive), so false_alarm_rate is unconstrained by step 3 and is
    computed here. The spec's pipeline computes neither."""
    miss = fa = tp = neither = 0
    for r in runs:
        tt = t_wet(field, trigger, r)
        th = t_wet(field, hazard, r)
        if th != INF and tt == INF:
            miss += 1
        elif tt != INF and th == INF:
            fa += 1
        elif tt != INF and th != INF:
            tp += 1
        else:
            neither += 1
    fired = tp + fa
    hazard_runs = tp + miss
    return {
        "true_positive": tp, "miss": miss, "false_alarm": fa,
        "neither": neither,
        "miss_rate": None if not hazard_runs else round(miss / float(hazard_runs), 4),
        "false_alarm_rate": None if not fired else round(fa / float(fired), 4),
    }


# ----------------------------------------------------------- step 5

# [CHOICE] Movement time -- how long it takes the household to complete
# evacuation once it acts. The spec names it (`movement_time`) and gives
# no value; it is a per-community input, not a physical constant, so it
# is a parameter here with no default baked into a claim.
def rule_for(H, landmarks, field, runs, movement_time):
    """The route-coupled rule for household H.

    If the route closes before H floods, the trigger must be upstream of
    the door -- a landmark that reliably wets before the route closes,
    with enough lead to complete movement."""
    routes = [lm for lm in landmarks if lm.is_route]
    if not routes:
        return {"buildable": False, "reason": "no route landmark"}
    # t_route: earliest route-closure across informative runs, short end
    route_mins = []
    for r in runs:
        ts = [t_wet(field, lm, r) for lm in routes]
        ts = [t for t in ts if t != INF]
        if ts:
            route_mins.append(min(ts))
    if not route_mins:
        return {"buildable": False, "reason": "route never closes in ensemble"}
    t_route_short = min(route_mins)
    deadline = t_route_short - movement_time
    # candidate triggers: reliably wet before the route (a stable pair
    # trigger -> route-landmark with trigger earlier), and wet by deadline
    stable = stable_pairs(landmarks, field, runs)
    route_ids = set(lm.id for lm in routes)
    candidates = []
    for earlier, later, used in stable:
        if later.id in route_ids and not earlier.is_route:
            # earliest this trigger is ever seen (short end)
            tt = min(t_wet(field, earlier, r) for r in used
                     if t_wet(field, earlier, r) != INF)
            if tt <= deadline:
                candidates.append((earlier, later, tt))
    if not candidates:
        return {"buildable": False,
                "reason": "no stable trigger leaves movement_time before "
                          "the route closes"}
    # the LAST landmark before the deadline: latest trigger that still
    # leaves enough time, so the household is not evacuated needlessly early
    trigger, route_lm, tt = max(candidates, key=lambda c: c[2])
    rel = reliability(trigger, H, field, runs)
    lb = lead(trigger, H, field, runs)
    return {"buildable": True, "trigger": trigger.id, "route": route_lm.id,
            "t_route_short": t_route_short, "movement_time": movement_time,
            "trigger_wets_by": tt, "reliability": rel, "lead_to_H": lb}


# ----------------------------------------------------------- step 6

def build_card(rule):
    if not rule.get("buildable"):
        return "NO CARD: " + rule.get("reason", "not buildable")
    rel = rule["reliability"]
    lb = rule["lead_to_H"]
    lines = []
    lines.append("+" + "-" * 52 + "+")
    lines.append("| IF   water is over <%s>" % rule["trigger"])
    lines.append("| THEN <%s> closes in ~%s steps"
                 % (rule["route"],
                    rule["t_route_short"] - rule["trigger_wets_by"]))
    if lb:
        lines.append("|      your area floods ~%s to %s steps after"
                     % (lb["min"], lb["p90"]))
    lines.append("| ACT  leave now, via the open route, NOT via <%s>"
                 % rule["route"])
    # the two numbers the spec's card does not carry:
    lines.append("| REL  false-alarm rate %s   miss rate %s"
                 % (rel["false_alarm_rate"], rel["miss_rate"]))
    lines.append("+" + "-" * 52 + "+")
    return "\n".join(lines)


def derive(landmarks, field, runs, household=None, movement_time=1):
    """The whole pipeline. Returns the stable rules and, if a household
    landmark is given, the route-coupled card.

    FALSIFIABLE: if step 3 finds no stable orderings, this returns an
    empty rule set -- the spec's 'empty output is a valid, honest
    result', not a fabricated rule."""
    stable = stable_pairs(landmarks, field, runs)
    result = {"n_landmarks": len(landmarks), "n_runs": len(runs),
              "stable_pairs": [(a.id, b.id) for a, b, _u in stable],
              "n_stable": len(stable), "empty": len(stable) == 0}
    if household is not None:
        result["card_rule"] = rule_for(household, landmarks, field, runs,
                                        movement_time)
    return result


if __name__ == "__main__":
    if "--selftest" in sys.argv[1:]:
        sys.stderr.write(
            "pipeline.py has no checks of its own. The checks that "
            "exercise it live in selftest_oir.py.\n"
            "    python3 observable-indicator-rules/selftest_oir.py\n")
        sys.exit(2)
    HERE = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, HERE)
    import ensembles as ENS
    print("PIPELINE ON SYNTHETIC ENSEMBLES (see ensembles.py)")
    print("Nothing below is a real community; every field is constructed.")
    print("")
    for name in ("stable", "flipping", "false_alarm_heavy"):
        lms, field, runs, H, mt = getattr(ENS, name)()
        r = derive(lms, field, runs, household=H, movement_time=mt)
        print("== %s ==" % name)
        print("  stable pairs: %d   empty output: %s"
              % (r["n_stable"], r["empty"]))
        if "card_rule" in r:
            print(build_card(r["card_rule"]))
        print("")
