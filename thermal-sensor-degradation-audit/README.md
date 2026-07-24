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

Each layer ships the experiment that would break it in its `falsify`
field. The four claims TSD_001–004 (mount pair, gasket, drift, corruption
signature) live in [`CLAIM_TABLE.md`](CLAIM_TABLE.md) alongside the
frozen-vs-on-the-table breakdown and scope bounds.

A failed check updates the claim. The material constants and kinetic
rates are frozen estimates; the *coupling* — heat drives all seven
pathways together, and they bias the record in one direction — is what
the audit asserts.

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
material pairs, and gasket list. To auto-integrate the L7 corruption
check into the package verdict, pass `readings_before=` and
`readings_during=` (per-timestamp reading arrays from your network); if
both are supplied, a positive signature (variance collapse + range
clipping) flags the whole package RED for record trustworthiness, even
when the physical-layer flags are green.

## License

CC0 / public domain. See this folder's `LICENSE` and the repo root `LICENSE`.
