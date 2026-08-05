# null-harness

**Calibrate any gate against known-answer controls before you trust it.**

A "gate" is any callable `f(data) -> bool | str verdict`. The harness
knows nothing else about it. Runs the gate over N draws of a
negative control (correct answer: don't fire) and N draws of a
positive control (correct answer: must fire), reports FP and TP,
sweeps the positive-control amplitude to find the smallest signal
the gate can detect, and applies a fail-condition classifier.

CC0. `numpy` + stdlib. Single file.

## Fail conditions the harness catches

| shape                    | verdict                            | meaning                                  |
|--------------------------|------------------------------------|------------------------------------------|
| `FP ≥ 0.9 ∧ TP ≥ 0.9`   | `CONSTANT_FIRES`                   | always says "yes"; not a gate            |
| `FP + TP < 0.10`         | `CONSTANT_SILENT`                  | never says "yes"; not a gate             |
| `FP > 0.10`              | `TOO_MANY_FALSE_ALARMS`            | too many false alarms                    |
| `\|TP − FP\| < 0.10`     | `NO_DISCRIMINATION`                | fires at same rate on both               |
| otherwise                | `OK`                               | real gate; `min_amp` is the sensitivity |

## Controls (correct answer is known)

**Negative (gate should not fire):**

- `gen_white_noise(N, sigma)` — no scale structure
- `gen_wellposed_fisher(k)` — identity, condition number 1
- `gen_null_residual(N, sigma)` — `y_obs = y_pred + noise`
- `gen_smooth_surface(N)` — polynomial, no singularity anywhere

**Positive (gate must fire; `amp/eps/strength/ratio` is the sweep knob):**

- `gen_noise_with_z2_term(N, amp)` — noise plus a real hidden `x²`
- `gen_degenerate_fisher(k, eps)` — one small eigenvalue = true rank deficiency
- `gen_true_pole(N, x0, strength)` — actual `1/(x-x0)` singularity
- `gen_scale_dependent_noise(N, ratio)` — real heteroskedasticity

## Usage

```python
from null_harness import (
    gen_white_noise, gen_noise_with_z2_term,
    bake_off, sweep_threshold, report,
)

# your gate: any callable that returns bool | str
def my_gate(data):
    x, r = data["x"], data["residuals"]
    A = np.vstack([np.ones_like(x), x, x*x]).T
    coef, *_ = np.linalg.lstsq(A, r, rcond=None)
    return abs(coef[2]) > 3 * ols_stderr(coef, A, r)

# calibrate
row = bake_off(my_gate,
               gen_white_noise(200),
               gen_noise_with_z2_term(200, amp=0.5),
               n_draws=1000)
row["min_amp"] = sweep_threshold(
    my_gate,
    lambda a: gen_noise_with_z2_term(200, amp=a),
    amps=[0.02, 0.05, 0.1, 0.2, 0.5],
    n_draws=200)
report([{"name": "my_gate", **row}])
```

Registry is a dict the caller fills. No imports required to plug in a
new gate — just pass the callable to `bake_off`.

## What "fires" means

Default: Python truthiness. `True` fires, `"EQUIPMENT_NOISE"` fires,
`False` / `""` / `None` do not. If the gate returns a string verdict
and only ONE of its values counts as "fire," wrap the gate:

```python
def m2_gate1(data):
    md = MetrologyDiagnostic(...).run()
    return md["gates"]["Gate1_Scale"] == "EQUIPMENT_NOISE"
```

That way the same harness handles bool-returning and category-returning
gates the same way.

## Demo — including a gate the static reading predicted would fail

[`samples/null_harness.sample.txt`](samples/null_harness.sample.txt)
runs five gates:

```
gate                              FP      TP     min_amp   verdict
------------------------------------------------------------------
always_true_gate               1.000   1.000         n/a   CONSTANT_FIRES
always_false_gate              0.000   0.000         n/a   CONSTANT_SILENT
z2_ols_3sigma                  0.004   1.000         0.2   OK
fisher_smin<0.05               0.000   1.000         n/a   OK
M2_Gate1_EQUIPMENT_NOISE       0.000   0.000         n/a   CONSTANT_SILENT
```

- The two trivial gates (`always_true`, `always_false`) prove the
  harness catches both trivial-fail shapes.
- `z2_ols_3sigma` is a real gate: FP = 0.004 (well below the 0.10
  cutoff), TP = 1.000, min_amp = 0.2 (smallest `x²` amplitude at
  which TP ≥ 0.5 on 200 draws).
- `fisher_smin<0.05` discriminates identity from a matrix with one
  small eigenvalue.
- **`M2_Gate1_EQUIPMENT_NOISE`** — Gate 1 of the
  `energy/modules/metrology_diagnostic.py` stack, wrapped as a
  callable. Comes back **CONSTANT_SILENT (FP = TP = 0)**. Static
  reading of the code explains why: for equal-size halves,
  ```
  res_coarse = ( mean|first_half| + mean|second_half| ) / 2
             = ( sum|first| + sum|second| ) / (2 * n_half)
             = mean|all|
             = res_fine
  ```
  so `ratio1 ≡ 1.0` and the `> 1.8` branch is unreachable. Gate 1
  emits `SYSTEMATIC_SIGNAL` on every input. The harness verifies
  the static prediction empirically over 200 draws of white noise
  and 200 of scale-dependent noise, and returns
  `CONSTANT_SILENT` under the `EQUIPMENT_NOISE`-fires convention.
  Either that convention or the mirror one (`fires ==
  SYSTEMATIC_SIGNAL`) diagnoses the same thing — the gate is
  constant, not a gate.

## Why this file exists

The rest of the repo has audits and lenses that call code they trust.
This is the trust-calibration step: before a gate is used to reject a
model or accept a "verdict," the harness checks whether it can even
tell noise from signal. The four fail-conditions above are the
minimum. Any gate that survives here is a real gate; any gate that
does not is on the fix-or-remove list.

Pairs naturally with:

- `divergence-playground/null_ensemble.py` — tests whether an
  *observation* could arise by chance under a null.
- `divergence-playground/coincidence.py` (C1–C4) — tests whether a
  *convergence* across observations is real.
- `null-harness/null_harness.py` (this file) — tests whether a
  *gate* can distinguish signal from noise in the first place.

Three levels: **observation ≠ chance? → convergence ≠ shadow? → gate
≠ constant?** All CC0, all stdlib-plus-numpy at most.

## License

CC0 1.0 Universal. Public domain.
