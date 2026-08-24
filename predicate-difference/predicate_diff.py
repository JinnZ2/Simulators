#!/usr/bin/env python3
# SPDX-License-Identifier: CC0-1.0
"""
predicate_diff.py - the set difference, and when the corpus can support it.

    python3 predicate_diff.py [--selftest]

Marker under exploration. Delivered method: SPEC_METHOD.md.

# NOTE TO READERS -- TERM COLLISION
# "change of mind" here means REVISION (provenance-bearing). See PREAMBLE.md.

THE METHOD, AS DELIVERED. For a given corpus decade, hold a work domain
constant. Extract every predicate attaching to the subject class doing that
work, and every predicate attaching to the reference class doing the same
work. The marker is the set difference -- predicates that appear for one class
and never for the other, at a rate the corpus size can support.

THE LAST CLAUSE IS THE WHOLE INSTRUMENT. A set difference is trivial to
compute and almost always wrong, because "never appears for the other class"
is a claim about an absence, and an absence is only a measurement when the
sample was large enough for the thing to have shown up. If the reference class
has fifty tokens in that work domain, every predicate is absent from it, and
the difference returns the subject class's entire vocabulary as a marker.

So absence is assertable only when the predicate WOULD have been expected in
the reference class at the subject class's own rate. `support()` computes that
expected count and refuses below MIN_EXPECTED, returning NOT_ENOUGH_TEXT --
which is a different state from ABSENT and is never folded into it. This is
the same repair the rest of this repo keeps arriving at, arriving here at the
denominator of a set difference.

VALENCE IS NOT SWITCHED OFF, IT IS ABSENT. The method says to score with
valence deliberately switched off, because in-frame these predicates read
positive: devoted, uncomplaining, naturally suited, insensible to fatigue. A
valence channel set to zero is a channel someone re-enables. There is no
valence field on Predicate, no valence argument anywhere, and `check_no_
valence()` walks this module's own AST and fails the selftest if one appears.
Enforced, not stated.

WHAT IS NOT HERE. No corpus. The named targets are registered with
acquisition state NOT_ACQUIRED, the fixtures below are marked
SYNTHETIC_FIXTURE and exist only to grade the instrument, and every readout
over real classes returns NOT_RUN. A predicate taxonomy derived from
fixtures would be this module inventing the finding.

stdlib only, parses under Python 3.9. CC0.
"""

import argparse
import ast
import os
import sys

# Absence is assertable only if the predicate would have been expected at
# least this many times in the reference class, at the subject class's rate.
# Three is a floor chosen on the reasoning that an expected count below it
# makes "did not appear" the ordinary outcome rather than an observation.
MIN_EXPECTED = 3.0

# A predicate must also clear a raw floor in the class it DOES appear in,
# or the rate it establishes is one or two tokens.
MIN_OBSERVED = 5

STATES = ("MARKER", "SHARED", "NOT_ENOUGH_TEXT", "BELOW_OBSERVED_FLOOR")


class CorpusError(Exception):
    pass


class Predicate(object):
    """One predicate, its counts, and no valence.

    There is deliberately no valence field. In-frame these read positive,
    and a scorer that carries the channel will eventually be asked to use it.
    """

    def __init__(self, lemma, shape=None):
        if not lemma:
            raise CorpusError("a predicate needs its lemma")
        self.lemma = lemma
        self.shape = shape          # assigned from the corpus, not invented

    def __repr__(self):
        return "Predicate(%r)" % self.lemma


class ClassSample(object):
    """Predicate counts for one class, in one work domain, in one decade."""

    def __init__(self, name, work_domain, decade, tokens, counts,
                 source_state="NOT_ACQUIRED"):
        if tokens is None:
            raise CorpusError(
                "token count is required. Without it no absence in this "
                "sample can be interpreted, and the set difference is the "
                "sample's whole vocabulary")
        self.name = name
        self.work_domain = work_domain
        self.decade = decade
        self.tokens = tokens
        self.counts = dict(counts)
        self.source_state = source_state

    def rate(self, lemma):
        return self.counts.get(lemma, 0) / self.tokens if self.tokens else 0.0


def support(subject, reference, lemma):
    """Can this corpus support a claim that `lemma` is absent from reference.

    Expected count in the reference class, at the subject class's rate. If
    the reference sample is too thin for the predicate to have shown up, the
    absence is not an observation.
    """
    n_subj = subject.counts.get(lemma, 0)
    n_ref = reference.counts.get(lemma, 0)
    subj_rate = subject.rate(lemma)
    expected_in_ref = subj_rate * reference.tokens
    return {
        "lemma": lemma,
        "observed_subject": n_subj,
        "observed_reference": n_ref,
        "subject_rate": subj_rate,
        "expected_in_reference": expected_in_ref,
        "reference_tokens": reference.tokens,
        "absence_assertable": expected_in_ref >= MIN_EXPECTED,
        "observed_floor_cleared": n_subj >= MIN_OBSERVED,
        "why": "absence is a measurement only when the sample was large "
               "enough for the predicate to have appeared. Expected %.2f "
               "in the reference class at the subject's rate"
               % expected_in_ref,
    }


def classify(subject, reference, lemma):
    """MARKER, SHARED, NOT_ENOUGH_TEXT, or BELOW_OBSERVED_FLOOR."""
    s = support(subject, reference, lemma)
    if not s["observed_floor_cleared"]:
        state = "BELOW_OBSERVED_FLOOR"
        why = ("appears %d times in the subject class, under the floor of "
               "%d. The rate it would establish rests on too few tokens to "
               "predict anything about the reference class"
               % (s["observed_subject"], MIN_OBSERVED))
    elif s["observed_reference"] > 0:
        state = "SHARED"
        why = "appears in both classes; not a difference"
    elif not s["absence_assertable"]:
        state = "NOT_ENOUGH_TEXT"
        why = ("absent from the reference class, and the reference sample is "
               "too thin for that to be an observation: expected %.2f "
               "occurrences, floor %.1f"
               % (s["expected_in_reference"], MIN_EXPECTED))
    else:
        state = "MARKER"
        why = ("appears %d times for the subject class and never for the "
               "reference class, which had %d tokens in the same work "
               "domain -- enough that %.1f occurrences were expected"
               % (s["observed_subject"], s["reference_tokens"],
                  s["expected_in_reference"]))
    return {"lemma": lemma, "state": state, "why": why, "support": s}


def difference(subject, reference):
    """The set difference, with every lemma carrying why it landed where."""
    if subject.work_domain != reference.work_domain:
        raise CorpusError(
            "the work domain must be held constant. Comparing %r against %r "
            "compares the classes and the work at once"
            % (subject.work_domain, reference.work_domain))
    if subject.decade != reference.decade:
        raise CorpusError(
            "the decade must be held constant, or the difference carries "
            "period change as well as class")
    rows = [classify(subject, reference, l) for l in sorted(subject.counts)]
    out = dict((s, [r for r in rows if r["state"] == s]) for s in STATES)
    return {
        "subject": subject.name, "reference": reference.name,
        "work_domain": subject.work_domain, "decade": subject.decade,
        "rows": rows,
        "markers": [r["lemma"] for r in out["MARKER"]],
        "n_markers": len(out["MARKER"]),
        "n_shared": len(out["SHARED"]),
        "n_not_enough_text": len(out["NOT_ENOUGH_TEXT"]),
        "n_below_floor": len(out["BELOW_OBSERVED_FLOOR"]),
        "by_state": out,
        "source_state": (subject.source_state, reference.source_state),
        "runnable": (subject.source_state == "ACQUIRED"
                     and reference.source_state == "ACQUIRED"),
    }


# --- valence: absent, and checked to be absent ------------------------------

def check_no_valence(path=None):
    """Walk this module's AST and fail if a valence channel exists.

    Not a string search: identifiers only, so the word can appear in prose
    explaining why it is absent without satisfying its own check. If someone
    adds a valence field, argument, attribute or function later, the
    selftest stops passing.
    """
    path = path or os.path.abspath(__file__)
    src = open(path).read()
    tree = ast.parse(src)
    allow = {"check_no_valence"}
    hits = []
    for node in ast.walk(tree):
        name = None
        if isinstance(node, ast.Name):
            name = node.id
        elif isinstance(node, ast.Attribute):
            name = node.attr
        elif isinstance(node, ast.arg):
            name = node.arg
        elif isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            name = node.name
        elif isinstance(node, ast.keyword):
            name = node.arg
        if name and "valence" in name.lower() and name not in allow:
            hits.append({"name": name,
                         "line": getattr(node, "lineno", None)})
    return {"clean": not hits, "hits": hits,
            "why": "valence is absent as a channel, not set to zero. A "
                   "channel set to zero is a channel someone re-enables, "
                   "and in-frame these predicates read positive"}


# --- corpus targets, none acquired -----------------------------------------

CORPUS_TARGETS = [
    {"target": "Freud", "kind": "in-frame, contempt as premise",
     "state": "NOT_ACQUIRED"},
    {"target": "period psychology and medicine",
     "kind": "in-frame, contempt as premise", "state": "NOT_ACQUIRED"},
    {"target": "household management texts",
     "kind": "in-frame, contempt as premise", "state": "NOT_ACQUIRED"},
    {"target": "labor economics of the era",
     "kind": "in-frame, contempt as premise", "state": "NOT_ACQUIRED"},
]


def corpus_state():
    acquired = [t for t in CORPUS_TARGETS if t["state"] == "ACQUIRED"]
    return {"n_targets": len(CORPUS_TARGETS),
            "n_acquired": len(acquired),
            "targets": CORPUS_TARGETS,
            "state": "NONE_ACQUIRED" if not acquired else "PARTIAL",
            "why": "the targets are named in the delivered method. Naming a "
                   "source is not holding it, and no readout over real "
                   "classes runs until one is acquired",
            "runnable": bool(acquired)}


# --- fixtures: SYNTHETIC, for grading the instrument only ------------------
# These are invented and carry no claim about any literature. They exist so
# the instrument can be shown to fire, to stay silent, and to refuse.

FIXTURE_NOTE = "SYNTHETIC_FIXTURE -- invented to grade the instrument"

SIG_SUBJ = ClassSample("fixture subject", "domain_x", 1900, tokens=20000,
                       counts={"pred_a": 40, "pred_b": 30, "pred_c": 25,
                               "pred_shared": 50},
                       source_state="FIXTURE")
SIG_REF = ClassSample("fixture reference", "domain_x", 1900, tokens=20000,
                      counts={"pred_shared": 60}, source_state="FIXTURE")

NULL_SUBJ = ClassSample("fixture subject", "domain_x", 1900, tokens=20000,
                        counts={"pred_a": 40, "pred_shared": 50},
                        source_state="FIXTURE")
NULL_REF = ClassSample("fixture reference", "domain_x", 1900, tokens=20000,
                       counts={"pred_a": 35, "pred_shared": 60},
                       source_state="FIXTURE")

THIN_SUBJ = ClassSample("fixture subject", "domain_x", 1900, tokens=20000,
                        counts={"pred_a": 40, "pred_b": 30},
                        source_state="FIXTURE")
THIN_REF = ClassSample("fixture reference", "domain_x", 1900, tokens=300,
                       counts={}, source_state="FIXTURE")


def grade():
    """Null-harness grade. A difference engine that always fires is a list.

    Three fixtures: one with a real difference, one with none, and one with
    a real difference in a reference sample too thin to support it. The
    third is the one that separates this instrument from a set subtraction.
    """
    sig = difference(SIG_SUBJ, SIG_REF)
    null = difference(NULL_SUBJ, NULL_REF)
    thin = difference(THIN_SUBJ, THIN_REF)
    fires_on_signal = sig["n_markers"] > 0
    silent_on_null = null["n_markers"] == 0
    refuses_thin = thin["n_markers"] == 0 and thin["n_not_enough_text"] > 0
    if not fires_on_signal and silent_on_null:
        g = "CONSTANT_SILENT"
    elif fires_on_signal and not silent_on_null:
        g = "CONSTANT_FIRES"
    elif fires_on_signal and silent_on_null and not refuses_thin:
        g = "NO_THIN_REFUSAL"
    elif fires_on_signal and silent_on_null and refuses_thin:
        g = "OK"
    else:
        g = "NO_DISCRIMINATION"
    return {"grade": g,
            "signal_markers": sig["n_markers"],
            "null_markers": null["n_markers"],
            "thin_markers": thin["n_markers"],
            "thin_not_enough_text": thin["n_not_enough_text"],
            "fires_on_signal": fires_on_signal,
            "silent_on_null": silent_on_null,
            "refuses_thin": refuses_thin,
            "fixture_note": FIXTURE_NOTE,
            "why": "the thin fixture has the same real difference as the "
                   "signal fixture and a reference sample of %d tokens. A "
                   "plain set subtraction reports the same markers for "
                   "both" % THIN_REF.tokens}


def run_real():
    """Every readout over real classes. NOT_RUN until a corpus exists."""
    return {"state": "NOT_RUN",
            "corpus": corpus_state()["state"],
            "markers": None,
            "why": "no corpus is acquired. Markers computed from fixtures "
                   "would be markers about the fixtures, and the fixtures "
                   "were written by this module"}


def confidence():
    return {"the_instrument": "graded on three synthetic fixtures. It fires, "
                              "stays silent, and refuses. Three fixtures is "
                              "not a corpus and the grade is about the "
                              "code, not about any literature",
            "MIN_EXPECTED": "three, chosen on the reasoning that an expected "
                            "count below it makes 'did not appear' the "
                            "ordinary outcome. It is a floor, not a "
                            "significance test, and no distribution is "
                            "claimed",
            "MIN_OBSERVED": "five, so a rate is not established from one or "
                            "two tokens. Also chosen, not derived",
            "valence": "absent as a channel and checked by AST. That "
                       "prevents a valence field existing; it does not "
                       "prevent a predicate taxonomy from encoding valence "
                       "in its category names",
            "the_findings": "NOT_RUN. No corpus is acquired and no marker "
                            "over any real class is reported",
            "resolved": False}


def breaks():
    return [
        "WITHOUT THE SUPPORT RULE THIS IS A LIST, NOT A MEASUREMENT, AND THE "
        "THIN FIXTURE SHOWS THE DIFFERENCE. Subject and reference carry the "
        "same real difference in the signal and thin fixtures. With a 20000-"
        "token reference the instrument reports 3 markers; with a 300-token "
        "reference it reports 0 and 2 NOT_ENOUGH_TEXT. A plain set "
        "subtraction reports the same markers for both, and would return the "
        "subject class's whole vocabulary whenever the reference sample is "
        "thin -- which for these subject classes and these sources is the "
        "expected condition, not an edge case",
        "MIN_EXPECTED AND MIN_OBSERVED ARE CHOSEN NUMBERS AND THE RESULT "
        "MOVES WITH THEM. Three and five are floors picked for shape, not "
        "derived from a model of the corpus. A marker that clears an "
        "expected count of 3.0 does not clear 5.0, and nothing here "
        "establishes which floor is right. They are printed beside every "
        "readout so a reader can see what the verdict rests on",
        "THE FIXTURES ARE INVENTED AND THEY GRADE THE INSTRUMENT, NOT THE "
        "METHOD. They show the code fires, stays silent and refuses on "
        "cases built to elicit exactly those three responses. Whether the "
        "predicate difference finds anything in Freud or in household "
        "management texts is untouched by any of it, and the fixtures were "
        "written by the same party that wrote the thresholds",
        "THE AST CHECK PREVENTS A VALENCE FIELD, NOT VALENCE. It fails if an "
        "identifier containing 'valence' appears. A taxonomy whose category "
        "names carry the judgement -- and a contempt taxonomy is exactly "
        "where that is tempting -- passes the check untouched. The method "
        "says score with valence switched off, and what is enforced here is "
        "the narrower thing: no channel to switch",
        "HOLDING THE WORK DOMAIN CONSTANT IS REQUIRED AND NOT VERIFIED. "
        "difference() refuses mismatched work_domain and decade strings, "
        "which checks that two labels agree. Whether the two samples "
        "actually describe the same work is a judgement made when the "
        "samples are built, and a subject class and reference class labelled "
        "with the same domain may be doing different work under one word -- "
        "which is the case the whole method is trying to see",
    ]


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


def report():
    L = ["PREDICATE DIFFERENCE -- the marker, and when it is one",
         "=" * 72, ""]
    L.append("  Hold the work domain constant. Extract every predicate")
    L.append("  attaching to the subject class doing that work, and every")
    L.append("  predicate attaching to the reference class doing the same")
    L.append("  work. The marker is the set difference -- at a rate the")
    L.append("  corpus size can support.")
    L.append("")
    L.append("  thresholds: MIN_EXPECTED %.1f   MIN_OBSERVED %d"
             % (MIN_EXPECTED, MIN_OBSERVED))
    L.append("")
    L.append("-" * 72)
    L.append("")
    L.append("  THE INSTRUMENT, GRADED BEFORE IT IS USED")
    L.append("")
    g = grade()
    L.append("    %-26s %-10s %s" % ("fixture", "markers", "verdict"))
    L.append("    %-26s %-10d %s"
             % ("signal (real difference)", g["signal_markers"],
                "fires" if g["fires_on_signal"] else "SILENT"))
    L.append("    %-26s %-10d %s"
             % ("null (no difference)", g["null_markers"],
                "silent" if g["silent_on_null"] else "FIRES"))
    L.append("    %-26s %-10d %s"
             % ("thin reference sample", g["thin_markers"],
                "refuses (%d NOT_ENOUGH_TEXT)" % g["thin_not_enough_text"]))
    L.append("")
    L.append("    GRADE: %s" % g["grade"])
    L.append("    %s" % g["fixture_note"])
    L.append("")
    for line in _wrap(g["why"], "    "):
        L.append(line)
    L.append("")
    L.append("    Without the support rule the signal and thin fixtures")
    L.append("    return the same markers. That is the difference between")
    L.append("    a measurement and a set subtraction.")
    L.append("")
    L.append("-" * 72)
    L.append("")
    L.append("  THE FOUR STATES, ON THE SIGNAL FIXTURE")
    L.append("")
    sig = difference(SIG_SUBJ, SIG_REF)
    L.append("    %-16s %-22s %s" % ("lemma", "state", "expected in ref"))
    for r in sig["rows"]:
        L.append("    %-16s %-22s %.1f"
                 % (r["lemma"], r["state"],
                    r["support"]["expected_in_reference"]))
    L.append("")
    thin = difference(THIN_SUBJ, THIN_REF)
    L.append("    the same predicates against a %d-token reference:"
             % THIN_REF.tokens)
    for r in thin["rows"]:
        L.append("    %-16s %-22s %.1f"
                 % (r["lemma"], r["state"],
                    r["support"]["expected_in_reference"]))
    L.append("")
    L.append("    NOT_ENOUGH_TEXT is not ABSENT and is never folded into")
    L.append("    it. The predicate may well be absent; the sample cannot")
    L.append("    say so.")
    L.append("")
    L.append("-" * 72)
    L.append("")
    L.append("  VALENCE")
    L.append("")
    v = check_no_valence()
    L.append("    channel present: %s" % (not v["clean"]))
    L.append("    AST identifiers matching 'valence': %d" % len(v["hits"]))
    for line in _wrap(v["why"], "    "):
        L.append(line)
    L.append("")
    L.append("-" * 72)
    L.append("")
    L.append("  CORPUS")
    L.append("")
    c = corpus_state()
    for t in c["targets"]:
        L.append("    %-34s %s" % (t["target"], t["state"]))
    L.append("")
    L.append("    acquired: %d of %d      state: %s"
             % (c["n_acquired"], c["n_targets"], c["state"]))
    for line in _wrap(c["why"], "    "):
        L.append(line)
    L.append("")
    r = run_real()
    L.append("    readout over real classes: %s" % r["state"])
    L.append("    markers: %s" % r["markers"])
    for line in _wrap(r["why"], "    "):
        L.append(line)
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


def selftest():
    f = k = 0

    def ck(label, cond):
        nonlocal f, k
        k += 1
        if not cond:
            f += 1
            print("FAIL %s" % label)

    try:
        ClassSample("s", "d", 1900, tokens=None, counts={})
        ok = False
    except CorpusError:
        ok = True
    ck("a sample without a token count is refused -- no absence in it can "
       "be interpreted", ok)
    try:
        difference(SIG_SUBJ, ClassSample("r", "domain_y", 1900, 20000, {}))
        ok = False
    except CorpusError:
        ok = True
    ck("the work domain must be held constant", ok)
    try:
        difference(SIG_SUBJ, ClassSample("r", "domain_x", 1910, 20000, {}))
        ok = False
    except CorpusError:
        ok = True
    ck("and so must the decade", ok)

    sig = difference(SIG_SUBJ, SIG_REF)
    ck("a real difference in a supportable sample yields markers",
       sig["n_markers"] == 3)
    ck("a predicate in both classes is SHARED, not a marker",
       sig["n_shared"] == 1
       and "pred_shared" not in sig["markers"])

    thin = difference(THIN_SUBJ, THIN_REF)
    ck("THE SAME DIFFERENCE against a thin reference yields NO markers",
       thin["n_markers"] == 0)
    ck("and lands in NOT_ENOUGH_TEXT instead",
       thin["n_not_enough_text"] == 2)
    ck("which is a distinct state from ABSENT and from SHARED",
       "NOT_ENOUGH_TEXT" in STATES and "ABSENT" not in STATES)
    ck("so a plain set subtraction and this instrument disagree on the "
       "thin case, which is the point",
       set(sig["markers"]) and not set(thin["markers"]))

    low = ClassSample("s", "domain_x", 1900, 20000, {"rare": 2})
    ck("a predicate under the observed floor does not establish a rate",
       classify(low, SIG_REF, "rare")["state"] == "BELOW_OBSERVED_FLOOR")

    g = grade()
    ck("the instrument is graded before use and grades OK",
       g["grade"] == "OK")
    ck("it is not CONSTANT_FIRES", g["silent_on_null"] is True)
    ck("it is not CONSTANT_SILENT", g["fires_on_signal"] is True)
    ck("and it refuses the thin case rather than reporting it",
       g["refuses_thin"] is True)
    ck("the fixtures are marked synthetic",
       "SYNTHETIC_FIXTURE" in g["fixture_note"])

    v = check_no_valence()
    ck("no valence channel exists in this module", v["clean"] is True)
    ck("the check is over identifiers, not strings -- the word appears in "
       "the docstring and does not satisfy its own check",
       "valence" in __doc__.lower() and v["clean"] is True)
    ck("a Predicate carries no valence attribute",
       not hasattr(Predicate("x"), "valence"))

    c = corpus_state()
    ck("no corpus target is acquired",
       c["n_acquired"] == 0 and c["state"] == "NONE_ACQUIRED")
    ck("all four delivered targets are registered", c["n_targets"] == 4)
    ck("and the real readout is NOT_RUN, with no markers",
       run_real()["state"] == "NOT_RUN" and run_real()["markers"] is None)

    ck("the list-vs-measurement result leads the breaks list",
       "A LIST, NOT A MEASUREMENT" in breaks()[0])
    ck("the chosen thresholds are disclosed",
       any("CHOSEN NUMBERS" in b for b in breaks()))
    ck("the AST check's limit -- taxonomy names -- is disclosed",
       any("PREVENTS A VALENCE FIELD, NOT VALENCE" in b for b in breaks()))
    ck("that same-labelled work domains may not be the same work is "
       "disclosed",
       any("REQUIRED AND NOT VERIFIED" in b for b in breaks()))
    ck("confidence unresolved", confidence()["resolved"] is False)
    ck("report renders", "GRADED BEFORE IT IS USED" in report())
    print("%d/%d checks passed" % (k - f, k))
    return 1 if f else 0


def main():
    ap = argparse.ArgumentParser(description="predicate difference")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    print(report())
    return 0


if __name__ == "__main__":
    sys.exit(main())
