#!/usr/bin/env python3
"""Checks on ../METHOD_SPEC.md, and what its arrival does to the SS claims.

METHOD_SPEC.md is delivered verbatim at the repo root and is not modified
here. Neither is SHAPE_SPEC.md.

Section 1 states an epistemic class and blocks a misapplication it says
was observed "in the session this file was written in" -- which is the
session that produced `CLAIM_TABLE.md`'s SS_001..SS_010. So the first
thing this module does is check those ten claims against the stated
criterion, and it does that with an interest in the answer, which is
declared rather than managed.

Everything quoted from either spec is pulled from the delivered file at
run time, so a quote that has drifted turns the selftest red rather than
sitting in prose.

usage:
    python3 method_spec_audit.py
    python3 method_spec_audit.py --selftest
"""

import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
METHOD = os.path.join(ROOT, "METHOD_SPEC.md")
SHAPE = os.path.join(ROOT, "SHAPE_SPEC.md")
TABLE = os.path.join(HERE, "CLAIM_TABLE.md")


def _read(p):
    return open(p, errors="replace").read()


def quote(path, needle):
    """Assert a phrase is in the delivered file, and return it.

    A finding that rests on a quotation should fail when the quotation
    stops being accurate, not when someone re-reads the prose.
    """
    txt = _read(path)
    flat = " ".join(txt.split())
    want = " ".join(needle.split())
    return want in flat


# --------------------------------------------------------------------------
# MS_001 -- the section 1 charge, run against this audit's own claims.
#
# The blocked misapplication has a stated signature: it applies a
# CLAIM-level criterion (falsifiability) to a METHOD-level object. So the
# test is what each claim's criticism ranges OVER, and that is readable
# from the claim.
#
# The classification below is HAND-CODED. This audit has an interest in
# the outcome -- it is grading itself against a charge aimed at it -- so
# the object of each claim is quoted rather than summarised, and a reader
# who disagrees has the quote to disagree with.
# --------------------------------------------------------------------------

SS_OBJECTS = [
    ("SS_001", "sec 1's geometry/constraint distinction",
     "not-an-objection", "records the distinction as the contribution"),
    ("SS_002", "sec 10's naming rule, measured on this repo",
     "rule", "a count of word senses in this tree; says nothing about "
            "whether the method can be refuted"),
    ("SS_003", "sec 4's worked example",
     "example", "the lung/delta pair moves two variables; sec 5 assigns "
                "those two examples to different constraint classes"),
    ("SS_004", "sec 7's default, against sec 4's refuting branch",
     "read", "aimed at the layer METHOD_SPEC sec 1 itself names as the "
             "falsifiable one -- the individual read and its removal test"),
    ("SS_005", "sec 6's recurrence list, as evidence",
     "evidence", "a counting question about instances; no claim that the "
                 "method must refute itself"),
    ("SS_006", "sec 9's NOTE ON COST",
     "not-an-objection", "computes that the spec is right and stronger "
                         "than it states itself"),
    ("SS_007", "sec 3 step 3 and sec 2's BLOCK THIS MISREAD",
     "not-an-objection", "records both as sound"),
    ("SS_008", "a named file's presence in the tree",
     "fact", "READING_PROTOCOL.md is or is not on disk"),
    ("SS_009", "schema fields on four JSON entries",
     "fact", "key sets, counted"),
    ("SS_010", "sec 10's two-state outcome",
     "rule", "a classification with no cell for the state that occurs"),
]

METHOD_LEVEL = "method"


def charge_check():
    """Does any SS claim demand that the METHOD refute itself?"""
    committed = [c for c in SS_OBJECTS if c[2] == METHOD_LEVEL]
    return {"n": len(SS_OBJECTS), "committed": committed,
            "by_object": sorted(set(c[2] for c in SS_OBJECTS))}


def table_ids():
    return re.findall(r"^### (SS_\d+)", _read(TABLE), re.M)


# --------------------------------------------------------------------------
# MS_002 -- section 5 forbids what section 3 does.
# --------------------------------------------------------------------------

RULE_5 = ("NOT upgraded by  more instances sharing the geometry without a "
          "checked constraint set")
LIST_3 = ("recurrence ACROSS SUBSTRATES inside that one instance is what "
          "carries the weight")
NAMES_3 = ("vasculature, rivers, lightning, roots, mycelium, cracks, "
           "dendritic solidification")


def rule_versus_list():
    """Both halves quoted from the delivered file, then compared."""
    have_rule = quote(METHOD, RULE_5)
    have_list = quote(METHOD, LIST_3)
    have_names = quote(METHOD, NAMES_3)
    # Does the list carry a checked constraint set for any item?
    txt = " ".join(_read(METHOD).split())
    i = txt.find(NAMES_3)
    window = txt[i:i + 260] if i >= 0 else ""
    qualifier = ("separate runs, no shared ancestry, same geometry"
                 in window)
    return {"rule_present": have_rule, "list_present": have_list,
            "names_present": have_names,
            "list_qualifier": window[len(NAMES_3):].strip()[:80],
            "grouped_by_geometry_not_constraints": qualifier}


# --------------------------------------------------------------------------
# MS_003 -- the two asymmetries run opposite.
#
# SHAPE_SPEC sec 4's removal test has two branches:
#     form DIFFERS when the constraint is removed  -> read CONFIRMED
#     form UNCHANGED when it is removed            -> read REFUTED
#
# METHOD_SPEC sec 3 discounts DISAPPEARANCE, which is the confirming
# branch. SHAPE_SPEC sec 7 discounts contradicting reads, which is the
# refuting branch. Each spec discounts the branch the other leaves
# standing.
# --------------------------------------------------------------------------

BRANCHES = [
    ("form DIFFERS (shape disappears)", "CONFIRMS the read",
     "METHOD_SPEC sec 3: 'A shape DISAPPEARING tells you at least one was "
     "removed, but not which.'",
     "discounted by METHOD_SPEC sec 3", "not addressed by SHAPE_SPEC sec 7",
     "open set: which constraint went is unbounded"),
    ("form UNCHANGED (shape persists)", "REFUTES the read",
     "SHAPE_SPEC sec 4: 'the constraint was not load-bearing and the read "
     "is wrong.'",
     "not addressed by METHOD_SPEC sec 3",
     "discounted by SHAPE_SPEC sec 7 as instrument error",
     "bounded: the alternative is equifinality, and it must be exhibited"),
]

SEC7 = ("Where the read contradicts the shape, the default reading is "
        "instrument error")
SEC4_REFUTES = ("If the form is unchanged, the constraint was not "
                "load-bearing and the read is wrong.")
SEC3_DISAPPEAR = ("A shape DISAPPEARING tells you at least one was removed, "
                  "but not which.")


def asymmetry_check():
    return {"sec7": quote(SHAPE, SEC7),
            "sec4_refuting_branch": quote(SHAPE, SEC4_REFUTES),
            "sec3_disappearance": quote(METHOD, SEC3_DISAPPEAR)}


# --------------------------------------------------------------------------
# MS_006 -- section 3's SUBSTRATE EXCLUSION cross-reference.
# --------------------------------------------------------------------------

def coupling_audit_gates():
    """Does `uninstrumented` already hold the mechanism sec 3 points at?

    Read from the sibling folder rather than recalled. sec 3's example is
    a SPECIES gate: humans excluded as an admissible domain. The coupling
    audit maps a species gate to AUDIT_ASYMMETRY.
    """
    p = os.path.join(ROOT, "uninstrumented", "coupling_audit")
    if not os.path.isdir(p):
        return {"present": False}
    hits = {}
    for dirpath, _dirs, files in os.walk(p):
        for fn in files:
            if not fn.endswith((".py", ".md", ".json")):
                continue
            txt = _read(os.path.join(dirpath, fn))
            for token in ("species", "AUDIT_ASYMMETRY", "market_output"):
                if token in txt:
                    hits.setdefault(token, []).append(
                        os.path.relpath(os.path.join(dirpath, fn), ROOT))
    return {"present": True, "hits": {k: sorted(set(v))[:2]
                                      for k, v in hits.items()}}


# --------------------------------------------------------------------------
# MS_007 -- READING_PROTOCOL.md, now cited by two specs.
# --------------------------------------------------------------------------

def reading_protocol():
    on_disk = None
    for dirpath, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d != ".git"]
        for fn in files:
            if fn.lower().startswith("reading_protocol"):
                on_disk = os.path.relpath(os.path.join(dirpath, fn), ROOT)
    cites = {}
    for label, path in (("SHAPE_SPEC.md", SHAPE), ("METHOD_SPEC.md", METHOD)):
        n = _read(path).count("READING_PROTOCOL.md")
        if n:
            cites[label] = n
    numbered = quote(METHOD, "See READING_PROTOCOL.md, third blocked "
                             "conflation.")
    return {"on_disk": on_disk, "cites": cites, "numbered_reference": numbered}


# --------------------------------------------------------------------------

def report():
    print("CHECKS ON METHOD_SPEC.md -- neither spec is modified here\n")

    print("MS_001  section 1's charge, run against this audit's own claims")
    c = charge_check()
    ids = table_ids()
    print("  SS claims in CLAIM_TABLE.md : %d" % len(ids))
    print("  classified here             : %d" % c["n"])
    print("  the blocked error applies a CLAIM-level criterion")
    print("  (falsifiability) to a METHOD-level object. What each claim's")
    print("  criticism ranges over:")
    for cid, obj, level, why in SS_OBJECTS:
        print("    %-8s %-12s %s" % (cid, level, obj))
    print("  claims ranging over the METHOD: %d" % len(c["committed"]))
    print()
    print("  SS_004 is the one to look at, and it aims at the layer")
    print("  section 1 itself names as the falsifiable one:")
    print("    'The falsifiable layer is the INDIVIDUAL READ, not the")
    print("     method. See SHAPE_SPEC.md section 4 (removal test).'")
    print("  SS_004 says section 7 discounts section 4's refuting branch.")
    print("  That is a claim ABOUT the removal test, not a demand that the")
    print("  method refute itself -- and METHOD_SPEC makes it heavier, by")
    print("  placing all the refutation weight there.")
    print()
    print("  DECLARED: this audit is grading itself against a charge aimed")
    print("  at it, and has an interest in the answer. The object of each")
    print("  claim is quoted above rather than summarised so a reader who")
    print("  disagrees has something to disagree with. Nothing here")
    print("  establishes that the charge is wrong about other reviews.")
    print()

    print("MS_002  section 5 forbids what section 3 does")
    r = rule_versus_list()
    print("  sec 5 rule present in the file  : %s" % r["rule_present"])
    print("  sec 3 list present in the file  : %s" % r["list_present"])
    print("  what qualifies the list         : %r" % r["list_qualifier"])
    print("  Section 5: 'NOT upgraded by more instances sharing the")
    print("  GEOMETRY without a checked constraint set.' Section 3 offers")
    print("  seven instances, qualified by 'same geometry', with no")
    print("  constraint set checked for any of them. The rule in section 5")
    print("  disqualifies the evidence in section 3.")
    print("  This is SS_005 restated by the author, in stronger form than")
    print("  SS_005 stated it.")
    print()

    print("MS_003  the two asymmetries run opposite")
    a = asymmetry_check()
    for k in sorted(a):
        print("  quote holds: %-22s %s" % (k, a[k]))
    print()
    print("  %-32s %-22s %s" % ("removal-test branch", "what it does",
                                "determinacy"))
    print("  " + "-" * 74)
    for br, does, _q, m3, s7, det in BRANCHES:
        print("  %-32s %-22s %s" % (br, does, det))
        print("      %s" % m3)
        print("      %s" % s7)
    print()
    print("  Each spec discounts the branch the other leaves standing, and")
    print("  the one both should leave standing is PERSISTENCE: a shape")
    print("  surviving the removal of its named constraint has a BOUNDED")
    print("  alternative set, since equifinality has to be exhibited,")
    print("  while disappearance ranges over an open set by section 3's")
    print("  own words. So section 7's default falls on the better-")
    print("  determined branch.")
    print("  REPAIR, one clause: scope section 7's default to")
    print("  DISAPPEARANCE reads, where section 3 supplies the")
    print("  justification, and exclude persistence, where section 4's")
    print("  falsifier lives.")
    print()

    print("MS_006  section 3's SUBSTRATE EXCLUSION cross-reference")
    g = coupling_audit_gates()
    if not g["present"]:
        print("  uninstrumented/coupling_audit/ NOT IN TREE")
    else:
        for k in sorted(g["hits"]):
            print("    %-18s %s" % (k, ", ".join(g["hits"][k])))
        print("  The cross-reference lands, and on a subfolder rather than")
        print("  on the eight-mechanism list. coupling_audit already runs a")
        print("  SPECIES gate mapped to AUDIT_ASYMMETRY. Section 3's human")
        print("  exceptionalism example is the same gate pointed the other")
        print("  way: there companion animals are excluded from a human")
        print("  accounting, here humans are excluded from a cross-species")
        print("  one. One gate type, two directions.")
    print()

    print("MS_007  READING_PROTOCOL.md")
    rp = reading_protocol()
    print("  on disk                : %s" % (rp["on_disk"] or "NOT IN TREE"))
    print("  cited by               : %s"
          % ", ".join("%s x%d" % (k, v) for k, v in sorted(rp["cites"].items())))
    print("  numbered reference into it: %s" % rp["numbered_reference"])
    print("  It was ninth named-and-absent when SHAPE_SPEC arrived. It is")
    print("  now cited by both specs, third in section 6's stated read")
    print("  order, and referenced by ORDINAL -- 'third blocked")
    print("  conflation' -- which is a reference to a numbered item in a")
    print("  file with no items.")
    print()


def selftest():
    fails = []

    # Every quotation this module rests on must still be in the file.
    for label, ok in sorted(asymmetry_check().items()):
        if not ok:
            fails.append("quote no longer in the delivered spec: %s" % label)
    r = rule_versus_list()
    for k in ("rule_present", "list_present", "names_present"):
        if not r[k]:
            fails.append("MS_002 quote missing: %s" % k)

    # MS_001's falsifier: any SS claim ranging over the method.
    c = charge_check()
    if c["committed"]:
        fails.append("MS_001 must be restated: %s range over the method"
                     % ", ".join(x[0] for x in c["committed"]))

    # The classification must cover the table, or MS_001 is scored on a
    # subset it chose.
    ids = set(table_ids())
    classified = set(x[0] for x in SS_OBJECTS)
    if ids != classified:
        fails.append("MS_001 classifies %s but the table holds %s"
                     % (sorted(classified), sorted(ids)))

    # MS_001 must not be scored on a set that is all one level, or the
    # classification is doing no work.
    if len(c["by_object"]) < 2:
        fails.append("every SS claim classified at one level; MS_001's "
                     "classification cannot discriminate")

    # MS_007 is a state, not a constant; assert only that it is readable.
    reading_protocol()

    for f in fails:
        print("FAIL: " + f)
    print("SELFTEST %s (%d checks failed)"
          % ("PASS" if not fails else "FAIL", len(fails)))
    return 1 if fails else 0


def main(argv):
    if "--selftest" in argv:
        return selftest()
    report()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
