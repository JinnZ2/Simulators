<!-- SPDX-License-Identifier: CC0-1.0 -->
# EXPECTED — FABLE WORK ORDER 2026-09-27b (FWO-8 .. FWO-14)

Written and committed BEFORE any demo input, fixture or module of this order
was coded (key-holder rule 1). The commit that lands this file is the
registration; its id is cited in `CLAIM_TABLE.md` for every claim that
scores a prediction below. Nothing in this file is edited after that commit;
a prediction that fails is recorded as failed in the claim table, and this
file stays as written.

Every line is PROPOSED unless tagged otherwise. Where the order states an
expectation, it is copied; where the order states none, the expectation
registered here is this session's and says so.

## Key-holder rule, as it will be scored

For each instrument: rule 1 (this commit precedes coding), rule 2 (demo
inputs from an external document with SOURCE, not constructed to fit), rule 3
(one fixture built to FAIL). A held prediction names which of 1-3 were met.
Rule 2 is NOT expected to be met by FWO-8: its inputs are the three FWO-5
cases, which are CONSTRUCTED / CARRIED, so any FWO-8 hold is scored with
rule 2 unmet and said so. Rule 2 is NOT expected to be met by FWO-9, FWO-10,
FWO-11 or FWO-13 either: every external document those items need sits
behind the egress allowlist, and a value recalled from memory is not a
sourced value. The register of what was reachable is in `SOURCES.md`.

## FWO-8 edge taxonomy

- E8.1 (order's, PROPOSED): across the three FWO-5 demos, `edge_class` =
  `DIRECT` is empty or near-empty. "Near-empty" is fixed here as at most
  ONE route across all three cases. If any DIRECT row appears it is
  recorded by name.
- E8.2 (this session's): every CONVERTED route in the three cases takes
  `INSTITUTIONAL`, `ACCESS` or `TEMPORAL`; `RECURSIVE` appears at most once
  (the grant-purchased instrument in case (b) is the candidate); nothing
  takes `MEASUREMENT` in cases (a) or (c).
- E8.3 (order's hard constraint, will be asserted not predicted): a route
  coupled on SURVIVAL only scores INDEPENDENT at the selection layer; no
  function returns one number combining the two sides.
- E8.4 (order's carried question, answer registered): FWO-5 case (b)'s
  independent dependency is `data_access` alone (the open-dataset route
  discharges in citation). `publication` is NOT independent on the FWO-5
  reading: its preprint route is `none/none`, which FWO-2 reads as
  independent per [CHOICE 3], but the dependency reads ENCLOSED_PLURALITY
  because the APC route dominates. The registered answer is therefore
  `data_access` at the row level and `data_access` + `publication` at the
  route level; the first run of FWO-5 printed `independent rows
  ['data_access', 'publication']` at 0.200 (2 of 10), so the ROW-level
  answer registered here is expected to be REFUTED by the recorded render
  and the route-level one to hold. Both are written down so the failure
  is scorable.
- E8.5 (two-layer mis-placement): FWO-5's route schema carries
  medium_of_account and medium_of_settlement and its conversion_point
  vocabulary carries six points; the mis-placement is that a conversion at
  `input_purchase` is recorded on the settlement field. Expected: in case
  (c) every `input_purchase` row has settles_in == obligation_medium ==
  USD, so the account/settlement pair cannot distinguish it from a
  `settlement` row; the new field that separates them is `edge_class`,
  and every case-(c) `input_purchase` row is expected to read `ACCESS`.

## FWO-9 question-space column

- E9.1: no numeric loss estimate exists in the module (asserted, not
  predicted).
- E9.2 (this session's): the class "question arising only from a
  constraint the funded population does not live under" attaches to at
  least `credential` and `publication`; `tax` closes at least
  "instrument needing no funder"; `input_purchase` closes "result with no
  product downstream". Every other cell may read UNKNOWN.

## FWO-10 three-standards register

- E10.1 (order's, PROPOSED): the applied-to-the-medium column reads
  NOT_APPLIED in all three seed rows. Expected to be NOT_EVALUABLE here
  rather than held or refuted: no standard can be fetched, so the column
  reads UNKNOWN (not searched), which is not NOT_APPLIED. A hold on this
  prediction from memory alone would be `HELD_UNINDEPENDENT` and is not
  claimed in advance.
- E10.2: the prior-art check (common-mode / N-1 applied to a currency or
  payment system) is NOT_RUN at the document level; from memory the
  payment-system resilience literature addresses the plumbing (settlement
  systems, operational continuity) and not the medium. Recorded as
  CARRIED_FROM_MEMORY, unverified.

## FWO-11 lag count

- E11.1 (order's): the Antikythera mechanism reads
  RECOVERED_NOT_REDISCOVERED.
- E11.2 (this session's): of the six seed cases, at most two read FULL
  with a dated reach; at least one reads UNKNOWN on the reach date.
- E11.3: every seed date is UNSOURCED (recalled, no document reached), so
  the lag distribution over SOURCED rows is empty and says so; the
  distribution over unsourced rows is printed apart and never merged.
- E11.4: the survivor-filter statement appears in every render header
  (asserted).
- E11.5: no seed passes the settlement check into `independent`; every
  seed reads CANDIDATE.

## FWO-12 unpaid maintenance

- E12.1 (order's, PROPOSED): the discretionary-effort literature measures
  attitude by survey only. NOT_EVALUABLE here (no search runs); from
  memory, the engagement instruments are surveys and organisational
  citizenship behaviour is rated by supervisor or self, i.e. also a
  survey; whether any counted-behaviour study exists is UNKNOWN.
- E12.2: the instrument refuses to run on anything but a declared public
  dataset; the design's own constructed fixture reads NOT_RUN for the
  measurand and is used only to show the filter and the prediction check
  can fail.
- E12.3 (order's testable prediction, PROPOSED): unpaid maintenance falls
  as token-coupling rises. Not run. A constructed FAIL fixture is built in
  which it rises.

## FWO-13 tax step

- E13.1: appearances 1 and 2 register (OBSERVED); appearance 3 is
  CANDIDATE and cannot be verified here (egress); expected to stay
  CANDIDATE, neither registered nor dropped, with the memory reading
  (value of donated services is not income to the volunteer under the
  fringe-benefit rules as recalled) recorded as unverified.
- E13.2: the tax row type is its own type, refused if written as an FWO-6
  entry.
- E13.3: the prior-art check (de minimis / fringe-benefit rules treated as
  channel removal rather than compliance) is NOT_RUN; from memory no such
  treatment is recalled, which is an unbounded null and is recorded as one.

## FWO-14 reference-instability series

- DESIGN ONLY. No prediction registered; no row is run. Candidate rows are
  listed as CANDIDATE_UNSOURCED and the direction of G(t) is not assumed.

## Carried audit questions

- Q4 answer registered above at E8.4.
- Q3 (ESP-1 sub-period lead fixture): the first-run result is recorded
  BEFORE any repair, whatever it is. This session's expectation: a trailer
  lead of a fraction of one oscillation period reads TRAILER_LEADS and the
  fixture lands on NEITHER_MODE; if it reads CAB_LEADS or SIMULTANEOUS the
  period ambiguity the sibling's ESP_003 describes is present here and is
  recorded as a finding.
