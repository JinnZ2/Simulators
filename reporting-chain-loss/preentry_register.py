# SPDX-License-Identifier: CC0-1.0
"""
preentry_register.py -- WO-5 PRE-ENTRY LOSS, the half that never enters.

Two things, both from the order:

(1) A register of the gates that sit UPSTREAM of the form, none of them
    logged anywhere. Each is a place a mechanical observation is lost before
    the record begins, so the reports that arrive are not a sample of machine
    conditions -- they are a sample of conditions severe enough to overcome a
    reporting cost that varies per operator. The register carries the order's
    seven entries verbatim in structure (L0, L0', L1, L1', L2, delegation,
    form-field), each with whether it is logged and whether it conditions the
    sample.

(2) The Test B calibration structure, on CONSTRUCTED operators. The order's
    inverted finding is that "operators do not report" is a calibrated
    estimate from direct evidence: an operator's reporting rate tracks their
    own (reports acted on)/(reports filed) ratio. This module builds two
    worlds -- one where the rate tracks that ratio (calibrated; the fix is at
    closure, not the operator) and one where it does not (something else is
    driving it) -- and shows the classifier separates them. spearman is
    imported from readout-count, not restated.

    The order's STATED LIMITATION is built in as a refusal: delegation-as-null
    makes the per-operator prior UNESTIMABLE for exactly the operators it
    matters most for (the ones who proxy-file read as zero-reporters). If the
    proxy-filed count is undeclared, calibration() returns
    UNESTIMABLE_PROXY_UNDECLARED rather than a number, and pooling proxy-filers
    as zero-reporters is shown to corrupt the correlation.

Nothing here is a measurement of any plant or any operator. The register is
the order's own account; the operators are CONSTRUCTED and seeded.

Stdlib only. Parses under 3.9. ASCII only. CC0.

    python3 preentry_register.py            # render the register + Test B
    python3 preentry_register.py --choices  # the [CHOICE n] markers
    python3 test_hop.py                     # the checks; prints their count
"""

from __future__ import annotations

import os
import random
import sys

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(_ROOT, "readout-count"))
from readout_count import spearman            # noqa: E402  (imported, not restated)

# [CHOICE 1] the tracking threshold: a Spearman rho at or above this reads the
#   constructed world as calibrated. Stated, printed; the order names none.
TRACK_RHO = 0.6

CHOICES = {
    1: "tracking threshold rho >= %.2f reads calibrated; stated, not the "
       "order's" % TRACK_RHO,
}

# The seven gates, from the order. `logged` is False for all (the order says
# none is logged); `conditions_sample` marks the ones that bias which reports
# arrive. Text is the order's, structured not paraphrased.
GATES = [
    {"id": "L0", "name": "INCENTIVE GATE",
     "cost": "reporting costs the reporter: time off the line, line-stop "
             "attribution, reputation",
     "logged": False, "conditions_sample": True},
    {"id": "L0'", "name": "LEARNED PRIOR",
     "cost": "operator's estimate of P(report acted on), from their own "
             "filed-report history; rationally low; non-reporting is correct "
             "inference, not disengagement",
     "logged": False, "conditions_sample": True, "strongest": True},
    {"id": "L1", "name": "INTERFACE GATE",
     "cost": "input device assumes a hand the job does not produce; four or "
             "five attempts per letter on a sub-centimetre key grid",
     "logged": False, "conditions_sample": True},
    {"id": "L1'", "name": "LITERACY / SPELLING GATE",
     "cost": "a mechanical observation must pass a written-language gate to "
             "enter the system at all",
     "logged": False, "conditions_sample": True},
    {"id": "L2", "name": "DEVICE GATE",
     "cost": "personal phone, personal data, personal battery",
     "logged": False, "conditions_sample": True},
    {"id": "DELEGATION", "name": "DELEGATION-AS-NULL",
     "cost": "observation -> spoken account -> proxy typing; provenance drops; "
             "the observer with the most direct coupling reads as contributing "
             "least",
     "logged": False, "conditions_sample": True, "breaks_test_b": True},
    {"id": "FORM-FIELD", "name": "FORM-FIELD LOSS",
     "cost": "what the operator noticed -- sound, vibration, a change in how "
             "the machine takes load -- has no field; never-encodable, not "
             "filtered",
     "logged": False, "conditions_sample": False, "term_gap": True},
]


def register_summary():
    """The structural reading the order draws: with every gate unlogged and
    most of them conditioning which reports arrive, the arriving reports are a
    sample of conditions past a per-operator threshold, not a sample of
    machine conditions. Counts, not a verdict on anyone."""
    n = len(GATES)
    logged = sum(1 for g in GATES if g["logged"])
    conds = sum(1 for g in GATES if g["conditions_sample"])
    return {
        "gates": n,
        "logged": logged,                       # 0: none of them
        "unlogged": n - logged,
        "conditions_sample": conds,
        "arriving_reports_are": "a sample past a per-operator threshold, "
                                "not a sample of machine conditions",
        "threshold_estimated": False,           # the order: "unestimated"
    }


def rational_rate(closure_ratio):
    """A constructed monotone map from (acted on)/(filed) to a reporting
    rate. The order's inverted finding: a rational operator reports more when
    more of their reports are acted on. Kept simple and increasing; this is a
    generator for the CONSTRUCTED world, not a claim about operators."""
    return 0.05 + 0.9 * closure_ratio


def make_world(seed=0, n_ops=40, calibrated=True, noise=0.03):
    """CONSTRUCTED operators. Each has a closure_ratio (acted on / filed). In
    the calibrated world their reporting rate is rational_rate(closure) plus
    small noise; in the other world the rate is independent of closure. No
    operator here is real."""
    rng = random.Random(seed)
    ops = []
    for i in range(n_ops):
        cr = rng.random()
        if calibrated:
            rate = rational_rate(cr) + rng.uniform(-noise, noise)
        else:
            rate = rng.random()
        ops.append({"op": i, "closure_ratio": cr,
                    "reporting_rate": max(0.0, min(1.0, rate)),
                    "proxy_filed": False})
    return ops


def calibration(ops, proxy_declared=True):
    """Test B: does the reporting rate track the closure ratio?

    Returns UNESTIMABLE_PROXY_UNDECLARED when the proxy-filed status is not
    declared -- the order's STATED LIMITATION, not an oversight. When declared,
    proxy-filers are EXCLUDED (their rate reads 0 through no choice of theirs)
    and the correlation is taken on the rest."""
    if not proxy_declared:
        return {"rho": None, "verdict": "UNESTIMABLE_PROXY_UNDECLARED",
                "n_used": None, "n_proxy": None,
                "why": "the per-operator prior is unestimable for proxy-filers; "
                       "any run must declare the proxy-filed count or the "
                       "sample is silently conditioned on people who can type"}
    used = [o for o in ops if not o["proxy_filed"]]
    n_proxy = sum(1 for o in ops if o["proxy_filed"])
    x = [o["closure_ratio"] for o in used]
    y = [o["reporting_rate"] for o in used]
    rho = spearman(x, y)
    if rho is None:
        verdict = "NOT_EVALUABLE"
    elif rho >= TRACK_RHO:
        verdict = "TRACKS_calibrated"          # [CHOICE 1]
    else:
        verdict = "DOES_NOT_TRACK"
    return {"rho": rho, "verdict": verdict, "n_used": len(used),
            "n_proxy": n_proxy}


def delegation_corruption(ops, frac_proxy=0.25, seed=1):
    """The confound made a number. Take a calibrated world, mark a fraction of
    operators as proxy-filers, and read it two ways: (a) declared and excluded
    -- the clean correlation; (b) pooled, the proxy-filers forced to
    reporting_rate 0 as the system records them. Pooling corrupts the
    correlation. Returns both, so the cost of not declaring is visible."""
    rng = random.Random(seed)
    marked = [dict(o) for o in ops]
    idx = list(range(len(marked)))
    rng.shuffle(idx)
    for i in idx[:int(frac_proxy * len(marked))]:
        marked[i]["proxy_filed"] = True

    clean = calibration(marked, proxy_declared=True)

    pooled = [dict(o) for o in marked]
    for o in pooled:
        if o["proxy_filed"]:
            o["reporting_rate"] = 0.0           # the system's own record
            o["proxy_filed"] = False            # pooled: provenance dropped
    pooled_res = calibration(pooled, proxy_declared=True)
    return {"declared_and_excluded": clean, "pooled_as_zero": pooled_res}


def render():
    out = []
    out.append("WO-5 PRE-ENTRY LOSS -- the gates upstream of the form")
    out.append("CONSTRUCTED operators for Test B; the register is the order's "
               "own account. Not a plant.")
    out.append("")
    out.append("[CHOICE 1] %s" % CHOICES[1])
    out.append("")

    out.append("Register (none logged):")
    for g in GATES:
        tag = " [strongest]" if g.get("strongest") else \
              " [breaks Test B]" if g.get("breaks_test_b") else \
              " [term gap]" if g.get("term_gap") else ""
        out.append("  %-11s %-24s conditions_sample=%s%s"
                   % (g["id"], g["name"], g["conditions_sample"], tag))
    s = register_summary()
    out.append("  -> %d gates, %d logged, %d condition which reports arrive"
               % (s["gates"], s["logged"], s["conditions_sample"]))
    out.append("  -> arriving reports are %s" % s["arriving_reports_are"])
    out.append("  -> the threshold is estimated: %s" % s["threshold_estimated"])
    out.append("")

    out.append("Test B -- does reporting rate track (acted on)/(filed)?")
    cal = calibration(make_world(calibrated=True))
    unc = calibration(make_world(calibrated=False))
    out.append("  calibrated world:   rho=%.3f  %s  (n=%d)"
               % (cal["rho"], cal["verdict"], cal["n_used"]))
    out.append("  uncalibrated world: rho=%.3f  %s  (n=%d)"
               % (unc["rho"], unc["verdict"], unc["n_used"]))
    out.append("  both branches reachable, so the classifier is not constant.")
    out.append("")

    out.append("Test B refuses when the proxy-filed count is undeclared "
               "(the order's stated limitation):")
    ref = calibration(make_world(calibrated=True), proxy_declared=False)
    out.append("  %s" % ref["verdict"])
    out.append("")

    out.append("Delegation confound, made a number (calibrated world, 25 "
               "percent proxy-filers):")
    dc = delegation_corruption(make_world(calibrated=True))
    a = dc["declared_and_excluded"]
    b = dc["pooled_as_zero"]
    out.append("  declared and excluded: rho=%.3f  %s"
               % (a["rho"], a["verdict"]))
    out.append("  pooled as zero:        rho=%.3f  %s"
               % (b["rho"], b["verdict"]))
    out.append("  pooling proxy-filers as zero-reporters pulls the "
               "correlation down: the cost of not declaring.")
    return "\n".join(out)


def main(argv):
    if "--selftest" in argv:
        sys.stderr.write(
            "preentry_register.py has no --selftest. The checks are in "
            "test_hop.py:\n    python3 %s\n"
            % os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "test_hop.py"))
        return 2
    if "--choices" in argv:
        for k in sorted(CHOICES):
            print("[CHOICE %d] %s" % (k, CHOICES[k]))
        return 0
    print(render())
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
