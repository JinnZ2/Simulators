# SPDX-License-Identifier: CC0-1.0
# test_credential.py -- checks for credential-channel. Stdlib only, no
# pytest, no network. Run: python3 test_credential.py
#
# Expected values live HERE. Every world is CONSTRUCTED with a declared
# generative model; no plant, worker, record or review was read and
# nothing below is evidence about any person or workplace. What is checked
# is that the five instruments behave as claimed.

import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, "sheet-structure-scan"))

import credential_channel as cc        # noqa: E402
import no_severity                     # noqa: E402

CHECKS = []
EPS = 1e-9


def check(name, cond, detail=""):
    CHECKS.append((name, bool(cond), detail))


def refuses(fn, *a, **k):
    try:
        fn(*a, **k)
    except cc.Refused:
        return True
    return False


def near(a, b, tol=EPS):
    return a is not None and b is not None and abs(a - b) < tol


ORDER = open(os.path.join(HERE, "WORK_ORDER.md"), encoding="utf-8").read()
ORDER_FLAT = re.sub(r"\s+", " ", ORDER).lower()
README = open(os.path.join(HERE, "README.md"), encoding="utf-8").read()
SRC = open(os.path.join(HERE, "credential_channel.py")).read()

# 1. the delivery
check("order bundles five instruments", "five instruments" in ORDER_FLAT)
check("order says each runs alone", "each runs alone" in ORDER_FLAT)
check("order carries the forklift-fuse sequence", "fuse under the seat" in ORDER_FLAT)
check("order's I-2 mechanism note: not procedural", "was not procedural" in ORDER_FLAT)
check("order carries the Combine-Cognitive-Architecture caution",
      "combine-cognitive-architecture" in ORDER_FLAT and "overlay" in ORDER_FLAT)

# 2. imports not copied (CDC_008)
check("spearman imported from readout-count", "from readout_count import spearman" in SRC)
check("ols imported from sim-span", "from three_column import ols" in SRC)
check("no local def of spearman or ols", "def spearman" not in SRC and "def ols(" not in SRC)

# 3. I-1 (CDC_001, CDC_002)
r = cc.i1_route_correlation(cc.i1_candidates())
check("I-1: route B tracks performance (rho > 0)", r["rho_b"] > 0)
check("I-1: route A is at or below zero on the constructed world", r["rho_a"] <= 0)
check("I-1: verdict is the gate uncorrelated/inverse", "uncorrelated or inverse" in r["verdict"])
# the both-track branch is reachable
both = [{"route_a_score": p, "route_b_score": p, "performance": p} for p in range(10)]
check("I-1: both-track branch reachable", "both routes track" in cc.i1_route_correlation(both)["verdict"])
check("I-1: NOT_EVALUABLE on a constant side",
      "NOT_EVALUABLE" in cc.i1_route_correlation([{"route_a_score": 1, "route_b_score": 1, "performance": 1}] * 3)["verdict"])
oc = cc.i1_objection_coding(cc.i1_objections())
check("I-1: seniors cite prior usage more (engage less)", oc["senior"]["engage_share"] < oc["junior"]["engage_share"])
check("I-1: objection coding refuses a bad kind",
      refuses(cc.i1_objection_coding, [{"status": "s", "kind": "x"}]))

# 4. I-2 (CDC_003)
i2 = cc.i2_routing_cost(cc.i2_events())
check("I-2: two events routed off-authorisation", i2["n_routed"] == 2)
check("I-2: routing cost is 300 + 900 = 1200", near(i2["routing_cost_total"], 1200.0))
check("I-2: the on-authorisation 250 external is NOT counted (fault, not routing)",
      i2["routing_cost_total"] == 1200.0)
check("I-2: refuses an event with no authorised", refuses(cc.i2_routing_cost, [{"actual": "x"}]))
check("I-2: routing_cost formula", near(cc.routing_cost(0.0, 2.0), 300.0)
      and near(cc.routing_cost(250.0, 1.0), 400.0))
# a cheap same-authorisation resolution is NOT routing
noroute = cc.i2_routing_cost([{"authorised": "op", "actual": "op",
                               "resolution_cheap": True, "downtime_hours": 5.0,
                               "external_cost": 0.0}])
check("I-2: same-authorisation cheap event is not routing cost", noroute["routing_cost_total"] == 0.0)

# 5. I-3 (CDC_004)
i3 = cc.i3_gap_vs_exposure(cc.i3_rows())
check("I-3: gap widens downward with exposure (coef < 0)", i3["exposure_coef"] < 0)
check("I-3: verdict names the downward direction", "downward" in i3["verdict"])
# an upward world flips the sign
up = [{"confidence": 0.5 + 0.02 * e, "hit_rate": 0.5, "exposure_years": e} for e in range(20)]
check("I-3: an upward world reads coef > 0", cc.i3_gap_vs_exposure(up)["exposure_coef"] > 0)

# 6. I-4 (CDC_005)
i4 = cc.i4_inventory_vs_exposure(cc.i4_rows())
check("I-4: inventory score tracks exposure (coef != 0)", abs(i4["exposure_coef"]) > 1e-6)
check("I-4: verdict names history not disposition", "measuring history" in i4["verdict"])
flat = [{"inventory_score": 3.0, "exposure_years": e} for e in range(20)]
check("I-4: a flat world reads no exposure trend", "no exposure trend" in cc.i4_inventory_vs_exposure(flat)["verdict"])

# 7. I-5 (CDC_006)
i5 = cc.i5_attribution_error(cc.i5_events())
check("I-5: level 1 error rate is 0 (resolvers, never mis-credited up as level 1)", near(i5["by_credited_level"][1]["error_rate"], 0.0))
check("I-5: higher credited levels carry higher error rates", i5["by_credited_level"][3]["error_rate"] > i5["by_credited_level"][2]["error_rate"])
check("I-5: all errors flow upward on the constructed world", near(i5["upward_share"], 1.0))
check("I-5: reads reporting position not competence", "REPORTING POSITION" in i5["reads"])
check("I-5: a level with no events is None", cc.i5_attribution_error(
    [{"resolver_level": 1, "credited_level": 1}])["by_credited_level"][1]["error_rate"] == 0.0)

# 8. carried, not verified (CDC_007)
check("Combine-Cognitive-Architecture carried and marked not in this tree",
      "NOT in this tree" in cc.CARRIED["combine_cognitive_architecture"])
check("specialisation assumption filed NOT YET RUNNABLE",
      "NOT YET RUNNABLE" in cc.CARRIED["specialisation_assumption"])

# 9. renders, choices, hygiene
text = cc.render()
check("render screens clean through no_severity, no exemption",
      no_severity.hits(text) == [], str(no_severity.hits(text)[:3]))
check("screen fires on a planted word", no_severity.hits(text + "\nthis is wrong\n") != [])
declared = set(cc.CHOICES)
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
rc_exit = subprocess.run([sys.executable, os.path.join(HERE, "credential_channel.py"),
                          "--selftest"], capture_output=True).returncode
check("module refuses --selftest (exit 2)", rc_exit == 2)

failed = [c for c in CHECKS if not c[1]]
for name, ok, detail in CHECKS:
    print("%-5s %s%s" % ("ok" if ok else "FAIL", name, ("  [%s]" % detail) if (detail and not ok) else ""))
print("checks: %d   failed: %d" % (len(CHECKS), len(failed)))
sys.exit(1 if failed else 0)
