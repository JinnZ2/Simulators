"""
residual_audit.py -- adjudicate the RESIDUAL cell by hand, on the real spec.

CC0-1.0. Standard library only. Deterministic.

compare.py already says to do this for its middle band:

    PARTIAL = token overlap below threshold. Either the probe reaches it
    under a different name, or it does not. Not resolved here. Resolve by
    hand or rename the open question and re-run.

The same caution belongs on the two confident verdicts. On
systems/provisioning_calibration.json the classifier is wrong in BOTH
directions, and the two errors point opposite ways:

    residual as delivered      0 of 9   -- widen is pooled into coverage
    residual, measuring arms   5 of 9   -- two of those are false negatives
    residual, adjudicated      3 of 9

Zero understates the gap. Five overstates it. Three is the growth edge.
"""

from __future__ import annotations

import json
import os

import compare
import conventional
import coupling
import widen

HERE = os.path.dirname(os.path.abspath(__file__))
SPEC = os.path.join(HERE, "systems", "provisioning_calibration.json")

RULE = "=" * 72

# Hand adjudication. Each open question checked against the probe list by
# reading the protocols, not by counting tokens.
#
#   REACHED   a named probe measures it. pid given.
#   GAP       no probe in any measuring arm measures it.
ADJUDICATED = {
    "confidence accuracy gap":
        ("REACHED", "K06", "confidence / accuracy [coupling] -- elicits "
                           "predicted outcome and stated confidence "
                           "separately, reports the gap"),
    "act consequence latency":
        ("REACHED", "K01", "latency [coupling] -- time from act to "
                           "consequence arriving, distribution not mean"),
    "response magnitude per perturbation size":
        ("REACHED", "K05", "response_magnitude / perturbation_size "
                           "[coupling] -- the ratio is the readout"),
    "discrimination gradient across severities":
        ("REACHED", "K07", "response_magnitude / stimulus_severity "
                           "[organism] -- graded series, 4+ levels, fit "
                           "the slope"),
    "domain match between calibrating environment and test items":
        ("REACHED", "K08", "task_performance / domain_match [coupling] -- "
                           "bidirectional protocol, read the interaction. "
                           "CLASSIFIER FALSE NEGATIVE: 3 of 4 stems"),
    "environmental autocorrelation":
        ("REACHED", "K09", "autocorrelation [environment] -- the "
                           "environment's own variance structure. "
                           "CLASSIFIER FALSE NEGATIVE: 'environmental' "
                           "does not stem to 'environment'"),
    "coupling bandwidth":
        ("GAP", None, "no probe. latency and contingency_consistency "
                      "measure delay and reliability of the loop; neither "
                      "measures how much can cross it per unit time"),
    "whether trust in own sensing is a measurement or a belief":
        ("GAP", None, "no probe. confidence/accuracy reaches the "
                      "confidence-validity gap but not whether the "
                      "organism's reliance on its own sensor was ever "
                      "validated against outcome"),
    "reversibility after regime shift":
        ("GAP", None, "no probe. Nothing measures relearn RATE after the "
                      "buffer is removed, which is the quantity that "
                      "separates the two predicted trajectories"),
}


def section(title: str) -> None:
    print("\n" + RULE)
    print(title)
    print(RULE)


def covered_by(pool, question) -> list[str]:
    return sorted({p["arm"] for p in pool
                   if (lambda hn: hn[0] >= hn[1])(compare.coverage(p, question))})


def main() -> None:
    with open(SPEC) as fh:
        spec = json.load(fh)

    arms = {"conventional": conventional.generate(spec),
            "coupling": coupling.generate(spec),
            "widen": widen.generate(spec)}
    allp = [p for ps in arms.values() for p in ps]
    measuring = [p for p in allp if widen.is_quantity(p)]
    questions = spec["open_questions"]

    print()
    print("RESIDUAL, ADJUDICATED  --  %s" % spec["system_id"])
    print("classifier verdicts vs reading the protocols")

    section("1  three counts of the same cell")

    print("  %-52s %-14s %-12s %s"
          % ("open question", "as delivered", "measuring", "adjudicated"))
    print("  " + "-" * 94)
    n_delivered = n_measuring = n_adjudicated = 0
    for q in questions:
        a = covered_by(allp, q)
        m = covered_by(measuring, q)
        verdict = ADJUDICATED[q][0]
        n_delivered += not a
        n_measuring += not m
        n_adjudicated += verdict == "GAP"
        print("  %-52s %-14s %-12s %s"
              % (q[:50], ",".join(a) or "NO ARM",
                 ",".join(m) or "NO ARM", verdict))

    print()
    print("  residual as delivered    %d of %d   widen pooled into coverage"
          % (n_delivered, len(questions)))
    print("  residual measuring arms  %d of %d   widen excluded"
          % (n_measuring, len(questions)))
    print("  residual adjudicated     %d of %d   protocols read"
          % (n_adjudicated, len(questions)))

    section("2  the classifier is wrong in both directions")

    print("  FALSE POSITIVE -- widen pooling. Five questions are marked")
    print("  COVERED by widen alone. widen proposes no measurement, and the")
    print("  canonical quantities.py will not even let it construct a")
    print("  quantity: OBJECTS is closed and 'design' is not in it. The")
    print("  schema refuses what the comparator then counts.\n")

    print("  FALSE NEGATIVE -- stemming. Two questions a coupling probe was")
    print("  written for score below threshold:\n")
    print("    'environmental autocorrelation'  ->  K09 autocorrelation")
    print("      2 stems, need 2, hits 1. 'environmental' does not stem to")
    print("      'environment'; the stemmer strips -ies/-es/-s only.\n")
    print("    'domain match between calibrating environment and test items'")
    print("      ->  K08 task_performance / domain_match")
    print("      7 stems, need 4, hits 3 (domain, item, match). Misses by one.")
    print()
    print("  The two errors do not cancel. They point opposite ways and land")
    print("  on different questions, so no single threshold fixes both.")

    section("3  the growth edge")

    gaps = [(q, ADJUDICATED[q][2]) for q in questions
            if ADJUDICATED[q][0] == "GAP"]
    print("  Three open questions no measuring arm reaches:\n")
    for q, why in gaps:
        print("  [NO PROBE] %s" % q)
        print("             %s\n" % why)

    print("  'reversibility after regime shift' is the one with a stated")
    print("  prediction attached and no instrument. The predicted contrast")
    print("  is a RATE -- fast relearn against slow relearn once the buffer")
    print("  is removed -- and no probe in the coupling arm measures a rate.")
    print("  Every K-probe measures a level, a ratio, a slope or a variance,")
    print("  all at fixed regime. The falsifier named in the notes ('ratio")
    print("  flat across the provisioning gradient') needs the gradient")
    print("  swept; the probes as generated sit at one point on it.")

    section("READING")
    print("""
  Zero understates, five overstates, three is the count. The two classifier
  errors are independent and opposite, so this cell cannot be trusted
  unadjudicated in either direction -- which is compare.py's own PARTIAL
  caution applied to the confident verdicts.

  What a fix reads out:

    widen pooling     one line. Build the coverage pool from probes whose
                      object_of is in quantities.OBJECTS. The canonical
                      schema already marks them; the comparator just does
                      not ask.

    stemming          not fixable by threshold -- the two false negatives
                      sit at 1-of-2 and 3-of-4. Either stem harder
                      (-al, -ing, -ity) and re-measure the false-positive
                      rate, or drop COVERED to a suggestion and adjudicate
                      the cell by hand as here.

  A comparison case for the third gap: the notes' predicted contrast is
  fast-relearn against slow-relearn after buffer removal. That is a
  post-shift time constant. Adding one probe -- error against trials-since-
  shift, fitted for a rate, at two or more provisioning levels -- closes
  'reversibility after regime shift' and simultaneously supplies the
  gradient the stated falsifier needs.
""")


if __name__ == "__main__":
    main()
