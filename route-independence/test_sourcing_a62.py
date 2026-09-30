# SPDX-License-Identifier: CC0-1.0
"""Checks for WORK ORDER standing/A-6.2 (sourcing_a62.py).

Run:  python3 route-independence/test_sourcing_a62.py
Prints the check count and whether the fixture built to FAIL exists; NO_FAIL_FIXTURE in the
summary line otherwise.
"""
import ast
import inspect
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import repairs_a31 as R        # noqa: E402
import sourcing_a62 as A       # noqa: E402
import standing_a61 as S61     # noqa: E402

_checks = 0
_failed = 0
FAIL_FIXTURE = [False]


def check(cond, msg):
    global _checks, _failed
    _checks += 1
    if not cond:
        _failed += 1
        sys.stderr.write("FAIL: %s\n" % msg)


def raises(exc, fn, *a, **k):
    try:
        fn(*a, **k)
    except exc:
        return True
    return False


def render(store=None):
    buf = io.StringIO()
    A.render(buf, store)
    return buf.getvalue()


def full(span="x", **over):
    rec = {"url": A.LII_URL, "retrieval_date": "2026-09-29", "span": span, "sha256": A.sha256_of(span)}
    rec.update(over)
    return rec


# CONSTRUCTED TEST SPAN: placeholder words in the shape of item 6's structure.  It is not
# the regulation's text and carries none of it.
FORMS1 = ["placeholder b1-%s" % r for r in A.ROMAN]
FORMS1[8] += " land"
FORMS1[9] += " area"
FORMS1[10] += " also counts toward (c)(1)(iv) and (c)(2)(ii)"
FORMS2 = ["placeholder b2-%s" % r for r in A.ROMAN[:5]]
FORMS2[0] += " members reside in an area"


def test_span(n1=11, catch_all=True):
    b1 = " ".join("(%s) %s;" % (r, t) for r, t in zip(A.ROMAN[:n1], FORMS1[:n1]))
    b2 = " ".join("(%s) %s;" % (r, t) for r, t in zip(A.ROMAN[:5], FORMS2))
    tail = " or by other evidence." if catch_all else "."
    return ("CONSTRUCTED TEST SPAN\n(a) placeholder.\n(b) placeholder. (1) two or more of: %s%s\n"
            "(2) any one of: %s\n(c) placeholder.\n" % (b1, tail, b2))


# ------------------------------------------------------------------ item 0 ---

def t_rule0():
    check(A.rule0(full())["status"] == A.SOURCED, "all four fields -> SOURCED")
    for f in ("url", "retrieval_date", "span", "sha256"):
        rec = full()
        del rec[f]
        r = A.rule0(rec)
        check(r["status"] == A.NOT_SOURCED and f in r["missing"], "missing %s -> NOT_SOURCED naming it" % f)
    check(A.rule0(full(sha256=A.sha256_of("y")))["missing"] == ["sha256"], "a hash of another span fails")
    check(A.rule0(full(url="law.cornell.edu/cfr"))["missing"] == ["url"], "url without a scheme fails")
    check(A.rule0(full(retrieval_date="Sept 29"))["missing"] == ["retrieval_date"], "non-ISO date fails")
    check(A.rule0(full(span="   ", sha256=A.sha256_of("   ")))["status"] == A.NOT_SOURCED, "blank span fails")
    repo = full(url="repo:abc1234:route-independence/x.py")
    check(A.rule0(repo)["missing"] == ["url"] and A.rule0(repo, A.REPO_ADDRESS)["status"] == A.SOURCED,
          "repo: address fails URL_RULE, passes REPO_ADDRESS [CHOICE 86]")
    graded = {"grade": "P", "reader": "the amendment's author", "text": "carried summary"}
    check(A.rule0(graded)["status"] == A.NOT_SOURCED, "graded P with no span is NOT sourced")
    check(A.rule0(full(grade="K", reader="nobody"))["status"] == A.SOURCED, "grade and reader are not read")
    for fn in (A.rule0, A.gate_a62):
        src = inspect.getsource(fn)
        body = src.split('"""', 2)[2]
        names = [n.id for n in ast.walk(ast.parse(src)) if isinstance(n, ast.Name)]
        check("grade" not in body and "reader" not in body and "grade" not in names,
              "%s reads no grade and no reader" % fn.__name__)
    store = [dict(full(span="ok"), source_id="Z-1")]
    check(A.gate_a62("MISMATCH", [("Z-1", A.CARRIED)], store=store) == "MISMATCH", "non-MATCH passes through")
    check(A.gate_a62("MATCH", [("Z-1", A.CARRIED)], False, store=store) == A.UNFALSIFIABLE_AS_RUN, "not enumerated")
    check(A.gate_a62("MATCH", [("Z-1", A.CARRIED)], True, True, store=store) == A.UNFALSIFIABLE_AS_RUN, "aggregate")
    check(A.gate_a62("MATCH", [("Z-1", A.CARRIED), ("k", A.CONSTRUCTED)], store=store) == A.CONSTRUCTED_PASS,
          "constructed input")
    check(A.gate_a62("MATCH", [("Z-2", A.CARRIED)], store=store) == A.UNSOURCED_PASS, "carried, no span")
    check(A.gate_a62("MATCH", [], store=store) == A.UNSOURCED_PASS, "a MATCH on no named input is unsourced")
    check(A.gate_a62("MATCH", [("Z-1", A.CARRIED)], store=store) == "MATCH", "a stored span lets MATCH through")
    ff = A.fail_fixture()
    check(ff == {"old": "MATCH", "rule0": A.UNSOURCED_PASS}, "fail fixture %s" % ff)
    if ff["old"] == "MATCH" and ff["rule0"] != "MATCH":
        FAIL_FIXTURE[0] = True


# ------------------------------------------------------------------ item 1 ---

WANT = {
    "E-A1 majority CONSTRUCTED": A.CONSTRUCTED_PASS, "E-A1 at least 2 of 3": A.CONSTRUCTED_PASS,
    "E-A2-1 (reading)": A.UNSOURCED_PASS, "E-A2-2": A.UNSOURCED_PASS, "E-A2-3": A.UNSOURCED_PASS,
    "E-A2-4": A.UNSOURCED_PASS, "E-A2.1-1": A.UNSOURCED_PASS, "E-A2.1-2": A.UNSOURCED_PASS,
    "E-A3-1 (reading)": A.CONSTRUCTED_PASS, "E-A3-5": A.CONSTRUCTED_PASS,
    "E-A3.1-1 (LITERAL_ALL)": A.UNSOURCED_PASS, "E-A3.1-1 (DECLARED_LITERAL)": A.UNSOURCED_PASS,
    "E-A3.1-2 (EVIDENCE)": A.CONSTRUCTED_PASS, "E-A3.1-2 (SCHEMA_DEFAULT)": A.CONSTRUCTED_PASS,
    "E-A4-1 (transitive steps)": A.CONSTRUCTED_PASS, "E-A5-1 (LAWFUL_STRICT)": A.CONSTRUCTED_PASS,
    "E-A5-4 (without hops)": A.CONSTRUCTED_PASS, "E-A6.1-1": A.CONSTRUCTED_PASS,
    "E-A6.1-3": A.UNFALSIFIABLE_AS_RUN,
}


def t_rerun():
    rows = A.rerun()
    got = dict((r["row"], r["new"]) for r in rows)
    check(got == WANT, "rule-0 status per row %s" % [(k, got.get(k)) for k in WANT if got.get(k) != WANT[k]])
    check(all(r["raw"] == "MATCH" for r in rows), "every re-gated row is a raw MATCH")
    check(len([r for r in rows if r["old"] == "MATCH"]) == 8, "the erratum's sweep kept 8 at MATCH")
    check(not [r for r in rows if r["new"] == "MATCH"], "no row reads MATCH under rule 0")
    for r in rows:
        if r["new"] == "MATCH":
            check(all(s["status"] == A.SOURCED for s in r["sources"]), "MATCH only on sourced input")
    for n in A.NAMED_ROWS:
        r = [x for x in rows if x["row"] == n or x["row"].startswith(n + " ")]
        check(len(r) == 1 and r[0]["new"] == A.UNSOURCED_PASS and r[0]["old"] == "MATCH", "%s reported" % n)
        check(not [s for s in r[0]["sources"] if s["span_stored"] or s["hash"]], "%s: span N, hash N" % n)
    rep = sorted(r["row"] for r in rows if r["repo_address"] == "MATCH")
    check(rep == ["E-A2-4", "E-A3.1-1 (DECLARED_LITERAL)", "E-A3.1-1 (LITERAL_ALL)"],
          "REPO_ADDRESS reads MATCH on the three in-repo rows only %s" % rep)
    full_rows = [r["row"] for r in rows if all(s["span_stored"] and s["hash"] for s in r["sources"])]
    check(sorted(full_rows) == rep, "span and hash present exactly on the in-repo rows")
    loc = [(s["source_id"]) for r in rows for s in r["sources"] if s["locator_in_text"]]
    # A-6.3 item 8 moved both addresses into the url field; the A-6.2 finding (W-1a, W-2a) is the before state
    check(set(loc) == set(), "no locator left in any carried text after A-6.3 item 8 [CHOICE 85] %s" % set(loc))
    check(A.load_store() == [], "the span store is empty")
    d = subprocess.run(["git", "diff", "--quiet", "HEAD", "--"] + [m + ".py" for m in
                       ("settlement_split", "gate_state", "gate_state_a21", "thermal_gates", "repairs_a31",
                        "chains_a4", "termini_a5", "eligibility_a6")], cwd=HERE)
    check(d.returncode == 0, "A-1..A-6 modules not edited")
    d = subprocess.run(["git", "diff", "--quiet", "HEAD", "--", "AMENDMENT_*.md", "ERRATUM_*.md", A.ORDER_FILE],
                       cwd=HERE)
    check(d.returncode == 0, "no amendment, erratum or order file edited")


# ------------------------------------------------------------------ item 2 ---

def t_derived():
    check(A.weakest(["P", "S"]) == "S" and A.weakest(["P", "P"]) == "P", "weakest parent")
    check(A.weakest(["P", A.NOT_RECORDED]) == A.NOT_RECORDED, "NOT_RECORDED is off the order and wins")
    old = A.committed_a61_sample()
    if old:
        dc = A.derived_print_check(old)
        check(dc["status"] == "FAIL" and len(dc["lines"]) == 2, "A-6.1 render at 37c8e58 FAILs on 2 lines")
    buf = io.StringIO()
    S61.render(buf)
    check(A.derived_print_check(buf.getvalue())["status"] == "PASS", "A-6.1 render now carries the grade")
    check(A.derived_print_check(render())["status"] == "PASS", "A-6.2 render passes its own check")
    check(A.derived_print_check("derived: COMBINATION paths 2036\n")["status"] == "FAIL", "planted: no grade -> FAIL")
    check(A.derived_print_check("outside the retrieved text: >= 7 paths\n")["status"] == "FAIL",
          "planted: the A-6.1 label without a grade -> FAIL")
    check(A.derived_print_check("derived: x 2036 [grade NOT_RECORDED via LII-83.11]\n")["status"] == "PASS",
          "with the tag -> PASS")
    ds = A.derived_values()
    check(all(d["grade"] == A.NOT_RECORDED for d in ds), "every derived value here inherits NOT_RECORDED")
    vals = dict((d["label"], d["value"]) for d in ds)
    check(vals["unread paths outside the retrieved text (erratum bound)"] == ">= 7" and
          vals["residence-presuming outside the retrieved text (erratum bound)"] == ">= 2", "erratum bounds")
    check(vals["enumerated forms outside the retrieved text (ITEM)"] == 12, "16 enumerated - 4 retrieved")
    check(vals["residence-presuming enumerated forms outside the retrieved text (GEOGRAPHIC)"] == 2 and
          vals["residence-presuming enumerated forms outside the retrieved text (LITERAL)"] == 0,
          "the erratum's >= 2 outside equals GEOGRAPHIC, not LITERAL")
    rp = S61.residence_presuming_paths()
    check(rp["outside_retrieved_text"]["grade"] == A.NOT_RECORDED, "A-6.1 derived dict carries its grade")


# -------------------------------------------------------------- items 3, 4 ---

PINNED = {
    "AMENDMENT_A4_2026-09-28_route-chains.md": {
        "nearest": [(36, "1", "gate"), (68, "4", "gates"), (98, "4", "steps"), (353, "3", "chains"),
                    (535, "1", "leaves")]},
    "AMENDMENT_A5_2026-09-28_terminus-diversity.md": {"nearest": [(45, "0", "chains"), (605, "1", "routes")]},
    "AMENDMENT_A6_2026-09-28_eligibility-recognition.md": {
        "nearest": [(28, "1", "case sets"), (136, "1", "profiles"), (468, "1", "criteria")]},
    "AMENDMENT_A6.1_2026-09-28_standing-scarcity-consolidation.md": {
        "nearest": [(91, "1", "routes"), (135, "0", "routes"), (171, "one", "chains"),
                    (729, "1", "evidence paths")]},
}


def t_pins():
    for f, want in sorted(PINNED.items()):
        p = A.pins(f)
        check(p["nearest"] == want["nearest"], "%s nearest pins %s" % (f[:12], p["nearest"]))
        check(len(p["window"]) == len(p["nearest"]), "%s totals equal under window and nearest" % f[:12])
    p = A.pins("AMENDMENT_A6.1_2026-09-28_standing-scarcity-consolidation.md")
    check(p["window_to_nearest"] == ([(52, "one", "routes")], [(171, "one", "chains")]),
          "A-6.1: the identity swap under an unchanged total %s" % (p["window_to_nearest"],))
    for f in PINNED:
        if not f.startswith("AMENDMENT_A6.1"):
            check(A.pins(f)["window_to_nearest"] == ([], []), "%s: no identity change window -> nearest" % f[:12])
    a6 = A.pins("AMENDMENT_A6_2026-09-28_eligibility-recognition.md")
    check(a6["nearest_to_agree"] == ([(136, "1", "profiles")], []) and len(a6["flags"]) == 1,
          "A-6: agreement flags '1 of P-0..P-4 ... (unit: profiles)'")
    for f in PINNED:
        if not f.startswith("AMENDMENT_A6_"):
            check(A.pins(f)["flags"] == [], "%s: no flag" % f[:12])


def t_agreement():
    check(A.agreement(" TOKEN, NOT_RECORDED or CYCLE leaf ", "leaves") == "AGREE", "leaf agrees with leaves")
    check(A.agreement(" ", "routes") == "NO_NOUN", "no words -> NO_NOUN")
    check(A.agreement(" chains ", "routes") == "DISAGREE", "chains vs routes")
    check(A.agreement(" residence_presumption_chain has BOTH ", "chains") == "AGREE", "underscore split")
    check(A.agreement(" case ", "case sets") == "DISAGREE", "multiword unit compares its last word")
    nf = A.non_nearest_fixture()
    check(nf["nearest_owner"] == ["2"], "nearest-before assigns '(unit: routes)' to 2 (the order's 'wrong')")
    check(nf["agree_owner"] == [] and len(nf["flags"]) == 1 and nf["flags"][0]["agreeing"] == ["3"],
          "agreement FLAGs, names 3 as agreeing, assigns nothing %s" % nf)
    for name, body, owner in S61.ANNOTATION_FIXTURES:
        a = A.attach_agree("Expected: %s" % body)
        check([t["token"] for t in a["tokens"] if t["owns"]] == [owner] and not a["flags"],
              "erratum fixture %s still owned by %s" % (name, owner))


# ------------------------------------------------------------------ item 5 ---

def t_aggregate():
    ea = A.erratum_sweep_ran_aggregate_condition()
    check(ea["ran"] is False, "the erratum sweep did not run the aggregate condition: %s" % ea["evidence"])
    rows = A.rerun()
    cp = [r for r in rows if r["old"] == A.CONSTRUCTED_PASS and r["module"] != "standing_a61"]
    check(len(cp) == 9, "9 prior rows at CONSTRUCTED_PASS")
    check(not [r for r in cp if r["old_no_aggregate"] != r["old"]], "0 of 9 change label under the condition")
    check([k for k, v in A.AGGREGATE_READING.items() if v[0]] == ["E-A6.1-3"], "only E-A6.1-3 is an aggregate")
    check(set(A.AGGREGATE_READING) == set(r["row"] for r in rows), "every re-gated row has a declared reading")
    check(A.gate_a62("MATCH", [("k", A.CONSTRUCTED)], True, True) == A.UNFALSIFIABLE_AS_RUN,
          "an aggregate reading would move a CONSTRUCTED_PASS row (reachable)")


# ------------------------------------------------------------ items 6, 7 ---

def t_83_11():
    check(len(A.paths(A.ITEM)) == 16, "ITEM: 16 enumerated forms")
    comb = A.paths(A.COMBINATION)
    b1 = [p for p in comb if p[0].startswith("(b)(1)")]
    check(len(b1) == 2 ** 11 - 1 - 11 == 2036 and all(len(p) >= 2 for p in b1), "(b)(1) combinations: 2036")
    check(len(comb) == 2041, "COMBINATION total 2036 + 5")
    check(raises(A.SourcingError, A.paths, "PAIR"), "an undeclared path definition is refused")
    want = {(A.ITEM, A.LITERAL): 1, (A.ITEM, A.GEOGRAPHIC): 3, (A.COMBINATION, A.LITERAL): 1,
            (A.COMBINATION, A.GEOGRAPHIC): 2036 - (2 ** 9 - 1 - 9) + 1}
    for (d, cd), n in sorted(want.items()):
        check(A.residence_count(d, cd)["residence"] == n, "residence %s/%s = %d" % (d, cd, n))
    check(want[(A.COMBINATION, A.GEOGRAPHIC)] == 1535, "1535 = 1534 (b)(1) sets with ix or x + (b)(2)(i)")
    rows = A.score_rescoped()
    check(not [r for r in rows if r["status"] == "MATCH"], "no rescoped row reads MATCH (span not stored)")
    er = dict(((r["definition"], r["coding"]), r["status"]) for r in rows if r["row"] == "E-A6-3 ERRATUM")
    check(er[(A.ITEM, A.LITERAL)] == R.UNMET_UNFALSIFIED and er[(A.ITEM, A.GEOGRAPHIC)] == A.UNSOURCED_PASS,
          "the divergence: LITERAL UNMET_UNFALSIFIED, GEOGRAPHIC UNSOURCED_PASS")
    rest = [r for r in rows if r["row"] == "E-A6-3 open remainder"]
    check(len(rest) == 1 and rest[0]["status"] == A.NE_BY_CONSTRUCTION != A.NE_TRUNCATED,
          "open remainder NOT_EVALUABLE_BY_CONSTRUCTION, a distinct reason")
    check(A.RIN_139_TARGET[1] == "enumerated forms, 83.11(b)(1)-(2)", "RIN_139 target rescoped")
    text = render()
    for line in text.splitlines():
        if "[path=" in line:
            check("coding=" in line, "definition and coding tagged on every rescoped line")


# ------------------------------------------------------------------ item 8 ---

def t_intake():
    d = tempfile.mkdtemp()
    try:
        store = os.path.join(d, "s.json")
        check(raises(A.SourcingError, A.intake, A.LII_ID, "https://example.org/x", "2026-09-30", "t", store),
              "a url other than the declared one is refused")
        check(raises(A.SourcingError, A.intake, A.LII_ID, A.LII_URL, "30 Sept", "t", store), "bad date refused")
        check(raises(A.SourcingError, A.intake, A.LII_ID, A.LII_URL, "2026-09-30", "", store), "empty span refused")
        check(not os.path.exists(store), "nothing written on refusal")
        span = test_span()
        rec = A.intake(A.LII_ID, A.LII_URL, "2026-09-30", span, store)
        check(rec["sha256"] == A.sha256_of(span) and A.rule0(rec)["status"] == A.SOURCED, "stored record SOURCED")
        A.intake(A.LII_ID, A.LII_URL, "2026-09-30", span, store)
        check(len(A.load_store(store)) == 1, "identical intake is idempotent")
        parsed = A.parse_83_11(span)
        check(len(parsed["b1"]) == 11 and len(parsed["b2"]) == 5 and parsed["b1_open_catch_all"],
              "structure parsed from the span; the (c)(1)(iv) cross-reference is not a marker")
        ev = A.reevaluate_e_a6_3(A.load_store(store))
        check(ev["state"] == "SPAN_STORED" and ev["coding_agrees_with_item_7"] ==
              {A.LITERAL: True, A.GEOGRAPHIC: True}, "residence recoded from the span agrees with item 7 %s" % ev)
        er = dict(((r["definition"], r["coding"]), r["status"]) for r in ev["rows"] if r["row"] == "E-A6-3 ERRATUM")
        check(er[(A.ITEM, A.GEOGRAPHIC)] == "MATCH",
              "LIMIT: a constructed span with the declared url passes rule 0 and lets MATCH through")
        A.intake(A.LII_ID, A.LII_URL, "2026-10-01", test_span(n1=10), store)
        check(len(A.load_store(store)) == 2, "append-only: a second span is added, the first kept")
        check(A.reevaluate_e_a6_3(A.load_store(store))["state"] == "STRUCTURE_MISMATCH",
              "the latest span with 10 (b)(1) forms reads STRUCTURE_MISMATCH")
        A.intake(A.LII_ID, A.LII_URL, "2026-10-02", "no markers here", store)
        check(A.reevaluate_e_a6_3(A.load_store(store))["state"] == "STRUCTURE_NOT_PARSED", "no markers")
        check(A.parse_83_11(test_span(catch_all=False))["b1_open_catch_all"] is False, "catch-all detected by text")
    finally:
        shutil.rmtree(d)
    check(A.reevaluate_e_a6_3()["state"] == "NO_SPAN_STORED", "the repository's store holds no 83.11 span")
    with open(A.SPAN_STORE, encoding="utf-8") as fh:
        check(json.load(fh)["records"] == [], "span_store.json ships empty")


# ---------------------------------------------------------------- hygiene ---

def t_hygiene():
    r = render()
    for seed in ("0", "7"):
        p = subprocess.run([sys.executable, os.path.join(HERE, "sourcing_a62.py")], capture_output=True, text=True,
                           env=dict(os.environ, PYTHONHASHSEED=seed))
        check(p.stdout == r, "render identical under PYTHONHASHSEED=%s" % seed)
    src = os.path.join(HERE, "sourcing_a62.py")
    p = subprocess.run([sys.executable, src, "--selftest"], capture_output=True, text=True)
    check(p.returncode == 2, "refuses --selftest")
    p = subprocess.run([sys.executable, src, "--choices"], capture_output=True, text=True)
    check(len([l for l in p.stdout.splitlines() if l.startswith("[CHOICE")]) == len(A.CHOICES), "--choices")
    check(sorted(A.CHOICES) == list(range(84, 95)), "choices numbered 84..94")
    text = open(src).read()
    body = text.split('"""', 2)[2]
    start = body.index("CHOICES = {")
    end = body.index("\n}\n", start)
    rest = body[:start] + body[end:]
    for k in A.CHOICES:
        check(("[CHOICE %d]" % k) in rest, "[CHOICE %d] cited outside its declaration" % k)
    raw = open(src, "rb").read()
    check(all(b < 128 for b in raw), "ASCII")
    ast.parse(raw.decode("ascii"), feature_version=(3, 8))
    p = subprocess.run([sys.executable, os.path.join(HERE, "..", "sheet-structure-scan", "no_severity.py")],
                       input=r, capture_output=True, text=True)
    check("no severity or interpretation vocabulary" in p.stdout, "render screens clean")
    log = subprocess.run(["git", "log", "--format=%h", "-n", "1", "--", A.ORDER_FILE], cwd=HERE,
                         capture_output=True, text=True).stdout.strip()
    if log:
        check(log == A.EXPECTED_COMMIT_A62, "the order's last commit is its registration commit (%s)" % log)
    order = open(os.path.join(HERE, A.ORDER_FILE), encoding="utf-8").read()
    check(order.startswith("WORK ORDER — standing/A-6.2 : physical sourcing rule"), "order landed as delivered")
    lo = A.order_lint()
    check(lo["saw_2036"] is False and len(lo["ok"]) == 2, "A-3.1 lint on the order: 2036 unseen, 2 OK tokens")
    sample = os.path.join(HERE, "samples", "sourcing_a62.sample.txt")
    if os.path.exists(sample):
        check(open(sample, encoding="utf-8").read() == r, "sample matches a fresh render")
    p = subprocess.run([sys.executable, os.path.join(HERE, "test_standing_a61.py")], capture_output=True)
    check(p.returncode == 0, "test_standing_a61.py still green")


for fn in (t_rule0, t_rerun, t_derived, t_pins, t_agreement, t_aggregate, t_83_11, t_intake, t_hygiene):
    fn()

n = 1 if FAIL_FIXTURE[0] else 0
tag = "" if n else "  NO_FAIL_FIXTURE"
print("sourcing-a62: %d checks, %d failed; fail fixtures present: %d of 1%s" % (_checks, _failed, n, tag))
sys.exit(1 if _failed else 0)
