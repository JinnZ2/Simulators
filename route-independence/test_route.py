# SPDX-License-Identifier: CC0-1.0
"""Checks for route-independence (FWO-1, FWO-2, FWO-3).

Run:  python3 route-independence/test_route.py
Prints the check count; nothing stores it. Demo fixtures are
implementation-authored: they are regression checks on the instruments,
not validation of any row against the world.
"""
import ast
import importlib.util
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import entry_condition_match as ecm   # noqa: E402
import route_independence as ri       # noqa: E402
import untried_options_audit as uoa   # noqa: E402

_checks = 0
_failed = 0


def check(cond, msg):
    global _checks, _failed
    _checks += 1
    if not cond:
        _failed += 1
        sys.stderr.write("FAIL: %s\n" % msg)


def demo(name):
    return os.path.join(HERE, "demo", name)


def screen():
    path = os.path.join(HERE, "..", "sheet-structure-scan", "no_severity.py")
    if not os.path.exists(path):
        return None
    spec = importlib.util.spec_from_file_location("no_severity", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ============================================================ FWO-1

STUDY = """study: s
food | DECOUPLED | src
exit | REMOVED | src
"""


def rows(text):
    name, r, ref = ecm.parse_rows(text)
    assert not ref, ref
    return r


def t_fwo1():
    s = rows(STUDY)
    # every row MATCH -> TRANSFERABLE
    r = ecm.evaluate(s, rows("food | DECOUPLED | src\nexit | REMOVED | src\n"))
    check(r["overall"] == ecm.TRANSFERABLE, "all-match reads TRANSFERABLE")
    # one row UNKNOWN -> never TRANSFERABLE
    r = ecm.evaluate(s, rows("food | DECOUPLED | src\nexit | UNKNOWN | src\n"))
    check(r["overall"] == ecm.NOT_EVALUABLE, "UNKNOWN load-bearing row -> NOT_EVALUABLE")
    check(r["rows"][1]["result"] == ecm.UNKNOWN and r["rows"][1]["reason"] == "population_row_unknown",
          "per-row UNKNOWN carries its reason")
    r = ecm.evaluate(s, rows("food | DECOUPLED | src\n"))
    check(r["overall"] == ecm.NOT_EVALUABLE and r["rows"][1]["reason"] == "population_row_absent",
          "an absent population row is UNKNOWN(population_row_absent), not a default")
    # non-load-bearing UNKNOWN still blocks TRANSFERABLE [CHOICE 1]
    s2 = rows("food | DECOUPLED | src\nexit | REMOVED | src | load_bearing=no\n")
    r = ecm.evaluate(s2, rows("food | DECOUPLED | src\nexit | UNKNOWN | src\n"))
    check(r["overall"] == ecm.NOT_EVALUABLE and "unknown_rows_block_transferable" in r["reason"],
          "non-load-bearing UNKNOWN blocks TRANSFERABLE")
    r = ecm.evaluate(s2, rows("food | COUPLED | src\nexit | UNKNOWN | src\n"))
    check(r["overall"] == ecm.NOT_TRANSFERABLE and r["unknown_not_load_bearing"] == ["exit"],
          "non-load-bearing UNKNOWN is excluded from a tally that has a MISMATCH, and listed")
    # PARTIAL lists both sides; distinct from NOT_TRANSFERABLE
    r = ecm.evaluate(s, rows("food | DECOUPLED | src\nexit | PRESENT | src\n"))
    check(r["overall"] == ecm.PARTIAL and r["hold"] == ["food"] and r["fail"] == ["exit"],
          "PARTIAL lists hold and fail")
    r = ecm.evaluate(s, rows("food | COUPLED | src\nexit | PRESENT | src\n"))
    check(r["overall"] == ecm.NOT_TRANSFERABLE and r["hold"] == [] and r["fail"] == ["food", "exit"],
          "no match -> NOT_TRANSFERABLE, not PARTIAL")
    # marker derives DECOUPLED; conflict reported
    name, pr, ref = ecm.parse_rows("shelter | UNKNOWN | | dwellings_held=2\n")
    check(not ref and pr[0]["state"] == "DECOUPLED" and pr[0]["derived_from_marker"],
          "dwellings_held > 1 derives DECOUPLED from UNKNOWN")
    name, pr, ref = ecm.parse_rows("shelter | COUPLED | src | dwellings_held=2\n")
    check(pr[0]["state"] == "DECOUPLED" and pr[0]["marker_conflict"], "marker overrides and reports conflict")
    name, pr, ref = ecm.parse_rows("shelter | COUPLED | src | dwellings_held=1\n")
    check(pr[0]["state"] == "COUPLED" and not pr[0]["derived_from_marker"], "dwellings_held=1 derives nothing")
    # gradient refused; duplicate refused
    name, pr, ref = ecm.parse_rows("food | PARTLY_DECOUPLED | src\n")
    check(ref and ref[0][0] == "INVALID_STATE", "gradient state refused as INVALID_STATE")
    name, pr, ref = ecm.parse_rows("food | COUPLED |\nfood | COUPLED |\n")
    check(any(k == "DUPLICATE_CONDITION" for k, _ in ref), "duplicate condition refused")
    # sourced / synthetic
    name, pr, ref = ecm.parse_rows("food | COUPLED |\nwater | COUPLED | a source\n")
    check(pr[0]["sourced"] is False and pr[1]["sourced"] is True, "empty source reads SYNTHETIC")
    # demo: expected structure stated before the run
    _, srows, sref = ecm.load(demo("universe25_study.txt"))
    check(not sref and len(srows) == 8, "study file parses to eight rows")
    results = {}
    for tag in ("a_effort_coupled", "b_short_supply", "c_paid_provision"):
        _, prow, pref = ecm.load(demo("population_%s.txt" % tag))
        check(not pref, "population %s parses" % tag)
        results[tag] = ecm.evaluate(srows, prow)
    a, b, c = results["a_effort_coupled"], results["b_short_supply"], results["c_paid_provision"]
    prov = ["food", "water", "shelter", "thermal", "waste_removal"]
    check(all(x in a["fail"] for x in prov), "(a) mismatches on the provision rows")
    b_prov = [r for r in b["rows"] if r["condition"] in prov]
    check(sum(1 for r in b_prov if r["result"] == ecm.MISMATCH) >= 4
          and all(r["result"] in (ecm.MISMATCH, ecm.UNKNOWN) for r in b_prov),
          "(b) mismatches on most provision rows per row; its one UNKNOWN row stays UNKNOWN")
    check(b["overall"] == ecm.NOT_EVALUABLE, "(b) is NOT_EVALUABLE on its UNKNOWN row")
    check(c["overall"] != ecm.TRANSFERABLE, "(c) is never TRANSFERABLE (the order's own kill line)")
    check(c["overall"] == ecm.PARTIAL and "exit" in c["fail"] and all(x in c["hold"] for x in prov),
          "(c) matches provision rows and mismatches on exit")
    _, prow, pref = ecm.load(demo("population_fail_gradient.txt"))
    check(pref and pref[0][0] == "INVALID_STATE", "the required failing demo input is refused")
    # every overall member reachable
    seen = set(x["overall"] for x in results.values())
    seen.add(ecm.evaluate(s, rows("food | DECOUPLED | src\nexit | REMOVED | src\n"))["overall"])
    seen.add(ecm.evaluate(s, rows("food | COUPLED | src\nexit | PRESENT | src\n"))["overall"])
    check(seen == set(ecm.OVERALLS), "every overall member is reached: %s" % sorted(seen))
    text = ecm.render("s", "p", c)
    check("PARTIAL" in text and "hold=[" in text and "fail=[" in text, "render carries both PARTIAL lists")


# ============================================================ FWO-2

ROUTES = """dominant: USD
n | r1 | goods | USD | yes | s
n | r2 | USD   | USD | yes | s
"""


def t_fwo2():
    dom, r, ref = ri.parse_routes(ROUTES)
    check(not ref and dom == "USD", "routes parse")
    m = ri.measure(r, dom)["n"]
    check(m["flag"] == ri.ENCLOSED_PLURALITY and m["independent_count"] == 0 and m["route_count"] == 2,
          "two routes, none settling in their own medium -> ENCLOSED_PLURALITY")
    dom, r, ref = ri.parse_routes("dominant: USD\nn | r1 | hours | hours | yes | s\nn | r2 | USD | USD | yes | s\n")
    m = ri.measure(r, dom)["n"]
    check(m["flag"] == ri.NOT_ENCLOSED and m["independent_count"] == 1, "one self-settling route -> NOT_ENCLOSED")
    dom, r, ref = ri.parse_routes("dominant: USD\nn | r1 | goods | UNKNOWN | yes | s\nn | r2 | USD | USD | yes | s\n")
    m = ri.measure(r, dom)["n"]
    check(m["flag"] == ri.UNKNOWN and m["independent_count"] == (0, 1) and m["independence_ratio"] == (0.0, 0.5),
          "an UNKNOWN medium gives a band and an UNKNOWN flag, never False")
    dom, r, ref = ri.parse_routes("dominant: USD\nn | r1 | goods | USD | yes | s\n")
    check(ri.measure(r, dom)["n"]["flag"] == ri.SINGLE_ROUTE, "one route -> SINGLE_ROUTE")
    check(ri.measure_need([], "USD")["flag"] == ri.NOT_EVALUABLE, "zero routes -> NOT_EVALUABLE")
    check(ri.independence_ratio(0, 0) is None, "ratio is None, not 0.0, on zero routes")
    check(ri.independence_ratio(0, 4) == 0.0 and ri.independence_ratio(2, 4) == 0.5, "ratio arithmetic")
    # the dominant token never counts as independent even when it settles in itself
    check(ri.discharges_own_obligations("USD", "USD", "USD") is False, "dominant token is not independent")
    check(ri.discharges_own_obligations("hours", "hours", "USD") is True, "own medium, not dominant -> independent")
    check(ri.discharges_own_obligations("hours", "UNKNOWN", "USD") is None, "UNKNOWN medium -> None")
    # TEST OF THE TEST: permitted reaches no measure
    dom, r, ref = ri.parse_routes("dominant: USD\nn | r1 | goods | USD | yes | s\nn | r2 | USD | USD | yes | s\n")
    dom2, r2, ref2 = ri.parse_routes("dominant: USD\nn | r1 | goods | USD | no | s\nn | r2 | USD | USD | UNKNOWN | s\n")
    m1, m2 = ri.measure(r, dom)["n"], ri.measure(r2, dom2)["n"]
    same = all(m1[k] == m2[k] for k in ("route_count", "independent_count", "independence_ratio", "flag"))
    check(same, "flipping `permitted` moves no measure")
    check([p["permitted"] for p in m2["routes"]] == ["no", "UNKNOWN"], "permitted is carried per route as its own field")
    src = open(os.path.join(HERE, "route_independence.py"), encoding="utf-8").read()
    tree = ast.parse(src)
    for fn in ("discharges_own_obligations", "independence_ratio", "flag_for"):
        node = next(n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name == fn)
        consts = [n.value for n in ast.walk(node) if isinstance(n, ast.Constant) and isinstance(n.value, str)]
        reads = [n for n in ast.walk(node) if isinstance(n, ast.Subscript)
                 and isinstance(n.slice, ast.Constant) and n.slice.value == "permitted"]
        check(not reads, "%s never reads r['permitted']" % fn)
        names = [n.id for n in ast.walk(node) if isinstance(n, ast.Name)]
        check("permitted" not in names, "%s binds no name `permitted`" % fn)
    # refusals
    dom, r, ref = ri.parse_routes("n | r1 | goods | USD | yes | s\n")
    check(any(k == "DOMINANT_UNDECLARED" for k, _ in ref), "no dominant header is refused")
    dom, r, ref = ri.parse_routes("dominant: USD\nn | r1 | goods | USD | maybe | s\n")
    check(any(k == "INVALID_PERMITTED" for k, _ in ref), "permitted outside yes/no/UNKNOWN is refused")
    # demo
    dom, r, ref = ri.load(demo("routes.txt"))
    check(not ref, "demo routes parse")
    res = ri.measure(r, dom)
    check(res["water"]["flag"] == ri.ENCLOSED_PLURALITY, "demo: water reads ENCLOSED_PLURALITY")
    check(res["food"]["flag"] == ri.UNKNOWN and res["food"]["unknown_routes"] == ["gift_mutual_aid"],
          "demo: food carries one UNKNOWN medium and the flag stays UNKNOWN")
    check(res["control_constructed"]["flag"] == ri.NOT_ENCLOSED, "demo: constructed control reaches NOT_ENCLOSED")
    check("household_production" in res["food"]["synthetic_routes"], "unsourced demo row is marked SYNTHETIC")
    cc = ri.cross_check(res["water"])
    check(cc["status"] in ("AGREE", "PRIOR_ART_NOT_IMPORTED"), "cross-check runs or reports the sibling absent")
    if cc["status"] == "AGREE":
        check(cc["n_eff"] == 1 and cc["n_nominal"] == 2, "prior instrument reads n_eff 1 of 2")
        cc2 = ri.cross_check(res["control_constructed"])
        check(cc2["status"] == "AGREE" and cc2["n_eff"] == 2, "prior instrument agrees on the control")
    check(ri.cross_check(res["food"])["status"] == "NOT_EVALUABLE", "cross-check refuses to code an UNKNOWN medium")


# ============================================================ FWO-3

def rec(text):
    r, ref = uoa.parse_record(text)
    assert not ref, ref
    return r


def t_fwo3():
    base = ("decision: d\nproposer: p\nfirst_cost_bearers: p; q\nauthorizer: a\n"
            "authorizer_prior_exposure: yes\noptions_tried: x\noptions_not_tried: w\n"
            "reviewer: t\nreviewer_can_add_options: yes\nreviewer_added_options: w; z\nsource: s\n")
    a = uoa.audit(rec(base))
    check(a["C1"] == uoa.YES and a["C2"] == uoa.YES and a["C3"] == uoa.YES and a["C4"] == uoa.YES,
          "full record: C1-C4 YES")
    check(a["C5"] == uoa.RETURN_FOR_REDO and a["C5_options"] == ["z"], "unlisted reviewer option -> RETURN_FOR_REDO(z)")
    a = uoa.audit(rec(base.replace("reviewer_added_options: w; z", "reviewer_added_options: w")))
    check(a["C5"] == uoa.ALL_ALREADY_LISTED, "listed reviewer option -> ALL_ALREADY_LISTED")
    a = uoa.audit(rec(base.replace("reviewer_added_options: w; z", "reviewer_added_options:")))
    check(a["C5"] == uoa.NONE_ADDED, "empty reviewer_added_options -> NONE_ADDED")
    a = uoa.audit(rec(base.replace("reviewer_added_options: w; z\n", "")))
    check(a["C5"] == uoa.ABSENT_FIELD, "no reviewer_added_options slot -> ABSENT_FIELD")
    # NO vs ABSENT_FIELD kept apart on C3
    a_no = uoa.audit(rec(base.replace("options_not_tried: w", "options_not_tried:")))
    a_ab = uoa.audit(rec(base.replace("options_not_tried: w\n", "")))
    check(a_no["C3"] == uoa.NO and a_ab["C3"] == uoa.ABSENT_FIELD, "C3: empty slot is NO, no slot is ABSENT_FIELD")
    check("options_not_tried" in a_ab["absent_fields"], "absent field is listed by name")
    # C1
    check(uoa.audit(rec(base.replace("first_cost_bearers: p; q", "first_cost_bearers: q")))["C1"] == uoa.NO,
          "proposer names others -> C1 NO")
    check(uoa.audit(rec(base.replace("first_cost_bearers: p; q", "first_cost_bearers: UNKNOWN")))["C1"] == uoa.UNKNOWN,
          "UNKNOWN cost bearers -> C1 UNKNOWN")
    # C4 independence
    check(uoa.audit(rec(base.replace("reviewer: t", "reviewer: p")))["C4"] == uoa.NO, "reviewer == proposer -> C4 NO")
    check(uoa.audit(rec(base.replace("reviewer: t", "reviewer: a")))["C4"] == uoa.NO, "reviewer == authorizer -> C4 NO")
    no_auth = base.replace("reviewer_can_add_options: yes\n", "").replace("reviewer_added_options: w; z", "reviewer_added_options:")
    check(uoa.audit(rec(no_auth))["C4"] == uoa.UNKNOWN, "authority unstated and undemonstrated -> C4 UNKNOWN")
    demo_auth = base.replace("reviewer_can_add_options: yes\n", "")
    check(uoa.audit(rec(demo_auth))["C4"] == uoa.YES, "authority demonstrated by an added option -> C4 YES")
    # refusals
    r, ref = uoa.parse_record("decision: d\ndecision: e\n")
    check(any(k == "DUPLICATE_FIELD" for k, _ in ref), "duplicate field refused")
    r, ref = uoa.parse_record("no colon here\n")
    check(any(k == "MALFORMED_LINE" for k, _ in ref), "line without a colon refused")
    # demo records
    recdir = os.path.join(HERE, "demo", "records")
    names = sorted(os.listdir(recdir))
    audits = {}
    for n in names:
        r, ref = uoa.load(os.path.join(recdir, n))
        check(not ref, "record %s parses" % n)
        audits[n] = uoa.audit(r)
    real = [n for n in names if audits[n]["source_status"] == "read"]
    synth = [n for n in names if audits[n]["source_status"] == "synthetic"]
    check(len(real) >= 5 and len(synth) == 2, "five read records and two synthetic ones")
    check(all(audits[n]["source"] for n in real), "every read record names its source")
    check(audits["synthetic-return-for-redo.txt"]["C5"] == uoa.RETURN_FOR_REDO, "constructed record fires RETURN_FOR_REDO")
    check(audits["synthetic-empty-slot.txt"]["C3"] == uoa.NO, "constructed record shows the NO state")
    # the order's expectation on institutional records, and the finding that a slot exists
    c3 = dict((n, audits[n]["C3"]) for n in real)
    check(all(audits[n]["C1"] == uoa.ABSENT_FIELD for n in real), "no read record carries a first_cost_bearers slot")
    check(all(audits[n]["C2"] == uoa.ABSENT_FIELD for n in real), "no read record carries an authorizer_prior_exposure slot")
    with_slot = [n for n in real if c3[n] == uoa.YES]
    check(set(with_slot) == {"seam-gaps-g05.txt"},
          "the council's untried-and-available slot is on one read record: %s" % with_slot)
    considered = [n for n in real if audits[n]["C3c"] == uoa.YES]
    check(set(considered) == {"pep-0572.txt", "rust-rfc-template.txt", "madr-template.txt"},
          "the considered-and-rejected slot is on three engineering records: %s" % considered)
    check(all(audits[n]["C3a"] == uoa.ABSENT_FIELD for n in real),
          "no read record carries a slot for options tried in the world")
    check(c3["openai-model-spec.txt"] == uoa.ABSENT_FIELD and c3["design-basis-ai.txt"] == uoa.ABSENT_FIELD,
          "both AI documents read ABSENT_FIELD on C3")
    check(not [n for n in real if audits[n]["C4"] == uoa.YES],
          "no read record gives an independent reviewer authority to add options")
    check(audits["pep-0572.txt"]["C4"] == uoa.NO, "PEP 572 reads C4 NO on PEP 1's stated authority")
    check(not [n for n in real if audits[n]["C5"] == uoa.RETURN_FOR_REDO],
          "RETURN_FOR_REDO fires on no read record")
    # options_considered never counts toward C3 [CHOICE 4]
    a = uoa.audit(rec("decision: d\noptions_considered: x; y\n"))
    check(a["C3"] == uoa.ABSENT_FIELD and a["C3c"] == uoa.YES, "a considered-and-rejected list does not read as C3")


# ============================================================ renders / headers

def t_renders():
    ns = screen()
    _, srows, _ = ecm.load(demo("universe25_study.txt"))
    _, prow, _ = ecm.load(demo("population_c_paid_provision.txt"))
    texts = [ecm.render("s", "c", ecm.evaluate(srows, prow))]
    dom, r, _ = ri.load(demo("routes.txt"))
    texts.append(ri.render(ri.measure(r, dom), dom))
    for n in sorted(os.listdir(os.path.join(HERE, "demo", "records"))):
        rr, _ = uoa.load(os.path.join(HERE, "demo", "records", n))
        texts.append(uoa.render(uoa.audit(rr)))
    if ns is None:
        check(True, "no_severity not beside this folder; screen NOT_RUN")
    else:
        for t in texts:
            clean, h = ns.check(t)
            check(clean, "render screens clean: %s" % h[:3])
        planted, _ = ns.check("this row is wrong")
        check(not planted, "screen fires on a plant")
    for f in ("entry_condition_match.py", "route_independence.py", "untried_options_audit.py"):
        src = open(os.path.join(HERE, f), encoding="utf-8").read()
        check(src.startswith("# SPDX-License-Identifier: CC0-1.0"), "%s carries the CC0 header" % f)
        for banned in ("import urllib", "import socket", "import http", "import requests"):
            check(banned not in src, "%s has no network import (%s)" % (f, banned))
        check("import subprocess" not in src, "%s has no subprocess" % f)


if __name__ == "__main__":
    t_fwo1()
    t_fwo2()
    t_fwo3()
    t_renders()
    print("route-independence: %d checks, %d failed" % (_checks, _failed))
    sys.exit(1 if _failed else 0)
