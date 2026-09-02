# removal-closure

A pre-registered work order, delivered verbatim in `WORK_ORDER.md`,
about a METHOD: how claims of coupling between an environmental
constant and a biological rhythm reach closure, and whether
removability of the constant predicts time-to-closure. No mechanism is
proposed and no coupling is asserted, here or in the order.

Two instruments, one stdlib file each.

**`removal_closure.py`** computes what the order's procedure asks for
from a flat CSV in its schema — years to closure, the three
falsification rules with `undetermined` where they cannot run, Cramér's
V imported from `label-position-test`, Spearman imported from
`readout-count`, and a pre-registration hash over the removability
coding. **No data ships.** The five seed rows are read back from the
order and 0 of 5 count by its own rule; their years-to-closure column
is checked against their own year cells and comes back consistent.

**`rhythm_gaps.py`** runs the order's attached gaps where they can be
run. The dataset they point at is on GitHub and was reachable — the
first in this family — so G2 (pause threshold) and G3 (distribution
shape) are computed on its intermediate table, and G1, G4, G5, G6, G7
are stated not-run with the reason from the repository's own scripts.
The dataset is not checked in; its sha256 and the upstream commit are
printed, and the pinned run is in `samples/`.

    python3 removal-closure/removal_closure.py                       # unfilled, seed readiness + arithmetic
    python3 removal-closure/removal_closure.py --csv ROWS.csv        # the numbers
    python3 removal-closure/removal_closure.py --csv ROWS.csv --precode   # the P2 digest
    python3 removal-closure/rhythm_gaps.py --csv unsplit_ioi_...csv --commit <hash>
    RHYTHM48_CSV=path/to/unsplit_ioi_...csv python3 removal-closure/selftest_rmc.py

Two headline numbers from the gaps, both properties of the file:

- **G2.** The upstream split applies no minimum pause; the shortest
  trailing pause in the table is 0.001 s. Re-merged at 0.50 s the
  analysed unit's mean moves from 2.257 s to 3.531 s. The direction is
  fixed by construction; the size is the measurement.
- **G3.** The right-tail ratio (p95 − median) / (median − p05) exceeds
  1 in 49 of 49 languages, 1.46–2.64 on the analysed unit and 2.10–3.41
  on the speech run.

| file | what |
|---|---|
| `WORK_ORDER.md` | delivered verbatim |
| `removal_closure.py` | the main-table instrument |
| `rhythm_gaps.py` | the attached gaps, G2 and G3 run |
| `selftest_rmc.py` | known answers first, both directions; pins the dataset numbers when the file is present |
| `CLAIM_TABLE.md` | `RMC_001..RMC_011` |
| `samples/` | constructed rows, pinned renders, the dataset run |

Both instruments refuse `--selftest`. Renders screen clean through the
repo's `no_severity` with no exemption. No author section. Stdlib only,
parses under 3.9, runs on a phone, CC0.
