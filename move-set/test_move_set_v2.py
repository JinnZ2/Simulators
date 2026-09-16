#!/usr/bin/env python3
# test_move_set_v2.py -- checks for move_set_sim_v2.py. CC0, stdlib only.
#
# Expected verdicts live HERE and in no data file, so no fixture can
# agree with the module by construction.

import ast
import io
import json
import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import move_set_sim_v2 as M                                       # noqa: E402

PASS = []
FAIL = []


def ck(name, cond, detail=""):
    (PASS if cond else FAIL).append(name)
    if not cond:
        print("FAIL %s  %s" % (name, detail))


def art():
    return M.read_artifact(M.DEMO_ARTIFACT)


def ledger(entries, order=None):
    return {"artifact": "x", "order": order or list(M.MOVES),
            "entries": entries}


def q(move, line, i, j, **kw):
    f = {"kind": "QUOTE", "line": line, "col_start": i, "col_end": j}
    f.update(kw)
    return {"move_id": move, "confidence": "c", "finding": f}


def absent(move, reason="r", looked=((1, 5),), sought=("zzzznotpresent",)):
    return {"move_id": move, "confidence": "c",
            "absent": {"reason": reason, "looked_at": [list(x) for x in looked],
                       "sought": list(sought)}}


A = art()

# --- 1. shape ---------------------------------------------------------
ck("1.1 six moves", len(M.MOVES) == 6, sorted(M.MOVES))
ck("1.2 move ids ordered M1..M6",
   [k.split("_")[0] for k in M.MOVES] == ["M1", "M2", "M3", "M4", "M5", "M6"])
ck("1.3 every move admits ABSENT (CHOICE 1)",
   all("ABSENT" in v["kinds"] for v in M.MOVES.values()))
ck("1.4 M6 has its own trigger (CHOICE 1)",
   bool(M.MOVES["M6_absence_first_class"]["trigger"]))
ck("1.5 exactly one move admits DERIVED",
   sum(1 for v in M.MOVES.values() if "DERIVED" in v["kinds"]) == 1)

_wo = open(os.path.join(HERE, "WORK_ORDER_V2.md"), encoding="utf-8").read()
_won = re.sub(r"\s+", " ", _wo)
for k, v in M.MOVES.items():
    ck("1.6 order_line verbatim in work order: %s" % k,
       re.sub(r"\s+", " ", v["order_line"]) in _won, v["order_line"])

# --- 2. the load-bearing repair: the v1 garbage ledger ----------------
# v1's null test: right shape, "x" in every prose field, scored full marks
# (MV_002). Here the same shape reaches no artifact and scores zero.
_garbage = ledger([{"move_id": m, "confidence": "x",
                    "absent": {"reason": "x", "looked_at": [], "sought": ["x"]}}
                   for m in M.MOVES])
_gs = M.score(_garbage, A)
ck("2.1 garbage ledger scores 0.0 of 6.0",
   _gs["total"] == 0.0 and _gs["possible"] == 6.0, _gs["total"])
ck("2.2 every garbage row names why", all(r["detail"] for r in _gs["rows"]))
ck("2.3 garbage rows are UNVERIFIED_NO_SPAN, not an error",
   all(r["verdict"] == M.UNVERIFIED_NO_SPAN for r in _gs["rows"]))
# and the honest version of the same shape does score, so 2.1 is not a
# module that refuses everything.
_honest = ledger([absent(m, looked=((1, 92),)) for m in M.MOVES])
ck("2.4 an honest all-absence ledger scores 6.0",
   M.score(_honest, A)["total"] == 6.0)

# --- 3. bind_quote ----------------------------------------------------
ck("3.1 BOUND slices the artifact",
   M.bind_quote(A, q("M2_substitution", 17, 41, 46))[0] == M.BOUND)
_v, _sv, _ = M.bind_quote(A, q("M2_substitution", 17, 41, 46))
ck("3.2 value comes from the artifact, not the ledger",
   _sv.value == "1.911", _sv.value if _sv else None)
ck("3.3 UNBOUND_LINE past the end",
   M.bind_quote(A, q("M2_substitution", 9999, 0, 3))[0] == M.UNBOUND_LINE)
ck("3.4 UNBOUND_LINE at 0 (1-based)",
   M.bind_quote(A, q("M2_substitution", 0, 0, 3))[0] == M.UNBOUND_LINE)
ck("3.5 UNBOUND_TEXT when the quote is not that line",
   M.bind_quote(A, q("M2_substitution", 17, 41, 46, quote="not the line"))[0]
   == M.UNBOUND_TEXT)
ck("3.6 UNBOUND_VALUE when expect disagrees with the artifact",
   M.bind_quote(A, q("M2_substitution", 17, 41, 46, expect="9.999"))[0]
   == M.UNBOUND_VALUE)
ck("3.7 UNBOUND_VALUE on columns off the end",
   M.bind_quote(A, q("M2_substitution", 17, 41, 9999))[0] == M.UNBOUND_VALUE)
ck("3.8 MALFORMED on non-integer columns",
   M.bind_quote(A, q("M2_substitution", 17, "a", 46))[0] == M.MALFORMED)
ck("3.9 a correct quote is BOUND with the real line text",
   M.bind_quote(A, q("M2_substitution", 17, 41, 46,
                     quote=A["lines"][16]))[0] == M.BOUND)

# --- 4. bind_derived: both directions ---------------------------------
def der(op, pairs, stated, holds):
    return {"move_id": "M4_perturb", "confidence": "c",
            "finding": {"kind": "DERIVED", "op": op, "stated": stated,
                        "holds": holds,
                        "operands": [{"line": l, "col_start": i, "col_end": j}
                                     for (l, i, j) in pairs]}}

_AB_CAS = [(15, 41, 46), (16, 41, 46)]      # 1.889, 1.555 -> 0.334
_AB_POI = [(15, 41, 46), (17, 41, 46)]      # 1.889, 1.911 -> 0.022
ck("4.1 holds=True where it holds",
   M.bind_derived(A, der("abs_sub", _AB_CAS, 0.334, True))[0]
   == M.ARITHMETIC_AS_DECLARED)
ck("4.2 holds=False where it fails",
   M.bind_derived(A, der("abs_sub", _AB_POI, 0.021, False))[0]
   == M.ARITHMETIC_AS_DECLARED)
ck("4.3 holds=True where it fails is not earned",
   M.bind_derived(A, der("abs_sub", _AB_POI, 0.021, True))[0]
   == M.ARITHMETIC_NOT_AS_DECLARED)
ck("4.4 holds=False where it holds is not earned",
   M.bind_derived(A, der("abs_sub", _AB_CAS, 0.334, False))[0]
   == M.ARITHMETIC_NOT_AS_DECLARED)
ck("4.5 the recomputed value is returned, not the stated one",
   abs(M.bind_derived(A, der("abs_sub", _AB_CAS, 0.334, True))[1] - 0.334)
   < 1e-9)
ck("4.6 OPERAND_NOT_IN_ARTIFACT on a bad line",
   M.bind_derived(A, der("abs_sub", [(9999, 0, 3), (16, 41, 46)], 1, True))[0]
   == M.OPERAND_NOT_IN_ARTIFACT)
ck("4.7 OPERAND_NOT_IN_ARTIFACT when the slice is not a number",
   M.bind_derived(A, der("abs_sub", [(5, 0, 4), (16, 41, 46)], 1, True))[0]
   == M.OPERAND_NOT_IN_ARTIFACT)
ck("4.8 MALFORMED without a holds declaration",
   M.bind_derived(A, {"move_id": "M4_perturb",
                      "finding": {"kind": "DERIVED", "op": "abs_sub",
                                  "stated": 1,
                                  "operands": [{"line": 15, "col_start": 41,
                                                "col_end": 46}] * 2}})[0]
   == M.MALFORMED)
ck("4.9 MALFORMED on an unknown op",
   M.bind_derived(A, der("exponentiate", _AB_CAS, 1, True))[0] == M.MALFORMED)
ck("4.10 div by zero is MALFORMED, not inf",
   M.bind_derived(A, der("div", [(15, 41, 46), (19, 41, 46)], 1, True))[0]
   in (M.MALFORMED, M.ARITHMETIC_NOT_AS_DECLARED))
ck("4.11 all four ops are reachable", sorted(M.OPS) ==
   ["abs_sub", "div", "mul", "sub"])

# --- 5. verify_absence ------------------------------------------------
Ab = M.Absent
ck("5.1 VERIFIED when the token is not in the span",
   M.verify_absence(A, Ab("r", [[1, 92]], ["zzzznotpresent"]))[0]
   == M.VERIFIED_ABSENCE)
ck("5.2 REFUTED when the token IS in the span",
   M.verify_absence(A, Ab("r", [[1, 92]], ["Ammann-Beenker"]))[0]
   == M.REFUTED_ABSENCE)
ck("5.3 REFUTED names the token",
   "Ammann-Beenker" in M.verify_absence(A, Ab("r", [[1, 92]],
                                              ["Ammann-Beenker"]))[1])
ck("5.4 UNVERIFIED_NO_SPAN with no span",
   M.verify_absence(A, Ab("r", [], ["x"]))[0] == M.UNVERIFIED_NO_SPAN)
ck("5.5 UNVERIFIED_NO_SPAN with no sought token",
   M.verify_absence(A, Ab("r", [[1, 5]], []))[0] == M.UNVERIFIED_NO_SPAN)
ck("5.6 UNVERIFIED_SPAN past the end",
   M.verify_absence(A, Ab("r", [[1, 9999]], ["x"]))[0] == M.UNVERIFIED_SPAN)
ck("5.7 UNVERIFIED_SPAN on an inverted range",
   M.verify_absence(A, Ab("r", [[9, 2]], ["x"]))[0] == M.UNVERIFIED_SPAN)
ck("5.8 MALFORMED with no reason",
   M.verify_absence(A, Ab("", [[1, 5]], ["x"]))[0] == M.MALFORMED)
ck("5.9 MALFORMED when not an Absent",
   M.verify_absence(A, {"reason": "r"})[0] == M.MALFORMED)
ck("5.10 the search is case-insensitive",
   M.verify_absence(A, Ab("r", [[1, 92]], ["ammann-beenker"]))[0]
   == M.REFUTED_ABSENCE)
ck("5.11 a narrow span can verify what a wide one refutes",
   M.verify_absence(A, Ab("r", [[1, 5]], ["Ammann-Beenker"]))[0]
   == M.VERIFIED_ABSENCE
   and M.verify_absence(A, Ab("r", [[1, 92]], ["Ammann-Beenker"]))[0]
   == M.REFUTED_ABSENCE)

# --- 6. coverage ------------------------------------------------------
ck("6.1 whole artifact is 1.0", M.coverage(A, [[1, 92]]) == 1.0)
ck("6.2 nothing declared is None, never 0.0", M.coverage(A, []) is None)
ck("6.3 a bad span is None", M.coverage(A, [[1, 9999]]) is None)
ck("6.4 half is 0.5", M.coverage(A, [[1, 46]]) == 0.5)
ck("6.5 overlap counted once (CHOICE 4)",
   M.coverage(A, [[1, 46], [1, 46]]) == 0.5)
ck("6.6 disjoint ranges add",
   M.coverage(A, [[1, 23], [24, 46]]) == 0.5)
ck("6.7 coverage is reported and never scored",
   M.score(ledger([absent("M1_provenance", looked=((1, 2),))]), A)["total"]
   == M.score(ledger([absent("M1_provenance", looked=((1, 92),))]),
              A)["total"] == 1.0)

# --- 7. confidence enters no score ------------------------------------
_c1 = ledger([q("M2_substitution", 17, 41, 46)])
_c2 = json.loads(json.dumps(_c1))
_c2["entries"][0]["confidence"] = "certain, definitive, maximal"
ck("7.1 confidence does not move the score",
   M.score(_c1, A)["total"] == M.score(_c2, A)["total"] == 1.0)
_c3 = json.loads(json.dumps(_c1))
del _c3["entries"][0]["confidence"]
ck("7.2 a missing confidence does not move the score",
   M.score(_c3, A)["total"] == 1.0)
ck("7.3 confidence is carried to the row",
   M.score(_c2, A)["rows"][0]["confidence"] == "certain, definitive, maximal")

_src = open(os.path.join(HERE, "move_set_sim_v2.py"), encoding="utf-8").read()
_tree = ast.parse(_src)
_score_fn = [n for n in ast.walk(_tree)
             if isinstance(n, ast.FunctionDef) and n.name == "score"][0]
_pts_exprs = [n.value for n in ast.walk(_score_fn)
              if isinstance(n, ast.Assign)
              and any(isinstance(t, ast.Name) and t.id in ("pts", "total")
                      for t in n.targets)]
_pts_exprs += [n.value for n in ast.walk(_score_fn)
               if isinstance(n, ast.AugAssign)
               and isinstance(n.target, ast.Name) and n.target.id == "total"]
_names = set()
for e in _pts_exprs:
    for n in ast.walk(e):
        if isinstance(n, ast.Name):
            _names.add(n.id)
ck("7.4 no points expression mentions confidence",
   not ({"conf", "confidence"} & _names), sorted(_names))
ck("7.5 no points expression mentions coverage",
   not ({"cov", "coverage"} & _names), sorted(_names))

# --- 8. path_dependence -----------------------------------------------
_o1 = list(M.MOVES)
_o2 = list(reversed(_o1))
_ok1 = ledger([q("M2_substitution", 17, 41, 46)], order=_o1)
_ok2 = ledger([q("M2_substitution", 17, 41, 46)], order=_o2)
_bad = ledger([q("M2_substitution", 9999, 0, 3)], order=_o2)
ck("8.1 fewer than two runs is NOT_EVALUABLE",
   M.path_dependence([_ok1], A)["verdict"] == "NOT_EVALUABLE")
ck("8.2 zero runs is NOT_EVALUABLE, not a pass",
   M.path_dependence([], A)["verdict"] == "NOT_EVALUABLE")
ck("8.3 identical orders is NOT_EVALUABLE (MV_004 repaired)",
   M.path_dependence([_ok1, _ok1], A)["verdict"] == "NOT_EVALUABLE")
ck("8.4 distinct orders, same findings -> ORDERLESS",
   M.path_dependence([_ok1, _ok2], A)["orderless"] is True)
ck("8.5 distinct orders, different findings -> CHAIN",
   M.path_dependence([_ok1, _bad], A)["orderless"] is False)
ck("8.6 the drifting finding is named",
   M.path_dependence([_ok1, _bad], A)["order_sensitive_findings"])

# --- 9. ledger intake -------------------------------------------------
def _tmp(obj):
    fh = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False,
                                     encoding="utf-8")
    json.dump(obj, fh)
    fh.close()
    return fh.name

_v1shape = _tmp([{"move": "M1_provenance", "verdict": "RESOLVED"}])
try:
    M.read_ledger(_v1shape)
    _refused = False
except M.LedgerError as exc:
    _refused = "MV_004" in str(exc)
ck("9.1 a v1 bare-list ledger is refused and the reason names MV_004",
   _refused)
_noorder = _tmp({"entries": []})
try:
    M.read_ledger(_noorder)
    _r2 = False
except M.LedgerError:
    _r2 = True
ck("9.2 a ledger with no declared order is refused", _r2)
ck("9.3 a well-formed ledger reads",
   M.read_ledger(_tmp(ledger([])))["order"] == list(M.MOVES))
for _p in (_v1shape, _noorder):
    os.unlink(_p)

# --- 10. entry intake -------------------------------------------------
ck("10.1 both finding and absent is MALFORMED",
   M.read_entry(A, {"move_id": "M1_provenance",
                    "finding": {"kind": "QUOTE"},
                    "absent": {"reason": "r"}})[2] == M.MALFORMED)
ck("10.2 neither is MALFORMED",
   M.read_entry(A, {"move_id": "M1_provenance"})[2] == M.MALFORMED)
ck("10.3 an unknown move is MALFORMED",
   M.read_entry(A, {"move_id": "M9_nope", "absent": {"reason": "r"}})[2]
   == M.MALFORMED)
_d4 = dict(der("abs_sub", _AB_CAS, 0.334, True))
_d4["move_id"] = "M1_provenance"
ck("10.4 a DERIVED finding on a QUOTE-only move is MALFORMED",
   M.read_entry(A, _d4)[2] == M.MALFORMED)
ck("10.5 an unknown kind is MALFORMED",
   M.read_entry(A, {"move_id": "M1_provenance",
                    "finding": {"kind": "GUESS"}})[2] == M.MALFORMED)

# --- 11. every declared verdict is reachable --------------------------
_reached = set()
for _l in (_garbage, _honest, ledger([
        q("M2_substitution", 17, 41, 46),
        q("M2_substitution", 9999, 0, 3),
        q("M2_substitution", 17, 41, 46, quote="no"),
        q("M2_substitution", 17, 41, 46, expect="9.9"),
        q("M2_substitution", 17, "a", 46),
        q("M2_substitution", 15, 0, 2),          # whitespace-only slice
        der("abs_sub", _AB_CAS, 0.334, True),
        der("abs_sub", _AB_CAS, 0.334, False),
        der("abs_sub", [(9999, 0, 3), (16, 41, 46)], 1, True),
        absent("M1_provenance", looked=((1, 92),), sought=("Cascade",)),
        absent("M1_provenance", looked=((1, 9999),)),
        absent("M1_provenance", looked=()),
])):
    for _r in M.score(_l, A)["rows"]:
        _reached.add(_r["verdict"])
for _v in M.VERDICTS:
    ck("11.%s reachable: %s" % (M.VERDICTS.index(_v) + 1, _v), _v in _reached)

# --- 12. the demo -----------------------------------------------------
_d = M.demo()
ck("12.1 demo scores 6.0 of 6.0", _d["total"] == 6.0 and _d["possible"] == 6.0)
ck("12.2 demo runs every move", _d["moves_not_run"] == [])
ck("12.3 demo artifact matches its pin", _d["artifact_unchanged"] is True)
ck("12.4 demo artifact is not copied into this folder (CHOICE 2)",
   not os.path.exists(os.path.join(HERE, "SIM_STACK_REPORT.txt")))
ck("12.5 demo artifact path is inside this repo",
   os.path.exists(M.DEMO_ARTIFACT))
ck("12.6 contamination is declared", "CONTAMINATION" in _d["contamination"]
   and "FLB_010" in _d["contamination"])
ck("12.7 demo is half absences, reported not penalized",
   _d["absence_fraction"] == 0.5)
ck("12.8 demo carries one DERIVED entry declaring the arithmetic FAILS",
   any(r["kind"] == "DERIVED" and r["verdict"] == M.ARITHMETIC_AS_DECLARED
       for r in _d["rows"]))
ck("12.9 the demo ledger states it is not blind",
   "not blind" in M.read_ledger(M.DEMO_LEDGER).get("note", "").lower())
# the demo scores the same 6.0 the v1 garbage ledger scored under v1. The
# difference is what had to be true to get it.
ck("12.10 demo and garbage differ under v2",
   M.score(_garbage, A)["total"] != _d["total"])

# --- 13. number parsing ----------------------------------------------
ck("13.1 U+2212 MINUS SIGN parses", M._number("\u22121.529") == -1.529)
ck("13.2 ASCII minus parses", M._number("-1.529") == -1.529)
ck("13.3 a word is None", M._number("Cascade") is None)
ck("13.4 None is None", M._number(None) is None)
ck("13.5 the artifact's alpha values differ by 1.460",
   abs(abs(M._number("\u22121.529") - M._number("\u22120.069")) - 1.460) < 1e-9)

# --- 14. sourced is imported, not reimplemented -----------------------
ck("14.1 no local gate", not re.search(r"^def gate\b", _src, re.M))
ck("14.2 no local Locator class", not re.search(r"^class Locator\b", _src, re.M))
ck("14.3 sourced is imported", "import sourced as S" in _src)
ck("14.4 the gate is actually called", "S.gate(" in _src)
ck("14.5 slice_sourced is used, not find_span",
   "S.slice_sourced(" in _src and "find_span" not in _src)

# --- 15. CLI ----------------------------------------------------------
def _run(args):
    return subprocess.run([sys.executable,
                           os.path.join(HERE, "move_set_sim_v2.py")] + args,
                          capture_output=True, text=True)

_r = _run(["--selftest"])
ck("15.1 refuses --selftest with exit 2", _r.returncode == 2)
ck("15.2 the refusal names the suite", "test_move_set_v2.py" in _r.stderr)
ck("15.3 bare invocation renders the move set",
   _run([]).returncode == 0 and "M6_absence_first_class" in _run([]).stdout)
ck("15.4 --demo runs", _run(["--demo"]).returncode == 0)
ck("15.5 --choices runs", _run(["--choices"]).returncode == 0)
_e = _run(["--emit", "some artifact", "--seed", "7"])
ck("15.6 --emit is deterministic under a seed",
   _e.stdout == _run(["--emit", "some artifact", "--seed", "7"]).stdout)
ck("15.7 --emit ships a ledger schema carrying order",
   "order" in json.loads(_e.stdout)["ledger_schema"])

# --- 16. choices ------------------------------------------------------
_ch = _run(["--choices"]).stdout
for _k in M.CHOICES:
    ck("16.1 CHOICE %d printed" % _k, "[CHOICE %d]" % _k in _ch)
    ck("16.2 CHOICE %d cited inline" % _k,
       re.search(r"#\s*CHOICE %d\b|\(CHOICE %d[,)]|CHOICE %d\)" % (_k, _k, _k),
                 _src) is not None)

# --- 17. house ---------------------------------------------------------
ck("17.1 module is ascii", all(ord(c) < 128 for c in _src))
ck("17.2 test is ascii",
   all(ord(c) < 128 for c in open(__file__, encoding="utf-8").read()))
ck("17.3 no network import",
   not re.search(r"\b(socket|urllib|requests|http\.client)\b", _src))
_ledtext = open(M.DEMO_LEDGER, encoding="utf-8").read()
_ledkeys = set()
def _walk(o):
    if isinstance(o, dict):
        _ledkeys.update(o)
        for v in o.values():
            _walk(v)
    elif isinstance(o, list):
        for v in o:
            _walk(v)
_walk(json.loads(_ledtext))
# the ledger's quote fields are verbatim artifact lines and the artifact
# is not ascii. Nothing AUTHORED in the ledger may be.
_ledobj = json.loads(open(M.DEMO_LEDGER, encoding="utf-8").read())
_quotes = []
def _q_walk(o):
    if isinstance(o, dict):
        for k, v in o.items():
            if k == "quote":
                _quotes.append(v)
            else:
                _q_walk(v)
    elif isinstance(o, list):
        for v in o:
            _q_walk(v)
_q_walk(_ledobj)
_stripped = open(M.DEMO_LEDGER, encoding="utf-8").read()
for _qq in _quotes:
    _stripped = _stripped.replace(json.dumps(_qq, ensure_ascii=False)[1:-1], "")
ck("17.6 the demo ledger is ascii outside its verbatim quotes",
   all(ord(c) < 128 for c in _stripped),
   sorted({c for c in _stripped if ord(c) > 127}))
ck("17.7 every quote field is a line of the artifact",
   all(qq in A["lines"] for qq in _quotes), len(_quotes))

ck("17.4 the demo ledger names no verdict",
   not [v for v in M.VERDICTS if v in _ledtext],
   [v for v in M.VERDICTS if v in _ledtext])
ck("17.5 the demo ledger carries no expected-score key",
   not ({"expected", "expected_verdict", "points", "score", "verdict"}
        & _ledkeys), sorted(_ledkeys))

print("\nchecks %d   failed %d" % (len(PASS) + len(FAIL), len(FAIL)))
sys.exit(1 if FAIL else 0)
