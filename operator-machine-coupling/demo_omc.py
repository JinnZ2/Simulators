# SPDX-License-Identifier: CC0-1.0
"""
A worked pass over the three instruments on CONSTRUCTED data: the pairing
separation, the two shape discriminators, and the permission confound. No row
is a measurement of any operator, machine, or organism. Screened through
sheet-structure-scan/no_severity, with one declared exemption: `error`,
which is the marker's own incident-taxonomy category name ("operator error")
and appears in the discriminator's OPERATOR_ERROR verdict.

    python3 operator-machine-coupling/demo_omc.py            # print
    python3 operator-machine-coupling/demo_omc.py --write    # write samples/
"""

from __future__ import annotations

import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, "sheet-structure-scan"))

import coupling_separation as cs   # noqa: E402
import discriminators as dc        # noqa: E402
import permission_state as ps      # noqa: E402
import no_severity                 # noqa: E402

O = cs.Obs
R = ps.Rec


def render():
    L = []
    L.append("OPERATOR-MACHINE-COUPLING -- CONSTRUCTED DATA, NOT A MEASUREMENT")
    L.append("=" * 64)
    L.append("")
    L.append("1. the pairing separation (SS decomposition):")
    mu = 20.0
    a = {"op0": 3.0, "op1": 0.0, "op2": -3.0}
    b = {"u0": 3.0, "u1": 0.0, "u2": -3.0}
    r = {("op0", "u0"): -1, ("op0", "u1"): -1, ("op0", "u2"): 2,
         ("op1", "u0"): -1, ("op1", "u1"): 3, ("op1", "u2"): -2,
         ("op2", "u0"): 2, ("op2", "u1"): -2, ("op2", "u2"): 0}
    obs = [O(i, j, mu + a[i] + b[j] + r[(i, j)]) for i in a for j in b]
    d = cs.decompose(obs)
    L.append("   SS operator=%.1f  SS unit=%.1f  SS pairing=%.1f  (fraction %.3f)"
             % (d.ss_op, d.ss_unit, d.ss_pair, d.ss_pair / d.ss_total))
    mis = cs.averaged_over_pairings_misses(obs)
    bp = mis["best_pair"]
    L.append("   top-residual pairing: %s  operator main effect=%.1f  "
             "unit main effect=%.1f"
             % (bp["pair"], bp["operator_main_effect"], bp["unit_main_effect"]))
    L.append("   -> both partners average; a main-effects model predicts %.1f, "
             "the pairing delivers %.1f. The %.1f is the coupling that "
             "averaging discards." % (bp["main_effects_predicts"],
                                      bp["observed"], bp["residual"]))

    L.append("")
    L.append("2. operator-error vs coupling-failure discriminator:")
    x1 = [0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3]
    x2 = [0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2]
    L.append("   drops with time-on-unit, flat in role  -> %s"
             % dc.error_vs_coupling(x1, x2, [-float(v) for v in x1]))
    L.append("   drops with role, flat in time-on-unit  -> %s"
             % dc.error_vs_coupling(x1, x2, [-float(v) for v in x2]))
    L.append("   the two hour-counts collinear          -> %s (cannot split)"
             % dc.error_vs_coupling(x1, x1, [-float(v) for v in x1]))

    L.append("")
    L.append("3. fixed-advantage vs convergence-curve discriminator:")
    t = [0, 1, 2, 3, 4, 5, 6, 7]
    L.append("   flat from first contact (genotype control) -> %s"
             % dc.fixed_vs_convergence(t, [2.0 for _ in t]))
    L.append("   accrues with time-in-pairing (coupling)    -> %s"
             % dc.fixed_vs_convergence(
                 t, [0.1, 0.6, 1.2, 1.7, 1.9, 2.0, 2.0, 2.0]))

    L.append("")
    L.append("4. the permission confound (naive vs controlled):")
    conf = ([R("dedicated", ps.COUPLED_AUTHORIZED, 10, None, None)] * 3 +
            [R("dedicated", ps.COUPLED_PROHIBITED, 2, None, None)] +
            [R("pooled", ps.COUPLED_AUTHORIZED, 10, None, None)] +
            [R("pooled", ps.COUPLED_PROHIBITED, 2, None, None)] * 3)
    att = ps.attribution(conf)
    L.append("   naive assignment effect      = %+.1f" % att["naive_assignment_effect"])
    L.append("   controlled for permission    = %+.1f  -> the effect was "
             "permission, not assignment" % att["controlled_assignment_effect"])
    L.append("   with the field absent        -> %s"
             % ps.attribution([R("dedicated", None, 10, None, None),
                               R("pooled", None, 2, None, None)]
                              )["controlled_assignment_effect"])
    return "\n".join(L)


def _exempt():
    """`error` is the marker's incident-taxonomy category name ('operator
    error') surfaced by the OPERATOR_ERROR verdict; a delivered domain term,
    not authored severity language. Verified three ways in selftest_omc? no --
    verified in the demo run below and asserted here."""
    return {"error"}


def main(argv):
    text = render()
    hits = no_severity.hits(text)
    exempt = _exempt()
    real = [(l, w, s) for (l, w, s) in hits if w.lower() not in exempt]
    if real:
        sys.stderr.write("no_severity FAILED (beyond declared exemption):\n")
        for l, w, s in real:
            sys.stderr.write("  line %d: %r in %r\n" % (l, w, s))
        return 1
    # three-arm: masked is clean; the exempt token is the only firer
    masked = text
    for w in exempt:
        masked = re.sub(r"\b%s\b" % w, "X", masked, flags=re.I)
    assert no_severity.check(masked)[0], "masked render is not clean"
    firers = {w.lower() for (_l, w, _s) in hits}
    assert firers == {x.lower() for x in exempt}, "exemption is not the firer set"
    note = " (declared exemption: error -- marker's 'operator error' category)"
    if "--write" in argv:
        out = os.path.join(HERE, "samples", "omc_demo.sample.txt")
        with open(out, "w") as fh:
            fh.write(text + "\n")
        sys.stderr.write("wrote %s (no_severity: clean%s)\n" % (out, note))
    else:
        print(text)
        sys.stderr.write("\n(no_severity: clean%s)\n" % note)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
