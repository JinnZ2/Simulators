# SPDX-License-Identifier: CC0-1.0
"""Checks for AMENDMENT A-2.1 (gate_state_a21.py).

Run:  python3 route-independence/test_gate_state_a21.py
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
import gate_state_a21 as A           # noqa: E402

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
    A.render(buf)
    return buf.getvalue()


def defined_names(path):
    tree = ast.parse(open(path, encoding="utf-8").read())
    return set(n.name for n in tree.body if isinstance(n, (ast.FunctionDef, ast.ClassDef))) | \
        set(t.id for n in tree.body if isinstance(n, ast.Assign) for t in n.targets if isinstance(t, ast.Name))


SRC = os.path.join(HERE, "gate_state_a21.py")
CONV = {"HERE", "CHOICES", "render", "main", "check_expectations", "fail_fixture", "fixture_rows", "events_declared"}   # per-module conventions
SRC_TEXT = open(SRC, encoding="utf-8").read()
TREE = ast.parse(SRC_TEXT)


# ---------------------------------------------------------------- structure ---

def t_structure():
    for other in ("dependency_chain_audit.py", "edge_taxonomy.py", "settlement_split.py", "gate_state.py"):
        clash = (defined_names(os.path.join(HERE, other)) & defined_names(SRC)) - CONV
        check(not clash, "gate_state_a21 redefines no name of %s (clash %s)" % (other, sorted(clash)))
    check(A.EXPECTED_COMMIT_A21 not in (G.EXPECTED_COMMIT_A2, S.EXPECTED_COMMIT), "A-2.1 registers its own EXPECTED commit")
    # no parser of its own: every row goes through G.gate, every event through G.event
    calls = [n.func.attr for n in ast.walk(TREE) if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
             and isinstance(n.func.value, ast.Name) and n.func.value.id == "G"]
    check("gate" in calls and "event" in calls and "per_jurisdiction" in calls and "check_expectations" in calls,
          "rows, events, readings and A-2's expectations all go through gate_state")
    # section 3: PROPOSED fields are not built
    for key in ("access_is_right", "revocable_by"):
        check(all(key not in r for r in A.fixture_rows()), "no row carries the proposed field %s" % key)
        refs = [n for n in ast.walk(TREE) if isinstance(n, ast.Subscript) and isinstance(n.slice, ast.Constant) and n.slice.value == key]
        check(not refs, "no subscript reads the proposed field %s" % key)
    check(A.PROPOSED["status"] == "NOT_BUILT" and "question" in A.PROPOSED, "PROPOSED carries status NOT_BUILT and the amendment's question")
    # E-A2-4's scan holds on this module too
    bad = []
    for node in ast.walk(TREE):
        if isinstance(node, (ast.BoolOp, ast.Compare, ast.BinOp, ast.IfExp)):
            if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Mod) and isinstance(node.left, ast.Constant):
                continue
            names = set()
            for sub in ast.walk(node):
                if isinstance(sub, ast.Constant) and isinstance(sub.value, str):
                    names.add(sub.value)
                if isinstance(sub, (ast.Name,)):
                    names.add(sub.id)
                if isinstance(sub, ast.Attribute):
                    names.add(sub.attr)
            if "DISCRETIONARY" in names and ({"OPEN", "OPEN_STATES", "INDEPENDENT", "is_open"} & names):
                bad.append(ast.dump(node)[:60])
    check(not bad, "E-A2-4 scan holds on gate_state_a21 (%s)" % bad[:2])


# ---------------------------------------------------------------- sources ---

def t_sources():
    check(set(G.SOURCES) <= set(A.SOURCES21), "A-2.1's table contains A-2's [CHOICE 9]")
    for sid in G.SOURCES:
        check(A.SOURCES21[sid] == G.SOURCES[sid], "A-2 id %s keeps its A-2 entry" % sid)
    check(A.SOURCES21["W-1a"]["grade"] == "P" and A.SOURCES21["W-1a"]["upgrades"] == "W-1", "W-1a is P and upgrades W-1")
    check(A.SOURCES21["W-2a"]["grade"] == "P" and A.SOURCES21["W-2a"]["precision"] == "year", "W-2a is P at year precision")
    check(G.hold_grade("W-1a", A.SOURCES21) == "P" and G.hold_grade("W-1a") is None, "the upgraded id is P in A-2.1's table and unknown to A-2's")
    for sid in ("UT-73-2-27", "UT-73-1-1"):
        check(A.SOURCES21[sid]["input"] is False and A.SOURCES21[sid]["grade"] == "S", "%s recorded at S, not adopted as input" % sid)
        r = D.route("x", D.NONE_MEDIUM, D.NONE_MEDIUM, "CONSTRUCTED: test")
        refuses(lambda: G.gate(r, "rid", "Utah", "2010", None, G.PROHIBITED, None, sid, sources=A.SOURCES21),
                G.GateError, "NOT adopted as input", "a row citing %s is refused" % sid)
    check(A.HB_16_1005_VERIFICATION_A21.startswith("RESOLVED") and "CARRIED here" in A.HB_16_1005_VERIFICATION_A21,
          "the effective-date verification is RESOLVED by the author and CARRIED here")
    check(G.HB_16_1005_VERIFICATION.startswith("NOT_RUN"), "A-2's own record of NOT_RUN is untouched")


# ---------------------------------------------------------------- fixtures ---

def t_fixtures():
    rows = A.fixture_rows()
    check(len(rows) == 9, "nine rows: seven corrected water rows and A-2's two gleaning rows")
    by = dict((r["gate_note"].split(";")[0][:5], r) for r in rows)
    check(G.gate_reading(by["F-W1a"]) == G.PROHIBITED and by["F-W1a"]["gate_grade"] == "S"
          and "prior appropriation" in by["F-W1a"]["gate_instrument"], "F-W1a PROHIBITED on the doctrine at S")
    check(G.gate_reading(by["F-W1b"]) == G.UNKNOWN_STATE and not by["F-W1b"]["hold_eligible"] and by["F-W1b"]["gate_source"] is None,
          "F-W1b UNKNOWN, unsourced, not hold-eligible [CHOICE 11]")
    check(by["F-W1a"]["t_to"] == by["F-W1b"]["t_from"] == "2009" and by["F-W1b"]["t_to"] == by["F-W2"]["t_from"] == G.HB_16_1005_EFFECTIVE,
          "the Colorado intervals meet at 2009 and at the effective date")
    check(by["F-W2"]["gate_source"] == "W-1a" and by["F-W2"]["gate_grade"] == "P", "F-W2 now rests on W-1a at P")
    check(by["F-W3a"]["condition"] and by["F-W3b"]["condition"] and by["F-W3a"]["condition"] != by["F-W3b"]["condition"],
          "the two Utah rows carry distinct conditions [CHOICE 10]")
    check(by["F-W3a"]["t_from"] == by["F-W3b"]["t_from"] == "2010" and by["F-W3c"]["t_to"] == "2010", "Utah at year precision")
    check(G.gate_reading(by["F-W4"]) == G.UNKNOWN_STATE and by["F-W4"]["t_from"] is None, "F-W4 UNKNOWN with no t: the year-precision reading is superseded")
    check(G.gate_reading(G.fixture_f_w4()) == G.OPEN, "A-2's own F-W4 still reads OPEN in A-2; superseded, not edited")
    check(all(r["source"].startswith("CARRIED") for r in rows), "every row declares itself CARRIED")
    # readings
    st, payload = G.reading_at(rows, "rainwater_rooftop", "Utah", "2026")
    check(st == "BY_CONDITION" and set(payload.values()) == {G.METERED_PERMISSION, G.PROHIBITED}, "Utah at 2026 reads BY_CONDITION")
    check(G.reading_at(rows, "rainwater_rooftop", "Utah", "2005")[0] == G.UNKNOWN_STATE, "Utah before 2010 reads UNKNOWN (F-W3c)")
    check(G.reading_at(rows, "rainwater_rooftop", "Colorado", "2012")[0] == G.UNKNOWN_STATE, "Colorado 2009..2016 reads UNKNOWN (F-W1b)")
    check(G.reading_at(rows, "rainwater_rooftop", "Colorado", "2000")[0] == G.PROHIBITED, "Colorado before 2009 reads PROHIBITED")
    check(G.reading_at(rows, "rainwater_rooftop", "Texas", "2026")[0] == G.UNKNOWN_STATE, "Texas reads UNKNOWN")
    # BY_CONDITION is not open unless every condition is open; CONFLICT without conditions
    r = D.route("x", D.NONE_MEDIUM, D.NONE_MEDIUM, "CONSTRUCTED: test")
    two_open = [G.gate(r, "q", "J", "2000", None, G.OPEN, None, "W-3", condition="a"), G.gate(r, "q", "J", "2000", None, G.OPEN, None, "W-3", condition="b")]
    check(G._reading_open(G.reading_at(two_open, "q", "J", "2026")[1]), "two OPEN conditions read open")
    check(not G._reading_open(payload), "one OPEN-less condition set does not read open")
    dup = [G.gate(r, "q", "J", "2000", None, G.OPEN, None, "W-3", condition="a")] * 2
    check(G.reading_at(dup, "q", "J", "2026")[0] == "CONFLICT", "two rows under one condition is CONFLICT")
    refuses(lambda: G.gate(r, "q", "J", "2000", None, G.OPEN, None, "W-3", condition=" "), G.GateError, "condition", "a blank condition is refused")


def t_events():
    ev = A.events_declared()
    co = [e for e in ev if e["jurisdiction"] == "Colorado"]
    check(len(co) == 1 and co[0]["from_state"] == G.UNKNOWN_STATE and co[0]["direction"] == "UNKNOWN_DIRECTION" and co[0]["grade"] == "P",
          "the Colorado event now runs from UNKNOWN at P: its direction is unknown until the 2009 bill is sourced")
    ut = [e for e in ev if e["jurisdiction"] == "Utah"]
    check(len(ut) == 1 and ut[0]["date"] == "2010" and ut[0]["hold_eligible"], "one Utah event at 2010, hold-eligible")
    rec = G.events_reconcile(ev, G.events_derived(A.fixture_rows()))
    check(len(rec["derived_declared"]) == 3 and not rec["declared_underived"], "three derived boundaries have declared rows")
    check(rec["derived_undeclared"] == [("rainwater_rooftop", "Colorado", "2009", G.PROHIBITED, G.UNKNOWN_STATE)],
          "the one undeclared derived boundary is the unsourced 2009 bill")
    tl = G.tally_events(ev, jurisdiction="Colorado")
    check(tl["LOOSENING"] == 0 and tl["UNKNOWN_DIRECTION"] == 1, "A-2's Colorado LOOSENING is gone; the count reads UNKNOWN_DIRECTION")
    check(G.tally_events(G.events_declared(), jurisdiction="Colorado")["LOOSENING"] == 1, "A-2's own event table is untouched")


# ------------------------------------------------------------- expectations ---

def t_expectations():
    exp = A.check_expectations()
    by = dict((l.split(" ")[0], (v, h)) for l, v, h, _ in exp)
    check(by["E-A2.1-1"] == ("MATCH", "HELD(P)"), "E-A2.1-1 MATCH, HELD(P) (got %s)" % (by["E-A2.1-1"],))
    check(by["E-A2.1-2"] == ("MATCH", "HELD(S)"), "E-A2.1-2 MATCH, HELD(S): it rests on E-A2-3, which carries the gleaning row's S")
    pj = G.per_jurisdiction(A.fixture_rows(), "2026")
    r = pj["water"]["routes"]["rainwater_rooftop"]
    check(r["open_status"] == "UNMEASURED_OPEN" and r["verdict"] == "OPEN_IN_NONE", "rainwater is UNMEASURED_OPEN, not a closure [CHOICE 12]")
    check(pj["food"]["routes"]["gleaning"]["open_status"] == "OPEN_IN_NONE_MEASURED", "gleaning, every jurisdiction known, reads OPEN_IN_NONE_MEASURED")
    check(r["grade_by_jurisdiction"] == {"Colorado": "P", "Texas": None, "Utah": "P"}, "grades per jurisdiction at 2026 [CHOICE 13]")
    before = G.per_jurisdiction(G.fixture_rows(), "2026")["water"]["routes"]["rainwater_rooftop"]["grade_by_jurisdiction"]
    check(before == {"Colorado": "S", "Texas": "S", "Utah": None}, "A-2's grades re-scored the same way: Utah had NO in-force row, so the 'S -> P' is None -> P there")
    # A-2's four over the corrected rows
    a21 = dict((l.split(" ")[0] + ("L" if "(literal)" in l else ""), (v, h))
               for l, v, h, _ in G.check_expectations(rows_in=A.fixture_rows(), pair=(A.fixture_f_w1a(), A.fixture_f_w2_p())))
    check(a21["E-A2-1L"][0] == "MISMATCH" and a21["E-A2-1"] == ("MATCH", "HELD(S)"), "E-A2-1 over F-W1a/F-W2: literal MISMATCH, reading MATCH at S (the doctrine row is S)")
    for k in ("E-A2-2", "E-A2-3", "E-A2-4"):
        check(a21[k] == ("MATCH", "HELD(S)"), "%s holds over the corrected rows" % k)
    a, b = G.ungated(A.fixture_f_w1a()), G.ungated(A.fixture_f_w2_p())
    check(a != b and S.unamended_reading(a) == S.unamended_reading(b), "F-W1a and F-W2 differ as whole records (source) and agree on every FWO-5-derived field")
    check(G.ungated(G.fixture_f_w1()) == G.ungated(G.fixture_f_w2()), "A-2's pair is still identical as whole records")
    # E-A2-3's falsifier is still reachable on the corrected table
    src = "CONSTRUCTED: test"
    rr = D.route(G._RAIN, D.NONE_MEDIUM, D.NONE_MEDIUM, src)
    allopen = [G.gate(rr, "rainwater_rooftop", j, "2000", None, G.OPEN, None, None, requirement="water", tag=G.CONSTRUCTED_UNSOURCED)
               for j in ("Colorado", "Utah", "Texas")]
    check(G.open_in_every_sourced(G.per_jurisdiction(allopen, "2026"), include_ineligible=True), "the falsifier still fires on a constructed all-OPEN set")


def t_fail_fixture():
    global FAIL_FIXTURE
    ff = A.fail_fixture()
    check(ff["as_written_reads"] == G.UNKNOWN_STATE, "A-2's F-W3 as written reads UNKNOWN")
    check(ff["as_written_dated_beside_corrected"] == "CONFLICT", "dated and undivided beside the corrected rows it reads CONFLICT")
    check(ff["corrected"][0] == "BY_CONDITION", "the corrected pair alone reads BY_CONDITION")
    FAIL_FIXTURE = ff["as_written_dated_beside_corrected"] == "CONFLICT" and ff["corrected"][0] == "BY_CONDITION"


def t_hygiene():
    r = render()
    check(r == render(), "render deterministic")
    lines = [l for l in r.splitlines() if l.startswith("expected ")]
    check(lines and all(l.startswith("expected MATCH") for l in lines), "both A-2.1 rows MATCH; nothing to print first")
    ns = screen()
    if ns is not None:
        ok, h = ns.check(r)
        check(ok, "render screens clean with no exemption (%s)" % [x[1] for x in h][:5])
        check(not ns.check(r + "\nthis cell is wrong\n")[0], "a planted word is caught")
    p = subprocess.run([sys.executable, SRC, "--selftest"], capture_output=True)
    check(p.returncode == 2, "refuses --selftest with exit 2")
    p = subprocess.run([sys.executable, SRC, "--choices"], capture_output=True, text=True)
    check(p.returncode == 0 and p.stdout.count("[CHOICE") == len(A.CHOICES), "--choices prints every choice")
    check(sorted(A.CHOICES) == [9, 10, 11, 12, 13], "choices numbered on from A-2's 1..8")
    for k in A.CHOICES:
        check(("[CHOICE %d]" % k) in SRC_TEXT.split('"""', 2)[2], "[CHOICE %d] is cited outside its declaration" % k)
    p = subprocess.run([sys.executable, SRC], capture_output=True)
    check(p.returncode == 0, "runs with exit 0")
    src = open(SRC, "rb").read()
    check(all(b < 128 for b in src), "ASCII")
    ast.parse(src.decode("ascii"), feature_version=(3, 8))
    check(True, "parses under 3.8")
    amd = "AMENDMENT_A2.1_2026-09-28_source-upgrades.md"
    check(os.path.exists(os.path.join(HERE, amd)), "the amendment is present verbatim")
    log = subprocess.run(["git", "log", "--format=%h", "-n", "1", "--", amd], cwd=HERE, capture_output=True, text=True).stdout.strip()
    if log:
        check(log == A.EXPECTED_COMMIT_A21, "the amendment's last commit is the registered EXPECTED commit (%s)" % log)
    sample = os.path.join(HERE, "samples", "gate_state_a21.sample.txt")
    if os.path.exists(sample):
        check(open(sample, encoding="utf-8").read() == r, "sample matches a fresh render")
    p = subprocess.run([sys.executable, os.path.join(HERE, "test_gate_state.py")], capture_output=True)
    check(p.returncode == 0, "test_gate_state.py still green")


for fn in (t_structure, t_sources, t_fixtures, t_events, t_expectations, t_fail_fixture, t_hygiene):
    fn()

tag = "" if FAIL_FIXTURE else "  NO_FAIL_FIXTURE: gate_state_a21"
print("gate-state-a21: %d checks, %d failed; fail fixture present on 1 of 1 instruments%s" % (_checks, _failed, tag)
      if FAIL_FIXTURE else "gate-state-a21: %d checks, %d failed%s" % (_checks, _failed, tag))
sys.exit(1 if _failed else 0)
