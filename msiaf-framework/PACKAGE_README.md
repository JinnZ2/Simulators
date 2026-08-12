# MSIAF — Multi-Dimensional Systemic Incident Analysis Framework

A framework for analyzing and preventing transportation and logistics incidents by
tracing how friction points across **four interlocking dimensions** align to
manufacture outcomes that are typically mislabeled as "driver error" or "worker
inattention."

> Incidents rarely result from a single failure point; they occur when minor
> friction points across multiple dimensions align.

## The Four Dimensions

| # | Dimension | What it covers |
|---|-----------|----------------|
| D1 | **Human Factors & Physiology** | Fatigue, hydration, nutrition, circadian state, cognitive load, visual processing |
| D2 | **Operations & System Design** | Dispatch pressure, routing algorithms, pacing systems, app UX, scheduling |
| D3 | **Infrastructure & Environment** | Road condition, curb policy, intersection geometry, AGV lanes, terminal design |
| D4 | **Financial, Insurance & Regulatory** | Penalty clauses, SLA terms, labor classification, liability structure, insurance incentives |

The cascade typically runs **D4 → D2 → D1 → D3**: financial penalty structures force
rigid dispatch, which degrades the human operator's physiological state, which meets
an environmental hazard that was never communicated or mitigated.

## Repository Contents

### Framework Docs
- [`docs/framework-overview.md`](docs/framework-overview.md) — Core concepts and systemic interconnection pathways
- [`docs/investigation-checklist.md`](docs/investigation-checklist.md) — The 4-phase post-incident investigation protocol

### Case Studies (Reactive Analysis)
- [`case-studies/reefer-trucking.md`](case-studies/reefer-trucking.md) — Long-haul perishable freight: temperature excursion clause → dispatch pressure → fatigue → soft-shoulder run-off
- [`case-studies/last-mile-delivery.md`](case-studies/last-mile-delivery.md) — Urban gig delivery: 2-hour windows → per-package penalties → right-hook cyclist collision; alley backing stress-test
- [`case-studies/warehouse-distribution.md`](case-studies/warehouse-distribution.md) — Fulfillment center: temp-agency split liability → algorithmic pick-rate escalation → 2 AM AGV collision
- [`case-studies/maritime-port.md`](case-studies/maritime-port.md) — Intermodal port: demurrage clocks → chassis pool fragmentation → automation blind zones
- [`case-studies/multimodal-infrastructure.md`](case-studies/multimodal-infrastructure.md) — Corridor freight volume → pavement fatigue → infrastructure degradation pathway

### Proactive Safety Models
- [`models/reefer-financial-redesign.md`](models/reefer-financial-redesign.md) — Graduated penalty curves, shared risk pools, dispatcher incentive recalibration, dynamic underwriting
- [`models/last-mile-architecture.md`](models/last-mile-architecture.md) — Full D1–D4 redesign + alleyway stress-test + residual risks
- [`models/warehouse-architecture.md`](models/warehouse-architecture.md) — Joint-employer liability, zero-cross routing, UWB proximity, enforced rest lockouts
- [`models/infrastructure-wim.md`](models/infrastructure-wim.md) — Weigh-in-motion sensors, load-aware routing, V2I geofenced warnings

### Proxies (Early-Warning Indicators)
- [`proxies/proxy-catalog.md`](proxies/proxy-catalog.md) — Leading-indicator proxies across rail, ports, waterways, light-duty, freight corridors, and drone logistics

## Investigation Protocol (Summary)

Investigators must evaluate all four phases sequentially before drawing conclusions:

1. **Environmental Audit** — physical conditions, road hazards, maintenance status
2. **Information Feed Verification** — accuracy/latency of GPS, weather, dispatch data
3. **Operational Context Review** — dispatch logs, timing constraints, incentives, shift history
4. **Physiological Baseline Assessment** — duty hours, food/hydration access, rest quality

## Design Principle

The proactive models invert every failure point: the same D4→D2→D1→D3 cascade that
manufactures incidents is rewired from **pressure to protection**, so that safety
becomes the path of least resistance — not a heroic individual act.

## Status

Work in progress. Known open threads:
- Legal drafting for a Joint-Employer Safety Liability standard
- Cross-platform fatigue ledger regulatory mechanics
- V2I communication standards for infrastructure-to-vehicle links
- Drone delivery corridor integration into the framework
