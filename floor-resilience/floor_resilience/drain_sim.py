"""Skill-drain simulation (work order section 5).

A port of the published single-file model ``skill-drain-simulator/index.html``
(JS). Same mechanics, every constant exposed and tagged ASSUMED.

Two random sources:

* ``rng="numpy"`` (default): vectorized over operators with
  ``numpy.random.Generator``. Matches the JS model in expectation, not draw
  for draw.
* ``rng="js"``: a line-by-line replay of the JS generator (mulberry32 plus the
  same Knuth Poisson draw, in the same order). With the default seed it
  reproduces the published numbers exactly, which is how the port is checked.

Note on the published figures. Plant A +48 % and the 14-month lead time are
one 40-run draw. Across 30 seed bases at 40 runs the JS model gives
A +48 % (sd 6 pp), B +7 % (sd 4 pp), lead 12 months (sd 6). At 2000 runs it
settles at A +47 %, B +6 %, indicator month 13, alarm month 28-32 across
three seed bases: a lead of 15-19 months. The +50 % alarm sits a few points
under the peak of Plant A's expected scrap curve, so noise decides when it trips.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field, replace
from typing import Optional

import numpy as np

from .schema import Site


@dataclass
class Params:
    n_operators: int = 20            # ASSUMED
    months: int = 60                 # ASSUMED
    runs: int = 40                   # ASSUMED
    initial_veterans: int = 12       # ASSUMED (default plant only)
    turnover_pct: float = 2.5        # ASSUMED monthly quit chance, percent
    retirement_wave_pct: float = 60  # ASSUMED share of veterans retiring in 36 mo
    tau_years: float = 3.0           # ASSUMED years to tacit skill
    screen: str = "written"          # written | hands_on
    reserve: int = 0                 # reserve-line veterans
    drift_rate: float = 3.0          # ASSUMED drifts per machine-month
    fail_rate: float = 0.3           # ASSUMED true failures per machine-month
    parts_per_fault: float = 40.0    # ASSUMED scrapped parts per fault
    vet_skill: float = 0.7           # ASSUMED skill counted as veteran
    newbie_skill: float = 0.4        # ASSUMED skill counted as new hire
    newbies_per_mentor: float = 3.0  # ASSUMED
    first_year_quit_mult: float = 2.0  # ASSUMED, written screen only
    handoff_skill: float = 0.5       # ASSUMED reserve handoff start
    vets_for_full_inhouse: float = 4.0   # ASSUMED
    inspector_base: int = 2          # ASSUMED
    scrap_per_inspector: float = 400.0   # ASSUMED
    indicator_drop: float = 0.30     # ASSUMED veterans-down trigger
    alarm_rise: float = 0.50         # ASSUMED scrap-up trigger


# New-hire starting skill ranges by screen (low, width). ASSUMED.
_START = {"written": (0.02, 0.04), "hands_on": (0.22, 0.10)}

_SCREEN_MAP = {  # site hiring.screen_type -> model screen. interview ASSUMED
    "written": "written", "interview": "written",
    "hands_on_trial": "hands_on", "working_shift": "hands_on",
}


@dataclass
class InitialFloor:
    """Starting state for one run: arrays of length n."""
    skill: np.ndarray
    retire: np.ndarray        # month of retirement, inf if none
    age: np.ndarray           # months on the job; 999 marks a starting veteran
    reserve: np.ndarray       # bool


@dataclass
class SimResult:
    params: Params
    scrap: np.ndarray
    vets: np.ndarray
    outsourced: np.ndarray
    missed_drift: np.ndarray
    true_fail: np.ndarray
    inspectors: np.ndarray
    base: float
    indicator_month: Optional[int]
    alarm_month: Optional[int]
    source: str = "default plant"
    notes: list[str] = field(default_factory=list)

    @property
    def lead_time(self) -> Optional[int]:
        if self.indicator_month is None or self.alarm_month is None:
            return None
        return self.alarm_month - self.indicator_month

    @property
    def scrap_change(self) -> float:
        return float(self.scrap[-1] / self.base - 1) if self.base else float("nan")

    def summary(self) -> dict:
        last = -1
        caught = self.missed_drift[last] + self.true_fail[last]
        return {
            "scrap_month_end": float(self.scrap[last]),
            "scrap_change": self.scrap_change,
            "veterans_month_end": float(self.vets[last]),
            "inspectors_month_end": int(self.inspectors[last]),
            "outsourced_month_end": float(self.outsourced[last]),
            "catchable_share_month_end": float(self.missed_drift[last] / caught) if caught else None,
            "indicator_month": self.indicator_month,
            "alarm_month": self.alarm_month,
            "lead_time_months": self.lead_time,
        }


# --- JS generator replay ---------------------------------------------------
_M = 0xFFFFFFFF


class Mulberry32:
    """Exact replay of the JS ``rng(seed)`` in the published model."""

    def __init__(self, seed: int):
        self.seed = seed & _M

    def random(self) -> float:
        self.seed = (self.seed + 0x6D2B79F5) & _M
        s = self.seed
        t = ((s ^ (s >> 15)) * (1 | s)) & _M
        t = ((t + (((t ^ (t >> 7)) * (61 | t)) & _M)) & _M) ^ t
        return ((t ^ (t >> 14)) & _M) / 4294967296.0

    def poisson(self, lam: float) -> int:
        limit, k, p = math.exp(-lam), 0, 1.0
        while True:
            k += 1
            p *= self.random()
            if not p > limit:
                return k - 1


def _default_floor_js(p: Params, r: Mulberry32) -> InitialFloor:
    n = p.n_operators
    skill, retire, age = np.zeros(n), np.full(n, math.inf), np.zeros(n)
    for i in range(n):
        vet = i < p.initial_veterans
        skill[i] = 0.85 + 0.12 * r.random() if vet else 0.25 + 0.4 * r.random()
        if vet and r.random() < p.retirement_wave_pct / 100:
            retire[i] = 1 + math.floor(r.random() * 36)
        age[i] = 999 if vet else 24
    reserve = np.zeros(n, bool)
    reserve[: p.reserve] = True
    return InitialFloor(skill, retire, age, reserve)


def _default_floor_np(p: Params, g: np.random.Generator) -> InitialFloor:
    n, v = p.n_operators, p.initial_veterans
    is_vet = np.arange(n) < v
    skill = np.where(is_vet, 0.85 + 0.12 * g.random(n), 0.25 + 0.4 * g.random(n))
    retire = np.full(n, math.inf)
    wave = is_vet & (g.random(n) < p.retirement_wave_pct / 100)
    retire[wave] = 1 + np.floor(g.random(wave.sum()) * 36)
    age = np.where(is_vet, 999.0, 24.0)
    reserve = np.arange(n) < p.reserve
    return InitialFloor(skill, retire, age, reserve)


def _run_js(p: Params, seed: int, floor: Optional[InitialFloor]):
    r = Mulberry32(seed)
    f = floor if floor is not None else _default_floor_js(p, r)
    s, retire, age, res = f.skill.copy(), f.retire.copy(), f.age.copy(), f.reserve.copy()
    n, q, tau = len(s), p.turnover_pct / 100, p.tau_years * 12
    lo, width = _START[p.screen]
    out = np.zeros((5, p.months))
    for m in range(1, p.months + 1):
        for i in range(n):
            leave = handoff = False
            if m >= retire[i]:
                leave, handoff = True, bool(res[i])
            elif not res[i]:
                mult = p.first_year_quit_mult if (age[i] < 12 and p.screen == "written") else 1
                if r.random() < q * mult:
                    leave = True
            if leave:
                s[i] = p.handoff_skill if handoff else lo + width * r.random()
                retire[i], age[i] = math.inf, 0
        vets = int(np.sum((s >= p.vet_skill) | (res & (age >= 999))))
        newbies = int(np.sum(s < p.newbie_skill))
        mf = min(1.0, vets / max(1.0, newbies / p.newbies_per_mentor))
        s += (1 - s) / (tau / (0.3 + 0.7 * mf))
        age += 1
        miss = fail = 0
        for i in range(n):
            d = r.poisson(p.drift_rate)
            for _ in range(d):
                if r.random() > s[i]:
                    miss += 1
            fail += r.poisson(p.fail_rate)
        out[:, m - 1] = _month_row(p, s, miss, fail)
    return out


def _run_np(p: Params, g: np.random.Generator, floor: Optional[InitialFloor]):
    f = floor if floor is not None else _default_floor_np(p, g)
    s, retire, age, res = f.skill.copy(), f.retire.copy(), f.age.copy(), f.reserve.copy()
    n, q, tau = len(s), p.turnover_pct / 100, p.tau_years * 12
    lo, width = _START[p.screen]
    out = np.zeros((5, p.months))
    for m in range(1, p.months + 1):
        retiring = m >= retire
        mult = np.where((age < 12) & (p.screen == "written"), p.first_year_quit_mult, 1.0)
        quits = (~retiring) & (~res) & (g.random(n) < q * mult)
        leave = retiring | quits
        handoff = retiring & res
        fresh = lo + width * g.random(n)
        s = np.where(leave, np.where(handoff, p.handoff_skill, fresh), s)
        retire = np.where(leave, math.inf, retire)
        age = np.where(leave, 0.0, age)
        vets = int(np.sum((s >= p.vet_skill) | (res & (age >= 999))))
        newbies = int(np.sum(s < p.newbie_skill))
        mf = min(1.0, vets / max(1.0, newbies / p.newbies_per_mentor))
        s = s + (1 - s) / (tau / (0.3 + 0.7 * mf))
        age = age + 1
        drifts = g.poisson(p.drift_rate, n)
        miss = int(g.binomial(drifts, 1 - s).sum())
        fail = int(g.poisson(p.fail_rate, n).sum())
        out[:, m - 1] = _month_row(p, s, miss, fail)
    return out


def _month_row(p: Params, s: np.ndarray, miss: int, fail: int):
    vets_now = float(np.sum(s >= p.vet_skill))
    inhouse = min(1.0, vets_now / p.vets_for_full_inhouse)
    return [(miss + fail) * p.parts_per_fault, vets_now,
            (miss + fail) * (1 - inhouse), miss, fail]


def floor_from_site(site: Site, p: Params) -> tuple[InitialFloor, Params, list[str]]:
    """Starting floor from a site file instead of the default 12-veteran plant.

    Skill from tenure: s = 1 - exp(-tenure / tau)  (ASSUMED). Retirements come
    from retiring_within_months, so the random retirement wave is not applied.
    """
    notes: list[str] = []
    ops = [o for o in site.operators if o.left_date is None]
    if not ops:
        raise ValueError("site has no current operators; cannot start from it")
    tau = p.tau_years * 12
    skill, retire, age, reserve = [], [], [], []
    missing_tenure = 0
    for o in ops:
        t = o.tenure_months
        if t is None:
            missing_tenure += 1
            t = 0.0
        sk = 1 - math.exp(-t / tau)
        skill.append(sk)
        age.append(999.0 if sk >= p.vet_skill else float(t))
        r = o.retiring_within_months
        retire.append(max(1, math.ceil(r)) if r is not None else math.inf)
        reserve.append(bool(o.reserve))
    if missing_tenure:
        notes.append(f"{missing_tenure} operator(s) with no tenure started at skill 0")
    screen = _SCREEN_MAP.get(site.hiring.screen_type or "", None)
    if screen is None:
        notes.append(f"hiring screen unknown; using '{p.screen}' (ASSUMED)")
        screen = p.screen
    p2 = replace(p, n_operators=len(ops), screen=screen,
                 reserve=int(sum(reserve)))
    floor = InitialFloor(np.array(skill), np.array(retire, float),
                         np.array(age), np.array(reserve, bool))
    return floor, p2, notes


def simulate(params: Optional[Params] = None, seed: int = 1000,
             rng: str = "numpy", site: Optional[Site] = None) -> SimResult:
    """Average ``params.runs`` seeded runs. Same seed, same answer."""
    p = params or Params()
    if p.screen not in _START:
        raise ValueError(f"screen must be one of {sorted(_START)}")
    floor, notes, source = None, [], "default plant"
    if site is not None:
        floor, p, notes = floor_from_site(site, p)
        source = f"site: {site.name or 'unnamed'}"
    acc = np.zeros((5, p.months))
    if rng == "js":
        for k in range(p.runs):
            acc += _run_js(p, seed + k * 7919, floor)
    elif rng == "numpy":
        g = np.random.default_rng(seed)
        for _ in range(p.runs):
            acc += _run_np(p, g, floor)
    else:
        raise ValueError("rng must be 'numpy' or 'js'")
    acc /= p.runs
    scrap, vets, outs, miss, fail = acc
    base = float(scrap[:3].mean())
    insp = p.inspector_base + np.maximum(0, np.ceil((scrap - base) / p.scrap_per_inspector))
    v0 = vets[0]
    ind = next((m + 1 for m in range(p.months) if vets[m] < (1 - p.indicator_drop) * v0), None)
    alarm = next((m + 1 for m in range(p.months) if scrap[m] > (1 + p.alarm_rise) * base), None)
    return SimResult(p, scrap, vets, outs, miss, fail, insp.astype(int), base,
                     ind, alarm, source, notes)


def plant_a(**kw) -> Params:
    """Published Plant A: written screen, no reserve line."""
    return Params(screen="written", reserve=0, **kw)


def plant_b(**kw) -> Params:
    """Published Plant B: hands-on trial, 3 reserve veterans."""
    return Params(screen="hands_on", reserve=3, **kw)
