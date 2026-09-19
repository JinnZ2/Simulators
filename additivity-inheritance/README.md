# additivity-inheritance

WO-9 delivered verbatim (`WORK_ORDER.md`) and built to: trace the
additivity assumption forward from the Fisher synthesis. **These are OPEN
QUESTIONS instrumented, not a critique of statistics** -- the tools are
not in dispute, their inherited assumptions are the object. Anyone who
converts this into an argument against statistical genetics has mis-read
the order.

```
  correlation, regression, chi-squared, ANOVA were developed for
  heritable-difference questions, then handed to fields with no
  connection to them -- carrying design choices about what a
  distribution is, what an outlier is, what between-group variance means.

  the merge: Fisher models genes as gas molecules under thermodynamics,
  letting continuous variation, selection and Mendelian inheritance
  coexist. Modern statistics runs on that synthesis. Was information
  left out?
```

CC0. Python 3.9+, stdlib only, no network, phone-buildable.
`additivity_inheritance.py` renders on bare invocation, prints its
choices with `--choices`, and refuses `--selftest` (exit 2);
`python3 test_additivity.py` runs the checks and prints their count.
**No primary source is read** -- not Mendel 1865, not Naudin 1862, not
Fisher 1918 -- and every corpus is CONSTRUCTED; the history is a starting
map, not a citation (`AI_006`).

---

## WHAT RUNS

| item | computes | scope |
|---|---|---|
| R1 | the four-code distribution (stated / stated+tested / present+unstated / relaxed) by field and decade, and the C-share against declared field distance | CONSTRUCTED corpus built to carry the prediction; a known-answer run on the coder |
| R2 | how many non-additive phenomena had to fight the frame to re-enter | CONSTRUCTED records |
| R3 | prior art at the merge specifically | NOT_RUN -- unsearched, egress-blocked; if it exists WO-9 becomes a pointer |
| R4 | a citation trace (BFS over citation edges) against a structural trace (adds inheritance edges), on the eugenics/Mendel case | CONSTRUCTED graph to the order's description; a known-answer instance |
| decomposition | the interaction SS a balanced-2x2 additive model assigns to its residual | exact arithmetic |

---

## THE TWO RESULTS THAT SURVIVE THE CONSTRUCTION

- **R4 is the portable finding.** The order's methodological result is
  that citation tracing cannot detect a precondition carried by a shared
  structural inheritance -- eugenics predates Mendel's rediscovery, and
  Galton had to be told of Mendel in 1900, so the precondition reached
  both camps through the fork they inherited, not through a citation. The
  graph reproduces it exactly: the citation trace does NOT reach the
  precondition, the structural trace does, so it is a false negative. And
  the trace is not `CONSTANT_SILENT` -- when the precondition is cited,
  both traces reach it (`AI_004`).
- **The additive decomposition loses a real interaction to the residual,
  exactly.** On a balanced 2x2 with cell means `[[10, 12], [12, 20]]`,
  `SS_interaction = (a - b - c + d)^2 / 4 = 9`, and a main-effects-only
  model has that 9 AS its residual. Candidate 1 of the order -- "anything
  non-additive survives only as nuisance" -- is arithmetic on a design
  this small: the interaction is not lost to a modelling choice downstream,
  it is assigned to noise by the decomposition itself (`AI_005`).
  `interaction_ss` is registered in `tools/known_answer.py`.

The load-bearing lineage claim (variance partitioning descends from the
merge; heritability inherits additivity) is CARRIED and not verified here;
the order says test it first, and if it is false WO-9 collapses cheaply.

Four `[CHOICE n]` markers, each printed where it takes effect.
