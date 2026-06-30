"""
response.py -- couples a forcing state + a divergence-corrected analog + a
site into regional response BANDS (temperature, precip variance, ecosystem
lag, growing-season pressure).

CC0. stdlib-only. Anti-freeze + honest-gap.

Everything returned is a BAND (low, high) or a flagged gap, never a point
estimate. Where a site datum is missing, the dependent response is widened
and tagged "gap_widened" instead of being filled with a fake number.

The couplings are intentionally simple and legible -- linear/threshold blends,
not a tuned GCM. The point is a fork-able skeleton the keeper improves with
real local data, not a black box that emits an authoritative answer.
"""

from dataclasses import dataclass
from typing import Optional
import baseline
import divergence as dvg
import sitespec as site_mod
import sitespec as site_mod


@dataclass
class ResponseBands:
    forcing_F: float
    regime: str                      # which side of the transition we sit on
    temp_anomaly_C: tuple            # (low, high) regional, signed
    precip_variance_rel: tuple       # (low, high) multiple of baseline variance
    ecosystem_lag_decades: tuple
    growing_season_pressure: str     # qualitative
    gaps_widening_this: list
    recovery_expectation: str
    confidence: str
    provenance: str


def _blend(band: tuple, scale_lo: float, scale_hi: float) -> tuple:
    return (band[0] * scale_lo, band[1] * scale_hi)


def respond(forcing_state,
            analog: baseline.Analog,
            site: site_mod.Site,
            forcing_severity: float) -> ResponseBands:
    """
    forcing_state : a StommelState or KramersState (has .mode/.dominant/.spinodal)
    analog        : chosen paleo analog (baseline.Analog)
    site          : user Site
    forcing_severity : 0..1, how far across the transition the forcing sits
                       (caller derives this from the sweep; 1 = at/past spinodal)
    """
    report = dvg.diverge(analog, site.now_state or None)
    gaps = site.gaps()
    widened = []

    # --- regime from the forcing state -----------------------------------
    spinodal = getattr(forcing_state, "spinodal", False)
    mode = getattr(forcing_state, "mode", None) or getattr(forcing_state, "dominant", "")
    if spinodal or "collapse" in str(mode) or mode == "haline_collapsed":
        regime = "past_spinodal_collapse"
    elif mode in ("transitional",) or 0.6 <= forcing_severity < 1.0:
        regime = "in_transition_band"
    else:
        regime = "pre_transition"

    # --- temperature band ------------------------------------------------
    # analog NH cooling, scaled by how far across we are, signed negative
    base_cool = analog.nh_cooling_C
    sev = max(0.0, min(1.0, forcing_severity))
    temp_lo = -base_cool[1] * sev          # deeper cooling at high end
    temp_hi = -base_cool[0] * sev
    # divergence says faster/choppier -> widen the cold tail
    if "FASTER" in report.rate_adjustment:
        temp_lo *= 1.3
    temp_band = (round(temp_lo, 2), round(temp_hi, 2))

    # --- precip variance band -------------------------------------------
    # analogs all report higher interannual variance; lost buffers amplify it
    pv_lo, pv_hi = 1.2, 2.0
    if "FASTER" in report.rate_adjustment:
        pv_hi *= 1.4
    if "drainage" in gaps or "soil_thermal_mass" in gaps:
        pv_hi *= 1.3
        widened.append("precip_variance (missing drainage/thermal mass)")
    precip_band = (round(pv_lo, 2), round(pv_hi, 2))

    # --- ecosystem lag ---------------------------------------------------
    eco = analog.ecosystem_lag_decades
    if "soil_thermal_mass" in gaps or "soil_depth_cm" in gaps:
        eco = (eco[0], eco[1] * 1.5)
        widened.append("ecosystem_lag (missing soil data)")

    # --- growing season pressure ----------------------------------------
    gs = site.growing_season_days
    if not gs.known():
        gs_pressure = ("UNKNOWN -- supply growing_season_days. Direction is "
                       "compression + higher year-to-year swing.")
        widened.append("growing_season (missing growing_season_days)")
    else:
        comp = sev * 0.4   # up to ~40% compression at full severity (crude)
        gs_pressure = (f"~{int(gs.value)}d baseline -> compresses toward "
                       f"~{int(gs.value*(1-comp))}d at this severity, with "
                       f"high interannual variance (frost-window instability)")

    return ResponseBands(
        forcing_F=getattr(forcing_state, "F", float("nan")),
        regime=regime,
        temp_anomaly_C=temp_band,
        precip_variance_rel=precip_band,
        ecosystem_lag_decades=eco,
        growing_season_pressure=gs_pressure,
        gaps_widening_this=widened,
        recovery_expectation=report.recovery_adjustment,
        confidence=report.confidence_after,
        provenance=(f"analog={analog.name}({analog.source_class}); "
                    f"divergence-corrected; site gaps={gaps or 'none'}"),
    )


if __name__ == "__main__":
    from forcing import StommelBox
    s = site_mod.Site(name="demo", lat=46.7, lon=-92.6)
    box = StommelBox()
    st = box.state(0.25)   # past spinodal
    rb = respond(st, baseline.EVENT_8200, s, forcing_severity=1.0)
    print(rb)
