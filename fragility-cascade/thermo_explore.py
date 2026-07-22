#!/usr/bin/env python3
"""
thermo_explore.py -- AI-facing exploration surface over the thermo_pm referee.
CC0 / Public Domain.  stdlib-only.

The playground an AI plays against: propose a plan (a dependency tree,
flattened to an execution order), get a structured verdict grounded in
physical ground truth, then query the graph to adapt.

This layer knows ONLY physics. It ignores mode-gated processes entirely
(those belong to the institutional layer / EcoSimulator, which sits on top).
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
import copy

from thermo_pm import System, Resource, Process, EPS


# =============================================================================
# Structured verdict -- an AI branches on this, not on a string
# =============================================================================
@dataclass
class Verdict:
    ok: bool
    reached_goal: bool
    step: int                       # index that failed, -1 if none
    process: str                    # process that failed, "" if none
    law: str                        # presence | skill | energy | matter | ""
    detail: str                     # the equation / missing set that didn't close
    unmet: Dict[str, float] = field(default_factory=dict)   # for presence fails
    state: Dict[str, float] = field(default_factory=dict)   # amounts after valid prefix


# =============================================================================
# Playground
# =============================================================================
class Playground:
    def __init__(self, system: System, goals: Dict[str, float]):
        self.system = system
        self.goals = goals

    # ---- physical processes only: institutional gates are not ground truth ---
    def _physical(self) -> List[Process]:
        return [p for p in self.system.processes.values()
                if not any(k.startswith("mode:") for k in p.inputs)]

    def _goal_met(self, s: System) -> bool:
        return all(s.resources.get(g, Resource(g, "matter", 0)).amount >= a - EPS
                   for g, a in self.goals.items())

    # ---- the referee, made actionable -------------------------------------
    def propose(self, plan: List[str]) -> Verdict:
        s = copy.deepcopy(self.system)
        for i, pname in enumerate(plan):
            if pname not in s.processes:
                return Verdict(False, False, i, pname, "undefined",
                               f"no process named '{pname}'")
            proc = s.processes[pname]

            # classify the failure BEFORE mutating, so the AI gets a clean reason
            if proc.skill_required and s._match(proc.skill_required) is None:
                return Verdict(False, False, i, pname, "skill",
                               f"needs skill '{proc.skill_required}'",
                               state=self._amounts(s))
            if not s.has_enough(proc.inputs):
                unmet = {k: a for k, a in proc.inputs.items()
                         if s._match(k) is None or s._match(k).amount < a - EPS}
                return Verdict(False, False, i, pname, "presence",
                               f"missing {unmet}", unmet=unmet,
                               state=self._amounts(s))
            for t in ("energy", "matter"):
                e_in, e_out = s._typed_in(proc, t), s._typed_out(proc, t)
                if e_out > e_in + EPS:
                    return Verdict(False, False, i, pname, t,
                                   f"{t}: out {e_out:g} > in {e_in:g} "
                                   f"-- unsourced. declare a draw or a stock.",
                                   state=self._amounts(s))

            ok, why = s.run_process(proc)
            if not ok:  # belt-and-suspenders; classifier above should catch it
                return Verdict(False, False, i, pname, "run", why,
                               state=self._amounts(s))

        return Verdict(True, self._goal_met(s), -1, "", "",
                       "all steps closed" if self._goal_met(s)
                       else "valid but goal not yet reached",
                       state=self._amounts(s))

    # ---- graph queries the AI uses to build/repair the tree ---------------
    def producers(self, resource: str) -> List[str]:
        """Processes whose outputs or byproducts yield `resource`."""
        base = resource.partition(":")[0]
        out = []
        for p in self._physical():
            names = set(p.outputs) | set(p.byproducts)
            if resource in names or base in {n.partition(":")[0] for n in names}:
                out.append(p.name)
        return out

    def frontier(self, plan: Optional[List[str]] = None) -> List[str]:
        """Processes that CAN fire given the state after `plan` (default: start)."""
        s = copy.deepcopy(self.system)
        for pname in (plan or []):
            if pname in s.processes:
                s.run_process(s.processes[pname])
        fire = []
        for p in self._physical():
            if (p.skill_required is None or s._match(p.skill_required)) \
               and s.has_enough(p.inputs):
                fire.append(p.name)
        return fire

    def solve(self, max_steps: int = 25) -> Optional[List[str]]:
        """Reference auto-explorer (BFS) -- a floor, not the point.
        The AI is meant to drive via propose/producers/frontier."""
        from collections import deque
        start = copy.deepcopy(self.system)
        phys = self._physical()

        def h(s):  # state signature
            return ",".join(f"{r}={s.resources[r].amount:.2f}"
                            for r in sorted(s.resources))

        q, seen = deque([(start, [])]), set()
        while q:
            cur, plan = q.popleft()
            if self._goal_met(cur):
                return plan
            if len(plan) >= max_steps or h(cur) in seen:
                continue
            seen.add(h(cur))
            for p in phys:
                nxt = copy.deepcopy(cur)
                ok, _ = nxt.run_process(p)
                if ok:
                    q.append((nxt, plan + [p.name]))
        return None

    @staticmethod
    def _amounts(s: System) -> Dict[str, float]:
        return {n: round(r.amount, 3) for n, r in s.resources.items()}


# =============================================================================
# Demo -- the falsification loop, first principles, grounded
# =============================================================================
if __name__ == "__main__":
    from thermo_pm import build_demo

    pg = Playground(build_demo(), goals={"wall": 1})
    print("=" * 62)
    print("PLAYGROUND -- AI proposes, reality referees")
    print("=" * 62)

    # naive AI: reach the goal in one leap
    v = pg.propose(["form_wall"])
    print("\n[propose] form_wall")
    print(f"   {'OK' if v.ok else 'FALSIFIED'} @step{v.step} "
          f"({v.law}): {v.detail}")

    # AI backward-chains from the unmet inputs
    print("\n[query] what the AI asks next:")
    for r in ("mechanical_work", "steam_heat", "biomass"):
        print(f"   producers({r}) = {pg.producers(r)}")
    print(f"   frontier(start) = {pg.frontier()}")

    # AI reassembles a first-principles order and re-proposes
    plan = ["gather_biomass", "burn_biomass", "make_boiler",
            "run_engine", "form_wall"]
    v = pg.propose(plan)
    print("\n[propose] " + " -> ".join(plan))
    print(f"   {'VALID, goal reached' if (v.ok and v.reached_goal) else v.detail}")
    print(f"   waste_heat = {v.state.get('waste_heat', 0):g} J  (computed)")

    # reference floor: the tool can also find one itself
    print("\n[solve] BFS floor:", " -> ".join(pg.solve() or ["<none>"]))
    print("=" * 62)
