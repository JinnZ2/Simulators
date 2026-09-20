# SPDX-License-Identifier: CC0-1.0
# test_chain.py -- checks for chain-position. Stdlib only, no pytest, no
# network. Run: python3 test_chain.py
#
# Expected values live HERE. What is checked is the three instruments'
# machinery on CONSTRUCTED data and the order's carried clause set; nothing
# below inspects any vendor or any deployed system.

import ast
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, "sheet-structure-scan"))

import chain_position as CP           # noqa: E402
import load_class as LC               # noqa: E402
import trust_provenance as TP         # noqa: E402
import no_severity                    # noqa: E402

CHECKS = []


def ok(name, cond, detail=""):
    CHECKS.append((name, bool(cond), detail))


def close(x, y, tol=1e-9):
    return x is not None and y is not None and abs(x - y) <= tol


# --- clause_audit: the null result is the finding, and it is not constant ---

a = CP.clause_audit()
ok("all carried OWASP clauses sit at the gateway, none inside the agent",
   a["inside_container"] == 0)
ok("the null result is the finding verdict",
   a["verdict"] == "NULL_RESULT_no_clause_places_position_inside")
ok("clause count matches the carried set", a["n_clauses"] == len(CP.CLAUSES))
demo = CP.CLAUSES + [{"id": "X", "text": "agent told its index",
                     "locus": CP.INSIDE_CONTAINER, "source": "constructed"}]
ad = CP.clause_audit(demo)
ok("a clause placing position inside raises the count -- not constant",
   ad["inside_container"] == 1
   and ad["verdict"] == "SOME_CLAUSE_places_position_inside")
und = CP.clause_audit([{"id": "Y", "text": "t", "locus": "nonsense"}])
ok("an out-of-vocabulary locus reads UNDECLARED, not inside and not gateway",
   und["counts"][CP.UNDECLARED] == 1 and und["inside_container"] == 0)

# --- horn_fork: both failure modes, neither selected ------------------------

ha = CP.horn_fork(CP.HORN_A)
hb = CP.horn_fork(CP.HORN_B)
hx = CP.horn_fork("neither")
ok("Horn A relocates", ha["horn"] == "A" and ha["failure"] == "RELOCATES")
ok("Horn B is evidence-absent",
   hb["horn"] == "B" and hb["failure"] == "EVIDENCE_ABSENT")
ok("an unknown source selects no horn (UNDEFINED, horn None)",
   hx["horn"] is None and hx["failure"] == "UNDEFINED")

# --- evidence_check: the absence is the container's, not the check's --------

ev = CP.evidence_check(CP.locally_correct_container())
ok("a locally-correct container cannot answer chain position",
   ev["can_answer"] is False and ev["state"] == "EVIDENCE_ABSENT")
ok("it names what would be needed (a cross-boundary observation)",
   ev["would_need"] and "outside this boundary" in ev["would_need"][0])
got = CP.evidence_check(CP.locally_correct_container()
                        + [{"id": "m", "carries_chain_position": True}])
ok("handed a chain manifest, the same check CAN answer -- not constant",
   got["can_answer"] is True and got["state"] == "EVIDENCE_PRESENT")

# --- stability_product: the compounding, by hand ---------------------------

ok("four compounding factors give 0.90345024",
   close(LC.stability_product([0.01, 0.02, 0.03, 0.04]), 0.90345024))
ok("empty conjunction is 1.0", LC.stability_product([]) == 1.0)
ok("one certain failure is 0.0", LC.stability_product([1.0]) == 0.0)
ok("an unassessed factor is None, not zero",
   LC.stability_product([0.01, None]) is None)
ok("an out-of-range factor is None",
   LC.stability_product([1.5]) is None)
ok("a zero factor multiplies through (1.0), distinct from an absent one",
   close(LC.stability_product([0.0, 0.5]), 0.5)
   and LC.stability_product([None, 0.5]) is None)

# --- reachable_controller: the states are kept apart -----------------------

ok("the illustrative case reads OK with a value",
   LC.reachable_controller([0.01, 0.02, 0.03, 0.04])["state"] == "OK")
ok("an unassessed factor is UNPROPAGATABLE (the order's RULE)",
   LC.reachable_controller([0.01, None])["state"] == "UNPROPAGATABLE")
ok("an out-of-range factor is MALFORMED, a different state",
   LC.reachable_controller([1.5])["state"] == "MALFORMED")

# --- redundancy_adjudicability: the discriminator is spec, not diversity ----

ok("disagreement against a verifiable spec is FAULT_DETECTED",
   LC.redundancy_adjudicability(True, ["A", "B"])["verdict"] == "FAULT_DETECTED")
ok("disagreement with no verifiable spec is NOISE",
   LC.redundancy_adjudicability(False, ["A", "B"])["verdict"]
   == "NOISE_unadjudicable")
ok("agreement of correlated copies is no signal",
   LC.redundancy_adjudicability(False, ["A", "A"])["verdict"]
   == "NO_SIGNAL_agreement")
ok("three verdicts are reachable, so it is not constant",
   len({LC.redundancy_adjudicability(True, ["A", "B"])["verdict"],
        LC.redundancy_adjudicability(False, ["A", "B"])["verdict"],
        LC.redundancy_adjudicability(False, ["A", "A"])["verdict"]}) == 3)

# --- the registers, carried from the order ---------------------------------

ok("three engineering gaps carried", len(LC.ENGINEERING_GAPS) == 3)
ok("two counter-arguments carried, both UNRESOLVED",
   len(LC.COUNTER_ARGUMENTS) == 2
   and all(c["status"] == "UNRESOLVED" for c in LC.COUNTER_ARGUMENTS))
ok("seven assumed stabilities named", len(LC.ASSUMED_STABILITIES) == 7)

# --- trust_provenance: the load-bearing UNEXAMINED / NOT_AUDITABLE split ----

recs = TP.sample_records()
ok("a payload-only record is UNEXAMINED (cannot say), not a negative",
   TP.assignment_auditability(recs["payload_only"])["verdict"] == "UNEXAMINED")
ok("a declared-absent provenance is NOT_AUDITABLE (a known negative)",
   TP.assignment_auditability(recs["declared_absent"])["verdict"]
   == "NOT_AUDITABLE")
ok("a complete record is AUDITABLE",
   TP.assignment_auditability(recs["auditable"])["verdict"] == "AUDITABLE")
ok("UNEXAMINED and NOT_AUDITABLE are different states (the second-order gap)",
   TP.assignment_auditability(recs["payload_only"])["verdict"]
   != TP.assignment_auditability(recs["declared_absent"])["verdict"])
ok("spec_satisfied tracks the AUDITABLE verdict",
   TP.spec_satisfied(recs["auditable"]) is True
   and TP.spec_satisfied(recs["payload_only"]) is False)
ok("the spec requires the scorer's own provenance (the recursion)",
   "scorer_provenance" in TP.PROVENANCE_SPEC)
ok("no common object to audit exists, so the claim stays UNVERIFIED",
   TP.common_object_exists()["exists"] is False)

# --- renders screen clean through no_severity ------------------------------

for name, mod in (("chain_position", CP), ("load_class", LC),
                  ("trust_provenance", TP)):
    R = mod.render()
    h = no_severity.hits(R)
    ok("%s render screens clean (no exemption)" % name, not h, str(h)[:200])

# --- module hygiene --------------------------------------------------------

for fn in ("chain_position.py", "load_class.py", "trust_provenance.py",
           "test_chain.py"):
    b = open(os.path.join(HERE, fn), "rb").read()
    ok("%s is ASCII" % fn, all(x < 128 for x in b))
    ast.parse(b.decode("ascii"), feature_version=(3, 9))
    ok("%s parses under 3.9" % fn, True)

for fn in ("chain_position.py", "load_class.py", "trust_provenance.py"):
    p = subprocess.run([sys.executable, os.path.join(HERE, fn), "--selftest"],
                       capture_output=True)
    ok("%s refuses --selftest with exit 2" % fn, p.returncode == 2)
    p = subprocess.run([sys.executable, os.path.join(HERE, fn)],
                       capture_output=True)
    ok("%s bare invocation renders and exits 0" % fn,
       p.returncode == 0 and len(p.stdout) > 200)

# --- WORK_ORDER landed verbatim, README present ----------------------------

wo = os.path.join(HERE, "WORK_ORDER.md")
_wo = open(wo, "rb").read().decode("ascii", "ignore")
ok("WORK_ORDER.md present and is WO-1",
   os.path.exists(wo) and "WO-1" in _wo
   and "Chain position detectability from inside a container" in _wo)
README = open(os.path.join(HERE, "README.md"), encoding="utf-8").read()
README_FLAT = " ".join(README.split())
ok("README carries no author or working-style section",
   not re.search(r"^#+ .*(author|working style)", README, re.I | re.M))
ok("README states the CONSTRUCTED scope and no-vendor-internals",
   "CONSTRUCTED" in README_FLAT and "vendor internals" in README_FLAT)

# ---------------------------------------------------------------------------

failed = [(n, d) for n, o, d in CHECKS if not o]
for n, o, d in CHECKS:
    print("%s  %s%s" % ("ok  " if o else "FAIL", n,
                        ("  -- " + d) if (d and not o) else ""))
print()
print("checks: %d   failed: %d" % (len(CHECKS), len(failed)))
sys.exit(1 if failed else 0)
