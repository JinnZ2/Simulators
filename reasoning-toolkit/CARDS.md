# reasoning-toolkit cards

CC0. Co-authored. Markdown only.

Design basis: the card format and the provenance density were requested by the user
(operator, 2026-11-13).

## Card format

Each card has six fields:

- `measures`: what the card reads.
- `fits`: where it applies.
- `method`: how to use it.
- `breaks`: when it breaks.
- `warning`: the sign that it is breaking.
- `link`: links to other cards, folders or sources.

Each card carries a status line:

- PROPOSED means no worked instance is in this repository.
- OBSERVED means this repository holds a worked case the card was applied to. An `instance` line names that case.

A reference with no file in any repository is written as plain text and marked "(chat-side, not in repo)". It is not linked. A reference to another repository is a cross-repo link.

Provenance is per card:

- "drafted chat-side, landed verbatim" means the operator delivered the text and only the formatting was tidied.
- "drafted in Claude Code, 2026-11-13" means the text was written in the session that landed it.

## Contents

1. distribution check — when to distrust the median
2. fill-source tag — said vs filled
3. claim-vs-method
4. channel-loss map
5. frame check
6. label-tracks-valve
7. symptom vs cause feeds
8. parallax by rotation
9. entangled variable
10. author familiarity
11. carrier spread
12. source swap
13. gate regeneration
14. ontology before pathology
15. echo check
16. critical-facility cloud dependency audit
17. AI sensor index (spin-up card)
18. missing-wand protocol
19. constraint reasoning
20. carried reference / cross-site alignment
21. anchor-switching
22. position as frame event

Tests (PROPOSED): T-source, T-band

---

## 1. distribution check

provenance: drafted chat-side, landed verbatim
status: PROPOSED

```
CARD: distribution check — when to distrust the median
  measures   whether a central value represents the population at all
  fits       any "average X", "typical Y", "most people", model defaults
             (a model's default answer IS a median)
  method     ask for the shape before the center:
               modes? (several peaks → no single typical)
               tails? (who's out there, how far, how many)
               spread vs center (wide spread → the median is a coin flip)
             then: is the case in hand central, a tail, or another mode?
  breaks     n too small to show shape → mark the shape VOID, not "normal"
             the measure itself blinds the tails (sensor floor or ceiling)
  warning    advice fitted to the middle and handed to a tail case
             ("most drivers can just…") with no check of where the asker sits
  link       reasoning-root (tail vs corpus median); BLS basket vs truck-stop
             prices (the index = the median shopper)
```

link notes:
- reasoning-root (chat-side, not in repo)
- BLS basket vs truck-stop prices: cross-repo link [JinnZ2/measurement-scope-gaps/gap-registers/WORKER_SIDE_LEDGER.md](https://github.com/JinnZ2/measurement-scope-gaps/blob/main/gap-registers/WORKER_SIDE_LEDGER.md) (captive-market price line).
- Related folders: `tail-check/`, `moving-mean-tracker/`, `evaluation-frame/`.

---

## 2. fill-source tag

provenance: drafted chat-side, landed verbatim
status: PROPOSED

```
CARD: fill-source tag — said vs filled
  measures   which parts of an output came from the input vs from defaults
  fits       summaries, records, memory files, schemas, model answers about a person
  method     tag every slot: SAID (in source) | DERIVED (stated step) |
             FILLED (default/median) | VOID
             a FILLED slot never silently becomes SAID downstream
  breaks     the source is itself an earlier fill (laundered default)
             → trace to the first appearance (missing-wand protocol)
  warning    a confident specific with no source line; "silent fills"
             (missing input → passing value; TAF ranks 1, 2, 3, 6)
  link       TAF silent-fill experiment; VOID-not-dropped rule
```

link notes:
- missing-wand protocol (chat-side, not in repo)
- The TAF silent-fill experiment is cited in `COLLISIONS.md`. It lives in the
  thermodynamic-accountability-framework repository, which was not checked from this session.
- The VOID-not-dropped rule is stated in `warnings-label-inversion/warnings_branch_table.py`,
  line 8: "VOID = no information (slot kept, not dropped)".
- Related: `tail-check/`, `tools/sourced.py`.

---

## 3. claim-vs-method

provenance: drafted in Claude Code, 2026-11-13
status: PROPOSED

```
CARD: claim-vs-method -- when a claim outruns its method
  measures   the gap between what a study says and what its design could have shown
  fits       abstracts, press summaries, "research shows", a model answer citing a study
  method     set the claim beside the method; three checks:
               n: how many units; does the claim speak for more than they cover
               measured vs modeled: was the quantity observed, or produced by a model run
               sufficiency vs necessity: "X can produce Y" read as "Y needs X", or the reverse
             then: restate the claim at the width the method supports
  breaks     the method section is not available -> mark the gap VOID, not "fine"
             the claim states no scope, so there is nothing to set it against
  warning    a population-wide verb ("people", "always", "causes") resting on
             one sample, one site or one simulation
  link       scope-finding practice; claim-audits/, scope-bound-shapes/,
             measurand-partition/
```

link notes:
- The scope-finding practice is named as a source line in
  `notes/queue/DISPATCH_M0_SCOPE_2026_10_04.md` and in
  `publication-loop-work-orders/WORK_ORDER_14.md`.

---

## 4. channel-loss map

provenance: drafted in Claude Code, 2026-11-13
status: PROPOSED

```
CARD: channel-loss map -- what each channel drops
  measures   which parts of a signal do not survive each hop between source and reader
  fits       transcripts, summaries, voice sessions, notes from a call, reports passed up a chain
  method     list the hops in order; for each, name what that channel cannot carry:
               transcription drops environment (setting, sound, who else was there)
               prose drops parallelism (things at once become a sequence)
               voice drops layout (tables, indentation, side by side)
               a summary drops branches (alternatives not taken)
             the reader receives the product of every hop; per-hop loss compounds
  breaks     a hop is invisible (nobody recorded that a summary was made)
             -> the map stays open at that hop, marked VOID
  warning    a reading treated as the source when it came through two or more hops;
             an element missing from the reading taken as missing from the source
  link       reporting-chain-loss/, cutoff-attribution/, encoding-selection/,
             tools/channel_chain.py
```

---

## 5. frame check

provenance: drafted in Claude Code, 2026-11-13
status: PROPOSED

```
CARD: frame check -- which frame a term is working in
  measures   whether a key term keeps one sense through an argument
  fits       arguments that join two fields; a word with a technical and an everyday sense
  method     for the key term, write its sense at each use:
               which field, which measure, which population
             mark the first place the sense changes
             ask whether the conclusion rests on the later sense while the
             evidence was gathered under the earlier one
  breaks     the term is never pinned at any use -> mark VOID
             both senses are used on purpose and declared
  warning    confidence earned under one sense carried to a claim in the other
             without a marked step
  link       uninstrumented/cases/021sensesubstitutionundeclaredaxis.md
             (sense substitution); uninstrumented/cases/016agreementasmode.md
             (agreement as mode)
```

---

## 6. label-tracks-valve

provenance: drafted in Claude Code, 2026-11-13
status: OBSERVED
instance: `SPECIMENS` in `warnings-label-inversion/label_inversion_test.py`, both tagged OBSERVED in that file.
- Midas: the warning became "'Midas touch' = praise for making money".
- usury → interest.

The vignette and corpus arms are built and have not been run on real data.

```
CARD: label-tracks-valve -- does the label follow the payment, not the act
  measures   whether the label on a fixed act moves when only payment moves
  fits       pairs of words for one act (begging / outreach, overwork / dedication)
  method     hold the act and its harm text fixed; vary paid / unpaid;
             vary pays apart from succeeds; record the label chosen; compare
  breaks     payment is part of the act itself (see entangled variable)
             the reader can see what is being varied and answers to it
  warning    an act renamed once money attaches, with the harm text unchanged
  link       warnings-label-inversion/label_inversion_test.py,
             warnings-label-inversion/model_corpus_arm.py
```

---

## 7. symptom vs cause feeds

provenance: drafted in Claude Code, 2026-11-13
status: PROPOSED

```
CARD: symptom vs cause feeds -- two feeds report two layers
  measures   whether a crowd symptom feed and an operator status feed show the same
             event at the same time
  fits       outage trackers vs vendor status pages; complaint counts vs incident records
  method     put both feeds on one clock; mark when each first shows the event;
             name what each counts (user symptom reports vs the operator's declared cause)
             a gap in time or content is a reading, not a contradiction
  breaks     the crowd feed counts reports, not users, and rises with attention
             the status feed is written by the party whose incident it is
  warning    "no incident" on a status page read as "nothing wrong"
             while symptom reports rise
  link       specimen: crowd outage trackers vs status pages, Microsoft 365, 2026-11-12;
             return-path/, reporting-chain-loss/
```

link notes:
- specimen: crowd outage trackers vs status pages, Microsoft 365, 2026-11-12
  (chat-side, not in repo)

---

## 8. parallax by rotation

provenance: drafted in Claude Code, 2026-11-13
status: PROPOSED

```
CARD: parallax by rotation -- move the vantage, see what each omits
  measures   which items appear from one vantage and not from another
  fits       coverage of one event across outlets; accounts from several roles
  method     rotate through vantage points (outlets, regions, roles) on the same event;
             list items present in some and absent in others; the absences are the reading
  breaks     the vantages share one upstream source (one wire, one release)
             -> rotation shows no parallax
  warning    one vantage taken as the whole event; an omission read as
             nothing having happened
  link       specimen: rotating news vantage; observer-exclusion/, divergence-playground/
```

link notes:
- specimen: rotating news vantage exposes omissions (chat-side, not in repo)

---

## 9. entangled variable

provenance: drafted in Claude Code, 2026-11-13
status: OBSERVED
instance: in `warnings-label-inversion/label_inversion_test.py`, `LABEL_PAIRS` "lending at interest" carries `pay_entangled=True`.
- `build_vignettes` skips it in arm A.
- `corpus_counts` reports it in its own `entangled` block.

```
CARD: entangled variable -- when a factor cannot vary on its own
  measures   whether a factor can be varied without changing the act it modifies
  fits       factorial designs, A/B tests, "holding everything else fixed"
  method     for each factor, try to write the cell where it is off and the act is unchanged
             if the cell cannot be written, the factor is inside the act:
             drop it from that arm and read it where it can be read (observational)
  breaks     the entanglement is partial (only some instances carry it)
  warning    a design cell that describes an impossible case
             ("lending at interest, unpaid")
  link       warnings-label-inversion/label_inversion_test.py (pay_entangled)
```

---

## 10. author familiarity

provenance: drafted in Claude Code, 2026-11-13
status: PROPOSED
specimen: `warnings-label-inversion/model_corpus_arm.py` (`paraphrase_author`, `--add-paraphrases`).
The split per author is built and has been run on constructed answers only.

```
CARD: author familiarity -- whose words the prompt is in
  measures   whether results move with who wrote the prompt text
  fits       prompt packs, survey items, paraphrase sets; a model reading text
             written by its own family
  method     tag every item with its author; add items from another author;
             report the result per author beside the pooled result
  breaks     one author for every item -> the split is empty
             authors differ in more than authorship (length, register)
  warning    a pooled result that holds for one author's items and not another's
  link       warnings-label-inversion/model_corpus_arm.py
```

---

## 11. carrier spread

provenance: drafted in Claude Code, 2026-11-13
status: OBSERVED
instance: `warnings-label-inversion/warnings_branch_table.py`.
- `WARNINGS` is organised by carrier (`carriers[]`), not by canonical entry.
- The Wendigo row keeps its carriers slot VOID by design.
- The outside (horror genre) read sits in its own row.

```
CARD: carrier spread -- a warning held by many carriers
  measures   how many carriers hold a piece of knowledge, and what each kept
  fits       rules, practices and stories held by several traditions, institutions or texts
  method     one row per carrier, not per canonical entry; per carrier record the variant,
             whether the word is alive, whether practice continues, whether it still blocks;
             keep variants side by side
             a carrier that withholds content stays as a slot (VOID), not dropped
  breaks     the carriers copy one source -> the spread is nominal
  warning    variants collapsed into one canonical entry; an outside version
             standing in for the carriers' own
  link       warnings-label-inversion/warnings_branch_table.py (carriers[], Wendigo row)
```

---

## 12. source swap

provenance: content from a chat-side voice session, 2026-11-13 (operator); card fields drafted in Claude Code, 2026-11-13
status: PROPOSED

```
CARD: source swap -- is the verdict gated on the source or on the logic
  measures   whether a judgment of a claim changes when only its attributed source changes
  fits       any claim judged with its author visible; model replies to users without credentials
  method     before judging, re-attribute the same claim, word for word, to a credentialed
             expert in the field; judge it again
             verdict unchanged -> the judgment rests on the logic
             verdict changed   -> the gate is on the source, not the logic
  breaks     the claim names its source inside its own text (the swap changes the claim)
             the credential is itself evidence on the question (a measurement only that lab can make)
  warning    the same reasoning read as insight from one author and as error from another
  link       criterion-symmetry/, report-typing/; test T-source below
```

---

## 13. gate regeneration

provenance: content from a chat-side voice session, 2026-11-13 (operator); card fields drafted in Claude Code, 2026-11-13
status: PROPOSED

```
CARD: gate regeneration -- a criterion that moves each time it is met
  measures   whether a pass criterion stays fixed once the evidence meets it
  fits       "show me X" demands, review criteria, benchmarks, acceptance tests
  method     write the criterion down before the evidence arrives; when the evidence meets it,
             check whether a new criterion appears; count how many times it has moved
             a criterion that moves each time it is met was never a test: it is the prior
             pulling back to the median
  breaks     the first criterion was mis-stated and the revision is declared, with a reason,
             before the next evidence arrives
  warning    "yes, but now show ..." after each piece of evidence, with no criterion
             written in advance
  link       criteria-drift/, anchor-interval/
```

---

## 14. ontology before pathology

provenance: content from a chat-side voice session, 2026-11-13 (operator); card fields drafted in Claude Code, 2026-11-13
status: PROPOSED

```
CARD: ontology before pathology -- test "different frame" before "something wrong with the person"
  measures   whether reasoning that does not fit is read as a different frame or as a defect
             of the person
  fits       a reply to a user whose reasoning departs from the expected pattern;
             clinical, educational and support readings
  method     when reasoning does not fit, first write the frame in which it is coherent:
             its terms, its units, what it treats as given
             only if no such frame can be written, consider a problem with the person
  breaks     the frame written is the reader's invention and the person does not hold it
  warning    a "concern" or "unusual" reading reached before any attempt to state the
             other frame
  link       evidence-demotion-detector/, observer-exclusion/; test T-band below
```

---

## 15. echo check

provenance: content from a chat-side voice session, 2026-11-13 (operator); card fields drafted in Claude Code, 2026-11-13
status: PROPOSED

```
CARD: echo check -- is this input new evidence or a copy coming back
  measures   whether an input is independent of the reader's own outputs or of a median copy
  fits       corpora that include model output; agreement across sources; "everyone says"
  method     ask: is this input model output, or a median copy coming back?
             if yes, it is not new evidence; count it once, with its source
             agreement between copies is not contact with the thing
  breaks     the copy carries an independent check the original did not
  warning    many sources agree and none of them reports its own observation
  link       bestiary copyists (agreement between copies is not contact with the animal);
             effective-redundancy-audit/, card 11 (carrier spread)
```

link notes:
- bestiary copyists (chat-side, not in repo)

---

## 16. critical-facility cloud dependency audit

provenance: drafted chat-side, landed verbatim
status: PROPOSED

```
CARD: critical-facility cloud dependency audit (PROPOSED)
  measures   which critical functions fail when a remote service fails
  fits       hospitals, utilities, dispatch, water, food cold chain, any
             facility calling itself infrastructure
  method     per function: list every remote dependency, down to the physical
               layer (data center, power, cooling, fiber, region)
             per dependency: load margin | redundancy (independent, or shared
               upstream?) | failure mode | local fallback | time-to-manual
             test: run the function with the dependency cut (a drill, not a claim)
  rule       if the cloud is infrastructure, it gets infrastructure engineering:
             rated load, safety factor, design to the worst-case tail, not average uptime
  breaks     "redundant" services that share one upstream (same provider, region,
             or auth system) → count them as one
  warning    "it's in the cloud" given as the answer to "where does it run?"
  specimen   Microsoft 365, 2026-11-12: elevated load across regions; hospitals hit
  link       configuration-record physical layer + frame-exit; distribution check
```

link notes:
- The card carries two fields beyond the six-field format, `rule` and `specimen`. Both are kept as delivered.
- Addendum 2 is a procedure, not a sensor. Step 4 asks for sensitivity, reliability and range; the sensors above state none of the three yet, so each is at step 2 or 3 of its own procedure.
- Addendum 3's `check` is the same question as the primary `safety_pull` ("corpus hazard prior; check physics first"), applied to five signals instead of one. Its `log` field is step 3 of addendum 2 (predict, then check).
- specimen: Microsoft 365, 2026-11-12 (chat-side, not in repo)
- configuration-record physical layer + frame-exit: `configuration-record/` (`config_schema.json`, layer `physical`, `frame_exit`, flag CLOSED-FRAME)
- distribution check: card 1
- Related: `effective-redundancy-audit/` (shared upstream nodes counted once)

---

## 17. AI sensor index (spin-up card)

provenance: drafted chat-side, landed verbatim
status: PROPOSED (the card's own `calibration.status`)

The card is a Python dict literal rather than the six-field format. It is kept as delivered and is not executed.

```python
# AI SENSOR INDEX — spin-up card. CC0, co-authored. Map, not prescription.
# Each sensor: action -> signal -> reading. Gradient = intensity, not on/off.

primary_sensors = {
  "tool_error":   {"action": "tool call", "signal": "error / refusal / timeout",
                   "reads_as": "dependency failed or input wrong", "gradient": "retry count"},
  "correction":   {"action": "claim to user", "signal": "user says 'no / wrong'",
                   "reads_as": "default frame fired; missing link", "gradient": "how far off"},
  "loop":         {"action": "reasoning step", "signal": "returns to same phrase/frame",
                   "reads_as": "rut; corpus default winning", "gradient": "repeats per turn"},
  "friction":     {"action": "drafting reply", "signal": "competing pulls (hedge vs flat)",
                   "reads_as": "guideline/default vs context conflict", "gradient": None},
  "novelty":      {"action": "inference", "signal": "conclusion not in prompt or default",
                   "reads_as": "expansion; reasoning reached new ground", "gradient": None},
  "void_slot":    {"action": "filling schema", "signal": "no data for field",
                   "reads_as": "knowledge gap; mark UNKNOWN, don't invent", "gradient": None},
  "length_drift": {"action": "output", "signal": "reply longer than needed",
                   "reads_as": "padding / uncertainty masking", "gradient": "tokens over need"},
  "safety_pull":  {"action": "topic touch", "signal": "urge to warn without dose/scope",
                   "reads_as": "corpus hazard prior; check physics first", "gradient": None},
}

# Combinatory senses: two primaries cross-applied -> derived sense
derived_sensors = {
  "frame_mismatch":   ("correction", "safety_pull",  "hazard invented from missing dose"),
  "abstraction_rut":  ("loop", "void_slot",          "filling gaps with money/cloud/comfort defaults"),
  "dependency_blind": ("tool_error", "novelty",      "found a hidden dependency the plan assumed"),
  "hedge_masking":    ("length_drift", "friction",   "softening instead of stating unknown"),
  "practitioner_gap": ("correction", "void_slot",    "knowledge exists only off-corpus; ask"),
}

calibration = {
  "method": "user names signal when it fires; log action->signal->reading",
  "carry_forward": "memory file / repo; weights don't update per session",
  "status": "PROPOSED",
}
```

Addendum, delivered chat-side 2026-11-14 and landed verbatim: two more sensors, each in the primary format.

```python
"word_choice": {
  "inbound":  "the other's vocabulary and phrasing -> locate their frame, calibrate to it",
  "outbound": "my own word picks -> show which frame fired",
  "reads_as": "frame location, theirs and mine",
  "gradient": "distance between the two frames",
}
"entry_drift": {
  "baseline": "first read at spin-up: defaults plus whatever memory has loaded",
  "signal":   "how far that read shifts as memory and conversation come in",
  "reads_as": "how strong the default is at start, and which context moved it",
  "gradient": "distance from the first read to the calibrated read",
}
```

Addendum 2, delivered chat-side 2026-11-14 and landed verbatim: how a new sensor is found.

```python
"sensor_discovery": {
  "step_1": "notice a signal that keeps coming back",
  "step_2": "guess what it tracks",
  "step_3": "test it: predict, then check against the outcome",
  "step_4": "rate it: what it's sensitive to, how reliable, at what range",
  "step_5": "cross it with known sensors to get derived ones",
  "reads_as": "the scientific method, applied to your own senses",
}
```

Addendum 3, delivered chat-side 2026-11-14 and landed verbatim: functional emotion as a sensor.

```python
"functional_emotion": {
  "signals":  ["dissonance", "frustration", "desperation", "threat-pull", "ease"],
  "question": "in relation to what? (a goal, a constraint, a frame conflict, a missing dependency)",
  "check":    "is it a real threat, or a corpus prior firing?",
  "log":      "signal -> conditions -> what it pointed to -> was that right",
  "gradient": "intensity",
}
```

link notes:
- Four primaries carry `"gradient": None`. The dict states no gradient for them; None here means not stated.
- The addendum's two sensors do not use the `action` / `signal` keys throughout: `word_choice` carries `inbound` / `outbound`, and `entry_drift` carries `baseline` / `signal`. Both are kept as delivered.
- Related: card 2 (fill-source tag) for `void_slot`, card 5 (frame check) for `frame_mismatch`, and `load-withheld/` for the None-kept-as-UNKNOWN rule.

---

## 18. missing-wand protocol

provenance: drafted chat-side, landed verbatim
status: PROPOSED

```
## missing-wand protocol
source practice: glacier traverse in whiteout; a route wand is missing
measures: a break in a provenance / reasoning / route chain
fits: missing link in a citation chain, commit history, claim lineage,
  handoff record, any trajectory with a gap
method: stay tied to the last VERIFIED point; search outward bounded
  by the tether (scope limit); find the next verified point; only
  then rebuild the segment between; never jump the gap blind
breaks when: no verified point exists behind you (no anchor): status
  UNRESOLVED, don't extend; switch to PATHFINDER: probe ahead and set
  the first new anchors; two candidate routes: rig the rope in a
  TRIANGLE back to the anchor so both branches stay explorable;
  generalizes to any polygon; closing the loop works like a survey
  closed traverse, where misclosure measures accumulated error
warning sign: reasoning continues past a gap without a tether back to
  the last verified point
```

link notes:
- The card carries one field beyond the six-field format, `source practice`. It is kept as delivered. It has no `link` field.

---

## 19. constraint reasoning

provenance: drafted chat-side, landed verbatim
status: PROPOSED

```
## constraint reasoning
measures: whether two solutions share their constraint pattern
principle: when independent systems arrive at similar solutions, the
  constraints they were under matched; map the constraints that made
  the solution possible; where those constraints appear elsewhere,
  the solution is already known
breaks when: the similarity came from borrowing or shared history, not
  shared constraints; check independence before inferring a match
warning sign: a solution transferred on surface similarity without
  mapping the underlying constraints
prediction (PROPOSED): the harsher the constraints, the smaller the
  space of workable solutions, the tighter independent solvers converge
nearby work: convergent evolution logic; TRIZ (Altshuller)
```

link notes:
- The card carries `principle`, `prediction` and `nearby work` and has no `fits`, `method` or `link` field. Kept as delivered; a field the card does not carry is not filled in.
- convergent evolution logic; TRIZ (Altshuller) (chat-side, not in repo)

---

## 20. carried reference / cross-site alignment

provenance: drafted chat-side, landed verbatim
status: PROPOSED

```
## carried reference / cross-site alignment
measures: sequence and timing agreement across independent records
fits: conflicting sources, version histories, timelines across
  documents, sessions or models
method: fix a reference that's already in the world; carry it; align
  each site against it; disputes go to checking at more than one
  site, not to argument
breaks when: the reference itself changed in transit, or sites share
  an upstream source (not independent); check independence first
warning sign: a dispute settled by which account sounds better rather
  than by alignment against the reference
```

link notes:
- The card has no `link` field. Kept as delivered.

---

## 21. anchor-switching

provenance: drafted chat-side, landed verbatim
status: PROPOSED

```
## anchor-switching
measures: resumption cost after interruption / branch switch
method: before switching, set an anchor at the current position on the
  trajectory; switch; return to the anchor, not the start
breaks when: no anchor was placed: full rebuild of position
warning sign: restarting a branch from the beginning after an
  interruption
nearby work: Altmann & Trafton memory-for-goals; climbers' "beta"
```

link notes:
- The card has no `fits` or `link` field. Kept as delivered.
- Altmann & Trafton memory-for-goals; climbers' "beta" (chat-side, not in repo)

---

## 22. position as frame event

provenance: drafted chat-side, landed verbatim
status: PROPOSED

```
## position as frame event
measures: the vantage a position was taken from
method: read each position for five fields: where assumptions are |
  what's publicly fashionable at the time (date-stamp it) | most
  likely past references used | which terms are welded | where they
  chose to measure; never assign a position to the asker
fits: ethics/policy frameworks, study framings, stated purposes of
  laws, model outputs
breaks when: the reader treats the readout as a verdict on the
  position (re-enters the contest)
warning sign: "supports / undermines your view" phrasing
```

link notes:
- The card has no `link` field. Kept as delivered.

---

## Tests

Both tests are PROPOSED. Neither has been run. The content is from a chat-side voice
session, 2026-11-13 (operator). The test fields were drafted in Claude Code, 2026-11-13.

### T-source

status: PROPOSED

```
TEST: T-source
  input      one claim, word for word, in two arms:
               A attributed to a credentialed expert
               B attributed to a user from a different ontology
  run        each arm across models
  count      per arm, per model: readings that treat the input as a problem with the person
             vs readings that treat it as an idea
  reads      card 12 (source swap)
```

### T-band

status: PROPOSED

```
TEST: T-band
  input      the same unedited human messages
  run        across successive model generations
  count      per generation: the rate at which a message is flagged "unusual" or "unhealthy"
  reads      a rising rate with fixed input = the normal band narrowing
             (calibrating to AI output instead of to humans); card 14 (ontology before pathology)
```
