#!/usr/bin/env python3
# coding.py -- CC0, stdlib only, phone-buildable, parses under 3.9
#
# The coding scheme for Arm 1. The drop's ask is "a reading room and a
# coding scheme, nothing else". This is the second half. The first half
# is not available here and is not substituted for.
#
# NO INSTRUMENT IS CODED IN THIS FOLDER.
#
#   Every published family-functioning, parenting-capacity and
#   child-welfare host tested from this environment refuses CONNECT
#   (measured, see AUDIT_NOTES). Inventing items and coding them would
#   produce an E-fraction table that reads as a result about real
#   statutory instruments -- tools that carry weight in decisions about
#   real families. That is the one thing this folder will not do.
#
#   The fixtures below are AUTHORED HERE to exercise the coder. Ground
#   truth for them lives in how they were written, never in what the
#   coder says about them, and every one is labelled.
#
# THE SCHEME'S ONE SUBSTANTIVE CHANGE TO THE DELIVERED DESIGN
#
#   LOCUS as delivered has four codes and X is "external condition coded
#   AS a personal property". Given an item, separating P from X takes a
#   judgment about whether the underlying variable is externally caused
#   -- a claim about the world, not a property of the text. So X-fraction
#   as delivered is the coder's attribution rather than a measurement of
#   the instrument.
#
#   Here LOCUS is DERIVED from two declared fields that can be disagreed
#   with independently:
#
#     subject_class    mechanical, from the item's own grammatical
#                      subject. Recomputable by anyone holding the text.
#     externally_caused declared per item with a stated basis. The
#                      causal claim, visible as one.
#
#   X = subject is a person AND externally_caused is declared true.
#   Nothing hand-sets a locus; the selftest asserts it.

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
_NIC = os.path.join(os.path.dirname(HERE), "nonidentity-census")

# Imported, not reimplemented. `subject_span` and `head_noun` were built
# for research-claim subjects and work unmodified on instrument-item
# wording. Their documented limit travels with them: the mapping from a
# head noun to a class is a word list, which is nonidentity-census T1-1.
# That limit is why the causal field is kept separate -- a word list over
# grammatical subjects is a far smaller and more inspectable judgment
# than a claim about what causes housing instability.


def _extractor():
    if _NIC not in sys.path:
        sys.path.insert(0, _NIC)
    import t1_predicate_unit
    return t1_predicate_unit


# ------------------------------------------------------------- the codes

P = "P"                      # property of a person
H = "H"                      # property of household interaction
E = "E"                      # property of conditions outside the household
X = "X"                      # external condition coded AS a personal property
UNCLASSIFIED = "UNCLASSIFIED"
LOCUS_CODES = (P, H, E, X, UNCLASSIFIED)

PERSON = "PERSON"
HOUSEHOLD = "HOUSEHOLD"
CONDITION = "CONDITION"
SUBJECT_CLASSES = (PERSON, HOUSEHOLD, CONDITION, UNCLASSIFIED)

NOT_DECLARED = "NOT_DECLARED"

EXPLAINS = "EXPLAINS"
CO_OCCURS = "CO_OCCURS"
DIRECTIONALITY = (EXPLAINS, CO_OCCURS, NOT_DECLARED)

EXTERNAL = "EXTERNAL"
ACTION_TARGETS = (PERSON, HOUSEHOLD, EXTERNAL, NOT_DECLARED)

MANDATORY = "MANDATORY"
DISCRETIONARY = "DISCRETIONARY"
NONE = "NONE"
ATTENUATION = (MANDATORY, DISCRETIONARY, NONE, NOT_DECLARED)

# [CHOICE] The head-noun word lists. Small, inspectable, and the whole
# mechanical half of the scheme. A head noun outside all three returns
# UNCLASSIFIED and is never forced -- the drop asks for exactly that.
_PERSON_NOUNS = {
    "caregiver", "caregivers", "parent", "parents", "mother", "father",
    "guardian", "adult", "carer", "respondent", "child", "youth",
    "she", "he", "they",
}
_HOUSEHOLD_NOUNS = {
    "household", "family", "home", "members", "relationships",
    "communication", "conflict", "routine", "routines", "roles",
}
_CONDITION_NOUNS = {
    "schedule", "shift", "employment", "housing", "tenancy", "rent",
    "benefit", "benefits", "income", "debt", "transport", "transit",
    "service", "utilities", "utility", "distance", "wait", "waitlist",
    "policy", "eviction", "hours", "notice",
}


def subject_class(text):
    """PERSON | HOUSEHOLD | CONDITION | UNCLASSIFIED, from the item's own
    grammatical subject. Mechanical and recomputable."""
    T = _extractor()
    span, _rest = T.subject_span(text)
    head = T.head_noun(span)
    if not head:
        return UNCLASSIFIED, None
    if head in _PERSON_NOUNS:
        return PERSON, head
    if head in _HOUSEHOLD_NOUNS:
        return HOUSEHOLD, head
    if head in _CONDITION_NOUNS:
        return CONDITION, head
    return UNCLASSIFIED, head


# --------------------------------------------------------------- an item

def item(ref, text=None, externally_caused=NOT_DECLARED, cause_basis=None,
         directionality=NOT_DECLARED, action_target=NOT_DECLARED,
         attenuation=NOT_DECLARED, subject_class_override=None,
         override_reason=None):
    """One coded item.

    `text` is OPTIONAL and `ref` is not. Item wording in many published
    instruments is licensed rather than free, so an audit that publishes
    its working data would reproduce licensed content. An item can
    therefore be coded by reference with the subject class declared and
    the text withheld -- see the note in AUDIT_NOTES on what that costs.

    `externally_caused` takes True or False only WITH a basis. A causal
    claim with no stated basis is refused rather than recorded, because
    it is the field the whole X-fraction rests on."""
    if externally_caused in (True, False) and not cause_basis:
        raise ValueError(
            "externally_caused=%r needs a cause_basis. It is a claim about "
            "the world and the X-fraction rests on it." % externally_caused)
    if directionality not in DIRECTIONALITY:
        raise ValueError("directionality %r" % (directionality,))
    if action_target not in ACTION_TARGETS:
        raise ValueError("action_target %r" % (action_target,))
    if attenuation not in ATTENUATION:
        raise ValueError("attenuation %r" % (attenuation,))
    if subject_class_override is not None:
        if subject_class_override not in SUBJECT_CLASSES:
            raise ValueError("subject_class %r" % (subject_class_override,))
        if not override_reason:
            raise ValueError(
                "a declared subject class needs an override_reason. The "
                "mechanical route is the checkable one; leaving it "
                "silently is how a word list becomes an unexamined "
                "judgment.")
        sc, head = subject_class_override, None
    elif text is None:
        raise ValueError(
            "an item with no text needs subject_class_override plus an "
            "override_reason -- there is nothing to extract from.")
    else:
        sc, head = subject_class(text)
    return {"ref": ref, "text": text, "subject_class": sc,
            "head_noun": head,
            "subject_declared": subject_class_override is not None,
            "override_reason": override_reason,
            "externally_caused": externally_caused,
            "cause_basis": cause_basis,
            "directionality": directionality,
            "action_target": action_target,
            "attenuation": attenuation}


def locus(it):
    """DERIVED, never hand-set.

        subject PERSON     + externally_caused True   -> X
        subject PERSON     + anything else            -> P
        subject HOUSEHOLD                             -> H
        subject CONDITION                             -> E
        subject UNCLASSIFIED                          -> UNCLASSIFIED

    An item whose subject is a person and whose causal field is
    NOT_DECLARED codes P, not X. That is deliberate: X is the audit's
    conclusion about an item, and a conclusion nobody declared is not
    one."""
    sc = it["subject_class"]
    if sc == PERSON:
        return X if it["externally_caused"] is True else P
    if sc == HOUSEHOLD:
        return H
    if sc == CONDITION:
        return E
    return UNCLASSIFIED


# ------------------------------------------------------------ the outcomes

def outcomes(items):
    """The drop's three primary outcomes, plus the one its own coding
    scheme collects and does not report.

    Every fraction carries its denominator and the unclassified count,
    because the three denominators are different and the drop names one
    ('total items'). See AUDIT_NOTES."""
    codes = [locus(i) for i in items]
    n = len(items)
    unc = codes.count(UNCLASSIFIED)
    ph = [i for i, c in zip(items, codes) if c in (P, H)]
    mand = sum(1 for i in ph if i["attenuation"] == MANDATORY)
    declared_dir = [i for i in items if i["directionality"] != NOT_DECLARED]
    explains = sum(1 for i in declared_dir if i["directionality"] == EXPLAINS)
    return {
        "n_items": n,
        "unclassified": unc,
        "counts": dict((c, codes.count(c)) for c in LOCUS_CODES),
        "e_fraction": _frac(codes.count(E), n),
        "e_denominator": n,
        "x_fraction": _frac(codes.count(X), n),
        "x_denominator": n,
        "attenuation_coverage": _frac(mand, len(ph)),
        "attenuation_denominator": len(ph),
        # NOT one of the drop's three. The drop codes DIRECTIONALITY --
        # "does any item permit an external cause to EXPLAIN a household
        # observation, or only to co-occur with it" -- and reports no
        # outcome for it. An instrument can score well on all three
        # published numbers and still permit no external cause to
        # explain anything.
        "explain_fraction_ADDED": _frac(explains, len(declared_dir)),
        "explain_denominator": len(declared_dir),
        "directionality_not_declared":
            sum(1 for i in items if i["directionality"] == NOT_DECLARED),
    }


def _frac(num, den):
    """A fraction with an empty denominator is NOT zero."""
    return None if not den else round(num / float(den), 4)


def table(items):
    rows = []
    for it in items:
        rows.append((it["ref"], locus(it), it["subject_class"],
                     it["head_noun"] or "-",
                     it["externally_caused"], it["directionality"],
                     it["attenuation"]))
    return rows


# ------------------------------------------------------------- fixtures

# AUTHORED HERE. Not drawn from, paraphrased from, or modelled on any
# published instrument. Ground truth is the authoring, and each carries
# the class it was written to be. They exist to exercise the coder and
# to make the null test possible; they are not a corpus and no number
# taken over them is about any instrument.
FIXTURES_NOTE = (
    "13 items authored in this file to exercise the coder. NOT drawn "
    "from any published instrument, and no fraction over them is a "
    "statement about any instrument.")


def fixtures():
    return [
        # written to be P
        item("FX-01", "Parent demonstrates consistent supervision.",
             attenuation=NONE, action_target=PERSON),
        item("FX-02", "Caregiver responds to distress without escalation.",
             attenuation=DISCRETIONARY, action_target=PERSON),
        # written to be H
        item("FX-03", "The household resolves conflict without escalation.",
             attenuation=NONE, action_target=HOUSEHOLD),
        item("FX-04", "Family routines are predictable across the week.",
             attenuation=DISCRETIONARY, action_target=HOUSEHOLD,
             directionality=CO_OCCURS),
        # written to be E
        item("FX-05", "Employment schedule permits attendance at "
                      "appointments.",
             action_target=EXTERNAL, directionality=EXPLAINS),
        item("FX-06", "Utility service has been disconnected in the past "
                      "year.",
             action_target=EXTERNAL, directionality=CO_OCCURS),
        # written to be X: person-subject, externally caused, declared
        item("FX-07", "Caregiver fails to provide stable housing.",
             externally_caused=True,
             cause_basis="tenancy availability and rent level are set "
                         "outside the household",
             attenuation=NONE, action_target=PERSON),
        item("FX-08", "Parent does not attend scheduled appointments.",
             externally_caused=True,
             cause_basis="appointment times are set by the service and "
                         "transport is a condition, not a capacity",
             attenuation=DISCRETIONARY, action_target=PERSON),
        # written to be P despite a person subject: cause NOT declared,
        # so it is not X. A conclusion nobody declared is not one.
        item("FX-09", "Caregiver does not maintain employment.",
             attenuation=NONE, action_target=PERSON),
        # written to be P with the causal claim declared FALSE
        item("FX-10", "Parent declines offered in-home support.",
             externally_caused=False,
             cause_basis="the support was offered and reachable; the "
                         "decision is the item's subject",
             attenuation=NONE, action_target=PERSON),
        # written to be UNCLASSIFIED: head noun outside all three lists
        item("FX-11", "Supervision arrangements vary between weekdays.",
             attenuation=NOT_DECLARED),
        # written to exercise the MANDATORY branch. Without one anywhere,
        # attenuation_coverage is 0.0 whatever the denominator does, and
        # a measure that cannot move is not being tested.
        item("FX-13", "Caregiver seeks help when a routine breaks down.",
             attenuation=MANDATORY, action_target=PERSON,
             directionality=EXPLAINS),
        # written to be codeable by reference only, text withheld
        item("FX-12", None, subject_class_override=PERSON,
             override_reason="item wording is licensed; the subject is a "
                             "person and the class is declared rather "
                             "than extracted",
             externally_caused=True,
             cause_basis="the condition named is set by a benefit rule",
             attenuation=NONE, action_target=PERSON),
    ]


if __name__ == "__main__":
    if "--selftest" in sys.argv[1:]:
        sys.stderr.write(
            "coding.py has no checks of its own. The checks that exercise "
            "it live in selftest_hsa.py.\n"
            "    python3 household-scope-audit/selftest_hsa.py\n")
        sys.exit(2)
    fx = fixtures()
    print("THE CODING SCHEME, ON AUTHORED FIXTURES")
    print("")
    print("  " + FIXTURES_NOTE.replace(". ", ".\n  "))
    print("")
    print("  %-7s %-13s %-13s %-11s %-6s %-11s %s" % (
        "ref", "LOCUS", "subject", "head", "ext?", "direction",
        "attenuation"))
    for r in table(fx):
        print("  %-7s %-13s %-13s %-11s %-6s %-11s %s" % r)
    print("")
    o = outcomes(fx)
    print("  n items %d   unclassified %d" % (o["n_items"], o["unclassified"]))
    print("  E-fraction            %-8s over %d" % (
        o["e_fraction"], o["e_denominator"]))
    print("  X-fraction            %-8s over %d" % (
        o["x_fraction"], o["x_denominator"]))
    print("  attenuation coverage  %-8s over %d" % (
        o["attenuation_coverage"], o["attenuation_denominator"]))
    print("  explain fraction      %-8s over %d   ADDED, not one of the "
          "three" % (o["explain_fraction_ADDED"], o["explain_denominator"]))
