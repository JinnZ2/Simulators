# MARKER — ROUTING DATA LAYER: REQUIRED ENVELOPE, MEASURED STATE, STANDING COST

CC0. Marker format. Claim table with refutation conditions.
Not a position under defense. Not a critique of any routing system,
vendor, or reasoning architecture.

## WHAT THIS DOCUMENT IS

An envelope specification for the DATA LAYER that heavy-vehicle
automated routing requires. It states what the layer must contain,
what is measurably in it now, the error classes observed in service,
and the standing cost to close the gap.

The null falls out of the envelope. It is not asserted up front.

SCOPE: the data layer only. Sensing, control, and reasoning
architecture are out of scope. No claim here is about whether a
system can reason. Every claim here is about what the reasoning
would be reasoning OVER.

## WHY THE ENVELOPE IS THE RIGHT FRAME

Capability claims in this domain ship without scope conditions:
"routes commercial vehicles," "sees through canopy," "current to
state DOT feeds." No error rate, no revisit interval, no minimum
feature size, no leaf-on/leaf-off condition, no per-jurisdiction
coverage statement.

An unscoped claim substitutes for a solution. Requiring the envelope
converts the disagreement into a measurement.

## SECTION 1 — REQUIRED CONTENTS OF THE LAYER

    R1  Road existence and current geometry
    R2  Structure existence and status (bridges, overpasses)
    R3  Vertical clearance, per structure, current
    R4  Weight limits, per segment, INCLUDING seasonal variation
    R5  Truck-route designation, per segment
    R6  Exit / ramp existence and current closure state
    R7  Active construction: closures, lane shifts, detours
    R8  Dock geometry, per door: painted line offset, approach
        clearance, surface state
    R9  Update latency per field, per jurisdiction
    R10 Provenance and confidence per record

R8 and R9 are the two that are absent by construction rather than
merely incomplete. See Section 4.

## SECTION 2 — OBSERVED FAILURE CLASSES

Field observations, Upper Midwest corridors, commercial operation.
Instances below are named cases. A larger population is held in a
separate operator repo; these are additional to it.

    F1  NONEXISTENT INFRASTRUCTURE STILL ROUTED OVER
        System routes across a structure that no longer stands.
        Instances: bridge cases in both the Minneapolis and
        Milwaukee metros.

    F2  CLOSED SEGMENT SHOWN OPEN
        Instance: Black Dog Road and Cliff Road shown open,
        not open.

    F3  NONEXISTENT EXIT / RAMP ASSIGNED
        Instance: I-794, Milwaukee — routed to an exit that does
        not currently exist.

    F4  NON-TRUCK-ROUTE ASSIGNMENT
        System assigns segments not designated for commercial
        vehicles.

    F5  RESTRICTION NOT HELD
        Structures and weigh points treated as passable that are
        not; vertical and weight restrictions absent or stale.

    F6  INDEPENDENT SYSTEMS DISAGREE, BOTH WRONG
        Instance: commercial trucking navigation and a shipper's
        mandated store app returned different routings for the
        same movement. Neither was correct. Errors were in
        different directions.
        This is the load-bearing class. Two independently
        maintained systems, both marketed as current, both
        wrong — indicates the fault is upstream of either
        vendor's maintenance.

    F7  PER-DOCK GEOMETRY UNAVAILABLE
        Painted dock lines vary door to door: offsets observed
        at roughly two to three inches, asymmetric left versus
        right. Correct approach requires tires placed on the
        actual lines present. Offsets originate at build, shift
        with repaint, frost heave, and patching.
        No central record of per-door geometry exists.

## SECTION 3 — CLAIM TABLE

    ID    CLAIM                                REFUTED IF
    ----  -----------------------------------  --------------------
    RDL-1 Required layer (R1-R10) is not       A complete record is
          held complete by any party for       produced for any
          the operating region                 state in region

    RDL-2 F1-F6 are not vendor maintenance     Single-vendor fix
          defects; the source record is        closes F6 without
          incomplete upstream of vendors       new field survey

    RDL-3 R8 has no record anywhere; it        A per-door geometry
          exists only as operator reading      dataset is located

    RDL-4 Update origination requires county   A funded, staffed
          and municipal reporting that is      per-jurisdiction
          not funded or staffed at the rate    reporting function
          road state changes                   is demonstrated

    RDL-5 The cost to close is STANDING, not   A one-time survey
          capital: it recurs with each         holds accuracy across
          construction season and grows with   a full freeze-thaw
          network size                         and construction cycle

    RDL-6 Overhead sensing does not close      Canopy-penetrating
          the gap: it returns ground surface,  sensing demonstrated
          not road STATE (closure, removal,    to detect a removed
          coning, designation)                 structure at stated
                                               error rate

    RDL-7 The binding failure mode is NO       System demonstrated
          LEGAL ACTION AVAILABLE, not wrong    to have a safe action
          selection: committed lane, no        set at F1-F3 discovery
          shoulder, parked cars, traffic       in dense urban
          behind at a light                    committed-lane case

## SECTION 4 — THE TWO STRUCTURAL ABSENCES

Distinguish incomplete records from records that were never created.

    INCOMPLETE (R1-R7): a reporting chain exists across the region's
    state DOTs. It does not capture everything. Improvable in
    principle by funding the existing chain.

    NEVER CREATED (R8, R9): per-door dock geometry, and per-field
    update latency, have no originating record anywhere. They were
    never written down because operators absorb the variance at
    zero recorded cost. Closing them means paying to CREATE a
    record that has never existed, then maintaining it against
    frost heave, repaint, and resurfacing.

This is the same structure as sampling absence elsewhere: the
question was not asked and answered unremarkably. It was not
answerable at that instrument.

## SECTION 5 — THE ENTROPY / UPDATE-RATE FORM

State the constraint as a rate comparison, not as a maturity claim.

    dE/dt   environment state-change rate
            (construction season, seasonal weight restriction,
             frost heave, repaint, structure removal, signal
             coverage change)

    dM/dt   sustainable model refresh rate
            (bounded by jurisdiction reporting capacity, survey
             cost, and funding, NOT by compute or reasoning)

    Where dE/dt > dM/dt sustained, the null is STRUCTURAL, not
    a maturity gap. "Not yet" and "different answer" are
    distinguishable claims, and this form distinguishes them.

    TEST: measure both rates for one county over one full
    construction season. Cheapest available test. No field
    automation required.

## SECTION 5B - NOMINAL-CASE CYCLE ACCOUNTING

Every element below is stated for the NOMINAL case: no rain, good
surface, favorable traffic, no wildlife in the roadway, no
mechanical fault. This is the best available reading. Any claim of
time or labor saving must survive here before adverse conditions
are considered.

Each element is classified by what sets its rate.

    ELEMENT                     RATE SET BY           FASTER
                                                      DECISION
                                                      LAYER MOVES
                                                      IT?
    --------------------------  --------------------  ------------
    Fuel terminal data entry    Terminal software.    NO
                                Fields (trip, truck,
                                trailer, driver ID,
                                mileage) accepted
                                ONE AT A TIME, with
                                keypad debounce,
                                screen redraw, and
                                network round trip
                                for authorization
    Nozzle handling, cap,       Mechanical fixture    NO
    latch, dual tanks
    Fuel flow                   Pump plumbing         NO
    Thermal / charge readiness  Pack physics in       NO
    (see Section 5C)            cold
    Gate check-in               Gate guard            NO
                                throughput; serial
                                human checkpoint
    Lock removal, seal check    Custody procedure;    NO - and
                                keys must be held     ADDS STAFFED
                                by someone            LABOR
    Yard transit                Administrative        NO
                                speed limit
                                (10-15 mph)
    Backing into a single       Clearance, not        NO - higher
    slot between trailers       decision time;        speed raises
                                shared yard with      contact risk
                                yard dogs in motion
    Landing gear / dollies      Gearbox ratio         NO
    Airline disconnect          Air dump rate         NO
    Fifth wheel pin pull        Load transfer         NO
    Sensor cleaning             New standing task     N/A - ADDS
                                                      LABOR

    RESULT: on the nominal cycle, every element is gated by
    another party, rate-limited by hardware, or a single-attempt
    spatial task. No element is gated by decision latency.

### The serial-interface condition

    The time-saving claim is CONDITIONAL, and the condition is
    never stated with it:

      For a faster decision layer to save time on this cycle, the
      interfaces it meets must be PARALLEL. Under current
      architecture they are all SERIAL:
        - fuel terminal accepts one field at a time
        - gate is one checkpoint, one unit at a time
        - fueling or charging requires a mechanic or attendant to
          confirm the unit is present and in order before the
          transfer is authorized
        - software must be within spec for that transfer to be
          allocated at all

      So the saving requires the terminals, the gate process, the
      authorization chain, and the transfer interfaces to be
      rebuilt as parallel systems. That rebuild is the cost, and
      it is not on the comparison sheet.

    CLAIM RDL-8: no time or labor saving is available on the
    nominal cycle under current serial interface architecture.
    REFUTED IF: a cycle-time breakdown identifies any element on
    the nominal cycle whose rate is set by decision latency.

### Where the cost relocates

    Removed from the sheet:  one wage line.
    Added to the sheet, all STANDING costs:
        gate staffing at higher load
        key custody across carriers' locks
        seal verification as a staffed function
        sensor cleaning and calibration
        thermal fuel and heater maintenance (Section 5C)
        mapping and dock-geometry updates (Sections 1, 4)
        recovery function for RDL-7 no-legal-action events

    CLAIM RDL-9: the labor cost does not leave the system; it
    relocates into standing functions absent from the comparison.
    REFUTED IF: a full-ledger comparison carries the relocated
    functions and still shows a net saving.

## SECTION 5C - COLD-CLIMATE ENERGY ENVELOPE

Northern operating envelope reaches approximately negative fifty.
Two loads, failing differently:

    TRACTION ENERGY  - moving the unit.
    THERMAL / HOTEL  - keeping the storage medium inside its own
                       operating window. Runs while parked. A pack
                       below window loses usable capacity and will
                       not accept charge, so energy is spent
                       keeping storage warm enough to deliver
                       energy.

    Consequence on current architecture: liquid fuel present in
    the northern envelope for THERMAL reasons before traction
    reasons - diesel-fired coolant heater or the engine itself.

    Absent functions in a driverless unit: nobody plugs it in,
    nobody notices a heater fault, nobody addresses gelled fuel
    or a plugged filter.

    CLAIM RDL-10: in this envelope the energy question is a
    thermal-maintenance question, not a traction question, and it
    requires an attending human or a new standing service
    function.
    REFUTED IF: unattended thermal hold demonstrated across a
    full northern winter at stated fault rate.

## SECTION 5D - PARALLEL-EXECUTED FUNCTIONS, UNNOTATED

The elements in 5B are the ones with names. This section is the
work that has no line anywhere: functions executed INSIDE the time
of a movement that is required regardless, at zero added cycle
time.

Origin of the parallelism: the operator has a body that is going
to the back of the trailer anyway - for the lock, the doors, the
landing gear. Everything below rides along with that movement.

    FUNCTION                          EXECUTED DURING
    --------------------------------  ------------------------
    Dock approach assessment:         walk back to remove the
    grade, surface state, approach    lock, before backing
    angle, what occupies either side
    Tire inspection, repeated pass    rolling up doors /
                                      landing gear
    Post-trip inspection              same window
    SENSOR CROSS-VALIDATION:          same window
    onboard lamp status checked
    against externally observed
    lamps. Onboard reports OK on a
    lamp that is visibly burnt out.
    Operator is the validator for
    the automated layer.
    Landing gear condition:           while cranking it
    corrosion, wear, service need
    Running repair: small fixes       while cranking it
    performed on the spot

    CONSEQUENCE FOR THE CYCLE: perception and assessment cost
    ZERO added time, because they overlap a required physical
    movement. By the time the operator is seated, the maneuver is
    already planned.

    An automated unit cannot overlap these. It has no reason to be
    at the rear of the trailer, so lock handling requires separate
    actuation and site assessment is a discrete sensing pass - two
    serial steps where the operator had one.

    This is the first element in the cycle where the operator is
    measurably AHEAD rather than tied. It is a coupling property,
    not a decision-speed property.

    CLAIM RDL-11: the cycle contains inspection, sensor
    cross-validation, condition assessment, and running repair
    executed in parallel with required movement, at zero added
    cycle time, and none of it is notated in any job
    specification, cost model, or automation comparison.
    REFUTED IF: a cost model is produced that carries these
    functions as line items.

    CLAIM RDL-12: the operator currently serves as the validation
    layer for onboard sensing (lamp status instance), so removing
    the operator removes the only cross-check on that sensor
    class.
    REFUTED IF: an independent onboard cross-validation path for
    external lamp status is demonstrated.

    WHY IT IS UNNOTATED: it never generated a record. The work was
    absorbed at zero recorded cost, so pricing the job prices only
    driving - the written-down part. Same structure as R8 dock
    geometry (Section 4) and the same zeroing operation as
    uncounted non-transacting capacity.

    The comparison sheet is therefore not merely missing costs. It
    is missing the WORK.

## SECTION 5E - RECEIVING INTERFACE AND DEAD-WAIT RECOVERY

The delivery end is a second interface layer, human-gated at every
step, on the COUNTERPARTY's process. Nothing here is under the
carrier's control.

    ELEMENT                           RATE SET BY
    --------------------------------  --------------------------
    Park, secure truck, collect       operator
    paperwork
    Buzzer at the side door           receiver responds when
                                      they respond
    Paperwork handover, signature     physical document; bill of
    or stamp                          lading signature is the
                                      legal record of handoff
    Door assignment / instruction     receiver
    to wait

    CLAIM RDL-13: the delivery handoff requires the counterparty's
    process to change - electronic proof of delivery accepted at
    EVERY receiving facility, including small ones - or a person
    to carry the paper. There are thousands of counterparties.
    REFUTED IF: universal electronic handoff acceptance is
    demonstrated across a full store network including
    non-chain receivers.

### Operator-supplied work on the RECEIVER's side of the line

    Opening the receiver's door
    Opening the trailer
    Deploying the receiver's dock plate
    Turning on trailer lights so the interior is visible
    Checking every pallet out against the paperwork
    Moving obstructions clear so the unload runs faster
    Cleaning the receiver's dock

    This is throughput supplied to a facility that is not paying
    for it and not recording it. Not in the job description.

### DEAD-WAIT RECOVERY - the largest single time element

    OBSERVED CASE: app marks arrival at the delivery. No one is at
    the dock to receive. Operator walks around to the front of the
    store, locates a person, brings them back to the dock.

      Operator path:   minutes.
      Automated path:  the unit sits at the dock until someone
                       arrives on their own - observed at
                       forty-five minutes to an hour.

    On this element the automated case is not marginally slower.
    It is worse by the FULL DURATION OF THE WAIT, per stop,
    across thousands of stops. The recovery requires leaving the
    vehicle, entering a building, and locating an unspecified
    person - not available to the unit under any current
    architecture.

    CLAIM RDL-14: dead-wait recovery is the largest recoverable
    time element in the delivery cycle, is performed entirely by
    the operator leaving the vehicle, and appears in no cycle-time
    model or automation comparison.
    REFUTED IF: an automated dead-wait recovery path is
    demonstrated, or detention data is produced showing the
    recovery has no material effect on cycle time.

    NOTE ON DIRECTION: Sections 5B-5D establish elements where the
    automated case is TIED (hardware- or party-gated). 5D and 5E
    establish elements where it is BEHIND. No element has been
    identified where it is ahead.

## SECTION 5F - CROSS-PARTY OVERLAP AND FAULT WORKAROUNDS

### Cross-party task overlap

    OBSERVED SEQUENCE: while the receiver moves the last pallets
    and puts the electric pallet jack away, the operator pulls the
    dock plate, closes and SEALS the trailer, closes and locks the
    receiver's door, and has the paperwork in hand. The receiver
    turns from plugging in the jack; signatures are taken; the
    operator leaves.

    Two parties' tasks run in the SAME window and finish together.
    Nothing scheduled this. It comes from reading where the other
    party is in their task and timing against it.

    CLAIM RDL-15: the delivery close-out is executed as an
    overlapped two-party sequence, not as serial handoff, and the
    overlap is produced by the operator tracking the receiver's
    task state.
    REFUTED IF: comparable overlap is demonstrated between an
    automated unit and receiving staff without added coordination
    staffing.

### Fault workarounds - no automated analogue

    OBSERVED FAULT CASES and the operator's held alternates:
        electric pallet jack down  -> transition to a different
                                      door / alternate approach
        dock plate down            -> pull out a manual plate
        no staff present at dock   -> locate a person in the store
                                      (Section 5E)
        staffing shortage / lunch  -> same

    These are alternate procedures held because the failure has
    been encountered before. A unit executing a fixed procedure
    has ONE path, so a downed dock plate is a FAILED delivery
    rather than a slower one.

    CLAIM RDL-16: the operator holds a set of fault workarounds
    that convert facility equipment failures from failed
    deliveries into slower deliveries, and this set is not
    specified, documented, or transferable to a fixed-procedure
    system.
    REFUTED IF: a facility-fault fallback set is specified and
    demonstrated across the observed fault classes.

### The notification layer is known not to work

    Both the shipper's store application and the carrier's app
    register arrival. Theory: managers are alerted and know a
    truck is parked at the dock.

    OBSERVED: during a lunch period the alert lands on nobody. The
    operator recovers it by walking the store (Section 5E).

    CLAIM RDL-17: the arrival-notification layer an automated unit
    would depend on is already known to fail under ordinary
    conditions (breaks, shortage, absence), and the current
    fallback is the operator. Removing the operator removes the
    fallback for a layer with a measured failure mode.
    REFUTED IF: arrival-notification reliability data is produced
    showing the failure rate is immaterial, or an automated
    fallback is demonstrated.

## SECTION 6 - WHAT WOULD CHANGE THE READING

Stated so the marker is falsifiable rather than a position.

    - A funded per-jurisdiction reporting function demonstrated at
      the rate road state changes (refutes RDL-4, RDL-5)
    - Per-door dock geometry dataset located or produced and
      maintained across one freeze-thaw cycle (refutes RDL-3)
    - Canopy-penetrating sensing with published error rate on road
      STATE detection, not ground surface (refutes RDL-6)
    - Demonstrated safe action set at F1-F3 discovery in a
      committed-lane urban case (refutes RDL-7)

## SECTION 7 — PROVENANCE

The failure classes are in-service observations from commercial
operation, accumulated over roughly two and a half years, in a
region spanning Wisconsin, Minnesota, Michigan, North Dakota,
South Dakota, and Iowa. A larger instance population is held in a
separate repo.

The observations exist only in operators. No channel currently
carries them into the record the routing layer is built from.
That absence is itself an instance of the pattern this document
describes.

## OUT OF SCOPE

No section characterizing the author or any operator. No
working-style or author-profile content. Instances are
observations, not biography.
