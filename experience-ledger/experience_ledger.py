#!/usr/bin/env python3
# experience_ledger.py  -- CC0, stdlib only, phone-buildable
#
# Origin claims confer present-tense standing. The standing is almost
# never rechecked. This does not score the claim -- it emits the
# maintenance question the field skipped.
#
# The rule under test is NOT institutional-vs-informal. It is whether
# the field grants automatic CONTINUITY from an origin claim.
#
#   "coded since I was twelve"          -> continuity granted
#   "modelled as a kid"                 -> continuity granted
#   "ran the school paper / scouts"     -> continuity granted, decades
#   "ran machinery from age six"        -> continuity not granted
#
# Same grammatical form. Opposite handling. Nothing measured in either.
#
# usage:  python3 experience_ledger.py --check claim.json
#         python3 experience_ledger.py --classes
#         python3 experience_ledger.py --transfer "tube repair" "field diagnosis"

import json
import sys

UNCHECKED = None

# ---------------------------------------------------------------------
# DECAY CLASSES
# Competence decays. Standing does not. That asymmetry is the finding.
# Standing is granted at the rate of the slowest-decaying reading and
# then never re-read.
# ---------------------------------------------------------------------

DECAY_CLASSES = {
    "physiological": {
        "examples": "flexibility, strength, aerobic capacity, grip endurance",
        "decay": "fast -- weeks to months without load",
        "reacquisition": "fast, but bounded by current tissue and age",
        "present_measurable": "measure it today. It is directly testable "
                              "and costs one session.",
    },
    "procedural_motor": {
        "examples": "machine operation, instrument playing, welding bead, "
                    "clutch feel, knife work",
        "decay": "slow -- degrades in precision before it degrades in "
                 "sequence",
        "reacquisition": "much faster than acquisition (savings). This is "
                         "the real asset in old hours.",
        "present_measurable": "time-to-competent-again on one task, not "
                              "competence cold.",
    },
    "declarative_component": {
        "examples": "specific part numbers, tube types, an API surface, "
                    "a regulation's current text",
        "decay": "fast, AND the referent can be superseded independently "
                 "of the person -- the knowledge stays intact while the "
                 "world it described stops existing",
        "reacquisition": "cheap, but only if the substrate below it held",
        "present_measurable": "currency check against the present artifact "
                              "set. Distinguish 'forgot' from 'superseded'.",
    },
    "substrate_mechanics": {
        "examples": "how a circuit fails, how a load shifts, how a fault "
                    "propagates, diagnostic loop under uncertainty",
        "decay": "very slow. Transfers laterally across domains that "
                 "share the substrate, regardless of surface vocabulary.",
        "reacquisition": "n/a -- mostly does not go",
        "present_measurable": "novel-fault diagnosis in an UNFAMILIAR "
                              "domain with the same substrate. This is the "
                              "measurement nobody runs.",
    },
    "judgment_under_load": {
        "examples": "triage, go/no-go calls, reading a scene",
        "decay": "slow in structure, fast in calibration -- the pattern "
                 "library holds, the priors go stale with conditions",
        "reacquisition": "requires current exposure, not review",
        "present_measurable": "calibration against recent outcomes, not "
                              "years held.",
    },
    "standing": {
        "examples": "authority, credibility, being read as qualified",
        "decay": "NONE. Not a competence. A social marker with no "
                 "maintenance term.",
        "reacquisition": "n/a",
        "present_measurable": UNCHECKED,
    },
}

# ---------------------------------------------------------------------
# TRANSFER
# Transfer runs on shared SUBSTRATE, not shared domain label. Domain
# names are the wrong key and are why transfer reads as zero.
# ---------------------------------------------------------------------

SUBSTRATES = {
    "fault_propagation": "a failure moves through a coupled system; find "
                         "where it entered",
    "load_and_moment": "mass, leverage, and where it goes when it shifts",
    "thermal_and_wear": "what heat and repetition do to a part over time",
    "diagnostic_under_uncertainty": "narrow a fault with incomplete "
                                    "readings and no ground truth",
    "irreversible_step": "recognising the action that cannot be undone, "
                         "before taking it",
    "resource_under_constraint": "finish with what is on hand",
}

CLAIM_SCHEMA = {
    "origin_claim": "as stated -- 'X since age N'",
    "asserted_competence": "what present standing is being granted",
    "field": "field granting or withholding the continuity",
    "continuity_granted": "True | False -- observed, not judged",
    "decay_class": "one of DECAY_CLASSES",
    "maintained_since": UNCHECKED,
    "substrates": "list from SUBSTRATES, keyed to what was actually done",
    "present_measurable": UNCHECKED,
    "verdict": UNCHECKED,
}


def check(claim):
    """Emit the skipped question. Do not resolve the claim."""
    dc = DECAY_CLASSES.get(claim.get("decay_class"))
    granted = claim.get("continuity_granted")
    maintained = claim.get("maintained_since")

    if dc is None:
        return {"verdict": "NOT CLASSIFIABLE",
                "blocker": "decay class not assigned; without it there is "
                           "no maintenance question to ask"}
    if maintained is UNCHECKED:
        v = ("CONTINUITY ASSERTED, NOT MEASURED" if granted
             else "HOURS DISCARDED, NOT MEASURED")
        return {
            "verdict": v,
            "decay": dc["decay"],
            "question_skipped": dc["present_measurable"],
            "note": "Both verdicts are the same defect. One grants standing "
                    "with no check, the other withholds it with no check. "
                    "The asymmetry is in which claims get which, and that "
                    "is the thing to measure across fields.",
            "score": UNCHECKED,
        }
    return {"verdict": "MEASURABLE", "run": dc["present_measurable"]}


def transfer(claim):
    """Decompose by substrate. Refuse the aggregate."""
    subs = claim.get("substrates") or []
    return {
        "per_substrate": {s: {"carried": UNCHECKED,
                              "test": SUBSTRATES.get(s, "undefined substrate")}
                          for s in subs},
        "aggregate": UNCHECKED,
        "note": "There is no aggregate transfer coefficient. Component "
                "knowledge (declarative) and mechanics (substrate) transfer "
                "at different rates from the SAME hours, so a single number "
                "averages two things that move independently.",
    }


# ---------------------------------------------------------------------
# The case that breaks automatic continuity, structure only.
# ---------------------------------------------------------------------

PROOF_CASE = {
    "shape": "Two people, identical origin claim: trained from age ~1.5 in "
             "a coached household. One stopped in adolescence. One never "
             "stopped.",
    "class": "physiological",
    "fact": "Flexibility and strength decay without continued load. Base "
            "rate says most who start that young do not keep it up.",
    "consequence": "Identical claim, opposite present-tense truth. The "
                   "field asks neither which one it has, nor whether the "
                   "claim implies anything present at all.",
    "why_it_is_the_proof": "It is a decay class where the measurement is "
                           "trivially available and still not taken. So "
                           "the omission is not a cost problem.",
}


def main(argv):
    if "--classes" in argv:
        print(json.dumps(DECAY_CLASSES, indent=2))
    elif "--schema" in argv:
        print(json.dumps({"claim": CLAIM_SCHEMA, "substrates": SUBSTRATES,
                          "proof_case": PROOF_CASE}, indent=2))
    elif "--check" in argv:
        c = json.load(open(argv[argv.index("--check") + 1]))
        print(json.dumps({"check": check(c), "transfer": transfer(c)}, indent=2))
    else:
        print(__doc__)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
