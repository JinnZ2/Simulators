#!/usr/bin/env python3
"""units_test.py -- R-2, folded into RESULTS.md.

The published Methods label the transport parameters "exchange rates of
0.22/0.45/0.45 years". Read as TIMES (yr) the four-box steady state
under-produces the tropics and sends the southern source NEGATIVE; read
as RATES (1/yr) the polar-only baseline reproduces (tropics ~163). A
negative source is a sign error, not a calibration difference, so the
unit word is settled from the published values alone -- no archive code.

The forward model (`fourbox_forward.py`, delivered verbatim, prints at
import) is run with stdout captured and its functions called in place;
nothing is copied. Runs its assertions on plain invocation. Stdlib only,
parses under Python 3.9.

    python3 units_test.py
"""

import contextlib
import io
import os
import runpy
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
FWD = os.path.join(HERE, "fourbox_forward.py")


def load(path):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        ns = runpy.run_path(path)
    return ns


def readings_table(F):
    """For each reading of 0.22/0.45/0.45, the polar-only steady state:
    tropics (TN+TS) and SH, and whether tropics reproduces 163."""
    rows = []
    polar = {"NH": F["GISP2_PI"], "TN": F["interp"](1 / 3),
             "TS": F["interp"](2 / 3), "SH": F["WAIS_PI"]}
    for label, T in F["READINGS"].items():
        E = F["E_of"](polar, T)
        tropics = E["TN"] + E["TS"]
        rows.append({"reading": label, "tropics": tropics, "SH": E["SH"],
                     "reproduces_163": abs(tropics - 163.0) < 0.5})
    return rows


def render(rows):
    L = ["R-2  units label: TIMES vs RATES, polar-only steady state",
         "%-18s %12s %10s %14s" % ("reading", "tropics Tg/yr", "SH Tg/yr", "reproduces 163?")]
    for r in rows:
        L.append("%-18s %12.2f %10.2f %14s"
                 % (r["reading"], r["tropics"], r["SH"], "yes" if r["reproduces_163"] else "no"))
    return "\n".join(L)


def checks(rows):
    times = next(r for r in rows if "TIMES" in r["reading"])
    rates = next(r for r in rows if "RATES" in r["reading"])
    fails = []
    if not (times["SH"] < 0):
        fails.append("times-reading SH is not negative (%.2f)" % times["SH"])
    if not (abs(rates["tropics"] - 163.0) < 0.5):
        fails.append("rate-reading tropics not within 0.5 of 163 (%.2f)" % rates["tropics"])
    return fails


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if "--selftest" in argv:
        print("units_test asserts on plain invocation; no separate --selftest", file=sys.stderr)
        return 2
    F = load(FWD)
    rows = readings_table(F)
    print(render(rows))
    fails = checks(rows)
    for f in fails:
        print("ASSERT FAILED: " + f)
    print("units_test: 2 asserts, %d failed" % len(fails))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
