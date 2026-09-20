# SPDX-License-Identifier: CC0-1.0
# test_check.py -- checks for deep-research-correction. Stdlib only, no
# pytest, no network. Run: python3 test_check.py
#
# Expected values live HERE. What is checked is the checker's machinery and
# its recomputation of the notice's mechanical items; nothing below audits
# the repository's instruments or the target's suite results.

import ast
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, "sheet-structure-scan"))
sys.path.insert(0, os.path.join(ROOT, "measurand-partition"))

import check                        # noqa: E402
import no_severity                  # noqa: E402

CHECKS = []


def ok(name, cond, detail=""):
    CHECKS.append((name, bool(cond), detail))


TARGET = os.path.join(HERE, check.TARGET)
NOTICE = os.path.join(HERE, "CORRECTION_NOTICE.md")
TDOC = open(TARGET, encoding="utf-8").read()
NDOC = open(NOTICE, encoding="utf-8").read()

# --- documents landed verbatim and present ---------------------------------

ok("target document present", os.path.exists(TARGET) and len(TDOC) > 40000)
ok("correction notice present", os.path.exists(NOTICE) and len(NDOC) > 8000)
ok("notice states its issue date 2026-09-18",
   "**Correction issued:** 2026-09-18" in NDOC)
ok("target self-dates 2026-09-19",
   "**Research date:** 2026-09-19" in TDOC)

# --- count_relation: the C-2 classifier, null-tested -----------------------

ok("count_relation DISJOINT on 63+157=220",
   check.count_relation(63, 157, 220) == "DISJOINT")
ok("count_relation NESTED on total==outer, inner<outer",
   check.count_relation(63, 157, 157) == "NESTED")
ok("count_relation NEITHER on 300", check.count_relation(63, 157, 300)
   == "NEITHER")
ok("count_relation is not constant (three distinct verdicts reachable)",
   len({check.count_relation(63, 157, 220),
        check.count_relation(63, 157, 157),
        check.count_relation(63, 157, 300)}) == 3)
ok("count_relation does not read equal parts as nested",
   check.count_relation(100, 100, 100) == "NEITHER")

# --- per-check recomputation -----------------------------------------------

rows = {r["id"]: r for r in check.run_all()}

c1 = rows["C-1"]
ok("C-1 CONFIRMED_FROM_DOC", c1["verdict"] == "CONFIRMED_FROM_DOC")
ok("C-1 reads the research date off the target",
   c1["research_date"] == "2026-09-19")
ok("C-1 finds the re-execution date claim",
   c1["reexec_claim"] == "2026-09-19")
ok("C-1 anchors on the notice issue date",
   c1["notice_issue"] == "2026-09-18")

c2 = rows["C-2"]
ok("C-2 CONFIRMED_FROM_DOC", c2["verdict"] == "CONFIRMED_FROM_DOC")
ok("C-2 the 220 reading is DISJOINT", c2["disjoint_reading"] == "DISJOINT")
ok("C-2 the 157 reading is NESTED", c2["nested_reading"] == "NESTED")
ok("C-2 TL;DR enumerates four values against five folders",
   len(c2["tldr_values"]) == 4 and c2["tldr_folders"] == 5)
ok("C-2 the four values are 130,136,211,220",
   c2["tldr_values"] == [130, 136, 211, 220])

c3 = rows["C-3"]
ok("C-3 CONFIRMED_FROM_DOC", c3["verdict"] == "CONFIRMED_FROM_DOC")
ok("C-3 flags a future-year URL segment (3026)",
   "3026" in c3["future_year_segments"])

c4 = rows["C-4"]
ok("C-4 CONFIRMED_FROM_DOC", c4["verdict"] == "CONFIRMED_FROM_DOC")
ok("C-4 the target's own figures reconcile (550+303=853)",
   c4["doc_reconciles"] is True)
ok("C-4 structural verdict is UNPARTITIONED (imported)",
   c4["structural"] == "UNPARTITIONED")
ok("C-4 local git recompute is available and differs from the target",
   c4["local"].get("available") and c4["local"]["total"] != 853)

# the structural verdict is common.attribution, not a local restatement
import common                       # noqa: E402
_direct = common.attribution(
    observed="x", setting="one field", unmeasured=["a", "b"], assigned_to="x")
ok("C-4 UNPARTITIONED is what common.attribution returns for "
   "residual->observed with unmeasured present",
   _direct["verdict"] == "UNPARTITIONED")

c5 = rows["C-5"]
ok("C-5 CONFIRMED_FROM_DOC", c5["verdict"] == "CONFIRMED_FROM_DOC")
ok("C-5 both characterizing clauses present", len(c5["present"]) == 2)

c6 = rows["C-6"]
ok("C-6 CONFIRMED_FROM_DOC", c6["verdict"] == "CONFIRMED_FROM_DOC")

c7 = rows["C-7"]
ok("C-7 CARRIED (true count egress-blocked)", c7["verdict"] == "CARRIED")
ok("C-7 records the operator figure 20+", c7["operator_figure"] == "20+")

u1 = rows["U-1"]
ok("U-1 CONFIRMED_HERE", u1["verdict"] == "CONFIRMED_HERE")
ok("U-1 the repo names the void VOID_KEY_HOLDER, not the notice's name",
   u1["repo_name"] == "VOID_KEY_HOLDER"
   and u1["notice_name"] == "VOID_SAME_AUTHOR")
ok("U-1 the instance-or-class scope is not declared",
   u1["scope_declared"] is False)

nf = rows["NOTE-folders"]
ok("NOTE ledger absent in this checkout (branch vs main)",
   "ledger" in nf["absent"])
ok("NOTE four of five named folders resolve here",
   len(nf["present"]) == 4)

# --- verdict vocabulary is closed ------------------------------------------

allowed = set(check.VERDICTS) | {"UNPARTITIONED"}
ok("every verdict is in the closed set",
   all(r["verdict"] in check.VERDICTS for r in rows.values()))

# --- render screens clean through no_severity ------------------------------

R = check.render()
ok("render screens clean through no_severity (no exemption)",
   len(no_severity.hits(R)) == 0, str(no_severity.hits(R))[:200])

# --- module hygiene --------------------------------------------------------

for fn in ("check.py", "test_check.py"):
    src = open(os.path.join(HERE, fn), "rb").read()
    ok("%s is ASCII" % fn, all(b < 128 for b in src))
    ast.parse(src.decode("ascii"), feature_version=(3, 9))
    ok("%s parses under 3.9" % fn, True)

p = subprocess.run([sys.executable, os.path.join(HERE, "check.py"),
                    "--selftest"], capture_output=True)
ok("check.py refuses --selftest with exit 2", p.returncode == 2)
p = subprocess.run([sys.executable, os.path.join(HERE, "check.py")],
                   capture_output=True)
ok("check.py bare invocation renders and exits 0",
   p.returncode == 0 and len(p.stdout) > 200)

README = open(os.path.join(HERE, "README.md"), encoding="utf-8").read()
README_FLAT = " ".join(README.split())  # collapse line wraps for phrase match
ok("README carries no author or working-style section",
   not re.search(r"^#+ .*(author|working style)", README, re.I | re.M))
ok("README states the checker's scope is document integrity, not the repo",
   "document integrity and measurand assignment only" in README_FLAT
   and "nothing here audits the repository's instruments" in README_FLAT)

# ---------------------------------------------------------------------------

failed = [(n, d) for n, o, d in CHECKS if not o]
for n, o, d in CHECKS:
    print("%s  %s%s" % ("ok  " if o else "FAIL", n,
                        ("  -- " + d) if (d and not o) else ""))
print()
print("checks: %d   failed: %d" % (len(CHECKS), len(failed)))
sys.exit(1 if failed else 0)
