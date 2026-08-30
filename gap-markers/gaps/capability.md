# CAPABILITY AND RESPONSE GAPS

CC0. Schema in ../README.md.

---

    GAP_ID          CAP-01-STAGING-AS-PRODUCTION
    DOMAIN          industrial capacity / emergency logistics
    STATE           unasked
    WHAT_EXISTS     MITRE has published the framework: regions are the right
                    unit, and every region should run functions-based
                    resilience assessments incorporating private and local
                    knowledge. A University of Colorado group maps regional
                    construction capacity against disaster risk.
    WHAT_IS_MISSING The MITRE framework is a recommendation with no program.
                    The Colorado method is scoped to single-family residential
                    rebuilding, not industrial production.
                    The requirement itself is unstated: a staging ring must be
                    a PRODUCTION ring. Waiting on rail from the west coast or
                    a ship from a port is not available; material has to be
                    made at the staging site.
                    The needed items are high mass and low value density —
                    culvert and pipe, aggregate and concrete, plate for
                    temporary spans, timber cribbing, tank and pump
                    fabrication, electrical distribution gear — the class
                    where freight cost dominates and long hauls are
                    irrational. This is the capacity that was consolidated or
                    offshored, and several remaining national plants sit
                    inside the affected area because that is where river and
                    rail were.
    KIND            boundary-artifact

    NOTE  SUPPLY-CHAIN CONCENTRATION SUBSTITUTION. Federal supply chain work
          (Quadrennial Supply Chain Review, critical materials studies)
          measures geographic concentration as a risk factor, but "geographic"
          there means country or trade bloc. Domestic concentration inside a
          single hazard footprint is not in the frame. Reshoring to the middle
          of the country reads as pure risk reduction in that framework.

    NOTE  Industrial and manufacturing sites sit on the same compromised
          substrate — heavy industry sited itself on flat riverside ground for
          water and barge access — so the counted-on capacity is
          disproportionately located where the ground is worst. Aquifers and
          drainage around those sites are affected too.

---

    GAP_ID          CAP-02-CAPABILITY-ON-RAMP
    DOMAIN          federal contracting / emergency response
    STATE           unowned
    WHAT_EXISTS     FEMA Advance Contracts and the USACE Advanced Contracting
                    Initiative pre-position contract tools. A Disaster
                    Response Registry exists and USACE builds its response
                    list from it.
    WHAT_IS_MISSING Entry is via SAM registration — federal contractor
                    apparatus, CAGE code — built for firms carrying federal
                    work as a business line. Emergency authorities accelerate
                    awards to contractors ALREADY inside the system rather
                    than creating entry points for new ones. Surge capacity is
                    therefore definitionally the set of firms that were
                    already federal contractors before the event. Local
                    capability that is not registered is invisible regardless
                    of proximity or fitness.
    KIND            boundary-artifact

    NOTE  Concrete instance: dredges and rock crushers are needed ahead of
          dams, waterways, and locks to relieve sediment pressure and prevent
          further flooding. The equipment exists, owned by aggregate producers
          and marine contractors, positioned by where the gravel market is
          rather than where a sediment emergency would be. There is no list.
          There is a procurement process that runs after declaration.

---

    GAP_ID          CAP-03-GRADUATED-FABRICATION-RESPONSE
    DOMAIN          emergency response doctrine
    STATE           assembly
    WHAT_EXISTS     Graduated-capability response is standard doctrine in
                    medical first response: whoever is nearest and capable
                    works until someone better-equipped relieves them.
                    Spontaneous volunteer response is a repeatedly observed
                    pattern; willingness is not the constraint.
    WHAT_IS_MISSING The doctrine has not been applied to fabrication.
                    Current contractor model responds only on condition that
                    all machines are staged in first — four or five days
                    before anything starts, more with complexity. Contractors
                    do what they are paid to do; people die in the interval.
                    What is absent:
                      - a matching layer routing a need at a site to a shop
                        that can make the part, currently brokered through
                        contracting officers
                      - communication that does not assume cell service
                      - triage converting "I have a welder and a trailer"
                        into a specific task at a specific place in sequence
                    The resilient asset is general-purpose capability and hand
                    tools, because the electricity situation is unknown —
                    people who can sandcast aluminum or iron, run a battery
                    welder, work from a measurement rather than a drawing.
                    That is precisely the capacity lean manufacturing
                    eliminated as underutilized.
    KIND            boundary-artifact

    NOTE  Fabrication demand is spur-of-the-moment and specific: e.g. making
          gear for an old dam so it can run to clear silt, because failing
          that breaks the infrastructure and floods the community downstream.

---

    GAP_ID          CAP-04-RESPONDER-SCENARIO-MISMATCH
    DOMAIN          mutual aid systems / responder training
    STATE           unasked
    WHAT_EXISTS     US&R task forces, configured around a structural-collapse
                    scenario on stable ground: concrete cutting, shoring,
                    heavy rescue over a compact drivable footprint.
    WHAT_IS_MISSING NMSZ is a ground-failure problem over a large
                    non-drivable footprint: earthmoving, dewatering, dredging,
                    temporary spans, water treatment. Registered responders
                    are not informed the event differs in kind and will arrive
                    with the equipment they use for other earthquakes. They
                    will bring the wrong equipment or not enough, and bill for
                    it — which is legitimate — but efficiency and optimization
                    are lost and people suffer in the interval.
                    Root cause: no equipment-type demand estimate has been
                    published for this event, so a responder who wanted to
                    bring the right thing has nothing to read.
    KIND            boundary-artifact

---

    GAP_ID          CAP-05-CROSS-DISCIPLINE-RESCUE-ROSTER
    DOMAIN          MSHA / FEMA / ARFF / NSS
    STATE           unowned
    WHAT_EXISTS     Mature rescue disciplines, each with its own
                    credentialing, dispatch, and equipment cache:
                      mine rescue      MSHA, own competitions and
                                       certification; tailings, silt, and
                                       quicksand-mud extraction — the closest
                                       existing trade to what liquefaction
                                       produces
                      ARFF             large-volume foam, fixed and mobile
                                       turrets, crash rescue; the discipline
                                       built for hydrocarbon fire, which is
                                       what pipeline and tank farm fires are
                      wildland         containment and drafting logic for
                                       fire with no working hydrant network
                      cave rescue      NSS / National Cave Rescue Commission;
                                       confined space in unstable wet
                                       irregular ground, no line of sight, no
                                       radio path — the same problem as
                                       collapsed structure in liquefied ground
                                       or a compromised underground facility
    WHAT_IS_MISSING No shared roster, no cross-credentialing to the FEMA and
                    US&R world. An event needing mine rescue tactics in a
                    suburb and ARFF at a pipeline in a flooded field maps to
                    no single discipline's dispatch. The capability exists in
                    full and arrives partially or not at all.
    KIND            boundary-artifact

    NOTE  Municipal structural crews are neither equipped nor trained for
          sustained flammable-liquid fire, and are also the crews whose water
          supply has failed.

---

    GAP_ID          CAP-06-STOCKPILE-FACILITY-SURVIVABILITY
    DOMAIN          GAO oversight / stockpile management
    STATE           unasked
    WHAT_EXISTS     GAO oversight is inventory-focused: what is held,
                    shortfalls, supplier counts. CRS stockpile overview covers
                    procurement and expiration. FEMA 460 covers seismic design
                    of steel storage racks.
    WHAT_IS_MISSING Facility survivability is not an audited dimension. FEMA
                    460 is guidance, not requirement, with no indication of
                    application at federal stockpile sites. The actual failure
                    mode — building survives, racking collapses cross-aisle,
                    contents buried — is unaddressed. Siting for distribution
                    logistics and security correlates stockpile location with
                    the hazard corridor.
    KIND            boundary-artifact

    NOTE  JIT AND VENDOR-HELD LAYER. The model moved to just-in-time and
          vendor-held off-site stock. Vendor warehouses carry no FEMA
          standards, were not secure, and inventory is self-inventory verified
          only every six months to two years by region. The reported stockpile
          total is therefore partly fictional — it includes material not yet
          manufactured, backed by supply chains running the same corridors.

    NOTE  DEPENDENCY IS CYCLIC, NOT A LIST. Road is needed to reach the
          stockpile; the stockpile is needed to fix the road; power is needed
          for pumps to reach either. This is not mapped as a redundancy web.

---

    GAP_ID          CAP-07-GRID-COUPLING
    DOMAIN          electric grid / regional interdependency
    STATE           unasked
    WHAT_EXISTS     Large power transformers: multi-year lead times, largely
                    imported, custom-built per site, moved by heavy rail and
                    specialized trailers over the routes in TRA-02.
    WHAT_IS_MISSING If transformers pull out across the middle of the country,
                    propagation to the rest of the grid is not modelled for
                    this event. ERCOT separation cuts both ways — it limits
                    inbound cascading and also limits ability to import
                    support through DC ties that are small relative to load.
                    Coupled effect, coupled resources, nationwide ripple.
    KIND            boundary-artifact

---

    GAP_ID          CAP-08-DEBRIS-BURIAL-DENOMINATOR
    DOMAIN          solid waste regulation / FEMA public assistance
    STATE           uncounted
    WHAT_EXISTS     Texas TCEQ requires burial residue to be deed recorded
                    under municipal solid waste rules. FEMA requires
                    applicants to document staging, reduction, and final
                    disposal sites.
    WHAT_IS_MISSING The TCEQ requirement attaches only to the permitted
                    pathway. The FEMA record is a reimbursement and
                    environmental-review artifact in a project file, never on
                    title. Population splits three ways:
                      1. recorded burials
                      2. unrecorded burials — county crew, own property, no
                         reimbursement claim, emergency permit waiver
                      3. flood-emplaced debris, never a disposal event, no
                         agency with jurisdiction to record it
                    Ratio unknown. Missing denominator.
    KIND            boundary-artifact

    NOTE  Tornado-debris burial has been standard practice since the
          1950s-60s and continues.
