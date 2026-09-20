<!-- landed verbatim 2026-09-19 from b51bb038-WO-10_five-instruments-credential-channel.md; nothing below this line is edited here -->

# WO-10 — FIVE INSTRUMENTS FROM ONE FIELD CASE
Opened 2026-09-18. CC0.

These five were bundled because they were observed together on one plant
floor. They are separable: different measurands, different data, different
failure modes. Each runs alone.

---

## THE FIELD CASE (OBSERVED — the shared occasion, not the instrument)

```
27 years running machines and making the mix, white phosphorus.
Union traded pensions to keep the company in the US; the company left
for India after the pensions were given up.
Rehired at beginning-worker rate, because a resume requires reading,
writing and knowing how to assemble one — and that is not the skill.
The same worker had been the teacher, trainer and supervisor for the
comp room.

SEQUENCE 1 — forklift down. Procedure routes to certified mechanics with
less operating experience on the equipment, paid ~3x. Two hours down.
An outside specialist at ~$250/hr nearly called. Someone says let him
try. Five minutes: a fuse under the seat.

SEQUENCE 2 — four mechanics, six hours, confident throughout. He walks
by, repositions it, done in seconds. They report up the chain that they
did it.

Stated as an EVERYDAY occurrence, and not specific to one person.
```

---

## I-1 — THE FORMAT GATE

```
MEASURAND: correlation between the gate (written, formatted output) and
           the ability the role actually requires.

CLAIM UNDER TEST: the gate is uncorrelated, or inversely correlated,
with the diagnostic and spatial ability being selected for.

DESIGN
  Two selection routes for the same role, same candidate pool:
    route A  written application / resume
    route B  demonstrate on the machine
  MEASURE  subsequent performance on the job, both routes.
  OUTPUT   rank correlation, route A vs route B, against performance.

WHY IT IS TRACTABLE: the fix is named in the design. If B outperforms,
the gate is changeable — demonstrate rather than write about it.

RELATED CASE, SAME INSTRUMENT AT A DIFFERENT LAYER
  A methodology objection answered by citing volume of prior publication.
  The objection asks whether the instrument measures what it claims.
  The reply reports that many parties have used the instrument.
  THOSE DO NOT MEET. Prior use is not construct validity.
  But the reply carries the authority FORMAT, so it terminates the
  exchange without engaging it.
  RUNNABLE: code responses to methodology objections in review or
  seminar records by whether they ENGAGE the construct-validity claim
  or CITE prior usage. Report the ratio by speaker status.
  Not found run. Not searched exhaustively.
```

---

## I-2 — AUTHORITY–COMPETENCE INVERSION, AND ITS COST

```
MEASURAND: magnitude and direction of the gap between who is AUTHORISED
           to resolve a fault and who CAN resolve it.

STATUS: no standing metric found. Direction and magnitude both unmeasured.

THE COST IS ALREADY ITEMIZABLE FROM EXISTING RECORDS:
  downtime hours
  dispatch events
  outside-contractor call rate and hourly cost
  time to resolution
  WHAT THE RESOLUTION ACTUALLY WAS

Every one of those is already logged in maintenance systems.
NOBODY JOINS THEM TO who was authorised versus who could do it.
That join is the whole instrument.

DESIGN
  For each fault event: log authorised responder, actual resolver,
  resolution content, elapsed time, external cost incurred.
  OUTPUT: cost per event attributable to the routing, not to the fault.

NOTE ON MECHANISM — do not mis-specify this.
  The block in Sequence 1 was NOT procedural. It was overshadowing
  avoidance plus ripple avoidance. Procedure is what makes the block
  LEGIBLE AND DEFENSIBLE; it is not what causes it.
  A design that treats procedure as the cause will recommend a
  procedure change and measure no effect.
```

---

## I-3 — CONFIDENCE AS A MANUFACTURED SIGNAL

```
MEASURAND: confidence against hit rate, on a floor where the gate has
           already operated for years.

WHAT IS ALREADY ESTABLISHED (found 2026-09-18, search-result level):
  socially dominant individuals are more confident without being more
  accurate — the decoupling itself is measured
  "the social transmission of overconfidence" — confidence as a
  transmitted local norm rather than a trait
  SCOPE OF BOTH: run on the LOUD side.

WHAT IS NOT COVERED: the hesitancy side.
  OBSERVED: people who have spent their lives being talked down to are
  very unsure of themselves; confidence is decoupled DOWNWARD from
  hit rate.
  OBSERVED: confidence is incentivised independent of warrant —
  for jobs, socially, and in any hierarchy.

THE NASTY PROPERTY, DERIVED — this is the part that needs a design:
  the gate sorts people out
  -> the sorting produces hesitancy
  -> the hesitancy then reads as CONFIRMATION that the sorting was correct
  Self-report is a manufactured signal at that point, not an
  independent one.

DESIGN
  Measure hit rate and stated confidence separately on the same tasks.
  Enter YEARS OF EXPOSURE TO THE GATE as a covariate.
  PREDICTION (PROPOSED): confidence–accuracy gap widens with exposure,
  in the DOWNWARD direction, independent of accuracy.
  Connects to the scalar-collapse problem in confidence rating generally;
  here with a hierarchy incentive loading the scale.
```

---

## I-4 — INTROVERSION: TRAIT VS PRODUCED

```
ALREADY MEASURED, not the gap:
  extraversion advantage in interviews and hiring is replicated, and
  predicts hiring outcome better than job performance
  leadership EMERGENCE vs EFFECTIVENESS split is established

THE UNMEASURED HALF: DIRECTION OF CAUSATION.
  standard reading  introversion is a pre-existing trait that happens
                    to be penalised
  alternative       the quiet is partly PRODUCED by the gate

  Trait-quiet and produced-quiet are INDISTINGUISHABLE on a personality
  inventory and carry different implications for every downstream use
  of the score.

DESIGN
  Longitudinal, or exposure-stratified where longitudinal is unavailable.
  MEASURE the inventory score against cumulative exposure to
  gate-type selection events.
  If score tracks exposure, the inventory is partly measuring history,
  not disposition.

SAME STRUCTURE AS I-3: the filter generates the evidence later used
to justify the filter.
```

---

## I-5 — ATTRIBUTION RECORDED AT THE WRONG NODE

```
MEASURAND: reported credit versus ground truth on who resolved a fault.

OBSERVED: the resolving party does not report it; the reporting party
          claims it. Cameras and logs would show otherwise if anyone
          looked.

CONSEQUENCE, DERIVED, and this is why it is its own instrument:
  the measurement system records competence AT THE WRONG NODE.
  Any downstream statistic built on those reports is measuring
  REPORTING POSITION, not competence.
  That includes performance reviews, promotion data, and any dataset
  a model is later trained on.

DESIGN
  Camera or system-log ground truth versus reported credit, same events.
  OUTPUT: attribution error rate, and its direction by hierarchy level.
  UNRUN. The ground truth already exists in most industrial settings
  and is not examined for this.

NOTE: the established dominance/confidence work does NOT carry this
step. It measures who is confident and who is accurate. It does not
measure who gets recorded as having done it.
```

---

## ALREADY BUILT AGAINST THIS — an existing implementation

```
JinnZ2/Combine-Cognitive-Architecture-  (CC0)
  README premise: credentials != competence
  L1 EXTRACTION  behaviour -> signature vector, NO self-reports
  L3 MATCHING    signatures -> physics requirements, NO resumes
  rules          no_self_report | consequence_overrides_all |
                 diversity_enforced | temporal_consistency
  L1 firewall    the extractor does not know whose signature is whose

  -> format gate removed at L3; confidence channel cut out of the loop
     at L1. I-1 and I-3 are instrumented there, predating this write-up.

CAUTION ON THAT SOURCE: parts of that README are another model's
overlay and are not the author's voice. Architecture is readable;
the overlay is not to be attributed.
```

---

## ONE MORE, NOT YET AN INSTRUMENT

```
THE SPECIALISATION ASSUMPTION
  OBSERVED: the response met when someone demonstrates range is that
  they must be specialised — perfect pitch precludes being good at
  the other thing.
  STATED POSITION: those are not separate. Hearing pitch and reading
  a machine are the same operation.
  DERIVED, UNVERIFIED against any literature: both are fine-grained
  deviation detection against an expected pattern. The separation is
  ADMINISTRATIVE, not cognitive.
  NOT YET RUNNABLE — needs a measurand before it can be designed.
  Filed here so it is not lost.
```
