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
#
# B1, checked. p_write IS specified on its own axes -- supply_assumption,
# time_to_writing_station, reward_structure -- and does NOT read the wage or
# block count that drive generation. So this is not S4's rank dictionary: the
# two mappings are separate functions of separate inputs.
#
# It fails the separator anyway. Both dictionaries were hand-assigned in the
# same position ordering, so the mapping admits NO position with high
# generation and high writing probability, and the -0.99 is a CONSTRAINT that
# was typed in rather than a correlation the model produced. See
# admissibility_check() and RESIDENT_WRITER.
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


# The position the five-row mapping cannot express: someone resident (low
# supply assumption, continuous presence, so high generation) who is ALSO
# compensated to write and near a station. A station scientist, a resident
# researcher, a paid observer. Not exotic -- absent.
RESIDENT_WRITER = {"supply_assumption": 0.25,
                   "time_to_writing_station": 0.85,
                   "reward_structure": 0.85}


def admissibility_check(demo, threshold_gen=100.0, threshold_p=0.5):
    """B1's separator: does the mapping admit high generation AND high
    p_write?

    If it does not, the -0.99 is a constraint and should print as one.
    """
    hi_gen = [n for n, g in demo.items() if g >= threshold_gen]
    both = [n for n in hi_gen if writing_probability(n) >= threshold_p]
    return {"high_generation_positions": hi_gen,
            "of_those_also_high_p_write": both,
            "max_p_write_among_high_generation":
                max([writing_probability(n) for n in hi_gen] or [0.0]),
            "mapping_admits_the_separator": bool(both),
            "reads_the_same_inputs_as_generation": False,
            "verdict": "CONSTRAINT, not a correlation" if not both
                       else "correlation; the separator is admitted",
            "why": "p_write is a function of supply assumption, station "
                   "distance and reward. Generation is a function of wage "
                   "and block count. Different inputs, so this is not the "
                   "S4 rank-dictionary defect -- but both dictionaries were "
                   "hand-assigned in one ordering, so no row is high on "
                   "both and the anti-correlation was assembled rather than "
                   "measured"}


def with_resident_writer(demo, generation=125.0):
    """Add the missing position and re-run. Does the inversion survive?"""
    rows = [assess(p["position"], demo[p["position"]]) for p in M1.POSITIONS]
    p = S9.p_write(RESIDENT_WRITER)
    rows = rows + [{"position": "resident_writer",
                    "observations_generated": generation,
                    "writing_probability": p,
                    "record_present": generation * p,
                    "assessed_contribution": generation * p,
                    "assessment_ratio": p}]
    return {"rows": rows, "readout": merit_vs_writing_time(rows)}


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
        "THE -0.99 IS A CONSTRAINT THAT WAS TYPED IN, NOT A CORRELATION "
        "THAT WAS MEASURED. p_write is a function of supply assumption, "
        "station distance and reward; generation is a function of wage and "
        "block count -- different inputs, so this is NOT the S4 "
        "rank-dictionary defect. But both dictionaries were hand-assigned "
        "in one ordering, the mapping admits no position that is high on "
        "both, and adding one such position moves the number materially. "
        "The inversion is a property of which five rows were typed in",
        "and the row that breaks it -- a resident who is also compensated "
        "to write -- is one the mapping had no slot for. Same shape as the "
        "blank agent, one level down: the five-row list excluded the "
        "position that would have refuted the finding",
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
    ac = admissibility_check(demo)
    L.append("  B1 -- IS THE ANTI-CORRELATION MEASURED OR TYPED IN?")
    L.append("")
    L.append("    p_write reads the same inputs as generation : %s"
             % ac["reads_the_same_inputs_as_generation"])
    L.append("    high-generation positions                   : %s"
             % ", ".join(ac["high_generation_positions"]))
    L.append("    of those, also high p_write                 : %s"
             % (", ".join(ac["of_those_also_high_p_write"]) or "NONE"))
    L.append("    max p_write among them                      : %.3f"
             % ac["max_p_write_among_high_generation"])
    L.append("    verdict                                     : %s"
             % ac["verdict"])
    L.append("")
    L.extend(SH.wrap(ac["why"], "    "))
    L.append("")
    L.append("-" * 72)
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
    wr = with_resident_writer(demo)
    L.append("  ADDING THE POSITION THE MAPPING CANNOT EXPRESS")
    L.append("")
    L.extend(SH.wrap("A resident writer: low supply assumption and "
                     "continuous presence, so high generation, AND "
                     "compensated and near a station, so high p_write. A "
                     "station scientist or a paid resident observer. Not "
                     "exotic -- absent from the five rows.", "    "))
    L.append("")
    L.append("    p_write for that position               : %.3f"
             % S9.p_write(RESIDENT_WRITER))
    L.append("    corr with generation, 5 rows            : %+.3f"
             % mv["corr_with_generated"])
    L.append("    corr with generation, 6 rows            : %+.3f"
             % wr["readout"]["corr_with_generated"])
    L.append("    generation vs p_write, 5 rows           : %+.3f"
             % mv["corr_generation_vs_writing"])
    L.append("    generation vs p_write, 6 rows           : %+.3f"
             % wr["readout"]["corr_generation_vs_writing"])
    L.append("    readout, 6 rows                         : %s"
             % wr["readout"]["tracks"])
    L.append("")
    L.extend(SH.wrap("One added row moves the constraint materially. The "
                     "inversion is therefore a property of WHICH FIVE "
                     "POSITIONS WERE TYPED IN, not of the coupling -- and "
                     "the row that breaks it is one the five-row mapping "
                     "had no slot for, which is the same shape as the blank "
                     "agent in agents.py.", "    "))
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
       "anti-correlated on the five rows",
       mv["corr_generation_vs_writing"] < -0.8)

    # B1
    ac = admissibility_check(demo)
    ck("B1: p_write does NOT read the inputs that drive generation, so this "
       "is not the S4 rank-dictionary defect",
       ac["reads_the_same_inputs_as_generation"] is False)
    ck("B1: and the mapping admits NO position high on both, so the -0.99 "
       "is a constraint that was typed in",
       ac["mapping_admits_the_separator"] is False
       and ac["verdict"].startswith("CONSTRAINT"))
    wr = with_resident_writer(demo)
    ck("B1: one added position that IS high on both flips the sign of the "
       "correlation with generation",
       mv["corr_with_generated"] < -0.5
       < wr["readout"]["corr_with_generated"])
    ck("B1: so the inversion is a property of which five rows were typed "
       "in, not of the coupling",
       wr["readout"]["tracks"] != "INVERTS generation")
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
