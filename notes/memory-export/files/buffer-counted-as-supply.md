---
name: buffer-counted-as-supply
description: Marker under exploration — systems where a depleting buffer (frozen storage, aquifer elasticity, skill base) is counted as supply, so the aggregate metric holds until an abrupt threshold.
sources: [field]
aliases: [buffer as supply, masking buffer, southwest aquifer, inelastic transition, stock vs flow]
---

MARKER, not a position under defense.

## The shape

A system runs on a STOCK built over long timescales. The managing layer measures only FLOW.
The stock reads as free, and its drawdown appears in the metric as normal — sometimes even as
recharge. The aggregate holds, occasionally improves, right up to a threshold, then does not
recover.

Parent shape in [[median-case-calibration]] (substrate depletion). Instrument side in
[[uninstrumented]].

## Directional read, uncoalesced

The southwest US is expected to undergo changes similar in kind to the Asian Water Tower case
— "unexpected" meaning not expected to be as severe as they will be.

## Supporting cases in the literature (retrieved, re-verify)

- **Sacramento Valley** — satellite radar plus GPS plus groundwater and geology, 2016–2022:
  elastic behavior through the wetter 2016–2020 period, then abrupt acceleration in 2021
  during the 2020–2022 drought. Subsidence several decimetres per year faster than estimated
  recoverable deformation; large areas entering an inelastic regime. **Elastic and inelastic
  compression look identical on the instrument until one stops reversing.**
- **High Mountain Asia** — roughly 24.2 Gt/yr groundwater loss, about two-thirds of the region
  declining 2003–2020, steepest in Ganges-Brahmaputra, Indus, Amu Darya. Climate explains
  about half the variability; human withdrawal increasingly dominant after 2010. Stated buffer
  term: glacier melt may soften the decline around the 2060s, then depletion accelerates —
  an "unsustainable buffer effect." Localized interior-plateau gains are attributed to
  precipitation plus glacier-melt and permafrost-thaw infiltration — a one-way transfer from
  the frozen stock appearing as a POSITIVE number in the groundwater column.
- **Instrument caveat on that water balance:** analysis argues observed precipitation is
  substantially underestimated (wind-induced gauge undercatch, sparse and uneven gauge
  density), producing evapotranspiration-exceeds-precipitation and runoff coefficients above
  0.5.

## Why the southwest read is structurally defensible (extension, not the original marker)

Same three-part stack: frozen seasonal buffer (snowpack); surface allocation set on a
wet-anomaly baseline (the Colorado compact); aquifer as the unpriced shock absorber.

Two error sources, both biased optimistic, and both wrong AT the transition rather than
gradually:

1. Aquifer capacity can go inelastic abruptly, so projections treating storage as a linear
   reserve overshoot. Past yield, **the container is gone, not just the water.**
2. Warming shifts snowpack toward rain and early runoff, so the buffer stops FUNCTIONING as
   storage before it stops EXISTING as water.

## Measurement to run

Subsidence rate vs estimated recoverable deformation, per basin — the Sacramento comparison
applied to Central Valley and Willcox-type basins. If a basin is already past that line, then
projections built on recoverable storage describe a container that no longer exists.

Data path: InSAR plus GPS plus groundwater records. Same instrument set as the Sacramento work.
