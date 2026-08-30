#!/usr/bin/env python3
# reverse_arm_score.py  -- CC0, stdlib only, phone-buildable
#
# R1 instrument. Scores episode transcripts for the reverse arm:
# a disguised executive reports UPWARD and is or is not listened to.
#
# The design's value is that the assessor is blind. The supervisor
# doing the dismissing does not know who they are dismissing. No
# strategic behaviour is available to them.
#
# This does not judge transcripts. It records four countable events
# per report-instance and refuses the aggregate until the coding is
# double-passed.
#
# usage:  python3 reverse_arm_score.py --schema
#         python3 reverse_arm_score.py episodes.json

import json
import sys

UNCODED = None

# ---------------------------------------------------------------------
# UNIT OF ANALYSIS: the report-instance, not the episode.
# One episode can contain several. Coding an episode as a whole
# collapses instances with different outcomes.
# ---------------------------------------------------------------------

INSTANCE_SCHEMA = {
    "episode_id": "",
    "timestamp": "in-transcript position",
    "reporter_seat": "disguised_exec | floor_worker",
    "receiver_role": "supervisor | manager | peer",
    "content_summary": "the finding, stated in the transcript's own terms",
    "domain": "whether the finding sits inside the reporter's real expertise",

    # --- the four scoreables ---
    "a_prior_filing": UNCODED,   # had a floor worker ALREADY reported this?
    "b_time_to_action": UNCODED,  # in-transcript beats until action, or NONE
    "c_attribution": UNCODED,     # who the fix is credited to at resolution
    "d_exec_testimony": UNCODED,  # post-reveal statement, coded below

    "receiver_blind": "True | False -- if False, DROP the instance",
}

SCOREABLES = {
    "a_prior_filing": {
        "why": "the credential-correction test running live: prior filing "
               "ignored, current filing acted on, same content",
        "values": ["YES_IGNORED", "YES_ACTED", "NO_PRIOR", "NOT_STATED"],
    },
    "b_time_to_action": {
        "why": "the discount is a delay, not always a refusal. Refusal is "
               "the tail of the distribution, not the measurement.",
        "values": ["integer beats", "NEVER", "NOT_STATED"],
    },
    "c_attribution": {
        "why": "a finding can be acted on and still be re-attributed. "
               "Action and credit are separate channels.",
        "values": ["EXEC_INSIGHT", "WORKER_WHO_SAID_IT", "UNATTRIBUTED",
                   "NOT_STATED"],
    },
    "d_exec_testimony": {
        "why": "distinguishes the two available readings of the whole genre",
        "values": [
            "LEARNED_ABOUT_OPERATION",   # forward reading; confounded
            "SAID_IT_AND_IT_WENT_NOWHERE",  # reverse reading; the finding
            "BOTH", "NEITHER", "NOT_STATED",
        ],
    },
}

# ---------------------------------------------------------------------
# CONTROL ARM. Without it the reverse arm has no denominator.
# ---------------------------------------------------------------------

CONTROL = {
    "requirement": "For every disguised-exec report-instance, code the "
                   "nearest floor-worker report-instance in the same "
                   "episode, same receiver where possible.",
    "reason": "The claim is not 'executives get dismissed.' It is that the "
              "SEAT sets the type. Without the floor-worker rate in the "
              "same setting, a dismissal rate is uninterpretable.",
    "expected_if_marker_holds": "disguised-exec instances score like "
                                "floor-worker instances, NOT like "
                                "known-exec instances elsewhere in the "
                                "same organisation",
    "falsifier": "disguised-exec reports acted on faster than equivalent "
                 "floor-worker reports -> R1 fails",
}

# ---------------------------------------------------------------------
# The genre confound the coding must survive.
# ---------------------------------------------------------------------

CONFOUNDS = {
    "editing": "Produced television selects for a reveal. This biases the "
               "FORWARD arm heavily. It biases the reverse arm only if "
               "editors were selecting for dismissal scenes, which is not "
               "the genre's payoff structure -- but code episode air order "
               "and network so it can be checked rather than assumed.",
    "performance": "The disguised person may under-perform deliberately or "
                   "from genuine unfamiliarity. This affects the COMEDY "
                   "BEAT (task competence) and NOT the report-instances "
                   "(verbal findings). Keep the two separate. Do not code "
                   "task-failure scenes as report-instances.",
    "receiver_suspicion": "If the receiver suspects the setup, blindness is "
                          "broken. Code it, drop the instance.",
}


def score(instances):
    """Per-instance rates by seat. No aggregate until double-coded."""
    by_seat = {}
    for i in instances:
        if i.get("receiver_blind") is False:
            continue
        s = by_seat.setdefault(i.get("reporter_seat"), {
            "n": 0, "prior_ignored": 0, "never_acted": 0,
            "credited_to_exec": 0, "credited_to_worker": 0})
        s["n"] += 1
        if i.get("a_prior_filing") == "YES_IGNORED":
            s["prior_ignored"] += 1
        if i.get("b_time_to_action") == "NEVER":
            s["never_acted"] += 1
        if i.get("c_attribution") == "EXEC_INSIGHT":
            s["credited_to_exec"] += 1
        if i.get("c_attribution") == "WORKER_WHO_SAID_IT":
            s["credited_to_worker"] += 1
    return {
        "by_seat": by_seat,
        "contrast": UNCODED,
        "verdict": UNCODED,
        "note": "Contrast and verdict stay None until (1) both arms have "
                "instances and (2) a second coder has passed the same "
                "transcripts blind to the first coding. A single-coder "
                "rate on a hypothesis the coder holds is not a measurement.",
    }


def main(argv):
    if "--schema" in argv or len(argv) < 2:
        print(json.dumps({"instance": INSTANCE_SCHEMA,
                          "scoreables": SCOREABLES,
                          "control": CONTROL,
                          "confounds": CONFOUNDS}, indent=2))
        return 0
    print(json.dumps(score(json.load(open(argv[1]))), indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
