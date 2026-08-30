#!/usr/bin/env python3
# audit.py -- CC0, stdlib only, phone-buildable, parses under 3.9
#
# What building the pipeline surfaces. The pipeline itself is faithful to
# the spec (pipeline.py); this is what running it on controlled
# ensembles shows, and where the spec's card is silent.
#
# THE ROUTER IS AN INPUT AND IS NOT RUN. Every field is synthetic
# (ensembles.py). Nothing here is a claim about any real community; the
# findings are about the pipeline's logic, which is a property of the
# post-processing and not of any field.

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pipeline as P  # noqa: E402
import ensembles as ENS  # noqa: E402


def falsifiable_fires():
    """The spec's own falsifiable condition, checked both ways.

    'If step 3 finds no stable orderings ... this method returns nothing
    rather than a false rule.' The flipping ensemble must return empty;
    the stable ensemble must not."""
    lf, ff, rf, _h, _m = ENS.flipping()
    ls, fs, rs, _h2, _m2 = ENS.stable()
    flip = P.derive(lf, ff, rf)
    stab = P.derive(ls, fs, rs)
    return {"flipping_empty": flip["empty"],
            "stable_nonempty": not stab["empty"],
            "flipping_pairs": flip["n_stable"],
            "stable_pairs": stab["n_stable"],
            "honest": flip["empty"] and not stab["empty"]}


def ordinal_survives_cardinal():
    """The spec's central bet: 'the SEQUENCE in which places wet is far
    more stable' than magnitude. The stable ensemble has a fixed order
    with gaps varying 5x; the pipeline should extract the order and the
    lead BAND (not a point) should be wide."""
    ls, fs, rs, h, _m = ENS.stable()
    lb = P.lead(ls[0], ls[2], fs, rs)   # bridge -> house
    return {"stable_pairs": len(P.stable_pairs(ls, fs, rs)),
            "lead_min": lb["min"], "lead_p90": lb["p90"],
            "band_width": lb["p90"] - lb["min"],
            "band_is_wide": (lb["p90"] - lb["min"]) >= lb["min"]}


def false_alarm_blindness():
    """THE FINDING. Step 3 catches misses and is blind to false alarms.

    A trigger with a perfectly stable order (never wets after the house
    when the house wets) but a high false-alarm rate passes step 3, and
    the spec's card carries a lead band with no reliability line. The
    two error rates are asymmetric in the pipeline:

      miss:        caught by step 3 (the sign flips)   -> kept ~ 0
      false alarm: NOT caught (same sign as a TP)      -> unconstrained
    """
    lms, field, runs, h, mt = ENS.false_alarm_heavy()
    trigger = [lm for lm in lms if lm.id == "upstream_culvert"][0]
    stable = P.stable_pairs(lms, field, runs)
    kept = any(a.id == "upstream_culvert" and b.id == "household"
               for a, b, _u in stable)
    rel = P.reliability(trigger, h, field, runs)
    return {"trigger_kept_by_step3": kept,
            "miss_rate": rel["miss_rate"],
            "false_alarm_rate": rel["false_alarm_rate"],
            "true_positive": rel["true_positive"],
            "false_alarm": rel["false_alarm"],
            "spec_card_shows_it": False,
            "note": "step 3 keeps a trigger that cries wolf in %d of %d "
                    "firings; the spec's card has no line for it"
                    % (rel["false_alarm"],
                       rel["true_positive"] + rel["false_alarm"])}


def strict_tie_handling():
    """Step 3's criterion is strict sign-invariance, so a tie (two
    landmarks wetting in the same step) is a third value and drops a
    pair that is otherwise A-no-later-than-B in every run.

    That is OVER-strict -- it drops a weak ordering that is still a
    usable rule ('when A is wet, B is wet or imminent'). But over-strict
    DROPS rules rather than inventing them, which is the correct
    direction to err for a life-safety product. Demonstrated on a pair
    that ties in one run and is strictly ordered in another."""
    a = P.Landmark("A", 1.0)
    b = P.Landmark("B", 1.0)
    field = {
        "r1": {"A": [0, 5, 5], "B": [0, 0, 5]},   # A(1) < B(2)
        "r2": {"A": [0, 5, 5], "B": [0, 5, 5]},   # A(1) == B(1)  tie
    }
    runs = ["r1", "r2"]
    strict = P.stable_pairs([a, b], field, runs)
    # weak reading: A never strictly after B -> would be kept
    signs, _u = P._ordering(field, a, b, runs)
    weak_ok = all(s <= 0 for s in signs)
    return {"strict_keeps_it": len(strict) > 0,
            "weak_would_keep_it": weak_ok,
            "signs": signs,
            "over_strict": (len(strict) == 0) and weak_ok,
            "direction": "drops a valid rule -- conservative, the safe "
                         "way to fail for a life-safety product"}


def neither_wet_excluded():
    """A run where neither landmark wets carries no ordering
    information. The pipeline excludes it rather than counting it as
    agreement (which would inflate stability) or a flip (which would
    suppress a real rule). Checked: a pair stable on informative runs
    stays stable when uninformative runs are added."""
    a = P.Landmark("A", 1.0)
    b = P.Landmark("B", 1.0)
    field = {
        "r1": {"A": [0, 5, 5], "B": [0, 0, 5]},        # A(1) < B(2)
        "r2": {"A": [0, 5, 5], "B": [0, 0, 5]},        # A(1) < B(2)
        "r3": {"A": [0, 0, 0], "B": [0, 0, 0]},        # neither wets
    }
    runs = ["r1", "r2", "r3"]
    signs, used = P._ordering(field, a, b, runs)
    stable = P.stable_pairs([a, b], field, runs)
    return {"neither_run_excluded": "r3" not in used,
            "informative_runs_used": used,
            "pair_still_stable": len(stable) > 0}


def render():
    out = []
    w = out.append
    w("OBSERVABLE-INDICATOR RULES -- what building the pipeline surfaces")
    w("")
    w("The spec calls the post-processing 'stdlib, phone-buildable' and")
    w("the router 'the only non-phone term'. So the router output is an")
    w("INPUT: pipeline.py consumes a time-resolved depth field and never")
    w("runs a solver. Every field here is SYNTHETIC (ensembles.py),")
    w("constructed so ground truth is known. Nothing is a real")
    w("community; the findings are about the pipeline's logic.")
    w("")

    w("1. THE FALSIFIABLE CONDITION FIRES, BOTH WAYS")
    f = falsifiable_fires()
    w("   flipping ensemble -> empty output: %s" % f["flipping_empty"])
    w("   stable ensemble   -> non-empty:    %s" % f["stable_nonempty"])
    w("   The spec: 'empty output is a valid, honest result'. A pipeline")
    w("   that always emitted a rule would be CONSTANT_FIRES; this one")
    w("   returns nothing when every pair flips, and rules when they do")
    w("   not. %s." % ("honest" if f["honest"] else "NOT honest"))
    w("")

    w("2. THE ORDINAL BET HOLDS -- sequence survives where magnitude does")
    w("   not")
    o = ordinal_survives_cardinal()
    w("   stable pairs found: %d" % o["stable_pairs"])
    w("   bridge -> house lead band: %s to %s steps (width %s)"
      % (o["lead_min"], o["lead_p90"], o["band_width"]))
    w("   The order is invariant while the gap varies %sx across runs, so"
      % (int(round(o["lead_p90"] / max(o["lead_min"], 1)))))
    w("   the band is wide and the point estimate would lie. Reporting")
    w("   the band, and planning against the short end, is the honest")
    w("   product -- and it is what the spec asks for.")
    w("")

    w("3. THE FINDING -- STEP 3 IS BLIND TO FALSE ALARMS")
    fa = false_alarm_blindness()
    w("   A trigger with a perfectly stable order is kept by step 3: %s"
      % fa["trigger_kept_by_step3"])
    w("   its miss rate:        %s   (step 3 forces this ~0)"
      % fa["miss_rate"])
    w("   its false-alarm rate: %s   (step 3 does NOT constrain this)"
      % fa["false_alarm_rate"])
    w("   %d true positives, %d false alarms."
      % (fa["true_positive"], fa["false_alarm"]))
    w("")
    w("   Step 3 drops a pair on any MISS -- a dry trigger when the")
    w("   hazard wets flips the sign. It does NOT drop on a FALSE ALARM")
    w("   -- a dry hazard when the trigger wets reads as trigger-before-")
    w("   hazard, the SAME sign as a true positive. So a trigger that")
    w("   cries wolf half the time passes, and the spec's card carries a")
    w("   clean lead band with no line for it.")
    w("")
    w("   For a rule people ACT on -- evacuate every time it fires -- the")
    w("   false-alarm rate is what decides whether they obey it the")
    w("   tenth time. The pipeline computes the timing (ordering + short-")
    w("   end band) and neither error rate. reliability() adds both; the")
    w("   card here carries a REL line the spec's card does not.")
    w("")

    w("4. THE STABILITY CRITERION IS OVER-STRICT, WHICH IS THE SAFE WAY")
    st = strict_tie_handling()
    w("   a pair that ties in one run and is ordered in another:")
    w("     strict sign-invariance keeps it: %s" % st["strict_keeps_it"])
    w("     the weak order (A never after B) holds: %s"
      % st["weak_would_keep_it"])
    w("   So the spec's criterion DROPS a weak-but-valid ordering. That")
    w("   loses some usable rules -- but it drops rules rather than")
    w("   inventing them, which is the correct direction to fail for a")
    w("   life-safety card. Recorded as a containment, not a fault.")
    w("")

    w("5. RUNS WITH NO WETTING CARRY NO ORDER, AND ARE EXCLUDED")
    nw = neither_wet_excluded()
    w("   neither-wet run excluded from the pair check: %s"
      % nw["neither_run_excluded"])
    w("   pair still stable on the informative runs: %s"
      % nw["pair_still_stable"])
    w("   Counting a no-information run as agreement would inflate")
    w("   stability; as a flip would suppress a real rule. Excluding it")
    w("   is the honest reading, and it is a [CHOICE] the spec leaves")
    w("   open.")
    w("")

    w("6. WHAT THIS FOLDER DOES NOT ESTABLISH")
    w("   No real community has a stable trigger, a false-alarm rate, or")
    w("   a derivable card here -- that takes the router run on real")
    w("   terrain, which is the non-phone term. What is established is")
    w("   that the pipeline extracts stable orderings, returns empty")
    w("   when there are none, plans against the short end, couples the")
    w("   route -- and that as the spec writes it, the card omits")
    w("   the two rates a person acting on it is never shown: how")
    w("   often it fires for nothing, and how often the water comes")
    return "\n".join(out)


if __name__ == "__main__":
    if "--selftest" in sys.argv[1:]:
        sys.stderr.write(
            "audit.py has no checks of its own. The checks that exercise "
            "it and pipeline.py live in selftest_oir.py.\n"
            "    python3 observable-indicator-rules/selftest_oir.py\n")
        sys.exit(2)
    print(render())
