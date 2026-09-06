# RIG STATUS — the number is the gap

The work order asks for a measurement. This records why one has not been
taken here and exactly what it would take to produce one, so the gap is
posted rather than papered over.

## Not runnable in this environment

The rig needs three things this machine does not have:

```
GPU / accelerator      absent
wall AC power meter     absent (external device, never auto-detected)
nvidia-smi on PATH      absent  (trace_parse.probe_hardware(): nvidia_smi=None)
```

`trace_parse.probe_hardware()` reports `capture_runnable=False` here. So
**no joule figure is produced, and none is fabricated.** The rig ships ready
to run; the first number is the current gap, exactly as the work order's
POSTING NOTE states.

This is the same posture the rest of this session's builds take toward
egress-blocked data: build the machinery, exercise it on constructed inputs
whose answer is known in advance, and mark the real measurement as the gap
rather than inventing a value for it.

## What HAS been done, on constructed traces

- the phase integrator `integral (P(t) - P_idle) dt` is trapezoidal,
  baseline-subtracted, and registered in `tools/known_answer.py` with three
  cases (constant / ramp / zero-marginal) whose areas are fixed by
  construction and whose expected values are all distinct;
- the per-run record holds each phase energy as a number **plus its state**,
  so an absent phase is `None` (not `0.0`) and an undersampled phase carries
  a number **and** an `UNDERSAMPLED` flag;
- undersampling is demonstrated: a narrow spike sampled at 5 Hz undercounts
  the same spike at 200 Hz and is flagged, matching the work order's "1 Hz
  will miss the peak";
- `succession_loss` reduces to `(N-1) x (E_spinup + E_teardown)` and is exact
  on constructed runs; `amortization_curve` for RUN B falls with N toward the
  per-task floor while RUN A stays flat;
- wall and card are never blended (`blend_wall_card` raises); cold and warm
  are never averaged (`mean_over_runs` / `amortization_curve` raise on a mix).

## To produce the first number, on a machine that has the hardware

1. Inline a wall AC meter with a logged export (Kill-A-Watt / smart plug).
2. Log the card at >= 10 Hz:
   `nvidia-smi --query-gpu=power.draw --format=csv,noheader -lms 100`
3. Mark the four phase windows (idle / spin-up / task / teardown) by wall
   clock, per run.
4. Parse with `trace_parse.parse_wall_csv` and `trace_parse.parse_nvidia_smi`
   (pass the `-lms` value as `interval_s`), build `LifecycleRun`s with
   `phase_energy.run_from_traces`, and render with `render.py`.
5. Record cold vs warm separately, ambient temperature, and the hardware and
   model — a joule figure without those is not reproducible.

The acceptance test is met elsewhere, by a second party: the DIRECTION and
SHAPE of the amortization curve reproducing on different hardware. Absolute
joules are hardware-specific; the shape is the finding.
