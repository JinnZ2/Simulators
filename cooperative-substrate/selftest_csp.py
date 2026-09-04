#!/usr/bin/env python3
"""Checks for the four cooperative-substrate checks and the order audit.
Known answers first, both directions. Writes samples/.

    python3 cooperative-substrate/selftest_csp.py
"""

import ast
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "sheet-structure-scan"))
import p1_deps_extract as P1  # noqa: E402
import p2_substrate_audit as P2  # noqa: E402
import p3_comprehension as P3  # noqa: E402
import p4_goal_coherence as P4  # noqa: E402
import order_audit as A  # noqa: E402
import no_severity  # noqa: E402

FAILS = []
N = [0]


def check(name, cond):
    N[0] += 1
    if not cond:
        FAILS.append(name)
        print("  FAIL  " + name)


def run(args):
    return subprocess.run([sys.executable] + args, capture_output=True, text=True, cwd=HERE)


def main():
    print("selftest_csp")
    # ---- constraints, from the files
    c = A.constraints()
    check("five shipped files under 300 lines", all(v["under_300"] for v in c.values()))
    check("no non-stdlib import in any shipped file", all(not v["non_stdlib"] for v in c.values()))
    check("no network module imported by any shipped file", all(not v["network_modules"] for v in c.values()))
    check("every shipped file parses under 3.9", all(v["parses_3_9"] for v in c.values()))
    for f in A.SHIPPED + ["order_audit.py"]:
        check("%s refuses --selftest with rc 2" % f, run([f, "--selftest"]).returncode == 2)

    # ---- P1 known answers
    fx = A.p1_fixture()
    check("fixture a: 7 records across six classes, 1 argued", fx["a_records"] == 7 and len(fx["a_by_class"]) == 6 and fx["a_argued"] == 1)
    check("fixture b: zero records (the extractor has a reachable zero)", fx["b_records"] == 0)
    check("ratio is None when nothing is argued, 7.0 when one is", fx["ratio_b_only"] is None and fx["ratio_all"] == 7.0)
    recs = P1.extract("Values were verified. Samples were obtained from a supplier.", "x", "x")
    check("verification in a different sentence does not verify", recs and not recs[0]["verified_in_argument"])
    recs = P1.extract("Samples were obtained from a supplier and were verified by assay.", "x", "x")
    check("verification in the same sentence verifies", recs and recs[0]["verified_in_argument"])
    recs = P1.extract("Peak areas were computed following the procedure of Smith and Jones, twice.", "x", "x")
    check("one span one class emits once, and keeps the author list", len(recs) == 1 and recs[0]["dependency"] == "the procedure of Smith and Jones")
    check("source_span points at the dependency text",
          all(r["dependency"] == " ".join("Peak areas were computed following the procedure of Smith and Jones, twice."[r["source_span"][0]:r["source_span"][1]].split()) for r in recs))
    it = A.p1_in_tree()
    check("in-tree documents produce records with nothing argued", it["records"] > 0 and it["argued"] == 0 and it["ratio"] is None)

    # ---- P2 known answers
    px = A.p2_proxy_limits()
    check("a call inside try/except reads verified (the proxy's upper bound)", px["try_only"]["verified"] == 1)
    check("a bound result tested by the next statement reads verified", px["checked"]["verified"] == 1)
    check("a bare call reads unverified", px["bare"]["verified"] == 0)
    check("ast sees no call in a comprehension; bytecode count is reported beside it",
          px["comprehension"]["sites"] == 0 and px["comprehension"]["bytecode_calls"] >= 0)
    tree = ast.parse("import math\nx = math.sqrt(2.0)\ny = json.loads(s)\nz = list()\nw = f()\n")
    recs, sites = P2.call_records(tree)
    layers = sorted(r["layer"] for r in recs)
    check("layers: numeric, transport, allocation and function_call each assigned once beside four function_call records",
          sites == 4 and layers == ["allocation", "function_call", "function_call", "function_call", "function_call", "numeric", "transport"])
    check("compile records carry one row per code object with instruction counts",
          all("instructions" in r for r in P2.compile_records("def f():\n    return 1\n", "<t>")) and len(P2.compile_records("def f():\n    return 1\n", "<t>")) == 2)
    sh = A.p2_shipped()
    check("0 of 4 shipped checks verify every contract", all(r["unverified"] > 0 for r in sh.values()))
    check("ratio exceeds 1 wherever layers stack", all(r["ratio"] > 1 for r in sh.values()))
    empty = P2.call_records(ast.parse("x = 1\n"))
    check("no call sites: ratio undefined not zero", empty[1] == 0)
    try:
        P2.resolve("no_such_module_zz")
        check("unresolvable target raises", False)
    except SystemExit:
        check("unresolvable target raises", True)

    # ---- P3 known answers
    check("cosine of identical profiles is 1, of disjoint is 0, of empty is None",
          abs(P3.cosine({"a": 1, "b": 2}, {"a": 1, "b": 2}) - 1) < 1e-12 and P3.cosine({"a": 1}, {"b": 1}) == 0.0 and P3.cosine({}, {"a": 1}) is None)
    prof, n = P3.profile("x mass y the mass z".split(), "mass", 1)
    check("profile drops stop words and the term itself", n == 2 and dict(prof) == {"x": 1, "y": 1, "z": 1})
    prof, _ = P3.profile("mass alpha beta".split(), "alpha", 3, exclude=("mass",))
    check("exclude keeps the original term out of a stand-in profile", "mass" not in prof and "beta" in prof)
    cc = A.p3_constructed()
    check("same-sense constructed corpus: observed 1.0 above its null", cc["same_sense"]["observed"] > 0.99 and cc["same_sense"]["gap_sd"] > 3)
    check("disjoint-sense constructed corpus: observed 0, null 0, gap undefined",
          cc["disjoint_sense"]["observed"] == 0.0 and cc["disjoint_sense"]["null_mean"] == 0.0 and cc["disjoint_sense"]["gap_sd"] is None)
    check("mean_pairwise is None below two profiles", P3.mean_pairwise({"a": {"x": 1}}) == (None, 0))
    sm = A.p3_sample()
    check("per term on the sample: mechanism and confidence clear the null by > 5 sd, instrument and claim by < 2",
          sm["mechanism"]["gap_sd"] > 5 and sm["confidence"]["gap_sd"] > 5 and abs(sm["instrument"]["gap_sd"]) < 2 and abs(sm["claim"]["gap_sd"]) < 2)
    r = P3.run(os.path.join(HERE, "..", "uninstrumented", "cases"), "mass", null="shuffle", reps=5)
    check("a term below min_count everywhere: undefined observed, null with 0 reps, not zero",
          r["consistency_observed"] is None and r["null"]["reps"] == 0 and r["null"]["mean"] is None)
    check("the third-row statement is on every render", A.P3.UNCONSTRUCTABLE in P3.render(r))

    # ---- P4 known answers
    k4 = A.p4_known(trials=400)
    check("p=0: every trial answers in exactly N steps", k4["p0_steps"] == 50.0 and k4["p0_rate"] == 1.0)
    check("p=1: no answer for N > 1", k4["p1_rate"] == 0.0)
    check("simulation within 3 binomial se of the exact rate on every row", k4["worst_sim_vs_exact_in_se"] < 3.0)
    check("exact termination is non-increasing in p", k4["monotone_nonincreasing"])
    check("unbounded expectation at p = 0.5 is N^2", abs(k4["unbounded_at_0_5"] - 2500) < 1e-6)
    check("expectation grows by > 1000x between 0.55 and 0.60 at N = 50", k4["growth_0_55_to_0_60"] > 1000)
    ex = P4.exact(3, 0.0, 10)
    check("exact at p=0, N=3: rate 1 at step 3", abs(ex["termination_rate"] - 1) < 1e-12 and abs(ex["mean_steps_to_answer"] - 3) < 1e-12)
    check("exact at N=1 is immediate at any p", P4.exact(1, 0.9, 5)["termination_rate"] == 1.0)
    # by hand: E_1 = 1 + p*E_0, E_0 = 1 + E_1, so E_0 = 2/(1-p) -- a first draft of
    # this line wrote 1 + 1/(1-p) and the function was right against it
    check("unbounded expectation at N=2: E_0 = 2/(1-p) = 4 at p = 0.5", abs(P4.expected_steps_unbounded(2, 0.5) - 4.0) < 1e-12)
    b = A.p4_budget_relative()
    check("the zero is budget-relative: same walk, rate 0.125 at 10N and 1.000 at 2000N", b["rate_at_10N"] < 0.2 and b["rate_at_2000N"] > 0.999)
    sim = P4.simulate(4, 1.0, 20, 40)
    check("no answer produced renders undefined, not zero steps", sim["mean_steps_to_answer"] is None and "undefined" in P4._f(None))
    check("grid parses the order's spec to 21 points", len(P4.grid("0.0:1.0:0.05")) == 21)

    # ---- framing and README
    fs = A.framing_scan()
    sev = {w for v in fs.values() for w in v["severity_hits"]}
    check("the only severity hit in comments and strings is the delivered contract token", sev == {"corrupt"})
    check("moral list fires once, on `kind` in the type sense (recorded, not removed)",
          {w for v in fs.values() for w in v["moral_hits"]} == {"kind"})
    rd = A.readme_checks()
    check("framing claim and one-scale-up note are verbatim in README; four falsification rows; no author heading",
          rd["framing_verbatim"] and rd["note_verbatim"] and rd["falsification_rows"] == 4 and not rd["author_or_provenance_heading"])

    # ---- renders, screen, exemption harness on `corrupt`
    out2 = P2.render(P2.audit(os.path.join(HERE, "p4_goal_coherence.py")))
    masked = out2.replace("corrupt", "c0rrupt")
    check("P2 render: masked, the screen is clean", not no_severity.hits(masked))
    check("P2 render: the delivered token is the only firer", {w for _, w, _ in no_severity.hits(out2)} == {"corrupt"})
    check("P2 render: a planted word is caught through the exemption", {w for _, w, _ in no_severity.hits(masked + "\nthis is wrong\n")} == {"wrong"})
    out1 = P1.render_report(P1.run(os.path.join(HERE, "fixtures"))[1])
    out3 = P3.render(P3.run(os.path.join(HERE, "..", "uninstrumented", "cases"), "mechanism", null="shuffle", reps=100))
    rows = P4.run(50, P4.grid("0.0:1.0:0.05"), 300, 10, 0)
    out4 = P4.render(rows)
    outa = A.render().replace("corrupt", "c0rrupt")
    for name, txt in (("P1", out1), ("P3", out3), ("P4", out4), ("audit", outa)):
        check("%s render screens clean" % name, not no_severity.hits(txt))
    check("screen fires on a planted word", bool(no_severity.hits(out4 + "\nthis is wrong\n")))
    os.makedirs(os.path.join(HERE, "samples"), exist_ok=True)
    for name, txt in (("p1_fixture", out1), ("p2_on_p4", out2), ("p3_mechanism", out3), ("p4_coherence", out4), ("order_audit", A.render())):
        with open(os.path.join(HERE, "samples", name + ".sample.txt"), "w", encoding="utf-8") as fh:
            fh.write(txt + "\n")
    with open(os.path.join(HERE, "samples", "coherence.sample.jsonl"), "w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps({k: v for k, v in r.items() if k != "_steps"}, sort_keys=True) + "\n")
    with open(os.path.join(HERE, "samples", "deps_fixture.sample.jsonl"), "w", encoding="utf-8") as fh:
        for r in P1.run(os.path.join(HERE, "fixtures"))[0]:
            fh.write(json.dumps(r, sort_keys=True) + "\n")
    rc = run(["run_all.py", "--trials", "50"])
    check("run_all runs standalone with no inputs and reports P1 NOT_RUN", rc.returncode == 0 and "P1 dependency records: NOT_RUN" in rc.stdout)
    print("selftest: %d checks, %d failed" % (N[0], len(FAILS)))
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
