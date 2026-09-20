#!/usr/bin/env python3
# SPDX-License-Identifier: CC0-1.0
"""
wo4_lumber -- DIMENSIONAL SUBSTITUTION, the arithmetic (WO-4a).

The order's claim: nominal 4x4 against actual 3.5x3.5 is a structural
substitution, not a naming convention, and "bending stiffness scales with
the FOURTH POWER of depth; a 12.5% dimensional reduction removes ~40% of
stiffness". This module computes it and reports two things the order
folds into one.

  1. The VALUE holds and the MECHANISM is mislabelled. For a rectangle,
     bending stiffness goes as the second moment of area, I = b h^3 / 12:
     the CUBE of depth times the width. A 4x4 shrinks in both dimensions,
     so the ratio is (3.5/4)^3 x (3.5/4) = (3.5/4)^4 = 0.586, a 41.4%
     loss -- the order's ~40%. Shrink the depth alone and it is
     (3.5/4)^3 = 0.670, a 33% loss. The fourth power is the product of a
     cubic in depth and a linear in width, and the order's sentence
     attributes all of it to depth. Same number, different physics,
     and the difference is load-bearing the moment the section is not
     square: a 2x4 (1.5 x 3.5) keeps 0.502 of a full 2x4's stiffness.
  2. STIFFNESS and STRENGTH are two quantities. The order's arithmetic
     is about stiffness (deflection under load, I) and its test measures
     "load capacity to failure", which is strength (section modulus,
     S = b h^2 / 6, times the material's modulus of rupture). For the
     4x4 the strength ratio is (3.5/4)^3 = 0.670, not 0.586. The test as
     written would return the strength number and be read against the
     stiffness claim.

Nothing here is a measurement of any piece of wood. The confounds the
order names -- joinery, wood quality, seasoning -- are carried; moisture
content is the one "same species" does not hold, since rough-cut stock is
ordinarily green and dimensional stock is dried and surfaced.

`stiffness_ratio` is registered in tools/known_answer.py.

Python 3.9, ASCII only, stdlib only. Refuses --selftest.
"""

from __future__ import annotations

import sys

from common import refuse_selftest

# nominal -> actual (inches). The 4x4 pair is the order's; the others are
# the US softwood dimension standard, CARRIED from memory, unverified.
SIZES = {
    "2x4": ((2.0, 4.0), (1.5, 3.5)),
    "2x6": ((2.0, 6.0), (1.5, 5.5)),
    "2x8": ((2.0, 8.0), (1.5, 7.25)),
    "2x10": ((2.0, 10.0), (1.5, 9.25)),
    "2x12": ((2.0, 12.0), (1.5, 11.25)),
    "4x4": ((4.0, 4.0), (3.5, 3.5)),
    "6x6": ((6.0, 6.0), (5.5, 5.5)),
}
CHOICES = {
    1: "the strong axis is the larger dimension (h); loaded on edge",
    2: "material terms (E, modulus of rupture) are held equal across the "
       "pair; the ratios are geometric only",
}


def second_moment(b, h):
    """I = b h^3 / 12 for a rectangle, strong axis. None on a non-positive
    dimension."""
    if b is None or h is None or b <= 0 or h <= 0:
        return None
    return b * h ** 3 / 12.0


def section_modulus(b, h):
    """S = b h^2 / 6. None on a non-positive dimension."""
    if b is None or h is None or b <= 0 or h <= 0:
        return None
    return b * h ** 2 / 6.0


def stiffness_ratio(nominal_b, nominal_h, actual_b, actual_h):
    """I_actual / I_nominal, the stiffness the substitution keeps. None on
    a non-positive dimension, never 0 or 1 by default."""
    i_n = second_moment(nominal_b, nominal_h)
    i_a = second_moment(actual_b, actual_h)
    if i_n is None or i_a is None:
        return None
    return i_a / i_n


def strength_ratio(nominal_b, nominal_h, actual_b, actual_h):
    """S_actual / S_nominal, the strength the substitution keeps."""
    s_n = section_modulus(nominal_b, nominal_h)
    s_a = section_modulus(actual_b, actual_h)
    if s_n is None or s_a is None:
        return None
    return s_a / s_n


def depth_only_ratio(nominal_h, actual_h):
    """(h_a / h_n)^3 -- what 'scales with depth' gives if the width is
    held at nominal. The order's fourth power is this times the width
    ratio."""
    if nominal_h is None or actual_h is None or nominal_h <= 0 or actual_h <= 0:
        return None
    return (actual_h / nominal_h) ** 3


def table():
    rows = []
    for name, ((nb, nh), (ab, ah)) in sorted(SIZES.items()):
        b, h = (min(nb, nh), max(nb, nh))
        b2, h2 = (min(ab, ah), max(ab, ah))
        rows.append({"nominal": name, "actual": "%gx%g" % (ab, ah),
                     "stiffness_kept": stiffness_ratio(b, h, b2, h2),
                     "strength_kept": strength_ratio(b, h, b2, h2),
                     "depth_only_kept": depth_only_ratio(h, h2),
                     "linear_reduction": 1.0 - h2 / h})
    return rows


def quantity_mismatch():
    """The arithmetic names stiffness; the test measures strength. On the
    4x4 the two ratios differ, and the readout says by how much."""
    st = stiffness_ratio(4.0, 4.0, 3.5, 3.5)
    sr = strength_ratio(4.0, 4.0, 3.5, 3.5)
    return {"arithmetic_quantity": "stiffness (I)",
            "test_quantity": "strength (S x MOR)",
            "same_quantity": False,
            "stiffness_kept_4x4": st, "strength_kept_4x4": sr,
            "reads": "a to-failure test returns the strength ratio %.3f "
                     "and would be read against the stiffness claim %.3f"
                     % (sr, st)}


def render():
    out = ["WO-4a  LUMBER: DIMENSIONAL SUBSTITUTION, THE ARITHMETIC "
           "(nothing measured)", "-" * 72,
           "  %-8s %-10s %10s %10s %10s %10s"
           % ("nominal", "actual", "lin. red.", "stiff kept", "str kept",
              "depth-only")]
    for r in table():
        out.append("  %-8s %-10s %10.3f %10.3f %10.3f %10.3f"
                   % (r["nominal"], r["actual"], r["linear_reduction"],
                      r["stiffness_kept"], r["strength_kept"],
                      r["depth_only_kept"]))
    q = quantity_mismatch()
    out.append("")
    out.append("  4x4: the order's ~40%% holds (%.1f%% of stiffness removed) "
               "and its mechanism does not: I = b h^3/12 is cubic in depth, "
               "linear in width; the fourth power is both shrinking"
               % (100 * (1 - q["stiffness_kept_4x4"])))
    out.append("  " + q["reads"])
    out.append("  2x4: %.3f of a full 2x4's stiffness kept -- half"
               % stiffness_ratio(2.0, 4.0, 1.5, 3.5))
    out.append("  confounds carried from the order: joinery, wood quality, "
               "seasoning; moisture is the one 'same species' does not hold")
    for k in sorted(CHOICES):
        out.append("  [CHOICE %d] %s" % (k, CHOICES[k]))
    return "\n".join(out) + "\n"


def main(argv):
    if "--selftest" in argv:
        return refuse_selftest("wo4_lumber.py")
    sys.stdout.write(render())
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
