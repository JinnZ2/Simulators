#!/usr/bin/env python3
"""
retro_sim_stack.py — run the gate backwards over a drop that already shipped.

CC0-1.0. Stdlib only.

The sim stack in ../aperiodic-order-sim-stack/ was delivered as a finished
result: three simulations, one conclusion, no gate. Auditing it afterwards
took reading four figures against a report and rerunning a control the
drop skipped.

This script asks the cheaper question: which of those findings would the
gate have caught, and at what stage?

Companion to replay_sim_stack.py, which replays the same three sims as
delivered. The two disagree about SIM-B, and the disagreement is the
useful part — see AUDIT_NOTES.md section 1.

Every number below is sourced. Nothing is invented for the demonstration:

  [R]  SIM_STACK_REPORT.txt, as delivered
  [F]  a shipped figure, read directly off the panel
  [C]  ../aperiodic-order-sim-stack/finite_n_control.py, measured
  [G]  gate.py's own docstring usage example

Run with strict=False so the post-stage guards accumulate findings instead
of stopping at the first one. Pre-stage guards deny regardless — that is
the design, and two of the three sims never open.
"""

from __future__ import annotations

import os

from gate import Control, Gate, GateError, Resolution

HERE = os.path.dirname(os.path.abspath(__file__))
RUNS = os.path.join(HERE, "runs")

RULE = "=" * 74


def banner(text: str) -> None:
    print("\n" + RULE)
    print(text)
    print(RULE)


# ---------------------------------------------------------------------------
# SIM-A — denied at the door
# ---------------------------------------------------------------------------

def sim_a() -> None:
    banner("SIM-A  structure factor")

    g = Gate("SIM-A", strict=False, log_dir=RUNS)
    try:
        g.pre(
            question="does the cascade set share spectral order with the "
                     "Ammann-Beenker tiling",
            statistic="structure factor S(k), radial average",
            discriminates="S(k) separates pure-point from diffuse order",
            expected="AB: dense point spectrum, many sharp peaks off k=0. "
                     "cascade: flat, S(k) -> 1",
            # [G] both scales are gate.py's own usage example.
            resolution=[Resolution("k-grid vs Bragg peak width",
                                   instrument=0.39, feature=0.063)],
            controls=[Control("periodic lattice",
                              predicted="sharp peaks at reciprocal vectors")],
        )
    except GateError as exc:
        print("  DENIED at pre(). the sim never runs.\n")
        print("  %s\n" % exc)
        print("  The k-grid is 6.2x coarser than the peaks it must resolve.")
        print("  At the gate's default 2x margin that is a 12.4x shortfall.")
        print("  A run in this configuration cannot see Bragg peaks whether")
        print("  or not they are there, so its null carries no information.")
        print()
        print("  This is the audit's Finding 4 — 'no Bragg star visible in")
        print("  the S(k) figure' — arriving before the figure exists, as an")
        print("  arithmetic check on two declared numbers.")
        return

    raise AssertionError("SIM-A was expected to deny at pre()")


# ---------------------------------------------------------------------------
# SIM-B — denied on the artifact floor
# ---------------------------------------------------------------------------

def sim_b() -> None:
    banner("SIM-B  fractal dimension  (the decisive sim)")

    # [C] artifact budget measured by finite_n_control.py: worst finite-N
    #     shift 0.137 plus box-ladder shift 0.115.
    # [R] the separation the sim must resolve.
    artifact_floor = 0.252
    separation = 0.334

    g = Gate("SIM-B", strict=False, log_dir=RUNS)
    try:
        g.pre(
            question="do the quasiperiodic and cascade fractal dimensions "
                     "coincide",
            statistic="box-counting dimension D_f, plateau fit",
            discriminates="D_f separates sets by how coverage scales",
            expected="if the classes are distinct, |D_f(AB) - D_f(cascade)| "
                     "exceeds the estimator's artifact floor",
            resolution=[Resolution("estimator artifact floor vs separation",
                                   instrument=artifact_floor,
                                   feature=separation)],
            controls=[
                Control("Line, true D_f = 1", predicted="1.000"),
                Control("matched-N Poisson at 1,024 pts",
                        predicted="~1.9, as at 12,000 pts"),
            ],
        )
    except GateError as exc:
        print("  DENIED at pre().\n")
        print("  %s\n" % exc)
        print("  Artifact floor %.3f, separation %.3f. The floor alone does"
              % (artifact_floor, separation))
        print("  not swallow the effect — but the gate's default 2x margin")
        print("  requires %.3f, and the effect is %.3f."
              % (artifact_floor * 2, separation))
        print()
        print("  Read this as the gate's policy dial rather than a verdict:")
        print("  at margin 1.0 the declaration passes, narrowly. That is the")
        print("  audit's Finding 2 restated — direction survives, magnitude")
        print("  does not — as a margin the operator has to choose out loud")
        print("  instead of a precision quietly implied by three decimals.")
        print()
        print("  Rerunning below at margin 1.0 to reach the post-stage guards.")
        sim_b_relaxed(artifact_floor, separation)
        return

    raise AssertionError("SIM-B was expected to deny at pre()")


def sim_b_relaxed(artifact_floor: float, separation: float) -> None:
    g = Gate("SIM-B-margin1", strict=False, log_dir=RUNS)
    g.pre(
        question="do the quasiperiodic and cascade fractal dimensions coincide",
        statistic="box-counting dimension D_f, plateau fit",
        discriminates="D_f separates sets by how coverage scales",
        expected="if the classes are distinct, |D_f(AB) - D_f(cascade)| "
                 "exceeds the estimator's artifact floor",
        resolution=[Resolution("estimator artifact floor vs separation",
                               instrument=artifact_floor, feature=separation,
                               margin=1.0,
                               note="margin relaxed from the 2.0 default")],
        controls=[
            Control("Line, true D_f = 1", predicted="1.000"),
            Control("matched-N Poisson at 1,024 pts",
                    predicted="~1.9, as at 12,000 pts"),
        ],
        shares_input_with=["SIM-A"],
    )

    # [F] sim_b_boxcount_local.png — the report's headline estimator.
    g.record("D_f_AB_boxcount", 1.889, layer="physical", object_of="AB tiling",
             note="[F] plateau fit, 12,000 pts")
    g.record("D_f_cascade_boxcount", 1.555, layer="physical",
             object_of="cascade set", note="[F] plateau fit, 1,024 pts")

    # [F] sim_b_sandbox_local.png — shipped, absent from the report.
    g.record("D_f_AB_sandbox", 1.946, layer="physical", object_of="AB tiling",
             note="[F] mass-radius, never reported")
    g.record("D_f_cascade_sandbox", 1.969, layer="physical",
             object_of="cascade set", note="[F] mass-radius, never reported")

    # The Line control ran twice and disagreed with itself.
    g.control_result("Line, true D_f = 1",
                     "box-count 1.000 (pass); sandbox 1.913 (fail, "
                     "error 0.913 > the 0.334 effect under study)")
    # The matched-N control is deliberately left unrun — as in the drop.

    g.claim("the quasiperiodic and cascade dimensions do not coincide",
            supported_by=["D_f_AB_boxcount", "D_f_cascade_boxcount"])
    g.claim("the two classes do not share a common fractal geometry",
            supported_by=[])

    report = g.close(
        observed="two estimators shipped. box-count separates by +0.334, "
                 "sandbox by -0.023 with the sign reversed. the sandbox "
                 "estimator fails the Line control at 1.913.")
    print()
    print(g.summary(report))
    print()
    print("  The gate cannot know the sandbox numbers exist unless they are")
    print("  recorded, and it cannot stop an author from omitting them. What")
    print("  it does force is the shape of the record: the Line control has")
    print("  one slot, both results go in it, and the disagreement is in the")
    print("  report next to the claim that rests on it. Finding 1 becomes a")
    print("  line item rather than something to notice in an unreferenced")
    print("  figure.")
    print()
    print("  G-CTRL flags the matched-N Poisson run as declared-never-run.")
    print("  G-SUP marks the geometry claim unsupported: it names nothing.")


# ---------------------------------------------------------------------------
# SIM-C — the void
# ---------------------------------------------------------------------------

def sim_c() -> None:
    banner("SIM-C  threshold sweep")

    g = Gate("SIM-C", strict=False, log_dir=RUNS)
    g.pre(
        question="does the band-edge knee correspond to the cascade "
                 "branching threshold",
        statistic="band-edge splitting vs aperiodicity fraction f",
        discriminates="a knee in the splitting curve locates a threshold",
        expected="if the two correspond, the knee sits at the cascade's own "
                 "branching fraction",
        # f is swept in steps of 0.05 [F]; a knee must be at least a few
        # steps wide to be locatable at all.
        resolution=[Resolution("f-grid vs knee width", instrument=0.05,
                               feature=0.15,
                               note="[F] sweep step read off the sweep panel")],
        controls=[Control("threshold inserted at a known f",
                          predicted="detector recovers the inserted f")],
    )

    # [R] both numbers straight from the SIM-C section.
    g.record("knee_splitting", 0.0812, layer="physical",
             object_of="tight-binding lattice model",
             note="[R] normalized to t0 = 1")
    g.record("cascade_E_split", 0.0015, layer="physical",
             object_of="cascade set", note="[R] normalized to E0")

    # [R] the report divides one by the other and gets 54.1.
    value = g.ratio("ratio_54x", "knee_splitting", "cascade_E_split")
    print("\n  g.ratio(...) returned %r" % (value,))

    g.claim("the two systems show different threshold behavior",
            supported_by=[])

    report = g.close(
        observed="no sharp threshold found. splitting grows gradually. "
                 "curvature has comparable peaks at f = 0.45 / 0.55 / 0.65 / "
                 "0.70 / 0.80 / 0.90 and the winner lands on a local minimum "
                 "of the curve it is meant to find the knee of.")
    print()
    print(g.summary(report))
    print()
    print("  G-DIM voids the 54.1. Both operands are real, both are")
    print("  dimensionless, the division runs without error — and the")
    print("  quotient is a property of the lattice model over a property of")
    print("  the cascade set, which denotes nothing. The report reaches the")
    print("  same place in words: 'the two systems operate on very different")
    print("  normalized energy scales.' The gate reaches it as a void.")
    print()
    print("  G-CTRL: the positive control was declared and never run, so the")
    print("  null cannot be entered as evidence. That is Finding 3, caught")
    print("  structurally rather than by noticing a null promoted to a")
    print("  positive three sections later.")
    print()
    print("  G-SUP: the threshold claim names no quantity. Recorded")
    print("  unsupported.")


# ---------------------------------------------------------------------------
# the overall conclusion
# ---------------------------------------------------------------------------

def overall() -> None:
    banner("SIM-STACK  the overall conclusion")

    g = Gate("SIM-STACK", strict=False, log_dir=RUNS)
    g.pre(
        question="do the three sims converge on structural distinctness",
        statistic="agreement of three verdicts",
        discriminates="three independent lines agreeing constrains more than "
                      "one line does",
        expected="if the lines are independent, agreement multiplies "
                 "confidence",
        # [R] the matched-N baseline is fine enough to resolve the claimed
        #     separation — this one passes.
        resolution=[Resolution("matched-N baseline vs claimed separation",
                               instrument=0.021, feature=0.334)],
        controls=[Control("independence check",
                          predicted="if the sims share point sets, agreement "
                                    "is qualified, not independent")],
    )
    g.control_result(
        "independence check",
        "SIM-A and SIM-B run on the same two point sets; SIM-C shares the "
        "cascade's branching parameters")

    g.convergence(
        across=["SIM-A", "SIM-B", "SIM-C"],
        shared=["the same Ammann-Beenker point set",
                "the same 1,024-point cascade set",
                "one author's generator code, unpublished"],
    )

    report = g.close(
        observed="the three lines are not independent. SIM-A and SIM-B are "
                 "two statistics on one pair of point sets, and SIM-C's "
                 "contribution is a null.")
    print()
    print(g.summary(report))
    print()
    print("  G-IND does not forbid the convergence claim. It requires the")
    print("  shared input to be named, which downgrades 'three independent")
    print("  simulations converge' to a qualified claim about two statistics")
    print("  over one pair of point sets. The report's word is 'independent'.")
    print("  Nothing in the drop establishes that.")


def main() -> None:
    os.makedirs(RUNS, exist_ok=True)

    print(RULE)
    print("THE GATE, RUN BACKWARDS OVER A DROP THAT ALREADY SHIPPED")
    print(RULE)
    print("Subject: ../aperiodic-order-sim-stack/")
    print("Sources: [R] report  [F] figure  [C] measured control  [G] gate.py")

    sim_a()
    sim_b()
    sim_c()
    overall()

    banner("WHAT THE GATE WOULD HAVE CAUGHT")
    print("""
  Finding 1  two estimators, opposite signs, one reported
             PARTIAL — G-CTRL gives the Line control one slot that both
             results must go into, so the disagreement lands next to the
             claim. The gate cannot compel an author to record a run.

  Finding 2  decisive gap ~75% inside the artifact budget
             CAUGHT at pre() — G-RES, as a comparison of two declared
             numbers, before any point set is generated. But see
             AUDIT_NOTES.md section 1: replay_sim_stack.py declares
             SIM-B's resolution as smallest-box vs nearest-neighbour
             spacing and PASSES. Same guard, same sim, opposite
             verdicts. G-RES is only as strong as the pair declared,
             and nothing makes the binding pair the declared one.

  Finding 3  SIM-C's null entered as positive evidence
             CAUGHT twice — G-CTRL on the unrun positive control, G-SUP
             on the claim that names nothing.

  Finding 4  no Bragg peaks in the S(k) figure
             CAUGHT at pre() — G-RES. The k-grid is 6.2x coarser than the
             peak width. SIM-A never runs.

  Not in the audit, surfaced here:
             G-DIM voids the ratio 54.1. Two real numbers, a clean
             division, and a quotient that is a property of one object
             over a property of another.

             G-IND downgrades 'three independent simulations converge'.
             Two of the three are statistics on the same pair of point
             sets.

  Two of the four audit findings are pre-stage arithmetic. They cost two
  declared numbers each and would have landed before the first figure was
  rendered. The audit cost four figures read against a report and a
  control rerun from scratch.
""")


if __name__ == "__main__":
    main()
