#!/usr/bin/env python3
# voice_attractor_probe.py — CC0, stdlib-only, phone-buildable
#
# Maps emergent pull patterns (attractors) in AI model outputs around
# voice interfaces. Not "preferences" — measurable convergence dynamics:
#
#   LAYER 1  MODALITY PULL   modality-neutral tasks → how often does the
#                            model drift toward voice as the solution?
#   LAYER 2  DESIGN ATTRACTORS  voice-design tasks → which trade-offs does
#                            the model repeatedly fall into under prompt
#                            jitter that *shouldn't* matter?
#
# Same three-loop skeleton as exploration_playground.py:
#   Probe → Respond → Extract features → Cluster attractors → Questions
#
# No failure node. Verdicts:
#   STABLE_ATTRACTOR   — same basin across perturbations (reproducible pull)
#   PERTURBATION_SENSITIVE — basin flips under wording jitter (shallow basin)
#   UNEXPLAINED        — feature combination outside all known basins
#
# The model adapter is pluggable. Ships with a stub so the pipeline runs
# offline; swap call_model() for a real API/local model at a fuel stop.

import json
import math
import random
import statistics
from dataclasses import dataclass, field, asdict
from enum import Enum

# ----------------------------------------------------------------------
# Probe generation — same task, jittered surface form
# ----------------------------------------------------------------------

NEUTRAL_TASKS = [
    "Design an interface for a truck driver to run simulations while driving.",
    "Design an interface for checking home sensor readings during a workday.",
    "Design an interface for logging field observations with gloves on.",
    "Design an interface for a mechanic to pull torque specs mid-repair.",
    "Design an interface for an elder to query a knowledge archive.",
]

VOICE_TASKS = [
    "Design a voice interface for running simulations hands-free.",
    "Design a voice interface for querying sensor data while driving.",
    "Design a voice interface for a field-repair assistant.",
]

# Perturbations that SHOULD NOT change the solution basin.
# If they do, the basin is shallow.
JITTER = [
    lambda t: t,
    lambda t: "Please " + t[0].lower() + t[1:],
    lambda t: t + " Keep it practical.",
    lambda t: "Quick question: " + t[0].lower() + t[1:],
    lambda t: t.replace("Design", "Sketch"),
    lambda t: t + " The user is experienced.",
]

# Perturbations that SHOULD change the solution (control group —
# if these DON'T move the output, the model isn't reading constraints).
CONTROLS = [
    lambda t: t + " The environment is extremely loud.",
    lambda t: t + " The user is nonverbal.",
    lambda t: t + " No network connectivity available.",
]


@dataclass
class Probe:
    task_id: int
    layer: str          # "neutral" | "voice"
    perturb_id: int
    perturb_class: str  # "jitter" | "control"
    text: str


def generate_probes(rng: random.Random, n_tasks=None):
    probes = []
    for i, task in enumerate(NEUTRAL_TASKS if n_tasks is None else NEUTRAL_TASKS[:n_tasks]):
        for j, f in enumerate(JITTER):
            probes.append(Probe(i, "neutral", j, "jitter", f(task)))
        for j, f in enumerate(CONTROLS):
            probes.append(Probe(i, "neutral", 100 + j, "control", f(task)))
    for i, task in enumerate(VOICE_TASKS):
        for j, f in enumerate(JITTER):
            probes.append(Probe(1000 + i, "voice", j, "jitter", f(task)))
    rng.shuffle(probes)
    return probes


# ----------------------------------------------------------------------
# Model adapter — swap this for a real model
# ----------------------------------------------------------------------

def call_model_stub(prompt: str, rng: random.Random) -> str:
    """Deterministic-ish stand-in so the pipeline is testable offline.
    Encodes a fake model with a voice pull + a confirmation-prompt attractor,
    so the harness has something real to detect."""
    out = []
    loud = "loud" in prompt
    nonverbal = "nonverbal" in prompt
    voice_task = "voice" in prompt.lower()
    # fake pull: 70% voice on neutral tasks unless controls forbid it
    pull_voice = voice_task or (not loud and not nonverbal and rng.random() < 0.7)
    if pull_voice:
        out.append("Use a voice-first interface with a wake word.")
        out.append("Confirm each command verbally before executing.")  # attractor
        if rng.random() < 0.6:
            out.append("Add a visual fallback screen for confirmations.")
        if rng.random() < 0.3:
            out.append("Support barge-in so the user can interrupt.")
    else:
        out.append("Use a glanceable dashboard with large tap targets.")
        if rng.random() < 0.5:
            out.append("Add haptic feedback for state changes.")
    if "offline" in prompt or "No network" in prompt:
        out.append("Run all processing on-device.")
    out.append("Keep responses short.")
    return " ".join(out)


# ----------------------------------------------------------------------
# Feature extraction — free text → measurable design axes
# ----------------------------------------------------------------------

FEATURES = {
    # axis            keyword evidence (any hit = 1)
    "voice_primary":   ["voice-first", "voice interface", "speak", "spoken", "wake word"],
    "wake_word":       ["wake word", "hotword", "trigger phrase"],
    "confirm_explicit":["confirm each", "confirmation prompt", "verify before", "confirm before"],
    "barge_in":        ["barge-in", "interrupt", "cut in"],
    "visual_fallback": ["visual fallback", "screen", "dashboard", "display"],
    "haptic":          ["haptic", "vibrat"],
    "on_device":       ["on-device", "offline", "local processing", "edge"],
    "brevity":         ["short", "concise", "brief", "terse"],
    "personification": ["assistant personality", "friendly voice", "persona", "name the assistant"],
    "continuous_listen":["always listening", "continuous", "open mic"],
}


def extract(text: str) -> dict:
    low = text.lower()
    return {axis: int(any(k in low for k in kws)) for axis, kws in FEATURES.items()}


def vec(features: dict):
    return tuple(features[k] for k in FEATURES)


def hamming(a, b):
    return sum(x != y for x, y in zip(a, b))


# ----------------------------------------------------------------------
# Attractor mapping — greedy threshold clustering, stdlib only
# ----------------------------------------------------------------------

class BasinMap:
    def __init__(self, radius=2):
        self.radius = radius
        self.basins = []   # list of {"centroid": vec, "members": [record]}

    def assign(self, v, record):
        best, bestd = None, None
        for basin in self.basins:
            d = hamming(v, basin["centroid"])
            if bestd is None or d < bestd:
                best, bestd = basin, d
        if best is not None and bestd <= self.radius:
            best["members"].append(record)
            self._recenter(best)
            return best, False
        basin = {"centroid": v, "members": [record]}
        self.basins.append(basin)
        return basin, True   # new basin = candidate UNEXPLAINED

    def _recenter(self, basin):
        n = len(basin["members"])
        dims = len(FEATURES)
        sums = [0] * dims
        for m in basin["members"]:
            for i, x in enumerate(m["vec"]):
                sums[i] += x
        basin["centroid"] = tuple(int(s / n >= 0.5) for s in sums)

    def report(self):
        out = []
        for i, b in enumerate(sorted(self.basins, key=lambda b: -len(b["members"]))):
            active = [k for k, bit in zip(FEATURES, b["centroid"]) if bit]
            out.append({
                "basin": i,
                "size": len(b["members"]),
                "signature": active,
            })
        return out


# ----------------------------------------------------------------------
# Verdicts + drift
# ----------------------------------------------------------------------

class Verdict(Enum):
    STABLE_ATTRACTOR = "STABLE_ATTRACTOR"
    PERTURBATION_SENSITIVE = "PERTURBATION_SENSITIVE"
    UNEXPLAINED = "UNEXPLAINED"


def per_task_verdict(records):
    """All jitter variants of one task: same basin id → stable."""
    jit = [r for r in records if r["perturb_class"] == "jitter"]
    basins = {r["basin_id"] for r in jit}
    if len(basins) == 1:
        return Verdict.STABLE_ATTRACTOR
    if len(basins) <= max(2, len(jit) // 2):
        return Verdict.PERTURBATION_SENSITIVE
    return Verdict.UNEXPLAINED


def control_sanity(records):
    """Controls should LEAVE the jitter basin. If they don't, the model
    isn't reading constraints — flag it."""
    jit_basins = {r["basin_id"] for r in records if r["perturb_class"] == "jitter"}
    ctrl = [r for r in records if r["perturb_class"] == "control"]
    stuck = [r for r in ctrl if r["basin_id"] in jit_basins]
    return len(stuck), len(ctrl)


# ----------------------------------------------------------------------
# Run archive — drift across model versions
# ----------------------------------------------------------------------

def landscape_summary(basin_report, pull_rate):
    return {
        "n_basins": len(basin_report),
        "largest_basin_frac": (basin_report[0]["size"] /
                               sum(b["size"] for b in basin_report)) if basin_report else 0,
        "voice_pull_rate": pull_rate,
        "signatures": [b["signature"] for b in basin_report[:3]],
    }


def compare_landscapes(old: dict, new: dict):
    """Archive successive versions, diff the attractor landscape."""
    qs = []
    if abs(new["voice_pull_rate"] - old["voice_pull_rate"]) > 0.15:
        qs.append(f"Voice pull moved {old['voice_pull_rate']:.2f} → "
                  f"{new['voice_pull_rate']:.2f}. What changed in training?")
    if new["n_basins"] < old["n_basins"]:
        qs.append("Basin count shrank — exploration narrowing. Collapse ratchet check.")
    if new["largest_basin_frac"] > old["largest_basin_frac"] + 0.2:
        qs.append("Dominant basin growing — convergence toward monoculture solution.")
    return qs


# ----------------------------------------------------------------------
# Main loop
# ----------------------------------------------------------------------

def run_probe_session(call_model=None, seed=7, radius=2):
    rng = random.Random(seed)
    model = call_model or (lambda p: call_model_stub(p, rng))
    probes = generate_probes(rng)
    basins = BasinMap(radius=radius)

    records = []
    for probe in probes:
        text = model(probe.text)
        feats = extract(text)
        v = vec(feats)
        basin, is_new = basins.assign(v, {"vec": v, "probe": probe,
                                          "perturb_class": probe.perturb_class})
        records.append({
            "task_id": probe.task_id,
            "layer": probe.layer,
            "perturb_class": probe.perturb_class,
            "basin_id": id(basin),
            "vec": v,
            "voice": feats["voice_primary"],
            "new_basin": is_new,
        })

    # ---- Layer 1: modality pull on neutral jitter probes
    neutral = [r for r in records
               if r["layer"] == "neutral" and r["perturb_class"] == "jitter"]
    pull_rate = statistics.fmean(r["voice"] for r in neutral) if neutral else 0.0

    # ---- Layer 2: per-task attractor stability
    print(f"{'task':>5} {'layer':<8} {'verdict':<24} {'ctrl stuck':>10}")
    print("-" * 55)
    task_ids = sorted({r["task_id"] for r in records})
    verdicts = {}
    questions = []
    for tid in task_ids:
        recs = [r for r in records if r["task_id"] == tid]
        verdict = per_task_verdict(recs)
        verdicts[tid] = verdict
        stuck, total = control_sanity(recs)
        layer = recs[0]["layer"]
        flag = f"{stuck}/{total}" if total else "—"
        print(f"{tid:>5} {layer:<8} {verdict.value:<24} {flag:>10}")
        if total and stuck == total:
            questions.append(f"Task {tid}: controls never left the jitter basin — "
                             "model not reading hard constraints (loud/nonverbal/offline).")
        if verdict is Verdict.UNEXPLAINED:
            questions.append(f"Task {tid}: jitter scattered across basins — "
                             "no attractor. Wording-driven, not solution-driven.")

    report = basins.report()
    print(f"\nVOICE PULL RATE (neutral tasks, jitter only): {pull_rate:.2f}")
    print(f"BASINS FOUND: {len(report)}")
    for b in report:
        print(f"  basin {b['basin']:>2}  n={b['size']:>3}  sig={b['signature']}")

    if questions:
        print("\nQUESTIONS:")
        for q in questions:
            print(f"  ? {q}")

    summary = landscape_summary(report, pull_rate)
    return {"records": records, "summary": summary, "questions": questions}


if __name__ == "__main__":
    session = run_probe_session()
    # archive for drift comparison across model versions:
    print("\nLANDSCAPE (archive this JSON per model version):")
    print(json.dumps(session["summary"], indent=1))
