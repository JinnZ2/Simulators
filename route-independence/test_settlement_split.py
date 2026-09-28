# SPDX-License-Identifier: CC0-1.0
"""Checks for AMENDMENT A-1 (settlement_split.py).

Run:  python3 route-independence/test_settlement_split.py
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
    S.render(buf)
    return buf.getvalue()


def defined_names(path):
    tree = ast.parse(open(path, encoding="utf-8").read())
    return set(n.name for n in tree.body if isinstance(n, (ast.FunctionDef, ast.ClassDef))) | \
        set(t.id for n in tree.body if isinstance(n, ast.Assign) for t in n.targets if isinstance(t, ast.Name))


SRC = os.path.join(HERE, "settlement_split.py")
CONV = {"HERE", "CHOICES", "render", "main", "check_expectations", "routes_of", "fail_fixture"}   # per-module conventions


# ---------------------------------------------------------------- structure ---

def t_structure():
    for other in ("dependency_chain_audit.py", "edge_taxonomy.py"):
        clash = (defined_names(os.path.join(HERE, other)) & defined_names(SRC)) - CONV
        check(not clash, "settlement_split redefines no name of %s (clash %s)" % (other, sorted(clash)))
    # the split is never merged: no expression names both halves
    tree = ast.parse(open(SRC, encoding="utf-8").read())
    merged = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.BinOp, ast.BoolOp, ast.Compare, ast.Call)):
            if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Mod) and isinstance(node.left, ast.Constant):
                continue   # a format string printing the two side by side is not a merge (IRB_018: % is BinOp)
            names = set()
            for sub in ast.walk(node):
                if isinstance(sub, ast.Constant) and isinstance(sub.value, str):
                    names.add(sub.value)
                if isinstance(sub, ast.Name):
                    names.add(sub.id)
            if {"settles_claim", "removes_gate"} <= names and not isinstance(node, ast.Call):
                merged.append(ast.dump(node)[:60])
    check(not merged, "no BinOp/BoolOp/Compare reads settles_claim and removes_gate together (%s)" % merged[:2])
    # no arithmetic on a status
    touched = [ast.dump(sub)[:40] for node in ast.walk(tree) if isinstance(node, ast.BinOp)
               and not (isinstance(node.op, ast.Mod) and isinstance(node.left, ast.Constant))
               for sub in ast.walk(node)
               if isinstance(sub, ast.Attribute) and sub.attr in ("INDEPENDENT", "CONVERTED", "UNKNOWN")]
    check(not touched, "no arithmetic touches a status (%s)" % touched[:2])


# ------------------------------------------------------------------ fields ---

def t_fields():
    src = "CONSTRUCTED: test"
    r = D.route("x", D.DOMINANT, D.DOMINANT, src, conversion_point="settlement")
    m = S.migrate(r)
    check(m["obligation_origin"] == S.UNDECIDED and m["settles_claim"] is None and m["removes_gate"] is None,
          "migration lands UNDECIDED with the split undeclared")
    check(not S.scorable(m), "a migrated row is not scorable")
    check(r.get("obligation_origin") is None, "migration copies; the FWO-5 record is unchanged")
    refuses(lambda: S.scorable(r), S.SplitError, "not been migrated", "scorable refuses an unmigrated route")
    refuses(lambda: S.declare(r, "NATURAL", True, False, "b"), S.SplitError, "obligation_origin", "an origin outside the three is refused")
    refuses(lambda: S.declare(r, S.CONSTRUCTED, True, False, ""), S.SplitError, "origin_basis", "a declaration without basis is refused")
    refuses(lambda: S.declare(r, S.CONSTRUCTED, "yes", False, "b"), S.SplitError, "settles_claim", "a non-tri value is refused")
    refuses(lambda: S.declare(r, S.UNDECIDED, True, None, "b"), S.SplitError, "UNDECIDED carries no split",
            "UNDECIDED cannot carry a split declaration")
    d = S.declare(r, S.CONSTRUCTED, True, False, "a fine")
    check(S.scorable(d) and S.split_of(d) == "CLAIM_ONLY", "a declared row scores; a fine is CLAIM_ONLY")
    check(S.split_of(S.declare(r, S.BIOLOGICAL, False, True, "b")) == "GATE_ONLY", "gate only")
    check(S.split_of(S.declare(r, S.CONSTRUCTED, True, True, "b")) == "BOTH", "both")
    check(S.split_of(S.declare(r, S.BIOLOGICAL, False, False, "b")) == "NEITHER", "neither")
    check(S.split_of(S.declare(r, S.CONSTRUCTED, True, None, "b")) == "UNDECLARED_HALF", "an undeclared half is its own label, not a False")
    check(S.split_of(S.declare(r, S.UNDECIDED, None, None, "b")) == "UNDECIDED", "explicit UNDECIDED with a reason")
    fl = S.declare(r, S.BIOLOGICAL, True, False, "the reading the amendment calls unsupported")
    check(fl["reads_requirement_as_claim"] is True, "BIOLOGICAL + settles_claim is admitted and flagged")
    check(S.declare(r, S.BIOLOGICAL, False, True, "b")["reads_requirement_as_claim"] is False, "the flag is off on GATE_ONLY")
    check(S.declare(r, S.UNDECIDED, None, None, "b")["reads_requirement_as_claim"] is False, "flag is not raised on UNDECIDED")


def t_tokens():
    src = "CONSTRUCTED: test"
    r = D.route("open dataset", "citation", "citation", src)
    refuses(lambda: S.token(r, "GOLD", None, 1, "b"), S.SplitError, "token_type", "an unlisted token type is refused")
    refuses(lambda: S.token(r, "CITATION", None, 0, "b"), S.SplitError, "int >= 1 or UNMEASURED", "hops 0 on a non-monetary token is refused")
    refuses(lambda: S.token(r, "CITATION", None, True, "b"), S.SplitError, "int >= 1", "a bool is not an int here")
    refuses(lambda: S.token(r, "CITATION", "CREDENTIAL", S.UNMEASURED, "b"), S.SplitError, "contradictory",
            "an observed converts_to with UNMEASURED hops is refused")
    refuses(lambda: S.token(r, "NONE", None, 1, "b"), S.SplitError, "NONE carries hops None", "token NONE with hops is refused")
    refuses(lambda: S.token(r, "MONETARY", None, 1, "b"), S.SplitError, "hops 0", "MONETARY with hops != 0 is refused")
    refuses(lambda: S.token(r, "CITATION", None, S.UNMEASURED, " "), S.SplitError, "token_basis", "a token without basis is refused")
    t = S.token(r, "CITATION", None, S.UNMEASURED, "b")
    check(r.get("token_type") is None, "token copies; the FWO-5 record is unchanged")
    check(S.horizon_status(t, 1)[0] == D.UNKNOWN and S.horizon_status(t, 5)[0] == D.UNKNOWN,
          "F-A4: UNMEASURED hops never read INDEPENDENT at any horizon")
    t2 = S.token(r, "CITATION", "CREDENTIAL", 2, "b")
    check(S.horizon_status(t2, 1) [0] == D.INDEPENDENT, "a hop-2 conversion is INDEPENDENT at horizon 1")
    check(S.horizon_status(t2, 2)[0] == D.CONVERTED and S.horizon_status(t2, 2)[1] == 2, "and CONVERTED at hop 2 within horizon 2")
    n = S.token(r, "NONE", None, None, "b")
    check(S.horizon_status(n, 9)[0] == D.INDEPENDENT, "token NONE stays INDEPENDENT at every horizon")
    c = D.route("apc", D.DOMINANT, D.DOMINANT, src, conversion_point="publication")
    check(S.horizon_status(S.token(c, "MONETARY", None, 0, "b"), 1) == (D.CONVERTED, 1, "FWO-5 reading at hop 1"),
          "a CONVERTED route keeps FWO-5's reading with hop 1")
    refuses(lambda: S.horizon_status(t2, 0), S.SplitError, "int >= 1", "horizon 0 is refused")
    refuses(lambda: S.horizon_status(r, 1), S.SplitError, "no token fields", "an untokened route is refused")


# ------------------------------------------------------------ fixtures ---

def t_fixtures():
    a1, a2, a3, a4 = S.fixture_f_a1(), S.fixture_f_a2(), S.fixture_f_a3(), S.fixture_f_a4()
    check(a1["settles_claim"] is True and a1["removes_gate"] is False, "F-A1 settles a claim, removes no gate")
    check(a2["removes_gate"] is True and a2["settles_claim"] is False, "F-A2 removes a gate, settles no claim")
    check(a3["settles_claim"] is False and a3["removes_gate"] is False, "F-A3 both FALSE")
    check(all(f["source"].startswith("CONSTRUCTED") for f in (a1, a2, a3, a4)), "every fixture declares itself CONSTRUCTED")
    # E-A2: the unamended reading, measured
    check(not S.forces_settlement(a3), "unamended FWO-5 does NOT force a settlement reading on F-A3 (E-A2 fails as stated)")
    check(S.unamended_reading(a3)["status"] == D.INDEPENDENT and S.unamended_reading(a3)["obligation_medium"] == D.NONE_MEDIUM,
          "F-A3 under FWO-5: INDEPENDENT, obligation none")
    check(S.indistinguishable_under_fwo5(a1, a2), "F-A1 and F-A2 are one reading under every FWO-5-derived field")
    check(a1["conversion_point"] != a2["conversion_point"], "the only field separating them is the authored label")
    check(S.split_of(a1) != S.split_of(a2), "under the split they part")
    check(not S.indistinguishable_under_fwo5(a1, a3), "the indistinguishability check is not constant")
    check(S.forces_settlement(a1), "forces_settlement fires on a fine, so it is not CONSTANT_SILENT")
    check(S.horizon_status(a4, 3)[0] == D.UNKNOWN, "F-A4 does not score INDEPENDENT")


def t_cases():
    cases = S.declared_cases()
    check(len(cases) == 3, "three FWO-5 cases declared")
    for c in cases:
        for _, r in S.routes_of(c):
            check("obligation_origin" in r and r["origin_basis"], "every route of %s carries an origin and a basis" % c["name"])
    by = dict((c["name"], S.origin_tally(c)) for c in cases)
    check(by["a_household_phenology"][S.BIOLOGICAL] == 1 and by["b_open_access_finding"][S.BIOLOGICAL] == 0
          and by["c_bitcoin_exit"][S.BIOLOGICAL] == 0, "declared BIOLOGICAL: a 1, b 0, c 0")
    check(len(by["a_household_phenology"]["undecided"]) == 6, "case (a) leaves six routes UNDECIDED under [CHOICE 1]")
    check(by["a_household_phenology"]["split"].get("BOTH") == 1, "the property tax is the one BOTH row [CHOICE 2]")
    check(all(not t["flagged"] for t in by.values()), "no delivered row reads a biological requirement as a claim")
    # a missing declaration is refused, and an extra one
    res = D.case_a_household()
    tbl = dict(S._A_ORIGIN)
    del tbl[("energy", "daylight")]
    refuses(lambda: S.apply_table(res, tbl, S.declare, "origin declaration"), S.SplitError, "no origin declaration",
            "an undeclared route is refused, never defaulted")
    tbl = dict(S._A_ORIGIN)
    tbl[("energy", "moonlight")] = (S.UNDECIDED, None, None, "x")
    refuses(lambda: S.apply_table(res, tbl, S.declare, "origin declaration"), S.SplitError, "does not have",
            "a table row the case lacks is refused")
    # E-A3
    cb = S.tokened_case_b()
    h1, h2 = S.horizon_rows(cb, 1), S.horizon_rows(cb, 2)
    check(h1["independent_rows"] == ["data_access", "publication"], "horizon 1 reproduces FWO-5: data_access and publication")
    check(h2["independent_rows"] == ["publication"], "horizon 2: data_access drops, publication stays on the preprint route")
    alt = S.horizon_rows(S.case_b_alt_reading(), 2)
    check(alt["independent_rows"] == [], "under [CHOICE 6]'s alternative reading nothing survives at two hops (the falsifier, printed)")
    # section 2
    u = S.universal_claim(5)
    check(S.net_positions(u) == [0] * 5 and S.placing_parties(u) == [] and S.both_sides(u) == [0, 1, 2, 3, 4],
          "a universal claim nets to zero and every party is on both sides")
    p = [[0, 2, 2], [0, 0, 0], [0, 0, 0]]
    check(S.net_positions(p) == [4, -2, -2] and S.placing_parties(p) == [0] and S.both_sides(p) == [],
          "a claim held by one against all leaves one placing party")
    check(S.net_positions([]) is None and S.net_positions([[0, 1], [0]]) is None, "empty or non-square is None")
    # expectations as recorded
    exp = dict(S.check_expectations(cases, cb))
    check(exp["E-A1 majority CONSTRUCTED over decided rows [CHOICE 4]"] == "MATCH", "E-A1 majority MATCH")
    check(exp["E-A1 at least 2 of 3 cases carry zero declared BIOLOGICAL edges"] == "MATCH", "E-A1 two of three MATCH")
    check(exp["E-A2 unamended FWO-5 forces a settlement reading on F-A3"] == "MISMATCH", "E-A2 MISMATCH is the recorded result")
    check(exp["E-A3 case (b) at two hops returns no INDEPENDENT route"] == "MISMATCH", "E-A3 whole-case MISMATCH is the recorded result")
    check(exp["E-A3 the citation route itself is not INDEPENDENT at two hops"] == "MATCH", "E-A3 on the named route MATCH")


def t_fail_fixture():
    global FAIL_FIXTURE
    ff = S.fail_fixture()
    check(len(ff) == 3 and all(c["source"].startswith("CONSTRUCTED") for c in ff), "three constructed cases")
    exp = dict(S.check_expectations(ff))
    check(exp["E-A1 at least 2 of 3 cases carry zero declared BIOLOGICAL edges"] == "MISMATCH",
          "the fail fixture makes E-A1 FAIL")
    FAIL_FIXTURE = exp["E-A1 at least 2 of 3 cases carry zero declared BIOLOGICAL edges"] == "MISMATCH"
    # F-A3 is the amendment's designated fail fixture and E-A2 fails on it
    check(dict(S.check_expectations([]))["E-A2 unamended FWO-5 forces a settlement reading on F-A3"] == "MISMATCH",
          "F-A3, the amendment's own fail fixture, makes E-A2 FAIL")


def t_hygiene():
    r = render()
    check(r == render(), "render deterministic")
    ns = screen()
    if ns is not None:
        ok, h = ns.check(r)
        check(ok, "render screens clean with no exemption (%s)" % [x[1] for x in h][:5])
        check(not ns.check(r + "\nthis cell is wrong\n")[0], "a planted word is caught")
    p = subprocess.run([sys.executable, SRC, "--selftest"], capture_output=True)
    check(p.returncode == 2, "refuses --selftest with exit 2")
    p = subprocess.run([sys.executable, SRC], capture_output=True)
    check(p.returncode == 0, "runs with exit 0")
    src = open(SRC, "rb").read()
    check(all(b < 128 for b in src), "ASCII")
    ast.parse(src.decode("ascii"), feature_version=(3, 8))
    check(True, "parses under 3.8")
    check(os.path.exists(os.path.join(HERE, "AMENDMENT_A1_2026-09-28_settlement-vs-gate.md")), "the amendment is present verbatim")
    log = subprocess.run(["git", "log", "--format=%h", "-n", "1", "--", "AMENDMENT_A1_2026-09-28_settlement-vs-gate.md"],
                         cwd=HERE, capture_output=True, text=True).stdout.strip()
    if log:
        check(log == S.EXPECTED_COMMIT, "the amendment's last commit is the registered EXPECTED commit (%s)" % log)
    sample = os.path.join(HERE, "samples", "settlement_split.sample.txt")
    if os.path.exists(sample):
        check(open(sample, encoding="utf-8").read() == r, "sample matches a fresh render")
    # the two siblings still run unchanged
    for t in ("test_dependency_chain.py", "test_single_channel.py"):
        p = subprocess.run([sys.executable, os.path.join(HERE, t)], capture_output=True)
        check(p.returncode == 0, "%s still green" % t)


for fn in (t_structure, t_fields, t_tokens, t_fixtures, t_cases, t_fail_fixture, t_hygiene):
    fn()

tag = "" if FAIL_FIXTURE else "  NO_FAIL_FIXTURE: settlement_split"
print("settlement-split: %d checks, %d failed; fail fixture present on 1 of 1 instruments%s" % (_checks, _failed, tag)
      if FAIL_FIXTURE else "settlement-split: %d checks, %d failed%s" % (_checks, _failed, tag))
sys.exit(1 if _failed else 0)
