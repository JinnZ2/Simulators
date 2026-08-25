---
name: periodicity-break-axis
description: Cross-domain marker tested by simulation — quasi-periodic photonic crystal laser vs tungsten collision-cascade damage; SIM-B box-counting results in, SIM-A and SIM-C failed audit.
sources: [field]
aliases: [QPCSEL, quasi-periodic photonic crystal, tungsten cascade, SIM-A, SIM-B, SIM-C]
---

MARKER, not a position under defense. Two papers — a quasi-periodic photonic crystal laser, and
tungsten radiation damage / collision cascades — brought as a shape to explore.

**Method choice: test the shape by SIMULATION rather than by argument.**

## SIM-B (box-counting fractal dimension) — stands

- Ammann-Beenker D_f = 1.889
- Synthetic cascade D_f = 1.555
- Controls: Poisson 1.911; periodic lattice 1.964; line 1.000

Corrected on audit: plateau-based separation is about 4.5x cluster spread, not the 15x
originally reported.

## SIM-A — BROKEN

The AB structure factor shows only the k=0 forward peak. Bragg peaks were missed by k-grid
aliasing, and no periodic-lattice control was run. The reported "68 peaks" and alpha = -1.529
are finite-aperture ringing.

## SIM-C — BROKEN

The knee / E_split ratio is a units mismatch, and the 16x16 grid is too small.

## Scope limit

The cascade point set is a SYNTHETIC BRANCHING WALK, not molecular dynamics. **No claim about
tungsten is supported by any of it.**

## Live question after the audit

The GEOMETRY version of the axis is closed. The "periodicity-assuming models fail where
symmetry breaks" version is untested — and needs a RESIDUAL test, not a point-set test.
