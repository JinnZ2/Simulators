#!/usr/bin/env python3
# SPDX-License-Identifier: CC0-1.0
"""
diff.py - CARRIED / DROPPED / ADDED, and a null test on the matcher.

    python3 diff.py [--selftest]

DROPPED is the measurement. ADDED is not a defect -- it is where the
downstream model contributed -- but it must be visible so it is not later
mistaken for operator intent.

THE MATCHER IS THE INSTRUMENT AND IT IS TESTED BEFORE IT IS TRUSTED. Deciding
whether a ledger line is "present in the delivered code" is a text-matching
judgement, and the same problem has already produced two opposite failures in
this repo -- measurement-fork's classifier over-matched on one corpus and
under-matched on another, with no single threshold fixing both. So `match()`
is graded on known-carried and known-dropped fixtures and reports FP, TP and a
null-harness grade. A DROPPED count from an ungraded matcher is not a
measurement.

CARRIED IS SPLIT. A [K?] entry that matches is CARRIED_UNCONFIRMED, counted
apart, because the voice-layer failure mode is exactly a ledger holding a
mangled transcription while the diff reads CARRIED. That is the one failure
mode nothing else catches, and the split is the only handling available from
this side: it cannot detect the mangling, but it refuses to count it as
evidence.

A NEGATED ENTRY IS NOT SCORED, BECAUSE THE MATCHER READS IT BACKWARDS. The
first real ledger written against this module carried the line "remove unused
rng and statistics import", and it matched the delivered S4 code at share
1.00 -- the matcher's maximum -- while `import statistics` is absent from that
file. The words survive in the prose describing the removal. For an entry
asking that something be taken OUT, presence of its stems is evidence the item
was DROPPED, so the matcher does not merely mis-score it, it inverts it, and
it does so at full confidence. `match()` therefore returns `matched=None` with
state NEGATED, and `diff()` routes those entries to UNSCORABLE_NEGATED, out of
both counts and out of the rate denominator. None is not False: "the
instrument cannot read this entry" is a different state from "the item is
absent from the code". The detector is graded on its own fixtures, because a
negation detector that never fires would restore the inversion silently.

stdlib only, parses under Python 3.9. CC0.
"""

import argparse
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import provenance as P                                          # noqa: E402

STOP = set("a an the of to in on for and or is are be was were with by that "
           "this it its as at from not no than then so if which what when "
           "each per over under into out up down do does did has have had "
           "must may can will would should any all one two three".split())

MIN_STEM = 4
MATCH_THRESHOLD = 0.55

# Cues that an entry asks for an ABSENCE. Presence of such an entry's stems in
# the code is evidence AGAINST it having been carried, so the share is read
# backwards and the entry is refused rather than scored.
NEGATION_CUES = ("remove", "removes", "removed", "removal", "delete",
                 "deleted", "drop the", "dropped the", "strip", "stripped",
                 "eliminate", "eliminated", "without", "no longer",
                 "should not", "must not", "never", "instead of")


def negated(entry_text):
    """True if the entry asks for something to be absent."""
    t = " " + entry_text.lower() + " "
    return any(c in t for c in NEGATION_CUES)


def stems(text):
    words = re.findall(r"[a-z]+", text.lower())
    return set(w[:6] for w in words if len(w) >= MIN_STEM and w not in STOP)


def match(entry_text, code_text, threshold=MATCH_THRESHOLD):
    """Share of the entry's distinctive stems present in the code.

    `matched` is None -- not False -- when the entry cannot be scored. None
    means the instrument could not read it; False means it read it and the
    item is absent.
    """
    a = stems(entry_text)
    if not a:
        return {"share": None, "matched": None, "n_stems": 0,
                "state": "NO_STEMS"}
    if negated(entry_text):
        b = stems(code_text)
        return {"share": len(a & b) / len(a), "matched": None,
                "n_stems": len(a), "state": "NEGATED",
                "why": "the entry asks for an absence, so a high share is "
                       "evidence the item was NOT carried. The matcher reads "
                       "this backwards and is refused rather than inverted"}
    b = stems(code_text)
    share = len(a & b) / len(a)
    return {"share": share, "matched": share >= threshold,
            "n_stems": len(a), "state": "OK"}


def diff(ledger, code_text, added_items=()):
    """Three counts, with CARRIED split by confirmation state."""
    if not ledger.sealed:
        raise P.SealError(
            "the ledger is not sealed. A diff against an unsealed ledger "
            "cannot distinguish 'written before the spec' from 'extracted "
            "after the code', which is the whole ordering rule")
    carried, dropped, carried_unconf, dropped_unconf = [], [], [], []
    unscorable = []
    for e in ledger.entries:
        if e["tag"] not in P.GROUND_TRUTH + P.GROUND_TRUTH_UNCONFIRMED:
            continue
        m = match(e["text"], code_text)
        confirmed = e["tag"] in P.GROUND_TRUTH
        if m["matched"] is None:
            unscorable.append(e["text"])
        elif m["matched"]:
            (carried if confirmed else carried_unconf).append(e["text"])
        else:
            (dropped if confirmed else dropped_unconf).append(e["text"])
    return {
        "CARRIED": carried,
        "CARRIED_UNCONFIRMED": carried_unconf,
        "DROPPED": dropped,
        "DROPPED_UNCONFIRMED": dropped_unconf,
        "UNSCORABLE_NEGATED": unscorable,
        "ADDED": list(added_items),
        "n_ground_truth": len(carried) + len(dropped),
        "drop_rate": (len(dropped) / (len(carried) + len(dropped)))
        if (carried or dropped) else None,
        "rate_reportable": (len(carried) + len(dropped)) >= 10,
        "why_rate_may_be_none": "the drop rate is over CONFIRMED [K] entries "
                                "only. With none confirmed there is no "
                                "denominator, and the spec's own note "
                                "applies: the first several runs ARE the "
                                "baseline",
        "why_unscorable": "an entry asking for an absence is read backwards "
                          "by a presence matcher, at full confidence. It is "
                          "refused rather than scored, and it is out of the "
                          "rate denominator as well as out of both counts",
    }


# --- the matcher, graded ---------------------------------------------------

CODE_FIXTURE = """
def doe_selection(antler_size, sparring_competence, proximity, familiarity):
    # partner selection by the doe, three arms
    return weighted_choice(antler_size, proximity, familiarity)

def novelty(year, prior_years_sparred, floor):
    # annual regrowth with different geometry; floor is the parameter
    return annual_delta(year) * (floor + (1 - floor) * 0.55 ** prior)
"""

KNOWN_CARRIED = [
    "doe performs partner selection",
    "novelty has a floor set by the annual delta",
    "three arms for doe selection: null, size, other",
    "antler geometry changes each year",
]

KNOWN_DROPPED = [
    "tenure obligation consumes hours in the money economy",
    "mortality-weighted sampling dominates the inferred model",
    "the assessor scores contribution from the written record",
    "wage runs against metabolic expenditure",
]


def grade_matcher(threshold=MATCH_THRESHOLD):
    tp = sum(1 for t in KNOWN_CARRIED
             if match(t, CODE_FIXTURE, threshold)["matched"])
    fp = sum(1 for t in KNOWN_DROPPED
             if match(t, CODE_FIXTURE, threshold)["matched"])
    tpr = tp / len(KNOWN_CARRIED)
    fpr = fp / len(KNOWN_DROPPED)
    if tpr == 0.0 and fpr == 0.0:
        grade = "CONSTANT_SILENT"
    elif tpr == 1.0 and fpr == 1.0:
        grade = "CONSTANT_FIRES"
    elif tpr - fpr < 0.5:
        grade = "NO_DISCRIMINATION"
    else:
        grade = "OK"
    return {"threshold": threshold, "true_carried_rate": tpr,
            "false_carried_rate": fpr, "grade": grade,
            "n_signal": len(KNOWN_CARRIED), "n_null": len(KNOWN_DROPPED)}


def threshold_sweep(ts=(0.2, 0.35, 0.5, 0.55, 0.7, 0.85)):
    return [grade_matcher(t) for t in ts]


# --- the negation detector, graded -----------------------------------------
# A detector that never fires restores the inversion silently, so it is null
# tested the same way the matcher is. The first entry below is the real one:
# it matched the delivered S4 code at share 1.00 while the import it asks to
# be removed is absent from that file.

KNOWN_NEGATED = [
    "remove unused rng and statistics import",
    "the rank_prospect dict should not be hardcoded",
    "run without the mortality weighting",
    "novelty must not decay to zero",
]

KNOWN_POSITIVE = [
    "the doe performs partner selection",
    "novelty has a floor set by the annual delta",
    "engagement rate proportional to expected doe access",
    "antler geometry changes each year",
]


def grade_negation():
    tp = sum(1 for t in KNOWN_NEGATED if negated(t))
    fp = sum(1 for t in KNOWN_POSITIVE if negated(t))
    tpr, fpr = tp / len(KNOWN_NEGATED), fp / len(KNOWN_POSITIVE)
    if tpr == 0.0 and fpr == 0.0:
        grade = "CONSTANT_SILENT"
    elif tpr == 1.0 and fpr == 1.0:
        grade = "CONSTANT_FIRES"
    elif tpr - fpr < 0.5:
        grade = "NO_DISCRIMINATION"
    else:
        grade = "OK"
    return {"true_negated_rate": tpr, "false_negated_rate": fpr,
            "grade": grade, "n_signal": len(KNOWN_NEGATED),
            "n_null": len(KNOWN_POSITIVE)}


def confidence():
    return {"matcher": "graded on 4 known-carried and 4 known-dropped "
                       "fixtures, which is 8 items and not a corpus",
            "DROPPED_count": "only as good as the matcher grade printed "
                             "beside it",
            "CARRIED_UNCONFIRMED": "not evidence. A mangled ledger entry "
                                   "matching mangled code would land here "
                                   "and the diff cannot tell",
            "drop_rate": "UNMEASURED. first runs are the baseline",
            "negation_detector": "a cue list, graded on 4 and 4. It fires on "
                                 "the surface form of a negation and any "
                                 "paraphrase steps around it, the same limit "
                                 "every keyword screen in this repo has",
            "resolved": False}


def breaks():
    return [
        "THE MATCHER CANNOT SEE THE FOURTH FAILURE MODE AND NOTHING HERE "
        "CAN. If a [K] item was transcribed wrong, the ledger holds the "
        "wrong version, the code implements the wrong version, and the diff "
        "reads CARRIED. Splitting CARRIED by confirmation state does not "
        "detect it -- it only refuses to count an unconfirmed match as "
        "evidence, which is the most this side of the channel can do",
        "eight fixtures is not a corpus. The grade says the matcher "
        "discriminates on eight hand-written strings, and measurement-fork "
        "already showed a stem matcher failing in opposite directions on "
        "two different real corpora",
        "the threshold is a single number over a share of stems, and the "
        "sweep shows the grade moving with it. Nothing here establishes "
        "0.55 beyond it working on these eight",
        "THE NEGATION DETECTOR IS A CUE LIST AND AN ENTRY CAN BE PHRASED "
        "PAST IT. 'the module runs on two arms rather than a constant' asks "
        "for a removal and contains no cue, so it is scored as a positive "
        "entry and the inversion returns. What the detector buys is that the "
        "cases it does catch are refused instead of counted backwards; it "
        "does not establish that the unrefused entries are all positive",
        "ADDED is supplied by the caller, not detected. Nothing scans "
        "delivered code for items with no ledger entry, so the [X] column "
        "is only as complete as whoever filled it in -- and attribution "
        "creep is precisely the case where they did not",
    ]


def report():
    L = ["HANDOFF DIFF -- carried, dropped, added", "=" * 72, ""]
    L.append("  THE MATCHER, GRADED BEFORE IT IS USED")
    L.append("")
    L.append("  %-12s %-16s %-16s %s"
             % ("threshold", "true carried", "false carried", "grade"))
    for g in threshold_sweep():
        L.append("  %-12.2f %-16.2f %-16.2f %s"
                 % (g["threshold"], g["true_carried_rate"],
                    g["false_carried_rate"], g["grade"]))
    L.append("")
    g = grade_matcher()
    L.append("  shipped threshold %.2f -> %s" % (g["threshold"], g["grade"]))
    L.append("")
    L.append("  A DROPPED count from an ungraded matcher is not a")
    L.append("  measurement. The grade prints beside the count, always.")
    L.append("")
    L.append("-" * 72)
    L.append("")
    L.append("  CARRIED IS SPLIT BY CONFIRMATION STATE")
    L.append("")
    L.append("    CARRIED              [K] entry found in the code")
    L.append("    CARRIED_UNCONFIRMED  [K?] entry found in the code")
    L.append("")
    L.append("    The second is not evidence. The voice-layer failure mode")
    L.append("    is a ledger holding a mangled transcription while the")
    L.append("    diff reads CARRIED, and no matcher can see that. The")
    L.append("    split does not detect it; it refuses to count it.")
    L.append("")
    L.append("-" * 72)
    L.append("")
    L.append("  A NEGATED ENTRY IS REFUSED, NOT SCORED")
    L.append("")
    n = grade_negation()
    L.append("    true negated %.2f   false negated %.2f   %s"
             % (n["true_negated_rate"], n["false_negated_rate"], n["grade"]))
    L.append("")
    real = "remove unused rng and statistics import"
    m = match(real, "import statistics was removed; rng is unused here")
    L.append("    the real case that produced this:")
    L.append("      %r" % real)
    L.append("      share %.2f   matched %s   state %s"
             % (m["share"], m["matched"], m["state"]))
    L.append("")
    L.append("    Maximum share, and the import it asks to remove is")
    L.append("    absent. For an entry asking for an absence, presence of")
    L.append("    its stems is evidence AGAINST it. matched is None -- the")
    L.append("    instrument could not read the entry, which is a")
    L.append("    different state from reading it and finding nothing.")
    return "\n".join(L)


def selftest():
    f = k = 0

    def ck(label, cond):
        nonlocal f, k
        k += 1
        if not cond:
            f += 1
            print("FAIL %s" % label)

    g = grade_matcher()
    ck("the matcher is graded before use and grades OK on the fixtures",
       g["grade"] == "OK")
    ck("it is not CONSTANT_FIRES", g["false_carried_rate"] < 1.0)
    ck("it is not CONSTANT_SILENT", g["true_carried_rate"] > 0.0)
    sw = threshold_sweep()
    ck("the grade moves with the threshold, so 0.55 is a choice",
       len({r["grade"] for r in sw}) > 1)

    lg = P.Ledger("wo")
    lg.add("doe performs partner selection", "K")
    lg.add("tenure obligation consumes hours", "K")
    lg.add("novelty has a floor set by the annual delta", "K?")
    try:
        diff(lg, CODE_FIXTURE)
        ok = False
    except P.SealError:
        ok = True
    ck("a diff against an unsealed ledger is refused", ok)

    lg.seal()
    d = diff(lg, CODE_FIXTURE, added_items=["GEOMETRY_DELTA term"])
    ck("the carried [K] item lands in CARRIED",
       "doe performs partner selection" in d["CARRIED"])
    ck("the dropped [K] item lands in DROPPED",
       any("tenure" in x for x in d["DROPPED"]))
    ck("the matched [K?] item lands in CARRIED_UNCONFIRMED, not CARRIED",
       len(d["CARRIED_UNCONFIRMED"]) == 1 and len(d["CARRIED"]) == 1)
    ck("the drop rate is over confirmed entries only",
       d["n_ground_truth"] == 2 and abs(d["drop_rate"] - 0.5) < 1e-9)
    ck("and it is not reportable at this n, per the spec's baseline note",
       d["rate_reportable"] is False)
    ck("ADDED is carried through and is not empty here",
       d["ADDED"] == ["GEOMETRY_DELTA term"])

    empty = P.Ledger("e")
    empty.add("only unconfirmed", "K?")
    empty.seal()
    d2 = diff(empty, CODE_FIXTURE)
    ck("with no confirmed entries the drop rate is None, not zero",
       d2["drop_rate"] is None)

    ng = grade_negation()
    ck("the negation detector is graded and is not CONSTANT_SILENT",
       ng["grade"] == "OK" and ng["true_negated_rate"] > 0.0)
    ck("it does not fire on positive entries",
       ng["false_negated_rate"] == 0.0)
    real = "remove unused rng and statistics import"
    mr = match(real, "import statistics was removed; rng is unused here")
    ck("the real negated entry scores share 1.00 against code that does "
       "NOT contain the import -- the inversion, measured",
       abs(mr["share"] - 1.0) < 1e-9)
    ck("and it is refused rather than scored: matched is None, not False",
       mr["matched"] is None and mr["state"] == "NEGATED")
    neg = P.Ledger("n")
    neg.add("remove unused rng and statistics import", "K")
    neg.add("doe performs partner selection", "K")
    neg.seal()
    dn = diff(neg, CODE_FIXTURE)
    ck("a negated entry lands in UNSCORABLE_NEGATED",
       len(dn["UNSCORABLE_NEGATED"]) == 1)
    ck("and is out of the rate denominator as well as out of both counts",
       dn["n_ground_truth"] == 1)
    ck("an empty-stem entry is also None, not False",
       match("", CODE_FIXTURE)["matched"] is None)

    ck("the undetectable fourth failure mode leads the breaks list",
       "CANNOT SEE THE FOURTH FAILURE MODE" in breaks()[0])
    ck("ADDED being caller-supplied rather than detected is disclosed",
       any("supplied by the caller, not detected" in b for b in breaks()))
    ck("confidence unresolved", confidence()["resolved"] is False)
    ck("the cue list being steppable-around is disclosed",
       any("phrased past it" in b.lower() for b in breaks()))
    ck("report renders", "graded before it is used" in report().lower())
    ck("and the report shows the negated case",
       "REFUSED, NOT SCORED" in report())
    print("%d/%d checks passed" % (k - f, k))
    return 1 if f else 0


def main():
    ap = argparse.ArgumentParser(description="handoff diff")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    print(report())
    return 0


if __name__ == "__main__":
    sys.exit(main())
