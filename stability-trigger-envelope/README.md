# stability-trigger-envelope

A tractor stability system fires on serpentine downgrades while the trailer is
quiet. This folder holds the work order (`WORK_ORDER.md`, landed verbatim) and
one instrument, `descent_record.py`, that sorts a descent into what the two
IMU channels actually show. Everything runs on **CONSTRUCTED** data.
**The real run is NOT_RUN.**

stdlib only. CC0. Runs on a phone (Pydroid / a-Shell / Termux).

```
python3 descent_record.py          # render the fixtures
python3 test_descent_record.py     # 47 checks, REGRESSION on CONSTRUCTED data
```

---

## POSTURE — who this is for

This is written from the risk-mitigation side, for the people who drive the
grade. The question is not "was the driver right" or "is the vendor wrong".
The question is:

```
where does the risk go when the trigger fires on the wrong body,
and does any record catch it on the way?
```

When the instrument cannot tell, it says so and names why. It never turns a
missing channel into a clean reading. `OUT_OF_ENVELOPE` means **unassessed**,
not **clear**.

---

## 0. PROVENANCE (verbatim from the work order)

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

---

## THE SHAPE

```
            sensor here                       risk mass here
            (frame, back of cab)              (trailer, high CG)
                  |                                  |
   serpentine --> CAB oscillates -----lags-----> TRAILER quiet
   9-13% grade        |                              ^
                      v                              |
               trigger reads "rollover"              |
                      |                              |
                      v                              |
               system BRAKES  --- removes momentum --+   (FAULT B: sign inverted)
                      |           loads trailer into
                      |           the next reversal
                      v
               operator throttles against it, brakes in the
               window after the trailer settles
                      |
                      v
               logged as a DRIVER event  --> ORDER 1..4 relocation
```

Three faults, kept separate (all DERIVED):

```
FAULT A  measured body != at-risk body     cab frame sensor vs trailer mass
FAULT B  response sign inverted            brake removes the momentum holding
                                           the combination straight
FAULT C  baseline offset on a descent      pitch eats flat-calibrated headroom;
                                           bank adds a lateral gravity term that
                                           FLIPS SIGN each reversal
         whether the controller estimates grade/bank: UNREAD (proprietary)
```

Relocation chain -- the cost the safety score does not see:

```
ORDER 1  trigger docked as a driver event
ORDER 2  operator holds 25-35 mph to stay under the trigger --> queue
ORDER 3  passes around the truck, sightline occluded --> buggy near-misses
ORDER 4  incident ahead on the grade: no backing, no turnaround,
         closure holds everyone; drops with 1-2 access roads, ~3 h alternate
scoring  orders 2-4 never enter the score; crash forms carry no field
         for the trigger or the rule
```

Envelope variables (region-independent):

```
V1  grade x curve-reversal rate    trigger envelope
V2  access roads to the drop       closure trap
V3  alternate-route distance       reroute cost
V4  slow/vulnerable users present  passing hazard
V5  winter surface duration        sensor degradation + margin gone
```

---

## T1-T6 -- DESIGN TEXT (cheapest first)

None of these has been run. Each says what it needs, what it predicts, and
what would kill the fault it tests.

### T1 -- paired IMU, one descent (needs: 2 phones)  -- instrument BUILT, run NOT_RUN

```
rig      phone A rigid on the cab (not the dash pad -- a hard mount)
         phone B rigid on the trailer front wall or landing-gear crossmember
         both logging gyro roll rate (deg/s) at >= 20 Hz, plus GPS
sync     before rolling: both phones side by side, one sharp tap/drop on a
         hard surface; that spike is the sync mark (# sync_ts= in the CSV)
         repeat at the bottom of the grade -- two marks bound drift
event    note the ESP intervention time (dash light / audible / brake feel)
         as esp_event_ts on the cab clock
predict  cab RMS >> trailer RMS; cab envelope leads trailer by ~one
         reversal; trailer quiet at the trigger timestamp
read     descent_record.classify() -> GEOMETRIC_CAB_MODE if all three hold
FALSIFIER A  trailer roll high whenever the trigger fires
             -> TRAILER_ROLL_RISK on those runs -> Fault A void for this unit
```

The phone on the cab is **not** the OEM frame sensor. T1 compares cab against
trailer. It does not compare phone against OEM.

### T2 -- trigger-onset speed per named grade (needs: T1 rig, repeats)  -- primitive BUILT

```
method   same road, same load, repeated runs at stepped speeds; record
         fired / quiet per run
read     envelope_edge(records, road_id)
           < 3 runs                -> INSUFFICIENT_RUNS
           quiet runs only          -> NO_TRIGGER_OBSERVED (lower bound only)
           quiet top < fired bottom -> EDGE_BRACKETED (onset + bracket;
                                       bracket low end None if no quiet run)
           quiet above a fired run  -> ONSET_OVERLAP (not a clean edge)
           grade/surface differ     -> mixed_conditions reported, not pooled
output   onset speed per grade = the measured edge of the validation envelope
FALSIFIER C  onset speed independent of grade and bank -> Fault C void
```

Grade comes in as `grade_pct`, a declared input. Grade-from-GPS is NOT_BUILT.

### T3 -- event-log audit (needs: shop diagnostic tool)  -- NOT_BUILT

No instrument can be written until a real log is read. The report template:

```
field                                  present / absent / UNREAD
-------------------------------------  -------------------------
intervention type (RSC / YSC)
raw lateral accel at trigger
yaw rate at trigger
steer angle at trigger
wheel speeds / vehicle speed
grade estimate
bank / superelevation estimate
load / air-bag pressure (mass estimate)
trailer state (any channel)
driver override flag (throttle during intervention)
```

The two rows that decide Fault C and Fault A are `grade/bank estimate` and
`trailer state`.

### T4 -- relocation count (needs: T1 log + state crash data)  -- tally BUILT, join UNMEASURED

```
per descent  downstream_event = none | pass | near_miss | incident | closure
built        relocation_tally(records): counts by event, by V2 bin;
             never summed into one score
unbuilt      join slowdown segments against state crash records filtered
             to horse-drawn vehicles on the same segments -- no state data
             attached here
```

### T5 -- validation coverage (needs: vendor disclosure)  -- UNMEASURED

```
score corridors on V1-V5 (the record already carries the fields);
ask the vendor whether validation sets include high-V1-V5 corridors
answer   UNREAD until disclosed
```

### T6 -- scoring-rule displacement (needs: fleet telematics)  -- NOT_BUILT

```
speed on flagged grades before vs after the sensor-event docking policy;
queue length where measurable. Needs a fleet's speed history across the
policy date. No fleet data here.
```

---

## THE INSTRUMENT -- descent_record.py

```
DescentRecord  region road_id grade_pct curve_reversals        V1
               access_count_to_drop                            V2
               alternate_route_hours                           V3
               slow_users_present                              V4
               surface_state dry|wet|snow|ice                  V5
               speed_mph esp_event_ts
               cab_imu_file trailer_imu_file (None allowed)
               downstream_event none|pass|near_miss|incident|closure
```

`classify(record)` walks gates in order. The first gate that stops the read
names the reason.

```
1  surface or grade outside declared range  -> OUT_OF_ENVELOPE  (unassessed)
2  no esp_event_ts                          -> NOT_EVALUABLE
3  no cab trace                             -> NOT_EVALUABLE
4  no trailer trace                         -> TRAILER_CHANNEL_ABSENT (not inferred)
5  sync mark missing / clocks disagree      -> NOT_EVALUABLE
6  window not covered / gap in a trace      -> NOT_EVALUABLE
7  readings: RMS per channel, trailer RMS at trigger, amplitude ratio,
   lead from envelope cross-correlation
8  trailer high                             -> TRAILER_ROLL_RISK
   cab high + ratio ok + CAB_LEADS          -> GEOMETRIC_CAB_MODE
   anything else                            -> NEITHER_MODE (reason given)
```

**NEITHER_MODE is an addition to the work order's label set.** Three real
states fit none of the five: both channels quiet, the trailer leading the cab,
and a lead that cannot be resolved. Forcing any of them into
`GEOMETRIC_CAB_MODE` would manufacture support for Fault A. Forcing them into
`TRAILER_ROLL_RISK` would manufacture its falsifier. So they get their own
label, and the reason travels with it.

**Clock rule.** Misalignment is read from the sync marks. If it exceeds
tolerance, the run is NOT_EVALUABLE. The instrument never shifts one trace to
fit the other: phone clock drift is not measured, and a shifted trace can
fabricate the very lead T1 is looking for. The tolerance (0.5 s) is held below
the smallest lag counted as a lead (1.0 s). The loader refuses a threshold
file that breaks this.

**Lead from envelopes, not raw roll.** A quasi-periodic roll signal
cross-correlates at every whole period, so a raw-signal lag is ambiguous by a
reversal. The moving-RMS envelope carries the onset, and the onset is what
"cab leads" means.

**Thresholds** live in `thresholds.json` as an append-only log. Every value
is `PLACEHOLDER`: chosen so the constructed fixtures are readable, not
measured on any unit, road or trailer. To change a value, append an entry.
The test pins a digest of the shipped prefix, so an in-place edit fails and an
append passes. Every Reading prints the threshold status.

### Fixtures -- REGRESSION, not validation

The fixtures are implementation-authored. They show that the code does what it
was written to do. They say nothing about any road.

```
F1  serpentine, cab-only oscillation  GEOMETRIC_CAB_MODE      fires
    (ratio 11.9, trailer lags 3.95 s, r 0.985)
F2  real trailer roll                 TRAILER_ROLL_RISK       fires
F3  no trailer IMU                    TRAILER_CHANNEL_ABSENT  fires
F4  clocks misaligned 3.0 s           NOT_EVALUABLE           fires
F5  two runs on a road                INSUFFICIENT_RUNS       fires
X1  1.5 s gap in trailer trace        NOT_EVALUABLE
X2  snow surface                      OUT_OF_ENVELOPE
X3  both channels quiet               NEITHER_MODE
X4  cab high, trailer leads           NEITHER_MODE
X5  four runs, stepped speeds         EDGE_BRACKETED 27-30 mph
```

Trace CSV format (one file per phone):

```
# sync_ts=2.0
t_s,roll_dps
0.00,0.012
0.05,-0.034
...
```

---

## 7. SCOPE LIMITS

- One operator, one or few units. The stability system model is UNREAD.
- The Bendix sensor set and mount are a reference case, not this unit.
- A phone IMU on a cab mount is not the frame-mounted sensor. T1 compares cab
  against trailer, not phone against OEM sensor.
- Speed-differential crash risk (Solomon 1964 U-curve) is cited from memory,
  NOT searched, and its method is contested. Nothing here load-bears on it.
- The ESP intervention is not claimed to cause any specific crash. The claim
  is an unrecorded risk path.

## 8. SOURCES -- SECONDARY, not fetched here

```
Bendix SD-13-4986  ESP EC-80 service data -- sensor set; YAS sensor on a
                   cross-member near the back of the cab
Bendix SD-13-4869  EC-60 ABS/ATC/ESP (Advanced) -- sensor level, parallel
                   to road surface; load sensor in air bag
US 7,085,639 et al. road-bank gravity contamination -> false YSC/RSC activation
WO 2002/020318     lateral accel compensation for inclined plane
```

Carried as the work order stated them. None was re-read in this build.

## 9. CROSS-LINKS

```
TAF labor_thermodynamics/driver_hours_evidence_register.py
    TRUST_PROTOCOL.machine_side_rule -- this case is its worked instance:
    the throttle-then-brake correction logs as driver-fighting-system
TAF in_progress/serpentine_grade_esp_notes.md
    the operator notes this work order was cut from
aeb-false-positive-measurand -- NAMED, NOT FOUND in any attached repo.
    Nearest in-tree match: TAF docs/case-studies/class8_aeb_field_advisory.md.
    Not substituted; pointer left open.
```

---

## TYPED ABSENCES -- what is not here, and why

```
item                              status        why
--------------------------------  ------------  ----------------------------------
real paired-IMU run               NOT_RUN       no field traces supplied
stability system on the unit      UNREAD        not disclosed; Bendix is a reference case
controller grade/bank estimation  UNREAD        proprietary
T3 event-log audit                NOT_BUILT     needs a real log from a shop tool; template above
T4 crash-record join              UNMEASURED    no state crash data attached
T5 validation coverage            UNMEASURED    needs vendor disclosure
T6 scoring-rule displacement      NOT_BUILT     needs fleet telematics across the policy date
grade from GPS                    NOT_BUILT     grade_pct is a declared input
bank / superelevation             UNMEASURED    no channel; Fault C's bank term is untested
thresholds                        PLACEHOLDER   none measured
sources (sec. 8)                  NOT_FETCHED   carried from the work order, not re-read
Solomon 1964                      NOT_SEARCHED  not load-bearing
aeb-false-positive-measurand      NOT_FOUND     named in the work order, absent from attached repos
```

Files: `WORK_ORDER.md` (verbatim), `README.md`, `CLAIM_TABLE.md`,
`descent_record.py`, `thresholds.json`, `test_descent_record.py`,
`samples/descent_record.sample.txt`.
