#!/usr/bin/env python3
# SPDX-License-Identifier: CC0-1.0
"""
wo2_band_sweep -- SWEEP THE OPERATING BAND INSTEAD OF SCORING A POINT.

Engagement has a FLOOR (minimum stimulation before the task registers)
and a CEILING (saturation, shutdown), two parameters that move
independently. A single-point instrument reads one level nobody chose for
the subject, so no-response-below-floor and shutdown-at-ceiling return
the same score, and both read as deficit.

This module sweeps a constructed stimulation level against task
performance and returns a CURVE per subject with floor, ceiling, width,
and where a standard test point falls relative to each -- NOT a score.
Its demonstration is the fault the order states: three constructed
subjects (band shifted low, band shifted high, flat) return the SAME
single-point score at the standard level and separate under the sweep.

Absences are kept apart: a curve that never registers is NOT_REGISTERED,
one that never turns down inside the swept range has ceiling NOT_REACHED
(not "no ceiling"), fewer than three levels is NOT_ESTIMABLE, and a
standard point outside a located band is placed on the side it falls.

Nothing here is a measurement of any person; every curve is CONSTRUCTED
and marked PROPOSED.

Python 3.9, ASCII only, stdlib only. Refuses --selftest.
"""

from __future__ import annotations

import sys

from common import Refused, refuse_selftest

REGISTER = 0.5     # [CHOICE 1]
MIN_LEVELS = 3     # [CHOICE 2]
CHOICES = {
    1: "a task REGISTERS at a level when performance >= %.2f; the "
       "threshold is stipulated and printed, not derived" % REGISTER,
    2: "floor and ceiling need at least %d swept levels; below that the "
       "curve is NOT_ESTIMABLE" % MIN_LEVELS,
    3: "the ceiling is the first level AFTER the peak at which performance "
       "drops back below the register threshold; a curve still registering "
       "at the top of the sweep has ceiling NOT_REACHED",
}
POSITIONS = ("BELOW_FLOOR", "IN_BAND", "ABOVE_CEILING", "NOT_LOCATABLE",
             "NOT_SWEPT")


def read_curve(subject, points, status="PROPOSED"):
    """points: list of (level, performance), performance in [0, 1]."""
    if not points:
        raise Refused("curve %s: no points" % subject)
    seen = set()
    for lv, pf in points:
        if isinstance(lv, bool) or not isinstance(lv, (int, float)):
            raise Refused("curve %s: level %r" % (subject, lv))
        if isinstance(pf, bool) or not isinstance(pf, (int, float)) \
                or not 0 <= pf <= 1:
            raise Refused("curve %s: performance %r not in [0, 1]"
                          % (subject, pf))
        if lv in seen:
            raise Refused("curve %s: level %r swept twice" % (subject, lv))
        seen.add(lv)
    if status not in ("OBSERVED", "DERIVED", "PROPOSED"):
        raise Refused("curve %s: status %r" % (subject, status))
    return {"subject": subject, "points": sorted(points), "status": status}


def band(curve):
    """Floor, ceiling, width from a sorted curve."""
    pts = curve["points"]
    if len(pts) < MIN_LEVELS:
        return {"subject": curve["subject"], "state": "NOT_ESTIMABLE",
                "floor": None, "ceiling": None, "width": None,
                "n_levels": len(pts)}
    registering = [lv for lv, pf in pts if pf >= REGISTER]
    if not registering:
        return {"subject": curve["subject"], "state": "NOT_REGISTERED",
                "floor": None, "ceiling": None, "width": None,
                "n_levels": len(pts)}
    floor = registering[0]
    peak_i = max(range(len(pts)), key=lambda i: (pts[i][1], -i))
    ceiling = None
    for lv, pf in pts[peak_i + 1:]:
        if pf < REGISTER:
            ceiling = lv
            break
    if ceiling is None:
        return {"subject": curve["subject"], "state": "CEILING_NOT_REACHED",
                "floor": floor, "ceiling": None, "width": None,
                "n_levels": len(pts)}
    return {"subject": curve["subject"], "state": "BAND_LOCATED",
            "floor": floor, "ceiling": ceiling, "width": ceiling - floor,
            "n_levels": len(pts)}


def single_point(curve, level):
    """What a one-point instrument returns: the performance at the standard
    level, or NOT_SWEPT if that level is not on the curve (no
    interpolation -- a point nobody measured is not a reading)."""
    for lv, pf in curve["points"]:
        if lv == level:
            return pf
    return "NOT_SWEPT"


def position(b, level):
    """Where the standard test point falls relative to the band."""
    if b["floor"] is None:
        return "NOT_LOCATABLE"
    if level < b["floor"]:
        return "BELOW_FLOOR"
    if b["ceiling"] is not None and level >= b["ceiling"]:
        return "ABOVE_CEILING"
    return "IN_BAND"


def report(curve, standard_level):
    b = band(curve)
    return {"subject": curve["subject"], "band": b,
            "single_point": single_point(curve, standard_level),
            "position": position(b, standard_level),
            "standard_level": standard_level}


# --- constructed demo, PROPOSED ---------------------------------------------

LEVELS = list(range(0, 11))
STANDARD = 5


def _step(lo, hi, inside=0.9, outside=0.1):
    return [(lv, inside if lo <= lv <= hi else outside) for lv in LEVELS]


DEMO = [
    read_curve("band-low", _step(1, 4)),
    read_curve("band-high", _step(6, 9)),
    read_curve("flat-low", [(lv, 0.1) for lv in LEVELS]),
    read_curve("band-open", _step(2, 10)),
]


def render(curves=None, standard=STANDARD):
    cs = DEMO if curves is None else curves
    out = ["WO-2  BAND SWEEP   (curves CONSTRUCTED, PROPOSED)   standard "
           "test point %s" % standard, "-" * 72,
           "  %-10s %-20s %6s %8s %6s %10s %s"
           % ("subject", "state", "floor", "ceiling", "width",
              "point-read", "standard point sits")]
    for c in cs:
        r = report(c, standard)
        b = r["band"]
        f = lambda v: "--" if v is None else str(v)
        out.append("  %-10s %-20s %6s %8s %6s %10s %s"
                   % (c["subject"], b["state"], f(b["floor"]),
                      f(b["ceiling"]), f(b["width"]),
                      r["single_point"] if isinstance(r["single_point"], str)
                      else "%.2f" % r["single_point"], r["position"]))
    reads = {c["subject"]: report(c, standard)["single_point"] for c in cs}
    same = len(set(str(v) for v in reads.values() if v != "NOT_SWEPT"))
    out.append("")
    out.append("  distinct single-point reads across the set: %d   "
               "distinct band states: %d"
               % (same, len(set(band(c)["state"] for c in cs))))
    out.append("  a curve, not a score; the point-read column is what a "
               "fixed-level instrument returns")
    for k in sorted(CHOICES):
        out.append("  [CHOICE %d] %s" % (k, CHOICES[k]))
    return "\n".join(out) + "\n"


def main(argv):
    if "--selftest" in argv:
        return refuse_selftest("wo2_band_sweep.py")
    sys.stdout.write(render())
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
