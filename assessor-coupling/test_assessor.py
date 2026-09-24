# SPDX-License-Identifier: CC0-1.0
# test_assessor.py -- checks for assessor-coupling. Stdlib only, no pytest,
# no network. Run: python3 test_assessor.py
#
# Expected values live HERE and in no module under test. What is checked is
# the parser against the delivered order, the scorer's arithmetic on
# CONSTRUCTED arrangements, and what the delivered precedent record can and
# cannot bound. Nothing below is a statement about any organization,
# assessor, regulator or sector, and no party is scored anywhere.

import ast
import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, "sheet-structure-scan"))

import conditions as cond            # noqa: E402
import precedent as prec             # noqa: E402
import no_severity                   # noqa: E402

CHECKS = []


def ok(name, c, detail=""):
    CHECKS.append((name, bool(c), detail))


def close(x, y, tol=1e-9):
    return x is not None and y is not None and abs(x - y) <= tol


def raises(exc, fn, *a, **k):
    try:
        fn(*a, **k)
    except exc:
        return True
    except Exception:
        return False
    return False


WO = os.path.join(HERE, "WORK_ORDER.md")
# the delivered order is a .md and carries en/em dashes; the ASCII rule is a
# rule about .py files. Containment is checked whitespace-flattened because
# the order wraps its lines.
_wo = open(WO, encoding="utf-8").read()
_WO_FLAT = " ".join(_wo.split())
ok("WORK_ORDER.md present and is the assessor-coupling WO-6",
   os.path.exists(WO) and "WO-6" in _wo
   and "Assessor" in _wo.splitlines()[0])

# --- the ordinal collision is recorded, not resolved by overwriting -------

_other = os.path.join(ROOT, "criterion-externality", "WORK_ORDER.md")
ok("the other WO-6 already in the tree is untouched and different",
   os.path.exists(_other)
   and open(_other, encoding="utf-8").read() != _wo)
ok("the other WO-6 is a different subject",
   "FOURTH INDEPENDENCE AXIS"
   in open(_other, encoding="utf-8").read())

# --- conditions parsed, not retyped --------------------------------------

cs = cond.conditions()
ok("the order's block yields eight conditions", len(cs) == 8,
   "got %d" % len(cs))
ok("they are numbered 1..8 in order",
   [c.n for c in cs] == list(range(1, 9)))
for c in cs:
    ok("condition %d's title is contained in the order" % c.n,
       c.title in _WO_FLAT)
ok("condition 8 is the one with no gloss line",
   [c.n for c in cs if not c.gloss] == [8])

_lits = []
for fn in ("conditions.py", "precedent.py"):
    tree = ast.parse(open(os.path.join(HERE, fn), encoding="ascii").read())
    _lits += [n.value for n in ast.walk(tree)
              if isinstance(n, ast.Constant) and isinstance(n.value, str)]
_LIT_FLAT = " ".join(" ".join(s.split()) for s in _lits)
ok("no condition title is retyped as a literal in the modules",
   not any(c.title in _LIT_FLAT for c in cs))

_tmp = os.path.join(tempfile.mkdtemp(), "empty.md")
open(_tmp, "w", encoding="utf-8").write("# not the order\n")
ok("a document with no conditions block raises",
   raises(cond.OrderUnparsed, cond.conditions, _tmp))
ok("a document with no precedent record raises",
   raises(cond.OrderUnparsed, prec.cases, _tmp))

# --- hop-1 never enters the independence vector [CHOICE 1] ---------------

_tree = ast.parse(open(os.path.join(HERE, "conditions.py"),
                       encoding="ascii").read())
_score = [n for n in ast.walk(_tree)
          if isinstance(n, ast.FunctionDef) and n.name == "score"]
ok("score() is defined once", len(_score) == 1)
_names = set()
for n in ast.walk(_score[0]):
    if isinstance(n, ast.Attribute):
        _names.add(n.attr)
    if isinstance(n, ast.Name):
        _names.add(n.id)
ok("score() never reads a hop-1 field",
   not any("hop1" in x for x in _names), repr(sorted(_names)))

_a = cond.arrangement("a", {1: cond.PASSES}, cond.PASSES, "constructed")
_b = cond.arrangement("b", {1: cond.PASSES}, cond.FAILS, "constructed")
ok("two arrangements differing only in hop-1 score identically",
   cond.score(_a) == cond.score(_b)
   and cond.counts(cond.score(_a)) == cond.counts(cond.score(_b)))
ok("the report carries hop-1 and marks it unscored",
   cond.report(_a)["hop1_payment"] == cond.PASSES
   and cond.report(_a)["hop1_scored"] is False)

# --- the four states, and all of them reachable --------------------------

ctl = cond.controls()
seen = set()
for arr in ctl:
    seen |= set(cond.score(arr).values())
ok("every declared state is reached by a control",
   seen == set(cond.STATES), repr(sorted(seen)))
ok("an all-pass arrangement exists, so the scorer is not constant",
   any(cond.counts(cond.score(a))[cond.PASSES] == 8 for a in ctl))
ok("an arrangement declaring nothing scores eight UNDECLARED, not eight "
   "fails [CHOICE 3]",
   cond.counts(cond.score(ctl[3]))[cond.UNDECLARED] == 8)
ok("counts carry their denominator [CHOICE 4]",
   cond.counts(cond.score(ctl[0]))["denominator"] == 8)
ok("the arrangement schema has no field for a party's name",
   "name" not in cond.Arrangement._fields
   and not any("name" in f for f in cond.Arrangement._fields))
ok("an arrangement with no stated basis is refused",
   raises(ValueError, cond.arrangement, "x", {1: cond.PASSES},
          cond.UNDECLARED, ""))
ok("a state outside the declared set is refused",
   raises(ValueError, cond.arrangement, "x", {1: "GOOD"},
          cond.UNDECLARED, "b"))
ok("a hop-1 value outside the declared set is refused",
   raises(ValueError, cond.arrangement, "x", {1: cond.PASSES}, "MAYBE",
          "b"))

# --- the order's own reading of the current position ---------------------

vec = cond.stated_position()
ok("the current-position section parses to six fails",
   sorted(n for n in vec if vec[n] == cond.FAILS) == [3, 4, 5, 6, 7, 8],
   repr(vec))
ok("condition 2 is UNVERIFIABLE_AS_STATED, not a fail [CHOICE 2]",
   vec[2] == cond.UNVERIFIABLE_AS_STATED)
ok("condition 1 is UNDECLARED -- the section does not mention it",
   vec[1] == cond.UNDECLARED)
ok("no condition is scored as passing in that reading",
   cond.counts(vec)[cond.PASSES] == 0)
ok("the one property the order records as stated is hop-1",
   cond.hop1_stated() is True)
ok("and hop-1 is not a member of the eight, so it moves nothing",
   6 == cond.counts(vec)[cond.FAILS]
   and all("pay" not in c.title.lower() for c in cs))

# --- pool_fraction -------------------------------------------------------

ok("every source coupled is 1.0",
   close(cond.pool_fraction([(10.0, True), (30.0, True)]), 1.0))
ok("a quarter coupled is 0.25",
   close(cond.pool_fraction([(10.0, True), (30.0, False)]), 0.25))
ok("declared and uncoupled is 0.0, a measurement",
   cond.pool_fraction([(10.0, False), (30.0, False)]) == 0.0)
ok("an empty record is None, not 0.0", cond.pool_fraction([]) is None)
ok("an UNDECLARED source is None, not 0.0",
   cond.pool_fraction([(10.0, True), (30.0, cond.UNDECLARED)]) is None)
ok("a record summing to zero is None",
   cond.pool_fraction([(0.0, True)]) is None)

ok("field_distribution refuses a set not declared complete [CHOICE 5]",
   raises(cond.SelectiveApplication, cond.field_distribution,
          {"x": [(1.0, True)]}))
_d = cond.field_distribution({"x": [(1.0, True)], "y": [(1.0, False)],
                              "z": []}, complete_field=True)
ok("a declared-complete field returns a distribution with its undetermined "
   "count kept apart",
   _d["n"] == 3 and _d["determined"] == 2 and _d["not_determinable"] == 1)
ok("the distribution is values, and the per-id map is beside it, not a rank",
   _d["values"] == [0.0, 1.0] and set(_d["by_id"]) == {"x", "y"})

# --- the precedent record ------------------------------------------------

pc = prec.cases()
ok("the record parses to ten cases", len(pc) == 10, "got %d" % len(pc))
ok("across three eras", len(set(c.era for c in pc)) == 3)
for c in pc:
    ok("case lead %r is contained in the order" % c.lead,
       c.lead and c.lead in _WO_FLAT)
ok("no case lead is retyped as a literal in the modules",
   not any(c.lead in _LIT_FLAT for c in pc))
ok("the prior-defense list is four items",
   len(prec.prior_defense()) == 4)
ok("the non-financial coupling list is five items",
   len(prec.non_financial_couplings()) == 5)
ok("the prior-defense section is not read as a precedent era",
   not any(c.era.lower().startswith("the common prior defense")
           for c in pc))

# --- what the record can and cannot bound --------------------------------

d = prec.defense_discrimination()
ok("the delivered record cannot evaluate the prior defense",
   d["state"] == prec.NOT_EVALUABLE and d["reason"] == "selected_on_outcome")
ok("and the reason is a count, not an opinion: the negative arm is zero",
   d["not_failed"] == 0 and d["failed"] == len(pc))
ok("discrimination is None, not zero", d["discrimination"] is None)

_neg = [{"failed": True}, {"failed": True}, {"failed": False}]
_e = prec.defense_discrimination(corpus=_neg)
ok("a corpus carrying a negative arm returns a figure, so NOT_EVALUABLE is "
   "a property of the delivered corpus and not of the check [CHOICE 7]",
   _e["state"] == prec.EVALUABLE and close(_e["discrimination"], 2 / 3.0))

sel = prec.selection_declared()
ok("the order declares the record illustrative and not systematic",
   all(sel.values()), repr(sel))
t = prec.finding_vs_scope()
ok("the record's summary sentence is present verbatim",
   t["summary_present"] is True)
ok("the summary sentence and the scope limit are in tension",
   t["in_tension"] is True)
ok("the supported reading is scoped to the selected cases",
   "selected cases" in t["supported_reading"])
ok("the order's own step 2 is named as what would settle it",
   "step 2" in t["step_named_by_order"])

# --- condition 6 ---------------------------------------------------------

c6 = prec.condition_six_position()
ok("the earliest entry in the record is a personal-liability remedy",
   c6["earliest_case_is_personal_liability"] is True)
ok("the order records condition 6 as least discussed now",
   c6["order_calls_it_least_discussed"] is True)
ok("and the current-position reading has it failing",
   c6["current_position_state"] == cond.FAILS)

# --- step 4 and step 5 ---------------------------------------------------

ok("step 4 is NOT_RUN with the reason stated",
   prec.STEP4["run"] is False and "reachable" in prec.STEP4["reason"])
ok("step 5 is NOT_RUN with the reason stated",
   prec.STEP5["run"] is False and "blind" in prec.STEP5["reason"])
_inst = prec.disclosure_coverage({2: True})
ok("a disclosure instrument mentioning one condition leaves the rest "
   "UNDECLARED, not absent [CHOICE 3]",
   _inst[2] is True
   and sum(1 for v in _inst.values() if v == cond.UNDECLARED) == 7)
ok("a coverage value outside the declared set is refused",
   raises(ValueError, prec.disclosure_coverage, {2: "yes"}))

# --- companions ----------------------------------------------------------

ok("WO-1, WO-4 and WO-5 resolve by folder plus content marker [CHOICE 8]",
   prec.companions() == {"WO-1": "RESOLVED", "WO-4": "RESOLVED",
                         "WO-5": "RESOLVED"}, repr(prec.companions()))
ok("a companion whose folder is absent reads ABSENT, not RESOLVED",
   prec.companion_state("WO-1", root=os.path.join(HERE, "samples"))
   == "ABSENT")

# --- the screen ----------------------------------------------------------

for fn, txt in (("conditions", cond.render()), ("precedent", prec.render())):
    clean, hits = no_severity.check(txt)
    ok("%s render screens clean with no exemption" % fn, clean,
       repr(hits[:3]))
_pc, _ph = no_severity.check("this arrangement is wrong and the finding is "
                             "invalid")
ok("the screen fires on a planted token", (not _pc) and bool(_ph))

# --- CLI contract --------------------------------------------------------

for fn in ("conditions.py", "precedent.py"):
    p = subprocess.run([sys.executable, os.path.join(HERE, fn),
                        "--selftest"], capture_output=True)
    ok("%s refuses --selftest with exit 2" % fn, p.returncode == 2)
    ok("%s names this test file in its refusal" % fn,
       b"test_assessor.py" in p.stderr)
    p = subprocess.run([sys.executable, os.path.join(HERE, fn)],
                       capture_output=True)
    ok("%s bare invocation renders and exits 0" % fn,
       p.returncode == 0 and len(p.stdout) > 200)
    p = subprocess.run([sys.executable, os.path.join(HERE, fn), "--choices"],
                       capture_output=True)
    ok("%s prints its choices" % fn,
       p.returncode == 0 and b"[CHOICE" in p.stdout)

_declared = sorted(list(cond.CHOICES) + list(prec.CHOICES))
ok("the choice numbers are 1..8 with no collision across the two modules",
   _declared == list(range(1, 9)), repr(_declared))
_srclines = []
for _f in ("conditions.py", "precedent.py"):
    for _ln in open(os.path.join(HERE, _f),
                    encoding="ascii").read().splitlines():
        if not re.match(r"^\s*\d+:\s", _ln):
            _srclines.append(_ln)
_SRC = "\n".join(_srclines)
ok("every declared choice is cited at a site outside its own declaration",
   all(("[CHOICE %d]" % n) in _SRC for n in _declared),
   repr([n for n in _declared if ("[CHOICE %d]" % n) not in _SRC]))

# --- ASCII, and the README -----------------------------------------------

for fn in ("conditions.py", "precedent.py", "test_assessor.py"):
    raw = open(os.path.join(HERE, fn), "rb").read()
    ok("%s is ASCII" % fn, all(b < 128 for b in raw))

README = os.path.join(HERE, "README.md")
ok("README.md present", os.path.exists(README))
if os.path.exists(README):
    _rd = open(README, encoding="utf-8").read()
    ok("README carries no author or working-style section",
       not re.search(r"^#+ .*(author|working style)", _rd, re.I | re.M))
    ok("README states the CONSTRUCTED scope",
       "CONSTRUCTED" in " ".join(_rd.split()))
    ok("README records the ordinal collision",
       "criterion-externality" in _rd)

# -------------------------------------------------------------------------

failed = [(n, d) for n, o, d in CHECKS if not o]
for n, o, d in CHECKS:
    print("%s  %s%s" % ("ok  " if o else "FAIL", n,
                        ("  -- " + d) if (d and not o) else ""))
print()
print("checks: %d   failed: %d" % (len(CHECKS), len(failed)))
sys.exit(1 if failed else 0)
