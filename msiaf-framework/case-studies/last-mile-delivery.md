# Case Study: Urban Last-Mile Delivery — The Right-Hook Cyclist Collision

**Incident type:** Delivery van right-turn across a bike lane; cyclist struck
(fractured clavicle, concussion). Recorded as *"driver error — failure to yield."*

## Setup

A gig-platform driver (independent contractor) runs 47 stops in a 3-hour block,
with "Premium" 2-hour windows on several packages, in a rented cargo van. At 4:52
PM, turning right across a painted bike lane on a four-lane arterial, they strike
a cyclist traveling straight.

## Alignment of Friction Points

### D4 (Financial/Insurance/Regulatory) → D2
- **Misclassification as pressure cooker:** Per-package pay, no breaks, no overtime.
  One late delivery drops the On-Time Reliability Score below 97% → 3-day platform
  suspension. Every traffic law, rest break, and mirror check is a direct financial
  loss.
- **Insurance punishes safety:** Contingent platform liability above the driver's
  personal commercial policy; $2,500 deductible; premiums double after any report.
  Rational incentive to avoid reporting and to take delay-avoidance risks.
- **Receiver-side penalties:** 15-minute window miss = 6% chargeback, passed
  straight to the driver via the reliability score.

### D2 (Operations) → D1
- **Algorithmic density without slack:** 3.8 minutes/stop average, assuming legal
  parking within 50 feet and instant curb-to-door transit. Live countdown nags:
  *"You are 2 stops behind schedule."*
- **No mandated rest:** Contractor classification exempts meal/rest breaks. Six
  hours on soda and chips degrades visual scanning and decision-making.
- **Cognitive fragmentation:** Navigation app, scan-and-photograph interface,
  dispatch messages, and blind-spot mirrors compete; phone mounted low, pulling
  gaze down and right.

### D3 (Infrastructure & Municipal Design)
- **Trap bike lane:** Dashed merge 50 ft before the intersection invites drivers
  into the bike lane; no green box, no protected geometry, no leading bicycle
  interval. The design creates a high-conflict weave at the cyclist's blind-spot
  moment. (Predates protected-intersection guidance; known to increase right-hook
  collisions ~35% vs. corner-protected designs.)
- **Missing sidewalk + bus stop:** Deferred sidewalk (1997 drainage easement
  dispute) means bus passengers step directly into the bike lane — further
  attention fragmentation.
- **Loading-zone policy:** Two 30-minute commercial zones on a 1.2-mile strip,
  both occupied at peak; $250 fine for the bike lane; stopping in a travel lane
  is a moving violation. The code *trains* drivers to roll through the bike lane
  and then swerve across it.
- **Signal phasing:** Right-on-red permitted, no dedicated turn arrow, no bicycle
  signal head — a predictable conflict every 90 seconds.

### D1 (Human Factors, at the Moment)
- 5 hours into the shift, no meal, mild dehydration, rising cortisol from the
  countdown. Useful field of view narrowed; stereotyped glances instead of true
  head-checks.
- The *"behind schedule"* chime fires 2.3 seconds before turn initiation, pulling
  a reflexive 0.8-second gaze to the screen — the interval in which the cyclist
  enters the right-front blind spot.

## Investigation Findings (per checklist)

1. **D3 audit:** City's 2018 Complete Streets policy exempted arterials from
   protected-facility retrofits on cost grounds — codifying a known high-conflict
   design. Missing sidewalk was a 2012 Tier 1 priority, defunded in 2020. Loading
   zones sized on 1985 commercial-density studies.
2. **Feed verification:** Route optimizer used suburban completion times; no
   fields for parking search time, bike-lane congestion, or intersection conflict
   risk. No safety lockout of non-critical alerts while moving.
3. **Operational review:** Back-to-back 3-hour blocks; contractor agreement claims
   driver "sole discretion" while real-time routing, windows, and penalties amount
   to behavioral control — a regulatory loophole enabling tempo enforcement without
   duty of care. Internal comms show the company knows drivers skip rest and
   double-park to protect scores.
4. **Physiological assessment:** 5.5 hours of vehicle sleep, last full meal 9
   hours prior — fatigue equivalent to ~0.05% BAC reaction-time degradation. Five
   simultaneous visual tasks demanded in the final 4 seconds.

## Takeaway

> A regulatory ecosystem that classifies the driver as an independent contractor
> (D4) freed the platform to impose 2-hour windows with per-package penalties (D4),
> creating an app that nags for speed at the intersection (D2), while compelling a
> sleep- and nutrition-deprived state (D1). Municipal code forced the driver into
> the bike lane to search for parking (D3) on a road whose cost-exemption preserved
> known right-hook geometry (D3). The cyclist's injury was designed into the system
> long before the driver turned the wheel.

**Proactive redesign + alleyway stress-test:** see
[`../models/last-mile-architecture.md`](../models/last-mile-architecture.md).
