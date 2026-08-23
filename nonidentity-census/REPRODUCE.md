# REPRODUCE

All commands from `nonidentity-census/`. Stdlib only, no install step,
parses under Python 3.9.

## What runs here

```sh
python3 t1_predicate_unit.py --selftest   # transcription check vs BOUNDARY.md D3
python3 t1_predicate_unit.py --null       # known-signal / known-null, fail class
python3 t1_predicate_unit.py --demo       # per-row labels and decided_by
python3 t2_sample.py --selftest           # aggregation path, inline fixture
python3 t2_sample.py --fixture            # per-field table, n=6, NOT a corpus
```

Expected, and pinned in `samples/`:

| command | expected |
|---|---|
| `t1 --selftest` | `SELFTEST PASS (0 checks failed)` |
| `t1 --null` | signal 12/12, null 0/5, fail class `OK` |
| `t1 --demo` | `decided by predicate: 2  by table: 10  undecidable: 0` |
| `t2 --selftest` | `SELFTEST PASS (0 checks failed)` |
| `t2 --fixture` | 4 fields, law row `undec 1.000` |

`--selftest` on T1 fails if `BOUNDARY.md`'s D3 table and the code's
`UNIT_TABLE` / `BIGRAM_TABLE` disagree. Editing a boundary decision after a
run turns it red, which is the point of parsing the decisions rather than
restating them.

## What does not run here

```sh
python3 t2_sample.py --openalex           # NEVER EXECUTED
```

Blocked on 2026-08-23 by this environment's egress policy:

```sh
curl -sS "$HTTPS_PROXY/__agentproxy/status"     # shows the refusals
curl -sS "https://api.openalex.org/works?per-page=1"
# curl: (56) CONNECT tunnel failed, response 403
```

`--openalex` prints a warning to stderr saying it has never been executed.
Treat a first run as untested code. To run T2 as specified from an unblocked
host:

```sh
python3 t2_sample.py --openalex > t2_base_rate.txt
```

Or with a corpus obtained any other way, one JSON object per line, keys
`id` / `field` / `abstract`:

```sh
python3 t2_sample.py --jsonl abstracts.jsonl
```

T3 has no command. It iterates over T2's non-identity cases and there are
none, because T2 did not run.

## T5

Four `WebSearch` queries, verbatim, in the order run:

1. `reform resistance identity threat versus material self-interest institutions held constant`
2. `municipal amalgamation resistance identity preserved versus dissolved fiscal effect held constant`
3. `organizational identity threat merger name retained study resistance economic stakes controlled`
4. `experiment manipulating perceived identity continuity holding material outcomes constant support for merger vignette`
5. `natural experiment reform changed mechanism preserved institutional identity resistance same material loss comparison`

Five queries were run; `FINDINGS.md` T5-2 says four because query 1 predates
the T5 thread and was run while scoping. Both counts are in the record rather
than one being quietly corrected.

Result set is not reproducible: search indexes change and are not versioned.
This is the same non-reproducibility `criteria-drift` measures, and it means
T5's negative has no fixed denominator.
