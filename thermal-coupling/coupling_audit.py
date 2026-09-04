#!/usr/bin/env python3
"""coupling_audit -- the delivered thermal_coupling module checked against
its own claims.

`thermal_coupling.py` is a MARKER module: one forcing (temperature)
entering a hazard chain at five lag classes, a product-form coincidence
term, six claims TC-01..TC-06 under a refutation protocol, and the
statement that CAL_FOS is its only free parameter. This module imports
it, changes nothing, and computes what its docstrings and claim table
assert from its own functions:

  1. the CAL_FOS calibration sentence -- where a 50 deg slope crosses
     FoS = 1, under each value of the flag the sentence does not name;
  2. TC-04 as a shape -- the sign of the second difference of the
     joint-strength curve, and the first derivative at the cold and
     warm ends;
  3. the constant census -- every numeric literal inside a function
     body, by AST, against the functions' own docstrings;
  4. TC-01 -- the lag span in decades;
  5. TC-02 -- the product against an additive counterpart on the
     module's own Demo D scenarios;
  6. TC-03 -- freeze-thaw non-monotonicity measured, and whether the
     snow half is implemented (does depth depend on temperature in the
     code?);
  7. TC-06 -- a sweep of snow temperature for total count against
     runout and coincidence;
  8. named referents -- the folder the module says it belongs to, the
     wiki-link it cites, and one header source not used in any function.

Nothing here is a statement about any slope, snowpack, or the cited
literature, which was not read (allowlist egress).

CC0. stdlib only. Parses under Python 3.9.
"""

import ast
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, HERE)
import thermal_coupling as TC  # noqa: E402

SRC = os.path.join(HERE, "thermal_coupling.py")


def _src():
    with open(SRC, encoding="utf-8") as fh:
        return fh.read()


# ------------------------------------------------------- 1. calibration

def fos_crossing(slope_deg, fracture_favorable, lo=-10.0, hi=-0.5, step=0.01):
    """Warmest-to-coldest scan for the temperature at which FoS crosses
    1 for the given slope; None if it never does on [lo, hi]."""
    t = lo
    prev = TC.factor_of_safety(t, slope_deg, fracture_favorable)
    while t < hi:
        t2 = min(hi, t + step)
        cur = TC.factor_of_safety(t2, slope_deg, fracture_favorable)
        if prev >= 1.0 > cur:
            return round(t2, 2)
        prev, t = cur, t2
    return None


def calibration():
    return {
        "favorable": fos_crossing(50, True),
        "unfavorable": fos_crossing(50, False),
        "band_stated": (-3.0, -0.5),
        "point_stated": -2.0,
        "fos_50_at_-0.5_unfavorable": round(TC.factor_of_safety(-0.5, 50, False), 3),
    }


# ------------------------------------------------------------ 2. TC-04

def strength_shape(overburden_m=10.0, a=-9.5, b=-1.0, h=0.01):
    """First derivative of joint strength at two temperatures and the
    sign of the second difference across the domain."""
    def s(t):
        return TC.joint_shear_strength_ratio(t, overburden_m)

    def d1(t):
        return (s(t + h) - s(t - h)) / (2 * h)
    ts = [a + i * (b - a) / 40 for i in range(41)]
    # second difference of the LOSS (1 - strength), the quantity TC-04 names
    second = [-(s(t + h) - 2 * s(t) + s(t - h)) for t in ts]
    return {"slope_cold": d1(a), "slope_warm": d1(b),
            "sensitivity_rises_toward_0": abs(d1(b)) > abs(d1(a)),
            "loss_second_difference": "positive (loss convex)" if all(x > 0 for x in second)
            else "negative (loss concave)" if all(x < 0 for x in second) else "mixed",
            "creep_rises_toward_0": TC.creep_sensitivity(-1) > TC.creep_sensitivity(-9),
            "clamp_top": TC.joint_shear_strength_ratio(0.0) == TC.joint_shear_strength_ratio(-0.2)}


# ------------------------------------------------- 3. constant census

def constant_census():
    """Numeric literals inside function bodies, per function, with the
    literal 0.0 / 1.0 / 2 style structural constants excluded, and
    whether the function's docstring names a source."""
    tree = ast.parse(_src())
    trivial = {0, 1, 2, 0.0, 1.0, 2.0, 100, 365, 360, 10.0}
    out = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            doc = ast.get_docstring(node) or ""
            cited = any(k in doc for k in ("et al", "Mamot", "Steinkogler", "Kaeab", "Arenson", "Swiss"))
            lits = []
            for n in ast.walk(node):
                if isinstance(n, ast.Constant) and isinstance(n.value, (int, float)) and not isinstance(n.value, bool):
                    if n.value not in trivial:
                        lits.append(n.value)
            out[node.name] = {"literals": lits, "docstring_cites": cited}
    module_level = [n.value for n in ast.walk(tree)
                    if isinstance(n, ast.Assign) and isinstance(n.value, ast.Constant)
                    and isinstance(n.value.value, (int, float))]
    return {"functions": out,
            "total_literals": sum(len(v["literals"]) for v in out.values()),
            "functions_with_uncited_literals": [k for k, v in out.items() if v["literals"] and not v["docstring_cites"]],
            "cal_fos": TC.CAL_FOS}


# ------------------------------------------------------------ 4. TC-01

def lag_span():
    taus = [v[1] for v in TC.LAG.values()]
    return {"classes": len(taus), "decades": math.log10(max(taus) / min(taus))}


# ------------------------------------------------------------ 5. TC-02

def demo_d_scenarios():
    scen = [("cold dry-slab trig", -14.0, -1.0, 0.9, 60),
            ("trigger, unprimed", -0.5, -9.0, 0.1, 2),
            ("BOTH", -0.5, -1.0, 0.9, 60)]
    out = {}
    for name, tsnow, tmean, retreat, yrs in scen:
        s = TC.chain_state(tsnow, tsnow - 1, tsnow + 3, 1.0, tmean, 8.0, 55, retreat, yrs, 0.9, 1.0)
        L = s["lag_class_states"]
        factors = [L["snowpack_trigger"], L["bedrock_primed"], L["sediment_primed"], L["debuttress_primed"]]
        out[name] = {"product": s["COINCIDENCE"], "additive": round(sum(factors) / len(factors), 4)}
    return out


def product_vs_additive():
    d = demo_d_scenarios()
    rank_p = sorted(d, key=lambda k: -d[k]["product"])
    rank_a = sorted(d, key=lambda k: -d[k]["additive"])
    return {"scenarios": d, "rank_product": rank_p, "rank_additive": rank_a,
            "unprimed_is_zero_under_product": d["trigger, unprimed"]["product"] == 0.0,
            "unprimed_nonzero_under_additive": d["trigger, unprimed"]["additive"] > 0}


# ------------------------------------------------------------ 6. TC-03

def freeze_thaw_profile(amp=9.0):
    ts = [-12, -8, -5, -3, -1, 0, 1, 3, 5, 8, 12]
    prof = [(t, TC.freeze_thaw_cycles(t, amp)) for t in ts]
    vals = [v for _, v in prof]
    peak_t = [t for t, v in prof if v == max(vals)]
    interior_peak = max(vals) > vals[0] and max(vals) > vals[-1]
    symmetric = all(TC.freeze_thaw_cycles(t, amp) == TC.freeze_thaw_cycles(-t, amp) for t in ts)
    return {"profile": prof, "peak_t": peak_t, "interior_peak": interior_peak, "symmetric_about_0": symmetric,
            "dip_at_0": TC.freeze_thaw_cycles(0, amp) < TC.freeze_thaw_cycles(-3, amp)}


def snow_half_implemented():
    """Does depth depend on temperature anywhere in the module? The
    docstring says warming thins the pack; the function takes depth as
    an input. Read from the AST: is `depth_m` ever assigned, or is any
    depth computed from a temperature argument?"""
    tree = ast.parse(_src())
    assigned = set()
    for n in ast.walk(tree):
        if isinstance(n, ast.Assign):
            for t in n.targets:
                if isinstance(t, ast.Name):
                    assigned.add(t.id)
    depth_names = [a for a in assigned if a in ("depth_m", "snow_depth_m", "depth")]
    return {"depth_assigned_anywhere": bool(depth_names), "depth_names_assigned": depth_names,
            "weak_layer_index_args": [a.arg for a in
                                      next(n for n in tree.body if isinstance(n, ast.FunctionDef)
                                           and n.name == "weak_layer_index").args.args]}


# ------------------------------------------------------------ 7. TC-06

def snow_sweep():
    """Sweep t_snow with the rest fixed at Demo D's BOTH scenario:
    total count, runout multiplier, coincidence."""
    rows = []
    for i in range(0, 15):
        tsnow = -14.0 + i * 1.0
        s = TC.chain_state(tsnow, tsnow - 1, tsnow + 3, 1.0, -1.0, 8.0, 55, 0.9, 60, 0.9, 1.0)
        rows.append({"t_snow": tsnow, "total": s["avalanche"]["total"],
                     "runout": s["avalanche"]["runout_multiplier"], "coinc": s["COINCIDENCE"]})
    falls_then_rises = any(rows[i]["total"] < rows[i - 1]["total"] for i in range(1, len(rows))) and \
        any(rows[i]["total"] > rows[i - 1]["total"] for i in range(1, len(rows)))
    count_down_coinc_up = any(rows[i]["total"] < rows[i - 1]["total"] and rows[i]["coinc"] > rows[i - 1]["coinc"]
                              for i in range(1, len(rows)))
    count_down_runout_up = any(rows[i]["total"] < rows[i - 1]["total"] and rows[i]["runout"] > rows[i - 1]["runout"]
                               for i in range(1, len(rows)))
    src = _src()
    coinc_expr = src[src.index("coincidence = "):src.index("return {", src.index("coincidence = "))]
    return {"rows": rows, "total_non_monotone": falls_then_rises,
            "any_step_with_count_down_and_coincidence_up": count_down_coinc_up,
            "any_step_with_count_down_and_runout_up": count_down_runout_up,
            "runout_in_coincidence_term": "runout" in coinc_expr,
            "runout_over_1_when_wet": all(r["runout"] >= 1.0 for r in rows)}


# ------------------------------------------------------- 8. referents

def referents():
    src = _src()
    folder = os.path.isdir(os.path.join(ROOT, "earth-systems-physics"))
    citing = 0
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in (".git", "__pycache__")]
        if os.path.abspath(dirpath).startswith(HERE):
            continue          # this folder quotes the name to check it; counted apart
        for fn in filenames:
            if fn.endswith((".md", ".py")) and os.path.join(dirpath, fn) not in (
                    os.path.join(ROOT, "CLAUDE.md"), os.path.join(ROOT, "README.md")):
                try:
                    with open(os.path.join(dirpath, fn), encoding="utf-8", errors="ignore") as fh:
                        if "rate-mismatch-polytope" in fh.read():
                            citing += 1
                except OSError:
                    pass
    body = src.split('"""', 2)[2]     # everything after the module docstring
    return {"earth_systems_physics_folder": folder,
            "module_cites_polytope": "rate-mismatch-polytope" in src,
            "rate_mismatch_polytope_files_citing": citing,
            "biskaborn_0_19_used_in_code": "0.19" in body,
            "polytope_exists": os.path.exists(os.path.join(ROOT, "rate-mismatch-polytope"))}


# ------------------------------------------------ 9. the extension

def extension():
    """airblast_extension.py against the module it says it extends, and
    against its own anchors."""
    import airblast_extension as AB
    src_core = _src()
    with open(os.path.join(HERE, "airblast_extension.py"), encoding="utf-8") as fh:
        src_ext = fh.read()
    body_ext = src_ext.split('"""', 2)[2]
    # F1..F3 as facts about the core module
    f1 = "t_snow_c" in src_core and "t_air" not in src_core
    f2 = "blast" not in src_core.lower()
    f3 = min(v[1] for v in TC.LAG.values()) == 1.0 / 365
    # coupling coefficient bounds the header states
    r = AB.PARTICLE_R
    lo, hi = (r["rock"] / r["snow"]) ** 1.5, (r["rock"] / r["snow"]) ** 2.0
    # meltwater calibration sentence: ratio 19 C over -1 C
    base = AB.meltwater_index(-1.0, 0.72, 0.20, 0.08)
    ratio = AB.meltwater_index(19.0, 0.72, 0.20, 0.08) / base
    # blast anchors
    p_full = AB.powder_cloud_pressure(57.0, 1.0)
    p_none = AB.powder_cloud_pressure(57.0, 0.0)
    # diurnal
    hours = list(range(24))
    temps = [AB.diurnal_air_temp(9.0, 8.0, h) for h in hours]
    # copy or import
    imports_core = "import thermal_coupling" in src_ext
    shared = [k for k in TC.LAG if k in AB.LAG]
    identical = all(TC.LAG[k] == AB.LAG[k] for k in shared)
    # TC-10 direction terms in code
    direction_in_code = any(w in body_ext.split("CLAIM_TABLE_ADD")[0].lower().replace('"""', "")
                            for w in ("lateral", "longitudinal"))
    return {
        "F1_core_uses_snow_temp_no_air": f1, "F2_core_has_no_blast": f2, "F3_core_fastest_is_snowpack": f3,
        "coupling_bounds": (lo, hi), "coupling_stated": (8.9, 18.4),
        "coupling_at_default_exponent": AB.thermal_coupling_coefficient(1, 0, 0),
        "melt_ratio_19_over_minus1": ratio, "melt_ratio_stated": 2.3,
        "blast_full_mean_kPa": p_full["mean_kPa"], "blast_full_anchor": ">15",
        "blast_none_mean_kPa": p_none["mean_kPa"], "blast_none_anchor": 2.5,
        "peak_over_mean": p_full["peak_kPa"] / p_full["mean_kPa"],
        "footprint_at_10kPa": AB.blast_footprint_km2(10.0),
        "diurnal_max_hour": hours[temps.index(max(temps))], "diurnal_min_hour": hours[temps.index(min(temps))],
        "diurnal_decades_faster": math.log10((1.0 / 365) / (1.0 / 8760)),
        "extension_imports_core": imports_core, "shared_lag_classes": len(shared), "shared_identical": identical,
        "tc10_direction_in_code": direction_in_code,
        "runout_multiplier_read_by_extension": "runout_multiplier" in src_ext,
    }


# ---------------------------------------------------------------- render

def _f(x, d=3):
    return "--" if x is None else (("%%.%df" % d) % x if isinstance(x, float) else str(x))


def render():
    out = []
    w = out.append
    w("coupling_audit -- thermal_coupling.py against its own claims")
    w("")
    c = calibration()
    w("1. CAL_FOS  '50 deg slope warmed from -4 C crosses FoS = 1 between -3 and -0.5; this value puts it at -2'")
    w("   crossing with fracture_favorable=True: %s C   with False: %s (FoS at -0.5 C = %s)" % (
        _f(c["favorable"], 2), _f(c["unfavorable"], 2), c["fos_50_at_-0.5_unfavorable"]))
    w("   the sentence holds under the flag it does not name, and not under the default.")
    w("")
    sh = strength_shape()
    w("2. TC-04  joint strength: slope at -9.5 C %s /K, at -1 C %s /K; sensitivity rises toward 0 C: %s" % (
        _f(sh["slope_cold"], 4), _f(sh["slope_warm"], 4), sh["sensitivity_rises_toward_0"]))
    w("   second difference of the loss across the domain: %s; the inline comment says 'convex: steeper near 0'" % sh["loss_second_difference"])
    w("   creep_sensitivity rises toward 0 C: %s; strength is clamped above -0.2 C (0 C reads as -0.2): %s" % (
        sh["creep_rises_toward_0"], sh["clamp_top"]))
    w("   TC-04 states its own criterion, sensitivity rising toward melting; the module's function")
    w("   has it falling by a factor of %.1f from -9.5 to -1 C. The claim is refuted by its own code." % (
        abs(sh["slope_cold"] / sh["slope_warm"])))
    w("")
    cc = constant_census()
    w("3. CONSTANTS  'CAL_FOS is the ONLY free parameter': CAL_FOS = %s; numeric literals inside function bodies: %d" % (
        cc["cal_fos"], cc["total_literals"]))
    for fn, v in cc["functions"].items():
        if v["literals"]:
            w("   %-28s %-40s docstring cites a source: %s" % (fn, str(v["literals"])[:40], v["docstring_cites"]))
    w("   functions carrying literals with no source in their docstring: %s" % cc["functions_with_uncited_literals"])
    w("")
    ls = lag_span()
    w("4. TC-01  %d lag classes spanning %.2f decades (claim: >=5, ~4)" % (ls["classes"], ls["decades"]))
    w("")
    pa = product_vs_additive()
    w("5. TC-02  Demo D under the product and under an additive mean of the same four factors")
    for k, v in pa["scenarios"].items():
        w("   %-20s product %s  additive %s" % (k, _f(v["product"], 4), _f(v["additive"], 4)))
    w("   rank by product %s; by additive %s" % (pa["rank_product"], pa["rank_additive"]))
    w("   the unprimed slope is 0 under the product and %s under the additive: the form is the claim," % (
        "non-zero" if pa["unprimed_nonzero_under_additive"] else "zero"))
    w("   shown in the module's own arithmetic; the falsifier is an event set, and none is here.")
    w("")
    ft = freeze_thaw_profile()
    w("6. TC-03  freeze-thaw cycles vs mean T: interior peak %s at %s; symmetric about 0: %s; dip at 0: %s" % (
        ft["interior_peak"], ft["peak_t"], ft["symmetric_about_0"], ft["dip_at_0"]))
    sn = snow_half_implemented()
    w("   snow half: depth assigned anywhere in the module: %s; weak_layer_index takes %s" % (
        sn["depth_assigned_anywhere"], sn["weak_layer_index_args"]))
    w("   'warming THINS the pack' is in the docstring and not in the code: depth is an input,")
    w("   so the elevation non-monotonicity TC-03 claims for snow is asserted, not produced.")
    w("")
    ss = snow_sweep()
    w("7. TC-06  sweep t_snow -14..0 at Demo D's BOTH: total non-monotone %s; runout >= 1 throughout %s" % (
        ss["total_non_monotone"], ss["runout_over_1_when_wet"]))
    w("   a step with count down and runout up: %s; with count down and COINCIDENCE up: %s" % (
        ss["any_step_with_count_down_and_runout_up"], ss["any_step_with_count_down_and_coincidence_up"]))
    w("   the runout multiplier enters the coincidence term: %s -- what TC-06 says rises is the" % ss["runout_in_coincidence_term"])
    w("   runout, which the module computes and no downstream term reads.")
    w("   t_snow | total | runout | coinc")
    for r in ss["rows"]:
        w("   %6.1f | %.3f | %.2f | %.4f" % (r["t_snow"], r["total"], r["runout"], r["coinc"]))
    w("")
    rf = referents()
    w("8. REFERENTS  folder earth-systems-physics exists: %s; this module cites rate-mismatch-polytope: %s;" % (
        rf["earth_systems_physics_folder"], rf["module_cites_polytope"]))
    w("   other files in the tree citing it (this folder excluded): %d; the polytope exists: %s" % (
        rf["rate_mismatch_polytope_files_citing"], rf["polytope_exists"]))
    w("   Biskaborn +0.19 C is in the header and used in no function: %s" % (not rf["biskaborn_0_19_used_in_code"]))
    w("")
    ex = extension()
    w("9. THE EXTENSION  airblast_extension.py against the core module and its own anchors")
    w("   F1 core drives on snowpack temperature with no air term: %s; F2 core has no blast term: %s; F3 core's fastest class is snowpack: %s" % (
        ex["F1_core_uses_snow_temp_no_air"], ex["F2_core_has_no_blast"], ex["F3_core_fastest_is_snowpack"]))
    w("   coupling snow/rock at r^-1.5 and r^-2.0: %.1f..%.1f (header states %s..%s); at the default exponent %.1f" % (
        ex["coupling_bounds"][0], ex["coupling_bounds"][1], ex["coupling_stated"][0], ex["coupling_stated"][1],
        ex["coupling_at_default_exponent"]))
    w("   meltwater ratio 19 C over -1 C from the function: %.2f; the docstring says calibrated to %.1f" % (
        ex["melt_ratio_19_over_minus1"], ex["melt_ratio_stated"]))
    w("   the index is linear in (t_air + 5), so the ratio is (19+5)/(-1+5) = 6 whatever the coupling; the")
    w("   calibration sentence is not produced by the function it sits on.")
    w("   blast at 57 m/s, full snow: mean %.1f kPa against anchor %s; no snow: %.1f against %.1f; peak/mean %.2f" % (
        ex["blast_full_mean_kPa"], ex["blast_full_anchor"], ex["blast_none_mean_kPa"], ex["blast_none_anchor"], ex["peak_over_mean"]))
    w("   footprint at 10 kPa: %.2f km2 (anchor 0.8); diurnal max at hour %d, min at hour %d; diurnal class %.2f decades below snowpack" % (
        ex["footprint_at_10kPa"], ex["diurnal_max_hour"], ex["diurnal_min_hour"], ex["diurnal_decades_faster"]))
    w("   the extension imports the core: %s; it re-declares LAG with %d shared classes, identical: %s -- a copy, not an import" % (
        ex["extension_imports_core"], ex["shared_lag_classes"], ex["shared_identical"]))
    w("   TC-10's lateral/longitudinal terms appear in any function: %s; the core's runout multiplier is read by the extension: %s" % (
        ex["tc10_direction_in_code"], ex["runout_multiplier_read_by_extension"]))
    w("")
    w("Nothing here is a statement about any slope or snowpack; the cited literature was not read.")
    return "\n".join(out) + "\n"


def main(argv):
    if "--selftest" in argv:
        sys.stderr.write("coupling_audit.py has no checks of its own; they live in selftest_tca.py.\n")
        return 2
    sys.stdout.write(render())
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
