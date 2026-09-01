#!/usr/bin/env python3
# corpus_loop_sim.py -- CC0, stdlib only, parses under 3.9,
# phone-buildable. WORK ORDER -- FABLE -- 04, TASK 3.
#
# Purpose: let someone else FALSIFY or BOUND the self-confirming loop
# in LOOP_SELF_CONFIRMING_PRIOR.md without needing the transcripts.
#
# HOLD -- NOT A FORECAST. No calibration data exists for f, g, or the
# decay. Every constant below is marked [PLACEHOLDER]. The sim shows
# the SHAPE of the loop and identifies which single unmeasured
# quantity, if measured, most constrains the trajectory. That
# parameter is the finding. No absolute number is emitted as a
# prediction, and the module refuses to print a dated forecast.
#
# The loop (prose-independent form in LOOP_SELF_CONFIRMING_PRIOR.md):
#   P_adv(t) = f(C_t)                 read the prior from the corpus
#   R(t)     = g(P_adv(t), incident)  policy response rises with it
#   C_(t+1)  = C_t + emit(R(t),D(t),K) response enters the record
#   D(t+1)   = D_min + (D(t)-D_min)*decay   contested -> background
#
# D is GAP-C's missing measurement (does the record keep the
# counter-evidence when a frame goes background); K is GAP-B's
# (coupling distance, author to dependency chain). Both are knobs on
# the loop; the sim's contribution is to say which one bounds it, and
# to make explicit that the answer is itself set by an unmeasured
# emission coefficient.

import sys

# ---- [PLACEHOLDER] constants. None is calibrated. The RATIO
#      A_D / A_K decides which knob bounds the loop, and that ratio
#      is exactly GAP-B / GAP-C measured -- see report().
BASE = 0.30     # [PLACEHOLDER] baseline adversarial fraction of new text
A_R = 0.30      # [PLACEHOLDER] response severity -> adversarial framing
A_D = 0.40      # [PLACEHOLDER] dispute density -> counter-evidence attached
A_K = 0.30      # [PLACEHOLDER] coupling distance -> decoupled framing
R0 = 0.10       # [PLACEHOLDER] baseline response severity
GAIN = 0.60     # [PLACEHOLDER] g slope: prior -> response
DECAY = 0.70    # [PLACEHOLDER] D relaxation toward its floor
V = 1.0         # [PLACEHOLDER] text volume emitted per generation
T = 40          # generations
INCIDENT = 0.25  # [PLACEHOLDER] one-time t=0 bump to response severity


def _clamp(x):
    return 0.0 if x < 0.0 else (1.0 if x > 1.0 else x)


def run(p0=0.35, d0=0.30, d_min=0.05, k=0.5,
        a_d=A_D, a_k=A_K, t=T):
    """One trajectory. Returns (P_adv list, D list). All inputs are
    placeholder; the shape, not the values, is the output."""
    adv = p0
    tot = 1.0
    d = d0
    P, Dtrace = [p0], [d0]
    for step in range(t):
        p_adv = adv / tot                     # f: read prior
        incident = INCIDENT if step == 0 else 0.0
        r = _clamp(R0 + GAIN * p_adv + incident)   # g: response
        adv_frac = _clamp(BASE + A_R * r - a_d * d + a_k * k)
        adv += V * adv_frac
        tot += V
        d = d_min + (d - d_min) * DECAY       # contested -> background
        P.append(adv / tot)
        Dtrace.append(d)
    return P, Dtrace


def d_floor(Dtrace, eps=1e-3):
    """Where dispute density stops falling: the first generation within
    eps of the floor it converges to."""
    floor = Dtrace[-1]
    for i, d in enumerate(Dtrace):
        if abs(d - floor) <= eps:
            return i, round(floor, 4)
    return len(Dtrace) - 1, round(floor, 4)


def _range(finals):
    return round(max(finals) - min(finals), 4)


def sensitivity_D(k=0.5, a_d=A_D):
    """Sweep the D-track (initial dispute density and its floor) with K
    held; range of final P_adv is the loop's sensitivity to keeping
    recorded dispute -- GAP-C."""
    finals = []
    for d0 in [0.05, 0.15, 0.30, 0.45, 0.60]:
        for d_min in [0.0, 0.10, 0.30]:
            if d_min > d0:
                continue
            P, _ = run(d0=d0, d_min=d_min, k=k, a_d=a_d)
            finals.append(P[-1])
    return _range(finals), finals


def sensitivity_K(d0=0.30, d_min=0.05, a_k=A_K):
    """Sweep coupling distance with the D-track held; range of final
    P_adv is the loop's sensitivity to writing-layer insulation --
    GAP-B."""
    finals = []
    for k in [0.0, 0.25, 0.5, 0.75, 1.0]:
        P, _ = run(d0=d0, d_min=d_min, k=k, a_k=a_k)
        finals.append(P[-1])
    return _range(finals), finals


def constraining_parameter(a_d=A_D, a_k=A_K):
    """Which single unmeasured quantity most constrains the trajectory,
    under the current [PLACEHOLDER] coefficients. Returns the name and
    both ranges -- and the caveat that the ranking is decided by the
    a_d / a_k ratio, itself GAP-C vs GAP-B, both unmeasured."""
    rd, _ = sensitivity_D(a_d=a_d)
    rk, _ = sensitivity_K(a_k=a_k)
    if rd == rk:
        name = "TIED (at these placeholder coefficients)"
    else:
        name = "D (dispute retention, GAP-C)" if rd > rk \
            else "K (coupling distance, GAP-B)"
    return {"parameter": name, "range_D": rd, "range_K": rk}


def falsifier(a_d_zero=0.0):
    """FALSIFIER (LOOP_SELF_CONFIRMING_PRIOR.md): if P_adv is
    insensitive to D across the plausible range, preserving recorded
    dispute does not bound the loop and the mechanism is NOT
    load-bearing. Reachable by construction: at a_d = 0 the D-track
    carries no emission coefficient and the D-sweep range collapses."""
    rd_live, _ = sensitivity_D(a_d=A_D)
    rd_null, _ = sensitivity_D(a_d=a_d_zero)
    fired = rd_null < 1e-3
    return {"D_sensitivity_live": rd_live,
            "D_sensitivity_at_a_d_zero": rd_null,
            "falsifier_fires_when_coefficient_zero": fired,
            "reading": "with a real (nonzero) dispute coefficient the "
                       "loop IS sensitive to D; the falsifier is the "
                       "branch that fires if measurement finds that "
                       "coefficient near zero"}


def _sparkline(vals):
    lo, hi = min(vals), max(vals)
    span = hi - lo or 1.0
    bars = "▁▂▃▄▅▆▇█"
    return "".join(bars[min(7, int((v - lo) / span * 7))] for v in vals)


def report():
    L = []
    w = L.append
    w("CORPUS LOOP SIM -- SHAPE, NOT FORECAST")
    w("all constants are [PLACEHOLDER]; no value here is a prediction")
    w("")
    P, Dtr = run()
    w("P_adv trajectory (shape only, placeholder coefficients):")
    w("  " + _sparkline(P) + "  (start %.3f -> end %.3f, monotone %s)"
      % (P[0], P[-1], all(b >= a - 1e-9 for a, b in zip(P, P[1:]))))
    fi, fl = d_floor(Dtr)
    w("D floor: dispute density converges to %.4f, reached by "
      "generation %d" % (fl, fi))
    w("")
    sd, _ = sensitivity_D()
    sk, _ = sensitivity_K()
    w("sensitivity of final P_adv:")
    w("  to D-track (GAP-C, dispute retention): range %.4f" % sd)
    w("  to K (GAP-B, coupling distance):       range %.4f" % sk)
    cp = constraining_parameter()
    w("  most-constraining parameter here: %s" % cp["parameter"])
    w("")
    w("THE FINDING (not a forecast):")
    w("  the loop's boundedness is decided by whichever of {D, K}")
    w("  carries the larger EMISSION COEFFICIENT (A_D vs A_K here).")
    w("  those coefficients are exactly GAP-C and GAP-B -- how much")
    w("  keeping recorded dispute, and how much author-chain coupling,")
    w("  actually change the adversarial fraction of what gets")
    w("  written. NEITHER is measured. so the single most valuable")
    w("  measurement is the larger of the two emission coefficients;")
    w("  the ranking above INVERTS if that ratio inverts, which is")
    w("  why the ratio -- not either sweep's number -- is the target.")
    w("")
    f = falsifier()
    w("FALSIFIER branch (must be reachable):")
    w("  D-sensitivity with a live coefficient: %.4f" %
      f["D_sensitivity_live"])
    w("  D-sensitivity at coefficient = 0:      %.4f  -> fires %s" %
      (f["D_sensitivity_at_a_d_zero"],
       f["falsifier_fires_when_coefficient_zero"]))
    w("  %s" % f["reading"])
    w("")
    w("NO DATED FORECAST IS EMITTED. The sim reports shape and the")
    w("parameter to measure; it does not say where P_adv goes in the")
    w("world, because f, g and decay are uncalibrated.")
    return "\n".join(L)


def selftest():
    n = [0]

    def chk(name, ok):
        n[0] += 1
        if not ok:
            sys.stderr.write("FAIL %s\n" % name)
            sys.exit(1)

    # shape: under a severe response and thin dispute retention, P_adv
    # rises; the trajectory is monotone non-decreasing
    P, D = run(d0=0.05, d_min=0.0, k=0.8)
    chk("P_adv rises under low D / high K", P[-1] > P[0])
    chk("trajectory monotone",
        all(b >= a - 1e-9 for a, b in zip(P, P[1:])))

    # higher dispute retention lowers the final adversarial share
    hi_d, _ = run(d0=0.60, d_min=0.30, k=0.5)
    lo_d, _ = run(d0=0.05, d_min=0.00, k=0.5)
    chk("more dispute retention -> lower P_adv", hi_d[-1] < lo_d[-1])

    # higher coupling distance raises it
    hi_k, _ = run(d0=0.30, d_min=0.05, k=1.0)
    lo_k, _ = run(d0=0.30, d_min=0.05, k=0.0)
    chk("more decoupling -> higher P_adv", hi_k[-1] > lo_k[-1])

    # D floor is the converged value and is reached
    _, Dtr = run(d0=0.5, d_min=0.1)
    fi, fl = d_floor(Dtr)
    chk("D floor is the converged value", abs(fl - Dtr[-1]) < 1e-6)
    chk("D floor reached before end", fi <= len(Dtr) - 1)

    # both sensitivities are nonzero with live coefficients
    sd, _ = sensitivity_D()
    sk, _ = sensitivity_K()
    chk("D sensitivity nonzero live", sd > 0)
    chk("K sensitivity nonzero live", sk > 0)

    # the ranking inverts when the coefficient ratio inverts -- so the
    # finding is the ratio, not either sweep
    cp_normal = constraining_parameter(a_d=0.6, a_k=0.1)
    cp_inv = constraining_parameter(a_d=0.1, a_k=0.6)
    chk("ranking is D when A_D dominates",
        cp_normal["parameter"].startswith("D"))
    chk("ranking is K when A_K dominates",
        cp_inv["parameter"].startswith("K"))

    # the falsifier branch is reachable
    f = falsifier()
    chk("falsifier fires at coefficient zero",
        f["falsifier_fires_when_coefficient_zero"])
    chk("loop live-sensitive to D otherwise",
        f["D_sensitivity_live"] > 1e-3)

    # no dated forecast: the report emits no absolute year/probability
    # claim about the world
    rep = report()
    for banned in ("by 20", "in 20", "will reach", "forecast:",
                   "we predict"):
        chk("no forecast token %r" % banned, banned not in rep.lower())
    chk("hold stated", "not a forecast" in rep.lower())

    print("corpus_loop_sim selftest: %d/%d checks pass" % (n[0], n[0]))


if __name__ == "__main__":
    if "--selftest" in sys.argv[1:]:
        selftest()
    else:
        print(report())
