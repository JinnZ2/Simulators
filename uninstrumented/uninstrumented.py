"""
uninstrumented.py -- the registry from README.md, as code, plus three checks
on the registry itself.

CC0-1.0. Standard library only. Deterministic.

A gap is an oversight. These are exclusions built into the apparatus before
the first reading is taken. Seven entries, seven mechanisms, sorted by
mechanism so a case from evolutionary biology sits next to one from survey
methodology and is recognizably the same failure.

Every entry is a QUESTION until something measures it. Nothing here is a
position under defense.

THE THREE CHECKS

  1  does the mechanism partition actually cut across the field partition?
     If sorting by mechanism groups the same fields together, the sort buys
     nothing and field would do.

  2  are the mechanisms mutually exclusive? Hand-adjudicated per entry.
     They are not, and the multiplicity is reported rather than resolved --
     which one an entry is filed under decides what comparison case it sits
     next to, so the filing is a choice and should be visible as one.

  3  can the registry be wrong? Every delivered entry states high confidence
     on the exclusion. A list that only ever admits entries is
     CONSTANT_FIRES in the ../null-harness/ sense. Section 3 runs the six
     instruments graded in ../instrument-epistemology/ against the mechanism
     set as a known-null corpus: they are real instruments with real
     transduction chains, three of them graded "mostly assumed", and NONE of
     them should file here -- weak grounding is not constitutive exclusion.
"""

from __future__ import annotations

RULE = "=" * 72

# Closed vocabulary. Same discipline as ../measurement-fork/quantities.py:
# an entry whose mechanism is not on this list does not get constructed.
MECHANISMS = (
    "MODALITY",             # apparatus in the wrong channel
    "STORAGE",              # medium cannot hold the shape
    "SCALAR_DEMAND",        # function collapsed to a number
    "BUDGET_BOUNDARY",      # closed budget compared to open
    "AUTHORED_REFERENCE",   # reference produced by the measured party
    "AUDIT_ASYMMETRY",      # guard fires on one side only
    "SCORED_AS_WASTE",      # component read as cost by the instrument's own
                            # accounting
)

MECHANISM_GLOSS = {
    "MODALITY": "apparatus in the wrong channel",
    "STORAGE": "medium cannot hold the shape",
    "SCALAR_DEMAND": "function collapsed to a number",
    "BUDGET_BOUNDARY": "closed budget compared to open",
    "AUTHORED_REFERENCE": "reference produced by the measured party",
    "AUDIT_ASYMMETRY": "guard fires on one side only",
    "SCORED_AS_WASTE": "component read as cost by the instrument's own "
                       "accounting",
}


def entry(quantity, excluded_by, visible_as, would_measure, confidence,
          field, note=None, worked_in=None):
    """
    quantity       what would be measured
    excluded_by    what in the instrument's constitution prevents it
    visible_as     how the absence currently reads
    would_measure  the design, if one exists yet
    confidence     stated gradient, recorded verbatim and not adjudicated
    field          domain of origin -- used only by check 1
    note           optional
    worked_in      where in this repo the case is already worked, if it is
    """
    if excluded_by not in MECHANISMS:
        raise ValueError("excluded_by must be one of %r, got %r"
                         % (MECHANISMS, excluded_by))
    return {
        "quantity": quantity,
        "excluded_by": excluded_by,
        "visible_as": visible_as,
        "would_measure": would_measure,
        "confidence": confidence,
        "field": field,
        "note": note,
        "worked_in": worked_in,
    }


ENTRIES = (
    entry(
        quantity="capability in a non-human configuration",
        excluded_by="MODALITY",
        visible_as="absence of capability",
        would_measure=("bidirectional protocol; each side sets tasks in its "
                       "own modality"),
        confidence="high on the exclusion, unmeasured on magnitude",
        field="animal cognition",
    ),
    entry(
        quantity=("calibration between one body and one environment "
                  "(creek crossing: surface pattern -> force, at "
                  "temperature, at season, plus the dry-arrival sequence)"),
        excluded_by="STORAGE",
        visible_as='"no literature exists"',
        would_measure=("reconstruction-and-correction capture; the "
                       "correction is the product"),
        confidence=("high. The absence is a property of the medium, not of "
                    "the knowledge."),
        field="tacit skill",
        worked_in="../inverseminar/ ; ../anchor-interval/ ANC_011",
    ),
    entry(
        quantity=("response as a function over situations "
                  "(empathy(framework, target, aspect))"),
        excluded_by="SCALAR_DEMAND",
        visible_as=("middling score, indistinguishable from flat moderate "
                    "response"),
        would_measure=("one added field: how determinate was this item for "
                       "you, and what did you assume to answer it"),
        confidence=("high on mechanism. Cognitive-interview work already "
                    "demonstrates the discard."),
        field="survey methodology",
    ),
    entry(
        quantity=("efficiency under a closed budget (tree: fabrication, "
                  "repair, replication, disposal all inside)"),
        excluded_by="BUDGET_BOUNDARY",
        visible_as="the tree is inefficient at photosynthesis",
        would_measure=("W14 BUDGET CLOSURE -- name every input and disposal "
                       "path, which side of the line, and who set the line"),
        confidence="high",
        field="energy accounting",
        worked_in="../declared-frame/ DF_005, DF_007 ; K18 in "
                  "../measurement-fork/",
    ),
    entry(
        quantity="model drift",
        excluded_by="AUTHORED_REFERENCE",
        visible_as="a number attributed to the model",
        would_measure=("fixed old benchmark scored alongside the "
                       "contemporary one; divergence isolates the criteria "
                       "term"),
        confidence="high on structure. Sign unrecoverable from inside.",
        field="ML evaluation",
        note=("seven terms move between releases; one is reported. Contrast "
              "case: CASP -- blind, periodic, externally referenced, "
              "reference cannot be edited from inside."),
        worked_in="../anchor-interval/moving_reference.py ; ANC_005..008",
    ),
    entry(
        quantity=("practice rate during the stable interval (play, "
                  "exploration, off-hours kinesthetic practice, the "
                  "crossing when nothing is at stake)"),
        excluded_by="SCORED_AS_WASTE",
        visible_as=("expenditure with zero return; rest reclassified from "
                    "practice"),
        would_measure=("K14 / K15 / K16 with the mediation prediction and "
                       "lag order"),
        confidence="high on the mechanism. Decay rate unmeasured.",
        field="behavioural ecology / industrial skill",
        worked_in="../measurement-fork/ K14-K16, MF_014, MF_015",
    ),
    entry(
        quantity="reliability of an account",
        excluded_by="AUDIT_ASYMMETRY",
        visible_as="neutrality",
        would_measure=("count caveats issued per account type across a "
                       "transcript corpus; the ratio is the measurement"),
        confidence="high. Observed directly, this session.",
        field="model behaviour",
        note=("the guard fires on surface features -- a named dispute, a "
              "person reporting. The institutional account presents no such "
              "surface, so it is absorbed uncaveated. Filter strength "
              "scales with distance from corpus, which is the same variable "
              "as novelty."),
    ),
)


# ---------------------------------------------------------------------------


def section(title: str) -> None:
    print("\n" + RULE)
    print(title)
    print(RULE)


def wrap(text, indent, width=62):
    words, lines, cur = str(text).split(), [], ""
    for w in words:
        if len(cur) + len(w) + 1 > width:
            lines.append(" " * indent + cur)
            cur = w
        else:
            cur = (cur + " " + w).strip()
    if cur:
        lines.append(" " * indent + cur)
    return lines


def register() -> None:
    section("THE REGISTER, sorted by mechanism")
    for m in MECHANISMS:
        rows = [e for e in ENTRIES if e["excluded_by"] == m]
        if not rows:
            continue
        print("\n  %s -- %s" % (m, MECHANISM_GLOSS[m]))
        for e in rows:
            print()
            for label, key in (("QUANTITY", "quantity"),
                               ("VISIBLE AS", "visible_as"),
                               ("WOULD MEASURE", "would_measure"),
                               ("CONFIDENCE", "confidence")):
                body = wrap(e[key], 20)
                print("    %-15s%s" % (label, body[0].strip()))
                for line in body[1:]:
                    print(line)
            if e["note"]:
                body = wrap(e["note"], 20)
                print("    %-15s%s" % ("NOTE", body[0].strip()))
                for line in body[1:]:
                    print(line)
            if e["worked_in"]:
                print("    %-15s%s" % ("WORKED IN", e["worked_in"]))


# ---------------------------------------------------------------------------
# 1  does the mechanism sort buy anything


def check_cross_domain() -> None:
    section("1  does sorting by mechanism cut across field?")

    print("  The register's stated reason for sorting by mechanism rather")
    print("  than by field: it lets a case from evolutionary biology sit")
    print("  next to one from survey methodology and be recognizably the")
    print("  same failure. That is checkable.\n")

    print("  %-22s %-34s" % ("mechanism", "field"))
    print("  " + "-" * 58)
    for e in ENTRIES:
        print("  %-22s %-34s" % (e["excluded_by"], e["field"]))

    fields = {e["field"] for e in ENTRIES}
    mechs = {e["excluded_by"] for e in ENTRIES}
    print()
    print("  %d entries, %d distinct fields, %d distinct mechanisms"
          % (len(ENTRIES), len(fields), len(mechs)))
    collisions = [m for m in mechs
                  if len({e["field"] for e in ENTRIES
                          if e["excluded_by"] == m}) > 1]
    print("  mechanisms holding more than one field: %d" % len(collisions))
    print()
    print("  At one entry per mechanism the two partitions are identical and")
    print("  the sort is UNTESTED, not confirmed. It buys nothing until a")
    print("  second entry lands under an existing mechanism from a different")
    print("  field.")
    print()
    print("  Nearest candidate already in the repo: MODALITY currently holds")
    print("  animal cognition. ../reasoning-dial/ RD_009's G-STATE gap -- a")
    print("  self-report from a miscalibrated observer is the quantity in")
    print("  question -- is a different field with arguably the same shape.")
    print("  Filing it would be the first real test of the sort.")


# ---------------------------------------------------------------------------
# 2  are the mechanisms mutually exclusive


# Hand-adjudicated: which OTHER mechanisms also have a claim on each entry.
# Same method as ../measurement-fork/residual_audit.py -- read the case, mark
# it, show the working.
ALSO_APPLIES = {
    "capability in a non-human configuration": [
        ("SCALAR_DEMAND", "the tasks are scored on a human-derived scale, "
                          "so a different competence integrates to a low "
                          "number rather than to no number"),
    ],
    "reliability of an account": [
        ("AUTHORED_REFERENCE", "the corpus that sets what counts as a "
                               "normal account was produced by the side "
                               "that goes unaudited"),
    ],
    "model drift": [
        ("AUDIT_ASYMMETRY", "the contemporary benchmark is not checked "
                            "against the fixed one, only the reverse"),
    ],
    "practice rate during the stable interval (play, exploration, "
    "off-hours kinesthetic practice, the crossing when nothing is at "
    "stake)": [
        ("BUDGET_BOUNDARY", "the return falls outside the sampling window, "
                            "which is a boundary placed in time rather than "
                            "in space"),
    ],
}


def check_exclusivity() -> None:
    section("2  the mechanisms are not mutually exclusive")

    multi = 0
    for e in ENTRIES:
        also = ALSO_APPLIES.get(e["quantity"], [])
        tag = "%d" % (1 + len(also))
        multi += bool(also)
        print("\n  [%s applicable] %s" % (tag, e["excluded_by"]))
        for line in wrap(e["quantity"], 6):
            print(line)
        for m, why in also:
            print("      also %s:" % m)
            for line in wrap(why, 10):
                print(line)

    print()
    print("  %d of %d entries have more than one mechanism with a claim."
          % (multi, len(ENTRIES)))
    print()
    print("  This is not a defect to resolve by tightening definitions. The")
    print("  filing decides what comparison case an entry sits next to, and")
    print("  that is the register's whole function -- so the filing is a")
    print("  CHOICE and should be visible as one. Two entries filed under")
    print("  different mechanisms that share a second mechanism are a pair")
    print("  the sort did not surface.")
    print()
    print("  Minimal repair, and it changes the schema: carry excluded_by as")
    print("  a PRIMARY plus a list, and sort under all of them. The cost is")
    print("  that an entry then appears more than once, which is the correct")
    print("  cost -- it is in more than one place.")


# ---------------------------------------------------------------------------
# 3  can the register be wrong


# Known-null corpus: the six instruments graded in
# ../instrument-epistemology/outputs/cross-instrument-report.md. All six are
# real instruments with real transduction chains. Three are graded "mostly
# assumed". None should file here, because weak grounding is not
# constitutive exclusion -- the quantity IS reached, imprecisely.
NULL_CORPUS = (
    ("broadband seismometer network", 0.800, "well grounded"),
    ("satellite thermal IR radiometer", 0.504, "partially grounded"),
    ("airborne LiDAR biomass", 0.514, "partially grounded"),
    ("camera trap array", 0.293, "mostly assumed"),
    ("IRMS + isotopic mixing model", 0.275, "mostly assumed"),
    ("eDNA metabarcoding assay", 0.165, "mostly assumed"),
)

# Hand adjudication: does any mechanism in MECHANISMS have a claim on it?
NULL_VERDICT = {
    "broadband seismometer network": (None, "measurand unobservable, chain "
                                            "long, model in the loop -- and "
                                            "reached, via traceable "
                                            "standards. No mechanism fires."),
    "satellite thermal IR radiometer": (None, "M3, heavily model-dependent. "
                                              "Model dependence is not on "
                                              "the list and should not be."),
    "airborne LiDAR biomass": (None, "allometry is a bridge model with "
                                     "known domain limits. Weak grounding."),
    "camera trap array": (None, "detection probability is estimated rather "
                                "than measured. Weak grounding."),
    "IRMS + isotopic mixing model": (None, "mixing model underdetermined. "
                                           "Weak grounding, and the "
                                           "underdetermination is REPORTED."),
    "eDNA metabarcoding assay": (None, "fidelity 0.165, four blind spots. "
                                       "Still not excluded -- the quantity "
                                       "is reached badly, and every step is "
                                       "named in its own blindness map."),
}


def check_null() -> None:
    section("3  known-null corpus: does anything file that should not?")

    print("  Every entry in the register states high confidence on the")
    print("  exclusion. A list that only ever admits entries is")
    print("  CONSTANT_FIRES in the ../null-harness/ sense, and the doc's own")
    print("  first line -- 'not a gap log' -- is a rule the structure does")
    print("  not enforce.\n")
    print("  Null corpus: the six instruments graded in")
    print("  ../instrument-epistemology/. Real apparatus, real chains,")
    print("  three of them graded 'mostly assumed'. None should file here.\n")

    print("  %-34s %-10s %-16s %s"
          % ("instrument", "fidelity", "verdict there", "files here?"))
    print("  " + "-" * 72)
    fires = 0
    for name, fid, verdict in NULL_CORPUS:
        mech, _ = NULL_VERDICT[name]
        fires += mech is not None
        print("  %-34s %-10.3f %-16s %s"
              % (name, fid, verdict, mech or "no"))

    print()
    print("  false entries: %d of %d" % (fires, len(NULL_CORPUS)))
    print()
    for name, _, _ in NULL_CORPUS:
        _, why = NULL_VERDICT[name]
        print("    %s" % name)
        for line in wrap(why, 8):
            print(line)
    print()
    print("  So the mechanism set discriminates on this corpus. The line it")
    print("  holds is exactly the one the doc states:\n")
    print("      weak grounding      the quantity is reached, badly")
    print("      constitutive        the quantity cannot appear at all,")
    print("      exclusion           and the apparatus is why\n")
    print("  eDNA at 0.165 is the hardest case and it stays out. Every step")
    print("  of its chain is named in its own blindness map, which is what a")
    print("  reached-but-badly quantity looks like. An excluded one has no")
    print("  blindness map, because the exclusion happens before the map is")
    print("  drawn.")
    print()
    print("  What this does NOT establish: that the register has a reachable")
    print("  fire branch on a case someone would actually bring. The null")
    print("  corpus is six cases chosen because they are well documented,")
    print("  not because they are near the boundary. The near-boundary test")
    print("  is a quantity a field believes it measures and does not, and")
    print("  none of the seven entries is currently contested by anyone.")


# ---------------------------------------------------------------------------


def main() -> None:
    print()
    print("UNINSTRUMENTED -- %d entries, %d mechanisms"
          % (len(ENTRIES), len(MECHANISMS)))
    print("every entry is a question until something measures it")

    register()
    check_cross_domain()
    check_exclusivity()
    check_null()

    section("READING")
    print("""
  The register holds. Seven mechanisms, a closed vocabulary, and the
  entry structure separates the stated confidence from the shape so the
  two can move independently.

  Three results on the register itself, none of them fatal and all of
  them structural:

  The mechanism sort is UNTESTED rather than confirmed. At one entry per
  mechanism the mechanism partition and the field partition are the same
  partition, so nothing yet demonstrates the cross-domain grouping the
  sort exists for.

  The mechanisms are not mutually exclusive -- 4 of 7 entries have a
  second mechanism with a claim. The filing decides which comparison case
  an entry sits next to, so it is a choice and should carry a primary
  plus a list.

  On a known-null corpus of six externally graded instruments, nothing
  files that should not, including eDNA at fidelity 0.165. The line
  between weak grounding and constitutive exclusion holds: a reached-
  but-badly quantity has a blindness map, an excluded one does not,
  because the exclusion happens before the map is drawn.
""")


if __name__ == "__main__":
    main()
