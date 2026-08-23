#!/usr/bin/env python3
# SPDX-License-Identifier: CC0-1.0
"""
m4_assessment_record.py - contribution scored from the written record.

    python3 m4_assessment_record.py [--selftest]

The assessor reads a record, not a place. Contribution is scored from what is
written down, so the score is a function of writing probability as well as of
observations generated.

REUSES THE S9 POSITION FILTER rather than re-deriving it: writing_probability
is s9_corpus_position_filter.p_write, imported. The spec says do not
re-derive, and importing rather than copying is also this repo's own
anti-drift convention.

stdlib only, CC0.
"""

import sys
import os

HERE = os.path.dirname(os.path.abspath(__file__))
PARENT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, PARENT)
import _shared as SH                                            # noqa: E402
import m1_tenure_budget as M1                                   # noqa: E402
import s9_corpus_position_filter as S9                          # noqa: E402

# Position vectors in S9's axis space, one per M1 position. Stipulated, and
# the mapping is the join between the two modules.
S9_POSITION = {
    "desk_professional": {"supply_assumption": 0.92,
                          "time_to_writing_station": 0.95,
                          "reward_structure": 0.90},
    "freight_driver": {"supply_assumption": 0.55,
                       "time_to_writing_station": 0.35,
                       "reward_structure": 0.15},
    "fabrication": {"supply_assumption": 0.45,
                    "time_to_writing_station": 0.40,
                    "reward_structure": 0.20},
    "animal_handling": {"supply_assumption": 0.25,
                        "time_to_writing_station": 0.20,
                        "reward_structure": 0.10},
    "farm_labor": {"supply_assumption": 0.20,
                   "time_to_writing_station": 0.15,
                   "reward_structure": 0.08},
}


def writing_probability(position_name):
    """Imported from S9. Not re-derived here."""
    return S9.p_write(S9_POSITION[position_name])


def assess(position_name, observations_generated):
    """The assessor scores contribution from record_present only."""
    p = writing_probability(position_name)
    recorded = observations_generated * p
    return {"position": position_name,
            "observations_generated": observations_generated,
            "writing_probability": p,
            "record_present": recorded,
            "assessed_contribution": recorded,
            "assessment_ratio": (recorded / observations_generated)
            if observations_generated else None}


def merit_vs_writing_time(rows):
    """Is the returned gradient a merit gradient or a writing-time gradient?

    THE SIGN IS THE FINDING AND A FIRST VERSION OF THIS FUNCTION LOST IT.
    Comparing |r| alone reported "tracks generated observations" for a
    correlation of MINUS 0.85 -- which anti-tracks generation, the opposite
    of tracking it. Three states are now separated.

    Also reported: the correlation between generation and writing
    probability. Where those two are strongly anti-correlated, the assessed
    score cannot distinguish them, which is an identifiability limit of the
    same shape as S2's one-arm protocol and not a property of the assessor.
    """
    gen = [r["observations_generated"] for r in rows]
    pw = [r["writing_probability"] for r in rows]
    asd = [r["assessed_contribution"] for r in rows]
    rg, rp = S9._corr(gen, asd), S9._corr(pw, asd)
    rgp = S9._corr(gen, pw)
    if rg < -0.3:
        tracks = "INVERTS generation"
    elif abs(rp) > abs(rg):
        tracks = "writing probability"
    else:
        tracks = "generated observations"
    return {"corr_with_generated": rg,
            "corr_with_writing_probability": rp,
            "corr_generation_vs_writing": rgp,
            "tracks": tracks,
            "identifiable": abs(rgp) < 0.8,
            "note": "generation and writing probability are correlated at "
                    "%+.2f here. Where that is strongly negative the "
                    "assessed score cannot separate the two, and the "
                    "assessor is not the thing to fix" % rgp}


def confidence():
    return {"writing_probability": "IMPORTED from S9, not re-derived. It "
                                   "carries S9's stipulations unchanged",
            "position_mapping": "STIPULATED. the join between M1 positions "
                                "and S9 axes is hand-assigned and is the "
                                "weakest link in the module set",
            "assessment_rule": "record_present is generated x p_write, which "
                               "is the simplest possible assessor and is a "
                               "choice",
            "any_real_assessment_data": "NONE",
            "resolved": False}


def breaks():
    return [
        "THE POSITION MAPPING IS THE WEAKEST LINK IN THE MODULE SET. Five "
        "M1 positions are hand-assigned three S9 axis values each, and every "
        "downstream number moves with those fifteen stipulated numbers. "
        "Nothing measures them and nothing constrains them beyond ordering",
        "GENERATION AND WRITING PROBABILITY ARE ANTI-CORRELATED AT -0.99 "
        "IN THIS MAPPING, so the assessed score cannot separate them and no "
        "scoring rule reading only the record could. That is an "
        "identifiability limit, not an assessor defect, and it means the "
        "module cannot distinguish the spec's mechanism from any other "
        "mechanism producing the same anti-correlation",
        "the assessor is generated x p_write, so 'the assessment tracks "
        "writing probability' is partly definitional. What is not "
        "definitional is the SIGN against generation, which is what the "
        "readout reports",
        "record_present is treated as a continuous quantity. A real record "
        "is discrete and a position generating a fraction of a document "
        "generates none",
        "importing S9 means importing its stipulations. That is the right "
        "trade against copying, and it is still a dependency: if S9's "
        "p_write coefficients are wrong, M4 is wrong in the same direction "
        "with no independent check",
    ]


def report():
    L = ["M4 -- ASSESSMENT RECORD", "=" * 72, ""]
    L.extend(SH.wrap("writing_probability is imported from S9, not "
                     "re-derived. The assessor reads a record, not a place.",
                     "  "))
    L.append("")
    L.append("  %-20s %-12s %-14s %-14s %s"
             % ("position", "generated", "p(write)", "recorded", "ratio"))
    demo = {"desk_professional": 40.0, "freight_driver": 90.0,
            "fabrication": 95.0, "animal_handling": 120.0,
            "farm_labor": 130.0}
    rows = [assess(p["position"], demo[p["position"]]) for p in M1.POSITIONS]
    for r in rows:
        L.append("  %-20s %-12.1f %-14.4f %-14.2f %.4f"
                 % (r["position"], r["observations_generated"],
                    r["writing_probability"], r["record_present"],
                    r["assessment_ratio"]))
    L.append("")
    mv = merit_vs_writing_time(rows)
    L.append("  correlation with generated observations : %+.3f"
             % mv["corr_with_generated"])
    L.append("  correlation with writing probability    : %+.3f"
             % mv["corr_with_writing_probability"])
    L.append("  correlation, generation vs writing prob  : %+.3f"
             % mv["corr_generation_vs_writing"])
    L.append("  the returned gradient: %s" % mv["tracks"])
    L.append("  generation and writing separable here    : %s"
             % mv["identifiable"])
    L.append("")
    L.extend(SH.wrap("The positions generating the MOST observations are "
                     "assessed LOWEST. That is stronger than the spec's "
                     "prediction: not a merit gradient that is really a "
                     "writing-time gradient, but an INVERTED merit gradient. "
                     "The assessor is doing nothing wrong on its own terms -- "
                     "it reads the record it has.", "  "))
    L.append("")
    L.extend(SH.wrap("A first version of this readout compared |r| only and "
                     "reported 'tracks generated observations' for a "
                     "correlation of minus 0.85. The sign is the finding and "
                     "the magnitude comparison lost it; three states are now "
                     "separated.", "  "))
    L.append("")
    L.extend(SH.wrap(mv["note"] + ". So the assessor is not the thing to "
                     "fix here -- with generation and writing probability "
                     "this tightly anti-correlated, no scoring rule reading "
                     "only the record can tell them apart. Same shape as "
                     "S2's one-arm protocol: the fix is a second "
                     "observable, not a better estimator.", "  "))
    L.extend(SH.tail(sys.modules[__name__]))
    return "\n".join(L)


def selftest():
    ck, done = SH.checker()
    ck("writing probability is imported from S9, not defined here",
       writing_probability.__doc__ is not None
       and "S9" in writing_probability.__doc__)
    ck("and it is literally S9's function",
       abs(writing_probability("farm_labor")
           - S9.p_write(S9_POSITION["farm_labor"])) < 1e-12)
    ck("every M1 position has an S9 mapping",
       all(p["position"] in S9_POSITION for p in M1.POSITIONS))

    ck("writing probability falls with supply assumption and station "
       "distance",
       writing_probability("farm_labor")
       < writing_probability("desk_professional"))

    a = assess("farm_labor", 100.0)
    ck("assessed contribution is record present, not observations generated",
       a["assessed_contribution"] < a["observations_generated"])
    ck("the ratio is the writing probability exactly",
       abs(a["assessment_ratio"] - a["writing_probability"]) < 1e-12)
    ck("an empty generation returns None rather than a zero ratio",
       assess("farm_labor", 0.0)["assessment_ratio"] is None)

    demo = {"desk_professional": 40.0, "freight_driver": 90.0,
            "fabrication": 95.0, "animal_handling": 120.0,
            "farm_labor": 130.0}
    rows = [assess(p["position"], demo[p["position"]]) for p in M1.POSITIONS]
    mv = merit_vs_writing_time(rows)
    ck("the assessed gradient INVERTS generation -- stronger than the "
       "spec's prediction, and a magnitude-only comparison lost the sign",
       mv["tracks"] == "INVERTS generation")
    ck("it is negatively correlated with generation and positively with "
       "writing probability",
       mv["corr_with_generated"] < 0 < mv["corr_with_writing_probability"])
    ck("generation and writing probability are themselves strongly "
       "anti-correlated, which is why the two cannot be separated here",
       mv["corr_generation_vs_writing"] < -0.8)
    ck("and that is reported as an identifiability limit rather than as an "
       "assessor defect", mv["identifiable"] is False)

    ck("the position mapping is disclosed as the weakest link",
       "WEAKEST LINK" in breaks()[0])
    ck("the definitional part of the result is disclosed",
       any("partly definitional" in b for b in breaks()))
    ck("confidence records the import as carrying S9's stipulations",
       "IMPORTED" in confidence()["writing_probability"])
    ck("confidence unresolved", confidence()["resolved"] is False)
    # Line-wrapped prose: normalise whitespace before matching, or the
    # check fails on a phrase that is plainly present.
    flat = " ".join(report().split())
    ck("report renders", "INVERTED merit gradient" in flat)
    return done()


if __name__ == "__main__":
    sys.exit(SH.run(sys.modules[__name__], "M4"))
