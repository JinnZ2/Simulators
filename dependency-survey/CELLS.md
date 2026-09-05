# CELLS — coded cells, human-editable

One block per coded cell. `survey.py` parses this file; edit here, not in
code. A cell not listed here is UNKNOWN by default. Cells are added
incrementally.

Block format (exactly these keys; omit a key to leave it empty):

    ## T<n> x S<n>
    status: MEASURED | MISSING | SCOPE-DIFFERENT
    measured_as: quantity + units + how obtained   (required for MEASURED)
    reference: what frame/boundary/baseline this substrate's measure is taken against   (SCOPE-DIFFERENT)
    maps_to: what in the comparison substrate it corresponds to   (SCOPE-DIFFERENT)
    breaks_at: where the correspondence fails, and on what   (SCOPE-DIFFERENT)
    scope_note: optional free text; NOT the admissibility basis for SCOPE-DIFFERENT (the three transform fields are)
    source: where the coder got it
    provisional: yes | no   (optional; a claim to be checked, not an established finding)
    transfer: the analogue quantity in this term's missing substrate, in that substrate's own units (optional, for a gap's target)
    no_transfer: yes | no   (optional; the transfer question cannot be stated in the target's own units)

Per ADDENDUM_01: a MEASURED cell needs `measured_as` with units; a
SCOPE-DIFFERENT cell needs all three of `reference` / `maps_to` /
`breaks_at` (a SCOPE_TRANSFORM), NOT units. A SCOPE-DIFFERENT cell with
a prose note and no complete transform is not admissible and downgrades
to UNKNOWN, reported on its own line.

Seeded cells (carried in from prior sessions; do not re-derive):

## T1 x S1
status: MEASURED
measured_as: energy intake per unit handling time, and its variance; standard optimal-foraging currency, J/s
source: optimal foraging literature

## T1 x S2
status: MISSING
source: named in session as the worked example; cost asymmetry is well measured in optimal-foraging work and appears unmeasured in multiagent harnesses
provisional: yes

## T3 x S5
status: SCOPE-DIFFERENT
scope_note: dependencies real and load-bearing but drawn outside the accounting boundary, so the self-model is accurate within its boundary and wrong about what holds the boundary up; same error one scale down is the adult child in the parents' basement, with insurance liability, tax exposure and maintenance decisions all outside the drawn boundary
source: prior session
