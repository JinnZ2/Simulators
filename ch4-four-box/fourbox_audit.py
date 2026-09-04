#!/usr/bin/env python3
"""fourbox_audit -- the two delivered CH4 box scripts read against each
other and against their own arithmetic.

`fourbox_forward.py` rebuilds a four-box CH4 model forward-only (E = M·C
with prescribed concentrations) and prints the published emissions
beside two readings of the transport parameters -- as exchange TIMES
and as exchange RATES -- plus a consistency scan. `closure_diagnostic.py`
takes the rates reading and asks what tropical and southern
concentrations reproduce the published +SCA emissions. Both are landed
verbatim and print at import, so this module runs each with stdout
captured and calls their functions in place; nothing is copied.

Computed here:
  1. the constants' identities (IPD, the SCA offsets, the TS split, the
     published attenuation, Tg per ppb per box against the global value);
  2. which reading reproduces the published polar-only emissions, as the
     largest absolute residual per box under each;
  3. the two scripts' transport matrices agree under the rates reading;
  4. the +SCA run's southern box under the rates reading (a negative
     source), and the closure gap the diagnostic reports;
  5. the consistency scan: the time scale at which the implied NH-SH
     gradient equals the observed 48 ppb, by bisection, and the gradient
     implied under the reading that reproduces the published emissions.

Every published figure is carried from the scripts and unchecked
(allowlist egress). Nothing here is a statement about the atmosphere.

CC0. stdlib only. Parses under Python 3.9.
"""

import contextlib
import io
import os
import runpy
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
FWD = os.path.join(HERE, "fourbox_forward.py")
CLO = os.path.join(HERE, "closure_diagnostic.py")


def load(path):
    """Run a delivered script with its prints captured; return its
    namespace and its printed output."""
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        ns = runpy.run_path(path)
    return ns, buf.getvalue()


# ----------------------------------------------------------- 1. identities

def identities(F):
    global_tg_per_ppb = F["MOLES_AIR_TOTAL"] * 1e-9 * F["MOLAR_MASS_CH4"] / 1e12
    return {
        "IPD": F["GISP2_PI"] - F["WAIS_PI"],
        "SCA_is_GISP2_plus_46": F["SCA_PI"] == F["GISP2_PI"] + 46,
        "SCA_is_WAIS_plus_94": F["SCA_PI"] == F["WAIS_PI"] + 94,
        "TS_is_213_minus_88": F["PUB_SCA"]["TS"] == 213 - 88,
        "A_published": 163 / 213,
        "tg_per_ppb_box": F["TG_PER_PPB"],
        "tg_per_ppb_global": global_tg_per_ppb,
        "box_is_quarter_of_global": abs(F["TG_PER_PPB"] * 4 - global_tg_per_ppb) < 1e-12,
    }


# ------------------------------------------------- 2. which reading fits

def polar_residuals(F):
    polar = {"NH": F["GISP2_PI"], "TN": F["interp"](1 / 3), "TS": F["interp"](2 / 3), "SH": F["WAIS_PI"]}
    out = {}
    for label, T in F["READINGS"].items():
        E = F["E_of"](polar, T)
        res = {b: E[b] - F["PUB_POLAR"][b] for b in F["BOXES"]}
        out[label] = {"E": E, "residuals": res, "max_abs": max(abs(v) for v in res.values()),
                      "negative_source": [b for b, v in E.items() if v < 0]}
    return out


# -------------------------------------------- 3. the two matrices agree

def matrices_agree(F, C):
    m1 = F["build_M"](F["READINGS"]["as RATES (1/yr)"])
    m2 = C["M"]()
    diff = max(abs(m1[i][j] - m2[i][j]) for i in range(4) for j in range(4))
    return {"max_abs_diff": diff, "agree": diff < 1e-12}


# ------------------------------------------------ 4. the +SCA southern box

def sca_run(F, C):
    T = F["READINGS"]["as RATES (1/yr)"]
    withsca = {"NH": F["GISP2_PI"], "TN": F["interp"](1 / 3), "TS": F["SCA_PI"], "SH": F["WAIS_PI"]}
    E = F["E_of"](withsca, T)
    return {"E_SH_with_TS_at_SCA": E["SH"], "published_SH": 10.0,
            "tn_needed": C["tn_needed"], "sh_needed": C["sh_needed"],
            "closure_gap_ppb": C["sh_needed"] - C["WAIS"],
            "A_mine": C["tp"] / (C["e"]["TN"] + C["e"]["TS"]), "A_published": 163 / 213}


# ------------------------------------------------- 5. consistency scan

def implied_gradient(F, scale):
    T_pairs = {k: v * scale for k, v in F["base"].items()}
    M = F["build_M"](T_pairs)
    Cc = F["solve4"](M, [F["PUB_POLAR"][b] for b in F["BOXES"]])
    ppb = [c / F["TG_PER_PPB"] for c in Cc]
    return ppb[0] - ppb[3]


def scale_for_observed(F, target=48.0, lo=1.0, hi=10.0):
    for _ in range(100):
        mid = (lo + hi) / 2
        if implied_gradient(F, mid) < target:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def consistency(F):
    rates_as_times_scale = (1 / 0.22) / 0.22    # the rates reading, expressed as a multiple of the times base
    return {"scale_at_48": scale_for_observed(F),
            "gradient_at_scale_1": implied_gradient(F, 1.0),
            "rates_reading_scale": rates_as_times_scale,
            "gradient_under_rates_reading": implied_gradient(F, rates_as_times_scale),
            "observed": 48.0}


# ---------------------------------------------------------------- render

def render():
    F, out_f = load(FWD)
    C, out_c = load(CLO)
    o = []
    w = o.append
    w("fourbox_audit -- the two delivered scripts against each other and their own arithmetic")
    w("")
    idn = identities(F)
    w("1. IDENTITIES  IPD %.0f; SCA = GISP2+46 %s = WAIS+94 %s; TS = 213-88 %s; A published %.3f" % (
        idn["IPD"], idn["SCA_is_GISP2_plus_46"], idn["SCA_is_WAIS_plus_94"], idn["TS_is_213_minus_88"], idn["A_published"]))
    w("   Tg per ppb: %.4f per box, %.4f global; box is a quarter of global: %s" % (
        idn["tg_per_ppb_box"], idn["tg_per_ppb_global"], idn["box_is_quarter_of_global"]))
    w("")
    pr = polar_residuals(F)
    w("2. WHICH READING  polar-only emissions against the published, per reading")
    for label, r in pr.items():
        w("   %-16s max |residual| %5.1f Tg/yr; negative sources: %s" % (label, r["max_abs"], r["negative_source"] or "none"))
    best = min(pr, key=lambda k: pr[k]["max_abs"])
    w("   the reading that reproduces the published polar run: %s" % best)
    w("")
    ma = matrices_agree(F, C)
    w("3. MATRICES  forward script (rates reading) vs closure script: max |diff| %.2e, agree %s" % (ma["max_abs_diff"], ma["agree"]))
    w("")
    sr = sca_run(F, C)
    w("4. +SCA RUN  with TS prescribed at SCA and SH at WAIS, E_SH = %.1f Tg/yr against a published %.0f" % (
        sr["E_SH_with_TS_at_SCA"], sr["published_SH"]))
    w("   the diagnostic's C_TN for E_TN = 88: %.1f ppb; C_SH for E_SH = 10: %.1f ppb; closure gap %.1f ppb above WAIS" % (
        sr["tn_needed"], sr["sh_needed"], sr["closure_gap_ppb"]))
    w("   attenuation A: %.3f from the diagnostic against %.3f published" % (sr["A_mine"], sr["A_published"]))
    w("   a prescribed southern concentration and a prescribed southern source cannot both hold in a")
    w("   forward model; the gap is the size of the disagreement in ppb.")
    w("")
    cs = consistency(F)
    w("5. CONSISTENCY  implied NH-SH gradient at published emissions: %.1f ppb at scale 1; observed %.0f" % (
        cs["gradient_at_scale_1"], cs["observed"]))
    w("   the scale at which the gradient equals 48: %.2f (times base x %.2f)" % (cs["scale_at_48"], cs["scale_at_48"]))
    w("   the rates reading is the times base x %.2f, and there the implied gradient is %.1f ppb" % (
        cs["rates_reading_scale"], cs["gradient_under_rates_reading"]))
    w("   so the reading that reproduces the published emissions yields a polar gradient about")
    w("   %.1fx the observed one; the scan and the emissions fit do not pick the same transport." % (
        cs["gradient_under_rates_reading"] / cs["observed"]))
    w("")
    w("Every published figure is carried from the scripts; nothing here is a statement about the atmosphere.")
    return "\n".join(o) + "\n"


def main(argv):
    if "--selftest" in argv:
        sys.stderr.write("fourbox_audit.py has no checks of its own; they live in selftest_fb.py.\n")
        return 2
    sys.stdout.write(render())
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
