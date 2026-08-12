# MSIAF Proxy Catalog — Comparative Grounding Report

Prior grading of all cataloged proxies through the lab protocol.
Sorted by grounded fraction (how much of the chain is measured vs assumed).

| Rank | Proxy | Mode | Chain fidelity | Grounded | Weakest link | Verdict |
|---|---|---|---|---|---|---|
| 1 | river-water-level | waterway | 0.931 | 1.00 | level->clearance | well grounded |
| 2 | river-draft-limits | waterway | 0.874 | 1.00 | depth->limit | well grounded |
| 3 | freight-corridor-volume | corridor | 0.810 | 1.00 | volume->axle spectrum | well grounded |
| 4 | port-dwell-time | port | 0.525 | 0.83 | dwell->risk pressure | well grounded |
| 5 | rail-unplanned-maintenance | rail | 0.765 | 0.75 | degradation->failures | partially grounded |
| 6 | rail-speed-restrictions | rail | 0.720 | 0.75 | defect->inspection finding | partially grounded |
| 7 | ldv-service-trips | light_duty | 0.510 | 0.75 | pressure->dispatch volume | partially grounded |
| 8 | ldv-congestion-time | light_duty | 0.713 | 0.75 | strain->delay | partially grounded |
| 9 | freight-terminal-throughput | intermodal | 0.713 | 0.75 | pressure->volume | partially grounded |
| 10 | freight-container-dwell | intermodal | 0.760 | 0.75 | friction->dwell | partially grounded |
| 11 | port-cargo-damage | port | 0.476 | 0.67 | protocol->handling quality | partially grounded |
| 12 | ldv-roadside-calls | light_duty | 0.504 | 0.67 | deferral->failure | partially grounded |
| 13 | wh-late-fee-waivers | port | 0.532 | 0.67 | lateness->waiver | partially grounded |
| 14 | wh-temp-turnover | warehouse | 0.297 | 0.50 | hazard->quit intent | partially grounded |
| 15 | behavior-venue-congestion | behavioral | 0.385 | 0.25 | purpose->timing | mostly assumed — investigation incomplete |
| 16 | drone-corridor-density | aerial | 0.480 | 0.25 | density->conflict | mostly assumed — investigation incomplete |

## Reading the table

- **Chain fidelity** is multiplicative across the causal chain — a proxy with one
  assumed 0.55 link cannot exceed it, no matter how good the sensor is.
- **Grounded fraction** weights measured=1.0, estimated=0.5, assumed=0.0 per link.
- Bottom-of-table proxies are where investigation effort pays off most:
  they are *used* in MSIAF reasoning but rest on assumed links.

## Priority queue for full investigations

1. **ldv-roadside-calls** (grounded 0.67) — weakest: deferral->failure
1. **wh-late-fee-waivers** (grounded 0.67) — weakest: lateness->waiver
1. **wh-temp-turnover** (grounded 0.50) — weakest: hazard->quit intent
1. **behavior-venue-congestion** (grounded 0.25) — weakest: purpose->timing
1. **drone-corridor-density** (grounded 0.25) — weakest: density->conflict