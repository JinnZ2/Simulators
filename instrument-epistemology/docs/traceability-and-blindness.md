# Traceability, Model-Dependence, and Blindness

## The Traceability Pyramid

```
        SI definition (physical constant / procedure)
              ↑ realization
        Primary standard (national metrology institute)
              ↑ calibration
        Reference standard (lab)
              ↑ calibration
        Working standard (field)
              ↑ calibration
        Instrument indication
```

Every arrow is a link with its own uncertainty. **A broken arrow anywhere means
the reading floats free of the SI.** Many ecological measurands (biomass,
biodiversity, habitat complexity) have *no primary standard at all* — the chain
terminates at an inter-lab comparison or a convention. That is not a scandal;
but it must be recorded as `estimated`, never `measured`.

## The Model-Dependence Ladder

| Rung | Name | Uncertainty dominated by | Example |
|---|---|---|---|
| M0 | Direct indication | Instrument physics | voltage from thermocouple |
| M1 | Calibrated reading | Reference standard quality | temperature from calibrated thermometer |
| M2 | Model-derived | Empirical model transferability | biomass from LiDAR height metrics + allometry |
| M3 | Model-inverted | Inverse-problem assumptions + priors | subsurface structure from seismic inversion |

Rule: **report the rung.** A biomass number without "M2, allometry from 42
harvested trees in Panama" is an instrument reading pretending to be a fact.

## The Blindness Taxonomy

| Type | Definition | Example |
|---|---|---|
| **Null state** | Nature configuration yields no signal | eDNA: species absent from reference library → reads as absent even when present |
| **Alias state** | Distinct states yield identical signal | camera trap: 1 animal passing 10× ≡ 10 animals passing 1× without ID |
| **Saturation** | Response flattens above threshold | LiDAR saturates in dense canopy: upper strata invisible |
| **Gate** | Upstream threshold converts "not detected" to "absent" | qPCR cycle cutoff; minimum detection size in nets |
| **Frame** | Sampling design defines what exists | plots placed on accessible terrain systematically miss steep habitat |

## The Meta-Rule

**Absence of signal is evidence of absence only to the extent the blindness map
is empty.** Every investigation must end by stating what the instrument cannot
see — otherwise "no detection" silently becomes "no phenomenon," which is the
oldest error in empirical science.
