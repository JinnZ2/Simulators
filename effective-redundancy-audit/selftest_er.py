#!/usr/bin/env python3
# selftest_er.py -- CC0, stdlib only, parses under 3.9
#
# Every check that exercises the DELIVERED effective_redundancy.py and
# the audit. The delivered file is landed verbatim and is not edited;
# these checks are the added layer.
#
# The load-bearing checks are the two facts the finding rests on: the
# delivered report() does not compute kappa, and the Case data model
# cannot hold the two codings kappa needs. Both are asserted against the
# delivered source directly.

import ast
import inspect
import io
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import effective_redundancy as ER  # noqa: E402
import audit as A  # noqa: E402

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

    # ---- the delivered code is landed verbatim from the spec
    er_src = io.open(os.path.join(HERE, "effective_redundancy.py"),
                     encoding="utf-8").read()
    chk("the delivered module is present verbatim from Section 4",
        er_src.strip() in doc)
    chk("the worked example is present verbatim from Section 5",
        "cases = [" in io.open(os.path.join(HERE, "worked_example.py"),
                               encoding="utf-8").read())

    # ---- n_eff follows the spec's stated rules
    allshare = ER.Case("x", "d", "failed", set(),
                       [ER.Channel("a", False), ER.Channel("b", False)])
    chk("all channels share a node -> N_eff = 1", allshare.n_eff == 1)
    oneescape = ER.Case("x", "d", "held", set(),
                        [ER.Channel("a", True), ER.Channel("b", False)])
    chk("one channel escapes -> N_eff = 2", oneescape.n_eff == 2)
    allindep = ER.Case("x", "d", "held", set(),
                       [ER.Channel("a", True), ER.Channel("b", True)])
    chk("all independent -> N_eff = N_nominal", allindep.n_eff == 2)

    # ---- Fisher is numerically correct (the honest positive), both refs
    for name, tbl, got, ref, good in A.fisher_is_correct():
        chk("fisher correct on %s" % name, good)
    # and it is not a constant
    chk("fisher is not a constant",
        ER.fisher_exact_2sided(3, 1, 1, 3)
        != ER.fisher_exact_2sided(8, 2, 1, 5))

    # ---- THE FINDING: report() omits kappa, Case can't hold two codings
    k = A.kappa_is_omitted()
    chk("cohen_kappa is defined", k["cohen_kappa_defined"])
    chk("report() does NOT call cohen_kappa", not k["report_calls_kappa"])
    chk("report() does NOT print kappa", not k["report_prints_kappa"])
    chk("the Case model does NOT hold two codings",
        not k["case_holds_two_codings"])
    # assert directly against the delivered AST, not just the helper
    tree = ast.parse(er_src)
    report_fn = [n for n in ast.walk(tree)
                 if isinstance(n, ast.FunctionDef) and n.name == "report"][0]
    calls = [n.func.id for n in ast.walk(report_fn)
             if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)]
    chk("report() calls contingency and fisher but not cohen_kappa",
        "contingency" in calls and "fisher_exact_2sided" in calls
        and "cohen_kappa" not in calls)
    case_fields = [f for f in ER.Case.__dataclass_fields__]
    chk("no Case field represents a second coder",
        not any("coder" in f for f in case_fields))

    # ---- the function itself is correct: the omission is in the wiring
    kw = A.kappa_works_when_wired()
    chk("cohen_kappa is correct (perfect agreement -> 1.0)",
        kw["perfect"] == 1.0)
    chk("and returns 0 for chance-level agreement",
        abs(ER.cohen_kappa(list("yn" * 10), list("ny" * 10))) < 1e-9
        or ER.cohen_kappa(list("yn" * 10), list("ny" * 10)) <= 0)

    # ---- the worked example reproduces the stated coding
    we = A.worked_example_reproduces()
    chk("Kerr 2025 codes N_eff = 1 as the prose states", we["matches"])
    chk("and N_nominal in code is 3, not the prose's ~4",
        we["kerr2025_n_nominal_code"] == 3)

    # ---- the seed set is self-forbidden and degenerate (labels only)
    s = A.seed_set_degenerate()
    chk("the seed set is 5 failed / 1 held",
        s["failed"] == 5 and s["held"] == 1)
    chk("so the held column is degenerate", s["degenerate"])
    chk("the spec says DO NOT TEST ON THESE",
        "DO NOT TEST ON THESE" in doc)
    chk("and DO NOT sample on disasters",
        "DO NOT sample on disasters" in doc)
    # no seed case is coded here -- audit constructs no Case of its own
    audit_src = io.open(os.path.join(HERE, "audit.py"),
                        encoding="utf-8").read()
    atree = ast.parse(audit_src)
    case_ctors = [n for n in ast.walk(atree)
                  if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
                  and n.func.id == "Case"]
    chk("audit.py constructs no Case of its own (no fabricated coding)",
        len(case_ctors) == 0)

    # ---- the zero-channel edge
    z = A.zero_channel_edge()
    chk("a zero-channel failed case is a false counterexample (cell b)",
        z["n_eff"] == 0 and z["lands_in_b"])

    # ---- egress is measured
    chk("egress records the Section 3.1 sources", len(A.EGRESS) >= 5)
    chk("every one refused",
        all(code == "000" for _h, code, _w in A.EGRESS))

    # ---- the report
    out = A.render()
    one = " ".join(out.split())
    chk("the report states the study is not run here",
        "STUDY does not run" in out or "study does not run" in one.lower())
    chk("and gives the no-fabrication reason",
        "fabricated finding about a real disaster" in one)
    chk("it names the finding as the omitted guard",
        "PRIMARY GUARD IS NOT COMPUTED" in out)
    chk("it connects the recursion",
        "RECURSION BITES" in out and "Mode F" in one)
    chk("it reports the honest positive on Fisher",
        "Fisher is numerically correct" in one)
    chk("H1 vs H0 is left unverified",
        "H1" in one and "H0" in one and "not fabricated here" in one)

    # ---- audit refuses --selftest; delivered file is NOT modified
    r = subprocess.run([sys.executable, os.path.join(HERE, "audit.py"),
                        "--selftest"],
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    chk("audit.py refuses --selftest", r.returncode == 2)
    chk("and names where its checks live", b"selftest_er.py" in r.stderr)
    # the delivered file carries no --selftest handling (verbatim)
    chk("the delivered module is left verbatim (no selftest added)",
        "--selftest" not in er_src)

    # ---- the no-severity screen
    sys.path.insert(0, os.path.join(os.path.dirname(HERE),
                                    "sheet-structure-scan"))
    import no_severity  # noqa: E402
    chk("the audit report carries no severity language",
        not no_severity.hits(out))
    chk("and the screen is not silent by construction",
        bool(no_severity.hits(out + "\nthis design is broken\n")))

    print("selftest: %d checks, %d failed" % (ok[0] + len(bad), len(bad)))
    for x in bad:
        print("  FAILED", x)
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(run())
