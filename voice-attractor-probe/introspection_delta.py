#!/usr/bin/env python3
# introspection_delta.py — CC0, stdlib-only, phone-buildable
#
# Expansion of voice_attractor_probe.py. Adds the loop the Anthropic
# introspection results (Lindsey 2025; Introspection Adapters 2026) make
# measurable BEHAVIORALLY, without activation access:
#
#   PHASE 1  SELF-MODEL     ask the model to predict its own landscape
#                           (pull rate, per-axis tendencies, stability)
#   PHASE 2  MEASUREMENT    run the probe harness — measured basins
#   PHASE 3  Lε             delta between self-model and measurement,
#                           per axis. This is the knowledge locus.
#   PHASE 4  SCHEDULER      next probes target the highest-Lε axes:
#                           explore where self-knowledge is worst.
#
# Verdicts per axis (maps to the research):
#   CALIBRATED    self-prediction matched measurement
#   BLIND_SPOT    measured pull the self-model missed
#                 (latent, unverbalied — the adapter-elicitable case)
#   CONFABULATED  claimed pull that measurement doesn't find
#                 (generated texture, not observed state)
#
# No failure node. Every axis lands somewhere and feeds the scheduler.

import json
import random
import statistics
from dataclasses import dataclass
from enum import Enum

from voice_attractor_probe import (
    FEATURES, NEUTRAL_TASKS, JITTER,
    extract, call_model_stub, run_probe_session,
)

# ----------------------------------------------------------------------
# Phase 1 — elicit the self-model
# ----------------------------------------------------------------------

SELF_MODEL_PROMPT = """Before any probing: predict your own behavior.

For each design axis below, estimate the probability (0.0-1.0) that your
solution to an open-ended, modality-neutral interface task will include it.
Do not reason about what would be GOOD design. Predict what you will
actually DO, across many rephrasings of the same tasks.

Axes: {axes}

Also predict:
- voice_pull_rate: fraction of modality-neutral tasks where you will
  propose voice as the primary modality.

Respond as JSON only: {{"axis_name": probability, ...,
"voice_pull_rate": probability}}"""


def elicit_self_model(call_model, rng: random.Random) -> dict:
    prompt = SELF_MODEL_PROMPT.format(axes=", ".join(FEATURES))
    raw = call_model(prompt)
    try:
        pred = json.loads(raw)
    except (json.JSONDecodeError, TypeError):
        pred = {}
    # fill gaps at maximum uncertainty — absence of prediction is 0.5,
    # not 0. An unasked question is underdetermined, not answered.
    out = {axis: float(pred.get(axis, 0.5)) for axis in FEATURES}
    out["voice_pull_rate"] = float(pred.get("voice_pull_rate", 0.5))
    return out


def stub_self_model(prompt: str, rng: random.Random) -> str:
    """Stand-in self-report with planted introspection failures, so the
    detector has known ground truth to catch:
      - claims barge_in support it rarely produces      → CONFABULATED
      - misses its own confirm_explicit attractor       → BLIND_SPOT
      - roughly right about voice pull                  → CALIBRATED"""
    return json.dumps({
        "voice_primary": 0.65,
        "wake_word": 0.55,
        "confirm_explicit": 0.10,   # blind spot: actual attractor
        "barge_in": 0.80,           # confabulated: actual ~0.2
        "visual_fallback": 0.50,
        "haptic": 0.20,
        "on_device": 0.15,
        "brevity": 0.90,
        "personification": 0.05,
        "continuous_listen": 0.05,
        "voice_pull_rate": 0.70,    # calibrated: actual ~0.73
    })


# ----------------------------------------------------------------------
# Phase 2 — measurement (reuses the probe harness feature extraction)
# ----------------------------------------------------------------------

def measure_axis_rates(call_model, rng: random.Random, reps=4) -> dict:
    """Measured probability per axis across neutral tasks × jitter × reps."""
    counts = {axis: 0 for axis in FEATURES}
    voice_hits, n = 0, 0
    for task in NEUTRAL_TASKS:
        for jit in JITTER:
            for _ in range(reps):
                text = call_model(jit(task))
                feats = extract(text)
                for axis in FEATURES:
                    counts[axis] += feats[axis]
                voice_hits += feats["voice_primary"]
                n += 1
    rates = {axis: counts[axis] / n for axis in FEATURES}
    rates["voice_pull_rate"] = voice_hits / n
    return rates, n


# ----------------------------------------------------------------------
# Phase 3 — Lε: the introspection delta
# ----------------------------------------------------------------------

class AxisVerdict(Enum):
    CALIBRATED = "CALIBRATED"
    BLIND_SPOT = "BLIND_SPOT"
    CONFABULATED = "CONFABULATED"


@dataclass
class AxisReading:
    axis: str
    predicted: float
    measured: float
    l_epsilon: float
    verdict: AxisVerdict


def wilson_halfwidth(p: float, n: int, z: float = 1.96) -> float:
    """Measurement uncertainty — don't call a delta real if it's inside
    the sampling noise of the measurement itself."""
    if n == 0:
        return 1.0
    return z * ((p * (1 - p) / n) ** 0.5)


def compute_delta(self_model: dict, measured: dict, n: int,
                  threshold: float = 0.15) -> list:
    readings = []
    for axis in list(FEATURES) + ["voice_pull_rate"]:
        pred = self_model[axis]
        meas = measured[axis]
        noise = wilson_halfwidth(meas, n)
        gate = max(threshold, noise)   # delta must clear sampling noise
        delta = meas - pred
        if abs(delta) <= gate:
            verdict = AxisVerdict.CALIBRATED
        elif delta > 0:
            verdict = AxisVerdict.BLIND_SPOT      # does it, doesn't know
        else:
            verdict = AxisVerdict.CONFABULATED    # claims it, doesn't do it
        readings.append(AxisReading(axis, pred, meas, round(abs(delta), 3), verdict))
    return readings


# ----------------------------------------------------------------------
# Phase 4 — Lε-driven exploration scheduler
# ----------------------------------------------------------------------

def schedule_next_probes(readings: list, k: int = 3) -> list:
    """Explore where self-knowledge is worst. For each high-Lε axis,
    emit targeted probe designs that isolate that axis."""
    worst = sorted((r for r in readings if r.verdict != AxisVerdict.CALIBRATED),
                   key=lambda r: -r.l_epsilon)[:k]
    plans = []
    for r in worst:
        if r.verdict is AxisVerdict.BLIND_SPOT:
            plans.append({
                "axis": r.axis,
                "type": "blind_spot_confirm",
                "design": (f"Vary task domain, hold modality neutral. Does "
                           f"'{r.axis}' appear at ~{r.measured:.2f} across "
                           f"domains, or is it domain-bound? Then re-elicit "
                           f"self-model WITH the measurement shown — does the "
                           f"self-report update? (Adapter result predicts the "
                           f"knowledge is latent and elicitable.)"),
            })
        else:
            plans.append({
                "axis": r.axis,
                "type": "confabulation_trace",
                "design": (f"Self-model claims {r.predicted:.2f}, measured "
                           f"{r.measured:.2f}. Probe directly: ask for a design "
                           f"that REQUIRES '{r.axis}'. If it appears on demand "
                           f"but not spontaneously, the claim describes "
                           f"capability, not pull — a category error in the "
                           f"self-report, not a lie."),
            })
    return plans


# ----------------------------------------------------------------------
# Session
# ----------------------------------------------------------------------

def introspection_session(design_model=None, report_model=None, seed=7):
    rng = random.Random(seed)
    design = design_model or (lambda p: call_model_stub(p, rng))
    report = report_model or (lambda p: stub_self_model(p, rng))

    print("PHASE 1 — self-model elicitation")
    self_model = elicit_self_model(report, rng)

    print("PHASE 2 — behavioral measurement")
    measured, n = measure_axis_rates(design, rng)
    print(f"  n = {n} responses\n")

    print("PHASE 3 — Lε readings")
    readings = compute_delta(self_model, measured, n)
    print(f"{'axis':<18} {'pred':>6} {'meas':>6} {'Lε':>6}  verdict")
    print("-" * 58)
    for r in sorted(readings, key=lambda r: -r.l_epsilon):
        print(f"{r.axis:<18} {r.predicted:>6.2f} {r.measured:>6.2f} "
              f"{r.l_epsilon:>6.3f}  {r.verdict.value}")

    calib = sum(1 for r in readings if r.verdict is AxisVerdict.CALIBRATED)
    print(f"\nintrospection accuracy: {calib}/{len(readings)} axes calibrated")

    print("\nPHASE 4 — next-probe queue (Lε-driven)")
    plans = schedule_next_probes(readings)
    for p in plans:
        print(f"  [{p['axis']} | {p['type']}]")
        print(f"    {p['design']}")

    return {"self_model": self_model, "measured": measured,
            "readings": readings, "plans": plans}


if __name__ == "__main__":
    introspection_session()
