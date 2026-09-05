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

## SECTION 6 — WHAT WOULD CHANGE THE READING

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
