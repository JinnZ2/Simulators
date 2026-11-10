# run_10 -- toolbox trigger: N misclosure near-identical across seeds

```text
status     : INCOMPLETE -- gate rule: tools missing, see ledger/NEEDS_TOOL.md
code       : runs/run_10.py
seed       : 0..9
params     : model/base.py DEFAULTS, unedited ; arms: drought_sd=0, dep=0, fires off, dt 1/52 1/104 1/208 1/64 1/128, years 30..300
results    : (c) roundoff of the deposition counter. Not (a), not (b).
flags      : 6 (below)
provenance : DERIVED -- recomputed in this tree: python3 runs/run_10.py ; pinned in samples/run_10.sample.txt
feeds      : L0_N_BUDGET ; CC_001_n_misclosure_seed_invariance ; ANCHOR_run9 (test 2) ; budget_closure
l0_closure : N CLOSED, water CLOSED in every arm ; C / P / energy VOID
```

## Trigger

N misclosure -5.0e-11 in each of seeds 0-9. A residual that should be noise was
the same to two digits. Three explanations were named before the run.

## Reading

```text
hypothesis                        reading     evidence
(a) seed not wired to fire draw   RULED OUT   with precipitation identical in every seed (drought_sd=0,
                                              total 300.0000000000 in all), fire sequences are still
                                              10 distinct of 10
(b) fires identical across seeds  RULED OUT   10 distinct fire-time sequences of 10; counts 75..81
(c) roundoff, deterministic part  SUPPORTED   a counter with no model and no random draw reproduces it
```

```text
dt       model N misclosure    bare counter minus 300    (opposite sign: the audit subtracts the counter)
1/52     -5.062e-11            +5.008e-11
1/104    +7.124e-11            -7.094e-11
1/208    +4.452e-10            -4.447e-10
1/64     +1.4e-13               0             (1/64 is exact in binary)
```

Where it flows: deposition is the one term added at a constant rate to a
counter that grows to 300. Each add rounds; the bias has one sign and
accumulates. Remove the term (dep=0) and the residual is ~1e-14 with a sign
that varies by seed. Fire off changes nothing (-5.07e-11).

The pools did not lose 5e-11 of N. The boundary counter over-counted it.

## Flags

```text
- INCOMPLETE under the gate rule (2026-11-10). The reading (c) rests on hand-written
  checks, not on the toolbox: six of the brief's seven tools do not exist. The
  evidence stands as logged; the trigger is not counted as resolved.
- Not converging with dt: the residual GROWS as dt shrinks (more adds). It stays
  10^4 below the CLOSED tolerance at every dt tried.
- Growth with run length is not smooth: -9.0e-13, +1.3e-12, -1.6e-11, -5.1e-11 at
  30, 75, 150, 300 yr. The sign flips once. Bias depends on the counter's
  binary exponent, which steps at 32, 64, 128, 256.
- The dep=0 arm had 0 fires in all three seeds (no input, fuel never reaches
  threshold). So that arm removed deposition AND fire together. The fire-off
  arm at dep=1 is the separate half.
- Not repaired. A compensated-sum counter would remove the residual; it would
  also change model/base.py, which the candidate anchor pins by hash.
- Fire count at dt 1/128 is 81, at 1/104 and 1/208 it is 79, at 1/52 it is 80.
  The trajectory is step-size sensitive at the level of one or two fires.
```
