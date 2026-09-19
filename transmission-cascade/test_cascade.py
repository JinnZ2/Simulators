# SPDX-License-Identifier: CC0-1.0
# test_cascade.py -- checks for transmission-cascade. Stdlib only, no
# pytest, no network. Run: python3 test_cascade.py
#
# Expected values live HERE. Every world is CONSTRUCTED with a declared
# generative model; no dataset was recoded and nothing below is evidence
# about any cascade. What is checked is the machinery: the coder gate, the
# type-by-layer distribution, the recompute split and the competing fit.

import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, "sheet-structure-scan"))

import transmission_cascade as tc     # noqa: E402
import no_severity                     # noqa: E402

CHECKS = []
EPS = 1e-9


def check(name, cond, detail=""):
    CHECKS.append((name, bool(cond), detail))


def refuses(fn, *a, **k):
    try:
        fn(*a, **k)
    except tc.Refused:
        return True
    return False


def near(a, b, tol=EPS):
    return a is not None and b is not None and abs(a - b) < tol


ORDER = open(os.path.join(HERE, "WORK_ORDER.md"), encoding="utf-8").read()
ORDER_FLAT = re.sub(r"\s+", " ", ORDER).lower()
README = open(os.path.join(HERE, "README.md"), encoding="utf-8").read()
SRC = open(os.path.join(HERE, "transmission_cascade.py")).read()

# 1. the delivery
check("order names all four transmission types",
      all(t.split("_")[0].lower() in ORDER_FLAT for t in tc.TYPES))
check("order names overimitation the load-bearing construct",
      "load-bearing construct" in ORDER_FLAT)
check("order says coder reliability first", "coder reliability first" in ORDER_FLAT)
check("order states the divergence is the decisive prediction",
      "the decisive one" in ORDER_FLAT)
check("order states the taxonomy transfer is unvalidated",
      "itself unvalidated" in ORDER_FLAT)

# 2. cohen_kappa is imported not copied (TC_008)
check("cohen_kappa is imported from effective-redundancy-audit",
      "from effective_redundancy import cohen_kappa" in SRC)
check("no local def of cohen_kappa", "def cohen_kappa" not in SRC)

# 3. R2 gate (TC_001)
ev = tc.cascade_events()
c1, c2 = tc.two_coders(ev, agree=0.85)
rel = tc.r2_reliability(c1, c2)
check("R2: high agreement clears the floor", rel["gate"] == "R1_INTERPRETABLE")
check("R2: kappa 1.0 on identical coders", near(tc.r2_reliability(c1, c1)["kappa"], 1.0))
low1, low2 = tc.two_coders(ev, agree=0.35, seed=9)
rl = tc.r2_reliability(low1, low2)
check("R2: low agreement fails the floor", rl["gate"] == "R1_UNINTERPRETABLE")
check("R2: the failing gate names domain-boundedness as the finding",
      "domain-bound" in rl["reads"])
check("R2: refuses a non-type label", refuses(tc.r2_reliability, ["X"], ["EMULATION"]))
check("R2: refuses misaligned lists", refuses(tc.r2_reliability, ["EMULATION"], ["EMULATION", "IMITATION"]))

# 4. R1 gated on R2 (TC_002)
r1 = tc.r1_distribution(ev, rel)
check("R1: distribution present when R2 cleared", r1["distribution"] is not None)
check("R1: three layers", r1["layers"] == [1, 2, 3])
check("R1: overimitation rises with layer (constructed shape)",
      r1["distribution"][1]["OVERIMITATION"] < r1["distribution"][3]["OVERIMITATION"])
r1w = tc.r1_distribution(ev, rl)
check("R1: WITHHELD when R2 failed, not computed anyway", r1w["distribution"] is None
      and r1w["gate"] == "R1_UNINTERPRETABLE")

# 5. R3 (TC_003, TC_004)
r3 = tc.r3_recompute(tc.condition_runs())
check("R3: emulation recomputes above overimitation", r3["emulation_share"] > r3["overimitation_share"])
check("R3: verdict is type-predicts", r3["verdict"].startswith("type predicts"))
check("R3: overimitation share is lowest", tc.r3_recompute(tc.condition_runs())["by_type"]["OVERIMITATION"]["recompute_share"]
      == min(tc.r3_recompute(tc.condition_runs())["by_type"][t]["recompute_share"] for t in tc.TYPES))
check("R3: a run with neither response is uneval, not a repeat",
      tc.r3_recompute([{"type": "EMULATION", "response": "x"}])["by_type"]["EMULATION"]["uneval"] == 1)
check("R3: NOT_EVALUABLE when a decisive type has no runs",
      "NOT_EVALUABLE" in tc.r3_recompute([{"type": "IMITATION", "response": "repeat"}])["verdict"])
# the taxonomy-does-not-transfer branch is reachable
flat = [{"type": t, "response": "repeat"} for t in tc.TYPES for _ in range(10)]
flat += [{"type": "OVERIMITATION", "response": "recompute"} for _ in range(20)]
check("R3: does-not-transfer branch reachable", "does not transfer" in tc.r3_recompute(flat)["verdict"])
check("R3: refuses a non-type", refuses(tc.r3_recompute, [{"type": "X", "response": "repeat"}]))

# 6. R4 (TC_005, TC_006)
r4a = tc.r4_competing(tc.competing_rows(id_effect=0.0))
check("R4: type-real survives identification entering",
      "survives" in r4a["verdict"] and abs(r4a["type_with_identification"]) >= tc.MATERIAL)
r4b = tc.r4_competing(tc.competing_rows(id_effect=0.8, type_effect=0.0))
check("R4: type-null adds nothing once identification is entered",
      "adds nothing" in r4b["verdict"])
check("R4: the material floor is what separates them (both survive a relative-only test)",
      abs(r4b["type_with_identification"]) < tc.MATERIAL)
check("R4: identification coefficient is recovered in the id-real world",
      abs(r4b["identification_coef"]) > abs(r4a["identification_coef"]))

# 7. renders, choices, hygiene
text = tc.render()
check("render screens clean through no_severity, no exemption",
      no_severity.hits(text) == [], str(no_severity.hits(text)[:3]))
check("screen fires on a planted word", no_severity.hits(text + "\nthis is wrong\n") != [])
declared = set(tc.CHOICES)
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
check("README marks the data CONSTRUCTED", "CONSTRUCTED" in README)
rc_exit = subprocess.run([sys.executable, os.path.join(HERE, "transmission_cascade.py"),
                          "--selftest"], capture_output=True).returncode
check("module refuses --selftest (exit 2)", rc_exit == 2)

failed = [c for c in CHECKS if not c[1]]
for name, ok, detail in CHECKS:
    print("%-5s %s%s" % ("ok" if ok else "FAIL", name, ("  [%s]" % detail) if (detail and not ok) else ""))
print("checks: %d   failed: %d" % (len(CHECKS), len(failed)))
sys.exit(1 if failed else 0)
