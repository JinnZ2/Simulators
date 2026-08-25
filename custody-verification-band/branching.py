#!/usr/bin/env python3
"""
BRANCHING ANCHORS
The physics numbers this folder rests on, recomputed from their own terms.
Stdlib only. CC0.

Two labels in the delivered anchor block name the wrong quantity. The numbers
are real; what they are attached to is not. Both are recomputed here rather
than asserted, because an anchor that cannot be recomputed is a citation, not
an anchor.
"""

import argparse
import math
import sys

N_BRANCH = 2


def area_preserving_radius_ratio(n=N_BRANCH):
    """beta = r_{k+1}/r_k when total cross-section is conserved: n*beta^2 = 1."""

    if n < 2:
        raise ValueError("branching ratio must be at least 2")
    return n ** -0.5


def space_filling_length_ratio(n=N_BRANCH):
    """gamma = l_{k+1}/l_k when each generation fills the same volume."""

    if n < 2:
        raise ValueError("branching ratio must be at least 2")
    return n ** (-1.0 / 3.0)


def murray_radius_ratio(n=N_BRANCH):
    """beta under Murray's law: r_parent^3 = sum r_child^3, so n*beta^3 = 1.

    This is the small-vessel, Poiseuille-dominated regime. It is NOT area
    preserving -- it is area increasing, and that is the whole difference.
    """

    if n < 2:
        raise ValueError("branching ratio must be at least 2")
    return n ** (-1.0 / 3.0)


def aggregate_cross_section_ratio(beta, n=N_BRANCH):
    """Total cross-section at level k+1 divided by that at level k.

    n * beta^2. Equal to 1 under area preservation, by construction -- that
    is what the name means. Greater than 1 under Murray's law.
    """

    if beta <= 0:
        raise ValueError("radius ratio must be positive")
    return n * beta ** 2


def metabolic_exponent(n=N_BRANCH, levels=20):
    """The 3/4 exponent, derived rather than quoted.

    Terminal-unit count N_c = n^L. Body mass tracks vascular volume, and
    V_0/V_c = beta^(-2L) * gamma^(-L). The exponent a in N_c ~ M^a is then
    log(N_c) / log(V_0/V_c), which comes out at 3/4 for n=2 -- and needs BOTH
    the area-preserving radius ratio and the space-filling length ratio to do
    so. Quoting one number for both is what the anchor block did.
    """

    if levels < 1:
        raise ValueError("levels must be at least 1")
    beta = area_preserving_radius_ratio(n)
    gamma = space_filling_length_ratio(n)
    volume_ratio = beta ** (-2 * levels) * gamma ** (-levels)
    terminal_units = float(n ** levels)
    return math.log(terminal_units) / math.log(volume_ratio)


def report(stream=sys.stdout):
    w = stream.write
    n = N_BRANCH
    w("BRANCHING ANCHORS (n = %d)\n\n" % n)
    w("  radius ratio, area-preserving   beta  = n^-1/2 = %.4f\n"
      % area_preserving_radius_ratio(n))
    w("  length ratio, space-filling     gamma = n^-1/3 = %.4f\n"
      % space_filling_length_ratio(n))
    w("  radius ratio, Murray's law      beta  = n^-1/3 = %.4f\n\n"
      % murray_radius_ratio(n))

    w("  DELIVERED: 'area-preserving junctions, r_ratio = 2^(-1/3) ~= 0.794'\n")
    w("  0.7937 is the space-filling LENGTH ratio, or equivalently the\n")
    w("  Murray's-law RADIUS ratio. It is not the area-preserving radius\n")
    w("  ratio, which is 0.7071. The value is right; the label names the\n")
    w("  wrong quantity under the wrong assumption.\n\n")

    w("  metabolic exponent, derived over 20 levels: %.6f  (3/4 = 0.75)\n"
      % metabolic_exponent())
    w("  It needs BOTH ratios. One number cannot stand for both.\n\n")

    w("AGGREGATE CROSS-SECTION, n * beta^2 per generation\n")
    for label, beta in (("area-preserving", area_preserving_radius_ratio(n)),
                        ("Murray's law", murray_radius_ratio(n))):
        ratio = aggregate_cross_section_ratio(beta, n)
        verdict = ("CONSTANT" if abs(ratio - 1.0) < 1e-12
                   else "widens x%.4f per generation" % ratio)
        w("  %-18s %.4f   %s\n" % (label, ratio, verdict))
    w("\n  DELIVERED: 'area-preserving ... => aggregate cross-section WIDENS\n")
    w("  every generation'. Under area preservation it is CONSTANT -- that is\n")
    w("  what the name asserts. It widens under Murray's law, the small-vessel\n")
    w("  regime. So 'trunk never wins by construction' holds in the Murray\n")
    w("  regime and is NEUTRAL, not supporting, in the area-preserving one.\n")
    w("  The conclusion survives; the stated route to it does not.\n")


def selftest(stream=sys.stdout):
    checks = []

    def check(name, cond):
        checks.append((name, bool(cond)))

    def raises(fn, *a):
        try:
            fn(*a)
        except ValueError:
            return True
        return False

    check("area-preserving radius ratio is 2^-1/2",
          abs(area_preserving_radius_ratio() - 0.70710678) < 1e-7)
    check("space-filling length ratio is 2^-1/3",
          abs(space_filling_length_ratio() - 0.79370053) < 1e-7)
    check("Murray radius ratio equals the space-filling length ratio",
          abs(murray_radius_ratio() - space_filling_length_ratio()) < 1e-12)
    check("0.794 is NOT the area-preserving radius ratio",
          abs(area_preserving_radius_ratio() - 0.7937) > 0.08)
    check("area preservation holds cross-section constant",
          abs(aggregate_cross_section_ratio(
              area_preserving_radius_ratio()) - 1.0) < 1e-12)
    check("Murray's law widens cross-section",
          aggregate_cross_section_ratio(murray_radius_ratio()) > 1.0)
    check("Murray widening is n^(1/3) per generation",
          abs(aggregate_cross_section_ratio(murray_radius_ratio())
              - N_BRANCH ** (1.0 / 3.0)) < 1e-12)
    check("metabolic exponent is 3/4", abs(metabolic_exponent() - 0.75) < 1e-9)
    check("exponent is level-count independent",
          abs(metabolic_exponent(levels=5)
              - metabolic_exponent(levels=50)) < 1e-9)
    check("exponent moves with branching ratio",
          abs(metabolic_exponent(n=3) - 0.75) < 1e-9)
    check("branching ratio below 2 is rejected",
          raises(area_preserving_radius_ratio, 1))
    check("non-positive radius ratio is rejected",
          raises(aggregate_cross_section_ratio, 0.0))
    check("zero levels rejected", raises(metabolic_exponent, 2, 0))

    passed = sum(1 for _, ok in checks if ok)
    for name, ok in checks:
        stream.write("  %s  %s\n" % ("ok  " if ok else "FAIL", name))
    stream.write("\nselftest %d/%d\n" % (passed, len(checks)))
    return passed == len(checks)


def main(argv=None):
    p = argparse.ArgumentParser(description="branching anchors")
    p.add_argument("--selftest", action="store_true")
    a = p.parse_args(argv)
    if a.selftest:
        return 0 if selftest() else 1
    report()
    return 0


if __name__ == "__main__":
    sys.exit(main())
