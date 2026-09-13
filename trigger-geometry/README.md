# trigger-geometry

**Was this response validated in THIS geometry.**

A trigger is a sensed quantity, a threshold and a programmed response. Give
it one, plus a geometry it will operate in, and it reports whether the
RESPONSE was validated there.

It does not evaluate the sensor. It does not evaluate the threshold. Those
are usually fine. It evaluates the inference between the reading and the
action.

    WORK_ORDER.md       delivered verbatim
    trigger_geometry.py the instrument
    cases.py            constructed triggers and geometries, no verdicts
    test_trigger.py     every expected verdict lives here
    CLAIM_TABLE.md      TG_001..TG_013
    samples/            one pinned run of each

    python3 trigger_geometry.py        # the corpus
    python3 trigger_geometry.py --choices
    python3 test_trigger.py            # prints its own check count

Stdlib only. No network. Parses under 3.9. Phone-buildable. CC0.

---

## The failure class

Not *the sensor was wrong*. The dangerous one is

    SENSOR CORRECT + MODEL INVERTED

The reading is accurate. The response was derived where it reduces the
hazard, and is applied where it raises it.

**Redundancy does not touch this class.** Two sensors agreeing on the same
correct reading feed the same wrong inference; a third makes the wrong
action more confident. That is a hard constraint, and it is measured rather
than promised -- `redundancy_effect()` sweeps the field and requires every
flag unchanged, and the suite asserts from the AST that no check body reads
it (TG_009).

---

## Shape of a read

                    trigger                     geometry
                       |                            |
         +-------------+-------------+              |
         |             |             |              |
    sensed        inferred       response      class, reversal,
    quantity      hazard         + envelope    two times, why the
         |             |             |         geometry exists
         |             |             |              |
         v             v             v              v
    +--------------------------------------------------------+
    |  T1 accumulation      reversal AND envelope SINGLE      |
    |  T2 response couples   feeds the next input cycle        |
    |  T3 envelope unstated  no claim either way               |
    |  T4 proxy state        observable and state part silently|
    |  T5 degradation        DEGRADED where consequence is high|
    |  T6 geometry absent    class not in the envelope         |
    +--------------------------------------------------------+
         |                    |                    |
         v                    v                    v
      sensor              inference             response
     (carried,         NOT_CONTRADICTED     NOT_CONTRADICTED
      never              / INVERTED           / INVERTED
      computed)          / UNRATED            / UNRATED
                         / NOT_EVALUABLE      / NOT_EVALUABLE

    response_validated_here : True | False | UNRATED
    validated_reason        : CLEAN | FLAGGED | ABSENT
                            | UNSTATED_ENVELOPE | CHECKS_NOT_EVALUABLE
                            | INTAKE_INCOMPLETE

Three verdicts, never one. No arithmetic operator touches any of them, and
the suite asserts it from the AST.

---

## The accumulation point

    single curve       |\        one reversal, damps, the test passes
                       | \_____

    serpentine grade   |\  /\  /\      still carrying curve one when
                       | \/  \/  \     curve two arrives; amplitude
                                       GROWS for geometric reasons

The two times are the road's reversal period against the rig's relaxation
time. `accumulation_ratio` reports `relax / period` -- above 1 the system
has not settled before the next reversal -- and it **gates nothing**,
because T1 as specified reads neither time and making the ratio a
precondition would stop T1 firing on the order's own reference case, where
both times are unmeasured (TG_005, `[CHOICE 6]`).

Registered in `tools/known_answer.py`: 7/2 -> 3.5, 1/4 -> 0.25, an absent
time -> None (never 0.0, which would read as *damps instantly* on a geometry
nobody timed), a zero period -> None.

---

## What the order left open, and what was decided

Nine `[CHOICE n]` markers, printed by `--choices` and cited inline at the
site where each takes effect. The load-bearing ones:

| | |
|---|---|
| `[CHOICE 1]` | **Three of the order's six checks have no field in the order's own intake schema.** T2, T4 and T5 run on declared three-value fields this build added. `UNDECLARED` neither fires nor clears. (TG_002) |
| `[CHOICE 3]` | The hard constraints name `ABSENT`; the Return block's three values do not carry it. `validated_reason` rides beside them. (TG_004) |
| `[CHOICE 5]` | An absent `reversal_period` is a finding, not a block -- the Open section and case A pull opposite ways. (TG_006) |
| `[CHOICE 9]` | A check nobody ran blocks a `True`. Validating on an unevaluated check is the pass this instrument exists to refuse. |

---

## Findings

`CLAIM_TABLE.md`, TG_001..TG_013. The three that change how the order reads:

- **TG_001** -- case A's requirement of `False` (not ABSENT) forces the
  reference failure to be an **instance-count** failure and not a
  class-absence one. The validating set knew the geometry and ran it once.
- **TG_002 / TG_003** -- three of six checks have no schema field, and the
  consequence is that under the delivered schema alone **the clean branch is
  unreachable**, so the order's own falsifier case D cannot be built without
  the added fields.
- **TG_011** -- *no enum of geometry classes* is met, and the cost is that
  T6 is string equality: two names for one geometry read as two. An enum
  would fix it and is exactly what the constraint forbids. Recorded, not
  repaired.

**TG_013 is UNVERIFIED and covers the whole folder.** Every trigger and
geometry in `cases.py` is CONSTRUCTED and says so. No control unit was read,
no geometry surveyed, no time measured. The reference case is transcribed
from the order's prose -- an operator's account, carried as such. What is
established is that the order's five validation cases return what the order
says they must; whether the six checks separate an inverted response from a
sound one on a real trigger is untouched in both directions.

---

## Nothing in it is about trucks

The corpus carries two non-vehicle readings from the order's own scope
section: the deposition zone in the lee of an obstruction, where the correct
surface reading supports the inverted inference (the same shape worked at
length in `terrain-prior/`), and the committed dive, where the prior is
sound and the commit point is wrong for want of a rate.

Siblings: `terrain-prior/` (the same inversion read off an indicator rather
than a trigger), `null-harness/` (`CONSTANT_SILENT`, which is what an
instrument that never returns clean would be), `reasoning-gate/` (`G-RES`,
the feature-against-instrument pair the two times are an instance of).
