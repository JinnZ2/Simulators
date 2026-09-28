# SPDX-License-Identifier: CC0-1.0
"""Checks for AMENDMENT A-2 (gate_state.py).

Run:  python3 route-independence/test_gate_state.py
Prints the check count and whether a fixture built to FAIL exists (key-holder
rule 3); NO_FAIL_FIXTURE in the summary line otherwise.
"""
import ast
import importlib.util
import io
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import dependency_chain_audit as D   # noqa: E402
import settlement_split as S         # noqa: E402
import gate_state as G               # noqa: E402

_checks = 0
_failed = 0
FAIL_FIXTURE = False


def check(cond, msg):
    global _checks, _failed
    _checks += 1
    if not cond:
        _failed += 1
        sys.stderr.write("FAIL: %s\n" % msg)


def refuses(fn, exc, needle, msg):
    try:
        fn()
    except exc as e:
        check(needle in str(e), "%s (refusal names %r; got %s)" % (msg, needle, e))
        return
    check(False, "%s (expected a refusal naming %r)" % (msg, needle))


def screen():
    path = os.path.join(HERE, "..", "sheet-structure-scan", "no_severity.py")
    if not os.path.exists(path):
        return None
    spec = importlib.util.spec_from_file_location("no_severity", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def render():
    buf = io.StringIO()
    G.render(buf)
    return buf.getvalue()


def defined_names(path):
    tree = ast.parse(open(path, encoding="utf-8").read())
    return set(n.name for n in tree.body if isinstance(n, (ast.FunctionDef, ast.ClassDef))) | \
        set(t.id for n in tree.body if isinstance(n, ast.Assign) for t in n.targets if isinstance(t, ast.Name))


SRC = os.path.join(HERE, "gate_state.py")
CONV = {"HERE", "CHOICES", "render", "main", "check_expectations", "fail_fixture"}   # per-module conventions
SRC_TEXT = open(SRC, encoding="utf-8").read()
TREE = ast.parse(SRC_TEXT)


def _strings_and_names(node):
    out = set()
    for sub in ast.walk(node):
        if isinstance(sub, ast.Constant) and isinstance(sub.value, str):
            out.add(sub.value)
        if isinstance(sub, ast.Name):
            out.add(sub.id)
        if isinstance(sub, ast.Attribute):
            out.add(sub.attr)
    return out


# ---------------------------------------------------------------- structure ---

def t_structure():
    for other in ("dependency_chain_audit.py", "edge_taxonomy.py", "settlement_split.py"):
        clash = (defined_names(os.path.join(HERE, other)) & defined_names(SRC)) - CONV
        check(not clash, "gate_state redefines no name of %s (clash %s)" % (other, sorted(clash)))
    check(G.NONE_ORIGIN not in S.ORIGINS, "NONE is not a member of A-1's ORIGINS; A-1 is not edited")
    check(G.UNKNOWN_STATE == "UNKNOWN" and G.STATES[-1] == "UNKNOWN" and len(G.STATES) == 5, "the five gate states, UNKNOWN last")
    # E-A2-4 by AST: no expression names DISCRETIONARY together with OPEN or INDEPENDENT
    bad = []
    for node in ast.walk(TREE):
        if isinstance(node, (ast.BoolOp, ast.Compare, ast.BinOp, ast.IfExp)):
            if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Mod) and isinstance(node.left, ast.Constant):
                continue   # a format string is not a reading (IRB_018)
            names = _strings_and_names(node)
            if "DISCRETIONARY" in names and ({"OPEN", "OPEN_STATES", "INDEPENDENT", "is_open"} & names):
                bad.append(ast.dump(node)[:70])
    check(not bad, "E-A2-4: no expression reads DISCRETIONARY beside OPEN / INDEPENDENT (%s)" % bad[:2])
    check(G.DISCRETIONARY not in G.OPEN_STATES and G.OPEN_STATES == ("OPEN",), "E-A2-4: OPEN_STATES holds OPEN alone")
    # the scan is not silent: a planted expression fires
    planted = ast.parse("x = 1 if state == DISCRETIONARY else (state == OPEN)")
    fired = [n for n in ast.walk(planted) if isinstance(n, (ast.BoolOp, ast.Compare, ast.BinOp, ast.IfExp))
             and "DISCRETIONARY" in _strings_and_names(n) and "OPEN" in _strings_and_names(n)]
    check(fired, "the E-A2-4 scan fires on a planted expression")
    # the module never touches FWO-5's INDEPENDENT at all
    attrs = [n.attr for n in ast.walk(TREE) if isinstance(n, ast.Attribute) and n.attr == "INDEPENDENT"]
    check(not attrs, "gate_state references D.INDEPENDENT nowhere; a gate row is never promoted to a status")
    # closures and loosenings are never netted: no BinOp subtracts or adds two tally members
    net = []
    for node in ast.walk(TREE):
        if isinstance(node, ast.BinOp) and isinstance(node.op, (ast.Sub, ast.Add)):
            names = _strings_and_names(node)
            if {"CLOSURE", "LOOSENING"} & names:
                net.append(ast.dump(node)[:60])
    check(not net, "no arithmetic nets CLOSURE against LOOSENING (%s)" % net[:2])
    check(G.EXPECTED_COMMIT_A2 != S.EXPECTED_COMMIT, "A-2 registers its own EXPECTED commit, not A-1's")


# ------------------------------------------------------------------ dates ---

def t_dates():
    r = {"route": "x", "t_from": "2016-08-10", "t_to": None}
    check(G.at(r, "2016-08-10") and G.at(r, "2026") and not G.at(r, "2016-08-09"), "[t_from, t_to) with t_to None open-ended")
    r2 = {"route": "x", "t_from": None, "t_to": "1788"}
    check(G.at(r2, "1787-12-31") and not G.at(r2, "1788") and not G.at(r2, "1788-06-01"), "t_to exclusive at year precision")
    check(not G.at({"route": "x", "t_from": None, "t_to": None}, "2026"), "a row with no t is in force nowhere")
    refuses(lambda: G.at(r, "10 Aug 2016"), G.GateError, "ISO date", "a non-ISO t is refused")
    refuses(lambda: G._date("2016-8-1", "t", "x"), G.GateError, "ISO date", "an unpadded date is refused")
    check(G._date("2011", "t", "x") == "2011" and G._date("2011-09", "t", "x") == "2011-09", "reduced precision admitted [CHOICE 2]")


# ------------------------------------------------------------------- rows ---

def _row():
    return D.route("r", D.NONE_MEDIUM, D.NONE_MEDIUM, "CONSTRUCTED: test")


def t_rows():
    r = _row()
    g = G.gate(r, "rid", "Nowhere", "2000", None, G.OPEN, None, "W-3", tag=None)
    check("gate_state" not in r and g["gate_state"] == G.OPEN, "gate copies; the FWO-5 record is unchanged")
    check(G.gate_reading(g) == G.OPEN and g["hold_eligible"] and g["gate_grade"] == "S", "a sourced, dated row reads its state and is hold-eligible")
    refuses(lambda: G.gate(r, "rid", "", "2000", None, G.OPEN, None, "W-3"), G.GateError, "jurisdiction", "jurisdiction is required")
    refuses(lambda: G.gate(r, "", "J", "2000", None, G.OPEN, None, "W-3"), G.GateError, "route_id", "route_id is required")
    refuses(lambda: G.gate(r, "rid", "J", "2000", None, "CLOSED", None, "W-3"), G.GateError, "gate_state", "a state outside the five is refused")
    refuses(lambda: G.gate(r, "rid", "J", "2000", None, G.OPEN, None, None), G.GateError, "gate_source is required", "a non-UNKNOWN row without a source is refused")
    refuses(lambda: G.gate(r, "rid", "J", "2000", None, G.OPEN, None, "X-9"), G.GateError, "section-2 id", "an unlisted source id is refused")
    refuses(lambda: G.gate(r, "rid", "J", "2016", "2015", G.OPEN, None, "W-3"), G.GateError, "t_from < t_to", "a reversed interval is refused")
    refuses(lambda: G.gate(r, "rid", "J", "2000", None, G.OPEN, None, "W-3", requirement="wifi"), G.GateError, "requirement", "an off-list requirement is refused")
    refuses(lambda: G.gate(r, "rid", "J", "2000", None, G.OPEN, None, "W-3", tag="SOURCED"), G.GateError, "tag", "an unlisted tag is refused")
    u = G.gate(r, "rid", "J", "2000", None, G.UNKNOWN_STATE, None, None)
    check(G.gate_reading(u) == G.UNKNOWN_STATE and not u["hold_eligible"], "UNKNOWN needs no source and is not hold-eligible")
    c = G.gate(r, "rid", "J", "2000", None, G.OPEN, None, None, tag=G.CONSTRUCTED_UNSOURCED)
    check(G.gate_reading(c) == G.OPEN and not c["hold_eligible"], "a CONSTRUCTED_UNSOURCED row reads but never enters a hold")
    k = G.gate(r, "rid", "J", "2000", None, G.OPEN, None, "G-3")
    check(k["gate_grade"] == "K" and not k["hold_eligible"], "a grade-K source is stored and excluded from holds")
    # 3a: no t -> UNKNOWN, never OPEN
    nt = G.gate(r, "rid", "J", None, None, G.OPEN, None, "W-3")
    check(nt["gate_state"] == G.OPEN and G.gate_reading(nt) == G.UNKNOWN_STATE, "declared OPEN with no t READS UNKNOWN (3a)")
    check(G.gate_reading(_row()) == G.UNKNOWN_STATE, "a row never given gate fields reads UNKNOWN [CHOICE 1]")
    check(G.gate_reading(dict(g, jurisdiction="")) == G.UNKNOWN_STATE, "a row with no jurisdiction reads UNKNOWN")
    check(not G.is_open(G.DISCRETIONARY) and not G.is_open(G.METERED_PERMISSION) and not G.is_open(G.PROHIBITED)
          and not G.is_open(G.UNKNOWN_STATE) and G.is_open(G.OPEN), "OPEN is the only open state (E-A2-4)")
    # reading_at
    rows = [G.gate(r, "rid", "J", None, "2010", G.PROHIBITED, None, "W-1"), G.gate(r, "rid", "J", "2010", None, G.OPEN, None, "W-3")]
    check(G.reading_at(rows, "rid", "J", "2009")[0] == G.PROHIBITED and G.reading_at(rows, "rid", "J", "2010")[0] == G.OPEN, "reading_at picks the in-force row")
    check(G.reading_at(rows, "rid", "K", "2010")[0] == "NO_ROW", "no row in that jurisdiction")
    check(G.reading_at([nt], "rid", "J", "2026")[0] == G.UNKNOWN_STATE, "a no-t row reads UNKNOWN at every t (3a)")
    gap = [G.gate(r, "rid", "J", None, "2010", G.PROHIBITED, None, "W-1"), G.gate(r, "rid", "J", "2012", None, G.OPEN, None, "W-3")]
    check(G.reading_at(gap, "rid", "J", "2011")[0] == "NO_ROW_AT_T", "a gap between rows is NO_ROW_AT_T, not a state")
    dup = rows + [G.gate(r, "rid", "J", "2000", None, G.PROHIBITED, None, "W-1")]
    check(G.reading_at(dup, "rid", "J", "2011")[0] == "CONFLICT", "two rows in force at once is CONFLICT")


# ----------------------------------------------------------------- events ---

def t_events():
    e = G.event("rid", "J", "1788", "case", G.OPEN, G.DISCRETIONARY, "G-2")
    check(e["direction"] == "CLOSURE" and e["grade"] == "P/S" and e["hold_eligible"] and not e["flagged"], "OPEN -> DISCRETIONARY is a CLOSURE, hold-eligible at P/S")
    k = G.event("rid", "J", None, "x", G.UNKNOWN_STATE, G.OPEN, "G-3")
    check(k["flagged"] and k["undated"] and not k["hold_eligible"] and k["direction"] == "UNKNOWN_DIRECTION", "a K, undated event is flagged and excluded")
    refuses(lambda: G.event("rid", "J", "1788", "x", G.OPEN, G.OPEN, "G-2"), G.GateError, "equal", "from == to is not a change")
    refuses(lambda: G.event("rid", "J", "1788", "x", G.OPEN, G.PROHIBITED, "nope"), G.GateError, "section-2 id", "an unlisted event source is refused")
    refuses(lambda: G.event("", "J", "1788", "x", G.OPEN, G.PROHIBITED, "G-2"), G.GateError, "route_id", "route_id is required on an event")
    refuses(lambda: G.event("rid", "J", "1788", "x", "SHUT", G.PROHIBITED, "G-2"), G.GateError, "from_state", "an off-enum state is refused")
    check(G.direction(G.PROHIBITED, G.DISCRETIONARY) == "LATERAL" and G.direction(G.DISCRETIONARY, G.PROHIBITED) == "LATERAL",
          "PROHIBITED <-> DISCRETIONARY is LATERAL: not ordered [CHOICE 3]")
    check(G.direction(G.PROHIBITED, G.METERED_PERMISSION) == "LOOSENING" and G.direction(G.METERED_PERMISSION, G.PROHIBITED) == "CLOSURE",
          "the transition table is its own reverse")
    check(G.direction(G.OPEN, G.UNKNOWN_STATE) == "UNKNOWN_DIRECTION", "an UNKNOWN end is UNKNOWN_DIRECTION")
    ev = G.events_declared()
    check(len(ev) == 3 and sum(1 for x in ev if x["hold_eligible"]) == 2, "three declared events, two hold-eligible")
    tl = G.tally_events(ev)
    check(tl["CLOSURE"] == 1 and tl["LOOSENING"] == 1 and tl["excluded_k"] == 1 and "net" not in tl, "tally counts apart; no net key")
    ue = G.event("rid", "J", "2001", "x", G.OPEN, G.PROHIBITED, G.CONSTRUCTED_UNSOURCED)
    check(G.tally_events([ue])["excluded_unsourced"] == 1 and not ue["hold_eligible"], "an unsourced event is counted apart")
    rec = G.events_reconcile(ev, G.events_derived(G.fixture_rows()))
    check(len(rec["derived_declared"]) == 2 and not rec["derived_undeclared"] and not rec["declared_underived"],
          "the two derived boundary events match the declared table; the K event, undated, is outside the comparison")
    # E-A2-2 arithmetic
    rows = G.fixture_rows()
    check(G.route_count(rows, "England", "1700") == 1 and G.route_count(rows, "England", "2026") == 1, "route count does not move across 1788")
    check(G.tally_events(ev, jurisdiction="England")["CLOSURE"] == 1, "the removal count finds it")
    check(G.route_count(rows, "Atlantis", "2026") == 0, "an unlisted jurisdiction counts zero routes")


# --------------------------------------------------------------- section 3c ---

def t_none():
    r = S.migrate(_row())
    n = G.declare_none(r, "the route's own name states the absence")
    check(n["obligation_origin"] == G.NONE_ORIGIN and S.scorable(n) and S.split_of(n) == "NEITHER", "NONE is scorable under A-1 and splits NEITHER")
    check(r["obligation_origin"] == S.UNDECIDED, "declare_none copies")
    refuses(lambda: G.declare_none(r, ""), G.GateError, "grounds", "NONE without grounds is refused")
    refuses(lambda: G.declare_none(S.declare(_row(), S.CONSTRUCTED, True, False, "b"), "g"), G.GateError, "only an UNDECIDED row",
            "a decided row does not move to NONE")
    refuses(lambda: G.declare_none(_row(), "g"), G.GateError, "not been migrated", "an unmigrated row is refused")
    rr = G.reread_undecided()
    check(rr["undecided_before"] == 10, "ten UNDECIDED rows, the RIN_061 count")
    check(len(rr["moved_to_none"]) == 8 and len(rr["stayed_undecided"]) == 2, "eight move to NONE on stated grounds, two stay [CHOICE 7]")
    stayed = sorted(k[2] for k in rr["stayed_undecided"])
    check(stayed == ["notebook, unshared; whether it is ever disseminated is undeclared", "public chain"], "the two that stay are the undeclared-medium rows")
    for c in rr["cases"]:
        for _, x in S.routes_of(c):
            check(x["origin_basis"], "every re-read row carries grounds (%s)" % x["route"][:20])
    # a case with an UNDECIDED row the grounds table does not name is refused, never defaulted
    src = "CONSTRUCTED: test"
    res = D.result("zz", [D.dependency("labor", [D.route("moonlight labor", D.NONE_MEDIUM, D.NONE_MEDIUM, src)])], src)
    mig = S.apply_table(res, {("labor", "moonlight labor"): (S.UNDECIDED, None, None, "x")}, S.declare, "origin declaration")
    refuses(lambda: G.reread_undecided([mig]), G.GateError, "no 3c grounds", "an unnamed UNDECIDED row is refused")


# --------------------------------------------------------------- fixtures ---

def t_fixtures():
    w1, w2, w3, w4, g1, g2 = G.fixture_rows()
    check(G.gate_reading(w1) == G.PROHIBITED and G.gate_reading(w2) == G.METERED_PERMISSION, "F-W1 PROHIBITED, F-W2 METERED_PERMISSION")
    check(w1["t_to"] == w2["t_from"] == G.HB_16_1005_EFFECTIVE == "2016-08-10", "the boundary is the carried effective date")
    check(G.gate_reading(w3) == G.UNKNOWN_STATE and w3["gate_state"] == G.PROHIBITED, "F-W3 declared PROHIBITED reads UNKNOWN: W-2 carries no date [CHOICE 5]")
    check(G.gate_reading(w4) == G.OPEN and G.gate_reading(G.fixture_f_w4(strict=True)) == G.UNKNOWN_STATE, "F-W4 OPEN at year precision, UNKNOWN under the strict reading [CHOICE 6]")
    check(G.gate_reading(g1) == G.OPEN and G.gate_reading(g2) == G.DISCRETIONARY, "F-G1 OPEN, F-G2 DISCRETIONARY")
    check(all(r["source"].startswith("CARRIED") for r in G.fixture_rows()), "every fixture row declares itself CARRIED")
    check(all(r["hold_eligible"] for r in G.fixture_rows()), "every delivered fixture row is hold-eligible (S or P)")
    check(all(r["obligation_origin"] == S.BIOLOGICAL for r in G.fixture_rows()), "the rows carry A-1's BIOLOGICAL origin; the gate is on the A-2 fields")
    a3 = G.fixture_f_a3_retired()
    check(a3["gate_tag"] == G.CONSTRUCTED_UNSOURCED and a3["retired"] and not a3["hold_eligible"] and G.gate_reading(a3) == G.UNKNOWN_STATE,
          "F-A3 kept, tagged, excluded, reads UNKNOWN")
    check(a3["route"] == S.fixture_f_a3()["route"], "the retired row is A-1's own row, not a rewrite")
    check("VERIFIED" not in G.HB_16_1005_VERIFICATION and G.HB_16_1005_VERIFICATION.startswith("NOT_RUN"), "the effective-date verification is recorded NOT_RUN")
    check(G.SOURCES["G-2"]["conflict"]["resolved"] is False and G.SOURCES["G-2"]["conflict"]["carried"] == "Court of Common Pleas",
          "the G-2 court conflict is carried open, Common Pleas carried [CHOICE 4]")
    check(G.hold_grade("G-2") == "S" and G.hold_grade("G-1") == "P" and G.hold_grade("G-3") is None and G.hold_grade("nope") is None,
          "hold grades: P/S -> S, K -> None")
    check(G.weakest(["P", "S"]) == "S" and G.weakest(["P"]) == "P" and G.weakest([]) is None, "weakest grade")
    check(len(G.NOT_SOURCED) == 3, "three not-sourced items carried, no fixture for any")


# ------------------------------------------------------------- expectations ---

def t_expectations():
    exp = G.check_expectations()
    by = dict((l, (v, h)) for l, v, h, _ in exp)
    check(len(exp) == 5, "five expectation rows (E-A2-1 in two readings)")
    lit = [v for l, (v, h) in by.items() if l.startswith("E-A2-1 (literal)")][0]
    check(lit == "MISMATCH", "E-A2-1 literal ('gate_state ALONE') is the recorded MISMATCH")
    rd = [(v, h) for l, (v, h) in by.items() if l.startswith("E-A2-1 (reading)")][0]
    check(rd == ("MATCH", "HELD(S)"), "E-A2-1 on the reading MATCH, HELD(S)")
    for pre in ("E-A2-2", "E-A2-3", "E-A2-4"):
        vh = [(v, h) for l, (v, h) in by.items() if l.startswith(pre)][0]
        check(vh == ("MATCH", "HELD(S)"), "%s MATCH, HELD(S) (got %s)" % (pre, vh))
    check(not any(h.startswith("HELD(P)") for _, (_, h) in by.items()), "no hold reads HELD(P): every prediction rests on at least one S source")
    # E-A2-3 per jurisdiction
    pj = G.per_jurisdiction(G.fixture_rows(), "2026")
    w = pj["water"]["routes"]["rainwater_rooftop"]
    check(w["readings"] == {"Colorado": G.METERED_PERMISSION, "Texas": G.OPEN, "Utah": G.UNKNOWN_STATE} and w["verdict"] == "OPEN_IN_SOME",
          "rainwater per jurisdiction at 2026: CO metered, TX open, UT unknown")
    check(pj["food"]["routes"]["gleaning"]["verdict"] == "OPEN_IN_NONE", "gleaning England 2026: not open")
    check(pj["shelter"]["verdict"] == "NOT_EVALUABLE", "shelter has no sourced row: NOT_EVALUABLE, not a pass")
    check(G.per_jurisdiction(G.fixture_rows(True), "2026")["water"]["routes"]["rainwater_rooftop"]["verdict"] == "OPEN_IN_NONE",
          "under the strict F-W4 reading rainwater is OPEN nowhere at 2026 from section 2 alone")
    check(G.per_jurisdiction(G.fixture_rows(), "1700")["food"]["routes"]["gleaning"]["verdict"] == "OPEN_IN_ALL",
          "the same route at t=1700 reads OPEN_IN_ALL: the reading is (jurisdiction, t)-indexed, not existence-in-any-regime")
    check(G.hold(True, [], False).startswith("NOT_EVALUABLE") and G.hold(False, ["S"], True) == "FAILED" and G.hold(True, ["P"], True) == "HELD(P)",
          "hold vocabulary: NOT_EVALUABLE / FAILED / HELD(grade)")


def t_fail_fixture():
    global FAIL_FIXTURE
    ff = G.fail_fixture()
    check(ff["unamended_identical"], "F-W1 vs F-W2 through FWO-5 + A-1: one identical record (the amendment's fail fixture)")
    a, b = ff["unamended_pair"]
    check("gate_state" not in a and S.unamended_reading(a)["status"] == "INDEPENDENT", "the unamended record has no gate field and reads INDEPENDENT")
    pj = G.per_jurisdiction(ff["all_open_rows"], "2026")
    r = pj["water"]["routes"]["rainwater_rooftop"]
    check(r["verdict"] == "OPEN_IN_ALL" and not r["hold_eligible"], "the constructed all-OPEN set trips the falsifier and is hold-ineligible")
    check(G.open_in_every_sourced(pj, include_ineligible=True) == [("water", "rainwater_rooftop")] and G.open_in_every_sourced(pj) == [],
          "the falsifier fires on it and enters no hold")
    check(all(x["gate_tag"] == G.CONSTRUCTED_UNSOURCED for x in ff["all_open_rows"]), "every constructed row is tagged")
    FAIL_FIXTURE = ff["unamended_identical"] and r["verdict"] == "OPEN_IN_ALL"


def t_hygiene():
    r = render()
    check(r == render(), "render deterministic")
    lines = [l for l in r.splitlines() if l.startswith("expected ")]
    check(lines and lines[0].startswith("expected MISMATCH"), "failed predictions print first (rule 4)")
    ns = screen()
    if ns is not None:
        ok, h = ns.check(r)
        check(ok, "render screens clean with no exemption (%s)" % [x[1] for x in h][:5])
        check(not ns.check(r + "\nthis cell is wrong\n")[0], "a planted word is caught")
    p = subprocess.run([sys.executable, SRC, "--selftest"], capture_output=True)
    check(p.returncode == 2, "refuses --selftest with exit 2")
    p = subprocess.run([sys.executable, SRC, "--choices"], capture_output=True, text=True)
    check(p.returncode == 0 and p.stdout.count("[CHOICE") == len(G.CHOICES), "--choices prints every choice")
    for k in G.CHOICES:
        check(("[CHOICE %d]" % k) in SRC_TEXT.split('"""', 2)[2], "[CHOICE %d] is cited outside its declaration" % k)
    p = subprocess.run([sys.executable, SRC], capture_output=True)
    check(p.returncode == 0, "runs with exit 0")
    src = open(SRC, "rb").read()
    check(all(b < 128 for b in src), "ASCII")
    ast.parse(src.decode("ascii"), feature_version=(3, 8))
    check(True, "parses under 3.8")
    amd = "AMENDMENT_A2_2026-09-28_gate-state.md"
    check(os.path.exists(os.path.join(HERE, amd)), "the amendment is present verbatim")
    log = subprocess.run(["git", "log", "--format=%h", "-n", "1", "--", amd], cwd=HERE, capture_output=True, text=True).stdout.strip()
    if log:
        check(log == G.EXPECTED_COMMIT_A2, "the amendment's last commit is the registered EXPECTED commit (%s)" % log)
    sample = os.path.join(HERE, "samples", "gate_state.sample.txt")
    if os.path.exists(sample):
        check(open(sample, encoding="utf-8").read() == r, "sample matches a fresh render")
    p = subprocess.run([sys.executable, os.path.join(HERE, "test_settlement_split.py")], capture_output=True)
    check(p.returncode == 0, "test_settlement_split.py still green")


for fn in (t_structure, t_dates, t_rows, t_events, t_none, t_fixtures, t_expectations, t_fail_fixture, t_hygiene):
    fn()

tag = "" if FAIL_FIXTURE else "  NO_FAIL_FIXTURE: gate_state"
print("gate-state: %d checks, %d failed; fail fixture present on 1 of 1 instruments%s" % (_checks, _failed, tag)
      if FAIL_FIXTURE else "gate-state: %d checks, %d failed%s" % (_checks, _failed, tag))
sys.exit(1 if _failed else 0)
