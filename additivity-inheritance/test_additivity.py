# SPDX-License-Identifier: CC0-1.0
# test_additivity.py -- checks for additivity-inheritance. Stdlib only, no
# pytest, no network. Run: python3 test_additivity.py
#
# Expected values live HERE. Corpora are CONSTRUCTED, R3 is NOT_RUN, the
# history is CARRIED and unread; nothing below is a claim about the
# history of statistics. What is checked is the machinery and the one
# exact arithmetic result.

import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, "sheet-structure-scan"))

import additivity_inheritance as ai   # noqa: E402
import no_severity                     # noqa: E402

CHECKS = []
EPS = 1e-9


def check(name, cond, detail=""):
    CHECKS.append((name, bool(cond), detail))


def refuses(fn, *a, **k):
    try:
        fn(*a, **k)
    except ai.Refused:
        return True
    return False


def near(a, b, tol=EPS):
    return a is not None and b is not None and abs(a - b) < tol


ORDER = open(os.path.join(HERE, "WORK_ORDER.md"), encoding="utf-8").read()
ORDER_FLAT = re.sub(r"\s+", " ", ORDER).lower()
README = open(os.path.join(HERE, "README.md"), encoding="utf-8").read()
SRC = open(os.path.join(HERE, "additivity_inheritance.py")).read()

# 1. the delivery
check("order frames these as OPEN QUESTIONS not a critique",
      "these are open questions" in ORDER_FLAT and "not a critique of statistics" in ORDER_FLAT)
check("order names the false-negative methodological result",
      "false negative" in ORDER_FLAT)
check("order says citation tracing cannot detect a structural precondition",
      "citation tracing cannot detect a precondition carried by a shared structural inheritance" in ORDER_FLAT)
check("order says test the lineage claim first", "test it first" in ORDER_FLAT)
check("order's R3 is prior-art NOT SEARCHED", "not searched" in ORDER_FLAT)

# 2. R1 (AI_001)
check("r1_code refuses an uncoded paper", refuses(ai.r1_code, {"field": "x", "decade": 2000}))
check("r1_code refuses a bad code", refuses(ai.r1_code, {"additivity": "Z"}))
r1 = ai.r1_distribution(ai.r1_corpus())
check("R1: C-share rises monotonically with distance", r1["prediction"].startswith("C rises"))
check("R1: the four distances are present", [d for d, _ in r1["c_share_by_distance"]] == [1, 2, 3, 4])
check("R1: C-share is 0.2 .. 0.8", near(r1["c_share_by_distance"][0][1], 0.2)
      and near(r1["c_share_by_distance"][-1][1], 0.8))
# the non-monotone (finding) branch is reachable
flat = [{"field": "medicine", "decade": 2000, "additivity": "C_PRESENT_UNSTATED"},
        {"field": "education", "decade": 2000, "additivity": "A_STATED"}]
check("R1: non-monotone branch reachable", "does not rise" in ai.r1_distribution(flat)["prediction"])

# 3. R2 (AI_002)
r2 = ai.r2_reentry(ai.r2_records())
check("R2: 3 of 4 had to fight", r2["had_to_fight"] == 3 and r2["n"] == 4)
check("R2: names epigenetics among them", "epigenetics" in r2["phenomena"])
check("R2: share None on empty", ai.r2_reentry([])["share"] is None)

# 4. R3 (AI_003)
check("R3 is NOT_RUN with a reason", ai.R3["status"] == "NOT_RUN" and "egress-blocked" in ai.R3["reason"])

# 5. R4 the citation-trace false negative (AI_004)
r4 = ai.r4_known_answer()
check("R4: citation trace does NOT reach the precondition", r4["citation_reaches_precondition"] is False)
check("R4: structural trace DOES reach it", r4["structural_reaches_precondition"] is True)
check("R4: this is a false negative", r4["false_negative"] is True)
# the two traces agree when the precondition IS cited (no false negative)
nodes = ["a", "b"]
edges = [("a", "b", "citation")]
check("R4: with a citation edge, both traces reach it (no false negative)",
      ai.citation_trace(nodes, edges, "a", "b") and ai.structural_trace(nodes, edges, "a", "b"))
edges_inh = [("a", "b", "inheritance")]
check("R4: with only an inheritance edge, citation misses and structural reaches",
      (not ai.citation_trace(nodes, edges_inh, "a", "b")) and ai.structural_trace(nodes, edges_inh, "a", "b"))

# 6. the arithmetic (AI_005)
vc = ai.variance_components({(0, 0): 10.0, (0, 1): 12.0, (1, 0): 12.0, (1, 1): 20.0})
check("SS_interaction = additive residual", near(vc["ss_interaction"], vc["additive_residual"]))
check("SS_interaction = 9.00 by hand", near(vc["ss_interaction"], 9.0))
check("SS_total = SS_G + SS_E + SS_interaction (exact on balanced 2x2)",
      near(vc["ss_total"], vc["ss_g"] + vc["ss_e"] + vc["ss_interaction"]))
check("interaction_ss formula (a-b-c+d)^2/4", near(ai.interaction_ss(10, 12, 12, 20), 9.0))
check("a purely additive world has zero interaction SS",
      near(ai.interaction_ss(10, 12, 14, 16), 0.0))
check("variance_components refuses a non-2x2", refuses(ai.variance_components, {(0, 0): 1.0}))

# 7. lineage claim carried, not verified (AI_006)
check("lineage claim carried and not verified here", ai.LINEAGE_CLAIM["verified_here"] is False)

# 8. renders, choices, hygiene
text = ai.render()
check("render screens clean through no_severity, no exemption",
      no_severity.hits(text) == [], str(no_severity.hits(text)[:3]))
check("screen fires on a planted word", no_severity.hits(text + "\nthis is wrong\n") != [])
declared = set(ai.CHOICES)
cited = set()
for m in re.findall(r"\[CHOICE ([\d\-,]+)\]", SRC):
    if "-" in m:
        lo, hi = m.split("-"); cited |= set(range(int(lo), int(hi) + 1))
    else:
        cited |= set(int(x) for x in m.split(","))
check("every declared choice is cited", declared <= cited, str(declared - cited))
check("every cited choice is declared", cited <= declared, str(cited - declared))
check("module is ASCII", all(ord(c) < 128 for c in SRC))
check("README carries no author or working-style section",
      not re.search(r"^#+ .*(author|working style)", README, re.I | re.M))
check("README marks corpora CONSTRUCTED", "CONSTRUCTED" in README)
rc_exit = subprocess.run([sys.executable, os.path.join(HERE, "additivity_inheritance.py"),
                          "--selftest"], capture_output=True).returncode
check("module refuses --selftest (exit 2)", rc_exit == 2)

failed = [c for c in CHECKS if not c[1]]
for name, ok, detail in CHECKS:
    print("%-5s %s%s" % ("ok" if ok else "FAIL", name, ("  [%s]" % detail) if (detail and not ok) else ""))
print("checks: %d   failed: %d" % (len(CHECKS), len(failed)))
sys.exit(1 if failed else 0)
