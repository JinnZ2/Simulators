#!/usr/bin/env python3
# SPDX-License-Identifier: CC0-1.0
"""
corroboration.py - what agreement between two modules is worth.

    python3 corroboration.py [--selftest]

Marker under exploration. Delivered spec: SPEC_ECHO.md.

THE SPEC'S CONSEQUENCE, MADE RUNNABLE. "If YES is frequent, results across
modules are not independent -- they share a generator. Any agreement between
two modules is then weaker evidence than it appears, because agreement may be
inherited rather than found."

That is a statement about pairs, so this module works on pairs. For two
modules it returns a STATE, never a number:

  INHERITED       both YES. Agreement is expected from the shared generator
                  and is not independent evidence of anything.
  MIXED           one YES, one NO. Unquantified: the generator is in one arm.
  INDEPENDENT     both NO, as far as examined.
  UNKNOWN         either is UNEXAMINED.

NO DISCOUNT FACTOR IS RETURNED, BECAUSE THERE IS NO BASE RATE TO BUILD ONE
FROM. echo_register refuses the base rate on a selection effect -- every
examined row is there because someone noticed an echo, and noticing one is
the same act as finding one -- so any numeric weight here would be a rate
laundered through arithmetic. The state is the readout.

UNEXAMINED IS NOT INDEPENDENT, AND THAT IS THE WHOLE MODULE. The register
defaults every module to UNEXAMINED. Fold UNEXAMINED into NO and the pair
table fills with INDEPENDENT, the shared generator vanishes, and corroboration
across the repo reads strong -- from a register in which nothing has been
examined. `misread()` runs exactly that mistake against the live register and
prints both tables side by side, because the inversion is invisible in the
result and obvious in the diff.

A YES IS NOT A DEFECT. The spec is explicit: not a defect claim, not a
discipline failure, a property of a single-builder instrument that cannot be
removed by effort, only counted. An instrument that matches its builder's
manual procedure may be matching it because the procedure is right. What YES
costs is the independence of two readings, not the correctness of either.

stdlib only, parses under Python 3.9. CC0.
"""

import argparse
import itertools
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import echo_register as R                                      # noqa: E402

STATES = ("INHERITED", "MIXED", "INDEPENDENT", "UNKNOWN")

STATE_GLOSS = {
    "INHERITED": "both YES: agreement is expected from the shared generator "
                 "and is not independent evidence",
    "MIXED": "one YES, one NO: the generator is in one arm and the weight "
             "is unquantified",
    "INDEPENDENT": "both NO, as far as examined",
    "UNKNOWN": "at least one is UNEXAMINED. Not independent, not inherited, "
               "and not to be read as either",
}


def pair_state(v1, v2, unexamined_as=None):
    """The state of one pair. `unexamined_as` exists only to be misused."""
    a = unexamined_as if (v1 == "UNEXAMINED" and unexamined_as) else v1
    b = unexamined_as if (v2 == "UNEXAMINED" and unexamined_as) else v2
    if "UNEXAMINED" in (a, b):
        return "UNKNOWN"
    if a == "YES" and b == "YES":
        return "INHERITED"
    if a == "NO" and b == "NO":
        return "INDEPENDENT"
    return "MIXED"


def table(register, unexamined_as=None):
    """Every pair of modules, counted by state."""
    names = sorted(register.rows)
    out = dict((s, 0) for s in STATES)
    for m1, m2 in itertools.combinations(names, 2):
        s = pair_state(register.verdict(m1), register.verdict(m2),
                       unexamined_as=unexamined_as)
        out[s] += 1
    out["n_pairs"] = len(names) * (len(names) - 1) // 2
    return out


def misread(register=None):
    """The register read correctly, and the same register read with
    UNEXAMINED folded into NO.

    Both tables come from identical data. The second is what the repo looks
    like if the default is mistaken for an answer.
    """
    register = register or R.seeded()
    correct = table(register)
    folded = table(register, unexamined_as="NO")
    return {
        "correct": correct,
        "unexamined_read_as_NO": folded,
        "established_independent_correctly": correct["INDEPENDENT"],
        "established_independent_if_misread": folded["INDEPENDENT"],
        "why": "identical data. UNEXAMINED is the default for every module "
               "that nobody has looked at, and reading it as NO converts "
               "'not looked at' into 'looked at and clear'",
    }


def weight():
    """No numeric discount, and the reason it is not a small-n problem."""
    br = R.Register().base_rate()
    return {"discount_factor": None,
            "state": "NOT_DERIVABLE",
            "why": "a numeric weight needs a base rate, and the base rate "
                   "is refused on a selection effect rather than on n. "
                   "Every examined row exists because someone noticed an "
                   "echo, so the numerator and the denominator are the "
                   "same act",
            "base_rate_state": br["state"]}


def confidence():
    return {"pair_states": "four states, no number. A discount factor would "
                           "be the refused base rate laundered through "
                           "arithmetic",
            "UNEXAMINED": "a third state everywhere, never folded into NO. "
                          "Folding it inverts the readout while leaving it "
                          "looking the same",
            "what_YES_costs": "the independence of two readings, not the "
                              "correctness of either. An instrument matching "
                              "its builder's procedure may be matching it "
                              "because the procedure is right",
            "current_table": "every pair is UNKNOWN. One module has a "
                             "verdict and it has no examined partner, so "
                             "nothing here establishes independence or "
                             "inheritance for any pair",
            "resolved": False}


def breaks():
    return [
        "NOTHING IN THIS REPO IS ESTABLISHED INDEPENDENT AND THE TABLE SAYS "
        "SO IN ONE NUMBER: zero pairs. One module carries a verdict, every "
        "other row is UNEXAMINED, so every pair is UNKNOWN. That is not a "
        "finding about the modules -- it is the register reporting that the "
        "work has not been done, and it is the correct output for a register "
        "nobody has filled",
        "READ UNEXAMINED AS NO AND THE SAME DATA SAYS ALMOST EVERYTHING IS "
        "INDEPENDENT. misread() prints both. The failure needs no bad faith "
        "and leaves no trace in the result: a default silently becomes an "
        "answer, and the table looks identical in shape",
        "the pair states are about the REGISTER, not about the modules. Two "
        "modules marked NO are independent only in the sense that the "
        "operator examined both and reported no match to an unaided "
        "procedure, which is one person's introspective report about their "
        "own habits and is not otherwise checkable",
        "SEPARABILITY FROM DOMAIN EXPERTISE IS UNRESOLVED AND THIS MODULE "
        "CANNOT RESOLVE IT. The spec lists it open. An expert's instrument "
        "matching their manual procedure may echo the procedure or may "
        "simply be correct, and from a pair table those are the same row. "
        "YES is logged as a fact about shared structure, never as a fact "
        "about quality",
        "the register is per module and the delivered instances are per "
        "file: three instances collapse into one row, and a module with one "
        "echo and a module with twelve are the same YES. The pair table "
        "inherits that flattening",
    ]


def report():
    L = ["CORROBORATION -- what agreement between two modules is worth",
         "=" * 72, ""]
    L.append("  'If YES is frequent, results across modules are not")
    L.append("  independent -- they share a generator. Any agreement")
    L.append("  between two modules is then weaker evidence than it")
    L.append("  appears, because agreement may be inherited rather")
    L.append("  than found.'")
    L.append("")
    L.append("  FOUR STATES, NO NUMBER")
    L.append("")
    for s in STATES:
        L.append("    %s" % s)
        for line in _wrap(STATE_GLOSS[s], "      "):
            L.append(line)
    L.append("")
    w = weight()
    L.append("    discount factor: %s   %s"
             % (w["discount_factor"], w["state"]))
    for line in _wrap(w["why"], "    "):
        L.append(line)
    L.append("")
    L.append("-" * 72)
    L.append("")
    L.append("  THE SAME REGISTER, READ TWO WAYS")
    L.append("")
    m = misread()
    L.append("    %-22s %-12s %s" % ("", "correct", "UNEXAMINED as NO"))
    for s in STATES:
        L.append("    %-22s %-12d %d"
                 % (s, m["correct"][s], m["unexamined_read_as_NO"][s]))
    L.append("    %-22s %-12d %d"
             % ("pairs", m["correct"]["n_pairs"],
                m["unexamined_read_as_NO"]["n_pairs"]))
    L.append("")
    L.append("    pairs established INDEPENDENT:")
    L.append("      correctly   %d" % m["established_independent_correctly"])
    L.append("      if misread  %d" % m["established_independent_if_misread"])
    L.append("")
    for line in _wrap(m["why"], "    "):
        L.append(line)
    L.append("")
    L.append("    Identical data. Nothing in this repo is established")
    L.append("    independent, and that is the register reporting that the")
    L.append("    work has not been done -- not a finding about modules.")
    L.append("")
    L.append("-" * 72)
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


def selftest():
    f = k = 0

    def ck(label, cond):
        nonlocal f, k
        k += 1
        if not cond:
            f += 1
            print("FAIL %s" % label)

    ck("both YES is INHERITED, not corroboration",
       pair_state("YES", "YES") == "INHERITED")
    ck("both NO is INDEPENDENT as far as examined",
       pair_state("NO", "NO") == "INDEPENDENT")
    ck("one of each is MIXED", pair_state("YES", "NO") == "MIXED")
    ck("UNEXAMINED with YES is UNKNOWN, not INHERITED",
       pair_state("UNEXAMINED", "YES") == "UNKNOWN")
    ck("UNEXAMINED with NO is UNKNOWN, NOT INDEPENDENT -- the whole rule",
       pair_state("UNEXAMINED", "NO") == "UNKNOWN")
    ck("and two UNEXAMINED are UNKNOWN, never independent by default",
       pair_state("UNEXAMINED", "UNEXAMINED") == "UNKNOWN")

    m = misread()
    ck("on the live register every pair is UNKNOWN",
       m["correct"]["UNKNOWN"] == m["correct"]["n_pairs"]
       and m["correct"]["n_pairs"] > 2000)
    ck("so ZERO pairs are established independent",
       m["established_independent_correctly"] == 0)
    ck("folding UNEXAMINED into NO turns most pairs INDEPENDENT",
       m["established_independent_if_misread"] > 2000)
    ck("from identical data -- the pair count does not move",
       m["correct"]["n_pairs"] == m["unexamined_read_as_NO"]["n_pairs"])
    ck("and the inversion is the second break, stated as needing no bad "
       "faith",
       "no bad faith" in breaks()[1])

    w = weight()
    ck("no numeric discount factor is returned",
       w["discount_factor"] is None and w["state"] == "NOT_DERIVABLE")
    ck("and the reason is the refused base rate, not a small sample",
       w["base_rate_state"] == "REFUSED_SELECTION_EFFECT"
       and "same act" in w["why"])

    ck("the zero-established-independent result leads the breaks list",
       "ZERO PAIRS" in breaks()[0].upper())
    ck("what a YES costs is independence, not correctness",
       "not the correctness of either" in confidence()["what_YES_costs"])
    ck("separability from domain expertise is left open, not resolved",
       any("SEPARABILITY" in b for b in breaks()))
    ck("the per-module flattening of per-file instances is disclosed",
       any("three instances collapse into one row" in b for b in breaks()))
    ck("confidence unresolved", confidence()["resolved"] is False)
    ck("report renders both tables",
       "READ TWO WAYS" in report() and "if misread" in report())
    print("%d/%d checks passed" % (k - f, k))
    return 1 if f else 0


def main():
    ap = argparse.ArgumentParser(description="corroboration weight")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    print(report())
    return 0


if __name__ == "__main__":
    sys.exit(main())
