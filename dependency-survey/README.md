# dependency-survey

A work order delivered verbatim in `WORK_ORDER.md`, built as it asks: a
fixed five-term set applied across five substrates, cell by cell, to
locate terms MEASURED in one substrate and MISSING in another (an
experiment sitting there) and terms behaving differently because of the
SCOPE. A survey instrument, not an argument — it emits coded cells and
the gaps that fall out of them, and does not conclude that the
substrates share structure.

The load-bearing constraint, in two bars (`ADDENDUM_01`, a RESCOPE not a
narrow): **a MEASURED cell must carry a MEASURED_AS that states units;
a SCOPE-DIFFERENT cell must carry a SCOPE_TRANSFORM** — `reference` /
`maps_to` / `breaks_at`, **not units** — because frame information is not
denominated in the quantity's units. A MEASURED cell with no units
downgrades to MISSING; a SCOPE-DIFFERENT cell with a prose note and no
complete transform downgrades to UNKNOWN, counted apart from the
never-coded UNKNOWN cells. That is what keeps the table from becoming a
vocabulary map, and it is the E7 cross-substrate table of
`cooperative-substrate/` (`CSP_019`) with the admissibility bar made
enforceable.

The cell store is `CELLS.md`, human-editable, one block per coded cell;
`survey.py` parses it, so a cell recodes without touching code. A cell
not in `CELLS.md` is UNKNOWN.

    python3 dependency-survey/run_all.py          # the full report
    python3 dependency-survey/survey.py           # the grid, validity flagged
    python3 dependency-survey/gaps.py             # the gap list
    python3 dependency-survey/selftest_ds.py

| file | what |
|---|---|
| `WORK_ORDER.md` | delivered verbatim |
| `ADDENDUM_01.md` | delivered verbatim; rescopes the SCOPE-DIFFERENT bar |
| `CELLS.md` | the coded cells, human-editable data store |
| `survey.py` | the 5×5 grid, the two admissibility bars, validation |
| `gaps.py` | gap derivation, transfer questions, NO-TRANSFER |
| `report.py` | table, cell records, gap list, UNKNOWN + scope-incomplete counts |
| `run_all.py` | emits the full report |
| `CLAIM_TABLE.md` | `DS_001..DS_008` |

## What the seed produces

Three cells are coded (the order's seeds); 22 are UNKNOWN, reported as a
count and listed, kept apart from MISSING — absence and not-yet-looked
are different results (`DS_004`).

- **`DS_002`, the sharp one, and its rescope:** the seed's own `T3 x S5`
  was coded SCOPE-DIFFERENT with a scope note and no MEASURED_AS. The
  first-run instrument caught its own work order on that cell, and
  `ADDENDUM_01` is the branch record: it **rescopes** the rule rather
  than patching it — SCOPE-DIFFERENT now needs a SCOPE_TRANSFORM
  (`reference` / `maps_to` / `breaks_at`), not units, because a
  "measured, but the frame differs" status reports frame information,
  which is not in the quantity's units. **The seed still fails**, now
  against the adjusted rule (a prose note, no transform), and downgrades
  to UNKNOWN, counted on its own line. It did not fail the units rule; it
  fails the rule that should have been written (`DS_008`). Detected by
  the validator, left in `CELLS.md` as delivered, not repaired.
- **`DS_003`:** exactly one gap falls out — `T1` (cost asymmetry)
  validly MEASURED in `S1` (energy per handling time, J/s), MISSING in
  `S2` (multiagent harnesses), PROVISIONAL and OPEN with the transfer
  question stated in `S2`'s own units. This is `CSP_019`'s worked
  example ("cost asymmetry measured in foraging, missing in harnesses")
  with the units on the measured side and the transfer question left as
  the research queue. NO-TRANSFER and TRANSFER-STATED are reachable
  (coded on the target cell), so the gap list is not a constant.

## Envelope

Valid for locating gaps and scope-differences across coded cells; not
valid for concluding shared structure — the discriminator (real shared
structure vs projected frame) is applied later against transfer
*results*, which do not exist yet (`DS_007`). The units heuristic is
lexical and stated at its callsite (`DS_005`). No term requiring intent
is added. Stdlib only, parses under 3.9, phone-buildable, CC0.
