#!/usr/bin/env python3
"""Checks for audit.py against the delivered scripts, which are imported
and never edited. Known answers first, both directions. Writes samples/.

    python3 railcar-containment/selftest_rail.py
"""

import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "sheet-structure-scan"))
import audit as A  # noqa: E402
import tenability as T  # noqa: E402
import t_hold as H  # noqa: E402
import detection_loop as D  # noqa: E402
import no_severity  # noqa: E402

FAILS = []
N = [0]


def check(name, cond):
    N[0] += 1
    if not cond:
        FAILS.append(name)
        print("  FAIL  " + name)


def main():
    print("selftest_rail")
    check("audit refuses --selftest with rc 2",
          subprocess.run([sys.executable, os.path.join(HERE, "audit.py"), "--selftest"], capture_output=True).returncode == 2)
    check("all seven delivered files present", all(os.path.exists(os.path.join(HERE, f)) for f in A.DELIVERED))
    c = A.constraints()
    check("delivered scripts are stdlib-only", all(not v["non_stdlib"] for v in c.values()))
    check("t_hold imports math and never uses it", c["t_hold.py"]["imported_unused"] == ["math"])

    # ---- calibration
    an = A.anchor()
    check("CO and visibility anchors reproduce exactly; thermal lands 127.5 s short of its 400 s anchor",
          an["anchor_residuals"]["co"] == 0.0 and an["anchor_residuals"]["od"] == 0.0 and abs(an["anchor_residuals"]["temp"] + 127.5) < 1e-9)
    check("thermal anchor 400 s lies past the end of the source term at 290 s",
          T.ANCHORS_S["temp"] > T.ASSUMPTIONS["vent_rise_s"] + T.ASSUMPTIONS["vent_peak_s"] + T.ASSUMPTIONS["vent_decay_s"])
    coef = A._coef()
    a = dict(T.ASSUMPTIONS)
    r = T.simulate(a["V_intercity_m3"] * 1.02, 1.0, coef, a)
    check("two percent more volume and the thermal channel is never crossed: calibrated to the edge of never", r["t_thermal_s"] is None)
    check("t_available at anchor is 230 s, the visibility channel, inside the published window",
          an["t_available"] == 230.0 and an["binding_channel"] == "od" and an["inside_window"])
    # positive control on the calibrator: a reachable target is hit
    one = T.calibrate(a, {"od": 150.0})
    check("calibrator hits a reachable target to within one time step (DT 0.5 s)",
          abs(A.T.simulate(a["V_intercity_m3"], 1.0, one, a)["t_visibility_s"] - 150.0) <= T.DT)

    # ---- volume
    vs = A.volume_scaling()
    check("t_available is monotone in volume (RC_001's sign)", vs["monotone_in_volume"])
    check("subway/intercity ratio 0.515 as the delivered screen prints", abs(vs["subway_over_intercity"] - 0.515) < 0.002)
    ex = vs["exponent_range"]["min"]
    check("the volume exponent of t_available spans more than a factor of two (0.79 to 2.23)", ex[0] < 1.0 < ex[1] and ex[1] / ex[0] > 2)
    check("the binding channel switches from visibility to CO dose at 200 m3", vs["binding"][160] == "od" and vs["binding"][200] == "co")

    # ---- containment
    cf = A.containment_form()
    check("tenability never crossed at fractions 0.1 and 0.05; the linear stretch has a value there",
          cf["never_crossed_at"] == [0.1, 0.05] and cf["rows"][0.1]["detection_loop_stretch"] == 2300.0)
    check("where both are defined tenability exceeds the linear stretch by 1.2 to 1.34",
          all(1.19 < v["ratio_tenability_over_stretch"] < 1.35 for f, v in cf["rows"].items() if v["ratio_tenability_over_stretch"] and f < 1.0))
    vc = A.volume_vs_containment()
    check("RC_002 arithmetic: containment to 0.5 gives 2.43x, volume 100 -> 160 gives 1.94x, same order",
          abs(vc["containment_ratio_half"] - 2.43) < 0.01 and abs(1 / vc["volume_ratio_100_over_160"] - 1.94) < 0.01)
    check("at fraction 0.2 containment gives 6.7x, which is where the claim's own falsifier is scoped", abs(vc["containment_at_0_2"] / cf["base"] - 6.72) < 0.02)

    # ---- t_hold
    hr = A.hold_requirements()
    check("t_hold reads none of the params file's offgas_to_flame_s", not hr["offgas_key_read_by_t_hold"])
    check("t_hold applies a default 1.5 margin where the README envelope says none applied", hr["default_margin"] == 1.5 and A.envelope_of_readme()["margin_in_readme"])
    lat = {"sensor_detect_s": 15, "visual_detect_s": 120, "crew_decide_s": 30}
    line = {"max_run_to_egress_m": 900, "line_speed_mps": 18.0, "decel_mps2": 1.0, "door_release_s": 10, "platform_clear_s": 90, "tunnel_walkout_s": 600, "underground": True}
    check("t_hold known answer: visual/STOP = 120+30+18+10+600 = 778", H.required_hold(line, lat, "visual", "stop")["t_hold_required_s"] == 778.0)
    check("t_hold known answer: sensor/RUN = 15+30+(900/18+8)+10+90 = 203", H.required_hold(line, lat, "sensor", "run")["t_hold_required_s"] == 203.0)
    check("walkout is the largest term on both tunnel lines (0.77, 0.89) and not on the surface line",
          hr["clear_dominates_worst"]["metro_long_tunnel"] > 0.85 and hr["clear_dominates_worst"]["intercity_surface"] < 0.5)

    # ---- detection loop
    sh = A.shift_arithmetic()
    check("sensor arm's mean lead is 130 s against a tunnel deficit of 728 s before detection", sh["mean_lead_s"] == 130.0 and sh["tunnel_deficit_before_detection_s"] == 728.0)
    de = A.detection_by_egress(trials=1500)
    check("detection gain is largest near egress 240 s and below 0.05 at 900 s; containment gain rises past 0.85",
          de[240]["detection_gain"] > de[900]["detection_gain"] and de[900]["detection_gain"] < 0.05 and de[900]["containment_gain"] > 0.85)
    check("the station case is RC_005's own falsifier: detection alone moves P(clear) by more than 0.4", de[240]["detection_gain"] > 0.4)
    p = dict(D.DEFAULTS, egress_action_mean_s=0.0, egress_action_sd_s=0.0, crew_decide_mean_s=0.0, crew_decide_sd_s=0.0,
             visual_detect_mean_s=0.0, visual_detect_sd_s=0.0)
    check("detection loop known answer: with every latency zero both arms clear every trial", D.run_arm("visual", 500, 1.0, p, 1)["p_cleared"] == 1.0)
    p2 = dict(D.DEFAULTS, egress_action_mean_s=1e6, egress_action_sd_s=0.0)
    check("and with an unreachable egress neither arm ever clears", D.run_arm("sensor", 500, 0.2, p2, 1)["p_cleared"] == 0.0)

    # ---- envelope of the README, sibling instrument
    er = A.envelope_of_readme()
    check("README scores 4 of 6 on the sibling instrument, E5 and E6 absent, row valid",
          er["row"]["envelope_score"] == 4 and er["row"]["E5"] == 0 and er["row"]["E6"] == 0 and er["valid"])

    # ---- render and screen
    out = A.render()
    hits = {w for _, w, _ in no_severity.hits(out)}
    check("audit render screens clean", not hits)
    check("screen fires on a planted word", bool(no_severity.hits(out + "\nthis is wrong\n")))
    os.makedirs(os.path.join(HERE, "samples"), exist_ok=True)
    with open(os.path.join(HERE, "samples", "audit.sample.txt"), "w", encoding="utf-8") as fh:
        fh.write(out + "\n")
    ra = subprocess.run([sys.executable, os.path.join(HERE, "run_all.py")], capture_output=True, text=True, cwd=HERE)
    check("delivered run_all runs end to end", ra.returncode == 0 and "DETECTION LOOP" in ra.stdout)
    with open(os.path.join(HERE, "samples", "run_all.sample.txt"), "w", encoding="utf-8") as fh:
        fh.write(ra.stdout)
    print("selftest: %d checks, %d failed" % (N[0], len(FAILS)))
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
