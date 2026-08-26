#!/usr/bin/env python3
"""What archival availability does to L, before any archive is opened.

MARKER.md specifies L = year_literature_adopts - year_excluded_reading_
dateable, and §4 says the excluded reading is oral by default and has to
be found in a dateable artifact. So the second term is set by WHEN SOMEONE
WROTE IT DOWN and whether that artifact survived and was catalogued -- not
by when the population held the reading.

That is a censoring process with a direction, and its direction is
computable without opening a single archive. Three things fall out, and
the third is the useful one.

    1. L is ATTENUATED. The archival delay subtracts from the measured
       lead, so a real lead is under-reported.

    2. F4 is BIASED TOWARD ACCEPTANCE. The control the spec proposes --
       field biologists' unpublished notes, abstracts, correspondence --
       is better archived than trade periodicals and trapper reports.
       Better archived means it surfaces earlier relative to when it was
       held, so the record shows the field holding the reading first even
       when both held it at the same time.

    3. BOTH RUN AGAINST THE HYPOTHESIS. A positive result survives them.
       A null does not distinguish "no lead" from "archives too sparse to
       see one", which is F1 arriving inside F2.

And one bias runs the other way, which the spec does not guard: coding
leniency on ambiguous archival text. §5 pre-registers CASE selection and
nothing pre-registers ARTIFACT CODING.

No parameter here is measured. The archival hazards are stipulated and
the point is the sign and the ordering, not the numbers.

stdlib only. CC0. Parses under Python 3.9.

    python3 archival_bias.py
    python3 archival_bias.py --selftest
"""

import math
import os
import random
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

# [CHOICE] per-year probability that a held reading reaches a dateable,
# surviving, catalogued artifact. Stipulated. The ORDERING is the claim:
# institutional correspondence is better archived than trade periodicals.
P_EXCLUDED = 0.06          # trade press, hearing testimony, field notes
P_FIELD = 0.18             # named-scientist collections, abstracts
TRIALS = 20000


def _first_year(rng, p, cap=200):
    """Years until the reading reaches the record. Geometric."""
    for k in range(cap):
        if rng.random() < p:
            return k
    return cap


# --------------------------------------------------------------------------
# 1. attenuation of L
# --------------------------------------------------------------------------

def attenuation(true_lead, p=P_EXCLUDED, trials=TRIALS, seed=3):
    rng = random.Random(seed)
    obs = [true_lead - _first_year(rng, p) for _ in range(trials)]
    mean = sum(obs) / float(len(obs))
    pos = sum(1 for v in obs if v > 0) / float(len(obs))
    return {"true": true_lead, "observed_mean": mean,
            "recovered": mean / true_lead if true_lead else float("nan"),
            "frac_positive": pos}


# --------------------------------------------------------------------------
# 2. F4 under differential archiving
#
# Both populations hold the reading in the SAME year. Whose appears first
# in the record? If the field's does, F4 is accepted and the exclusion
# reading is rejected -- on a difference in archiving, not in holding.
# --------------------------------------------------------------------------

def f4_bias(gap_years=0, p_ex=P_EXCLUDED, p_fi=P_FIELD, trials=TRIALS,
            seed=11):
    """gap_years: how much EARLIER the excluded population truly held it."""
    rng = random.Random(seed)
    field_first = tie = ex_first = 0
    for _ in range(trials):
        ex = -gap_years + _first_year(rng, p_ex)
        fi = 0 + _first_year(rng, p_fi)
        if fi < ex:
            field_first += 1
        elif fi > ex:
            ex_first += 1
        else:
            tie += 1
    n = float(trials)
    return {"gap": gap_years, "field_first": field_first / n,
            "tie": tie / n, "excluded_first": ex_first / n}


def gap_needed(target=0.5, p_ex=P_EXCLUDED, p_fi=P_FIELD):
    """How big a true lead before the record shows it more often than not."""
    for g in range(0, 80):
        if f4_bias(g, p_ex, p_fi, trials=4000, seed=23)["excluded_first"] \
                >= target:
            return g
    return None


# --------------------------------------------------------------------------
# 3. the one bias that runs toward the hypothesis
#
# Ambiguous archival text coded after the direction of the reversal is
# known. Not simulated with data -- the quantity is the coder's threshold,
# and the point is that §5 pre-registers case selection and nothing
# pre-registers coding.
# --------------------------------------------------------------------------

def coding_leniency(ambiguous_share, lenient_accept, strict_accept):
    """Share of ambiguous artifacts scored as carrying the reading."""
    return {"ambiguous_share": ambiguous_share,
            "lenient": ambiguous_share * lenient_accept,
            "strict": ambiguous_share * strict_accept,
            "spread": ambiguous_share * (lenient_accept - strict_accept)}


# --------------------------------------------------------------------------
# 4. the label
# --------------------------------------------------------------------------

PREV = os.path.join(ROOT, "question-availability", "MARKER.md")

PREV_Q2 = "Posing the question costs the asker standing"
PREV_Q2_MECH = ("the label is applied prior to content, so the content "
                "never reaches evaluation")
NEW_Q2 = "Q2 is: reading held, no channel"
NEW_Q2_MECH = "no instrument was pointed at them"


def _flat(p):
    return " ".join(open(p, errors="replace").read().split())


def label_drift():
    if not os.path.exists(PREV):
        return {"previous_present": False}
    a, b = _flat(PREV), _flat(os.path.join(HERE, "MARKER.md"))
    return {"previous_present": True,
            "prev_q2": " ".join(PREV_Q2.split()) in a,
            "prev_q2_mech": " ".join(PREV_Q2_MECH.split()) in a,
            "new_q2": " ".join(NEW_Q2.split()) in b,
            "new_q2_mech": " ".join(NEW_Q2_MECH.split()) in b}


def artifact_exists(token):
    for dirpath, dirs, _f in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in (".git", "__pycache__")]
        if os.path.basename(dirpath) == token:
            return True
    return os.path.exists(os.path.join(ROOT, token + ".md"))


# --------------------------------------------------------------------------

def report():
    print("ARCHIVAL BIAS IN L -- computed before any archive is opened\n")

    print("1  L is attenuated by the archival delay")
    print("   The excluded reading is dated by when someone WROTE IT DOWN")
    print("   and the artifact survived, not by when it was held.")
    print("   Stipulated archival hazard %.2f/yr (mean delay %.1f y):\n"
          % (P_EXCLUDED, 1.0 / P_EXCLUDED))
    print("   %-12s %-16s %-12s %s" % ("true lead", "observed mean",
                                       "recovered", "P(observed > 0)"))
    print("   " + "-" * 58)
    for t in (5, 10, 20, 30, 50):
        a = attenuation(t)
        print("   %-12d %-16.1f %-12.2f %.2f"
              % (t, a["observed_mean"], a["recovered"], a["frac_positive"]))
    print()
    a10, a20 = attenuation(10), attenuation(20)
    print("   A true 20-year lead measures as %.1f and shows positive in"
          % a20["observed_mean"])
    print("   %.0f%% of cases. A true 10-year lead measures NEGATIVE on"
          % (100 * a20["frac_positive"]))
    print("   average (%.1f) and is positive %.0f%% of the time -- a coin"
          % (a10["observed_mean"], 100 * a10["frac_positive"]))
    print("   flip on a real effect twice the mean archival delay.")
    print("   The bias runs AGAINST the hypothesis, which is the good")
    print("   direction: a positive L survives it. A null does not -- F2")
    print("   and F1 become the same observation, and the spec lists them")
    print("   as different falsifiers.")
    print()

    print("2  F4 is biased toward acceptance by differential archiving")
    print("   The spec's own control is field biologists' notes,")
    print("   abstracts and correspondence -- institutionally archived.")
    print("   Stipulated hazard %.2f/yr against %.2f/yr for trade press.\n"
          % (P_FIELD, P_EXCLUDED))
    print("   %-22s %-14s %-8s %s" % ("true excluded lead", "field appears",
                                      "tie", "excluded appears"))
    print("   " + "-" * 62)
    for g in (0, 5, 10, 20, 40):
        b = f4_bias(g)
        print("   %-22d %-14.2f %-8.2f %.2f"
              % (g, b["field_first"], b["tie"], b["excluded_first"]))
    print()
    need = gap_needed()
    print("   At a TRUE lead of zero -- both held it the same year -- the")
    print("   record shows the field first in %.0f%% of cases. F4 would be"
          % (100 * f4_bias(0)["field_first"]))
    print("   accepted on a difference in archiving, not in holding.")
    print("   The excluded population needs a true lead of about %s years"
          % need)
    print("   before the record shows it first more often than not.")
    print("   Also conservative. Also collapses F4 into F1.")
    print()

    print("3  what this means for reading a result")
    print("   Both principal biases run against the hypothesis, so:")
    print("     L > 0 survives them        -> the finding is strengthened")
    print("     L ~ 0 does not discriminate -> F1, F2 and F4 return the")
    print("                                    same observation")
    print("   The spec lists F1, F2 and F4 as separate falsifiers. Under")
    print("   archival censoring they are not separable on the L")
    print("   distribution alone. Separating them needs the archival")
    print("   hazard ESTIMATED -- which is doable from the same corpus,")
    print("   by dating artifacts against claimed observation dates. §4")
    print("   already says to record both. That field is the control.")
    print()

    print("4  the one bias that runs the other way, and is unguarded")
    c = coding_leniency(0.40, 0.80, 0.25)
    print("   §5 pre-registers CASE selection. Nothing pre-registers")
    print("   ARTIFACT CODING. If %.0f%% of artifacts are ambiguous and a"
          % (100 * c["ambiguous_share"]))
    print("   coder who knows which way the literature moved accepts")
    print("   %.0f%% of them where a blind coder accepts %.0f%%, the"
          % (100 * 0.80, 100 * 0.25))
    print("   difference is %.0f%% of the whole corpus -- entered as"
          % (100 * c["spread"]))
    print("   earlier dates, which inflates L directly.")
    print("   Fix is standard and cheap: code artifacts blind to the")
    print("   direction of the reversal. The spec guards selection and")
    print("   not coding, and coding is where the leniency lives.")
    print()

    print("5  the label")
    d = label_drift()
    for k in sorted(d):
        print("   %-18s %s" % (k, d[k]))
    print()
    print("   question-availability, three drops back:")
    print("     Q2 unaskable -- '%s'" % PREV_Q2)
    print("     '%s'" % PREV_Q2_MECH)
    print("   here:")
    print("     '%s'" % NEW_Q2)
    print("     '%s'" % NEW_Q2_MECH)
    print()
    print("   Two different mechanisms under one label. The first is a")
    print("   channel that exists and penalises entry; the second is no")
    print("   channel at all. This spec's §1 distinguishes itself from")
    print("   'solicited and rejected' and not from the previous Q2,")
    print("   because the previous Q2 has been overwritten.")
    print("   Case 021's sense substitution inside the family's own")
    print("   vocabulary -- fourth instance in this tree after `state`,")
    print("   `parity` and 021's own cases.")
    print()
    print("   It has a consequence. `QA_003` identified the PREVIOUS Q2")
    print("   as `affect routing`, the mechanism uninstrumented recorded")
    print("   as named-in-prose and filed nowhere. That identification")
    print("   does not transfer to this Q2, so whoever files a twelfth")
    print("   mechanism has to say which one -- and if they file this")
    print("   one, `affect routing` is still unfiled.")
    print("   This spec's own title is the better name for what it")
    print("   describes: OBSERVER EXCLUSION, not 'unaskable'.")
    print()

    print("6  cross-links")
    for t in ("question-availability", "uninstrumented", "report-typing",
              "median-case-calibration"):
        print("   %-26s %s" % (t, "yes" if artifact_exists(t) else "NO"))
    print()


def selftest():
    fails = []

    # 1: attenuation must be real, signed, and able to vanish.
    a20 = attenuation(20)
    if a20["recovered"] >= 0.95:
        fails.append("no attenuation at a 20-year lead (%.2f); finding 1 "
                     "must be restated" % a20["recovered"])
    if a20["observed_mean"] >= 20:
        fails.append("observed mean exceeds the true lead; the censoring "
                     "has the wrong sign")
    if attenuation(50)["recovered"] <= attenuation(5)["recovered"]:
        fails.append("attenuation does not ease as the true lead grows; "
                     "the model is not a fixed delay")

    # 2: F4 bias must exist at a true gap of zero and be reversible.
    b0 = f4_bias(0)
    if b0["field_first"] <= b0["excluded_first"]:
        fails.append("no F4 bias at zero true gap (%.2f vs %.2f); finding 2 "
                     "must be restated"
                     % (b0["field_first"], b0["excluded_first"]))
    b40 = f4_bias(40)
    if b40["excluded_first"] <= b0["excluded_first"]:
        fails.append("a large true lead does not show up in the record; "
                     "the model cannot return a positive")
    g = gap_needed()
    if g is None or g == 0:
        fails.append("gap_needed returned %r; the bias is either unbounded "
                     "or absent" % g)

    # 3: the two hazards must differ, or finding 2 is about nothing.
    if not P_FIELD > P_EXCLUDED:
        fails.append("the archival hazards no longer differ; finding 2 "
                     "assumes institutional archiving is better")

    # 4: coding leniency must be signed the other way.
    c = coding_leniency(0.4, 0.8, 0.25)
    if c["spread"] <= 0:
        fails.append("coding leniency does not run toward the hypothesis; "
                     "finding 4 must be restated")

    # 5: both quotations must still match their sources.
    d = label_drift()
    if not d.get("previous_present"):
        fails.append("question-availability/MARKER.md is missing; finding 5 "
                     "rests on it")
    for k in ("prev_q2", "prev_q2_mech", "new_q2", "new_q2_mech"):
        if not d.get(k):
            fails.append("quotation %r no longer matches its source" % k)

    # cross-links must discriminate.
    # `report-typing` landed 2026-08-26 and stopped being the absent
    # half of this pair. Absent sample moved to `merit-anchoring`.
    got = [artifact_exists(t) for t in
           ("question-availability", "merit-anchoring")]
    if all(got) or not any(got):
        fails.append("artifact_exists returns one answer for both tokens")

    for f in fails:
        print("FAIL: " + f)
    print("SELFTEST %s (%d checks failed)"
          % ("PASS" if not fails else "FAIL", len(fails)))
    return 1 if fails else 0


def main(argv):
    if "--selftest" in argv:
        return selftest()
    report()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
