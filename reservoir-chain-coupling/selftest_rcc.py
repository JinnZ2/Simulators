#!/usr/bin/env python3
# selftest_rcc.py -- CC0, stdlib only, parses under 3.9
#
# Every check that exercises operator_swap.py and chain.py.
#
# The load-bearing separation is FIRM vs SOFT: the arithmetic results
# (one-sided bias, band width, compounding) are asserted to survive a
# sweep of the synthetic coefficients, so they are properties of the
# operator swap and not of the toy's magnitudes; the null chains are
# asserted to report REFUTED, so the detector is not CONSTANT_FIRES.

import ast
import io
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import operator_swap as OP  # noqa: E402
import chain as CH  # noqa: E402

ok = [0]
bad = []


def chk(name, cond):
    if cond:
        ok[0] += 1
    else:
        bad.append(name)


def run():
    doc = io.open(os.path.join(HERE, "SOURCE_DROP.md"),
                  encoding="utf-8").read()

    # ---- the two operators are the spec's, verbatim
    chk("the independent operator is max",
        OP.combine(OP.INDEPENDENT, 3, 4) == 4)
    chk("the coupled operator is sum",
        OP.combine(OP.COUPLED, 3, 4) == 7)
    chk("both operator names appear in the spec",
        "max( wave" in doc and "wave(n) + pool" in doc)

    # ---- RESULT 1: the bias is one-sided, over a sweep
    one_sided_violation = False
    for crest in range(1, 15):
        for pool in range(0, crest):
            for wave in range(0, 20):
                ib, cb = OP.one_sided(wave, pool, crest)
                if ib and not cb:            # independent-only: forbidden
                    one_sided_violation = True
    chk("independent never breaches where coupled does not (RESULT 1)",
        not one_sided_violation)
    # and the other direction DOES occur, or RESULT 1 is vacuous
    coupled_only_seen = any(
        (not OP.one_sided(w, p, c)[0]) and OP.one_sided(w, p, c)[1]
        for c in range(1, 15) for p in range(0, c) for w in range(0, 20))
    chk("coupled-only DOES occur (RESULT 1 is not vacuous)",
        coupled_only_seen)

    # ---- RESULT 2: the disagreement band width equals the pool
    for crest in (5.0, 10.0, 20.0):
        for pool in (0.5, 2.0, crest - 1):
            b = OP.disagreement_band(pool, crest)
            chk("band width equals pool (crest %g pool %g)" % (crest, pool),
                abs(b["width"] - pool) < 1e-12)
            chk("band is [freeboard, crest)",
                b["lo"] == crest - pool and b["hi"] == crest)
    chk("zero pool gives no band",
        OP.disagreement_band(0.0, 10.0)["width"] == 0.0)

    # ---- RESULT 3: agreement outside the band, both directions
    crest, pool = 10.0, 4.0
    chk("below the freeboard, neither breaches",
        not OP.disagree(3.0, pool, crest))
    chk("at/above the crest, both breach",
        not OP.disagree(10.0, pool, crest))
    chk("inside the band, they disagree",
        OP.disagree(6.0, pool, crest))

    # ---- disagree() and breaches() agree with each other
    chk("disagree is exactly the xor of the two breach verdicts",
        all(OP.disagree(w, 4, 10)
            == (OP.breaches(OP.INDEPENDENT, w, 4, 10)
                != OP.breaches(OP.COUPLED, w, 4, 10))
            for w in range(0, 15)))

    # ---- the chain: the signal case is load-bearing
    c = CH.compare(CH.signal_chain(), 6.0)
    chk("signal chain: coupled breaches extra nodes",
        c["coupled_breaches_extra"] and not c["breach_sets_identical"])
    chk("signal chain: independent breaches no extra (RESULT 1 in chain)",
        c["independent_breaches_extra"] == [])
    chk("signal chain: RUN1 breach set is a subset of RUN2's",
        set(c["run1_independent"]["breach_set"])
        <= set(c["run2_coupled"]["breach_set"]))
    chk("signal verdict is load-bearing", "LOAD-BEARING" in c["verdict"])

    # ---- the nulls: the detector does NOT always fire
    hi = CH.compare(CH.null_high_freeboard(), 6.0)
    chk("high-freeboard null: breach sets identical",
        hi["breach_sets_identical"])
    chk("and the verdict is REFUTED", "REFUTED" in hi["verdict"])
    lo = CH.compare(CH.null_no_freeboard(), 6.0)
    chk("no-freeboard null: breach sets identical",
        lo["breach_sets_identical"])
    chk("and the verdict is REFUTED", "REFUTED" in lo["verdict"])

    # ---- FIRM: the qualitative finding survives a coefficient sweep
    save_r, save_a = CH.RELEASE_GAIN, CH.ATTENUATION
    try:
        signal_holds = True
        nulls_hold = True
        for rg in (1.0, 3.0, 6.0, 10.0):
            for at in (0.3, 0.5, 0.7, 0.9):
                CH.RELEASE_GAIN, CH.ATTENUATION = rg, at
                if CH.compare(CH.signal_chain(), 6.0)["breach_sets_identical"]:
                    signal_holds = False
                if not CH.compare(
                        CH.null_high_freeboard(), 6.0)["breach_sets_identical"]:
                    nulls_hold = False
        chk("signal stays load-bearing across the coefficient sweep (FIRM)",
            signal_holds)
        chk("the high-freeboard null stays refuted across the sweep",
            nulls_hold)
    finally:
        CH.RELEASE_GAIN, CH.ATTENUATION = save_r, save_a

    # ---- RESULT 1 across chains, the harness's own check
    chk("chain.one_sided_holds is True across all fixtures",
        CH.one_sided_holds(
            [CH.signal_chain(), CH.null_high_freeboard(),
             CH.null_no_freeboard()], [2, 4, 6, 8, 10, 14]) is True)

    # ---- route() differs between runs ONLY by the operator
    src = io.open(os.path.join(HERE, "chain.py"), encoding="utf-8").read()
    tree = ast.parse(src)
    route = [n for n in ast.walk(tree)
             if isinstance(n, ast.FunctionDef) and n.name == "route"][0]
    # the only op-dependent call in route is OP.breaches(op, ...)
    op_calls = [n for n in ast.walk(route)
                if isinstance(n, ast.Name) and n.id == "op"]
    chk("op enters route exactly once (as the breach operator)",
        len(op_calls) == 1)
    chk("route's wave update does not branch on the operator",
        "op ==" not in src.split("def route")[1].split("def ")[0])

    # ---- everything is synthetic; no real reservoir is named
    combined = src + io.open(os.path.join(HERE, "operator_swap.py"),
                             encoding="utf-8").read()
    for real in ("Bonneville", "Grand Coulee", "Mica", "Columbia",
                 "Snake", "McNary"):
        chk("no real structure named in the modules: %s" % real,
            real not in combined)
    chk("the synthetic coefficients are marked SYNTHETIC",
        "[SYNTHETIC]" in src)

    # ---- the reports
    o1, o2 = OP.render(), CH.render()
    one = " ".join((o1 + " " + o2).split())
    chk("operator_swap states the bias is one-sided",
        "ONE-SIDED" in o1)
    chk("chain declares route an abstract combiner, not hydraulics",
        "abstract combiner" in one and "not a hydraulic" in one.lower())
    chk("chain states what it is NOT",
        "IS NOT" in o2 and "any real chain" in one)
    chk("chain points at the HEC-RAS run as the real test",
        "HEC-RAS" in one and "columbia-chain-cascade" in one)
    chk("the report marks synthetic coefficients",
        "SYNTHETIC" in o2)

    # ---- both modules refuse --selftest
    for mod in ("operator_swap.py", "chain.py"):
        r = subprocess.run([sys.executable, os.path.join(HERE, mod),
                            "--selftest"],
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        chk("%s refuses --selftest" % mod, r.returncode == 2)
        chk("%s names where its checks live" % mod,
            b"selftest_rcc.py" in r.stderr)

    # ---- the no-severity screen
    sys.path.insert(0, os.path.join(os.path.dirname(HERE),
                                    "sheet-structure-scan"))
    import no_severity  # noqa: E402
    for label, text in (("operator_swap", o1), ("chain", o2)):
        chk("%s report carries no severity language" % label,
            not no_severity.hits(text))
    chk("the screen is not silent by construction",
        bool(no_severity.hits(o2 + "\nthis design is broken\n")))

    print("selftest: %d checks, %d failed" % (ok[0] + len(bad), len(bad)))
    for x in bad:
        print("  FAILED", x)
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(run())
