"""
gate_fork.py -- the fork's own claims, through the canonical gate.

CC0-1.0. Stdlib only.

IMPORTS the gate from ../reasoning-gate/ rather than copying it. This folder
received a pre-repair copy in one drop and three more stale files in the
next (MF_006, MF_011); an import cannot go stale. Same arrangement as
msiaf-gdprf-bridge/ and reasoning-dial/gate_dial.py. `GATE_SRC` overrides.

    python3 ../tools/check_gate_drift.py     # verifies there is one gate

The subject is this folder's own findings about the fork -- not the domain
the spec describes, and not the fork's conclusions about that domain.
"""

from __future__ import annotations

import json
import os
import sys

GATE_SRC = os.environ.get(
    "GATE_SRC",
    os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                 "reasoning-gate"))
sys.path.insert(0, GATE_SRC)

from gate import Control, Gate, GateError, Resolution  # noqa: E402

import compare  # noqa: E402
import conventional  # noqa: E402
import coupling  # noqa: E402
import residual_audit as audit  # noqa: E402
import widen  # noqa: E402

GUARDS = os.path.join(GATE_SRC, "guards.json")
RUNS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "runs")
SPEC = audit.SPEC

RULE = "=" * 74


def banner(text: str) -> None:
    print("\n" + RULE)
    print(text)
    print(RULE)


def _counts(spec):
    """(delivered_residual, measuring_residual, adjudicated_gaps, missed_gaps)."""
    arms = {"conventional": conventional.generate(spec),
            "coupling": coupling.generate(spec),
            "widen": widen.generate(spec)}
    allp = [p for ps in arms.values() for p in ps]
    measuring = [p for p in allp if widen.is_quantity(p)]

    def covered(pool, q):
        return any(h >= n for h, n in
                   (compare.coverage(p, q) for p in pool))

    qs = spec["open_questions"]
    gaps = [q for q in qs if audit.ADJUDICATED[q][0] == "GAP"]
    delivered = [q for q in qs if not covered(allp, q)]
    measuring_res = [q for q in qs if not covered(measuring, q)]
    missed = [q for q in gaps if covered(allp, q)]   # gap the classifier hid
    return len(delivered), len(measuring_res), len(gaps), len(missed)


def residual_as_delivered(spec) -> None:
    banner("FORK-RESIDUAL   the residual cell, classifier as delivered")

    _, _, n_gaps, n_missed = _counts(spec)

    g = Gate("FORK-RESIDUAL", guards=GUARDS, strict=False, log_dir=RUNS)
    try:
        g.pre(
            question="how many open questions does no measuring arm reach",
            statistic="stemmed-token coverage over all arms, 60% threshold",
            discriminates="a question below threshold against every probe is "
                          "one nothing measures",
            expected="the residual count equals the number of questions with "
                     "no probe written for them",
            # Instrument scale: gaps the classifier fails to report, as
            # delivered. Feature scale: gaps there are to find.
            resolution=[Resolution(
                "gaps missed by the classifier vs gaps present",
                instrument=float(n_missed), feature=float(n_gaps),
                note="as delivered the classifier reports 0 residual against "
                     "%d real gaps: recall 0 of %d" % (n_gaps, n_gaps))],
            controls=[
                Control("known gap", predicted="a question with no probe "
                                               "written for it appears in "
                                               "RESIDUAL"),
                Control("known reach", predicted="a question a named probe "
                                                 "was written for does not"),
            ],
        )
    except GateError as exc:
        print("  DENIED at pre().\n")
        print("  %s\n" % exc)
        print("  The classifier misses %d of %d gaps, so its positional"
              % (n_missed, n_gaps))
        print("  error on the quantity being measured is the whole quantity.")
        print("  Recall on the growth edge is zero, and a cell that cannot")
        print("  report a gap is not measuring gaps.")
        print()
        print("  G-RES is doing here what it did to SIM-A: an instrument")
        print("  whose error equals the feature returns a null that carries")
        print("  no information. The residual of 0 is that null.")
        return
    raise AssertionError("FORK-RESIDUAL was expected to deny")


def residual_adjudicated(spec) -> None:
    banner("FORK-ADJUDICATED   the same cell, protocols read")

    delivered, measuring, n_gaps, n_missed = _counts(spec)

    g = Gate("FORK-ADJUDICATED", guards=GUARDS, strict=False, log_dir=RUNS)
    g.pre(
        question="how many open questions does no measuring arm reach",
        statistic="hand adjudication: each question read against every "
                  "probe's protocol",
        discriminates="reading a protocol answers whether it measures the "
                      "quantity; token overlap only estimates it",
        expected="a count between the delivered 0 and the widen-excluded %d, "
                 "since the two classifier errors point opposite ways"
                 % measuring,
        resolution=[Resolution(
            "adjudication granularity vs the count",
            instrument=1.0, feature=float(n_gaps),
            note="one question resolved at a time against a count of %d"
                 % n_gaps)],
        controls=[
            Control("cited probe exists",
                    predicted="every REACHED verdict names a probe id "
                              "present in the coupling arm"),
            Control("cited probe measures it",
                    predicted="the named probe's rendered quantity matches "
                              "the described one"),
        ],
        shares_input_with=["compare.py coverage()"],
    )
    g.control_result("cited probe exists",
                     "all 6 REACHED verdicts cite a K-probe present in the "
                     "generated arm")
    g.control_result("cited probe measures it",
                     "all 6 cited quantities match the described one")

    g.record("residual_delivered", delivered, layer="instrument",
             object_of="compare.py coverage() with all arms pooled")
    g.record("residual_measuring", measuring, layer="instrument",
             object_of="compare.py coverage() with widen excluded")
    g.record("gaps_adjudicated", n_gaps, layer="instrument",
             object_of="hand adjudication of the probe list",
             note="instrument-level: a property of how the probe list was "
                  "read, not yet of the design")

    # Instrument-scoped: this is a fact about reading the probe list.
    g.claim("no probe in any measuring arm reaches %d of the spec's open "
            "questions" % n_gaps,
            supported_by=["gaps_adjudicated"], scope="instrument")

    # Physical-scoped: a statement about the design itself, on the same
    # support. The gate should not let this stand on an instrument count.
    g.claim("the measurement design has %d unmeasured quantities" % n_gaps,
            supported_by=["gaps_adjudicated", "residual_delivered"])

    report = g.close(
        observed="adjudicated %d gaps; delivered classifier reported %d and "
                 "widen-excluded reported %d" % (n_gaps, delivered, measuring),
        diverged=True)
    print()
    print(g.summary(report))
    print()
    print("  Two claims, one support. The instrument-scoped one stands: it")
    print("  says what reading the probe list returned. The physical-scoped")
    print("  one is qualified, because a count of what a probe list contains")
    print("  is not yet a statement about the design -- a quantity can be")
    print("  unmeasured because nobody wrote the probe, or because it is not")
    print("  measurable, and this instrument cannot tell those apart.")


def void_the_ratio(spec) -> None:
    banner("FORK-VOID   the cell the fork exists to produce, gated")

    g = Gate("FORK-VOID", guards=GUARDS, strict=False, log_dir=RUNS)
    g.pre(
        question="do the two arms' task_performance numbers compare",
        statistic="ratio of the two reported task_performance values",
        discriminates="a ratio is defined when both operands are properties "
                      "of one object",
        expected="if the arms measure the same quantity, the ratio is "
                 "interpretable; if not, it is void",
        resolution=[Resolution("object_of granularity vs the distinction",
                               instrument=1.0, feature=4.0,
                               note="4 objects in quantities.OBJECTS, "
                                    "resolved one at a time")],
        controls=[Control("same-object ratio",
                          predicted="two quantities of one object divide "
                                    "normally")],
    )
    g.control_result("same-object ratio",
                     "response_magnitude / stimulus_severity is both [organism]"
                     " and computes")

    g.record("perf_conventional", 0.72, layer="physical",
             object_of="organism",
             note="task_performance [organism], conventional arm C05")
    g.record("perf_coupling", 0.91, layer="physical",
             object_of="coupling",
             note="task_performance / domain_match [coupling], K08")

    value = g.ratio("apparent_deficit", "perf_conventional", "perf_coupling")
    print("\n  g.ratio(...) returned %r" % (value,))

    report = g.close(
        observed="both arms report task_performance; the objects differ, so "
                 "the ratio is void",
        diverged=False)
    print()
    print(g.summary(report))
    print()
    print("  This is the VOID RATIO cell reaching the same verdict twice, by")
    print("  two routes. quantities.py refuses the comparison at design time")
    print("  because the object_of fields differ. G-DIM refuses it at report")
    print("  time on the same grounds. The fork's contribution is that the")
    print("  first happens before anyone runs anything.")


def main() -> None:
    os.makedirs(RUNS, exist_ok=True)
    with open(SPEC) as fh:
        spec = json.load(fh)

    print(RULE)
    print("THE FORK, THROUGH THE CANONICAL GATE")
    print(RULE)
    print("gate: %s" % GATE_SRC)
    print("spec: %s" % os.path.basename(SPEC))

    residual_as_delivered(spec)
    residual_adjudicated(spec)
    void_the_ratio(spec)

    banner("READING")
    print("""
  The gate is imported, not copied. That is the whole point of running it
  from here: this folder received a pre-repair gate.py in one drop and three
  more stale files in the next, and an import cannot go stale. Run
  ../tools/check_gate_drift.py to confirm there is still exactly one.

  FORK-RESIDUAL denies at pre(). The classifier misses every gap it is
  meant to find, so its error on the quantity equals the quantity, and the
  residual of 0 is a null from an instrument that could not have seen the
  feature.

  FORK-ADJUDICATED passes and splits on scope. The same count supports an
  instrument-level claim about what reading the probe list returned, and
  fails to support a physical-level claim about the design -- because a
  quantity can be unmeasured for two different reasons and this instrument
  cannot separate them.

  FORK-VOID reaches the fork's own headline cell from the other end. G-DIM
  voids the cross-arm task_performance ratio at report time; quantities.py
  refuses it at design time. Same verdict, and the design-time one is the
  cheaper of the two.
""")


if __name__ == "__main__":
    main()
