# Thermal Sensor Degradation Audit

CC0. stdlib-only. Anti-freeze. A single-file audit for asking *what does
sustained heat do to the sensor package that is supposed to measure the heat* —
the mounting hardware, the polymer seals, the electronics, and the reading
itself.

This is scaffolding, not authority. Every layer returns a **falsifiable
prediction**, not a stored verdict. When the field measurement disagrees with a
prediction, update the claim — do not retune the sim to match.

---

## What it is / is not

IS: a lumped, hand-checkable pass over seven degradation pathways that all share
one driver (temperature over time), rolled into one `audit()` call that returns
a package-level `GREEN` / `YELLOW` / `RED` verdict plus the per-layer numbers and
the experiment that would refute each one.

IS NOT: an FEA model, a qualification test, or a substitute for co-located
reference hardware. The material constants are handbook envelopes and the
kinetics are order-of-magnitude Arrhenius/Q10 accelerations. Treat the outputs
as a triage that tells you *which joint, seal, or channel to instrument first*,
not as a pass/fail certificate.

---

## Layers

| layer | function | what it answers |
|---|---|---|
| L1 material properties | `MATERIALS`, `f_to_c` | CTE, service ceiling, creep onset for 15 common mount/enclosure materials |
| L2 wet bulb | `wet_bulb_c` | Stull (2011) approximation — the human maintenance window and the corrosion driver |
| L3 surface amplification | `surface_temp_c` | dark surface in full sun runs well above air temp (lumped radiative-convective balance) |
| L4 differential expansion | `pair_mismatch` | mismatch microstrain + displacement across a bolted dissimilar-material pair |
| L5 gasket compression set | `compression_set` | Arrhenius-accelerated permanent seal deformation over an exposure window |
| L6 electronic drift | `aging_multiplier`, `sensor_drift` | Arrhenius (Ea ≈ 0.7 eV) aging multiplier vs the 25 °C rating, projected drift |
| L7 corruption signature | `corruption_signature` | detects the low-bias fingerprint of a sensor degrading *during* the event it measures |
| driver | `audit` | one call → package verdict, worst flag wins |

---

## The headline claim (L7)

The measurement-corruption layer carries the argument the rest of the stack
supports:

> **corruption(trend) = corruption(measurement) × corruption(framework)** —
> multiplicative, not additive.

A sensor package degrades *during* the extreme events it is deployed to record.
Differential expansion loosens the mount, compression set breaks the seal, and
Arrhenius aging accelerates all at the tail of the distribution — exactly when
the reading matters most. The signature is **variance collapse + range clipping
+ a post-event step offset**, and its direction is **low-biased**: the recorded
tail understates the true tail. A network that is silently losing sensitivity at
the top of its range will report a *calmer* record than reality, and a framework
that trusts the record inherits the bias multiplicatively.

---

## Refutation protocol (refute the claim, not the model)

Each layer ships the experiment that would break it, in its `falsify` field.

**TSD_001** — *A dissimilar-material bolted pair flagged GREEN loses <5 % fastener
torque over 30 thermal cycles; a RED pair loses materially more.* Refutation:
instrument torque and fretting wear on a GREEN joint and a RED joint over 30
cycles. If the GREEN joint loosens or the RED joint holds, the microstrain
thresholds in `pair_mismatch` are wrong.

**TSD_002** — *A gasket held above its creep-onset temperature for the exposure
window takes the predicted permanent set.* Refutation: pull the gasket, measure
recovered thickness vs original. If recovery beats the model's `set_fraction`,
the base rate or Q10 in `compression_set` is wrong.

**TSD_003** — *Sensor drift tracks the Arrhenius projection within 2×.* Refutation:
co-locate a reference-grade sensor for the exposure window; if the field unit's
divergence falls outside 2× of `projected_drift_pct`, the Ea or enclosure-rise
estimate is wrong.

**TSD_004** — *The corruption signature (variance collapse + range clipping) marks a
low-biased tail.* Refutation: run an independent mobile reference traverse during
a heat event. If the fixed network's tail does **not** read low against the
traverse when the signature fires, L7 is detecting an artifact, not a bias.

A failed check updates the claim. The material constants and kinetic rates are
frozen estimates; the *coupling* — heat drives all seven pathways together, and
they bias the record in one direction — is what the audit asserts.

---

## Run it

```
python3 thermal_sensor_degradation_audit.py
```

Ships with a heat-dome worked case (110 °F air, 45 % RH, 45 days sustained) that
returns a `RED` verdict — the aluminum/ABS and steel/nylon mounts blow past the
microstrain ceiling and both elastomer gaskets reach full compression set.
Sample output at
[`samples/heat_dome.sample.txt`](samples/heat_dome.sample.txt).

Call `audit()` directly with your own air temp, humidity, exposure window,
material pairs, and gasket list. `corruption_signature()` takes before/during
reading arrays and is not wired into the driver — feed it your own network
traces.

## License

CC0 / public domain. See this folder's `LICENSE` and the repo root `LICENSE`.
