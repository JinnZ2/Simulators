# SPDX-License-Identifier: CC0-1.0
"""Checks for the 2026-09-27b order: edge_taxonomy, question_space,
standards_register, lag_count, unpaid_maintenance, tax_step.

Run:  python3 route-independence/test_single_channel.py
Prints the check count and, per instrument, whether a fixture built to FAIL
exists (key-holder rule 3); an instrument without one is named as
NO_FAIL_FIXTURE in the summary line.
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
import edge_taxonomy as E            # noqa: E402
import question_space as Q           # noqa: E402
import standards_register as S       # noqa: E402
import lag_count as L                # noqa: E402
import unpaid_maintenance as U       # noqa: E402
import tax_step as T                 # noqa: E402

_checks = 0
_failed = 0


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


def render_of(mod):
    buf = io.StringIO()
    mod.render(buf)
    return buf.getvalue()


def defined_names(path):
    tree = ast.parse(open(path, encoding="utf-8").read())
    return set(n.name for n in tree.body if isinstance(n, (ast.FunctionDef, ast.ClassDef))) | \
        set(t.id for n in tree.body if isinstance(n, ast.Assign) for t in n.targets if isinstance(t, ast.Name))


FAIL_FIXTURES = {}

# Declared no_severity exemptions, measured in three arms (masked clean; unmasked only these
# words fire; a plant outside the mask is caught).  Every exempted string is delivered or
# carried text the render quotes; authored words were reworded instead.
EXEMPT = {
    "standards_register": ["fracture-critical"],                                  # the order's own term
    "tax_step": [T.CONSEQUENCE, "volunteer or unpaid repair", "meld-as-error-class"],   # OBSERVED text and the order's table row
}
EXEMPT_WORDS = {"standards_register": {"critical"}, "tax_step": {"repair", "error", "confirms"}}


# ------------------------------------------------------------ edge_taxonomy ---

def t_edge():
    fwo5 = defined_names(os.path.join(HERE, "dependency_chain_audit.py"))
    here = defined_names(os.path.join(HERE, "edge_taxonomy.py"))
    clash = (fwo5 & here) - {"HERE", "CHOICES", "render", "main", "check_expectations"}  # per-module conventions, not FWO-5 API
    check(not clash, "edge_taxonomy redefines no FWO-5 name (clash %s)" % sorted(clash))
    cases = E.annotated_cases()
    check(len(cases) == 3, "three annotated cases")
    src = "CONSTRUCTED: test"
    ind = D.route("x", "hours", "hours", src)
    refuses(lambda: E.annotate(ind, "ACCESS", "SURVIVAL", "b"), E.EdgeError, "INDEPENDENT",
            "an INDEPENDENT route refuses an edge_class")
    conv = D.route("y", "USD", "USD", src, conversion_point="tax")
    refuses(lambda: E.annotate(conv, "WRONG", "SURVIVAL", "b"), E.EdgeError, "edge_class",
            "unknown edge_class refused")
    refuses(lambda: E.annotate(conv, "ACCESS", "NEITHER", "b"), E.EdgeError, "coupling_side",
            "unknown coupling_side refused")
    refuses(lambda: E.annotate(conv, "ACCESS", "SURVIVAL", ""), E.EdgeError, "edge_basis",
            "an annotation without a basis is refused")
    unk = D.route("z", "BTC", None, src)
    refuses(lambda: E.annotate(unk, "ACCESS", "SURVIVAL", "no reason"), E.EdgeError, "declared",
            "a non-UNKNOWN class on an UNKNOWN route needs a declared basis")
    check(E.annotate(unk, "ACCESS", "SURVIVAL", "declared: settles in USD by the vendor's own terms")["edge_class"] == "ACCESS",
          "a declared basis admits a class on an UNKNOWN route")
    a = E.annotate(conv, "ACCESS", "SURVIVAL", "b")
    check(E.layer_status(a, "selection") == D.INDEPENDENT and E.layer_status(a, "survival") == D.CONVERTED,
          "SURVIVAL-only route is INDEPENDENT at the selection layer and CONVERTED at the survival layer (hard constraint)")
    b = E.annotate(conv, "ACCESS", "SELECTION", "b")
    check(E.layer_status(b, "selection") == D.CONVERTED and E.layer_status(b, "survival") == D.INDEPENDENT,
          "SELECTION-only route: the mirror")
    c = E.annotate(conv, "ACCESS", "BOTH", "b")
    check(E.layer_status(c, "selection") == D.CONVERTED and E.layer_status(c, "survival") == D.CONVERTED, "BOTH: both")
    u2 = E.annotate(conv, "ACCESS", "UNKNOWN", "b")
    check(E.layer_status(u2, "selection") == D.UNKNOWN, "UNKNOWN side reads UNKNOWN, never a default")
    refuses(lambda: E.layer_status(a, "money"), E.EdgeError, "layer", "unknown layer refused")
    refuses(lambda: E.layer_status(conv, "selection"), E.EdgeError, "not annotated", "an unannotated route is refused")
    # never merged: no function returns a value built from both layers; no arithmetic on a layer reading
    tree = ast.parse(open(os.path.join(HERE, "edge_taxonomy.py"), encoding="utf-8").read())
    both = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and getattr(node.func, "id", "") == "layer_status":
            both.append(node)
    fn_with_two = 0
    for fn in [n for n in tree.body if isinstance(n, ast.FunctionDef)]:
        calls = [n for n in ast.walk(fn) if isinstance(n, ast.Call) and getattr(n.func, "id", "") == "layer_status"]
        layers = set()
        for cl in calls:
            if len(cl.args) > 1 and isinstance(cl.args[1], ast.Constant):
                layers.add(cl.args[1].value)
        if len(layers) == 2 and fn.name != "render":
            fn_with_two += 1
    check(fn_with_two == 0, "no non-render function reads both layers (found %d)" % fn_with_two)
    arith = [n for n in ast.walk(tree) if isinstance(n, ast.BinOp) and isinstance(n.op, (ast.Add, ast.Mult, ast.Div, ast.Sub))
             and any(isinstance(x, ast.Call) and getattr(x.func, "id", "") == "layer_status" for x in ast.walk(n))]
    check(not arith, "no arithmetic over a layer reading")
    # annotation table completeness
    res = D.case_a_household()
    refuses(lambda: E.annotate_case(res, {}), E.EdgeError, "no annotation", "a route without an annotation is refused")
    extra = dict(E._A)
    extra[("labor", "phantom")] = (None, None, "x")
    refuses(lambda: E.annotate_case(res, extra), E.EdgeError,
            "does not have", "an annotation for a route the case lacks is refused")
    # expectations as recorded
    ex = dict(E.check_expectations(cases))
    check(ex["E8.1 DIRECT at most one route across the cases [CHOICE 2]"] == "MATCH", "E8.1 MATCH (as recorded)")
    check(ex["E8.4 row-level: case (b) independent rows == ['data_access']"] == "MISMATCH",
          "E8.4 row-level MISMATCH, as EXPECTED_2026-09-27b.md predicted it would be")
    check(sum(len(E.direct_rows(c)) for c in cases) == 0, "DIRECT rows: zero across the three cases")
    ff = E.fail_fixture()
    check(dict(E.check_expectations([ff]))["E8.1 DIRECT at most one route across the cases [CHOICE 2]"] == "MISMATCH",
          "fail fixture makes E8.1 fail")
    FAIL_FIXTURES["edge_taxonomy"] = True
    m = E.misplacement_report(dict((c["name"], c) for c in cases)["c_bitcoin_exit"])
    check(m["points_without_slot"] == ["input_purchase"], "case (c): input_purchase is the point the two-layer pair cannot place")
    check([p for p in m["by_point"] if p["conversion_point"] == "input_purchase"][0]["routes"] == 3,
          "case (c) input_purchase carries 3 routes (the 3:1 of the first run)")
    b = dict((c["name"], c) for c in cases)["b_open_access_finding"]
    check(E.layer_rows(b, "selection") == ["data_access", "publication"], "case (b) selection-layer rows")
    check("instrument" in E.layer_rows(b, "survival"), "case (b) survival layer frees the grant-bought instrument")


# ----------------------------------------------------------- question_space ---

def t_question():
    col = Q.demo_column()
    check([c["point"] for c in col] == list(Q.POINTS), "every point once, in order")
    check(Q.TAX_STEP if hasattr(Q, "TAX_STEP") else T.TAX_STEP in Q.POINTS, "tax_step is a point, imported")
    refuses(lambda: Q.declare("nowhere", ["Q1"], "b"), Q.ColumnError, "conversion point", "unknown point refused")
    refuses(lambda: Q.declare("tax", ["Q9"], "b"), Q.ColumnError, "unknown class", "unknown class refused")
    refuses(lambda: Q.declare("tax", ["Q1"], ""), Q.ColumnError, "basis", "no basis refused")
    refuses(lambda: Q.declare("tax", ["Q1", "Q1"], "b"), Q.ColumnError, "twice", "duplicate class refused")
    refuses(lambda: Q.column(col[:-1]), Q.ColumnError, "no cell", "a missing point is refused, not implied")
    refuses(lambda: Q.column(col + [col[0]]), Q.ColumnError, "twice", "a duplicated point is refused")
    bad = dict(col[0]); bad["loss"] = 3
    refuses(lambda: Q.column([bad] + col[1:]), Q.ColumnError, "loss", "a loss estimate is refused")
    check(Q.declare("tax", [], "declared none")["closes"] == [] and Q.declare("tax", "UNKNOWN", "b")["closes"] == "UNKNOWN",
          "declared-none and UNKNOWN are two states")
    tree = ast.parse(open(os.path.join(HERE, "question_space.py"), encoding="utf-8").read())
    names = [n.name for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]
    check(not any(any(w in n for w in ("loss", "estimate", "count", "score")) for n in names),
          "no function named for a loss, estimate, count or score (%s)" % names)
    check(all(v == "MATCH" for _, v in Q.check_expectations(col)), "E9.2 MATCH on the declared column")
    check(Q.check_expectations(Q.fail_fixture())[0][1] == "MISMATCH", "fail fixture makes E9.2 fail")
    FAIL_FIXTURES["question_space"] = True


# ------------------------------------------------------- standards_register ---

def t_standards():
    rows = S.seed_rows()
    check(len(rows) == 6 and all(r["applied_to_medium"] == "UNKNOWN_NOT_SEARCHED" for r in rows),
          "six seed rows, every applied cell UNKNOWN_NOT_SEARCHED")
    check(S.applied_verdict(rows) == "NOT_EVALUABLE", "verdict NOT_EVALUABLE on an unsearched column")
    check(S.check_expectations(rows)[0][1] == "NOT_EVALUABLE", "E10.1 NOT_EVALUABLE, not MATCH")
    refuses(lambda: S.row("f", "s", "r", "NOT_APPLIED", "CARRIED_FROM_MEMORY: x"), S.RegisterError, "memory",
            "a memory row cannot fill the applied cell")
    refuses(lambda: S.row("f", "s", "r", "MAYBE", "READ: x"), S.RegisterError, "applied_to_medium", "bad state refused")
    ff = S.fail_fixture()
    check(S.applied_verdict(ff) == "SOME_APPLIED" and S.check_expectations(ff)[0][1] == "MISMATCH",
          "fail fixture: one APPLIED row makes ALL_NOT_APPLIED fail")
    clean = [S.row("f", "s", "r", "NOT_APPLIED", "READ: x")] * 2
    check(S.applied_verdict(clean) == "ALL_NOT_APPLIED", "ALL_NOT_APPLIED reachable on a searched column")
    check(any("inspector is paid through the same path" in r["inspector_note"] for r in rows),
          "the carried OBSERVED inspector line is on the structural row")
    check(all(e["medium"] for e in S.PRIOR_ART["entries"]), "every prior-art entry states the plumbing/medium split")
    FAIL_FIXTURES["standards_register"] = True


# ---------------------------------------------------------------- lag_count ---

def t_lag():
    cases = L.seed_cases()
    check(len(cases) == 6, "six seed cases")
    check(all(c["source"]["kind"] == "UNSOURCED" for c in cases), "every seed UNSOURCED")
    check(L.lag_years(-200, 1821, "FULL") == 2021, "lag by arithmetic across the era boundary")
    check(L.lag_years(-125, None, "RECOVERED_NOT_REDISCOVERED") is None, "no lag for the recovered class")
    check(L.lag_years(500, 2006, "NOT_REACHED") is None, "no lag for NOT_REACHED even with dates")
    refuses(lambda: L.lag_years(1900, 1800, "FULL"), L.LagError, "NEGATIVE_LAG", "reach before production refused")
    refuses(lambda: L.case(**L.fail_fixture()), L.LagError, "NEGATIVE_LAG", "the fail fixture is refused at construction")
    FAIL_FIXTURES["lag_count"] = True
    refuses(lambda: L.case("x", "p", "pop", 1, None, "FULL", {"kind": "CONSTRUCTED"}), L.LagError, "reach_date",
            "FULL without a reach date refused")
    refuses(lambda: L.case("x", "p", "pop", 1, 2, "UNKNOWN", {"kind": "CONSTRUCTED"}), L.LagError, "FULL/PARTIAL only",
            "a reach date on UNKNOWN refused")
    refuses(lambda: L.case("x", "p", "", 1, 2, "FULL", {"kind": "CONSTRUCTED"}), L.LagError, "population",
            "an empty population refused")
    refuses(lambda: L.case("x", "p", "pop", 1, 2, "FULL", {"kind": "CONSTRUCTED"}, not_sold="maybe"), L.LagError,
            "True, False or UNKNOWN", "selector takes three values")
    d = L.distribution(cases)
    check(d["sourced_lags"] == [] and len(d["unsourced_lags"]) == 4, "sourced empty; four unsourced lags")
    check(sum(d["by_reached"].values()) == 6, "by_reached conserves cases")
    check(all(v == "MATCH" for _, v in L.check_expectations(cases)), "E11.1/2/3/5 MATCH (rule 2 unmet; recorded)")
    ok = L.case("y", "p", "pop", 1, 2, "FULL", {"kind": "CONSTRUCTED"}, True, True, True, settlement_check="INDEPENDENT")
    check(L.independence(ok) == "INDEPENDENT", "INDEPENDENT reachable with selector and settlement reading")
    sel = L.case("y", "p", "pop", 1, 2, "FULL", {"kind": "CONSTRUCTED"}, True, True, True)
    check(L.independence(sel) == "CANDIDATE", "selector alone gives CANDIDATE")
    no = L.case("y", "p", "pop", 1, 2, "FULL", {"kind": "CONSTRUCTED"}, True, False, True, settlement_check="INDEPENDENT")
    check(L.independence(no) == "NOT_INDEPENDENT_BY_SELECTOR", "a sold result is not independent whatever the settlement reading")
    r = render_of(L)
    check(r.count(L.SURVIVOR_LINE) >= 1 and r.index(L.SURVIVOR_LINE) < r.index("approx"), "survivor line in the header")


# ------------------------------------------------------ unpaid_maintenance ---

def t_unpaid():
    recs = U.demo_records()
    check([U.classify(r) for r in recs] == ["UNPAID", "NOT_UNPAID", "NOT_UNPAID", "UNKNOWN"],
          "classification: distinct+unplanned+unpaid; same person; planned; missing field UNKNOWN")
    check(U.unpaid_share(recs)["status"] == "NOT_RUN", "no public dataset: NOT_RUN, no share")
    r = U.unpaid_share(recs, public_source="CONSTRUCTED: test only")
    check(r["status"] == "RUN" and abs(r["share"] - 1 / 3.0) < 1e-12 and r["unknown"] == 1,
          "with a declared source the share is over classified records and UNKNOWN counted apart")
    check(U.unpaid_share([recs[3]], "x")["status"] == "NOT_EVALUABLE", "all-UNKNOWN is NOT_EVALUABLE, never 0")
    check(U.prediction_check([(0.1, 0.3), (0.5, 0.2), (0.9, 0.1)]) == "FALLS", "FALLS reachable")
    check(U.prediction_check([(0.1, 0.3), (0.5, 0.3), (0.9, 0.31)]) == "FLAT", "FLAT within the band")
    check(U.prediction_check([(0.1, 0.3), (0.5, 0.2)]) == "NOT_EVALUABLE", "two points: NOT_EVALUABLE")
    check(U.prediction_check(U.fail_fixture()) == "RISES", "fail fixture: the prediction fails on it")
    FAIL_FIXTURES["unpaid_maintenance"] = True
    check(U.ANCHOR["source"].startswith("CARRIED"), "the Linux anchor is CARRIED")


# ----------------------------------------------------------------- tax_step ---

def t_tax():
    rows = T.seed_rows()
    check(len(rows) == 3 and T.check_expectations(rows)[0][1] == "MATCH", "E13.1 MATCH: 2 REGISTERED, 1 CANDIDATE")
    refuses(lambda: T.tax_row(**T.fail_fixture()), T.TaxRowError, "REGISTERED requires", "fail fixture refused")
    FAIL_FIXTURES["tax_step"] = True
    refuses(lambda: T.refuse_fwo6_shape({"id": "x", "changed": [], "reconversions": [], "source": "x"}), T.TaxRowError,
            "own row type", "an FWO-6 entry shape is refused")
    refuses(lambda: T.tax_row("x", "r", "c", "OBSERVED", "FILED", "s"), T.TaxRowError, "status", "bad status refused")
    check(T.tax_row("v", "r", "c", "PROPOSED", "REGISTERED", "VERIFIED: doc")["status"] == "REGISTERED",
          "a VERIFIED source can register a PROPOSED row")
    loaded = T.load()
    check([r["id"] for r in loaded] == [r["id"] for r in rows], "the written register loads and matches the seed")
    x = T.fwo6_cross_reference()
    check(x["fwo6_entries"] == 8 and "bitcoin_cryptocurrency" in x["with_tax_mechanism"], "FWO-6 cross-reference reads the register unchanged")
    check(all(not any(n in r["route"] + r["converts_how"] for n in ("Mr", "Ms", "Dr")) for r in rows), "no person named")


# --------------------------------------------------------------- hygiene ---

def t_hygiene():
    ns = screen()
    mods = [E, Q, S, L, U, T]
    for m in mods:
        r = render_of(m)
        check(r == render_of(m), "%s render deterministic" % m.__name__)
        if ns is not None:
            ex = EXEMPT.get(m.__name__, [])
            masked = r
            for token in ex:
                check(token in r, "%s: exempted text %r is present in the render" % (m.__name__, token[:30]))
                masked = masked.replace(token, "")
            ok, h = ns.check(masked)
            check(ok, "%s render screens clean outside the declared exemptions (%s)" % (m.__name__, [x[1] for x in h][:5]))
            if ex:
                words = set(x[1] for x in ns.hits(r))
                check(words <= EXEMPT_WORDS[m.__name__],
                      "%s: unmasked, only the exempted words fire (%s)" % (m.__name__, sorted(words)))
                check(not ns.check(masked + "\nthis cell is wrong\n")[0], "%s: a planted word outside the exemption is caught" % m.__name__)
        p = subprocess.run([sys.executable, os.path.join(HERE, m.__name__ + ".py"), "--selftest"], capture_output=True)
        check(p.returncode == 2, "%s refuses --selftest with exit 2" % m.__name__)
        p = subprocess.run([sys.executable, os.path.join(HERE, m.__name__ + ".py")], capture_output=True)
        check(p.returncode == 0, "%s runs with exit 0" % m.__name__)
        src = open(os.path.join(HERE, m.__name__ + ".py"), "rb").read()
        check(all(b < 128 for b in src), "%s is ASCII" % m.__name__)
        ast.parse(src.decode("ascii"), feature_version=(3, 8))
        check(True, "%s parses under 3.8" % m.__name__)
    exp = os.path.join(HERE, "EXPECTED_2026-09-27b.md")
    check(os.path.exists(exp), "EXPECTED file present")
    sample = os.path.join(HERE, "samples", "edge_taxonomy.sample.txt")
    if os.path.exists(sample):
        check(open(sample, encoding="utf-8").read() == render_of(E), "edge_taxonomy sample matches a fresh render")


for fn in (t_edge, t_question, t_standards, t_lag, t_unpaid, t_tax, t_hygiene):
    fn()

missing = [k for k in ("edge_taxonomy", "question_space", "standards_register", "lag_count", "unpaid_maintenance", "tax_step")
           if not FAIL_FIXTURES.get(k)]
tag = "" if not missing else "  NO_FAIL_FIXTURE: %s" % ",".join(missing)
print("single-channel: %d checks, %d failed; fail fixtures present on %d of 6 instruments%s"
      % (_checks, _failed, 6 - len(missing), tag))
sys.exit(1 if _failed else 0)
