# sustained-activation-gate

**A stuck-carrier / hysteresis module for the cascade-regime family.**

Tilted quartic double-well with Kramers-escape noise. A brief drive relaxes.
A drive held past threshold locks the order parameter "on" and it does not
relax when the drive drops. A targeted inhibition can release the lock
without moving the baseline — but only if the coupling between order
parameter and baseline is below a boundary θ.

CC0. stdlib only. Phone-buildable. No numpy, no network, no cloud.

## What it does

- **FIRM** physics: tilted double-well, Kramers escape, hysteresis. Fixed
  points solved directly for the shipped `WellConfig`.
- **SOLID** exploration: sweeps `baseline_leak` and locates the boundary θ
  where a sustained lock stops sparing baseline.
- **INSTRUCTIVE NEGATIVE**: shows θ is *duration-independent* — baseline
  collapses faster than the lock persists, so drag is set by coupling, not
  by dwell time.
- **FRONTIER (now built)**: θ(restore_rate). Faster homeostasis tolerates
  more coupling. The trade-off Tier 3 relocated, now runnable.

The physics claims are structural (they stand regardless of substrate);
the biology labels are held in a swappable `INTERPRETATION` dict tagged
inline with confidence.

## Reliability tiers

| Tier | Surface | Result |
|---|---|---|
| **FIRM** | `compare_programs()` | 4/4 structural claims come out True: brief relaxes, sustained locks 129 steps, inhibition releases cleanly, baseline preserved |
| **SOLID** | `explore_separability()` | Clean boundary **θ ≈ 0.0052** at default config, by bisection |
| **INSTRUCTIVE NEGATIVE** | `explore_theta_vs_persistence()` | θ flat at 0.0052–0.0054 across noise 0.006–0.060 — drag saturates fast, set by leak not by dwell |
| **FRONTIER (built)** | `explore_theta_vs_restore()` | θ rises **23.9× as restore grows 40×** (0.0013 → 0.0307) — separability is a race between restoration and coupling |

## Interpretations (SOFT layer)

`INTERPRETATIONS` is a registry of substrate labels for the same physics.
Set `SELECTED_INTERPRETATION` to one of:

| key | substrate | confidence |
|---|---|---|
| `c1_vlpag_stress_circuit` | mouse C1→vlPAG stress circuit, days-long anxiety lock (default) | ANALOGY_GRADE — one paper, small-n, unsettled |
| `amoc_overturning` | Atlantic Meridional Overturning bistability, freshwater loading | STRUCTURAL_ANALOGY — bistability well established; release arm speculative |
| `grid_load_blackout` | cascading blackout as a load-driven lock, controlled islanding as release | ENGINEERING_ANALOGY — textbook cascading-failure class |

The physics rows are identical across interpretations. Only the labels
move. Add a new substrate by adding a dict; if the shape (brief-relaxes /
sustained-locks / inhibition-releases / baseline-spared) applies, the
labels transfer without editing any dynamics code.

## Run

```
python3 sustained_activation_gate.py
```

Runs all four surfaces in order and prints the audit. Pinned output at
[`samples/sustained_activation_gate.sample.txt`](samples/sustained_activation_gate.sample.txt).

## Key results (reproduced verbatim from the pinned sample)

### Structural (Tier 1)
- brief spike relaxes on its own: **True**
- sustained drive locks (hysteresis): **True**
- targeted inhibition releases lock: **True**
- release spares baseline: **True**

### Separability boundary (Tier 2)
- separability holds for **leak < θ ≈ 0.0052**
- below θ: the lock spares baseline (the "spares autonomic function" arm)
- above θ: sustained lock drags housekeeping — the claim would fail

### Persistence axis is duration-independent (Tier 3, instructive negative)
- θ ≈ 0.0052–0.0054 across noise 0.006 → 0.060
- drag saturates fast; dwell time is not the controlling variable
- single-seed lock durations are metastable noise, must be seed-averaged

### The frontier surface
- **θ rises 23.9× as restore grows 40×** (0.0013 → 0.0307)
- "spares baseline" is possible on either side of the trade-off:
  near-zero coupling **OR** fast restoration
- **Wet-lab payoff:** a measured value for autonomic restoration rate
  OR for order-parameter → baseline coupling pins the other via this curve

## Refutation protocol

Every claim is refutable. See [`CLAIM_TABLE.md`](CLAIM_TABLE.md). When a
claim fails, **update the claim** — never retune the constants to protect
a favored surface. The trajectory is the witness.

Every surface in this file was rebuilt at least once because iterative
trajectory-checking caught an axis bug that looked correct in aggregate
output. The `_sanity_trajectory` helper is called before the frontier
surface for that reason; do not skip it when extending.

## License

CC0. See the repo root [`LICENSE`](../LICENSE).
