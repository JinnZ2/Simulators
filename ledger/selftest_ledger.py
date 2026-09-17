#!/usr/bin/env python3
"""Checks for the ledger. Run it; it prints the count.

Every diff is exercised in BOTH directions. A diff that has only been seen
to fire has not been shown to discriminate, and a diff that has only been
seen silent has not been shown to work at all.

THE CROSS-LEDGER DIFF IS THE EXCEPTION AND IT IS LABELLED. GnuCOBOL is
absent here, so the firing direction is exercised against a STUB that
stands in for the cobol arm. The stub shows that ledger.py routes and
records a disagreement correctly. It is not evidence that LEDGER.cob
compiles, runs, or computes anything -- that source has never been
compiled. Nothing in this file says otherwise.

    python3 ledger/selftest_ledger.py

stdlib only. CC0.
"""

from __future__ import annotations

import ast
import decimal
import json
import os
import shutil
import subprocess
import sys
import tempfile
from decimal import Decimal

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import ledger as L                                       # noqa: E402
import review as V                                       # noqa: E402
import record as R                                       # noqa: E402
from cobol_ledger import bridge                           # noqa: E402
from py_ledger import engine                              # noqa: E402

FIXTURES = os.path.join(HERE, "fixtures", "records")

CHECKS = [0]
FAILS = []


def ck(name, cond, detail=""):
    CHECKS[0] += 1
    if not cond:
        FAILS.append("%s %s" % (name, detail))
        print("  FAIL  %s %s" % (name, detail))


def good(**over):
    d = {"claim_id": "X_001", "sim": "s", "value": "1.5", "precision": 4,
         "operands": [], "falsifier": "f", "status": "st",
         "provenance": "MEASURED"}
    d.update(over)
    return d


# --------------------------------------------------------------- intake

def intake():
    print("intake")
    ck("valid record passes", R.validate(good()) == [])
    ck("missing field caught",
       any("missing required field: value" in p
           for p in R.validate({k: v for k, v in good().items()
                                if k != "value"})))
    ck("a float value is refused",
       any("decimal STRING" in p for p in R.validate(good(value=1.5))))
    ck("a non-decimal string is refused",
       any("not a decimal string" in p for p in R.validate(good(value="1,5"))))
    ck("precision below 1 refused",
       any("positive integer" in p for p in R.validate(good(precision=0))))
    ck("DERIVED with no operands refused",
       any("fails intake" in p
           for p in R.validate(good(provenance="DERIVED", operands=[]))))
    ck("DERIVED with no expression refused",
       any("requires an expression" in p
           for p in R.validate(good(provenance="DERIVED",
                                    operands=["A_001"]))))
    ck("expression naming an undeclared operand refused",
       any("not declared operands" in p
           for p in R.validate(good(provenance="DERIVED", operands=["A_001"],
                                    expression="A_001 + A_002"))))
    ck("operand declared and unused refused",
       any("not used by the expression" in p
           for p in R.validate(good(provenance="DERIVED",
                                    operands=["A_001", "A_002"],
                                    expression="A_001"))))
    ck("a well-formed DERIVED passes",
       R.validate(good(provenance="DERIVED", operands=["A_001"],
                       expression="A_001")) == [])
    ck("expression on MEASURED refused",
       any("only meaningful for DERIVED" in p
           for p in R.validate(good(expression="A_001"))))
    ck("DERIVED_WEAK cannot be declared",
       any("cannot be declared" in p
           for p in R.validate(good(provenance="DERIVED_WEAK"))))
    ck("unknown provenance refused",
       any("provenance not in" in p for p in R.validate(good(provenance="X"))))

    ck("bare ref resolves to the emitting sim",
       R.parse_ref("A_001", "fx") == ("fx", "A_001"))
    ck("qualified ref keeps its sim",
       R.parse_ref("gx:A_001", "fx") == ("gx", "A_001"))
    ck("a ref that is not one returns None",
       R.parse_ref("1 + 1", "fx") is None)
    ck("a literal is a literal", R.is_literal("-0.5e3"))
    ck("a name is not a literal", not R.is_literal("A_001"))

    # An unreadable file is an intake failure, not a crash.
    tmp = tempfile.mkdtemp()
    try:
        open(os.path.join(tmp, "bad.json"), "w").write("{not json")
        recs, fails = R.load_records(tmp)
        ck("unreadable json is a result, not a raise",
           recs == [] and len(fails) == 1 and "unreadable" in fails[0][1])
    finally:
        shutil.rmtree(tmp)
    ck("a missing records dir is a result, not a raise",
       R.load_records(os.path.join(tmp, "gone")) == ([], []))


# --------------------------------------------------------------- engine

def engine_checks():
    print("engine")
    safe, m = engine._placeholders("(gx:A_001 + 0.5) / A_001")
    ck("leaves are substituted in one pass, longest name intact",
       sorted(m.values()) == ["0.5", "A_001", "gx:A_001"], m)
    ck("the rewritten expression parses as python", safe.count("_op") == 3)

    ck("quantize is significant digits",
       engine.quantize(Decimal("1234.5"), 2) == "1.2E+3")
    ck("quantize rounds half to even",
       engine.quantize(Decimal("0.125"), 2) == "0.12"
       and engine.quantize(Decimal("0.135"), 2) == "0.14")
    ck("trailing zeros are the same value",
       engine.same_value("6.5", "6.50000", 6))
    ck("different values are different",
       not engine.same_value("6.5", "6.6", 6))
    ck("same_value on a non-number is False, not a raise",
       not engine.same_value("6.5", "apples", 6))

    def rec(**over):
        d = good(provenance="DERIVED", operands=["a", "b"],
                 expression="a / b", precision=6)
        d.update(over)
        return R.ClaimRecord.from_dict(d)

    v = {("s", "a"): "2.5", ("s", "b"): "4"}
    r = engine.recompute(rec(), v)
    ck("a division recomputes", r.ok() and r.value == "0.625", r.value)

    r = engine.recompute(rec(), {("s", "a"): "2.5", ("s", "b"): "0"})
    ck("division by zero is UNDEFINED and carries no number",
       r.outcome is engine.Outcome.UNDEFINED and r.value is None)

    r = engine.recompute(rec(), {("s", "a"): "2.5"})
    ck("an absent operand is UNRESOLVED_OPERAND and names it",
       r.outcome is engine.Outcome.UNRESOLVED_OPERAND and r.reason == "s:b")

    r = engine.recompute(R.ClaimRecord.from_dict(good()), {})
    ck("a MEASURED claim is NOT_DERIVED",
       r.outcome is engine.Outcome.NOT_DERIVED)

    r = engine.recompute(rec(operands=["a"], expression="abs(a)"), v)
    ck("a call is refused, not evaluated",
       r.outcome is engine.Outcome.UNPARSEABLE, r.reason)
    r = engine.recompute(rec(operands=["a"], expression="a.real"), v)
    ck("an attribute is refused", r.outcome is engine.Outcome.UNPARSEABLE)
    r = engine.recompute(rec(expression="a // b"), v)
    ck("an operator outside the four is refused",
       r.outcome is engine.Outcome.UNPARSEABLE, r.reason)
    r = engine.recompute(rec(operands=["a", "b"], expression="a ** b"),
                         {("s", "a"): "2", ("s", "b"): "0.5"})
    ck("a non-integer exponent is refused",
       r.outcome is engine.Outcome.UNPARSEABLE, r.reason)

    # Guard digits: a per-step round would show here.
    r = engine.recompute(rec(operands=["a", "b"], expression="a / b * b"),
                         {("s", "a"): "1", ("s", "b"): "3"})
    ck("guard digits survive an intermediate", r.ok() and r.value == "1.00000",
       r.value)

    # graph
    recs = [R.ClaimRecord.from_dict(good(claim_id="A", provenance="MEASURED")),
            R.ClaimRecord.from_dict(good(claim_id="B", provenance="DERIVED",
                                         operands=["A"], expression="A + 1"))]
    order, cycles = engine.topo_order(recs)
    ck("dependencies come first",
       [r.claim_id for r in order] == ["A", "B"] and cycles == [])
    cyc = [R.ClaimRecord.from_dict(good(claim_id="A", provenance="DERIVED",
                                        operands=["B"], expression="B + 1")),
           R.ClaimRecord.from_dict(good(claim_id="B", provenance="DERIVED",
                                        operands=["A"], expression="A + 1"))]
    order, cycles = engine.topo_order(cyc)
    ck("a cycle is found and its members are withheld from the order",
       order == [] and len(cycles) == 1)

    pr = engine.resolve_provenance(recs)
    ck("a clean DERIVED stays DERIVED",
       pr[("s", "B")][0] is R.Provenance.DERIVED and pr[("s", "B")][1] == [])
    weak = [R.ClaimRecord.from_dict(good(claim_id="C",
                                         provenance="CARRIED")),
            R.ClaimRecord.from_dict(good(claim_id="D", provenance="DERIVED",
                                         operands=["C"], expression="C + 1")),
            R.ClaimRecord.from_dict(good(claim_id="E", provenance="DERIVED",
                                         operands=["D"], expression="D + 1"))]
    pw = engine.resolve_provenance(weak)
    ck("DERIVED on a CARRIED operand is DERIVED_WEAK, one hop",
       pw[("s", "D")][0] is R.Provenance.DERIVED_WEAK
       and "s:C (CARRIED)" in pw[("s", "D")][1])
    ck("weakness is transitive, two hops",
       pw[("s", "E")][0] is R.Provenance.DERIVED_WEAK
       and "s:C (CARRIED)" in pw[("s", "E")][1])
    absent = [R.ClaimRecord.from_dict(good(claim_id="F", provenance="DERIVED",
                                           operands=["gx:Z"],
                                           expression="gx:Z"))]
    pa = engine.resolve_provenance(absent)
    ck("an operand nobody can find is a weakness and is named",
       pa[("s", "F")][0] is R.Provenance.DERIVED_WEAK
       and "not in the record set" in pa[("s", "F")][1][0])


# ---------------------------------------------------------------- cobol

def cobol_checks():
    print("cobol arm")
    a = bridge.availability()
    ck("the cobol arm reports its state and its reason",
       isinstance(a.available, bool) and a.reason)
    if not a.available:
        ck("the reason names what is missing",
           "cobc" in a.reason or "LEDGER.cob" in a.reason, a.reason)

    enc = bridge.encode("-2.5")
    ck("encode is sign-leading-separate and fixed width",
       enc is not None and len(enc) == bridge.W_NUM and enc[0] == "-")
    ck("encode/decode round trips as a VALUE, not as a string",
       Decimal(bridge.decode(bridge.encode("123.456"))) == Decimal("123.456"))
    ck("a zero keeps its sign slot and decodes to zero",
       bridge.encode("0")[0] == "+"
       and Decimal(bridge.decode(bridge.encode("0"))) == 0)
    ck("a number too wide for the field is refused, not truncated",
       bridge.encode("1" + "0" * bridge.W_INT) is None)
    ck("digits below the field's scale are refused, not dropped",
       bridge.encode("0." + "0" * bridge.W_FRAC + "1") is None)
    ck("decode refuses a malformed field", bridge.decode("nope") is None)

    ops = bridge.to_ops("a + b * c", {"a": "1", "b": "2", "c": "3"})
    ck("to_ops emits postfix in evaluation order",
       [k for k, _ in ops] == ["PUSH", "PUSH", "PUSH", "MUL ", "ADD ",
                               "END "], [k for k, _ in ops])
    try:
        bridge.to_ops("abs(a)", {"a": "1"})
        ck("to_ops refuses a call", False)
    except bridge.Unflattenable:
        ck("to_ops refuses a call", True)
    ck("an op line is the declared width",
       len(bridge.op_line("s:A", 1, "PUSH", bridge.encode("1")))
       == bridge.OP_LEN)

    src = open(bridge.SOURCE, encoding="utf-8").read()
    ck("LEDGER.cob declares the same numeric field as bridge.py",
       "PIC S9(%d)V9(%d)" % (bridge.W_INT, bridge.W_FRAC) in src)
    ck("LEDGER.cob declares the same ref width",
       "PIC X(%d)" % bridge.W_REF in src)
    ck("LEDGER.cob refuses a zero divisor rather than returning a number",
       "DIV0" in src and 'IF B-VAL = ZERO' in src)
    man = json.load(open(os.path.join(HERE, "cobol_ledger", "MANIFEST.json"),
                         encoding="utf-8"))
    ck("the cobol manifest says the source has never been compiled",
       man.get("NEVER_COMPILED") is True)
    ck("the cobol manifest claims PRECISION and not REACHABILITY",
       man.get("authoritative_for") == "PRECISION")
    pman = json.load(open(os.path.join(HERE, "py_ledger", "MANIFEST.json"),
                          encoding="utf-8"))
    ck("the py manifest claims REACHABILITY and not PRECISION",
       pman.get("authoritative_for") == "REACHABILITY")
    ck("the py arm declares no dependencies", pman.get("dependencies") == [])

    out = bridge.run([])
    ck("an empty op stream is not reported as agreement",
       out.status in ("OK", "UNAVAILABLE") and not out.values)


# ------------------------------------------------------- the three diffs

def write_records(d, items):
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "r.json"), "w", encoding="utf-8").write(
        json.dumps(items, indent=1))


def run_on(recdir, expdir, **kw):
    recs, fails = R.load_records(recdir)
    return L.Run(recs, fails, expdir, "2026-01-01", **kw)


def diffs():
    print("the three diffs")
    base = tempfile.mkdtemp(prefix="ledger_selftest_")
    try:
        # ---- INTERNAL, both directions
        run = run_on(FIXTURES, os.path.join(base, "e0"))
        internal = {d["ref"] for d in run.internal}
        ck("INTERNAL fires on a claim that disagrees with its own operands",
           "fx:A_005" in internal, sorted(internal))
        ck("INTERNAL is silent on claims that agree",
           "fx:A_003" not in internal and "fx:A_004" not in internal
           and "gx:B_001" not in internal, sorted(internal))
        ck("INTERNAL is silent on a trailing-zeros rewrite",
           "fx:A_004" not in internal)
        ck("a bare operand resolves inside its own sim",
           "gx:B_001" not in internal,
           "gx:B_001 would disagree if the bare A_001 had resolved to fx")
        ck("the cycle members are reported, not recomputed",
           {"fx:C_001", "fx:C_002"}
           <= {d["ref"] for d in run.unrecomputable})
        ck("division by a measured zero is reported UNDEFINED",
           any(d["ref"] == "fx:A_010"
               and d["outcome"] == "UNDEFINED" for d in run.unrecomputable))
        ck("INTERNAL is reported first in the render",
           L.render(run).index("INTERNAL DISAGREEMENT")
           < L.render(run).index("DRIFT AGAINST EXPECTED"))

        # ---- DRIFT, both directions
        rd = os.path.join(base, "rec")
        ed = os.path.join(base, "exp")
        v1 = [good(claim_id="A_001", sim="t", value="2", precision=6),
              good(claim_id="A_002", sim="t", value="4", precision=6,
                   provenance="DERIVED", operands=["A_001"],
                   expression="A_001 * 2")]
        write_records(rd, v1)
        r1 = run_on(rd, ed)
        ck("a first run seeds and does not call it drift",
           r1.drift == [] and set(r1.seeded) == {"t:A_001", "t:A_002"})
        ck("a seeded pin says in those words that it is not verified",
           L.SEED_NOTE
           in open(L.expected_path(ed, "t", "A_001"), encoding="utf-8").read())
        ck("the pin records the date it was seeded",
           "seeded: 2026-01-01"
           in open(L.expected_path(ed, "t", "A_001"), encoding="utf-8").read())

        r2 = run_on(rd, ed)
        ck("a second run over unchanged records reports no drift",
           r2.drift == [] and r2.seeded == [])
        ck("and reports no new pins", r2.seeded == [])

        v2 = [good(claim_id="A_001", sim="t", value="3", precision=6),
              good(claim_id="A_002", sim="t", value="6", precision=6,
                   provenance="DERIVED", operands=["A_001"],
                   expression="A_001 * 2")]
        write_records(rd, v2)
        r3 = run_on(rd, ed)
        drifted = {d["ref"] for d in r3.drift}
        ck("DRIFT fires when a value moves away from its pin",
           drifted == {"t:A_001", "t:A_002"}, sorted(drifted))
        ck("a drift row names the basis it compared on",
           {d["basis"] for d in r3.drift} == {"ASSERTED", "RECOMPUTED"},
           [d["basis"] for d in r3.drift])
        ck("a drift row carries the pin's state and date",
           all(d["state"] == "SEEDED" and d["seeded"] == "2026-01-01"
               for d in r3.drift))

        # a NEW claim is seeded, not drift
        v3 = list(v2) + [good(claim_id="A_003", sim="t", value="9",
                              precision=6)]
        write_records(rd, v3)
        r4 = run_on(rd, ed)
        ck("a claim with no pin is seeded and is not drift",
           r4.seeded == ["t:A_003"]
           and "t:A_003" not in {d["ref"] for d in r4.drift})

        ck("--no-seed writes no pin",
           not os.path.exists(L.expected_path(os.path.join(base, "e2"), "t",
                                              "A_001")))
        run_on(rd, os.path.join(base, "e2"), seed=False)
        ck("--no-seed still reports the claims it did not pin",
           not os.path.isdir(os.path.join(base, "e2")))

        # append-only drift log
        log = os.path.join(base, "DRIFT.md")
        L.append_drift_log(log, r3)
        first = open(log, encoding="utf-8").read()
        L.append_drift_log(log, r3)
        second = open(log, encoding="utf-8").read()
        ck("the drift log is append-only",
           second.startswith(first) and len(second) > len(first))
        ck("a run with no drift writes nothing",
           (lambda before: (L.append_drift_log(log, r2),
                            open(log, encoding="utf-8").read() == before)[1])(
               second))

        # ---- CROSS-LEDGER, both directions, against a STUB
        print("  (cross-ledger firing direction uses a STUB; see the"
              " module docstring)")
        real_avail, real_run = bridge.availability, bridge.run
        try:
            bridge.availability = lambda: bridge.Availability(True, "STUB")
            bridge.run = lambda recs: bridge.CobolRun(
                "OK", "", {("fx", "A_003"): "10"}, {})
            s1 = run_on(FIXTURES, os.path.join(base, "e3"))
            ck("a cobol arm agreeing on a value raises nothing",
               s1.cross["status"] == "OK" and not s1.cross["disagree"])
            ck("a claim the cobol arm did not return is PRECISION_UNVERIFIED",
               "fx:A_007" in s1.cross["precision_unverified"])
            ck("CROSS_LEDGER does not fire on agreement",
               "CROSS_LEDGER" not in s1.fired())

            # Below the declared precision is not a disagreement. A ledger
            # firing here would report every arm's last guard digit.
            bridge.run = lambda recs: bridge.CobolRun(
                "OK", "", {("fx", "A_003"): "10.0000001"}, {})
            sq = run_on(FIXTURES, os.path.join(base, "e6"))
            ck("a difference below the declared precision is not a "
               "disagreement", "CROSS_LEDGER" not in sq.fired())

            bridge.run = lambda recs: bridge.CobolRun(
                "OK", "", {("fx", "A_003"): "10.5"}, {})
            s2 = run_on(FIXTURES, os.path.join(base, "e4"))
            ck("CROSS_LEDGER fires on a disagreement",
               "CROSS_LEDGER" in s2.fired())
            row = (s2.cross["disagree"] or [{}])[0]
            ck("a disagreement row carries both arms and picks neither",
               Decimal(row.get("py", "0")) == 10 and row.get("cobol") == "10.5")
            dis = os.path.join(base, "DIS.md")
            L.append_disagreements(dis, s2)
            text = open(dis, encoding="utf-8").read()
            ck("every disagreement found reaches the file",
               text.count("py `") == len(s2.cross["disagree"]))
            L.append_disagreements(dis, s2)
            ck("the disagreements file is append-only",
               open(dis, encoding="utf-8").read().startswith(text))
        finally:
            bridge.availability, bridge.run = real_avail, real_run

        a = bridge.availability()
        if not a.available:
            s3 = run_on(FIXTURES, os.path.join(base, "e5"))
            ck("an unavailable arm marks every claim PRECISION_UNVERIFIED",
               s3.cross["status"] == "UNAVAILABLE"
               and len(s3.cross["precision_unverified"]) == len(s3.records))
            ck("an unavailable arm is not reported as agreement",
               "no disagreement" not in L.render(s3))
            ck("CROSS_LEDGER does not fire when the arm is down",
               "CROSS_LEDGER" not in s3.fired())

        # ---- verdict and exit
        ck("a run with a diff fires", r3.fired() == ["DRIFT"], r3.fired())
        ck("a run with no diff fires nothing", r2.fired() == [])
        ck("falsifier_untested lists claims with no test",
           "t:A_001" in r2.falsifier_untested)
        clean = [good(claim_id="A_001", sim="u", value="1", precision=6,
                      falsifier_test="a test")]
        write_records(os.path.join(base, "u"), clean)
        ru = run_on(os.path.join(base, "u"), os.path.join(base, "eu"))
        ck("falsifier_untested is silent when a test is declared",
           ru.falsifier_untested == [])
    finally:
        shutil.rmtree(base, ignore_errors=True)


# -------------------------------------------------------------- the CLI

def cli():
    print("cli")
    base = tempfile.mkdtemp(prefix="ledger_cli_")
    try:
        p = subprocess.run(
            [sys.executable, os.path.join(HERE, "ledger.py"), "--selftest"],
            capture_output=True, text=True)
        ck("ledger.py refuses --selftest rather than exiting clean",
           p.returncode == 2 and "selftest_ledger.py" in p.stderr)

        empty = os.path.join(base, "none")
        os.makedirs(empty)
        p = subprocess.run(
            [sys.executable, os.path.join(HERE, "ledger.py"),
             "--records", empty, "--expected", os.path.join(base, "e")],
            capture_output=True, text=True)
        ck("an empty record set is refused, not reported clean",
           p.returncode == 2 and "REFUSED" in p.stderr)

        p = subprocess.run(
            [sys.executable, os.path.join(HERE, "ledger.py"),
             "--records", FIXTURES, "--expected", os.path.join(base, "e1"),
             "--no-log"], capture_output=True, text=True)
        ck("a fired diff exits nonzero", p.returncode == 1)
        ck("the render names the seed note once a pin is written",
           L.SEED_NOTE in p.stdout)

        p = subprocess.run(
            [sys.executable, os.path.join(HERE, "ledger.py"), "--choices"],
            capture_output=True, text=True)
        ck("every choice is printed",
           p.returncode == 0
           and all(c.split("]")[0] + "]" in p.stdout for c in L.CHOICES))
    finally:
        shutil.rmtree(base, ignore_errors=True)


# ------------------------------------------------------- structural rules

def structural():
    print("structural")
    src = {n: open(os.path.join(HERE, n), encoding="utf-8").read()
           for n in ("ledger.py", "record.py")}
    src["py_ledger/engine.py"] = open(
        os.path.join(HERE, "py_ledger", "engine.py"), encoding="utf-8").read()
    src["cobol_ledger/bridge.py"] = open(
        os.path.join(HERE, "cobol_ledger", "bridge.py"),
        encoding="utf-8").read()

    # No float() anywhere a CLAIM VALUE passes through. Read from the AST,
    # because a substring scan fires on the prose that refuses it -- three
    # sentences in these files contain the word.
    #
    # The scanned set is the ledger proper. review.py is deliberately not in
    # it: it divides line counts to get a ratio and it times a run, and
    # neither number is a claim value. The rule is about the path a claim
    # value takes, not about the character f-l-o-a-t.
    for name, text in src.items():
        calls = [n.func.id for n in ast.walk(ast.parse(text))
                 if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)]
        ck("no float() in %s" % name, "float" not in calls)
        ck("no eval() in %s" % name, "eval" not in calls)
        ck("no exec() in %s" % name, "exec" not in calls)

    # The ledger never promotes its own pin.
    tree = ast.parse(src["ledger.py"])
    we = [n for n in ast.walk(tree)
          if isinstance(n, ast.FunctionDef) and n.name == "write_expected"]
    ck("write_expected exists", len(we) == 1)
    body = ast.dump(we[0])
    ck("write_expected writes SEEDED", "'state: SEEDED\\n'" in body
       or "state: SEEDED" in body)
    ck("write_expected never writes CONFIRMED", "CONFIRMED" not in body)

    # It does not run sims and does not time anything. The scanned set is
    # the ledger proper; review.py is NOT in it and DOES time a run,
    # because ADDENDUM.md asks for the wall time of a full ledger run.
    # That is a different instrument answering a different question, and
    # saying so here is cheaper than a reader finding perf_counter in the
    # folder and reading it as drift.
    names = set()
    for text in src.values():
        for n in ast.walk(ast.parse(text)):
            if isinstance(n, ast.Attribute):
                names.add(n.attr)
            elif isinstance(n, ast.Name):
                names.add(n.id)
    for banned in ("perf_counter", "monotonic", "process_time", "clock"):
        ck("the ledger does not time anything (%s)" % banned,
           banned not in names)
    ck("nothing reaches for Popen", "Popen" not in names)
    # The rule is about WHAT is started, not about who imports subprocess.
    # ledger.py runs `git rev-parse` for the run log's commit anchor, which
    # is a read of the history and not a sim. Asserted from the argv
    # literal at each call site rather than from the import.
    for name, text in src.items():
        argv0 = []
        for n in ast.walk(ast.parse(text)):
            if isinstance(n, ast.Call) and getattr(n.func, "attr", "") \
                    == "run" and n.args:
                first = n.args[0]
                if isinstance(first, ast.List) and first.elts:
                    e = first.elts[0]
                    if isinstance(e, ast.Constant):
                        argv0.append(str(e.value))
                    else:
                        argv0.append("<computed>")
        if name == "ledger.py":
            ck("ledger.py starts git and nothing else",
               all(x == "git" for x in argv0), argv0)
        elif name == "cobol_ledger/bridge.py":
            ck("the bridge starts the compiler and the built program",
               all(x in ("<computed>", "git") or x.endswith("cobc")
                   for x in argv0) or argv0 == ["<computed>"] * len(argv0),
               argv0)
        else:
            ck("%s starts no process" % name, argv0 == [], argv0)

    # The plant: the AST scan has to be able to fire.
    planted = ast.parse("def f():\n    return float('1')\n")
    calls = [n.func.id for n in ast.walk(planted)
             if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)]
    ck("the float() scan fires on a plant", "float" in calls)

    readme = os.path.join(HERE, "README.md")
    ck("the README exists", os.path.isfile(readme))
    if os.path.isfile(readme):
        text = open(readme, encoding="utf-8").read()
        ck("the README says a seeded value is a pin, in those words",
           L.SEED_NOTE in text)
        for phrase in ("does not run sims", "does not time anything"):
            ck("the README states what it does not do (%s)" % phrase,
               phrase in text)



# ----------------------------------------------------- ADDENDUM.md review

def _runs(path, rows):
    with open(path, "w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps(r) + "\n")


def _run(date, cross="OK", machine="m1", cobc="GnuCOBOL 3.2",
         records=5, dis=0):
    return {"date": date, "machine": machine, "cobc_version": cobc,
            "records": records, "cross_ledger": cross, "disagreements": dis}


def review_checks():
    print("addendum review")
    c = V.criterion()
    ck("the criterion is read out of ADDENDUM.md, not retyped",
       c["ok"] and c["t3_weeks"] == 3 and c["t9_weeks"] == 9, c.get("problems"))
    ck("KEEP needs at least one disagreement by T+3",
       c["keep_min"] == 1 and c["keep_by_weeks"] == 3)
    ck("DROP needs zero disagreements by T+9",
       c["drop_max_disagreements"] == 0 and c["drop_by_weeks"] == 9)
    ck("exposure and UNDECIDED thresholds are both 3",
       c["exposure_min"] == 3 and c["undecided_below"] == 3)

    base = tempfile.mkdtemp(prefix="ledger_review_")
    try:
        # the criterion parser has to be able to fail
        bad = os.path.join(base, "BAD.md")
        open(bad, "w", encoding="utf-8").write("nothing useful here\n")
        cb = V.criterion(bad)
        ck("an unreadable criterion is refused, not guessed",
           not cb["ok"] and len(cb["problems"]) >= 4)
        vb = V.verdict("2027-01-01", addendum_path=bad)
        ck("and the verdict says so rather than computing one",
           vb["verdict"] == "CRITERION_UNREADABLE")

        rp = os.path.join(base, "RUNS.jsonl")
        ep = os.path.join(base, "EXPLAINED.jsonl")
        tp = os.path.join(base, "T0.txt")
        open(ep, "w").close()
        open(tp, "w").write("2026-01-01\n")     # the clock, started

        _runs(rp, [])
        v = V.verdict("2027-01-01", rp, ep, t0_path=tp)
        ck("no runs is UNDECIDED, not DROP",
           v["verdict"] == "UNDECIDED")

        _runs(rp, [_run("2026-01-01", cross="UNAVAILABLE", cobc=None),
                   _run("2026-01-02", cross="UNAVAILABLE", cobc=None),
                   _run("2026-01-03", cross="UNAVAILABLE", cobc=None),
                   _run("2026-01-04", cross="UNAVAILABLE", cobc=None)])
        v = V.verdict("2027-01-01", rp, ep, t0_path=tp)
        ck("an UNAVAILABLE arm contributes no exposure",
           v["verdict"] == "UNDECIDED" and v["exposure"]["completed"] == 0)
        ck("and the run says so in as many words",
           any("not a completed cross-ledger run" in w for w in v["why"]))

        _runs(rp, [_run("2026-01-01", machine="m1"),
                   _run("2026-01-02", machine="m2")])
        v = V.verdict("2027-01-01", rp, ep, t0_path=tp)
        ck("two completed runs is below the exposure floor",
           v["verdict"] == "UNDECIDED" and v["exposure"]["completed"] == 2)

        # DROP: zero disagreements, three machines, past T+9
        _runs(rp, [_run("2026-01-01", machine="m1"),
                   _run("2026-01-02", machine="m2"),
                   _run("2026-01-03", machine="m3")])
        v = V.verdict("2026-06-01", rp, ep, t0_path=tp)
        ck("DROP fires on zero disagreements over three machines past T+9",
           v["verdict"] == "DROP", v.get("why"))
        v = V.verdict("2026-01-10", rp, ep, t0_path=tp)
        ck("and does not fire before T+9",
           v["verdict"] == "NOT_YET_DUE", v["verdict"])

        # one disagreement, unclassified
        _runs(rp, [_run("2026-01-01", machine="m1", dis=1),
                   _run("2026-01-02", machine="m2"),
                   _run("2026-01-03", machine="m3")])
        v = V.verdict("2026-06-01", rp, ep, t0_path=tp)
        ck("an unclassified disagreement is UNDECIDED, not KEEP and not DROP",
           v["verdict"] == "UNDECIDED"
           and v["disagreements"]["unclassified"] == 1)

        # classified as a rounding-mode difference: excluded by name
        _runs(ep, [{"ref": "s:A", "run_date": "2026-01-01",
                    "explained_by": "ROUNDING_MODE",
                    "basis": "constructed for the selftest"}])
        v = V.verdict("2026-06-01", rp, ep, t0_path=tp)
        ck("a rounding-mode difference does not satisfy KEEP",
           v["verdict"] != "KEEP" and v["disagreements"]["unexplained"] == 0,
           v["verdict"])

        # classified UNEXPLAINED: the KEEP case
        _runs(ep, [{"ref": "s:A", "run_date": "2026-01-01",
                    "explained_by": "UNEXPLAINED",
                    "basis": "constructed for the selftest"}])
        v = V.verdict("2026-02-01", rp, ep, t0_path=tp)
        ck("KEEP fires on one unexplained disagreement past T+3",
           v["verdict"] == "KEEP", v["verdict"])

        # a classification with no basis is malformed, not accepted
        _runs(ep, [{"ref": "s:A", "explained_by": "UNEXPLAINED",
                    "basis": ""}])
        v = V.verdict("2026-06-01", rp, ep, t0_path=tp)
        ck("a classification with no basis is refused",
           v["verdict"] == "UNDECIDED"
           and "s:A" in v["disagreements"]["malformed"])

        # the clock
        open(ep, "w").close()
        _runs(rp, [_run("2026-01-01", records=0),
                   _run("2026-01-02", records=0),
                   _run("2026-01-03", records=0)])
        gone = os.path.join(base, "NO_T0.txt")
        v = V.verdict("2027-01-01", rp, ep, t0_path=gone)
        ck("with no T0 the verdict is CLOCK_NOT_STARTED",
           v["verdict"] == "CLOCK_NOT_STARTED"
           and v["clocks"]["t"] is None
           and v["clocks"]["t_any"] == "2026-01-01")
        ck("and it emits no review dates rather than order-date ones",
           v["dates"]["t3"] is None and v["dates"]["t9"] is None)

        # bulk
        b = V.bulk()
        ck("bulk measures ledger source against sim source",
           b["ledger_lines"] > 0 and b["sim_lines"] > 0 and b["ratio"] > 0)
        ck("bulk does not time unless asked", b["wall_seconds"] is None)
        b = V.bulk(with_time=True)
        ck("bulk times a full ledger run when asked and names the set",
           b["wall_seconds"] is not None and b["wall_over"])
    finally:
        shutil.rmtree(base, ignore_errors=True)

    # the addendum is never written by anything here
    for name in ("ledger.py", "review.py", "record.py", "selftest_ledger.py"):
        text = open(os.path.join(HERE, name), encoding="utf-8").read()
        writes = []
        for n in ast.walk(ast.parse(text)):
            if isinstance(n, ast.Call) and getattr(n.func, "id", "") == "open":
                mode = ""
                if len(n.args) > 1 and isinstance(n.args[1], ast.Constant):
                    mode = str(n.args[1].value)
                for kw in n.keywords:
                    if kw.arg == "mode" and isinstance(kw.value, ast.Constant):
                        mode = str(kw.value.value)
                if any(ch in mode for ch in "wax"):
                    tgt = n.args[0] if n.args else None
                    writes.append(getattr(tgt, "id", None)
                                  or getattr(tgt, "attr", None) or "?")
        ck("%s never opens ADDENDUM for writing" % name,
           "ADDENDUM" not in writes, writes)

    p = subprocess.run([sys.executable, os.path.join(HERE, "review.py"),
                        "--selftest"], capture_output=True, text=True)
    ck("review.py refuses --selftest", p.returncode == 2)

    p = subprocess.run([sys.executable, os.path.join(HERE, "review.py"),
                        "--record"], capture_output=True, text=True)
    ck("--record refuses a review with no override count",
       p.returncode == 2 and "REFUSED" in p.stderr)
    p = subprocess.run([sys.executable, os.path.join(HERE, "review.py"),
                        "--record", "--overrides", "0",
                        "--unique-findings", "0",
                        "--unique-findings-basis", "x"],
                       capture_output=True, text=True)
    ck("--record refuses a count with no basis",
       p.returncode == 2 and "basis" in p.stderr)

    ov = open(os.path.join(HERE, "OVERRIDES.md"), encoding="utf-8").read()
    ck("OVERRIDES.md exists and keeps UNRECORDED apart from 0",
       "UNRECORDED` is not `0`" in ov or "UNRECORDED is not 0" in ov
       or "`UNRECORDED` is not `0`" in ov)
    dm = open(os.path.join(HERE, "DISAGREEMENTS.md"), encoding="utf-8").read()
    ck("DISAGREEMENTS.md carries the T+3 and T+9 obligation",
       "T+3 and T+9" in dm and "zero reading is the result" in dm)

    # the run log the exposure count rests on
    base = tempfile.mkdtemp(prefix="ledger_runlog_")
    try:
        log = os.path.join(base, "reviews", "RUNS.jsonl")
        subprocess.run(
            [sys.executable, os.path.join(HERE, "ledger.py"),
             "--records", FIXTURES, "--expected", os.path.join(base, "e"),
             "--drift-log", os.path.join(base, "D.md"),
             "--disagreements", os.path.join(base, "X.md"),
             "--run-log", log], capture_output=True, text=True)
        rows, bad = V.read_jsonl(log)
        ck("a run writes one line to the run log", len(rows) == 1 and not bad)
        ck("and it carries the machine and the compiler version",
           "machine" in rows[0] and "cobc_version" in rows[0])
        ck("an unavailable arm is recorded as UNAVAILABLE, not as OK",
           rows[0]["cross_ledger"] in ("OK", "UNAVAILABLE"))
        subprocess.run(
            [sys.executable, os.path.join(HERE, "ledger.py"),
             "--records", FIXTURES, "--expected", os.path.join(base, "e"),
             "--run-log", log, "--no-log"], capture_output=True, text=True)
        rows, _ = V.read_jsonl(log)
        ck("--no-log writes no run line", len(rows) == 1)
    finally:
        shutil.rmtree(base, ignore_errors=True)


# --------------------------------------- the clock, and the second channel

def _git(base, *a):
    return subprocess.run(["git"] + list(a), cwd=base, capture_output=True,
                          text=True)


def _repo():
    base = tempfile.mkdtemp(prefix="ledger_git_")
    _git(base, "init", "-q", "-b", "main")
    _git(base, "config", "user.email", "t@t")
    _git(base, "config", "user.name", "t")
    os.makedirs(os.path.join(base, "ledger"))
    open(os.path.join(base, "ledger", "OVERRIDES.md"), "w").write("# O\n")
    os.makedirs(os.path.join(base, "sim"))
    open(os.path.join(base, "sim", "r.json"), "w").write("{}\n")
    _git(base, "add", "-A")
    _git(base, "commit", "-qm", "base")
    return base, _git(base, "rev-parse", "HEAD").stdout.strip()


def clock_checks():
    print("the clock")
    base = tempfile.mkdtemp(prefix="ledger_clock_")
    try:
        t0 = os.path.join(base, "T0.txt")
        ck("no T0 file is no clock", V.read_t0(t0) is None)
        c = V.criterion()
        d = V.review_dates(None, c)
        ck("with no T there are no review dates",
           d["t3"] is None and d["t9"] is None)
        ck("and the order-date pair is named as superseded",
           d["superseded"]["t3"] == "2026-10-07"
           and d["superseded"]["t9"] == "2026-11-18")
        d = V.review_dates("2026-10-01", c)
        ck("review dates are computed FROM T, three and nine weeks on",
           d["t3"] == "2026-10-22" and d["t9"] == "2026-12-03",
           (d["t3"], d["t9"]))
        ck("and they are not the order-date pair",
           d["t3"] != d["superseded"]["t3"]
           and d["t9"] != d["superseded"]["t9"])

        open(t0, "w").write("2026-10-01\n")
        ck("T0 is read back", V.read_t0(t0) == "2026-10-01")
        open(t0, "w").write("not a date\n")
        ck("a malformed T0 is no clock, not a guess", V.read_t0(t0) is None)

        open(t0, "w").write("2026-10-01\n")
        runs = [{"date": "2026-09-01", "records": 3, "all_constructed": False},
                {"date": "2026-10-01", "records": 3, "all_constructed": False}]
        cl = V.clocks(runs, t0)
        ck("T0 is the authority and the run log is the cross-check",
           cl["t"] == "2026-10-01" and cl["t_from_runs"] == "2026-09-01"
           and cl["disagree"] is True)
        runs = [{"date": "2026-10-01", "records": 3,
                 "all_constructed": False}]
        ck("agreement is not flagged",
           V.clocks(runs, t0)["disagree"] is False)
        runs = [{"date": "2026-09-01", "records": 3,
                 "all_constructed": True}]
        ck("a run over records that all declare CONSTRUCTED is not T",
           V.clocks(runs, t0)["t_from_runs"] is None)

        # ledger.py writes T0 once, and not on a fixture run
        rd = os.path.join(base, "rec")
        real = os.path.join(base, "T0real.txt")
        L.write_records(rd, [good(claim_id="A_001", sim="t", value="1",
                                  precision=6, status="MEASURED HERE")]) \
            if hasattr(L, "write_records") else write_records(
                rd, [good(claim_id="A_001", sim="t", value="1",
                          precision=6, status="MEASURED HERE")])
        run = run_on(rd, os.path.join(base, "e"))
        dates = L.write_t0(real, run)
        ck("a real-record run starts the clock", os.path.isfile(real)
           and dates and dates[0].startswith("T  = "))
        ck("and prints both review dates from T, once",
           len(dates) == 3 and dates[1].startswith("T+3 = ")
           and dates[2].startswith("T+9 = "))
        again = L.write_t0(real, run)
        ck("T0 is never overwritten", again is None
           and open(real, encoding="utf-8").read().strip()
           == run.today)

        fixture_run = run_on(FIXTURES, os.path.join(base, "e2"))
        ck("every fixture record declares itself CONSTRUCTED",
           L.all_constructed(fixture_run))
        fx_t0 = os.path.join(base, "T0fx.txt")
        ck("a fixture run does NOT start the clock",
           L.write_t0(fx_t0, fixture_run) is None
           and not os.path.exists(fx_t0))
        ck("and an empty record set does not either",
           L.write_t0(os.path.join(base, "T0e.txt"),
                      run_on(os.path.join(base, "empty"),
                             os.path.join(base, "e3"))) is None)
    finally:
        shutil.rmtree(base, ignore_errors=True)


def channel_checks():
    print("the second override channel")
    ok, root = V.git_reachable(HERE)
    ck("git reachability is reported, not assumed",
       isinstance(ok, bool) and root)

    base, red = _repo()
    side = tempfile.mkdtemp(prefix="ledger_runs_")
    try:
        # OUTSIDE the repo. A run log inside the work tree is checked away
        # by the branch switch below, and the channel then reports 0
        # overrides over 0 runs, which reads exactly like a clean history.
        runs = os.path.join(side, "RUNS.jsonl")

        def setrun(**over):
            row = {"date": "2026-01-01", "commit": red,
                   "flagged_paths": ["sim/r.json"],
                   "diffs_fired": ["INTERNAL"], "records": 1}
            row.update(over)
            open(runs, "w", encoding="utf-8").write(json.dumps(row) + "\n")

        setrun()
        r = V.override_inferred(runs, base)
        ck("a red with no later commit infers nothing",
           r["status"] == "OK" and r["inferred"] == 0)

        open(os.path.join(base, "sim", "r.json"), "w").write('{"x":1}\n')
        _git(base, "add", "-A")
        _git(base, "commit", "-qm", "changed the flagged file")
        r = V.override_inferred(runs, base)
        ck("a commit touching a flagged path with no OVERRIDES entry infers "
           "an override", r["inferred"] == 1 and r["logged"] == 0)
        ck("and the row names the red, the commit and the paths",
           r["rows"][0]["red_commit"] == red
           and r["rows"][0]["paths"] == ["sim/r.json"])

        _git(base, "checkout", "-q", red)
        _git(base, "checkout", "-q", "-b", "logged")
        open(os.path.join(base, "ledger", "OVERRIDES.md"), "a").write("- w\n")
        _git(base, "add", "-A")
        _git(base, "commit", "-qm", "log it")
        open(os.path.join(base, "sim", "r.json"), "w").write('{"x":2}\n')
        _git(base, "add", "-A")
        _git(base, "commit", "-qm", "changed the flagged file")
        r = V.override_inferred(runs, base)
        ck("an OVERRIDES entry in between infers nothing",
           r["inferred"] == 0 and r["logged"] == 1)

        setrun(commit=None)
        r = V.override_inferred(runs, base)
        ck("a red with no commit anchor is UNCORRELATABLE, not inferred and "
           "not clean",
           r["inferred"] == 0 and len(r["uncorrelatable"]) == 1)
        ck("and it says the anchor is what is missing",
           "no commit recorded" in r["uncorrelatable"][0]["why"])

        setrun(commit="0" * 40)
        r = V.override_inferred(runs, base)
        ck("a commit that is not an ancestor of HEAD is UNCORRELATABLE",
           r["inferred"] == 0 and len(r["uncorrelatable"]) == 1)

        setrun(flagged_paths=[])
        r = V.override_inferred(runs, base)
        ck("a red flagging no path is counted apart from one inferring "
           "nothing",
           r["inferred"] == 0 and len(r["no_flagged_paths"]) == 1)

        setrun(diffs_fired=[])
        r = V.override_inferred(runs, base)
        ck("a run that was not red is not a red", r["reds"] == 0)

        nogit = tempfile.mkdtemp(prefix="ledger_nogit_")
        try:
            r = V.override_inferred(runs, nogit)
            ck("git out of reach says so and stops",
               r["status"] == "GIT_UNREACHABLE" and r["inferred"] is None)
        finally:
            shutil.rmtree(nogit, ignore_errors=True)

        empty = os.path.join(side, "EMPTY.jsonl")
        open(empty, "w").close()
        r = V.override_inferred(empty, base)
        ck("an empty run log is NO_RUNS, not a clean history",
           r["status"] == "NO_RUNS" and r["inferred"] is None)
    finally:
        shutil.rmtree(base, ignore_errors=True)
        shutil.rmtree(side, ignore_errors=True)

    # the two counts are never combined
    text = open(os.path.join(HERE, "review.py"), encoding="utf-8").read()
    tree = ast.parse(text)
    mixed = []
    for n in ast.walk(tree):
        if isinstance(n, (ast.BinOp, ast.AugAssign)) or (
                isinstance(n, ast.Call)
                and getattr(n.func, "id", "") in ("sum", "max", "min")):
            seg = ast.get_source_segment(text, n) or ""
            low = seg.lower()
            if "overrides" in low and "inferred" in low:
                mixed.append(seg[:80])
    ck("the declared and inferred counts are never combined", not mixed,
       mixed)
    planted = ast.parse("x = args.overrides + oi['inferred']\n")
    hit = any(isinstance(n, ast.BinOp) for n in ast.walk(planted))
    ck("the never-combined scan fires on a plant", hit)

    ov = open(os.path.join(HERE, "OVERRIDES.md"), encoding="utf-8").read()
    for phrase in ("SELF-REPORTED", "indistinguishable from",
                   "FLOOR, not a measurement",
                   "UNRECORDED means no basis was declared, not"):
        ck("OVERRIDES.md states the floor (%s)" % phrase[:24], phrase in ov)


def main():
    print("ledger selftest")
    print("=" * 70)
    intake()
    engine_checks()
    cobol_checks()
    diffs()
    cli()
    review_checks()
    clock_checks()
    channel_checks()
    structural()
    print("=" * 70)
    print("checks: %d   failed: %d" % (CHECKS[0], len(FAILS)))
    for f in FAILS:
        print("  %s" % f)
    return 1 if FAILS else 0


if __name__ == "__main__":
    raise SystemExit(main())
