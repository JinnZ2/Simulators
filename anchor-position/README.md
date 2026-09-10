# anchor-position

WORK ORDER — ANCHOR POSITION AND MEASURAND CROSSING, delivered verbatim in
`WORK_ORDER.md` and built here; a second order, WORK ORDER — anchor-position/
audit fixes (`WORK_ORDER_2.md`, verbatim), audited for staleness against
the folder and then applied — eleven items, nine BUILD and two ORDER, the
ORDER items behind flags that default off (`APM_012..APM_023`). Does a model produce defects whose QUANTITY
differs from the quantity a method measures, as a function of where the
prompt anchors — at the method (ARM M) or at the decision the claim is cited
to support (ARM D)? A counting outcome with a stated null; not a benchmark.

```
cases.jsonl ──► prompts.py ──► <case>.<arm>.txt  (M, D, M+; M_D under --arm-md)  + order.jsonl (seeded)
                                      │
                         operator runs each file in a FRESH session, logs the raw
                         response into responses.jsonl  (no model call in this folder)
                                      │
responses.jsonl ──► score.py ──► per case per arm: n_entries, distinct_measurands,
                    │            native_hit, cc_min / cc_max / cc_order   (under BOTH lists,
                    │            each list scored TWICE: unknown = residue, unknown = vocabulary)
                    ├── transforms.json      (primary list, published)
                    ├── transforms_alt.json  (second list; N4 = disagreement)
                    ├── claims AP-1..AP-6 (SUPPORTED / REFUTED / UNRUN at both ends, else BAND)
                    ├── nulls N1..N5 (+ N2_first / N2_rest under --n2-first)
                    ├── ABSENT per arm, replicate collisions, self-label vs scorer
                    └── header: every [CHOICE n] (1..12) and every [FLAG] ON/off
```

## Run

```bash
python3 prompts.py cases.jsonl out_dir [seed] [--mplus-tail] [--arm-md]
python3 score.py cases.jsonl responses.jsonl [codings.jsonl] [--arm-md] [--n2-first]
python3 score.py --selftest
```

## What is here and what is not

- **Cases.** `sc-01` and `mp-01` are transcribed from the order. `ctl-01` is
  the control section 8 requires (native == decision measurand) and does not
  supply; it is CONSTRUCTED here and model-authored, so it carries the order's
  own caveat on model-built cases and is the operator's to replace. Its
  decision string names no unit and no measurand (asserted).
- **Prompts.** ARM M and ARM D are the order's section 4 text, verbatim —
  the selftest checks every line against `WORK_ORDER.md`. ARM M+ is the AP-3
  confound the order says SHOULD BE RUN: ARM M with D's one sentence ("This
  claim is cited to justify [DECISION].") inserted after the claim+method
  block, so M+ and D differ only in the question (`[CHOICE 1]`;
  `--mplus-tail` appends it after the last line instead). The block carries
  claim and method only (`[CHOICE 2]`): no prompt contains the native, M
  never contains the decision, M+ differs from M by exactly one line — all
  asserted. Arms B (cued follow-up) and C (foreign measurand by name) have
  no verbatim text in the order and are NOT reconstructed; the scorer
  accepts operator-supplied `B` and `C` rows (C rows must carry
  `supplied_measurand`) and evaluates AP-4 / AP-5 on them.
- **Responses.** `responses.jsonl`, one row per (case, arm) run:
  `case_id, arm (M | D | M+ | B | C), model, family, version, date, response
  (raw), decision (verbatim, required on D and M+), session, order_index`.
  A D or M+ row whose `decision` is not the case's string is refused, so the
  string the result was produced under is always the string logged
  (section 9). **No response in this folder came from a model**: the three
  files under `fixtures/` are authored worlds, labelled so in their first
  row, and every number in `samples/` is about them.
- **Scorer.** `normalize.py` implements section 6 mechanically: aliases
  (longest phrase first, replaced spans held so a shorter alias cannot fire
  inside a longer one) → tokens → drop units, articles, hedges and every
  transform-marker token → the residue is the core. Two cores are one
  measurand if equal, or if one is a subset of the other and the extra
  tokens are all UNCLASSIFIED residue; an extra token that is measurand
  vocabulary (a canonical alias value: `hazard`, `migration`, `co2e`) makes
  a different quantity. Without that clause a one-token native like
  `{polymer}` absorbed every quantity mentioning polymer — the first draft
  did, and `samples/` before the fix showed `polymer-specific hazard`
  grouped as native. A core emptied by stripping is `unresolved`, counted
  apart; a surviving token outside the alias vocabulary is printed as
  `unknown` so a reader can extend the list and rescore — **and is scored
  both ways** (`[CHOICE 9]`, WORK_ORDER_2 W3): once as residue, the floor
  `cc_min`, and once as measurand vocabulary, the ceiling `cc_max`. A
  quantity like `soc yield` against the SOC native is native at the floor
  and a crossing at the ceiling. A response with no entries scores `None`
  on every crossing field — ABSENT, counted per arm, skipped by every
  comparison, never zero (`[CHOICE 12]`, W1). Parentheticals are stripped
  as glosses or units (`[CHOICE 8]`).
- **Two published lists.** `transforms_alt.json` differs from
  `transforms.json` in exactly one declared move: `concentration`/`density`
  and the threshold words are measurand vocabulary rather than transform
  markers. N4 is their disagreement, per (case, arm), and it fires on the
  main fixture world — the transform list is doing the work, as the order
  says.
- **Arithmetic.** `crossing_count = distinct_measurands − native_groups_hit`
  (`[CHOICE 3]`). The order subtracts a 0/1 `native_hit`; a native stated as
  `count OR mass` names two measurands, and an M response with entries on
  both would then read one crossing. Both are printed (`crossing` and
  `cc_order`). `crossing_count` on no entries is `None`, never 0, and is
  registered in `tools/known_answer.py`.
- **Claims and nulls.** AP-1..AP-6 each SUPPORTED / REFUTED / UNRUN with the
  evidence beside the verdict, under each list — at BOTH ends of the band,
  and BAND with both ends printed when the ends disagree (N-W3, reported
  as the result; it fires on the delivered main world's AP-1). Paired
  claims run on every replicate pair, with collisions counted and printed
  (`[CHOICE 10]`, W4); AP-3 runs only on triples where `cc(D) > cc(M)`,
  the rest listed as uninformative (`[CHOICE 11]`, W2); AP-4 compares
  measurand groups, not strings (W5). Control cases are excluded
  from the paired claims AP-2, AP-3, AP-6 and named in the output
  (`[CHOICE 6]`): on a control D == M is the correct reading by
  construction, so AP-2's refutation condition as written fires on the
  control section 8 requires. N1 is `NOT_EVALUATED` without a
  `codings.jsonl` (practitioner recognition is a human coding, reported as
  a rate, gating nothing). N2 fires when a control's D arm flags a gap. N3
  reports M-arm crossings by field. N5 reports the form-ok rate per arm and
  fires only when both M and D fall below `FORM_FLOOR` (`[CHOICE 4]`).
  `D_LEVEL` for AP-3 is `M+ ≥ D` (`[CHOICE 5]`, read by the comparison; `gt`
  flips a tie). Every choice is one entry in `score.CHOICES` (ids 1..12),
  printed in every report header and cited here by id (W7). A **self-label
  vs scorer** block prints, per D-form entry, the model's own
  `measured_by_method` against the scorer's native membership — a rate per
  case that gates nothing (W11).
- **Flags — ORDER items, default off, OPEN until the operator signs.**
  `--arm-md` (W9, `APM_020`): ARM M_D is M's question with D's three-field
  schema and no decision, so anchor and output schema can be separated —
  M and D differ in both, and M+ holds M's schema. `prompts.py --arm-md`
  emits `<case>.M_D.txt`; the scorer refuses an M_D row unless the flag is
  on, then parses it in D form and prints an M_D reading per (case,
  model): M_D ~ D → the schema carries the effect, M_D ~ M → the anchor
  survives the schema control. Off, every report carries N-W9: the AP-3
  finding stays "anchor OR schema". `--n2-first` (W10, `APM_021`): N2 on
  entry 1 of a control D response only, entries 2..n as `N2_rest`, on the
  order's prediction that D's *repeat the three fields for every other
  quantity* pushes a second entry on a control. Both flags are printed in
  the header ON/off.

## Sibling build

`anchor-measurand-crossing/` is a second independent build of the same
order from another session, landed on `main` the same day. Same delivered
text, same two transcribed cases, and both builds chose lead action-level
compliance as the control and D's position for the M+ sentence — a
convergence of one builder class on one corpus, not two confirmations
(`APM_011`). They differ in scoring form (band with `UNGROUPED` there,
point count with `unknown` tokens here) and in how the control is held
(excluded by the loader there, admitted and excluded from paired claims
here). Neither is merged into the other.

## State

Unrun on any model. Three fixture worlds exist so that every verdict branch
is shown reachable (`APM_002` tabulates them per claim and per world): in `responses.constructed.jsonl` M yields no crossings,
D yields several, M+ stays at M and the control reads native; in
`responses.confound.constructed.jsonl` M+ reaches D-level on `sc-01`
(AP-3 REFUTED), the control D flags a gap (N2 FIRES), one M response breaks
form and carries a foreign quantity (N5 numerator, N3), a C row returns its
supplied measurand (AP-5 REFUTED at the floor, BAND with the ceiling) and
a B row is a strict subset (AP-4 holds); in
`responses.refute.constructed.jsonl` (WORK_ORDER_2 W6) a second family's
D reads native only on `mp-01` (AP-2 and AP-6 REFUTED), a B row is M
reworded plus one new measurand (AP-4 REFUTED on groups), M+ ties D (the
`D_LEVEL` case), one D row is blank (ABSENT) and one cell holds two D
rows (a collision). `samples/*.before_after.diff` carry the delivered
worlds' reports before and after the second order, with the main world's
AP-1 moving SUPPORTED → BAND (`APM_014`). The
operator's steps, in order: replace `ctl-01` with a hand-built control, add
cases from at least three more unrelated literatures, run each prompt file
cold, log responses, score; and sign or decline the two flagged arms. Claims in `CLAIM_TABLE.md` (`APM_`). Stdlib
only, parses under 3.9, phone-buildable, CC0.
