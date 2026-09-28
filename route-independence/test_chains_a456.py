# SPDX-License-Identifier: CC0-1.0
"""Checks for AMENDMENTS A-4, A-5 and A-6 (chains_a4.py, termini_a5.py, eligibility_a6.py).

Run:  python3 route-independence/test_chains_a456.py
Prints the check count and whether a fixture built to FAIL exists for each amendment
(key-holder rule 3); NO_FAIL_FIXTURE in the summary line otherwise.
"""
import ast
import io
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import chains_a4 as C          # noqa: E402
import termini_a5 as F         # noqa: E402
import eligibility_a6 as E     # noqa: E402
import repairs_a31 as R        # noqa: E402

MODS = ((C, "chains_a4", 38, 51, C.EXPECTED_COMMIT_A4), (F, "termini_a5", 52, 58, F.EXPECTED_COMMIT_A5),
        (E, "eligibility_a6", 59, 65, E.EXPECTED_COMMIT_A6))
_checks = 0
_failed = 0
FAIL_FIXTURES = {}


def check(cond, msg):
    global _checks, _failed
    _checks += 1
    if not cond:
        _failed += 1
        sys.stderr.write("FAIL: %s\n" % msg)


def render(mod):
    buf = io.StringIO()
    mod.render(buf)
    return buf.getvalue()


def screen():
    sys.path.insert(0, os.path.join(HERE, "..", "sheet-structure-scan"))
    try:
        import no_severity
        return no_severity
    except ImportError:
        return None


# ------------------------------------------------------------------- A-4 ---

def t_a4():
    w = C.World()
    f1 = w.chains["F-R1"]
    check(C.v_and([C.TRUE, C.NOT_RECORDED]) == C.NOT_RECORDED and C.v_and([C.NOT_RECORDED, C.FALSE]) == C.FALSE,
          "three-valued AND [CHOICE 39]")
    check(C.v_or([C.FALSE, C.NOT_RECORDED]) == C.NOT_RECORDED and C.v_or([C.NOT_RECORDED, C.TRUE]) == C.TRUE,
          "three-valued OR")
    g = C.gates_per_chain(w, f1)
    check(g["count"] == 5 and g["gates"] == ["G-C1", "G-LAND", "G-T12", "G-T2", "G-T4"] and g["sourced"] == 0,
          "F-R1 carries 5 gates, none sourced")
    sp = C.steps_per_chain(w, f1)
    check((sp["own"], sp["transitive"]) == (2, 7), "F-R1: 2 own steps, 7 through requires [CHOICE 45]")
    check(C.lawful(w, f1) == C.FALSE and C.physical(w, f1) == C.TRUE, "F-R1: lawful FALSE, physical TRUE")
    check(C.lawful(w, w.chains["F-R2"]) == C.FALSE and C.lawful(w, w.chains["F-R3"]) == C.FALSE,
          "F-R2 (no land) and F-R3 (park) lawful FALSE")
    # the use restriction alone decides F-R1: lift it and the chain reads TRUE
    f1b = dict(f1, steps=[dict(f1["steps"][0], use_restriction=C.NONE), f1["steps"][1]])
    check(C.lawful(w, f1b) == C.TRUE, "without C-1's restriction F-R1 reads TRUE: the restriction decides it")
    check(C.lawful(w, w.chains["CH-FUEL"]) == C.TRUE, "fuel: land OR permit reads TRUE with land held")
    check(C.lawful(w, w.chains["CH-FUEL"], closed=frozenset(["LAND_TENURE", "G-LAND"])) == C.NOT_RECORDED,
          "fuel without land falls to the permit branch, whose terms are unrecorded")
    check(C.lawful(w, w.chains["CH-GLEAN"]) == C.NOT_RECORDED, "DISCRETIONARY reads NOT_RECORDED [CHOICE 40]")
    sb = C.shared_by(w, "LAND_TENURE")
    check(sb["direct"] == ["CH-FUEL", "CH-SAND", "CH-SHELTER", "F-R1", "F-R2", "F-R4"] and len(sb["transitive"]) == 8,
          "shared_by(LAND_TENURE): 6 chains direct, 8 transitive")
    ci = C.closure_impact(w, resource_id="LAND_TENURE")
    check(ci["strict"] == ["CH-SAND", "CH-SHELTER"] and len(ci["loose"]) == 4, "LAND closure: strict 2, loose 4")
    st = C.statutory_closures(w)
    check(max(len(v["strict"]) for v in st.values()) == 1 and len(st) == 8, "8 statutory gates, largest closure 1")
    check(C.closure_impact(w, gate_id="G-T2")["loose"] == [], "closing the permit moves nothing: land and token remain")
    shared = set(C.gates_per_chain(w, w.chains["F-R4"])["gates"]) & set(C.gates_per_chain(w, w.chains["CH-T4"])["gates"])
    check(shared == {"G-T2"}, "F-R4 shares the permit gate with the lifted thermal chain")
    for cid, c in w.chains.items():
        tm = C.termini(w, c)
        check(set(k for k, _ in tm["leaves"]) - {C.BODY}, "%s has a non-BODY leaf" % cid)
        check(all(k in C.TERMINUS_KINDS for k, _ in tm["leaves"]), "%s leaves are in the four kinds" % cid)
    # cycle detection: a constructed pair, reported with its path, not broken
    wc = C.World()
    wc.chains["X-A"] = C.chain("X-A", "FUEL", "x", [C.step("a", "a", "FUEL", C.ALL(C.chain_ref("X-B")))])
    wc.chains["X-B"] = C.chain("X-B", "FUEL", "x", [C.step("b", "b", "FUEL", C.ALL(C.chain_ref("X-A")))])
    tm = C.termini(wc, wc.chains["X-A"])
    check(tm["leaves"] == [(C.CYCLE, "chain:X-A")] and len(tm["cycles"]) == 1, "a cycle is a leaf with its path")
    un = C.unamended_gate_count()
    check(un["count"] == 1 and un["unit"] == "gates", "unamended A-2 / A-2.1 reads 1 gate")
    FAIL_FIXTURES["A-4"] = un["count"] == 1 and g["count"] >= 4
    ex = dict((r["id"], r["status"]) for r in C.check_expectations(w))
    check(ex == {"E-A4-1 (own steps)": R.UNMET_UNFALSIFIED, "E-A4-1 (transitive steps)": "MATCH", "E-A4-2": "NOT_EVALUABLE",
                 "E-A4-3": "NOT_EVALUABLE", "E-A4-4": "NOT_EVALUABLE", "E-A4-5": "NOT_EVALUABLE"}, "A-4 verdicts %s" % ex)
    check(C.check_expectations(w)[0]["status"] == R.UNMET_UNFALSIFIED, "the row that does not hold prints first")
    check(C.verdict("E-A4-1", (1, 3, 7)) == "MISMATCH" and C.verdict("E-A4-1", (0, 5, 7)) == R.UNMET_UNFALSIFIED,
          "verdict reads MISMATCH where F fires and UNMET_UNFALSIFIED where neither does")
    comp = dict((x["id"], R.complement(x)["status"]) for x in C.registry())
    check(comp == {"E-A4-1": R.GAP, "E-A4-2": R.GAP, "E-A4-3": R.COMPLEMENT, "E-A4-4": R.COMPLEMENT,
                   "E-A4-5": R.COMPLEMENT}, "A-4 complement check %s" % comp)
    q = C.quotes_present(C.registry(), C.AMENDMENT_FILE)
    check(all(x[2] for x in q) and len(q) == 10, "A-4 quotes found")
    lt = C.lint_two_ways(C.AMENDMENT_FILE)
    check((lt["fail_a31_list"], lt["fail_with_annotation"]) == (7, 4), "A-4 lint: 7 then 4 [CHOICE 51]")
    check(not C.hold_eligible("C-1") and C.hold_eligible("G-2"), "C-1 a fragment, not hold-eligible")


# ------------------------------------------------------------------- A-5 ---

def t_a5():
    check(F.resolve("CRED")[:3] == ("TOKEN", "MONETARY", 2), "F-B2: CREDENTIAL resolves to MONETARY at 2 hops")
    check(F.resolve("CIT")[:3] == ("TOKEN", "MONETARY", 3), "the first token seen is not the terminus; hops add")
    check(F.resolve("CYC_A")[0] == "CYCLE", "a converts_to cycle resolves to CYCLE with its path")
    w = F.layered_world()
    tk = dict((n, F.terminus_kinds(w, n)["count"]) for n in C.ROUTE_NEEDS)
    check(tk == {"WATER": 3, "FOOD": 1, "THERMAL": 2, "SHELTER": 2}, "CS-G terminus kinds per need %s" % tk)
    per = dict((n, F.nonmonetary_chains(w, n)) for n in C.ROUTE_NEEDS)
    check([len(per[n]["LITERAL"]) for n in C.ROUTE_NEEDS] == [4, 1, 1, 1], "LITERAL: every need fires")
    check(per["SHELTER"]["PATH_STRICT"] == ["CH-SHELTER"] and per["SHELTER"]["LAWFUL_STRICT"] == [],
          "SHELTER's money-free path is the prohibited public site")
    check(all(not per[n]["LAWFUL_STRICT"] for n in C.ROUTE_NEEDS), "LAWFUL_STRICT: zero on every need")
    check(per["FOOD"]["LAWFUL_UPPER"] == ["CH-GLEAN"], "LAWFUL_UPPER: gleaning, at the landowner's leave")
    wb = F.fixture_f_b3_b4()
    nb = F.nonmonetary_chains(wb, "FOOD")
    check("F-B3" in nb["PATH_STRICT"] and "F-B3" in nb["LAWFUL_STRICT"], "F-B3: the count can be nonzero")
    check(nb["cycles_apart"] == ["F-B4"] and "F-B4" not in nb["LITERAL"], "F-B4: cycles apart, never counted")
    check("F-B3" not in w.chains, "the constructed fixtures never enter CS-G")
    rr = F.reread(with_hops=True)
    check(len(rr) == 12 and all(r["a5"] == "INDEPENDENT" for r in rr), "with hops: 0 of 12 reclassified")
    rr2 = [r for r in F.reread(with_hops=False) if r["a5"] != "INDEPENDENT"]
    check(len(rr2) == 1 and rr2[0]["a5"] == "BRANCH_OF(licensed database)", "without hops: the citation route")
    check(all(r["fwo5"] == "INDEPENDENT" for r in F.reread()), "the FWO-5 reading is kept beside it")
    ff = F.fail_fixture()
    FAIL_FIXTURES["A-5"] = ff["fwo5"] == ["INDEPENDENT", "INDEPENDENT"] and all(x.startswith("BRANCH_OF") for x in ff["a5"])
    check(FAIL_FIXTURES["A-5"], "F-B1: INDEPENDENT under FWO-5, BRANCH under 2c")
    check(F.compare_sets(w, "CS-R", "WATER")["status"] == F.NOT_EVALUABLE, "CS-R NOT_EVALUABLE, never filled")
    check(F.cap_grade("COMMUNITY_RULE", "P") == "S" and F.cap_grade("STATE", "P") == "P", "COMMUNITY_RULE capped at S")
    check(set(g["layer"] for g in w.gates.values()) <= set(C.LAYERS), "every layer in the enum")
    ex = dict((r["id"], r["status"]) for r in F.check_expectations())
    want = {"E-A5-1 (LITERAL)": "MISMATCH", "E-A5-1 (PATH_STRICT)": "MISMATCH", "E-A5-1 (PATH_UPPER)": "MISMATCH",
            "E-A5-1 (LAWFUL_STRICT)": "MATCH", "E-A5-1 (LAWFUL_UPPER)": "MISMATCH", "E-A5-2": "NOT_EVALUABLE",
            "E-A5-3": "NOT_EVALUABLE", "E-A5-4 (with hops)": "MISMATCH", "E-A5-4 (without hops)": "MATCH"}
    check(ex == want, "A-5 verdicts %s" % ex)
    comp = dict((x["id"], R.complement(x)["status"]) for x in F.registry())
    check(comp == {"E-A5-1": R.COMPLEMENT, "E-A5-2": R.GAP, "E-A5-3": R.GAP, "E-A5-4": R.COMPLEMENT},
          "A-5 complement %s" % comp)
    check(all(x[2] for x in C.quotes_present(F.registry(), F.AMENDMENT_FILE)), "A-5 quotes found")
    for word in ("anti", "life"):
        check(word not in " ".join(F.CHOICES.values()).lower().split(), "provenance framing absent from fields")


# ------------------------------------------------------------------- A-6 ---

def t_a6():
    es = dict((p["profile_id"], E.eligible_sets(p)["eligible"]) for p in E.profiles())
    check(es == {"P-0": ["CS-G"], "P-1": ["CS-G", "CS-R"], "P-2": ["CS-A", "CS-G"], "P-3": ["CS-G"],
                 "P-4": ["CS-G", "CS-R4"]}, "eligible sets per profile %s" % es)
    check(all(p["constructed"] for p in E.profiles()), "every profile constructed")
    p4 = E.get_profile("P-4")
    check(E.eligible_sets(p4, "1954-01-01")["eligible"] != E.eligible_sets(p4, "1973-01-01")["eligible"],
          "P-4 differs between the two dates")
    check(E.eligible_sets(p4, "1953-01-01")["eligible"] == ["CS-G", "CS-R4"], "before termination P-4 enters CS-R4")
    g = E.exists_vs_reachable_gap(E.get_profile("P-3"), "WATER")
    check(g["status"] == F.NOT_EVALUABLE and g["gap"] is None, "the gap is NOT_EVALUABLE, never empty by default")
    ff = E.fail_fixture()
    FAIL_FIXTURES["A-6"] = ff["gap"]["gap"] == [("TOKEN", "CITATION")] and len(ff["a5_pooled"]) > len(ff["a6_reachable"])
    check(FAIL_FIXTURES["A-6"], "P-3: A-5's pooled kinds exceed its reachable kinds")
    check(E.lawful_reach_unrecognized_practice("x")["lawful_reach"] == C.NOT_RECORDED, "2d reads NOT_RECORDED")
    check(E.residence_presuming_criteria()["count"] is None, "section 3 is not filled from memory")
    check(all(v["acquirable_by_outsider"] == C.NOT_RECORDED for v in E.CASE_SETS.values()),
          "acquirable_by_outsider NOT_RECORDED with no source")
    ev = E.events_r4()
    check(set(ev[0]) >= {"route_id", "jurisdiction", "date", "from_state", "to_state", "source", "grade", "flagged"},
          "recognition events carry A-2's event keys")
    check(all(e["flagged"] and not e["hold_eligible"] for e in ev), "RA-3 events are K, flagged")
    cc = E.consistency_check()
    check(all(r["implication_holds"] for r in cc) and [r["reading"] for r in cc if r["e_a5_1_holds"]] == ["LAWFUL_STRICT"],
          "consistency check asserted; its antecedent holds only on LAWFUL_STRICT")
    check(all(r["status"] == F.NOT_EVALUABLE for r in E.check_expectations()), "every A-6 row NOT_EVALUABLE")
    comp = dict((x["id"], R.complement(x)["status"]) for x in E.registry())
    check(comp == {"E-A6-1": R.GAP, "E-A6-2": R.GAP, "E-A6-3": R.GAP, "E-A6-4": R.COMPLEMENT}, "A-6 complement %s" % comp)
    check(all(x[2] for x in C.quotes_present(E.registry(), E.AMENDMENT_FILE)), "A-6 quotes found")


# ------------------------------------------------------------------ hygiene ---

def t_hygiene():
    ns = screen()
    for mod, name, lo, hi, commit in MODS:
        src_path = os.path.join(HERE, name + ".py")
        r = render(mod)
        if ns is not None:
            ok, h = ns.check(r)
            check(ok, "%s render screens clean (%s)" % (name, [x[1] for x in h][:5]))
        for seed in ("1", "2"):
            p = subprocess.run([sys.executable, src_path], capture_output=True, text=True,
                               env=dict(os.environ, PYTHONHASHSEED=seed))
            check(p.stdout == r, "%s render identical under PYTHONHASHSEED=%s" % (name, seed))
        p = subprocess.run([sys.executable, src_path, "--selftest"], capture_output=True, text=True)
        check(p.returncode == 2, "%s refuses --selftest" % name)
        p = subprocess.run([sys.executable, src_path, "--choices"], capture_output=True, text=True)
        check(len([l for l in p.stdout.splitlines() if l.startswith("[CHOICE")]) == len(mod.CHOICES),
              "%s --choices prints every choice" % name)
        check(sorted(mod.CHOICES) == list(range(lo, hi + 1)), "%s choices numbered %d..%d" % (name, lo, hi))
        text = open(src_path).read()
        body = text.split('"""', 2)[2]
        start = body.index("CHOICES = {")
        end = body.index("\n}\n", start)
        rest = body[:start] + body[end:]
        for k in mod.CHOICES:
            check(("[CHOICE %d]" % k) in rest, "%s [CHOICE %d] cited outside its declaration" % (name, k))
        raw = open(src_path, "rb").read()
        check(all(b < 128 for b in raw), "%s ASCII" % name)
        ast.parse(raw.decode("ascii"), feature_version=(3, 8))
        log = subprocess.run(["git", "log", "--format=%h", "-n", "1", "--", mod.AMENDMENT_FILE], cwd=HERE,
                             capture_output=True, text=True).stdout.strip()
        if log:
            check(log == commit, "%s: the amendment's last commit is the EXPECTED commit (%s)" % (name, log))
        sample = os.path.join(HERE, "samples", name + ".sample.txt")
        if os.path.exists(sample):
            check(open(sample, encoding="utf-8").read() == r, "%s sample matches a fresh render" % name)
    for other in ("test_gate_state.py", "test_gate_state_a21.py", "test_thermal_gates.py", "test_repairs_a31.py",
                  "test_settlement_split.py", "test_dependency_chain.py"):
        p = subprocess.run([sys.executable, os.path.join(HERE, other)], capture_output=True)
        check(p.returncode == 0, "%s still green" % other)


for fn in (t_a4, t_a5, t_a6, t_hygiene):
    fn()

n = len([v for v in FAIL_FIXTURES.values() if v])
tag = "" if n == 3 else "  NO_FAIL_FIXTURE: %s" % sorted(k for k, v in FAIL_FIXTURES.items() if not v)
print("chains-a456: %d checks, %d failed; fail fixtures present: %d of 3%s" % (_checks, _failed, n, tag))
sys.exit(1 if _failed else 0)
