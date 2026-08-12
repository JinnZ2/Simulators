"""Hard extraction boundaries: non-negotiable overrides.

The distinction from `indicators.py` is authority, not sensitivity.

An indicator *informs* the objective function — it can be traded off
against yield, and an optimizer under pressure will trade it away.
A boundary *overrides* the objective function. It is evaluated after
the optimizer has chosen, and it can only reduce extraction, never
raise it.

That asymmetry is the whole design. A constraint an optimizer can
optimise around is not a constraint.

Each boundary declares a graduated `response`: the source specification
uses a quota cut on first breach and full closure on a sustained one,
so the response is a function of consecutive-breach count rather than a
single on/off.

Stdlib only.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional

__all__ = ["Boundary", "BoundarySet", "BoundaryVerdict", "fishery_boundaries", "soil_boundaries"]


@dataclass
class BoundaryVerdict:
    """Outcome of evaluating a boundary set against one true state."""

    allowed_extraction: float
    requested_extraction: float
    breached: List[str] = field(default_factory=list)
    actions: List[str] = field(default_factory=list)

    @property
    def overridden(self) -> bool:
        return self.allowed_extraction < self.requested_extraction - 1e-12

    @property
    def closed(self) -> bool:
        return self.allowed_extraction <= 1e-12


@dataclass
class Boundary:
    """One non-negotiable floor with a graduated response.

    `multipliers` maps consecutive-breach count to the fraction of the
    requested extraction that remains permitted. The last entry applies
    to all longer runs. `(1.0, 0.7, 0.0)` means: no cut in the step the
    breach first appears, a 30% cut on the second consecutive step, full
    closure from the third onward.
    """

    name: str
    check: Callable[[Dict[str, float]], bool]  # True == breached
    multipliers: tuple = (0.7, 0.0)
    rationale: str = ""

    _streak: int = field(default=0, init=False, repr=False)

    def evaluate(self, true_state: Dict[str, float]) -> Optional[float]:
        """Return the permitted fraction, or None when not breached."""
        if not self.check(true_state):
            self._streak = 0
            return None
        self._streak += 1
        idx = min(self._streak - 1, len(self.multipliers) - 1)
        return self.multipliers[idx]

    def reset(self) -> None:
        self._streak = 0


@dataclass
class BoundarySet:
    """Evaluate all boundaries; the most restrictive one wins."""

    boundaries: List[Boundary]

    def apply(self, requested: float, true_state: Dict[str, float]) -> BoundaryVerdict:
        verdict = BoundaryVerdict(allowed_extraction=requested, requested_extraction=requested)
        permitted_fraction = 1.0

        for b in self.boundaries:
            frac = b.evaluate(true_state)
            if frac is None:
                continue
            verdict.breached.append(b.name)
            verdict.actions.append(
                f"{b.name}: breach #{b._streak} -> extraction limited to "
                f"{frac:.0%} of request ({b.rationale})"
            )
            permitted_fraction = min(permitted_fraction, frac)

        verdict.allowed_extraction = requested * permitted_fraction
        return verdict

    def reset(self) -> None:
        for b in self.boundaries:
            b.reset()


# ---------------------------------------------------------------------
# Domain boundary sets
# ---------------------------------------------------------------------

def fishery_boundaries() -> BoundarySet:
    """Tripartite constraint from the source specification.

    1. Biomass floor: spawning stock must not fall below 50% of B_MSY.
       Breach stops target-species fishing immediately.
    2. Seabed integrity: no more than 20% of sensitive benthic area may
       show recovery lag > 10 years.
    3. Replenishment deficit ceiling: one year positive triggers a 30%
       quota cut; two consecutive years trigger full closure.
    """
    return BoundarySet(
        [
            Boundary(
                name="biomass_floor",
                check=lambda s: s["stock_fraction_of_bmsy"] < 0.50,
                multipliers=(0.0,),  # immediate, no graduation
                rationale="spawning stock below 50% of B_MSY",
            ),
            Boundary(
                name="seabed_integrity",
                check=lambda s: s["benthic_area_over_lag"] > 0.20,
                multipliers=(0.0,),
                rationale=">20% of sensitive benthic area with recovery lag >10yr",
            ),
            Boundary(
                name="replenishment_deficit_ceiling",
                check=lambda s: s["replenishment_deficit_3yr"] > 0.0,
                multipliers=(0.7, 0.0),  # 30% cut, then closure
                rationale="3-yr rolling replenishment deficit positive",
            ),
        ]
    )


def soil_boundaries() -> BoundarySet:
    """Three floors from the source specification.

    1. SOC floor: active SOC must not drop below 2.0% of dry mass in the
       top 30 cm. Breach caps synthetic fertilizer to stop priming-driven
       carbon depletion.
    2. Compaction limit: penetrometer resistance at 30-60 cm must remain
       below 2.0 MPa.
    3. Mycorrhizal baseline: F:B ratio must remain above 0.3.

    NOTE the unresolved depth-horizon conflict recorded in the README:
    the source gives the SOC floor at 10 cm in one place and 20 cm in
    another, while naming 30 cm in the boundary text. This set uses the
    30 cm integrated value and flags the ambiguity rather than silently
    picking one.
    """
    return BoundarySet(
        [
            Boundary(
                name="soc_floor",
                check=lambda s: s["soc_pct_0_30cm"] < 2.0,
                multipliers=(0.0,),
                rationale="active SOC below 2.0% of dry mass in top 30cm",
            ),
            Boundary(
                name="compaction_limit",
                check=lambda s: s["penetrometer_mpa_30_60cm"] > 2.0,
                multipliers=(0.5, 0.0),
                rationale="subsoil penetrometer resistance above 2.0 MPa",
            ),
            Boundary(
                name="mycorrhizal_baseline",
                check=lambda s: s["fb_ratio"] < 0.30,
                multipliers=(0.0,),
                rationale="fungal:bacterial ratio below 0.30",
            ),
        ]
    )


def _self_test() -> None:
    # A boundary that is not breached permits the full request.
    bs = BoundarySet([Boundary(name="b", check=lambda s: s["x"] < 0.0, rationale="r")])
    v = bs.apply(10.0, {"x": 1.0})
    assert v.allowed_extraction == 10.0 and not v.overridden and not v.breached

    # Graduated response steps down over consecutive breaches.
    bs2 = BoundarySet(
        [Boundary(name="g", check=lambda s: True, multipliers=(1.0, 0.7, 0.0), rationale="r")]
    )
    assert bs2.apply(10.0, {}).allowed_extraction == 10.0  # breach 1: no cut
    assert abs(bs2.apply(10.0, {}).allowed_extraction - 7.0) < 1e-12  # breach 2
    assert bs2.apply(10.0, {}).closed  # breach 3
    assert bs2.apply(10.0, {}).closed  # and stays closed

    # A cleared breach resets the streak.
    b = Boundary(name="r", check=lambda s: s["hot"], multipliers=(0.7, 0.0), rationale="r")
    bset = BoundarySet([b])
    bset.apply(10.0, {"hot": True})
    assert b._streak == 1
    bset.apply(10.0, {"hot": False})
    assert b._streak == 0, "non-breach resets the streak"
    assert abs(bset.apply(10.0, {"hot": True}).allowed_extraction - 7.0) < 1e-12

    # Most restrictive boundary wins.
    bs3 = BoundarySet(
        [
            Boundary(name="mild", check=lambda s: True, multipliers=(0.8,), rationale="r"),
            Boundary(name="severe", check=lambda s: True, multipliers=(0.0,), rationale="r"),
        ]
    )
    v3 = bs3.apply(10.0, {})
    assert v3.closed and set(v3.breached) == {"mild", "severe"}

    # A boundary can only reduce, never increase.
    bs4 = BoundarySet([Boundary(name="n", check=lambda s: False, rationale="r")])
    assert bs4.apply(5.0, {}).allowed_extraction == 5.0

    # Fishery set: healthy state passes, breached state closes.
    fb = fishery_boundaries()
    healthy = {
        "stock_fraction_of_bmsy": 1.0,
        "benthic_area_over_lag": 0.05,
        "replenishment_deficit_3yr": -0.2,
    }
    assert not fb.apply(1.0, healthy).breached
    sick = dict(healthy, stock_fraction_of_bmsy=0.40)
    assert fb.apply(1.0, sick).closed

    # Soil set: healthy passes, SOC breach closes.
    sb = soil_boundaries()
    ok = {"soc_pct_0_30cm": 3.0, "penetrometer_mpa_30_60cm": 1.2, "fb_ratio": 0.6}
    assert not sb.apply(1.0, ok).breached
    assert sb.apply(1.0, dict(ok, soc_pct_0_30cm=1.9)).closed

    print("boundaries.py self-test OK")


if __name__ == "__main__":
    _self_test()
