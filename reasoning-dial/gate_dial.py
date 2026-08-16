"""
gate_dial.py — put the dial drop through the gate the last drop produced.

CC0-1.0. Stdlib only.

Imports the gate from ../reasoning-gate/ rather than copying it, so the two
cannot drift. Same arrangement as msiaf-gdprf-bridge/, the repo's other
cross-folder import. Set GATE_SRC to override the path.

The subject is SOURCE_DROP.md's own claims, declared and closed the way any
sim would be. Nothing here is a claim about a reasoning model: no reasoning
model was run, and the gate is used to say so precisely.
"""

from __future__ import annotations

import math
import os
import sys

GATE_SRC = os.environ.get(
    "GATE_SRC",
    os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                 "reasoning-gate"))
sys.path.insert(0, GATE_SRC)

from gate import Control, Gate, GateError, Resolution  # noqa: E402

import dial_response as dial  # noqa: E402

GUARDS = os.path.join(GATE_SRC, "guards.json")
RUNS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "runs")


def knee_claim() -> None:
    """The knee table. Denied before it can be recorded."""
    print("\n" + "=" * 74)
    print("DIAL-KNEE   the knee locations")
    print("=" * 74)

    g = Gate("DIAL-KNEE", guards=GUARDS, strict=False, log_dir=RUNS)
    try:
        g.pre(
            question="where does the marginal value of thinking fall off",
            statistic="argmax |d2Q/d(log B)^2| over a swept budget range",
            discriminates="a knee separates the paying region from the "
                          "saturated one",
            expected="knee increases with problem difficulty; gradient there "
                     "decreases",
            # Instrument scale: the rule can return either shoulder, so its
            # positional uncertainty is the distance between them --
            # 2*ln(2+sqrt3)*s = 3.556 in log-budget at D_r = 2.
            # Feature scale: the knee shift the claim needs to detect,
            # ln(knee(D_r=4)) - ln(knee(D_r=2)) = 2.985.
            resolution=[Resolution(
                "shoulder-to-shoulder ambiguity vs the knee shift being read",
                instrument=2.0 * dial.Z_SHOULDER * dial.params(2.0)[1],
                feature=(math.log(dial.knee_saturation(4.0))
                         - math.log(dial.knee_saturation(2.0))),
                note="the rule may return either extremum, so its positional "
                     "uncertainty is the gap between them")],
            controls=[Control("monotone parameterisation",
                              predicted="knee rises with D_r")],
        )
    except GateError as exc:
        print("  DENIED at pre().\n")
        print("  %s\n" % exc)
        print("  The rule can land on either curvature extremum, so it")
        print("  localises the knee no better than the %.2f log-units between"
              % (2.0 * dial.Z_SHOULDER * dial.params(2.0)[1]))
        print("  them -- a factor of %.0fx in tokens. The shift it is being"
              % math.exp(2.0 * dial.Z_SHOULDER * dial.params(2.0)[1]))
        print("  used to detect is %.2f log-units. The ambiguity is larger"
              % (math.log(dial.knee_saturation(4.0))
                 - math.log(dial.knee_saturation(2.0))))
        print("  than the effect before the margin is applied at all.")
        print()
        print("  Note what did NOT catch this. G-FIT asks for a discrimination")
        print("  argument and gets a sentence; it cannot check whether the")
        print("  statistic actually names one point. The ambiguity only became")
        print("  a denial once it was written as two numbers for G-RES. See")
        print("  README 'Where the gate did not help'.")
        return
    raise AssertionError("DIAL-KNEE was expected to deny")


def gradient_claim() -> None:
    """The gradient and cross-gradient. These survive."""
    print("\n" + "=" * 74)
    print("DIAL-GRAD   the gradient and cross-gradient")
    print("=" * 74)

    g = Gate("DIAL-GRAD", guards=GUARDS, strict=False, log_dir=RUNS)
    g.pre(
        question="is thinking budget worth spending on a problem of this "
                 "difficulty",
        statistic="dQ/d(log B) and d2Q/d(log B) d(D_r)",
        discriminates="the cross-gradient is positive where extra budget "
                      "still buys quality and negative where it does not; "
                      "it is a signed quantity with an interior zero",
        expected="dQ/d(log B) at fixed budget peaks at intermediate D_r, so "
                 "the cross-gradient changes sign there",
        # Central difference on D_r with h = 1e-4 against a feature that
        # varies on a scale of ~1 in D_r.
        resolution=[Resolution("finite-difference step vs D_r scale",
                               instrument=1e-4, feature=1.0)],
        controls=[
            Control("trivial limit", predicted="gradient -> 0 as D_r -> 0"),
            Control("saturated limit",
                    predicted="gradient -> 0 as D_r grows without bound"),
        ],
    )

    budget = 1000.0
    rows = [(0.25 * i, dial.gradient(budget, 0.25 * i)) for i in range(0, 41)]
    peak_d_r, peak_g = max(rows, key=lambda r: r[1])

    g.control_result("trivial limit", "gradient(B=1000, D_r=0) = %.5f"
                     % dial.gradient(budget, 0.0))
    g.control_result("saturated limit", "gradient(B=1000, D_r=10) = %.5f"
                     % dial.gradient(budget, 10.0))

    g.record("peak_D_r", peak_d_r, layer="generator",
             object_of="the logistic response model in dial_response.py",
             note="set by MU0, MU_SLOPE, S0 -- not a property of any model")
    g.record("peak_gradient", peak_g, layer="generator",
             object_of="the logistic response model in dial_response.py")
    g.record("fd_step", 1e-4, layer="instrument",
             object_of="the cross-gradient estimator")

    # Scoped to the generator, because that is all it is about.
    g.claim("dQ/d(log B) at fixed budget peaks at intermediate difficulty, so "
            "the cross-gradient has an interior zero",
            supported_by=["peak_D_r", "peak_gradient"],
            scope="generator")

    # The same statement about a deployed model, which nothing here supports.
    g.claim("a reasoning model gains most from extra thinking on "
            "intermediate-difficulty problems",
            supported_by=["peak_D_r", "peak_gradient"])

    report = g.close(
        observed="gradient peaks at D_r = %.2f with an interior sign change "
                 "in the cross-gradient, as predicted" % peak_d_r,
        diverged=False)
    print()
    print(g.summary(report))
    print()
    print("  Two claims on identical support. The generator-scoped one is")
    print("  supported: it is a statement about the curve in dial_response.py,")
    print("  and that curve is what was measured. The second says the same")
    print("  thing about a reasoning model and is downgraded to qualified,")
    print("  because every quantity under it is generator-level.")
    print()
    print("  That gap is the whole finding. The maths is fine. What is missing")
    print("  is a measured quality-vs-budget curve from a real model, which")
    print("  would move peak_D_r from generator to physical and let the second")
    print("  claim stand.")


def independence() -> None:
    """The drop's own convergence claim across four domains."""
    print("\n" + "=" * 74)
    print("DIAL-SYNTH   'the convergence point is interior visibility'")
    print("=" * 74)

    g = Gate("DIAL-SYNTH", guards=GUARDS, strict=False, log_dir=RUNS)
    g.pre(
        question="do reasoning, learning, exploring and harnesses converge on "
                 "interior visibility",
        statistic="agreement of four literature summaries",
        discriminates="four independent research programmes reaching one "
                      "conclusion constrains more than one programme does",
        expected="if the four are independent, agreement is evidence",
        resolution=[Resolution("survey granularity vs claimed convergence",
                               instrument=1.0, feature=4.0,
                               note="one domain resolved per section, four "
                                    "domains claimed to converge")],
        controls=[Control("shared-source check",
                          predicted="if the four sections share sources or a "
                                    "single author's framing, the agreement "
                                    "is qualified")],
    )
    g.control_result(
        "shared-source check",
        "all four sections are one author's summary, selected and framed "
        "together for one argument; several cite the same search results")

    g.convergence(
        across=["reasoning", "learning", "exploring", "harnesses"],
        shared=["one author's selection of what to include",
                "a shared 2026 publication window",
                "the interior-visibility thesis, stated before the survey"],
    )

    report = g.close(
        observed="the four domains are surveyed by one writer to one thesis; "
                 "the agreement is a property of the selection as much as of "
                 "the literature",
        diverged=True)
    print()
    print(g.summary(report))
    print()
    print("  G-IND does not refuse the claim. Interior visibility may well be")
    print("  the right reading. It requires the shared input named, which")
    print("  turns 'four domains converge' into a qualified claim about one")
    print("  survey -- and that is the honest version.")


def main() -> None:
    os.makedirs(RUNS, exist_ok=True)
    print("=" * 74)
    print("THE DIAL DROP, THROUGH THE GATE THE LAST DROP PRODUCED")
    print("=" * 74)
    print("gate: %s" % GATE_SRC)

    knee_claim()
    gradient_claim()
    independence()

    print("\n" + "=" * 74)
    print("READING")
    print("=" * 74)
    print("""
  Three declarations, three different outcomes, none of them "wrong drop".

  DIAL-KNEE denies at pre() on G-RES. Writing the rule's positional
  ambiguity as a number makes it 3.56 log-units -- a 35x span in tokens --
  against a knee shift of 2.99 that it is meant to detect. The knee table
  never gets recorded.

  DIAL-GRAD passes and splits. The same two numbers support a
  generator-scoped claim and fail to support the physical one, which G-LAYER
  downgrades to qualified. This is the cheapest possible statement of what
  the drop is missing: not better maths, a measurement.

  DIAL-SYNTH passes with its convergence qualified. Four domains summarised
  by one author to one thesis are not four independent witnesses.

  The gate was built from an audit of a fractal-geometry drop. It transfers
  to a survey of reasoning research without modification, which is one more
  sample against its own n=1 caveat -- and the guard that fires hardest here,
  G-RES on an ambiguous knee, is the same guard that fired on SIM-C's knee.
""")


if __name__ == "__main__":
    main()
