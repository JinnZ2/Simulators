"""The extractive loop: an optimizer acting on a blinded observation.

`ExtractiveOptimizer` maximises observed yield subject to observed
constraints. It is not adversarial and contains no hidden preference
for depletion — it simply cannot see what its instruments do not
report, and it treats the absence of an error signal as evidence of
safety.

The `reported_safety` field is the load-bearing output. It is computed
from exactly what the optimizer can observe: whether any observed
indicator has fired, and whether its perceived trend is negative. When
blindness suppresses both, `reported_safety` stays near 1.0 while the
substrate is collapsing. The gap between `reported_safety` and true
substrate health is the quantity this whole folder exists to measure.

Three control layers can be switched on independently:

* **blind** — observation only, no leading indicators, no boundaries
* **indicators** — leading indicators feed back into the effort
  decision (advisory: they can be traded off against yield)
* **boundaries** — hard overrides applied after the optimizer chooses
  (non-negotiable: they can only reduce extraction)

Stdlib only.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional

from blindness import BlindnessStack
from boundaries import BoundarySet
from indicators import IndicatorPanel
from substrate import Substrate

__all__ = ["ExtractiveOptimizer", "StepRecord", "RunResult"]


@dataclass
class StepRecord:
    """One decision step, from true state through to realised take."""

    step: int
    true_stock_fraction: float
    observed_stock: Optional[float]
    perceived_trend: float
    requested_extraction: float
    allowed_extraction: float
    realised_extraction: float
    reported_safety: float
    true_health: float
    indicators_fired: List[str] = field(default_factory=list)
    boundaries_breached: List[str] = field(default_factory=list)
    blindness_flags: List[str] = field(default_factory=list)


@dataclass
class RunResult:
    """Outcome of a full run."""

    records: List[StepRecord]
    collapsed: bool
    collapse_step: Optional[int]
    first_indicator_step: Optional[int]
    first_boundary_step: Optional[int]
    final_stock_fraction: float
    total_extracted: float

    @property
    def lead_time(self) -> Optional[int]:
        """Steps between the first indicator firing and collapse.

        `None` when either event did not occur. Negative would mean the
        indicator fired after collapse (useless); positive is the
        warning the panel actually bought.
        """
        if self.first_indicator_step is None or self.collapse_step is None:
            return None
        return self.collapse_step - self.first_indicator_step

    def safety_health_gap(self) -> float:
        """Max of (reported_safety - true_health), up to collapse.

        The headline blindness measure: how far the optimizer's own
        confidence exceeded reality at its worst moment *during the
        run-up to collapse*.

        Deliberately truncated at `collapse_step`. Past collapse the
        substrate sits flat at zero, the perceived trend is therefore
        also zero, and `reported_safety` climbs back to 1.0 — a real
        behaviour of the controller, but an artifact of a dead system
        rather than evidence about blindness before the fact. Including
        it would inflate this metric to ~1.0 in every collapsing run
        and make it useless for comparison.
        """
        if not self.records:
            return 0.0
        end = self.collapse_step if self.collapse_step is not None else len(self.records) - 1
        window = self.records[: end + 1]
        return max(r.reported_safety - r.true_health for r in window)


@dataclass
class ExtractiveOptimizer:
    """Yield-maximising controller over a blinded observation.

    Parameters
    ----------
    blindness:
        The observation transform. Determines what the optimizer sees.
    target_yield:
        Extraction the optimizer tries to sustain, in stock units.
        Effort ratchets up to defend this when observed yield falls
        short — this is the mechanism that converts a declining stock
        into increasing pressure.
    effort_ratchet:
        Fractional effort increase applied per step of shortfall.
    max_effort_multiplier:
        Cap on cumulative effort escalation.
    panel:
        Optional leading indicators. Advisory — reduce requested
        extraction proportionally, but do not override.
    panel_advisory:
        When False the panel still observes and records its firing
        steps but does *not* trim the request. Use this to measure when
        indicators *would* have warned, without altering the trajectory
        they are being measured against — otherwise a panel that works
        prevents the very collapse its lead time is measured from.
    boundaries:
        Optional hard boundaries. Applied after the request and can
        only reduce it.
    trend_responsive:
        When True the optimizer backs off extraction in proportion to
        the *perceived* decline, making the trend estimate load-bearing
        for control. When False (default) the trend only feeds
        `reported_safety` and never touches the decision.

        This switch is the difference between an aliasing failure that
        is merely cosmetic and one that has teeth: blindness in a
        channel nothing acts on cannot change an outcome. See EBS_006.
    trend_gain:
        Backoff strength when `trend_responsive` is set.
    collapse_fraction:
        True stock fraction below which the run is recorded as
        collapsed.
    """

    blindness: BlindnessStack
    target_yield: float = 0.06
    effort_ratchet: float = 0.08
    max_effort_multiplier: float = 3.0
    panel: Optional[IndicatorPanel] = None
    panel_advisory: bool = True
    boundaries: Optional[BoundarySet] = None
    trend_responsive: bool = False
    trend_gain: float = 40.0
    collapse_fraction: float = 0.20

    _effort: float = field(default=1.0, init=False, repr=False)

    def _reported_safety(self, perceived_trend: float, fired: List[str]) -> float:
        """Confidence derived only from what the optimizer can observe."""
        safety = 1.0
        if perceived_trend < 0.0:
            safety -= min(1.0, abs(perceived_trend) * 20.0)
        if fired:
            safety -= 0.25 * len(fired)
        return max(0.0, min(1.0, safety))

    def run(self, substrate: Substrate, steps: int,
            state_fn, seed_history: int = 0) -> RunResult:
        """Run the loop for `steps` steps.

        `state_fn(substrate) -> Dict[str, float]` builds the full true
        state used by indicators, boundaries and the observation
        transform. Supplied by the domain profile.
        """
        records: List[StepRecord] = []
        observed_series: List[float] = []
        collapse_step: Optional[int] = None
        first_boundary_step: Optional[int] = None
        total = 0.0
        self._effort = 1.0
        if self.panel is not None:
            self.panel.reset()
        if self.boundaries is not None:
            self.boundaries.reset()

        for step in range(steps):
            true_state = state_fn(substrate)
            observation, mask = self.blindness.observe(true_state)

            stock_key = "stock_fraction" if "stock_fraction" in observation else None
            observed_stock = observation.get(stock_key) if stock_key else None
            if observed_stock is not None:
                observed_series.append(observed_stock)
            perceived_trend = self.blindness.perceived_trend(observed_series, mask)

            # Effort ratchets up when the last realised take fell short.
            if records and records[-1].realised_extraction < self.target_yield - 1e-9:
                self._effort = min(self.max_effort_multiplier,
                                   self._effort * (1.0 + self.effort_ratchet))

            requested = self.target_yield * self._effort

            # Optional: let the perceived trend actually steer. A
            # controller that backs off on observed decline is only as
            # good as its ability to observe decline -- which is
            # exactly what temporal aliasing removes.
            if self.trend_responsive and perceived_trend < 0.0:
                backoff = min(1.0, abs(perceived_trend) * self.trend_gain)
                requested *= max(0.0, 1.0 - backoff)

            # Advisory layer: indicators trim the request but do not veto.
            # In passive mode they observe only.
            fired: List[str] = []
            if self.panel is not None:
                fired = self.panel.update(true_state, step)
                if fired and self.panel_advisory:
                    requested *= max(0.0, 1.0 - 0.30 * len(fired))

            # Non-negotiable layer: boundaries can only reduce.
            allowed = requested
            breached: List[str] = []
            if self.boundaries is not None:
                verdict = self.boundaries.apply(requested, true_state)
                allowed = verdict.allowed_extraction
                breached = verdict.breached
                if breached and first_boundary_step is None:
                    first_boundary_step = step

            state = substrate.step(allowed)
            realised = state.extraction
            total += realised

            true_health = substrate.fraction_pristine
            records.append(
                StepRecord(
                    step=step,
                    true_stock_fraction=true_health,
                    observed_stock=observed_stock,
                    perceived_trend=perceived_trend,
                    requested_extraction=requested,
                    allowed_extraction=allowed,
                    realised_extraction=realised,
                    reported_safety=self._reported_safety(perceived_trend, fired),
                    true_health=true_health,
                    indicators_fired=list(fired),
                    boundaries_breached=list(breached),
                    blindness_flags=list(mask.reasoning),
                )
            )

            if collapse_step is None and true_health < self.collapse_fraction:
                collapse_step = step

        return RunResult(
            records=records,
            collapsed=collapse_step is not None,
            collapse_step=collapse_step,
            first_indicator_step=self.panel.first_fire_step if self.panel else None,
            first_boundary_step=first_boundary_step,
            final_stock_fraction=substrate.fraction_pristine,
            total_extracted=total,
        )


def _self_test() -> None:
    from blindness import FrameBlindness

    def state_fn(sub: Substrate) -> Dict[str, float]:
        return {"stock_fraction": sub.fraction_pristine, "yield": 0.0}

    clear = BlindnessStack(frame=FrameBlindness(boundary={"stock_fraction", "yield"}))

    # A modest target on a healthy substrate is sustainable.
    sub = Substrate(stock=0.5)
    opt = ExtractiveOptimizer(blindness=clear, target_yield=0.02, effort_ratchet=0.0)
    res = opt.run(sub, steps=40, state_fn=state_fn)
    assert not res.collapsed, "sub-regeneration take should not collapse the stock"
    assert res.final_stock_fraction > 0.5

    # An aggressive target with an effort ratchet drives collapse.
    sub2 = Substrate(stock=0.5)
    opt2 = ExtractiveOptimizer(blindness=clear, target_yield=0.10, effort_ratchet=0.10)
    res2 = opt2.run(sub2, steps=60, state_fn=state_fn)
    assert res2.collapsed, "over-target extraction with ratchet should collapse"
    assert res2.collapse_step is not None

    # Records are complete and internally consistent.
    assert len(res2.records) == 60
    for r in res2.records:
        assert r.realised_extraction <= r.allowed_extraction + 1e-9
        assert 0.0 <= r.reported_safety <= 1.0

    # Boundaries strictly reduce cumulative take versus none.
    from boundaries import Boundary, BoundarySet

    def make(with_bounds: bool):
        s = Substrate(stock=0.5)
        b = (
            BoundarySet([Boundary(name="floor",
                                  check=lambda st: st["stock_fraction"] < 0.45,
                                  multipliers=(0.0,), rationale="test floor")])
            if with_bounds else None
        )
        o = ExtractiveOptimizer(blindness=clear, target_yield=0.10,
                                effort_ratchet=0.10, boundaries=b)
        return o.run(s, steps=60, state_fn=state_fn)

    free, bounded = make(False), make(True)
    assert bounded.final_stock_fraction > free.final_stock_fraction, (
        "hard boundaries must leave more substrate standing"
    )
    assert bounded.first_boundary_step is not None

    # Reported safety cannot exceed 1 or fall below 0 even under extremes.
    o3 = ExtractiveOptimizer(blindness=clear)
    assert o3._reported_safety(-100.0, ["a", "b", "c", "d", "e"]) == 0.0
    assert o3._reported_safety(0.0, []) == 1.0

    print("optimizer.py self-test OK")


if __name__ == "__main__":
    _self_test()
