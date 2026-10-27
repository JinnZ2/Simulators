# Case 024: write latency of cumulative all-optical switching

## QUANTITY

The total elapsed time from first pulse on a region to a stable, fully
reversed magnetic domain (write latency), together with the minimum pulse
count that makes reversal deterministic. Neither quantity is reported in
the UCSD vector-beam study or its supplement; the supplement quantifies
energy and pulse density but not a completion time.

## EXCLUDED BY

- **MODALITY** The readout is a post-sweep Faraday microscope image: a
  spatial record acquired after the process has finished. The instrument
  holds a two-dimensional state, not a time series; the time axis of the
  write was spent as a scanning parameter (sweep speed 1-30 um/s at 1
  kHz), never as a measured observable. The domain-arrival time is
  not collected; the observation cannot contain it.
- **BUDGET BOUNDARY** The 1 kHz regenerative amplifier fixes the
  inter-pulse interval at 1 ms. Latency components below 1 ms per pulse
  are excluded by the source's constitution, not by the material's
  recovery - the thermal recovery time of the film is itself
  uninstrumented, and is bounded above, not below, by the laser.
- **SCALAR DEMAND** Speed is reported as a single ratio ("more than
  1,000x faster") read off the femtosecond pulse duration. The
  cumulative multi-pulse process is collapsed into that one number, so
  no decomposition of latency into pulses, recovery, and domain growth
  survives into the report.

## OCCASION

The UC San Diego study of optical beam shaping induced reconfigurable
magnetic domains (Khalid et al., Nature Communications 17, 10843,
September 2026), and the press coverage of it. The headline speed claim
is prospective, not measured; the paper's own evidence establishes the
write is cumulative (roughly 200-2,000 pulses per illuminated area at
1 kHz), which is orders of magnitude slower than a single 120 fs pulse.

## VISIBLE AS

The quantity reappears as a smell: a femtosecond number attached to a
seconds-scale process, and as the absence of any write-completion
measurement in a study whose purpose is fast memory. It also appears
as the unexplained persistence of the multi-pulse requirement - the
number of pulses needed is set by sweep speed rather than measured,
so the time budget of the write is unknown even in principle to the
experiment that established it.

## WOULD MEASURE

Time-resolved magneto-optical imaging with ns-to-us framing (pump-probe
Faraday/Kerr or single-shot multislice imaging), reporting
reversal-probability-per-pulse-count curves at fixed spot size and
fluence, plus time-resolved reflectivity for inter-pulse thermal
recovery. Two discriminators separate the regimes: if reversal
probability per additional pulse is flat, the write is a nucleation-and-
growth accumulation whose latency is pulse count times inter-pulse
interval; if there is a sharp threshold pulse count, the minimum write
time is that count times the interval, and the recovery time becomes the
binding quantity below it.

## CONFIDENCE

The exclusion is real (nothing in the paper or supplement measures a
write time): about 85%. That the true write latency is faster than
roughly a second per spot under the reported conditions: not above
about 30%. These are independent claims.

## OPEN SUB-QUESTIONS

- What is the minimum pulse count for deterministic reversal at each
  spot size and N, and is it set by thermal accumulation or by domain
  growth?
- What is the thermal recovery time of a [Pt/Co]N film between 800 nm,
  120 fs pulses, and does it, rather than any laser, set the repetition
  ceiling for continuous writing?
- Does domain growth continue between pulses (accumulating), or does
  each pulse fully reset the thermal state (independent trials)?

## FALSIFIERS FOR THE CASE ITSELF

- The study or supplement contains a time-resolved reversal
  measurement I have missed (it does not as of the version of record,
  October 2026).
- A prior work measured cumulative multi-pulse AOS write latency for
  Pt/Co multilayers under comparable conditions, making this a
  literature gap rather than a case (single-shot ferrimagnetic AOS
  timing is well measured; this regime is not).
- The sweep conditions imply a completion time directly from the
  reported data (they bound it only from above, via pulse counts).

License: CC0. Grounded in the version of record and supplement of
Khalid et al. (2026) as read on 2026-10-27, and the UC San Diego Today
coverage dated 2026-09-28.
