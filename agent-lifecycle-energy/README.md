# agent-lifecycle-energy

The GAP 4 measurement rig, built to `WORK_ORDER.md`. It measures the joule
cost of agent **disposability**: N single-task agents (each paying a full
spin-up and teardown) against one persistent agent doing N tasks (paying
spin-up and teardown once), holding work delivered constant. In every current
accounting the two look identical. In joules they are not, and the headline
figure — `succession_loss` — is the difference.

## The number is the gap

The work order asks for a measurement, and this environment cannot take one:
no GPU, no wall AC meter, no `nvidia-smi` (`trace_parse.probe_hardware()`
reports `capture_runnable=False`). So **no joule figure is produced and none
is fabricated** — the first number is the posted gap, exactly as the work
order's POSTING NOTE frames it (`RIG_STATUS.md`). What ships is the machinery,
correct by construction and exercised on constructed traces whose areas are
known in advance.

## What it computes

Joules by phase over a lifecycle — idle / spin-up / task / teardown —
baseline-subtracted against the idle window so the figure is marginal:

```
E_phase = integral (P(t) - P_idle) dt        trapezoidal, over the phase
```

on **two channels** (wall meter = full system draw; card telemetry =
accelerator only), for **two lifecycle patterns** (RUN A: N disposable
single-task agents; RUN B: one persistent agent, N tasks). Derived:

- `setup_fraction` = E_spinup / (E_spinup + E_task + E_teardown), per lifecycle;
- `amortization_curve` = joules_per_task vs N — falls for RUN B toward the
  per-task floor, flat for RUN A;
- `succession_loss` = (total E, RUN A) − (total E, RUN B) at the same N =
  **(N−1) × (E_spinup + E_teardown)**, the joule cost of disposability.

## Two work-order rules enforced in code, not described

- **Wall and card are never blended.** Every derived figure takes one
  `channel`; `blend_wall_card` raises. `wall_card_ratio` compares them (the
  "delta between A and B" the work order asks for) without summing.
- **Cold and warm are never averaged.** `mean_over_runs` and
  `amortization_curve` raise `ThermalStateMix` on a mixed set; the render
  prints cold and warm as separate blocks.

## Absent is not zero

A phase with no samples is `NO_SAMPLES` (`joules=None`); one sample is
`SINGLE_SAMPLE`; a phase below the work order's 10 Hz floor is `UNDERSAMPLED`
— a real number **and** a flag, because "1 Hz will miss the peak and
undercount." A run missing any phase has a `NOT_COMPUTABLE` total, never a
partial sum passed off as a whole.

## Files

| file | what |
|---|---|
| `WORK_ORDER.md` | delivered verbatim |
| `phase_energy.py` | the integrator, the per-run record, the derived figures, the enforced invariants |
| `trace_parse.py` | nvidia-smi and wall-CSV parsers + the hardware probe |
| `render.py` | the report (raw records beside derived figures), screened through `no_severity` |
| `selftest_ale.py` | 42 checks on constructed traces |
| `CLAIM_TABLE.md` | `ALE_001..ALE_009` |
| `RIG_STATUS.md` | why no number here, and how to produce one on hardware |
| `samples/ale_report.sample.txt` | one constructed report |

## Run

```
python3 agent-lifecycle-energy/selftest_ale.py       # 42 checks
python3 agent-lifecycle-energy/render.py             # print the sample report
python3 tools/known_answer.py                        # the integrator's known-answer run
```

The integrator is registered in `tools/known_answer.py` (constant / ramp /
zero-marginal, distinct expected values) and covered by the repo's
known-answer test. `phase_energy.py` and `trace_parse.py` refuse
`--selftest` with rc 2. Stdlib only, parses under Python 3.9,
phone-buildable, CC0. This rig measures ONE local machine, ONE model,
lifecycle patterns held against each other — a small claim, and currently an
unmade one.
