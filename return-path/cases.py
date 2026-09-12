# SPDX-License-Identifier: CC0-1.0
"""
Hand-built channels for return_path.py.

EVERY CASE IS CONSTRUCTED. No channel here is a measurement of any real
correction channel, and every number is stipulated by the person who typed
it. A, B, C, D and E are the order's own validation cases; the rest exist
so that each return state and each flag is reachable by something -- a
declared state no case populates cannot be told from a state nobody looked
for.

Raw inputs only. No expected verdict lives in this file: expectations are
in test_return.py, so no case can agree with the module by construction.

Where the order's description of a case does not fix a field, the value is
marked [STIPULATED] in the scope_note, which is carried verbatim and parsed
by nothing.

CC0.
"""

# A -- direct physical consequence. The order's first case, and the one it
# says the instrument must pass or it is not a diagnostic.
A_physical_consequence = {
    "channel_id": "A_physical_consequence",
    "receipt": "MANDATORY",
    "signal_encodings": 0,
    "encoder_position": "NONE",
    "latency": 0.0,
    "build_on_time": 720.0,
    "time_unit": "hours",
    "construction": "SLOW_SIDE_ONLY",
    "scope_note": ("CONSTRUCTED. A load fails under an unrated part; the "
                   "failure arrives at the operator, unwritten, at the "
                   "moment of failure. [STIPULATED] build_on_time 720 h."),
}

# B -- fast, well-run, ignorable. Same-day turnaround, elective receipt.
B_incident_reporting = {
    "channel_id": "B_incident_reporting",
    "receipt": "ELECTIVE",
    "signal_encodings": 0,
    "encoder_position": "NONE",
    "latency": 8.0,
    "build_on_time": 720.0,
    "time_unit": "hours",
    "construction": "SLOW_SIDE_ONLY",
    "scope_note": ("CONSTRUCTED. Same-day turnaround that the receiving "
                   "party may decline to act on. Encodings held at 0 and "
                   "construction at SLOW_SIDE_ONLY so the case isolates C1, "
                   "which is what the order asks it to test; a real "
                   "incident report would carry at least one encoding."),
}

# B again, entered as its own name describes it. An incident REPORTING
# system writes a report, which is at least one encoding, so C2 fires too
# and the case cannot "fail C1 ONLY". Both readings ship; neither is picked.
B_report_written = dict(B_incident_reporting,
                        channel_id="B_report_written",
                        signal_encodings=1,
                        encoder_position="THIRD_PARTY")
B_report_written["scope_note"] = (
    "CONSTRUCTED. The order requires case B to fail C1 and nothing else, "
    "and the channel it describes is one where somebody writes an incident "
    "report. Entered faithfully the case fails C1 and C2, so the stated "
    "requirement holds only of the encodings-0 entry above.")


# C -- the 1-2 year anonymous publication loop.
C_publication_loop = {
    "channel_id": "C_publication_loop",
    "receipt": "ELECTIVE",
    "signal_encodings": 2,
    "encoder_position": "SLOW_SIDE",
    "latency": 18.0,
    "build_on_time": 3.0,
    "time_unit": "months",
    "construction": "SLOW_SIDE_ONLY",
    "scope_note": ("CONSTRUCTED. Gaps posted, carried by crawlers, "
                   "published later, statistics read back. Two encodings: "
                   "the post, then the published statistic. [CHOICE 7] "
                   "encoder_position names the first encoder. [STIPULATED] "
                   "latency 18 months, build_on_time 3 months."),
}

# D -- field observation against a corpus claim. The order fixes C1, C3 and
# C4 and leaves C2 open, so the case ships as two channels differing in one
# field, rather than as one channel with a field picked quietly.
D_field_report_written = {
    "channel_id": "D_field_report_written",
    "receipt": "ELECTIVE",
    "signal_encodings": 1,
    "encoder_position": "SLOW_SIDE",
    "latency": 40.0,
    "build_on_time": 2.0,
    "time_unit": "years",
    "construction": "REQUIRES_THIRD_PARTY",
    "scope_note": ("CONSTRUCTED. Long-baseline direct observation of a "
                   "behaviour the published record describes differently; "
                   "the observer writes it up. [STIPULATED] latency 40 y: "
                   "the elapsed standing time of the observation, entered "
                   "because the intake has no value for a channel that "
                   "does not exist. See D_no_channel."),
}

D_field_no_report = dict(D_field_report_written,
                         channel_id="D_field_no_report",
                         signal_encodings=0,
                         encoder_position="NONE")
D_field_no_report["scope_note"] = (
    "CONSTRUCTED. Same observation, nothing written. The order leaves C2 "
    "open on case D and this is the other half of it.")

# D again, entered as the order describes it rather than as the intake can
# hold it: no channel exists, so no latency exists.
D_no_channel = dict(D_field_report_written, channel_id="D_no_channel")
del D_no_channel["latency"]
D_no_channel["scope_note"] = (
    "CONSTRUCTED. The order says of case D that no channel exists from the "
    "observation to the claim. A channel that does not exist has no "
    "latency, so the honest entry omits the field and the return is "
    "INTAKE_INCOMPLETE -- which is not the verdict the order requires of "
    "case D. Both readings ship; neither is picked.")

# E -- FALSIFIER. The party being corrected writes the correction.
E_fast_side_writes = {
    "channel_id": "E_fast_side_writes",
    "receipt": "MANDATORY",
    "signal_encodings": 1,
    "encoder_position": "FAST_SIDE",
    "latency": 1.0,
    "build_on_time": 100.0,
    "time_unit": "hours",
    "construction": "SLOW_SIDE_ONLY",
    "scope_note": ("CONSTRUCTED. Everything ideal except that the party "
                   "being corrected writes the correction."),
}

# --- reachability. Each of these exists because some declared state is
# otherwise populated by nothing.

F_receipt_unspecified = dict(A_physical_consequence,
                             channel_id="F_receipt_unspecified",
                             receipt="UNSPECIFIED")
F_receipt_unspecified["scope_note"] = (
    "CONSTRUCTED. Receipt not stated. Scored as ELECTIVE and flagged, so "
    "the unknown is scored in the failing direction rather than the "
    "flattering one.")

G_build_on_time_absent = dict(A_physical_consequence,
                              channel_id="G_build_on_time_absent")
del G_build_on_time_absent["build_on_time"]
G_build_on_time_absent["scope_note"] = (
    "CONSTRUCTED. The order's Open section: nobody measures when output "
    "starts being built on, so this is the return it expects to be most "
    "common. A finding about the system, not a defect in the instrument.")

H_build_on_time_zero = dict(A_physical_consequence,
                            channel_id="H_build_on_time_zero",
                            build_on_time=0.0)
H_build_on_time_zero["scope_note"] = (
    "CONSTRUCTED. Output built on the moment it exists. C3 is computable "
    "here and the ratio is not: the check and the number the order pairs "
    "with it have different domains.")

I_receipt_out_of_vocabulary = dict(A_physical_consequence,
                                   channel_id="I_receipt_out_of_vocabulary",
                                   receipt="probably mandatory")
I_receipt_out_of_vocabulary["scope_note"] = (
    "CONSTRUCTED. A value outside the declared set. Scoring it as ELECTIVE "
    "would be inference; it lands in `invalid`, not in `missing`.")

J_encoder_none_above_zero = dict(A_physical_consequence,
                                 channel_id="J_encoder_none_above_zero",
                                 signal_encodings=1)
J_encoder_none_above_zero["scope_note"] = (
    "CONSTRUCTED. The order's one cross-field rule: encoder_position NONE "
    "is valid only at zero encodings.")

CASES = (A_physical_consequence, B_incident_reporting, B_report_written,
         C_publication_loop,
         D_field_report_written, D_field_no_report, D_no_channel,
         E_fast_side_writes, F_receipt_unspecified, G_build_on_time_absent,
         H_build_on_time_zero, I_receipt_out_of_vocabulary,
         J_encoder_none_above_zero)

BY_ID = {c["channel_id"]: c for c in CASES}
