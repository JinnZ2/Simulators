# Run note — gate_check.py

Built to the work order as delivered. One file, standard library, offline,
CC0. Four checks, presence or absence only, file and line reported, no
diagnosis, no severity, no summary judgement. Thresholds live in
`thresholds.txt`; `gate_check.py` reads that file and never writes it or
`threshold_chain.txt`.

## What it does

```
python3 gate_check.py [repo_path] [--json]
```

Walks the path for source files (`.py .sh .js .ts .go .rs .c .h .cpp .java
.rb`) and prose (`.md .txt .rst`), skipping `.git`, `__pycache__`,
`node_modules`, virtualenvs, `build`, `dist`. Python is read by AST and
tokenizer; other source by one-line regex; prose by regex. Output is one
line per check, or one JSON object with `--json`.

## Decisions the order did not specify

1. **Per-check label mapping** (flagged in the code as the builder's
   derivation): a hit in code gives `HELD_RETRIEVABLE` with `file:line`; a
   hit only in a comment, docstring or prose file gives `HELD_UNRETRIEVABLE`
   with the mention's location under `mention`; neither gives `NOT_HELD`.
   `OUT_OF_ENVELOPE` is returned by check 4 only.
2. **Check 1 tokens**: exactly the three the order names (`UNKNOWN`,
   `BLOCKED`, `OUT_OF_ENVELOPE`, with hyphen and space variants, case-
   insensitive). A bare `return None` is NOT counted as an unknown path;
   the order named tokens, so the tokens are the rule.
3. **Check 2 (kill rule)**: Python, an `if` whose body raises, returns
   nothing, or calls `sys.exit`/`exit`/`abort`/`quit`; other source, a line
   carrying both a condition keyword and an exit/abort/throw/raise; prose,
   the words *kill rule*, *refuse(s)*, *void*, *abort*, *returns nothing*.
4. **Check 3 (test files)**: a file named `test_*.py`, `*_test.py`, or
   containing `selftest` in its name, OR any `.py` that defines
   `selftest()`/`self_test()`. The second clause was added after the first
   run read `count=0` on a folder whose failure checks live in a selftest
   function inside its main module. An assertion is `assert`, a call whose
   name starts with `assert`, or a call named `check`; it counts as sitting
   on a failure path when it is inside an `assertRaises`/`pytest.raises`
   block, or is `assertRaises`/`assertIsNone`/`assertFalse`, or its own line
   carries one of a declared word list (`None`, `raise`, `error`, `fail`,
   `void`, `empty`, `refus*`, `reject*`, `block*`, `unknown`, `invalid`,
   `missing`, `absent`, `not_found`, `abort*`, `exit`). A word list decides
   this, so an assertion phrased without those words is not counted. `count`
   and `present` are separate fields; the threshold from `thresholds.txt` is
   reported beside them as `threshold` and `at_or_above_threshold`, both
   `null` when the file is absent.
5. **Check 4 (demo)**: a demo is a `.py` whose path contains `demo`,
   `example` or `sample`. No such file gives `NOT_HELD` with a detail line.
   A demo that reads an input (`sys.argv`, `argparse`, `input(`, `open(`,
   stdin, environment) and holds a kill-shaped conditional gives
   `HELD_RETRIEVABLE`; reads an input with no such conditional gives
   `NOT_HELD`; no demo reads any input gives `OUT_OF_ENVELOPE`, the order's
   "demo is the whole artifact" case.
6. **Thresholds file location**: beside the script first, then the repo
   root. Parse: `key = value`, `#` comments, nothing else. Non-integer
   values for the one known key read as absent.
7. **Language coverage**: Python gets structural checks; everything else
   gets line regexes. Stated so a non-Python repo's result is read as what
   it is.

## Runs at delivery

- Its own folder: check 1 pins `gate_check.py:33`, the line that defines
  the token regex. Any repo containing this checker will hold check 1 on
  that line. Reported, not special-cased.
- `crediting-rate/`: checks 1 and 2 held in code; check 3 `count=5`,
  `present=True` after decision 4; check 4 `NOT_HELD` (no demo file).
- `framework-instruments/instruments/b2-audit-isolation`: check 1
  `NOT_HELD` (its refusal state is the word `void`, not one of the three
  tokens); check 3 `count=9`.
- `play-sims/sponge-reef`: all four `NOT_HELD`.
- Two constructed folders: one with a demo that reads no input and a
  README stating a void rule returns `HELD_UNRETRIEVABLE` ×2 and
  `OUT_OF_ENVELOPE`; one with a demo that reads `argv` and raises on `None`
  returns `HELD_RETRIEVABLE` for checks 2 and 4. With no `thresholds.txt`
  on the path, check 3 reports `count` and `present` with `threshold=None`.

## Not built

No correctness judgement, no framework read, no science evaluated, no
severity language, no `FAIL` label, no recommendation.
