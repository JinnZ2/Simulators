# PREREG -- ports of the original run 6, 7, 8 code

Written 2026-11-11, before `originals.py` exists. The original code arrived
from the chat side the same day and is filed verbatim in
`forest-model-ledger/runs/run_6.py`, `run_7.py`, `run_8.py`. This is a second
branch beside the rebuild (PART 2 of `PREREG.md`); the rebuild and its results
stay as they are.

```text
branch ORIGINAL   the delivered code, ported to the standard library, draw for draw
branch REBUILD    PART 2 of PREREG.md: L 64, 40 reps, window 0.05 -- unchanged
```

## How the port is checked

`export_originals.py` (needs numpy and scipy, run once) executes the three
delivered files and writes their results at full precision to
`fixtures/originals_expected.json`, with the numpy and scipy versions and the
sha256 of each source file. The port reads no numpy at runtime. Random draws
come from `playground/numpy_stream.py`, itself checked against numpy's recorded
output (`fixtures/numpy_stream_check.json`).

## Targets, fixed now

```text
O7  run 7   11 droughts: grid mean and grid sd equal to the numpy run within 1e-12 (the burned and
            vegetated cell counts are integers, so this asks for the same burns);
            ODE fraction within 1e-9 (the port uses bisection, the original scipy brentq)
O8  run 8   5 droughts x 4 spot levels: mean and sd within 1e-12; ODE within 1e-9
O6  run 6   fires 47 at fire_thr 0.6, and 56 / 48 / 45 / 38 at 0.3 / 0.5 / 0.8 / 1.2: exact
            late biomass mean, swing, tree share, Ls range, sweep columns: equal at the printed precision
            OLD misclosure at the five printed checkpoints: equal at 3 decimals
            CONSERVED max |misclosure|: below 1e-8, reported beside the numpy value
```

Not targeted, and said now: bit-for-bit floats in run 6. The original uses
numpy matrix products (BLAS) and pairwise sums; the port uses plain loops, so
sums can differ in the last bits. The run-6 misclosure is itself roundoff, so
its digits are not expected to match; its size is.

A miss on any target is reported as a miss. The port is not adjusted to a
target after it is seen, except to correct a transcription error against the
delivered source, and any such correction is listed in the results.

## Rebuild against original (the divergence is data)

Fixed now, before the two are put side by side:

```text
F1  stated as ODE / grid by drought for both branches; no single number
F3  window 0.05 on |grid - ODE| at spot 0.2, the same window PREREG.md fixed for the rebuild,
    applied to the original's three points (drought 0.5 / 0.6 / 0.7). The original declared no
    window; that is recorded as such (C3), and the 0.05 reading of it is this file's, not the run's.
seed spread   the original design (L 100, 10 reps, spot 0.2, drought 0.5 / 0.6 / 0.7) repeated
    on seeds 4 .. 23: mean and sd over seeds of (grid mean - ODE), and how many of the 20 seeds
    fall inside 0.05 at each drought. A hand-written seed loop, not a multi-seed tool.
C6  by_config {original, rebuild} on |grid - ODE| at drought 0.5, stability_tol 0.02
card  one coincidence card per feature (F1, F3). Evidence is entered; no slot is set by the code.
      "design difference" is not one of the card's five causes and is recorded as evidence text only.
```
