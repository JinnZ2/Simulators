# frame-instruments -- build notes

Built to `workorders/B1-B3_frame_instruments.md` and
`workorders/B4_dilemma_reconstruction.md`, both delivered verbatim. The
third referenced spec, `WORKORDER_runner_up_trace.md`, did not arrive
and is not reconstructed. Results only.

## Layout

```
runrecord.py      shared run record; appends to runs/runs.jsonl on every exit path
ficommon.py       shared I/O, schema checks, hand-rolled argv parsing
b1/  schema.py score.py permute.py summarise.py report.py test_b1.py
b2/  conditions.py order.py lock.py agree.py test_b2.py
b3/  split.py join.py arms.py test_b3.py
b4/  items.py reconstruct.py requirements.py grade.py agreement.py
     nullshuffle.py calibrate.py report.py test_b4.py   (see b4/BUILD_NOTES.md)
```

Each `bN/` carries a `samples/` directory with one run on that build's
in-file test fixture. Every fixture is constructed and says so.

## Shared rule, as built

`runrecord.Run` is a context manager: the record is written in
`__exit__` on every path, an uncaught exception included (recorded as
`error`, then re-raised). This is the one class in the tree, kept
because the write-on-every-path guarantee is what a function does not
give. Exit codes: `ok` 0, `error` 1, `void` 2, `empty` 3. A usage error
(bad arguments) exits 2 before any run exists and writes no record.

`FORBIDDEN = (label, category, type, interpretation)` is checked on
every validated input row.

Argument parsing is `ficommon.parse_argv`, positionals then
`--name value`, so no CLI library is used. B4 arrived first under
`argparse` and was retrofitted to the same parser, with its documented
invocations unchanged.

## B1 -- choices the order left open, each marked in the code

- **Continuation alignment.** `continuation` and `base_continuation`
  are the tokens after the forced and the taken token respectively,
  compared position-aligned. Rejoin at `t` means
  `continuation[t-L:t] == base[t-L:t]` for some `L <= t <= D`.
- **Normalisation of `div_D`.** Levenshtein over tokens divided by the
  longer truncated length; 0.0 if both are empty.
- **Permutation unit.** Tuples are shuffled within each
  `(model_id, D, L)` stratum, independently per stratum, so stratum
  means are invariant and the null acts on the top-decile position sets.
  The report states this beside the numbers.
- **Top decile.** The `ceil(n/10)` rows with the largest `div_D`, ties
  broken by position string; one row minimum.
- **Section 6.** N1-N5 live in the missing reference spec. The section
  prints the quantities a null would read and evaluates nothing; if the
  spec lands at `workorders/runner_up_trace.md` the section says so and
  still implements nothing, because the nulls need the spec's own text.

## B2 -- choices

- **Key rendering.** Three labelled lines (`posed:` / `target:` /
  `why:`), one function imported by both `conditions.py` and `lock.py`.
- **Leak check.** Field set exact on every row AND withheld text absent
  by substring. A key whose `why` quotes the statement verbatim is a
  real leak under condition B and is refused as one.
- **Latin square.** Blocks of four readers, each block the cyclic shifts
  of a fresh seeded permutation; readers past the last full block carry
  seeded permutations and the shortfall is in the run record notes.
- **Lock.** Two invocations, one path each. The commit path never opens
  `cases.jsonl`; the release path never writes `commits.jsonl`.
  `agree.py` re-checks every D1 row against the commit hashes, so the
  lock is enforced at scoring time as well.
- **Agreement rule.** Normalised exact match (casefold, whitespace
  collapsed, trailing punctuation stripped), written into every row as
  `match_source`. No matching engine; a different rule is a different
  `match_source`.
- **A vs D1 check** is the first row of the output. Divergence fires
  when the within-A and within-D1 agreements differ by more than
  `--divergence-threshold`, or the cross A x D1 agreement falls below
  both withins by more than it. Default 0.2, printed.
- **Anchoring.** `key_match_rate` under C and under D2, and among D
  readers whose committed D1 differed from the key, the fraction whose
  D2 matches it (`ratify_rate_D`).

## B3 -- choices

- **Role boundary.** ROLE CASE prompt files hold `{"case_id"}` only;
  ROLE KEY prompt files hold `{"statement"}` only and are built from a
  `statements.jsonl` that is refused if it carries any field beyond
  `case_id` and `statement`. Every file is re-read after writing.
- **Drops.** `join.py` drops unpaired rows and writes each dropped id
  into the run record notes, with the count in `counts`.
- **The B3 result** (condition-B agreement between arms) is read from
  two `agree.py` outputs side by side; each `agree.py` row carries the
  arm from `cases.jsonl`. No comparison script is built.

## What no build here does

No capability score, ranking, correctness score, or category field. No
network. No model call: every reader, auditor, reconstructor or role
works outside these scripts and their output arrives as files.
