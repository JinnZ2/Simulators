# stability-trigger-envelope

A stability system firing outside the envelope it was validated in, and the
costs that firing relocates into places no safety score reads.

**Posture: risk mitigation. Audience: the people driving.** Nothing here is an
argument against stability control. The claim is narrower and is about
coverage: a system that works on flat roads and single turns can read a
serpentine descent wrong, and when it does, the correction the operator makes
is recorded as the operator's fault.

CC0. Standard library only. Parses under Python 3.9. Phone-buildable.

---

## STATE — read before quoting anything

```
CHECKS RUN         python3 test_envelope.py -> 217 checks, 0 failed
                   (2026-09-27, first execution). The code was written in a
                   session whose command execution was unavailable and was
                   run once when it returned. F1-F5 fire. ESP_010 records
                   the sequence rather than replacing it.
RENDER NOT SEEN    python3 descent_record.py has not been executed. The
                   render path shares every function with the checks except
                   the three render_* formatters and main(); those four are
                   unobserved.
REAL RUN           NOT_RUN. No descent, no IMU, no vehicle. T1-T6 are designs.
```

The first filing of this block said WRITTEN, NOT RUN. It is kept in ESP_010
rather than deleted, because a module written blind and then found to pass is
a different record from one written and checked as it went, and the
difference is worth having.

---

## 0. PROVENANCE — carried verbatim from the work order

```
field source   single operator, loaded Class 8 tractor-trailer,
               repeated descents; multiple regions        N_operators = 1
status scale   OBSERVED / SECONDARY / DERIVED / PROPOSED / UNREAD
do not         name the operator, the carrier, or the unit;
               no characterization of the operator anywhere
UNREAD         which stability system the operator's tractor runs.
               Bendix ESP documents below are the REFERENCE CASE for
               sensor set and mounting, not a claim about this unit.
```

The "do not" line is structural rather than editorial: `descent_record.py` has
no field for an operator, a carrier or a unit, and `test_envelope.py` reads
the schema's own field names against a token list rather than trusting a
sentence. There is also no field anywhere for how anyone drove.

---

## The case

```
road     two-lane descents 9-13%, continuous reversing curves
         (serpentine) for the length of the grade               OBSERVED
event    stability system reads rollover risk and BRAKES        OBSERVED
         oscillation is in the CAB, not the trailer             OBSERVED
         phone gyro (cab) read the descent as ordinary, same as
         prior runs, while the system fired                     OBSERVED
recovery throttle AGAINST the intervention to hold momentum and
         straighten the trailer, then brake manually in the
         window after the trailer settles and before the next
         reversal                                               OBSERVED
envelope works on flat roads and single 90-degree turns on
         flat; fails on downgrade x curves                      OBSERVED
```

## Three faults, kept apart

```
FAULT A   measured body != at-risk body                        DERIVED
          sensor on a frame cross-member near the back of the
          cab; at-risk mass is the trailer, which lags and was
          not oscillating. The observable comes apart from the
          state that matters.

FAULT B   response sign inverted                                DERIVED
          braking removes the momentum holding the combination
          and loads the trailer into the next reversal

FAULT C   baseline offset on a descent                          DERIVED
          frame pitched down before any curve; the lateral
          channel additionally carries a gravity term from bank
          that FLIPS SIGN at each reversal
          whether the controller estimates grade or bank        UNREAD
```

They are kept apart because they call for different tests and different
repairs. A is a mounting and sensing question, B is a control question, C is a
calibration question, and a single verdict over all three would need none of
them measured.

## What the instrument does

`descent_record.py` addresses **FAULT A only**. Given a descent record with a
cab trace and a trailer trace it says which body was carrying the motion:

```
GEOMETRIC_CAB_MODE       cab high, trailer low, cab first
TRAILER_ROLL_RISK        the trailer is the body moving
TRAILER_CHANNEL_ABSENT   no trailer trace -- NOT a quiet trailer
NOT_EVALUABLE(reason)    clocks unaligned, gap in trace, axes disagree,
                         or the two bodies move comparably
OUT_OF_ENVELOPE          outside what this READER declares it can read
```

`OUT_OF_ENVELOPE` is about the reader, not the vehicle. Measuring the
vehicle's validation envelope is T2 and T5, and neither has been run.

Two refusals are built in rather than described. `TRAILER_CHANNEL_ABSENT` is
an absence and is never inferred, because the whole of Fault A turns on the
difference between a quiet trailer and an unmeasured one. And where amplitude
and onset point opposite ways the verdict is `NOT_EVALUABLE`: two readings
disagreeing is not a verdict with a caveat.

**Onset, not phase.** The second axis is onset timing -- first exceedance of
the amplitude envelope, and the envelope lag within one period of the event --
and not a phase lead. On a serpentine the forcing is periodic, so a phase lead
is fixed only modulo one curve reversal, and the case's own prediction is a
lead of about one reversal. That is exactly the value a phase reading cannot
resolve. See `RUN_NOTE.md` CHOICE 1.

## 7. SCOPE LIMITS — carried from the work order

```
- one operator, one or few units; stability system model UNREAD
- the Bendix sensor set and mount are a reference case, not this unit
- phone IMU on a cab mount != frame-mounted sensor; T1 compares
  cab vs trailer, not phone vs OEM sensor
- speed-differential crash risk (Solomon 1964 U-curve) cited from
  memory, NOT searched; method contested -- do not load-bear on it
- ESP intervention is not claimed to cause any specific crash; the
  claim is an unrecorded risk path
```

Added by the build, in the same spirit:

```
- every fixture is CONSTRUCTED and authored by the same hand that wrote the
  classifier, so they are REGRESSION and not validation
- every threshold is PLACEHOLDER with no measurement behind it; the amplitude
  ratio that separates the two bodies is a round number, not a finding
- the checks have run once and the render has not (see STATE, above)
```

## Files

```
WORK_ORDER.md         the dispatch, verbatim
README.md             this file
TESTS.md              T1-T6 as design text
descent_record.py     the instrument
cases.py              F1-F8 constructed fixtures
test_envelope.py      checks; expected verdicts live here, not in cases.py
thresholds.txt        data only, every value PLACEHOLDER
threshold_chain.txt   append-only provenance, one entry per value
CLAIM_TABLE.md        ESP_* claims
RUN_NOTE.md           every choice the order left open
```

```
python3 test_envelope.py    # checks; prints the total, never stores it
python3 descent_record.py   # the fixtures rendered
```

## 8. Sources (SECONDARY, none read in this session)

```
Bendix SD-13-4986   ESP EC-80 Controller service data -- sensor set; YAS
                    sensor on a cross-member near the back of the cab
Bendix SD-13-4869   EC-60 ABS/ATC/ESP (Advanced) -- sensor level, parallel to
                    the road surface; load sensor in the air bag
US 7,085,639 et al. road-bank gravity contamination -> false YSC/RSC
                    activation
WO 2002/020318      lateral accel compensation for an inclined plane
```

Every one is carried from the work order at SECONDARY and was not retrieved,
read or checked here. No claim in this folder rests on the content of any of
them.

## 9. Cross-links

```
driver_hours_evidence_register.py   TRUST_PROTOCOL.machine_side_rule
   this case is its worked instance: a correction made against a false
   machine intervention logs as the driver fighting the system
AEB takeover studies                same defect class, other direction
Noise-as-Information-Sensor         tools/two_body_source.py is the same
   tools/                           measurand -- which of two coupled bodies
                                    a signal sits on -- reached from the
                                    other side. Its NC_013 is why this
                                    folder reads onset instead of phase.
```

`driver_hours_evidence_register.py` is NOT in this repository as of writing
and is carried as named-and-absent rather than reconstructed.
