# SPDX-License-Identifier: CC0-1.0
"""
GAP 4 rig machinery: phase-integrated agent-lifecycle energy.

Built to WORK_ORDER.md. The rig measures joules by phase over an agent
lifecycle (idle / spin-up / task / teardown), on TWO channels (wall meter,
card telemetry), for two lifecycle patterns (RUN A: N disposable
single-task agents; RUN B: one persistent agent doing N tasks), and reports
three derived figures: setup_fraction, amortization_curve, succession_loss.

WHAT RUNS HERE AND WHAT DOES NOT.

This file is the machinery. It integrates a power trace, holds the per-run
record, and computes the derived figures -- all of it correct by
construction and checked on constructed traces in selftest_ale.py. What it
CANNOT do in this environment is take a measurement: there is no GPU, no
wall meter, and no `nvidia-smi` here (see trace_parse.probe_hardware and
RIG_STATUS.md). So no real joule figure is produced, and none is
fabricated. The rig ships ready to run on hardware; the number is the gap.

TWO RULES FROM THE WORK ORDER, ENFORCED IN CODE, NOT DESCRIBED:

  - "Report wall and card figures separately. Never blend them." Every
    derived figure takes a single `channel` in {"wall", "card"};
    `blend_wall_card` raises. A ratio across the two channels is a reported
    diagnostic, not a blend, so `wall_card_ratio` is allowed -- it compares,
    it does not sum.
  - "Report cold and warm start separately. Never average them." Every
    aggregation refuses a set that mixes `cold_or_warm`; `mean_over_runs`
    raises on a mixed set, and so does any curve or loss built across one.

ABSENT IS NOT ZERO. A phase with no samples cannot be integrated and its
energy is `None` with flag NO_SAMPLES, never 0.0 joules; one sample is
SINGLE_SAMPLE (a window needs two points). A phase whose effective sample
rate is below the work order's 10 Hz floor carries a real number AND an
UNDERSAMPLED flag -- present-but-suspect, a third state, because the work
order says 1 Hz "will miss the peak and undercount": the number exists and
should not be trusted as a peak.

Stdlib only. Parses under Python 3.9. ASCII only. CC0.

    python3 agent-lifecycle-energy/selftest_ale.py
"""

from __future__ import annotations

from collections import namedtuple
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

# A power sample: t in seconds (monotonic), watts instantaneous draw.
Sample = namedtuple("Sample", "t watts")

# From the work order, not a [CHOICE]: "Sample at >= 10 Hz on both if
# possible. Spin-up is short and spiky; 1 Hz will miss the peak and
# undercount." A phase sampled below this floor is flagged UNDERSAMPLED.
MIN_HZ = 10.0

# Phase-energy flags. Kept apart on purpose (absent-vs-known-negative):
OK = "OK"                    # >= 2 samples, rate >= MIN_HZ
UNDERSAMPLED = "UNDERSAMPLED"  # >= 2 samples, rate < MIN_HZ; number present
SINGLE_SAMPLE = "SINGLE_SAMPLE"  # one sample; no window; joules None
NO_SAMPLES = "NO_SAMPLES"    # empty phase; joules None

CHANNELS = ("wall", "card")

# [CHOICE 1] the idle baseline P_idle is the MEAN of the PHASE 0 samples.
# The median is more robust to a single transient in the idle window; the
# mean is used here and the method is recorded in `IdleBaseline.method` so a
# reader can see which was taken. Printed on every render.
BASELINE_METHOD = "mean"

# [CHOICE 2] integration is trapezoidal over the sampled (t, watts) points.
# A left/right Riemann sum would bias a rising or falling phase by up to one
# sample-interval's worth of area; trapezoidal is exact on any piecewise-
# linear trace, which is what a sampled meter delivers between points. The
# rule is pinned by tools/known_answer.py (constant, ramp, zero-marginal).
INTEGRATION = "trapezoidal"


class ChannelBlend(Exception):
    """Raised on any attempt to combine wall and card energies into one
    figure. The work order: never blend them."""


class ThermalStateMix(Exception):
    """Raised on any attempt to average or aggregate across cold and warm
    starts. The work order: never average them."""


class IdleBaselineUnknown(Exception):
    """Raised when a marginal energy is asked for with no idle baseline to
    subtract. You cannot report a marginal figure without P_idle."""


class MismatchedRuns(Exception):
    """Raised when succession_loss or a curve is asked to compare runs that
    differ on something that must be held constant (N, model, task class,
    thermal state, or channel)."""


@dataclass
class IdleBaseline:
    watts: float
    method: str
    n: int


@dataclass
class PhaseEnergy:
    """Marginal joules over one phase on one channel, plus the state of the
    measurement. `joules` is None exactly when the phase could not be
    integrated (NO_SAMPLES / SINGLE_SAMPLE); an UNDERSAMPLED phase carries a
    number that is a lower bound on a spiky peak, flagged."""
    joules: Optional[float]
    flag: str
    n: int
    duration_s: Optional[float]
    hz: Optional[float]
    channel: str
    phase: str

    @property
    def is_number(self) -> bool:
        return self.joules is not None


def _check_channel(channel: str) -> None:
    if channel not in CHANNELS:
        raise ValueError(
            "channel must be one of %r (wall and card are measured "
            "separately and never blended); got %r" % (CHANNELS, channel))


def idle_baseline(phase0: List[Sample]) -> IdleBaseline:
    """P_idle from the PHASE 0 (idle) window. Raises if the window is empty
    -- there is nothing to baseline-subtract against."""
    if not phase0:
        raise IdleBaselineUnknown(
            "PHASE 0 idle window is empty; no P_idle to subtract")
    watts = [s.watts for s in phase0]
    val = sum(watts) / float(len(watts))     # BASELINE_METHOD == "mean"
    return IdleBaseline(watts=val, method=BASELINE_METHOD, n=len(watts))


def integrate(samples: List[Sample], p_idle: float,
              channel: str, phase: str) -> PhaseEnergy:
    """Marginal energy over one phase:  integral (P(t) - P_idle) dt,
    trapezoidal, baseline-subtracted. Returns a PhaseEnergy carrying the
    number AND the state of the measurement -- an empty or single-sample
    phase yields joules=None (not 0.0), an undersampled phase yields a
    number flagged UNDERSAMPLED."""
    _check_channel(channel)
    n = len(samples)
    if n == 0:
        return PhaseEnergy(None, NO_SAMPLES, 0, None, None, channel, phase)
    if n == 1:
        return PhaseEnergy(None, SINGLE_SAMPLE, 1, 0.0, None, channel, phase)
    # trapezoidal integral of the baseline-subtracted trace
    joules = 0.0
    for a, b in zip(samples[:-1], samples[1:]):
        dt = b.t - a.t
        if dt < 0:
            raise ValueError(
                "%s/%s: samples not monotonic in t (%r -> %r)"
                % (channel, phase, a.t, b.t))
        ma = a.watts - p_idle
        mb = b.watts - p_idle
        joules += 0.5 * (ma + mb) * dt
    duration = samples[-1].t - samples[0].t
    hz = (n - 1) / duration if duration > 0 else None
    if hz is None:
        # all samples at one instant; a degenerate window
        return PhaseEnergy(None, SINGLE_SAMPLE, n, 0.0, None, channel, phase)
    flag = OK if hz >= MIN_HZ else UNDERSAMPLED
    return PhaseEnergy(joules, flag, n, duration, hz, channel, phase)


# --------------------------------------------------------------------------
# The per-run record. Matches the work order's per-run record exactly, with
# each E_* held as a PhaseEnergy (number + state) rather than a bare float,
# so an absent or undersampled phase cannot masquerade as a measured zero.
# --------------------------------------------------------------------------

PHASES = ("spinup", "task", "teardown")


@dataclass
class LifecycleRun:
    run_id: str
    condition: str            # "A" (disposable) or "B" (persistent)
    N: int                    # tasks in A == agents; tasks in B == tasks
    task_class: str
    model_id: str
    cold_or_warm: str         # "cold" or "warm" -- never averaged across
    ambient_c: Optional[float]
    # per phase, per channel:
    energy: Dict[str, Dict[str, PhaseEnergy]] = field(default_factory=dict)
    wall_clock_per_phase: Dict[str, float] = field(default_factory=dict)

    def phase(self, phase: str, channel: str) -> PhaseEnergy:
        _check_channel(channel)
        return self.energy[channel][phase]


def _validate_condition(cond: str) -> None:
    if cond not in ("A", "B"):
        raise ValueError("condition must be 'A' or 'B'; got %r" % cond)


def _validate_thermal(cw: str) -> None:
    if cw not in ("cold", "warm"):
        raise ValueError("cold_or_warm must be 'cold' or 'warm'; got %r" % cw)


def run_from_traces(run_id, condition, N, task_class, model_id,
                    cold_or_warm, ambient_c,
                    idle_traces: Dict[str, List[Sample]],
                    phase_traces: Dict[str, Dict[str, List[Sample]]]
                    ) -> LifecycleRun:
    """Build a LifecycleRun from raw traces.

    `idle_traces`  : {channel: [Sample,...]}      -- PHASE 0 per channel
    `phase_traces` : {channel: {phase: [Sample]}} -- PHASE 1/2/3 per channel

    Each channel is baseline-subtracted against its OWN idle window (a wall
    idle and a card idle are different numbers and are never crossed).
    """
    _validate_condition(condition)
    _validate_thermal(cold_or_warm)
    energy: Dict[str, Dict[str, PhaseEnergy]] = {}
    wall_clock: Dict[str, float] = {}
    for channel in CHANNELS:
        _check_channel(channel)
        base = idle_baseline(idle_traces.get(channel, []))
        energy[channel] = {}
        for phase in PHASES:
            samples = phase_traces.get(channel, {}).get(phase, [])
            pe = integrate(samples, base.watts, channel, phase)
            energy[channel][phase] = pe
            if pe.duration_s is not None:
                # phases agree in wall-clock across channels; last writer ok
                wall_clock[phase] = pe.duration_s
    return LifecycleRun(
        run_id=run_id, condition=condition, N=N, task_class=task_class,
        model_id=model_id, cold_or_warm=cold_or_warm, ambient_c=ambient_c,
        energy=energy, wall_clock_per_phase=wall_clock)


# --------------------------------------------------------------------------
# Derived figures. Each takes a single channel; none crosses wall and card.
# NOT_COMPUTABLE is returned (never 0.0) when a component energy is absent.
# --------------------------------------------------------------------------

NOT_COMPUTABLE = "NOT_COMPUTABLE"
UNDERSAMPLED_PRESENT = "UNDERSAMPLED_PRESENT"


@dataclass
class Total:
    joules: Optional[float]
    flag: str                 # OK | UNDERSAMPLED_PRESENT | NOT_COMPUTABLE
    reason: Optional[str]
    channel: str


# [CHOICE 3] the record's E_task is PER REPRESENTATIVE TASK -- one task's
# execution energy, not the whole task phase of a multi-task run. If a RUN B
# task window covered N tasks, divide by the task count before recording. The
# work order's record lists a single E_task, and this is the interpretation
# that makes the two totals below build from the same per-task number:
#
#   RUN A (N disposable agents, 1 task each):  N * (E_spinup + E_task + E_teardown)
#   RUN B (1 persistent agent, N tasks):       E_spinup + N * E_task + E_teardown
#
# so succession_loss reduces to (N-1)(E_spinup + E_teardown) -- the extra
# spin-up/teardown cycles disposability pays for, exactly.


def lifecycle_energy(run: LifecycleRun, channel: str) -> Total:
    """The three phase energies of ONE lifecycle episode, summed:
    E_spinup + E_task + E_teardown on one channel. This is the per-episode
    figure setup_fraction is taken over. NOT_COMPUTABLE if any phase could
    not be integrated (never a partial sum passed off as a whole)."""
    _check_channel(channel)
    total = 0.0
    undersampled = False
    for phase in PHASES:
        pe = run.phase(phase, channel)
        if not pe.is_number:
            return Total(None, NOT_COMPUTABLE,
                         "%s phase is %s" % (phase, pe.flag), channel)
        if pe.flag == UNDERSAMPLED:
            undersampled = True
        total += pe.joules
    return Total(total, UNDERSAMPLED_PRESENT if undersampled else OK,
                 None, channel)


def total_energy(run: LifecycleRun, channel: str) -> Total:
    """Total energy of the whole RUN on one channel, built from the
    per-task phase energies and the lifecycle pattern (see [CHOICE 3]):
    RUN A pays N full lifecycles; RUN B pays one spin-up and one teardown
    with N task executions. NOT_COMPUTABLE if any component phase is
    absent."""
    _check_channel(channel)
    s = run.phase("spinup", channel)
    t = run.phase("task", channel)
    d = run.phase("teardown", channel)
    for pe in (s, t, d):
        if not pe.is_number:
            return Total(None, NOT_COMPUTABLE,
                         "%s phase is %s" % (pe.phase, pe.flag), channel)
    undersampled = any(pe.flag == UNDERSAMPLED for pe in (s, t, d))
    if run.condition == "A":
        total = run.N * (s.joules + t.joules + d.joules)
    else:  # "B"
        total = s.joules + run.N * t.joules + d.joules
    return Total(total, UNDERSAMPLED_PRESENT if undersampled else OK,
                 None, channel)


@dataclass
class SetupFraction:
    value: Optional[float]
    flag: str
    reason: Optional[str]
    channel: str


def setup_fraction(run: LifecycleRun, channel: str) -> SetupFraction:
    """E_spinup / (E_spinup + E_task + E_teardown) on one channel -- a
    per-lifecycle property, so it is taken over the single-episode figure
    (lifecycle_energy), not the run total, and does not depend on N."""
    _check_channel(channel)
    tot = lifecycle_energy(run, channel)
    if tot.joules is None:
        return SetupFraction(None, NOT_COMPUTABLE, tot.reason, channel)
    if tot.joules == 0.0:
        return SetupFraction(None, NOT_COMPUTABLE,
                             "lifecycle marginal energy is zero", channel)
    spin = run.phase("spinup", channel)
    return SetupFraction(spin.joules / tot.joules, tot.flag, None, channel)


def _tasks_delivered(run: LifecycleRun) -> int:
    """Both conditions deliver N tasks: RUN A is N agents x 1 task, RUN B is
    1 agent x N tasks. Work delivered is held constant across the pair."""
    return run.N


@dataclass
class SuccessionLoss:
    joules: Optional[float]
    N: int
    channel: str
    cold_or_warm: str
    reason: Optional[str]


def succession_loss(run_a: LifecycleRun, run_b: LifecycleRun,
                    channel: str) -> SuccessionLoss:
    """THE HEADLINE. (total E, RUN A) - (total E, RUN B) at the same N, same
    model, same task class, same thermal state, same channel. The joule cost
    of disposability, holding work delivered constant. Refuses any mismatch
    rather than differencing two things that are not comparable."""
    _check_channel(channel)
    if run_a.condition != "A" or run_b.condition != "B":
        raise MismatchedRuns(
            "succession_loss compares a RUN A (disposable) against a RUN B "
            "(persistent); got conditions %r and %r"
            % (run_a.condition, run_b.condition))
    for attr in ("N", "model_id", "task_class", "cold_or_warm"):
        if getattr(run_a, attr) != getattr(run_b, attr):
            raise MismatchedRuns(
                "succession_loss requires equal %s; A=%r B=%r"
                % (attr, getattr(run_a, attr), getattr(run_b, attr)))
    ta = total_energy(run_a, channel)
    tb = total_energy(run_b, channel)
    if ta.joules is None or tb.joules is None:
        return SuccessionLoss(
            None, run_a.N, channel, run_a.cold_or_warm,
            "NOT_COMPUTABLE: %s"
            % (ta.reason if ta.joules is None else tb.reason))
    return SuccessionLoss(ta.joules - tb.joules, run_a.N, channel,
                          run_a.cold_or_warm, None)


@dataclass
class AmortPoint:
    N: int
    joules_per_task: Optional[float]
    flag: str
    reason: Optional[str]


def amortization_curve(runs: List[LifecycleRun], channel: str
                       ) -> List[AmortPoint]:
    """joules_per_task_instance vs N, for one condition, one channel, one
    thermal state, one model, one task class. Refuses a set that mixes any
    of those -- averaging a cold curve into a warm one, or a disposable
    condition into a persistent one, would be exactly the blend the work
    order forbids. Sorted by N."""
    _check_channel(channel)
    if not runs:
        return []
    ref = runs[0]
    for r in runs:
        if r.condition != ref.condition:
            raise MismatchedRuns(
                "amortization_curve mixes conditions %r and %r"
                % (ref.condition, r.condition))
        if r.cold_or_warm != ref.cold_or_warm:
            raise ThermalStateMix(
                "amortization_curve mixes %r and %r starts; the work order "
                "says never average them" % (ref.cold_or_warm, r.cold_or_warm))
        if r.model_id != ref.model_id or r.task_class != ref.task_class:
            raise MismatchedRuns(
                "amortization_curve mixes model/task class")
    out = []
    for r in sorted(runs, key=lambda x: x.N):
        tot = total_energy(r, channel)
        tasks = _tasks_delivered(r)
        if tot.joules is None or tasks == 0:
            out.append(AmortPoint(r.N, None, NOT_COMPUTABLE,
                                  tot.reason or "zero tasks"))
        else:
            out.append(AmortPoint(r.N, tot.joules / tasks, tot.flag, None))
    return out


# --------------------------------------------------------------------------
# Diagnostics that COMPARE the channels (allowed) vs BLEND them (refused).
# --------------------------------------------------------------------------

def wall_card_ratio(run: LifecycleRun, phase: str) -> Optional[float]:
    """wall / card marginal energy for one phase -- a reported ratio, the
    'delta between A and B' the work order asks for. This is a comparison,
    not a blend: it does not sum the two channels into one energy. Returns
    None if either channel could not be integrated, or if card is zero."""
    w = run.phase(phase, "wall")
    c = run.phase(phase, "card")
    if not w.is_number or not c.is_number or c.joules == 0.0:
        return None
    return w.joules / c.joules


def blend_wall_card(*_a, **_k):
    """FORBIDDEN. The work order: report wall and card separately, never
    blend. Summing or averaging the two channels into one energy is the
    blend this refuses. Use wall_card_ratio to compare them."""
    raise ChannelBlend(
        "wall and card measure different things (full system vs accelerator "
        "only) and are never combined into one figure; report them "
        "separately and use wall_card_ratio to compare")


def mean_over_runs(runs: List[LifecycleRun], channel: str) -> Optional[float]:
    """Mean total energy across repeats on one channel. Refuses a set that
    mixes cold and warm starts, or conditions -- a repeat set must be one
    thermal state and one condition, or the mean is meaningless."""
    _check_channel(channel)
    if not runs:
        return None
    ref = runs[0]
    for r in runs:
        if r.cold_or_warm != ref.cold_or_warm:
            raise ThermalStateMix(
                "mean_over_runs mixes %r and %r starts; never average them"
                % (ref.cold_or_warm, r.cold_or_warm))
        if r.condition != ref.condition:
            raise MismatchedRuns("mean_over_runs mixes conditions")
    vals = []
    for r in runs:
        tot = total_energy(r, channel)
        if tot.joules is None:
            return None          # an absent total is not averaged in as 0
        vals.append(tot.joules)
    return sum(vals) / float(len(vals))


if __name__ == "__main__":
    import sys
    sys.stderr.write(
        "phase_energy.py is the rig machinery, not a runnable check. "
        "The known-answer and constructed-trace checks live in "
        "agent-lifecycle-energy/selftest_ale.py; run that.\n")
    sys.exit(2)
