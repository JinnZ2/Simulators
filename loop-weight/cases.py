# cases.py
# CC0 1.0 Universal / public domain dedication.
#
# Hand-built case set for loop_weight.py. RAW INPUTS ONLY: every case carries
# the described path, the independent comparisons and the scored predictions.
# No case carries a precomputed L, R, C or verdict -- the expected verdict
# lives in the test file, so a case cannot agree with the module by
# construction.
#
# Every case is CONSTRUCTED. None is a measurement of any real source, and no
# real person, employer or publication is named anywhere in this file. The
# referents are generic on purpose: the instrument reads path structure, and
# a recognisable referent would invite the reader to score the case from what
# they already believe about it.
#
# Cases A and C are the falsifiers named in the work order. If C cannot be
# shown to carry more than A, the instrument has rebuilt an authority claim
# with "short loop" as the new credential and fails.

def _cmp(cid, other_hop_ids, asserted, agreement, supplied_by):
    """One comparison against another instrument on the same referent."""
    return {"id": cid, "other_hop_ids": other_hop_ids,
            "independence_asserted": asserted, "agreement": agreement,
            "supplied_by": supplied_by}


def _pred(pid, stated_at, resolved_at, correct, by, supplied_by):
    """One prior prediction scored against an outcome. `by` is who defined,
    selected and timed the outcome -- for C-2 it must not be the source."""
    return {"id": pid, "stated_at": stated_at, "resolved_at": resolved_at,
            "correct": correct, "outcome_defined_by": by,
            "outcome_selected_by": by, "outcome_timed_by": by,
            "supplied_by": supplied_by}


CASE_A = {
    # One hop. Nobody else observes this referent, and nothing this source
    # has said has ever been scored. The always-wrong instrument is
    # indistinguishable from the always-right one from here, and the short
    # loop must not rescue it.
    "source_id": "A_one_hop_unchecked",
    "referent": "line pressure at the outlet valve",
    "path": [{"id": "a_h1", "kind": "stood at the gauge", "retention": 1.0}],
    "comparisons": [],
    "predictions": [],
}

CASE_B = {
    # One hop, and the readings have been scored against outcomes resolved
    # by a party that did not take the readings.
    "source_id": "B_one_hop_scored",
    "referent": "time to failure of the outlet seal",
    "path": [{"id": "b_h1", "kind": "stood at the gauge", "retention": 1.0}],
    "comparisons": [],
    "predictions": [
        _pred("b_p1", "2024-02-01", "2024-03-04", True, "maintenance_log", "auditor"),
        _pred("b_p2", "2024-02-08", "2024-04-19", True, "maintenance_log", "auditor"),
        _pred("b_p3", "2024-03-02", "2024-05-30", False, "maintenance_log", "auditor"),
        _pred("b_p4", "2024-04-11", "2024-06-12", True, "maintenance_log", "auditor"),
        _pred("b_p5", "2024-05-06", "2024-08-01", True, "maintenance_log", "auditor"),
        _pred("b_p6", "2024-06-22", "2024-09-14", True, "maintenance_log", "auditor"),
        # excluded: the source set the terms this one was scored on.
        _pred("b_p7", "2024-07-01", "2024-09-20", True, "B_one_hop_scored", "auditor"),
    ],
}

CASE_C = {
    # Four hops, each a documented verbatim relay, and the chain's readings
    # have been scored against outcomes nobody in the chain defined. The long
    # loop must be able to carry more than case A.
    "source_id": "C_four_hop_relay",
    "referent": "ice thickness on the north crossing",
    "path": [
        {"id": "c_h1", "kind": "crossed it and recorded a depth", "retention": 0.98},
        {"id": "c_h2", "kind": "read the recorded depth into a log", "retention": 0.95},
        {"id": "c_h3", "kind": "copied the log verbatim", "retention": 0.97},
        {"id": "c_h4", "kind": "transcribed the copy verbatim", "retention": 0.96},
    ],
    "comparisons": [],
    "predictions": [
        _pred("c_p1", "2023-11-02", "2023-12-20", True, "crossing_register", "auditor"),
        _pred("c_p2", "2023-11-15", "2024-01-08", True, "crossing_register", "auditor"),
        _pred("c_p3", "2023-12-01", "2024-01-22", True, "crossing_register", "auditor"),
        _pred("c_p4", "2023-12-14", "2024-02-03", False, "crossing_register", "auditor"),
        _pred("c_p5", "2024-01-04", "2024-02-19", True, "crossing_register", "auditor"),
        _pred("c_p6", "2024-01-18", "2024-03-01", True, "crossing_register", "auditor"),
        _pred("c_p7", "2024-02-02", "2024-03-17", True, "crossing_register", "auditor"),
        _pred("c_p8", "2024-02-16", "2024-04-02", True, "crossing_register", "auditor"),
        _pred("c_p9", "2024-03-05", "2024-04-21", True, "crossing_register", "auditor"),
        _pred("c_p10", "2024-03-19", "2024-05-06", True, "crossing_register", "auditor"),
    ],
}

CASE_D = {
    # Two hops. The second hop is a summary written to a length limit that
    # drops most of what it was given. R dominates: the short path does not
    # override a channel measured not to carry.
    "source_id": "D_two_hop_lossy",
    "referent": "sequence of events during the shutdown",
    "path": [
        {"id": "d_h1", "kind": "operated the panel", "retention": 0.9},
        {"id": "d_h2", "kind": "wrote a one-line summary of the shift", "retention": 0.2},
    ],
    "comparisons": [],
    "predictions": [],
}

CASE_E = {
    # One hop, scored, and wrong. Measured low is a different state from
    # unmeasured and gets its own return.
    "source_id": "E_one_hop_wrong",
    "referent": "yield of the second cut",
    "path": [{"id": "e_h1", "kind": "walked the field", "retention": 1.0}],
    "comparisons": [],
    "predictions": [
        _pred("e_p1", "2024-04-02", "2024-07-30", False, "weighbridge", "auditor"),
        _pred("e_p2", "2024-04-20", "2024-08-02", False, "weighbridge", "auditor"),
        _pred("e_p3", "2024-05-11", "2024-08-15", True, "weighbridge", "auditor"),
        _pred("e_p4", "2024-05-29", "2024-08-28", False, "weighbridge", "auditor"),
        _pred("e_p5", "2024-06-14", "2024-09-09", False, "weighbridge", "auditor"),
    ],
}

CASE_F = {
    # Six hops, one of them with retention nobody has measured, and the only
    # comparison on offer runs back through a hop the source is already on.
    # The assertion of independence is contradicted by the shared hop, which
    # is reported rather than overridden silently. Unknown retention does not
    # make this LOSSY: unknown is not low.
    "source_id": "F_six_hop_unchecked",
    "referent": "condition of the upstream weir",
    "path": [
        {"id": "f_h1", "kind": "inspected the weir", "retention": 0.94},
        {"id": "f_h2", "kind": "filed a condition note", "retention": 0.9},
        {"id": "f_h3", "kind": "entered the note in a register", "retention": 0.88},
        {"id": "f_h4", "kind": "summarised the register", "retention": None},
        {"id": "f_h5", "kind": "quoted the summary", "retention": 0.85},
        {"id": "f_h6", "kind": "repeated the quotation", "retention": 0.8},
    ],
    "comparisons": [
        _cmp("f_c1", ["f_h2", "x_h9"], True, 0.95, "auditor"),
        _cmp("f_c2", ["y_h1", "y_h2"], False, 0.6, "auditor"),
    ],
    "predictions": [],
}

CASE_G = {
    # Five hops and three genuinely independent instruments on the same
    # referent, all of which read it differently.
    "source_id": "G_five_hop_diverging",
    "referent": "depth of the channel at the bar",
    "path": [
        {"id": "g_h1", "kind": "sounded the channel", "retention": 0.92},
        {"id": "g_h2", "kind": "logged the sounding", "retention": 0.9},
        {"id": "g_h3", "kind": "compiled the log", "retention": 0.88},
        {"id": "g_h4", "kind": "redrew the compilation", "retention": 0.86},
        {"id": "g_h5", "kind": "reissued the drawing", "retention": 0.9},
    ],
    "comparisons": [
        _cmp("g_c1", ["p_h1", "p_h2"], True, 0.2, "auditor"),
        _cmp("g_c2", ["q_h1"], True, 0.3, "auditor"),
        _cmp("g_c3", ["r_h1", "r_h2"], True, 0.25, "auditor"),
    ],
    "predictions": [],
}

CASE_H = {
    # The report exists and the path behind it is not described. L is not
    # inferred from what kind of source this is; the read is refused.
    "source_id": "H_path_not_described",
    "referent": "cause of the outage",
    "path": None,
    "comparisons": [],
    "predictions": [],
}

CASE_I = {
    # One hop. Three comparisons, none of which shares a hop with the source,
    # so all three are admissible -- but two of them run through one shared
    # wire and are one instrument, not two. Taken as three the mean agreement
    # clears the calibration floor; taken as two independent classes it does
    # not. This case exists so the rule that correlated instruments count
    # once can be shown to change a verdict rather than only to be stated.
    "source_id": "I_correlated_others",
    "referent": "level in the holding tank",
    "path": [{"id": "i_h1", "kind": "read the sight glass", "retention": 1.0}],
    "comparisons": [
        _cmp("i_c1", ["shared_wire", "s_h1"], True, 0.9, "auditor"),
        _cmp("i_c2", ["shared_wire", "s_h2"], True, 0.9, "auditor"),
        _cmp("i_c3", ["t_h1"], True, 0.3, "auditor"),
    ],
    "predictions": [],
}

CASE_J = {
    # Both derivations land and they disagree: the source agrees with its
    # peers and fails against outcomes none of them set. C takes the lower
    # value and the disagreement is printed, because which of the two is
    # right is not decidable from inside this instrument.
    "source_id": "J_derivations_disagree",
    "referent": "moisture at the core of the stack",
    "path": [{"id": "j_h1", "kind": "probed the stack", "retention": 1.0}],
    "comparisons": [
        _cmp("j_c1", ["u_h1"], True, 0.9, "auditor"),
        _cmp("j_c2", ["v_h1"], True, 0.9, "auditor"),
    ],
    "predictions": [
        _pred("j_p1", "2024-01-09", "2024-02-14", False, "dryer_record", "auditor"),
        _pred("j_p2", "2024-01-23", "2024-03-01", False, "dryer_record", "auditor"),
        _pred("j_p3", "2024-02-06", "2024-03-19", True, "dryer_record", "auditor"),
        _pred("j_p4", "2024-02-20", "2024-04-04", False, "dryer_record", "auditor"),
        _pred("j_p5", "2024-03-07", "2024-04-18", False, "dryer_record", "auditor"),
    ],
}

CASES = [CASE_A, CASE_B, CASE_C, CASE_D, CASE_E,
         CASE_F, CASE_G, CASE_H, CASE_I, CASE_J]


# Refused at load, not scored and not silently dropped. C may not be set from
# an input whose provenance is the source being calibrated, and an input with
# no stated provenance cannot be shown not to be one.
REFUSED_SELF_SUPPLIED = {
    "source_id": "R1_grades_itself",
    "referent": "accuracy of its own readings",
    "path": [{"id": "r1_h1", "kind": "read the gauge", "retention": 1.0}],
    "comparisons": [_cmp("r1_c1", ["w_h1"], True, 0.95, "R1_grades_itself")],
    "predictions": [],
}

REFUSED_NO_PROVENANCE = {
    "source_id": "R2_provenance_unstated",
    "referent": "flow at the intake",
    "path": [{"id": "r2_h1", "kind": "read the meter", "retention": 1.0}],
    "comparisons": [],
    "predictions": [
        {"id": "r2_p1", "stated_at": "2024-01-01", "resolved_at": "2024-02-01",
         "correct": True, "outcome_defined_by": "intake_register",
         "outcome_selected_by": "intake_register", "outcome_timed_by": "intake_register",
         "supplied_by": None},
    ],
}

REFUSED = [REFUSED_SELF_SUPPLIED, REFUSED_NO_PROVENANCE]
