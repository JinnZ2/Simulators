# return-path

Built to `WORK_ORDER.md`, which is delivered verbatim and modified by
nothing here.

Scores a proposed or existing correction channel against four requirements
and returns the **SET** of requirements failed. It does not rank channels,
does not recommend, does not resolve, and does not ask whether a channel is
useful. A channel can be valuable and still not be a return path. Marking a
gap is not correcting an error.

```
python3 return_path.py     # the case set, the choices, the measured properties
python3 test_return.py     # the checks; the count is printed, not stored here
```

## The four checks

| code | fires when | field it reads |
|---|---|---|
| `C1_RECEIPT` | `receipt != MANDATORY` | `receipt` |
| `C2_SIGNAL` | `signal_encodings > 0` | `signal_encodings` |
| `C3_LATENCY` | `latency >= build_on_time` | `latency`, `build_on_time` |
| `C4_CONSTRUCTION` | `construction != SLOW_SIDE_ONLY` | `construction` |

Each reads its own fields and no others. That is asserted twice: by running
the flip experiment (`independence()` — change one check's fields, only that
check moves) and by reading each function's body out of the AST and
comparing it against the `CHECK_FIELDS` table, so the table cannot drift
from the functions it describes.

`grade` is `RETURN_PATH_GRADED` if and only if `failed` is empty. Nothing
sums, counts or averages the set — asserted from the AST.

## The case set

```
A_physical_consequence      RETURN_PATH_GRADED   (none)
B_incident_reporting        NOT_A_RETURN_PATH    C1
B_report_written            NOT_A_RETURN_PATH    C1, C2
C_publication_loop          NOT_A_RETURN_PATH    C1, C2, C3
D_field_report_written      NOT_A_RETURN_PATH    C1, C2, C3, C4
D_field_no_report           NOT_A_RETURN_PATH    C1, C3, C4
D_no_channel                INTAKE_INCOMPLETE    missing: latency
E_fast_side_writes          NOT_A_RETURN_PATH    C2   + F_FAST_SIDE_ENCODER
F_receipt_unspecified       NOT_A_RETURN_PATH    C1   + F_UNSPECIFIED_RECEIPT
G_build_on_time_absent      INTAKE_INCOMPLETE    missing: build_on_time
H_build_on_time_zero        NOT_A_RETURN_PATH    C3   ratio UNDEFINED
I_receipt_out_of_vocabulary INTAKE_INCOMPLETE    invalid: receipt
J_encoder_none_above_zero   INTAKE_INCOMPLETE    invalid: encoder_position
```

Every channel is **CONSTRUCTED** and every number is stipulated by whoever
typed it. Nothing here is a measurement of any real correction channel.

Expected verdicts live in `test_return.py` and not in `cases.py`, so no case
can agree with the module by construction.

## Two of the order's own cases could not be entered as described

Recorded rather than smoothed, and shipped as paired variants so the reading
is visible instead of chosen quietly.

**B.** The order requires case B to fail `C1` **only**, and the channel it
describes is *an incident reporting system* — where somebody writes a
report, which is at least one encoding. Entered faithfully it fails `C1` and
`C2`. The stated requirement holds of the encodings-0 entry alone.

**D.** The order says of case D that *no channel exists* from the
observation to the claim, and requires it to fail `C1`, `C3` and `C4`. A
channel that does not exist has no latency, and a channel with no latency
returns `INTAKE_INCOMPLETE` — which is not a verdict at all. `D_no_channel`
is the faithful entry; `D_field_report_written` and `D_field_no_report`
enter an elapsed standing time instead, and split on the `C2` axis the order
leaves open.

## Where the intake refuses

`INTAKE_INCOMPLETE` on any absent field, naming it. On a present-but-
unusable field the return is the same grade and the field lands in
`invalid` rather than `missing`: absent and present-and-wrong are different
states, and the order names only the first.

`failed` is `None` when no check ran and `[]` when four ran and none fired.
`ratio` is `None` in three distinguishable situations and `ratio_state`
carries which.

The order's own Open section expects `INTAKE_INCOMPLETE` to be the most
common return, because nobody measures when output starts being built on.
That is a finding about the system, not a defect in the instrument.

## Hard constraints, each enforced rather than promised

- **No banned field name** — an AST walk over identifiers and dict keys for
  the standing family the order bans, using `tools/authority_scan.py` and
  null-tested on a plant. A substring scan would fire on the sentences here
  naming what is refused.
- **No content scoring** — `scope_note` is carried byte-for-byte, exactly
  one comparison in the module names it and that one is the presence test,
  and no branch inside `read()` reads it. There is no content field at all.
- **No conversion of times, no default for either** — both times are
  required, `time_unit` is recorded and never used to convert.

## Seven declared choices

The order leaves seven decisions open. Each is in `CHOICES`, printed in the
header of every render, and none is silent. The largest is `[CHOICE 1]`:
the order names `INTAKE_INCOMPLETE` as a return and gives the `grade` field
two values, so the return shape has no slot for the return the order's own
Open section expects to be most common.

## Findings

`CLAIM_TABLE.md`, `RP_001..RP_015`. `RP_015` is UNVERIFIED: nothing has been
run against a real channel, so whether these four checks separate return
paths from recommendation channels in the field is untouched in both
directions.

Stdlib only. No network. Parses under Python 3.9. Phone-buildable. CC0.
