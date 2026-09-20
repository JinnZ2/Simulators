# SPDX-License-Identifier: CC0-1.0
# test_hop.py -- checks for reporting-chain-loss. Stdlib only, no pytest, no
# network. Run: python3 test_hop.py
#
# Expected values live HERE. What is checked is the two instruments'
# machinery on CONSTRUCTED data; nothing below is a measurement of any plant
# or any operator.

import ast
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, "sheet-structure-scan"))
sys.path.insert(0, os.path.join(ROOT, "readout-count"))

import hop_compose as HC              # noqa: E402
import preentry_register as PR        # noqa: E402
import no_severity                    # noqa: E402

CHECKS = []


def ok(name, cond, detail=""):
    CHECKS.append((name, bool(cond), detail))


def close(x, y, tol=1e-9):
    return x is not None and y is not None and abs(x - y) <= tol


# --- composed_bias: the closed form, by hand -------------------------------

ok("single hop is its own offset (empty downstream product = 1)",
   close(HC.composed_bias([0.9], [1.0]), 1.0))
ok("two hops gain 0.9 same sign: 0.9*1 + 1 = 1.9",
   close(HC.composed_bias([0.9, 0.9], [1.0, 1.0]), 1.9))
ok("identity gain accumulates undamped: 1 + 1 = 2.0",
   close(HC.composed_bias([1.0, 1.0], [1.0, 1.0]), 2.0))
ok("all offsets zero is an EXACT zero",
   HC.composed_bias([0.9, 0.9], [0.0, 0.0]) == 0.0)

# --- the absence/zero split ------------------------------------------------

ok("unspecified gain is None, not zero",
   HC.composed_bias([0.9, None], [1.0, 1.0]) is None)
ok("length mismatch is None",
   HC.composed_bias([0.9], [1.0, 1.0]) is None)
ok("a real zero and an absence are different objects",
   HC.composed_bias([0.9], [0.0]) == 0.0
   and HC.composed_bias([0.9, None], [1.0, 1.0]) is None)

# --- retained gain and the DPI floor ---------------------------------------

ok("retained gain is the product of the per-hop gains",
   close(HC.retained_ground_gain([0.9, 0.9, 0.9]), 0.9 ** 3))
ok("retained gain is None when a gain is unspecified",
   HC.retained_ground_gain([0.9, None]) is None)
ok("DPI floor holds in the model: |a|<=1 gives non-increasing partial "
   "products", HC.gain_is_nonincreasing([0.9] * 8) is True)
ok("a gain above 1 breaks the non-increase (would violate the floor)",
   HC.gain_is_nonincreasing([1.5, 1.5]) is False)
ok("gain_is_nonincreasing is None on an unspecified gain",
   HC.gain_is_nonincreasing([0.9, None]) is None)

# --- rescaled bias: the reader who takes the terminal AS ground -------------

rb = HC.rescaled_bias([0.9, 0.9], [1.0, 1.0])
ok("rescaled bias is B/G and amplifies (|G|<=1)",
   rb["state"] == "OK" and close(rb["value"], 1.9 / 0.81))
dead = HC.rescaled_bias([0.9, 0.0, 0.9], [1.0, 1.0, 1.0])
ok("a dead hop makes the ground UNRECOVERABLE, value None not infinity",
   dead["state"] == "GROUND_UNRECOVERABLE" and dead["value"] is None)
nev = HC.rescaled_bias([0.9, None], [1.0, 1.0])
ok("rescaled bias is NOT_EVALUABLE on an unspecified gain",
   nev["state"] == "NOT_EVALUABLE" and nev["value"] is None)

# --- ensemble: directed compounds, random cancels; not constant ------------

rows = {r["N"]: r for r in HC.ensemble()}
ok("directed |bias| grows with N", rows[16]["directed_mean_abs_bias"]
   > rows[1]["directed_mean_abs_bias"])
ok("directed exceeds random at every N>1",
   all(rows[n]["directed_mean_abs_bias"] > rows[n]["random_mean_abs_bias"]
       for n in (2, 4, 8, 16)))
ok("the directed/random ratio grows with the chain",
   rows[16]["directed_over_random"] > rows[2]["directed_over_random"])
zero_mag = HC.ensemble(ns=(4,), magnitude=0.0)
ok("at magnitude 0 both arms are exactly 0 (NO_INCENTIVE) -- not constant",
   zero_mag[0]["directed_mean_abs_bias"] == 0.0
   and zero_mag[0]["random_mean_abs_bias"] == 0.0
   and zero_mag[0]["directed_verdict"] == "NO_INCENTIVE")
ok("the ensemble is deterministic under its seed",
   HC.ensemble(ns=(8,), seed=3) == HC.ensemble(ns=(8,), seed=3))

# --- pre-entry register ----------------------------------------------------

s = PR.register_summary()
ok("seven gates, none logged", s["gates"] == 7 and s["logged"] == 0)
ok("six gates condition which reports arrive", s["conditions_sample"] == 6)
ok("the arriving-reports reading is a threshold sample, not machine "
   "conditions", "per-operator threshold" in s["arriving_reports_are"])
ok("the threshold is recorded as unestimated", s["threshold_estimated"]
   is False)
ok("every gate carries a cost string",
   all(g["cost"] for g in PR.GATES))
ok("L0' is marked the strongest and DELEGATION marked as breaking Test B",
   any(g.get("strongest") for g in PR.GATES if g["id"] == "L0'")
   and any(g.get("breaks_test_b") for g in PR.GATES
           if g["id"] == "DELEGATION"))

# --- Test B calibration: both branches reachable ---------------------------

cal = PR.calibration(PR.make_world(calibrated=True))
unc = PR.calibration(PR.make_world(calibrated=False))
ok("calibrated world TRACKS", cal["verdict"] == "TRACKS_calibrated"
   and cal["rho"] >= PR.TRACK_RHO)
ok("uncalibrated world DOES_NOT_TRACK", unc["verdict"] == "DOES_NOT_TRACK")
ok("calibration is not a constant classifier",
   cal["verdict"] != unc["verdict"])

# --- the STATED LIMITATION: undeclared proxy -> UNESTIMABLE -----------------

ref = PR.calibration(PR.make_world(), proxy_declared=False)
ok("undeclared proxy count returns UNESTIMABLE, not a number",
   ref["verdict"] == "UNESTIMABLE_PROXY_UNDECLARED" and ref["rho"] is None)
ok("the refusal states why (silently conditioned on people who can type)",
   "who can type" in ref["why"])

# --- delegation confound made a number -------------------------------------

dc = PR.delegation_corruption(PR.make_world(calibrated=True))
clean = dc["declared_and_excluded"]
pooled = dc["pooled_as_zero"]
ok("declared-and-excluded reading stays calibrated",
   clean["verdict"] == "TRACKS_calibrated")
ok("pooling proxy-filers as zero-reporters pulls the correlation down",
   pooled["rho"] < clean["rho"])
ok("the confound can flip the verdict (the cost of not declaring)",
   pooled["verdict"] == "DOES_NOT_TRACK"
   and clean["verdict"] == "TRACKS_calibrated")

# --- spearman is imported, not restated ------------------------------------

src = open(os.path.join(HERE, "preentry_register.py"), encoding="utf-8").read()
ok("spearman is imported from readout-count, not defined here",
   "from readout_count import spearman" in src
   and "def spearman" not in src)

# --- renders screen clean through no_severity ------------------------------

for name, mod in (("hop_compose", HC), ("preentry_register", PR)):
    R = mod.render()
    h = no_severity.hits(R)
    ok("%s render screens clean (no exemption)" % name, not h,
       str(h)[:200])

# --- module hygiene --------------------------------------------------------

for fn in ("hop_compose.py", "preentry_register.py", "test_hop.py"):
    b = open(os.path.join(HERE, fn), "rb").read()
    ok("%s is ASCII" % fn, all(x < 128 for x in b))
    ast.parse(b.decode("ascii"), feature_version=(3, 9))
    ok("%s parses under 3.9" % fn, True)

for fn in ("hop_compose.py", "preentry_register.py"):
    p = subprocess.run([sys.executable, os.path.join(HERE, fn), "--selftest"],
                       capture_output=True)
    ok("%s refuses --selftest with exit 2" % fn, p.returncode == 2)
    p = subprocess.run([sys.executable, os.path.join(HERE, fn)],
                       capture_output=True)
    ok("%s bare invocation renders and exits 0" % fn,
       p.returncode == 0 and len(p.stdout) > 200)

# --- WORK_ORDER landed verbatim, README present ----------------------------

wo = os.path.join(HERE, "WORK_ORDER.md")
_wo_ascii = open(wo, "rb").read().decode("ascii", "ignore")
ok("WORK_ORDER.md present and is WO-5",
   os.path.exists(wo) and "WO-5" in _wo_ascii
   and "Hop distance and pre-entry loss" in _wo_ascii)
README = open(os.path.join(HERE, "README.md"), encoding="utf-8").read()
README_FLAT = " ".join(README.split())
ok("README carries no author or working-style section",
   not re.search(r"^#+ .*(author|working style)", README, re.I | re.M))
ok("README states the transit/pre-entry split and the CONSTRUCTED scope",
   "TRANSIT LOSS" in README_FLAT and "PRE-ENTRY LOSS" in README_FLAT
   and "CONSTRUCTED" in README_FLAT)

# ---------------------------------------------------------------------------

failed = [(n, d) for n, o, d in CHECKS if not o]
for n, o, d in CHECKS:
    print("%s  %s%s" % ("ok  " if o else "FAIL", n,
                        ("  -- " + d) if (d and not o) else ""))
print()
print("checks: %d   failed: %d" % (len(CHECKS), len(failed)))
sys.exit(1 if failed else 0)
