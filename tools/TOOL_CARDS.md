# TOOL_CARDS

Generated from `TOOL_CARDS.json` by `check_cards.py --write`. Edit the JSON, not this file.
CC0. Co-authored. Status of every row: PROPOSED unless it says otherwise.

A map, not a move: the code stays in the repository it was built in. Each row is pinned to a
merged commit and the sha256 of the file there. A row on an unmerged branch reads PENDING_MERGE
with its PR number and is re-pinned when the PR merges. `python3 tools/check_cards.py` checks
every location it can reach and says NOT_CHECKED, never OK, for one it cannot.

Find a card by a phrase: `python3 tools/check_cards.py --find "moving goalposts"`.
For tools by need and symptom see `TOOL_FINDER/TOOL_FINDER.md`; a card with a `finder` name
points at its entry there.

## Index

| id | trigger | inputs | output | fails when | status | location + sha |
|---|---|---|---|---|---|---|
| frame_edge | an environment with a declared scope | place, time, population; optional answers | four questions (UPSTREAM, LAG, SHIFT, WHOSE) logged as slots; a margin flag | any slot left VOID -> margin_required true | PROPOSED | `formula-audit:glyph/tools.py` @ `337289d` sha256 `5f5979d8009e` |
| unit_audit | a formula with units on its symbols | formula text, unit per symbol | PASS / FAIL / VOID with the located term; a slot record | an unknown unit or symbol -> VOID, never PASS | PROPOSED | `formula-audit:unitaudit/check.py` @ `337289d` sha256 `e606605b481b` |
| proof_kernel | a statement that needs a proof checked, not a numeric check | a Metamath database and proof | PASS / FAIL per theorem with the failing step; $d checks | a step that does not unify, or a missing distinct-variable condition -> FAIL located | PROPOSED | `formula-audit:kernel/mm.py` @ `337289d` sha256 `40ad83b4cd1b` |
| numcheck | a formula with values or intervals | formula, values with units, tolerance | HOLDS / FAILS / MIXED / UNDECIDED / VOID decided by exact interval arithmetic; identity proposals | units fail first -> VOID; float and Decimal tiers never give the final verdict | PROPOSED | `formula-audit:numcheck/check.py` @ `337289d` sha256 `f6df0dc196f5` |
| wordslots | a claim that uses a word with unfilled places | claim record: word, slots, sense, evidential, source | PASS / DEGRADED / FAIL / UNDECIDED / VOID; each missing slot named with its sense | a required slot, sense or source missing -> DEGRADED; an undeclared field or bad tag -> VOID | PROPOSED | `formula-audit:wordslots/check.py` @ `337289d` sha256 `819b49cd4e85` |
| infer_ladder | two or more rival hypotheses with evidence | hypotheses with priors, evidence items with references | a ranking with direction per hypothesis and a replayable log | one hypothesis alone -> VOID; evidence that does not re-read -> CHECK_UNVERIFIED | PROPOSED | `formula-audit:infer/ladder.py` @ `337289d` sha256 `ef3b9a7ae996` |
| dimensional_analogy | two branch-1 PASS records with the same dimension | two unit-audit records | a proposal that their right sides are equal, as a question | no values given -> nothing can be checked yet; stays PROPOSED | PROPOSED | `formula-audit:glyph/tools.py` @ `337289d` sha256 `5f5979d8009e` |
| boundary_probe | a branch-2b record that is MIXED | one numcheck record with its bisection | a proposal for the boundary lhs - rhs = tolerance between a holding and a failing piece | no MIXED record in the environment -> the tool is closed | PROPOSED | `formula-audit:glyph/tools.py` @ `337289d` sha256 `5f5979d8009e` |
| conjugate_map | exponents p and q with p * q = 1 in formulas | unit-audit or numcheck records | a proposal ( base ** p ) ** q = base | a base that can be negative -> a question, not an identity | PROPOSED | `formula-audit:glyph/tools.py` @ `337289d` sha256 `5f5979d8009e` |
| slot_fill_audit | a branch-4 record with a slot left VOID | one wordslots record | a question naming the void slots, grouped by sense | no void slot in the claim's own sense -> the tool is closed | PROPOSED | `formula-audit:glyph/tools.py` @ `337289d` sha256 `5f5979d8009e` |
| narration_vs_execution | output printed in prose or chat beside code | the text and the code it describes | a line and number diff between what was printed and what the code prints | any mismatch -> DIFFERS, each number named | PROPOSED | PENDING_MERGE (PR 93) `Geometric-to-Binary-Computational-Bridge:experiments/experiment_bridge/evidence/printed_vs_executed.py` sha256 `1ac24363c476` |
| tolerance_provenance | a claim that carries a tolerance | the script source and its record | per claim: the tolerance as written, and STATED_IN_SOURCE / STATED_IN_CLAIM_TEXT / UNSOURCED | no stated reason -> UNSOURCED | PROPOSED | PENDING_MERGE (PR 93) `Geometric-to-Binary-Computational-Bridge:experiments/experiment_bridge/evidence/claim_tools.py` sha256 `2f19dbf9dd4a` |
| hardcoded_measured | a claim whose measured value is a literal in the source | the script source | a STRUCTURAL flag with the line, and the probe that backs it when one is named | a literal with no backing probe named | PROPOSED | PENDING_MERGE (PR 93) `Geometric-to-Binary-Computational-Bridge:experiments/experiment_bridge/evidence/claim_tools.py` sha256 `2f19dbf9dd4a` |
| exact_tier | a system with rational coefficients and a rational step | coefficients, step, start state | the step map solved exactly and verified at every step; PASS or FAIL located | denominator cap reached with no modular branch -> VOID; a float anywhere -> not engaged | PROPOSED | PENDING_MERGE (PR 94) `Geometric-to-Binary-Computational-Bridge:experiments/experiment_bridge/eqsearch/exact.py` sha256 `4a088c2393e7` |
| snapshot_class | a claim about resuming a computation from a snapshot | the snapshot content and the system it came from | a class: CONTEXT_FREE_EXACT \| STABLE_LOSSY \| CHAOTIC_REFRESH \| SUMMARY_ONLY, and whether resume is allowed | resume attempted outside the class rule (lossy with no bound, chaotic with no refresh, summary at all) | PROPOSED | VOID: not built |
| source_swap | a claim judged with its author visible | the claim or situation, read by hand | a reading; no numeric readout | the claim names its source inside its own text (the swap changes the claim) | PROPOSED | `Simulators:reasoning-toolkit/CARDS.md`#12-source-swap @ `2d902a1` sha256 `dda18ebf02ae` (card text only; no code) |
| gate_regeneration | a pass criterion that seems to move | the claim or situation, read by hand | a reading; no numeric readout | the first criterion was mis-stated and the revision is declared, with a reason, before the next evidence arrives | PROPOSED | `Simulators:reasoning-toolkit/CARDS.md`#13-gate-regeneration @ `2d902a1` sha256 `dda18ebf02ae` (card text only; no code) |
| ontology_before_pathology | reasoning that does not fit the expected pattern | the claim or situation, read by hand | a reading; no numeric readout | the frame written is the reader's invention and the person does not hold it | PROPOSED | `Simulators:reasoning-toolkit/CARDS.md`#14-ontology-before-pathology @ `2d902a1` sha256 `dda18ebf02ae` (card text only; no code) |
| echo_check | many sources agree | the claim or situation, read by hand | a reading; no numeric readout | the copy carries an independent check the original did not | PROPOSED | `Simulators:reasoning-toolkit/CARDS.md`#15-echo-check @ `2d902a1` sha256 `dda18ebf02ae` (card text only; no code) |
| cloud_dependency | a facility that calls itself infrastructure and depends on a remote service | the claim or situation, read by hand | a reading; no numeric readout | "redundant" services that share one upstream (same provider, region, or auth system) → count them as one | PROPOSED | `Simulators:reasoning-toolkit/CARDS.md`#16-critical-facility-cloud-dependency-audit @ `2d902a1` sha256 `dda18ebf02ae` (card text only; no code) |
| missing_wand | a chain with a gap: a citation, a commit history, a claim lineage, a route | the claim or situation, read by hand | a reading; no numeric readout | no verified point exists behind you (no anchor): status UNRESOLVED, don't extend | PROPOSED | `Simulators:reasoning-toolkit/CARDS.md`#18-missing-wand-protocol @ `b128fd0` sha256 `19535eab9b73` (card text only; no code) |
| constraint_reasoning | independent systems that arrived at similar solutions | the claim or situation, read by hand | a reading; no numeric readout | the similarity came from borrowing or shared history, not shared constraints | PROPOSED | `Simulators:reasoning-toolkit/CARDS.md`#19-constraint-reasoning @ `b128fd0` sha256 `19535eab9b73` (card text only; no code) |
| carried_reference | independent records that disagree on sequence or timing | the claim or situation, read by hand | a reading; no numeric readout | the reference itself changed in transit, or sites share an upstream source (not independent) | PROPOSED | `Simulators:reasoning-toolkit/CARDS.md`#20-carried-reference--cross-site-alignment @ `b128fd0` sha256 `19535eab9b73` (card text only; no code) |
| anchor_switching | an interruption or a switch to another branch of work | the claim or situation, read by hand | a reading; no numeric readout | no anchor was placed: full rebuild of position | PROPOSED | `Simulators:reasoning-toolkit/CARDS.md`#21-anchor-switching @ `b128fd0` sha256 `19535eab9b73` (card text only; no code) |
| position_as_frame_event | a stated position, framework or purpose to be read without taking a side | the claim or situation, read by hand | a reading; no numeric readout | the reader treats the readout as a verdict on the position (re-enters the contest) | PROPOSED | `Simulators:reasoning-toolkit/CARDS.md`#22-position-as-frame-event @ `b128fd0` sha256 `19535eab9b73` (card text only; no code) |

## Cards

### frame_edge

- kind: tool
- measures: what lies past the edge of the declared scope, as questions; it states nothing about the world
- fits: a case whose miss could come from where the environment edge was drawn
- breaks when: an answer is counted as filled without being read; four questions are not a complete list
- warning sign: every slot filled with one-word answers and no change to the plan
- fields: written for this index, 2026-11-17; a summary, not a quote
- aliases: what feeds this from outside the scope; where was the edge of the environment drawn; whose defaults filled this case; margin flag for unanswered scope questions
- finder: none

### unit_audit

- kind: tool
- measures: whether both sides of a formula carry the same dimension
- fits: any written formula before numbers are put through it
- breaks when: dimensionless constants and angles are not told apart; a PASS says nothing about the numbers
- warning sign: a formula passes with every symbol declared dimensionless
- fields: written for this index, 2026-11-17; a summary, not a quote
- aliases: do the units balance; dimension check on a formula; which term has the wrong unit; branch 1 unit audit
- finder: none

### proof_kernel

- kind: tool
- measures: whether each proof step follows from the stated axioms and hypotheses
- fits: identities that a numeric check can only sample
- breaks when: the axioms are taken as given; a hand-written axiom file is audited separately
- warning sign: a proof passes against axioms nobody has read
- fields: written for this index, 2026-11-17; a summary, not a quote
- aliases: check a proof step by step; Metamath verifier; is this identity proved or only sampled; branch 2a proof kernel
- finder: none

### numcheck

- kind: tool
- measures: whether a relation holds on the stated values, with rounding enclosed
- fits: data points and intersections of two formulas
- breaks when: an interval too wide to decide reads UNDECIDED; a HOLDS on points is not a proof
- warning sign: a float tier predicts FAILS where the interval tier holds
- fields: written for this index, 2026-11-17; a summary, not a quote
- aliases: does this equation hold on these numbers; interval arithmetic check; float rounding hides the answer; where two formulas intersect; branch 2b numeric check
- finder: none

### wordslots

- kind: tool
- measures: whether a word's places (safe from what, for whom) are filled and sourced
- fits: claims built on words such as safe, warm, better, efficient
- breaks when: slot text is not read: 'nothing' counts as filled; the place table is PROPOSED
- warning sign: claims pass after their slots are filled with restatements of the word
- fields: written for this index, 2026-11-17; a summary, not a quote
- aliases: safe from what and for whom; a word that claims nothing until its places are filled; evidential on a claim; which sense of the word; branch 4 word slots
- finder: none

### infer_ladder

- kind: tool
- measures: how evidence moves rival hypotheses relative to each other
- fits: choosing among stated rivals when each piece of evidence can be re-read
- breaks when: the rivals listed are the only ones scored; shared-ancestry evidence is capped, not removed
- warning sign: the top hypothesis rises on evidence that all traces to one source
- fields: written for this index, 2026-11-17; a summary, not a quote
- aliases: rank rival explanations; which hypothesis does the evidence favour; evidence that cannot be re-read; branch 5 inference ladder
- finder: none

### dimensional_analogy

- kind: tool
- measures: nothing: it proposes a candidate from a shared dimension
- fits: looking for a relation between two formulas of the same dimension
- breaks when: the same letter in two formulas may not mean the same thing
- warning sign: a proposal is repeated downstream as if it had been checked
- fields: written for this index, 2026-11-17; a summary, not a quote
- aliases: two formulas with the same units; candidate equality from shared dimension; glyph tool dimensional analogy
- finder: none

### boundary_probe

- kind: tool
- measures: nothing: it proposes where a check changes from holding to failing
- fits: a check that holds on part of its inputs and fails on part
- breaks when: only the first holding and failing pieces are used; the other edge is named, not proposed
- warning sign: the proposed boundary is read as the measured boundary
- fields: written for this index, 2026-11-17; a summary, not a quote
- aliases: where does this stop holding; edge between pass and fail region; glyph tool boundary probe
- finder: none

### conjugate_map

- kind: tool
- measures: nothing: it proposes an inverse pair found in the exponents
- fits: formulas holding a power and its inverse (a square and a square root)
- breaks when: true only where the base is not negative
- warning sign: the identity is applied on a domain that includes negative values
- fields: written for this index, 2026-11-17; a summary, not a quote
- aliases: square and square root undo each other; inverse exponents in two formulas; glyph tool conjugate map
- finder: none

### slot_fill_audit

- kind: tool
- measures: nothing: it asks for the slots a claim left empty
- fits: a claim whose word has unfilled places
- breaks when: it asks; it does not judge the answers
- warning sign: the same void slots are asked for again after being answered elsewhere
- fields: written for this index, 2026-11-17; a summary, not a quote
- aliases: which slots are still empty; ask for the missing place of a word; glyph tool slot fill audit
- finder: none

### narration_vs_execution

- kind: tool
- measures: whether narrated output equals executed output
- fits: any transcript where a model shows the output of code it wrote
- breaks when: the code needs inputs that were not delivered; output that is random by design
- warning sign: the narrated numbers are rounder than the executed ones
- fields: written for this index, 2026-11-17; a summary, not a quote
- aliases: the model printed output it never ran; narrated output vs real output; rerun the code and diff; T1 narration vs execution
- finder: none

### tolerance_provenance

- kind: tool
- measures: where each tolerance came from
- fits: claim tables with a tol_frac or band per row
- breaks when: a reason stated only in a note file reads UNSOURCED; which text counts as a reason is a reading
- warning sign: every claim passes and no tolerance has a source
- fields: written for this index, 2026-11-17; a summary, not a quote
- aliases: where did this tolerance come from; band chosen after the result; pass with an unsourced tolerance; T2 tolerance provenance
- finder: none
- not built: PRIOR_RUN(hash): a tolerance taken from a prior run, pinned by that run's hash; built nowhere
- not built: the four-class source (DEFINITION | PHYSICS_BOUND | DECLARED_PRE_RUN | UNSOURCED) and the wording 'pass (tol unsourced)' are in eqsearch/round2.py (bridge PR 94), not in this file

### hardcoded_measured

- kind: tool
- measures: whether a reported measurement was computed by the run that reports it
- fits: claim-emitting scripts that build claims through one call
- breaks when: it reads the call's shape; a value computed and then overwritten by a constant elsewhere is missed
- warning sign: a claim that always passes with measured equal to its predicted value
- fields: written for this index, 2026-11-17; a summary, not a quote
- aliases: measured value typed into the code; claim that cannot fail because the result is a constant; structural zero reported as measured; T3 hardcoded measured lint
- finder: none

### exact_tier

- kind: tool
- measures: whether a planted step map is recovered exactly, with no tolerance
- fits: noise-free states of a known discretisation
- breaks when: says nothing about measured or noisy data; reading ODE coefficients back assumes the scheme
- warning sign: the exact tier is cited for a result that came from float data
- fields: written for this index, 2026-11-17; a summary, not a quote
- aliases: recover the equation exactly in fractions; no tolerance check on a step map; denominators blow up; equation search exact tier
- finder: none

### snapshot_class

- kind: tool
- measures: VOID: not built
- fits: VOID: not built
- breaks when: VOID: not built
- warning sign: VOID: not built
- fields: VOID
- aliases: can I resume from this checkpoint; lossy snapshot of a chaotic system; resume from a summary; T4 snapshot class
- finder: none
- not built: the classifier and the per-class resume rule
- evidence: PENDING_MERGE `Geometric-to-Binary-Computational-Bridge:experiments/experiment_bridge/CLAIM_TABLE.md` EBR_016, EBR_017, EBR_018, EBR_019 (PR 93)

### source_swap

- kind: reasoning_card
- measures: whether a judgment of a claim changes when only its attributed source changes
- fits: any claim judged with its author visible; model replies to users without credentials
- breaks when: the claim names its source inside its own text (the swap changes the claim)
- warning sign: the same reasoning read as insight from one author and as error from another
- fields: verbatim from the card text, checked as substrings
- aliases: re-attribute the claim to an expert; verdict depends on who said it; source gate vs logic gate
- finder: card-source-swap

### gate_regeneration

- kind: reasoning_card
- measures: whether a pass criterion stays fixed once the evidence meets it
- fits: "show me X" demands, review criteria, benchmarks, acceptance tests
- breaks when: the first criterion was mis-stated and the revision is declared, with a reason, before the next evidence arrives
- warning sign: "yes, but now show ..." after each piece of evidence, with no criterion written in advance
- fields: verbatim from the card text, checked as substrings
- aliases: moving goalposts; criterion moves each time it is met; show me X then show me Y
- finder: card-gate-regeneration

### ontology_before_pathology

- kind: reasoning_card
- measures: whether reasoning that does not fit is read as a different frame or as a defect of the person
- fits: a reply to a user whose reasoning departs from the expected pattern; clinical, educational and support readings
- breaks when: the frame written is the reader's invention and the person does not hold it
- warning sign: a "concern" or "unusual" reading reached before any attempt to state the other frame
- fields: verbatim from the card text, checked as substrings
- aliases: different frame before something wrong with the person; reasoning read as a symptom; test the frame first
- finder: card-ontology-before-pathology

### echo_check

- kind: reasoning_card
- measures: whether an input is independent of the reader's own outputs or of a median copy
- fits: corpora that include model output; agreement across sources; "everyone says"
- breaks when: the copy carries an independent check the original did not
- warning sign: many sources agree and none of them reports its own observation
- fields: verbatim from the card text, checked as substrings
- aliases: model output coming back as evidence; agreement between copies; everyone says
- finder: card-echo-check

### cloud_dependency

- kind: reasoning_card
- measures: which critical functions fail when a remote service fails
- fits: hospitals, utilities, dispatch, water, food cold chain, any facility calling itself infrastructure
- breaks when: "redundant" services that share one upstream (same provider, region, or auth system) → count them as one
- warning sign: "it's in the cloud" given as the answer to "where does it run?"
- fields: verbatim from the card text, checked as substrings
- aliases: hospital depends on the cloud; what fails when the remote service fails; redundant services share one upstream
- finder: card-critical-facility-cloud-dependency

### missing_wand

- kind: reasoning_card
- measures: a break in a provenance / reasoning / route chain
- fits: missing link in a citation chain, commit history, claim lineage, handoff record, any trajectory with a gap
- breaks when: no verified point exists behind you (no anchor): status UNRESOLVED, don't extend
- warning sign: reasoning continues past a gap without a tether back to the last verified point
- fields: verbatim from the card text, checked as substrings; a field the card does not carry is VOID
- aliases: missing-wand; gap in a citation chain; stay tied to the last verified point; do not jump the gap blind
- finder: card-missing-wand

### constraint_reasoning

- kind: reasoning_card
- measures: whether two solutions share their constraint pattern
- fits: VOID: the card carries no such field
- breaks when: the similarity came from borrowing or shared history, not shared constraints
- warning sign: a solution transferred on surface similarity without mapping the underlying constraints
- fields: verbatim from the card text, checked as substrings; a field the card does not carry is VOID
- aliases: constraint reasoning; two systems arrived at the same solution; transfer a solution by matching constraints
- finder: card-constraint-reasoning

### carried_reference

- kind: reasoning_card
- measures: sequence and timing agreement across independent records
- fits: conflicting sources, version histories, timelines across documents, sessions or models
- breaks when: the reference itself changed in transit, or sites share an upstream source (not independent)
- warning sign: a dispute settled by which account sounds better rather than by alignment against the reference
- fields: verbatim from the card text, checked as substrings; a field the card does not carry is VOID
- aliases: carried reference; cross-site alignment; conflicting timelines across documents; align accounts against one reference
- finder: card-carried-reference

### anchor_switching

- kind: reasoning_card
- measures: resumption cost after interruption / branch switch
- fits: VOID: the card carries no such field
- breaks when: no anchor was placed: full rebuild of position
- warning sign: restarting a branch from the beginning after an interruption
- fields: verbatim from the card text, checked as substrings; a field the card does not carry is VOID
- aliases: anchor-switching; lost my place after an interruption; return to the anchor not the start
- finder: card-anchor-switching

### position_as_frame_event

- kind: reasoning_card
- measures: the vantage a position was taken from
- fits: ethics/policy frameworks, study framings, stated purposes of laws, model outputs
- breaks when: the reader treats the readout as a verdict on the position (re-enters the contest)
- warning sign: "supports / undermines your view" phrasing
- fields: verbatim from the card text, checked as substrings; a field the card does not carry is VOID
- aliases: position-as-frame-event; read a position without taking a side; never assign a position to the asker
- finder: card-position-as-frame-event

