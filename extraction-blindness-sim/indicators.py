"""Decay-velocity leading indicators.

The yield signal is a *lagging* indicator: by the time output falls, the
substrate is already past its tipping point. These indicators are
selected for one property — they move while output is still nominal.

Each indicator answers "how fast is the foundation thinning?" rather
than "how much are we getting?". An indicator fires when its value
crosses `threshold` in `direction`, sustained for `persistence` steps
(so a single noisy sample does not trip it).

Two domain sets are provided, with values from the source specification:

**Fishery**
  mean trophic level · juvenile-to-adult catch ratio ·
  benthic recovery lag · replenishment deficit

**Soil**
  fungal-to-bacterial ratio velocity · humic recalcitrance shift ·
  subsoil compaction hysteresis · metabolic quotient qCO2

Stdlib only.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional

__all__ = ["Indicator", "IndicatorPanel", "fishery_panel", "soil_panel"]


@dataclass
class Indicator:
    """One leading indicator with a firing rule.

    Parameters
    ----------
    name:
        Identifier used in reports.
    extract:
        Callable mapping the true-state dict to this indicator's value.
    threshold:
        Firing level.
    direction:
        ``"below"`` fires when value < threshold; ``"above"`` fires when
        value > threshold.
    persistence:
        Consecutive steps the condition must hold before the indicator
        reports fired. Guards against single-sample noise.
    measures:
        Short statement of what physical quantity this stands in for.
    """

    name: str
    extract: Callable[[Dict[str, float]], float]
    threshold: float
    direction: str = "below"
    persistence: int = 2
    measures: str = ""

    _streak: int = field(default=0, init=False, repr=False)
    _fired_at: Optional[int] = field(default=None, init=False, repr=False)
    history: List[float] = field(default_factory=list, init=False, repr=False)

    def __post_init__(self) -> None:
        if self.direction not in ("below", "above"):
            raise ValueError("direction must be 'below' or 'above'")
        if self.persistence < 1:
            raise ValueError("persistence must be >= 1")

    def update(self, true_state: Dict[str, float], step: int) -> bool:
        """Feed one step. Returns True while the indicator is fired."""
        value = self.extract(true_state)
        self.history.append(value)

        breaching = value < self.threshold if self.direction == "below" else value > self.threshold
        self._streak = self._streak + 1 if breaching else 0

        if self._streak >= self.persistence and self._fired_at is None:
            self._fired_at = step
        return self.fired

    @property
    def fired(self) -> bool:
        return self._fired_at is not None

    @property
    def fired_at(self) -> Optional[int]:
        """First step at which this indicator fired, or None."""
        return self._fired_at

    def reset(self) -> None:
        self._streak = 0
        self._fired_at = None
        self.history.clear()


@dataclass
class IndicatorPanel:
    """A set of indicators evaluated together."""

    indicators: List[Indicator]

    def update(self, true_state: Dict[str, float], step: int) -> List[str]:
        """Feed one step. Returns names of indicators fired so far."""
        for ind in self.indicators:
            ind.update(true_state, step)
        return [i.name for i in self.indicators if i.fired]

    @property
    def first_fire_step(self) -> Optional[int]:
        """Earliest step at which any indicator fired."""
        steps = [i.fired_at for i in self.indicators if i.fired_at is not None]
        return min(steps) if steps else None

    def report(self) -> List[dict]:
        return [
            {
                "name": i.name,
                "fired": i.fired,
                "fired_at": i.fired_at,
                "threshold": i.threshold,
                "direction": i.direction,
                "latest": i.history[-1] if i.history else None,
                "measures": i.measures,
            }
            for i in self.indicators
        ]

    def reset(self) -> None:
        for i in self.indicators:
            i.reset()


# ---------------------------------------------------------------------
# Domain panels
# ---------------------------------------------------------------------

def fishery_panel() -> IndicatorPanel:
    """Leading indicators for a harvested fish stock.

    Thresholds are the source specification's stated trigger levels.
    The load-bearing one is `replenishment_deficit`: positive means the
    principal is being liquidated, and it goes positive long before
    biomass shows a statistically significant drop.
    """
    return IndicatorPanel(
        [
            Indicator(
                name="replenishment_deficit",
                extract=lambda s: s["replenishment_deficit"],
                threshold=0.0,
                direction="above",
                persistence=2,  # "two consecutive quarters"
                measures="(catch - recruitment) / recruitment; >0 liquidates principal",
            ),
            Indicator(
                name="mean_trophic_level",
                extract=lambda s: s["mean_trophic_level"],
                threshold=-0.10,
                direction="below",
                persistence=2,
                measures="decline per decade; fishing down the food web",
            ),
            Indicator(
                name="juvenile_adult_ratio",
                extract=lambda s: s["juvenile_adult_ratio"],
                threshold=0.55,
                direction="above",
                persistence=2,
                measures="recruitment failure before spawning biomass drops",
            ),
            Indicator(
                name="benthic_recovery_lag",
                extract=lambda s: s["benthic_recovery_lag"],
                threshold=10.0,
                direction="above",
                persistence=2,
                measures="years for trawled seabed to regain complexity",
            ),
        ]
    )


def soil_panel() -> IndicatorPanel:
    """Leading indicators for an agricultural soil.

    Thresholds from the source specification. `fb_ratio` at 0.3 is also
    a hard boundary (see boundaries.py) — it appears in both layers
    deliberately: the indicator gives lead time, the boundary is the
    non-negotiable floor.
    """
    return IndicatorPanel(
        [
            Indicator(
                name="fb_ratio",
                extract=lambda s: s["fb_ratio"],
                threshold=0.45,
                direction="below",
                persistence=2,
                measures="fungal:bacterial; mycorrhizal network disruption",
            ),
            Indicator(
                name="humic_recalcitrance",
                extract=lambda s: s["humic_recalcitrance"],
                threshold=0.60,
                direction="below",
                persistence=2,
                measures="humic:fulvic; burning structural carbon for nutrient supply",
            ),
            Indicator(
                name="compaction_hysteresis",
                extract=lambda s: s["compaction_hysteresis"],
                threshold=0.25,
                direction="above",
                persistence=2,
                measures="surface moisture vs deep drainage divergence; hardpan forming",
            ),
            Indicator(
                name="qco2",
                extract=lambda s: s["qco2"],
                threshold=1.5,
                direction="above",
                persistence=2,
                measures="CO2 per unit microbial biomass; stress dissipation not humification",
            ),
        ]
    )


def _self_test() -> None:
    # Fires only after persistence is satisfied.
    ind = Indicator(name="t", extract=lambda s: s["v"], threshold=0.5,
                    direction="below", persistence=2)
    assert not ind.update({"v": 0.4}, 0), "one breach is not enough at persistence=2"
    assert ind.update({"v": 0.4}, 1), "two consecutive breaches fire"
    assert ind.fired_at == 1

    # Once fired, stays fired (the record of the crossing is kept).
    assert ind.update({"v": 0.9}, 2)
    assert ind.fired_at == 1

    # A broken streak resets before firing.
    ind2 = Indicator(name="t2", extract=lambda s: s["v"], threshold=0.5,
                     direction="below", persistence=3)
    for i, v in enumerate([0.4, 0.4, 0.9, 0.4, 0.4]):
        ind2.update({"v": v}, i)
    assert not ind2.fired, "interrupted streak must not fire"
    ind2.update({"v": 0.4}, 5)
    assert ind2.fired and ind2.fired_at == 5

    # Direction 'above'.
    ind3 = Indicator(name="t3", extract=lambda s: s["v"], threshold=0.0,
                     direction="above", persistence=1)
    assert not ind3.update({"v": -0.1}, 0)
    assert ind3.update({"v": 0.1}, 1)

    try:
        Indicator(name="bad", extract=lambda s: 0.0, threshold=0.0, direction="sideways")
        raise AssertionError("bad direction should raise")
    except ValueError:
        pass

    # Panel reports the earliest fire across members.
    panel = IndicatorPanel(
        [
            Indicator(name="slow", extract=lambda s: s["a"], threshold=0.5,
                      direction="below", persistence=1),
            Indicator(name="fast", extract=lambda s: s["b"], threshold=0.5,
                      direction="below", persistence=1),
        ]
    )
    panel.update({"a": 0.9, "b": 0.9}, 0)
    panel.update({"a": 0.9, "b": 0.1}, 1)  # 'fast' fires
    panel.update({"a": 0.1, "b": 0.1}, 2)  # 'slow' fires
    assert panel.first_fire_step == 1
    names = {r["name"]: r["fired_at"] for r in panel.report()}
    assert names == {"fast": 1, "slow": 2}

    panel.reset()
    assert panel.first_fire_step is None

    # Domain panels are well-formed and their extractors run.
    fp = fishery_panel()
    fp.update(
        {
            "replenishment_deficit": -0.1,
            "mean_trophic_level": 0.0,
            "juvenile_adult_ratio": 0.3,
            "benthic_recovery_lag": 1.0,
        },
        0,
    )
    assert len(fp.report()) == 4 and fp.first_fire_step is None

    sp = soil_panel()
    sp.update(
        {"fb_ratio": 0.8, "humic_recalcitrance": 0.9,
         "compaction_hysteresis": 0.0, "qco2": 0.8},
        0,
    )
    assert len(sp.report()) == 4 and sp.first_fire_step is None

    print("indicators.py self-test OK")


if __name__ == "__main__":
    _self_test()
