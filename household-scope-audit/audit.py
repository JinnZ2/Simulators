#!/usr/bin/env python3
# audit.py -- CC0, stdlib only, phone-buildable, parses under 3.9
#
# What can be established about Arm 1's design without a reading room.
#
# ARM 1 IS NOT RUN HERE AND IS NOT SIMULATED. Every published
# instrument and manual host tested from this environment refuses
# CONNECT; the measurement is in EGRESS below. No instrument item is
# invented, paraphrased or coded anywhere in this folder -- these are
# tools that carry weight in decisions about real families, and a
# fabricated E-fraction table would read as a result about them.
#
# What IS established: properties of the coding scheme and of the
# design, each demonstrated on authored fixtures whose ground truth is
# the authoring.

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import coding as C  # noqa: E402

# Measured 2026-08-29 from this environment, not assumed. Every host
# returned 000 (no response through the proxy) except github.com.
EGRESS = [
    ("www.ncbi.nlm.nih.gov", "000"),
    ("pubmed.ncbi.nlm.nih.gov", "000"),
    ("onlinelibrary.wiley.com", "000"),
    ("www.acf.hhs.gov", "000"),
    ("www.childwelfare.gov", "000"),
    ("apps.who.int", "000"),
    ("www.gov.uk", "000"),
    ("github.com", "400"),
]


# ------------------------------------------------- the coder's null test

def subject_null_test():
    """The mechanical half, both directions.

    A classifier that cannot return UNCLASSIFIED forces every item into
    a class, which is the failure the drop's own ask names ('marked
    unclassified rather than forced'). One that classifies nothing is
    equally useless. Both are checked."""
    signal = [
        ("Parent demonstrates supervision.", C.PERSON),
        ("Caregiver responds to distress.", C.PERSON),
        ("The household resolves conflict.", C.HOUSEHOLD),
        ("Family routines are predictable.", C.HOUSEHOLD),
        ("Employment schedule permits attendance.", C.CONDITION),
        ("Utility service has been disconnected.", C.CONDITION),
    ]
    null = [
        "Supervision arrangements vary between weekdays.",
        "Consistency fluctuates across the reporting period.",
        "Attunement is difficult to observe directly.",
    ]
    hit = sum(1 for t, want in signal if C.subject_class(t)[0] == want)
    forced = sum(1 for t in null if C.subject_class(t)[0] != C.UNCLASSIFIED)
    return {"signal_n": len(signal), "signal_correct": hit,
            "null_n": len(null), "null_forced": forced,
            "can_classify": hit > 0,
            "can_decline": forced < len(null),
            "verdict": "OK" if hit == len(signal) and forced == 0
            else "CHECK"}


# ------------------------ X is a causal judgment, and it moves two outcomes

def cause_coupling():
    """Declaring one item's cause moves TWO of the three outcomes.

    FX-09 -- 'Caregiver does not maintain employment' -- is a person
    subject with the causal field NOT_DECLARED, so it codes P. Declaring
    it externally caused moves it to X, which:

      raises X-fraction              (numerator +1)
      shrinks attenuation coverage's denominator  (P and H items -1)

    The two outcomes are coupled through one judgment about the world,
    and the drop reports them side by side as though they were separate
    readings."""
    base = C.fixtures()
    before = C.outcomes(base)
    moved = []
    for it in base:
        if it["ref"] == "FX-09":
            it = dict(it)
            it["externally_caused"] = True
            it["cause_basis"] = ("declared here to demonstrate the "
                                 "coupling; not a claim about employment")
        moved.append(it)
    after = C.outcomes(moved)
    return {"before": before, "after": after,
            "x_moved": (before["x_fraction"], after["x_fraction"]),
            "atten_denominator_moved": (before["attenuation_denominator"],
                                        after["attenuation_denominator"]),
            "atten_moved": (before["attenuation_coverage"],
                            after["attenuation_coverage"]),
            "e_moved": (before["e_fraction"], after["e_fraction"])}


def reverse_causation():
    """The confound the drop excludes from Arm 1, landing on Arm 1.

        REVERSE CAUSATION ... The audit arm is unaffected -- it measures
        representational capacity, not causal share.

    True of the E-fraction, which asks whether an item with a condition
    subject EXISTS -- a property of the text. False of the X-fraction,
    which asks whether a person-subject item's variable is externally
    caused. Reverse causation is exactly the case where it is not, so
    the same text yields two X-fractions under two defensible causal
    readings."""
    base = C.fixtures()
    outward, inward = [], []
    for it in base:
        if it["ref"] == "FX-09":
            a = dict(it)
            a["externally_caused"] = True
            a["cause_basis"] = "labour market read as the cause of job loss"
            b = dict(it)
            b["externally_caused"] = False
            b["cause_basis"] = "job loss read as downstream of the household"
            outward.append(a)
            inward.append(b)
        else:
            outward.append(it)
            inward.append(it)
    o, i = C.outcomes(outward), C.outcomes(inward)
    return {"x_outward": o["x_fraction"], "x_inward": i["x_fraction"],
            "e_outward": o["e_fraction"], "e_inward": i["e_fraction"],
            "e_unchanged": o["e_fraction"] == i["e_fraction"],
            "x_changed": o["x_fraction"] != i["x_fraction"]}


# ------------------------------- an outcome the coded fields do not carry

def directionality_invisible():
    """Two item sets, identical on all three published outcomes, that
    differ on whether an external cause may EXPLAIN a household
    observation.

    The drop codes DIRECTIONALITY and reports no outcome for it. So an
    instrument that records external conditions and never lets them do
    any work is indistinguishable, in the published numbers, from one
    that does."""
    a = C.fixtures()
    b = []
    for it in a:
        it2 = dict(it)
        if it2["directionality"] == C.EXPLAINS:
            it2["directionality"] = C.CO_OCCURS
        b.append(it2)
    oa, ob = C.outcomes(a), C.outcomes(b)
    same = all(oa[k] == ob[k] for k in
               ("e_fraction", "x_fraction", "attenuation_coverage"))
    return {"three_outcomes_identical": same,
            "explain_a": oa["explain_fraction_ADDED"],
            "explain_b": ob["explain_fraction_ADDED"],
            "differ": oa["explain_fraction_ADDED"]
            != ob["explain_fraction_ADDED"]}


# ------------------------------------------ where the unclassified items go

def unclassified_placement():
    """The drop's ask says mark them unclassified rather than forcing,
    and does not say which denominator they sit in.

    E-fraction is stated as 'E items / total items'. Keeping an
    unclassified item in that denominator biases E-fraction low by
    exactly the unclassified share; dropping it changes the denominator
    per outcome. Both are reported and neither is picked."""
    fx = C.fixtures()
    o = C.outcomes(fx)
    kept = o["e_fraction"]
    n_class = o["n_items"] - o["unclassified"]
    dropped = None if not n_class else round(
        o["counts"][C.E] / float(n_class), 4)
    return {"unclassified": o["unclassified"], "n_items": o["n_items"],
            "e_in_denominator": kept, "e_out_of_denominator": dropped,
            "picked": None}


# ------------------------------------------------------------- the report

def render():
    out = []
    w = out.append
    w("HOUSEHOLD-SCOPE AUDIT -- Arm 1's coding scheme, and what the")
    w("design can be checked on without a reading room")
    w("")
    w("SOURCE_DROP.md asks for Arm 1, and for \"a reading room and a")
    w("coding scheme, nothing else.\" The coding scheme is built. The")
    w("reading room is not available and is not substituted for.")
    w("")

    w("0. ARM 1 IS NOT RUN. THE CORPUS IS UNREACHABLE, MEASURED.")
    for host, code in EGRESS:
        w("     %-28s %s" % (host, code))
    w("   Every publisher, statutory and archive host returns no")
    w("   response through this environment's proxy; only github.com")
    w("   answers. Egress is an allowlist, so substituting a publisher")
    w("   does not help.")
    w("")
    w("   NO INSTRUMENT ITEM IS INVENTED, PARAPHRASED OR CODED ANYWHERE")
    w("   IN THIS FOLDER. These are tools that carry weight in decisions")
    w("   about real families; a fabricated E-fraction table would read")
    w("   as a result about them. The fixtures used below are authored")
    w("   in coding.py, labelled there, and no fraction over them is a")
    w("   statement about any instrument.")
    w("")
    w("   A SECOND CONSTRAINT, which binds whoever DOES have the reading")
    w("   room: item wording in many published instruments is licensed")
    w("   rather than free. An audit publishing its item-level working")
    w("   data would reproduce it. So the scheme codes by REFERENCE with")
    w("   the text optional -- and that is not free either, because the")
    w("   field most in need of checking is the one that then cannot be")
    w("   published with the item beside it.")
    w("")

    w("1. THE CODER, NULL-TESTED BOTH WAYS")
    nt = subject_null_test()
    w("   items written to have a class:      %d of %d classified correctly"
      % (nt["signal_correct"], nt["signal_n"]))
    w("   items written to have none:         %d of %d forced into one"
      % (nt["null_forced"], nt["null_n"]))
    w("   can classify: %s    can decline: %s    %s" % (
        nt["can_classify"], nt["can_decline"], nt["verdict"]))
    w("   A classifier that cannot decline forces every item into a")
    w("   class, which is the failure the drop's own ask names. One that")
    w("   classifies nothing is equally useless. Both directions are")
    w("   checked because either alone passes for a coder that is not")
    w("   doing its job.")
    w("")

    w("2. X IS A CAUSAL JUDGMENT, AND IT MOVES TWO OF THE THREE OUTCOMES")
    cc = cause_coupling()
    w("   LOCUS as delivered has X = \"external condition coded AS a")
    w("   personal property\". Separating P from X takes a claim about")
    w("   what causes the underlying variable -- about the world, not")
    w("   about the text. Two coders who disagree about whether housing")
    w("   instability is externally caused produce different")
    w("   X-fractions on identical items.")
    w("")
    w("   Declaring ONE fixture's cause, changing no text:")
    w("     X-fraction               %-8s -> %s" % cc["x_moved"])
    w("     attenuation denominator  %-8s -> %s"
      % cc["atten_denominator_moved"])
    w("     attenuation coverage     %-8s -> %s" % cc["atten_moved"])
    w("     E-fraction               %-8s -> %s   (unchanged)"
      % cc["e_moved"])
    w("   Two of the three published outcomes move together on one")
    w("   judgment, and the drop reports them side by side as separate")
    w("   readings. The third does not move, which is the point: the")
    w("   E-fraction is a property of the text.")
    w("")
    w("   AND THE COUPLING RUNS IN THE FLATTERING DIRECTION. The item")
    w("   that moved carried no attenuation rule, so leaving the")
    w("   denominator RAISED attenuation coverage. A coder attributing")
    w("   more to external cause makes the instrument score higher on")
    w("   discounting for external cause, on the same manual. Whether")
    w("   that holds in general depends on how attenuation is")
    w("   distributed across the items a coder reclassifies -- which is")
    w("   measurable in a real audit and is not measured here.")
    w("")
    w("   THE SPLIT IS IN THE SCHEME HERE, not in the write-up:")
    w("   LOCUS is DERIVED from two declared fields --")
    w("     subject_class      mechanical, from the item's own subject,")
    w("                        recomputable by anyone holding the text")
    w("     externally_caused  declared per item WITH a stated basis;")
    w("                        refused without one")
    w("   -- so the causal claim is visible as one and can be disagreed")
    w("   with separately from the reading of the text. An item whose")
    w("   subject is a person and whose cause is NOT_DECLARED codes P,")
    w("   never X: a conclusion nobody declared is not one.")
    w("")

    w("3. REVERSE CAUSATION DOES REACH ARM 1")
    rc = reverse_causation()
    w("   The drop's confound section says: \"The audit arm is")
    w("   unaffected -- it measures representational capacity, not")
    w("   causal share.\"")
    w("")
    w("   True of the E-fraction and false of the X-fraction, from the")
    w("   drop's own definitions. Same items, two defensible causal")
    w("   readings of one of them:")
    w("     external cause read outward   X %-8s E %s" % (
        rc["x_outward"], rc["e_outward"]))
    w("     cause read inward             X %-8s E %s" % (
        rc["x_inward"], rc["e_inward"]))
    w("   E unchanged: %s     X changed: %s" % (
        rc["e_unchanged"], rc["x_changed"]))
    w("   Reverse causation is precisely the case where a person-subject")
    w("   item's variable is NOT externally caused, so the confound the")
    w("   drop excludes from Arm 1 lands on one of Arm 1's three primary")
    w("   outcomes. Section 2 is the same finding reached from the other")
    w("   side.")
    w("")

    w("4. ONE CODED FIELD HAS NO OUTCOME, AND IT IS THE ONE THAT")
    w("   SEPARATES RECORDING FROM EXPLAINING")
    di = directionality_invisible()
    w("   The drop codes four fields and publishes three outcomes.")
    w("   DIRECTIONALITY -- \"does any item permit an external cause to")
    w("   EXPLAIN a household observation, or only to co-occur with")
    w("   it\" -- is collected and not reported. So is ACTIONABILITY")
    w("   TARGET.")
    w("")
    w("   Two item sets, identical text, differing only in whether the")
    w("   external items may explain:")
    w("     all three published outcomes identical: %s"
      % di["three_outcomes_identical"])
    w("     explain fraction                        %s vs %s" % (
        di["explain_a"], di["explain_b"]))
    w("   An instrument that records external conditions and never lets")
    w("   them do any work is indistinguishable, in the three published")
    w("   numbers, from one that does. The field is already collected;")
    w("   what is missing is one line in the outcome list.")
    w("")

    w("5. WHERE THE UNCLASSIFIED ITEMS SIT IS NOT SPECIFIED")
    up = unclassified_placement()
    w("   The ask says mark them unclassified rather than forcing them,")
    w("   which is right and is the reason the coder has the state at")
    w("   all. It does not say which denominator they occupy.")
    w("     unclassified %d of %d items" % (up["unclassified"],
                                            up["n_items"]))
    w("     E-fraction with them in the denominator   %s"
      % up["e_in_denominator"])
    w("     E-fraction with them out                  %s"
      % up["e_out_of_denominator"])
    w("   E-fraction is stated as 'E items / total items', so keeping")
    w("   them in biases it low by exactly their share. Both are")
    w("   reported and neither is picked.")
    w("")

    w("6. WHAT THIS FOLDER DOES NOT ESTABLISH")
    w("   No E-fraction, X-fraction or attenuation coverage for any")
    w("   instrument. No claim about whether the gap is real -- the")
    w("   drop states its own retraction condition (E-fraction")
    w("   materially non-zero and attenuation mandatory) and nothing")
    w("   here bears on it in either direction.")
    w("")
    w("   Arm 2 UNMEASURED: human scorers, and a simulated practitioner")
    w("   panel would be a fabricated claim about practitioners.")
    w("   Arm 3 UNMEASURED: administrative records, unreachable and")
    w("   not public.")
    w("")
    w("   What is established is about the coding scheme and the")
    w("   design, and every demonstration above runs on items authored")
    w("   in this folder for that purpose.")
    return "\n".join(out)


if __name__ == "__main__":
    if "--selftest" in sys.argv[1:]:
        sys.stderr.write(
            "audit.py has no checks of its own. The checks that exercise "
            "it and coding.py live in selftest_hsa.py.\n"
            "    python3 household-scope-audit/selftest_hsa.py\n")
        sys.exit(2)
    print(render())
