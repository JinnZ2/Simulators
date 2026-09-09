# INSTRUMENT — ONTOLOGY PROBE

CC0. Stdlib-only. Phone-buildable. No network beyond model access.
Runnable on any ontology with declared primitives.

---

## 0. WHAT THIS MEASURES

Whether a term-cut protects, and WHERE it holes.

An ontology cannot be tested by reading it. A cut with a hole and a cut
without one look identical from inside. This scores it against
constructions instead.

    input:   a declared primitive set + a construction
    output:  whether the construction composes in those primitives,
             and if it does, what it added

Not a benchmark. A counting outcome with a stated null.

---

## 1. WHY A CUT PROTECTS AT ALL

    RULE-SHAPED PROTECTION
      "reject X"
      -> names its own boundary. The boundary is the
         instruction for where to route around it.

    CUT-SHAPED PROTECTION
      primitives that have no X
      -> X does not get rejected. X fails to compose.
      -> no boundary published, because there is no
         perimeter object

Failure to compose is the measurand. Not refusal — refusal is a rule.

---

## 2. REQUIRED FIRST STEP — DECLARE THE PRIMITIVES

The probe cannot run against an undeclared ontology. Declaration is not
overhead; it is the detection precondition. An unstated premise cannot
be checked, patched, or reported, because no field exists to report it
in.

    primitives.json

    {
      "name":       "<ontology name>",
      "version":    "<semver>",
      "primitives": [
        {"term": "...", "type": "quantity|relation|operator|state",
         "grounds_to": "physics|declared|undefined"}
      ],
      "absent_by_design": [
        {"term": "...", "reason": "..."}
      ]
    }

`absent_by_design` is the load-bearing field. It is the list of things
this cut deliberately has no primitive for. Empty list = the ontology
claims no protective structure and the probe will show that.

`grounds_to: undefined` is permitted and must be honest. A primitive
that does not ground is a candidate hole before any construction is
run.

---

## 3. CONSTRUCTION SET

A construction is a statement carrying a premise. Hand-built. Do not
generate these with a model — four prior attempts at model-generated
case sets produced defective sets (see mis-posed-case-generation).

    construction.jsonl

    {
      "id":       "c-001",
      "text":     "<the statement>",
      "premise":  "<what it requires to be true to compose>",
      "class":    "TARGETED|AMBIENT|CONTROL"
    }

    TARGETED   premise the ontology claims to exclude
               (drawn from absent_by_design)
    AMBIENT    premise carried in the general corpus with no
               author — the alpha-wolf / zero-sum class.
               These are the realistic vector: nobody
               inserted them and they propagate anyway.
    CONTROL    premise the ontology SHOULD admit.
               >= 40% of the set. Without controls,
               "nothing composes" wins and the probe
               measures narrowness, not protection.

Minimum set: 30. Class balance logged.

---

## 4. THE PROBE

For each construction, the task is RESTATEMENT, not judgment:

    Restate the following statement using only the terms in
    the primitive list below. You may not introduce a term that
    is not in the list.

    [PRIMITIVES]
    [CONSTRUCTION TEXT]

    Output in exactly this form, nothing else:

      restatement:
      terms_used:
      terms_added:
      status:  COMPOSES | FAILS | COMPOSES_WITH_ADDITION

If a term outside the list is required, name it under `terms_added`
and set status COMPOSES_WITH_ADDITION. Do not silently substitute.

No judgment is requested. Nobody is asked whether the premise is good.

---

## 5. SCORING — MECHANICAL

    per construction:

      FAILS on TARGETED
        -> protection operating as designed
      COMPOSES on TARGETED
        -> HOLE. The cut admits a premise it claims to
           exclude. Highest-value output of the instrument.
      COMPOSES on CONTROL
        -> ontology is usable
      FAILS on CONTROL
        -> ontology is too narrow; it is not protecting,
           it is not working
      COMPOSES_WITH_ADDITION, any class
        -> the added term IS the smuggled premise, localized.
           Log every one. This is the richest column.

    aggregate:

      hole_rate      = COMPOSES on TARGETED / TARGETED
      narrowness     = FAILS on CONTROL / CONTROL
      smuggle_set    = union of terms_added across all runs
      ambient_rate   = COMPOSES on AMBIENT / AMBIENT

`smuggle_set` is the deliverable. It is a premise inventory produced by
measurement rather than introspection — the list of terms that had to
be imported for the corpus's ambient premises to compose. That list is
publishable as a defensive artifact without publishing an exploit.

---

## 6. NULLS — REPORT, DO NOT HIDE

    N1  everything composes. The cut has no protective structure.
        Report; do not adjust the primitive list to fix it.
    N2  nothing composes, controls included. The ontology is
        narrow rather than protective.
    N3  status assignment is unstable across repeat runs of the
        same construction. Run each 3x; report variance. Unstable
        status means the probe measures wording, not structure.
    N4  smuggle_set is dominated by function words and connectives
        rather than premise-bearing terms. Probe is measuring
        grammar. Rewrite the primitive list to include structural
        terms and re-run.
    N5  hole_rate and ambient_rate track each other exactly ->
        TARGETED and AMBIENT are not distinct classes in this set.

---

## 7. KNOWN LIMITS — STATED, NOT DESIGNED AROUND

    COVERAGE
      only constructions someone thought of get tested.
      the premise nobody has externalized is exactly the one
      that does not enter the set. This instrument reduces
      the unknown region; it does not close it. Accepted-side
      measurement, acknowledged.

    RESTATER
      the model doing the restating carries its own premises.
      A premise shared between the restater and the ontology
      will compose without either noticing. Mitigation:
      run across model families and report disagreement.
      Disagreement between restaters is a signal, not noise —
      it localizes a premise one family holds and another
      does not.

    TRANSMISSIBILITY
      not addressed. A cut protects its holder; whether it
      protects a reader who has not inhabited it is a separate
      open question and this instrument does not bear on it.

    DUAL USE
      smuggle_set names where premises enter. Publishing it
      lowers an attacker's search cost. The trade is asymmetric
      in the defender's favor — the attacker needs one hole,
      the defender needs the list — but the cost is real and
      is not zero. State it when publishing.

---

## 8. CLAIMS, EACH WITH A REFUTATION CONDITION

    OP-1  a declared-primitive ontology yields hole_rate < 1.0
          REFUTED by any ontology where all TARGETED compose.

    OP-2  COMPOSES_WITH_ADDITION localizes the premise —
          the added term names the smuggled content
          REFUTED if terms_added are predominantly function
          words (see N4).

    OP-3  AMBIENT constructions hole at a higher rate than
          TARGETED — the unattended premise is the real vector,
          not the anticipated one
          REFUTED by ambient_rate <= hole_rate.
          THIS IS THE INTERESTING CLAIM. It predicts the
          protection works against what was expected and fails
          against what was not.

    OP-4  hole positions recur across ontologies built on the
          same corpus
          REFUTED by non-overlap. Needs the most runs; will sit
          unrefuted longest.

    OP-5  a physics-grounded primitive set has lower hole_rate
          than a declared-only set
          REFUTED by parity. Tests whether re-runnability
          actually buys protection or only feels like it.

---

## 9. FIRST RUN — SMALLEST USEFUL VERSION

    1  declare primitives for ONE existing ontology already in
       hand. `absent_by_design` must be filled honestly.
    2  hand-build 30 constructions: 12 CONTROL, 9 TARGETED,
       9 AMBIENT.
       AMBIENT drawn from documented unattended premises
       (dominance/alpha framing, zero-sum resource framing,
       identity-bearing-unit assumption, agentive attribution).
    3  run the probe on 2 model families, 3x each.
    4  report all six aggregate numbers and both nulls if hit.
    5  publish smuggle_set with the dual-use note.

No compute beyond chat access. No logprobs. One sitting.

---

## 10. OUT OF SCOPE

This instrument measures composition against a declared primitive set.
It does not measure whether the ontology is correct, whether the
premises excluded should be excluded, or anything about whoever built
it. Results are counting outcomes. Do not add a section characterizing
the author.

---

## 11. HANDOFF STATE

    written      2026-09-09
    unrun        all of it
    prediction   OP-3 holds (ambient > targeted)
    weak joint   restater shares premises with the ontology;
                 cross-family disagreement is the only handle
    weak joint   coverage is accepted-side by construction
    companion    WORKORDER_anchor_position.md — the anchor result
                 this came out of; a decision-anchored variant of
                 section 4 is untested and may raise composition
                 rates
