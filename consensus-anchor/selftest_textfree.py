#!/usr/bin/env python3
"""Selftest for textfree.py.

The arms that earned their place are the ones checking the instrument
rather than the result:

  the chance baseline must be measured and must exceed 1/K
  J=0 must sit at chance for both rules -- the isolated control
  hysteresis must carry state, or the gap is zero by construction
  both limbs of every reported verdict must be reachable

CC0. stdlib only. Parses under Python 3.9.
"""

import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import textfree as TF  # noqa: E402


def run():
    ok, bad = [0], []

    def chk(name, cond):
        if cond:
            ok[0] += 1
        else:
            bad.append(name)

    # -- 1. no corpus anywhere
    src = open(os.path.join(HERE, "textfree.py"), encoding="utf-8").read()
    chk("no network, no file reads of data",
        "urllib" not in src and "requests" not in src
        and "open(" not in src.split("def run(")[1].split("def chance")[0])
    chk("only stdlib imports",
        all(ln.split()[1].split(".")[0] in
            ("json", "math", "os", "random", "sys", "selftest_textfree")
            for ln in src.split("\n")
            if ln.startswith("import ") or ln.startswith("    import ")))

    # -- 2. the chance baseline. MEASURED, and above 1/K.
    b = TF.chance_baseline(seeds=200)
    chk("chance is measured, not assumed", b["seeds"] == 200)
    chk("and it exceeds the naive 1/K", b["mean"] > b["naive_1_over_k"])
    chk("by a margin that matters",
        b["mean"] / b["naive_1_over_k"] > 1.10)
    chk("it carries an sd", b["sd"] > 0)
    # a smaller population has a HIGHER chance baseline
    small = TF.chance_baseline(seeds=200, n=30)
    chk("the baseline moves with N, so it is not a constant",
        small["mean"] > b["mean"])

    # -- 3. J=0 is the isolated control and must sit at chance
    thr = b["mean"] + TF.MARGIN * b["sd"]
    for rule in TF.RULES:
        m0 = sum(TF.run(0.0, rule, 5000 + s, eta=0.0)[1]
                 for s in range(6)) / 6.0
        chk("%s at J=0 sits at chance" % rule, m0 < thr)

    # -- 4. the mean-invariance result, both directions
    d = TF.mean_invariance(TF.DIST)
    sm = TF.mean_invariance(TF.SAMPLED)
    chk("DIST conserves the population mean to machine precision",
        d["max_drift"] < 1e-12)
    chk("SAMPLED does not", sm["max_drift"] > 0.1)
    chk("both reach total agreement",
        d["agree_on_a_distribution"] and sm["agree_on_a_distribution"])
    chk("DIST agrees on a near-uniform distribution",
        d["modal_mass_end"] < 0.35)
    chk("SAMPLED agrees on a near-degenerate one",
        sm["modal_mass_end"] > 0.8)
    chk("so agreement and consensus are not the same measurement",
        d["agree_on_a_distribution"] == sm["agree_on_a_distribution"]
        and d["modal_mass_end"] < sm["modal_mass_end"])

    # -- 5. hysteresis must carry state, or the gap is zero by
    #       construction. Checked by breaking it deliberately.
    rows = TF.hysteresis(TF.SAMPLED, eta=0.0, seeds=3, dwell=100)
    chk("the threaded sweep produces a gap",
        max(abs(r["gap"]) for r in rows) > 0.05)
    saved = TF.run

    def _stateless(J, rule, seed, eta=TF.ETA, field=0.0, steps=TF.T,
                   state=None, n=TF.N, k=TF.K):
        return saved(J, rule, seed, eta=eta, field=field, steps=steps,
                     state=None, n=n, k=k)
    try:
        TF.run = _stateless
        flat = TF.hysteresis(TF.SAMPLED, eta=0.0, seeds=3, dwell=100)
        chk("and dropping the carried state collapses it",
            max(abs(r["gap"]) for r in flat)
            < max(abs(r["gap"]) for r in rows) / 2.0)
    finally:
        TF.run = saved

    # -- 6. the sweep-rate control must be able to say either thing
    h = TF.hysteresis_is_bistability(TF.SAMPLED, eta=0.0, seeds=3,
                                     dwells=(50, 200))
    chk("the control returns a gap per dwell",
        len(h["by_dwell"]) == 2)
    chk("it reports whether the gap shrinks", "shrinks" in h)
    chk("and computes no verdict", "verdict" not in h and "why" in h)
    chk("DIST's gap is small and SAMPLED's is not",
        TF.hysteresis_is_bistability(TF.DIST, eta=0.0, seeds=3,
                                     dwells=(50, 200))["by_dwell"][-1]
        ["max_gap"] < 0.05 < h["by_dwell"][-1]["max_gap"])

    # -- 7. J_c moves with eta, which is the [CHOICE 2] result
    jcs = []
    for eta in TF.ETA_GRID:
        sw = TF.sweep(TF.SAMPLED, eta=eta, seeds=4)
        jcs.append(TF.find_jc(sw, b)["J_c"])
    found = [j for j in jcs if j is not None]
    chk("J_c is found at more than one eta", len(found) >= 2)
    chk("and it is not the same value", len(set(found)) > 1)
    chk("it rises with noise", found == sorted(found))

    # -- 8. the limbs are reported apart, never summed
    a = TF.arm(TF.DIST, eta=0.0)
    L = TF.h3_limbs(a)
    chk("three limbs", len([k for k in L if k != "note"]) == 3)
    chk("each is its own boolean",
        all(isinstance(L[k], bool) for k in L if k != "note"))
    chk("and no composite verdict is emitted",
        "verdict" not in L and "h3_false" not in L)
    chk("DIST fires the alignment limb", L["no_alignment_at_any_J"])

    # -- 9. find_jc uses the measured baseline, not 1/K
    body = src.split("def find_jc(")[1].split("\ndef ")[0]
    chk("find_jc reads the measured baseline", 'base["mean"]' in body)
    chk("and never 1/K", "1.0 / k" not in body and "1/k" not in body)
    chk("it returns found=False rather than a number when none exists",
        TF.find_jc([{"J": 0.0, "m": 0.0}], b)["found"] is False)
    chk("and J_c is None there",
        TF.find_jc([{"J": 0.0, "m": 0.0}], b)["J_c"] is None)

    # -- 10. smoothness refuses an empty denominator
    flat_rows = [{"J": 0.0, "m": 0.3}, {"J": 1.0, "m": 0.3}]
    chk("smoothness returns None on no net rise",
        TF.smoothness(flat_rows)["max_step_share"] is None)
    chk("and says why", "denominator" in TF.smoothness(flat_rows)["why"])

    # -- 11. the screen
    sys.path.insert(0, os.path.join(TF.ROOT, "sheet-structure-scan"))
    import no_severity  # noqa: E402
    out = TF.render(TF.full(seeds=3, hyst_seeds=2))
    chk("the report carries no severity language",
        not no_severity.hits(out))
    chk("and the screen is not silent by construction",
        bool(no_severity.hits(out + "\nthis rule is broken\n")))
    chk("the report states topology is not swept",
        "NOT swept" in out)
    # the phrase wraps across a line in the rendered report
    chk("and that this is not evidence about trained models",
        "evidence about trained language models" in " ".join(out.split()))

    print("selftest: %d checks, %d failed" % (ok[0] + len(bad), len(bad)))
    for x in bad:
        print("  FAILED", x)
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(run())
