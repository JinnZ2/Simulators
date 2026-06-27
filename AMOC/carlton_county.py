"""
carlton_county.py -- the worked vertical slice. Carlton County, MN, on the
Canadian Shield. This is the example a keeper FORKS: copy it, swap the Site
data for your own land, swap/aug the analog, rerun.

CC0. stdlib-only. Anti-freeze.

NOTHING here is authoritative for your land. The site numbers below are
explicitly marked by provenance. Where they are "estimate", they are a
placeholder begging to be replaced by a field measurement. The whole point of
the framework is that YOUR reading of YOUR ground beats any default.

Run:  python3 carlton_county.py
"""

import baseline
import sitespec
import trajectory


def build_site() -> sitespec.Site:
    P = sitespec.Provenance
    D = sitespec.Datum
    return sitespec.Site(
        name="Carlton County, MN (Canadian Shield)",
        lat=46.66, lon=-92.68,
        bedrock=D("Precambrian_shield", "class",
                  P("public_dataset", who="USGS surficial geology",
                    when="2024", confidence="high"),
                  "thin glacial till over crystalline bedrock; low storage"),
        soil_depth_cm=D(45.0, "cm",
                        P("estimate", confidence="low"),
                        "REPLACE: dig and measure A+B horizon on your parcel"),
        soil_thermal_mass=D(0.35, "rel_0_1",
                            P("estimate", confidence="low"),
                            "thin till -> low thermal buffering; REPLACE"),
        water_table_m=D(None, "m_below_surface",
                        P("estimate", confidence="low"),
                        "GAP: site-specific; shield perches water locally, "
                        "varies parcel to parcel"),
        drainage=D(0.55, "rel_0_1",
                   P("estimate", confidence="low"),
                   "mixed: shield runs off fast, bogs hold; REPLACE per parcel"),
        growing_season_days=D(120.0, "days",
                              P("public_dataset", who="NOAA normals 1991-2020",
                                when="2021", confidence="medium"),
                              "current frost-free window; expect compression "
                              "AND higher variance under transition"),
        now_state={
            "continental_ice": False,
            "meltwater_buffer": False,
            "permafrost_cycle": False,
            "sea_level_rising": True,
        },
    )


def main():
    site = build_site()

    print("=" * 70)
    print("CARLTON COUNTY -- AMOC REGIME-SHIFT TRAJECTORY SLICE")
    print("=" * 70)
    print("\nSite custody (what we know, how sure, who said so):")
    for k, v in site.custody().items():
        print(f"  {k:22s} {str(v['value']):>18s} {v['units']:18s} "
              f"[{v['source']}/{v['confidence']}]")
    print(f"\n  open site gaps: {site.gaps()}")

    # run the ensemble against the best-RATE analog (8.2ka) and the
    # ENSO-coupled analog (Heinrich 1), since a super-El-Nino-during-loading
    # scenario is exactly the Heinrich signal.
    for analog in (baseline.EVENT_8200, baseline.HEINRICH_1):
        print("\n" + "-" * 70)
        print(f"ANALOG: {analog.name}  (divergence-corrected for no-ice start)")
        print("-" * 70)
        ens = trajectory.run(site, analog, F_lo=0.0, F_hi=0.6, n=13)

        print(f"  spinodal F  stommel={ens.spinodal_F_stommel:.3f}  "
              f"kramers={ens.spinodal_F_kramers:.3f}")
        print(f"  cliff zones (F): {ens.cliff_zones}")
        print(f"  MODEL DISAGREEMENT band (F): {ens.model_disagreement}")
        print(f"    ^ under-determined zone: trust neither model here, "
              f"this IS the finding")
        print(f"  recovery: {ens.recovery_expectation[:88]}...")
        print(f"  confidence: {ens.confidence}")
        print("\n   F     ~Sv    sev   regime(stommel)        agree  temp_C")
        for p in ens.points:
            print(f"  {p.F:.3f} {p.sv:>5}  {p.severity:.2f}  "
                  f"{p.stommel_regime:22s} {str(p.models_agree):5s}  "
                  f"{p.temp_band_C}")

    print("\n" + "=" * 70)
    print("KEEPER GAPS to close before trusting any band:")
    for g in ens.keeper_gaps:
        print(f"  - {g}")
    print("\nNothing above is a forecast. It is a response surface. Fill the")
    print("gaps with field data and the bands narrow. Where models disagree,")
    print("the answer is 'under-determined', not an average.")


if __name__ == "__main__":
    main()
