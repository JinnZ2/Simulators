# transmission-cascade

WO-8 delivered verbatim (`WORK_ORDER.md`) and built to: two literatures
each hold half of a multi-level cascade coded by TRANSMISSION TYPE, and
neither cites the other. Literature A (organizational cascade) has depth
and outcome measures and identification-with-leader as a posture
moderator; Literature B (cultural evolution) has the transmission-content
taxonomy. The join is the deliverable.

```
  STIMULUS ENHANCEMENT   attention directed to an object
  EMULATION              the RESULT is copied; the means are not  -> recomputable
  IMITATION              the specific MEANS are reproduced
  OVERIMITATION          ALL steps copied, no access to why       -> not recomputable

  decisive prediction: under a condition change, a copied-STEPS
  transmission has nothing to recompute from; an emulation does.
  Types look alike under stable conditions and separate only when
  conditions change.
```

CC0. Python 3.9+, stdlib only, no network, phone-buildable.
`transmission_cascade.py` renders on bare invocation, prints its choices
with `--choices`, and refuses `--selftest` (exit 2); `python3
test_cascade.py` runs the checks and prints their count. **No dataset is
recoded** and every world is CONSTRUCTED with a declared generative
model; nothing here is a statement about any cascade (`TC_008`).
`cohen_kappa` is imported from `effective-redundancy-audit`, not copied.

---

## WHAT RUNS, IN ORDER

| step | computes | gate |
|---|---|---|
| R2 | Cohen's kappa between two coders' type labels, blind to layer and outcome | GATES R1: below the 0.60 floor the taxonomy does not code the material reliably, and that it is domain-bound is the finding |
| R1 | count of each transmission type per layer | WITHHELD unless R2 cleared the floor -- the distribution is not computed on unreliable labels |
| R3 | the recompute share per type after a condition change | a run with neither response is NOT_EVALUABLE, excluded from the denominator; NOT_EVALUABLE overall if a decisive type has no scored runs |
| R4 | is-overimitation and identification-with-leader entered together on the recompute outcome | type "adds nothing" unless its coefficient stays MATERIAL with identification entered |

---

## WHAT THE MACHINERY SHOWS

- **R2 gates R1 and the gate is not decorative.** On the high-agreement
  constructed coding kappa clears the floor and R1 renders; on a
  low-agreement coding R1 is WITHHELD and the module reports that the
  taxonomy is domain-bound, which is the order's stated useful result
  costing one subsample (`TC_001`, `TC_002`).
- **R3 is a known-answer run on the scorer.** The condition-change runs
  are generated with overimitation repeating and emulation recomputing
  -- the order's own prediction as a declared model -- so a scorer that
  did not recover emulation-above-overimitation would be broken; the
  does-not-transfer branch is reachable on a flat world, so the verdict
  is not `CONSTANT_FIRES` (`TC_003`, `TC_004`).
- **R4 enters the competing explanation alongside, not instead.** With a
  real type effect and null identification, type survives; with a real
  identification effect and null type, type adds nothing. The **material
  floor** is what separates them: both pass a relative-only test when the
  coefficients are noise near zero, so an absolute floor of 0.10 is
  required and declared (`TC_005`, `TC_006`).
- **The scope limit is the object, not a caveat.** The taxonomy's
  transfer from children-and-toolmaking to adult hierarchy is unvalidated
  and R2 is where that is tested; the join and the prediction are PROPOSED
  (`TC_007`).

Five `[CHOICE n]` markers, each printed where it takes effect.
