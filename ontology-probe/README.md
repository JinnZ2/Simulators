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
the report banners it.

## What is here

| file | what |
|---|---|
| `WORK_ORDER.md` | delivered text, verbatim |
| `primitives.json` | one reading of `SHAPE_SPEC.md` as a primitive set: 25 terms, 6 `absent_by_design`, one `undefined`; marked unconfirmed by the author |
| `constructions.jsonl` | three CANDIDATE constructions, `hand_built: false`, not admitted (section 3 forbids model-generated sets) |
| `probe.py` | the instrument: `declare`, `prompt`, `score`; refuses `--selftest` |
| `selftest_op.py` | the checks, both directions; writes `samples/` and `runs/` |
| `runs/constructed.jsonl`, `runs/constructed_constructions.jsonl` | the fixture: 30 constructions (12 / 9 / 9), 2 families × 3 repeats, one leak, one malformed |
| `CLAIM_TABLE.md` | `OP_001..008` |

## Run

```bash
python3 ontology-probe/probe.py declare                 # primitives report + admitted set (empty) + candidates
python3 ontology-probe/probe.py prompt CONSTRUCTION_ID  # refuses a candidate
python3 ontology-probe/probe.py score RUNS.jsonl [--fixture CONSTRUCTIONS.jsonl]
python3 ontology-probe/selftest_op.py
```

A run record: `run_id, ontology, ontology_version, construction_id,
model, family, repeat, date, raw_response, constructed`. The response is
the four-field form section 4 asks for; anything else parses MALFORMED
and is counted apart.

## The section 9 first run, from here

1. declare primitives — done for one ontology, as a reading
2. hand-build 30 constructions (12 CONTROL, 9 TARGETED, 9 AMBIENT) — **not done, cannot be done by a model**
3. run on 2 model families, 3× each — not done, no endpoint
4. report six aggregates and the nulls — the scorer does this on any log
5. publish `smuggle_set` with the dual-use note — the render carries the note

## Choices the order leaves open

Printed on every render. `[CHOICE 1]` primitive layout; `[CHOICE 2]`
COMPOSES_WITH_ADDITION rows in every denominator and no numerator;
`[CHOICE 3]` the leak cross-check beside the self-reported status;
`[CHOICE 4]` the N4 threshold and the OP-5 physics-share cut.

Stdlib only. Parses under 3.9. Phone-buildable. CC0.
