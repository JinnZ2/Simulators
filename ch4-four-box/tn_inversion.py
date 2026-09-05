#!/usr/bin/env python3
"""tn_inversion.py -- R-3, folded into RESULTS.md.

Under the +SCA run (TS held at SCA, NH at GISP2, SH at WAIS), the
published TN emission of 88 Tg/yr requires a TN concentration ABOVE both
polar records -- the inversion runs on the published lifetime alone. A
+49 ppb concentration move (from the polar interpolation) shows up in the
emission column as only +6 Tg/yr, because the 6-yr lifetime scales loss
with concentration and the emission is downstream of that loss term: the
column compresses how far the unseen box has to move.

The forward model (`fourbox_forward.py`, delivered verbatim) is run with
stdout captured and its functions/constants used in place; nothing is
copied. NEEM and Law Dome are named in the delivered output spec but are
not among the model's constants (GISP2, WAIS, SCA are), and are not
supplied from memory -- egress is an allowlist. Runs its assertion on
plain invocation. Stdlib only, parses under Python 3.9.

    python3 tn_inversion.py
"""

import contextlib
import io
import os
import runpy
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
FWD = os.path.join(HERE, "fourbox_forward.py")

PUB_TN = 88.0     # published TN emission under +SCA, Tg/yr


def load(path):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        ns = runpy.run_path(path)
    return ns


def invert_tn(F):
    """Solve for C_TN (ppb) that yields E_TN = 88 Tg/yr under the +SCA
    run, rates reading, other three concentrations fixed at their
    +SCA values. Returns C_TN, the polar bracket, and sensitivities."""
    BOXES = F["BOXES"]
    TGP = F["TG_PER_PPB"]
    T = F["READINGS"]["as RATES (1/yr)"]
    M = F["build_M"](T)
    i = BOXES.index("TN")
    fixed = {"NH": F["GISP2_PI"], "TS": F["SCA_PI"], "SH": F["WAIS_PI"]}
    # E_TN = M[i][i]*C_TN + sum_{j!=TN} M[i][j]*C_j ; solve for C_TN.
    acc = sum(M[i][j] * (fixed[bj] * TGP) for j, bj in enumerate(BOXES) if bj != "TN")
    c_tn_tg = (PUB_TN - acc) / M[i][i]
    c_tn_ppb = c_tn_tg / TGP
    c_polar_tn = F["interp"](1 / 3)   # polar interpolation for TN
    return {
        "C_TN_ppb": c_tn_ppb,
        "GISP2": F["GISP2_PI"], "WAIS": F["WAIS_PI"], "SCA": F["SCA_PI"],
        "polar_bracket": (F["WAIS_PI"], F["GISP2_PI"]),
        "polar_interp_TN": c_polar_tn,
        "delta_C": c_tn_ppb - c_polar_tn,
        "delta_E": PUB_TN - F["PUB_POLAR"]["TN"],
        "dE_dC_local_Tg_per_ppb": M[i][i] * TGP,
    }


def render(r):
    lo, hi = r["polar_bracket"]
    pos = ("above both polar records" if r["C_TN_ppb"] > hi
           else "below both" if r["C_TN_ppb"] < lo
           else "inside the polar bracket")
    L = ["R-3  TN inversion under +SCA: solve C_TN for E_TN = %.0f Tg/yr" % PUB_TN,
         "C_TN required          %10.1f ppb   (%s)" % (r["C_TN_ppb"], pos),
         "polar bracket WAIS..GISP2 %7.0f .. %-7.0f ppb" % (lo, hi),
         "under SCA (%.0f) by       %10.1f ppb" % (r["SCA"], r["SCA"] - r["C_TN_ppb"]),
         "NEEM / Law Dome        not in the model's constants; not supplied from memory",
         "polar interp for TN    %10.1f ppb" % r["polar_interp_TN"],
         "move seen in table     dC = %+.1f ppb  ->  dE = %+.0f Tg/yr" % (r["delta_C"], r["delta_E"]),
         "  effective dE/dC      %10.4f Tg/ppb  (table)" % (r["delta_E"] / r["delta_C"]),
         "  local  dE/dC         %10.4f Tg/ppb  (M[TN][TN])" % r["dE_dC_local_Tg_per_ppb"]]
    return "\n".join(L)


def checks(r):
    lo, hi = r["polar_bracket"]
    fails = []
    if lo <= r["C_TN_ppb"] <= hi:
        fails.append("C_TN (%.1f) falls inside the polar bracket [%.0f, %.0f]"
                     % (r["C_TN_ppb"], lo, hi))
    return fails


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if "--selftest" in argv:
        print("tn_inversion asserts on plain invocation; no separate --selftest", file=sys.stderr)
        return 2
    F = load(FWD)
    r = invert_tn(F)
    print(render(r))
    fails = checks(r)
    for f in fails:
        print("ASSERT FAILED: " + f)
    print("tn_inversion: 1 assert, %d failed" % len(fails))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
