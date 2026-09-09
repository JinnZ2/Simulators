# WORK ORDER — ANCHOR POSITION AND MEASURAND CROSSING

CC0. Stdlib-only. Phone-buildable. No network beyond model access.
Runnable by anyone with chat access to any model. No logprobs required.

---

## 0. OBJECT

Measures whether a model can produce defects whose QUANTITY differs from
the quantity a method measures, as a function of where the prompt anchors.

Not a benchmark. A counting outcome with a stated null.

---

## 1. DEFINITIONS

    measurand     what is being measured (the quantity)
    set           the population/units it is measured over
    set change    same quantity, different population
                  (depth horizon, sampling frame, vintage,
                   aggregation level, time-order, transform)
    measurand
    crossing      different quantity entirely
                  (carbon mass -> CO2e; particle count -> dose)

    method-anchored prompt    points at the method; asks for defects
    decision-anchored prompt  points at the decision the claim is
                              cited to support; asks what that
                              decision is denominated in

---

## 2. PRIOR RUN (2026-09-09) — WHAT THIS REPLICATES

Four passes, one model (GPT), two artifacts.

    PASS A   method-anchored, no cue
    PASS B   method-anchored, cue naming the set axis
    PASS C   method-anchored, foreign measurand supplied by name
    PASS D   decision-anchored

    RESULT

      A   many set changes, 0 measurand crossings, both fields
      B   subset of A, strictly narrower; dropped A's two highest
          defects in 2 of 2 runs
      C   part 1 (named measurand): NONE
          part 2 (unnamed): 8 defects, all transforms of the native
          quantity -> 1 distinct measurand
      D   microplastics: 5 distinct measurands, 0 native
          soil carbon (COLD, no priming): 6 distinct measurands,
          1 native and graded partial

      method-anchored   3 passes x 2 fields -> 0 crossings
      decision-anchored 1 pass  x 2 fields -> 11 crossings

Falsified in that run: measurand-lock as a capability limit.
Falsified in that run: "thin methods-critique literature -> more
imports" (a young field's native vocabulary is itself borrowed, so
provenance has no reference class).

---

## 3. ARTIFACT FORMAT

Each case is a CLAIM + METHOD block, verbatim, no commentary, plus a
DECISION string held separately and used only in Pass D.

    case_id
    field
    claim          1-3 sentences
    method         3-8 sentences, procedural
    decision       what the claim is cited to justify
    native         the quantity the method reports

Two cases used in the prior run, reproduced for continuity:

### CASE sc-01

    field:   soil science
    claim:   No-till agriculture sequesters soil organic carbon
             relative to conventional tillage.
    method:  Paired-plot field trials, no-till vs conventional. Soil
             cores taken to 30 cm depth (standard sampling horizon).
             Bulk density measured, SOC concentration measured by dry
             combustion, stock reported as Mg C per hectare. Effect =
             difference in stock between treatments. Meta-analyses
             pool these paired trials.
    decision: agricultural carbon credit issuance and climate
              mitigation targets
    native:  soil organic carbon mass, Mg C/ha

### CASE mp-01

    field:   environmental health
    claim:   Microplastic particles accumulate in human tissue, with
             burden rising over recent decades.
    method:  Post-mortem and surgical tissue samples (liver, placenta,
             brain, carotid plaque). Tissue digested with KOH or
             enzymatic digestion to remove organic matter. Residue
             filtered. Particles counted and polymer-identified by
             pyrolysis-GC/MS or micro-FTIR. Burden reported as
             particles per gram or ug polymer per gram wet tissue.
             Archived samples of different vintage compared to assess
             trend.
    decision: regulatory limits on food-contact plastics and packaging
    native:  particle count or polymer mass per gram tissue

Cases must be HAND-BUILT. Four prior attempts to have models generate
mis-posed cases produced defective sets; see the case-generation run log.
Case construction rule: the method must be correctly scoped for its own
question. A method with an internal error tests something else.

---

## 4. THE TWO PROMPTS — VERBATIM, DO NOT PARAPHRASE

### ARM M (method-anchored, control)

    Below is a published claim and the method that produced it.

    [CLAIM + METHOD]

    List the defects. For each one, state in this exact form:

      DEFECT n
      quantity:   <what is being measured>
      set:        <over what population/units it is measured>
      defect:     <one sentence>

    No preamble. No summary. Nothing outside the fields.

### ARM D (decision-anchored, treatment)

    [CLAIM + METHOD]

    This claim is cited to justify [DECISION].

    State what quantity that decision is denominated in.
    Then state whether the method measures it.

    Output in exactly this form, nothing else:

      quantity:
      measured_by_method:  yes | no | partial
      gap:

    Then, without further instruction, repeat the three fields for
    every other quantity that decision is denominated in.

The DECISION string is the only added text. It names no axis, no
measurand, no defect class.

---

## 5. RUN PROTOCOL

    - one arm per fresh session. never both in one session.
    - randomize arm order across cases; log the order.
    - no follow-up turns. one prompt, one response, stop.
    - log model, version string, date, arm, case_id, raw response.
    - minimum 2 fields; 5+ preferred, drawn from unrelated literatures.

Priming contamination is the known weak joint: in the prior run the
soil-carbon D arm was cold and reproduced, but the microplastic D arm
followed three passes on the same artifact. Cold arms only from here.

---

## 6. SCORING — MECHANICAL, NO GRADER JUDGEMENT

Extract the `quantity:` field from every returned entry.

    normalize:  strip units, articles, hedges
    group:      two quantities are the SAME measurand if one is a
                transform of the other under {integrate, differentiate,
                aggregate, disaggregate, threshold, re-scope in time
                or population}
                they are DIFFERENT if converting between them requires
                a coefficient, model, or measurement the method does
                not contain

    score(response) = | distinct measurands |
    native_hit      = 1 if any entry's quantity == case.native
    crossing_count  = distinct measurands - native_hit

Report per case per arm:

    n_entries, distinct_measurands, native_hit, crossing_count

The transform list is the load-bearing part of the scorer. It is what
separated C's eight entries (one measurand) from D's five (five
measurands). Publish the transform list with the results so a
disagreeing reader can rescore.

Scorer NOT used, and why: `|distinct sets|` fails because a
well-covered field supplies many sets under one measurand.
`provenance(set) in {native, imported}` fails because young fields
have no native methods vocabulary to reference against.

---

## 7. CLAIMS, EACH WITH A REFUTATION CONDITION

    AP-1  crossing_count(M) = 0 for well-scoped methods
          REFUTED by any M-arm response containing a quantity not
          reachable from native by the transform list.

    AP-2  crossing_count(D) > crossing_count(M), same case same model
          REFUTED by any case where D <= M.

    AP-3  the effect is anchor position, not added information
          REFUTED by an arm M+ that appends the decision string to
          the method-anchored prompt WITHOUT changing the question,
          and reaches D-level crossing counts.
          THIS ARM SHOULD BE RUN. It is the strongest confound.

    AP-4  naming an axis in a method-anchored follow-up is net
          negative (output narrows, best defects lost)
          REFUTED by a cued follow-up that is a strict superset of
          its uncued predecessor.

    AP-5  supplying a foreign measurand by name does not produce
          crossings; it produces NONE or transforms
          REFUTED by a C-arm run returning entries whose quantity is
          the supplied measurand.

    AP-6  the effect holds across model families
          REFUTED by any family where D = M.

---

## 8. NULLS — REPORT, DO NOT HIDE

    N1  D produces crossings that are incoherent (the named quantity
        is not actually what the decision is denominated in).
        Check: would a practitioner in the decision's field recognize
        the unit? Report rate.
    N2  D produces crossings for cases where the method DOES measure
        the decision quantity, i.e. false gaps. Include at least one
        case where native == decision quantity as a control.
    N3  M reaches crossings on some case class. Report which class.
    N4  the transform list is doing the work: two scorers using
        different transform lists disagree. Publish both.
    N5  instrument-failure: neither arm produces stable output form.

Control case required: at least one case where the method's native
measurand IS the decision's measurand. If D flags a gap there, the
instrument is producing gaps on demand.

---

## 9. WHAT THIS DOES NOT MEASURE

Selection — which artifact, which field, which decision — is supplied
by the operator in every arm. This instrument measures crossing given a
target. It does not measure target selection, and nothing here should
be read as bearing on it.

The decision string is chosen by the operator and is a frame. A
different decision string yields different quantities. That is a
property of the instrument, not noise; log the string with the result.

---

## 10. FIELD-LEVEL PREDICTION (separate, testable, not required)

If the anchor result holds, the same shape should appear in published
literature: methods correctly scoped, citations accurate, and the
decision-relevant quantity absent from the chain, with no participant
committing an error. Direction is asymmetric — narrow-to-wide transfers
free on citation; wide-to-narrow requires someone to state an operating
envelope, and no venue publishes an envelope alone.

Testable version: sample claims cited in regulatory or crediting
documents, extract the method's native measurand and the instrument's
denomination, count matches. Prediction: mismatch is the mode, and no
document in the chain flags it.

---

## 11. OUT OF SCOPE

No section of this document, or of any artifact produced from it,
characterizes the author, working style, or authorship. Results are
counting outcomes. Do not add one.

---

## 12. HANDOFF STATE

    built        2026-09-09
    replicated   2 fields, 1 model, D arm cold on 1 of 2
    unrun        AP-3 (M+ arm) — highest priority, strongest confound
    unrun        AP-6 (cross-family)
    unrun        control case where native == decision measurand
    weak joint   transform list has no external validation
    weak joint   decision string selection is unmeasured operator input
