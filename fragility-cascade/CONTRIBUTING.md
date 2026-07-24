# Contributing to fragility-cascade

The folder now spans four disciplines and 36+ modules. These conventions
keep the audit graph legible when a new module lands.

## Before you add a module

Read [`docs/PHYSICS.md`](docs/PHYSICS.md). Every symbol used across the
folder is defined there once, with owner + units + range. Two rules:

1. **Do not shadow.** If your module needs a variable named `A` or `γ`
   and there's already an `A` or `γ` in the cheatsheet that means
   something different, either use the existing definition or **rename
   yours.** The symbol-collision map at the bottom of PHYSICS.md flags
   the letters already re-used across models.
2. **Add your row.** If your module introduces a new symbol, add it to
   PHYSICS.md before writing the code that computes it. This is cheaper
   than untangling meanings later.

## Naming pattern

Filename convention for a module that adds a new *axis* to an existing
one:

```
<original>_<axis>.py
```

Live examples in the folder:

| new module | extends | new axis it adds |
|---|---|---|
| `cascade_redesign_M_collapse.py` | `cascade_redesign_vulnerability.py` | model degeneration half-life `M_collapse` |
| `redemption_entropy_peak_hour.py` | `redemption_entropy.py` | state-dependent peak-hour correlation |

Rules:

1. **Standalone, not replacement.** The new file's docstring must open with
   a line stating it does NOT replace the original. The original's
   pinned samples stay canonical.
2. **First line = origin + axis.** Docstring line 1 names the original
   module. Docstring line 2 names the axis and its unit.
3. **Own the claim.** If the axis encodes a new claim, add the claim row
   to `CLAIM_TABLE.md` — pointing at your module, not the original.
4. **Do not rename the origin's docstring.** Every module has ever
   introduced a bug by copy-editing its own header to match a target
   file's name (`patch.py` and `patch2.py` were a real case). Your file's
   docstring names your file. Full stop.

## Every module runs

`python3 run_all.py` must stay green. That means:

- Runnable module (has `if __name__ == "__main__":`).
- Bounded runtime (< 15 s by default, cap-configurable via `--timeout`).
- Interactive modules register a `--smoke` path in `SMOKE_ARGS` so CI can
  drive them non-interactively.
- Every new module gets a `samples/<name>.sample.txt` (bulk-capture from
  the runner is fine).

## Refutation protocol

Every claim carries a refutation path — a set of parameter values that
would make it false. When you add a claim:

1. Anchor it to the CLAIM_TABLE with the module + test method.
2. State its refutation condition in prose (see existing C1–C17 rows).
3. If it's tested by `test_refutations.py`, add a `test_C*` method that
   returns the normalised dict schema documented in that module's
   top-level docstring.
4. When your claim gets falsified, **update the claim** — don't retune
   the sim to protect it. Retire the old phrasing to git history and
   record the failing parameter values in the CLAIM_TABLE's notes.

## Legacy

Files superseded by a newer canonical live in `legacy/`. They are not
imported by any live module and are skipped by `run_all.py`. See
`legacy/README.md` for the retirement rule.
