# SPDX-License-Identifier: CC0-1.0
# test_terminal.py -- checks for terminal-crossing. Stdlib only, no pytest,
# no network. Run: python3 test_terminal.py
#
# Expected values live HERE and in no module under test. What is checked is
# the parser against the delivered order, the metric's arithmetic on
# CONSTRUCTED systems, and the audit's reading of the delivered candidates.
# Nothing below is a statement about any repository, spacecraft or black
# hole.

import ast
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, "sheet-structure-scan"))

import crossing_rate as cr            # noqa: E402
import audit                          # noqa: E402
import no_severity                    # noqa: E402

CHECKS = []


def ok(name, cond, detail=""):
    CHECKS.append((name, bool(cond), detail))


def close(x, y, tol=1e-9):
    return x is not None and y is not None and abs(x - y) <= tol


def raises(fn, *args, **kw):
    try:
        fn(*args, **kw)
    except ValueError:
        return True
    except Exception:
        return False
    return False


# --- the six conditions are parsed from the order, not retyped -------------

WO = os.path.join(HERE, "WORK_ORDER.md")
# the delivered order is a .md and carries em dashes; the ASCII rule is
# a rule about .py files. Containment is checked whitespace-flattened
# because the order wraps its lines.
_wo = open(WO, encoding="utf-8").read()
_WO_FLAT = " ".join(_wo.split())
ok("WORK_ORDER.md present and is WO-3",
   os.path.exists(WO) and "WO-3" in _wo)

conds = cr.conditions()
ok("the order's conditions section yields six bullets", len(conds) == 6,
   "got %d" % len(conds))
ids = cr.channel_ids()
ok("channel ids derived mechanically from the bullets [CHOICE 2]",
   ids == ["physical", "operator", "shared", "maintenance", "supply",
           "disposal"],
   repr(ids))
for cid, text in conds:
    ok("bullet for %s occurs verbatim in the order" % cid,
       " ".join(text.split()) in _WO_FLAT)

_src = open(os.path.join(HERE, "crossing_rate.py"), encoding="utf-8").read()
_tree = ast.parse(_src)
_strs = [n.value for n in ast.walk(_tree)
         if isinstance(n, ast.Constant) and isinstance(n.value, str)]
ok("no condition bullet is retyped as a literal in the module",
   not any(text in s for _, text in conds for s in _strs))

# the section is located by content; a document without it refuses
_tmp = os.path.join(HERE, "_no_section.md")
open(_tmp, "w").write("# nothing here\n\n- no bullets under a heading\n")
ok("a document with no Conditions section raises rather than returning []",
   raises(cr.conditions, _tmp))
os.remove(_tmp)

# --- channel(): the state vocabulary is closed ------------------------------

ok("channel accepts a declared state",
   cr.channel("physical", "ABSENT_MEASURED").state == "ABSENT_MEASURED")
ok("channel refuses a state outside the vocabulary",
   raises(cr.channel, "physical", "CLEAN"))
ok("three states and no more", len(cr.CHANNEL_STATES) == 3
   and "UNSEARCHED" in cr.CHANNEL_STATES
   and "ABSENT_MEASURED" in cr.CHANNEL_STATES)

# --- system(): an undeclared channel is UNSEARCHED [CHOICE 1] --------------

s_partial = cr.system("t", 1.0, "year",
                      [cr.channel("physical", "ABSENT_MEASURED")])
by = dict((cid, c.state) for cid, c in s_partial.channels.items())
ok("system fills every order channel", len(s_partial.channels) == 6)
ok("an undeclared channel reads UNSEARCHED, never ABSENT_MEASURED",
   by["operator"] == "UNSEARCHED" and by["physical"] == "ABSENT_MEASURED")
ok("system refuses a channel id outside the order's conditions",
   raises(cr.system, "t", 1.0, "year",
          [cr.channel("physical", "ABSENT_MEASURED")]
          + [cr.Channel("gravitational", "ABSENT_MEASURED", 0, None, None,
                        "")]))

# --- expected_crossings: None is not zero ----------------------------------

ok("a rate and a horizon in the same unit multiply",
   close(cr.expected_crossings(1.0, "per_year", 10.0, "year"), 10.0))
ok("units convert across the declared table",
   close(cr.expected_crossings(0.5, "per_day", 2.0, "day"), 1.0))
ok("a MEASURED zero rate returns 0.0, a number",
   cr.expected_crossings(0.0, "per_year", 10.0, "year") == 0.0)
ok("an absent rate returns None, not 0",
   cr.expected_crossings(None, "per_year", 10.0, "year") is None)
ok("an unknown rate unit returns None rather than a converted number "
   "[CHOICE 3]",
   cr.expected_crossings(1.0, "per_fortnight", 10.0, "year") is None)
ok("the UNBOUNDED sentinel in the unit slot returns None [CHOICE 3]",
   cr.expected_crossings(1.0, "per_year", 1.0, cr.UNBOUNDED) is None)
ok("an absent horizon returns None",
   cr.expected_crossings(1.0, "per_year", None, "year") is None)
ok("an unknown horizon unit returns None",
   cr.expected_crossings(1.0, "per_year", 10.0, "fortnight") is None)

# --- crossing_total: value is None on every state but COMPUTED -------------

for sysrec in cr.corpus():
    st, val = cr.crossing_total(sysrec)
    ok("%s: total state is declared" % sysrec.name, st in cr.TOTAL_STATES)
    if st != "COMPUTED":
        ok("%s: a non-COMPUTED total carries no number" % sysrec.name,
           val is None)
    else:
        ok("%s: a COMPUTED total carries a number" % sysrec.name,
           isinstance(val, float))

# --- verdict: all three returns reached, TERMINAL on a constructed control -

verds = dict((s.name, cr.verdict(s)) for s in cr.corpus())
ok("TERMINAL is reachable -- the verdict is not CONSTANT_FIRES",
   verds["control_all_absent"] == "TERMINAL")
ok("an undeclared channel blocks TERMINAL and reads NOT_ESTABLISHED",
   verds["control_partly_declared"] == "NOT_ESTABLISHED")
ok("every asymptote reads NOT_TERMINAL",
   all(verds[s.name] == "NOT_TERMINAL" for s in cr._asymptotes()))
ok("all three verdicts occur in the corpus",
   set(verds.values()) == {"TERMINAL", "NOT_TERMINAL", "NOT_ESTABLISHED"})

# --- the three asymptotes discriminate, and none totals zero ---------------

asym = cr._asymptotes()
ok("three asymptotes carried", len(asym) == 3)
shapes = [cr.shape(s) for s in asym]
ok("the three return three distinct arithmetic shapes",
   cr.discriminates(asym), repr(shapes))
ok("one asymptote is UNBOUNDED_HORIZON -- a state, not a number",
   ("UNBOUNDED_HORIZON", None, None) in shapes)
zeros = [s.name for s in asym if cr.crossing_total(s)[1] == 0.0]
ok("no asymptote returns a total of zero", zeros == [], repr(zeros))
ok("the control does return zero, so zero is reachable",
   cr.crossing_total(
       [s for s in cr.corpus() if s.name == "control_all_absent"][0])[1]
   == 0.0)
ok("discriminates() is not constant -- two identical shapes fail it",
   not cr.discriminates([asym[0], asym[0]]))

# --- a PRESENT channel with no rate keeps its count [CHOICE 4] -------------

s_norate = cr.system("nr", 1.0, "year",
                     [cr.channel("supply", "PRESENT", completed=3)]
                     + [cr.channel(c, "ABSENT_MEASURED")
                        for c in cr.channel_ids() if c != "supply"])
st, val = cr.crossing_total(s_norate)
ok("a PRESENT channel with no declared rate contributes its count only",
   st == "COMPUTED" and close(val, 3.0))
ok("and it is NOT_TERMINAL on the strength of the channel alone",
   cr.verdict(s_norate) == "NOT_TERMINAL")

# --- audit step 1: the proposed seventh is held apart ----------------------

ok("the proposed medium is not named by any of the six",
   audit.covered(audit.PROPOSED_SEVENTH) == [])
state, why = audit.falsifier_state(audit.PROPOSED_SEVENTH)
ok("an uncovered unshieldable medium makes the falsifier unsatisfiable",
   state == "UNSATISFIABLE_IF_COUNTED", state)
ok("both readings are stated and neither is taken",
   audit.PROPOSED_SEVENTH.state == "UNRESOLVED"
   and audit.PROPOSED_SEVENTH.reading_a
   and audit.PROPOSED_SEVENTH.reading_b)
_shield = audit.PROPOSED_SEVENTH._replace(shieldable=True)
ok("an uncovered but shieldable medium reads UNSATISFIED -- not constant",
   audit.falsifier_state(_shield)[0] == "UNSATISFIED")
_named = audit.PROPOSED_SEVENTH._replace(name="acoustic side channel")
ok("a medium the six do name reads COVERED_BY_CONDITIONS",
   audit.falsifier_state(_named)[0] == "COVERED_BY_CONDITIONS")
ok("the seventh is never merged into the parsed six [CHOICE 5]",
   audit.PROPOSED_SEVENTH.name not in
   [cid for cid in cr.channel_ids()]
   and len(cr.conditions()) == 6)

# --- audit: the three candidates, three mechanisms, two channels -----------

m = audit.mechanism_channel_map()
ok("three delivered candidates", len(audit.CANDIDATES) == 3)
ok("the order gives all three one verdict",
   set(c.order_verdict for c in audit.CANDIDATES) == {"FAILS"})
ok("three distinct mechanisms over two distinct channels",
   m["mechanisms"] == 3 and m["channels"] == 2,
   "%d / %d" % (m["mechanisms"], m["channels"]))
ok("the collision is on operator",
   [ch for ch, _ in m["collisions"]] == ["operator"])
unex = audit.conditions_unexercised()
ok("three of six conditions are exercised by no delivered candidate",
   sorted(unex) == ["maintenance", "physical", "shared"], repr(unex))

# --- carried states: contamination and the step 4 search -------------------

ok("contamination is carried UNKNOWN, a third state",
   audit.CONTAMINATION["state"] == "UNKNOWN"
   and " ".join(audit.CONTAMINATION["order_line"].split())
   in _WO_FLAT)
ok("the step 4 absence carries neither a corpus nor terms",
   audit.SEARCH_STATUS["corpus"] == "NOT_STATED"
   and audit.SEARCH_STATUS["terms"] == "NOT_STATED")
ok("the step 4 order line occurs verbatim in the order",
   " ".join(audit.SEARCH_STATUS["order_line"].split()) in _WO_FLAT)

# --- renders screen clean, and both modules refuse --selftest --------------

for mod, name in ((cr, "crossing_rate"), (audit, "audit")):
    clean, hits = no_severity.check(mod.render())
    ok("%s render screens clean with no exemption" % name, clean, repr(hits))

ok("the screen is not silent -- a planted token fires",
   not no_severity.check("this is a critical defect")[0])

for fn in ("crossing_rate.py", "audit.py"):
    p = subprocess.run([sys.executable, os.path.join(HERE, fn),
                        "--selftest"], capture_output=True)
    ok("%s refuses --selftest with exit 2" % fn, p.returncode == 2)
    ok("%s names this test file in its refusal" % fn,
       b"test_terminal.py" in p.stderr)
    p = subprocess.run([sys.executable, os.path.join(HERE, fn)],
                       capture_output=True)
    ok("%s bare invocation renders and exits 0" % fn,
       p.returncode == 0 and len(p.stdout) > 200)
    p = subprocess.run([sys.executable, os.path.join(HERE, fn), "--choices"],
                       capture_output=True)
    ok("%s prints its choices" % fn,
       p.returncode == 0 and b"[CHOICE" in p.stdout)

# --- ASCII, and the README -------------------------------------------------

for fn in ("crossing_rate.py", "audit.py", "test_terminal.py"):
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

# ---------------------------------------------------------------------------

failed = [(n, d) for n, o, d in CHECKS if not o]
for n, o, d in CHECKS:
    print("%s  %s%s" % ("ok  " if o else "FAIL", n,
                        ("  -- " + d) if (d and not o) else ""))
print()
print("checks: %d   failed: %d" % (len(CHECKS), len(failed)))
sys.exit(1 if failed else 0)
