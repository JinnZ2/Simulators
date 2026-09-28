# stability-trigger-envelope — claim table

Claims are `ESP_*` and are about THIS FOLDER: the instrument, the design and
the record. They are distinct from the work order's own FAULT A/B/C, V1-V5
and T1-T6, none of which this folder establishes.

The order's faults are DERIVED from one operator's account at N=1. Nothing
below upgrades any of them.

```
python3 test_envelope.py    # the checks, total printed
```

---

## The instrument

| id | claim | status |
|----|-------|--------|
| ESP_001 | **`TRAILER_CHANNEL_ABSENT` is an absence and is never inferred.** A trailer that was not instrumented has not been shown to be quiet. The whole of FAULT A turns on that difference: a correct reading of the cab says nothing about the body carrying the at-risk mass. `classify()` returns the absence before computing any ratio, so no number is produced against a body nobody measured. | RUN, 217/0 |
| ESP_002 | **Onset timing replaces the phase window, and the replacement is checked behaviourally.** Two cab traces with identical envelopes and carriers half a period apart must return the same verdict, the same agreement and the same onset lead; the same lag function on the raw traces must move. If a phase reading were still in the decision path the first assertion fails. The order's section 6 says "phase window" and is superseded by its own author's later instruction — see RUN_NOTE CHOICE 1. | RUN, 217/0 |
| ESP_003 | **A phase lead cannot read the case's own prediction.** The case predicts the cab leading the trailer by about one curve reversal. A cross-correlation of two periodic traces fixes the lead only modulo one period, so a lead of one reversal and a lead of nothing give the same peak. Measured in the sibling repository (`Noise-as-Information-Sensor`, `NC_013`): a constructed lag of 4 samples in a 40-sample period returned as a lead of 36, and the sign of that lead was deciding a verdict. | SUPPORTED elsewhere, carried |
| ESP_004 | **Amplitude and onset disagreeing returns `NOT_EVALUABLE`, not a verdict with a caveat.** F7 is the fixture. Two readings pointing opposite ways is not a finding. | RUN, 217/0 |
| ESP_005 | **Three onset states are kept apart.** `MEASURED` (a rise, timed), `NO_EVENT` (nothing moved), `NO_RISE` (already moving at the first sample, so the onset is outside the record). Only one is a measurement and the three call for different next actions. A steady oscillation returns `NO_RISE` rather than an onset at t=0, which would otherwise be an artifact of the envelope window shortening at the edge. | RUN, 217/0 |
| ESP_006 | **`OUT_OF_ENVELOPE` is the reader's envelope, not the vehicle's.** Measuring the vehicle's validation envelope is T2 and T5, neither run. Snow and ice are excluded because V5 says the margin is gone there — a refusal to report, and the opposite of a finding that nothing happens on ice. | RUN, 217/0 |
| ESP_007 | **Runs where nothing fired are kept and reported apart.** A descent with no trigger bounds the onset-speed edge from below; dropping it leaves the edge looking tighter than the data supports. `envelope_edge()` reports those speeds beside the edge and never inside it, and returns `INSUFFICIENT_RUNS` below three triggered runs because an edge without a spread is a point pretending to be a measurement. | RUN, 217/0 |
| ESP_008 | **No composite is emitted anywhere.** `relocation_tally()` returns counts by event and by access bin with `score: None` and the refusal stated in the return. A relocation index would repeat the move that lost orders 2-4: several costs collapsed into one number, comparable against a safety score built from different terms over a different denominator. | RUN, 217/0 |
| ESP_009 | **The no-characterization rule is structural.** There is no schema field for the operator, the carrier, the unit, or for how anyone drove, and `test_envelope.py` reads the record's own field names against a token list rather than trusting a sentence. T2's "correctly driven" is the one place the design asks for a judgement about driving, and it is left to the operator to declare per run with no field to store it in. | RUN, 217/0 |

## The state of this folder

| id | claim | status |
|----|-------|--------|
| ESP_010 | **Written blind, then run once: 217 checks, 0 failed.** First filing (2026-09-24): `descent_record.py`, `cases.py` and `test_envelope.py` were written in a session whose command execution was unavailable; F1-F5 were SPECIFIED to fire and not OBSERVED to fire, and the first run was named as the acceptance test. Resolution (2026-09-27): execution returned intermittently, `test_envelope.py` ran on the first attempt and printed `217 checks, 0 failed`, with no edit to any of the three files between writing and running. What that establishes: every assertion in the test file holds of the code, including the carrier-inversion check behind ESP_002 and the reachability of all five verdicts. What it does not: `descent_record.py`'s render path (`main()` and the three `render_*` formatters) has not been executed, and the rest of the block stands. Kept as a sequence rather than overwritten, since a module written without a runner and found to pass is a different record from one checked as it went. | RUN, 217/0; render unobserved |
| ESP_011 | **The fixtures are REGRESSION, not validation.** Every trace is generated by `cases.burst()` and every fixture was authored by the same hand that wrote the classifier. They can show a planted fault fires. They cannot show the classifier reads a real descent, which is T1. | SPECIFIED |
| ESP_012 | **Every threshold is PLACEHOLDER.** Nine values, each with an append-only provenance entry naming a builder rather than an operator, and each saying what would set it properly. The amplitude ratio that separates the two bodies is a round number. The verdicts move with these values and no measurement is behind any of them. | SUPPORTED |
| ESP_013 | **Every source is UNREAD.** The four items in section 8 are carried from the order at SECONDARY. None was retrieved, read or checked in this session, and no claim in this folder rests on the content of any of them. The reference sensor mounting — a cross-member near the back of the cab — is the load-bearing one for FAULT A and it is exactly the one nobody here has verified. | UNVERIFIED |
| ESP_014 | **FAULT B is the best-argued and least-tested of the three.** No test in T1-T6 addresses it, and none is specified here, because testing it means commanding a brake application on a descent with a loaded trailer. No bench or simulation substitute is designed. The gap is named rather than filled. | NOT BUILT, reason stated |
| ESP_015 | **The expensive tests are the ones about the record, not the vehicle.** T1, T2 and T3 need one operator and equipment they could carry. T4, T5 and T6 each need a party this folder does not have — a state records office, a vendor, a fleet — and each is `UNMEASURED`. That asymmetry is the case's own shape: what the truck does is measurable by the person driving it, and what the system records about them is not. | DERIVED |
| ESP_016 | **`driver_hours_evidence_register.py` is named and absent.** Cited in the order's cross-links as the register this case is a worked instance of. Not in this repository as of writing, and not reconstructed. | NAMED_AND_ABSENT |
| ESP_017 | **Nothing here is a measurement of any vehicle, road, operator or system.** No descent was recorded, no IMU was read, no log was pulled, no corridor was scored. Every number in the folder is either a placeholder threshold or a property of a generated fixture. | UNVERIFIED |

---

## What would refute these

- **ESP_001, ESP_004, ESP_005, ESP_007, ESP_008** are properties of the code
  and would have died on the first run if the code did not do what they say.
  That run is ESP_010; it happened on 2026-09-27 and they held. They die again
  on any later run that fails, which is what `test_envelope.py` is for.
- **ESP_002** dies if the verdict moves when only the carrier phase moves.
  The check passed once; it has not been run against a real trace.
- **ESP_003** dies if a cross-correlation is shown to distinguish a lead of
  one period from a lead of zero. It is a property of the operation and does
  not depend on any fixture.
- **ESP_011** stops being a limitation the moment a real paired-IMU log is
  classified and the verdict is checked against what the operator observed.
  That is T1 and it is the cheapest unrun thing here.
- **ESP_012** dies threshold by threshold as T1 and T2 produce measured
  values, each superseding its placeholder with a new append-only entry.
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
