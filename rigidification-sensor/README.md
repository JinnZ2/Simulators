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

---

## §6 — code: `harm.py`

`harm.py` is the first §3 tell instantiated as a reader. Reads a
signature on a coupled `System` of `Node`s (each with `draw` and
`regen` rates) and `Coupling`s (with `transfer` and `sensitivity`).
Returns numbers and a shape; no verdict.

**Signature fields:**

| field | meaning |
|-------|---------|
| `local` | per-node `max(0, draw − regen)` (surplus exports nothing) |
| `per_order` | total induced imbalance at each order outward |
| `displaced` | any cost moved through a coupling |
| `inflates` | bool per the caller's chosen `inflates_mode` |
| `inflates_mode` | which physics reading was applied — carries forward |

**`inflates` has four caller-selectable modes** (no default; the choice
is physics-substantive, so `read()` raises `InflatesModeUnset` if the
caller omits it):

| mode | physics analog | reading |
|------|----------------|---------|
| `strict` | shipped behavior | all orders must grow, including through boundary zeros |
| `multiplication_factor` | nuclear k, epidemic R0, feedback loop gain | consecutive non-zero pairs must grow; peak must exceed source |
| `horizon_limited` | propagation constant defined only within the medium | auto-caps `orders` at `len(couplings)`; strict check on the capped window |
| `peak_to_source` | amplifier gain reported as max_output / input | no monotone requirement; fires on any cascade whose peak exceeds source |

Each mode is registered in `INFLATES_MODES` with its physics analog and
a usage note. The returned signature carries `inflates_mode` so a
downstream reader always sees WHICH physics was applied.

**The four modes are documented against a single amplifying-cascade
case** (system: `a(3,1) → b(1,1) → c(1,1)` with `transfer=1.0,
sensitivity=2.0` on both couplings; `per_order = [2, 4, 8, 0]` at
default `orders=3`):

| mode | `inflates` | why |
|------|-----------|-----|
| `strict` | `False` | trailing zero at order 3 breaks the check |
| `multiplication_factor` | `True` | zero skipped; peak 8 > source 2 |
| `horizon_limited` | `True` | orders auto-capped at 2 → `[2, 4, 8]` |
| `peak_to_source` | `True` | 8 > 2 regardless of shape |

`_t_amplifying_coupling_inflates` locks in each mode's answer, so
future edits surface which cases move.

Self-test: `python3 harm.py` runs 6 assert-based tests (all pass) and
prints the mode registry.

Sample: [`samples/harm.sample.txt`](samples/harm.sample.txt)

---

## §7 — code: `simulator.py`

`harm.read` is a snapshot. `simulator.run` makes it dynamical: displaced
cost actually erodes the receiving node's `regen`, so the deficit
compounds. Persistence IS the §1 invariant — "cheaper to continue than
reverse" stops being a phrase and becomes a measured divergence.

Time carries the propagation: one coupling hop per tick, so `order == tick`.

**Per-tick tells:**

| field | meaning |
|-------|---------|
| `dof` | nodes still in surplus (`regen > draw`) — off-ramps open |
| `continuation` | current total imbalance — the bill this tick |
| `reversal` | cumulative eroded regen — capacity you'd rebuild to undo |
| `d_continuation` | change in continuation vs last tick |
| `d_reversal` | change in reversal vs last tick |

**`locked_at`**: first tick where `reversal > continuation` AND
`d_reversal > d_continuation` — the §1 threshold crossing. Past that
tick, pruning stops being cheap.

**Demo (amplifying chain, ticks 0–11):**

```
t  dof  contin  revers  dCont  dRev
0  1    2.0     2.0     2.0    2.0
1  0    3.0     4.0     1.0    2.0     ← locked_at
2  0    4.0     4.0     1.0    0.0
3+ 0    4.0     4.0     0.0    0.0     (saturated)
```

`dof` drops from 1 → 0 between tick 0 and tick 1 (off-ramp b closes as
its regen erodes past its draw). Lock fires at tick 1. After tick 2,
both metrics saturate at a shared cap because the erosion has driven
every node's regen to zero — read the lock at the crossing tick, not
at the trace's end.

Self-test: `python3 simulator.py` runs 3 tests + demo.

Sample: [`samples/simulator.sample.txt`](samples/simulator.sample.txt)

`simulator.py` is the first `§3 tells` instantiated as a live dial —
step 4 of the §5 handoff. Each tell is per-tick, so an operator can
watch the crossing arrive rather than diagnose it after.
