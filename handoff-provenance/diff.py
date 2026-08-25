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

AND AN ENTRY THE LENGTH FLOOR GUTS IS NOT SCORED AT ALL. Content words under
MIN_STEM characters are invisible to the matcher, so an entry whose claim
rests on short words is scored on whatever long words happen to sit beside
it. The first reportable drop rate this module produced -- 0.09 over eleven
entries -- was one false DROPPED of exactly that kind: "[K~] is a tag, added
to the existing tag set" scored on `added` and `existing` while `tag` and
`set` fell under the floor. `coverage()` measures the loss and `match()`
refuses the entry when most of its content words go, because a share over the
minority that survived is not a reading of the entry. The rule was added
after that result, which is disclosed in `breaks()` rather than smoothed, and
it does not restore the words: an entry losing one content word of four is
still scored with that one unseen.

A [K~] ENTRY IS NOT SCORED EITHER, FOR A DIFFERENT REASON. Its English was
flagged lossy by the operator at the time of speaking, and the matcher reads
English stems. A non-match on such an entry is ambiguous between "absent from
the code" and "the English was wrong, so the stems miss code that does
implement the shape", and nothing here separates those. It lands in
UNSCORABLE_TRANSLATION -- but unlike a NEGATED entry it stays inside
n_stated, because it WAS said. Two denominators come out of that: n_stated,
the population the channel loses things from, and n_scorable, what the
matcher can be trusted on. The drop rate runs over the smaller one and the
gap between them is the translation layer's footprint.

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
import ast
import io
import os
import re
import sys
import tokenize

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


# Every module in this folder carries the same disclosure surface: a report,
# a selftest, and the breaks/confidence readouts. Those functions QUOTE ledger
# entries in order to display them, so leaving them in the matched text lets
# an entry match the code that prints it. They are stripped with the prose.
REPORTING_FUNCTIONS = ("report", "selftest", "breaks", "confidence", "main",
                       "_wrap")


def implementation_surface(source, drop_reporting=True):
    """Source with docstrings, comments and the disclosure surface removed.

    A ledger entry says what the code should DO. Matching it against a file's
    prose matches it against a DESCRIPTION of the code, and a docstring
    repeating the entry earns a CARRIED with nothing implemented. That is a
    false-CARRIED generator and it fires hardest exactly where the ledger and
    the code were written by the same party in the same pass.

    String literals in expressions are kept: a gloss table mapping SHIFT to
    "the station" IS the implementation of "SHIFT is data about the station".
    A docstring saying the same sentence is not. The line is between a value
    the program carries and prose about the program.

    This REDUCES the contamination; it does not remove it. A self-diff --
    ledger and code written by one party in one pass -- is not a measurement
    whatever surface it runs against, and the caller is told so.
    """
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return source
    drop = set()
    for node in ast.walk(tree):
        if (drop_reporting
                and isinstance(node, ast.FunctionDef)
                and node.name in REPORTING_FUNCTIONS):
            end = getattr(node, "end_lineno", node.lineno)
            for ln in range(node.lineno, end + 1):
                drop.add(ln)
            continue
        body = getattr(node, "body", None)
        if not isinstance(body, list):
            continue
        for stmt in body:
            # A bare string expression: a docstring, or prose standing alone.
            if (isinstance(stmt, ast.Expr)
                    and isinstance(stmt.value, ast.Constant)
                    and isinstance(stmt.value.value, str)):
                end = getattr(stmt, "end_lineno", stmt.lineno)
                for ln in range(stmt.lineno, end + 1):
                    drop.add(ln)
    lines = source.splitlines()
    kept = [ln for i, ln in enumerate(lines, 1) if i not in drop]
    body_text = "\n".join(kept)
    out = []
    try:
        for tok in tokenize.generate_tokens(io.StringIO(body_text).readline):
            if tok.type == tokenize.COMMENT:
                continue
            out.append(tok.string)
    except (tokenize.TokenError, IndentationError):
        return body_text
    return " ".join(out)


def stems(text):
    words = re.findall(r"[a-z]+", text.lower())
    return set(w[:6] for w in words if len(w) >= MIN_STEM and w not in STOP)


# An entry's content words below MIN_STEM are invisible to the matcher. When
# the floor eats MOST of them, the share being computed is a share of the
# minority of the entry that survived, and it is not about the entry any more.
# The line is a majority, chosen as a principle rather than fitted: it is not
# set where it happens to rescue the entry that exposed this.
MIN_COVERAGE = 0.5


def coverage(text):
    """What share of an entry's content words the length floor keeps."""
    words = re.findall(r"[a-z]+", text.lower())
    content = [w for w in words if w not in STOP]
    if not content:
        return {"n_content": 0, "n_kept": 0, "share": 0.0, "lost": []}
    kept = [w for w in content if len(w) >= MIN_STEM]
    return {"n_content": len(content), "n_kept": len(kept),
            "share": len(kept) / len(content),
            "lost": sorted(set(w for w in content if len(w) < MIN_STEM))}


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
    cov = coverage(entry_text)
    if cov["share"] < MIN_COVERAGE:
        return {"share": None, "matched": None, "n_stems": len(a),
                "state": "LOW_COVERAGE", "coverage": cov,
                "why": "the length floor discards %d of this entry's %d "
                       "content words (%s). What is left is a minority of "
                       "the entry, so a share over it is not a reading of "
                       "the entry"
                       % (cov["n_content"] - cov["n_kept"], cov["n_content"],
                          ", ".join(cov["lost"]))}
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
    unscorable, untranslatable, uncovered = [], [], []
    scored = (P.GROUND_TRUTH + P.GROUND_TRUTH_UNCONFIRMED
              + P.GROUND_TRUTH_UNSCORABLE)
    for e in ledger.entries:
        if e["tag"] not in scored:
            continue
        if e["tag"] in P.GROUND_TRUTH_UNSCORABLE:
            # [K~]: the operator flagged this entry's English when speaking,
            # and the matcher reads English stems. A non-match is ambiguous
            # between "absent from the code" and "the English was wrong so
            # the stems miss code that does implement the shape", and nothing
            # here separates those. Refused, not scored -- the same repair as
            # NEGATED, one layer up.
            untranslatable.append(e["text"])
            continue
        m = match(e["text"], code_text)
        confirmed = e["tag"] in P.GROUND_TRUTH
        if m["matched"] is None:
            (uncovered if m["state"] == "LOW_COVERAGE"
             else unscorable).append(e["text"])
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
        "UNSCORABLE_TRANSLATION": untranslatable,
        "UNSCORABLE_COVERAGE": uncovered,
        "ADDED": list(added_items),
        "n_stated": len(ledger.by_tag(*P.STATED)),
        "n_scorable": len(ledger.by_tag(*P.MATCHER_SCORABLE)),
        "translation_footprint": ledger.translation_footprint(),
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
        "why_untranslatable": "a [K~] entry's English was flagged lossy by "
                              "the operator when speaking, and the matcher "
                              "reads English. A non-match cannot be told "
                              "from bad English missing code that does "
                              "implement the shape, so it is refused. It "
                              "stays in n_stated, because it WAS said",
        "why_uncovered": "the length floor discards content words shorter "
                         "than %d characters. When it eats most of an "
                         "entry's content words, the share is computed over "
                         "the minority that survived and is not a reading "
                         "of the entry" % MIN_STEM,
        "stated_vs_scorable": "n_stated is the population the channel loses "
                              "things from; n_scorable is what the matcher "
                              "can be trusted on. The gap is the "
                              "translation layer's footprint on this "
                              "ledger, and the drop rate runs over the "
                              "smaller number",
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
            "K_tilde": "refused by the matcher and still counted in "
                       "n_stated. Those are two different questions and "
                       "[K~] is the tag that made the module ask them "
                       "separately",
            "translation_footprint": "a count of stated entries the matcher "
                                     "cannot read. A property of this "
                                     "ledger and its flagger, not a rate "
                                     "for the translation layer at large",
            "self_diff": "a ledger diffed against code the same party "
                         "wrote in the same pass is contaminated whatever "
                         "surface it runs against. Stripping prose reduces "
                         "it; nothing here removes it",
            "coverage_rule": "a majority line on principle, added AFTER a "
                             "false DROPPED exposed the floor. The fixture "
                             "grade is unchanged and that is not the same "
                             "as having chosen the rule beforehand",
            "short_content_words": "still invisible below %d characters. "
                                   "The rule refuses entries the floor "
                                   "guts; it does not restore the words"
                                   % MIN_STEM,
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
        "A DOCSTRING CAN EARN A CARRIED. Matched against raw source, a "
        "ledger entry scores against any prose in the file that repeats it, "
        "so a module documenting an item it never implemented reads as "
        "having carried it -- and the effect is strongest exactly where "
        "ledger and code came from one party in one pass. "
        "implementation_surface() strips docstrings, comments and the "
        "disclosure functions, which cuts the obvious route. It does not "
        "make a self-diff a measurement: the ledger's own v0.2 run scores "
        "code written to satisfy it, and that number is an upper bound on "
        "carriage rather than a reading of the channel",
        "THE LENGTH FLOOR MAKES SHORT CONTENT WORDS INVISIBLE AND THE "
        "COVERAGE RULE DOES NOT GIVE THEM BACK. Below %d characters a word "
        "is dropped, so 'doe', 'arm', 'gap', 'key' and 'ice' are not read "
        "at all. MIN_COVERAGE refuses an entry when MOST of its content "
        "words go that way; an entry losing one of four is still scored, "
        "with that one invisible. The spec's headline instance -- the S4 "
        "doe-choice arm -- is exactly that case, and it is scored on "
        "'performs partner selection' with the doe unseen. The rule was "
        "also added after a false DROPPED, not before" % MIN_STEM,
        "A [K~] ENTRY IS REFUSED BY THE MATCHER, WHICH MEANS FLAGGING AN "
        "ENTRY LOSSY REMOVES IT FROM THE MEASUREMENT. That is correct -- a "
        "non-match on flagged English is genuinely ambiguous -- and it has a "
        "cost with no defence here: an operator who flags liberally shrinks "
        "n_scorable until the drop rate runs over almost nothing, and the "
        "readout looks the same as a clean channel. The footprint count is "
        "printed beside it for exactly that reason, and reading one without "
        "the other is the misread this arrangement invites",
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
    L.append("  THE LENGTH FLOOR, AND WHAT IT MAKES INVISIBLE")
    L.append("")
    L.append("    content words under %d characters are not read." % MIN_STEM)
    L.append("")
    L.append("    %-46s %-8s %s" % ("entry", "kept", "lost"))
    for t in ("[K~] is a tag, added to the existing tag set",
              "the doe performs partner selection"):
        c = coverage(t)
        L.append("    %-46s %d of %-3d %s"
                 % (t[:46], c["n_kept"], c["n_content"],
                    ", ".join(c["lost"])))
    L.append("")
    L.append("    the first is refused: most of it is gone, so a share")
    L.append("    over the rest is not a reading of the entry. The second")
    L.append("    is scored -- and scored without its subject.")
    L.append("")
    L.append("-" * 72)
    L.append("")
    L.append("  TWO DENOMINATORS, AND A [K~] SITS BETWEEN THEM")
    L.append("")
    kt = P.Ledger("k-tilde demo")
    kt.add("doe performs partner selection", "K")
    kt.add("novelty has a floor set by the annual delta", "K~",
           note="operator flagged the rendering when speaking")
    kt.seal()
    dk = diff(kt, CODE_FIXTURE)
    m = match("novelty has a floor set by the annual delta", CODE_FIXTURE)
    L.append("    n_stated    %d   the population the channel loses from"
             % dk["n_stated"])
    L.append("    n_scorable  %d   what the matcher can be trusted on"
             % dk["n_scorable"])
    L.append("    footprint   %d   stated entries the matcher cannot read"
             % dk["translation_footprint"]["n_unreadable"])
    L.append("")
    L.append("    the [K~] entry above matches at share %.2f and is still"
             % m["share"])
    L.append("    refused. A non-match on flagged English cannot be told")
    L.append("    from bad English missing code that does implement the")
    L.append("    shape, so a match on it is not evidence either.")
    L.append("")
    L.append("    Flagging an entry lossy removes it from the measurement.")
    L.append("    An operator who flags liberally shrinks n_scorable until")
    L.append("    the rate runs over almost nothing, and that reads exactly")
    L.append("    like a clean channel. The footprint prints beside it.")
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

    src = open(os.path.join(HERE, "provenance.py")).read() \
        if os.path.exists(os.path.join(HERE, "provenance.py")) else ""
    if src:
        surf = implementation_surface(src)
        ck("the implementation surface drops docstring prose",
           "silence is not acceptance" in src
           and "silence is not acceptance" not in surf)
        ck("and keeps the values the program carries -- a gloss table IS "
           "the implementation of the sentence it glosses",
           "the station" in surf and "K~" in surf)
        ck("and drops the disclosure functions, which quote entries to "
           "print them",
           "REFUSED (shape question is upstream)" not in surf)
        ck("stripping is a reduction, not a removal, and says so",
           "does not remove it" in implementation_surface.__doc__)

    cov = coverage("[K~] is a tag, added to the existing tag set")
    ck("coverage counts the content words the length floor discards",
       cov["n_content"] == 6 and cov["n_kept"] == 2
       and cov["lost"] == ["k", "set", "tag"])
    mlc = match("[K~] is a tag, added to the existing tag set", "added "
                "to the existing set of tags")
    ck("a low-coverage entry is refused, not scored: the share would be "
       "over the minority of the entry that survived the floor",
       mlc["matched"] is None and mlc["state"] == "LOW_COVERAGE")
    ck("and share is None there, not a number to be read anyway",
       mlc["share"] is None)
    ck("the rule is a majority, not the value that rescues one entry",
       MIN_COVERAGE == 0.5)
    ck("an entry losing a minority of its content words is still scored",
       match("the doe performs partner selection",
             CODE_FIXTURE)["state"] == "OK")
    ck("adding the rule did not move the matcher grade on the fixtures",
       grade_matcher()["grade"] == "OK"
       and grade_matcher()["true_carried_rate"] == 1.0)

    kt = P.Ledger("k-tilde")
    kt.add("doe performs partner selection", "K")
    kt.add("novelty has a floor set by the annual delta", "K~",
           note="operator flagged the rendering when speaking")
    kt.seal()
    dk = diff(kt, CODE_FIXTURE)
    ck("a [K~] entry is refused by the matcher even when its stems match",
       len(dk["UNSCORABLE_TRANSLATION"]) == 1
       and match("novelty has a floor set by the annual delta",
                 CODE_FIXTURE)["matched"] is True)
    ck("and it is out of the drop-rate denominator",
       dk["n_ground_truth"] == 1)
    ck("but it stays in n_stated, because it WAS said",
       dk["n_stated"] == 2 and dk["n_scorable"] == 1)
    ck("the gap between the two denominators is the footprint, as a count",
       dk["translation_footprint"]["n_unreadable"] == 1
       and dk["translation_footprint"]["share"] is None)
    ck("liberal flagging shrinking the denominator is disclosed",
       any("flags liberally shrinks" in b for b in breaks()))

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
