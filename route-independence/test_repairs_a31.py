# SPDX-License-Identifier: CC0-1.0
"""Checks for AMENDMENT A-3.1 (repairs_a31.py).

Run:  python3 route-independence/test_repairs_a31.py
Prints the check count and whether a fixture built to FAIL exists (key-holder
rule 3); NO_FAIL_FIXTURE in the summary line otherwise.
"""
import ast
import io
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import gate_state as G          # noqa: E402
import settlement_split as S    # noqa: E402
import thermal_gates as T       # noqa: E402
import repairs_a31 as R         # noqa: E402

SRC = os.path.join(HERE, "repairs_a31.py")
SRC_TEXT = open(SRC).read()
_checks = 0
_failed = 0
FAIL_FIXTURES = 0


def check(cond, msg):
    global _checks, _failed
    _checks += 1
    if not cond:
        _failed += 1
        sys.stderr.write("FAIL: %s\n" % msg)


def render():
    buf = io.StringIO()
    R.render(buf)
    return buf.getvalue()


def screen():
    sys.path.insert(0, os.path.join(HERE, "..", "sheet-structure-scan"))
    try:
        import no_severity
        return no_severity
    except ImportError:
        return None


# ---------------------------------------------------------------- section 1 ---

def t_market():
    check(set(R.MARKET_GATES) == {T.TOKEN_PURCHASE, T.METERED_TOKEN}, "MARKET_GATES is the amendment's two kinds")
    check(set(R.NON_MARKET) == set(T.GATE_KINDS) - set(R.MARKET_GATES) and len(R.NON_MARKET) == 5,
          "NON_MARKET is every other gate_kind")
    check(set(R.MARKET_GATES) == set(T.MARKET_E32A), "the one definition equals E-A3-2a's own list")
    check(set(R.MARKET_GATES) != set(T.MARKET_2D), "and differs from section 2d as delivered")
    gates, zeros, acts = T.fixture_gates(), T.fixture_f_t6(), T.seed_actuators()
    r = R.e32a_rerun(gates, zeros, acts)
    check((r["covered"], r["n_cells"]) == (6, 50), "coverage 6/50 on the delivered K rows")
    check(r["sourced"] == 0, "no sourced row")
    check(r["tally"][R.UNMET_UNFALSIFIED] == [("state A", "heating.utility"), ("state B", "heating.utility")],
          "the metered utility lands in UNMET_UNFALSIFIED in both jurisdictions")
    check(len(r["tally"][R.MET]) == 4 and r["tally"][R.FALSIFIER] == [], "4 cells met, falsifier silent")
    check((r["prior_met_2d"], r["prior_met_e32a"], r["prior_parted"]) == (6, 4, ["heating.utility"]),
          "the prior two-definition result is carried beside it")
    nm = R.nonmarket_gates(gates, "state A", T.T_QUERY)
    check(nm.get("heating.utility") == 0, "section 2d's quantity under the one definition counts 0 for heating")
    r2 = R.e32a_rerun(gates + [R.fixture_retain_k()], zeros, acts)
    check(r2["tally"][R.FALSIFIER] == [("state X", "clothing.retain")], "the RETAIN K row reaches the falsifier")
    check((r2["covered"], r2["n_cells"]) == (7, 50), "coverage 7/50 with it")


# ---------------------------------------------------------------- section 2 ---

def t_complement():
    q = R.quotes_present()
    check(len(q) == 29 and all(x[3] for x in q), "every P and F quote is found in its amendment (%d)" % len(q))
    tab = dict(((e["id"], e["variant"]), c["status"]) for e, c in R.complement_table())
    want = {("A-1 E-A1", ""): R.FALSIFIER_UNDECLARED, ("A-1 E-A2", ""): R.COMPLEMENT,
            ("A-1 E-A3", ""): R.COMPLEMENT, ("E-A2-1", ""): R.FALSIFIER_UNDECLARED,
            ("E-A2-2", ""): R.FALSIFIER_UNDECLARED, ("E-A2-3", ""): R.COMPLEMENT,
            ("E-A2-4", ""): R.FALSIFIER_UNDECLARED, ("E-A2.1-1", ""): R.FALSIFIER_UNDECLARED,
            ("E-A2.1-2", ""): R.FALSIFIER_UNDECLARED, ("E-A3-1", ""): R.FALSIFIER_UNDECLARED,
            ("E-A3-2a", ""): R.GAP, ("E-A3-3", "literal [CHOICE 28]"): R.OVERSHOOT,
            ("E-A3-3", "side [CHOICE 28]"): R.COMPLEMENT, ("E-A3-4", "literal [CHOICE 29]"): R.GAP,
            ("E-A3-4", "R2-scoped [CHOICE 29]"): R.COMPLEMENT, ("E-A3-5", ""): R.FALSIFIER_UNDECLARED,
            ("E-A3-6", ""): R.NOT_A_PREDICTION, ("E-A3.1-1", ""): R.GAP, ("E-A3.1-2", ""): R.GAP}
    check(tab == want, "complement statuses as computed: %s" % dict((k, v) for k, v in tab.items() if want.get(k) != v))
    c = dict(((e["id"], e["variant"]), c) for e, c in R.complement_table())
    check(c[("E-A3-2a", "")]["gap_cells"] == ["{METERED_TOKEN,TOKEN_PURCHASE}", "{METERED_TOKEN}", "{}"],
          "E-A3-2a's gap: zero gates, METERED_TOKEN alone, purchase with metered")
    check(c[("E-A3-4", "literal [CHOICE 29]")]["gap_cells"] == ["('NON_BODY', False, True)"],
          "E-A3-4's literal gap: an unsourced non-body actuator with zero gates")
    check("{RETAIN,SHED}" in c[("E-A3-3", "literal [CHOICE 28]")]["overshoot_cells"],
          "E-A3-3 literal overshoot: an instrument on RETAIN and SHED satisfies P and fires F")
    check(c[("E-A3.1-1", "")]["gap_cells"] == ["(True, 0)"], "E-A3.1-1's own gap: only E-A3-2a mismatches")
    check(c[("E-A3.1-2", "")]["gap_cells"] == ["(False, True)"], "E-A3.1-2's own gap: meaning moved, reading did not")
    # the checker, null-tested both ways on planted entries
    base = {"id": "X", "variant": "", "amendment": "A-3", "p_quote": "x", "f_quote": "y", "f_form": R.STATED,
            "f_requires": R.PRESENCE, "requires_reason": "", "space": (0, 1, 2), "min_cells": 0, "max_cells": 2,
            "p": lambda w: all(c == 0 for c in w)}
    exact = dict(base, f=lambda w: any(c != 0 for c in w))
    narrow = dict(base, f=lambda w: any(c == 2 for c in w))
    wide = dict(base, f=lambda w: any(c in (0, 2) for c in w))
    check(R.complement(exact)["status"] == R.COMPLEMENT, "planted exact complement reads COMPLEMENT")
    check(R.complement(narrow)["status"] == R.GAP and R.complement(narrow)["gap_cells"] == ["1"],
          "planted narrower F reads GAP at the missing cell")
    check(R.OVERSHOOT in R.complement(wide)["status"], "planted wider F reads OVERSHOOT")
    und = dict(base, f_form=R.UNDECLARED, f=lambda w: False)
    check(R.complement(und)["status"] == R.FALSIFIER_UNDECLARED, "an undeclared F is counted apart [CHOICE 26]")
    check(R.complement(exact)["n_worlds"] == 10, "worlds of 0..2 cells over 3 states: 1 + 3 + 6")
    ea1 = R.e_a1_internal()
    check(ea1["worlds"] == 216 and ea1["parted"] > 0, "A-1 E-A1's two predicates part on some worlds")
    c3 = R.e311_counts()
    check(c3["LITERAL_ALL"] == (True, 10) and c3["DECLARED_LITERAL"] == (True, 2)
          and c3["DECLARED_CHARITABLE"] == (True, 0), "mismatch counts per reading: %s" % c3)


# ---------------------------------------------------------------- section 3 ---

def t_lint():
    ct = R.count_tokens
    check([x["status"] for x in ct("carries 3 gates")] == [R.OK], "3 gates: OK")
    check([x["status"] for x in ct("carries 3 cases")] == [R.UNIT_OUTSIDE_LIST], "3 cases: outside the list")
    check([x["status"] for x in ct("at least 2 of 3 cases")] == [R.UNIT_OUTSIDE_LIST] * 2, "2 of 3 cases: both")
    check(ct("at t=2026, E-A3-2a, HB 16-1005 (2016), Section 2, row 2c") == [], "identifiers, years, sections skip")
    check([x["status"] for x in ct("carries >= 1 NON-MARKET gate")] == [R.OK], "unit within three words")
    check([x["status"] for x in ct("counted 7.")] == [R.NO_UNIT], "a count at the end of a sentence is found")
    lt = dict((l["amendment"], l) for l in R.lint())
    check(lt["A-1"]["verdict"] == "LINT_FAIL" and lt["A-1"]["n_fail"] == 5, "A-1: 5 unlabelled counts")
    check(lt["A-2"]["verdict"] == "LINT_FAIL" and lt["A-2"]["n_fail"] == 2, "A-2: 2")
    check(lt["A-2.1"]["verdict"] == "PASS (no count token)", "A-2.1: no count token")
    check(lt["A-3"]["verdict"] == "LINT_FAIL" and lt["A-3"]["n_fail"] == 2, "A-3: 2 ('one state', 'one instrument')")
    check([x["status"] for x in lt["A-3"]["tokens"] if x["token"] == "four"] == [R.OK],
          "A-3's 'four gates' passes the lint (and counts positions, RIN_087)")
    check(lt["A-3.1"]["verdict"] == "LINT_FAIL" and lt["A-3.1"]["n_fail"] == 2,
          "A-3.1's own EXPECTED fails its own lint ('one mismatch', 'zero mismatches')")


# ---------------------------------------------------------------- section 4 ---

def t_nulls():
    row = {"t_from": R.NOT_RECORDED, "t_to": "2010"}
    check(R.at3(row, "2026") == R.NOT_IN_FORCE and R.at3(row, "2000") == R.UNDETERMINED, "at3, start not recorded")
    row = {"t_from": "2016", "t_to": R.NOT_RECORDED}
    check(R.at3(row, "2026") == R.UNDETERMINED and R.at3(row, "2000") == R.NOT_IN_FORCE, "at3, end not recorded")
    check(R.at3({"t_from": R.NOT_RECORDED, "t_to": R.NOT_RECORDED}, "2026") == R.UNDETERMINED, "at3, neither")
    check(R.at3({"t_from": "2016", "t_to": R.OPEN_ENDED}, "2026") == R.IN_FORCE, "at3, open-ended")
    check(R.at3({"t_from": R.OPEN_ENDED, "t_to": "2016"}, "2000") == R.IN_FORCE, "at3, open-ended start")
    g = dict(T.fixture_f_t4()[0])
    g["t_to"], g["trigger_condition"] = R.OPEN_ENDED, R.NOT_RECORDED
    check(R.applies3(g, "county X", "2026", None) == R.APPLIES, "unconditional query applies")
    check(R.applies3(g, "county X", "2026", "drought declaration in force") == R.UNDETERMINED,
          "a trigger not recorded is UNDETERMINED under a named condition")
    g["trigger_condition"] = R.NONE
    check(R.applies3(g, "county X", "2026", "drought declaration in force") == R.APPLIES, "NONE applies under it")
    orig = G.fixture_f_w3()
    snapshot = dict(orig)
    R.migrate_row(R.EVIDENCE, "A-2:F-W3", "A-2", orig)
    check(orig == snapshot, "migration returns a copy; the A-2 row is unchanged")
    for rule in R.RULES:
        s = R.migration_summary(rule)
        check(s["rows"] == 63 and s["rows_migrated"] == 31, "%s: 63 rows, 31 carry a nullable value" % rule)
        vals = [m["new"] for r in s["table"] for m in r["moves"]]
        check(None not in vals and "UNKNOWN" not in vals and S.UNDECIDED not in vals,
              "%s: no migrated value is None, UNKNOWN or UNDECIDED" % rule)
        acc = set(m["new"] for r in s["table"] for m in r["moves"] if m["field"] == "access_is_right")
        check(acc == {R.NOT_RECORDED}, "%s: access_is_right never takes NONE [CHOICE 33]" % rule)
        oo = [m for r in s["table"] for m in r["moves"] if m["field"] == "obligation_origin"]
        check(len(oo) == 2 and all(m["old"] == S.UNDECIDED and m["new"] == R.NOT_RECORDED for m in oo),
              "%s: the 2 UNDECIDED origins map to NOT_RECORDED; NONE rows untouched" % rule)
        check("A-2:F-W3" in s["by_class"][R.READING_CHANGED] and "A-2.1:F-W4" in s["by_class"][R.READING_CHANGED],
              "%s: the two rows with no t change reading (at() collapsed not-recorded into not-in-force)" % rule)
    ev, sd = R.migration_summary(R.EVIDENCE), R.migration_summary(R.SCHEMA_DEFAULT)
    check(len(ev["by_class"][R.READING_CHANGED]) == 22 and len(sd["by_class"][R.READING_CHANGED]) == 2,
          "rows whose reading moved: 22 under EVIDENCE, 2 under SCHEMA_DEFAULT")
    check(ev["fields"]["t_to"] == {R.NOT_RECORDED: 22, R.OPEN_ENDED: 2}, "EVIDENCE t_to: OPEN_ENDED only on W-2a rows")
    check(sd["fields"]["revocable_by"] == {R.NONE: 14} and ev["fields"]["revocable_by"] == {R.NOT_RECORDED: 14},
          "revocable_by: NONE by schema, NOT_RECORDED by evidence")


# ---------------------------------------------------------------- sections 5-7 ---

def t_e33_absence_coverage():
    gates = T.fixture_gates()
    r = R.e33_a31(gates + [T.row_fan_purchase()])
    check(r["literal_shared"] == ["market purchase"] and r["nonmarket_shared"] == [],
          "E-A3-3: a purchase on both sides fires the literal and not the amended reading")
    check(R.e33_a31(gates)["literal_shared"] == [], "K rows as delivered: disjoint either way")
    k = R.fixture_retain_k()
    check(k["grade"] == "K" and not k["hold_eligible"] and k["absence_bound"] and k["gate_kind"] == T.TOKEN_PURCHASE,
          "the RETAIN row: TOKEN_PURCHASE only, grade K, hold-ineligible, ABSENCE_BOUND [CHOICE 35]")
    for rule, e23 in ((R.EVIDENCE, R.NOT_TESTABLE_AS_POSED), (R.SCHEMA_DEFAULT, R.DECIDED_BY_PRESENCE)):
        ab = dict((x["id"], x) for x in R.absence_bound(rule))
        check(ab["E-A3-2a"]["status"] == R.NOT_TESTABLE_AS_POSED and ab["E-A3-4"]["status"] == R.NOT_TESTABLE_AS_POSED,
              "%s: unfired absence-bound falsifiers read NOT_TESTABLE_AS_POSED, never silent" % rule)
        check(ab["E-A2-3"]["status"] == e23, "%s: E-A2-3 reads %s" % (rule, e23))
    legs = dict((l["route"], l["status"]) for l in R.e23_legs(R.EVIDENCE))
    check(legs == {"gleaning": R.NOT_TESTABLE_AS_POSED, "rainwater_rooftop": R.DECIDED_BY_PRESENCE},
          "under EVIDENCE the rainwater leg is decided by Utah's sourced reading; gleaning is not testable")
    acts, zeros = T.seed_actuators(), T.fixture_f_t6()
    c = R.coverage_grid(gates, zeros, acts, T.jurisdictions(gates), True)
    check((c["covered"], c["total"], c["sourced"]) == (6, 50, 0), "coverage 6/50, sourced 0")
    check("6/50 (sourced 0/50)" in render(), "the render prints coverage beside the result")


# ---------------------------------------------------------------- section 8 ---

def t_expectations():
    rows = R.check_expectations()
    st = [(r["id"], r["status"]) for r in rows]
    check(st[0] == ("E-A3.1-1 (DECLARED_CHARITABLE)", R.UNMET_UNFALSIFIED),
          "the reading that lands in E-A3.1-1's own gap prints first")
    check(all(s == "MATCH" for i, s in st[1:]), "every other reading MATCHes: %s" % st)
    check(len(rows) == 5, "three readings of E-A3.1-1, two rules for E-A3.1-2")
    check(all("coverage" in r["hold"] for r in rows), "every hold carries its coverage")


def t_fail_fixture():
    global FAIL_FIXTURES
    ff = R.fail_fixture()
    ok1 = ff["heating_2d_nonmarket"] == 1 and ff["heating_a31"] == R.UNMET_UNFALSIFIED
    ok2 = ff["f_w3_at"] == R.NOT_IN_FORCE and ff["f_w3_at3"] == R.UNDETERMINED
    check(ok1, "fail fixture 1: section 2d as delivered reads heating as met; the one definition does not")
    check(ok2, "fail fixture 2: at() reads a row with no t NOT_IN_FORCE; at3 UNDETERMINED")
    FAIL_FIXTURES = int(ok1) + int(ok2)


def t_hygiene():
    r = render()
    ns = screen()
    if ns is not None:
        ok, h = ns.check(r)
        check(ok, "render screens clean with no exemption (%s)" % [x[1] for x in h][:5])
    for seed in ("1", "2"):
        env = dict(os.environ, PYTHONHASHSEED=seed)
        p = subprocess.run([sys.executable, SRC], capture_output=True, text=True, env=env)
        check(p.stdout == r, "render is identical under PYTHONHASHSEED=%s" % seed)
    p = subprocess.run([sys.executable, SRC, "--selftest"], capture_output=True, text=True)
    check(p.returncode == 2, "refuses --selftest with exit 2")
    p = subprocess.run([sys.executable, SRC, "--choices"], capture_output=True, text=True)
    check(p.returncode == 0 and len([l for l in p.stdout.splitlines() if l.startswith("[CHOICE")]) == len(R.CHOICES), "--choices prints every choice")
    check(sorted(R.CHOICES) == list(range(24, 38)), "choices numbered on from A-3's 14..23")
    body = SRC_TEXT.split('"""', 2)[2]
    rest = body[:body.index("CHOICES = {")] + body[body.index("MARKET_GATES = ("):]
    for k in R.CHOICES:
        check(("[CHOICE %d]" % k) in rest, "[CHOICE %d] is cited outside its declaration" % k)
    src = open(SRC, "rb").read()
    check(all(b < 128 for b in src), "ASCII")
    ast.parse(src.decode("ascii"), feature_version=(3, 8))
    check(True, "parses under 3.8")
    log = subprocess.run(["git", "log", "--format=%h", "-n", "1", "--", R.AMENDMENT_FILE], cwd=HERE,
                         capture_output=True, text=True).stdout.strip()
    if log:
        check(log == R.EXPECTED_COMMIT_A31, "the amendment's last commit is the registered EXPECTED commit (%s)" % log)
    for other in ("test_gate_state.py", "test_gate_state_a21.py", "test_thermal_gates.py",
                  "test_settlement_split.py"):
        p = subprocess.run([sys.executable, os.path.join(HERE, other)], capture_output=True)
        check(p.returncode == 0, "%s still green" % other)
    sample = os.path.join(HERE, "samples", "repairs_a31.sample.txt")
    if os.path.exists(sample):
        check(open(sample, encoding="utf-8").read() == r, "sample matches a fresh render")


for fn in (t_market, t_complement, t_lint, t_nulls, t_e33_absence_coverage, t_expectations, t_fail_fixture,
           t_hygiene):
    fn()

tag = "" if FAIL_FIXTURES else "  NO_FAIL_FIXTURE: repairs_a31"
print("repairs-a31: %d checks, %d failed; fail fixtures present: %d of 2%s" % (_checks, _failed, FAIL_FIXTURES, tag))
sys.exit(1 if _failed else 0)
