# COMBINED_SPEC (STEP 2)

Status: CONFIRMED by Kavik 2026-11-11 (relayed by chat-side Claude). All 15 design questions are
answered; sections 1-8 are written to those answers and section 9 keeps the question-and-answer
log. NOT BUILT: the build waits for the TAF cleanup approval round. Neither original is changed.
Citations point at `README.md` findings F1..F15 and O1..O7 and at `STEP1_REPORT.md`.

Sources: the study-aperture `experimental/playground` package (abbreviated **s-a**) and the
relational-playground package from PR #257 (abbreviated **#257**). The concept rows follow
`adapters/concept_map.py`, which has 41 rows. The build will live in
`Simulators/combined-playground/` (Q14).

---

## 1. Shape

```text
           input brief record (per builder)                         <- section 7
                         |
   value / claim intake --+--> state tokens (one per state, reason on every non-verdict)
                         |
     closure gate (tolerance declared per account, pre-run) --> AXIS reading (section 2)
                         |                                    PHYSICAL | INSTRUMENT | DETERMINATION
          known-answer / null / ladder gate ------>           + APPLICABILITY (not an axis)
                         |
   measurand identity -> observer regime -> comparison -> coincidence card     (section 3)
                         |
          trust record keyed (model, system scope, start state)                (section 5)
                         |
                       report  (no ranking; claim tags; every count rendered from data)
```

---

## 2. Axes, statuses and the #257 mapping

Three failure axes, canonical from s-a: **PHYSICAL**, **INSTRUMENT**, **DETERMINATION**.
APPLICABILITY is a separate field and is not a failure axis (Q11).

```text
status          meaning                                        reason field
OK              ran and passed                                 --
FAILED          ran and failed                                 required
INDETERMINATE   ran; not enough to say                         required
UNTESTED        no check addressed it                          required
CRASHED         did not run: the check raised                  exception + path, required  (Q3)
CLOSED_WITHIN   closure holds within sigma, not exactly        sigma + basis, required     (Q2)
OUTSIDE_DOMAIN  APPLICABILITY only: input beyond a bound       the bound, required         (Q11)
```

Every reason #257 can emit, mapped:

```text
#257 source                              condition                     -> field : status (reason)
l0.run_status INCOMPLETE "did not close" closure fail, ledger declared -> PHYSICAL : FAILED
                                         complete                         (F9: the leak is a model defect)
l0.run_status INCOMPLETE "did not close" closure fail, ledger NOT      -> DETERMINATION : FAILED
                                         declared complete                (F8, F9: accounting gap)
l0.run_status INCOMPLETE "no LIVE        every budget VOID             -> DETERMINATION : UNTESTED
  budget"                                                                 (NO_LIVE_BUDGET)          (Q1)
l0 NOISE                                 misclosure within k sigma     -> PHYSICAL : CLOSED_WITHIN
                                                                          (sigma, basis; sigma per account) (Q2)
certify / certify_tool UNTRUSTED         harness misses plants         -> INSTRUMENT : FAILED
certify_tool raise (ZeroDivisionError)   tool gate crashes             -> INSTRUMENT : CRASHED
                                                                          (exception, path); never a missing row (F2, Q3)
trust with no cases written              zero known-answer cases       -> INSTRUMENT : UNTESTED (s-a KA_NO_CASES)
known answer from the tested formula     circular case                 -> INSTRUMENT : UNTESTED
                                                                          (CIRCULAR_KNOWN_ANSWER)   (Q6)
size / population / founder bound hit    input beyond a declared bound -> APPLICABILITY : OUTSIDE_DOMAIN
                                                                          on no failure axis (F13, Q11)
```

Rules:

- R-A1: the "declared complete" flag is part of the ledger record and must be set explicitly.
  If it is absent, the ledger counts as NOT declared, and the failure lands on DETERMINATION,
  never on PHYSICAL (F9).
- R-A2: a crash is a record carrying the exception type, the call path that raised, and the
  inputs. A crash never produces "no row" (F2).
- R-A3: a field no gate read is UNTESTED, never OK by default.
- R-A4: closure tolerance is declared PER ACCOUNT, BEFORE the run. There is no global default; a
  missing tolerance refuses the run rather than filling 1e-9 silently (O4, Q13). The numerical
  roundoff floor is recorded separately as its own known class (forest run 10), not folded into
  sigma.
- R-A5: step-1 rows are NOT relabelled. Step 3 adds a second column, "relabeled under COMBINED
  mapping", beside the preserved step-1 code (Q15).

---

## 3. Order of gates

- **Measurand identity runs before a coincidence card opens.** If two values fail identity, no
  card opens and the pair is recorded `NOT_COMPARABLE(reason)` (F5: #257 opened 13 of 15 cards,
  all 8 of the pairs s-a VOIDs among them).
- Closure runs before any physics is read; both playgrounds already do this.
- **Observer regime** is declared per system before any cross-system comparison (Q9). Four
  fields, none merged:

```text
PASSIVE       null control: not disturbed and not reacting     chat-side addition, LABELED as such
PERTURBATION  the instrument physically disturbs the system    Kimi audit section 4.4, regime 1
REACTIVITY    behaviour changes under observation, observer    Kimi audit section 4.4, regime 2
              not modelled
STRATEGY      the system models the evaluation itself          Kimi audit section 4.4, regime 3
UNDECLARED    any regime not declared -> comparison REFUSED
```

  Built in the combined build, by neither original (s-a's three are stubs; #257 has three fields
  without PASSIVE).
- Full order: identity, then observer regime, then comparison, then card.

---

## 4. States: one token per state, a reason on every non-verdict

- **UNKNOWN requires a typed expiry trigger** (from #257 `NEEDS_EXPIRY`, typed per s-a
  `ExpiryTrigger`). Free text is accepted only as `UNTYPED` and counts as "no exit defined", so it
  does not satisfy the requirement (F10, F14, Q4). An UNKNOWN with no typed trigger is refused.
- **Scoped absence and detection limits** (from s-a `establish_sensitivity`, `claim_absence`).
  `ABSENT_AT_SENSITIVITY` must carry three things, or it is refused (F7):
  - the limit, and how it was established (from a ladder, or declared);
  - the effect size of interest;
  - the conditions the null holds under.
- Each state has a distinct token: INDETERMINATE, UNTESTED, CRASHED, CLOSED_WITHIN,
  OUTSIDE_DOMAIN, NOT_COMPARABLE, NOT_SCORED_STUB, UNTYPED, UNDECLARED and REFUSED are all
  different. None is ever read as 0, OK or "no row".
- A `reason` is required on every token that is not a verdict; an empty reason is refused at
  construction.
- Vocabularies are kept separate (s-a ConditionBasis, #257 STATUSES) with an explicit mapping
  table between them; merging would lose one side's distinctions (Q12).
- Claim tags (#257 OBSERVED / DERIVED / PROPOSED) and claim records (s-a ClaimRecord) are two
  objects linked 1:1: the tag is the status of a statement, the record is its provenance chain
  (Q8).

---

## 5. Trust

- Trust is keyed by **(model, system scope, start state)**, never by name alone (F4, Q5). Trust
  certified in one system does not transfer without its own certification or a declared transfer
  argument that the gate tests (s-a `ScopedDiagnostics`).
- A static instrument in a dynamic-model gate takes a declared start state (F1). Trust is
  recorded per start state; when the verdict varies across them, the record carries the flag
  `START_STATE_SENSITIVE` and lists every arm. It is not a blanket UNTRUSTED (Q5).
- The record carries the harness class (#257 `harness_class`) beside the axis reading: the
  harness class names the detector, the axis names the instrument (F3).

---

## 6. CIRCULAR_KNOWN_ANSWER

- Definition: the known answer was derived from the formula under test, or handed across from the
  other side's closed form.
- Detection: every known-answer case records its provenance; a provenance naming the tested
  formula or model makes the case `INSTRUMENT : UNTESTED (CIRCULAR_KNOWN_ANSWER, source)`, and it
  counts toward nothing (Q6). A circular test tested nothing.
- Step-1 instances: F12 (9 branching matches against #257's own closed form) and F8 (the
  self_registered forest arm, registry filled from the model's own fluxes).

---

## 7. Input-brief record per builder

- Each build files what it was given at build time, verbatim or by sha256, in its own tree. A
  build with no brief record reads `BRIEF_UNRECORDED`.
- A coincidence card's shared-source cause is read from the briefs, split by level: concept,
  naming, and partition or split (O7, `ORIGIN_NOTE.md`).
- Names that differ are recorded side by side and not merged (REACTIVITY vs PASSIVE).
- Continuity carries both tests as separate fields, `identity_check` (configuration) and
  `return_to_anchor` (system), with no composite (Q7).
- Families stay separate where their objects differ: percolation is two families with separate
  bounds, site spread on a grid and the bounded bond graph (Q10).

Sources owed to `combined-playground/sources/` when the build starts:

```text
Kimi audit, observer regimes   #256 forest-model-ledger/ledger/toolkit/cases/texts/
                               kimi_substrate_neutral_intelligence_audit.md, section 4.4
                               (head d402fa8, sha256 86945968...)          CHECKED
TAF GAP_INSTRUMENT_CRASH       TAF draft branches #82 / #85 (unmerged)     NOT CHECKED HERE:
                               to be verified from the TAF cleanup session, where they are readable
```

---

## 8. Per-concept provenance

`taken from`: s-a, #257, both, or new. `AI-readability` notes how a model reading the record could
misread it.

| # | concept | taken from | why | AI-readability note |
|---|---|---|---|---|
| 1 | failure axes PHYSICAL / INSTRUMENT / DETERMINATION | s-a | O2, F8, F9 | three named fields, never one status string; a model collapses a single status into "worked / didn't" |
| 2 | axis statuses OK / FAILED / INDETERMINATE / UNTESTED | s-a | F2, R-A3 | UNTESTED must be spelled out; a missing key reads as OK |
| 3 | closure gate before physics | both | F8 | identical arithmetic on both sides (bit-identical recompute) |
| 4 | intervention registry | s-a | F8 | an empty registry is a token, not an absent list |
| 5 | ledger declared complete | s-a | F9, R-A1 | explicit boolean; absent means NOT declared |
| 6 | value provenance read by the closure gate | s-a | F8 | provenance is a field, not prose |
| 7 | budget VOID with a reason | #257 | concept map (VOID in s-a) | VOID beside its reason; never dropped from the list |
| 8 | noise band on a misclosure | #257 | Q2 | CLOSED_WITHIN(sigma, basis), sigma per account |
| 9 | known-answer validation | both | F3 | case provenance is recorded so CIRCULAR can be detected (section 6) |
| 10 | planted defects on the lab itself | both | baselines | each plant names the axis it should hit |
| 11 | null harness | both | F2 | nulls-only must give a record, not a crash |
| 12 | FP / TP harness class | #257 | F3 | names the detector; sits next to the axis, never replaces it |
| 13 | zero cases is not a pass | s-a | F2 | UNTESTED token, never 0/0 |
| 14 | trust scoped to a context | s-a | F4 | the key is a pair; a bare model name is refused |
| 15 | detection limit from a ladder | s-a | F7 | the limit carries the ladder or a declared basis |
| 16 | non-detection as bounded null | both | F7 | fields: limit, effect size, scope |
| 17 | scoped absence claim | s-a | F7 | scope is part of the token |
| 18 | UNKNOWN carries what would end it | both | F10, F14 | typed trigger plus an optional note |
| 19 | UNKNOWN refused without an exit | #257 | F10 | refusal at construction, with a reason |
| 20 | stale reliance on an expired UNKNOWN | s-a | concept map | expiry is checked at read time, not only at write time |
| 21 | reevaluation keeps the original | s-a | concept map | the original is kept beside the revision; never overwritten |
| 22 | frozen anchor | both | concept map | -- |
| 23 | return test with tolerance | s-a, plus #257 deltas | concept map | the verdict and the deltas are both printed |
| 24 | one-change branch | #257 | F15 | a two-change branch is refused with both changes named |
| 25 | system vs configuration continuity | both | continuity AGREE, ORIGIN_NOTE, Q7 | two fields, identity_check and return_to_anchor, no composite (Q7) |
| 26 | two state tracks, crossing refused | s-a | concept map | -- |
| 27 | claim tags OBSERVED / DERIVED / PROPOSED | #257 | F15 | a tag on every claim; untagged claims are refused |
| 28 | claim record / support | s-a | concept map | linked 1:1 to its claim tag (Q8) |
| 29 | coincidence card | #257 | F5, F15 | opens only after identity passes (section 3) |
| 30 | measurand identity gates comparison | s-a | F5 | NOT_COMPARABLE(reason) is a distinct token |
| 31 | observer declared before comparison | #257 | observer card | UNDECLARED regime refuses the comparison (Q9) |
| 32 | observer regime partition | new (union) | ORIGIN_NOTE second note, Q9 | PASSIVE (null control) / PERTURBATION / REACTIVITY / STRATEGY; built in the combined build |
| 33 | no universal ranking | both | concept map | rank() raises |
| 34 | applicability / domain of validity | s-a | F12 | NOT ASSESSED is a token |
| 35 | percolation family | both, not merged | F11 | bond vs site with spread are different objects; two families, separate bounds (Q10) |
| 36 | branching family | both | F12, F13, F14 | exact bounded pmf plus unbounded closed form; bound refusals read APPLICABILITY OUTSIDE_DOMAIN (Q11) |
| 37 | uncertainty propagation | #257 | F6 | interval propagation flags distribution-to-mean loss (row 39) |
| 38 | denominator bound to cohort members | s-a | concept map | -- |
| 39 | distribution-to-mean information loss | s-a | F6 | a flag when an interval contains both mean² and E[X²] |
| 40 | value / condition basis vocabulary | both | concept map | kept separate, with a mapping table (Q12) |
| 41 | pre-registration before a run | #257 | concept map | prereg is hashed before the run |
| new | CIRCULAR_KNOWN_ANSWER | new | F8, F12 | section 6 |
| new | crash record | new | F2, R-A2 | CRASHED(exception, call, inputs) |
| new | declared start state for static instruments | new | F1 | START_STATE_SENSITIVE token |
| new | input-brief record | new | O7, ORIGIN_NOTE | BRIEF_UNRECORDED token |

---

## 9. Question-and-answer log

All 15 CONFIRMED by Kavik 2026-11-11, as proposed by chat-side Claude. Kept as the record of
how each choice was made; sections 1-8 are the spec.

### 9a. Q3, Q7, Q9, Q15 (first round)

```text
Q3   tool-gate crash -> INSTRUMENT : CRASHED(exception, path). Own status: FAILED = ran and failed,
     INDETERMINATE = not enough to say, CRASHED = did not run. Never a missing row.
     SOURCE: TAF draft branches #82 / #85 (unmerged). CARRIED, to be verified from the TAF cleanup
     session, where they are readable. Not checked here: those are TAF PRs,
     a repository outside this session's scope. Simulators' own #82 / #85 are unrelated and do not
     contain the label.
Q7   continuity: two fields, identity_check (configuration) and return_to_anchor (system),
     no composite. Branch rule: keep both.
Q9   observer partition = union of four: PASSIVE (null control: not disturbed, not reacting) |
     PERTURBATION | REACTIVITY | STRATEGY. Undeclared -> UNDECLARED -> comparison refused.
     Built in the combined build, by neither original.
     SOURCE CHECKED: Kimi audit, forest-model-ledger/ledger/toolkit/cases/texts/
     kimi_substrate_neutral_intelligence_audit.md on #256 (head d402fa8, file sha256 86945968...),
     section 4.4 "C4 -- Observer regimes": Regime 1 perturbation (instrument disturbs the system),
     Regime 2 reactivity (behaviour changes under observation without modelling the observer),
     Regime 3 strategy (system models the evaluation). Three regimes, as stated; PASSIVE is the
     chat-side addition as the null control and is not in the audit.
Q15  step-1 rows are kept exactly as recorded. Step 3 adds a second column,
     "relabeled under COMBINED mapping". Nothing is overwritten.
```

### 9b. The other 11 (second round)

Two numberings exist: the original 15 (left column; the full list is section 9 of the first draft, commit 6dfbc4e) and the 11-item
list sent for answering, which the answers use ("open #n"). Open #3, #7, #9 are NOT the
original Q3, Q7, Q9 answered in 9a. Sections 1-8 are now written to these answers.

```text
Q1  / open #1   all-VOID run -> DETERMINATION : UNTESTED, reason NO_LIVE_BUDGET
       (nothing was posed; s-a's own UNTESTED = no check addressed it)
Q2  / open #2   NOISE -> own status CLOSED_WITHIN(sigma, basis); sigma per account
       (N, C, water differ in scale and measurement error; the number is carried)
Q4  / open #3   UNKNOWN expiry: typed trigger required; free text accepted only as UNTYPED, counted
       as "no exit defined" (an untyped trigger cannot fire automatically)
Q5  / open #4   trust recorded per start state, keyed (model, system scope, start state); a verdict
       that varies -> flag START_STATE_SENSITIVE, not blanket UNTRUSTED
Q6  / open #5   CIRCULAR_KNOWN_ANSWER -> INSTRUMENT : UNTESTED, reason CIRCULAR_KNOWN_ANSWER
       (a circular test tested nothing). Revises section 6, which proposed INDETERMINATE.
Q8  / open #6   claim tags and ClaimRecord: two objects, linked 1:1
       (tag = status of a statement; record = its provenance chain)
Q10 / open #7   percolation: two families, separate bounds (site spread on a grid != bond graph)
Q11 / open #8   size-bound refusals -> APPLICABILITY : OUTSIDE_DOMAIN, on no failure axis
       (a size limit is a domain edge; s-a already has applicability mapping). Resolves F13.
Q12 / open #9   basis vocabularies kept separate, with a mapping table (merging loses distinctions)
Q13 / open #10  closure tolerance per account, DECLARED per run before execution, no global default;
       the roundoff floor is recorded separately as a known numerical class (forest run 10)
Q14 / open #11  combined build lives in a new folder: Simulators/combined-playground/
       (originals untouched)
```

Build: NOT STARTED. It waits for the TAF cleanup approval round; the sources it owes are listed
in section 7.
