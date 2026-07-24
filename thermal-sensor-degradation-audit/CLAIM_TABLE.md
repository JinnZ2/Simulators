# CLAIM_TABLE — thermal-sensor-degradation-audit

Every claim is refutable. **Refutation protocol: when a claim fails,
update the claim.** Material constants and kinetic rates are frozen
handbook envelopes; the coupling — heat drives all seven pathways
together, and they bias the record in one direction — is the assertion.

## The headline (v1 — see `L7_iteration.md`)

**TSD_L7 (multiplicative bias, operational restatement).** For a sensor
package operating past its service ceiling during an extreme event:

- Let **`b_m`** = fractional measurement bias
  = `(mean(readings_during) − mean_true) / mean_true`
  with `mean_true` from a co-located reference traverse.
- Let **`b_f`** = fractional framework/aggregation bias — the
  transformation the network's reporting protocol applies to the raw
  stream (median vs mean, spatial averaging, outlier rejection,
  clipping to service ceiling at the datalogger).
- The claim is **`b_trend ≈ b_m × b_f`** and **`sign(b_trend) < 0`**
  (systematic under-report toward the extreme tail).

The shipped `corruption_signature` (`variance_collapse` AND
`range_clipping`) is a **necessary but not sufficient** condition for
a positive L7 verdict. The signature identifies packages **at risk** of
the product structure; testing the product itself requires supplying
`b_m` (reference traverse) AND `b_f` (framework replay).

Iteration log lives in [`L7_iteration.md`](L7_iteration.md). v0 was the
metaphorical "corruption(trend) = corruption(measurement) ×
corruption(framework)" line; retired to git history when the review
found `corruption` was not operationally defined.

## The claim table

Each row is a specific falsifiable prediction with a specific field
experiment that would refute it.

| # | Claim | Module | Sample | Refuted if |
|---|-------|--------|--------|-----------|
| **TSD_001** | A dissimilar-material bolted pair flagged GREEN loses <5 % fastener torque over 30 thermal cycles; a RED pair loses materially more. | `pair_mismatch` | [`samples/heat_dome.sample.txt`](samples/heat_dome.sample.txt) | Instrument torque and fretting wear on a GREEN joint and a RED joint over 30 cycles. If the GREEN joint loosens or the RED joint holds, the microstrain thresholds in `pair_mismatch` are wrong. |
| **TSD_002** | A gasket held above its creep-onset temperature for the exposure window takes the predicted permanent set (`set_fraction`). | `compression_set` | [`samples/heat_dome.sample.txt`](samples/heat_dome.sample.txt) | Pull the gasket after the exposure window, measure recovered thickness vs original. If recovery beats the model's `set_fraction`, the base rate or Q10 in `compression_set` is wrong. |
| **TSD_003** | Sensor drift tracks the Arrhenius projection within 2×. | `sensor_drift` + `aging_multiplier` | [`samples/heat_dome.sample.txt`](samples/heat_dome.sample.txt) | Co-locate a reference-grade sensor for the exposure window. If the field unit's divergence falls outside 2× of `projected_drift_pct`, the Ea or enclosure-rise estimate is wrong. |
| **TSD_004** | The corruption signature (variance collapse + range clipping) marks a low-biased tail. | `corruption_signature` (auto-integrated into `audit()` when `readings_before` and `readings_during` are supplied) | (bring your own network trace) | Run an independent mobile reference traverse during a heat event. If the fixed network's tail does **not** read low against the traverse when the signature fires, L7 is detecting an artifact, not a bias. |
| **TSD_005** | Projected sensor drift scales approximately linearly with total time since last calibration at fixed internal temperature. `sensor_drift(..., t_cal_days=T)` returns drift proportional to `(days + T) / 365`. | `sensor_drift` (`t_cal_days=` parameter) | (bring your own two-cal-age comparison) | Reference-instrument comparison at two `t_cal_days` values (e.g. 30 vs 365) should show a drift ratio approximately `(30+event)/(365+event) → ~12` at same internal temp. If observed ratio differs by more than 2×, the Arrhenius-linear composition is wrong for this substrate. |
| **TSD_006** | When the wet-bulb crosses 31 °C AND maintenance is deferred during the extreme event, the physical-layer flags compound. A YELLOW physical verdict upgrades to RED because the extreme-event window is exactly when calibration would have caught the drift; deferral compounds L1–L6 damage. | `audit(..., maintenance_deferred=)` (auto-detected as True when `wet_bulb_c > 31`) | (bring your own maintenance log) | An event with `wet_bulb_c > 31 °C` where maintenance actually occurred AND the package showed only YELLOW physical flags AND the ex-post reference traverse read within 5% of the network record. |

## What is frozen, what is on the table

**Frozen** (handbook envelopes; do not retune to save the audit):

- `MATERIALS` table: CTE, service ceiling, creep onset per material.
- `GASKET_BASE_SET_PER_DAY`: elastomer rates at the 70 °C reference.
- `K_B = 8.617e-5 eV/K`, default `Ea = 0.7 eV`, default `Q10 = 2.0`.
- Threshold triples for the GREEN/YELLOW/RED flags.

**On the table** (update the CLAIM when a field measurement refutes it):

- The specific microstrain thresholds (500 / 1000).
- The specific compression-set thresholds (0.2 / 0.4).
- The 2× projection tolerance in TSD_003.
- The 5th/95th percentile choice inside `_percentile_range`.
- Whether the L7 signature bias is truly low-directional in every
  substrate (asphalt / concrete / instrumented outdoor plate).

## Scope bounds

- The kinetics are order-of-magnitude Arrhenius/Q10 accelerations, not
  FEA. Treat outputs as triage that tells you *which joint, seal, or
  channel to instrument first*, not as a qualification-test result.
- `corruption_signature` percentile check assumes the `before` window
  is representative of pre-event dynamic range. A pre-event window
  already suppressed (recent-history-only recording) will let the
  signature miss a real bias.
- Materials outside `MATERIALS` return no gasket model (silent gate)
  or no CTE (KeyError). Add materials to the table before auditing
  packages that use them.
