"""
proposed_probes.py -- do K14-K18 close the gaps MF_010 named?

CC0-1.0. Standard library only. Deterministic.

MF_010 adjudicated three open questions in
systems/provisioning_calibration.json as reached by no measuring arm:

    coupling bandwidth
    whether trust in own sensing is a measurement or a belief
    reversibility after regime shift

and named the shape of the missing instrument for the third: the predicted
contrast is a RATE, and no K-probe in the delivered coupling arm returns one.

Five probes have since been specified. This checks each gap against them by
reading the protocols, the same way residual_audit.py does -- not by adding
them to coupling.py, which is delivered and unmodified.

Result: two of three close, one does not, and the one that does not is the
one with the stated prediction.
"""

from __future__ import annotations

RULE = "=" * 72


def section(title: str) -> None:
    print("\n" + RULE)
    print(title)
    print(RULE)


# The proposed probes, as specified. object_of values are from the closed
# vocabulary in quantities.py; "returns" is the kind of quantity, which is
# what MF_010 turned on.
PROPOSED = (
    ("K14", "practice_rate", "coupling", "rate",
     "is the channel exercised during the stable interval. "
     "sweep: provisioning level. signature: expenditure with zero return, "
     "concurrent with all-nominal state variables."),
    ("K15", "baseline_freshness", "coupling", "duration",
     "time since last clean reference acquisition. protocol: inject a small "
     "known deviation; measure detection threshold. Threshold rises with "
     "staleness."),
    ("K16", "detection_latency", "coupling", "latency",
     "small-signal detection before the outcome column moves. "
     "sweep: baseline staleness."),
    ("K17", "aggregation_depth", "instrument", "count",
     "how many distinct object_of quantities sit under each single term in "
     "the model. protocol: decompose each term, tag each component with "
     "object_of. Count > 1 is a flag."),
    ("K18", "budget_closure", "design", "audit",
     "name every input and every disposal path; which are inside the "
     "boundary, which outside, and who set the line. A ratio comparing a "
     "closed budget to an open one is void."),
)

# Hand adjudication of MF_010's three gaps against the proposals above.
GAPS = (
    ("coupling bandwidth",
     "OPEN", None,
     "K14 measures how often the channel is exercised, K15 how stale the "
     "reference is, K16 how fast a small signal is detected. None measures "
     "how much can cross the loop per unit time. Rate-of-use, staleness and "
     "latency are three different quantities from capacity."),

    ("whether trust in own sensing is a measurement or a belief",
     "CLOSED", "K15",
     "the protocol injects a small KNOWN deviation and measures the "
     "detection threshold against it. That is the sensing apparatus scored "
     "against ground truth rather than against its own report, which is "
     "exactly the distinction the question asks for."),

    ("reversibility after regime shift",
     "PARTIAL", "K14",
     "K14 sweeps provisioning level, which supplies the gradient the stated "
     "falsifier needs ('ratio flat across the provisioning gradient') and "
     "which the delivered probes did not have. But no proposed probe "
     "measures relearn rate AFTER the buffer is removed. K16 is a latency "
     "swept against baseline staleness at fixed regime, not a time constant "
     "across a regime change."),
)


def check_kinds() -> None:
    section("1  MF_010 said no K-probe returns a rate")

    print("  %-6s %-22s %-12s %-10s" % ("id", "quantity", "object_of",
                                        "returns"))
    print("  " + "-" * 56)
    for pid, base, obj, kind, _ in PROPOSED:
        print("  %-6s %-22s %-12s %-10s" % (pid, base, obj, kind))
    print()
    rates = [p for p in PROPOSED if p[3] == "rate"]
    print("  probes returning a rate: %s"
          % (", ".join(p[0] for p in rates) or "none"))
    print()
    print("  K14 is the first. The delivered arm returned levels, ratios,")
    print("  slopes and variances, all at fixed regime.")
    print()
    print("  K18's object_of is `design`, outside quantities.OBJECTS -- so by")
    print("  MF_008 it is a widen move, not a probe, and must not enter the")
    print("  coverage pool. The specification says as much by calling it a")
    print("  widen move.")


def check_gaps() -> None:
    section("2  the three gaps against the proposals")

    for q, verdict, pid, why in GAPS:
        print("  [%-7s] %s" % (verdict, q))
        print("             %s" % (("via %s" % pid) if pid else "no probe"))
        for line in _wrap(why, 13):
            print(line)
        print()

    closed = sum(1 for _, v, _, _ in GAPS if v == "CLOSED")
    partial = sum(1 for _, v, _, _ in GAPS if v == "PARTIAL")
    still = sum(1 for _, v, _, _ in GAPS if v == "OPEN")
    print("  closed %d   partial %d   open %d   of %d"
          % (closed, partial, still, len(GAPS)))


def check_mediation() -> None:
    section("3  the mediation chain is the falsifiable part")

    print("  Predicted order, with lags:\n")
    print("      practice_rate falls        K14")
    print("        -> baseline_freshness degrades   K15   lag 1")
    print("          -> detection_latency rises     K16   lag 2")
    print()
    print("  all three while state variables read nominal.\n")
    print("  Stated falsifier: if K14 predicts K16 with K15 controlled out,")
    print("  the causal chain is wrong.\n")
    print("  That is a real mediation test and it is the strongest thing in")
    print("  the specification. It is refutable by a partial correlation on")
    print("  three measured series, it names which way the refutation cuts,")
    print("  and it does not depend on the effect being large.")
    print()
    print("  What it needs that is not specified: the lag units. 'lag 1' and")
    print("  'lag 2' are ordinal. Whether the lag is hours or seasons decides")
    print("  the sampling rate, and a mediation test sampled coarser than the")
    print("  lag returns the chain collapsed into a single step.")
    print()
    print("  That is a G-RES pair once the units are declared: sampling")
    print("  interval against the lag being resolved.")


def _wrap(text: str, indent: int, width: int = 58):
    words, lines, cur = text.split(), [], ""
    for w in words:
        if len(cur) + len(w) + 1 > width:
            lines.append(" " * indent + cur)
            cur = w
        else:
            cur = (cur + " " + w).strip()
    if cur:
        lines.append(" " * indent + cur)
    return lines


def main() -> None:
    print()
    print("PROPOSED PROBES K14-K18 AGAINST THE GAPS MF_010 NAMED")
    print("adjudicated by reading protocols; coupling.py is unmodified")

    check_kinds()
    check_gaps()
    check_mediation()

    section("READING")
    print("""
  Two of the three gaps move.

  `whether trust in own sensing is a measurement or a belief` closes on
  K15, because injecting a known deviation scores the sensing apparatus
  against ground truth rather than against its own report. That is the
  distinction the question asks for, and no delivered probe had it.

  `reversibility after regime shift` goes partial. K14 supplies the
  provisioning gradient the stated falsifier needs and the delivered
  probes lacked -- that half is closed. The other half is not: no proposed
  probe measures relearn rate after the buffer is removed. K16 is a
  latency swept against staleness at FIXED regime. The predicted contrast
  is across a regime change.

  `coupling bandwidth` does not move. Rate-of-use, staleness and latency
  are three quantities, and capacity is a fourth.

  The mediation chain K14 -> K15 -> K16 is the strongest part of the
  specification: refutable by a partial correlation, with the direction of
  refutation named in advance. Its one gap is that the lags are ordinal.
  Declare the units and it becomes a G-RES pair -- sampling interval
  against the lag being resolved -- and a mediation test sampled coarser
  than its own lag returns the chain collapsed into one step.
""")


if __name__ == "__main__":
    main()
