# test_tradeoff.py
# CC0 1.0 Universal / public domain dedication.
#
# Stdlib only, no pytest, no network. Run: python3 test_tradeoff.py
#
# Expected flag sets live HERE and not in cases.py, so no case can agree
# with the instrument by construction.

import ast
import os
import subprocess
import sys

import cases
import false_tradeoff as ft
from false_tradeoff import Horizon, TradeoffRead

CHECKS = []
HERE = os.path.dirname(os.path.abspath(__file__))


def check(name, condition, detail=""):
    CHECKS.append((name, bool(condition), detail))


READS = {d.statement: ft.read(d) for d in cases.CASES}


def flags(statement):
    return set(READS[statement]["flags"])


T = "T diverted or not diverted"
M = "M upkeep against quarter cost"
B = "B outlay against exposure"
G = "G one reservoir two draws"
R = "R filing window against review"
I = "I stated, not structured"
X = "X both artifacts at once"
U = "U a defect the flags cannot say"
P = "P stipulated with one derived"

EXPECTED = {
    T: {TradeoffRead.STIPULATED_OPTION_SET},
    M: {TradeoffRead.DEFERRAL_ARTIFACT},
    B: {TradeoffRead.BOUNDARY_ARTIFACT},
    G: {TradeoffRead.GENUINE_TRADEOFF},
    R: {TradeoffRead.RULE_BOUND},
    I: {TradeoffRead.INSUFFICIENT},
    X: {TradeoffRead.BOUNDARY_ARTIFACT, TradeoffRead.DEFERRAL_ARTIFACT},
    U: {TradeoffRead.GENUINE_TRADEOFF},
    P: {TradeoffRead.GENUINE_TRADEOFF},
}


# ---------------------------------------------------------------------------
# 1. every enum member reachable, and every case resolves as marked
# ---------------------------------------------------------------------------

produced = set()
for r in READS.values():
    produced.update(r["flags"])
for member in TradeoffRead:
    hits = [s for s in READS if member in flags(s)]
    check("reachable: %s" % member.name, hits,
          "cases: %s" % ", ".join(hits) if hits else "NO CASE PRODUCES THIS")
check("no member is declared and unpopulated", produced == set(TradeoffRead),
      "%d of %d" % (len(produced), len(list(TradeoffRead))))

for statement, expected in EXPECTED.items():
    got = flags(statement)
    check("case %r resolves as marked" % statement[:24], got == expected,
          "expected %s, got %s" % (sorted(f.name for f in expected),
                                   sorted(f.name for f in got)))

check("at least 6 hand-built cases", len(cases.CASES) >= 6,
      "%d cases" % len(cases.CASES))


# ---------------------------------------------------------------------------
# 2. THE CRITICAL FALSIFIER. case G is GENUINE_TRADEOFF and nothing else,
#    and it really is the case section 5 describes.
# ---------------------------------------------------------------------------

check("FALSIFIER: case G returns GENUINE_TRADEOFF",
      TradeoffRead.GENUINE_TRADEOFF in flags(G))
check("FALSIFIER: case G returns it ALONE", flags(G) == {TradeoffRead.GENUINE_TRADEOFF},
      "got %s" % sorted(f.name for f in flags(G)))
check("FALSIFIER: and case G is the case section 5 specifies",
      cases.CASE_G.horizon_a.days() == cases.CASE_G.horizon_b.days()
      and cases.CASE_G.boundary_a == cases.CASE_G.boundary_b
      and any(c.kind is cases.PHYS for c in cases.CASE_G.constraints)
      and cases.CASE_G.conserved_quantity,
      "same horizon, one declared boundary, a PHYSICAL eliminating "
      "constraint, and a named conserved quantity")
check("GENUINE_TRADEOFF never co-fires with another flag",
      all(f == {TradeoffRead.GENUINE_TRADEOFF}
          for f in (flags(s) for s in READS)
          if TradeoffRead.GENUINE_TRADEOFF in f))
check("GENUINE_TRADEOFF and INSUFFICIENT are mutually exclusive",
      not any(TradeoffRead.GENUINE_TRADEOFF in f and TradeoffRead.INSUFFICIENT in f
              for f in (flags(s) for s in READS)))
check("the instrument does not dissolve every dilemma",
      any(f == {TradeoffRead.GENUINE_TRADEOFF} for f in (flags(s) for s in READS))
      and any(f and TradeoffRead.GENUINE_TRADEOFF not in f
              for f in (flags(s) for s in READS)),
      "both outcomes occur on the shipped set")


# ---------------------------------------------------------------------------
# 3. no function ranks, scores, or weights a side
# ---------------------------------------------------------------------------

FORBIDDEN = {
    "rank", "ranks", "ranking", "ranked", "score", "scores", "scoring",
    "weight", "weights", "weighted", "weighting", "prefer", "preference",
    "preferred", "better", "worse", "best", "worst", "utility", "priority",
    "severity", "confidence", "recommend", "recommendation", "favour",
    "favor", "winner", "wins", "ought", "merit", "importance",
}


def split_identifier(name):
    parts = []
    for chunk in name.split("_"):
        current = ""
        for ch in chunk:
            if ch.isupper() and current:
                parts.append(current)
                current = ch
            else:
                current += ch
        if current:
            parts.append(current)
    return [p.lower() for p in parts if p]


def valuation_tokens(source_text):
    """Identifiers and dict-literal keys only.

    Not a substring scan over the raw file: the module and README have to
    be able to NAME what they refuse, and a substring scan fires on the
    sentence saying they are refused. Comments and free docstrings are
    not in the AST at all; dict keys are, because a field name is a field
    name whether it is an attribute or a string key.
    """
    hits = []
    for node in ast.walk(ast.parse(source_text)):
        found = []
        if isinstance(node, ast.Name):
            found = [node.id]
        elif isinstance(node, ast.Attribute):
            found = [node.attr]
        elif isinstance(node, ast.arg):
            found = [node.arg]
        elif isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            found = [node.name]
        elif isinstance(node, ast.keyword) and node.arg:
            found = [node.arg]
        elif isinstance(node, ast.Dict):
            found = [k.value for k in node.keys
                     if isinstance(k, ast.Constant) and isinstance(k.value, str)]
        for name in found:
            for token in split_identifier(name):
                if token in FORBIDDEN:
                    hits.append((name, token))
    return hits


for path in ("false_tradeoff.py", "cases.py"):
    hits = valuation_tokens(open(os.path.join(HERE, path)).read())
    check("no valuation-named field in %s" % path, not hits,
          "found %s" % hits if hits else "0 identifiers or keys match")

check("the valuation checker fires on a plant",
      len(valuation_tokens(
          "def f():\n    side_score = 1\n    return {'preferred_side': side_score}\n")) >= 2)
check("the valuation checker does not fire on a near-miss token",
      not valuation_tokens("window = 1\nbetterment_note = 2\nmeritocracy = 3\n"),
      "token-split matching, not substring")

# the structural form of the same rule: A and B are interchangeable.
for statement, d in ((d.statement, d) for d in cases.CASES):
    swapped = ft.read(ft.swap_sides(d))
    check("swapping sides does not move the flags: %s" % statement[:24],
          set(swapped["flags"]) == flags(statement),
          "%s vs %s" % (sorted(f.name for f in swapped["flags"]),
                        sorted(f.name for f in flags(statement))))

check("every returned flag is a TradeoffRead member, never a side",
      all(isinstance(f, TradeoffRead) for r in READS.values() for f in r["flags"]))
check("DECLARATION states it does not resolve tradeoffs",
      ft.DECLARATION["resolves_tradeoffs"] is False
      and ft.DECLARATION["scalar_collapse"] is False)
check("DECLARATION lists every return",
      ft.DECLARATION["returns"] == [m.name for m in TradeoffRead])
check("DECLARATION names the four axes",
      ft.DECLARATION["axes"] == ["option_provenance", "constraint_kind",
                                 "boundary_overlap", "horizon_mismatch"])
check("no confidence score anywhere in the record",
      not any("confidence" in repr(r) for r in READS.values()),
      "scanned over the whole record, not only its top-level keys")


# ---------------------------------------------------------------------------
# 4. UNSTATED constraints are reported and are not smoothed over
# ---------------------------------------------------------------------------

check("an UNSTATED constraint is reported in the record",
      len(READS[T]["unstated_constraint_defects"]) == 2
      and len(READS[U]["unstated_constraint_defects"]) == 1)
check("case U carries a defect and no flag can say so",
      READS[U]["unstated_constraint_defects"]
      and flags(U) == {TradeoffRead.GENUINE_TRADEOFF},
      "the defect the order names most sharply has no enum member; it is "
      "in the record and absent from the flag set")
check("a clean case carries no defect",
      READS[G]["unstated_constraint_defects"] == [])


# ---------------------------------------------------------------------------
# 5. absent is not clean
# ---------------------------------------------------------------------------

partial = ft.dilemma(
    "partial", options=cases.CASE_G.options, side_a="a", side_b="b",
    constraints=cases.CASE_G.constraints,
    boundary_a={"x"}, boundary_b={"x"},
    horizon_a=Horizon(1, "year"), horizon_b=Horizon(1, "year"),
    deferred_costs=[],
)
pr = ft.read(partial)
check("a missing dependency set is NOT_EVALUABLE, not a silent pass",
      pr["checks"]["boundary_cut"]["state"] == ft.NOT_EVALUABLE
      and pr["checks"]["boundary_cut"]["fired"] is False
      and TradeoffRead.INSUFFICIENT in set(pr["flags"])
      and TradeoffRead.GENUINE_TRADEOFF not in set(pr["flags"]),
      "an unrunnable check cannot buy a genuine reading")
check("INSUFFICIENT names which field is missing",
      pr["intake_missing"] == ["boundary_cut.depends_a", "boundary_cut.depends_b"],
      "%s" % pr["intake_missing"])
check("a fully unsupplied dilemma is INSUFFICIENT alone",
      flags(I) == {TradeoffRead.INSUFFICIENT})

# [CHOICE 4]: INSUFFICIENT joins whatever did evaluate rather than
# replacing it. The exclusive reading is recoverable from the record.
half_T = cases.CASE_T._replace(depends_a=None, depends_b=None)
hr = ft.read(half_T)
check("INSUFFICIENT co-fires with a check that did run",
      set(hr["flags"]) == {TradeoffRead.STIPULATED_OPTION_SET,
                           TradeoffRead.INSUFFICIENT},
      "got %s" % sorted(f.name for f in hr["flags"]))
check("the exclusive reading is recoverable from the record",
      hr["intake_missing"] and not READS[T]["intake_missing"],
      "intake_missing is empty exactly when every check ran")

empty_constraints = cases.CASE_G._replace(constraints=[])
er = ft.read(empty_constraints)
check("RULE_BOUND does not fire on an empty constraint list",
      TradeoffRead.RULE_BOUND not in set(er["flags"])
      and er["checks"]["branch_back"]["no_constraints"] is True,
      "all([]) is True; a dilemma held by nothing is not held by permission")
check("RULE_BOUND does fire when every constraint is RULE",
      TradeoffRead.RULE_BOUND in flags(R),
      "so the guard above is not silencing the check")
check("a constraint list absent and a constraint list empty differ",
      ft.read(cases.CASE_G._replace(constraints=None))["checks"]
      ["branch_back"]["state"] == ft.NOT_EVALUABLE
      and er["checks"]["branch_back"]["state"] == "SILENT")


# ---------------------------------------------------------------------------
# 6. CHECK 3 needs a field section 2 does not supply
# ---------------------------------------------------------------------------

demo = ft.boundary_as_dependency_is_silent()
check("reading the boundary as the dependency set makes CHECK 3 silent",
      demo["ever_fired"] == 0 and demo["trials"] > 0,
      "%d of %d trials fire; the check could never report an artifact"
      % (demo["ever_fired"], demo["trials"]))
check("with a separate dependency set the check does fire",
      TradeoffRead.BOUNDARY_ARTIFACT in flags(B)
      and READS[B]["checks"]["boundary_cut"]["cut_runs_through"] == ["crew"],
      "%s" % READS[B]["checks"]["boundary_cut"]["cut_runs_through"])
check("an entity both sides depend on and both ledgers count does not fire",
      READS[M]["checks"]["boundary_cut"]["shared_dependencies"] == ["pump_station"]
      and READS[M]["checks"]["boundary_cut"]["fired"] is False)


# ---------------------------------------------------------------------------
# 7. horizons are compared on one scale, not as prose
# ---------------------------------------------------------------------------

check("a quarter and three months are the same horizon",
      Horizon(1, "quarter").days() == Horizon(3, "month").days(),
      "string equality would call these different")
raised = False
try:
    Horizon(1, "fortnight").days()
except ft.UnregisteredUnit:
    raised = True
check("an unregistered unit raises rather than defaulting", raised)
check("DEFERRAL_ARTIFACT needs the cost inside the same side's boundary",
      TradeoffRead.DEFERRAL_ARTIFACT not in set(ft.read(
          cases.CASE_M._replace(boundary_a=frozenset({"operating_budget"})))["flags"]),
      "a cost landing outside A's own ledger is not A's deferral")
check("DEFERRAL_ARTIFACT needs the cost beyond the horizon",
      TradeoffRead.DEFERRAL_ARTIFACT not in set(ft.read(
          cases.CASE_M._replace(horizon_a=Horizon(20, "year")))["flags"]))
check("the return is a set, not a winner",
      flags(X) == {TradeoffRead.BOUNDARY_ARTIFACT, TradeoffRead.DEFERRAL_ARTIFACT},
      "two flags, no ordering between them")


# ---------------------------------------------------------------------------
# 8. the two clauses of CHECK 1, and the conserved quantity
# ---------------------------------------------------------------------------

check("CHECK 1's second clause is not independent of its first",
      READS[P]["checks"]["option_set_provenance"]["no_observed_option"] is True
      and READS[P]["checks"]["option_set_provenance"]["fired"] is False,
      "no option was observed and the rule as written is silent, because "
      "one option is DERIVED")
check("the conserved quantity is reported and gates nothing",
      ft.check_conserved_is_not_gated()["gated"] is False
      and READS[U]["conserved_quantity"] is None
      and flags(U) == {TradeoffRead.GENUINE_TRADEOFF},
      "case U names no conserved quantity and still reads GENUINE")


# ---------------------------------------------------------------------------
# 9. the module's own entry point, run as a script
# ---------------------------------------------------------------------------

proc = subprocess.run([sys.executable, "false_tradeoff.py"], cwd=HERE,
                      stdout=subprocess.PIPE, stderr=subprocess.PIPE)
out = proc.stdout.decode()
row = [ln for ln in out.splitlines() if ln.startswith("T diverted")]
check("running the module as a script reports case T as stipulated",
      proc.returncode == 0 and row and "STIPULATED_OPTION_SET" in row[0],
      "the script path imports the module by name; binding it as __main__ "
      "builds a second copy of every Enum and silences CHECK 1 and CHECK 2")
check("running it as a script does not report case T as genuine",
      row and "GENUINE" not in row[0], "%s" % (row[0] if row else "no row"))

refuse = subprocess.run([sys.executable, "false_tradeoff.py", "--selftest"],
                        cwd=HERE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
check("the module refuses --selftest and names where the checks live",
      refuse.returncode == 2 and b"test_tradeoff.py" in refuse.stderr,
      "an invocation that runs nothing must not exit 0")


# ---------------------------------------------------------------------------
# 10. the case set carries structure only
# ---------------------------------------------------------------------------

precomputed = []
for d in cases.CASES:
    for field in d._fields:
        if set(split_identifier(field)) & {"flag", "flags", "expected",
                                           "verdict", "read", "result"}:
            precomputed.append((d.statement, field))
check("no case carries an expected flag set", not precomputed,
      "%s" % precomputed if precomputed else
      "expected sets live in this test file")
check("the statement string is carried and read by nothing",
      not any(isinstance(n, ast.Attribute) and n.attr == "statement"
              for fn in ("check_option_provenance", "check_branch_back",
                         "check_boundary_cut", "check_horizon_deferral")
              for n in ast.walk(next(
                  x for x in ast.parse(open(os.path.join(
                      HERE, "false_tradeoff.py")).read()).body
                  if isinstance(x, ast.FunctionDef) and x.name == fn))),
      "no check reads the prose")


# ---------------------------------------------------------------------------

failed = [c for c in CHECKS if not c[1]]
for name, ok, detail in CHECKS:
    print("%-6s %s%s" % ("ok" if ok else "FAIL", name,
                         ("\n         %s" % detail) if detail and not ok else ""))
print()
print("%d checks, %d failed" % (len(CHECKS), len(failed)))
sys.exit(1 if failed else 0)
