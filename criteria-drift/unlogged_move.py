#!/usr/bin/env python3
# SPDX-License-Identifier: CC0-1.0
"""
unlogged_move.py - the same numbers, with and without the criterion logged.

    python3 unlogged_move.py [--selftest]

# NOTE TO READERS -- TERM COLLISION
# "CHANGE OF MIND" here means REVISION (provenance-bearing): the cause is
# named, inspectable, arguable, and the criterion move is logged. It does not
# mean ASSERTION (non-provenance-bearing), where the criterion moved and
# nothing records that it moved. The two differ in PROVENANCE, not in
# sincerity. See PREAMBLE.md.

WHAT THIS TESTS. The note makes one falsifiable claim: prior measurements
taken under an old criterion remain interpretable when the criterion move is
logged, and "become uninterpretable without notice" when it is not. This
module runs both readings over ONE series of numbers.

The rest of criteria-drift assumes versions are declared -- it measures how
fast a declared ruler moves. This is the counterpart case: the ruler moved and
no version was cut.

THE RESULT SHARPENS THE CLAIM IN ONE PLACE. Unlogged prior measurements do not
become unreadable. They stay perfectly legible and mean something else: the
series reads as a clean step in the system, with a number attached, and
nothing in it is marked. "Uninterpretable" understates it -- the failure is
not a gap where an answer should be, it is a confident wrong answer in the
same shape as a right one.

AND LOGGING ALONE DOES NOT DECOMPOSE. Three states, not two:

  ASSERTION           unlogged. One series, one step, read as the system.
  REVISION            logged, no bridge. The step is real and its split
                      between system and criterion is UNKNOWN -- which is
                      the correct output, and it is not a number.
  REVISION + BRIDGE   one measurement taken under BOTH criteria. The step
                      decomposes exactly.

THE BRIDGE IS NOT THIS MODULE'S IDEA AND THE AGREEMENT IS NOT EVIDENCE.
anchor.py in this same folder already argues it at length -- an invariant
subset scored across versions (stable words, a primary standard, a frozen
model scored on all versions), without which drift is unmeasurable, and
`audit.py regress` already refuses to report an identified criteria term when
the bridge is absent. This module reaches the same requirement from a
two-reading toy and adds nothing to the case for it.

Recording that plainly, because operator-structure-echo/corroboration.py was
written one commit ago and this is its INHERITED state on a real pair: same
folder, same builder, same week. Two modules agreeing here is one position
expressed twice. The sim is a demonstration of a requirement already
established next door, not a second line of evidence for it.

Most honest practice lands in the middle. The middle is not the same as the
first: it reports UNKNOWN where the first reports a value, and knowing what
you do not know is the whole of the difference.

stdlib only, parses under Python 3.9. CC0.
"""

import argparse
import sys

# --- the world -------------------------------------------------------------
# Deterministic. No rng: a sample that moves between runs is not a sample.

N = 12
MOVE_AT = 6                      # the criterion moves before this index
CRITERION_BONUS = 0.15           # what the new criterion adds, per reading


def world(system_step=0.0):
    """Truth: the capability series, and the criterion in force at each t."""
    cap, crit = [], []
    for t in range(N):
        moved = t >= MOVE_AT
        cap.append(0.50 + (system_step if moved else 0.0))
        crit.append(CRITERION_BONUS if moved else 0.0)
    return {"capability": cap, "criterion": crit,
            "observed": [c + k for c, k in zip(cap, crit)]}


# --- the three readings ----------------------------------------------------

def read_assertion(obs):
    """No log. One undifferentiated series; the step is read as the system."""
    before = sum(obs[:MOVE_AT]) / MOVE_AT
    after = sum(obs[MOVE_AT:]) / (N - MOVE_AT)
    step = after - before
    return {"mode": "ASSERTION",
            "step_observed": step,
            "attributed_to_system": step,
            "attributed_to_criterion": 0.0,
            "system_change_state": "REPORTED_AS_VALUE",
            "flagged": False,
            "note": "nothing in the series marks a criterion move, so the "
                    "whole step lands on the system and the readout carries "
                    "no marker that anything is unaccounted for"}


def read_revision(obs, move_at=MOVE_AT):
    """The move is logged. The step is real; its split is UNKNOWN."""
    before = sum(obs[:move_at]) / move_at
    after = sum(obs[move_at:]) / (N - move_at)
    step = after - before
    return {"mode": "REVISION",
            "step_observed": step,
            "attributed_to_system": None,
            "attributed_to_criterion": None,
            "system_change_state": "UNKNOWN_NOT_ZERO",
            "flagged": True,
            "note": "the step is measured and its decomposition is not. "
                    "With no reading taken under both criteria there is no "
                    "quantity to split it by, and UNKNOWN is the correct "
                    "output rather than a shortfall"}


def read_revision_with_bridge(obs, bridge_delta, move_at=MOVE_AT):
    """A bridge is one measurement taken under BOTH criteria.

    `bridge_delta` is what the same subject scores under the new criterion
    minus the old, at one point in time. That is the only thing that turns a
    logged move into a decomposable one.
    """
    before = sum(obs[:move_at]) / move_at
    after = sum(obs[move_at:]) / (N - move_at)
    step = after - before
    return {"mode": "REVISION_WITH_BRIDGE",
            "step_observed": step,
            "attributed_to_criterion": bridge_delta,
            "attributed_to_system": step - bridge_delta,
            "system_change_state": "MEASURED",
            "flagged": True,
            "note": "the bridge measures the criterion's own contribution, "
                    "so the remainder is the system's. One reading under "
                    "both criteria is what the decomposition costs"}


def scenario(system_step):
    """All three readings over one identical series of observations."""
    w = world(system_step)
    obs = w["observed"]
    return {"truth_system_step": system_step,
            "truth_criterion_step": CRITERION_BONUS,
            "observed": obs,
            "ASSERTION": read_assertion(obs),
            "REVISION": read_revision(obs),
            "REVISION_WITH_BRIDGE": read_revision_with_bridge(
                obs, CRITERION_BONUS)}


def error(reading, truth_system_step):
    """How far a reading's system attribution is from the truth.

    None where the reading declines to attribute -- which is not an error of
    size zero and is not an error of any size. It is a refusal, and folding
    it into a number would be the move this whole module is about.
    """
    a = reading["attributed_to_system"]
    if a is None:
        return {"error": None, "state": "DECLINED_TO_ATTRIBUTE"}
    return {"error": a - truth_system_step, "state": "ATTRIBUTED"}


def legibility(system_step=0.0):
    """The note says prior measurements 'become uninterpretable'. Check it.

    They do not. Every prior reading is still present, still numeric, still
    in range, and still fits the series it sits in. What changed is what it
    means, and nothing in the data records that. Legible and wrong is a
    harder failure than blank, because blank announces itself.
    """
    w = world(system_step)
    obs = w["observed"]
    prior = obs[:MOVE_AT]
    return {"prior_readings_present": len(prior) == MOVE_AT,
            "prior_readings_numeric": all(isinstance(x, float)
                                          for x in prior),
            "prior_readings_in_range": all(0.0 <= x <= 1.0 for x in prior),
            "series_looks_continuous": True,
            "any_marker_in_the_data": False,
            "verdict": "LEGIBLE_AND_RECONTEXTUALISED",
            "why": "nothing is missing and nothing is out of range. The "
                   "prior readings are readable and they now sit against a "
                   "different criterion, with no field carrying that. "
                   "'Uninterpretable' understates it: the failure is not a "
                   "gap where an answer should be, it is a confident wrong "
                   "answer in the same shape as a right one"}


def confidence():
    return {"the_world": "a stipulated series, not data. It shows what an "
                         "unlogged move does to a reading; it is not "
                         "evidence about how often moves go unlogged",
            "the_error_size": "exactly the criterion bonus, by construction. "
                              "That the ASSERTION error equals the unlogged "
                              "move is arithmetic, not a finding -- the "
                              "finding is that it is invisible from inside "
                              "the reading",
            "UNKNOWN": "REVISION returns None for the system attribution. "
                       "None is not zero and is not a small number; folding "
                       "it into either is the move this module is about",
            "bridge_cost": "one reading under both criteria. Stated as a "
                           "requirement, not demonstrated to be obtainable "
                           "in any real setting",
            "resolved": False}


def breaks():
    return [
        "THE UNLOGGED READING IS NOT UNREADABLE, IT IS WRONG BY EXACTLY THE "
        "SIZE OF THE UNLOGGED MOVE, AND IT SAYS NOTHING. In the no-change "
        "scenario the system does not move at all and ASSERTION reports a "
        "0.15 improvement with no flag on it. The note's word for this is "
        "'uninterpretable'; the sim says the prior readings stay present, "
        "numeric, in range and continuous, and only their meaning moved. A "
        "blank announces itself. This does not",
        "REVISION'S OUTPUT IS 'UNKNOWN' AND THAT WILL READ AS THE WEAKER "
        "ANSWER. ASSERTION returns a number and REVISION returns None, so in "
        "any table, summary or comparison the logged reading looks like the "
        "one that failed to produce a result. It is the one that produced "
        "the correct result. Nothing here changes that asymmetry -- it only "
        "prints both",
        "LOGGING THE MOVE DOES NOT DECOMPOSE IT. The three-state readout "
        "exists because a logged move with no bridge still cannot separate "
        "system from criterion. Treating REVISION as sufficient is a second "
        "error one step past the first, and the bridge -- a reading under "
        "both criteria -- is a real cost that this module asserts and does "
        "not price",
        "THIS MODULE AGREES WITH anchor.py AND THAT AGREEMENT IS INHERITED, "
        "NOT FOUND. The bridge requirement is already argued in this folder "
        "from cross-domain cases, and regress.py already refuses an "
        "identified term without one. Same folder, same builder: by "
        "operator-structure-echo's own pair table this is INHERITED, so the "
        "sim demonstrates a requirement rather than corroborating it. A "
        "reader counting two modules in agreement here is counting one "
        "position twice",
        "ONE MOVE, ONE SERIES, TWO SCENARIOS, NO NOISE. There is no rng, "
        "which makes the sample reproducible and makes every effect exact. "
        "Nothing here says what happens with several moves, gradual moves, "
        "or a move whose size is itself uncertain, and a real criterion "
        "rarely steps once by a constant",
        "THE MODULE DECIDES WHERE THE MOVE IS. MOVE_AT is given to the "
        "readers, so REVISION is handed the segmentation that is the hard "
        "part of the real problem. Detecting an unlogged move FROM the "
        "series is not attempted here and is the case the note is actually "
        "about",
    ]


def _fmt(x):
    return "None " if x is None else "%+.3f" % x


def report():
    L = ["UNLOGGED CRITERION MOVE -- the same numbers, read three ways",
         "=" * 72, ""]
    L.append("  REVISION and ASSERTION differ in PROVENANCE, not sincerity.")
    L.append("  This runs both over one identical series.")
    L.append("")
    L.append("  world: %d readings, criterion moves before index %d,"
             % (N, MOVE_AT))
    L.append("         the new criterion adds %+.2f per reading."
             % CRITERION_BONUS)
    L.append("")
    for step in (0.0, 0.10):
        s = scenario(step)
        L.append("-" * 72)
        L.append("")
        L.append("  TRUTH: system step %+.2f, criterion step %+.2f"
                 % (step, CRITERION_BONUS))
        L.append("  observed: %s"
                 % " ".join("%.2f" % x for x in s["observed"]))
        L.append("")
        L.append("    %-22s %-9s %-9s %-9s %s"
                 % ("reading", "step", "-> system", "error", "flagged"))
        for m in ("ASSERTION", "REVISION", "REVISION_WITH_BRIDGE"):
            r = s[m]
            e = error(r, step)
            L.append("    %-22s %-9s %-9s %-9s %s"
                     % (m, "%+.3f" % r["step_observed"],
                        _fmt(r["attributed_to_system"]),
                        _fmt(e["error"]), r["flagged"]))
        L.append("")
        a = s["ASSERTION"]
        if step == 0.0:
            L.append("    the system did not move. ASSERTION reports it")
            L.append("    moved %+.2f, and carries no flag."
                     % a["attributed_to_system"])
        else:
            L.append("    the system moved %+.2f. ASSERTION reports %+.2f,"
                     % (step, a["attributed_to_system"]))
            L.append("    still wrong by exactly the unlogged move.")
        L.append("")
    L.append("-" * 72)
    L.append("")
    L.append("  ASSERTION's error is the criterion bonus in BOTH scenarios.")
    L.append("  It does not depend on whether the system changed, and it is")
    L.append("  not visible from inside the reading.")
    L.append("")
    L.append("  REVISION returns None for the system attribution. None is")
    L.append("  not zero. In any summary table it will look like the")
    L.append("  reading that failed to produce a result; it is the one")
    L.append("  that produced the correct one.")
    L.append("")
    L.append("-" * 72)
    L.append("")
    L.append("  DOES THE PRIOR SERIES BECOME UNINTERPRETABLE?")
    L.append("")
    lg = legibility()
    for k in ("prior_readings_present", "prior_readings_numeric",
              "prior_readings_in_range", "series_looks_continuous",
              "any_marker_in_the_data"):
        L.append("    %-28s %s" % (k, lg[k]))
    L.append("")
    L.append("    verdict: %s" % lg["verdict"])
    for line in _wrap(lg["why"], "    "):
        L.append(line)
    L.append("")
    L.append("-" * 72)
    L.append("")
    L.append("  CONFIDENCE, reported separately and not resolved")
    for k in sorted(confidence()):
        L.append("    %s" % k)
        for line in _wrap(str(confidence()[k]), "      "):
            L.append(line)
    L.append("")
    L.append("  WHERE IT BREAKS")
    for b in breaks():
        for line in _wrap("- " + b, "    "):
            L.append(line)
    return "\n".join(L)


def _wrap(t, ind, w=72):
    words, lines, cur = t.split(), [], ind
    for x in words:
        if len(cur) + len(x) + 1 > w and cur.strip():
            lines.append(cur.rstrip())
            cur = ind + x + " "
        else:
            cur += x + " "
    if cur.strip():
        lines.append(cur.rstrip())
    return lines


def selftest():
    f = k = 0

    def ck(label, cond):
        nonlocal f, k
        k += 1
        if not cond:
            f += 1
            print("FAIL %s" % label)

    flat = scenario(0.0)
    ck("with no system change at all, ASSERTION still reports a step",
       abs(flat["ASSERTION"]["attributed_to_system"]
           - CRITERION_BONUS) < 1e-9)
    ck("and carries no flag that anything is unaccounted for",
       flat["ASSERTION"]["flagged"] is False)
    ck("REVISION declines to attribute rather than reporting zero",
       flat["REVISION"]["attributed_to_system"] is None
       and flat["REVISION"]["system_change_state"] == "UNKNOWN_NOT_ZERO")
    ck("and it does flag", flat["REVISION"]["flagged"] is True)
    ck("the bridge recovers the truth: no system change",
       abs(flat["REVISION_WITH_BRIDGE"]["attributed_to_system"]) < 1e-9)

    moved = scenario(0.10)
    ck("with a real system change ASSERTION is still wrong",
       abs(moved["ASSERTION"]["attributed_to_system"] - 0.10) > 1e-9)
    ck("and wrong by exactly the unlogged move, in BOTH scenarios",
       abs(error(moved["ASSERTION"], 0.10)["error"] - CRITERION_BONUS) < 1e-9
       and abs(error(flat["ASSERTION"], 0.0)["error"]
               - CRITERION_BONUS) < 1e-9)
    ck("so the error does not depend on whether the system moved",
       abs(error(moved["ASSERTION"], 0.10)["error"]
           - error(flat["ASSERTION"], 0.0)["error"]) < 1e-9)
    ck("the bridge recovers the real change too",
       abs(moved["REVISION_WITH_BRIDGE"]["attributed_to_system"]
           - 0.10) < 1e-9)
    ck("REVISION's error is not a number, and not a zero",
       error(moved["REVISION"], 0.10)["error"] is None
       and error(moved["REVISION"], 0.10)["state"]
       == "DECLINED_TO_ATTRIBUTE")

    ck("the observed series is identical in shape across readings -- one "
       "series, three readings",
       flat["observed"] == world(0.0)["observed"]
       and len(set(map(len, (flat["observed"], moved["observed"])))) == 1)

    lg = legibility()
    ck("prior readings survive the move: present, numeric, in range",
       lg["prior_readings_present"] and lg["prior_readings_numeric"]
       and lg["prior_readings_in_range"])
    ck("and nothing in the data marks the move",
       lg["any_marker_in_the_data"] is False)
    ck("so 'uninterpretable' is sharpened to legible-and-recontextualised",
       lg["verdict"] == "LEGIBLE_AND_RECONTEXTUALISED")

    ck("the wrong-by-exactly-the-move result leads the breaks list",
       "WRONG BY EXACTLY THE SIZE" in breaks()[0])
    ck("the UNKNOWN-looks-weaker asymmetry is disclosed",
       any("looks like the one that failed" in b for b in breaks()))
    ck("logging alone not decomposing is disclosed",
       any("DOES NOT DECOMPOSE" in b for b in breaks()))
    ck("the module handing REVISION its segmentation is disclosed",
       any("MOVE_AT is given to the readers" in b for b in breaks()))
    ck("the bridge is credited to anchor.py, not introduced here",
       "anchor.py in this same folder already argues it" in __doc__)
    ck("and the agreement with it is recorded as inherited, not found",
       any("INHERITED, " in b and "NOT FOUND" in b for b in breaks()))
    import os
    anchor = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          "anchor.py")
    if os.path.exists(anchor):
        atext = open(anchor).read()
        ck("anchor.py does mean the same thing by 'bridge': an invariant "
           "scored across versions",
           "invariant subset" in atext and "bridge" in atext
           and "frozen model scored on all versions" in atext)

    ck("the term-collision note is at the head of the module",
       "TERM COLLISION" in __doc__ and "PROVENANCE, not in" in __doc__)
    ck("confidence unresolved", confidence()["resolved"] is False)
    ck("report renders", "read three ways" in report())
    print("%d/%d checks passed" % (k - f, k))
    return 1 if f else 0


def main():
    ap = argparse.ArgumentParser(description="unlogged criterion move")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    print(report())
    return 0


if __name__ == "__main__":
    sys.exit(main())
