"""
battery-offgas-prearm / test_prearm.py -- checks for prearm.py.

License: CC0. Stdlib only. Parses under Python 3.9.
SELF-GRADED: the module and these checks share an author, so a pass is a
regression result, not a validation. The fixtures are CONSTRUCTED shapes.

    python3 battery-offgas-prearm/test_prearm.py
"""

import ast
import json
import math
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import prearm as P  # noqa: E402

CHECKS = []


def check(name, ok, detail=""):
    CHECKS.append((name, bool(ok), detail))


def near(a, b, tol=1e-9):
    return a is not None and abs(a - b) <= tol


CFG = P.demo_config()
BREATH = P.fx_breathing()
RAMP, RUNAWAY_S = P.fx_runaway()
GLITCH = P.fx_glitch()

# --- the three required checks ---------------------------------------------
r = P.evaluate(CFG, {"gas": BREATH})
check("breathing -> no trigger", r["detect_t"] is None and not r["actions"],
      str(r["actions"]))
check("breathing is ARMED, not UNRATED (the quiet is a measurement)",
      r["status"] == P.ARMED)

r = P.evaluate(CFG, {"gas": RAMP})
t0 = [a for a in r["actions"] if a["tier"] == 0]
check("ramp above rate threshold -> tier 0 fires",
      len(t0) == 1 and t0[0]["action"] == "OPEN_DISCONNECT", str(r["actions"]))
check("tier 0 fires before the constructed runaway",
      r["detect_t"] is not None and r["detect_t"] < RUNAWAY_S,
      "detect %s runaway %s" % (r["detect_t"], RUNAWAY_S))
check("tier 0 fires after the constructed onset (no false early trip)",
      r["detect_t"] is not None and r["detect_t"] > 1800.0)
check("tiers fire in order 0,1,2 at one instant",
      [a["tier"] for a in r["actions"]] == [0, 1, 2]
      and len({a["t"] for a in r["actions"]}) == 1)
check("tier 0 reason says latched", "latched" in t0[0]["reason"])

for thr in (None, 0, -1, "1.0", float("nan"), True):
    cfg = json.loads(json.dumps(CFG))
    cfg["channels"]["gas"]["rate_threshold"] = thr
    r = P.evaluate(cfg, {"gas": RAMP})
    check("no usable threshold (%r) -> UNRATED, refuse to arm" % (thr,),
          r["status"] == P.UNRATED and not r["actions"]
          and "refuse to arm" in r.get("refusal", ""), str(r))

# --- glitch rejection and the finding that forced it ----------------------
r = P.evaluate(CFG, {"gas": GLITCH})
check("single one-sample spike -> no trigger (Theil-Sen)",
      r["detect_t"] is None, str(r["actions"]))
orig = P.slope
try:
    P.slope = P.slope_lsq
    r_lsq = P.evaluate(CFG, {"gas": GLITCH})
finally:
    P.slope = orig
check("BOP_005 pinned: least-squares slope DOES trip on that spike",
      r_lsq["detect_t"] is not None,
      "if this goes red the finding that chose Theil-Sen no longer holds")

def _pulse(width):
    s = P.fx_breathing(seed=3, duration_s=1800)
    return [(t, v + (2000 if 900 <= t < 900 + 5 * width else 0)) for t, v in s]


check("BOP_010 boundary: 6-sample (30 s) step does not fire at window 60 s",
      P.evaluate(CFG, {"gas": _pulse(6)})["detect_t"] is None)
check("BOP_010 boundary: 7-sample (35 s) step fires -- a step this long is "
      "a sustained rise and rate alone cannot tell it from onset",
      P.evaluate(CFG, {"gas": _pulse(7)})["detect_t"] is not None)

# --- slope known answers ---------------------------------------------------
line = [(t, 3.0 + 2.0 * t) for t in range(10)]
check("slope of a straight line is its gradient", near(P.slope(line), 2.0))
check("lsq slope of a straight line is its gradient",
      near(P.slope_lsq(line), 2.0))
spiked = list(line); spiked[5] = (5, 1e6)
check("Theil-Sen ignores one outlier", near(P.slope(spiked), 2.0))
check("lsq does not", not near(P.slope_lsq(spiked), 2.0, 1.0))
check("flat line slope is 0.0, a measurement",
      P.slope([(t, 7.0) for t in range(5)]) == 0.0)
check("one point -> None, never 0.0", P.slope([(1, 2)]) is None)
check("no time spread -> None", P.slope([(1, 2), (1, 5)]) is None)
check("non-finite samples are dropped",
      near(P.slope([(0, 0.0), (1, float("nan")), (2, 2.0)]), 1.0))

# --- partial rating, faults, ceilings --------------------------------------
cfg = json.loads(json.dumps(CFG))
cfg["channels"]["h2"] = {"rate_threshold": None}
r = P.evaluate(cfg, {"gas": RAMP, "h2": BREATH})
check("one rated + one unrated -> ARMED_PARTIAL, unrated listed",
      r["status"] == P.PARTIAL and r["unrated"] == ["h2"]
      and r["detect_channel"] == "gas")

for key in ("window_s", "confirm_count", "max_gap_s", "on_sensor_fault"):
    cfg = json.loads(json.dumps(CFG)); cfg.pop(key)
    r = P.evaluate(cfg, {"gas": RAMP})
    check("missing %s -> UNRATED naming it" % key,
          r["status"] == P.UNRATED and key in r["missing"])

gap = [s for s in BREATH if not (600 < s[0] < 700)]
cfg = json.loads(json.dumps(CFG)); cfg["on_sensor_fault"] = "ALARM"
r = P.evaluate(cfg, {"gas": gap})
check("sample gap + ALARM policy -> ALARM, no disconnect",
      any(a["action"] == "ALARM" for a in r["actions"])
      and not any(a["tier"] == 0 for a in r["actions"]))
cfg["on_sensor_fault"] = "TRIP"
r = P.evaluate(cfg, {"gas": gap})
check("sample gap + TRIP policy -> tier 0 fires on the fault",
      any(a["tier"] == 0 and "SENSOR_FAULT" in a["reason"]
          for a in r["actions"]))
r = P.evaluate(CFG, {"gas": [(0, 1.0), (5, float("inf")), (10, 1.0)]})
check("non-finite reading is a fault, not a value",
      any(f["fault"] == "NON_FINITE_VALUE" for f in r["faults"]))
r = P.evaluate(CFG, {})
check("rated channel with no samples -> NO_SAMPLES fault, no trigger",
      any(f["fault"] == "NO_SAMPLES" for f in r["faults"])
      and r["detect_t"] is None)

cfg = json.loads(json.dumps(CFG)); cfg["level_ceiling"] = {"gas": 450.0}
r = P.evaluate(cfg, {"gas": BREATH})
check("declared level ceiling catches a slow high level rate misses",
      r["detect_t"] is not None and "LEVEL_CEILING" in r["actions"][0]["reason"])

# --- tier 2 interlock ------------------------------------------------------
for space in (None, "BASEMENT", "GARAGE", "vented"):
    cfg = json.loads(json.dumps(CFG)); cfg["tier2_discharge_space"] = space
    r = P.evaluate(cfg, {"gas": RAMP})
    t2 = [a for a in r["actions"] if a["tier"] == 2]
    check("tier 2 discharge space %r -> NOT_ARMED, tier 0 still fires" % space,
          t2 and t2[0]["action"] == "TIER2_NOT_ARMED"
          and any(a["tier"] == 0 for a in r["actions"]))
cfg = json.loads(json.dumps(CFG)); cfg["tier2_installed"] = False
r = P.evaluate(cfg, {"gas": RAMP})
check("tier 2 not installed -> NOT_ARMED with that reason",
      r["actions"][-1]["reason"] == "tier 2 not installed")

# --- margins and hazard arithmetic -----------------------------------------
check("heat margin HOLDS at 12/10", P.heat_margin(12, 10)["verdict"] == "HOLDS")
check("heat margin SHORT at 8/10", P.heat_margin(8, 10)["verdict"] == "SHORT")
check("heat margin UNMEASURED with None, ratio None",
      P.heat_margin(None, 10) == {"verdict": "UNMEASURED", "ratio": None})
check("cascade FIRST_CELL_WINDOW",
      P.cascade_margin(60, 20, 30)["verdict"] == "FIRST_CELL_WINDOW")
check("cascade NEIGHBOURS_ONLY",
      P.cascade_margin(10, 20, 30)["verdict"] == "NEIGHBOURS_ONLY")
check("cascade MARGIN_TOO_SHORT -> geometry, not relay",
      P.cascade_margin(-40, 20, 30)["verdict"] == "MARGIN_TOO_SHORT")
check("cascade UNMEASURED with any None",
      P.cascade_margin(60, None, 30)["verdict"] == "UNMEASURED")
check("pcm mass: 20 kJ at 200 kJ/kg -> 0.1 kg",
      near(P.pcm_mass_kg(20000, 200000), 0.1))
check("pcm mass None on absent latent", P.pcm_mass_kg(20000, None) is None)
check("co2 1 kg into 2 m3 is ~24%, far over the 4% IDLH",
      near(P.co2_fraction(1.0, 2.0), 1 - math.exp(-(1 / 1.84) / 2), 1e-12)
      and P.co2_fraction(1.0, 2.0) > 0.04 * 5)
check("co2 small release ~ V/room", near(P.co2_fraction(0.0184, 100.0), 1e-4,
                                         1e-7))
check("co2 None on no space", P.co2_fraction(1.0, 0) is None)

# --- structural ------------------------------------------------------------
src = open(os.path.join(HERE, "prearm.py")).read()
tree = ast.parse(src)
imports = {a.name.split(".")[0] for n in ast.walk(tree)
           if isinstance(n, ast.Import) for a in n.names}
imports |= {n.module.split(".")[0] for n in ast.walk(tree)
            if isinstance(n, ast.ImportFrom) and n.module}
check("stdlib only", imports <= {"json", "math", "random", "sys"},
      str(imports))
cfg_example = json.load(open(os.path.join(HERE, "config.example.json")))
check("shipped example config carries NO threshold number",
      all(c.get("rate_threshold") is None
          for c in cfg_example["channels"].values()))
check("shipped example config refuses to arm",
      P.load_config(cfg_example)["status"] == P.UNRATED)
check("four [CHOICE n] declared and each cited in a comment",
      len(P.CHOICES) == 4 and all(src.count("[CHOICE %d]" % i) >= 2
                                  for i in range(1, 5)))
p = subprocess.run([sys.executable, os.path.join(HERE, "prearm.py"),
                    "--selftest"], capture_output=True, text=True)
check("--selftest refuses with exit 2 naming this file",
      p.returncode == 2 and "test_prearm.py" in p.stderr)
p = subprocess.run([sys.executable, os.path.join(HERE, "prearm.py"),
                    "--demo"], capture_output=True, text=True)
sample = os.path.join(HERE, "samples", "demo.sample.txt")
check("demo matches the pinned sample",
      p.returncode == 0 and os.path.exists(sample)
      and p.stdout == open(sample).read())

# ---------------------------------------------------------------------------
failed = [c for c in CHECKS if not c[1]]
for name, ok, detail in CHECKS:
    print("%-4s %s%s" % ("ok" if ok else "FAIL", name,
                         ("\n       %s" % detail) if detail and not ok else ""))
print()
print("checks: %d   failed: %d" % (len(CHECKS), len(failed)))
sys.exit(1 if failed else 0)
