#!/usr/bin/env python3
# exploration_playground.py — CC0, stdlib-only, phone-buildable
#
# Three-loop scientific discovery engine over a region/interface substrate.
# No failure node. Every run lands in one of three verdicts:
#   SUPPORTED     — observation matched the hypothesis prediction
#   CONTRADICTED  — observation opposed the prediction (model update, not failure)
#   UNEXPLAINED   — behavior the current model doesn't cover (most valuable)
#
# Score = interestingness, not correctness:
#   reproducible × surprising × question-generating
#
# Loop:  Hypothesis → Simulate → Observe → Novelty → Questions → next experiment

import math
import random
import statistics
from dataclasses import dataclass, field, replace
from enum import Enum

# ----------------------------------------------------------------------
# Substrate
# ----------------------------------------------------------------------

@dataclass
class Region:
    name: str
    # material
    carrier_density: float      # mobile carriers
    mobility: float             # response to field
    permittivity: float         # field screening
    # dynamics
    trap_density: float         # capacity of traps
    trapped: float              # currently trapped carriers
    recombination_rate: float   # loss term
    # exploration
    adaptation_rate: float      # how fast mobility drifts under stress
    noise_strength: float       # thermal noise floor

    def snapshot(self):
        return {
            "region": self.name,
            "density": self.carrier_density,
            "mobility": self.mobility,
            "trapped": self.trapped,
        }


class Interface:
    """Carriers exchange across the junction; traps capture and release."""

    def __init__(self, a: Region, b: Region, conductance: float = 0.05):
        self.a, self.b = a, b
        self.conductance = conductance

    def exchange(self, dt: float, rng: random.Random):
        # gradient-driven flow (diffusive), mobility-weighted
        grad = self.a.carrier_density - self.b.carrier_density
        mob = 0.5 * (self.a.mobility + self.b.mobility)
        flow = self.conductance * mob * grad * dt
        self.a.carrier_density -= flow
        self.b.carrier_density += flow

        # trap dynamics at the junction — nonlinearity lives here
        for r in (self.a, self.b):
            free_traps = max(r.trap_density - r.trapped, 0.0)
            capture = 0.02 * r.carrier_density * free_traps * dt
            release = 0.01 * r.trapped * dt * (1.0 + abs(grad))  # field-assisted release
            delta = capture - release
            delta = max(-r.trapped, min(delta, r.carrier_density))
            r.trapped += delta
            r.carrier_density -= delta
        return flow


class Environment:
    """External drive. The imposed gradient — the extrinsic asymmetry."""

    def __init__(self, mode: str = "sine", amplitude: float = 1.0, period: float = 40.0):
        self.mode, self.amplitude, self.period = mode, amplitude, period

    def fieldstrength(self, t: float) -> float:
        if self.mode == "constant":
            return self.amplitude
        if self.mode == "sine":
            return self.amplitude * math.sin(2 * math.pi * t / self.period)
        if self.mode == "kick":
            # stroboscopic kick: sharp pulse once per period
            return self.amplitude if (t % self.period) < 1.0 else 0.0
        return 0.0


# ----------------------------------------------------------------------
# Engine
# ----------------------------------------------------------------------

@dataclass
class Config:
    steps: int = 400
    dt: float = 1.0
    seed: int = 0
    env_mode: str = "sine"
    env_amplitude: float = 1.0
    env_period: float = 40.0
    # region parameter overrides applied at build time
    overrides: dict = field(default_factory=dict)   # {"a.mobility": 1.3, ...}


def build_system(cfg: Config):
    a = Region("a", carrier_density=10.0, mobility=1.0, permittivity=1.0,
               trap_density=4.0, trapped=0.0, recombination_rate=0.005,
               adaptation_rate=0.01, noise_strength=0.05)
    b = Region("b", carrier_density=2.0, mobility=0.6, permittivity=2.0,
               trap_density=8.0, trapped=0.0, recombination_rate=0.002,
               adaptation_rate=0.02, noise_strength=0.05)
    regions = {"a": a, "b": b}
    for key, val in cfg.overrides.items():
        rname, pname = key.split(".")
        setattr(regions[rname], pname, val)
    iface = Interface(a, b)
    env = Environment(cfg.env_mode, cfg.env_amplitude, cfg.env_period)
    return regions, iface, env


def run(cfg: Config):
    rng = random.Random(cfg.seed)
    regions, iface, env = build_system(cfg)
    a, b = regions["a"], regions["b"]
    history = []
    t = 0.0
    for _ in range(cfg.steps):
        f = env.fieldstrength(t)

        # field update → carrier motion (drift injection into region a)
        drift = f * a.mobility / a.permittivity * cfg.dt
        a.carrier_density = max(a.carrier_density + drift, 0.0)

        # interface dynamics
        flow = iface.exchange(cfg.dt, rng)

        # recombination
        for r in (a, b):
            r.carrier_density *= (1.0 - r.recombination_rate * cfg.dt)

        # adaptation: mobility drifts under local stress + noise
        for r in (a, b):
            stress = abs(flow) + abs(f) * 0.1
            r.mobility += r.adaptation_rate * stress * cfg.dt * rng.gauss(0.5, 1.0)
            r.mobility += r.noise_strength * rng.gauss(0.0, 0.02)
            r.mobility = max(r.mobility, 0.01)

        history.append({
            "t": t, "field": f, "flow": flow,
            "a_density": a.carrier_density, "b_density": b.carrier_density,
            "a_mob": a.mobility, "b_mob": b.mobility,
            "a_trapped": a.trapped, "b_trapped": b.trapped,
        })
        t += cfg.dt
    return history


# ----------------------------------------------------------------------
# Observation engine
# ----------------------------------------------------------------------

class Observer:
    """Asks: what emerged? is it stable? did the system change phase?"""

    OBSERVABLES = ("a_density", "b_density", "a_mob", "b_mob", "a_trapped", "b_trapped")

    def __init__(self, history):
        self.h = history

    def tail(self, key, frac=0.25):
        n = max(int(len(self.h) * frac), 8)
        return [row[key] for row in self.h[-n:]]

    def summary(self):
        out = {}
        for key in self.OBSERVABLES:
            tail = self.tail(key)
            out[key] = {
                "mean": statistics.fmean(tail),
                "sd": statistics.pstdev(tail),
            }
        return out

    def stability(self, key):
        """Attractor check: does tail variance shrink relative to mid-run?"""
        n = len(self.h)
        mid = [r[key] for r in self.h[n // 4: n // 2]]
        tail = self.tail(key)
        mv, tv = statistics.pstdev(mid), statistics.pstdev(tail)
        if mv < 1e-12:
            return "flat"
        ratio = tv / mv
        if ratio < 0.5:
            return "attractor"
        if ratio > 2.0:
            return "diverging"
        return "wandering"

    def transitions(self, key, z=4.0):
        """Phase-change detector: derivative jumps beyond z sigma."""
        vals = [r[key] for r in self.h]
        diffs = [vals[i + 1] - vals[i] for i in range(len(vals) - 1)]
        if len(diffs) < 10:
            return []
        sd = statistics.pstdev(diffs) or 1e-12
        mu = statistics.fmean(diffs)
        return [i for i, d in enumerate(diffs) if abs(d - mu) > z * sd]


# ----------------------------------------------------------------------
# Hypothesis loop
# ----------------------------------------------------------------------

class Verdict(Enum):
    SUPPORTED = "SUPPORTED"
    CONTRADICTED = "CONTRADICTED"
    UNEXPLAINED = "UNEXPLAINED"


@dataclass
class Hypothesis:
    param: str          # e.g. "a.mobility"
    delta: float        # multiplicative perturbation, e.g. +0.4 → ×1.4
    observable: str     # which output it predicts
    direction: int      # +1 predicts increase, -1 predicts decrease
    note: str = ""


PARAM_SPACE = [
    "a.mobility", "b.mobility",
    "a.trap_density", "b.trap_density",
    "a.adaptation_rate", "b.adaptation_rate",
    "a.recombination_rate", "b.recombination_rate",
    "a.noise_strength", "b.noise_strength",
]

# naive prior: which direction does raising a param push each observable?
# The engine's job is to break this prior. UNEXPLAINED = prior has no entry.
PRIOR = {
    ("a.mobility", "a_density"): +1,
    ("a.mobility", "b_density"): +1,
    ("b.mobility", "b_density"): +1,
    ("a.trap_density", "a_trapped"): +1,
    ("b.trap_density", "b_trapped"): +1,
    ("a.recombination_rate", "a_density"): -1,
    ("b.recombination_rate", "b_density"): -1,
    ("a.adaptation_rate", "a_mob"): +1,
    ("b.adaptation_rate", "b_mob"): +1,
}


class HypothesisGenerator:
    def __init__(self, rng: random.Random):
        self.rng = rng

    def propose(self) -> Hypothesis:
        param = self.rng.choice(PARAM_SPACE)
        delta = self.rng.choice([-0.5, -0.25, 0.25, 0.5, 1.0])
        # pick an observable — sometimes one the prior covers, sometimes not
        observable = self.rng.choice(Observer.OBSERVABLES)
        direction = PRIOR.get((param, observable), 0) * (1 if delta > 0 else -1)
        return Hypothesis(param, delta, observable, direction,
                          note="prior" if direction else "no-prior")


# ----------------------------------------------------------------------
# Novelty + interestingness
# ----------------------------------------------------------------------

def perturbed_config(base: Config, hyp: Hypothesis, seed: int) -> Config:
    regions, _, _ = build_system(base)
    rname, pname = hyp.param.split(".")
    current = getattr(regions[rname], pname)
    new_overrides = dict(base.overrides)
    new_overrides[hyp.param] = current * (1.0 + hyp.delta)
    return replace(base, overrides=new_overrides, seed=seed)


def compare(base_summary, test_summary, observable):
    b = base_summary[observable]
    t = test_summary[observable]
    sd = b["sd"] or 1e-9
    zscore = (t["mean"] - b["mean"]) / sd
    return zscore


def judge(hyp: Hypothesis, zscore: float, threshold: float = 1.5) -> Verdict:
    if abs(zscore) < threshold:
        # no meaningful effect
        if hyp.direction == 0:
            return Verdict.SUPPORTED      # prior said nothing; nothing happened
        return Verdict.CONTRADICTED       # prior predicted an effect; none appeared
    observed_dir = 1 if zscore > 0 else -1
    if hyp.direction == 0:
        return Verdict.UNEXPLAINED        # effect where the model had no opinion
    return Verdict.SUPPORTED if observed_dir == hyp.direction else Verdict.CONTRADICTED


def reproducibility(base: Config, hyp: Hypothesis, base_summary, n=3, threshold=1.5):
    """Rerun with different noise seeds — does the effect hold sign?"""
    signs = []
    for s in range(101, 101 + n):
        cfg = perturbed_config(base, hyp, seed=s)
        summ = Observer(run(cfg)).summary()
        z = compare(base_summary, summ, hyp.observable)
        signs.append(0 if abs(z) < threshold else (1 if z > 0 else -1))
    nonzero = [s for s in signs if s]
    if not nonzero:
        return 0.0
    agreement = abs(sum(nonzero)) / len(signs)
    return agreement


def interestingness(verdict: Verdict, zscore: float, repro: float, n_questions: int):
    surprise = min(abs(zscore) / 3.0, 3.0)
    verdict_weight = {"SUPPORTED": 0.3, "CONTRADICTED": 1.0, "UNEXPLAINED": 2.0}[verdict.value]
    richness = 1.0 + 0.5 * n_questions
    return round(repro * surprise * verdict_weight * richness, 3)


# ----------------------------------------------------------------------
# Question generator
# ----------------------------------------------------------------------

def generate_questions(hyp: Hypothesis, verdict: Verdict, obs: Observer):
    qs = []
    if verdict is Verdict.UNEXPLAINED:
        qs.append(f"Why does {hyp.param} move {hyp.observable}? No coupling in prior — trace the pathway.")
        qs.append(f"Bisect: does {hyp.param} at half delta ({hyp.delta/2:+.2f}) still move {hyp.observable}?")
    if verdict is Verdict.CONTRADICTED:
        qs.append(f"Prior sign wrong for {hyp.param}→{hyp.observable}. What mediates the reversal? Check trap saturation.")
    trans = obs.transitions(hyp.observable)
    if trans:
        qs.append(f"Phase transition(s) in {hyp.observable} at step(s) {trans[:3]} — what changed immediately before?")
    stab = obs.stability(hyp.observable)
    if stab == "diverging":
        qs.append(f"{hyp.observable} diverging under {hyp.param}{hyp.delta:+.2f} — runaway or slow attractor?")
    return qs


# ----------------------------------------------------------------------
# The playground loop
# ----------------------------------------------------------------------

def playground(cycles=10, seed=7):
    rng = random.Random(seed)
    hypgen = HypothesisGenerator(rng)
    base = Config(seed=42)
    base_summary = Observer(run(base)).summary()

    log = []
    print(f"{'cyc':>3} {'param':<22} {'Δ':>6} {'obs':<10} {'z':>7} "
          f"{'verdict':<13} {'repro':>5} {'score':>7}")
    print("-" * 84)

    for c in range(cycles):
        hyp = hypgen.propose()
        cfg = perturbed_config(base, hyp, seed=100)
        history = run(cfg)
        obs = Observer(history)
        z = compare(base_summary, obs.summary(), hyp.observable)
        verdict = judge(hyp, z)
        repro = reproducibility(base, hyp, base_summary) if abs(z) >= 1.5 else 0.0
        questions = generate_questions(hyp, verdict, obs)
        score = interestingness(verdict, z, repro, len(questions))

        print(f"{c:>3} {hyp.param:<22} {hyp.delta:>+6.2f} {hyp.observable:<10} "
              f"{z:>7.2f} {verdict.value:<13} {repro:>5.2f} {score:>7.3f}")
        for q in questions:
            print(f"      ? {q}")

        log.append({"hyp": hyp, "z": z, "verdict": verdict,
                    "repro": repro, "score": score, "questions": questions})

    # rank by interestingness — this is the next-experiment queue
    ranked = sorted(log, key=lambda r: r["score"], reverse=True)
    print("\nNEXT-EXPERIMENT QUEUE (by interestingness):")
    for r in ranked[:3]:
        h = r["hyp"]
        print(f"  [{r['score']:>7.3f}] {h.param} {h.delta:+.2f} → {h.observable}  ({r['verdict'].value})")
    return log


if __name__ == "__main__":
    playground(cycles=12)
