# CLAIM TABLE — stability-trigger-envelope

Claims from building `descent_record.py` for DISPATCH ESP-1. Ids are
permanent. `WORK_ORDER.md` is untouched.

**REFUTATION PROTOCOL.** The thresholds are PLACEHOLDER and the gate order is
the claim. A failing check updates the claim, not the threshold. A threshold
changes only by an appended log entry that names the run behind it.

Everything below is about the code on CONSTRUCTED data. No claim here is
about any road, unit or operator.

---

### STE_001 — the five planted faults fire

F1 → GEOMETRIC_CAB_MODE, F2 → TRAILER_ROLL_RISK, F3 → TRAILER_CHANNEL_ABSENT,
F4 → NOT_EVALUABLE (clocks 3.0 s apart), F5 → INSUFFICIENT_RUNS.

These fixtures were written by the same hand as the classifier. They are
**REGRESSION, not validation**: they show the code keeps doing what it was
written to do, and nothing about whether Fault A holds on any unit.

**Falsifier:** any fixture label changes without a claim update.
**Status: SUPPORTED (regression only).**

---

### STE_002 — the classifier is not constant

Across F1–F5 and X1–X5, six distinct `classify` labels are reached. A
classifier that returned GEOMETRIC_CAB_MODE for everything would pass F1 and
support Fault A by construction. The test requires all six labels.

**Status: SUPPORTED.**

---

### STE_003 — absence is never read as a negative

A missing trailer trace yields TRAILER_CHANNEL_ABSENT, never "trailer quiet".
A missing sync mark, missing timestamp, uncovered window or sample gap yields
NOT_EVALUABLE with the reason. A surface or grade outside the declared range
yields OUT_OF_ENVELOPE, which the render states as "unassessed, not clear".
These gates run before any reading is taken, so no RMS value is ever computed
from a trace the gate has refused.

**Falsifier:** any input path that reaches a GEOMETRIC_CAB_MODE or
TRAILER_ROLL_RISK label with a channel absent.
**Status: SUPPORTED on the tested paths.**

---

### STE_004 — NEITHER_MODE is an addition to the work order's label set

The dispatch lists five labels. Three states fit none of them:

```
both channels quiet
cab high, trailer leads
cab high, lead unresolved (peak envelope correlation < lead_corr_min)
```

Folding them into GEOMETRIC_CAB_MODE would manufacture support for Fault A.
Folding them into TRAILER_ROLL_RISK would manufacture its falsifier. The
added label carries its reason. X3 and X4 exercise it.

**Status: DECLARED deviation from the work order.**

---

### STE_005 — clock offsets are detected, never corrected

Misalignment is the disagreement between the two traces' sync marks. Above
`clock_misalign_max_s`, the run is NOT_EVALUABLE. No trace is shifted. Phone
clock drift is unmeasured, and a shift can fabricate the lead T1 tests for.
The loader refuses any threshold file where the misalignment tolerance is at
or above `phase_window_min_s`, so an allowed offset can never read as a lead.

**Falsifier:** a threshold file with tolerance ≥ phase floor that loads.
**Status: SUPPORTED (mutation test).**

---

### STE_006 — the lead is read from envelopes, not raw roll

Raw roll on a serpentine is quasi-periodic, so its cross-correlation peaks at
every whole reversal and the lag is ambiguous by a period. The moving-RMS
envelope carries the onset. F1's constructed trailer starts 4.0 s after the
cab, and the envelope lag reads 3.95 s at r = 0.985. X4, where the trailer
starts first, reads a negative lag and TRAILER_LEADS.

**Falsifier:** a real paired trace where the envelope lag disagrees with a
hand-marked onset by more than the phase floor.
**Status: SUPPORTED on constructed traces; UNVERIFIED on field data.**

---

### STE_007 — thresholds are append-only and every one is PLACEHOLDER

`thresholds.json` is a sequential log. The loader takes the last entry per key,
refuses a broken sequence or an unknown status, and every Reading prints the
status it ran under. The test pins a sha256 of the shipped prefix (seq 1–16):
an in-place edit fails, an append passes.

**Status: SUPPORTED. Every value UNMEASURED.**

---

### STE_008 — relocation is counted, never scored

`relocation_tally` returns counts by `downstream_event` (every event present,
zeros included) and by V2 bin. It has no total, score, sum or index key, and
the counts conserve the record count. The work order's point is that orders
2–4 leave no trace in the safety score; collapsing them into one number would
repeat that loss one level up.

**Status: SUPPORTED.**

---

### STE_009 — the envelope edge reports what the runs support, and no more

`envelope_edge` returns INSUFFICIENT_RUNS below 3 runs on a road;
NO_TRIGGER_OBSERVED with only a lower bound when nothing fired;
EDGE_BRACKETED when every quiet run is slower than every fired run;
ONSET_OVERLAP when a quiet run sits at or above a fired speed (the trigger is
then being moved by something other than speed). Mixed grades or surfaces on
one road are listed in `mixed_conditions`, not pooled silently.

**Status: SUPPORTED on constructed runs.**

---

### STE_010 — nothing about the unit, the road or the faults is verified here

```
Fault A on the operator's unit      UNVERIFIED   T1 NOT_RUN
Fault B (sign inversion)            UNVERIFIED   no instrument; DERIVED only
Fault C (grade/bank offset)         UNVERIFIED   T2 NOT_RUN; bank unmeasured
controller grade/bank estimation    UNREAD       proprietary
Bendix sources, patents             NOT_FETCHED  SECONDARY, carried as given
```

**Status: UNVERIFIED.**

---

### STE_011 — a sub-period trailer lead is resolved, on the constructed fixture

Added on the 2026-09-27b carried audit question 3 (a fixture to exercise the
sibling repository's `NC_023`, the sub-period lead). X6 constructs the trailer
starting 2.0 s before the cab, a quarter of the 8 s forcing period, so the
lead is inside one period and a whole-period ambiguity (STE_006, the sibling's
ESP_003 / NC_013) cannot rescue it. First-run result, recorded before any
repair and with no threshold moved:

```
X6  cab high, trailer leads by 2.0 s   got NEITHER_MODE   lead TRAILER_LEADS
    trailer_lag_s -1.8   lag_corr 0.979   cab_rms 3.347   trailer_rms 0.382
```

The envelope lag reads 1.8 s against a constructed 2.0 s: 0.2 s short, four
grid steps, on a 4.0 s moving-RMS window. The sign and the class are right;
the magnitude is not exact and is reported as read. Nothing is retuned; the
expectation registered in `route-independence/EXPECTED_2026-09-27b.md` (Q3)
held.

**Falsifier:** a constructed sub-period lead that reads CAB_LEADS or
SIMULTANEOUS, or a real paired trace where a hand-marked sub-period lead
reads the other sign.
**Status: SUPPORTED on the constructed fixture; UNVERIFIED on field data.**
