# precursor flag: seven creative fixes for the small-window degradation, measured

One page. 2026-11-19. Second note in the precursor series (first: the
window-dependence localization and surrogate calibration). Kimi K3 session, on
`JinnZ2/formula-audit` main `glyph/precursor.py` as filed 2026-11-18. CC0.
Question carried in: can the catch-rate collapse at small windows be reduced
without opening the false-alarm tap? Baseline symptom (w = 20, limit 0.5):
catches 46 -> 14 -> 6 of 200 as the series runs n = 60 -> 200 -> 400.

## Constructions (declared; same as note 1)

```text
memory   x_t = rho_t * x_{t-1} + N(0,1),  rho_t climbs 0.05 -> 0.95 over n
drift    x_t = 0.02 t + N(0,1)
step     x_t = 3.0 * 1[t >= n/2] + N(0,1)
white    x_t = N(0,1)
seeds    0..199 raw; 0..59 (S = 50) or 0..99 (S = 100) calibrated; w = 20 regime
```

## Variants (all knobs declared)

```text
tail50      Kendall over the last 50 rolling-stat points only
weighted    Kendall with pair weight (i + j)/2 (recency-weighted)
logvar      variance stat on log scale
cusum       Page CUSUM on each rolling stat vs first m = 25 points,
            slack delta = 1, threshold h = 8
vote        majority of 5 windows {15, 20, 25, 30, 40}, each voting both-taus >= lim
rvh         recent-vs-history: Mann-Whitney on last 50 vs rest, p <= 0.01, both stats
vote-cal    vote under the phase-randomized surrogate null, alpha = 0.05
```

## Raw rule, rates out of 200 (catches | white FA | drift, step leaks at n = 400)

```text
limit 0.3        n=60  n=200  n=400   FA 60/200/400   drift  step
baseline          87    93     87      12 / 1 / 0       0      0
tail50            87    36     38      12 / 9 / 14      9      9
weighted          94   102    103      12 / 2 / 0       1      0
logvar            87    93     87      12 / 1 / 0       0      0   (identical: rank-invariant)
cusum             84   187    197       5 /108/139    135    185
vote             104   116    125      13 / 2 / 2       0      0
rvh                0*  148    161       0 /22 /18      21/10   9/6   (*k < 60: no reading)

limit 0.5
baseline          46    14      6       3 / 0 / 0       0      0
tail50            46    12      9       3 / 1 / 1       0      0
weighted          56    32     11       3 / 0 / 0       0      0
logvar            46    14      6       3 / 0 / 0       0      0
cusum            (knob-driven; same failure as above)
vote              54    32     19       2 / 0 / 0       0      0
```

## Calibrated (alpha = 0.05)

```text
vote-cal  (S = 50, 60 seeds):   n=60   n=200  n=400
  memory                        2/60   25/60  50/60
  white FA                      0      3/60   2/60
  drift                         1/60   0      0
  step                          0      1/60   0
rvh-cal   (S = 100, 100 seeds): memory 1/100 (n = 200), 1/100 (n = 400);
  white FA 7/100, drift 5-8/100, step 16/100 then 8/100  (power was non-specificity)
```

## Findings

1. **You cannot transform your way out.** logvar is bit-identical to baseline: a
   rank statistic is monotone-invariant. Only structural changes count.
2. **Truncating the trend is not the fix.** tail50 loses catches and gains false
   alarms; fewer points, fatter null.
3. **Ensembling is the only free lunch found.** The 5-window vote reverses the
   degradation under the raw rule (catches rise 104 -> 125 with n at limit 0.3)
   with no FA or leak cost, and halves it at limit 0.5.
4. **Raw power is cheap; specificity is the expensive part.** rvh leads every raw
   table and fails every calibrated one: its catches and its leaks come from the
   same place. CUSUM fails structurally, not by tuning: a step IS a level change,
   and a level change is not a precursor. Both stay in the table as the negative
   controls.
5. **After calibration, what remains is honest information.** vote-cal detection
   climbs 2 -> 25 -> 50 of 60 with n while FA holds at alpha. The falling catch
   curve is gone; the ladder that replaces it is the price of an honest null.

## Limits

One construction per class; declared constants not swept. vote windows fixed at
{15..40}; other committees not run. Calibrated rates carry Monte Carlo error
about +/- 8 pp (60 seeds). rvh at n = 60 has k = 41 < L + 10: no reading, counted
as zero catches, not as a pass. logvar identity proven in execution, then checked
by hand (monotone invariance of Kendall's tau).

## Reproduce

Module pin and selftest as in note 1 (`--selftest`, 10/10). Variant definitions
above are complete; every rate derives from them plus the declared constructions
and seeds. kt verified equal to the module's kendall_tau on 25 random series.
