#!/usr/bin/env python3
# SPDX-License-Identifier: CC0-1.0
"""
s5_adversarial_prior.py - does collective computation require competing
agents?

    python3 s5_adversarial_prior.py
    python3 s5_adversarial_prior.py --selftest

One substrate, two readouts.

  CONFLICT    the units have separable interests and the outcome is what
              those interests settle on
  ALLOCATION  the units are under a shared environmental constraint and the
              outcome is what the constraint permits

The module generates data from ONE process and fits both readouts, then asks
the question the fitting cannot answer: is there any observable on which the
two disagree? Showing that two hand-built models fit the same data is cheap
if they were built to. What is not cheap is enumerating what would separate
them and finding the list empty on the observables usually reported.

Literature instance, carried from the work order and NOT verified here: plant
root collectives have been rejected as swarm intelligence for lacking genetic
conflict. The criterion is audited below for independent justification --
meaning, does it predict any observable differently, or does it only relabel.

Marker under exploration, not a thesis. stdlib only, CC0.
"""

import random
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _shared as SH                                            # noqa: E402

READOUTS = ("CONFLICT", "ALLOCATION")


def generate(n_units=60, steps=120, resource=1.0, seed=4):
    """ONE generative process. No conflict term and no interest term appear
    in it: units take what is available, and availability falls as others
    take. That is all."""
    rng = random.Random(seed)
    uptake = [0.0] * n_units
    series = []
    for _ in range(steps):
        demand = [rng.uniform(0.5, 1.5) for _ in range(n_units)]
        total = sum(demand)
        share = [resource * d / total for d in demand]
        for i, s in enumerate(share):
            uptake[i] += s
        series.append(list(share))
    return {"uptake": uptake, "series": series, "n_units": n_units,
            "generative_terms": ("demand", "shared resource")}


def fit_conflict(data):
    """Read the same numbers as an outcome of separable interests."""
    up = data["uptake"]
    mean = sum(up) / len(up)
    var = sum((x - mean) ** 2 for x in up) / len(up)
    return {"readout": "CONFLICT",
            "parameter": "interest asymmetry",
            "value": var ** 0.5 / mean,
            "narrative": "units with stronger interests captured more",
            "residual": 0.0}


def fit_allocation(data):
    """Read the same numbers as an outcome of a shared constraint."""
    up = data["uptake"]
    mean = sum(up) / len(up)
    var = sum((x - mean) ** 2 for x in up) / len(up)
    return {"readout": "ALLOCATION",
            "parameter": "constraint tightness",
            "value": var ** 0.5 / mean,
            "narrative": "units received what the constraint permitted",
            "residual": 0.0}


def both_fit(data):
    c, a = fit_conflict(data), fit_allocation(data)
    return {"conflict": c, "allocation": a,
            "same_number": abs(c["value"] - a["value"]) < 1e-12,
            "residual_difference": abs(c["residual"] - a["residual"])}


# What would separate them, and whether it is usually reported.
SEPARATORS = [
    {"observable": "outcome under removal of the shared constraint",
     "conflict_predicts": "units keep competing; spread persists",
     "allocation_predicts": "spread collapses; the constraint was the cause",
     "usually_reported": False},
    {"observable": "outcome when units are genetically identical",
     "conflict_predicts": "no separable interests, so no structure",
     "allocation_predicts": "unchanged; the constraint does not read genomes",
     "usually_reported": False},
    {"observable": "uptake distribution shape",
     "conflict_predicts": "same",
     "allocation_predicts": "same",
     "usually_reported": True},
    {"observable": "total resource captured",
     "conflict_predicts": "same",
     "allocation_predicts": "same",
     "usually_reported": True},
    {"observable": "response to a resource pulse",
     "conflict_predicts": "same",
     "allocation_predicts": "same",
     "usually_reported": True},
]


def separator_audit():
    sep = [s for s in SEPARATORS
           if s["conflict_predicts"] != s["allocation_predicts"]]
    reported_sep = [s for s in sep if s["usually_reported"]]
    return {"observables": len(SEPARATORS),
            "that_separate": len(sep),
            "that_separate_and_are_usually_reported": len(reported_sep),
            "separating": [s["observable"] for s in sep],
            "why": "the observables that separate the two readouts are the "
                   "ones requiring an intervention -- remove the constraint, "
                   "or hold the genome fixed. The observables usually "
                   "reported are the ones both readouts predict identically"}


def criterion_audit():
    """Does 'lacks genetic conflict' do independent work?

    A criterion earns its place if it predicts some observable differently.
    Checked against the separator list rather than argued.
    """
    genetic = [s for s in SEPARATORS if "genetically identical" in
               s["observable"]]
    does_work = any(s["conflict_predicts"] != s["allocation_predicts"]
                    for s in genetic)
    return {"criterion": "requires genetic conflict among units",
            "predicts_a_different_observable": does_work,
            "which": [s["observable"] for s in genetic],
            "but": "the observable it predicts differently on is an "
                   "INTERVENTION -- hold the genome fixed and see whether "
                   "collective structure survives -- and a clonal root "
                   "system is that intervention, already run. So the "
                   "criterion is not empty; it is a prediction, and the case "
                   "it was used to exclude is the case that tests it",
            "independent_justification_located": "NOT_ESTABLISHED_HERE"}


def atomization_link():
    """The structural note from the work order, kept as a note.

    Adversarial framing requires discrete bounded agents with separable
    interests. A substrate that is not partitioned that way does not fail the
    criterion -- it fails to be addressable by it, which is a different state.
    """
    return {"requires": "discrete bounded units with separable interests",
            "fails_criterion": "a partitioned substrate whose units do not "
                               "compete",
            "not_addressable_by_criterion": "an unpartitioned substrate",
            "distinction": "failing a test and being outside its domain are "
                           "different verdicts, and a criterion that returns "
                           "the same answer for both cannot tell them apart"}


def confidence():
    return {"non_identifiability": "demonstrated on a constructed pair, and "
                                   "the construction is disclosed",
            "separator_list": "enumerated by the module's author and not "
                              "exhaustive",
            "literature_instance": "CARRIED FROM THE WORK ORDER, not "
                                   "verified here",
            "resolved": False}


def breaks():
    return [
        "two models built by one author to fit the same data will fit the "
        "same data. The demonstration is worth only what the SEPARATOR "
        "enumeration is worth, and that list is short, hand-made and not "
        "exhaustive",
        "fit_conflict and fit_allocation compute the same statistic and "
        "differ only in the label attached to it. That is the point being "
        "made and it is also a way of guaranteeing the point",
        "the generative process has no conflict term, so 'conflict fits it "
        "anyway' is an argument about the readout and not evidence that real "
        "collectives lack conflict",
        "the root-collective instance is carried from the work order. No "
        "paper is read or quoted here, and 'rejected for lacking genetic "
        "conflict' is not verified",
        "the criterion audit finds the criterion DOES predict a different "
        "observable, which runs against the framing the work order offers. "
        "It is reported that way rather than softened",
    ]


def report():
    L = ["S5 -- ADVERSARIAL PRIOR", "=" * 72, ""]
    data = generate()
    bf = both_fit(data)
    L.append("  1. ONE SUBSTRATE, TWO READOUTS")
    L.append("")
    L.append("    generative terms: %s" % ", ".join(data["generative_terms"]))
    L.append("    (no conflict term and no interest term appear in it)")
    L.append("")
    for key in ("conflict", "allocation"):
        r = bf[key]
        L.append("    %-12s parameter %-22s value %.4f"
                 % (r["readout"], r["parameter"], r["value"]))
        L.append("                 %s" % r["narrative"])
    L.append("")
    L.append("    same number: %s   residual difference: %.1e"
             % (bf["same_number"], bf["residual_difference"]))
    L.append("")
    L.extend(SH.wrap("Both readouts return the same number and the same "
                     "residual. The disagreement is entirely in the noun "
                     "attached to the parameter.", "    "))
    L.append("")
    L.append("-" * 72)
    L.append("")
    sa = separator_audit()
    L.append("  2. WHAT WOULD SEPARATE THEM, AND WHETHER IT IS REPORTED")
    L.append("")
    L.append("    %-46s %-10s %s"
             % ("observable", "separates", "usually reported"))
    for s in SEPARATORS:
        L.append("    %-46s %-10s %s"
                 % (s["observable"][:46],
                    "yes" if s["conflict_predicts"] != s["allocation_predicts"]
                    else "no",
                    "yes" if s["usually_reported"] else "no"))
    L.append("")
    L.append("    separate: %d of %d.  separate AND usually reported: %d"
             % (sa["that_separate"], sa["observables"],
                sa["that_separate_and_are_usually_reported"]))
    L.append("")
    L.extend(SH.wrap(sa["why"], "    "))
    L.append("")
    L.append("-" * 72)
    L.append("")
    ca = criterion_audit()
    L.append("  3. THE CRITERION AUDIT -- and it runs against the framing")
    L.append("")
    L.append("    criterion: %s" % ca["criterion"])
    L.append("    predicts a different observable: %s"
             % ca["predicts_a_different_observable"])
    L.append("    independent justification located: %s"
             % ca["independent_justification_located"])
    L.append("")
    L.extend(SH.wrap(ca["but"], "    "))
    L.append("")
    L.extend(SH.wrap("So the audit does not return 'the criterion is empty'. "
                     "It returns something more useful: the criterion is a "
                     "PREDICTION, and the case it was used to exclude is the "
                     "case that tests it. A clonal root system holds the "
                     "genome fixed, which is exactly the intervention the "
                     "criterion's own logic says should destroy collective "
                     "structure. Reported this way rather than softened, "
                     "because it is the opposite of what the framing "
                     "expects.", "    "))
    L.append("")
    al = atomization_link()
    L.append("  4. THE ADDRESSABILITY NOTE")
    L.append("")
    L.extend(SH.wrap(al["distinction"], "    "))
    L.append("")
    L.append("    fails the criterion:       %s" % al["fails_criterion"])
    L.append("    outside its domain:        %s"
             % al["not_addressable_by_criterion"])
    L.extend(SH.tail(sys.modules[__name__]))
    return "\n".join(L)


def selftest():
    ck, done = SH.checker()
    data = generate()
    ck("the generative process names no conflict or interest term",
       all(t in ("demand", "shared resource")
           for t in data["generative_terms"]))
    bf = both_fit(data)
    ck("both readouts return the same number", bf["same_number"])
    ck("and the same residual", bf["residual_difference"] < 1e-12)
    ck("they differ only in the noun attached",
       bf["conflict"]["parameter"] != bf["allocation"]["parameter"]
       and abs(bf["conflict"]["value"] - bf["allocation"]["value"]) < 1e-12)

    sa = separator_audit()
    ck("some observables do separate the readouts", sa["that_separate"] >= 2)
    ck("and none of the separating ones is usually reported",
       sa["that_separate_and_are_usually_reported"] == 0)
    ck("so the list is not empty in either direction -- it is not "
       "CONSTANT_SILENT and not CONSTANT_FIRES",
       0 < sa["that_separate"] < sa["observables"])

    ca = criterion_audit()
    ck("the criterion audit finds the criterion DOES predict a different "
       "observable, against the framing offered",
       ca["predicts_a_different_observable"] is True)
    ck("and independent justification is recorded as not established rather "
       "than as absent",
       ca["independent_justification_located"] == "NOT_ESTABLISHED_HERE")

    al = atomization_link()
    ck("failing a criterion and being outside its domain are kept apart",
       al["fails_criterion"] != al["not_addressable_by_criterion"])

    ck("the construction risk is the first break listed",
       "built by one author" in breaks()[0])
    ck("the against-framing result is disclosed in breaks",
       any("runs against the framing" in b for b in breaks()))
    ck("confidence unresolved", confidence()["resolved"] is False)
    ck("report renders", "ADDRESSABILITY" in report())
    return done()


if __name__ == "__main__":
    sys.exit(SH.run(sys.modules[__name__], "S5"))
