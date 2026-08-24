#!/usr/bin/env python3
# SPDX-License-Identifier: CC0-1.0
"""
shape_index.py - one shape, four bindings, different vocabulary.

    python3 shape_index.py [--selftest]

Marker under exploration. Delivered method: SPEC_METHOD.md.

# NOTE TO READERS -- TERM COLLISION
# "change of mind" here means REVISION (provenance-bearing). See PREAMBLE.md.

THE EXTENSION, AS DELIVERED. "Extend it across subject classes: women,
enslaved and formerly enslaved people, ethnic groups typed as lower, disabled
people. If the same predicate shape recurs across all four with different
vocabulary, that confirms it's a structural signature and not four separate
literatures."

THE OUTPUT FORMAT IS INFERRED AND THE INFERENCE IS FLAGGED. No "shape-index
format" exists in this repository. What does exist is scope-bound-shapes/,
where a SHAPE is "a structural sequence... defined by its sequence and its
selection rule, NOT by its materials", instantiated in bindings. Four subject
classes carrying one predicate shape in four vocabularies is that
distinction exactly -- shape invariant, materials varying -- so the index
below is built to it. It is not imported from scope-bound-shapes: that
module's Binding is a LIVE/FROZEN variable list, and forcing a predicate
shape into it would be fitting the object to the nearest available class.
If the delivered format is something else, this is the wrong shape of file
and the contents transfer.

DISJOINT VOCABULARY IS A REQUIREMENT, NOT AN INCIDENTAL. The method says the
shape must recur "with different vocabulary", and that clause carries the
weight. A shape recurring across all four bindings in the SAME words is
consistent with four literatures being one literature -- shared sources,
quotation, a single tradition restating itself -- which is the hypothesis the
extension exists to rule out. So `recurrence()` reports vocabulary overlap
separately and returns SHARED_VOCABULARY rather than STRUCTURAL_SIGNATURE
when the words are common across bindings. Full presence with shared
vocabulary is weaker evidence than partial presence with disjoint vocabulary,
and collapsing them into a count of bindings loses exactly that.

THE INDEX IS EMPTY OF REAL SHAPES. A predicate shape taxonomy comes from the
corpus. Naming the shapes here -- and they would be easy to name -- would be
this module writing the finding and then confirming it. The fixtures below
are marked SYNTHETIC_FIXTURE and grade the recurrence test; every real row
is NOT_RUN.

stdlib only, parses under Python 3.9. CC0.
"""

import argparse
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import predicate_diff as PD                                    # noqa: E402

SUBJECT_CLASSES = (
    "women",
    "enslaved and formerly enslaved people",
    "ethnic groups typed as lower",
    "disabled people",
)

VERDICTS = ("STRUCTURAL_SIGNATURE", "SHARED_VOCABULARY", "NOT_ESTABLISHED",
            "NOT_RUN")


class IndexError_(Exception):
    pass


class ShapeEntry(object):
    """One predicate shape, and the vocabulary realising it per binding.

    `realisations` maps subject class -> the marker lemmas carrying the shape
    in that class. A class with no realisation is simply absent from the map,
    which is not the same as a class checked and found not to carry it.
    """

    def __init__(self, shape_id, description, realisations, checked_classes,
                 derived_from, note=None):
        if not derived_from:
            raise IndexError_(
                "a shape entry records where the shape came from. A taxonomy "
                "with no provenance is the indexer's own categories")
        unknown = [c for c in realisations if c not in SUBJECT_CLASSES]
        if unknown:
            raise IndexError_("unknown subject class: %s"
                              % ", ".join(sorted(unknown)))
        missing = [c for c in realisations if c not in checked_classes]
        if missing:
            raise IndexError_(
                "a class cannot carry a realisation without having been "
                "checked: %s" % ", ".join(sorted(missing)))
        self.shape_id = shape_id
        self.description = description
        self.realisations = dict((c, sorted(set(v)))
                                 for c, v in realisations.items())
        self.checked_classes = sorted(set(checked_classes))
        self.derived_from = derived_from
        self.note = note

    def present_in(self):
        return sorted(c for c, v in self.realisations.items() if v)

    def unchecked(self):
        return sorted(c for c in SUBJECT_CLASSES
                      if c not in self.checked_classes)

    def vocabulary_overlap(self):
        """Words shared between any two bindings."""
        present = self.present_in()
        shared = set()
        for i, a in enumerate(present):
            for b in present[i + 1:]:
                shared |= (set(self.realisations[a])
                           & set(self.realisations[b]))
        return sorted(shared)

    def recurrence(self):
        present = self.present_in()
        unchecked = self.unchecked()
        overlap = self.vocabulary_overlap()
        n = len(present)
        if unchecked:
            verdict = "NOT_ESTABLISHED"
            why = ("%d of %d subject classes were not checked (%s). Presence "
                   "in the rest cannot establish recurrence across all four"
                   % (len(unchecked), len(SUBJECT_CLASSES),
                      ", ".join(unchecked)))
        elif n < len(SUBJECT_CLASSES):
            verdict = "NOT_ESTABLISHED"
            why = ("present in %d of %d classes. The extension's claim is "
                   "recurrence across all four" % (n, len(SUBJECT_CLASSES)))
        elif overlap:
            verdict = "SHARED_VOCABULARY"
            why = ("present in all %d classes and the vocabulary overlaps: "
                   "%s. Shared words are consistent with four literatures "
                   "being one, which is the hypothesis the extension exists "
                   "to rule out" % (n, ", ".join(overlap)))
        else:
            verdict = "STRUCTURAL_SIGNATURE"
            why = ("present in all %d classes with disjoint vocabulary. The "
                   "shape recurs and the words do not, which is what "
                   "separates a structural signature from a shared "
                   "literature" % n)
        return {"shape_id": self.shape_id,
                "verdict": verdict,
                "present_in": present,
                "n_present": n,
                "n_classes": len(SUBJECT_CLASSES),
                "unchecked": unchecked,
                "vocabulary_overlap": overlap,
                "disjoint": not overlap,
                "why": why}

    def row(self):
        r = self.recurrence()
        return {"shape_id": self.shape_id,
                "description": self.description,
                "bindings": "%d of %d" % (r["n_present"], r["n_classes"]),
                "disjoint_vocabulary": r["disjoint"],
                "verdict": r["verdict"],
                "realisations": dict(self.realisations),
                "unchecked": r["unchecked"],
                "derived_from": self.derived_from}


class ShapeIndex(object):
    def __init__(self):
        self.entries = []

    def add(self, entry):
        self.entries.append(entry)
        return entry

    def rows(self):
        return [e.row() for e in self.entries]

    def counts(self):
        out = dict((v, 0) for v in VERDICTS)
        for e in self.entries:
            out[e.recurrence()["verdict"]] += 1
        return out


# --- the real index: empty ------------------------------------------------

def real_index():
    """The index over the named corpus targets. No corpus, no shapes."""
    idx = ShapeIndex()
    return {"index": idx,
            "n_shapes": len(idx.entries),
            "state": "NOT_RUN",
            "corpus": PD.corpus_state()["state"],
            "why": "a predicate shape taxonomy is derived from the corpus. "
                   "None is acquired, so the index is empty -- and empty "
                   "here is the size of the work done, not a finding that "
                   "no shape recurs"}


# --- fixtures: SYNTHETIC, to grade the recurrence test ---------------------

FIXTURE_NOTE = "SYNTHETIC_FIXTURE -- invented to grade the recurrence test"
ALL_FOUR = list(SUBJECT_CLASSES)

FX_DISJOINT = ShapeEntry(
    "FX_1", "fixture shape, all four classes, no shared words",
    realisations={SUBJECT_CLASSES[0]: ["w_a1", "w_a2"],
                  SUBJECT_CLASSES[1]: ["w_b1"],
                  SUBJECT_CLASSES[2]: ["w_c1", "w_c2"],
                  SUBJECT_CLASSES[3]: ["w_d1"]},
    checked_classes=ALL_FOUR, derived_from=FIXTURE_NOTE)

FX_SHARED = ShapeEntry(
    "FX_2", "fixture shape, all four classes, one shared word",
    realisations={SUBJECT_CLASSES[0]: ["w_common", "w_a2"],
                  SUBJECT_CLASSES[1]: ["w_common"],
                  SUBJECT_CLASSES[2]: ["w_common", "w_c2"],
                  SUBJECT_CLASSES[3]: ["w_common"]},
    checked_classes=ALL_FOUR, derived_from=FIXTURE_NOTE)

FX_PARTIAL = ShapeEntry(
    "FX_3", "fixture shape, two classes only, disjoint",
    realisations={SUBJECT_CLASSES[0]: ["w_a1"],
                  SUBJECT_CLASSES[1]: ["w_b1"]},
    checked_classes=ALL_FOUR, derived_from=FIXTURE_NOTE)

FX_UNCHECKED = ShapeEntry(
    "FX_4", "fixture shape, all present but two classes never checked",
    realisations={SUBJECT_CLASSES[0]: ["w_a1"],
                  SUBJECT_CLASSES[1]: ["w_b1"]},
    checked_classes=[SUBJECT_CLASSES[0], SUBJECT_CLASSES[1]],
    derived_from=FIXTURE_NOTE)

FIXTURES = [FX_DISJOINT, FX_SHARED, FX_PARTIAL, FX_UNCHECKED]


def grade():
    """Does the recurrence test separate the four cases it must."""
    v = dict((e.shape_id, e.recurrence()["verdict"]) for e in FIXTURES)
    ok = (v["FX_1"] == "STRUCTURAL_SIGNATURE"
          and v["FX_2"] == "SHARED_VOCABULARY"
          and v["FX_3"] == "NOT_ESTABLISHED"
          and v["FX_4"] == "NOT_ESTABLISHED")
    distinct = len(set(v.values()))
    return {"verdicts": v,
            "grade": "OK" if ok else ("NO_DISCRIMINATION" if distinct < 2
                                      else "MISCLASSIFIES"),
            "n_distinct_verdicts": distinct,
            "fixture_note": FIXTURE_NOTE,
            "why": "FX_1 and FX_2 differ only in whether one word is shared "
                   "across bindings. A test that counts bindings returns the "
                   "same verdict for both, and the difference between them "
                   "is the whole extension"}


def confidence():
    return {"the_format": "INFERRED from scope-bound-shapes, where a shape "
                          "is defined by its structure and not its "
                          "materials. No shape-index format exists in this "
                          "repo, so if the delivered one differs this is "
                          "the wrong file shape and the contents transfer",
            "the_index": "empty of real shapes. A taxonomy comes from the "
                         "corpus and none is acquired",
            "disjointness": "treated as a requirement, on the method's own "
                            "words. A shape recurring in shared vocabulary "
                            "is reported as weaker, not as absent",
            "the_grade": "over four synthetic fixtures that separate three "
                         "verdicts. It grades the test, not the extension",
            "unchecked_classes": "a class never checked is never counted as "
                                 "absent. FX_4 exists to hold that case",
            "resolved": False}


def breaks():
    return [
        "FULL PRESENCE WITH SHARED VOCABULARY IS WEAKER THAN PARTIAL "
        "PRESENCE WITH DISJOINT VOCABULARY, AND A BINDING COUNT LOSES THAT. "
        "FX_1 and FX_2 both appear in all four classes and differ only in "
        "whether one word is common across them. A test that counts bindings "
        "returns four-of-four for both. Shared words are consistent with the "
        "four literatures being one literature -- quotation, a shared source, "
        "a single tradition restating itself -- which is precisely the "
        "hypothesis the extension was added to rule out, so the shared case "
        "returns SHARED_VOCABULARY and not a signature",
        "THE INDEX IS EMPTY AND THAT IS THE SIZE OF THE WORK DONE, NOT A "
        "FINDING. Zero shapes recorded does not mean no shape recurs across "
        "the four classes. It means no corpus has been read. Naming the "
        "shapes from here would be easy and would be this module writing the "
        "finding and then confirming it against its own fixtures",
        "THE OUTPUT FORMAT IS AN INFERENCE. The delivered instruction names "
        "a shape-index format that does not exist in this repository. The "
        "format used is built from scope-bound-shapes' distinction between a "
        "shape and its materials, which fits the extension's own "
        "same-shape-different-vocabulary claim closely. It is still a guess "
        "at what was asked for, and it is not imported from that module "
        "because its Binding is a LIVE/FROZEN variable list and forcing a "
        "predicate shape into it would fit the object to the nearest "
        "available class",
        "A CLASS NEVER CHECKED IS NOT A CLASS FOUND EMPTY, AND THE ENTRY "
        "SCHEMA IS THE ONLY THING ENFORCING IT. ShapeEntry refuses a "
        "realisation for a class not in checked_classes, and reports "
        "unchecked classes separately from absent ones. Nothing stops a "
        "caller declaring all four checked when two were skimmed -- the "
        "field records a claim about what was examined, not the examination",
        "THE FOUR SUBJECT CLASSES ARE CARRIED AS DELIVERED AND ARE NOT "
        "PARTITIONS OF ANYTHING. They overlap: a disabled woman is in two, "
        "and the classes as named are not defined against a stated "
        "reference class here at all. The predicate difference needs a "
        "reference class per comparison, and which reference each of the "
        "four is measured against is not settled by this index",
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


def _entry_block(e, L):
    r = e.recurrence()
    L.append("  SHAPE %s" % e.shape_id)
    for line in _wrap(e.description, "    "):
        L.append(line)
    L.append("    bindings:              %d of %d"
             % (r["n_present"], r["n_classes"]))
    L.append("    vocabulary disjoint:   %s" % r["disjoint"])
    if r["vocabulary_overlap"]:
        L.append("    shared words:          %s"
                 % ", ".join(r["vocabulary_overlap"]))
    if r["unchecked"]:
        L.append("    NOT CHECKED:           %d class(es)"
                 % len(r["unchecked"]))
    L.append("    per binding:")
    for c in SUBJECT_CLASSES:
        if c in e.realisations:
            L.append("      %-40s %s"
                     % (c[:40], ", ".join(e.realisations[c])))
        elif c in e.checked_classes:
            L.append("      %-40s (checked, none)" % c[:40])
        else:
            L.append("      %-40s NOT_CHECKED" % c[:40])
    L.append("    VERDICT: %s" % r["verdict"])
    for line in _wrap(r["why"], "      "):
        L.append(line)
    L.append("")


def report():
    L = ["SHAPE INDEX -- one shape, four bindings, different vocabulary",
         "=" * 72, ""]
    L.append("  If the same predicate shape recurs across all four subject")
    L.append("  classes with different vocabulary, that confirms it is a")
    L.append("  structural signature and not four separate literatures.")
    L.append("")
    L.append("  subject classes:")
    for c in SUBJECT_CLASSES:
        L.append("    %s" % c)
    L.append("")
    L.append("-" * 72)
    L.append("")
    L.append("  THE INDEX")
    L.append("")
    ri = real_index()
    L.append("    shapes recorded: %d" % ri["n_shapes"])
    L.append("    corpus:          %s" % ri["corpus"])
    L.append("    state:           %s" % ri["state"])
    L.append("")
    for line in _wrap(ri["why"], "    "):
        L.append(line)
    L.append("")
    L.append("-" * 72)
    L.append("")
    L.append("  THE RECURRENCE TEST, GRADED ON FIXTURES")
    L.append("")
    L.append("  %s" % FIXTURE_NOTE)
    L.append("")
    for e in FIXTURES:
        _entry_block(e, L)
    g = grade()
    L.append("  GRADE: %s   distinct verdicts: %d"
             % (g["grade"], g["n_distinct_verdicts"]))
    L.append("")
    for line in _wrap(g["why"], "  "):
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


def selftest():
    f = k = 0

    def ck(label, cond):
        nonlocal f, k
        k += 1
        if not cond:
            f += 1
            print("FAIL %s" % label)

    ck("all four delivered subject classes are carried",
       len(SUBJECT_CLASSES) == 4 and "women" in SUBJECT_CLASSES)

    try:
        ShapeEntry("x", "d", {SUBJECT_CLASSES[0]: ["w"]},
                   checked_classes=ALL_FOUR, derived_from=None)
        ok = False
    except IndexError_:
        ok = True
    ck("a shape entry records where the shape came from", ok)
    try:
        ShapeEntry("x", "d", {"not a class": ["w"]},
                   checked_classes=ALL_FOUR, derived_from="fx")
        ok = False
    except IndexError_:
        ok = True
    ck("an unknown subject class is refused", ok)
    try:
        ShapeEntry("x", "d", {SUBJECT_CLASSES[0]: ["w"]},
                   checked_classes=[SUBJECT_CLASSES[1]], derived_from="fx")
        ok = False
    except IndexError_:
        ok = True
    ck("a class cannot carry a realisation without having been checked", ok)

    r1 = FX_DISJOINT.recurrence()
    ck("all four classes with disjoint vocabulary is a structural signature",
       r1["verdict"] == "STRUCTURAL_SIGNATURE" and r1["disjoint"] is True)
    r2 = FX_SHARED.recurrence()
    ck("all four classes with ONE shared word is not",
       r2["verdict"] == "SHARED_VOCABULARY")
    ck("and both are present in all four, so a binding count cannot "
       "separate them",
       r1["n_present"] == r2["n_present"] == 4)
    ck("the shared word is named rather than just flagged",
       r2["vocabulary_overlap"] == ["w_common"])
    r3 = FX_PARTIAL.recurrence()
    ck("two of four is NOT_ESTABLISHED even with disjoint vocabulary",
       r3["verdict"] == "NOT_ESTABLISHED" and r3["disjoint"] is True)
    r4 = FX_UNCHECKED.recurrence()
    ck("unchecked classes give NOT_ESTABLISHED, not absence",
       r4["verdict"] == "NOT_ESTABLISHED" and len(r4["unchecked"]) == 2)
    ck("and the unchecked classes are named",
       SUBJECT_CLASSES[2] in r4["unchecked"])

    g = grade()
    ck("the recurrence test grades OK on the fixtures", g["grade"] == "OK")
    ck("and separates three distinct verdicts",
       g["n_distinct_verdicts"] == 3)
    ck("the fixtures are marked synthetic",
       "SYNTHETIC_FIXTURE" in g["fixture_note"])

    ri = real_index()
    ck("the real index is empty and NOT_RUN",
       ri["n_shapes"] == 0 and ri["state"] == "NOT_RUN")
    ck("because no corpus is acquired", ri["corpus"] == "NONE_ACQUIRED")
    ck("and empty is stated as the size of the work, not a finding",
       "not a finding that no shape recurs" in ri["why"])

    ck("the shared-vocabulary result leads the breaks list",
       "WEAKER THAN PARTIAL" in breaks()[0])
    ck("the empty index being not-a-finding is disclosed",
       any("SIZE OF THE WORK DONE" in b for b in breaks()))
    ck("the format being inferred is disclosed",
       any("FORMAT IS AN INFERENCE" in b for b in breaks()))
    ck("the classes overlapping, and no reference class being settled, is "
       "disclosed",
       any("NOT PARTITIONS OF ANYTHING" in b for b in breaks()))
    ck("confidence unresolved", confidence()["resolved"] is False)
    ck("report renders", "THE RECURRENCE TEST, GRADED" in report())
    print("%d/%d checks passed" % (k - f, k))
    return 1 if f else 0


def main():
    ap = argparse.ArgumentParser(description="shape index")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    print(report())
    return 0


if __name__ == "__main__":
    sys.exit(main())
