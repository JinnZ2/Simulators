# STRUCTURE GAPS

CC0. Schema in ../README.md.

---

    GAP_ID          STR-01-SEQUENCE-VS-EVENT
    DOMAIN          dam safety engineering / seismology
    STATE           unasked
    WHAT_EXISTS     USACE ER 1110-2-1806 (reissued 2024) requires
                    risk-informed seismic evaluation of every dam and levee
                    against site-specific ground motion. Duration IS handled
                    within an event — ground motion selection, and
                    liquefaction assessment is duration-sensitive.
                    Mainshock-aftershock cumulative damage is an active
                    research literature.
    WHAT_IS_MISSING Sequence has not landed in the standard. Each structure
                    is evaluated single-event, from an undamaged starting
                    condition. The 1811-12 sequence ran three main shocks over
                    two months with daily earthquakes continuing into 1814.
    KIND            boundary-artifact

---

    GAP_ID          STR-02-BASIN-CASCADE-AGGREGATION
    DOMAIN          dam safety / regional emergency planning
    STATE           unowned
    WHAT_EXISTS     District-portfolio coverage with the individual project as
                    unit of analysis. Federal dam safety guidelines
                    (FEMA P-93) put upstream-dam-failure cascade on each
                    owner's emergency action plan.
    WHAT_IS_MISSING No aggregate. No one runs multiple simultaneous partial
                    releases across basins arriving at an already-liquefied
                    valley. Cascade is owned per-owner, so the regional sum
                    has no owner. Hazus carries liquefaction probability;
                    dams are not an inventory class in it.
    KIND            boundary-artifact

---

    GAP_ID          STR-03-DUAL-FUNCTION-STRUCTURES
    DOMAIN          FHWA / USACE / private utility easement
    STATE           uncounted
    WHAT_EXISTS     National Bridge Inventory keyed on roadway. National
                    Inventory of Dams keyed on impoundment. NID tracks locks
                    as a project attribute.
    WHAT_IS_MISSING No cross-reference field. No dual-function flag in NID;
                    no dam field in NBI. Utility attachments — fiber, gas,
                    transmission — are typically private easements or
                    licenses, so even the owner's records may show a permit
                    rather than a routed critical line. The dual- and
                    triple-function population is uncounted and therefore
                    unprioritizable.
    KIND            boundary-artifact

---

    GAP_ID          STR-04-UNDERGROUND-FACILITY-DYNAMICS
    DOMAIN          mining engineering / facility siting / records storage
    STATE           unasked
    WHAT_EXISTS     Facilities selected for thermal stability, security, and
                    cost per square foot. 1811-12 contemporary accounts record
                    that many limestone caverns underlying the region
                    collapsed or filled with water — the opposite of the
                    design assumption.
    WHAT_IS_MISSING Modified openings are the specific exposure: rock removed
                    for expansion; bracings and rock bolts designed against
                    static load with no dynamic reserve and no specified
                    fatigue life for years of cycling; widened spans lower
                    roof natural frequency toward soft-column resonance.
                    Access is single-point — one portal, ramp, or shaft.
                    Ventilation and dewatering are powered.
    KIND            boundary-artifact

    NOTE  Failure mode is not roof collapse. Dewatering is sized against a
          pre-event seepage rate. If the event raises head and opens new
          pathways while the grid is down, the space fills.

    NOTE  Bounding case is faster than seepage. If a confined aquifer is
          overpressured and the void sits below the potentiometric surface,
          the regime is artesian flow into an open space, not seepage. With a
          breached confining layer above and a river system in flood over the
          top, driving head is large and sustained. Inflow carries sediment;
          pumps sized for water do not move slurry.

    NOTE  Pressure that cannot vent upward diffuses along any available
          gradient — karst, caves, any underground structure. Contents can be
          intact and functionally at zero.

---

    GAP_ID          STR-05-RETROFIT-BASELINE
    DOMAIN          bridge engineering / building stock
    STATE           undated
    WHAT_EXISTS     73% of all bridges in the NMSZ were built before 1990
                    (Wright et al. 2011). Retrofit proceeds project-by-project
                    on landmark structures. FEMA scenario projects 60%+ of
                    Memphis unreinforced masonry buildings collapsed or
                    uninhabitable.
    WHAT_IS_MISSING Nothing has touched fill, dual-function structures, or
                    underground facilities. One source cites a city retrofit
                    program at ~5% compliance; this figure needs a primary
                    source before use.
    KIND            knowledge (for the compliance figure) /
                    boundary-artifact (for the scope)
