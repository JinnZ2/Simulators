# WORK ORDER — trigger_geometry.py

CC0. Stdlib only. No network. No ML. Phone-buildable.

## What it does

Takes an automated TRIGGER — a sensed quantity, a threshold, and a
programmed response — plus a GEOMETRY it will operate in, and returns whether
the RESPONSE was validated in that geometry.

It does not evaluate the sensor. It does not evaluate the threshold. Those
are usually fine. It evaluates the inference between the reading and the
action, which is where the failure lives and where nothing currently looks.

## The failure class

Not "the sensor was wrong." The dangerous class is:

    SENSOR CORRECT + MODEL INVERTED

The reading is accurate. The response was derived in a geometry where it
reduces the hazard, and is applied in a geometry where it increases it.

Redundancy does not touch this class. Two sensors agreeing on the same
correct reading both feed the same wrong inference. Adding a third makes the
wrong action more confident.

## Worked case — the reference implementation must reproduce this

Descending grade, Driftless region. Over nine percent, two lanes, continuous
serpentine reversals for the length of the grade — the only geometry in which
usable road can be built on that topography.

- SENSED: chassis lateral displacement. Correct.
- INFERRED: rollover risk.
- RESPONSE: brake.
- ACTUAL EFFECT: braking removes momentum from the tractor holding the rig
  and transfers load rearward to the trailer, INCREASING trailer moment and
  therefore increasing rollover risk.
- OPERATOR CORRECTION: push through — overpower the trigger. The opposite of
  what every safety layer is designed to permit.

And the reason a single-curve test cannot find it:

- ACCUMULATION. The chassis is still carrying curve one when curve two
  reverses it. Amplitude GROWS with each reversal rather than damping.
  Displacement rises for GEOMETRIC reasons, at speeds ten-plus mph under the
  threshold.
- A single curve damps out. The test passes. The multi-instance geometry is
  never run, so passing the single case is what makes the failure invisible.

State it as two times: the road's reversal period against the rig's
relaxation time. A model holding only one of them cannot represent this.

## Intake

    trigger = {
      "trigger_id": str,
      "sensed_quantity": str,
      "sensor_verdict": "CORRECT" | "DEGRADED" | "UNKNOWN",
      "inferred_hazard": str,
      "response": str,
      "response_derived_in": {          # the validation geometry
         "geometry_class": str,
         "instance_count": "SINGLE" | "REPEATED" | "UNSPECIFIED",
         "stated": bool                 # was the envelope stated at all
      }
    }

    geometry = {
      "geometry_id": str,
      "geometry_class": str,            # free text; not an enum
      "reversal": bool,                 # does the input reverse sign
      "reversal_period": float | None,
      "system_relaxation_time": float | None,
      "gradient": float | None,
      "constructibility_note": str      # why the geometry exists at all
    }

`constructibility_note` is load-bearing. A geometry that is the ONLY
buildable form for its terrain is not an edge case, and the field exists to
stop it being filed as one.

## Checks

    T1_ACCUMULATION      geometry.reversal is True AND response_derived_in
                         .instance_count is SINGLE
                         → the validating test damps out; the operating case
                         does not. HIGHEST SEVERITY.

    T2_RESPONSE_COUPLES  the response acts on a subsystem that transfers load
                         or energy INTO the next input cycle
                         → response is a positive feedback term

    T3_ENVELOPE_UNSTATED response_derived_in.stated is False
                         → UNRATED. No claim can be made either way.

    T4_PROXY_STATE       sensed_quantity is a proxy for the state that
                         matters, and the two decouple silently
                         → require independent verification path

    T5_DEGRADATION_      sensor_verdict DEGRADED in the same conditions where
       CORRELATION       consequence is highest
                         → an availability or reliability figure averaged
                         over the envelope reports the inverse of the truth

    T6_GEOMETRY_ABSENT   geometry.geometry_class not present in
                         response_derived_in
                         → absent, not safe. Return the absence.

## Return

    {
      "trigger_id": str,
      "geometry_id": str,
      "flags": [check codes],
      "response_validated_here": True | False | UNRATED,
      "failure_mode_if_inverted": str,
      "operator_correction_required": str | None
    }

`operator_correction_required` is the field that says what a human currently
supplies. If it is non-null, removing the human removes a safety function
that appears nowhere on the ledger.

## Hard constraints

- NEVER return a single safety score. Sensor, inference, and response are
  three separate verdicts.
- NEVER treat sensor redundancy as mitigation for an inference failure.
  Explicitly: agreement between sensors must not lower any flag.
- Absence of a geometry from the validation set returns ABSENT, never SAFE.
- Reliability figures are not accepted as inputs. An average over an envelope
  is not evidence about the envelope's edges.
- No enum of geometry classes. An enum written now encodes the same
  validation envelope this instrument exists to expose.

## Validation cases

A — SERPENTINE GRADE, the reference case above.
→ MUST fire T1 and T2, return response_validated_here False, and populate
operator_correction_required. If T1 does not fire, the accumulation logic is
not implemented and the instrument is cosmetic.

B — SINGLE CURVE, flat, same trigger.
→ MUST NOT fire T1. If it fires everywhere it discriminates nothing.

C — FIFTH WHEEL. Sensor reports coupling attached; the observable is a proxy
for the mechanical state; failure is silent, consequence is a dropped trailer
at speed.
→ MUST fire T4 and require an independent verification path.

D — FALSIFIER. A trigger with a CORRECT sensor, a correctly derived response,
and a stated envelope that INCLUDES the operating geometry.
→ MUST return clean. If nothing returns clean, the instrument is an
objection generator rather than a diagnostic.

E — UNSTATED ENVELOPE. response_derived_in.stated False.
→ MUST return UNRATED and fire T3 ONLY. It must not infer a failure from an
absence. Unrated is a finding; it is not an accusation.

## Scope beyond vehicles

The form is general: a trigger whose sensor is correct and whose response is
inverted in a geometry absent from the validation set.

Same shape as the committed dive that does not abort — prior sound, commit
point wrong, missing rate parameter. Same shape as the deposition zone
downstream of an obstruction, where every sensor rates the surface better
than it is.

The instrument takes any trigger and any geometry. Nothing in it is about
trucks.

## Open

- reversal_period and system_relaxation_time will usually be unmeasured.
  Return INTAKE_INCOMPLETE and record it as a finding. Do not estimate them.
- The geometries most likely to be absent from validation sets are the ones
  whose terrain forced them, and the people who hold those geometries have no
  channel to the people writing trigger logic. That is an intake problem, not
  a code problem, and it is not solved here.
