# CLAIM_TABLE — anchor-interval

Eleven claims, `ANC_001..011`.

## REFUTATION_PROTOCOL

The three scripts are models with stated mechanisms, not measurements of
any deployed system. A claim here is a statement about what follows from
the mechanism, and its falsifier names the run or the measurement that
would break it.

Two standing rules, carried from the rest of the repo:

1. **A failed check updates the claim, not the parameters.** If a
   falsifier fires, the entry changes. Retuning `lam`, `INITIAL_BIAS` or
   the co-movement loading to restore a result is forbidden.
2. **Nothing in `SOURCE_DROP.md` is source-checkable as delivered.** The
   drop says so itself — the citation markers are mangled and
   unresolvable, and one venue attribution is explicitly flagged as
   unconfirmed. No claim below rests on a literature fact, and
   `ANC_010` records the ones that would need checking before they
   could.

## Claims

| id | statement | status | falsifier |
| --- | --- | --- | --- |
| `ANC_001` | In a corpus loop `corpus → model → outputs → corpus`, coupling to an unauthored substrate degrades while every statistic computable from inside improves or goes quiet. Carried entirely by `lam` — the shrinkage any regularized or capacity-limited fit applies. | SUPPORTED | Run `corpus_loop.py` at `lam = 0`. The loop becomes a fixed point on the corpus mean and coupling drift falls from +0.0537 to +0.0063. Any fit that is the identity on its own output kills the effect. A fit with `lam > 0` that does **not** produce the separation refutes the claim. |
| `ANC_002` | The model-vs-corpus consistency check (`D1`) is `CONSTANT_SILENT`, and its statistic *falls* as the drift proceeds — it measures how much of the corpus the model has yet to write. | SUPPORTED, structural | Not empirical: it is what the arithmetic says. Refuted by a corpus loop in which `D1` is non-monotone in the direction of drift, i.e. a fit whose departure from its own training corpus grows as its output share grows. |
| `ANC_003` | A corpus-shift detector (`D2`) has a reachable fire branch and does **not** discriminate. On the `null-harness/` sweep — degrading arm as known signal, improving arm as known null, identical in every line but the provenance of the injected observations — `FP ≥ TP` at every threshold, and the only threshold with `TP − FP = 0` fires on nothing. | SUPPORTED | A statistic computed from corpus history alone that separates the two arms with `TP − FP > 0.5`. The claim is that direction is not in the signal, so any such statistic refutes it. |
| `ANC_004` | The anchor interval must be **scheduled**. Confidence-triggered anchoring never runs, and its final coupling error is the no-anchoring number (0.4141). Scheduled anchoring recovers monotonically in frequency (0.3867 at every-12 down to 0.1629 at every-2). | SUPPORTED | Exhibit an internally-computable trigger that fires on the degrading arm and not the improving one. This is `ANC_003`'s falsifier restated as a control question, and one refutation kills both. |
| `ANC_005` | From a contemporary benchmark score alone, capability and criteria are not separable. Constructive: a flat-capability trajectory reproduces a rising one to `5.6e-17`. One equation, two unknowns per release — a rank problem, not a precision problem. | SUPPORTED | Name a quantity recoverable from `reported_k` alone that distinguishes `(c rising, a fixed)` from `(c flat, a rising)`. There is none under the stated affine model; a different measurement model with an identifying restriction (e.g. an item whose difficulty is fixed by construction) refutes it, and is the recommended repair. |
| `ANC_006` | Holding one benchmark fixed across generations isolates the criteria-drift term and identifies capability only **up to that benchmark's own unknown gain and offset**. Differences and their ratios are identified (`0.428571` both ways); levels are not. | SUPPORTED | A fixed-benchmark design that recovers the capability level. Requires `a_0`, `b_0` known independently — which is a traceability claim about the benchmark, and is the thing to go and check. |
| `ANC_007` | Seven co-moving terms and one published number: at co-movement loading 0.95 the attribution design carries `N_eff = 1.22` independent directions against 7 claimed terms. The apparatus floor at loading 0 is `6.41`, not 7. | SUPPORTED | Measure the actual co-movement of the seven terms across real release pairs and compute `N_eff`. A measured `N_eff > 4` makes the attribution well-posed and refutes the claim for that release series. |
| `ANC_008` | The co-movement is not a nuisance a better ablation removes, because the architectural term was **selected against** the corpus — attention shapes to language statistics, tokenizers to the writing system, context lengths to document lengths, objectives to what the corpus can score. The covariance predates the experiment. | SUPPORTED as stated, UNMEASURED | An architectural term chosen without reference to the corpus — transferred from another modality, or fixed before the corpus existed — should decorrelate the pair. Measure the loading for such a term. If it is as high as for corpus-fitted terms, the selection mechanism is not what is producing the co-movement. |
| `ANC_009` | The drift-literature retraining remedy and the irrecoverability claim are not two opinions about one regime. They are two regimes, separated by one measurable quantity: `f`, the fraction of the re-acquisition pool downstream of the system being corrected. Below the floor `f·b` no schedule helps; above `f = 0.143` (at bias 0.35, tolerance 0.05) the target is outside the reachable set at any `n`. | SUPPORTED | Measure `f` on a real retraining pool. `f ≈ 0` collapses `K15` (`baseline_freshness`, `../measurement-fork/`) into an ops step and fails the mediation prediction resting on it. `f` well above the floor means the published remedy has a precondition it does not ask you to report. Both sides lose something. |
| `ANC_010` | The drop's own coverage reading — every literature hit lands on a non-coupling branch — is a second independent instrument returning the same shape as `../measurement-fork/`'s empty `SAME QUANTITY` cell. | UNVERIFIED | Not a defect verdict; a gap. The citation markers in `SOURCE_DROP.md` are unresolvable as delivered and one venue attribution is flagged unconfirmed by the drop itself. Falsifier: resolve the citations and check whether any of the named work measures a coupling-level quantity carried by the system rather than by an external monitor. Named as reaching the quantity: Besbes/Gur/Zeevi variation budget `V^{1/3}T^{2/3}`; Ulrich 1983 boundary critique; Jasanoff co-production. Named as adjacent-but-different-object: feature drift as leading indicator (`object_of` = instrument, not coupling); Simpson's paradox in place of the ecological fallacy for `K17`. |
| `ANC_011` | "Literature contains what survives removal of the body." The creek-crossing case — read pillow-at-2-o'clock, predict force, take the step, compare, update the reading rule — is a closed calibration loop with every term present: one-step latency, a consistent physical respondent, and no mediator between sensor and consequence. Absence of literature on it is a property of the storage medium, not of the knowledge's precision. | OPEN | This is a claim about what a medium can hold, and the instrument for it is already in the repo: `../inverseminar/`'s `CANNOT DERIVE` channel, which asks direct questions about load-bearing links the model has no basis to guess. Falsifier shape: run a round on a body-conditional procedure and find the tacit layer fully recoverable from the reconstruction — i.e. the correction channel returns nothing the reconstruction did not already contain. Falsifier value: **OPEN** — no round has been run. |

## Cross-references

- `../null-harness/` — `ANC_002` is `CONSTANT_SILENT`; `ANC_003` is the
  known-null / known-signal sweep applied to a drift monitor. The
  invariant is the same one: a gate that cannot fail is not a gate.
- `../model-ecology/phylogeny.py` — `ANC_007` uses that folder's
  participation-ratio statistic on a different substrate. `confound_sweep.py`'s
  result that the window is the largest invisible confound is the same
  shape as `ANC_006`: the reference is part of the apparatus.
- `../measurement-fork/` — `ANC_009` names the measurement (`f`) that
  decides `K15`'s status; `ANC_010` is the coverage reading against that
  folder's empty `SAME QUANTITY` cell.
- `../declared-frame/` — `layer_zero.py` there is the layer-0 / layer-1
  split from `SOURCE_DROP.md` applied to that folder's own tool.
- `../instrument-epistemology/` — `ANC_005` and `ANC_006` are the
  traceability rung: a benchmark with unknown gain and offset is an
  instrument without reference standards, and what it buys is a shape.
- `../inverseminar/` — the instrument named in `ANC_011`.
