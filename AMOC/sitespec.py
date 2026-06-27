"""
sitespec.py -- the user's substrate. What THEY can measure on THEIR land.

(Operator originally drafted this as `site.py`; saved as `sitespec.py`
to match the README module table and every importing module's
`import sitespec`. Content is verbatim.)

CC0. stdlib-only. Anti-freeze + honest-gap.

The framework does not pretend to know your water table, your soil, your
growing season. You supply them. Every field carries provenance so a fork
can be audited: who measured this, when, how sure. Unknown stays None and
is reported as a gap -- never silently defaulted into a false precision.

site.py also owns the ONE mapping the rest of the code refuses to hide:
real freshwater flux (sverdrups) -> the nondimensional F axis in forcing.py.
That calibration is declared here, with its assumptions, so nobody reads a
nondimensional spinodal as if it were a measured sverdrup value.
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Provenance:
    source: str          # "field_measured" | "public_dataset" | "estimate" | "keeper"
    who: str = "unspecified"
    when: str = "unspecified"
    confidence: str = "low"   # low | medium | high


@dataclass
class Datum:
    value: Optional[float]
    units: str
    prov: Provenance
    note: str = ""

    def known(self) -> bool:
        return self.value is not None


@dataclass
class Site:
    name: str
    lat: float
    lon: float
    # --- physical substrate (user supplies; None = honest gap) ------------
    bedrock: Datum = field(default_factory=lambda: Datum(None, "class", Provenance("estimate")))
    soil_depth_cm: Datum = field(default_factory=lambda: Datum(None, "cm", Provenance("estimate")))
    soil_thermal_mass: Datum = field(default_factory=lambda: Datum(None, "rel_0_1", Provenance("estimate")))
    water_table_m: Datum = field(default_factory=lambda: Datum(None, "m_below_surface", Provenance("estimate")))
    drainage: Datum = field(default_factory=lambda: Datum(None, "rel_0_1", Provenance("estimate")))
    growing_season_days: Datum = field(default_factory=lambda: Datum(None, "days", Provenance("estimate")))
    # --- now-state overrides for divergence.py ----------------------------
    now_state: dict = field(default_factory=dict)

    def gaps(self) -> list:
        out = []
        for fld in ("bedrock", "soil_depth_cm", "soil_thermal_mass",
                    "water_table_m", "drainage", "growing_season_days"):
            d = getattr(self, fld)
            if not d.known():
                out.append(fld)
        return out

    def custody(self) -> dict:
        return {
            fld: {
                "value": getattr(self, fld).value,
                "units": getattr(self, fld).units,
                "source": getattr(self, fld).prov.source,
                "who": getattr(self, fld).prov.who,
                "confidence": getattr(self, fld).prov.confidence,
            }
            for fld in ("bedrock", "soil_depth_cm", "soil_thermal_mass",
                        "water_table_m", "drainage", "growing_season_days")
        }


# ----------------------------------------------------------------------
# forcing calibration: real Sv -> nondimensional F. DECLARED, not hidden.
# ----------------------------------------------------------------------
@dataclass
class ForcingCalibration:
    """
    Maps a freshwater flux in sverdrups to the nondimensional F used by the
    forcing models. This is the single most assumption-laden step in the whole
    framework, so it lives in the open with its reasoning attached.

    Default anchor (REPLACE with your own reading of the literature):
      - present-day excess N. Atlantic freshwater input ~0.1-0.3 Sv (loose)
      - AMOC-collapse box-model thresholds in the literature cluster ~0.1-0.4 Sv
        of ADDED freshwater, model-dependent and wide.
      We anchor F=0 at present excess and F=spinodal at the added-flux that
      box models associate with collapse. Linear between. This is deliberately
      crude; its only virtue is being explicit.
    """
    sv_at_F0: float = 0.15        # Sv corresponding to F=0 (present-ish excess)
    sv_at_spinodal: float = 0.50  # Sv associated with crossing collapse spinodal
    spinodal_F: float = 0.217     # nondim F where StommelBox loses thermal branch
    source_note: str = ("anchors are order-of-magnitude from published AMOC "
                        "box-model freshwater-hosing ranges; REPLACE per your "
                        "own literature read. Wide uncertainty is honest here.")

    def sv_to_F(self, sv: float) -> float:
        slope = self.spinodal_F / (self.sv_at_spinodal - self.sv_at_F0)
        return slope * (sv - self.sv_at_F0)

    def F_to_sv(self, F: float) -> float:
        slope = (self.sv_at_spinodal - self.sv_at_F0) / self.spinodal_F
        return self.sv_at_F0 + slope * F


if __name__ == "__main__":
    s = Site(name="demo", lat=46.7, lon=-92.6)
    print("gaps:", s.gaps())
    cal = ForcingCalibration()
    for sv in (0.15, 0.30, 0.50, 0.70):
        print(f"  {sv:.2f} Sv -> F={cal.sv_to_F(sv):+.3f}")
