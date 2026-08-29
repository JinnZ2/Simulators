# Observable-indicator rules from coupled routing

CC0, no rights reserved. Post-processing is stdlib, phone-buildable. The
router (2D unsteady solve) is the only non-phone term.

## THE INVERSION

    UPSTREAM (heavy, once)          HOUSEHOLD (zero compute, every time)
    ─────────────────────          ────────────────────────────────────
    coupled chain solve            a card:
    ensemble over antecedent          IF you see X
    arrival-time field                THEN Y is already true
                                      AND Z arrives in ~T
                                      SO act by <time>, via <route>

Notification is a dependency chain: someone upstream detects, decides,
sends, and the channel reaches — in time. Every link is outside the
household's control. A locally-evaluable rule removes the dependency: it
needs no channel, no compute, no permission from upstream. The household
reads it off what it can see.

## WHAT THE ROUTER MUST EMIT

Not the max envelope. The time-resolved field, per run:

    depth(x, y, t)        # every cell, every timestep
    velocity(x, y, t)
    run_id = (initiator, antecedent_state)   # the ensemble axis

Ordering is the product, not magnitude. Magnitude moves with the scenario;
the SEQUENCE in which places wet is far more stable. The pipeline keeps only
what survives the ensemble.

## PIPELINE

### 1. Landmarks — things a resident can see

    landmark = {
        id:        "county_rd_bridge",
        xy:        (x, y),
        visible_when: depth_threshold_m,   # water over deck / at girders / at
                                           #   a known mark — observable, not gauge
        is_route:  bool,                   # on an evacuation route out
    }
    # sources: resident knowledge, road low points, bridges, bends, known marks.
    # route low points are landmarks too — see step 5.

### 2. Wetting time per landmark per run

    def t_wet(field, lm, run):
        # first timestep depth at lm crosses its visibility threshold
        for t in timesteps(run):
            if depth(field, lm.xy, t, run) >= lm.visible_when:
                return t
        return INF                         # never wets in this run

### 3. Ordering stability across the ensemble  ← the load-bearing check

    # for each run, rank landmarks by t_wet.
    # a rule is only usable if the ORDER holds across the ensemble.
    def stable_pairs(landmarks, runs):
        for A, B in pairs(landmarks):
            order = [ sign(t_wet(A,r) - t_wet(B,r)) for r in runs ]
            if all_same(order):
                yield (A, B, consensus_order)   # A reliably wets before B
            # else: order flips with scenario → NOT a rule, drop it

Pairs whose order flips are magnitude-dependent and cannot be a household
rule. Only invariant orderings become cards. This is what keeps the product
honest.

### 4. Lead-time bands (not point estimates)

    # "20 min to already-happened" is the real spread. Report the band.
    def lead(A, B, runs):
        deltas = [ t_wet(B,r) - t_wet(A,r) for r in runs if both_wet ]
        return {
            "p10": percentile(deltas, 10),   # plan against the SHORT end
            "p50": percentile(deltas, 50),
            "p90": percentile(deltas, 90),
            "min": min(deltas),              # worst case = act-by anchor
        }

Plan against the short end. The card's act-by time uses `min`/`p10`, never
the median.

### 5. Anchor to the household + couple the route  ← the driving insight

    # the route out crosses the same drainages. it can flood before the
    # household does. then "leave when water reaches your door" is fatal.
    def rule_for(H, landmarks, runs):
        t_H     = t_wet(field, H, runs)                 # when H itself floods
        routes  = [lm for lm in landmarks if lm.is_route]
        t_route = min(t_wet(field, lm, runs) for lm in routes)  # route closes
        # the usable trigger is a landmark that:
        #   - reliably wets BEFORE t_route (step 3), and
        #   - leaves enough lead over t_route to complete movement
        trigger = last_landmark_before(t_route - movement_time, stable_pairs)
        return build_card(trigger, t_route, t_H)

If the route closes before the house floods, the trigger is upstream of the
door. The rule says leave on the first indicator, because the water at your
door means the road is already gone.

## OUTPUT — the card (zero compute, no channel)

    ┌────────────────────────────────────────────────┐
    │  IF   water is over <county_rd_bridge>          │
    │  THEN <your road out> closes in ~<min> min      │
    │       your area floods ~<t_H - t_trigger> after  │
    │  ACT  leave now, via <route>, NOT via <closed>   │
    └────────────────────────────────────────────────┘
    # one per community per stable trigger. paper-durable. needs nothing.

## WHY THIS SURVIVES THE FAILURE MODES

    detection down    → rule doesn't need the gauge, needs the bridge
    decision stalled  → rule doesn't wait for an upstream call
    notification late → rule already in hand, evaluated on sight
    route floods first → rule triggers upstream of the door, not at it

The heavy solve is done once, offline, upstream. The household holds a
result, not a computation. That is the only form that survives every link
of the notification chain failing at once.

## FALSIFIABLE

If step 3 finds no stable orderings — every pair flips across the ensemble —
then observable indicators are not derivable for that community and this
method returns nothing rather than a false rule. Empty output is a valid,
honest result.
