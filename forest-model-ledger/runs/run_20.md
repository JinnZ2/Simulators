# run_20 -- run_15's near-threshold classes as a range over the materiality margin (follow-up item 4)

```text
status     : COMPLETE -- a margin sweep with built tools; no trigger left unanswered by this run
code       : runs/run_20.py
seed       : 0-19 paired (run_15's seeds)
params     : base.DEFAULTS; arms uG, KG, kill_T, season, aT at x1.1 and x0.9; delta 0.40..0.60 sd step 0.02; band 2 sd
results    : at 0.50 the ten reproduce run_15's classes. Over 0.40-0.60 the 33 read HIDDEN 23..15, ABSORBED 4..12;
             SEED_SPECIFIC 2, INERT 2, UNRESOLVED 2 do not move
flags      : 4 (below)
provenance : DERIVED, model/base.py at the run_9 anchor hash; tools as frozen at 72244bf
feeds      : CC_003_nudges_that_move_nothing ; multi_seed_ensemble (held-out PROVISIONAL)
l0_closure : not re-read here; same model and seeds as run_15
```

## Class by delta (H HIDDEN_IN_NOISE, A ABSORBED, S SEED_SPECIFIC)

```text
nudge        eff sd  0.40 0.42 0.44 0.46 0.48 0.50 0.52 0.54 0.56 0.58 0.60
uG x1.1       0.523     H    H    H    H    H    H    H    A    A    A    A
uG x0.9       0.500     H    H    H    H    H    A    A    A    A    A    A
KG x1.1       0.458     H    H    H    A    A    A    A    A    A    A    A
KG x0.9       0.516     H    H    H    H    H    H    A    A    A    A    A
kill_T x1.1   0.585     H    H    H    H    H    H    H    H    H    H    A
kill_T x0.9   0.478     H    H    H    H    A    A    A    A    A    A    A
season x1.1   0.407     A    A    A    A    A    A    A    A    A    A    A
season x0.9   0.484     S    S    S    S    S    S    S    S    S    S    S
aT x1.1       0.432     H    H    A    A    A    A    A    A    A    A    A
aT x0.9       0.459     H    H    H    A    A    A    A    A    A    A    A
```

```text
delta  HIDDEN  ABSORBED  (SEED_SPECIFIC, INERT, UNRESOLVED fixed at 2, 2, 2)
0.40   23      4
0.50   18      9          run_15
0.60   15      12
```

## Flags

```text
1  The asked three (uG, KG, kill_T) are HIDDEN in both directions at delta <= 0.44 and ABSORBED in
   both at 0.60; at 0.50 each splits by sign. The sign split in run_15 is the margin, not the physics.
2  Every class change runs HIDDEN -> ABSORBED as delta rises; nothing reaches INERT or UNRESOLVED.
   The resolved/immaterial line is the only one the margin moves.
3  Counts assume the other 23 nudges do not cross: their largest effects are outside 0.40-0.60
   (kG x1.1 0.61 stays HIDDEN at 0.60) or UNRESOLVED (drought_sd, p_ign 0.35-0.37), which the
   margin cannot move. Read from samples/run_15.sample.txt, not re-simulated.
4  multi_seed_ensemble went back to PROVISIONAL on its held-out gate (FAIL_TP 0.995, heavy tails at
   15 seeds). Here every MOVED call is at |z| > 7 on 20 seeds; the held-out miss is not near these.
```
