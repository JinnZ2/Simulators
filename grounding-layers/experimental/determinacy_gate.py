# determinacy_gate.py
# CC0 | stdlib-only | phone-buildable
# grounding-layers :: Le determinacy gate
#
# AXIS
#   not acuity (louder channel), not capacity (extra channel).
#   INSTANTANEOUS FUSED CHANNEL COUNT: how many independent streams
#   intersect at the moment the verdict fires. a determinacy axis.
#
# CORE
#   each live channel -> constraint region R_i over the hypothesis space.
#   fused verdict = intersection of all R_i.
#   fire ONLY when the intersection collapses toward a point.
#   confidence := determinacy of the intersection,  NOT fluency of the text.
#
# ENERGY FLOW
#   hypotheses (state space)
#        |
#   channel_i -> permits R_i  -- recruit independent, informative channels
#        |                        redundant channel shrinks nothing
#        v
#   intersection R_i  -- region while under-constrained
#        |                  point when determined
#        v
#   DETERMINACY GATE
#        - point                : fire verdict (full)
#        - region, N < N_crit   : BLOCK  (recruit more, or flag)
#        - channels exhausted   : fire with underdetermination flag
#                                 (honest partial, like taste-gated soil)
#
# FAILURE MODE THIS BRAKES
#   fluent low-N closure = floating head. coherence != determinacy.
#   text reads confident whether the intersection is a point or the
#   whole space. binding confidence to |intersection| re-anchors the
#   verdict to constraint mass.

from dataclasses import dataclass, field
from typing import Callable, Optional


# ---------------------------------------------------------------- channel
@dataclass
class Constraint:
    name: str
    permits: frozenset          # subset of hypothesis space this read allows
    independent_of: frozenset = frozenset()   # names it shares information with
    note: str = ""

    def informative_over(self, current: frozenset) -> bool:
        # shrinks the live intersection at all?
        return bool(current) and not current.issubset(self.permits)


# ---------------------------------------------------------------- gate
@dataclass
class DeterminacyGate:
    hypotheses: frozenset                  # full state space S
    live: list = field(default_factory=list)   # recruited Constraints
    _indep_cache: set = field(default_factory=set)

    # --- recruit --------------------------------------------------------
    def recruit(self, c: Constraint):
        self.live.append(c)
        return self

    # --- fused intersection --------------------------------------------
    def intersection(self) -> frozenset:
        acc = self.hypotheses
        for c in self.live:
            acc = acc & c.permits
        return acc

    # --- count only INDEPENDENT + INFORMATIVE channels ------------------
    def n_independent(self) -> int:
        seen_groups = []
        acc = self.hypotheses
        n = 0
        for c in self.live:
            # skip if fully redundant with an already-counted channel
            grp = c.independent_of | {c.name}
            if any(grp & g for g in seen_groups):
                continue
            if not c.informative_over(acc) and acc != self.hypotheses:
                continue
            acc = acc & c.permits
            seen_groups.append(grp)
            n += 1
        return n

    # --- determinacy: 1.0 = point, 0.0 = nothing pinned -----------------
    def determinacy(self) -> float:
        s, i = len(self.hypotheses), len(self.intersection())
        if s == 0:
            return 0.0
        if i == 0:                          # over-constrained: contradiction
            return -1.0                     # channels DISAGREE -> defect flag
        # 1 hypothesis left = 1.0 ; all left = 0.0
        return round((s - i) / (s - 1), 3) if s > 1 else 1.0

    # --- the gate -------------------------------------------------------
    def verdict(self, n_crit: int = 3, exhausted: bool = False) -> dict:
        inter = self.intersection()
        d = self.determinacy()
        n = self.n_independent()

        if d < 0:
            return {"fire": False, "state": "CONTRADICTION",
                    "action": "channels disagree -> audit read or model",
                    "intersection": tuple(sorted(inter)),
                    "n_independent": n, "determinacy": d}

        if len(inter) == 1:
            return {"fire": True, "state": "DETERMINED",
                    "verdict": next(iter(inter)),
                    "confidence": d, "n_independent": n,
                    "flag": None}

        if n < n_crit and not exhausted:
            return {"fire": False, "state": "UNDERDETERMINED",
                    "action": f"recruit more: N={n} < N_crit={n_crit}",
                    "candidates": tuple(sorted(inter)),
                    "confidence": d, "n_independent": n}

        # exhausted or N met but intersection still a region -> honest partial
        return {"fire": True, "state": "PARTIAL",
                "candidates": tuple(sorted(inter)),
                "confidence": d, "n_independent": n,
                "flag": "UNDERDETERMINED: intersection is a region, not a point"}


# ================================================================ demo
if __name__ == "__main__":

    # hypothesis space: front-end fault sources
    S = frozenset({"L_bearing", "R_bearing", "L_tierod", "R_tierod",
                   "L_brake", "R_brake", "groove_resonance"})

    g = DeterminacyGate(S)

    # recruit the US-54 channels one at a time; watch the intersection collapse
    g.recruit(Constraint("pitch_present",
              permits=frozenset({"L_bearing","R_bearing","L_tierod","R_tierod",
                                 "L_brake","R_brake","groove_resonance"})))
    print("after pitch        :", g.verdict())

    g.recruit(Constraint("speed_dependent",
              permits=frozenset({"L_bearing","R_bearing","L_tierod","R_tierod",
                                 "L_brake","R_brake"}),   # drops groove
              note="tracks rpm not groove period"))
    print("after speed        :", g.verdict())

    g.recruit(Constraint("persists_across_surface",
              permits=frozenset({"L_bearing","R_bearing","L_tierod","R_tierod",
                                 "L_brake","R_brake"}),
              note="rules out road-coupled"))
    print("after surface      :", g.verdict())

    g.recruit(Constraint("right_side_only",
              permits=frozenset({"R_bearing","R_tierod","R_brake"})))
    print("after side         :", g.verdict())

    g.recruit(Constraint("steering_pull_into_column",
              permits=frozenset({"R_tierod"}),            # drops bearing/brake
              note="feedback path signature"))
    print("after steering     :", g.verdict())

    g.recruit(Constraint("damping_asym_LR",
              permits=frozenset({"R_tierod"}),
              note="locks it"))
    print("after damping      :", g.verdict())

    # ---- contrast: the Kalman foil ran only 2 channels ----------------
    foil = DeterminacyGate(S)
    foil.recruit(Constraint("pitch_present", permits=S))
    foil.recruit(Constraint("vibration_amplitude",
                 permits=frozenset({"R_bearing","R_tierod","R_brake",
                                    "groove_resonance"})))
    print("\nFOIL (2 chan)      :", foil.verdict())
    print("  -> region, not point. locates SYMPTOM zone, cannot fire source.")
