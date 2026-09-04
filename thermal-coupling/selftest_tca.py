#!/usr/bin/env python3
"""Checks for coupling_audit.py against the delivered thermal_coupling.py.
The delivered module is imported and never edited. Nothing here is a
statement about any slope, snowpack or the cited literature.

    python3 thermal-coupling/selftest_tca.py
"""

import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "sheet-structure-scan"))
import coupling_audit as A  # noqa: E402
import thermal_coupling as TC  # noqa: E402
import no_severity  # noqa: E402

FAILS = []
N = [0]


def check(name, cond):
    N[0] += 1
    if not cond:
        FAILS.append(name)
        print("  FAIL  " + name)


def main():
    print("selftest_tca")

    # ---- the delivered module runs and its demos reproduce
    demo = subprocess.run([sys.executable, os.path.join(HERE, "thermal_coupling.py")],
                          capture_output=True, text=True)
    check("delivered module runs rc 0", demo.returncode == 0)
    check("Demo A low band COINC 0.1756 as pinned", "0.1756" in demo.stdout)
    check("Demo D unprimed coincidence 0.0000", "0.0000" in demo.stdout)

    # ---- 1. calibration
    c = A.calibration()
    check("50 deg crossing at -1.99 C with fracture_favorable", c["favorable"] == -1.99)
    check("no crossing on [-10, -0.5] under the default flag", c["unfavorable"] is None and c["fos_50_at_-0.5_unfavorable"] > 1.0)
    check("crossing scan returns None on a flat-above-1 slope", A.fos_crossing(30, False) is None)
    check("crossing scan finds a steep slope's crossing", A.fos_crossing(65, False) is not None)

    # ---- 2. TC-04 shape
    sh = A.strength_shape()
    check("sensitivity falls toward 0 C in the delivered function", sh["sensitivity_rises_toward_0"] is False)
    check("loss is concave across the domain", sh["loss_second_difference"] == "negative (loss concave)")
    check("cold slope steeper than warm by more than 3x", abs(sh["slope_cold"] / sh["slope_warm"]) > 3.0)
    check("creep_sensitivity rises toward 0 C", sh["creep_rises_toward_0"])
    check("strength clamps above -0.2 C", sh["clamp_top"])
    # the claim's own criterion on a constructed convex-loss curve
    conv = [1.0 - 0.71 * ((t + 10) / 9.5) ** 2.0 for t in (-9.5, -1.0)]
    d_cold = 0.71 * 2 * ((-9.5 + 10) / 9.5) / 9.5
    d_warm = 0.71 * 2 * ((-1.0 + 10) / 9.5) / 9.5
    check("a convex loss (exponent 2) would have the warm slope steeper -- the criterion discriminates", d_warm > d_cold and conv[0] > conv[1])

    # ---- 3. constants
    cc = A.constant_census()
    check("more than one numeric literal lives in function bodies", cc["total_literals"] > 1)
    check("seven functions carry literals with no source in their docstring", len(cc["functions_with_uncited_literals"]) == 7)
    check("CAL_FOS read back", cc["cal_fos"] == TC.CAL_FOS == 2.825)

    # ---- 4. TC-01
    ls = A.lag_span()
    check("five lag classes over 4.56 decades", ls["classes"] == 5 and abs(ls["decades"] - 4.56) < 0.01)

    # ---- 5. TC-02
    pa = A.product_vs_additive()
    check("unprimed is 0 under the product and non-zero under the additive",
          pa["unprimed_is_zero_under_product"] and pa["unprimed_nonzero_under_additive"])
    check("BOTH ranks first under either form", pa["rank_product"][0] == "BOTH" and pa["rank_additive"][0] == "BOTH")

    # ---- 6. TC-03
    ft = A.freeze_thaw_profile()
    check("freeze-thaw profile has an interior peak at +/-3 and is symmetric about 0",
          ft["interior_peak"] and ft["peak_t"] == [-3, 3] and ft["symmetric_about_0"])
    check("a dip at 0 between the two peaks", ft["dip_at_0"])
    sn = A.snow_half_implemented()
    check("snow depth is never assigned in the module; weak_layer_index takes it as an input",
          sn["depth_assigned_anywhere"] is False and "depth_m" in sn["weak_layer_index_args"])
    check("weak_layer_index is independent of temperature at fixed gradient",
          TC.weak_layer_index(-10, -5, 1.0) == TC.weak_layer_index(-3, 2, 1.0))
    check("weak_layer_index returns 0 below the depth floor", TC.weak_layer_index(-10, 0, 0.05) == 0.0)

    # ---- 7. TC-06
    ss = A.snow_sweep()
    check("total is non-monotone across the sweep", ss["total_non_monotone"])
    check("a step exists with count down and runout up", ss["any_step_with_count_down_and_runout_up"])
    check("no step with count down and coincidence up", ss["any_step_with_count_down_and_coincidence_up"] is False)
    check("runout does not enter the coincidence term", ss["runout_in_coincidence_term"] is False)
    check("runout multiplier is 1 + 0.35 w exactly", abs(TC.avalanche_activity(5.0, 0, 0, 1.0)["runout_multiplier"] - 1.35) < 1e-3)

    # ---- 8. referents
    rf = A.referents()
    check("earth-systems-physics folder is absent", rf["earth_systems_physics_folder"] is False)
    check("the module cites rate-mismatch-polytope, at least ten other files do, and it exists nowhere",
          rf["module_cites_polytope"] and rf["rate_mismatch_polytope_files_citing"] >= 10 and rf["polytope_exists"] is False)
    check("Biskaborn's 0.19 is used in no function", rf["biskaborn_0_19_used_in_code"] is False)

    # ---- 9. the extension
    ex = A.extension()
    check("F1, F2, F3 hold as facts about the core module",
          ex["F1_core_uses_snow_temp_no_air"] and ex["F2_core_has_no_blast"] and ex["F3_core_fastest_is_snowpack"])
    check("coupling bounds 8.87..18.37 match the stated 8.9..18.4",
          abs(ex["coupling_bounds"][0] - 8.87) < 0.01 and abs(ex["coupling_bounds"][1] - 18.37) < 0.01)
    check("meltwater ratio from the function is 6.00 against a stated calibration of 2.3",
          abs(ex["melt_ratio_19_over_minus1"] - 6.0) < 1e-9 and ex["melt_ratio_stated"] == 2.3)
    check("blast anchors not reproduced: 13.0 vs >15 and 3.9 vs 2.5",
          abs(ex["blast_full_mean_kPa"] - 12.996) < 0.01 and abs(ex["blast_none_mean_kPa"] - 3.931) < 0.01)
    check("peak over mean is the stated 1.9", abs(ex["peak_over_mean"] - 1.9) < 1e-12)
    check("footprint anchor reproduces at 10 kPa", abs(ex["footprint_at_10kPa"] - 0.8) < 1e-12)
    check("diurnal max at 15 h and min at 3 h", ex["diurnal_max_hour"] == 15 and ex["diurnal_min_hour"] == 3)
    check("diurnal class is 1.38 decades below snowpack", abs(ex["diurnal_decades_faster"] - 1.38) < 0.01)
    check("the extension copies LAG rather than importing the core",
          ex["extension_imports_core"] is False and ex["shared_lag_classes"] == 5 and ex["shared_identical"])
    check("TC-10's direction terms are in no function and the runout multiplier is not read",
          ex["tc10_direction_in_code"] is False and ex["runout_multiplier_read_by_extension"] is False)
    demo2 = subprocess.run([sys.executable, os.path.join(HERE, "airblast_extension.py")],
                           capture_output=True, text=True)
    check("extension demo runs and prints its own 6.00 beside the published 2.30",
          demo2.returncode == 0 and "6.00" in demo2.stdout and "2.30" in demo2.stdout)

    # ---- CLI and screen
    rc = subprocess.run([sys.executable, os.path.join(HERE, "coupling_audit.py"), "--selftest"], capture_output=True).returncode
    check("coupling_audit refuses --selftest with rc 2", rc == 2)
    out = A.render()
    check("render screens clean", not no_severity.hits(out))
    check("screen fires on a planted word", bool(no_severity.hits(out + "\nthis is wrong\n")))
    with open(os.path.join(HERE, "samples", "coupling_audit.sample.txt"), "w", encoding="utf-8") as fh:
        fh.write(out)
    print("selftest: %d checks, %d failed" % (N[0], len(FAILS)))
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
