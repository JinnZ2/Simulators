# BUILD SPEC — Columbia chain cascade model with initiator modules and
# antecedent-condition coupling

Executable in HEC-RAS 2D on public data. CC0, no rights reserved.
Method reference: the Three Gorges breach product (DEM + HEC-RAS) — what
transfers is three choices, stated up front.

## 0. THE THREE CHOICES THAT MAKE IT USEFUL

    1. PUBLISH VELOCITY BANDS, not depth-and-extent
       m/s bands with area per band and a physical-consequence column
       per band. Velocity determines survival of people, vehicles,
       structures. Depth alone does not.

    2. PUBLISH TIME SLICES, not the maximum envelope
       t = 1, 6, 24, 72, 168 h. The envelope hides that the hazard field
       MOVES. A 168 h slice is a response-planning product; an envelope
       is a zoning product.

    3. OVERLAY EXPOSURE ON THE SAME SHEET
       population density + per-node counts on the hazard field, not in
       a separate consequence table.

## 1. DOMAIN — full chain, no reach truncation

    Upper:   Mica, Revelstoke, Keenleyside (CA) as inflow boundary
    US:      Grand Coulee, Chief Joseph, Wells, Rocky Reach,
             Rock Island, Wanapum, Priest Rapids
    Snake:   Lower Granite, Little Goose, Lower Monumental, Ice Harbor
    Lower:   McNary, John Day, The Dalles, Bonneville
    Estuary: Bonneville to the mouth, tide as downstream boundary

Full chain is required, not preferred: attenuation and amplification only
appear across nodes. A reach study cannot produce the answer.

Ownership layer, recorded per node — this is the governance variable:
USACE / USBR / PUD / BC Hydro / private. Federal EAP structure assigns
planning to the OWNER, so mixed ownership means no entity's plan spans
the chain. Record it as data, not commentary.

## 2. TERRAIN AND CHANNEL

    DEM        3DEP 1 m where available, 10 m elsewhere
    bathy      NOAA charts, USACE surveys, reservoir sedimentation
               surveys where they exist
    roughness  NLCD-derived Manning n, with burn-modified values
               (see module F)
    structures dam geometry from NID + project design memoranda

## 3. INITIATOR MODULES — swappable, same downstream engine

Each writes only a breach or release hydrograph at one or more nodes. The
routing engine downstream is identical, so modules are comparable.

    MODULE A — SINGLE STRUCTURE BREACH (baseline)
      parametric breach (Froehlich / Xu-Zhang) at each node in turn
      one run per node = the attenuation/amplification matrix

    MODULE B — SEISMIC (Cascadia M9, or crustal source)
      shaking duration 3-5 min, not 15 s
      per-node ground motion from site geology, NOT a single regional
      value
      simultaneous-onset breaches at multiple nodes
      liquefaction of embankment foundations and approach fills
      aftershock sequence: SECOND initiator into an already-damaged
      chain, weeks to a year later

    MODULE C — HYDROLOGIC (excessive event)
      atmospheric-river inflow, rain-on-snow
      overtopping without breach as a distinct case — a real reduction
      in high-risk area, worth its own scenario
      gate-capacity limits: partial opening is INSUFFICIENT to prevent
      cascade at sequential embankment dams; full opening is critical.
      Model partial opening as its own scenario, since it is the
      realistic operator error.

    MODULE D — CYBER / CONTROL FAILURE
      unauthorized or spurious gate operation
      no structural failure required — release schedule is the weapon
      key variables: how many gates, at how many nodes, for how long
        before manual override; and whether SCADA telemetry is
        trustworthy during the event (operators may be routing blind)
      cheapest scenario to run and the one with no seismic prerequisite

    MODULE E — COMBINED
      B or C as trigger, D as compounding (comms down, remote
      operation lost, gates in last commanded position)

## 4. MODULE F — ANTECEDENT CONDITION COUPLING (the amplifier)

This is the part standard breach modeling drops. It is not a refinement;
it changes the cascade outcome at the next
