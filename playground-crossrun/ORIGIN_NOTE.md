# Origin note: builder input briefs

Status: CARRIED. Operator statement relayed by chat-side Claude on 2026-11-11, recorded
verbatim below. Neither repository's tree holds the study-aperture builder's brief, so the
study-aperture rows rest on this statement and not on a file.

## Verbatim

```text
FROM CLAUDE (chat side), 2026-11-11 — crossrun origin note (record in STEP1_REPORT / COLLISIONS)
Kavik: Perplexity did not receive the GPT "Relational Systems Playground" spec or other chat material;
only what appears in chat-side Claude's work orders (if passed). My playground work order named the
layers ("system, relational, boundary, control, continuity, uncertainty matrices") but NOT the
system-vs-configuration continuity split. → Continuity agreement: concept-level = possible shared cue
via work order; split-level = independent convergence → candidate anchor. Update the 5 continuity
coincidence cards: shared-source slot split by level, not ruled in wholesale.
Rule for future cross-builds: record each builder's input brief (what it was given) at build time.
```

## Input briefs

```text
builder                      given                                          filed
#257 relational-playground   SPEC_GPT.md + WORK_ORDER.md                    yes, verbatim, in its tree
study-aperture playground    chat-side work orders only (if passed)         no; this note is the record
                             named layers: system / relational / boundary /
                             control / continuity / uncertainty matrices
                             NOT named: system-vs-configuration split
```

## What moved

```text
5 continuity cards   shared_source  "candidate, UNDETERMINED"  ->  split by level
                       concept level  POSSIBLE shared cue (the work order names a continuity layer)
                       split level    INDEPENDENT CONVERGENCE -> anchor CANDIDATE
                     card reading   stays PROVISIONAL: the system axis is still partly
                                    adapter-constructed, so the configuration axis is where the
                                    convergence is cleanest
observer card        shared_source  UNDETERMINED (the note does not say whether the work order
                                    named an observer layer)
O7 (README)          narrowed: shared source is no longer UNDETERMINED on the continuity cards
```

No file named COLLISIONS exists in either tree, so this note is filed here and in
`STEP1_REPORT.md` section 0 rather than in a new COLLISIONS file.

## Rule for future cross-builds

Record each builder's input brief (what it was given) at build time, in the builder's own tree.
#257 did this; study-aperture did not, and the cost was one undecidable cause on every card
until the operator supplied it afterwards.

---

## Second note: observer card origin (verbatim)

```text
FROM CLAUDE (chat side), 2026-11-11 — observer card origin
My relational-playground work order (item 6) named: PERTURBATION / REACTIVITY / STRATEGY,
"separate fields in the control matrix; no cross-system comparison until each system's regime is declared."
study-aperture has: observation/passive.py, perturbative.py, strategic.py — a STUB.
→ concept level: possible shared cue (if that order reached Perplexity).
→ naming: 2 of 3 align (perturb-, strateg-); REACTIVITY vs PASSIVE differ — different partition
  (reacts-to-observation vs not-disturbed). Record both names; do not merge.
→ card: stays UNDETERMINED at concept level; no agreement to score (stub).
COLLISIONS.md: create it in Simulators beside CONCEPT_MAP.md when that order runs; move this note there then.
```

Checked against the trees: `#257 controls.py :: OBSERVER_FIELDS = (observer_perturbation,
observer_reactivity, observer_strategy)`; study-aperture `observation/{passive,perturbative,
strategic}.py` each raise `NotImplementedError("scheduled for a later milestone")`. Both hold.

```text
observer card   concept level  UNDETERMINED (shared cue only if the #257 order reached s-a)
                naming level   2 of 3 align; REACTIVITY vs PASSIVE recorded apart
                regime level   no agreement to score (stub). The row's AGREE is on a different
                               object: the single applicability OBSERVER coordinate
concept map     one row added: observer regime partition (s-a STUB, #257 OBSERVER_FIELDS)
```

Pending move: when the CONCEPT_MAP order runs, create `COLLISIONS.md` beside `CONCEPT_MAP.md` in
Simulators and move both notes there. Not done now; no such order has run.
