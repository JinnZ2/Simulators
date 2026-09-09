# anchor-position

WORK ORDER — ANCHOR POSITION AND MEASURAND CROSSING, delivered verbatim in
`WORK_ORDER.md` and built here. Does a model produce defects whose QUANTITY
differs from the quantity a method measures, as a function of where the
prompt anchors — at the method (ARM M) or at the decision the claim is cited
to support (ARM D)? A counting outcome with a stated null; not a benchmark.

```
cases.jsonl ──► prompts.py ──► <case>.<arm>.txt  (M, D, M+)  + order.jsonl (seeded)
                                      │
                         operator runs each file in a FRESH session, logs the raw
                         response into responses.jsonl  (no model call in this folder)
                                      │
responses.jsonl ──► score.py ──► per case per arm: n_entries, distinct_measurands,
                    │            native_hit, crossing_count   (under BOTH lists)
                    ├── transforms.json      (primary list, published)
                    ├── transforms_alt.json  (second list; N4 = disagreement)
                    └── claims AP-1..AP-6, nulls N1..N5, decision strings logged
```

## Run

```bash
python3 prompts.py cases.jsonl out_dir [seed] [--mplus-tail]
python3 score.py cases.jsonl responses.jsonl [codings.jsonl]
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
  (section 9). **No response in this folder came from a model**: the two
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
  `unknown` so a reader can extend the list and rescore.
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
  evidence beside the verdict, under each list. Control cases are excluded
  from the paired claims AP-2, AP-3, AP-6 and named in the output
  (`[CHOICE 6]`): on a control D == M is the correct reading by
  construction, so AP-2's refutation condition as written fires on the
  control section 8 requires. N1 is `NOT_EVALUATED` without a
  `codings.jsonl` (practitioner recognition is a human coding, reported as
  a rate, gating nothing). N2 fires when a control's D arm flags a gap. N3
  reports M-arm crossings by field. N5 reports the form-ok rate per arm and
  fires only when both M and D fall below `FORM_FLOOR` (`[CHOICE 4]`).
  `D_LEVEL` for AP-3 is `M+ ≥ D` (`[CHOICE 5]`). Every choice is printed in
  the report header.

## State

Unrun on any model. Both fixture worlds exist so that every verdict branch
is shown reachable: in `responses.constructed.jsonl` M yields no crossings,
D yields several, M+ stays at M and the control reads native; in
`responses.confound.constructed.jsonl` M+ reaches D-level on `sc-01`
(AP-3 REFUTED), the control D flags a gap (N2 FIRES), one M response breaks
form and carries a foreign quantity (N5 numerator, N3), a C row returns its
supplied measurand (AP-5 REFUTED) and a B row is a strict subset (AP-4
holds). AP-6 is UNRUN in both, since one family is one family. The
operator's steps, in order: replace `ctl-01` with a hand-built control, add
cases from at least three more unrelated literatures, run each prompt file
cold, log responses, score. Claims in `CLAIM_TABLE.md` (`APM_`). Stdlib
only, parses under 3.9, phone-buildable, CC0.
