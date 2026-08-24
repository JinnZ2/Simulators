# transition-family-marker

A delivered results drop, plus checks on the parts that can be checked
without the generators.

`RESULTS_RUN_1.md` is **verbatim as delivered** and is not modified. All
added content is in `check_run_1.py`, `CLAIM_TABLE.md`, and this file. Same
arrangement as `../aperiodic-order-sim-stack/`, which is the nearest
precedent in this tree: a results drop with no generator, audited where
auditable and marked `UNVERIFIED` where not.

## The marker

Three phenomena proposed as one family of discontinuous transitions —
alignment homogenization, entropy depletion under recursive training, and a
loop/tree threshold in adaptive flow networks — with an Ising-style mapping
as the candidate common mechanism. Four sims (`SIM-A` … `SIM-D`) were the
first test. This folder holds run 1.

Confidence on the marker was `~0.40` before the run and `~0.40` after. The
drop's own summary is the right one: *the marker is not stronger, it is
better specified.*

## What the checks found

Three of the drop's claims need no generator, because they are algebra or
graph invariants. `python3 check_run_1.py` runs them.

**`SIM-D`'s derived constraint has its formula backwards, and the prose is
right.** The stated identity `temper(quench(p,s), T) == temper(p, T*(1+s))`
holds only at `s = 0`. The correct composition is `T/(1+s)`, because
tempering composes multiplicatively and a quench by `s` *is* a tempering at
`1/(1+s)`. The conclusion survives untouched — and gains a number the stated
version could not produce: the temperature that exactly undoes a quench is
**`T = 1+s`**.

**`SIM-C` returned the intact grid.** `loops=16, alive_edges=40` are exactly
`E = 40`, `E − V + 1 = 16` for a 5×5 grid. Not weak pruning — no pruning.
The reported outputs are computable from the grid dimensions alone.

**The damping in `SIM-C` is cancelled by the normalisation that follows
it.** `(0.85·C)/max(0.85·C) ≡ C/max(C)`. `damp=0.85` has no effect on
anything, which makes removing the max-normalisation necessary rather than
advisable.

Two more, read off the delivered table: the tail-mass inference is
under-determined without head and tail entropies reported separately, and
the "gradual, not steplike" negative is bounded by a 7-point grid whose
spacing varies 20× and is coarsest where the curve is steepest.

## What is not checked

Everything that is a property of code that is not here. In particular the
`NOT TUNED` discipline — the drop's strongest feature — cannot be confirmed
from outside, because a drop that had searched parameters and one that had
not produce identical results files. Recorded as `TFM_008`, `UNVERIFIED`.

One literature claim is carried and not verified: that `gamma=0.5` is the
marginal case for loop formation in the Katifori-type adaptation. Nothing
here rests on it.

## Files

| file | what |
|---|---|
| `RESULTS_RUN_1.md` | delivered, verbatim, unmodified |
| `check_run_1.py` | the checks. `--selftest`, or no argument for the report |
| `CLAIM_TABLE.md` | `TFM_001`–`TFM_008` with falsifiers |
| `samples/` | pinned output |

Stdlib only, parses under Python 3.9. CC0.
