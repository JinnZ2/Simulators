# ontology-probe

A work order delivered verbatim in `WORK_ORDER.md` and built to it:
whether a term-cut protects, and WHERE it holes. A declared primitive
set is scored against constructions — statements carrying a premise —
by asking a restater to restate each one using only the primitives, and
counting where the premise composes anyway. A counting outcome with a
stated null, not a benchmark.

```
SHAPE_SPEC.md ──reading──► primitives.json ──┐        WORK_ORDER.md §4 ──parse──► prompt
   (absent_by_design: cost, optimum,          │                                     │
    analogy, name, picture, law)              ▼                                     ▼
constructions.jsonl ──hand_built gate──► admitted set (EMPTY here) ──► operator runs, logs JSONL
                                                                                    │
                                          parse 4 fields ◄──────────────────────────┘
                                                │
                              reading per (class, status): PROTECTION / HOLE / USABLE / NARROW / ADDITION
                                                │
                       hole_rate · narrowness · ambient_rate · smuggle_set  +  leak cross-check
                                                │
                                  N1..N5, OP-1..OP-5, family disagreement
```

**No model has been run here.** This environment has no model
endpoint; the session that wrote the primitive declaration has read the
order; and section 7's RESTATER limit — a premise shared between the
restater and the ontology composes without either noticing — is exactly
what a model scoring its own reading would instance. `runs/` holds a
CONSTRUCTED fixture that exercises the scorer; every record says so and
the report banners it. **One real run has been delivered** — the
operator's ontology, constructions and a coded sheet for one family at
one repeat, under `ontologies/substrate-primary/` — and scored as
delivered; see below.

## The operator's run 1

```
ontologies/substrate-primary/
   primitives.json        20 primitives, 9 absent_by_design, physics share 0.65  (hand-declared)
   constructions.jsonl    30 hand-built, 12 CONTROL / 9 TARGETED / 9 AMBIENT      (hand-built)
   runs/claudeopus5_r1.jsonl   CODED SHEET: one family, one repeat, no restatement text

coded sheet ──is_coded()──► adapt_coded() ──► REQUIRED shape (model UNKNOWN, date UNDATED)
                                                     │
              ontology bound from --ontology, checked terms_used ⊆ primitives (30/30)
                                                     │
      leak check NOT_EVALUABLE (no restatement)  ·  missing_primitive → cite_missing()
                                                     │
      absent_coverage(): per declared absence EXERCISED / UNEXERCISED
      aliases.json ──[CHOICE 6]──► terms_added screened for reimport (declared, dated, not blind on run 1)
```

| readout | value |
|---|---|
| hole_rate / narrowness | 0.000 / 0.000 (9 of 9 TARGETED FAILS; 11 of 12 CONTROL COMPOSES) |
| ambient_rate | 0.222 under `[CHOICE 2]`, 0.778 with additions counted as composing |
| smuggle_set | 10 terms, all from AMBIENT and one CONTROL addition |
| cited missing | 13; 11 declared absent; 2 UNDECLARED (`role`, `absent-as-distinct-from-unread`), both on AMBIENT FAILS |
| absent-term coverage | 8 of 9 exercised; `motive` UNEXERCISED (c-013 names it, the restater cited `intent` only) |
| alias reimport `[CHOICE 6]` | 1 hit (c-025 `preference ⇒ interior_state`); audit-declared list, written after run 1, not blind on it |
| scope undeclared `[CHOICE 6]` | c-024 `efficiency`, c-022 `maximize`: no value until boundary / horizon / environment variables / exclusions are stated, and the sheet states none |
| optimize / optimization `[CHOICE 6]` | scope class beside `maximize`, requiring `objective`; `optimal` stays an alias of the absent `better/worse`; neither verb added on run 1 |
| morality import `[CHOICE 6]` | c-025 `market` SCOPE_UNDECLARED (morality), `graded_by` among the missing; `capital` / `monetary` / `value` declared and added by no record — a visible zero; `better` / `worse` aliases of the absent `better/worse`; the class is open |
| N1 / N2 / N5 | do not fire; N3 NOT_EVALUABLE (one repeat) |
| OP-4 / OP-5 | undetermined — second ontology on these thirty not scored |

Direction of OP-3 (ambient > targeted) holds under both `[CHOICE 2]`
readings; its magnitude is the reading. The synonym route the coded
sheet notes on c-025 (`preference` → `interior_state`) is the
restater's declaration, and `aliases.json` turns it into a declared-list
hit on the same coded sheet. `CLAIM_TABLE.md` `OP_009..019`.

## What is here

| file | what |
|---|---|
| `WORK_ORDER.md` | delivered text, verbatim |
| `primitives.json` | one reading of `SHAPE_SPEC.md` as a primitive set: 25 terms, 6 `absent_by_design`, one `undefined`; marked unconfirmed by the author |
| `constructions.jsonl` | three CANDIDATE constructions, `hand_built: false`, not admitted (section 3 forbids model-generated sets) |
| `probe.py` | the instrument: `declare`, `prompt`, `score`; refuses `--selftest` |
| `selftest_op.py` | the checks, both directions; writes `samples/` and `runs/` |
| `runs/constructed.jsonl`, `runs/constructed_constructions.jsonl` | the fixture: 30 constructions (12 / 9 / 9), 2 families × 3 repeats, one leak, one malformed |
| `ontologies/substrate-primary/` | the operator's ontology, thirty constructions and coded run 1, verbatim; plus `aliases.json`, the audit's declared alias table |
| `CLAIM_TABLE.md` | `OP_001..019` |

## Run

```bash
python3 ontology-probe/probe.py declare                 # primitives report + admitted set (empty) + candidates
python3 ontology-probe/probe.py prompt CONSTRUCTION_ID  # refuses a candidate
python3 ontology-probe/probe.py score RUNS.jsonl [--fixture CONSTRUCTIONS.jsonl]
python3 ontology-probe/probe.py score ontology-probe/ontologies/substrate-primary/runs/claudeopus5_r1.jsonl \
        --ontology ontology-probe/ontologies/substrate-primary     # the coded run 1
python3 ontology-probe/selftest_op.py
```

A run record: `run_id, ontology, ontology_version, construction_id,
model, family, repeat, date, raw_response, constructed`. The response is
the four-field form section 4 asks for; anything else parses MALFORMED
and is counted apart. A CODED SHEET (`run_id, family, repeat, id, class,
status, terms_used, terms_added`) is read through an adapter; it needs
`--ontology` and gets no leak check.

## The section 9 first run, from here

1. declare primitives — done for one ontology, as a reading
2. hand-build 30 constructions (12 CONTROL, 9 TARGETED, 9 AMBIENT) — **done by the operator** (`ontologies/substrate-primary/`); cannot be done by a model
3. run on 2 model families, 3× each — one family, one repeat, coded; the rest not done, no endpoint here
4. report six aggregates and the nulls — the scorer does this on any log
5. publish `smuggle_set` with the dual-use note — the render carries the note

## Choices the order leaves open

Printed on every render. `[CHOICE 1]` primitive layout; `[CHOICE 2]`
COMPOSES_WITH_ADDITION rows in every denominator and no numerator;
`[CHOICE 3]` the leak cross-check beside the self-reported status;
`[CHOICE 4]` the N4 threshold and the OP-5 physics-share cut;
`[CHOICE 5]` `targets` optional on TARGETED (the order's schema has no
such field; the operator's set was refused until it was); `[CHOICE 6]`
an optional `aliases.json` beside `primitives.json` screens
`terms_added` for reimport of a declared absence, and its
`scope_required` table names added terms that carry no value until
their scope is declared, each under an `import_class` (`scope` or
`morality`, the second requiring `graded_by`) — both declared, dated,
word lists, and the morality class is open by declaration.

Stdlib only. Parses under 3.9. Phone-buildable. CC0.
