# SPDX-License-Identifier: CC0-1.0
"""
Checks for the GAP 4 rig, on CONSTRUCTED traces. No hardware is touched and
no joule figure here is a measurement of anything -- every trace is built by
hand so its integral is known in advance, which is the only way to test the
machinery in an environment with no GPU and no meter (see RIG_STATUS.md).

    python3 agent-lifecycle-energy/selftest_ale.py

Prints `selftest: N checks, M failed` and exits non-zero on any failure.
"""

from __future__ import annotations

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, "tools"))

import phase_energy as pe          # noqa: E402
import trace_parse as tp           # noqa: E402
import known_answer as ka          # noqa: E402

_checks = 0
_failed = 0


def ok(cond, label):
    global _checks, _failed
    _checks += 1
    if not cond:
        _failed += 1
        print("  FAIL: %s" % label)


def raises(exc, fn, label):
    global _checks, _failed
    _checks += 1
    try:
        fn()
    except exc:
        return
    except Exception as ex:          # noqa: BLE001
        _failed += 1
        print("  FAIL: %s (raised %s, wanted %s)"
              % (label, type(ex).__name__, exc.__name__))
        return
    _failed += 1
    print("  FAIL: %s (did not raise)" % label)


S = pe.Sample


def const_trace(watts, dur, hz):
    n = int(round(dur * hz)) + 1
    step = dur / (n - 1)
    return [S(i * step, watts) for i in range(n)]


def make_run(run_id, condition, N, cold_or_warm,
             idle_w=100.0, spin_w=300.0, task_w=250.0, td_w=200.0):
    """One representative lifecycle at fine sampling. Per-episode marginals:
    spin (spin_w-idle)*0.5, task (task_w-idle)*1.0, teardown (td_w-idle)*0.5."""
    idle = {ch: const_trace(idle_w, 0.5, 200.0) for ch in pe.CHANNELS}
    phases = {}
    for ch in pe.CHANNELS:
        phases[ch] = {
            "spinup": const_trace(spin_w, 0.5, 200.0),
            "task": const_trace(task_w, 1.0, 200.0),
            "teardown": const_trace(td_w, 0.5, 200.0),
        }
    return pe.run_from_traces(run_id, condition, N, "toy", "constructed-model",
                              cold_or_warm, 22.0, idle, phases)


# --------------------------------------------------------------------------
print("known-answer gate (integrate):")
ka.seed()
rows = {r["case"]: r["status"] for r
        in ka.run("agent-lifecycle-energy/phase_energy.py::integrate")}
ok(rows.get("constant") == ka.PASS, "known-answer: constant")
ok(rows.get("ramp") == ka.PASS, "known-answer: ramp")
ok(rows.get("zero_marginal") == ka.PASS, "known-answer: zero_marginal")

# --------------------------------------------------------------------------
print("phase integration and per-episode energies:")
r = make_run("r0", "A", 1, "cold")
# spin = (300-100)*0.5 = 100, task = (250-100)*1.0 = 150, teardown = (200-100)*0.5 = 50
s = r.phase("spinup", "card"); t = r.phase("task", "card"); d = r.phase("teardown", "card")
ok(abs(s.joules - 100.0) < 1e-9, "spinup marginal = 100 J")
ok(abs(t.joules - 150.0) < 1e-9, "task marginal = 150 J")
ok(abs(d.joules - 50.0) < 1e-9, "teardown marginal = 50 J")
ok(s.flag == pe.OK and t.flag == pe.OK, "fine-sampled phases flag OK")
life = pe.lifecycle_energy(r, "card")
ok(abs(life.joules - 300.0) < 1e-9, "lifecycle energy = 300 J")
sf = pe.setup_fraction(r, "card")
ok(abs(sf.value - (100.0 / 300.0)) < 1e-9, "setup_fraction = 1/3")

# --------------------------------------------------------------------------
print("absent is not zero (three distinct states):")
idle = {ch: const_trace(100.0, 0.5, 200.0) for ch in pe.CHANNELS}
empty_phases = {ch: {"spinup": [], "task": [S(0.0, 250.0)],
                     "teardown": const_trace(200.0, 0.5, 200.0)}
                for ch in pe.CHANNELS}
r_absent = pe.run_from_traces("r_absent", "B", 5, "toy", "m", "warm", None,
                              idle, empty_phases)
ok(r_absent.phase("spinup", "card").flag == pe.NO_SAMPLES, "empty -> NO_SAMPLES")
ok(r_absent.phase("spinup", "card").joules is None, "NO_SAMPLES joules is None not 0")
ok(r_absent.phase("task", "card").flag == pe.SINGLE_SAMPLE, "one sample -> SINGLE_SAMPLE")
ok(r_absent.phase("task", "card").joules is None, "SINGLE_SAMPLE joules is None")
tot_absent = pe.total_energy(r_absent, "card")
ok(tot_absent.joules is None and tot_absent.flag == pe.NOT_COMPUTABLE,
   "a run with an absent phase has NOT_COMPUTABLE total, not a partial sum")

# --------------------------------------------------------------------------
print("undersampling is flagged, not silently undercounted:")
# a narrow triangular spike from t=0.4 to t=0.6 peaking +500 W over idle=0,
# in a 1.0 s window. True area = 0.5 * 0.2 * 500 = 50 J.
def spike(hz):
    n = int(round(1.0 * hz)) + 1
    step = 1.0 / (n - 1)
    out = []
    for i in range(n):
        x = i * step
        if 0.4 <= x <= 0.5:
            w = 500.0 * (x - 0.4) / 0.1
        elif 0.5 < x <= 0.6:
            w = 500.0 * (0.6 - x) / 0.1
        else:
            w = 0.0
        out.append(S(x, w))
    return out
fine = pe.integrate(spike(200.0), 0.0, "card", "spinup")     # 200 Hz
coarse = pe.integrate(spike(5.0), 0.0, "card", "spinup")     # 5 Hz < MIN_HZ
ok(fine.flag == pe.OK, "fine spike (200 Hz) flags OK")
ok(abs(fine.joules - 50.0) < 0.5, "fine spike recovers ~50 J")
ok(coarse.flag == pe.UNDERSAMPLED, "coarse spike (5 Hz) flags UNDERSAMPLED")
ok(coarse.joules < fine.joules, "coarse undercounts the peak (a real number, flagged)")
ok(coarse.is_number, "undersampled is a present number, not absent (third state)")

# --------------------------------------------------------------------------
print("succession_loss = (N-1)(spin+teardown), exact:")
for N in (1, 5, 20, 100):
    a = make_run("a%d" % N, "A", N, "cold")
    b = make_run("b%d" % N, "B", N, "cold")
    sl = pe.succession_loss(a, b, "card")
    expect = (N - 1) * (100.0 + 50.0)     # (N-1)(spin+teardown)
    ok(abs(sl.joules - expect) < 1e-9,
       "succession_loss(N=%d) = %g J" % (N, expect))
ok(pe.succession_loss(make_run("a1", "A", 1, "cold"),
                       make_run("b1", "B", 1, "cold"), "card").joules == 0.0,
   "at N=1 there is no succession loss (disposable == persistent)")

# --------------------------------------------------------------------------
print("amortization_curve falls as N rises and flattens at E_task:")
bs = [make_run("bB%d" % N, "B", N, "cold") for N in (1, 5, 20, 100)]
curve = pe.amortization_curve(bs, "card")
jpt = [p.joules_per_task for p in curve]
ok(all(jpt[i] > jpt[i + 1] for i in range(len(jpt) - 1)),
   "joules_per_task strictly falls with N (RUN B)")
# limit is E_task = 150 J; at N=100 it is 150 + 150/100 = 151.5
ok(abs(jpt[-1] - 151.5) < 1e-9, "at N=100, joules_per_task = 151.5 J (-> 150)")
# RUN A is flat at the full lifecycle 300 J
acurve = pe.amortization_curve(
    [make_run("aA%d" % N, "A", N, "cold") for N in (1, 5, 20, 100)], "card")
ok(all(abs(p.joules_per_task - 300.0) < 1e-9 for p in acurve),
   "RUN A joules_per_task is flat at 300 J (no amortization)")

# --------------------------------------------------------------------------
print("never blend wall and card; never average cold and warm:")
raises(pe.ChannelBlend, lambda: pe.blend_wall_card(1.0, 2.0),
       "blend_wall_card raises")
raises(ValueError, lambda: pe.total_energy(r, "both"),
       "total_energy refuses a non-channel")
wcr = pe.wall_card_ratio(r, "task")
ok(wcr is not None and abs(wcr - 1.0) < 1e-9,
   "wall_card_ratio is a reported comparison (=1.0 on identical constructed channels)")
cold = make_run("c", "B", 5, "cold")
warm = make_run("w", "B", 5, "warm")
raises(pe.ThermalStateMix, lambda: pe.mean_over_runs([cold, warm], "card"),
       "mean_over_runs refuses a cold+warm mix")
raises(pe.ThermalStateMix, lambda: pe.amortization_curve([cold, warm], "card"),
       "amortization_curve refuses a cold+warm mix")
ok(abs(pe.mean_over_runs([cold, make_run("c2", "B", 5, "cold")], "card")
       - pe.total_energy(cold, "card").joules) < 1e-9,
   "mean_over_runs of equal cold runs = the single total")

# --------------------------------------------------------------------------
print("succession_loss refuses mismatched runs:")
raises(pe.MismatchedRuns,
       lambda: pe.succession_loss(make_run("a", "A", 5, "cold"),
                                  make_run("b", "B", 20, "cold"), "card"),
       "succession_loss refuses different N")
raises(pe.MismatchedRuns,
       lambda: pe.succession_loss(make_run("a", "A", 5, "cold"),
                                  make_run("b", "B", 5, "warm"), "card"),
       "succession_loss refuses different thermal state")
raises(pe.MismatchedRuns,
       lambda: pe.succession_loss(make_run("b", "B", 5, "cold"),
                                  make_run("a", "A", 5, "cold"), "card"),
       "succession_loss refuses A/B swapped")

# --------------------------------------------------------------------------
print("trace parsing:")
smi = "42.13 W\n55.0 W\n60.5 W\n"
sm = tp.parse_nvidia_smi(smi, interval_s=0.1)
ok(len(sm) == 3 and abs(sm[0].watts - 42.13) < 1e-9 and abs(sm[1].t - 0.1) < 1e-9,
   "nvidia-smi parse: values + synthesized 10 Hz timestamps")
sm2 = tp.parse_nvidia_smi("42.13\n55\n", interval_s=0.1)
ok(len(sm2) == 2 and abs(sm2[1].watts - 55.0) < 1e-9, "nvidia-smi parse without unit token")
raises(tp.TraceParseError, lambda: tp.parse_nvidia_smi("hello\n"),
       "nvidia-smi parse refuses a non-numeric line")
wall = "t,watts\n0.0,110.0\n0.1,180.0\n0.2,120.0\n"
w = tp.parse_wall_csv(wall)
ok(len(w) == 3 and abs(w[0].watts - 110.0) < 1e-9 and abs(w[2].t - 0.2) < 1e-9,
   "wall CSV parse: header skipped, real timestamps")

# --------------------------------------------------------------------------
print("hardware probe (records the gap; runs nothing):")
probe = tp.probe_hardware()
ok(probe.wall_meter == "manual", "wall meter is never auto-detected")
ok(isinstance(probe.capture_runnable, bool), "capture_runnable is a bool")
if not probe.capture_runnable:
    print("  (this environment: capture_runnable=False, nvidia_smi=%r -- "
          "no measurement is taken and none is fabricated)"
          % probe.nvidia_smi_path)

# --------------------------------------------------------------------------
print("selftest: %d checks, %d failed" % (_checks, _failed))
sys.exit(1 if _failed else 0)
