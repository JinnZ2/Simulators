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
          known-answer / null / ladder gate ------>           + APPLICABILITY, COVERAGE (not axes)
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
APPLICABILITY is a separate field and is not a failure axis (Q11). **COVERAGE** is a separate
field too, and never feeds severity (R-A2):

```text
COVERAGE entry   kind ∈ {UNKNOWN, INFO, GAP_INSTRUMENT_CRASH}, module, input, reason,
                 missing_path, expiry_condition
source           TAF calibration/unified_audit.py @ 16285cc, lines 96-101, CHECKED (section 7)
```

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
  inputs. A crash never produces "no row" (F2). CRASHED stays an INSTRUMENT status, and it is
  reported on the coverage axis (kinds UNKNOWN / INFO / GAP_INSTRUMENT_CRASH), never in severity.
  The coverage entry carries TAF's fields: kind, module, input, reason, missing_path,
  expiry_condition (source: section 7).
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
TAF GAP_INSTRUMENT_CRASH       TAF main                                    CHECKED 2026-11-18, read-only
                               #85 pin: main merge commit 16285cc (PR #85; branch head 51083ca)
                               #82 pin: archive/unknown-axis-followup a2c5d99d8b41
                               definition: calibration/unified_audit.py:92-101
                               merged to main 2026-11-18 via #85 (16285cc); definition line 96,
                               COVERAGE_KINDS line 101
Decision rule, M4 branch G     JCGM 106:2012                               CHECKED_BY_RELAY
                               https://www.bipm.org/documents/20126/2071204/JCGM_106_2012_E.pdf
                               reader: Manus (browser), read 2026-11-18, relayed via chat;
                               not read by the building session (www.bipm.org egress refused)
                               ISO 14253-1: via JCGM's description only (paywalled; not read)
                               earlier status: NOT_CHECKED ("recalled, not re-read (VERIFY)")
```

G2 theory sources (not read by this session):

```text
Measurand identity (9c item 2)  JCGM 200:2012 (VIM), section 2.3 measurand:     NOT_CHECKED
                               "quantity intended to be measured"; identity read as same kind of
                               quantity + same specification of conditions. Recalled, not read
                               (VERIFY): www.bipm.org egress refused to this session's fetches
Comparison (9c item 3)         EA-4/02: En = |x1 - x2| / sqrt(U1^2 + U2^2), En <= 1 agree,  NOT_CHECKED
                               U expanded. Recalled, not read (VERIFY): european-accreditation.org
                               unreachable; ISO 13528 paywalled. Which EA document carries En is
                               itself unverified.
```

Quotes as relayed (JCGM 106:2012):

```text
3.3.9   acceptance interval: "interval of permissible measured quantity values"
3.3.10  rejection interval: "interval of non-permissible measured quantity values"
3.3.11  guard band: "interval between a tolerance limit and a corresponding acceptance limit"
        (note: includes the limits)
3.3.12  decision rule: "documented rule that describes how measurement uncertainty will be
        accounted for with regard to accepting or rejecting an item, given a specified
        requirement and the result of a measurement"
8.3.1.1 "Accepting or rejecting an item when the measured value of its property of interest
        is close to a tolerance limit may result in an incorrect decision and lead to
        undesirable consequences."
8.3.1.2 incorrect-decision probability "can be as large as 50 %" near the limit (simple
        acceptance)
8.3.1.3 "choosing acceptance limits offset from the tolerance limits, a conformity decision
        strategy called guardbanding"
8.3.2.1 guarded acceptance: "The risk of accepting a non-conforming item can be reduced by
        setting an acceptance limit AU inside the tolerance interval"
8.3.2.3 guard band width w = rU; "A common choice is r = 1, in which case w = U."
8.3.3.1 guarded rejection (partial quote, as relayed): an acceptance limit outside the
        tolerance interval "can be chosen so as to increase the probability that a rejected
        item is truly non-conforming"
```

Note 2026-11-18: 8.3.2.1/8.3.3.1 first entered as summaries because the relay to the build
paraphrased them; restored from the original Manus read. 8.3.1.1-8.3.1.3 added as relayed.

DERIVED (combined build, not stated by JCGM 106):

```text
UNRESOLVED middle zone  guarded acceptance (8.3.2.1) and guarded rejection (8.3.3.1) applied
                        together: accept below tol - U, reject above tol + U; between the two
                        limits neither is proven -> UNRESOLVED on INSTRUMENT
floor folded into U     U = k*sigma + roundoff floor (w = rU with r = 1, 8.3.2.3)
OK tier at roundoff     |m| <= roundoff floor -> OK; |m| <= tol - U -> CLOSED_WITHIN
```

Definition as quoted (identical text on #82, #85 and main 16285cc):

```text
# A module that raised is not a reading of the system. Its status is
# GAP_INSTRUMENT_CRASH and it goes to coverage with the exception and the
# missing path, never to severity (2026-11-11 follow-up to #80).
GAP_INSTRUMENT_CRASH = "GAP_INSTRUMENT_CRASH"
COVERAGE_KINDS = ("UNKNOWN", "INFO", "GAP_INSTRUMENT_CRASH")
coverage entry fields: kind, module, input, reason, missing_path, expiry_condition
```

Pin note: `calibration/unified_audit.py` on main 16285cc has sha256 fcccb9af8d8e..., unchanged from
the #85 branch head the spec first cited (65bb724f0484, since rebased to 51083ca). Only the commit
pin moved. The #82 version differs (a0864e725159...) and is kept at the archive ref above.

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
     2026-11-18: source CHECKED (read-only; section 7). Answer kept: CRASHED is an instrument
     status, reported on the coverage axis and never in severity.
     2026-11-18 coverage field declared (G1, found at gate)
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

### 9c. Open for next pass (2026-11-18)

Requested as "9b"; 9b already holds the second-round answers, so this is 9c. Each item is held
VOID or not built in combined-playground M1-M9 and needs a decision before it is built.

```text
2026-11-18  VOID-1   composite severity across axes (M3; section 2 defines per-axis status only)
2026-11-18  VOID-2   measurand identity criterion (M5; caller supplies verdict + reason)
2026-11-18  VOID-3   what a comparison computes (M5; caller supplies a token)
2026-11-18  VOID-4   effect of two systems declaring different observer regimes (M5)
2026-11-18  VOID-5   coincidence-card causes other than shared source (M5)
2026-11-18  VOID-6   how the gate tests a declared trust-transfer argument (M6)
2026-11-18  VOID-7   harness-class labels and their FP / TP thresholds (M6, M7)
2026-11-18  VOID-8   pass rule over counted known-answer cases (M7)
2026-11-18  VOID-9   continuity identity criterion (M8; identity_check is a caller token)
2026-11-18  VOID-10  interval propagation arithmetic (M9, row 37)
2026-11-18  VOID-11  expiry-trigger kind vocabulary (M2)
2026-11-18  VOID-12  vocabulary mapping rows (M2, Q12)
2026-11-18  also     CLOSED_WITHIN on INSTRUMENT / DETERMINATION -> VOID (M3; mapped to PHYSICAL only)
2026-11-18  TRIAGE   G1 REUSE (pins in combined-playground/cplay/pins.py; sample samples/pins_resolve.txt):
                     VOID-1  no composite; severity() is the per-axis vector (P1 TAF 16285cc
                             unified_audit.py "UNKNOWN is deliberately absent"; R-A2). The cited
                             "ai-metrology weights not bins" was NOT FOUND (no such repo or file)
                     VOID-5  card causes = shared source, method, model, training data, code, axioms;
                             undeclared -> UNDECLARED token (P5 formula-audit 4345de6 infer/ladder.py)
                     VOID-6  transfer argument passes iff every declared constraint matched and
                             independence checked, else REFUSED (P6 ladder cross_domain; P6 card)
                     VOID-10 interval propagation delegated to formula-audit numcheck, not copied
                             (P10 337289d numcheck/check.py, identical bytes on main 4345de6)
                     VOID-11 expiry vocabulary = TAF EXPIRY_KEYS instrument_class / sensitivity /
                             protocol / provenance (P11 16285cc); not mapped onto cplay ExpiryTrigger
                             kind / target / condition -- that mapping is VOID-12
2026-11-18  TRIAGE   G2 THEORY (sources NOT_CHECKED, VERIFY; section 7):
                     VOID-2  identity = same kind of quantity + same specification of conditions
                             (Measurand / measurand_identity; a missing condition key differs)
                     VOID-3  comparison = difference with combined uncertainty; En = |x1-x2| /
                             sqrt(U1^2+U2^2), En <= 1 -> OK; combined U = 0 -> VOID
                     VOID-4  differing regimes -> REFUSED naming both, unless a TransferArgument
                             passes (all constraints matched, independence checked)
                     VOID-8  ka_verdict: OK iff every counted case passes AND every planted fault
                             is caught; counts reported, no threshold; no plants -> UNTESTED
2026-11-18  TRIAGE   G3 rows 35-36 BUILT (cplay/families.py; samples/families.txt):
                     percolation, two families kept apart (Q10): site and bond on the square
                     lattice, union-find cluster growth (Newman-Ziff), mean first-span fraction;
                     L=32, 60 runs: site 0.5923 (se 0.0039), bond 0.5022 (se 0.0044)
                     branching (Q11): Galton-Watson extinction = smallest fixed point of the
                     offspring pgf in [0,1]; bounded pmf and Poisson closed form; m <= 1 -> q = 1
                     size bounds (L, pmf support) -> APPLICABILITY OUTSIDE_DOMAIN
                     known answers NOT_CHECKED (VERIFY): site ~0.5927, bond 0.5, Poisson
                     q = e^{lam(q-1)} -- recalled, no source read
2026-11-18  OPEN     VOID-7, VOID-9, VOID-12: author's call, open
2026-11-18  BRANCHED VOID-7 harness classes; decide on evidence from SPLIT rows. H-A by information
                     source (M7 labels), H-B by measured power (planted mutants caught / equivalent
                     nulls flagged, bins from counts, no threshold); cplay/harness_branches.py,
                     samples/harness_branches.txt. SPLIT: en_strong (misses uc_linear_sum), en_weak
                     (0/5), poisson (misses critical_strict at lam = 1); g_table CIRCULAR yet 2/3.
                     Held-VOID stays until a branch survives the cases
2026-11-18  DECIDED  VOID-7 on evidence: power = H-B (measured catch rate, the rating); H-A kept as
                     the provenance field. Evidence round added an RSS vs linear-sum case (|d| 0.6,
                     U 0.3 / 0.4: RSS En 1.2 FAILED, linear 0.857) and Poisson lam = 1: en_strong
                     4/5 -> 5/5, poisson 3/4 -> 4/4, no false alarms; en_weak stays 0/5 (SPLIT)
2026-11-18  BRANCHED VOID-9 continuity identity; decide on evidence from SPLIT rows. C-A exact state
                     hash, C-B every declared variable within tolerance (M8), C-C unbroken chain of
                     replay-verified transitions; cplay/continuity_branches.py,
                     samples/continuity_branches.txt. Known cases rebuilt after snapshot_delta
                     (Geometric-to-Binary-Computational-Bridge @85f3302, EBR_016-019): fib_exact,
                     spiral_lossy (ratio 0.0498, as EBR_017), lorenz_lossy, counts_word. Match with
                     the measured resume outcome: C-A 3/4 (fails spiral), C-B 2/4, C-C 2/4 (both
                     fail lorenz and counts). SPLIT: spiral, lorenz, counts. Held-VOID stays
2026-11-18  EVIDENCE VOID-9 round: C-C fixed to replay against the exact trajectory (first build kept
                     as C-C0); branch D added, class-conditioned on the T4 snapshot class
                     (CONTEXT_FREE_EXACT -> C-A, STABLE_LOSSY -> C-B, CHAOTIC_REFRESH -> exact-only,
                     SUMMARY_ONLY -> NOT_SAME). D holds 4/4 on the original cases -> PROPOSED as the
                     criterion. Fifth case bistable_loose (damped double well, class measured at a
                     reference snapshot deep in one basin -> STABLE_LOSSY; snapshot near the
                     separatrix, 1-dp rounding within tol 0.1 lands in the other basin): D FAILS it
                     (SAME vs measured NOT_SAME). D holds 5/5 only if growth is measured at each
                     case's own snapshot, which is the resume measurement itself. Matches: C-A 4/5,
                     C-C 4/5, D 4/5, C-B 2/5, C-C0 2/5. VOID-9 stays; D PROPOSED, broken by case 5
2026-11-18  STATUS   D -> broken by case 5 (global class): the class is measured once per system at
                     a reference snapshot, so a snapshot near a separatrix inherits the wrong class
2026-11-18  BRANCH   D2 basin margin (reading taken by the build; the order's definition was not in
                     its context): a lossy full-state snapshot is classed locally from N declared
                     ball samples (radius = tol) around the anchor; any sample growth > 1 ->
                     exact-only, all <= 1 -> C-B; N missing -> UNTESTED. 6 cases x 6 branches
                     (D and D2 kept): D2 6/6 at N = 32, seed 0; D 4/6; C-A 5/6; C-C 5/6; C-B 2/6
2026-11-18  PROPOSED D2, with the case 6 miss-rate table (bistable_sliver: ball almost entirely in one
                     basin, a thin sliver across the separatrix, the lossy snapshot in the sliver):
                     case 6 sliver: ball radius 0.05 around (0.06, -0.01); sliver fraction f_hat = 0.0405 (pool 2000, seeded); 400 trials per N
                     N     measured miss rate   predicted (1 - f)^N
                     1     0.9600               0.9595
                     2     0.9475               0.9206
                     4     0.8075               0.8476
                     8     0.7275               0.7184
                     16    0.5200               0.5161
                     32    0.2800               0.2663
                     64    0.0500               0.0709
                     128   0.0025               0.0050
                     256   0.0000               0.0000
                     a miss reads SAME on a NOT_SAME snapshot. D2 survives case 6 at N = 32, seed 0,
                     with a 0.28 measured miss rate at that N: survival is probabilistic, not
                     shown. VOID-9 stays until D2 survives case 6
2026-11-18  XREF     basin-margin rule: source pattern named as the "repose glyph" (conditional
                     stability); NOT LOCATED in any indexed JinnZ2 repository by code search
2026-11-18  XREF     corrected: oral-tradition glyph #4 (repose: rest is conditional, still loaded),
                     relayed in chat; not in a repository
2026-11-18  BRANCH   D2 bound rule: purpose inputs f_min, alpha (missing -> UNTESTED);
                     N = ceil(ln alpha / ln(1 - f_min)); zero hits -> SAME_WITH_BOUND recording
                     (f_min, alpha, N, hits 0); any hit -> NOT_SAME; exact-margin path D2m where a
                     case declares its separatrix (margin > tol -> SAME, else NOT_SAME).
                     6 cases at f_min 0.04, alpha 0.01, N 113: D2 6/6; D2m 2/2 (sliver margin 0.0411
                     vs tol 0.05; flat-cap estimate 4.4 % vs sampled sliver 4.05 %)
2026-11-18  NOT MET  VOID-9 decision test: case 6 at N 113 over 400 trials (pool seed 11, as before)
                     -> measured miss 0.0125 (5 of 400; Wilson 95 % [0.0054, 0.0289]) > alpha 0.01;
                     predicted (1 - 0.0405)^113 = 0.0094. 400 trials cannot separate 0.0094 from
                     0.01. Per the rule, VOID-9 stays VOID
2026-11-18  BRANCHED VOID-12 vocabulary mapping rows; decide on evidence from SPLIT rows. V-A same
                     label, V-B definitions match under the TOOL_CARDS VERBATIM / WRAP_COLLAPSED rule,
                     V-C same predicate + same slots; cplay/vocab_branches.py,
                     samples/vocab_branches.txt; 8 pairs across TAF @16285cc, COMBINED_SPEC / cplay
                     @9658b3e, formula-audit numcheck @4345de6, every definition pinned. SPLIT:
                     GAP_INSTRUMENT_CRASH | CRASHED (V-C only), UNKNOWN | UNKNOWN and
                     ABSENT_AT_SENSITIVITY pair (V-A only, slots differ), VOID | VOID (V-A only,
                     predicates differ: homonym). V-B maps no pair. Held-VOID stays
2026-11-18  DECIDED  VOID-12 on evidence: the mapping relation is V-C tiered -- MAPS (same predicate,
                     same slots), PARTIAL (same predicate, slots differ; the row names the slot
                     correspondence), HOMONYM (same label, no shared predicate), NONE. On the 8
                     pairs: MAPS 1 (GAP_INSTRUMENT_CRASH | CRASHED), PARTIAL 5, HOMONYM 1
                     (VOID | VOID), NONE 1 (HOLDS | OK). V-A and V-B kept as columns.
2026-11-18  OPEN     VOID-12 predicates were assigned by one reader (this build); a blind
                     second-reader predicate assignment is open
2026-11-18  GAP      rows 35-36 percolation (two families) and branching (bounded pmf + closed form):
                     families and bounds named, no algorithm stated; not built (closed by G3 below)
2026-11-18  CHOICE   M4 closure verdict rule: verdict() raises SpecGap; six candidates built beside it,
                     none adopted (A tolerance first / B floor added / C band first / D floor first /
                     E floor then max(tol, k*sigma) / F k*sigma*sqrt(n_legs), tol hard cap); table below
2026-11-18  CITED    FAILED routing in every branch: PHYSICAL iff ledger DECLARED complete, else
                     DETERMINATION -- section 2 mapping lines 62-65 and R-A1 lines 82-84 (not VOID)
2026-11-18  BRANCH   G guard band: U = k*sigma + roundoff floor; OK if |m| <= roundoff floor; CLOSED_WITHIN
                     if |m| <= tol - U; FAILED if |m| > tol + U; between -> UNRESOLVED token on
                     INSTRUMENT, never PHYSICAL; sigma or k missing -> VOID; token floor -> VOID
2026-11-18  RELABEL  G's proven-conformance zone was OK, now CLOSED_WITHIN; OK is reserved for the
                     exact tier |m| <= roundoff floor (per the c1 reading)
2026-11-18  DERIVED  G precondition, decided from the declarations before m is read: U >= tol ->
                     INSTRUMENT flag TOLERANCE_UNRESOLVABLE on the case, reported beside the verdict
                     (the instrument cannot prove conformance at the tolerance it is judged against)
2026-11-18  PROPOSAL verdict() = branch G once its source (section 7, decision rule) is CHECKED;
                     until then verdict() keeps raising SpecGap
2026-11-18  DECIDED  verdict() = verdict_branch_G (go-live); SpecGap removed. Source CHECKED_BY_RELAY
                     (section 7). Branches A-F stay as named alternatives with the SPLIT table;
                     systematic_check unchanged. Supersedes the CHOICE and PROPOSAL lines above.
2026-11-18  DERIVED  F reinterpreted as random-error consistency check (closed-traverse practice),
                     separate from conformance: systematic_check() flags DETERMINATION
                     SYSTEMATIC_ERROR_INDICATED when |m| > k*sigma*sqrt(n_legs); n_legs missing -> VOID;
                     never changes G's verdict. c9: G P:CW + SYSTEMATIC_ERROR_INDICATED.
                     verdict_branch_F stays in the SPLIT table as history
2026-11-18  READING  branch F gives no OK (the item states none); D / E CLOSED_WITHIN with no declared
                     sigma -> VOID (Q2 makes sigma part of CLOSED_WITHIN)
```

Merge log:

```text
2026-11-18  M1 #280 ba4c9fc  M2 #281 8bb5eee  M4 #283 02c98b9  M5 #284 f5cb3a6  M6 #285 2e900c1
            M7 #286 6d790c1  M8 #287 ab4b007  M9 #288 a827228
2026-11-18  M3 #282 landed via M4 merge 02c98b9 (no merge commit of its own: base auto-retargeted on
            branch delete, the PR was still draft, M4 carried its commits; GitHub marked #282 merged)
```

M4 branch table (combined-playground/samples/closure_branch_table.txt, constructed cases; verdict() = column G):

```text
P = PHYSICAL, D = DETERMINATION, I = INSTRUMENT, CW = CLOSED_WITHIN; n_legs = 4 for F
G source: JCGM 106:2012 sections 3.3.9-3.3.12, 8.3.2.1, 8.3.2.3 (w = rU, r = 1), 8.3.3.1; read by Manus (browser) 2026-11-18, relayed; ISO 14253-1 via JCGM's description only [CHECKED_BY_RELAY]
case  |m|           tol    k*sigma  floor   complete  A       B       C       D       E       F       G        G-pre        sys-check  split  G-differs
c1    1e-07         1e-06  3e-06    1e-12   True      P:OK    P:OK    P:CW    P:CW    P:CW    P:CW    I:UNRES  I:TOL_UNRES  --         SPLIT  G
c2    2e-06         1e-06  3e-06    1e-12   True      P:CW    P:CW    P:CW    P:FAIL  P:CW    P:FAIL  I:UNRES  I:TOL_UNRES  --         SPLIT  G
c3    5e-06         1e-06  3e-06    1e-12   True      P:FAIL  P:FAIL  P:FAIL  P:FAIL  P:FAIL  P:FAIL  P:FAIL   I:TOL_UNRES  --                
c4    1.0000005e-06 1e-06  --       1e-09   True      P:FAIL  P:OK    P:FAIL  P:FAIL  P:FAIL  VOID    VOID     VOID         VOID       SPLIT  
c5    5e-07         1e-06  --       1e-12   True      P:OK    P:OK    P:OK    VOID    VOID    VOID    VOID     VOID         VOID       SPLIT  
c6    5e-07         1e-06  --       TOKEN   True      P:OK    VOID    P:OK    VOID    VOID    VOID    VOID     VOID         VOID       SPLIT  
c7    2e-06         1e-06  --       1e-12   True      P:FAIL  P:FAIL  P:FAIL  P:FAIL  P:FAIL  VOID    VOID     VOID         VOID       SPLIT  
c8    5e-06         1e-06  3e-06    1e-12   ABSENT    D:FAIL  D:FAIL  D:FAIL  D:FAIL  D:FAIL  D:FAIL  D:FAIL   I:TOL_UNRES  --                
c9    5e-06         1e-05  2e-07    1e-12   True      P:OK    P:OK    P:OK    P:CW    P:CW    P:FAIL  P:CW     --           D:SYS_ERR  SPLIT  
c10   0             1e-05  2e-07    1e-12   True      P:OK    P:OK    P:CW    P:OK    P:OK    P:CW    P:OK     --           --         SPLIT  
c11   1.1e-05       1e-05  2e-07    1e-12   True      P:FAIL  P:FAIL  P:FAIL  P:FAIL  P:FAIL  P:FAIL  P:FAIL   --           D:SYS_ERR         
G-pre TOLERANCE_UNRESOLVABLE (U >= tol, independent of m): c1, c2, c3, c8
sys-check SYSTEMATIC_ERROR_INDICATED (diagnostic, n_legs = 4; changes no verdict): c9, c11
SPLIT (A-G): c1, c2, c4, c5, c6, c7, c9, c10
G differs from every A-F cell: c1, c2
SPLIT (A-F, as before): c1, c2, c4, c5, c6, c7, c9, c10
SPLIT (A-G) on non-VOID cells only: c1, c2, c4, c9, c10
SPLIT (A-C only, as before): c1, c4, c6, c10
```

SPLIT rows (A-G): c1, c2, c4, c5, c6, c7, c9, c10; non-VOID splits: c1, c2, c4, c9, c10. G differs
from every A-F cell on c1 and c2 (I:UNRES). TOLERANCE_UNRESOLVABLE flags c1, c2, c3, c8, where
U = 3e-6 >= tol = 1e-6: G cannot prove conformance there whatever m is. c9-c11 (U = 2e-7 < tol =
1e-5) reach G's other three outcomes: CLOSED_WITHIN, OK at exactly zero, FAILED. The systematic
check flags c9 and c11 (|m| > k*sigma*sqrt(4) = 4e-7); on c9 tolerance is met and the flag says
the loop's error is not random.
