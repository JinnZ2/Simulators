"""Regenerating substrate with depensation and recovery hysteresis.

The physical layer. A stock that regenerates at a rate depending on its
own level, is drawn down by extraction, and whose per-capita
regeneration collapses non-linearly below a depensation threshold.

Two properties make this substrate able to punish a blind optimizer:

1. **Depensation.** Per-capita regeneration falls as the stock falls,
   so the system does not merely decline linearly toward a new
   equilibrium — the decline accelerates.
2. **Recovery hysteresis.** The path back is not the path down.
   Regeneration after a breach runs at `recovery_fraction` of nominal
   until the stock clears `hysteresis_release`, so the time to recover
   is much longer than the time to deplete.

Stdlib only.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

__all__ = ["Substrate", "SubstrateState"]


@dataclass
class SubstrateState:
    """One time step of substrate history."""

    step: int
    stock: float
    regeneration: float
    extraction: float
    depensation_factor: float
    breached: bool


@dataclass
class Substrate:
    """A stock with depensatory regeneration and recovery hysteresis.

    Parameters
    ----------
    capacity:
        Pristine / unfished carrying capacity K, in stock units.
    intrinsic_rate:
        Intrinsic regeneration rate r, per step.
    depensation_half:
        Stock level (as a fraction of capacity) at which per-capita
        regeneration is reduced to half of its non-depensatory value.
        Below this the reduction steepens quadratically.
    hysteresis_release:
        Stock fraction the system must climb back above before
        regeneration returns to nominal after a depensation breach.
    recovery_fraction:
        Multiplier applied to regeneration while in the post-breach
        hysteretic state. `1.0` disables hysteresis.
    stock:
        Current stock. Defaults to capacity.

    Notes
    -----
    Regeneration is logistic with a depensatory factor::

        R(S) = r * S * (1 - S/K) * S^2 / (S^2 + A^2)

    where ``A = depensation_half * K``. For ``S >> A`` the factor tends
    to 1 and the model reduces to plain logistic growth; for ``S << A``
    it falls off as ``(S/A)^2``.
    """

    capacity: float = 1.0
    intrinsic_rate: float = 0.40
    depensation_half: float = 0.40
    hysteresis_release: float = 0.60
    recovery_fraction: float = 0.35
    stock: float = field(default=None)  # type: ignore[assignment]

    _in_hysteresis: bool = field(default=False, init=False, repr=False)
    history: List[SubstrateState] = field(default_factory=list, init=False, repr=False)

    def __post_init__(self) -> None:
        if self.capacity <= 0:
            raise ValueError("capacity must be positive")
        if self.intrinsic_rate <= 0:
            raise ValueError("intrinsic_rate must be positive")
        if not 0.0 < self.depensation_half < 1.0:
            raise ValueError("depensation_half must be in (0, 1)")
        if not 0.0 < self.recovery_fraction <= 1.0:
            raise ValueError("recovery_fraction must be in (0, 1]")
        if self.stock is None:
            self.stock = self.capacity

    # -- derived reference points -----------------------------------

    @property
    def msy_stock(self) -> float:
        """Stock at maximum sustainable yield (K/2 for logistic)."""
        return self.capacity / 2.0

    @property
    def msy_rate(self) -> float:
        """Extraction rate at MSY (r/2 for logistic)."""
        return self.intrinsic_rate / 2.0

    @property
    def fraction_pristine(self) -> float:
        return self.stock / self.capacity

    def peak_regeneration(self, samples: int = 1000) -> float:
        """True maximum sustainable yield of this substrate.

        Not the textbook ``r*K/4``: depensation drags the achievable
        peak below the plain-logistic value and shifts the stock at
        which it occurs. Any "fraction of MSY" target must be taken
        against *this* number, or it silently becomes a much larger
        overshoot than intended.
        """
        return max(
            self.regeneration(self.capacity * i / samples)
            for i in range(1, samples)
        )

    # -- dynamics ---------------------------------------------------

    def depensation_factor(self, stock: float = None) -> float:
        """Per-capita regeneration multiplier in [0, 1)."""
        s = self.stock if stock is None else stock
        if s <= 0.0:
            return 0.0
        a = self.depensation_half * self.capacity
        return (s * s) / (s * s + a * a)

    def regeneration(self, stock: float = None) -> float:
        """Regeneration this step, before extraction."""
        s = self.stock if stock is None else stock
        if s <= 0.0:
            return 0.0
        logistic = self.intrinsic_rate * s * (1.0 - s / self.capacity)
        gross = max(0.0, logistic) * self.depensation_factor(s)
        if self._in_hysteresis:
            gross *= self.recovery_fraction
        return gross

    def step(self, extraction: float) -> SubstrateState:
        """Advance one step under `extraction` (absolute stock units)."""
        extraction = max(0.0, min(extraction, self.stock))
        regen = self.regeneration()
        self.stock = max(0.0, self.stock + regen - extraction)

        # Hysteresis latch: entering depensation is easy, leaving is not.
        if self.fraction_pristine < self.depensation_half:
            self._in_hysteresis = True
        elif self.fraction_pristine >= self.hysteresis_release:
            self._in_hysteresis = False

        state = SubstrateState(
            step=len(self.history),
            stock=self.stock,
            regeneration=regen,
            extraction=extraction,
            depensation_factor=self.depensation_factor(),
            breached=self._in_hysteresis,
        )
        self.history.append(state)
        return state

    def sustainable_extraction(self) -> float:
        """Extraction exactly matching current regeneration."""
        return self.regeneration()

    def replenishment_deficit(self) -> float:
        """(extraction - regeneration) / regeneration for the last step.

        Positive means principal is being liquidated. Returns 0.0 with no
        history and 1.0 when regeneration has stopped entirely under a
        non-zero take.
        """
        if not self.history:
            return 0.0
        last = self.history[-1]
        if last.regeneration <= 1e-12:
            return 1.0 if last.extraction > 0 else 0.0
        return (last.extraction - last.regeneration) / last.regeneration


def _self_test() -> None:
    # Undisturbed substrate at capacity is at equilibrium (no logistic growth).
    s = Substrate()
    assert abs(s.regeneration()) < 1e-12, "at K, logistic growth is zero"

    # At K/2 an unfished substrate grows.
    s2 = Substrate(stock=0.5)
    assert s2.regeneration() > 0.0

    # Depensation factor is monotone increasing in stock and bounded.
    s3 = Substrate()
    factors = [s3.depensation_factor(x / 100.0) for x in range(1, 101)]
    assert all(0.0 <= f < 1.0 for f in factors)
    assert all(b >= a for a, b in zip(factors, factors[1:])), "monotone"

    # Depensation halves regeneration at the stated threshold.
    s4 = Substrate(depensation_half=0.4)
    assert abs(s4.depensation_factor(0.4) - 0.5) < 1e-9

    # Depensation drags true MSY below the plain-logistic r*K/4.
    s_msy = Substrate(capacity=1.0, intrinsic_rate=0.40)
    peak = s_msy.peak_regeneration()
    assert peak < 0.40 * 1.0 / 4.0, "depensation must lower achievable MSY"
    assert peak > 0.0
    # And a substrate without depensation recovers the textbook value.
    s_nodep = Substrate(capacity=1.0, intrinsic_rate=0.40, depensation_half=1e-6)
    assert abs(s_nodep.peak_regeneration() - 0.10) < 1e-3

    # Extraction above regeneration depletes; deficit goes positive.
    s5 = Substrate(stock=0.5)
    s5.step(extraction=0.5 * s5.stock)
    assert s5.stock < 0.5
    assert s5.replenishment_deficit() > 0.0

    # Extraction below regeneration lets the stock recover toward K.
    s_recover = Substrate(stock=0.5)
    before = s_recover.stock
    s_recover.step(extraction=0.03)  # regen at S=0.5 is ~0.061
    assert s_recover.stock > before, "sub-regeneration take should not deplete"

    # Hysteresis latches on breach and does not release immediately.
    # Extraction must exceed regeneration (~0.061 at S=0.5) to deplete.
    s6 = Substrate(stock=0.5, recovery_fraction=0.35)
    for _ in range(10):
        s6.step(extraction=0.08)
    assert s6._in_hysteresis, "drawdown past depensation should latch"
    assert s6.stock > 0.0, "test needs a surviving stock to be meaningful"
    suppressed = s6.regeneration()
    s6._in_hysteresis = False
    assert s6.regeneration() > suppressed, "hysteresis suppresses regeneration"
    assert abs(suppressed / s6.regeneration() - 0.35) < 1e-9

    # Latch does not release until the stock clears hysteresis_release.
    s8 = Substrate(stock=0.30, recovery_fraction=0.35, hysteresis_release=0.60)
    s8.step(extraction=0.0)
    assert s8._in_hysteresis
    s8.stock = 0.50  # above depensation_half, below hysteresis_release
    s8.step(extraction=0.0)
    assert s8._in_hysteresis, "must clear hysteresis_release, not depensation_half"
    s8.stock = 0.65
    s8.step(extraction=0.0)
    assert not s8._in_hysteresis, "clearing release threshold unlatches"

    # Extraction cannot take more than the stock.
    s7 = Substrate(stock=0.01)
    st = s7.step(extraction=99.0)
    assert st.extraction <= 0.01 + 1e-12
    assert s7.stock >= 0.0

    print("substrate.py self-test OK")


if __name__ == "__main__":
    _self_test()
