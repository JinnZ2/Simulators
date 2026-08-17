"""
coverage_check.py -- null-test compare.py's RESIDUAL classifier.

CC0-1.0. Standard library only. Deterministic.

WHY
---
compare.py's docstring calls the RESIDUAL cell the growth edge: the open
questions no arm reaches. That cell is produced by `coverage()`, which
compares stemmed tokens between an open question and a probe and calls the
question COVERED when the overlap clears 60% of the question's distinct
stems.

A lexical proxy deciding a semantic question is the same shape as
../reasoning-gate/'s G-FIT accepting a non-empty prose string. It may still
be a good enough proxy -- that is a measurement, not an assumption. So run
the checks ../null-harness/ would demand of any gate: does it fire when it
should, stay silent when it should, and is anything upstream of it
suppressing the signal?

Three checks. The classifier survives one null and fails another; it catches
the questions its probes were written for; and the arm pooling upstream of it
suppresses the growth edge outright. The third is the one that matters.
"""

from __future__ import annotations

import json
import os

import compare
import conventional
import coupling
import widen

HERE = os.path.dirname(os.path.abspath(__file__))
SPEC = os.path.join(HERE, "systems", "variable_provisioning.json")

RULE = "=" * 70


def section(title: str) -> None:
    print("\n" + RULE)
    print(title)
    print(RULE)


def arms(spec) -> dict[str, list]:
    return {"conventional": conventional.generate(spec),
            "coupling": coupling.generate(spec),
            "widen": widen.generate(spec)}


def covered_by(pool, question) -> list[str]:
    hit = set()
    for p in pool:
        h, need = compare.coverage(p, question)
        if h >= need:
            hit.add(p["arm"])
    return sorted(hit)


# ---------------------------------------------------------------------------

def check_known_null(spec) -> None:
    section("1  known null: a question no probe answers, in the probes' words")

    all_probes = [p for ps in arms(spec).values() for p in ps]
    nulls = (
        "does the organism report the environment coupling latency "
        "allocation performance",
        "measure the instrument organism environment consequence variance",
        "what colour is the apparatus",
    )
    print("  A word-salad question drawn from the probes' own vocabulary")
    print("  should NOT be marked covered. If it is, the classifier is")
    print("  measuring vocabulary rather than reach.\n")
    fired = 0
    for q in nulls:
        hit = covered_by(all_probes, q)
        fired += bool(hit)
        print("  %-8s %s" % ("COVERED" if hit else "silent", q[:52]))
    print()
    print("  %d of %d nulls fired." % (fired, len(nulls)))
    print()
    print("  The threshold does real work -- two of three are refused, and")
    print("  the flat-vocabulary one is refused outright. But one clears it:")
    print("  'measure the instrument organism environment consequence")
    print("  variance' shares five of its six stems with the coupling arm's")
    print("  autocorrelation probe, whose protocol reads 'measure the")
    print("  environment's own variance structure ...'. Five of six is a")
    print("  real overlap and the question is still nonsense.")
    print()
    print("  So the classifier's failure mode is specific: a null built from")
    print("  ONE probe's vocabulary beats it, while a null built from the")
    print("  whole pool's does not. That is a bound on what COVERED means,")
    print("  not a reason to discard it -- but it is why PARTIAL's 'not")
    print("  resolved here' caution belongs on COVERED as well.")


def check_known_signal(spec) -> None:
    section("2  known signal: a question a named probe was written for")

    measuring = [p for a, ps in arms(spec).items() if a != "widen" for p in ps]
    cases = (
        ("what does the environment's own variance structure look like",
         "coupling", "the autocorrelation probe is written for this"),
        ("how tightly could the loop close, given the latency actually "
         "available", "coupling", "the latency probe is written for this"),
    )
    print("  A question a probe was explicitly designed to reach should be")
    print("  marked covered by that arm.\n")
    missed = 0
    for q, want, why in cases:
        hit = covered_by(measuring, q)
        ok = want in hit
        missed += not ok
        print("  %-8s %-46s %s" % ("ok" if ok else "MISSED", q[:46], why))
    print()
    print("  PASSES." if not missed else "  FAILS: a designed-for question was missed.")


def check_arm_pooling(spec) -> None:
    section("3  arm pooling: does a non-measuring arm suppress the residual?")

    a = arms(spec)
    all_probes = [p for ps in a.values() for p in ps]
    measuring = [p for name, ps in a.items() if name != "widen" for p in ps]
    questions = spec["open_questions"]

    with_widen = [q for q in questions if not covered_by(all_probes, q)]
    without = [q for q in questions if not covered_by(measuring, q)]

    print("  compare.py pools every arm into `allp` and runs coverage over")
    print("  all of it. But its own output says of the widen arm:\n")
    print("      [widen] -- options, not quantities.\n")
    print("  An option is not a measurement. Counting it toward coverage")
    print("  lets a proposal to RENAME a question mark that question as")
    print("  REACHED.\n")
    print("  residual, widen included (compare.py as delivered) : %d of %d"
          % (len(with_widen), len(questions)))
    print("  residual, measuring arms only                      : %d of %d"
          % (len(without), len(questions)))
    print()
    for q in without:
        print("    [NO ARM] %s" % q)
    print()
    if len(without) > len(with_widen):
        print("  FAILS. %d open question(s) are hidden from the growth edge"
              % (len(without) - len(with_widen)))
        print("  by an arm that proposes no measurement.")
    else:
        print("  PASSES -- pooling changes nothing on this spec.")

    print()
    print("  HONEST NOTE. widen.py is reconstructed here, not delivered, and")
    print("  the version in this folder emits one probe per open question")
    print("  carrying that question's text -- so its overlap is total and")
    print("  this effect is maximal. A widen arm that did not echo the")
    print("  question would contribute less false coverage.")
    print()
    print("  The structural point survives either way: an arm that proposes")
    print("  no quantity should not appear in the denominator of a cell")
    print("  about which quantities are missing. The fix is one line in")
    print("  compare.py -- build the coverage pool from the measuring arms,")
    print("  and report widen separately as it already is elsewhere.")


def main() -> None:
    with open(SPEC) as fh:
        spec = json.load(fh)

    print()
    print("NULL-TESTING THE RESIDUAL CLASSIFIER")
    print("subject: compare.py coverage(), on %s"
          % os.path.basename(SPEC))

    check_known_null(spec)
    check_known_signal(spec)
    check_arm_pooling(spec)

    section("READING")
    print("""
  The tokeniser is roughly as good as a tokeniser can be here, and its
  limits are specific rather than general. It catches the questions its
  probes were written for, refuses a null built from the whole pool's
  vocabulary, and is beaten by a null built from ONE probe's -- five of six
  stems shared with the autocorrelation probe is a real overlap attached to
  a meaningless question. compare.py is already candid about the middle
  band: PARTIAL is explicitly "not resolved here". That caution belongs on
  COVERED too, because COVERED is the verdict that removes a question from
  the list.

  What fails is upstream of it. The coverage pool includes an arm that
  emits no quantities, so a proposal to rename a question can mark that
  question reached -- and RESIDUAL, the cell the docstring calls the
  product, is the one cell where a false COVERED costs the most. A missing
  measurement that never appears on the growth edge is not on any list at
  all.

  Neither result is about the domain. Both are about whether the harness
  can see its own gaps, which is the only thing a fork like this is for.
""")


if __name__ == "__main__":
    main()
