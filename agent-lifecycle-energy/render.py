# SPDX-License-Identifier: CC0-1.0
"""
Render a rig report from LifecycleRun records: the raw per-run records
alongside the derived figures, so the derived numbers can be recomputed from
the raw ones without trusting this pipeline (the work order asks for exactly
that). Wall and card are printed in separate columns and never blended; cold
and warm are printed as separate blocks and never averaged.

EVERYTHING HERE IS CONSTRUCTED. The traces are built by hand to exercise the
report; no row is a measurement of any machine, model, or task. The header
says so, and the hardware probe result is printed so the reader can see the
rig has not run.

The emitted text is screened through sheet-structure-scan/no_severity (the
report states structure, not a grade). Run:

    python3 agent-lifecycle-energy/render.py            # print
    python3 agent-lifecycle-energy/render.py --write    # write samples/
"""

from __future__ import annotations

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, "sheet-structure-scan"))

import phase_energy as pe          # noqa: E402
import trace_parse as tp           # noqa: E402
import no_severity                 # noqa: E402

S = pe.Sample


def const_trace(watts, dur, hz=200.0):
    n = int(round(dur * hz)) + 1
    step = dur / (n - 1)
    return [S(i * step, watts) for i in range(n)]


def build(run_id, condition, N, cold_or_warm):
    # Constructed marginals. CARD is the accelerator draw; WALL is higher --
    # it carries PSU losses, fans, RAM, storage -- so wall > card and the
    # ratio is above 1. A cold start pays a larger spin-up than a warm one.
    idle = {"card": const_trace(60.0, 0.5), "wall": const_trace(140.0, 0.5)}
    spin_card = 260.0 if cold_or_warm == "cold" else 180.0
    spin_wall = 380.0 if cold_or_warm == "cold" else 280.0
    phases = {
        "card": {"spinup": const_trace(spin_card, 0.5),
                 "task": const_trace(210.0, 1.0),
                 "teardown": const_trace(120.0, 0.4)},
        "wall": {"spinup": const_trace(spin_wall, 0.5),
                 "task": const_trace(320.0, 1.0),
                 "teardown": const_trace(210.0, 0.4)},
    }
    return pe.run_from_traces(run_id, condition, N, "toy-summarize",
                              "constructed-model", cold_or_warm, 22.0,
                              idle, phases)


def _j(x):
    return "--" if x is None else "%.1f" % x


def _phase_row(run, channel):
    s = run.phase("spinup", channel)
    t = run.phase("task", channel)
    d = run.phase("teardown", channel)
    return "%s / %s / %s" % (_j(s.joules), _j(t.joules), _j(d.joules))


def render():
    L = []
    L.append("GAP 4 RIG REPORT -- CONSTRUCTED TRACES, NOT A MEASUREMENT")
    L.append("=" * 62)
    probe = tp.probe_hardware()
    L.append("hardware probe: nvidia-smi=%r  card telemetry=%s  "
             "wall meter=%s  capture runnable=%s"
             % (probe.nvidia_smi_path, probe.has_gpu_telemetry,
                probe.wall_meter, probe.capture_runnable))
    L.append("baseline method: %s   integration: %s   floor: %.0f Hz"
             % (pe.BASELINE_METHOD, pe.INTEGRATION, pe.MIN_HZ))
    L.append("every joule below is built by hand to exercise the report; "
             "no row is a reading of any real machine, model, or task.")
    L.append("")

    for cw in ("cold", "warm"):
        L.append("---- %s start (cold and warm are never averaged together) ----"
                 % cw.upper())
        L.append("raw per-run records (marginal J, spinup / task / teardown, "
                 "per representative task):")
        L.append("  %-4s %-4s %-3s | %-22s | %-22s | %s"
                 % ("run", "cond", "N", "card (spin/task/tear)",
                    "wall (spin/task/tear)", "wall:card task ratio"))
        for N in (1, 5, 20, 100):
            for cond in ("A", "B"):
                r = build("%s%s%d" % (cw[0], cond, N), cond, N, cw)
                ratio = pe.wall_card_ratio(r, "task")
                L.append("  %-4s %-4s %-3d | %-22s | %-22s | %.2f"
                         % (r.run_id, cond, N, _phase_row(r, "card"),
                            _phase_row(r, "wall"),
                            ratio if ratio is not None else float("nan")))
        L.append("")
        L.append("derived (card channel, then wall channel, separately):")
        for channel in ("card", "wall"):
            aset = [build("%sA%d" % (cw[0], N), "A", N, cw)
                    for N in (1, 5, 20, 100)]
            bset = [build("%sB%d" % (cw[0], N), "B", N, cw)
                    for N in (1, 5, 20, 100)]
            sf = pe.setup_fraction(aset[0], channel)
            L.append("  [%s] setup_fraction (per lifecycle): %s"
                     % (channel, "--" if sf.value is None
                        else "%.3f" % sf.value))
            acurve = pe.amortization_curve(aset, channel)
            bcurve = pe.amortization_curve(bset, channel)
            L.append("  [%s] amortization_curve  joules_per_task vs N:"
                     % channel)
            L.append("        N:            %s"
                     % "  ".join("%7d" % p.N for p in bcurve))
            L.append("        RUN A (1-task):%s"
                     % "  ".join("%7.1f" % p.joules_per_task for p in acurve))
            L.append("        RUN B (N-task):%s"
                     % "  ".join("%7.1f" % p.joules_per_task for p in bcurve))
            L.append("  [%s] succession_loss  (total A - total B), same N:"
                     % channel)
            parts = []
            for N in (1, 5, 20, 100):
                a = build("%sA%d" % (cw[0], N), "A", N, cw)
                b = build("%sB%d" % (cw[0], N), "B", N, cw)
                sl = pe.succession_loss(a, b, channel)
                parts.append("N=%d: %s J" % (N, _j(sl.joules)))
            L.append("        " + "   ".join(parts))
        L.append("")
    L.append("succession_loss is the headline: the joule cost of "
             "disposability, work delivered held constant. It grows as "
             "(N-1) x (spin-up + teardown).")
    L.append("amortization_curve for RUN B falls with N toward the per-task "
             "floor; RUN A stays flat -- it pays a full lifecycle every task.")
    return "\n".join(L)


def main(argv):
    text = render()
    clean, h = no_severity.check(text)
    if not clean:
        sys.stderr.write("no_severity screen FAILED on the render:\n")
        for lineno, word, line in h:
            sys.stderr.write("  line %d: %r in %r\n" % (lineno, word, line))
        return 1
    if "--write" in argv:
        out = os.path.join(HERE, "samples", "ale_report.sample.txt")
        with open(out, "w") as fh:
            fh.write(text + "\n")
        sys.stderr.write("wrote %s (no_severity: clean)\n" % out)
    else:
        print(text)
        sys.stderr.write("\n(no_severity: clean)\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
