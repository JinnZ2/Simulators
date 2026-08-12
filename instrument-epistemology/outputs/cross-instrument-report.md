# Cross-Instrument Comparative Report

Six instruments, one question each: how does it know what it claims to know?

| Instrument | Domain | Rung | Chain fidelity | Traceability | Blind spots | Grounded | Verdict |
|---|---|---|---|---|---|---|---|
| Broadband seismometer network | physics | M1 | 0.800 | measured | 3 | 0.83 | well grounded |
| Satellite thermal IR radiometer | physics | M3 | 0.504 | measured | 3 | 0.58 | partially grounded |
| Airborne LiDAR | ecology | M2 | 0.514 | estimated | 3 | 0.58 | partially grounded |
| Camera trap array | ecology | M2 | 0.293 | estimated | 3 | 0.42 | mostly assumed — investigation incomplete |
| IRMS + isotopic mixing model | biology | M2 | 0.275 | measured | 3 | 0.42 | mostly assumed — investigation incomplete |
| eDNA metabarcoding assay | biology | M2 | 0.165 | estimated | 4 | 0.42 | mostly assumed — investigation incomplete |

## What separates the top from the bottom

1. **It is not the hardware.** The eDNA sequencer and the IRMS are as precisely built as
   the seismometer's digitizer. The difference is everything around the hardware:
   transduction chain, bridge model, reference standards, blindness map.
2. **Traceability is the strongest lever.** Both SI-traceable instruments (seismometer,
   SST radiometer via buoy network) sit at the top. Every instrument without a primary
   standard or reference population caps at 'estimated' no matter how good the sensor.
3. **Model rung predicts groundedness.** M1 (calibrated reading) > M2 (model-derived) >
   M3 (inverted). The reported quantity's rung is the single best predictor of how much
   of the 'measurement' is actually a model output.
4. **Every instrument has blind spots — the difference is whether they're mapped.**
   Even the seismometer has three (magnitude-completeness gate, station geometry frame,
   site-amplification alias). Well-grounded instruments know what they can't see.
5. **Forward simulation separates honest pipelines from lucky ones.** The naive
   seismometer pipeline fails; the response-deconvolved one recovers truth exactly.
   The ecology instruments fail at their *bridge model* stage, not their sensors.

## The pattern

Physics instruments know more not because nature is simpler there, but because
decades were spent building *standards, traceability chains, and response models*.
Ecological and biological instruments are at the M2 frontier: their instruments are
already excellent; what is missing is the institutional layer — reference standards,
inter-lab comparisons, and published blindness maps.