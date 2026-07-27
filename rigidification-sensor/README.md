# rigidification_sensor — trajectory spec

CC0. Draft skeleton. Not a prediction. A structure to run claims against.

Frame: this maps a branch, not an outcome. Selection of branches is
itself a claim (see §0). No actor, no motive, no controller is asserted
anywhere. "Control" throughout means control *parameter* — a knob — not
a hand on a knob.

---

## §0 — branch selection (the prior, stated openly)

These branches were drawn, others were not. That choice is a claim and
must be defensible before the rest is trusted.

    selected_because:
      - node carries high load with low observability (credit–insurance)
      - failure mode is reversibility-loss, which is measurable pre-outcome
      - candidate knobs are structural, so leverage exists without needing intent
    NOT_selected:
      - actor-driven / coordinated-cull branches — excluded: require
        asserting intent that is not in evidence
      - pure-noise branch (markets simply wrong) — retained as null
        hypothesis in §2, not excluded

If §0 is wrong, everything downstream inherits the error. Attack here first.

---

## §1 — invariant (the shape that survives any story told over it)

    invariant:
      statement: >
        variance in a system is suppressed faster than it regenerates;
        past a threshold the suppression is self-reinforcing —
        cheaper to continue than to reverse.
      names_no: [actor, motive, plan]
      is_a: rate crossing a line
      substrate_independent: true    # seeds, credit models, cultures — same shape

Everything else hangs off this. It is a process, not a plot.

---

## §2 — claims (each written so reality could kill it)

Value of the falsifier is left OPEN. We specify what *kind* of
measurement settles it and hand the hole to whoever has the compute.
An honest claim with a hole shaped like the missing data beats a
fabricated number.

    claim_template:
      id:
      statement:
      falsifier_shape:        # what class of measurement would disconfirm
      falsifier_value: OPEN   # not supplied — next operator measures it
      null_hypothesis:        # the boring explanation this must beat

    claim_001:
      statement: >
        variance in <node> is declining at a rate that outpaces regeneration.
      falsifier_shape: >
        evidence that regeneration keeps pace, OR that decline reverses
        below the cost-of-reversal threshold.
      falsifier_value: OPEN
      null_hypothesis: transient consolidation that self-corrects on cycle turn

    claim_002:
      statement: >
        homogenization rate responds to control-parameter K.
      falsifier_shape: >
        turning K (risk-pricing uniformity / subsidy gradient / liability
        rule) produces no measurable change in variance-suppression rate.
      falsifier_value: OPEN
      null_hypothesis: K is downstream of the rate, not a driver of it

    claim_003:
      statement: >
        cost-of-reversal at <node> is rising faster than cost-of-continuation.
      falsifier_shape: >
        reversal cost flat or falling relative to continuation cost over window.
      falsifier_value: OPEN
      null_hypothesis: measured asymmetry is an artifact of the accounting frame

---

## §3 — tells (observables; read near-real-time, before outcome resolves)

Tells measure REVERSIBILITY, not harm. Not watching for badness —
watching for off-ramps closing. Each tell is a degree-of-freedom count.

    tells:
      first_order:               # count viable alternatives ACTUALLY in use
        - viable options in-use at node, not merely catalogued
        - independent risk models pricing the node (vs. one shared model)
        - real alternatives surviving at each choice point
        direction_of_concern: counts trending down

      second_order:              # the sharpest alarm
        - cost_of_reversal vs cost_of_continuation, first derivative
        fires_when: reversal gets expensive faster than continuation
        why_it_matters: >
          this is the §1 threshold being crossed live — the last window
          where pruning is still possible but about to stop being.

    reading:
      solidifying: counts drop / reversal-cost derivative positive
      still_open:  counts hold or climb / reversal-cost derivative <= 0

---

## §4 — candidate knobs (for exploration, not asserted)

    candidate_control_parameters:
      credit_insurance_node:
        - risk-pricing uniformity   # uniform models force uniform behavior;
                                     # deviation penalized as error → variance drains
        - subsidy / liability gradient that makes monoculture cheaper than variance
      status: hypotheses. each feeds claim_002 as a testable K.

---

## §5 — handoff

Needs: more time, more compute, AI partners, iterated claims.
Task for next operator:
  1. contest §0
  2. instantiate <node> concretely
  3. measure the OPEN falsifiers
  4. stand up §3 tells as a live dial
Goal: make the branch legible enough to prune — pull probability back
under threshold by illuminating the off-ramp, not by predicting the fall.
