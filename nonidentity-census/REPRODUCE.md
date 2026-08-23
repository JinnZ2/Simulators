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

python3 t1_verb_first.py --selftest       # D6 instrument
python3 t1_verb_first.py --front          # steps 1-2 only, the residues
python3 t1_verb_first.py --score          # six-option tally + read_on split
python3 t1_verb_first.py --proxy          # morphological proxy vs the rule
python3 t1_verb_first.py --compare        # D1/D3 against D6, item by item

python3 t2_window.py --selftest           # D7 instrument, incl. two controls
python3 t2_window.py --proposal           # the three examples, classified
python3 t2_window.py --controls           # constructed known-truth pair
python3 t2_window.py --seed               # seed claims; STIPULATED banner

python3 t6_window_declaration.py --selftest  # incl. the welded-column gate
python3 t6_window_declaration.py --null      # the 2x2, run before any real run
python3 t6_window_declaration.py --table     # the 12 rows, all columns
python3 t6_window_declaration.py --matched   # matched set + the confound figure
python3 t6_window_declaration.py --exit      # the two association tables
python3 t6_window_declaration.py --run       # real run: 0 eligible papers
```

Expected, and pinned in `samples/`:

| command | expected |
|---|---|
| `t1 --selftest` | `SELFTEST PASS (0 checks failed)` |
| `t1 --null` | signal 12/12, null 0/5, fail class `OK` |
| `t1 --demo` | `decided by predicate: 2  by table: 10  undecidable: 0` |
| `t2 --selftest` | `SELFTEST PASS (0 checks failed)` |
| `t2 --fixture` | 4 fields, law row `undec 1.000` |
| `verb_first --selftest` | `SELFTEST PASS (0 checks failed)` |
| `verb_first --score` | `BEARER_REQUIRED 5 / READS_WITHOUT 2 / VERB_CARRIES_IT 3 / BOTH_READINGS 2`; read_on `RESIDUE 8 / CLAIM 1 / DROPPED_SUBJECT 3` |
| `verb_first --proxy` | `agreement 4/12` |
| `verb_first --compare` | `agree 9   DISAGREE 1   CONTESTED 2` |
| `t2_window --selftest` | `SELFTEST PASS (0 checks failed)` |
| `t2_window --proposal` | `W_dissolve 1 of 3   W_measure 2 of 3` |
| `t2_window --controls` | `N-coarse ratio=20`, `N-fine ratio=0.05` |
| `t2_window --seed` | `P-1 RESOLVES_IT`, `P-2` and `P-3` `UNDECIDABLE`, with the STIPULATED banner |
| `t6 --selftest` | `SELFTEST PASS (0 checks failed)` |
| `t6 --null` | four cells at 3; `the two columns are not welded. T6 may proceed.`; rc 0 |
| `t6 --matched` | `as-specified null set 5 of 12`, `matched null set 0 of 12` |
| `t6 --run` | `eligible papers: 0` |

`t6 --null` exits 1 and prints `STOP:` if an off-diagonal cell is empty. It
does not, on this data.

`t2_window.distribution()` raises `WindowGateError` on stipulated input
unless `allow_stipulated=True`. Every window in the seed is stipulated; no
methods section was read.

`t1_verb_first.py --score` raises `JudgementNotSupplied` for any item with no
step-3 judgement. The rule's discriminator is the judgement, so there is
nothing to fall back on and the module does not invent one.

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
