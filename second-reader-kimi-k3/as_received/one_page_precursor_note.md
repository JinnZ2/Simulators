# precursor flag: where the window dependence lives, and a calibrated fix

One page. 2026-11-19. Replay + extension by Kimi K3 (second-reader session), on
`JinnZ2/formula-audit` main `glyph/precursor.py` (as filed 2026-11-18). CC0.
Question carried in: the flag's sensitivity depends on the window — is that the
docstring, the language, the code, the repo, the rules, or the math?

## Constructions (declared; no others run)

```text
memory   x_t = rho_t * x_{t-1} + N(0,1),  rho_t climbs 0.05 -> 0.95 linearly over n
drift    x_t = 0.02 t + N(0,1)            (mean ramps 0 -> 8 sigma over n = 400)
step     x_t = 3.0 * 1[t >= n/2] + N(0,1) (one mid-series mean step of 3 sigma)
white    x_t = N(0,1)
seeds    0..199 (raw sweeps), 0..99 with surrogates 10000+s (calibration); n = 400
flag     module's own rule: rolling variance + lag-1 autocorr, Kendall tau of each,
         PRECURSOR iff both taus >= declared limit
```

## Raw fixed-limit rule: rates out of 200

```text
        limit 0.3                                  limit 0.5
w       memory   drift   step   white-FA           memory   drift   step   white-FA
20      87       0       0      0                  6        0       0      0
50      179      1       0      5                  109      0       0      1
100     191      2       0      8                  169      0       0      4
200     196      29      0      20                 186      10      0      8
```

## Surrogate-calibrated null (phase-randomized, S = 100, alpha = 0.05, add-one p)

Per series: preserve the periodogram, randomize phases, rerun the same pipeline on
each surrogate; flag iff both taus beat their surrogate 95th percentile.
Rates out of 100:

```text
w       memory (detection)   white (FA)   drift   step
20      65                   3            1       0
50      79                   2            0       0
100     63                   3            0       0
200     71                   1            0       0
```

## Findings

1. **The layer is the math.** The w-dependence is predicted by three textbook facts:
   rolling-variance noise ~ sqrt(2/(w-1)) (32% at w = 20); Kendall's null tightens as
   k^-1/2 but overlapping windows leave only ~k/w independent trend points (crude
   correction predicts FA ~ 10% where the iid null predicts ~0.001%; measured 6%);
   and the memory class's variance sigma^2/(1-rho^2) stays within 1.33 sigma^2 for
   rho <= 0.5, so the trend lives in the last stretch of the series — long flat
   histories dilute small-window trends (46 -> 6 catches as n runs 60 -> 400 at w = 20)
   and leave adequate ones flat (110 at w = 50, any n).
2. **Not the language or the code.** A JavaScript port (independent RNG, independent
   floats) reproduced six cells within binomial noise; an independent path through the
   module's own functions matched its flags 36/36.
3. **Not the docstring or the repo's honesty.** Both carry their limits as stated text
   ("readings, never a verdict"; "one construction").
4. **The raw rule is w-biased in both directions.** Too strict at small w (6/200
   detection at w = 20, limit 0.5), too loose at large w under limit 0.3 (drift leak
   29/200, white FA 20/200). Calibration removes both: detection ~ 65-79% at every w,
   FA at the stated alpha, drift and step leaks closed.
5. **Step and drift are not precursors to this instrument** once the null is right.
   The raw rule's drift leak was the inflated null, not the signal.

## Independent validation (found by literature search; snippets, not full texts)

```text
Dakos et al. 2012, PLoS ONE (methods for EWS in time series): same instrument
  class; rolling windows "half the size of the datasets"; window/bandwidth
  sensitivity analysis; significance from 1,000 surrogate datasets, not the iid
  null. The repo's "half the series" heuristic is this paper's rule of thumb.
Boettiger & Hastings 2012, J. R. Soc. Interface 9: "Quantifying limits to
  detection of early warning for critical transitions" — under the null, Kendall's
  tau "takes on almost any value in its range". Same inflated null, measured here.
O'Brien et al. 2023, Nat. Commun. 14: EWS "limited applicability to empirical
  lake data" — field-scale confirmation of the limitation.
```

## Limits

One construction per class; drift slope and step size are declared constants, not
swept. Calibration Monte Carlo: 100 seeds x 100 surrogates -> rate errors about
+/- 5 pp. Phase randomization asks "trend beyond a stationary series with the same
average spectrum" — a slightly different question than the raw flag; declared.
Scheffer et al. 2009 remains recalled-not-reread upstream (VERIFY).

## Reproduce

`python3 glyph/precursor.py --selftest` (10/10), then the sweep/calibration cells as
declared above; numpy path verified identical to the module's rolling stats on 30
random series before any run.
