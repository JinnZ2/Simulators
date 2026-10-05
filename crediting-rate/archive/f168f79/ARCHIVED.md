# ARCHIVED — crediting_rate_v2 build f168f79

Archived 2026-10-05. **Not the live build.** The live revision-2 module is
`../../crediting_rate_v2.py` (`ad56177` + `e4f5418`). Why it was kept is in
`../../README.md`, under the Revision 2 heading, and in `../../CLAIM_TABLE.md`
`CRD_025`.

Every file in this directory is **byte-identical to commit `f168f79`**,
nothing edited:

| here | was, at f168f79 |
|---|---|
| `crediting_rate_v2.py` | `crediting-rate/crediting_rate_v2.py` |
| `test_crediting_v2.py`, `make_fixtures_v2.py` | same names, `crediting-rate/` |
| `fixtures/v2/` | `crediting-rate/fixtures/v2/` |
| `samples/v2_f*.sample.txt` | `crediting-rate/samples/` |
| `README.md`, `CLAIM_TABLE.md`, `PREDICTION_V2.md` | same names, `crediting-rate/` |
| `WORK_ORDER_V2.md` | same; also identical to the live copy |

## Graded on its own fixtures

| F1 | F2 | F3 | F4 | F5 |
|---|---|---|---|---|
| ETYMOLOGY_TRACKING | CONTRIBUTION_TRACKING | FRAME_ASYMMETRIC | CONTAMINATED_FRAME | ETYMOLOGY_TRACKING |

On F5 the gap vanishes under the antiquity control (N2), and the verdict
does not change. That is the one place it parts from the live build. Its own
suite runs 124 checks, 0 failed, at `f168f79`.

**Cross-format fixture check: NOT_RUN.** It has not been run on the live
build's fixtures, and the live build has not been run on these.

## Running it

It does not run from here, and that is deliberate. It imports v1
`crediting_rate.py` from its own directory, and its test reads that file by
path. Copying v1 in beside it would make a second copy, and second copies
drift (`tools/check_gate_drift.py`). Run it at its own commit instead:

```
git worktree add --detach /tmp/crv2_f168f79 f168f79
cd /tmp/crv2_f168f79/crediting-rate
python3 test_crediting_v2.py
python3 crediting_rate_v2.py fixtures/v2/f5_antiquity.events.jsonl \
    fixtures/v2/f5_antiquity.mechanical.jsonl \
    fixtures/v2/f5_antiquity.depth.jsonl fixtures/v2/f5_antiquity.frame.json 7
```

## Ids

`CLAIM_TABLE.md` here uses `CRD_009..CRD_021` for claims different from the
live table's ids of the same numbers. Cite them as `archive/f168f79 CRD_0nn`.
