# TRANSPORT AND STAGING GAPS

CC0. Schema in ../README.md.

---

    GAP_ID          TRA-01-MUTUAL-ALTERNATE
    DOMAIN          continuity planning / all surface modes
    STATE           unasked
    WHAT_EXISTS     Continuity plans per mode. Each mode's plan names the
                    other modes as its alternate.
    WHAT_IS_MISSING Simultaneous loss of all modes is out of scope everywhere,
                    because each plan's alternate is another plan's subject.
                    The three surface modes fail by three DIFFERENT mechanisms
                    in the same event:
                      road   bridges and overpasses
                      rail   approach embankments
                      river  channel geometry
    KIND            boundary-artifact

---

    GAP_ID          TRA-02-RAIL-APPROACH-EMBANKMENT
    DOMAIN          rail engineering / geotechnical
    STATE           uncounted
    WHAT_EXISTS     Federal public treatment is one line: at least one
                    railroad bridge crossing the Mississippi is unlikely to
                    survive. Seismic rail work that exists is West Coast and
                    academic.
    WHAT_IS_MISSING No rail inventory, no fragility curves, nothing on
                    approach embankments or ballast. Rail bridges are private
                    carrier property inspected under carrier programs;
                    condition data is not public, so the federal assumption
                    cannot be tested from outside.
    KIND            boundary-artifact

    MECHANISM  Bridge piers are pile-founded to bearing. The approach
               embankment is not — it is fill placed on existing ground,
               because it is earthwork rather than structure, so the design
               already assumes the ground supports itself. On lowland
               deposits that were flooded, deposited on, and subsided, that
               assumption is the one liquefaction removes. Failure appears
               first at the abutment, where a pile-supported deck meets an
               embankment that has settled. That is a derailment at any speed.

    MECHANISM  Ballast is deliberately loose interlocked angular rock on
               alluvial or fill subgrade. Fouled ballast — fines from tie
               wear, coal dust — holds water and behaves closer to a
               liquefiable layer.

    NOTE  UNIT-OF-ANALYSIS FINDING. Route survival is a product of survivals
          along the corridor, not the maximum over assets. A held main-span
          crossing does not give a usable route if the delta-lowland
          approaches fail. No federal assessment uses the corridor as the
          unit.

    NOTE  Consolidation reduces the number of independent owners, which
          reduces independent routes. Redundancy on a map is not redundancy
          under one owner.

    NOTE  Repair is measured in seasons rather than weeks, because equipment
          cannot reach the work over the same failed roads.

---

    GAP_ID          TRA-03-RIVER-CHANNEL-GEOMETRY
    DOMAIN          navigation / hydrology
    STATE           unasked
    WHAT_EXISTS     Lock and dam condition is tracked as structural asset
                    condition.
    WHAT_IS_MISSING Navigation can be lost without any structural damage.
                    1811-12 did it hydraulically — banks caved wholesale,
                    islands vanished, channel filled and reformed, fissures
                    opened in the riverbed. The surveyed channel and its
                    buoyage are the navigable object, and re-establishing them
                    over that length is slow. Debris under water, stressed
                    dams, and damaged locks are additive to this, not the
                    whole of it.
    KIND            boundary-artifact

---

    GAP_ID          TRA-04-RUNWAY-AND-NODE
    DOMAIN          aviation / emergency logistics
    STATE           unasked
    WHAT_EXISTS     Air is treated as the backup mode.
    WHAT_IS_MISSING A runway is a long thin slab on prepared subgrade, sited
                    on flat river-valley ground because that is where flat is
                    — which is the alluvium. Differential settlement of a few
                    inches across a pavement joint is structurally trivial and
                    is a runway closure; unlike a road, it cannot be driven
                    slower. Further, the airfield is not the runway: fuel,
                    ground handling, lighting, navaids, and staff access are
                    each separately compromised. An intact strip with no fuel
                    farm is a landing site, not a node.
                    Rotorcraft relax the surface requirement and trade it for
                    tonnage, and require forward fuel arriving by the surface
                    modes that failed.
    KIND            boundary-artifact

---

    GAP_ID          TRA-05-STAGING-RING-LOCATION
    DOMAIN          emergency logistics
    STATE           unasked
    WHAT_EXISTS     Intermodal terminals exist with the required attributes —
                    track to hold and break a unit train, ground for cranes
                    and container handlers, outward road access, fuel, trailer
                    space.
    WHAT_IS_MISSING Those terminals are sited by market economics, which
                    clusters them at large cities — and the large cities in
                    the region are inside the affected area, not on its edge.
                    No staging ring has been located. Perimeter distance is
                    the governing variable and has not been computed.
    KIND            boundary-artifact

    NOTE  Candidate ring cities may not be outside the hazard. Central US
          crust transmits efficiently; 1811-12 was felt to Boston and
          Washington. Chicago and Indiana amplification depends on depth and
          strength, and Chicago has lake plain clays and lakefront fill, so
          site response applies there too. A staging ring cannot be selected
          without a site-response answer for each candidate — the same
          missing data, moved outward.
