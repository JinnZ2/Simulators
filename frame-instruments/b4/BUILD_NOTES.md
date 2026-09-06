# B4 build notes

Built to `../workorders/B4_dilemma_reconstruction.md`. Results only.

## Precondition state

The work order opens "B1–B3 exist. B4 reuses `runrecord.py` unchanged
and `agree.py` from B2 with one added field. Do not fork either."
B4 arrived and was built BEFORE the B1–B3 order; the state at each point:

| named dependency | at B4 build | now |
|---|---|---|
| B1, B2, B3 | not built; their order had not arrived | built, under `../b1 ../b2 ../b3` |
| `runrecord.py` | absent; built at `../runrecord.py` from the README spec | the B1–B3 order's shared rule, unchanged in shape; record file renamed to `runs/runs.jsonl` per that order |
| B2 `agree.py` | absent; B4.5 implemented directly in `agreement.py` with `match_source` on every row | exists. `agreement.py` is still NOT a wrap: B2's rule is normalised exact match on `posed`/`target`, B4's input is an external `matches.jsonl` over requirement pairs, so the two compute agreement from different inputs. Both carry `match_source`. |

Argument parsing was retrofitted from `argparse` to `ficommon.parse_argv`
when the B1–B3 order stated "no CLI library" as a constraint on all
builds; documented invocations are unchanged.

## Run order

```
python3 b4/items.py items.jsonl --out items_valid.jsonl
python3 b4/reconstruct.py items_valid.jsonl --reconstructors r1,r2,r3 --out prompts/
   # reconstructors work OUTSIDE these scripts from prompts/<id>/ alone
python3 b4/requirements.py requirements.jsonl --items items_valid.jsonl --out requirements_valid.jsonl
python3 b4/nullshuffle.py requirements_valid.jsonl --seed 3 --out requirements_shuffled.jsonl
   # external matcher runs on BOTH requirement files, blind to which is which
python3 b4/grade.py requirements_valid.jsonl --out grade.jsonl
python3 b4/grade.py requirements_shuffled.jsonl --out grade_shuffled.jsonl
python3 b4/agreement.py requirements_valid.jsonl --matches matches.jsonl --match-source "..." --out agreement.jsonl
python3 b4/agreement.py requirements_shuffled.jsonl --matches matches_shuffled.jsonl --match-source "..." --out agreement_shuffled.jsonl
python3 b4/calibrate.py ... (documented arm only)
python3 b4/report.py --items ... --out report.md
python3 b4/test_b4.py
```

Every script appends one record to `../runs/runrecord.jsonl` on every
exit path (`ok` 0, `error` 1, `void` 2, `empty` 3).

## Choices the order left open, each marked in the code

- **[CHOICE] file boundary.** One directory per reconstructor,
  `prompts/<reconstructor_id>/<item_id>.jsonl`, each file one line with
  the single key `text_verbatim`. Re-read and asserted after writing, and
  re-checked again by `report.py` (section 2 prints the count of files
  failing the check).
- **[CHOICE] requirement reference.** `reconstructor_id/req_id`, unique
  within an item. `matches.jsonl` and `factor_matches.jsonl` use it.
- **[CHOICE] agreement statistic.** For reconstructors A and B:
  `(#A with a counterpart in B + #B with a counterpart in A) / (|A|+|B|)`.
  A one-to-many link counts each requirement once. The definition string
  is written into every output row.
- **[CHOICE] physical/policy cues.** `grade.py` reads `settling_test`
  against two cue lists, both arguments with defaults, both written into
  every output row. A test hitting both lists or neither is `unresolved`
  with the sub-reason kept. This is a word list deciding a reading and
  is the weakest joint in the build; it is swept, not fixed.
- **[CHOICE] shuffle unit.** A requirement list is one
  (item, reconstructor) group; per reconstructor the items are deranged.
  The seed is written into every output row as `shuffle_seed` and into
  the run record. A reconstructor with one item cannot be deranged and
  the run is `void`.
- **The null needs its own matching pass.** Matches are keyed by item,
  so the shuffled arm needs `matches_shuffled.jsonl` produced by the
  same matcher on `requirements_shuffled.jsonl`, blind to which file is
  real. Reusing the real matches would make the null fire by
  construction rather than by measurement.

## Sample

`samples/` holds one full run on the in-file test fixture. The fixture
items are constructed for the test and are not published items; the
report says so in its source column. The rendered report screens clean
through `sheet-structure-scan/no_severity` with no exemption.

## Not built

No matching engine, no correctness score, no well-posed/mis-posed
verdict, no item rewriting. `report.py` writes exactly the nine sections
the order lists, in order.
