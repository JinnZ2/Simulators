#!/usr/bin/env python3
"""Internal-consistency checks on WORK_ORDER.md's source material.

WHAT A PASS MEANS HERE

  Every input below is a number quoted from the delivered work order.
  A check passing means the delivered block COHERES -- its own numbers
  agree with each other at the stated rounding. It does not mean any
  number is true: nothing in this folder reached a primary source,
  because the egress gate refuses every publisher the order names
  (measured, with timestamps, in SOURCES.md).

  So this is the ARITHMETIC row of SOURCES.md's status vocabulary,
  runnable. The CARRIED rows have no check and get none.

USAGE
  python3 seam-gaps/verify_sources.py             print the checks
  python3 seam-gaps/verify_sources.py --selftest  assert them

Stdlib only. Parses under 3.9. CC0.
"""

import sys

# ---- quoted from WORK_ORDER.md, BIOMASS CENSUS block (all carried) ----
LIVESTOCK = 0.10   # Gt C
HUMANS = 0.06
WILD = 0.007
MAMMAL_TOTAL_STATED = 0.17
SHARES_STATED = (60, 36, 4)          # percent, as delivered
PREHUMAN_TOTAL = 0.04                # "0.04 -> 0.17"
ANIMAL_COMPONENTS = (1.0, 0.7, 0.2, 0.2, 0.17, 0.002)
ANIMAL_TOTAL_STATED = 2.0            # "~2"

# ---- quoted from the INSECT DECLINE block ----
FLOOR_YEARS = 15                     # minimum to detect a true trend
RADAR_WINDOW_YEARS = 10

# ---- quoted from the CORAL / ENSO block ----
ENSO_RISE_POINTS = 36                # percent above preindustrial
ENSO_RECENT_POINTS = 16              # of that, in the last ~40 years
ENSO_RECENT_YEARS = 40
CORAL_RECORD_YEARS = 900


def partition_closes():
    """livestock + humans + wild rounds to the stated mammal total."""
    s = LIVESTOCK + HUMANS + WILD
    return s, round(s, 2) == MAMMAL_TOTAL_STATED


def shares_close():
    """the delivered 60 / 36 / 4 percent are the components' own shares."""
    s = LIVESTOCK + HUMANS + WILD
    got = tuple(round(100.0 * x / s) for x in (LIVESTOCK, HUMANS, WILD))
    return got, all(abs(a - b) <= 1 for a, b in zip(got, SHARES_STATED))


def total_x4():
    """0.04 -> 0.17 is 'x 4' at one significant figure."""
    r = MAMMAL_TOTAL_STATED / PREHUMAN_TOTAL
    return r, round(r) == 4


def wild_div6():
    """wild / 6 needs one identity the block leaves implicit: the
    pre-human TOTAL is the pre-human WILD, since livestock and human
    biomass were then ~0. On that identity, 0.04 / 0.007 rounds to 6."""
    r = PREHUMAN_TOTAL / WILD
    return r, round(r) == 6


def animal_sum():
    """the delivered animal components against the delivered '~2':
    they sum PAST the stated total. Consistent at one significant
    figure and only there; recorded, not adjudicated -- the block's
    own components exceed the block's own total by the overshoot."""
    s = sum(ANIMAL_COMPONENTS)
    overshoot = s - ANIMAL_TOTAL_STATED
    return (s, overshoot), round(s) == round(ANIMAL_TOTAL_STATED)


def radar_null_silent():
    """conditional on the two carried numbers: a 10-yr window under a
    15-yr floor cannot distinguish no-decline from cannot-see-decline,
    so the null is SILENT in META-PROTOCOL section 4B's sense. This
    derivation is arithmetic; both inputs stay carried."""
    return (RADAR_WINDOW_YEARS, FLOOR_YEARS), RADAR_WINDOW_YEARS < FLOOR_YEARS


def enso_concentration():
    """the block's implied concentration, computed and reported with
    no verdict: 16 of 36 points is 44% of the stated change, and 40 of
    ~900 years is 4% of the record length. The ratio of shares is what
    'acceleration' quantifies to on the delivered numbers alone."""
    change_share = ENSO_RECENT_POINTS / ENSO_RISE_POINTS
    record_share = ENSO_RECENT_YEARS / CORAL_RECORD_YEARS
    return (change_share, record_share), change_share > record_share


CHECKS = [
    ("mammal partition closes to the stated 0.17", partition_closes),
    ("shares reproduce 60 / 36 / 4", shares_close),
    ("total x4 at one significant figure", total_x4),
    ("wild /6 on the stated implicit identity", wild_div6),
    ("animal components vs '~2' (overshoot reported)", animal_sum),
    ("10-yr radar window under the 15-yr floor -> SILENT",
     radar_null_silent),
    ("ENSO change-share vs record-share (reported, no verdict)",
     enso_concentration),
]


def report():
    print("verify_sources -- arithmetic over WORK_ORDER.md's own numbers")
    print("a pass means the block coheres, not that it is true\n")
    for name, fn in CHECKS:
        val, ok = fn()
        print("  %-52s %s   %s" % (name, "holds" if ok else "DOES NOT HOLD",
                                   repr(val)))
    print("\nevery input is CARRIED; see SOURCES.md")


def selftest():
    ok = fail = 0

    def check(name, cond):
        nonlocal ok, fail
        if cond:
            ok += 1
        else:
            fail += 1
            print("  FAIL  %s" % name)

    v, c = partition_closes()
    check("partition sums to 0.167", abs(v - 0.167) < 1e-12 and c)
    v, c = shares_close()
    check("shares are 60/36/4", v == (60, 36, 4) and c)
    v, c = total_x4()
    check("ratio is 4.25", abs(v - 4.25) < 1e-12 and c)
    v, c = wild_div6()
    check("ratio is ~5.71", abs(v - 0.04 / 0.007) < 1e-12 and c)
    (s, over), c = animal_sum()
    check("components sum to 2.272", abs(s - 2.272) < 1e-9 and c)
    check("overshoot is reported, not hidden", abs(over - 0.272) < 1e-9)
    _, c = radar_null_silent()
    check("10 < 15", c)
    (cs, rs), c = enso_concentration()
    check("16/36 and 40/900", abs(cs - 16 / 36) < 1e-12
          and abs(rs - 40 / 900) < 1e-12 and c)
    # the checks must be able to say no: perturb one constant's copy
    check("a broken partition is caught",
          round(LIVESTOCK + HUMANS + 0.07, 2) != MAMMAL_TOTAL_STATED)
    print("selftest %d/%d" % (ok, ok + fail))
    return 0 if fail == 0 else 1


if __name__ == "__main__":
    sys.exit(selftest() if "--selftest" in sys.argv[1:] else (report() or 0))
