<!-- Template for REVISED_REPORT.md. Every count is a placeholder key in braces, filled by tools/report.py from registry/. validate.py lints this file: a digit outside a key, an id, a date or a legal citation is an error. Edit this file, then run tools/report.py. -->
# Revised report -- WO-REG-1 regulatory uncertainty registry (pilot)

## 0. How to read this

```text
every number      filled from registry/ by tools/report.py; validate.py re-renders and compares bytes
branch tags       [holds]  [scope-limited]  [no data]  [absent]   (WO acceptance: kept separate)
[INFERENCE]       a step this report takes that no tool computes
scope (NCR-N21)   the coded sample ({n.sample} rows) was drawn from permissive anchors; every count over
                  it is a count inside that sample. R8 rows and Frame C2 are reported apart, never pooled
coder             every PROPOSED field is one coder (ACT-REGISTRY) unless a second coding covers it (NCR-N24)
```

No sentence here grades an agency or a person. A status such as `NON-CONFORM: below floor` is the
output of RUS-0.2 or RUS-0.3 applied to recorded inputs; it carries the standard's assumptions with it.

## 1. What the registry holds

| object | count | | object | count |
|---|---|---|---|---|
| DECISION | {n.decision} | | EVIDENCE | {n.evidence} |
| NON_DECISION | {n.non_decision} | | SOURCE | {n.source} |
| REVERSAL | {n.reversal} | | ACTOR | {n.actor} |
| OUTCOME | {n.outcome} | | AUTHORITY | {n.authority} |
| ENDPOINT_ABSENCE | {n.endpoint_absence} | | CONFLICT | {n.conflict} |
| SUBSTANCE | {n.substance} | | NCR | {n.ncr} |
| ENDPOINT | {n.endpoint} | | CHANGE | {n.change} |
| all objects | {n.objects} | | edges | {n.edges} |

Pinned inputs re-hashed on every run: {pins.inputs}.

### Verification ledger (four-state rule, `tools/check_citations.citation_state`, imported)

| claim rows | searched this session | VERIFIED | CORRECTED | NOT_FOUND | UNREACHABLE |
|---|---|---|---|---|---|
| {led.rows} | {led.searched} | {led.verified} | {led.corrected} | {led.not_found} | {led.unreachable} |

Depth is search-index at most: the container's DNS refuses publisher hosts, so no primary page was
opened. An unsearched row is UNREACHABLE with the reason stated, never NOT_FOUND.

## 2. Findings

### F1. Annex A reproduces from its own standard [holds]

RUS-0.2 implemented from the pinned standard text (`tools/grade.py`) and run on the annex's own
inputs: {annex.mismatches} mismatches over {n.sample} rows. Three reproduction rules are the
registry's reading, not the annex's statement: R3 applied where the annex status is
`STATUTE/JUDICIAL-EXCEPTION`; R1 applied only where it sets market status (NCR-N06); R5 on A06.

### F2. One-directional non-conformity, by basis [scope-limited]

The annex grades rows on a mixed basis: D02 and A10 on the legal outcome, C04 on the agency action
(NCR-N02). Every row is graded on both, beside the annex.

{table.tallies}

```text
over_reachable   rows where some actual direction would fire R2's over-restrictive branch
over_possible    rows where the row's OWN actual could fire it under some matrix
                 (C_restrict > C_permit, matrix floor, no R3, actual D3 or above)
reading          HOLDS needs over_possible above zero; at zero the absence of over-restriction is fixed by the rows
                 and reads HOLDS_UNTESTABLE (REVIEW_v3 R13)
```

- Annex basis: over-restrictive rows {t.rus02.annex.src.over_restrictive}, over_possible
  {t.rus02.annex.src.over_possible}: `{t.rus02.annex.src.reading}`.
- Action basis: over-restrictive row(s) {t.rus02.action.src.over_rows}: `{t.rus02.action.src.reading}`.
- Outcome basis: `{t.rus02.outcome.src.reading}`.

### F3. Calibration sweep [holds] / M6 [no data]

{table.sweep}

- M4 and M6 state no U3 row in the bundle. M4's row is the unique non-decreasing row that reproduces the
  published counts (NCR-N08). No non-decreasing row reproduces M6 under its stated column rule (NCR-N07).
- M3's two labels agree once its column is counted from one: every row read in the zero-gap column.
- Below-floor range: {st.sweep_below_min}-{st.sweep_below_max} of {n.sample} across the variants reproduced
  and M7; M6's published value widens the top only if taken as stated.

### F4. RUS-0.3, one switch at a time [holds as computation; RUS-0.3 itself PROPOSED]

{table.components}

```text
+M7     symmetric tolerance: one class below the floor conforms by margin (REVIEW_v2 R7)
+SUB    substitution rule (not the cost-bearer Rule S of F6; NCR-N25): an "alternatives exist" credit stands only for a named alternative graded below
        the case's own C_permit grade; otherwise C_restrict is raised one point (REVIEW_v2 R9)
+R6     self-sealing overlay; R6b lowers U one class for a loosening of a self-sealing restriction (D01)
+R1L    NCR-N06's literal reading of R1 (level-setting rows included)
```

The action-basis reading is `{cmp.action.RUS-0.3.reading}` under RUS-0.3 and `{cmp.action.RUS-0.2.reading}`
under RUS-0.2: the over-restrictive row is A10 on both. On the outcome basis every variant reads
`{cmp.outcome.RUS-0.3.reading}`. Below-floor counts under RUS-0.3: action {cmp.action.RUS-0.3.below},
outcome {cmp.outcome.RUS-0.3.below}; the drop from RUS-0.2 comes from M7. SUB alone changes
{sub.action.statuses} statuses but lowers {sub.action.floors} floors one class ({sub.action.floor_rows}); those rows sit
two classes below their RUS-0.2 floor and one below the SUB floor, so they conform only with M7 on.
A tally that does not move is not a rule that does nothing.

### F5. Restrictive-side candidates (R8) [scope-limited: selected on direction, one coder]

| row | standard | gap | floor | actual | status | R6 |
|---|---|---|---|---|---|---|
| D03 | RUS-0.2 | {r8.D03.rus02.gap} | {r8.D03.rus02.floor} | {r8.D03.rus02.actual} | {r8.D03.rus02.status} | {r8.D03.rus02.r6} |
| D03 | RUS-0.3 | {r8.D03.rus03.gap} | {r8.D03.rus03.floor} | {r8.D03.rus03.actual} | {r8.D03.rus03.status} | {r8.D03.rus03.r6} |
| D04 | RUS-0.2 | {r8.D04.rus02.gap} | {r8.D04.rus02.floor} | {r8.D04.rus02.actual} | {r8.D04.rus02.status} | {r8.D04.rus02.r6} |
| D04 | RUS-0.3 | {r8.D04.rus03.gap} | {r8.D04.rus03.floor} | {r8.D04.rus03.actual} | {r8.D04.rus03.status} | {r8.D04.rus03.r6} |

The branch REVIEW_v2 R8 said could not fire does fire on rows built to test it. These rows show the
standard can return over-restriction; they are not evidence about the sample's rate of it.

### F6. Cost-bearer and direction, bivariate [no data under Rule S]

| frame | rule | concentrated restrictive/n | diffuse restrictive/n | Fisher p (two-sided) | reading |
|---|---|---|---|---|---|
| source frame | L | {bv.source_frame.L.conc} | {bv.source_frame.L.diff} | {bv.source_frame.L.p} | {bv.source_frame.L.reading} |
| source frame | S | {bv.source_frame.S.conc} | {bv.source_frame.S.diff} | {bv.source_frame.S.p} | {bv.source_frame.S.reading} |
| DECISION only | L | {bv.decision_only.L.conc} | {bv.decision_only.L.diff} | {bv.decision_only.L.p} | {bv.decision_only.L.reading} |
| DECISION only | S | {bv.decision_only.S.conc} | {bv.decision_only.S.diff} | {bv.decision_only.S.p} | {bv.decision_only.S.reading} |

"Not testable" is a property of the cell counts, not a null result (REVIEW_v2 R11).

### F7. Restrictive actions and forcing [scope-limited]

One list from `action_direction`: {fc.list} ({fc.n} rows). External forcing (statute, court, failed
confirmatory trial, post-market litigation, scheduled rule on new data, unmet post-market requirement):
{fc.forced} of {fc.n}. Not external: {fc.discretionary} (the agency's own study; AB 418 recorded as a
contested candidate, NCR-N03). With Frame C2's pentachlorophenol (discretionary): {fc.all_forced} of
{fc.all_n}. Reversed toward permissive from this list: {rv.2016.toward}.

### F8. Frame C2 (EPA, 2022) [holds at notice level; document level absent]

{c2.n} rows: {c2.merit} decisions on the merits ({c2.permissive} permissive, {c2.restrictive} restrictive:
pentachlorophenol, cancellation required) and {c2.na} case closures coded NA. Document-level coding of the
decisions was not run (gap FR-C2-DOCS).

### F9. Reversals [scope-limited]

| reading | restrictive -> permissive: n, median, years | permissive -> restrictive: n, median, years | exact Mann-Whitney U, p |
|---|---|---|---|
| D01 from 2016 (D03) | {rv.2016.restrictive_to_permissive.n}, {rv.2016.restrictive_to_permissive.median}: {rv.2016.restrictive_to_permissive.times} | {rv.2016.permissive_to_restrictive.n}, {rv.2016.permissive_to_restrictive.median}: {rv.2016.permissive_to_restrictive.times} | {rv.2016.U}, {rv.2016.p} |
| D01 from 1970 | {rv.1970.restrictive_to_permissive.n}, {rv.1970.restrictive_to_permissive.median}: {rv.1970.restrictive_to_permissive.times} | {rv.1970.permissive_to_restrictive.n}, {rv.1970.permissive_to_restrictive.median}: {rv.1970.permissive_to_restrictive.times} | {rv.1970.U}, {rv.1970.p} |

C03 (a permissive action vacated by a court, product left on the market) is in neither group. The
p value depends on which anchor D01 is measured from; the anchor is a reading, not a fact, and both are
shown. [INFERENCE] Faster loosening than tightening in these eight is consistent with the cost-bearer
branch at the reversal stage and is not a test of it: the reversals were selected through a sample drawn
on permissive anchors.

### F10. Cross-agency mirror pairs [holds]

{mi.divergent} of {mi.n} pairs diverge, {mi.ge2} by two or more points (recomputed from the v1 table the
source's own sentence summarizes; NCR-N10).

### F11. Symmetry [holds as computation]

Profile = (U grade, C_permit grade, C_restrict grade) [CHOICE]. Pairs with a matched profile and different
directions: {sym.src.pairs} on source C_restrict, {sym.reg.pairs} on the registry's coding. SYMMETRY-FAIL
(neither member carries R1, R3 or R5): {sym.src.fail} and {sym.reg.fail}. Of these, pairs whose members
differ in cost group: {sym.src.fail_mixed_group} and {sym.reg.fail_mixed_group}, so the symmetry fails do not
speak to the cost-bearer reading.

### F12. Single-failure flags over {ch.graded} graded cases [holds]

| flag | cases |
|---|---|
| NO_LOCATED_SOURCE | {ch.no_located_source} |
| ONE_SOURCE | {ch.one_source} |
| ONE_CODER | {ch.one_coder} |
| ORIGINATOR_ONLY (action direction) | {ch.originator_only} |
| AUTHORITY_GAP (a citation in the chain UNREACHABLE) | {ch.authority_gap} |

### F13. Gaps as nodes [absent / no data]

| gap | nodes |
|---|---|
| endpoint absences | {gap.absences} |
| non-decisions | {gap.non_decisions} |
| local-only ids (DTXSID / ontology lookup not run) | {gap.unmapped_ids} |
| authority citations UNREACHABLE | {gap.authority_gaps} |
| unlocated inputs | {gap.unlocated_inputs} |
| frames named, not loaded | {gap.frames} |
| decisions with no located disclosure record (never "no conflict") | {gap.disclosure} |
| ledger rows not searched | {gap.ledger_unsearched} |

### F14. Graded approach: did verification scale with consequence? [holds]

| tier | cases | ledger rows behind them | located (VERIFIED or CORRECTED) | share |
|---|---|---|---|---|
| T1 (C_permit C4) | {tier.T1.cases} | {tier.T1.rows} | {tier.T1.located} | {tier.T1.share} |
| T2 (C_permit C3) | {tier.T2.cases} | {tier.T2.rows} | {tier.T2.located} | {tier.T2.share} |
| T3 | {tier.T3.cases} | {tier.T3.rows} | {tier.T3.located} | {tier.T3.share} |

Tiers are assigned; verification effort in this session was spent on load-bearing rows, not by tier.
The mapping of "graded approach" to its source clause is in `schema/QA_MAPPING.md`.

### F15. Second coder [absent]

State: `{k2.state}` ({k2.reason}). The ten-row packet and the contamination probe are pinned in
`second_coder/`; the probe was answered before the packet was sent. Kappa per field is computed by
`tools/stats.py` when the coding arrives.

### F16. Frame A wording (REVIEW_v1 R1) [holds]

The pinned v2 report carries the corrected Frame A statements: {text.r1_found} of {text.r1_n} checked
phrases found once each (`tools/stats.py` TEXT_CHECKS).

## 3. Statements in the source that the registry corrects

{table.statements}

ST-17 is withdrawn, not corrected: NCR-N09 is REJECT, because the pinned sweep table lists M0 once.

## 4. NCR register ({ncr.review} review items, {ncr.audit} audit items)

Dispositions: ACCEPT {ncr.accept}, MODIFY {ncr.modify}, REJECT {ncr.reject}. Open: {ncr.open_ids}.

{table.ncr}

Every audit NCR rests on one coder and is flagged single-failure. Every change to a recorded value is in
`CHANGE_LOG.md` with its NCR.
