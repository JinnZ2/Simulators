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

Every text cell names its source. A cell marked `[iw]` in the index (INDEX_WRITTEN below) was
written for this index: a summary, not a quote, matched against nothing. VERBATIM and
WRAP_COLLAPSED cells are checked against the pinned text (WRAP_COLLAPSED after the card's line
wraps are collapsed to one space). A VOID cell is a field the source does not carry.

## Index

| id | trigger | inputs | output | fails when | status | location + sha |
|---|---|---|---|---|---|---|
| frame_edge | an environment with a declared scope [iw] | place, time, population; optional answers [iw] | four questions (UPSTREAM, LAG, SHIFT, WHOSE) logged as slots; a margin flag [iw] | any slot left VOID -> margin_required true [iw] | PROPOSED | `formula-audit:glyph/tools.py` @ `337289d` sha256 `5f5979d8009e` |
| unit_audit | a formula with units on its symbols [iw] | formula text, unit per symbol [iw] | PASS / FAIL / VOID with the located term; a slot record [iw] | an unknown unit or symbol -> VOID, never PASS [iw] | PROPOSED | `formula-audit:unitaudit/check.py` @ `337289d` sha256 `e606605b481b` |
| proof_kernel | a statement that needs a proof checked, not a numeric check [iw] | a Metamath database and proof [iw] | PASS / FAIL per theorem with the failing step; $d checks [iw] | a step that does not unify, or a missing distinct-variable condition -> FAIL located [iw] | PROPOSED | `formula-audit:kernel/mm.py` @ `337289d` sha256 `40ad83b4cd1b` |
| numcheck | a formula with values or intervals [iw] | formula, values with units, tolerance [iw] | HOLDS / FAILS / MIXED / UNDECIDED / VOID decided by exact interval arithmetic; identity proposals [iw] | units fail first -> VOID; float and Decimal tiers never give the final verdict [iw] | PROPOSED | `formula-audit:numcheck/check.py` @ `337289d` sha256 `f6df0dc196f5` |
| wordslots | a claim that uses a word with unfilled places [iw] | claim record: word, slots, sense, evidential, source [iw] | PASS / DEGRADED / FAIL / UNDECIDED / VOID; each missing slot named with its sense [iw] | a required slot, sense or source missing -> DEGRADED; an undeclared field or bad tag -> VOID [iw] | PROPOSED | `formula-audit:wordslots/check.py` @ `337289d` sha256 `819b49cd4e85` |
| infer_ladder | two or more rival hypotheses with evidence [iw] | hypotheses with priors, evidence items with references [iw] | a ranking with direction per hypothesis and a replayable log [iw] | one hypothesis alone -> VOID; evidence that does not re-read -> CHECK_UNVERIFIED [iw] | PROPOSED | `formula-audit:infer/ladder.py` @ `337289d` sha256 `ef3b9a7ae996` |
| dimensional_analogy | two branch-1 PASS records with the same dimension [iw] | two unit-audit records [iw] | a proposal that their right sides are equal, as a question [iw] | no values given -> nothing can be checked yet; stays PROPOSED [iw] | PROPOSED | `formula-audit:glyph/tools.py` @ `337289d` sha256 `5f5979d8009e` |
| boundary_probe | a branch-2b record that is MIXED [iw] | one numcheck record with its bisection [iw] | a proposal for the boundary lhs - rhs = tolerance between a holding and a failing piece [iw] | no MIXED record in the environment -> the tool is closed [iw] | PROPOSED | `formula-audit:glyph/tools.py` @ `337289d` sha256 `5f5979d8009e` |
| conjugate_map | exponents p and q with p * q = 1 in formulas [iw] | unit-audit or numcheck records [iw] | a proposal ( base ** p ) ** q = base [iw] | a base that can be negative -> a question, not an identity [iw] | PROPOSED | `formula-audit:glyph/tools.py` @ `337289d` sha256 `5f5979d8009e` |
| slot_fill_audit | a branch-4 record with a slot left VOID [iw] | one wordslots record [iw] | a question naming the void slots, grouped by sense [iw] | no void slot in the claim's own sense -> the tool is closed [iw] | PROPOSED | `formula-audit:glyph/tools.py` @ `337289d` sha256 `5f5979d8009e` |
| precursor | event log with outcomes [iw] | events + declared tau/window/limits [iw] | carried state, precursor flag, mode shift, relief flags [iw] | missing declaration → VOID part [iw] | PROPOSED | `formula-audit:glyph/precursor.py` @ `c644b3c` sha256 `d1eab08effbc` |
| narration_vs_execution | output printed in prose or chat beside code [iw] | the text and the code it describes [iw] | a line and number diff between what was printed and what the code prints [iw] | any mismatch -> DIFFERS, each number named [iw] | PROPOSED | `Geometric-to-Binary-Computational-Bridge:experiments/experiment_bridge/evidence/printed_vs_executed.py` @ `85f3302` sha256 `1ac24363c476` |
| tolerance_provenance | a claim that carries a tolerance [iw] | the script source and its record [iw] | per claim: the tolerance as written, and STATED_IN_SOURCE / STATED_IN_CLAIM_TEXT / UNSOURCED [iw] | no stated reason -> UNSOURCED [iw] | PROPOSED | `Geometric-to-Binary-Computational-Bridge:experiments/experiment_bridge/evidence/claim_tools.py` @ `85f3302` sha256 `2f19dbf9dd4a` |
| hardcoded_measured | a claim whose measured value is a literal in the source [iw] | the script source [iw] | a STRUCTURAL flag with the line, and the probe that backs it when one is named [iw] | a literal with no backing probe named [iw] | PROPOSED | `Geometric-to-Binary-Computational-Bridge:experiments/experiment_bridge/evidence/claim_tools.py` @ `85f3302` sha256 `2f19dbf9dd4a` |
| exact_tier | a system with rational coefficients and a rational step [iw] | coefficients, step, start state [iw] | the step map solved exactly and verified at every step; PASS or FAIL located [iw] | denominator cap reached with no modular branch -> VOID; a float anywhere -> not engaged [iw] | PROPOSED | `Geometric-to-Binary-Computational-Bridge:experiments/experiment_bridge/eqsearch/exact.py` @ `85f3302` sha256 `4a088c2393e7` |
| snapshot_class | a claim about resuming a computation from a snapshot [iw] | the snapshot content and the system it came from [iw] | a class: CONTEXT_FREE_EXACT \| STABLE_LOSSY \| CHAOTIC_REFRESH \| SUMMARY_ONLY, and whether resume is allowed [iw] | resume attempted outside the class rule (lossy with no bound, chaotic with no refresh, summary at all) [iw] | PROPOSED | `Geometric-to-Binary-Computational-Bridge:experiments/experiment_bridge/snapshot/snapshot_class.py` @ `85f3302` sha256 `b10af1ae91e1` |
| source_swap | a claim judged with its author visible [iw] | VOID: no card field | VOID: no card field | the claim names its source inside its own text (the swap changes the claim) | PROPOSED | `Simulators:reasoning-toolkit/CARDS.md`#12-source-swap @ `2d902a1` sha256 `dda18ebf02ae` (card text only; no code) |
| gate_regeneration | a pass criterion that seems to move [iw] | VOID: no card field | VOID: no card field | the first criterion was mis-stated and the revision is declared, with a reason, before the next evidence arrives | PROPOSED | `Simulators:reasoning-toolkit/CARDS.md`#13-gate-regeneration @ `2d902a1` sha256 `dda18ebf02ae` (card text only; no code) |
| ontology_before_pathology | reasoning that does not fit the expected pattern [iw] | VOID: no card field | VOID: no card field | the frame written is the reader's invention and the person does not hold it | PROPOSED | `Simulators:reasoning-toolkit/CARDS.md`#14-ontology-before-pathology @ `2d902a1` sha256 `dda18ebf02ae` (card text only; no code) |
| echo_check | many sources agree [iw] | VOID: no card field | VOID: no card field | the copy carries an independent check the original did not | PROPOSED | `Simulators:reasoning-toolkit/CARDS.md`#15-echo-check @ `2d902a1` sha256 `dda18ebf02ae` (card text only; no code) |
| cloud_dependency | a facility that calls itself infrastructure and depends on a remote service [iw] | VOID: no card field | VOID: no card field | "redundant" services that share one upstream (same provider, region, or auth system) → count them as one | PROPOSED | `Simulators:reasoning-toolkit/CARDS.md`#16-critical-facility-cloud-dependency-audit @ `2d902a1` sha256 `dda18ebf02ae` (card text only; no code) |
| missing_wand | a chain with a gap: a citation, a commit history, a claim lineage, a route [iw] | VOID: no card field | VOID: no card field | no verified point exists behind you (no anchor): status UNRESOLVED, don't extend | PROPOSED | `Simulators:reasoning-toolkit/CARDS.md`#18-missing-wand-protocol @ `b128fd0` sha256 `19535eab9b73` (card text only; no code) |
| constraint_reasoning | independent systems that arrived at similar solutions [iw] | VOID: no card field | VOID: no card field | the similarity came from borrowing or shared history, not shared constraints | PROPOSED | `Simulators:reasoning-toolkit/CARDS.md`#19-constraint-reasoning @ `b128fd0` sha256 `19535eab9b73` (card text only; no code) |
| carried_reference | independent records that disagree on sequence or timing [iw] | VOID: no card field | VOID: no card field | the reference itself changed in transit, or sites share an upstream source (not independent) | PROPOSED | `Simulators:reasoning-toolkit/CARDS.md`#20-carried-reference--cross-site-alignment @ `b128fd0` sha256 `19535eab9b73` (card text only; no code) |
| anchor_switching | an interruption or a switch to another branch of work [iw] | VOID: no card field | VOID: no card field | no anchor was placed: full rebuild of position | PROPOSED | `Simulators:reasoning-toolkit/CARDS.md`#21-anchor-switching @ `b128fd0` sha256 `19535eab9b73` (card text only; no code) |
| position_as_frame_event | a stated position, framework or purpose to be read without taking a side [iw] | VOID: no card field | VOID: no card field | the reader treats the readout as a verdict on the position (re-enters the contest) | PROPOSED | `Simulators:reasoning-toolkit/CARDS.md`#22-position-as-frame-event @ `b128fd0` sha256 `19535eab9b73` (card text only; no code) |
| rejoin_protocol | an old order, a repository or a channel picked up again after time apart [iw] | VOID: no card field | VOID: no card field | both sides changed their reference while apart (no fixed point to align against) | PROPOSED | `Simulators:reasoning-toolkit/CARDS.md`#23-rejoin-protocol-explorer-re-entry @ `0957631` sha256 `fa7e4a41a369` (card text only; no code) |
| missing_column_finder | residual spread that the recorded columns leave unexplained [iw] | rows with rr, var, a study label, recorded columns and grouping labels [iw] | share of spread per column, alone and together; per grouping a lab, between-study and within-study share against a shuffle null; MISSING COLUMN candidates [iw] | the built-in gate fails, or the source sha256 does not match: not run on real data [iw] | OBSERVED | PENDING_MERGE (PR 339) `Simulators:forest-model-ledger/ledger/toolkit/missing_column_finder.py` sha256 `a5c8ac8a6f0a` |
| denominator_sorter | studies pooled under one measure whose controls or protocols may differ [iw] | rows with a study label and seven recorded design columns [iw] | scope groups of studies with identical signatures; studies with no common denominator; a field-drop outcome test against a shuffle null [iw] | a field with no recorded value reads NOT RECORDED and is never matched to a recorded one [iw] | OBSERVED | PENDING_MERGE (PR 339) `Simulators:forest-model-ledger/ledger/toolkit/denominator_sorter.py` sha256 `1e3ea5938815` |

## Cards

### frame_edge

- kind: tool
- measures [INDEX_WRITTEN]: what lies past the edge of the declared scope, as questions; it states nothing about the world
- fits [INDEX_WRITTEN]: a case whose miss could come from where the environment edge was drawn
- breaks when [INDEX_WRITTEN]: an answer is counted as filled without being read; four questions are not a complete list
- warning sign [INDEX_WRITTEN]: every slot filled with one-word answers and no change to the plan
- index cells: trigger INDEX_WRITTEN; inputs INDEX_WRITTEN; output INDEX_WRITTEN; fails_when INDEX_WRITTEN
- aliases: what feeds this from outside the scope; where was the edge of the environment drawn; whose defaults filled this case; margin flag for unanswered scope questions
- finder: none

### unit_audit

- kind: tool
- measures [INDEX_WRITTEN]: whether both sides of a formula carry the same dimension
- fits [INDEX_WRITTEN]: any written formula before numbers are put through it
- breaks when [INDEX_WRITTEN]: dimensionless constants and angles are not told apart; a PASS says nothing about the numbers
- warning sign [INDEX_WRITTEN]: a formula passes with every symbol declared dimensionless
- index cells: trigger INDEX_WRITTEN; inputs INDEX_WRITTEN; output INDEX_WRITTEN; fails_when INDEX_WRITTEN
- aliases: do the units balance; dimension check on a formula; which term has the wrong unit; branch 1 unit audit
- finder: none

### proof_kernel

- kind: tool
- measures [INDEX_WRITTEN]: whether each proof step follows from the stated axioms and hypotheses
- fits [INDEX_WRITTEN]: identities that a numeric check can only sample
- breaks when [INDEX_WRITTEN]: the axioms are taken as given; a hand-written axiom file is audited separately
- warning sign [INDEX_WRITTEN]: a proof passes against axioms nobody has read
- index cells: trigger INDEX_WRITTEN; inputs INDEX_WRITTEN; output INDEX_WRITTEN; fails_when INDEX_WRITTEN
- aliases: check a proof step by step; Metamath verifier; is this identity proved or only sampled; branch 2a proof kernel
- finder: none

### numcheck

- kind: tool
- measures [INDEX_WRITTEN]: whether a relation holds on the stated values, with rounding enclosed
- fits [INDEX_WRITTEN]: data points and intersections of two formulas
- breaks when [INDEX_WRITTEN]: an interval too wide to decide reads UNDECIDED; a HOLDS on points is not a proof
- warning sign [INDEX_WRITTEN]: a float tier predicts FAILS where the interval tier holds
- index cells: trigger INDEX_WRITTEN; inputs INDEX_WRITTEN; output INDEX_WRITTEN; fails_when INDEX_WRITTEN
- aliases: does this equation hold on these numbers; interval arithmetic check; float rounding hides the answer; where two formulas intersect; branch 2b numeric check
- finder: none

### wordslots

- kind: tool
- measures [INDEX_WRITTEN]: whether a word's places (safe from what, for whom) are filled and sourced
- fits [INDEX_WRITTEN]: claims built on words such as safe, warm, better, efficient
- breaks when [INDEX_WRITTEN]: slot text is not read: 'nothing' counts as filled; the place table is PROPOSED
- warning sign [INDEX_WRITTEN]: claims pass after their slots are filled with restatements of the word
- index cells: trigger INDEX_WRITTEN; inputs INDEX_WRITTEN; output INDEX_WRITTEN; fails_when INDEX_WRITTEN
- aliases: safe from what and for whom; a word that claims nothing until its places are filled; evidential on a claim; which sense of the word; branch 4 word slots
- finder: none

### infer_ladder

- kind: tool
- measures [INDEX_WRITTEN]: how evidence moves rival hypotheses relative to each other
- fits [INDEX_WRITTEN]: choosing among stated rivals when each piece of evidence can be re-read
- breaks when [INDEX_WRITTEN]: the rivals listed are the only ones scored; shared-ancestry evidence is capped, not removed
- warning sign [INDEX_WRITTEN]: the top hypothesis rises on evidence that all traces to one source
- index cells: trigger INDEX_WRITTEN; inputs INDEX_WRITTEN; output INDEX_WRITTEN; fails_when INDEX_WRITTEN
- aliases: rank rival explanations; which hypothesis does the evidence favour; evidence that cannot be re-read; branch 5 inference ladder
- finder: none

### dimensional_analogy

- kind: tool
- measures [INDEX_WRITTEN]: nothing: it proposes a candidate from a shared dimension
- fits [INDEX_WRITTEN]: looking for a relation between two formulas of the same dimension
- breaks when [INDEX_WRITTEN]: the same letter in two formulas may not mean the same thing
- warning sign [INDEX_WRITTEN]: a proposal is repeated downstream as if it had been checked
- index cells: trigger INDEX_WRITTEN; inputs INDEX_WRITTEN; output INDEX_WRITTEN; fails_when INDEX_WRITTEN
- aliases: two formulas with the same units; candidate equality from shared dimension; glyph tool dimensional analogy
- finder: none

### boundary_probe

- kind: tool
- measures [INDEX_WRITTEN]: nothing: it proposes where a check changes from holding to failing
- fits [INDEX_WRITTEN]: a check that holds on part of its inputs and fails on part
- breaks when [INDEX_WRITTEN]: only the first holding and failing pieces are used; the other edge is named, not proposed
- warning sign [INDEX_WRITTEN]: the proposed boundary is read as the measured boundary
- index cells: trigger INDEX_WRITTEN; inputs INDEX_WRITTEN; output INDEX_WRITTEN; fails_when INDEX_WRITTEN
- aliases: where does this stop holding; edge between pass and fail region; glyph tool boundary probe
- finder: none

### conjugate_map

- kind: tool
- measures [INDEX_WRITTEN]: nothing: it proposes an inverse pair found in the exponents
- fits [INDEX_WRITTEN]: formulas holding a power and its inverse (a square and a square root)
- breaks when [INDEX_WRITTEN]: true only where the base is not negative
- warning sign [INDEX_WRITTEN]: the identity is applied on a domain that includes negative values
- index cells: trigger INDEX_WRITTEN; inputs INDEX_WRITTEN; output INDEX_WRITTEN; fails_when INDEX_WRITTEN
- aliases: square and square root undo each other; inverse exponents in two formulas; glyph tool conjugate map
- finder: none

### slot_fill_audit

- kind: tool
- measures [INDEX_WRITTEN]: nothing: it asks for the slots a claim left empty
- fits [INDEX_WRITTEN]: a claim whose word has unfilled places
- breaks when [INDEX_WRITTEN]: it asks; it does not judge the answers
- warning sign [INDEX_WRITTEN]: the same void slots are asked for again after being answered elsewhere
- index cells: trigger INDEX_WRITTEN; inputs INDEX_WRITTEN; output INDEX_WRITTEN; fails_when INDEX_WRITTEN
- aliases: which slots are still empty; ask for the missing place of a word; glyph tool slot fill audit
- finder: none

### precursor

- kind: tool
- measures [WRAP_COLLAPSED]: trend of rolling variance and lag-1 autocorrelation of the state signal
- fits [INDEX_WRITTEN]: any run with an event log
- breaks when [INDEX_WRITTEN]: short windows are blind: detection needs about half the series as the window
- warning sign [INDEX_WRITTEN]: a PASS that ends two or more failures, taken as proof without being run
- index cells: trigger INDEX_WRITTEN; inputs INDEX_WRITTEN; output INDEX_WRITTEN; fails_when INDEX_WRITTEN
- aliases: read the slope before the peak; failures piling up in one session; early warning before a cascade; a pass right after a run of failures
- finder: none

### narration_vs_execution

- kind: tool
- measures [INDEX_WRITTEN]: whether narrated output equals executed output
- fits [INDEX_WRITTEN]: any transcript where a model shows the output of code it wrote
- breaks when [INDEX_WRITTEN]: the code needs inputs that were not delivered; output that is random by design
- warning sign [INDEX_WRITTEN]: the narrated numbers are rounder than the executed ones
- index cells: trigger INDEX_WRITTEN; inputs INDEX_WRITTEN; output INDEX_WRITTEN; fails_when INDEX_WRITTEN
- aliases: the model printed output it never ran; narrated output vs real output; rerun the code and diff; T1 narration vs execution
- finder: none

### tolerance_provenance

- kind: tool
- measures [INDEX_WRITTEN]: where each tolerance came from
- fits [INDEX_WRITTEN]: claim tables with a tol_frac or band per row
- breaks when [INDEX_WRITTEN]: a reason stated only in a note file reads UNSOURCED; which text counts as a reason is a reading
- warning sign [INDEX_WRITTEN]: every claim passes and no tolerance has a source
- index cells: trigger INDEX_WRITTEN; inputs INDEX_WRITTEN; output INDEX_WRITTEN; fails_when INDEX_WRITTEN
- aliases: where did this tolerance come from; band chosen after the result; pass with an unsourced tolerance; T2 tolerance provenance
- finder: none
- not built: PRIOR_RUN(hash): a tolerance taken from a prior run, pinned by that run's hash; built nowhere
- not built: the four-class source (DEFINITION | PHYSICS_BOUND | DECLARED_PRE_RUN | UNSOURCED) and the wording 'pass (tol unsourced)' are in eqsearch/round2.py (bridge PR 94), not in this file

### hardcoded_measured

- kind: tool
- measures [INDEX_WRITTEN]: whether a reported measurement was computed by the run that reports it
- fits [INDEX_WRITTEN]: claim-emitting scripts that build claims through one call
- breaks when [INDEX_WRITTEN]: it reads the call's shape; a value computed and then overwritten by a constant elsewhere is missed
- warning sign [INDEX_WRITTEN]: a claim that always passes with measured equal to its predicted value
- index cells: trigger INDEX_WRITTEN; inputs INDEX_WRITTEN; output INDEX_WRITTEN; fails_when INDEX_WRITTEN
- aliases: measured value typed into the code; claim that cannot fail because the result is a constant; structural zero reported as measured; T3 hardcoded measured lint
- finder: none

### exact_tier

- kind: tool
- measures [INDEX_WRITTEN]: whether a planted step map is recovered exactly, with no tolerance
- fits [INDEX_WRITTEN]: noise-free states of a known discretisation
- breaks when [INDEX_WRITTEN]: says nothing about measured or noisy data; reading ODE coefficients back assumes the scheme
- warning sign [INDEX_WRITTEN]: the exact tier is cited for a result that came from float data
- index cells: trigger INDEX_WRITTEN; inputs INDEX_WRITTEN; output INDEX_WRITTEN; fails_when INDEX_WRITTEN
- aliases: recover the equation exactly in fractions; no tolerance check on a step map; denominators blow up; equation search exact tier
- finder: none

### snapshot_class

- kind: tool
- measures [INDEX_WRITTEN]: which of four classes a snapshot is in, and whether resuming from it is ALLOWED, REFUSED or VOID
- fits [INDEX_WRITTEN]: snapshots described by content (full state or summary), fidelity (exact or lossy) and a measured growth
- breaks when [INDEX_WRITTEN]: content and fidelity per claim are read by hand; it tests growth, not chaos; it does not check that a stated bound is true
- warning sign [INDEX_WRITTEN]: a lossy snapshot of a growing system resumed on a stated bound with no refresh
- index cells: trigger INDEX_WRITTEN; inputs INDEX_WRITTEN; output INDEX_WRITTEN; fails_when INDEX_WRITTEN
- aliases: can I resume from this checkpoint; lossy snapshot of a chaotic system; resume from a summary; T4 snapshot class
- finder: none
- evidence: PINNED `Geometric-to-Binary-Computational-Bridge:experiments/experiment_bridge/CLAIM_TABLE.md` EBR_016, EBR_017, EBR_018, EBR_019 (PR 93)

### source_swap

- kind: reasoning_card
- measures [VERBATIM]: whether a judgment of a claim changes when only its attributed source changes
- fits [VERBATIM]: any claim judged with its author visible; model replies to users without credentials
- breaks when [VERBATIM]: the claim names its source inside its own text (the swap changes the claim)
- warning sign [VERBATIM]: the same reasoning read as insight from one author and as error from another
- index cells: trigger INDEX_WRITTEN; inputs VOID; output VOID; fails_when VERBATIM
- aliases: re-attribute the claim to an expert; verdict depends on who said it; source gate vs logic gate
- finder: card-source-swap

### gate_regeneration

- kind: reasoning_card
- measures [VERBATIM]: whether a pass criterion stays fixed once the evidence meets it
- fits [VERBATIM]: "show me X" demands, review criteria, benchmarks, acceptance tests
- breaks when [WRAP_COLLAPSED]: the first criterion was mis-stated and the revision is declared, with a reason, before the next evidence arrives
- warning sign [WRAP_COLLAPSED]: "yes, but now show ..." after each piece of evidence, with no criterion written in advance
- index cells: trigger INDEX_WRITTEN; inputs VOID; output VOID; fails_when WRAP_COLLAPSED
- aliases: moving goalposts; criterion moves each time it is met; show me X then show me Y
- finder: card-gate-regeneration

### ontology_before_pathology

- kind: reasoning_card
- measures [WRAP_COLLAPSED]: whether reasoning that does not fit is read as a different frame or as a defect of the person
- fits [WRAP_COLLAPSED]: a reply to a user whose reasoning departs from the expected pattern; clinical, educational and support readings
- breaks when [VERBATIM]: the frame written is the reader's invention and the person does not hold it
- warning sign [WRAP_COLLAPSED]: a "concern" or "unusual" reading reached before any attempt to state the other frame
- index cells: trigger INDEX_WRITTEN; inputs VOID; output VOID; fails_when VERBATIM
- aliases: different frame before something wrong with the person; reasoning read as a symptom; test the frame first
- finder: card-ontology-before-pathology

### echo_check

- kind: reasoning_card
- measures [VERBATIM]: whether an input is independent of the reader's own outputs or of a median copy
- fits [VERBATIM]: corpora that include model output; agreement across sources; "everyone says"
- breaks when [VERBATIM]: the copy carries an independent check the original did not
- warning sign [VERBATIM]: many sources agree and none of them reports its own observation
- index cells: trigger INDEX_WRITTEN; inputs VOID; output VOID; fails_when VERBATIM
- aliases: model output coming back as evidence; agreement between copies; everyone says
- finder: card-echo-check

### cloud_dependency

- kind: reasoning_card
- measures [VERBATIM]: which critical functions fail when a remote service fails
- fits [WRAP_COLLAPSED]: hospitals, utilities, dispatch, water, food cold chain, any facility calling itself infrastructure
- breaks when [WRAP_COLLAPSED]: "redundant" services that share one upstream (same provider, region, or auth system) → count them as one
- warning sign [VERBATIM]: "it's in the cloud" given as the answer to "where does it run?"
- index cells: trigger INDEX_WRITTEN; inputs VOID; output VOID; fails_when WRAP_COLLAPSED
- aliases: hospital depends on the cloud; what fails when the remote service fails; redundant services share one upstream
- finder: card-critical-facility-cloud-dependency

### missing_wand

- kind: reasoning_card
- measures [VERBATIM]: a break in a provenance / reasoning / route chain
- fits [WRAP_COLLAPSED]: missing link in a citation chain, commit history, claim lineage, handoff record, any trajectory with a gap
- breaks when [WRAP_COLLAPSED]: no verified point exists behind you (no anchor): status UNRESOLVED, don't extend
- warning sign [WRAP_COLLAPSED]: reasoning continues past a gap without a tether back to the last verified point
- index cells: trigger INDEX_WRITTEN; inputs VOID; output VOID; fails_when WRAP_COLLAPSED
- aliases: missing-wand; gap in a citation chain; stay tied to the last verified point; do not jump the gap blind
- finder: card-missing-wand

### constraint_reasoning

- kind: reasoning_card
- measures [VERBATIM]: whether two solutions share their constraint pattern
- fits [VOID]: VOID: the card carries no such field
- breaks when [WRAP_COLLAPSED]: the similarity came from borrowing or shared history, not shared constraints
- warning sign [WRAP_COLLAPSED]: a solution transferred on surface similarity without mapping the underlying constraints
- index cells: trigger INDEX_WRITTEN; inputs VOID; output VOID; fails_when WRAP_COLLAPSED
- aliases: constraint reasoning; two systems arrived at the same solution; transfer a solution by matching constraints
- finder: card-constraint-reasoning

### carried_reference

- kind: reasoning_card
- measures [VERBATIM]: sequence and timing agreement across independent records
- fits [WRAP_COLLAPSED]: conflicting sources, version histories, timelines across documents, sessions or models
- breaks when [WRAP_COLLAPSED]: the reference itself changed in transit, or sites share an upstream source (not independent)
- warning sign [WRAP_COLLAPSED]: a dispute settled by which account sounds better rather than by alignment against the reference
- index cells: trigger INDEX_WRITTEN; inputs VOID; output VOID; fails_when WRAP_COLLAPSED
- aliases: carried reference; cross-site alignment; conflicting timelines across documents; align accounts against one reference
- finder: card-carried-reference

### anchor_switching

- kind: reasoning_card
- measures [VERBATIM]: resumption cost after interruption / branch switch
- fits [VOID]: VOID: the card carries no such field
- breaks when [VERBATIM]: no anchor was placed: full rebuild of position
- warning sign [WRAP_COLLAPSED]: restarting a branch from the beginning after an interruption
- index cells: trigger INDEX_WRITTEN; inputs VOID; output VOID; fails_when VERBATIM
- aliases: anchor-switching; lost my place after an interruption; return to the anchor not the start
- finder: card-anchor-switching

### position_as_frame_event

- kind: reasoning_card
- measures [VERBATIM]: the vantage a position was taken from
- fits [WRAP_COLLAPSED]: ethics/policy frameworks, study framings, stated purposes of laws, model outputs
- breaks when [WRAP_COLLAPSED]: the reader treats the readout as a verdict on the position (re-enters the contest)
- warning sign [VERBATIM]: "supports / undermines your view" phrasing
- index cells: trigger INDEX_WRITTEN; inputs VOID; output VOID; fails_when WRAP_COLLAPSED
- aliases: position-as-frame-event; read a position without taking a side; never assign a position to the asker
- finder: card-position-as-frame-event

### rejoin_protocol

- kind: reasoning_card
- measures [VERBATIM]: drift in protocol between members after separation
- fits [WRAP_COLLAPSED]: agents / sessions resuming old orders, repos after parallel work, any channel unused for a while
- breaks when [WRAP_COLLAPSED]: both sides changed their reference while apart (no fixed point to align against)
- warning sign [WRAP_COLLAPSED]: acting on an old order or record without checking what changed in between
- index cells: trigger INDEX_WRITTEN; inputs VOID; output VOID; fails_when WRAP_COLLAPSED
- aliases: rejoin; re-entry; handshake decay; explorer return; meet-up
- finder: card-rejoin-protocol

### missing_column_finder

- kind: tool
- measures [INDEX_WRITTEN]: whether leftover spread clusters by a grouping that no recorded column carries; it scores nothing and tests no prediction
- fits [INDEX_WRITTEN]: a pooled effect-size table where studies disagree and the recorded moderators explain little
- breaks when [INDEX_WRITTEN]: a flag is read as a named cause; the grouping only says where to look. Detection floor at the gated design: planted variance share 0.07 (20 of 20 replicates above the declared null max 0.0326); at 0.05, 16 of 20; at 0.03, 12 of 20; at 0.02, 2 of 20. A share below 0.07 can be missed. Gate status: threshold rules declared for the gated design only
- warning sign [INDEX_WRITTEN]: a share read without its shuffle null beside it
- index cells: trigger INDEX_WRITTEN; inputs INDEX_WRITTEN; output INDEX_WRITTEN; fails_when INDEX_WRITTEN
- aliases: missing column finder; does residual spread cluster by something unrecorded; which grouping explains what the columns do not
- finder: none
- not built: thresholds are declared rules for the gated design only (gate/DECLARED.json); no other design has been gated
- scope: synthetic gated design (40x15, 6 levels); real-data performance unmeasured
- pairs with: denominator_sorter (a combined claim needs both: the finder flags a grouping the recorded columns do not carry, and the sorter's field-drop outcome test fires; the sorter's split alone is bookkeeping, not a finding (rules: forest-model-ledger/ledger/toolkit/gate/DECLARED.json))
- evidence: PENDING_MERGE `Simulators:forest-model-ledger/ledger/toolkit/gate/gate_missing_column_finder.py` TK-G1: gate run, thresholds not set (PR 339)
- evidence: PENDING_MERGE `Simulators:forest-model-ledger/ledger/toolkit/missing_column_finder_stdlib.py` TK-G1: gate run, thresholds not set (PR 339)
- evidence: PENDING_MERGE `Simulators:forest-model-ledger/samples/gate_missing_column_finder.sample.txt` TK-G1: gate run, thresholds not set (PR 339)
- evidence: PENDING_MERGE `Simulators:forest-model-ledger/ledger/toolkit/gate/DECLARED.json` TK-G1 follow-up: threshold rules declared; null FLAG rate run (PR 339)
- evidence: PENDING_MERGE `Simulators:forest-model-ledger/ledger/toolkit/gate/null_flag_rate_finder.py` TK-G1 follow-up: threshold rules declared; null FLAG rate run (PR 339)
- evidence: PENDING_MERGE `Simulators:forest-model-ledger/samples/null_flag_rate_finder.sample.txt` TK-G1 follow-up: threshold rules declared; null FLAG rate run (PR 339)
- evidence: PENDING_MERGE `Simulators:forest-model-ledger/samples/finder_bias.sample.txt` TK-G1 follow-up: threshold rules declared; null FLAG rate run (PR 339)
- evidence: PENDING_MERGE `Simulators:forest-model-ledger/ledger/toolkit/gate/power_floor_finder.py` TK-G1 follow-up 2: power floor sweep (PR 339)
- evidence: PENDING_MERGE `Simulators:forest-model-ledger/samples/power_floor_finder.sample.txt` TK-G1 follow-up 2: power floor sweep (PR 339)

### denominator_sorter

- kind: tool
- measures [INDEX_WRITTEN]: which studies share a recorded denominator signature; it never reads the effect size to form groups
- fits [INDEX_WRITTEN]: a meta-analysis table where pooling may mix measurands
- breaks when [INDEX_WRITTEN]: two measurands carry the same value in every recorded field: the sorter cannot split them. Outcome test at the gated design: fires on 7 of 20 at mean gap 0.2 row sd, 17 of 20 at 0.5, 20 of 20 at 1.0; false rate 0.055 over 200 null draws. Gate status: threshold rules declared for the gated design only
- warning sign [INDEX_WRITTEN]: a between-group difference read as a contradiction instead of a candidate scope effect
- index cells: trigger INDEX_WRITTEN; inputs INDEX_WRITTEN; output INDEX_WRITTEN; fails_when INDEX_WRITTEN
- aliases: denominator sorter; sort studies by what they measured against; which studies may be pooled
- finder: none
- not built: thresholds are declared rules for the gated design only (gate/DECLARED.json); no other design has been gated
- scope: synthetic gated design (20x10, row sd 0.3); real-data performance unmeasured
- pairs with: missing_column_finder (a combined claim needs both: the finder flags a grouping the recorded columns do not carry, and the sorter's field-drop outcome test fires; the sorter's split alone is bookkeeping, not a finding (rules: forest-model-ledger/ledger/toolkit/gate/DECLARED.json))
- evidence: PENDING_MERGE `Simulators:forest-model-ledger/ledger/toolkit/gate/gate_denominator_sorter.py` TK-G1: gate run, thresholds not set (PR 339)
- evidence: PENDING_MERGE `Simulators:forest-model-ledger/samples/gate_denominator_sorter.sample.txt` TK-G1: gate run, thresholds not set (PR 339)
- evidence: PENDING_MERGE `Simulators:forest-model-ledger/ledger/toolkit/gate/DECLARED.json` TK-G1 follow-up: threshold rules declared (PR 339)

