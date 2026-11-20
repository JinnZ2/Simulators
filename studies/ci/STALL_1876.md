# CI stall, run #1876 (2026-11-20)

Status: record. Cause not established. Co-authored (owner + Claude Code). Observer slots: null.

## What happened

| item | value | source |
|---|---|---|
| workflow / run | `tests`, run #1876 (id 44742999444), push to `main` | GitHub Actions run list |
| commit | `1359c2c868ba4c44584f5aa03dfd18dc13fd25f7` (merge of PR #327) | same |
| job | `simulator-smoke`, job id 136311089217, conclusion `failure` | jobs list of the run |
| step | `enclosure-first-residual` (step 9), shown `in_progress` with no end time | same |
| times | job started 13:17:24Z, step started 13:17:30Z, job completed 14:03:25Z (about 46 min) | same |
| steps before it | all `success` | same |
| steps after it | did not run (`pending`) | same |
| other job | `grounding-layers`: `success` | same |

The step's command, from `.github/workflows/test.yml`:
`python -m unittest discover -s enclosure-first-residual/tests -p 'test_*.py'`

## What was checked

1. **Diff excludes the step.** `git diff 148031b..1359c2c --name-only`: 15 files, none under
   `enclosure-first-residual/`, none under `.github/`. The same step passed in run #1873 on
   `05101b9` and on the PR #327 head.
2. **Local run at `1359c2c`.** Same command: 26 tests, OK, 2 skipped, 3.3 s (Python 3.13.18,
   Claude Code's container).
3. **Log: VOID.** The job-log read returned HTTP 404; the download link points to a storage
   host the reading session's network refuses (CONNECT 403). No log line was read.
4. **Re-run: VOID.** The re-run call returned `403 Resource not accessible by integration`.
   The workflow has no manual trigger. No re-run was made.
5. **Discovery of the method layer.** `enclosure-first-residual/enclosure_first_residual.py`,
   `_find_method_layer()`, lines 182–198, called once at import (line 201).
   - It checks fixed paths only: `METHOD_LAYER_PATH` if set, then `method-layer` and
     `jinnz2/method-layer` under each of three parent directories. At most 7 candidates, two
     `os.path.isfile` calls each. No `os.walk`, `rglob` or `glob` in the file.
   - Timed locally: the function returns in about 0.00002 s; module import 0.009 s.
   - Full step with `METHOD_LAYER_PATH=/`: 2.76 s. With `METHOD_LAYER_PATH=$HOME` (`/root`):
     2.77 s. With a real method-layer checkout (0 skipped): 2.88 s. With `none`: 2.75 s.
   - The two skipped tests (`test_mirror_matches_G`, `test_round_trips_through_F`) skip when the
     method layer is absent. A search of the folder for `subprocess`, `socket`, `urllib`,
     `requests`, `sleep`, `.wait(` found nothing.
   - Reading: discovery is not a tree walk and does not account for the stall.

## Not established

- Why the step did not finish on the runner. Nothing read here points to the code in the step.
- Whether the runner had a method-layer checkout (the log was not read).

## What was changed

- `timeout-minutes: 5` on the `enclosure-first-residual` step in `.github/workflows/test.yml`
  (same branch as this note). A stall now ends the step after 5 minutes instead of the job
  running on. It does not remove the cause. No change to `_find_method_layer()`: item 5 shows no
  tree walk to bound.
