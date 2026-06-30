"""
trajectory.py -- the anti-freeze core. Generates TRAJECTORY ENSEMBLES across a
forcing range and an analog set. Never caches a verdict, never returns "your
region will be X." Returns the spread, where it is sensitive, and what fails
first -- so the keeper reads the response surface and decides.

CC0. stdlib-only.

Design rules (inherited from the JinnZ2 REFUTATION_PROTOCOL):
  - No stored conclusions. Every call recomputes from inputs.
  - Output is a distribution over (forcing severity x analog x site-gaps),
    not a single number.
  - Sensitivity is reported explicitly: change F by a step, see how far the
    band moves. A region whose outcome swings hard on a small F change is
    flagged as living near the cliff.
  - Disagreement between the two forcing models is surfaced, not hidden
    (Consensus-Fault: divergence-between-models is itself signal).
"""

from dataclasses import dataclass, asdict
from typing import Optional
import json

import baseline
import sitespec as site_mod
import response as resp
from forcing import StommelBox, KramersWell


@dataclass
class TrajectoryPoint:
    F: float
    sv: Optional[float]
    severity: float
    stommel_regime: str
    kramers_regime: str
    models_agree: bool
    temp_band_C: tuple
    precip_var_band: tuple
    growing_season: str


@dataclass
class Ensemble:
    site_name: str
    analog_name: str
    points: list
    spinodal_F_stommel: Optional[float]
    spinodal_F_kramers: Optional[float]
    cliff_zones: list          # F values where outcome swings hardest
    model_disagreement: list   # F values where the two models disagree on regime
    recovery_expectation: str
    confidence: str
    keeper_gaps: list
    honest_note: str


def _severity_from_band(F: float, band: dict) -> float:
    """0 pre-band, ramps to 1 at the collapse spinodal, >1 past it (clamped 1)."""
    lo = band.get("spinodal_recovery")
    hi = band.get("spinodal_collapse")
    if hi is None:
        return 0.0
    lo = lo if lo is not None else 0.0
    if F <= lo:
        return 0.0
    if F >= hi:
        return 1.0
    return (F - lo) / (hi - lo) if hi > lo else 1.0


def run(site: site_mod.Site,
        analog: baseline.Analog,
        F_lo: float = 0.0,
        F_hi: float = 0.6,
        n: int = 25,
        calibration: Optional[site_mod.ForcingCalibration] = None) -> Ensemble:

    cal = calibration or site_mod.ForcingCalibration()
    box = StommelBox()
    well = KramersWell()

    band = box.hysteresis_band(F_lo, max(F_hi, 1.6), n=80)
    sp_stommel = band.get("spinodal_collapse")
    sp_kramers = well.spinodal_forcing(0.0, 1.0, 200)

    points = []
    prev_temp_mid = None
    cliffs = []
    disagree = []

    for i in range(n):
        F = F_lo + (F_hi - F_lo) * i / (n - 1)
        sev = _severity_from_band(F, band)

        st = box.state(F, dT0=1.0, dS0=0.1)   # probe from thermal basin
        kr = well.state(F)

        rb = resp.respond(st, analog, site, forcing_severity=sev)

        st_regime = rb.regime
        kr_regime = ("past_spinodal_collapse" if kr.spinodal
                     else ("in_transition_band" if kr.barrier_on_to_off < 0.05
                           else "pre_transition"))
        agree = (st_regime == kr_regime)
        if not agree:
            disagree.append(round(F, 3))

        tp = TrajectoryPoint(
            F=round(F, 4),
            sv=round(cal.F_to_sv(F), 3),
            severity=round(sev, 3),
            stommel_regime=st_regime,
            kramers_regime=kr_regime,
            models_agree=agree,
            temp_band_C=rb.temp_anomaly_C,
            precip_var_band=rb.precip_variance_rel,
            growing_season=rb.growing_season_pressure,
        )
        points.append(tp)

        # cliff detection: large jump in temp band midpoint per F step
        mid = (rb.temp_anomaly_C[0] + rb.temp_anomaly_C[1]) / 2
        if prev_temp_mid is not None:
            if abs(mid - prev_temp_mid) > 0.5:   # >0.5C swing in one F step
                cliffs.append(round(F, 3))
        prev_temp_mid = mid

    # one divergence report for narrative fields
    report = resp.respond(box.state(F_hi), analog, site, forcing_severity=1.0)

    return Ensemble(
        site_name=site.name,
        analog_name=analog.name,
        points=points,
        spinodal_F_stommel=sp_stommel,
        spinodal_F_kramers=sp_kramers,
        cliff_zones=cliffs,
        model_disagreement=disagree,
        recovery_expectation=report.recovery_expectation,
        confidence=report.confidence,
        keeper_gaps=dvg_gaps(site, analog),
        honest_note=(
            "Trajectories, not a forecast. Bands widen where site data is "
            "missing; fill the keeper_gaps to narrow them. Where the two "
            "forcing models disagree (model_disagreement), trust neither -- "
            "that F is under-determined and is itself the finding."
        ),
    )


def dvg_gaps(site, analog):
    import divergence
    rep = divergence.diverge(analog, site.now_state or None)
    return site.gaps() + rep.keeper_gaps


def to_json(ens: Ensemble) -> str:
    d = asdict(ens)
    return json.dumps(d, indent=2)


if __name__ == "__main__":
    s = site_mod.Site(name="demo", lat=46.7, lon=-92.6)
    e = run(s, baseline.EVENT_8200, n=12)
    print("spinodal F (stommel/kramers):", e.spinodal_F_stommel, e.spinodal_F_kramers)
    print("cliffs:", e.cliff_zones)
    print("model disagreement at F:", e.model_disagreement)
    for p in e.points:
        print(f"  F={p.F:.3f} ~{p.sv}Sv sev={p.severity:.2f} "
              f"{p.stommel_regime:24s}/{p.kramers_regime:20s} "
              f"agree={p.models_agree} T={p.temp_band_C}")
