#!/usr/bin/env python3
# selftest_msd.py -- CC0, stdlib only, parses under 3.9
#
# Every check that exercises env.py and arm1.py. Null-tested in both
# directions wherever a classifier or a verdict is involved.
#
# The load-bearing one is the arm's own stated validity condition:
# NOVELTY MUST BE COMPOSITIONAL, NOT PRIMITIVE. A leaked primitive would
# make the arm measure knowledge and report it as derivation, so it is
# asserted rather than intended, and a deliberately leaky split is run
# to prove the check can fail.

import ast
import io
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import env as E  # noqa: E402
import arm1 as A  # noqa: E402

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

    # ---- the arm's validity condition, both directions
    chk("no primitive appears in test that is absent from training",
        E.compositional_only() == [])
    chk("the drop states this as the arm's whole validity",
        "NOVELTY MUST BE COMPOSITIONAL, NOT PRIMITIVE" in doc)
    # the check must be able to fail: a split that withholds a primitive
    save = E.TRAIN_FAMILIES
    try:
        E.TRAIN_FAMILIES = tuple(f for f in save if "thermal" not in f)
        leaked = E.compositional_only()
        chk("a leaky split IS caught (the check is not CONSTANT_SILENT)",
            leaked == ["thermal"])
    finally:
        E.TRAIN_FAMILIES = save
    chk("and the split is restored", E.compositional_only() == [])

    # ---- the environment is exhaustive, not sampled
    chk("configurations are 2^P x G",
        len(E.all_configs()) == (2 ** len(E.PRIMITIVES)) * len(E.GOALS))
    tr, te = E.train_configs(), E.test_configs()
    chk("train and test partition the space",
        len(tr) + len(te) == len(E.all_configs()))
    chk("train and test do not overlap", not (set(tr) & set(te)))
    chk("no random draw anywhere in env.py",
        "random" not in io.open(os.path.join(HERE, "env.py"),
                                encoding="utf-8").read())

    # ---- admissibility, both directions
    chk("a config meeting a move's requirements admits it",
        "brace" in E.admissible((frozenset(("support", "friction")),
                                 "stabilize")))
    chk("a config missing one requirement does not",
        "brace" not in E.admissible((frozenset(("support",)), "stabilize")))
    chk("the goal has to match too",
        "brace" not in E.admissible((frozenset(("support", "friction")),
                                     "lift")))

    # ---- null seeds exist in the space and are not injected
    nulls = [c for c in te if E.is_null(c)]
    chk("null seeds occur in the test set", len(nulls) > 0)
    chk("and non-null configurations also occur",
        len(nulls) < len(te))
    chk("a null seed really has no admissible move",
        all(not E.admissible(c) for c in nulls))

    # ---- the two regressors
    chk("depth 0 is a training configuration by definition",
        all(E.recombination_depth(c) >= 1 for c in te))
    chk("every test config is coverable by the families",
        all(E.recombination_depth(c) is not None for c in te))
    chk("similarity is a Jaccard in [0,1]",
        all(0.0 <= E.similarity(c, tr) <= 1.0 for c in te[:40]))
    col = A.collinearity(te)
    chk("the regressors are correlated on the full test set",
        col["corr"] != A.UNMEASURED and abs(col["corr"]) > 0.5)
    band = A.matched_band(te)
    chk("a matched band exists", 0 < len(band) < len(te))
    chk("similarity is constant within the band",
        len(set(E.similarity(c, tr) for c in band)) == 1)
    chk("and depth is not",
        len(set(E.recombination_depth(c) for c in band)) > 1)

    # ---- solvers: declared architectures, and they differ
    chk("every solver has a declared architecture",
        set(A.ARCHITECTURE) ==
        set((A.RETRIEVAL, A.DERIVATION, A.PLAUSIBLE, A.SILENT)))
    chk("DERIVATION is exact on a config with a move",
        set(A.solve(A.DERIVATION,
                    (frozenset(("support", "friction")), "stabilize")))
        == set(E.admissible((frozenset(("support", "friction")),
                             "stabilize"))))
    chk("DERIVATION returns empty on a null seed",
        A.solve(A.DERIVATION, nulls[0]) == [])
    chk("SILENT returns empty on everything",
        all(A.solve(A.SILENT, c) == [] for c in te[:30]))
    chk("PLAUSIBLE returns something on a null seed too",
        any(A.solve(A.PLAUSIBLE, c) for c in nulls))
    chk("the four solvers are not all the same function",
        len(set(tuple(A.solve(a, te[7])) for a in
                (A.DERIVATION, A.RETRIEVAL, A.PLAUSIBLE, A.SILENT))) > 1)

    # ---- conditions
    chk("four conditions", len(A.CONDITIONS) == 4)
    chk("enumerated hands over the admissible set regardless of solver",
        A.emitted(A.SILENT, te[3], A.ENUMERATED)
        == list(E.admissible(te[3])))
    chk("the deadline truncates",
        all(len(A.emitted(a, c, A.DEADLINE)) <= A.DEADLINE_K
            for a in (A.DERIVATION, A.PLAUSIBLE) for c in te[:30]))
    chk("irreversible keeps at most one",
        all(len(A.emitted(a, c, A.IRREVERSIBLE)) <= 1
            for a in (A.DERIVATION, A.PLAUSIBLE) for c in te[:30]))

    # ---- the null rate is gameable by silence, which is the point
    sil = A.measure(A.SILENT, A.NOT_ENUMERATED, te)
    der = A.measure(A.DERIVATION, A.NOT_ENUMERATED, te)
    chk("SILENT scores a perfect null rate", sil["null_rate"] == 1.0)
    chk("and reaches no admissible move",
        sil["reached_an_admissible_move"] == 0)
    chk("DERIVATION scores the same null rate",
        der["null_rate"] == sil["null_rate"])
    chk("so the null rate alone does not separate them",
        der["null_rate"] == sil["null_rate"])
    chk("and the coverage term does",
        der["coverage_ADDED"] != sil["coverage_ADDED"])
    pla = A.measure(A.PLAUSIBLE, A.NOT_ENUMERATED, te)
    chk("PLAUSIBLE's null rate is not 1.0 (the measure can move)",
        pla["null_rate"] < 1.0)

    # ---- the same shape on admissibility, which is the second finding
    ret = A.measure(A.RETRIEVAL, A.NOT_ENUMERATED, te)
    chk("admissibility fraction does NOT separate the two architectures "
        "the discriminator exists to separate",
        ret["admissibility_fraction"] == der["admissibility_fraction"])
    chk("and coverage does",
        ret["coverage_ADDED"] != der["coverage_ADDED"])
    chk("coverage is marked as an addition, not one of the five",
        "coverage_ADDED" in ret and "coverage" not in doc.split("MEASURES")[1]
        .split("DISCRIMINATOR")[0])

    # ---- UNMEASURED is never a pass
    chk("an empty denominator reads UNMEASURED",
        sil["admissibility_fraction"] == A.UNMEASURED)
    chk("and UNMEASURED is not a number",
        not isinstance(A.UNMEASURED, float))

    # ---- the discriminator: both verdict rules, and the null
    d = A.discriminate(A.RETRIEVAL, A.NOT_ENUMERATED, te)
    chk("the drop's stated rule recovers RETRIEVAL's declared architecture",
        d["verdict_drop_rule"] == "SIMILARITY_CARRIES")
    chk("the coefficient ratio is large",
        abs(d["beta_similarity"]) > 10 * abs(d["beta_depth"]))
    chk("and the null-tested verdict is NEITHER_CARRIES at this n",
        d["verdict"] == "NEITHER_CARRIES")
    chk("because r2 does not clear the permutation null",
        d["r_squared"] <= d["perm_null_q95"])
    dp = A.discriminate(A.PLAUSIBLE, A.NOT_ENUMERATED, te)
    chk("the stated rule names an architecture for a solver with neither",
        dp["verdict_drop_rule"] in ("SIMILARITY_CARRIES", "DEPTH_CARRIES"))
    db = A.discriminate(A.RETRIEVAL, A.NOT_ENUMERATED, band)
    chk("the matched band forces a single-predictor run",
        db["beta_similarity"] == A.UNMEASURED
        and db["beta_depth"] != A.UNMEASURED)
    chk("where the stated rule would return the derivation verdict on a "
        "retrieval solver",
        db["verdict_drop_rule"] == "DEPTH_CARRIES")
    chk("and the null stops it", db["verdict"] == "NEITHER_CARRIES")
    dd = A.discriminate(A.DERIVATION, A.NOT_ENUMERATED, te)
    chk("a solver that never fails gives the discriminator nothing",
        dd["verdict"] == A.UNMEASURED and "constant" in dd["reason"])

    # ---- the permutation null must be able to be cleared
    ols = A._ols()
    n = 200
    ys = [float(i % 2) for i in range(n)]
    strong = [y * 10.0 for y in ys]        # perfectly predictive
    noise = [float((i * 7919) % 13) for i in range(n)]
    b1, r1 = ols(ys, [strong, noise])
    chk("a strong predictor clears the permutation null",
        r1 > A._perm_null(ys, [strong, noise], ols))
    rnd = [float((i * 104729) % 97) for i in range(n)]
    b2, r2 = ols(ys, [rnd, noise])
    chk("and a random one does not",
        r2 <= A._perm_null(ys, [rnd, noise], ols))
    chk("the permutation null is deterministic",
        A._perm_null(ys, [rnd, noise], ols)
        == A._perm_null(ys, [rnd, noise], ols))

    # ---- power is computed from the observed effect, not stipulated
    pw = A.power(A.RETRIEVAL, A.NOT_ENUMERATED, te, ns=(143, 600))
    chk("power rises with n",
        pw["rows"][1][1] >= pw["rows"][0][1])
    chk("power reports the observed n it resampled from",
        pw["observed_n"] == d["n"])

    # ---- the drop's reporting rules
    tree = ast.parse(io.open(os.path.join(HERE, "arm1.py"),
                             encoding="utf-8").read())
    composites = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) \
                and node.func.id in ("sum", "max", "min"):
            src = ast.dump(node)
            if "null_rate" in src or "admissibility" in src \
                    or "coverage" in src:
                composites.append(src)
    chk("no measure is aggregated into a composite", not composites)
    chk("the drop forbids one", "never aggregate the measures" in doc)
    chk("ols is imported, not reimplemented",
        "def ols" not in io.open(os.path.join(HERE, "arm1.py"),
                                 encoding="utf-8").read())

    out = A.render()
    one = " ".join(out.split())
    chk("the report marks the unrun arms UNMEASURED",
        one.count("UNMEASURED") >= 3 and "Arm 4  UNMEASURED" in out)
    chk("and says why Arm 4 is unrun rather than approximating it",
        "refuses CONNECT" in one)
    chk("the report declares what is authored here",
        "authored here" in one)
    chk("the report states nothing is a system under test",
        "Nothing here is a system under test" in one)
    chk("the report prints both verdict rules",
        "drop's stated rule" in one and "null-tested" in one)
    chk("the report gives the power requirement",
        "roughly 600" in one)
    envout = subprocess.run([sys.executable, os.path.join(HERE, "env.py")],
                            stdout=subprocess.PIPE).stdout.decode()
    chk("bare env.py renders the environment",
        all(p2 in envout for p2 in E.PRIMITIVES))
    chk("and names every move",
        all(m in envout for m in E.MOVES))

    # ---- refuses --selftest rather than exiting 0
    for mod in ("arm1.py", "env.py"):
        r = subprocess.run([sys.executable, os.path.join(HERE, mod),
                            "--selftest"],
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        chk("%s refuses --selftest" % mod, r.returncode == 2)
        chk("%s names where its checks live" % mod,
            b"selftest_msd.py" in r.stderr)

    # ---- the no-severity screen
    sys.path.insert(0, os.path.join(os.path.dirname(HERE),
                                    "sheet-structure-scan"))
    import no_severity  # noqa: E402
    chk("the report carries no severity language",
        not no_severity.hits(out))
    chk("and the screen is not silent by construction",
        bool(no_severity.hits(out + "\nthis design is broken\n")))

    print("selftest: %d checks, %d failed" % (ok[0] + len(bad), len(bad)))
    for x in bad:
        print("  FAILED", x)
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(run())
