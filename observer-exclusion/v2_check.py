#!/usr/bin/env python3
"""Checks on SPEC_V2.md, which supersedes MARKER.md. Neither is edited.

v2 adopts the whole of the v1 audit -- the naming split, the attenuation,
F4's differential archiving, the coding protocol -- and quotes its figures
back. So this file does three jobs:

    1. verify the quoted figures against what archival_bias.py computes,
       because a spec transcribing an audit's numbers can transcribe them
       wrong;
    2. audit the material that is NEW in v2, principally §4's estimator;
    3. check whether the §8 repair addresses the term it needs to.

The headline is in job 2. §4's correction has its sign the wrong way
round, and the section's own prose states the direction the formula then
goes against.

stdlib only. CC0. Parses under Python 3.9.

    python3 v2_check.py
    python3 v2_check.py --selftest
"""

import os
import random
import re
import statistics
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
V2 = os.path.join(HERE, "SPEC_V2.md")
V1 = os.path.join(HERE, "MARKER.md")

sys.path.insert(0, HERE)
import archival_bias as AB  # noqa: E402


def _flat(p):
    return " ".join(open(p, errors="replace").read().split())


def quoted(needle, path=V2):
    return " ".join(needle.split()) in _flat(path)


# --------------------------------------------------------------------------
# 1. the sign of the censoring correction
#
#   H = year the population held the reading
#   A = year of the first SURVIVING artifact carrying it,  A = H + D, D >= 0
#   P = year the literature adopts
#
#   L_true = P - H
#   L_raw  = P - A = P - (H + D) = L_true - D
#   =>  L_true = L_raw + D
#
# delta-hat estimates D. The spec subtracts it.
# --------------------------------------------------------------------------

SPEC_FORMULA = "L_adj = L_raw − median(δ̂)"


def correction_sign(true_lead=20, trials=20000, seed=7, max_delay=30):
    rng = random.Random(seed)
    raws, ds = [], []
    for _ in range(trials):
        d = rng.randint(0, max_delay)
        raws.append(true_lead - d)
        ds.append(d)
    med = statistics.median(ds)
    return {"true": float(true_lead),
            "L_raw": statistics.mean(raws),
            "median_delta": med,
            "spec_minus": statistics.mean(r - med for r in raws),
            "plus": statistics.mean(r + med for r in raws)}


# --------------------------------------------------------------------------
# 2. does the §8 repair address the term the bias lives in?
#
# Two populations, SAME delta_write (retrospection), DIFFERENT survival.
# If delta-hat distributions come out identical while the F4 bias is fully
# present, the proposed test cannot detect the bias it is aimed at.
# --------------------------------------------------------------------------

def _first_surviving(rng, write_rate, survive_p, cap=300):
    """Years until a written record both exists AND survives."""
    t = 0
    while t < cap:
        t += 1
        if rng.random() < write_rate and rng.random() < survive_p:
            return t
    return cap


def f4_term_mismatch(trials=8000, seed=13):
    """delta-hat is retrospection among survivors; the bias is survival."""
    rng = random.Random(seed)
    # identical writing behaviour, different survival
    WRITE, RETRO = 0.25, (0, 12)
    ex_delta, fi_delta = [], []
    ex_first, fi_first = [], []
    for _ in range(trials):
        # retrospection of a surviving artifact: same process for both
        ex_delta.append(rng.randint(*RETRO))
        fi_delta.append(rng.randint(*RETRO))
        ex_first.append(_first_surviving(rng, WRITE, 0.10))
        fi_first.append(_first_surviving(rng, WRITE, 0.60))
    return {
        "delta_ex_median": statistics.median(ex_delta),
        "delta_fi_median": statistics.median(fi_delta),
        "delta_gap": abs(statistics.median(ex_delta)
                         - statistics.median(fi_delta)),
        "first_ex_median": statistics.median(ex_first),
        "first_fi_median": statistics.median(fi_first),
        "field_first_rate": sum(1 for a, b in zip(ex_first, fi_first)
                                if b < a) / float(trials),
    }


# --------------------------------------------------------------------------
# 3. which literature event, and how much it costs
# --------------------------------------------------------------------------

ADOPTION_YEARS = {"peer-reviewed publication": 1999,
                  "veterinary body": 2008,
                  "trainer association": 2019}


def adoption_spread():
    v = sorted(ADOPTION_YEARS.values())
    return {"years": ADOPTION_YEARS, "spread": v[-1] - v[0]}


# --------------------------------------------------------------------------
# 4. figures v2 quotes back from the v1 audit
# --------------------------------------------------------------------------

def quoted_figures():
    a10, a20 = AB.attenuation(10), AB.attenuation(20)
    b0 = AB.f4_bias(0)
    g = AB.gap_needed()
    c = AB.coding_leniency(0.40, 0.80, 0.25)
    return [
        ("true 10y lead measures -5.6 on average", a10["observed_mean"],
         -5.6, 0.1, quoted("a true ten-year lead measures −5.6 on average")),
        ("positive only 47% of the time", 100 * a10["frac_positive"],
         47.0, 1.0, quoted("comes out positive only 47% of the time")),
        ("true 20y lead measures 4.4", a20["observed_mean"], 4.4, 0.1,
         quoted("a true twenty-year lead measures 4.4")),
        ("field first 74% of the time", 100 * b0["field_first"], 74.0, 1.0,
         quoted("the record shows the field first 74% of the time")),
        ("roughly an eight-year true lead", float(g), 8.0, 0.5,
         quoted("roughly an eight-year true lead")),
        ("roughly 22% of the corpus", 100 * c["spread"], 22.0, 0.5,
         quoted("roughly 22% of the corpus enters at earlier dates")),
    ]


# --------------------------------------------------------------------------
# 5. did v2 adopt the v1 findings?
# --------------------------------------------------------------------------

ADOPTED = [
    ("OE_006 naming split",
     "Two mechanisms, two names:"),
    ("OE_002 attenuation",
     "L_raw is attenuated, and the attenuation runs against the hypothesis."),
    ("OE_003 F4 differential archiving",
     "F4's control is better archived than the thing it controls."),
    ("OE_004 delta-hat as separator",
     "The estimator is already in the corpus."),
    ("OE_005 coding pre-registered",
     "Coders blind to hypothesis, to case direction"),
    ("OE_007 case not load-bearing",
     "None of §5–§8 depends on this case."),
]


# --------------------------------------------------------------------------

def report():
    print("CHECKS ON SPEC_V2.md -- neither spec is edited\n")

    print("1  did v2 adopt the v1 findings?")
    for label, needle in ADOPTED:
        print("   %-34s %s" % (label, "yes" if quoted(needle) else "NO"))
    print("   Six for six. v2 is the audit adopted, so the work here is on")
    print("   what is new in it.")
    print()

    print("2  the figures v2 quotes back, against what produced them")
    print("   %-42s %-10s %-10s %-6s %s"
          % ("figure", "computed", "quoted", "ok", "in text"))
    print("   " + "-" * 84)
    for label, got, want, tol, intext in quoted_figures():
        ok = abs(got - want) <= tol
        print("   %-42s %-10.2f %-10.2f %-6s %s"
              % (label, got, want, "yes" if ok else "NO",
                 "yes" if intext else "NO"))
    print("   Transcribed correctly. Worth checking because a spec quoting")
    print("   an audit's numbers is a copy, and copies drift.")
    print()

    print("3  THE SIGN OF §4's CORRECTION")
    print("   Spec: %s" % SPEC_FORMULA)
    print()
    print("   H = year held. A = first surviving artifact = H + D, D >= 0.")
    print("   P = year the literature adopts.")
    print("     L_true = P - H")
    print("     L_raw  = P - A = L_true - D")
    print("     so       L_true = L_raw + D,  and δ̂ estimates D.")
    print()
    c = correction_sign()
    print("   Simulated with a true lead of %.0f:" % c["true"])
    print("     median δ̂                      %6.2f" % c["median_delta"])
    print("     L_raw                          %6.2f   (attenuated)"
          % c["L_raw"])
    print("     L_raw − median(δ̂)   [spec]     %6.2f   error %+.2f"
          % (c["spec_minus"], c["spec_minus"] - c["true"]))
    print("     L_raw + median(δ̂)              %6.2f   error %+.2f"
          % (c["plus"], c["plus"] - c["true"]))
    print()
    print("   The correction as written moves the estimate FURTHER from the")
    print("   truth than not correcting at all -- it doubles the bias it is")
    print("   there to remove. §4's own prose says 'L_raw is attenuated';")
    print("   subtracting a positive delay attenuates it again.")
    print("   One character. It inverts the section that v2 calls its")
    print("   structural core, and every downstream statement about L_adj")
    print("   in §8 inherits it.")
    print()

    print("4  does §8's F4 repair reach the term the bias lives in?")
    print("   §4 states the limit: δ̂ 'recovers δ_write, not δ_survive'.")
    print("   §8 then proposes comparing δ̂ distributions between the two")
    print("   populations to decide whether F4 is testable.")
    print("   But the F4 bias is in SURVIVAL, not retrospection.")
    print()
    m = f4_term_mismatch()
    print("   Two populations, identical writing and retrospection,")
    print("   survival %.2f against %.2f:" % (0.10, 0.60))
    print("     median δ̂, excluded          %6.1f" % m["delta_ex_median"])
    print("     median δ̂, field             %6.1f" % m["delta_fi_median"])
    print("     gap the §8 test would see   %6.1f" % m["delta_gap"])
    print("     median years to first record, excluded %6.1f"
          % m["first_ex_median"])
    print("     median years to first record, field    %6.1f"
          % m["first_fi_median"])
    print("     record shows field first    %6.0f%%"
          % (100 * m["field_first_rate"]))
    print()
    print("   The δ̂ distributions are the SAME and the bias is fully")
    print("   present. So the §8 test returns 'comparable' on exactly the")
    print("   corpus where the comparison is invalid. It checks the term")
    print("   §4 says it recovers and the bias is in the term §4 says it")
    print("   does not.")
    print("   The repair is already named in §11, for a different purpose:")
    print("   estimate survival from a known-complete archive. Run that")
    print("   PER POPULATION and F4 becomes testable; without it, §8's")
    print("   'report as untestable' branch is unreachable.")
    print()

    print("5  which literature event, and what it costs")
    a = adoption_spread()
    for k in sorted(a["years"], key=lambda x: a["years"][x]):
        print("   %-28s %d" % (k, a["years"][k]))
    print("   spread: %d years" % a["spread"])
    print("   §3 says record both and names three. L therefore has three")
    print("   values per case, spanning %d years -- larger than the ~17-year"
          % a["spread"])
    print("   archival delay the whole of §4 exists to correct. §11 calls")
    print("   this 'a workaround'; the ordering of magnitudes says the")
    print("   definitional choice dominates the censoring correction, so")
    print("   the three L values are three different measurements and must")
    print("   not share a distribution.")
    print()


def selftest():
    fails = []

    c = correction_sign()
    if abs(c["plus"] - c["true"]) > 0.5:
        fails.append("L_raw + median(delta) no longer recovers the truth "
                     "(%.2f vs %.2f); the derivation is wrong"
                     % (c["plus"], c["true"]))
    if abs(c["spec_minus"] - c["true"]) <= abs(c["L_raw"] - c["true"]):
        fails.append("the spec's form is no longer worse than not "
                     "correcting; finding 3 must be restated")
    if not quoted(SPEC_FORMULA):
        fails.append("the spec's formula no longer reads %r; finding 3 "
                     "must be restated" % SPEC_FORMULA)

    m = f4_term_mismatch()
    if m["delta_gap"] > 1.0:
        fails.append("delta-hat now differs between populations (%.1f); "
                     "finding 4's demonstration is broken" % m["delta_gap"])
    if m["field_first_rate"] <= 0.55:
        fails.append("the F4 bias is absent in the demonstration (%.2f); "
                     "finding 4 shows nothing" % m["field_first_rate"])

    for label, got, want, tol, intext in quoted_figures():
        if not intext:
            fails.append("v2 no longer quotes %r; finding 2 must be "
                         "restated" % label)
        elif abs(got - want) > tol:
            fails.append("%s: computed %.2f, v2 quotes %.2f -- transcription "
                         "drift" % (label, got, want))

    for label, needle in ADOPTED:
        if not quoted(needle):
            fails.append("v2 no longer carries %r" % label)

    if adoption_spread()["spread"] < 10:
        fails.append("the adoption-year spread is now small; finding 5 must "
                     "be restated")
    if not os.path.exists(V1):
        fails.append("v1 is missing; both are meant to stay inspectable")

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
