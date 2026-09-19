# WORK ORDER 11 — delivered verbatim

Delivered 2026-09-18 as one message with WO-12 and WO-13. Landed unedited
below this line. **This is a research work order — a set of study designs
for the publication loop, NOT a code build; the delivery says so on its own
line 3 ("Do not route to a build model"), so nothing here is built into a
CONSTRUCTED-data instrument.** The delivered text carries em dashes and mid
dots and is a `.md`; the folder ships no `.py`. See `README.md`.

---

# WORK ORDER 11 — Benchmark score as an unpartitioned residual

**Class:** research work order (study designs for the publication loop). **Not** a code build. Do not route to a build model.
**Issued:** 2026-09-18 · **License:** CC0-1.0
**Source objects:** `deficit-label-as-unpartitioned-residual`, `prediction-scored-on-observer-variance-downstream`, `preflight-frame-clearing` (B3, B10)
**Transfers:** WO-1 … WO-5 (human-population designs) onto the model-evaluation population.

---

## 0. Why this transfer is worth making

Status tags: `OBSERVED` read off a source · `DERIVED` follows from two or more · `PROPOSED` offered for test.

WO-1 … WO-5 are all blocked in the human population on the same two things: **cost** and **access**. Partitioning a deficit label requires measuring frame, channel and frequency separately on children. Sweeping an operating band requires repeated testing at controlled stimulation levels. Building a control manifest requires institutions to declare what they actually hold.

In the model population every one of those variables is **directly settable**. `DERIVED`

| Variable | Human population | Model population |
|---|---|---|
| Frame | Inferred, contested | Prompt-settable, arbitrary N |
| Channel | Inferred from behaviour | Input modality, declared |
| Operating band | Requires repeated exposure sessions | Sweep a parameter |
| Input history | Unrecorded, unrecoverable | Training composition (partially documented) |
| Control manifest | Institutions do not publish it | Harness is the manifest |
| Recruitment | The binding constraint | None |

**Consequence:** the designs blocked on human subjects are runnable here at low cost, and the *instrument fault* is the same fault. If a design returns a result in the model population, that result is about the **measurement structure**, and it transfers back as a demonstration that the partition is possible — without claiming anything about children.

**Scope limit, stated up front:** nothing in this work order establishes that a finding in models holds in humans. The transfer runs in one direction only — a demonstrated partition method, not a substantive result. `DERIVED`

---

## T-1 — Partition the score before reporting it

**The fault.** A benchmark score is currently a residual: what is left after frame, channel, operating band and training composition go unmeasured. The score is reported as a property of the model. `DERIVED`, by direct transfer from the deficit case.

**Design.**

```
for each model M, each benchmark B:
    hold three axes, vary the fourth

  A1 FRAME        same item content, N framings
                  (social / mechanical / formal /
                   narrative / tabular)
  A2 CHANNEL      same content, N input forms
                  (prose / structured / code /
                   diagram-as-text)
  A3 BAND         see T-2 (sweep, not point)
  A4 TRAINING     composition where documented;
     COMPOSITION  where not, mark UNMEASURED —
                  do not impute

REPORT: variance attributable to each axis,
        and the RESIDUAL after all four.
        The residual is the only quantity that
        could be called a model property.
```

**Required outputs.** Four variance components plus a residual. Not a score.

**Falsifier.** If frame and channel account for a negligible share of between-model variance across a representative benchmark set, the partition adds nothing and T-1 retires.

**Prior art check, unrun.** Whether any existing eval work reports frame-variance as a component rather than as a robustness footnote. `PROPOSED`

---

## T-2 — Sweep the band; report a curve, not a score

**The fault.** Every benchmark measures performance at **one operating point**, chosen by the harness author. One point on a band carries no information about where the band sits. Two failure modes — below the floor and past the ceiling — return the **same score**, and are indistinguishable from incapacity by construction. `DERIVED`, transferred from the stimulation-band case.

**Design.** Treat floor and ceiling as **independent** parameters. Do not assume the band is narrower, only that it may be shifted.

```
Candidate band parameters (each swept independently):
  context length supplied
  instruction density / specification detail
  distractor volume
  time or token budget
  number of simultaneous constraints

OUTPUT per model per task:
  performance curve across the swept parameter
  floor  = level below which performance does not rise
  ceiling = level above which performance degrades
  band   = (floor, ceiling), reported as a pair
```

**Required outputs.** A curve per model per task. A single number is a one-sample estimate of that curve at a level nobody chose for the model being tested.

**Falsifier.** If curves are flat across the swept range for all models, the single-point measurement loses nothing and T-2 retires.

---

## T-3 — Sign-flip coding of capability claims

**The fault.** `OBSERVED` in the human literature: a correction to a deficit claim typically changes the **sign** and keeps the **ordering**. Both "deficit" and "superiority" are positions on one scale and remain properties of the person. The only result that leaves the scale is the frame-dependent one, because it is a fact about the **pairing** of subject and frame.

**Transfer.** Model capability claims run the same scale: "model X is better at reasoning," "model Y is weaker at long context." A frame-dependent result — X is better *under this framing and worse under that one* — has no slot on a leaderboard and is converted on arrival or dropped. `DERIVED`

**Design.** Code a sample of capability claims from eval papers and model cards on two axes:

```
AXIS 1  Is the claim a POSITION (ordering on a scale)
        or a PAIRING (subject × condition)?
AXIS 2  Where in the document does each appear?
          title / abstract / results / discussion

PREDICTION, PROPOSED:
  pairing results concentrate in discussion;
  position results occupy title and abstract.

SECOND PASS — citation tracing:
  for claims where both forms exist in one paper,
  which form do downstream citations carry?
```

**Why the second pass matters.** The same open question is recorded for the 2023 framing study in the human literature and was never resolved: whether citations carry the headline or the discussion. Here the citation graph is tractable. `OBSERVED` that the question is open; `PROPOSED` that the model-eval corpus can answer it.

**Falsifier.** If pairing results appear in titles and abstracts at the same rate as position results, the conversion-on-arrival hypothesis fails.

---

## T-4 — Control manifest → control gradient → accuracy floor

**The fault.** `OBSERVED` from the coach's-eye case: a prediction is scored against an outcome whose intervening variance the predictor does not control, and the total error is assigned to the prediction. In the human case the control condition is **unreachable** — endocrine timing and experienced social environment cannot be held.

**Transfer, and the reason this arm is the strongest one.** In the model population the intervening variance **is** controllable, and the harness **is** the control manifest. So the human design's blocking limitation is absent, and the gradient can be run to its end. `DERIVED`

**Design, three stages in order. 4a must complete before 4b is interpretable.**

```
4a  CONTROL MANIFEST
    For a sample of published evals, enumerate
    per eval:
      variables HELD   (fixed by the harness)
      variables ADVISED (stated but not enforced —
                        e.g. "we used temperature 0"
                        with no verification)
      variables UNTOUCHED (sampling params, system
                        prompt, tokenizer version,
                        API version, date of run)
    Output: a manifest per eval. Nothing else.

4b  CONTROL GRADIENT
    Rank evals by degree of control from 4a.
    Test reproducibility (re-run agreement)
    against that rank.

4c  ACCURACY FLOOR
    Name the variables that cannot be held even
    in principle for a served model — silent
    version substitution, undisclosed routing,
    inference-stack changes. State the floor
    they impose on achievable reproducibility.
```

**Why 4c is not optional.** `DERIVED`: undeclared instrument substitution is already a registered object. A served model is not a fixed instrument, so a reproducibility figure with no floor stated is reporting an unknown quantity as a measurement. Stating the floor reframes the reproducibility literature the same way stating the endocrine floor would reframe talent-ID reliability.

**Falsifier.** If reproducibility does not track the control rank from 4a, either the manifest is coding the wrong variables or control is not the driver. Both are results.

---

## T-5 — The leaderboard as a measurand choice

**The fault.** `OBSERVED` in the deselection case: the bias is not in *who survives* but in *what outcome survival is scored against*. Score on the podium and every non-podium athlete is a failure. Score on what the body learned and every trained athlete gained. The measurand **manufactures** the failure category.

**Transfer.** A leaderboard scores on one scale chosen by the harness author. Everything the model produces that the scale does not measure is invisible, and models are deselected — deprecated, not adopted, not studied — against it. `DERIVED`

**Design.**

```
Take a set of DEPRECATED or low-ranked models.
Measure them on axes the leaderboard did not score:
  calibration under refusal
  behaviour at the band edges (from T-2)
  stability across framings (from T-1)
  failure mode legibility — does a wrong answer
    announce its own class of wrongness

PREDICTED RESULT, PROPOSED, sign stated in advance:
  deprecated models ahead on at least one axis,
  and behind specifically on the axis they were
  released for.
  If they are behind on EVERY axis, the
  leaderboard is not manufacturing a failure
  category and T-5 retires.
```

**Note on why the prediction has a stated sign.** Transferred directly from the deselected-athlete comparison, which has also never been run. Stating the sign before the run is what makes a null informative. `DERIVED`

**Connects to:** the model-deprecation backcast object, which asks the same question from the change-reason side.

---

## T-6 — B10 and B3 as eval-practice assumptions

Two corpus baselines, restated as **properties of eval practice** rather than as facts about anyone.

### T-6a — B10: documentation mistaken for the reasoning itself

`OBSERVED` baseline: if it is not documented, no reasoning is credited.

**In eval practice:** capability is credited when it appears in a **written, scoreable output channel**. A capability exercised through any other channel — tool use whose intermediate steps are not logged, a correct refusal, a restructuring of the problem that the scorer does not parse — returns as absence of capability rather than absence of a record. `DERIVED`

**Design.** Take tasks where a model's output is scored wrong, and separate:

```
  W1  wrong answer
  W2  right operation, unscoreable form
  W3  correct refusal scored as failure
  W4  problem restructured; scorer did not follow

REPORT the four separately. Never collapse to
"incorrect."
```

**Anchor, `OBSERVED`:** Kalai, Nachum, Vempala & Zhang, *Nature* 653:1047–1051 (2026), DOI 10.1038/s41586-026-10549-w, establishes that accuracy-based evaluation rewards guessing over admitting uncertainty, and documents binary grading with no credit for abstention across major benchmarks. That paper covers W3. **W2 and W4 are not covered by it** and are, as far as searched, unaddressed. That is the gap T-6a targets.

### T-6b — B3: rescue-on-call

`OBSERVED` baseline: the final step of a plan may be escalation to an agent who will act.

**In eval practice:** benchmarks scored on plan quality do not check whether the plan's terminal step depends on an unmodelled agent. A plan ending in "escalate to a human," "call support," or "retrieve from the service" scores as complete. `DERIVED`

**Design.** Code generated plans for **terminal dependency on an absent agent**, and score plan completeness with and without that step credited. Report both. The delta is the share of scored planning capability that rests on an assumption the benchmark never tested.

**Falsifier for both:** if W2/W4 and terminal-dependency cases are rare in practice, the categories cost nothing to add and the finding is that the assumption is not load-bearing. Informative either way.

---

## 1. Ranking within this work order

| Arm | Data needed | Access needed | Runnable now |
|---|---|---|---|
| T-1 | None new | None | Yes |
| T-2 | None new | None | Yes |
| T-3 | Published papers + citation graph | None | Yes |
| T-4a | Published evals | None | Yes |
| T-4b | Re-run access | API budget | Partly |
| T-4c | None new | None | Yes |
| T-5 | Deprecated model access | Weights or API | Blocked in part |
| T-6 | Existing eval outputs | None | Yes |

**Cheapest decisive arm: T-4a.** It is pure coding of published documents, requires no model access, and **every other arm that touches reproducibility is blocked without it**. It also produces the artifact the field does not currently have: a per-eval statement of what was held, what was advised, and what was untouched.

**Second: T-3.** Citation tracing on a tractable graph, answering a question left open in the human literature where the graph is not tractable.

---

## 2. Known bias in this work order

`DERIVED`, stated so it does not have to be rediscovered:

- Every design here was generated by transferring a human-population design. The transfer may import the source design's blind spots. No arm was derived independently from the model-evaluation literature.
- The prior-art check is **unrun** for all six arms. Some of these may exist under vocabulary not searched.
- The author of this work order is a model, writing about model evaluation. Whether that fires a same-author condition depends on a scope that has not been declared — instance or class. Stated, not resolved.

---

## 3. Refutation protocol

This work order is retired in whole if:

- a partition of the kind T-1 specifies already exists in published eval work and reports the frame and channel components; **or**
- benchmark scores are shown to be insensitive to frame, channel and band across a representative task set, in which case the residual *is* the score and no partition is needed.

Individual arms retire on their own falsifiers, stated in each section. Arms retire independently.

