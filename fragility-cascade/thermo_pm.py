#!/usr/bin/env python3
"""
thermo_pm.py -- Thermodynamic Project Management Engine
CC0 / Public Domain -- No rights reserved.  stdlib-only.

Consolidates the diagnostic fixes. The referee now WEIGHS: no process may
emit more energy or matter than it takes in (plus declared draws from
stocks). Presence-before-use is kept AND conservation is enforced.
Violations name the equation that did not close.

Resource types
    energy       conserved   (out + byproducts <= in)
    matter       conserved   (out + byproducts <= in; loss to sink allowed)
    information  NOT conserved, read-only when used as input
                 (skills, readings, permits, mode markers -- gates)
    artifact     NOT conserved, count-semantics, IS consumable
                 (tools wear, walls exist; a sink for spent matter)
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
import copy
from collections import deque

EPS = 1e-9
ResourceType = str  # "energy" | "matter" | "information" | "artifact"


# =============================================================================
# 1. Resource
# =============================================================================
@dataclass
class Resource:
    name: str
    type: ResourceType
    amount: float
    unit: str = ""
    location: str = "site"
    info_value: Optional[str] = None   # qualitative tag, e.g. "200", "clay_low"

    def copy(self) -> "Resource":
        return Resource(self.name, self.type, self.amount, self.unit,
                        self.location, self.info_value)


# =============================================================================
# 2. Process
# =============================================================================
@dataclass
class Process:
    name: str
    inputs: Dict[str, float]
    outputs: Dict[str, float]
    byproducts: Dict[str, float] = field(default_factory=dict)
    side_effects: Dict[str, float] = field(default_factory=dict)
    skill_required: Optional[str] = None
    efficiency: Optional[float] = None          # ADVISORY only; checked vs computed
    types: Dict[str, str] = field(default_factory=dict)  # declare type of NEW names


# =============================================================================
# 3. System
# =============================================================================
@dataclass
class System:
    name: str
    resources: Dict[str, Resource] = field(default_factory=dict)
    processes: Dict[str, Process] = field(default_factory=dict)
    types: Dict[str, str] = field(default_factory=dict)   # name -> type registry
    warnings: List[str] = field(default_factory=list)

    # ---- resource bookkeeping ------------------------------------------------
    def add_resource(self, res: Resource):
        self.types[res.name] = res.type
        if res.name in self.resources:
            self.resources[res.name].amount += res.amount
        else:
            self.resources[res.name] = res.copy()

    def register_process(self, p: Process):
        self.processes[p.name] = p
        for n, t in p.types.items():
            self.types.setdefault(n, t)

    def type_of(self, name: str) -> str:
        base = name.partition(":")[0]
        if name in self.types:
            return self.types[name]
        if base in self.types:
            return self.types[base]
        self.warnings.append(f"unknown type for '{name}', defaulting matter")
        return "matter"

    # ---- FIX 1: literal-match BEFORE ':' partition --------------------------
    def _match(self, key: str) -> Optional[Resource]:
        """Resolve an input key to a live resource, or None."""
        if key in self.resources:                 # literal name first
            return self.resources[key]
        base, _, val = key.partition(":")         # then info-value match
        if base in self.resources:
            r = self.resources[base]
            if val and r.info_value != val:
                return None
            return r
        return None

    def has_enough(self, requirements: Dict[str, float]) -> bool:
        for key, amt in requirements.items():
            r = self._match(key)
            if r is None or r.amount < amt - EPS:
                return False
        return True

    # ---- FIX 1b: information inputs are READ-ONLY gates ----------------------
    def consume(self, requirements: Dict[str, float]):
        for key, amt in requirements.items():
            r = self._match(key)
            if r is None:
                continue
            if r.type == "information":           # gate -> do not drain
                continue
            r.amount -= amt

    # ---- typed sums for the balance check -----------------------------------
    def _typed_in(self, proc: Process, want: str) -> float:
        tot = 0.0
        for key, amt in proc.inputs.items():
            r = self._match(key)
            t = r.type if r is not None else self.type_of(key)
            if t == want:
                tot += amt
        return tot

    def _typed_out(self, proc: Process, want: str) -> float:
        tot = 0.0
        for d in (proc.outputs, proc.byproducts):
            for name, amt in d.items():
                if self.type_of(name) == want:
                    tot += amt
        return tot

    # ---- FIX 2 + 4: weigh, then run -----------------------------------------
    def run_process(self, proc: Process) -> Tuple[bool, str]:
        # skill gate
        if proc.skill_required and self._match(proc.skill_required) is None:
            return False, f"missing skill '{proc.skill_required}' ({proc.name})"
        # presence
        if not self.has_enough(proc.inputs):
            missing = {k: a for k, a in proc.inputs.items()
                       if self._match(k) is None or self._match(k).amount < a - EPS}
            return False, f"missing resources {missing} ({proc.name})"

        # CONSERVATION pre-check -- energy and matter only
        for t in ("energy", "matter"):
            e_in = self._typed_in(proc, t)
            e_out = self._typed_out(proc, t)
            if e_out > e_in + EPS:
                return False, (f"{t} not conserved: out {e_out:g} > in {e_in:g} "
                               f"({proc.name})")

        # advisory: does declared efficiency match reality?
        e_in = self._typed_in(proc, "energy")
        e_out_useful = sum(a for n, a in proc.outputs.items()
                           if self.type_of(n) == "energy")
        e_bp = sum(a for n, a in proc.byproducts.items()
                   if self.type_of(n) == "energy")
        if proc.efficiency is not None and e_in > EPS:
            actual = e_out_useful / e_in
            if abs(actual - proc.efficiency) > 0.05:
                self.warnings.append(
                    f"{proc.name}: declared eff {proc.efficiency:.2f} "
                    f"!= computed {actual:.2f}")

        # commit: consume inputs
        self.consume(proc.inputs)

        # produce outputs (full declared amount; balance already guaranteed it fits)
        for name, amt in proc.outputs.items():
            self.add_resource(Resource(name, self.type_of(name), amt))
        for name, amt in proc.byproducts.items():
            self.add_resource(Resource(name, self.type_of(name), amt))

        # FIX 4: waste heat is the ENERGY RESIDUAL, not efficiency*out
        waste = e_in - e_out_useful - e_bp
        if waste > EPS:
            self.add_resource(Resource("waste_heat", "energy", waste, "J"))

        # side effects (clamp at 0)
        for name, delta in proc.side_effects.items():
            if name in self.resources:
                self.resources[name].amount = max(0.0,
                                                  self.resources[name].amount + delta)
        return True, "ok"


# =============================================================================
# 4. Validator
# =============================================================================
@dataclass
class ValidationError:
    step: int
    process_name: str
    message: str


class Validator:
    def __init__(self, system: System):
        self.original = system

    def validate(self, plan: List[str],
                 stability_thresholds: Optional[Dict[str, float]] = None
                 ) -> List[ValidationError]:
        sim = copy.deepcopy(self.original)
        errors: List[ValidationError] = []
        for i, pname in enumerate(plan):
            if pname not in sim.processes:
                errors.append(ValidationError(i, pname, "unknown process"))
                return errors
            ok, reason = sim.run_process(sim.processes[pname])
            if not ok:
                errors.append(ValidationError(i, pname, reason))
                return errors
        if stability_thresholds:
            for name, floor in stability_thresholds.items():
                if name in sim.resources and sim.resources[name].amount < floor:
                    errors.append(ValidationError(
                        len(plan), "STABILITY",
                        f"{name} = {sim.resources[name].amount:g} < {floor:g}"))
        return errors


# =============================================================================
# 5. Planner (BFS, mode-gated)
# =============================================================================
def plan_with_mode(system: System, goals: Dict[str, float], mode: str,
                   max_steps: int = 25) -> Optional[Tuple[List[str], System]]:
    allowed = []
    for p in system.processes.values():
        gate = next((k for k in p.inputs if k.startswith("mode:")), None)
        if gate is None or gate == f"mode:{mode}":
            allowed.append(p)

    start = copy.deepcopy(system)
    start.add_resource(Resource(f"mode:{mode}", "information", 1, info_value=mode))

    def met(s: System) -> bool:
        return all(s.resources.get(g, Resource(g, "matter", 0)).amount >= a - EPS
                   for g, a in goals.items())

    def h(s: System) -> str:
        return ",".join(f"{r}={s.resources[r].amount:.2f}"
                        for r in sorted(s.resources))

    queue = deque([(start, [])])
    seen = set()
    while queue:
        cur, plan = queue.popleft()
        if met(cur):
            return plan, cur
        if len(plan) >= max_steps:
            continue
        key = h(cur)
        if key in seen:
            continue
        seen.add(key)
        for proc in allowed:
            nxt = copy.deepcopy(cur)
            ok, _ = nxt.run_process(proc)
            if ok:
                queue.append((nxt, plan + [proc.name]))
    return None


# =============================================================================
# 6. Demo scenario -- self-proving: valid plan runs, conjuring is rejected
# =============================================================================
def build_demo() -> System:
    s = System("ForestedClayDemo")
    # fungible + stocks
    s.add_resource(Resource("human_labor",     "energy", 100_000, "J"))
    s.add_resource(Resource("standing_biomass", "energy", 50_000, "J"))   # STOCK
    s.add_resource(Resource("biomass_mass",    "matter", 20, "kg"))        # ash source
    s.add_resource(Resource("clay",            "matter", 500, "kg"))
    s.add_resource(Resource("water",           "matter", 200, "kg"))
    s.add_resource(Resource("waste_heat",      "energy", 0, "J"))
    # information gate (skill) + declared artifact/energy types for new names
    s.add_resource(Resource("masonry",         "information", 1, "bit"))

    common_types = {
        "biomass": "energy", "steam_heat": "energy", "mechanical_work": "energy",
        "ash": "matter", "crushed_aggregate": "matter",
        "boiler": "artifact", "wall": "artifact", "offsite_reserve": "matter",
        "diesel": "energy",
    }

    P = [
        Process("gather_biomass",
                inputs={"human_labor": 2000, "standing_biomass": 15000},
                outputs={"biomass": 15000}, types=common_types),
        Process("burn_biomass",
                inputs={"biomass": 10000, "biomass_mass": 3},
                outputs={"steam_heat": 4000}, byproducts={"ash": 2},
                types=common_types),
        Process("make_boiler",
                inputs={"clay": 80, "water": 30, "human_labor": 8000},
                outputs={"boiler": 1}, skill_required="masonry",
                types=common_types),
        Process("run_engine",
                inputs={"steam_heat": 2000, "boiler": 0.01},
                outputs={"mechanical_work": 1000}, types=common_types),
        Process("form_wall",
                inputs={"mechanical_work": 500, "clay": 100, "human_labor": 3000},
                outputs={"wall": 1}, types=common_types),
        # --- code_compliant: conjures matter from nothing -> MUST be rejected
        Process("import_fill_bad",
                inputs={"mode:code_compliant": 1, "human_labor": 2000},
                outputs={"crushed_aggregate": 5000}, types=common_types),
        # --- honest import: sourced from off-site reserve, diesel cost visible
        Process("import_fill_sourced",
                inputs={"mode:code_compliant": 1, "human_labor": 2000,
                        "offsite_reserve": 5000, "diesel": 3000},
                outputs={"crushed_aggregate": 5000}, types=common_types),
    ]
    for p in P:
        s.register_process(p)
    return s


if __name__ == "__main__":
    print("=" * 62)
    print("THERMO_PM -- referee now weighs")
    print("=" * 62)

    # 1) a valid site-only plan: waste is COMPUTED, not typed
    sys = build_demo()
    plan = ["gather_biomass", "burn_biomass", "make_boiler",
            "run_engine", "form_wall"]
    errs = Validator(sys).validate(plan)
    print("\n[1] site-only plan:", " -> ".join(plan))
    if errs:
        for e in errs:
            print(f"    FAIL step {e.step} ({e.process_name}): {e.message}")
    else:
        sim = copy.deepcopy(sys)
        for pn in plan:
            sim.run_process(sim.processes[pn])
        wh = sim.resources.get("waste_heat", Resource("w", "energy", 0)).amount
        print(f"    VALID. computed waste_heat = {wh:g} J")
        for w in sim.warnings:
            print(f"    advisory: {w}")

    # 2) the conjuring path is now CAUGHT with the equation that didn't close
    sys2 = build_demo()
    sys2.add_resource(Resource("mode:code_compliant", "information", 1))
    ok, why = sys2.run_process(sys2.processes["import_fill_bad"])
    print("\n[2] import_fill_bad (5000 kg from nothing):")
    print(f"    {'REJECTED' if not ok else 'ran'} -- {why}")

    # 3) the honest, sourced import passes; diesel + labor become visible waste
    sys3 = build_demo()
    sys3.add_resource(Resource("mode:code_compliant", "information", 1))
    sys3.add_resource(Resource("offsite_reserve", "matter", 5000, "kg"))
    sys3.add_resource(Resource("diesel", "energy", 3000, "J"))
    ok, why = sys3.run_process(sys3.processes["import_fill_sourced"])
    wh = sys3.resources.get("waste_heat", Resource("w", "energy", 0)).amount
    print("\n[3] import_fill_sourced (5000 kg drawn from reserve):")
    print(f"    {'VALID' if ok else 'rejected'} -- transport waste = {wh:g} J")

    print("\n" + "=" * 62)
    print("orderer -> referee: matter/energy cannot exceed inputs + stocks.")
    print("=" * 62)
