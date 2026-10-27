"""Power-state test (work order section 6a).

For each machine and each power state: does it run, does it need re-homing
after a dropout, is there a manual way, who on site can do it, when was it
last tested. Then a greedy load-shed plan for the minimal-power state.

Nothing is guessed silently. A cell with no data and nothing to derive it
from reads UNKNOWN. "never" (recorded as never tested) is kept apart from
"not recorded".
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from ..schema import Machine, Site

STATES = ("none", "intermittent", "minimal")
READY = ("RUNS", "MANUAL")


@dataclass
class Cell:
    machine: str
    state: str
    status: str                  # RUNS | MANUAL | MANUAL_NO_ONE | STOPS | UNKNOWN
    who_can_run: list[str]
    last_tested: str             # date, "never", or "not recorded"
    rehome_after_dropout: Optional[bool] = None
    basis: str = ""              # where the reading came from


@dataclass
class LoadPlan:
    budget_kw: Optional[float]
    keep: list[str] = field(default_factory=list)
    shed: list[str] = field(default_factory=list)
    unknown_draw: list[str] = field(default_factory=list)
    used_kw: float = 0.0


@dataclass
class PowerResult:
    cells: list[Cell]
    plan: LoadPlan

    @property
    def ready_share(self) -> Optional[float]:
        known = [c for c in self.cells if c.status != "UNKNOWN"]
        if not known:
            return None
        return sum(c.status in READY for c in known) / len(known)

    @property
    def confidence(self) -> float:
        if not self.cells:
            return 0.0
        return sum(c.status != "UNKNOWN" for c in self.cells) / len(self.cells)

    @property
    def never_tested(self) -> int:
        return sum(c.last_tested == "never" for c in self.cells)


def load_shed(machines: list[Machine], budget_kw: Optional[float]) -> LoadPlan:
    """Greedy: keep machines by priority (1 first) while the draw fits."""
    plan = LoadPlan(budget_kw)
    if budget_kw is None:
        plan.unknown_draw = [m.id for m in machines]
        return plan
    order = sorted(machines, key=lambda m: (m.priority is None, m.priority or 0, m.id))
    for m in order:
        if m.power_draw_kw is None:
            plan.unknown_draw.append(m.id)
        elif plan.used_kw + m.power_draw_kw <= budget_kw:
            plan.keep.append(m.id)
            plan.used_kw += m.power_draw_kw
        else:
            plan.shed.append(m.id)
    return plan


def _manual(m: Machine, recorded: Optional[bool]) -> Optional[bool]:
    if recorded is not None:
        return recorded
    if m.manual_mode is None:
        return None
    return m.manual_mode in ("partial", "full")


def _runs(m: Machine, state: str, recorded: Optional[bool],
          plan: LoadPlan) -> tuple[Optional[bool], str]:
    if state == "minimal":
        if m.id in plan.keep:
            return (recorded is not False), "in load-shed plan"
        if m.id in plan.shed:
            return False, "shed: does not fit the kW budget"
    if recorded is not None:
        return recorded, "site record"
    if state == "none" and m.power_draw_kw is not None:
        return m.power_draw_kw == 0, "derived: no power, draw > 0"
    return None, "no record"


def run(site: Site) -> PowerResult:
    plan = load_shed(site.machines, site.power_budget.minimal_kw)
    staff = [o for o in site.operators if o.left_date is None]
    cells = []
    for m in site.machines:
        people = [o.label for o in staff if m.id in o.can_run_manual]
        for state in STATES:
            rec = m.power.get(state)
            runs, basis = _runs(m, state, rec.runs if rec else None, plan)
            manual = _manual(m, rec.manual_alternative if rec else None)
            if runs:
                status = "RUNS"
            elif manual and people:
                status = "MANUAL"
            elif manual:
                status = "MANUAL_NO_ONE"
            elif runs is False and manual is False:
                status = "STOPS"
            else:
                status = "UNKNOWN"
            tested = "not recorded"
            if rec and rec.last_tested is not None:
                tested = str(rec.last_tested)
            cells.append(Cell(m.id, state, status, people, tested,
                              rec.rehome_after_dropout if rec else None, basis))
    return PowerResult(cells, plan)
