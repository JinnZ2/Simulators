# CLAIM_TABLE -- meander-ledger (MGL_)

Ids are permanent. Status: SUPPORTED / REFUTED / UNVERIFIED. Each claim names
what would move it.

```text
MGL_001  SUPPORTED   Sediment budget closes in 13 of 13 unplanted toy runs and a planted
                     hidden removal reads LEAK. Closure is by construction (every transfer
                     is a counter); it says nothing about flux sizes.
                     moves if: a run closes with the leak planted (T_SED_LEAK_DETECTED)
MGL_002  SUPPORTED   Water and energy closures are identities in this model and carry no
                     information; they are flagged IDENTITY in every report.
                     moves if: either budget gets independent counters (Q-05)
MGL_003  SUPPORTED   The toy reads depth and friction only through alpha = 2 Cf / H
                     (equal-alpha runs byte-identical).
                     moves if: T_ALPHA_ONLY fails
MGL_004  SUPPORTED   Sediment supply has no path into the planform (supply 0.2 and 2.0
                     byte-identical planforms).
                     moves if: T_SUPPLY_NO_PLANFORM fails, or a coupling term is added (Q-07)
MGL_005  SUPPORTED   The toy's lam/W is not grid-converged: ~8 at ds 0.5, 2.62 at ds 0.25.
                     No toy ratio is quotable as a property of the model.
                     moves if: a ds sweep with physically-scaled smoothing converges (Q-10)
MGL_006  SUPPORTED   In DS_THAPA_2025 lambda is nearly flat across W 30 m..3 km and
                     lam/W tracks 1/W (sd log ratio 0.484 vs sd log W 0.486; Spearman -0.733).
                     moves if: the file's hash changes, or a water-body mask changes the
                     width-bin table (Q-11)
MGL_007  SUPPORTED   The dataset's two wavelength columns do not agree (Spearman +0.033).
                     moves if: the method behind 'Wavelength (m)' is found and recomputed (Q-03)
MGL_008  UNVERIFIED  The recalled lambda ~ 10-14 W is a property of rivers. Not tested:
                     the source tables were not read, and this dataset cannot test it
                     (MGL_006: its instrument sets lambda).
                     moves if: Q-01's two-method comparison runs
MGL_009  SUPPORTED   Both wavelength estimators in this folder read noise as bends: the toy's
                     counts jitter-scale sign changes, the dataset's has a floor at its DEM
                     scale. Neither has a stated floor.
                     moves if: a known-curve run gives either a floor below its noise (Q-09)
MGL_010  SUPPORTED   No coincidence card here reaches slot 6; the card has no slot for a
                     missing coupling, and MC_004 is filed under shared_constraint with the
                     reading strained.
                     moves if: Q-18's coding of known missing-coupling cases fits slot 1
```
