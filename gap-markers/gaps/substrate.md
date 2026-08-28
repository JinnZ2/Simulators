# SUBSTRATE GAPS

CC0. Schema in ../README.md.

---

    GAP_ID          SUB-01-FILL-INVENTORY
    DOMAIN          engineering geology / land use / seismic hazard
    STATE           uncounted
    WHAT_EXISTS     Parcel-scale artificial-fill liquefaction mapping for
                    San Francisco Bay and Puget Sound. USGS names decades-old
                    man-made fill as the highest-hazard class.
    WHAT_IS_MISSING No central-US equivalent. Quaternary maps cover natural
                    deposits; historic anthropogenic fill is not a mapped unit.
                    Site-level undocumented fill is handled parcel-by-parcel
                    by consultants at development time; the data exists in
                    thousands of private geotechnical reports and nowhere in
                    aggregate.
    ENTRY_POINT     Historic aerial photography and Sanborn maps against
                    current parcel data; both are public.
    KIND            boundary-artifact

    NOTE  Most central-US jurisdictions require no geotechnical investigation
          at all for ordinary residential construction. This is an absent
          standard, not a low one.

    NOTE  ASCE 7 site classification averages the top 30 m only. Shallow fill
          over deeper alluvium is hidden by the average, and the column
          driving long-period amplification is never sampled.

---

    GAP_ID          SUB-02-DEPOSITION-DEPTH
    DOMAIN          fluvial geomorphology / geotechnical permitting
    STATE           assembly
    WHAT_EXISTS     Post-settlement alluvium is documented. Dating markers
                    exist: lead and cesium horizons, buried soil profiles for
                    pre-settlement contact.
    WHAT_IS_MISSING Depth of deposition since ~1800 over the Mississippi
                    valley is not translated into the geotechnical permitting
                    layer. Rate is not integrable — episodic flood-pulse
                    layering with alternating permeability, plus regime change
                    from levee confinement and upstream sediment cutoff.
    ENTRY_POINT     Existing academic core records; the translation is the
                    missing step, not the measurement.
    KIND            boundary-artifact

---

    GAP_ID          SUB-03-PAVEMENT-AS-CRUST
    DOMAIN          earthquake engineering / urban hydrology
    STATE           assembly
    WHAT_EXISTS     Suppression by a non-liquefiable surface layer over a
                    liquefiable stratum is established for natural
                    low-permeability clay crusts. Caltrans documents show
                    excess pore pressure continuing to build during
                    low-intensity later stages.
    WHAT_IS_MISSING Continuous engineered pavement has not been placed in the
                    crust slot. Different geometry: laterally continuous over
                    kilometres, jointed rather than plastic. Hydrology treats
                    impervious cover only as a runoff/recharge term, never as
                    a pre-event saturation precondition for the seismic case.
    KIND            boundary-artifact

---

    GAP_ID          SUB-04-CAPPING-PRESSURE-REDIRECT
    DOMAIN          geotechnical / buried utilities / containment
    STATE           unasked
    WHAT_EXISTS     Venting behaviour of liquefied ground is understood.
    WHAT_IS_MISSING Capping does not remove overpressure; it restricts the
                    vent path. Consequences not assembled:
                      - more energy retained in pore fluid, less dissipated
                        at surface; residual pressure carries into the next
                        shock of a multi-year aftershock sequence
                      - discharge concentrates at discontinuities, which are
                        the buried linear infrastructure — utility trenches,
                        conduit runs, pipeline corridors, tank foundations
                      - a backfilled trench is looser and more permeable than
                        surrounding ground, so a utility corridor is the
                        preferential drain AND the asset required to function
                      - caps over old landfills and industrial sites ARE the
                        containment
    KIND            boundary-artifact

---

    GAP_ID          SUB-05-AQUIFER-BREACH-COUPLING
    DOMAIN          hydrogeology / seismic hazard / water supply
    STATE           unasked
    WHAT_EXISTS     Memphis aquifer confining-unit breaches are documented and
                    imaged by seismic reflection: places where the upper clay
                    is missing or thin, connecting shallow aquifer to Memphis
                    aquifer. Fault communication documented — Meeman-Shelby
                    and Cuba faults extend from the Memphis Sand upward to
                    near surface, under the Mississippi. Memphis aquifer well
                    levels correlate with river levels at r ~0.74-0.78.
                    Coseismic head changes widely reported 1811-12.
    WHAT_IS_MISSING Existing Memphis liquefaction mapping is shallow and
                    scoped to foundation performance. Whether the same event
                    contaminates the aquifer supplying the city is not asked.
                    Fresh liquefaction creates new vertical conduits; existing
                    faults are already partial pathways.
    ENTRY_POINT     Overlay published breach locations on published
                    liquefaction susceptibility. Both are public.
    KIND            boundary-artifact

    NOTE  Mechanism differs by deposit type and this is not interchangeable
          with western US experience. Fractured rock: shaking changes
          fracture aperture and connectivity — a conduit-network permeability
          change, often localized, often reversing. Unconsolidated embayment
          sand and clay: poroelastic volume change in the medium itself —
          grain rearrangement, pore collapse, pressure spike, vertical
          expulsion at scale. Once fines migrate and a confining clay is
          breached in many places, the layering that made it a confined
          aquifer is permanently different.

---

    GAP_ID          SUB-06-VOID-LOCATION
    DOMAIN          karst geology / caving / emergency response
    STATE           unowned
    WHAT_EXISTS     Real karst across the region, notably Missouri and
                    Kentucky. Caving organizations hold distributed knowledge
                    of void locations and can read surface collapse features —
                    identify that ground was filled, that structures stood
                    there, that they most likely fell in.
    WHAT_IS_MISSING No agency dataset holds this. No cross-credentialing to
                    the disaster response cadre. The knowledge exists
                    distributed; no instrument collects it.
    KIND            boundary-artifact

    NOTE  This bears directly on SUB-01. "No one has a good idea of the
          extent" is true of the official record and false of what is
          knowable.
