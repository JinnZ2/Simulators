<!-- landed verbatim 2026-09-24 from the DISPATCH ESP-1 message; nothing below this line is edited here -->
<!-- amended 2026-09-24 by the dispatch author: sec. 9 line 'aeb-false-positive-measurand  override scored as error' replaced (the name was from working notes, not a repo artifact) -->

# DISPATCH ESP-1 — stability trigger outside its validation envelope

```
═══════════════════════════════════════════════════════════════
TARGET: Claude Code
REPO:   JinnZ2/Simulators, folder stability-trigger-envelope/
CLASS:  research work order (document) + ONE instrument built on
        CONSTRUCTED data. Real run NOT_RUN.
stdlib only, CC0, phone-buildable
POSTURE: risk-mitigation side, stated in README (worker audience)
═══════════════════════════════════════════════════════════════
```

## 0. PROVENANCE — carry into README verbatim

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

## 1. THE CASE

```
road     two-lane descents 9–13%, continuous reversing curves
         (serpentine) for the length of the grade               OBSERVED
event    stability system reads rollover risk and BRAKES         OBSERVED
         oscillation is in the CAB, not the trailer              OBSERVED
         operator's phone gyro (cab) read the descent as
         ordinary, same as prior runs, while the system fired    OBSERVED
recovery operator throttles AGAINST the intervention to hold
         momentum and straighten the trailer, then brakes
         manually in the window after the trailer settles and
         before the next reversal                                OBSERVED
envelope works on flat roads and single 90° turns on flat;
         fails on downgrade × curves                             OBSERVED
```

## 2. THREE FAULTS — keep separate

```
FAULT A  measured body ≠ at-risk body                        DERIVED
         yaw/lateral-accel sensor on a frame cross-member
         near the back of the cab (tractor)                  SECONDARY
         at-risk mass = trailer (high CG), which lags the
         tractor and was not oscillating                     OBSERVED
         same class as a fifth-wheel "attached" proxy: the
         observable comes apart from the state that matters

FAULT B  response sign inverted                              DERIVED
         braking removes momentum holding the combination
         and loads the trailer into the next reversal

FAULT C  baseline offset on a descent                        DERIVED
         frame pitched forward/down before any curve; flat-
         calibrated threshold has less headroom
         lateral channel additionally carries a gravity term
         from superelevation (bank), which FLIPS SIGN at each
         reversal
         listed reference sensor set has no pitch/grade
         sensor; sensor installed level, parallel to road    SECONDARY
         bank contamination of lateral accel is a known
         false-activation source; compensation methods exist
         in patents                                          SECONDARY
         whether the controller ESTIMATES grade/bank        UNREAD
                                            (proprietary)
```

## 3. RELOCATION CHAIN — the cost the safety score does not see

```
ORDER 1  sensor-triggered event docked as a driver event     OBSERVED
ORDER 2  operator avoids trigger range: 25–35 mph on grade
         → queue of following traffic                        OBSERVED
ORDER 3  impatient passes around the truck; truck occludes
         the passer's view; near-misses with horse-drawn
         buggies                                             OBSERVED
ORDER 4  incident ahead, truck approaching it on the grade:
         no backing, no turnaround; closure holds every
         vehicle; idle fuel (APU on or not), wear with zero
         output; other same-carrier trucks trapped; drops
         with 1–2 access roads, ~3 h alternate                OBSERVED
scoring  none of orders 2–4 enter the safety score; crash
         forms have no field for the trigger or the rule     DERIVED
```

## 4. ENVELOPE VARIABLES — region-independent

```
V1  grade × curve-reversal rate         trigger envelope
V2  access-road count to the drop       closure trap
V3  alternate-route distance            reroute cost
V4  slow/vulnerable users present       passing hazard
V5  winter surface duration             sensor degradation + margin gone
same dynamics reported across the UP, the Driftless, St. Croix
riverway, upper MN/WI and other high-V corridors      OBSERVED, N_op=1
```

## 5. TESTS — cheapest first

```
T1  PAIRED IMU, one descent                        needs: 2 phones
    cab + trailer IMUs, phone GPS for grade
    predict: cab amplitude >> trailer; cab leads trailer by
    ~one reversal; trailer quiet at trigger timestamp
    FALSIFIER A: trailer roll high whenever trigger fires
                 → Fault A void for this unit

T2  TRIGGER-ONSET SPEED per named grade            needs: T1 rig, repeats
    speed at which a correctly driven rig trips the trigger,
    per grade, repeated across runs
    = the measured edge of the validation envelope
    FALSIFIER C: onset speed independent of grade and bank
                 → Fault C void

T3  EVENT-LOG AUDIT                                needs: shop diagnostic tool
    does a logged roll intervention carry a bank/grade
    estimate or only raw lateral accel? does it log trailer
    state at all?
    report: fields present / absent

T4  RELOCATION COUNT                               needs: T1 log + state data
    field downstream_event per descent
    join slowdown segments against state crash records
    filtered to horse-drawn vehicles on the same segments
    join status: UNMEASURED

T5  VALIDATION COVERAGE                            needs: vendor disclosure
    score corridors on V1–V5; request whether validation
    sets include high-V1–V5 corridors
    status: UNMEASURED

T6  SCORING-RULE DISPLACEMENT                      needs: fleet telematics
    speed on flagged grades before vs after sensor-event
    docking policy; queue length where measurable
```

## 6. INSTRUMENT — build on constructed data

```
descent_record.py

DESCENT_RECORD fields
  region, road_id, grade_pct, curve_reversals          # V1
  access_count_to_drop                                 # V2
  alternate_route_hours                                # V3
  slow_users_present                                   # V4
  surface_state  dry|wet|snow|ice                      # V5
  speed_mph, esp_event_ts
  cab_imu_file, trailer_imu_file (may be None)
  downstream_event  none|pass|near_miss|incident|closure

classify(record) → one of
  GEOMETRIC_CAB_MODE        cab high, trailer low, cab leads
  TRAILER_ROLL_RISK         trailer high
  TRAILER_CHANNEL_ABSENT    no trailer trace — do not infer
  NOT_EVALUABLE(reason)     timestamps unaligned, gap in trace
  OUT_OF_ENVELOPE           surface or grade outside declared range

envelope_edge(records, road_id) → onset speed with spread,
  or INSUFFICIENT_RUNS (< 3 runs on that road)

relocation_tally(records) → counts by downstream_event,
  by V2 bin; never summed into a single score

thresholds (amplitude ratio, phase window) in a data file with
append-only provenance; every value declared PLACEHOLDER

CONSTRUCTED FIXTURES — planted faults must fire
  F1 serpentine, cab-only oscillation      → GEOMETRIC_CAB_MODE
  F2 real trailer roll                     → TRAILER_ROLL_RISK
  F3 no trailer IMU                        → TRAILER_CHANNEL_ABSENT
  F4 clocks misaligned > window            → NOT_EVALUABLE
  F5 two runs on a road                    → INSUFFICIENT_RUNS
fixtures are implementation-authored → REGRESSION, not validation
```

## 7. SCOPE LIMITS — state in README

```
- one operator, one or few units; stability system model UNREAD
- the Bendix sensor set and mount are a reference case, not this unit
- phone IMU on a cab mount ≠ frame-mounted sensor; T1 compares
  cab vs trailer, not phone vs OEM sensor
- speed-differential crash risk (Solomon 1964 U-curve) cited from
  memory, NOT searched; method contested — do not load-bear on it
- ESP intervention is not claimed to cause any specific crash; the
  claim is an unrecorded risk path
```

## 8. SOURCES (SECONDARY)

```
Bendix SD-13-4986  ESP EC-80 Controller service data — sensor set;
                   YAS sensor mounted on cross-member near back of cab
Bendix SD-13-4869  EC-60 ABS/ATC/ESP (Advanced) — sensor to be level,
                   parallel to road surface; load sensor in air bag
US 7,085,639 et al. road-bank gravity contamination → false YSC/RSC
                   activation
WO 2002/020318     lateral accel compensation for inclined plane
```

## 9. CROSS-LINKS

```
driver_hours_evidence_register.py  TRUST_PROTOCOL.machine_side_rule
  (this case is its worked instance: the operator's throttle-then-brake
   correction logs as driver-fighting-system)
AEB takeover studies   a correct driver override of a false
                       machine intervention is logged as
                       driver error (same defect class)
```

```
RETURN: file list; T1–T6 written as design text; descent_record.py
with F1–F5 firing; anything NOT built and why, as typed absence.
═══════════════════════════════════════════════════════════════
```
