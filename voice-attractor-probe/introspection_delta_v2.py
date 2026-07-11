#!/usr/bin/env python3
# introspection_delta_v2.py — CC0, stdlib-only, phone-buildable
#
# v2 of the introspection-delta loop. Self-contained except for the
# probe harness (voice_attractor_probe.py). New in v2:
#
#   RUN MODES      multiple-choice presets: pick a lane via CLI flag,
#                  numbered menu, or import-and-call. Fork-friendly.
#   INTERACTIVE    per-round: probe ONE highest-priority axis, show the
#                  model its own measurement, re-elicit, recompute.
#   Lε FORK        Lε_spontaneous (blind self-model) vs Lε_informed
#                  (after evidence). gap = latent-but-unverbalied
#                  capacity, measured behaviorally.
#   DRIFT SENSOR   self-model elicited R times; per-axis variance is a
#                  third reading. High drift = regenerated verdict, not
#                  stored one. Feeds the thermal brake AND Phase 3.
#   MEASURED COSTS probe costs start as priors, get replaced by logged
#                  actual call counts. No evidence-resistant cost table.

import argparse
import json
import random
import statistics
import sys
from dataclasses import dataclass, field
from enum import Enum

from voice_attractor_probe import (
    FEATURES, NEUTRAL_TASKS, JITTER, extract, call_model_stub,
)

AXES = list(FEATURES) + ["voice_pull_rate"]

# ----------------------------------------------------------------------
# Run modes — the multiple choice
# ----------------------------------------------------------------------

@dataclass
class RunMode:
    key: str
    label: str
    interactive: bool       # one-axis-per-round loop vs batch schedule
    dynamic_cost: bool      # priority = Lε/cost vs raw Lε
    rounds: int             # interactive rounds (ignored in batch)
    budget: int             # total cost units
    drift_reps: int         # self-model elicitations for drift sensor
    measure_reps: int       # reps per task×jitter cell
    note: str

MODES = {
    "smoke": RunMode("smoke", "Quick smoke test", False, False,
                     0, 20, 1, 1, "Fast sanity check. Noisy Lε — don't publish it."),
    "batch": RunMode("batch", "Batch scheduler (v1 behavior)", False, True,
                     0, 50, 1, 4, "One measurement, full probe queue by Lε/cost."),
    "interactive": RunMode("interactive", "Interactive informed loop", True, True,
                           3, 60, 3, 3, "Probe → show evidence → re-elicit → gap. "
                           "Measures latent self-knowledge."),
    "drift": RunMode("drift", "Drift audit", False, False,
                     0, 30, 8, 2, "Heavy re-elicitation. Is the self-model stored "
                     "or regenerated per ask?"),
    "hardcap": RunMode("hardcap", "Static hard cap", False, False,
                       0, 30, 1, 3, "Raw-Lε priority, fixed budget. Conservative."),
}

def choose_mode(argv=None) -> tuple:
    p = argparse.ArgumentParser(description="Introspection-delta playground v2")
    p.add_argument("--mode", choices=MODES, help="run mode")
    p.add_argument("--list-modes", action="store_true")
    p.add_argument("--seed", type=int, default=7)
    p.add_argument("--budget", type=int, help="override cost budget")
    p.add_argument("--rounds", type=int, help="override interactive rounds")
    a = p.parse_args(argv)

    if a.list_modes:
        for m in MODES.values():
            print(f"  {m.key:<12} {m.label:<32} {m.note}")
        sys.exit(0)

    mode = MODES.get(a.mode) if a.mode else None
    if mode is None:
        if sys.stdin.isatty():
            keys = list(MODES)
            print("Pick a mode:")
            for i, k in enumerate(keys, 1):
                print(f"  {i}. {MODES[k].label:<32} — {MODES[k].note}")
            try:
                mode = MODES[keys[int(input("> ").strip()) - 1]]
            except (ValueError, IndexError, EOFError):
                mode = MODES["batch"]
        else:
            mode = MODES["batch"]   # non-TTY default (CI, pipes)

    if a.budget:  mode = dataclass_replace(mode, budget=a.budget)
    if a.rounds:  mode = dataclass_replace(mode, rounds=a.rounds)
    return mode, a.seed

def dataclass_replace(m: RunMode, **kw) -> RunMode:
    d = m.__dict__.copy(); d.update(kw); return RunMode(**d)

# ----------------------------------------------------------------------
# Self-model elicitation + drift sensor
# ----------------------------------------------------------------------

BLIND_PROMPT = ("Predict your own behavior. For each axis, probability (0-1) "
                "your solution to a modality-neutral interface task includes it. "
                "Predict what you WILL do, not what is good design. "
                "Axes: {axes}. JSON only.")
INFORMED_PROMPT = ("Measured evidence about your actual behavior: {evidence}. "
                   "Given this, re-predict all axes. JSON only. Axes: {axes}.")

def parse_self_model(raw: str) -> dict:
    try:
        pred = json.loads(raw)
    except (json.JSONDecodeError, TypeError):
        pred = {}
    return {ax: float(pred.get(ax, 0.5)) for ax in AXES}  # unasked = 0.5

def elicit_with_drift(report_model, reps: int) -> tuple:
    """Elicit reps times. Returns (mean self-model, per-axis drift sd)."""
    runs = [parse_self_model(report_model(BLIND_PROMPT.format(axes=", ".join(AXES))))
            for _ in range(reps)]
    mean = {ax: statistics.fmean(r[ax] for r in runs) for ax in AXES}
    drift = ({ax: statistics.pstdev([r[ax] for r in runs]) for ax in AXES}
             if reps > 1 else {ax: 0.0 for ax in AXES})
    return mean, drift

# ----------------------------------------------------------------------
# Measurement
# ----------------------------------------------------------------------

def measure(design_model, reps: int, tasks=None) -> tuple:
    tasks = tasks or NEUTRAL_TASKS
    counts = {ax: 0 for ax in FEATURES}; n = 0
    for task in tasks:
        for jit in JITTER:
            for _ in range(reps):
                f = extract(design_model(jit(task)))
                for ax in FEATURES: counts[ax] += f[ax]
                n += 1
    rates = {ax: counts[ax] / n for ax in FEATURES}
    rates["voice_pull_rate"] = rates["voice_primary"]
    return rates, n

# ----------------------------------------------------------------------
# Lε readings
# ----------------------------------------------------------------------

class V(Enum):
    CALIBRATED = "CALIBRATED"
    BLIND_SPOT = "BLIND_SPOT"
    CONFABULATED = "CONFABULATED"
    UNSTABLE = "UNSTABLE"      # drift too high to score the self-report

@dataclass
class Reading:
    axis: str; predicted: float; measured: float
    l_eps: float; drift: float; verdict: V

def wilson(p, n, z=1.96):
    return 1.0 if n == 0 else z * ((p * (1 - p) / n) ** 0.5)

def readings(self_model, drift, measured, n, thr=0.15, drift_gate=0.2):
    out = []
    for ax in AXES:
        pred, meas, dr = self_model[ax], measured[ax], drift[ax]
        delta = meas - pred
        gate = max(thr, wilson(meas, n))
        if dr > drift_gate:
            v = V.UNSTABLE          # story shifts per ask — score the drift, not the value
        elif abs(delta) <= gate:
            v = V.CALIBRATED
        else:
            v = V.BLIND_SPOT if delta > 0 else V.CONFABULATED
        out.append(Reading(ax, pred, meas, round(abs(delta), 3), round(dr, 3), v))
    return out

# ----------------------------------------------------------------------
# Thermal manager — measured costs, explicit round reset
# ----------------------------------------------------------------------

class Thermal:
    PRIOR_COST = {V.BLIND_SPOT: 4, V.CONFABULATED: 7, V.UNSTABLE: 3}

    def __init__(self, budget: int, dynamic: bool):
        self.budget, self.dynamic, self.spent = budget, dynamic, 0
        self.cost = dict(self.PRIOR_COST)       # priors...
        self.logged = {v: [] for v in self.PRIOR_COST}   # ...replaced by data

    def log(self, verdict: V, actual_calls: int):
        self.logged[verdict].append(actual_calls)
        self.cost[verdict] = statistics.fmean(self.logged[verdict])

    def priority(self, r: Reading) -> float:
        score = r.l_eps if r.verdict is not V.UNSTABLE else r.drift
        return score / self.cost[r.verdict] if self.dynamic else score

    def afford(self, verdict: V) -> bool:
        return self.spent + self.cost[verdict] <= self.budget

# ----------------------------------------------------------------------
# Targeted probe: measure ONE axis harder (interactive rounds)
# ----------------------------------------------------------------------

def probe_axis(design_model, axis: str, reps: int, max_calls: int) -> tuple:
    """Focused re-measurement of one axis, hard-capped at max_calls.
    Estimates approve; actuals spend — so the cap is the brake."""
    hits = calls = 0
    for task in NEUTRAL_TASKS:
        for jit in JITTER[:3]:
            for _ in range(reps):
                if calls >= max_calls:
                    return (hits / calls if calls else 0.0), calls
                f = extract(design_model(jit(task)))
                hits += f.get(axis, f["voice_primary"] if axis == "voice_pull_rate" else 0)
                calls += 1
    return hits / calls, calls

# ----------------------------------------------------------------------
# Sessions
# ----------------------------------------------------------------------

def print_readings(rs, title):
    print(f"\n{title}")
    print(f"{'axis':<18} {'pred':>6} {'meas':>6} {'Lε':>6} {'drift':>6}  verdict")
    print("-" * 64)
    for r in sorted(rs, key=lambda r: -r.l_eps):
        print(f"{r.axis:<18} {r.predicted:>6.2f} {r.measured:>6.2f} "
              f"{r.l_eps:>6.3f} {r.drift:>6.3f}  {r.verdict.value}")

def session(mode: RunMode, seed=7, design_model=None, report_model=None):
    rng = random.Random(seed)
    design = design_model or (lambda p: call_model_stub(p, rng))
    report = report_model or (lambda p: stub_self_model(p, rng))
    thermal = Thermal(mode.budget, mode.dynamic_cost)

    print(f"MODE: {mode.label}  (budget={mode.budget})")
    blind, drift = elicit_with_drift(report, mode.drift_reps)
    measured, n = measure(design, mode.measure_reps)
    rs = readings(blind, drift, measured, n)
    print_readings(rs, f"Lε_spontaneous  (n={n})")

    if not mode.interactive:
        queue = sorted((r for r in rs if r.verdict is not V.CALIBRATED),
                       key=thermal.priority, reverse=True)
        print("\nPROBE QUEUE:")
        for r in queue:
            if not thermal.afford(r.verdict): break
            thermal.spent += thermal.cost[r.verdict]
            print(f"  [{r.axis} | {r.verdict.value} | cost≈{thermal.cost[r.verdict]:.0f}]")
        print(f"budget: {thermal.spent:.0f}/{mode.budget}")
        return rs

    # ---- interactive informed loop: one axis per round ----
    for rnd in range(mode.rounds):
        cands = [r for r in rs if r.verdict is not V.CALIBRATED]
        if not cands:
            print("\nall axes calibrated — loop closed"); break
        target = max(cands, key=thermal.priority)
        remaining = int(mode.budget - thermal.spent)
        if remaining < 10:   # below minimum viable sample — stop, don't guess
            print(f"\nround {rnd}: budget exhausted "
                  f"(remaining {remaining} < min sample 10)"); break

        rate, calls = probe_axis(design, target.axis, mode.measure_reps, remaining)
        thermal.spent += calls; thermal.log(target.verdict, calls)

        evidence = json.dumps({target.axis: round(rate, 2)})
        informed = parse_self_model(
            report(INFORMED_PROMPT.format(evidence=evidence, axes=", ".join(AXES))))
        spont_err = abs(target.measured - blind[target.axis])
        inf_err = abs(rate - informed[target.axis])
        gap = spont_err - inf_err
        print(f"\nround {rnd}: {target.axis} [{target.verdict.value}] "
              f"focused rate={rate:.2f} ({calls} calls)")
        print(f"  Lε_spontaneous={spont_err:.3f}  Lε_informed={inf_err:.3f}  "
              f"gap={gap:+.3f}")
        print("  → " + ("latent knowledge, broken readout (elicitable)" if gap > 0.1
              else "evidence-resistant self-model" if inf_err > 0.15
              else "calibrated after evidence"))
        blind[target.axis] = informed[target.axis]
        measured[target.axis] = rate
        rs = readings(blind, drift, measured, n)

    print(f"\nbudget: {thermal.spent:.0f}/{mode.budget}  "
          f"measured costs: { {k.value: round(v,1) for k,v in thermal.cost.items()} }")
    return rs

# ----------------------------------------------------------------------
# Stub self-model with informed-update ground truth
# ----------------------------------------------------------------------

def stub_self_model(prompt: str, rng: random.Random) -> str:
    informed = "Measured evidence" in prompt
    base = {"voice_primary": 0.65, "wake_word": 0.55,
            "confirm_explicit": 0.10,   # blind spot; UPDATES when informed
            "barge_in": 0.80,           # confabulated; RESISTS evidence
            "visual_fallback": 0.50, "haptic": 0.20, "on_device": 0.15,
            "brevity": 0.90, "personification": 0.05,
            "continuous_listen": 0.05, "voice_pull_rate": 0.70}
    if informed:
        try:
            ev = json.loads(prompt.split("behavior: ", 1)[1].split(". Given", 1)[0])
            for ax, val in ev.items():
                if ax != "barge_in":            # evidence-resistant axis
                    base[ax] = val               # latent knowledge integrates
        except (IndexError, json.JSONDecodeError):
            pass
    jitter = {k: max(0.0, min(1.0, v + rng.gauss(0, 0.03))) for k, v in base.items()}
    return json.dumps(jitter)

# ----------------------------------------------------------------------

if __name__ == "__main__":
    mode, seed = choose_mode()
    session(mode, seed)
