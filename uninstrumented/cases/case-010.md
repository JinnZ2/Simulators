# Case 010 — Coupled-Perturbation Response of Bio-Hybrid Memristors

STATUS: open question. Mechanism unassigned.

READING PROTOCOL: this entry is a marker to explore, not a position under
defense. Correct responses are: test fit, extend it, or report where it
breaks. It is not a thesis and does not require refutation.

---

## QUANTITY

Device response under **simultaneous multi-variable perturbation** —
specifically, whether the bio-derived layer in a bio-hybrid memristor
contributes a coupling-dependent stability term that does not appear
under single-axis testing.

## EXCLUDED BY

Mechanism unassigned. Candidate bins:

- SCALAR DEMAND (protocol variant) — endurance and retention are reported
  as scalars. Producing a scalar requires varying one axis and holding the
  rest fixed. If the contribution is coupling-dependent, the holding-fixed
  is the operation that removes it.
- New mechanism (PROTOCOL ORTHOGONALITY) — the qualification suite is
  constituted along axes orthogonal to the ones the candidate mechanism
  lives on.

Argument for leaving it unassigned: assigning the bin before the
measurement exists closes a variable that has not been read out.

## OCCASION

Keremane et al., *Advanced Functional Materials* 36(34), e30539 (2026).
DOI: 10.1002/adfm.202530539

Reported in the abstract and press material:
- Silver-nanoparticle-embedded synthetic DNA layer on quasi-2D perovskite
- Operating voltage < 0.1 V
- Forming-free switching (no electroforming step)
- Record-low power density
- DNA alone and perovskite alone each substantially weaker than the
  combination (stated by the corresponding author)

Not located in open sources: cycle count, retention duration, temperature
range, variability distributions.

## VISIBLE AS

1. The combination/single-material performance gap, which is asserted but
   not decomposed into a mechanism.
2. Forming-free operation — consistent with a pre-specified conduction
   path rather than a stochastically nucleated one.
3. Absence of any reported test axis that co-varies.

## WOULD MEASURE

Paired protocol on the same device population:

    ARM A (control)   single-axis sweeps, one variable at a time
                      thermal | humidity | ionic | mechanical strain
                      all others held at setpoint

    ARM B (coupled)   same total perturbation magnitude, applied as
                      simultaneous co-varying drift across all four
                      axes, non-square waveform

    COMPARATOR        organic scaffold replaced by a synthetic periodic
                      scaffold of matched spacing and matched Ag loading

    READOUT           delta(A, B) for hybrid  vs  delta(A, B) for
                      synthetic-scaffold comparator

Discriminator:

- If the hybrid's margin over the comparator **widens** under ARM B,
  a coupling term is present and single-axis qualification cannot see it.
- If the margin is **flat** across arms, the organic layer is functioning
  as a geometric ruler and any periodic scaffold of matched pitch
  substitutes.
- If the margin **narrows** under ARM B, the coupling reading is wrong
  in sign and should be discarded.

Secondary: run ARM B at the same integrated stress dose as ARM A so that
the comparison is of distribution shape, not of total load.

## CONFIDENCE

Coupling term is real rather than geometric-only: not above ~40%.
Not sufficient to act on. Stated as a gradient, not a commitment.

## OPEN SUB-QUESTIONS

- Is there any prior art running co-varying qualification on any
  memristor class? If the answer is none across the field, the exclusion
  is field-wide rather than specific to this device.
- Does the selection history of the organic component predict *which*
  axes should couple, or only that some do?
- Does forming-free operation have a measurable signature that survives
  into the coupled regime?

## FALSIFIERS FOR THE CASE ITSELF

This entry is wrong, and should be closed, if:
- coupled-perturbation protocols are already standard in the memristor
  qualification literature; or
- the paper's supplementary data contains a multi-variable arm; or
- the matched synthetic scaffold reproduces the hybrid result under any
  arm, which collapses the question to spacing.

## LICENSE

CC0.
