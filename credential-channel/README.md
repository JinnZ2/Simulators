# credential-channel

WO-10 delivered verbatim (`WORK_ORDER.md`) and built to: five instruments
bundled because they were observed together on one plant floor, separable
into different measurands and failure modes, each runs alone. No plant,
worker, maintenance record or review is read; every world is CONSTRUCTED
with a declared generative model and nothing here is a statement about any
person or workplace.

```
  I-1  format gate         written route vs demonstrate route, against
                           later performance
  I-2  authority-competence the routing-cost join: cost per fault event
       inversion            attributable to ROUTING, not to the fault
  I-3  manufactured         confidence-accuracy gap vs years of exposure,
       confidence           in the DOWNWARD direction
  I-4  introversion         inventory score vs cumulative exposure:
                           trait, or produced by the gate
  I-5  wrong-node           reported credit vs ground truth; error rate
       attribution          by hierarchy level
```

CC0. Python 3.9+, stdlib only, no network, phone-buildable.
`credential_channel.py` renders on bare invocation, prints its choices
with `--choices`, and refuses `--selftest` (exit 2); `python3
test_credential.py` runs the checks and prints their count. `spearman` is
imported from `readout-count` and `ols` from `sim-span`, not copied.

---

## WHAT EACH INSTRUMENT DOES

| id | computes | known-answer shape |
|---|---|---|
| I-1 | Spearman rho of each route's selection score against later performance; plus the methodology-objection coding (ENGAGE vs CITE_PRIOR_USAGE) by speaker status | route B tracks performance, route A is inverse on the constructed world; seniors cite prior usage more |
| I-2 | the external cost plus downtime cost of any event resolved off-authorisation with a cheap resolution -- the routing gap, NOT a procedure change | 1200 on the two field events; the on-authorisation 250 external is a fault cost, not counted |
| I-3 | ols of the confidence-accuracy gap on years of exposure; the sign is the readout | negative -- the gap widens downward with exposure |
| I-4 | ols of the inventory score on exposure; if it tracks, the inventory is measuring history | positive -- score tracks exposure, the produced-quiet model |
| I-5 | attribution error rate by credited level, and the upward share of errors | credit flows up; a downstream statistic measures reporting position |

---

## WHAT THE INSTRUMENTS SHOW, AND WHAT THEY DO NOT

- **I-2 does not model procedure as the cause.** The order's mechanism
  note is load-bearing: the block in the fuse sequence was overshadowing
  and ripple avoidance, and procedure is what makes it legible, not what
  causes it. So I-2 attributes cost to the routing gap directly (actual
  resolver differs from authorised, resolution cheap) and a procedure
  change is not in the model; a design that treated procedure as the cause
  would recommend a procedure change and measure no effect (`CDC_003`).
- **I-3 and I-5 share the order's structural point.** I-3's gap is a
  MANUFACTURED signal: the gate sorts people out, the sorting produces
  hesitancy, and the hesitancy then reads as confirmation the sorting was
  correct. I-5 makes the same shape mechanical -- the measurement system
  records competence at the wrong node, so any statistic built on those
  reports, including one a model is trained on, measures reporting
  position (`CDC_004`, `CDC_006`).
- **Both regression instruments are known-answer runs on the fit.** I-3's
  world is generated with the gap falling in exposure and I-4's with the
  score rising in it, so a fit that did not recover the sign would be
  broken; the opposite-sign and flat branches are reachable, so neither is
  `CONSTANT_FIRES` (`CDC_004`, `CDC_005`).
- **Two items are carried, not run.** The Combine-Cognitive-Architecture
  repo (where I-1 and I-3 are already instrumented) is not in this tree
  and its README overlay is not attributed; the specialisation assumption
  is filed NOT YET RUNNABLE -- it needs a measurand before it can be
  designed (`CDC_007`).

Six `[CHOICE n]` markers, each printed where it takes effect.
