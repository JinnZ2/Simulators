# Case Study: Warehouse / Distribution Center — The 2 AM AGV Collision

**Incident type:** Temporary order picker struck by an Automated Guided Vehicle
(AGV) in a shared aisle; compound femur fracture / crushed foot and pelvic injury.
Recorded as *"contractor error — stepped into active AGV right-of-way."*

## Setup

Regional fulfillment center, peak season. A 28-year-old picker employed through a
third-party staffing agency works an 11-hour overnight shift on an electric pallet
jack in aisles shared with laser-guided AGVs. At 2:15 AM (hour 9), reaching into a
bottom rack for a 42 lb box at a 220 picks/hour pace, they step backward into the
travel lane and are struck by an AGV carrying a 1,200 lb pallet.

## Alignment of Friction Points

### D4 — Financial & Contractual
- **Split-liability staffing:** 45% of peak labor via temp agency, which carries
  primary Workers' Comp while the facility operator holds floor control. The
  operator faces minimal premium impact from injuries — disincentivizing capital
  investment in physical separation.
- **SLA penalties:** Liquidated damages for missed same-day dispatch deadlines
  cascade to floor management; throughput is the sole bonus metric.

### D2 — Operations & Algorithmic Management
- **Dynamic rate escalation:** WMS auto-adjusts from 140 to 220 picks/hour at peak;
  wrist scanner shows per-item countdown, vibrates and logs a "productivity strike"
  beyond 16 seconds; three strikes = assignment termination.
- **Shared-corridor routing:** Traffic software routes high-speed AGVs through
  human picking aisles to optimize floor space, rather than segregated lanes.

### D3 — Physical & Automated Environment
- **Rack geometry blind spots:** Deep-rack storage forces pickers fully inside the
  rack frame — an inevitable blind spot on exit.
- **Sensor limitation + acoustic overload:** AGV lidar calibrated horizontally at
  12 in above floor (to avoid false stops from plastic wrap) misses a
  waist-level/upper-body projection until 18 in from impact. Ambient noise >84 dBA
  renders the backup beeper indistinguishable.

### D1 — Physiology & Biomechanics
- **Circadian trough:** 2:15 AM — reaction times slowed up to 300 ms.
- **Nutrition/hydration deficit:** Skipped midnight break to protect pick rate;
  low blood glucose and dehydration narrow peripheral vision (tunneling) and
  compromise core stabilization — the extra backward step balancing the 42 lb load.

## Comparative System Analysis

| Evaluation Focus | Legacy Reactive Model | MSIAF Proactive Industrial Architecture |
|---|---|---|
| Incident cause | Worker inattention / failure to look | Algorithmic over-pacing, blind rack geometry, shared AGV lanes, split-liability staffing |
| Legal liability | Liability pushed to temp agency; operator avoids Workers' Comp impact; high SLA pressure | Joint-employer safety liability; SLA clauses protected against safety-driven slowdowns |
| Operations & pacing | Dynamic pick rates accelerating at peak (220 units/hr); shared corridors | Ergonomically bound rates adjusting to fatigue and shift time; absolute spatial segregation |
| Infrastructure & automation | Shared lanes, line-of-sight LiDAR, masked beepers, blind corners | Interlocking barriers; 3D UWB non-line-of-sight proximity slowdowns; visual floor projections |
| Physiology & rest | Unmonitored breaks; rest skipped to avoid termination | System-enforced scanner lockouts; exoskeleton assistance for heavy picks |
| Investigation | Blames worker technique; retraining module | Audits WMS pacing, agency contracts, UWB data, floor geometry |

**Proactive redesign + stress-test:** see
[`../models/warehouse-architecture.md`](../models/warehouse-architecture.md).
