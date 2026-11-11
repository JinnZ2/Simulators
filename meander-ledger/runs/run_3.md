# run_3 -- TOO-SMOOTH CHECK on an open dataset (DS_THAPA_2025)

```text
code       : tools/scatter.py
seed       : 0 (slot-5 shuffle null, 200 reps)
params     : data/raw pinned at 0b9be85c, sha256 02aa7825 ; meander = distinct (Wavelength, Meander length, Sinuosity) [CHOICE 1] ; lambda <= 0 excluded [CHOICE 2]
results    : 16951 meanders ; lam/W median 15.81, IQR 7.23..29.27, p05..p95 1.68..63.02 ; 11.6% in 10..14 ; log-log slope 0.228, R2 0.116 ; linear R2 0.059 ; Spearman(ratio, W) -0.733 ; null R2 max 0.0005
flags      : 5 (below)
provenance : DERIVED -- recomputed in this tree from a third-party file (MIT): python3 tools/fetch_data.py && python3 tools/scatter.py
feeds      : L5_WAVELENGTH_ESTIMATOR ; L5_WIDTH_WATERMASK ; L5_SLOPE_DEM_PIXEL ; L5_LEOPOLD_WOLMAN_RATIO ; MC_001
l0_closure : void (observation run; no budget)
```

## Flags

```text
- The recalled relation is not in this dataset. lambda is nearly flat (median 1.6 to
  3.2 km) while W runs 30 m to 3 km, so lam/W is mostly 1/W: sd log10(ratio) 0.484,
  sd log10(W) 0.486. The 10..14 band is crossed only near W 100-200 m (bin median 13.80).
- Not too smooth -- too rough, and the roughness points at the instrument: lambda's
  floor (1st pct 358 m) sits at the DEM smoothing / 200 m vectorisation scale.
- The file carries two wavelength columns that do not agree (Spearman +0.033); the
  shipped script computes the second from coordinate differences; the first has no
  shipped method.
- W includes lakes and reservoirs (to 20101 m). Bank material and discharge are absent.
  Slope is a 30 m DEM pixel gradient and carries nothing (Spearman +0.003).
- The dataset's own meander classes sort by lam/W (Complex 2.97 ... Incipient 38.51; 1738 meanders carry mixed class labels across points, resolved by mode with a sorted tie-break [CHOICE 3]);
  they were built from these same geometric columns, so they are not an independent axis.
```
