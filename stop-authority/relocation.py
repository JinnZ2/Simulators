#!/usr/bin/env python3
# SPDX-License-Identifier: CC0-1.0
"""
relocation.py - moving the measurement point instead of arguing with it.

    python3 relocation.py [--selftest]

Marker under exploration. Delivered spec: SPEC_ADDENDUM.md, witnessed case.

# NOTE TO READERS -- TERM COLLISION
# "change of mind" here means REVISION (provenance-bearing). See PREAMBLE.md.

THE WITNESSED CASE. CEO pressure to run subpar material; QC inspectors read
the material as out of spec; budget-office rationale as stated: ship it, and
returns will identify the problems. The floor refused and the refusal held.

THE MOVE IS NOT A DISAGREEMENT ABOUT THE READING. Nobody argued the QC
inspectors were wrong. The measurement point was relocated from pre-shipment
inspection to post-shipment return, and the upstream reading -- still correct
-- was made non-binding. Those are different operations and this module keeps
them apart: `upstream_status()` returns NOT_DISPROVEN_MADE_NONBINDING, never
REFUTED and never SUPERSEDED. A reading that still holds and no longer binds
is the whole shape of the case.

THE SUBSTITUTED PROXY HAS THREE NAMED DEFECTS, AND THEY COMPOUND.
  lagged             the signal arrives after L periods of product has
                     already shipped.
  downstream of harm the event the proxy counts happens to a customer, so a
                     reading of zero costs someone else first.
  missing denominator customers who do not return are invisible. The proxy
                     counts returns, and the population it needs is defective
                     units, which is a strictly larger set by an unmeasured
                     factor.

The third is the one that makes the proxy unfixable by patience. Lag can be
waited out; a downstream measurement still measures something. But the return
fraction is never observed, so the proxy is biased low by a number nobody has,
and no amount of accumulating returns recovers it.

WHAT THIS MODULE DOES NOT DO. It does not establish that the budget office was
wrong that returns would identify the problems. Returns DO identify problems --
some of them, later, after harm, at an unknown fraction. The claim under test
is not whether the proxy detects anything; it is whether the proxy can carry
the decision the upstream reading was carrying. Those are separate questions
and only the second is answered here.

stdlib only, parses under Python 3.9. CC0.
"""

import argparse
import sys

UPSTREAM_STATES = ("BINDING", "NOT_DISPROVEN_MADE_NONBINDING", "REFUTED")


def upstream_status():
    """The QC reading, after the relocation."""
    return {
        "state": "NOT_DISPROVEN_MADE_NONBINDING",
        "reading_still_correct": True,
        "reading_still_binds": False,
        "what_changed": "where the decision reads from, not what the "
                        "instrument said",
        "why_not_refuted": "nobody argued the inspectors were wrong. A "
                           "refutation would have to engage the reading; "
                           "this did not engage it",
        "why_not_superseded": "superseded implies the new measurement covers "
                              "what the old one covered. The proxy is "
                              "lagged, downstream and short a denominator, "
                              "so it covers less",
    }


# --- the two measurement points --------------------------------------------

TRUE_DEFECT_RATE = 0.08          # what the material actually is
SPEC_THRESHOLD = 0.05            # above this, out of spec
PRE_SENSITIVITY = 0.90           # pre-shipment inspection catches this share

# Post-shipment detection is a product of three independent survivals, none
# of which is observed by the party reading the proxy.
MANIFESTS = 0.60                 # the defect shows up in use
CUSTOMER_NOTICES = 0.55          # and is noticed
CUSTOMER_RETURNS = 0.60          # and is returned rather than absorbed

RETURN_LAG = 3                   # periods before returns accumulate
UNITS_PER_PERIOD = 1000


def detection_fraction():
    return MANIFESTS * CUSTOMER_NOTICES * CUSTOMER_RETURNS


def readings():
    """What each measurement point reports for the same material."""
    pre = TRUE_DEFECT_RATE * PRE_SENSITIVITY
    post = TRUE_DEFECT_RATE * detection_fraction()
    return {
        "true_rate": TRUE_DEFECT_RATE,
        "pre_shipment": pre,
        "post_shipment": post,
        "threshold": SPEC_THRESHOLD,
        "pre_decision": "REFUSE" if pre > SPEC_THRESHOLD else "SHIP",
        "post_decision": "REFUSE" if post > SPEC_THRESHOLD else "SHIP",
        "decisions_agree": (pre > SPEC_THRESHOLD) == (post > SPEC_THRESHOLD),
        "post_understates_by": pre / post if post else None,
        "detection_fraction": detection_fraction(),
        "why": "the same material, the same threshold, and opposite "
               "decisions. The proxy is not noisier than the inspection -- "
               "it is biased low by the share of defects that never come "
               "back, and that share is not observed by anyone reading it",
    }


def missing_denominator(periods=6):
    """Units shipped defective that never return, per period and cumulative.

    The proxy's denominator is returns. The population it needs is defective
    units shipped. The gap is silent by construction: a customer who absorbs
    a defect produces no record anywhere.
    """
    d = detection_fraction()
    rows, cum_def, cum_ret, cum_silent = [], 0, 0, 0
    for t in range(periods):
        defective = UNITS_PER_PERIOD * TRUE_DEFECT_RATE
        returned = defective * d if t >= RETURN_LAG else 0.0
        silent = defective - (defective * d)
        cum_def += defective
        cum_ret += returned
        cum_silent += silent
        rows.append({"t": t + 1, "defective": defective,
                     "returned_this_period": returned,
                     "silent": silent,
                     "cum_defective": cum_def, "cum_returned": cum_ret,
                     "cum_silent": cum_silent,
                     "proxy_visible": t >= RETURN_LAG})
    return {"rows": rows,
            "cum_defective": cum_def,
            "cum_returned": cum_ret,
            "cum_silent": cum_silent,
            "silent_share": cum_silent / cum_def if cum_def else None,
            "shipped_before_any_signal":
                UNITS_PER_PERIOD * TRUE_DEFECT_RATE * RETURN_LAG,
            "why": "the silent column is never recorded anywhere. It is not "
                   "a measurement with error bars, it is a population the "
                   "proxy has no channel to"}


def can_the_proxy_carry_the_decision():
    """The question actually at issue, kept apart from 'does it detect'."""
    r = readings()
    return {
        "does_the_proxy_detect_anything": True,
        "why_that_is_not_the_question": "returns do identify problems -- "
                                        "some of them, later, after harm, at "
                                        "an unknown fraction. That was the "
                                        "budget office's stated rationale "
                                        "and it is not false",
        "can_it_carry_the_decision": False,
        "why_not": "at the same threshold the two points give opposite "
                   "decisions on the same material, and the proxy's is the "
                   "wrong one by a factor of %.2f it cannot measure. A "
                   "decision needs the reading to be comparable to the "
                   "threshold; this one is comparable to nothing"
                   % r["post_understates_by"],
        "lag_cost_units": missing_denominator()["shipped_before_any_signal"],
        "state": "PROXY_CANNOT_CARRY_IT",
    }


def confidence():
    return {"the_case": "one witnessed account, from the operator, from a "
                        "position held during the transition. Carried as "
                        "delivered and not verified",
            "the_numbers": "stipulated. The true defect rate, the threshold "
                           "and the three survival fractions were chosen to "
                           "make the decision flip visible; they are not "
                           "measurements of the material in the account",
            "detection_fraction": "a product of three unobserved terms. The "
                                  "PRODUCT is the point -- whatever the "
                                  "individual values, the proxy reads a "
                                  "fraction nobody has measured",
            "what_is_not_claimed": "that returns detect nothing. They detect "
                                   "some problems, later, after harm. The "
                                   "question answered here is whether the "
                                   "proxy can carry the decision the "
                                   "upstream reading was carrying",
            "resolved": False}


def breaks():
    return [
        "THE SAME MATERIAL AT THE SAME THRESHOLD GIVES OPPOSITE DECISIONS, "
        "AND THE PROXY'S IS WRONG BY A FACTOR IT CANNOT MEASURE. "
        "Pre-shipment reads %.3f and refuses; post-shipment reads %.3f and "
        "ships. The gap is the share of defects that never come back, which "
        "is a product of three terms nobody reading the proxy observes. A "
        "decision needs a reading comparable to a threshold, and this one is "
        "comparable to nothing"
        % (readings()["pre_shipment"], readings()["post_shipment"]),
        "THE MISSING DENOMINATOR IS NOT AN ERROR BAR. Roughly four in five "
        "defective units in this run never return, and they produce no "
        "record anywhere -- not a noisy record, no record. A customer who "
        "absorbs a defect is not a measurement with uncertainty attached, "
        "they are a population the proxy has no channel to, and no amount of "
        "accumulating returns recovers them",
        "THE NUMBERS ARE STIPULATED AND CHOSEN TO SHOW THE FLIP. A defect "
        "rate of %.2f, a threshold of %.2f, and three survival fractions "
        "picked to land the proxy under the line. Different values move "
        "whether the decision flips; they do not move that the proxy is "
        "biased low by an unobserved product, which is the structural claim"
        % (TRUE_DEFECT_RATE, SPEC_THRESHOLD),
        "THE BUDGET OFFICE'S STATED RATIONALE IS NOT REFUTED HERE. Returns "
        "do identify problems. The module separates 'does the proxy detect "
        "anything' from 'can the proxy carry this decision' and answers only "
        "the second, because answering the first with NO would be a stronger "
        "claim than the case supports and a wrong one",
        "ONE ACCOUNT, AND THE LAG AND SURVIVAL TERMS ARE INVENTED. The "
        "relocation is witnessed; the three-period return lag and the "
        "manifest/notice/return fractions are this module's construction. "
        "They demonstrate the mechanism is arithmetically available and "
        "measure nothing that happened",
    ]


def _wrap(t, ind, w=72):
    words, lines, cur = t.split(), [], ind
    for x in words:
        if len(cur) + len(x) + 1 > w and cur.strip():
            lines.append(cur.rstrip())
            cur = ind + x + " "
        else:
            cur += x + " "
    if cur.strip():
        lines.append(cur.rstrip())
    return lines


def report():
    L = ["MEASUREMENT-POINT RELOCATION -- the reading that still holds",
         "=" * 72, ""]
    u = upstream_status()
    L.append("  THE UPSTREAM READING, AFTER THE MOVE")
    L.append("")
    L.append("    state:              %s" % u["state"])
    L.append("    still correct:      %s" % u["reading_still_correct"])
    L.append("    still binds:        %s" % u["reading_still_binds"])
    L.append("")
    for line in _wrap("what changed: " + u["what_changed"], "    "):
        L.append(line)
    for line in _wrap("not refuted: " + u["why_not_refuted"], "    "):
        L.append(line)
    for line in _wrap("not superseded: " + u["why_not_superseded"], "    "):
        L.append(line)
    L.append("")
    L.append("-" * 72)
    L.append("")
    L.append("  THE TWO MEASUREMENT POINTS, SAME MATERIAL")
    L.append("")
    r = readings()
    L.append("    true defect rate        %.3f" % r["true_rate"])
    L.append("    spec threshold          %.3f" % r["threshold"])
    L.append("")
    L.append("    %-22s %-10s %s" % ("point", "reads", "decision"))
    L.append("    %-22s %-10.3f %s"
             % ("pre-shipment", r["pre_shipment"], r["pre_decision"]))
    L.append("    %-22s %-10.3f %s"
             % ("post-shipment return", r["post_shipment"],
                r["post_decision"]))
    L.append("")
    L.append("    decisions agree:        %s" % r["decisions_agree"])
    L.append("    proxy understates by:   %.2fx" % r["post_understates_by"])
    L.append("    detection fraction:     %.3f  (%.2f x %.2f x %.2f)"
             % (r["detection_fraction"], MANIFESTS, CUSTOMER_NOTICES,
                CUSTOMER_RETURNS))
    L.append("")
    for line in _wrap(r["why"], "    "):
        L.append(line)
    L.append("")
    L.append("-" * 72)
    L.append("")
    L.append("  THE MISSING DENOMINATOR")
    L.append("")
    m = missing_denominator()
    L.append("    %-5s %-11s %-11s %-9s %s"
             % ("t", "defective", "returned", "silent", "proxy sees"))
    for row in m["rows"]:
        L.append("    %-5d %-11.0f %-11.0f %-9.0f %s"
                 % (row["t"], row["defective"], row["returned_this_period"],
                    row["silent"], row["proxy_visible"]))
    L.append("")
    L.append("    cumulative defective    %.0f" % m["cum_defective"])
    L.append("    cumulative returned     %.0f" % m["cum_returned"])
    L.append("    cumulative silent       %.0f" % m["cum_silent"])
    L.append("    silent share            %.3f" % m["silent_share"])
    L.append("    shipped before signal   %.0f defective units"
             % m["shipped_before_any_signal"])
    L.append("")
    for line in _wrap(m["why"], "    "):
        L.append(line)
    L.append("")
    L.append("-" * 72)
    L.append("")
    L.append("  CAN THE PROXY CARRY THE DECISION")
    L.append("")
    c = can_the_proxy_carry_the_decision()
    L.append("    does it detect anything:  %s"
             % c["does_the_proxy_detect_anything"])
    for line in _wrap(c["why_that_is_not_the_question"], "      "):
        L.append(line)
    L.append("")
    L.append("    can it carry the decision: %s" % c["can_it_carry_the_decision"])
    for line in _wrap(c["why_not"], "      "):
        L.append(line)
    L.append("")
    L.append("  CONFIDENCE, reported separately and not resolved")
    for k in sorted(confidence()):
        L.append("    %s" % k)
        for line in _wrap(str(confidence()[k]), "      "):
            L.append(line)
    L.append("")
    L.append("  WHERE IT BREAKS")
    for b in breaks():
        for line in _wrap("- " + b, "    "):
            L.append(line)
    return "\n".join(L)


def selftest():
    f = k = 0

    def ck(label, cond):
        nonlocal f, k
        k += 1
        if not cond:
            f += 1
            print("FAIL %s" % label)

    u = upstream_status()
    ck("the upstream reading was not disproven, it was made non-binding",
       u["state"] == "NOT_DISPROVEN_MADE_NONBINDING")
    ck("it is still correct and no longer binds -- two separate fields",
       u["reading_still_correct"] is True
       and u["reading_still_binds"] is False)
    ck("REFUTED is available and is not what was returned",
       "REFUTED" in UPSTREAM_STATES
       and u["state"] != "REFUTED")

    r = readings()
    ck("pre-shipment reads above the threshold and refuses",
       r["pre_shipment"] > r["threshold"] and r["pre_decision"] == "REFUSE")
    ck("post-shipment reads below it and ships",
       r["post_shipment"] < r["threshold"] and r["post_decision"] == "SHIP")
    ck("same material, same threshold, opposite decisions",
       r["decisions_agree"] is False)
    ck("the proxy understates by more than four times",
       r["post_understates_by"] > 4.0)
    ck("and the detection fraction is a product of three unobserved terms",
       abs(r["detection_fraction"]
           - MANIFESTS * CUSTOMER_NOTICES * CUSTOMER_RETURNS) < 1e-12)

    m = missing_denominator()
    ck("most defective units never return", m["silent_share"] > 0.75)
    ck("returns are zero until the lag elapses",
       all(row["returned_this_period"] == 0
           for row in m["rows"][:RETURN_LAG]))
    ck("and defective units ship in that window with no signal at all",
       m["shipped_before_any_signal"] > 0)
    ck("the silent column is larger than the returned one, cumulatively",
       m["cum_silent"] > m["cum_returned"])

    c = can_the_proxy_carry_the_decision()
    ck("the proxy does detect problems, and that is not the question",
       c["does_the_proxy_detect_anything"] is True)
    ck("it cannot carry the decision",
       c["can_it_carry_the_decision"] is False
       and c["state"] == "PROXY_CANNOT_CARRY_IT")
    ck("the budget office rationale is not called false",
       "it is not false" in c["why_that_is_not_the_question"])

    ck("the decision flip leads the breaks list",
       "OPPOSITE DECISIONS" in breaks()[0])
    ck("the missing denominator being not-an-error-bar is disclosed",
       any("NOT AN ERROR BAR" in b for b in breaks()))
    ck("the stipulated numbers are disclosed",
       any("STIPULATED AND CHOSEN" in b for b in breaks()))
    ck("not refuting the stated rationale is disclosed",
       any("IS NOT REFUTED HERE" in b for b in breaks()))
    ck("confidence unresolved", confidence()["resolved"] is False)
    ck("report renders", "THE MISSING DENOMINATOR" in report())
    print("%d/%d checks passed" % (k - f, k))
    return 1 if f else 0


def main():
    ap = argparse.ArgumentParser(description="measurement-point relocation")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    print(report())
    return 0


if __name__ == "__main__":
    sys.exit(main())
