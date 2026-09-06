# WORK ORDER — CYCLE LEDGER + DATA-LAYER ENVELOPE INSTRUMENT

CC0. stdlib-only. Phone-buildable. No network dependency.
Source marker: MARKER_routing_data_layer.md (claims RDL-1 .. RDL-17)

## WHAT IS BEING ASKED FOR

Not an argument. Not a critique. An INSTRUMENT that any party —
carrier, vendor, regulator, researcher — can run against their own
operation and get a number out.

The marker states findings from one operator's corridor. The
instrument generalizes it so the finding is reproducible or
refutable by someone else's data.

Two deliverables, independent, either buildable alone.

## DELIVERABLE 1 — cycle_ledger.py

Input: a cycle described as ordered elements.
Output: the ledger, the classification, and the unclosed set.

### Per-element record

    element_id
    description
    rate_setter        one of:
                         HARDWARE      (plumbing, gearbox, air,
                                        load transfer, pack physics)
                         TERMINAL      (serial software interface,
                                        per-field accept cycle)
                         COUNTERPARTY  (gate guard, receiver,
                                        signature, door assignment)
                         ADMINISTRATIVE(posted speed, regulation)
                         SPATIAL       (clearance-bound, single
                                        attempt, no retry margin)
                         DECISION      (bound by choosing, not by
                                        executing)
    decision_latency_binds    bool — TRUE only if rate_setter
                              is DECISION
    currently_absorbed_by     OPERATOR | COUNTERPARTY | NONE
    notated                   bool — does this element appear in
                              any job spec, cost model, or
                              comparison?
    parallel_with             element_id or null — executed inside
                              another element's window at zero
                              added cycle time
    relocation_target         if operator removed: what standing
                              function absorbs it
    fault_alternates          count of held workarounds for this
                              element's known failure modes

### Required outputs

    1. RATE-SETTER HISTOGRAM
       Count of elements by rate_setter class.
       KEY READOUT: fraction where decision_latency_binds is TRUE.
       If that fraction is ~0, a faster decision layer cannot move
       the cycle, and the saving claim must name its mechanism
       elsewhere.

    2. TIED / BEHIND / AHEAD CLASSIFICATION
       TIED    — rate_setter is HARDWARE, TERMINAL, COUNTERPARTY,
                 ADMINISTRATIVE, or SPATIAL
       BEHIND  — element has parallel_with set (overlap lost), or
                 fault_alternates > 0 (fallback lost), or is a
                 recovery action requiring leaving the vehicle
       AHEAD   — decision_latency_binds TRUE
       Report all three counts. AHEAD is the claim's required
       support; if empty, say so plainly.

    3. UNNOTATED WORK REGISTER
       All elements where notated is FALSE.
       This is the work missing from the comparison sheet, not the
       cost missing from it. Report as a separate table with
       total count and which are safety-relevant.

    4. RELOCATION LEDGER
       For every element absorbed by OPERATOR, print its
       relocation_target. Group into standing functions.
       Output framing: what leaves the sheet (wage lines) vs what
       arrives on it (standing functions).

    5. SERIAL-INTERFACE CONDITION
       For every TERMINAL element, print the condition required
       for a faster sender to help: that interface rebuilt as
       parallel. Sum these into the stated precondition for the
       saving claim.

### Seed data

Ship with the marker's observed cycle as seed rows (fuel terminal,
gate, yard transit, backing, landing gear, airlines, fifth wheel,
dock approach assessment, tire inspection, lamp cross-validation,
receiving buzzer, paperwork, dead-wait recovery, close-out overlap,
fault workarounds, kingpin verification at 5 swaps/day).

Seed data must be clearly marked as ONE operator's corridor,
Upper Midwest, so a user replaces it rather than inherits it.

### NULL

If a user's own cycle returns a nonzero AHEAD count, the marker's
reading is wrong for that operation and the instrument should say
so without hedging. The tool must be able to return "the claim
holds here."

## DELIVERABLE 2 — rate_gap.py

Tests the structural-vs-maturity distinction (marker Section 5).

    INPUT
      environment_events   dated list for one jurisdiction over
                           one full construction season:
                           closures, reopenings, structure
                           removals, seasonal weight restriction
                           changes, repaints, resurfacing
      record_updates       dated list of when each of those
                           appeared in a routing data source

    OUTPUT
      dE/dt      environment state-change rate
      dM/dt      achieved record refresh rate
      lag distribution, per event class
      unrecorded set — events that never appeared at all

    READOUT
      dE/dt > dM/dt sustained, with a nonzero unrecorded set
        -> STRUCTURAL. Not a maturity gap.
      dM/dt >= dE/dt with unrecorded set empty
        -> maturity gap. Closes with funding.

    This is the cheapest test in the marker. One county, one
    season, no field automation, no vehicle required.

## BUILD CONSTRAINTS

    stdlib only. No pandas, no numpy, no network calls.
    Runs on a phone. Plain text or CSV in, plain text out.
    Every output must be readable without a terminal wider than
    60 columns.
    No dependency on any vendor API or proprietary map source.

## FRAMING CONSTRAINT

Framed as an argument against automation, this does not travel and
should not be built. Framed as an envelope instrument with a null
per readout, it travels to the people building the layer — who
have no access to this data.

Every absence must carry either a test or an explicit
"unrecoverable." Never an implication.

## OUT OF SCOPE

No characterization of the author or any operator. No
working-style or author-profile section. No biography. Instances
are observations only.

Sensing, control, and reasoning architecture are out of scope.
Every claim concerns what the reasoning would be reasoning OVER.

## OPEN, NOT GRADED

Continuous-operation duration for a driving stack is unpublished.
Industry reports uptime percentage against a maintenance-bay
operating model, not hours-to-degradation. The 14-hour regulated
figure and the 24-hour claim are therefore not comparable
quantities.

Do not assert an equivalence between operator fatigue and model
degradation. Different mechanism, unmeasured from inside. Record
as an open question with the missing measurement named.
