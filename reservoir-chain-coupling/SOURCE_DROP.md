# Reservoir-chain cascade: the coupling term independent-node evaluation drops

CC0, no rights reserved. Initiator-agnostic. Method-transferable to any
serial impoundment chain.

## CLAIM

Serial reservoir chains are evaluated per-structure. Each node gets its own
design flood, its own breach study, its own emergency action plan scoped to
its owner. This treats nodes as separable. They are not.

    outcome(node n)  IS  the initial condition of  node n+1

The error is not a modeling refinement. It is an operator swap:

    independent-node evaluation:   breach(n+1) = f( max( wave(n), pool(n+1) ) )
    coupled physics:               breach(n+1) = f(      wave(n) + pool(n+1)  )

A wave and a pool that each stay under a breach threshold can cross it
together. `max` cannot see this. `sum` can. The nonlinearity lives in the
threshold, and independent-node evaluation is on the wrong side of it.

## ANTECEDENT STATE — the gain, sampled at event onset (t0)

The buffer at each node is its remaining freeboard. Antecedent conditions
set that buffer BEFORE any wave arrives. They are the gain on the amplifier,
and they are node-specific.

    state(node) = {
        freeboard_m:        crest_elev - pool_elev,      # the buffer itself
        live_storage_frac:  1 - sediment_vol/design_vol, # design overstates buffer
        soil_sat_frac:      basin antecedent moisture,    # sets runoff coefficient
        swe_mm:             snowpack,                      # rain-on-snow gain
        burn_area_frac:     of contributing basin,
        burn_severity:      -> Manning n drop, runoff rise, debris load
        burn_years_since:   recovery decay
        manning_n_mod:      burn-adjusted channel roughness
        ice:                jam / gate-ice risk by season
    }

A node already near crest has no buffer. The arriving wave adds to pool and
crosses a threshold neither term reaches alone. Antecedent state decides
whether a node attenuates the wave or passes it amplified.

## PROPAGATION — one object, downstream order

    ic = boundary_inflow                 # top of chain
    for node in chain_downstream_order:
        h     = hydrograph_at(node)      # 0 unless this node is the initiator
        state = antecedent(node)         # gain
        out   = route(node, ic, h, state)
        ic    = out.downstream_hydrograph  # <-- feeds the NEXT node's IC
        record(out.hazard_field)

The engine `route()` is identical for every initiator. This is what makes
runs comparable and what makes the initiator irrelevant to the gap: the gap
is in the routing topology, not in the trigger.

## WHY IT HAS NO OWNER

Attenuation and amplification only appear ACROSS nodes. A reach study cannot
produce the answer — it is scoped to one structure by construction.

    per-structure EAP  -> planning assigned to the OWNER
    mixed ownership    -> no single entity's plan spans the chain
    -> the aggregation step across the full chain has no owner

Record ownership per node as a data column, not commentary. It is the
governance variable that explains the gap.

## WHAT IS MISSING IS AGGREGATION, NOT TOOLS

    2D unsteady solver         public (USACE HEC-RAS)
    breach parametrization     published (Froehlich, Xu-Zhang)
    terrain / bathymetry       public (3DEP, NOAA, NID)
    roughness                  public (NLCD-derived Manning n)
    exposure                   public (census / LandScan)

Every component is on the shelf. The missing step is holding the full chain
as one object with coupled initial conditions and node-specific antecedent
gain. That step is a study, not a discovery.

## MINIMAL FALSIFIABLE TEST

Run the same chain twice on identical published data:

    RUN 1   each node independent, node takes max(wave, pool)
    RUN 2   coupled, out(n) = ic(n+1), antecedent gain per node

Compare breach set, arrival times, velocity bands. If the breach sets are
identical, the coupling term is negligible and this claim is refuted. If
RUN 2 breaches nodes RUN 1 does not, the operator swap is load-bearing and
per-structure evaluation understates the chain.

## OUTPUT PRODUCTS (response-side, if extended)

    velocity bands   m/s + physical-consequence column   (survival, not depth)
    time slices      t = 1, 6, 24, 72, 168 h             (evac clock, not envelope)
    exposure overlay population on the hazard field       (who, not a side table)
