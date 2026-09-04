#!/usr/bin/env python3
"""Checks for fourbox_audit.py against the two delivered scripts, which
are run with stdout captured and never edited. Nothing here is a
statement about the atmosphere.

    python3 ch4-four-box/selftest_fb.py
"""

import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "sheet-structure-scan"))
import fourbox_audit as A  # noqa: E402
import no_severity  # noqa: E402

FAILS = []
N = [0]


def check(name, cond):
    N[0] += 1
    if not cond:
        FAILS.append(name)
        print("  FAIL  " + name)


def main():
    print("selftest_fb")
    F, out_f = A.load(A.FWD)
    C, out_c = A.load(A.CLO)
    check("both delivered scripts run and print", "TRANSPORT PARAMETER" in out_f and "CLOSURE GAP" in out_c)

    idn = A.identities(F)
    check("IPD 48, both SCA offsets, TS split and A published hold",
          idn["IPD"] == 48 and idn["SCA_is_GISP2_plus_46"] and idn["SCA_is_WAIS_plus_94"]
          and idn["TS_is_213_minus_88"] and abs(idn["A_published"] - 0.765) < 1e-3)
    check("Tg per ppb per box is a quarter of the global 2.848", idn["box_is_quarter_of_global"]
          and abs(idn["tg_per_ppb_global"] - 2.848) < 1e-9)

    pr = A.polar_residuals(F)
    check("rates reading max residual 4.2, times reading 47.7 with a negative SH source",
          abs(pr["as RATES (1/yr)"]["max_abs"] - 4.2) < 0.1 and abs(pr["as TIMES (yr)"]["max_abs"] - 47.7) < 0.1
          and pr["as TIMES (yr)"]["negative_source"] == ["SH"] and pr["as RATES (1/yr)"]["negative_source"] == [])
    # known answer on the forward operator: a uniform concentration with no transport gives E = C / lifetime
    T0 = {}
    E0 = F["E_of"]({b: 700.0 for b in F["BOXES"]}, T0)
    check("with no transport, E_b = C_b / lifetime_b exactly",
          all(abs(E0[b] - 700.0 * F["TG_PER_PPB"] / F["LIFETIME"][b]) < 1e-9 for b in F["BOXES"]))
    E1 = F["E_of"]({b: 700.0 for b in F["BOXES"]}, F["READINGS"]["as RATES (1/yr)"])
    check("with transport, a uniform concentration moves nothing between boxes",
          all(abs(E1[b] - E0[b]) < 1e-9 for b in F["BOXES"]))

    ma = A.matrices_agree(F, C)
    check("the two scripts' matrices agree to 1e-12", ma["agree"])

    sr = A.sca_run(F, C)
    check("+SCA southern source is -10.8 against a published 10", abs(sr["E_SH_with_TS_at_SCA"] + 10.8) < 0.1)
    check("closure diagnostic: C_TN 733.0, C_SH 711.3, gap 59.3",
          abs(sr["tn_needed"] - 733.0) < 0.1 and abs(sr["sh_needed"] - 711.3) < 0.1 and abs(sr["closure_gap_ppb"] - 59.3) < 0.1)
    check("attenuation 0.774 vs published 0.765", abs(sr["A_mine"] - 0.774) < 1e-3)

    cs = A.consistency(F)
    check("implied gradient 12.5 at scale 1; 48 reached at scale 4.34",
          abs(cs["gradient_at_scale_1"] - 12.5) < 0.1 and abs(cs["scale_at_48"] - 4.34) < 0.01)
    check("rates reading is the times base x 20.66 and yields 150.5 ppb",
          abs(cs["rates_reading_scale"] - 20.66) < 0.01 and abs(cs["gradient_under_rates_reading"] - 150.5) < 0.1)
    check("implied gradient is monotone in the scale on the scanned range",
          all(A.implied_gradient(F, s) < A.implied_gradient(F, s * 2) for s in (1, 2, 5, 10, 20, 50)))
    check("bisection recovers a planted target", abs(A.implied_gradient(F, A.scale_for_observed(F, 24.1)) - 24.1) < 0.01)

    rc = subprocess.run([sys.executable, os.path.join(HERE, "fourbox_audit.py"), "--selftest"], capture_output=True).returncode
    check("fourbox_audit refuses --selftest with rc 2", rc == 2)
    out = A.render()
    check("render screens clean", not no_severity.hits(out))
    check("screen fires on a planted word", bool(no_severity.hits(out + "\nthis is wrong\n")))
    with open(os.path.join(HERE, "samples", "fourbox_audit.sample.txt"), "w", encoding="utf-8") as fh:
        fh.write(out)
    print("selftest: %d checks, %d failed" % (N[0], len(FAILS)))
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
