# L7 iteration — walking the scientific-method loop on the headline claim

The **L7 multiplicative-bias claim** is the audit's payoff — every other
layer supports it. It deserves a hard pass under the loop: **restate →
review → scope → modify → find missing variables → test again → align**.

This file is the record of one iteration. When the next iteration runs
(field data comes back, or someone tightens an operator), amend below —
don't retune the code to save the previous phrasing.

---

## Iteration 0 — the shipped claim

**L7 v0:** *corruption(trend) = corruption(measurement) × corruption(framework) —
multiplicative, not additive.*

- Encoded by `corruption_signature` returning `variance_collapse` and
  `range_clipping` booleans plus a "LOW-BIAS LIKELY" read.
- Refutation: independent mobile reference traverse during heat event.

## Review — what's underspecified

1. **"corruption" is not operationally defined.** Is it bias magnitude?
   Fractional bias? Direction-signed? The code emits only booleans, so
   the multiplicative-composition promise cannot be directly measured
   from the audit's own output.
2. **"Multiplicative" is not verifiable from what the code returns.**
   Two booleans cannot show `b_trend ≈ b_m × b_f`. The claim asserts
   a functional form the code doesn't emit.
3. **Direction is asserted but not measured.** The read says "LOW-BIAS
   LIKELY" — but nothing in the code shows sign; the range check
   ignores whether the clipping is symmetric or one-sided.
4. **Scope is implicit.** The claim reads as universal but only applies
   to physically instrumented sensor packages exposed to extreme events.
   Digital measurement chains with self-referential calibration
   (GPS timing against atomic clocks) are outside the shipped scope.
5. **Framework corruption is not modelled.** The audit measures
   `corruption(measurement)` proxies (L1–L6). The framework term is
   the whole `× corruption(framework)` factor and it does not appear
   in the code — the claim asserts a two-factor product from one-factor
   evidence.

## Modify — L7 v1 (operational restatement)

**L7 v1:** For a sensor package operating past its service ceiling
during an extreme event:

1. Let `b_m` = fractional measurement bias
   `b_m = (mean(readings_during) − mean_true) / mean_true`
   where `mean_true` comes from a co-located reference traverse.
2. Let `b_f` = fractional framework/aggregation bias — the transformation
   the network's reporting protocol applies to the raw stream (median
   vs mean, spatial averaging, outlier rejection, clipping to service
   ceiling in the datalogger).
3. The **claim** is `b_trend ≈ b_m × b_f` and `sign(b_trend) < 0`
   (systematic under-report toward the extreme tail).
4. The **shipped signature** (`variance_collapse` AND `range_clipping`)
   is a **necessary but not sufficient** condition for a positive
   L7 verdict. The signature identifies packages *at risk* of the
   product structure; it does not measure the product itself.

## Search — missing variables

Candidates the current audit does not wire in that plausibly move the
multiplicative product:

| variable | why it matters | proposed home |
|---|---|---|
| **time since last calibration** (`t_cal_days`) | Arrhenius drift compounds with cumulative exposure time. Two packages with identical mount/gasket/electronics but one at t_cal=30d and one at t_cal=1000d have very different `b_m`. The current `sensor_drift` uses `days` as event window, not cumulative exposure. | `sensor_drift(..., t_cal_days=None)` |
| **maintenance-window closure during the event** | The wet-bulb human-limit note (>31 °C) says field maintenance closes during severe heat. If the extreme-event window is also when calibration would have caught the drift, deferral compounds the L1–L6 damage directly. Currently invisible in `audit()`. | `audit(..., maintenance_deferred=None)` |
| **network reporting protocol** (mean vs median vs trimmed mean) | This IS the framework-corruption term. A network reporting medians is robust to `b_m`; one reporting means propagates it multiplicatively. | new `framework_transform(...)` layer |
| **enclosure ingress** (moisture past a degraded gasket) | Compression set on the gasket doesn't just break the seal — it lets moisture in, which changes `aging_multiplier` (electrolytic aging accelerates in humid interiors). This is a coupling `compression_set` → `sensor_drift` the code currently treats as independent. | modify `sensor_drift` to accept a gasket-set fraction |
| **solar spectrum / cloud fraction** | `surface_temp_c` uses a fixed `solar_w_m2=1000`. Clouds during the event drop the amplification; clear skies push it. Real-event traces need the actual radiation. | expose `solar_w_m2` in `audit()` (already an arg on `surface_temp_c`) |
| **wind gustiness** | Scalar `wind_ms` misses the stochastic peaks that can transiently cool sensors below air. Affects the timing of the bias, not its sign. | future; requires timeseries not scalar |
| **reference-device decay** | If the "reference" the field traverse uses has itself been heat-soaked, `b_m` is confounded. This is not a code fix — it's a protocol requirement in the refutation experiment. | add scope-bound note in CLAIM_TABLE |

**Chosen for this iteration (the two whose absence directly breaks the
multiplicative-product claim):**

- `time_since_calibration_days` in `sensor_drift`
- `maintenance_deferred` in `audit()` (compounds with L1–L6 flags when
  the wet-bulb closes the maintenance window)

## Test again — new claims

Two claims land in `CLAIM_TABLE.md` as **TSD_005** and **TSD_006**;
`test_thermal_sensor_degradation_audit.py` gets new cases for both.

- **TSD_005 (cumulative calibration drift):** projected drift scales
  approximately linearly with time since last calibration at fixed
  internal temperature. Refutation: reference-instrument comparison
  at two `t_cal_days` values (e.g. 30, 365) should show drift ratio
  approx `365/30 ≈ 12` at same internal_c.
- **TSD_006 (maintenance-deferral compounding):** when the wet-bulb
  crosses 31 °C and `maintenance_deferred=True`, the package verdict
  fires RED even when the physical-layer flags are YELLOW. The
  human-limit note stops being a note; it enters the verdict.

## Align — what this iteration DOES and DOES NOT do

**Does:**

- Restate L7 with operational definitions of `b_m`, `b_f`, sign, and
  the necessary-but-not-sufficient status of the signature.
- Add `bias_estimate_fraction` and `sign` outputs to
  `corruption_signature`, so the multiplicative product becomes
  computable when a caller supplies reference-traverse means.
- Wire `time_since_calibration_days` and `maintenance_deferred` into
  `sensor_drift` and `audit` respectively.
- Add TSD_005 and TSD_006 to CLAIM_TABLE with specific refutation
  experiments and expected numerical predictions.
- Test all three additions.

**Does not (queued for a next iteration):**

- Model the framework-corruption term `b_f` as a real component —
  currently the audit still measures only the `b_m` side; the
  multiplicative structure is testable only when a caller supplies
  BOTH `b_m` from reference-traverse AND `b_f` from the network's
  reporting protocol.
- Timeseries wind / solar / humidity forcing — the current audit is
  lumped by design.
- Reference-device decay guard — added as a scope bound only.

## What refutes L7 v1

If a field campaign supplies `b_m` (from reference traverse) AND `b_f`
(from replaying the network's aggregation on both raw and processed
streams) AND the reported `b_trend` differs from `b_m × b_f` by more
than one order of magnitude in either direction across a heat-dome
sample — the multiplicative form is wrong, or a hidden variable moves
the product. Rewrite L7 v2 to the actually-observed functional form
and add whichever variable(s) close the gap.
