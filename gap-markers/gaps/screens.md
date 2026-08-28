# SCREENS NOT RUN

CC0. Schema in ../README.md.

Entries here share a property: the data already exists, the method already
exists, and the computation has not been performed. These are the cheapest
gaps to close.

---

    GAP_ID          SCR-01-TERRAIN-IMPOUNDMENT-SCREEN
    DOMAIN          landslide hazard / dam safety / flood mapping
    STATE           unowned
    WHAT_EXISTS     Barry Arm, Alaska is intensively studied — identified from
                    satellite imagery ~2020, joint USGS / state / Forest
                    Service monitoring, modelled wave heights. Taan Fiord 2015
                    is the proof of concept: 180 million tons into a fjord,
                    193 m runup, among the highest ever recorded.
                    High-resolution national elevation data exists from lidar
                    for most of the country. Runout is well approximated by
                    angle-of-reach relationships computable over a whole DEM.
    WHAT_IS_MISSING No systematic screen of US slopes above water bodies or
                    occupied valleys. Sites become known when someone spots
                    them, usually after a nearby event draws attention — in
                    2024 five landslides collapsed into Surprise Inlet, a
                    short distance from Barry Arm, at a site not flagged as an
                    imminent hazard. The known set is biased toward wherever a
                    researcher was already looking. How many such places exist
                    is genuinely unknown.
    ENTRY_POINT     Slope angle + relief above valley or impoundment +
                    downstream exposure, computed over the national DEM. This
                    is a compute job, not a research question.
    KIND            boundary-artifact

    WHY UNRUN       Two non-technical reasons. The screen produces a large
                    flagged set, and every flagged site becomes a liability
                    and disclosure question for whoever publishes the list.
                    And no agency owns "slope above a thing that matters" —
                    USGS runs landslides as a science program, USACE runs
                    dams, FEMA runs flood mapping; a screen crossing all three
                    has no home.

    SCOPE           Screen by terrain, not by trigger. Strip the glacier and
                    the specific initiating mechanism; keep the geometry —
                    impounded volume with elevation head above an occupied
                    confined valley plus any mechanism for fast release.
                    Includes lakes in fault zones, places sitting above
                    rivers, and weakened dam systems where debris loading
                    could cause collapse.

---

    GAP_ID          SCR-02-HAZARD-CLASS-CURRENCY
    DOMAIN          dam safety regulation
    STATE           undated
    WHAT_EXISTS     Tens of thousands of small dams — private farm ponds, old
                    mill dams — classified low-hazard. Classification is by
                    CONSEQUENCE, not condition, so low-hazard dams receive
                    little inspection.
    WHAT_IS_MISSING Hazard class is assigned once. Downstream development
                    changes. A pond above pasture in 1960 is above houses now,
                    and reclassification often never happens.
    ENTRY_POINT     Date of last hazard-class review, per structure. A null
                    or a decades-old date IS the finding. No fieldwork
                    required to produce the list.
    KIND            boundary-artifact

    NOTE  Small dams sit in chains along a single stream. One failure sends
          the next a surge it was never designed for.

---

    GAP_ID          SCR-03-IMPOUNDMENT-STORAGE-LOSS
    DOMAIN          reservoir management / remote sensing
    STATE           undated / unasked
    WHAT_EXISTS     A sediment-filled impoundment has lost flood storage while
                    still reading as a dam on a map. Global surface water
                    extent datasets run back to the mid-1980s from Landsat.
                    Surface area comes directly from optical or radar imagery;
                    combined with a hypsometric curve it gives volume. Radar
                    altimetry gives water surface elevation directly for
                    larger bodies.
    WHAT_IS_MISSING Reservoir bathymetry is not resurveyed on a routine
                    schedule. And the remote sensing products report water
                    extent as a HYDROLOGY variable — reading a trend in
                    surface area at constant pool as an indicator of
                    sedimentation makes it a CONDITION ASSESSMENT of the
                    structure, and that inference is not in the product.
    ENTRY_POINT     Two independent starting points:
                      1. date of last bathymetric survey, per impoundment
                      2. satellite time series of surface area at comparable
                         pool elevation, per impoundment, over the archive
    KIND            boundary-artifact

    NOTE  Same substitution as elsewhere: data collected as one thing, never
          asked the other question.

---

    GAP_ID          SCR-04-COMPOUND-DESIGN-CASE
    DOMAIN          hazard statistics / design standards
    STATE           unasked
    WHAT_EXISTS     Return-period design cases — the 500-year flood and
                    equivalents — estimated per variable from records often
                    under a century, under a stationarity assumption.
    WHAT_IS_MISSING Joint probability across hazard domains is not computed,
                    because it requires correlated hazard data across domains
                    that do not share a model. A compound event therefore
                    reads as unprecedented relative to a design case that
                    never contained it as a possibility. The event is outside
                    the FRAME, not outside the physics.
    KIND            boundary-artifact

    NOTE  The buildings-versus-lifelines split is the clean demonstration.
          Building codes are performance-based and life-safety-oriented and
          have worked. A buried gas main is not a building — it is a utility,
          regulated by a public utility commission on a rate case, where
          seismic hardening is a cost with no rate-recoverable benefit until
          failure. Different regulator, different economics, different unit of
          analysis. Result is a hardened structure connected to unhardened
          everything: the building is fine and uninhabitable. Kobe 1995
          demonstrated it — surviving buildings mattered little with water out
          for months.

    NOTE  Discounting is the mechanism, not malice. Once a monetary scalar
          stands in for a collapsed set of dimensions, it sets a discount
          rate, and a discount rate makes a 50-year failure worth almost
          nothing today. The design case is then whatever survives
          discounting, and a compound event is by definition what does not.

    NOTE  Failure-timing asymmetry explains why the same organizations
          engineer honestly elsewhere. For a launch, failure is immediate,
          attributable, and visible, so the incentive to engineer honestly
          survives contact with the budget. Infrastructure failure is delayed
          by decades and diffuse in attribution, so identical pressure
          produces opposite behaviour.

---

    GAP_ID          SCR-05-CASCADING-PROCESS-CHAIN-CLASSIFICATION
    DOMAIN          hazard classification / geomorphology
    STATE           assembly
    WHAT_EXISTS     Per-process models: rock avalanche runout, debris flow,
                    flood routing. Each a separate code with separate inputs.
    WHAT_IS_MISSING Chaining requires the output of one to become the initial
                    condition of the next, and uncertainty compounds at every
                    handoff, so most assessments model the dominant process
                    and treat the rest as boundary conditions. Classification
                    splits on ORIGIN, not on behaviour or deposit.
    KIND            boundary-artifact

    WORKED CASE     August 2026, Nepal / China border, Lhende Khola into
                    Bhote Koshi into Trishuli. USGS: debris avalanche and
                    flash flood triggered by rapid slope failure involving a
                    glacier. Initiating event is an ice-rock avalanche — ice
                    and rock detaching together, distinct from pure rockslide
                    or pure ice avalanche.
                    Not a lahar: lahar is volcanic-sourced by definition.
                    Not a jökulhlaup: that is impounded meltwater release.
                    Not a classic GLOF: no pre-existing lake burst.
                    Best fit is cascading process chain — ice-rock avalanche
                    to debris flow to flood wave, each phase with different
                    mechanics.

    NOTE  Deposit morphology resembles a lahar because middle-phase physics is
          nearly identical: hyperconcentrated-to-debris-flow slurry, saturated
          sediment moving as fluid, scour to bedrock, poorly sorted
          matrix-supported deposit with boulders in fines. Found in the field
          without historical record, it would be hard to distinguish from a
          volcanic lahar deposit on sedimentology alone. The naming convention
          tracks source, not process.

    NOTE  Initial reporting swung between glacier collapse, landslide, and
          GLOF. Each observer named the phase their instrument could see.

    NOTE  A secondary lake formed from debris buildup at the flood site and is
          rising — the chain continued after the classified event ended.

    US ANALOGUES    Both halves of an NMSZ outcome have historical precedent:
                    sudden release with entrainment (Johnstown 1889 — dam
                    failure moving as mud, trees, houses, rail cars), and
                    long-tail sediment loading that makes ordinary floods
                    catastrophic for decades (California hydraulic mining
                    debris, 1850s onward; hundreds of millions of cubic yards
                    into the Sacramento and Feather systems, raised riverbeds,
                    buried farmland, repeated flooding, ended by the Sawyer
                    Decision 1884). NMSZ produces both simultaneously.
