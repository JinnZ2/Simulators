<!-- SPDX-License-Identifier: CC0-1.0 -->
# EXPECTED — FWO-15, enclosure as corpus validity limit

Written and committed with the order and BEFORE any module, fixture or seed
case of FWO-15 was coded (key-holder rule 1, the fd198aa arrangement: order
plus this file, no module). Nothing here is edited after that commit. A
prediction that fails is recorded as failed in `CLAIM_TABLE.md`, and this
file stays as written.

The order itself is RECONSTRUCTED (2026-10-04) from a memory object that is
not in this tree. If the original 2026-09-27 text surfaces it supersedes the
order, and every prediction below is re-scored against the original.

Every line is PROPOSED unless tagged otherwise. Where the order states an
expectation it is copied and marked (order's). Where it states none, the
expectation is this session's and says so.

## What was done before this file

The order's section 5 prior-art check was RUN before this file, by web
search (result snippets; full texts sit behind the egress allowlist). Its
results are recorded in `FWO-15_PRIOR_ART.md` in the next commit. One
result bears on a prediction below (E15.3), so that prediction is NOT
blind and is marked so.

## Key-holder rule, as it will be scored

- Rule 1: this commit precedes every FWO-15 module. Expected: MET.
- Rule 2: inputs from an external document with SOURCE. Expected: UNMET
  for Build A (no corpus is reachable) and UNMET for Build B unless a
  seed case is sourced (see E15.5).
- Rule 3: at least one fixture per instrument built to FAIL. Expected: MET
  for both modules.
- The same agent writes the fixtures and their expected verdicts. Every
  fixture result is therefore REGRESSION, not validation, and the suite
  prints that word on its summary line.

## Thresholds fixed here, before any code

- Case-count floor, Build A: an arm's caveat rate is reported only when
  at least 20 coded studies in that arm carry E4 in {YES, NO}. Below the
  floor the arm reads UNMEASURED with its n printed. (this session's)
- Caveat rate = YES / (YES + NO). E4 = ABSENT is counted and printed apart
  and never enters the denominator. A rate with an empty denominator is
  None, never 0. (this session's)
- "<<" (order's word) is fixed as: human-arm Wilson 95% upper bound below
  the animal-arm Wilson 95% lower bound. Overlapping intervals with an
  absolute difference of at most 0.10 read NO_GAP. Overlapping intervals
  with a larger difference read INDETERMINATE, a state the order does not
  list and which is reported, not collapsed into either. (this session's)
- The two animal arms (captive-animal, production-animal) are compared to
  the human arm separately and are never pooled. (this session's)

## Build A — enclosure_caveat_register.py

- E15.0 (order's): ships DESIGN_WRITTEN. No corpus is in hand; the real-run
  branch is UNMEASURED.
- E15.1 (order's hypothesis, HERS): on a real corpus the human-arm caveat
  rate is << each animal-arm rate (GAP_CONFIRMED under the threshold above).
  Not scorable here.
- E15.2 (order's): the modal human-arm E2 value is ABSENT. Not scorable here.
- E15.3 (this session's, NOT blind, informed by the prior-art run): if a
  real corpus includes the cross-cultural market-integration sub-literature,
  that sub-literature returns E2 declared (food leg only) at a rate above
  the rest of the human arm, so the first real result is more likely
  SCOPE_LIMITED or INDETERMINATE than a clean GAP_CONFIRMED.
- E15.4 (this session's): in a captive-animal arm drawn from journals that
  endorse a housing-and-husbandry reporting item, E2 is declared (not
  ABSENT) in at least 80% of studies. E4, the CAVEAT, is expected to be
  much rarer than E2 in the animal arm too: declaring housing is not the
  same act as caveating generalization from it. Predicted animal-arm caveat
  rate band: 0.10 to 0.50. Not scorable here.

## Build B — coupling_gradient.py

Seed rows, counted as five: Amish; German village groups; Dutch;
Indigenous peoples; barter 1950s-1970s. (this session's count of the
order's seed lines)

- E15.5 (this session's): at most ONE seed row gets a dated, sourced
  coupling instrument in this session. The candidate is the barter row,
  whose instrument is a federal reporting rule and is the kind of thing
  that carries a date. HELD count predicted at least 4 of 5.
- E15.6 (this session's): behavior_before and behavior_after are sourced
  for ZERO seed rows. Every entered seed row reads shift NOT_EVALUABLE.
- E15.7 (this session's): any seed row that does enter carries an undated
  or coincident confound (mechanization, roads, media) and so could not
  read anything but CONFOUNDED_BEYOND_READ even if its behavior fields
  were filled.
- E15.8 (order's rule, asserted not predicted): a case with no confound
  column is rejected; an undated case is HELD; the pre-coupling record is
  labelled CONTROL; every output prints the survivor-filter line.

## Scope, asserted not predicted

- FWO-11 (`lag_count.py`) and FWO-9 (`question_space.py`) are referenced,
  not rebuilt: no FWO-15 module defines a function or class name that
  either of them defines.

## Fixture plan (all REGRESSION)

Build A: a gap world, a no-gap world, a scope-limited world, an
under-floor world, and a FAIL fixture whose study is coded before its
sampling frame was declared (must be refused). Build B: an undated case
(must be HELD), a case with no confound column (must be rejected), a dated
case whose confound coincides with the coupling date (must read
CONFOUNDED_BEYOND_READ), a visible-shift case, a not-visible case.
