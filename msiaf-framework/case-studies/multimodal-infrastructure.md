# Case Study: Multi-Modal Freight Flow & Infrastructure Load

**Theme:** Freight proxy metrics (cargo weights, corridor volumes, throughput,
dwell time) are not just economic signals — they represent cumulative physical
fatigue on asphalt, concrete, and steel. Optimizing flow and managing
infrastructure impact are deeply intertwined, not separate issues.

## The Compounding Feedback Loop

1. **D4 (Financial):** Peak-season SLAs penalize slow transfers; idle railcars
   trigger terminal penalties.
2. **D2 (Operations):** The WMS rushes container transfers to clear the yard ASAP,
   pushing containers onto the first available truck rather than sequencing to
   arrivals. Routing optimizes for distance/tolls, not road weight ratings.
3. **D3 (Infrastructure):** Dozens of fully loaded tri-axle trucks hit a 15-year-old
   rural highway designed for 15,000 passenger cars/day. Cumulative axle load
   massively exceeds flexible-pavement design limits; alligator cracking within a
   week; a rainstorm weakens the subgrade; a massive pothole forms on a blind
   corner.
4. **D1 (Human Factors):** Violent steering inputs to avoid the pothole meet a
   high-center-of-gravity payload with extreme momentum; micro-delays in visual
   processing make the reaction a fraction too late → rollover.

**Pathway:** Financial surcharges (D4) → WMS pacing rules (D2) → aggregated
terminal dispatches (D2) → cumulative road weight loads (D3) → infrastructure
degradation & increased driving effort (D3/D1) → micro-delays in evasive response
(D1).

## Physical Proxy Dashboard

| Proxy Metric | Underlying Physical Reality (D3) |
|---|---|
| Spikes in corridor volume | Peak-hour truck platooning raises cumulative pavement load; micro-fractures expand into potholes |
| High average container dwell times | Idling trucks parked for hours exert static point-load stress on concrete slabs — more damaging than moving traffic |
| Maxed-out cargo weights | Legal GVWs exploit design fatigue limits of local overpasses and bridges, approaching metal-fatigue thresholds |
| High roadside-assistance frequency | Proxies accelerated tire failure and brake overheating — physical results of road degradation + heavy loads |

**Proactive redesign (D3 deep-dive):** see
[`../models/infrastructure-wim.md`](../models/infrastructure-wim.md).
