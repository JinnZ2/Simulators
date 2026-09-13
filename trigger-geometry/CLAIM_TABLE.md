# CLAIM TABLE -- trigger-geometry

`TG_*` are findings about the build and about the delivered order. They are
distinct from the order's own `T1..T6`, which are checks, and from its
validation cases `A..E`.

Every case in `cases.py` is CONSTRUCTED. Nothing here has been run against a
real control unit, a real vehicle or a real road, and no claim below is a
statement about any of those.

---

## TG_001 -- case A's stated requirement forces the reference failure to be T1, not T6

**Status: SUPPORTED, and it is a choice the order makes rather than states.**

The worked case is a response derived in one geometry and applied in
another, which reads as T6 (`geometry_class not present in
response_derived_in`). But the hard constraints say an absent geometry
returns ABSENT and never SAFE, and validation case A says the serpentine
grade MUST return `response_validated_here False`.

`False` and `ABSENT` are different returns. So for case A to return what the
order requires, T6 must be SILENT, which means the envelope must NAME the
serpentine class. The reference case is therefore an **instance-count**
failure, not a class-absence one: the validating set knew the geometry and
ran it once.

That is the stronger reading of the order's own prose -- *"A single curve
damps out. The test passes. The multi-instance geometry is never run"* --
and `cases.py` enters the trigger that way, with the envelope naming both
classes and `instance_count` SINGLE.

**Falsified by:** a reading of case A on which UNRATED/ABSENT satisfies
"return response_validated_here False".

---

## TG_002 -- three of the order's six checks have no field in the order's own intake schema

**Status: SUPPORTED. Measured, not argued -- `schema_support()`.**

    T1  reversal, instance_count           in the schema
    T3  response_derived_in.stated         in the schema
    T6  geometry_class both sides          in the schema
    T2  does the response feed the next input cycle   NO FIELD
    T4  does the proxy decouple silently             NO FIELD
    T5  sensor_verdict (in) AND is this the high-consequence
        condition (NO FIELD)                          ONE OF EACH

The `MF_017` / `CW_015` / `DL_004` / `GC_012` / `UNI_013` / `SSS_050` /
`RT_009` shape -- a stated rule with no schema slot -- at **3 of 6 scale**,
the largest instance recorded in this family.

`[CHOICE 1]`: each becomes a DECLARED three-value field (`YES` / `NO` /
`UNDECLARED`). `UNDECLARED` returns NOT_EVALUABLE: it neither fires nor
clears, because inferring *the response does not couple* from nobody having
said so is the silence the instrument exists to refuse.

---

## TG_003 -- under the delivered schema alone, no trigger can ever be validated

**Status: SUPPORTED, and it follows from TG_002 plus the order's case D.**

Case D requires a clean return to be reachable -- *"If nothing returns
clean, the instrument is an objection generator rather than a diagnostic."*
Clean requires T2, T4 and T5 SILENT. Those three read the added fields. A
trigger written to the order's schema and nothing else declares none of
them, so all three return NOT_EVALUABLE, and `[CHOICE 9]` blocks a `True`
verdict on a check nobody ran.

So the falsifier case cannot be constructed from the delivered schema. The
three added fields are not a convenience; without them the clean branch is
`CONSTANT_SILENT` and the instrument fails its own case D by construction.

---

## TG_004 -- the hard constraints name a state and a shape the Return block does not carry

**Status: SUPPORTED. Two of them, in the same six lines.**

1. *"Absence of a geometry from the validation set returns ABSENT, never
   SAFE."* The stated return is `True | False | UNRATED`. There is no
   `ABSENT`. `[CHOICE 3]`: the three values stay exactly as delivered and
   `validated_reason` rides beside them, so ABSENT is distinguishable from
   an unstated envelope and from a check nobody ran -- three routes to
   UNRATED that call for three different next actions.
2. *"Sensor, inference, and response are three separate verdicts."* The
   Return block has one field. `[CHOICE 4]`: `verdicts` carries all three
   beside the delivered field, and `BEARS_ON` declares which check touches
   which, so the assignment can be disagreed with rather than guessed at.

---

## TG_005 -- T1 as written reads neither of the two times the order calls load-bearing

**Status: SUPPORTED.**

The order: *"State it as two times: the road's reversal period against the
rig's relaxation time. A model holding only one of them cannot represent
this."* T1 as specified reads `geometry.reversal` and
`response_derived_in.instance_count`, and neither time appears in it.

`[CHOICE 6]`: `accumulation_ratio` is computed where both are present and
**gates nothing**. Making it a precondition would stop T1 firing on the
order's own reference case, where the Open section says both times will
usually be unmeasured -- and the reference geometry in `cases.py` leaves
both `None`, as it says.

Registered in `tools/known_answer.py` with four cases; it is the only
function here returning a number rather than a declared vocabulary member.

---

## TG_006 -- the Open section and validation case A pull opposite ways on the two times

**Status: SUPPORTED. Resolved in favour of the case, and the resolution is
declared.**

Open: *"reversal_period and system_relaxation_time will usually be
unmeasured. Return INTAKE_INCOMPLETE and record it as a finding."* Case A:
the serpentine grade MUST fire T1 and return False, and names no times.

Returning INTAKE_INCOMPLETE on an absent time would make the order's own
reference case unreachable. `[CHOICE 5]`: absent times are recorded in
`times_unmeasured` and do not block; only an absent REQUIRED field returns
INTAKE_INCOMPLETE. Nothing estimates them, which is the part of the Open
instruction that is unambiguous.

---

## TG_007 -- case E's "T3 ONLY" forces T3 to suppress T6, not merely to outrank it

**Status: SUPPORTED.**

Case E has `stated` False and, naturally, no `geometry_class` in the
envelope. T6 would then return NOT_EVALUABLE, and on a trigger that named a
class for a different geometry it would FIRE -- either way not *T3 only*.

`[CHOICE 2]`: when T3 fires, T6 is set SILENT and the suppression is
REPORTED in a `suppressed` list rather than hidden. An envelope that was
never stated cannot be asked whether it covers a geometry.

---

## TG_008 -- two of the six checks cannot reach NOT_EVALUABLE through `read()`, and one is repairable and one is not

**Status: SUPPORTED. Measured in section 10 of the suite.**

T3 returns NOT_EVALUABLE when `stated` is not a bool -- and intake refuses a
non-bool `stated`, so the branch is unreachable through `read()`. The branch
is exercised on the check function directly and recorded here rather than
deleted: deleting it would make `t3_envelope_unstated` silently assume a
bool from a caller that is not `read()`.

T6's NOT_EVALUABLE branch WAS unreachable for the same reason, until a case
was added for the state that produces it honestly: an envelope **stated**
with no class named (`envelope_no_class`). That is a real trigger shape --
the envelope exists and does not say where -- and is distinct from case E,
where nothing was stated at all.

---

## TG_009 -- redundancy invariance is measured, not promised

**Status: SUPPORTED.**

*"Agreement between sensors must not lower any flag."* Stating it is cheap.
`redundancy_effect()` sweeps the field over seven settings including
`"two sensors, agreeing"` and `"three, unanimous"` and requires every flag,
every verdict and the return value unchanged; the suite also asserts from
the AST that no check function body names anything matching `redundan`, and
null-tests the sweep by showing it reports movement when a flag really
moves.

Two corpus cases declare agreeing sensors (`washout_detect` two agreeing,
`fineness_probe` three agreeing) and both still flag.

---

## TG_010 -- reliability figures raise rather than being dropped, and the screen is a word list

**Status: SUPPORTED, with the limit stated at the top of the module.**

*"Reliability figures are not accepted as inputs."* An ignored input is one
somebody assumes was used, so `read()` raises `ReliabilityInput` naming the
offending key, at any nesting depth. `[CHOICE 7]`.

The screen is twelve tokens matched against the split parts of a key name.
A figure under a name not on the list enters as an ordinary field. That is
`UNI_009` / `T1-1` / `ACL_017` again and is not repaired: no word list
separates a reliability figure from a number.

The token list deliberately does NOT appear in the identifier scan, because
`RELIABILITY_TOKENS` is itself an identifier and a module has to be able to
name what it refuses.

---

## TG_011 -- "no enum of geometry classes" is met structurally, and the cost is that T6 is string equality

**Status: SUPPORTED.**

No constant in the module holds a geometry class name (asserted by scanning
every upper-case tuple and list against the corpus's classes), `geometry_class`
is validated against nothing, and a class string invented inside the test
runs end to end and is correctly reported ABSENT rather than refused.

The cost: T6 compares the operating class against the envelope's declared
classes by **equality**. Two names for one geometry read as two geometries,
and one name covering two read as one. An enum would fix the first and is
exactly what the hard constraint forbids, for the stated reason -- *"an enum
written now encodes the same validation envelope this instrument exists to
expose."* Recorded, not repaired.

---

## TG_012 -- the unledgered safety function is counted per reading and per trigger, and the two differ

**Status: SUPPORTED.**

*"If it is non-null, removing the human removes a safety function that
appears nowhere on the ledger."* On this corpus: 5 readings of 11, 4
distinct triggers. `serpentine_brake` carries an operator correction in both
geometries it is read in, so a per-reading count alone double-counts one
function. Both numbers are printed; neither is the score.

---

## TG_013 -- UNVERIFIED: nothing here has met a trigger

**Status: UNVERIFIED, and it covers the whole folder.**

No trigger was read off a control unit. No `sensor_verdict` was measured. No
geometry was surveyed, and every `reversal_period` and
`system_relaxation_time` in `cases.py` is either `None` or a number invented
so the ratio has a value somewhere. The reference case is transcribed from
the work order's prose, which is an operator's account, and is carried as
such -- it is not confirmed here and nothing in TG_001..TG_012 rests on it
being true of any road.

What IS established is the order's own falsifier set: case A fires T1 and
T2 and returns False, case B does not fire T1, case C fires T4 and requires
an independent verification path, case D returns clean, case E returns
UNRATED on T3 alone. Whether the six checks separate an inverted response
from a sound one on a real trigger is untouched in both directions.

The order's second Open item is untouched too, and is not a code problem:
*"the geometries most likely to be absent from validation sets are the ones
whose terrain forced them, and the people who hold those geometries have no
channel to the people writing trigger logic."* `constructibility_note` is
the field that would carry that if anyone filled it, and every geometry here
fills it because the author of the case filled it.
