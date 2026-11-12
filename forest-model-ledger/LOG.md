# LOG -- constants in forest-model-ledger

Every numeric constant the model and the toolkit use, with the date it was set.
`tests/test_l0.py` (`T_LOG_LISTS_EVERY_CONSTANT`) fails when a value here and the
value in code part, so this file cannot drift quietly.

None of these is fitted or sourced. Each is a hand-set number: one point in
parameter space. A change is a new anchor candidate, not an edit (the candidate
anchor pins `model/base.py` by hash).

## model/base.py DEFAULTS -- set 2026-11-10, hand-set, no tuning pass

```text
name            value  meaning
dep               1.0  N deposition, N units / yr
uT                1.2  max specific N uptake, trees, 1/yr
uG                3.0  max specific N uptake, grasses, 1/yr
K                 2.0  half-saturation, soil N
b                 1.5  fungal benefit multiplier on tree uptake
Kf                1.0  half-saturation of fungal benefit and payment
KT               60.0  light ceiling, trees (N-equivalent stock)
KG               12.0  light ceiling, grasses
aG                0.2  competition of grass on tree
aT               0.25  competition of tree on grass
c                0.08  tree -> fungus payment, 1/yr
mT               0.04  tree turnover, 1/yr
mG                0.9  grass turnover, 1/yr
mF                1.5  fungal turnover, 1/yr
kT               0.25  tree-litter decomposition at full moisture, 1/yr
kG                2.0  fast-litter decomposition at full moisture, 1/yr
leach            0.05  leaching coefficient
P0                1.0  mean precipitation, W units / yr
season            0.6  seasonal amplitude of precipitation
et               0.02  evapotranspiration coefficient
drain             0.8  drainage coefficient, 1/yr
Wh                0.5  moisture half-saturation for biology
drought_sd       0.35  lognormal sd of the annual precipitation factor
drought           0.0  mean precipitation reduction, 0..1
fuel_th           6.0  fuel threshold for ignition (litter N)
W_dry            0.55  dryness threshold for ignition
p_ign             4.0  ignition hazard per yr once both thresholds are met
burn              0.8  litter fraction burned per fire
vol               0.6  burned N fraction volatilised
kill_G            0.7  grass fraction killed per fire
kill_T           0.03  tree fraction killed per fire
leak              0.0  PLANTED defect switch for testing the audit; 0 in every real run
```

## model/base.py INIT -- set 2026-11-10, hand-set

```text
S                 3.0
T                10.0
G                 3.0
F                 0.5
Lt                2.0
Lg                0.5
W                 1.0
```

## run settings -- set 2026-11-10

```text
years             300   run length of run_9, run_10, run_11
dt               1/52   RK4 step; residual and fire count at other steps in runs/run_10.md
seed                0   base cases; 0..9 for seed sweeps
```

## toolkit thresholds -- conventions, not derived

```text
rel_tol         1e-09   budget_closure: CLOSED when |misclosure| <= rel_tol * gross throughput   (2026-11-10)
k_sigma           2.0   budget_closure: NOISE when |misclosure| <= k_sigma * sigma_meas; sigma_meas void   (2026-11-10)
K_NOISE           2.0   assumption_nudge: inside noise when |diff| <= K_NOISE * sd over anchor seeds 0-9   (2026-11-10)
nudge size   x1.1 x0.9   assumption_nudge on run_9: per hand-set parameter; structural nudges x10   (2026-11-10)
```

## Known error, left in place

```text
2026-11-10  N misclosure at dt 1/52 is -5.0e-11: float64 roundoff in the deposition counter
            (runs/run_10.md, card CC_001). About 10^4 below the CLOSED tolerance of 5.8e-7.
            Decision 2026-11-10 (authors): leave the base unchanged. The compensated-sum
            counter is placeholder branch BR_RUN_9B_COMPENSATED_COUNTER.
```

## toolkit thresholds -- set 2026-11-11 (work order: toolkit build, staged), all [CHOICE]

Not checked by `T_LOG_LISTS_EVERY_CONSTANT` (that test reads model DEFAULTS and INIT
only). Each value is the one recorded in the tool's gate; gate history in each docstring.

```text
tool                    name         value  note
multi_seed_ensemble     REL_TOL       0.05  INVARIANT = sd <= REL_TOL |mean|; over-reads on outputs with a nonzero mean (run_14 flag 2)
multi_seed_ensemble     K_MOVED        5.0  paired |z| for MOVED; buys FP 0 on the gate
multi_seed_ensemble     K_EQ           2.0  EQUIVALENT = |mean| + K_EQ se <= delta
multi_seed_ensemble     K_SPIKE        3.0  variance spike = sd > K_SPIKE median sd
runs 14, 15             delta, band   0.5 sd, 2 sd of the base ensemble; material = |mean| > delta
parameter_recovery      DCHI2          9.0  plausible set
residual_regression     N_PERM         500  permutations per increment
residual_regression     ALPHA         0.01
residual_regression     MIN_DR2       0.10  material R2 increment
residual_regression     COLLINEAR     0.95  NOT_SEPARABLE
equation_family_swap    K_HANDOFF      3.0  per-point disagreement
equation_family_swap    MIN_RUN          3  points in a regime; first gate failed FP 0.07 without it
assumption_block_trace  ALPHA        0.001  was 0.01, failed FP 0.015
assumption_block_trace  MIN_STUDIES      8
gate.py                 harness        200 draws (60 for residual_regression) x harness seeds 0-4; PASS = fp 0 and tp 1 on every seed
```

## 2026-11-11 -- original code for runs 6, 7, 8 filed

```text
source      chat side, 2026-11-11: three files, "verbatim as executed 2026-11-10"
filed       runs/run_6.py  run_7.py  run_8.py, byte-identical to the delivery (sha256 in each run_N.md)
rerun here  numpy 2.5.3, scipy 1.18.1: each prints its logged output line for line
statuses    run_6 COMPLETE, run_7 COMPLETE, run_8 INCOMPLETE (card CC_002, 6 rows in NEEDS_TOOL.md) -- PROPOSED
corrections recorded as delivered: ODE / grid is a ratio by drought (478 / 321 / 62 at 0.3 / 0.4 / 0.5),
            not "~60x"; the spot-0.2 convergence was read by eye, no tolerance, 10 reps -> CA_1 candidate
kept apart  run_6.py header: leaking model = "run-4 equations"; FML_009: run 5's model. Not reconciled.
STATUS_MAP  REPORTED gained one exit (original code arrives and reproduces). PROPOSED.
```
- 2026-11-11  ANCHOR_run9: the planned tag is replaced by the branch archive/anchor-run9 at 55c651b (Kavik decision; tag pushes are refused from sessions). git_commit stays the pin.
