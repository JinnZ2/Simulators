# SPDX-License-Identifier: CC0-1.0
# test_unowned.py -- checks for unowned-join. Stdlib only, no pytest, no
# network. Run: python3 test_unowned.py
#
# Expected values live HERE and in no module under test. What is checked is
# the parser against the delivered order, the invariant's arithmetic on
# CONSTRUCTED structures, and the face mapping as a declared reading.
# Nothing below is a statement about any container, rule, report, boundary,
# channel, frog or institution.

import ast
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, "sheet-structure-scan"))

import invariant as inv               # noqa: E402
import faces                          # noqa: E402
import no_severity                    # noqa: E402

CHECKS = []


def ok(name, cond, detail=""):
    CHECKS.append((name, bool(cond), detail))


def close(x, y, tol=1e-9):
    return x is not None and y is not None and abs(x - y) <= tol


def raises(exc, fn, *args, **kw):
    try:
        fn(*args, **kw)
    except exc:
        return True
    except Exception:
        return False
    return False


# --- the order, and the faces parsed out of it -----------------------------

WO = os.path.join(HERE, "WORK_ORDER.md")
# the delivered order is a .md and carries em dashes and arrows; the ASCII
# rule is a rule about .py files. Containment is checked whitespace-flattened
# because the order wraps its lines.
_wo = open(WO, encoding="utf-8").read()
_WO_FLAT = " ".join(_wo.split())
ok("WORK_ORDER.md present and is WO-4",
   os.path.exists(WO) and "WO-4" in _wo)

fs = faces.faces()
ok("the order's faces section yields seven numbered faces", len(fs) == 7,
   "got %d" % len(fs))
ok("the faces are numbered 1..7 in order",
   [n for n, _l, _t in fs] == list(range(1, 8)))
for n, label, text in fs:
    ok("face %d's parsed text is contained in the order" % n,
       " ".join(text.split()) in _WO_FLAT)
ok("face labels come off the em dash, not a retyped list",
   [l for _n, l, _t in fs][:3]
   == ["CONTAINER / CHAIN POSITION",
       "REGULATION REACHING EXCLUSION STRUCTURALLY",
       "QUIET FAILURE"])

# no face text is a literal anywhere in the modules
_lits = []
for fn in ("invariant.py", "faces.py"):
    tree = ast.parse(open(os.path.join(HERE, fn), encoding="ascii").read())
    _lits += [n.value for n in ast.walk(tree)
              if isinstance(n, ast.Constant) and isinstance(n.value, str)]
_LIT_FLAT = " ".join(" ".join(s.split()) for s in _lits)
ok("no face's parsed text is retyped as a literal in the modules",
   not any(" ".join(t.split()) in _LIT_FLAT for _n, _l, t in fs))

# a document without the section raises rather than returning nothing
import tempfile                       # noqa: E402
_tmp = os.path.join(tempfile.mkdtemp(), "empty.md")
open(_tmp, "w", encoding="utf-8").write("# not the order\n\n## Something\n")
ok("a document with no faces section raises",
   raises(faces.OrderUnparsed, faces.faces, _tmp))

refs = faces.cross_refs()
ok("three faces carry an arrow to a companion order",
   sorted(refs.items()) == [(1, "WO-1"), (3, "WO-2"), (4, "WO-3")],
   repr(sorted(refs.items())))

# --- the invariant: A1-A4 and the five verdicts ----------------------------

ctl = inv.controls()
reached = set(inv.verdict(s) for s in ctl)
ok("every declared verdict is reached by a control",
   reached == set(inv.VERDICTS), repr(sorted(reached)))
ok("the verdicts are five and distinct", len(set(inv.VERDICTS)) == 5)

by = dict((s.sid, inv.verdict(s)) for s in ctl)
ok("a single scope covering the join is OWNED",
   by["ctl_owned"] == inv.OWNED)
ok("union-only coverage is its own state [CHOICE 1]",
   by["ctl_union"] == inv.UNOWNED_BY_UNION)
ok("an observable in no scope is UNOWNED",
   by["ctl_unowned"] == inv.UNOWNED)
ok("a component declared not locally correct is LOCAL_FAULT",
   by["ctl_local_fault"] == inv.LOCAL_FAULT)
ok("an undeclared scope is NOT_EVALUABLE, not an empty scope [CHOICE 2]",
   by["ctl_undeclared"] == inv.NOT_EVALUABLE)

ok("the shape holds on exactly the two unowned verdicts",
   [s.sid for s in ctl if inv.shape_holds(s)]
   == ["ctl_union", "ctl_unowned"])
ok("an instrument that always finds the shape is refused: 3 of 5 controls "
   "do not hold it",
   sum(1 for s in ctl if not inv.shape_holds(s)) == 3)

ok("locally_detectable is True only on OWNED",
   [inv.locally_detectable(s) for s in ctl]
   == [True, False, False, False, None])
ok("locally_detectable is None, not False, when not evaluable",
   inv.locally_detectable(ctl[4]) is None)
ok("owner names the covering component",
   inv.owner(ctl[0]) == "a" and inv.owner(ctl[1]) is None)
ok("uncovered lists the join observables in no scope",
   inv.uncovered(ctl[2]) == ("y",))
ok("uncovered is None when a scope is undeclared",
   inv.uncovered(ctl[4]) is None)

# A1 and the basis are enforced at construction
ok("A1 refuses a one-component structure",
   raises(ValueError, inv.structure, "x", [inv.component("a", ["p"])],
          ["p"], "b"))
ok("a structure with no stated basis is refused",
   raises(ValueError, inv.structure, "x",
          [inv.component("a", ["p"]), inv.component("b", ["q"])], ["p"], ""))
ok("an empty declared scope is refused as distinct from UNDECLARED",
   raises(ValueError, inv.component, "a", []))
ok("a locally_correct outside the three states is refused",
   raises(ValueError, inv.component, "a", ["p"], "maybe"))

# A3: an empty join is not evaluable
_ej = inv.Structure("ej", (inv.component("a", ["p"]),
                           inv.component("b", ["q"])), frozenset(), "b")
ok("A3: an empty join is NOT_EVALUABLE",
   inv.verdict(_ej) == inv.NOT_EVALUABLE)

# --- join_coverage -------------------------------------------------------

ok("coverage is 1.0 when the union covers the join",
   close(inv.join_coverage([["x"], ["y"]], ["x", "y"]), 1.0))
ok("coverage is 0.5 when half is reached",
   close(inv.join_coverage([["x"], ["w"]], ["x", "y"]), 0.5))
ok("a declared join no declared scope reaches is 0.0, a measurement",
   inv.join_coverage([["w"], ["z"]], ["x", "y"]) == 0.0)
ok("an empty join is None, not 0.0",
   inv.join_coverage([["x"]], []) is None)
ok("an UNDECLARED scope makes coverage None, not 0.0",
   inv.join_coverage([["x"], inv.UNDECLARED], ["x", "y"]) is None)

# --- no term is coined ---------------------------------------------------

ok("coin() refuses", raises(inv.TermCoinageRefused, inv.coin, "anything"))
ok("the term-gap status reports nothing coined",
   faces.term_status()["coined_here"] is False)
ok("no language is scored and the cross-language search is UNSEARCHED",
   faces.term_status()["cross_language"] == faces.UNSEARCHED
   and faces.term_status()["step3"]["languages_scored"] == 0
   and faces.term_status()["step3"]["search_run"] is False)
ok("the order's own NOT COINED HERE line is in the delivered text",
   "NOT COINED HERE." in _WO_FLAT)

# --- the faces through the invariant -------------------------------------

rows = dict((r["n"], r) for r in faces.fit())
ok("every parsed face has a declared structure",
   all(r["sid"] for r in rows.values()))
ok("every declared structure carries a basis",
   all(s.basis for s in faces.structures().values()))
ok("face 3 (quiet failure) is the union case, not the uncovered one",
   rows[3]["verdict"] == inv.UNOWNED_BY_UNION)
ok("face 1 (container / chain position) has the join in no scope",
   rows[1]["verdict"] == inv.UNOWNED)
ok("face 6 (the frog) returns NOT_EVALUABLE [CHOICE 7]",
   rows[6]["verdict"] == inv.NOT_EVALUABLE)
ok("face 6 is the only face the invariant cannot evaluate",
   [n for n in rows if rows[n]["verdict"] == inv.NOT_EVALUABLE] == [6])

c = faces.fit_counts()
ok("six of seven faces hold the shape, one is not evaluable",
   c["n_faces"] == 7 and c["shape_holds"] == 6 and c["not_evaluable"] == 1,
   repr(c))
ok("no face is left without a declared structure",
   c["no_structure"] == 0)

# the tautology warning is on the page, above the counts
_rend = faces.render()
ok("the render states the fit is not evidence, before the counts",
   _rend.index("near-tautological") < _rend.index("faces parsed:")
   and "near-tautological" in _rend)
ok("step 2 is NOT_RUN and says why",
   faces.STEP2["run"] is False and "second party" in faces.STEP2["reason"])

# --- companions ----------------------------------------------------------

ok("WO-1, WO-2 and WO-3 all resolve to a folder with a content marker "
   "[CHOICE 6]",
   all(faces.companion_state(w) == "RESOLVED"
       for w in ("WO-1", "WO-2", "WO-3")))
ok("a companion whose folder is absent reads ABSENT, not RESOLVED",
   faces.companion_state("WO-1", root=os.path.join(HERE, "samples"))
   == "ABSENT")
ok("a folder without its content marker is not a resolution",
   faces.companion_state("WO-2", root=HERE) in ("ABSENT",
                                                "FOLDER_NO_MARKER"))

# --- the 'no term means no code' claim -----------------------------------

k = faces.code_without_a_term()
ok("a checkable predicate exists and reaches every declared verdict",
   k["predicate_exists"] and k["verdicts_reachable"] == k["verdicts_declared"])
ok("it was built with no term coined", k["term_coined"] is False)
ok("the strong claim is reported REFUTED with its scope stated",
   k["strong_claim"] == "REFUTED_HERE" and "one folder" in
   k["strong_claim_scope"])
ok("the order's strong claim is in the delivered text",
   "NO PROCEDURES CAN BE MADE AROUND IT AND NO CODE CAN BE MADE AROUND IT"
   in _WO_FLAT)
ok("the surviving claim is the order's own transmission mechanism",
   "PROPOSAL" in k["surviving_claim"] and "REPORT" in k["surviving_claim"])
ok("the order's own status-off-form mechanism is in the delivered text",
   "has the surface form of a PROPOSAL" in _WO_FLAT)
ok("the transmission mechanism is NOT claimed tested here",
   k["mechanism_tested_here"] is False)

# --- the screen ----------------------------------------------------------

for fn, txt in (("invariant", inv.render()), ("faces", faces.render())):
    clean, hits = no_severity.check(txt)
    ok("%s render screens clean with no exemption" % fn, clean,
       repr(hits[:3]))
_pc, _ph = no_severity.check("this render is wrong and the value is invalid")
ok("the screen fires on a planted token", (not _pc) and bool(_ph))

# --- CLI contract --------------------------------------------------------

for fn in ("invariant.py", "faces.py"):
    p = subprocess.run([sys.executable, os.path.join(HERE, fn),
                        "--selftest"], capture_output=True)
    ok("%s refuses --selftest with exit 2" % fn, p.returncode == 2)
    ok("%s names this test file in its refusal" % fn,
       b"test_unowned.py" in p.stderr)
    p = subprocess.run([sys.executable, os.path.join(HERE, fn)],
                       capture_output=True)
    ok("%s bare invocation renders and exits 0" % fn,
       p.returncode == 0 and len(p.stdout) > 200)
    p = subprocess.run([sys.executable, os.path.join(HERE, fn), "--choices"],
                       capture_output=True)
    ok("%s prints its choices" % fn,
       p.returncode == 0 and b"[CHOICE" in p.stdout)

_declared = sorted(list(inv.CHOICES) + list(faces.CHOICES))
ok("the choice numbers are 1..8 with no collision across the two modules",
   _declared == list(range(1, 9)), repr(_declared))
# a marker inside the CHOICES dict is the declaration, not a citation; the
# check requires the marker on a line that is not a dict entry.
_srclines = []
for _f in ("invariant.py", "faces.py"):
    for _ln in open(os.path.join(HERE, _f), encoding="ascii").read().splitlines():
        if not re.match(r"^\s*\d+:\s", _ln):
            _srclines.append(_ln)
_SRC = "\n".join(_srclines)
ok("every declared choice is cited at a site outside its own declaration",
   all(("[CHOICE %d]" % n) in _SRC for n in _declared),
   repr([n for n in _declared if ("[CHOICE %d]" % n) not in _SRC]))

# --- ASCII, and the README -----------------------------------------------

for fn in ("invariant.py", "faces.py", "test_unowned.py"):
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
    ok("README records that no term is coined",
       "coin" in _rd.lower())

# ---------------------------------------------------------------------------

failed = [(n, d) for n, o, d in CHECKS if not o]
for n, o, d in CHECKS:
    print("%s  %s%s" % ("ok  " if o else "FAIL", n,
                        ("  -- " + d) if (d and not o) else ""))
print()
print("checks: %d   failed: %d" % (len(CHECKS), len(failed)))
sys.exit(1 if failed else 0)
