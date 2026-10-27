#!/usr/bin/env python3
# stability-trigger-envelope/test_envelope.py
#
# Checks for descent_record.py. Expected verdicts live HERE and not in
# cases.py, so a fixture cannot agree with the instrument by construction.
#
# The check total is printed and is not stored in any document: a count
# written into prose is a second place for it to drift.
#
# Standard library only. Parses under Python 3.9.

from __future__ import annotations

import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import cases
import descent_record as dr

CHECKS = 0


def ck(cond, label):
    global CHECKS
    CHECKS += 1
    if not cond:
        raise AssertionError("FAILED: " + label)


def carrier(n, period_samples, amp, onset_idx, rise_samples, phase_samples):
    """Same envelope as cases.burst, carrier shifted. Used to show the
    classifier does not read carrier phase."""
    out = []
    for i in range(n):
        if i < onset_idx:
            level = 0.0
        else:
            k = (i - onset_idx) / float(rise_samples)
            if k > 1.0:
                k = 1.0
            level = amp * k
        out.append(level * math.sin(2.0 * math.pi * (i - phase_samples)
                                    / period_samples))
    return out


def main() -> int:
    # ---------------------------------------------------------------- F1..F8
    r1 = dr.classify(cases.f1_cab_mode())
    ck(r1["verdict"] == "GEOMETRIC_CAB_MODE", "F1 returns GEOMETRIC_CAB_MODE")
    ck(r1["amplitude_ratio"] > 3.0, "F1 cab dominates in amplitude")
    ck(r1["cab_onset"]["state"] == "MEASURED", "F1 cab onset is timed")
    ck(r1["trailer_onset"]["state"] == "MEASURED", "F1 trailer onset is timed")
    ck(r1["onset_lead_s"] is not None and r1["onset_lead_s"] > 0,
       "F1 cab rises first")
    ck(abs(r1["onset_lead_s"] - 2.0) < 0.4,
       "F1 recovers the constructed one-reversal lead (2.0 s)")
    ck(r1["onset_agrees"] is True, "F1 onset agrees with amplitude")

    r2 = dr.classify(cases.f2_trailer_roll())
    ck(r2["verdict"] == "TRAILER_ROLL_RISK", "F2 returns TRAILER_ROLL_RISK")
    ck(r2["amplitude_ratio"] < 0.3334, "F2 trailer dominates in amplitude")
    ck(r2["onset_lead_s"] is not None and r2["onset_lead_s"] < 0,
       "F2 trailer rises first")
    ck(r2["onset_agrees"] is True, "F2 onset agrees with amplitude")

    r3 = dr.classify(cases.f3_no_trailer())
    ck(r3["verdict"] == "TRAILER_CHANNEL_ABSENT",
       "F3 returns TRAILER_CHANNEL_ABSENT")
    ck("has NOT been shown to be quiet" in r3["reason"],
       "F3 refuses the inference it would most invite")
    ck("amplitude_ratio" not in r3,
       "F3 computes no ratio against a body nobody measured")

    r4 = dr.classify(cases.f4_clock_skew())
    ck(r4["verdict"] == "NOT_EVALUABLE", "F4 returns NOT_EVALUABLE")
    ck("clocks" in r4["reason"] or "start times differ" in r4["reason"],
       "F4 names the clock offset")

    edge5 = dr.envelope_edge(cases.f5_two_runs(), "constructed-road-5")
    ck(edge5["state"] == "INSUFFICIENT_RUNS", "F5 returns INSUFFICIENT_RUNS")
    ck(edge5["runs_with_trigger"] == 2, "F5 has two runs with a trigger")
    ck(edge5["no_trigger_speeds"] == [26.0],
       "F5 keeps the no-trigger run rather than dropping it")

    r6 = dr.classify(cases.f6_out_of_envelope())
    ck(r6["verdict"] == "OUT_OF_ENVELOPE", "F6 returns OUT_OF_ENVELOPE")
    ck("ice" in r6["reason"], "F6 names the surface")

    r7 = dr.classify(cases.f7_axes_disagree())
    ck(r7["verdict"] == "NOT_EVALUABLE", "F7 returns NOT_EVALUABLE")
    ck(r7.get("onset_agrees") is False, "F7 records the disagreement")
    ck("opposite ways" in r7["reason"], "F7 names why it refuses")

    r8 = dr.classify(cases.f8_comparable())
    ck(r8["verdict"] == "NOT_EVALUABLE", "F8 returns NOT_EVALUABLE")
    ck("does not separate them" in r8["reason"],
       "F8 names what the record lacks")

    # every verdict in the closed vocabulary is reached by some fixture
    reached = set()
    for res in (r1, r2, r3, r4, r6, r7, r8):
        reached.add(res["verdict"])
    ck(reached == set(dr.VERDICTS),
       "every declared verdict is reached by a fixture: %s" % sorted(reached))

    # ------------------------------------------------- envelope_edge, both ways
    edge9 = dr.envelope_edge(cases.f9_enough_runs(), "constructed-road-9")
    ck(edge9["state"] == "MEASURED",
       "three runs with a trigger return an edge")
    ck(edge9["onset_speed_min"] == 29.0 and edge9["onset_speed_max"] == 36.0,
       "the edge carries its extremes")
    ck(abs(edge9["onset_speed_median"] - 32.0) < 1e-9, "the median is the middle run")
    ck(abs(edge9["spread_mph"] - 7.0) < 1e-9, "the edge carries a spread")
    ck(edge9["no_trigger_speeds"] == [24.0],
       "the no-trigger run is reported beside the edge, not inside it")
    ck(dr.envelope_edge(cases.f9_enough_runs(), "no-such-road")["state"]
       == "INSUFFICIENT_RUNS", "a road with no runs is insufficient, not empty")

    # --------------------------------------------- onset states stay apart
    floor = dr.threshold("onset_variance_floor")
    frac = dr.threshold("onset_frac")
    flat = dr.envelope([0.0] * 200, 5)
    ck(dr.onset(flat, 50.0, 0.0, frac, floor)["state"] == "NO_EVENT",
       "a still trace has NO_EVENT, not an onset at t=0")
    steady = dr.envelope(cases.burst(400, 100.0, 1.0, 0, 1), 25)
    ck(dr.onset(steady, 50.0, 0.0, frac, floor)["state"] == "NO_RISE",
       "a trace already moving at the first sample has NO_RISE")
    rising = dr.envelope(cases.burst(400, 100.0, 1.0, 150, 40), 25)
    ck(dr.onset(rising, 50.0, 0.0, frac, floor)["state"] == "MEASURED",
       "a burst that starts quiet has a measured onset")
    ck(set(dr.ONSET_STATES) == {"MEASURED", "NO_EVENT", "NO_RISE"},
       "the three onset states are declared")
    ck(dr.onset(flat, 50.0, 0.0, frac, floor)["state"]
       != dr.onset(steady, 50.0, 0.0, frac, floor)["state"],
       "nothing-moved and already-moving do not collapse")

    # ------------------------------- the classifier does not read carrier phase
    # Two cab traces with the SAME envelope and carriers half a period apart.
    # A phase reading moves between them; onset does not. This is the check
    # that the replacement is real rather than described.
    n, per = cases.N, cases.PERIOD_SAMPLES
    trl = dr.trace(0.0, cases.RATE_HZ, cases.burst(n, per, 0.15, 300, 40))
    cab_a = dr.trace(0.0, cases.RATE_HZ, carrier(n, per, 1.0, 200, 40, 0.0))
    cab_b = dr.trace(0.0, cases.RATE_HZ, carrier(n, per, 1.0, 200, 40, per / 2))
    base = cases.f1_cab_mode()
    rec_a = dict(base)
    rec_a["cab_imu"] = cab_a
    rec_a["trailer_imu"] = trl
    rec_b = dict(base)
    rec_b["cab_imu"] = cab_b
    rec_b["trailer_imu"] = trl
    ra = dr.classify(rec_a)
    rb = dr.classify(rec_b)
    ck(ra["verdict"] == rb["verdict"],
       "inverting the carrier does not move the verdict")
    ck(ra["onset_agrees"] == rb["onset_agrees"],
       "inverting the carrier does not move the agreement check")
    ck(abs(ra["onset_lead_s"] - rb["onset_lead_s"]) < 1e-9,
       "inverting the carrier does not move the onset lead")

    # and the same function on the RAW traces DOES move -- so the invariance
    # above is a property of reading envelopes, not of a weak comparison
    raw_a = dr.envelope_lag(cab_a["samples"], trl["samples"], cases.RATE_HZ,
                            2.0, 1.0)
    raw_b = dr.envelope_lag(cab_b["samples"], trl["samples"], cases.RATE_HZ,
                            2.0, 1.0)
    ck(raw_a["state"] == "MEASURED" and raw_b["state"] == "MEASURED",
       "the raw-trace lag computes for both carriers")
    ck(abs(raw_a["lead_s"] - raw_b["lead_s"]) > 0.5,
       "a raw-trace lag DOES move when the carrier is inverted, which is why "
       "it is not what the verdict reads")

    # -------------------------------------------------- schema and refusals
    rec = cases.f1_cab_mode()
    for key in rec:
        for token in dr.IDENTITY_TOKENS:
            ck(token not in key.lower(),
               "no schema field names a party: %r contains %r" % (key, token))
    ck(len(dr.IDENTITY_TOKENS) > 0, "the identity token list is not empty")

    try:
        cases._record(None, None, surface_state="gravel")
        ck(False, "an undeclared surface was accepted")
    except dr.SchemaError:
        ck(True, "an undeclared surface is refused")
    try:
        cases._record(None, None, downstream_event="delay")
        ck(False, "an undeclared downstream_event was accepted")
    except dr.SchemaError:
        ck(True, "an undeclared downstream_event is refused")
    try:
        dr.trace(0.0, 0.0, [1.0, 2.0])
        ck(False, "a non-positive sample rate was accepted")
    except dr.SchemaError:
        ck(True, "a non-positive sample rate is refused")
    try:
        dr.threshold("not_a_threshold")
        ck(False, "an undeclared threshold was accepted")
    except dr.SchemaError:
        ck(True, "an undeclared threshold is refused rather than defaulted")

    # a trace with a gap is refused rather than interpolated
    gapped = dict(cases.f1_cab_mode())
    bad = dict(gapped["cab_imu"])
    bad["gaps"] = 1
    gapped["cab_imu"] = bad
    rg = dr.classify(gapped)
    ck(rg["verdict"] == "NOT_EVALUABLE", "a gap in a trace refuses")
    ck("made up" in rg["reason"], "the gap refusal says why")

    # ------------------------------------------------------ relocation tally
    tally = dr.relocation_tally(cases.tally_set())
    ck(tally["score"] is None, "no composite score is emitted")
    ck("no composite" in tally["score_note"], "the refusal is stated")
    ck(tally["n_records"] == 9, "the tally carries its denominator")
    ck(tally["by_event"]["near_miss"] == 2, "near misses are counted")
    ck(tally["by_event"]["closure"] == 2, "closures are counted")
    ck(sum(tally["by_event"].values()) == tally["n_records"],
       "the event counts partition the records")
    ck(len(tally["by_access_bin"]) >= 2, "more than one access bin is used")
    for label in tally["by_access_bin"]:
        row = tally["by_access_bin"][label]
        ck(set(row.keys()) == set(dr.DOWNSTREAM_EVENTS),
           "every bin carries every event as a visible zero: %s" % label)

    # ------------------------------------------------------------ thresholds
    rows = dr._read_thresholds()
    chain = dr._chain_keys()
    for key in rows:
        ck(key in chain, "threshold %r has a provenance entry" % key)
    ck(len(rows) >= 12, "every threshold the module reads is declared")
    ck(all("UNPROVENANCED" not in line for line in dr.threshold_report()),
       "no declared threshold is unprovenanced today")

    # the instrument refuses --selftest rather than exiting 0 on an
    # invocation that runs nothing
    src = open(os.path.join(HERE, "descent_record.py")).read()
    ck("SystemExit(2)" in src,
       "descent_record.py refuses --selftest instead of passing silently")

    print("stability-trigger-envelope: %d checks, 0 failed" % CHECKS)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
