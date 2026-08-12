# Post-Incident Investigation Checklist

Investigators must evaluate all four phases **sequentially** before drawing any
conclusion regarding cause or accountability. The default output of this protocol
is a systemic-failure determination, not an individual-blame determination.

## Phase 1 — Environmental Audit
Document live physical conditions, surrounding vehicle behaviors, physical road
hazards, and the status of local municipal maintenance in the area.

*Evidence types: road geometry vs. current design guides (NACTO/AASHTO), soil
compaction tests, sidewalk/transit-stop placement records, loading-zone ordinances
and their underlying studies, deferred-maintenance records.*

## Phase 2 — Information Feed Verification
Assess the accuracy and latency of all data provided to the operator (GPS feeds,
weather warnings, dispatch alerts, app notifications) relative to actual ground
conditions.

*Evidence types: route-calculation timestamps vs. weather-alert issuance, ELD
urgency flags, in-cab notification logs vs. incident timeline, algorithmic inputs
(what the routing/pacing model did and did not account for).*

## Phase 3 — Operational Context Review
Audit dispatch communication logs, route timing constraints, financial
incentives/penalties tied to the load, and shift histories.

*Evidence types: explicit dispatch messages, per-stop time allocations, reliability
scores and suspension thresholds, compensation structures of dispatchers/managers,
contractor agreements vs. actual behavioral control, break-exemption clauses.*

## Phase 4 — Physiological Baseline Assessment
Review total duty hours, access to nutritional food and hydration during the trip,
rest break quality, and overall shift duration.

*Evidence types: duty logs, sleep conditions (e.g., cab sleeping in extreme heat),
food access at directed stops, fatigue-equivalence modeling (e.g., BAC-equivalent
reaction-time degradation), cognitive-load reconstruction of the final seconds.*

## Determination Pattern

The finding names the alignment, not the individual:

> *"The financial penalty structure (D4) forced a rigid dispatch schedule (D2) onto
> a driver in poor physiological state (D1), navigating an environmental hazard
> never communicated due to stale data (D3)."*
