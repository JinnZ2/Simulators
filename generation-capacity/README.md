# generation-capacity

CC0. Stdlib only. No dependencies.

Mechanism ten in the `uninstrumented` series: cases where the option space
itself was removed upstream, so a binary presented at the affected scale is
honest at that scale and manufactured at the scale above.

## MARKER PROTOCOL

This repo is a marker of something to explore, not a position under defense.
Correct responses are: test fit, extend it, or report where it breaks. It is
not a thesis to attack or defend, and it may or may not match what is done in
practice anywhere.

## THE CASE THAT SEPARATES THIS FROM MECHANISM 9

CATEGORY WELD fuses independent quantities into one handle so components move
without the record moving. This is different: nothing is fused and nothing is
concealed. The capacity to produce the quantity has been removed.

Worked instance. Someone who can name what is edible around them, when it is
up, and how to hold it through a season never faced two options. Remove that
across two or three generations and "buy it or go without" becomes physically
true for the person standing in it. An option-space audit asking how many
alternatives were generated gets the answer two, truthfully. The instrument
reads a found constraint. The constraint is real. It was not found in the
world.

## HANDOFF FROM binary_audit.py

O1 returning documented with a low count is the trigger. An option-space audit
closing clean on a low honest count is the signature of this mechanism, not
evidence of its absence.

    binary_audit.py --case X    ->  O1 documented, count <= 2
                                ->  capacity.py --case X

## READOUTS

    R1  recall_ratio       nameable / present, per place, per generation
    R2  transmission_gap   generations since capacity held at stated level
    R3  loop               deficit cited as grounds for the gate producing it

R1 slope within a case is the usable signal. Cross-case R1 is not valid until
the recall method is fixed and recorded (see CLAIM_TABLE disclosed weaknesses).

## CALIBRATION CONSTRAINT

R1 must be scored against what is present in the place. Scoring against a
central reference reproduces the mechanism being measured: knowledge of a
place scores zero on a test built from the set that excluded it. The
`scored_against` field enforces this — set to `center`, the reading is flagged
invalid and excluded from slope.

## USAGE

    python3 capacity.py                  table over cases/
    python3 capacity.py --case NAME      detail
    python3 capacity.py --new NAME       blank case skeleton
    python3 capacity.py --jsonl          machine readable
    python3 capacity.py --selftest       synthetic fixtures

## ADDING A CASE

    python3 capacity.py --new my-case > cases/my-case.json

Fill `present` and `nameable` only from readings that exist. Leave null
otherwise — the scorer prints `--` and does not estimate. Record
`source_present` and `source_nameable` including `NOT COLLECTED` where that is
the state.

## STATE

Two seed cases, zero quantified readings. Schema and calibration check are
tested against synthetic fixtures (8/8). The repo demonstrates a schema, not a
finding. G7 in CLAIM_TABLE is the checkable claim and has not been checked.
