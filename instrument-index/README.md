# instrument-index

REBUILT 2026-09-22 from design recovered from session 2026-09-20
transcript fragments. Original bytes lost. Sections marked `[RECOVERED]`
match recovered text; sections marked `[REBUILD-CHOICE]` are new.

An index of the instruments in one or more repositories. One row per
scannable file, thirteen fields, two renderings written from one pass,
and one pre-stated falsifier run on every build.

It ranks nothing and scores nothing. Every field is read out of the file,
read out of an override, or the literal `UNRATED`.

## Files

- `INDEX-SPEC.md` -- the specification, with the `[RECOVERED]` and
  `[REBUILD-CHOICE]` labels carried as delivered.
- `build_index.py` -- the builder. `collect()` once, `write_tsv()` and
  `write_md()` both reading the same rows.
- `tests/fixture/` -- the fixture recovered from the original smoke test,
  extended.
- `tests/fixture_claim/` -- a planted CLAIM-only majority, so the
  falsifier is shown firing.
- `tests/test_build_index.py` -- the test.
- `samples/` -- one run over the fixture, both renderings and the stderr
  flag stream.

## Run

```
python3 build_index.py --tsv INSTRUMENT-INDEX.tsv --md INSTRUMENT-INDEX.md repo1 repo2 ...
python3 tests/test_build_index.py
```

`build_index.py` has no `--selftest`; it exits 2 and names the test file.

## The three readings that do work

**`NOT-SCANNED` is not an empty repo.** A path passed but missing renders
"Unknown contents, not an empty repo."; a repo walked to zero rated rows
renders "Scanned, no rated instruments found (N file(s) unrated)."
Collapsing them reports a coverage hole as a zero.

**An unrated fraction is not a fraction of zero.** The axis check reads
the share of rated rows whose only shape is `CLAIM` against 0.70. With no
rated row the share is `None` and the verdict is "UNRATED: check not
run", not "axis holds at this build". The same field, two readings, and
the falsifier cannot fire on a corpus nobody has headered.

**An estimate labeled as an estimate is usable; an estimate wearing a
number is not.** `load_tok_est` is `bytes // 4` and says so in both
renderings. There is no tokenizer in the loop.

## What it does not do

It does not read the instrument. `catches` is the author's sentence,
carried; nothing checks that the instrument catches it. `gate` is the
author's word; nothing runs a gate. The axis check is a check on the
INDEX -- whether `input_shape` partitions the set -- and not on any
instrument in it.

Every file under `tests/` is CONSTRUCTED. None of them is an instrument,
and the `catches` sentences in the fixture describe nothing that exists.

Claims: `CLAIM_TABLE.md` (`II_001..II_014`). Check count printed by
`python3 tests/test_build_index.py`.

Stdlib only. Parses under 3.9. Phone-buildable. CC0.
