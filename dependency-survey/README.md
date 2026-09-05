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

`ADDENDUM_02` **narrows** the units bar (its own frame note: narrow, not
rescope): a units field naming a data **TYPE** (`boolean`, `verdict`,
`integer`, `unitless`, `dimensionless`) with no **CUT** (a threshold,
band, or comparison target) does not satisfy it — a type carries no
scale two coders can disagree about. A type-only cell downgrades to
MISSING with its own reason and is counted on its own
`measured_type_only` line in the report, visible as a zero when zero (the
same shape as the scope-incomplete line). Dimensionless is not the
problem; thresholdless is. The CUT need not be numeric — the addendum's
own repair `float magnitude; cut at non-finite` passes. On this repo's
seed the count is zero; the RE-CODING scope is an external corpus (the
Kimi falsifier survey Run 2), not held here (`DS_010`).

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
| `ADDENDUM_02.md` | delivered verbatim; narrows the units bar (type vs scale) |
| `RESULT_taxonomy_crossmodel.md` | delivered verbatim; cross-model replication of the taxonomy test (Kimi vs Perplexity) |
| `RESULT_repair_adjacency.md` | delivered verbatim; a third system (DeepSeek, by repair) and the strict hierarchy |
| `CELLS.md` | the coded cells, human-editable data store |
| `survey.py` | the 5×5 grid, the admissibility bars, validation |
| `gaps.py` | gap derivation, transfer questions, NO-TRANSFER |
| `report.py` | table, cell records, gap list, UNKNOWN + scope-incomplete + type-only counts |
| `taxonomy_replication.py` | transcription-consistency check of the crossmodel §1 nesting table + §6 count-refusal |
| `repair_adjacency.py` | transcription-consistency check of the refinement chain Kimi ⊃ DeepSeek ⊃ Perplexity |
| `run_all.py` | emits the full report |
| `CLAIM_TABLE.md` | `DS_001..DS_017` |

## The taxonomy test, replicated across models

`ADDENDUM_01` §2 left the SCOPE-DIFFERENT taxonomy OPEN because Runs 1
and 2 shared a system, so their agreement could not tell *converged*
from *remembered*. `RESULT_taxonomy_crossmodel.md` (delivered verbatim)
runs a **blind** Perplexity sort of the same 19 cells — no K-list, no
repo access — against the Kimi sort, and the question **splits**:
**membership replicated** (the two taxonomies are strictly nested, zero
cross-cutting — every Perplexity group under exactly one Kimi kind), so
SCOPE-DIFFERENT is **SEVERAL**; the **count did not** (4 Kimi kinds vs
11 Perplexity groups over 13 distinct), so *how many* is grain-dependent
and **UNSETTLED** (`DS_013`). `taxonomy_replication.py` makes the
strict-nesting headline checkable here — it transcribes the delivered §1
map and verifies it is a function (a **transcription-consistency check,
not a reproduction of the sort**; the 19-cell corpus is external model
output not held here), null-tested against a constructed cross-cut
(`DS_011`) — and encodes §6's *report membership, not a kind count* as a
**refusal in code**: `kind_count()` returns `UNSETTLED`, never an
integer (`DS_012`).

`RESULT_repair_adjacency.md` (delivered verbatim) adds a **third
system** — DeepSeek, sorting by *repair* into a 9-component adjacency
graph — and resolves the character of the count. The three groupings do
not conflict; they **nest in one order**, `Kimi (4-5) ⊃ DeepSeek (9) ⊃
Perplexity (11)`, zero cross-cutting: every DeepSeek component inside one
Kimi kind, every Perplexity group inside one DeepSeek component. **So
grain was never a disagreement — it is a cut height on a tree all three
independently found** (class / operation / operation-plus-referent).
`repair_adjacency.py` transcribes the §1–§3 memberships and verifies each
link of the chain is a refinement (`DS_014`), null-tested; it flags K4
**dead as a repair class** (its members scatter across three components,
`DS_015`), carries the straggler `T13`'s DeepSeek placement in C1 without
closing the gap (`DS_016`), and turns §6's refusal into a **cut-height**
statement — *a single number is a cut, and a cut with no stated height is
the thing the instrument exists to catch* (`DS_017`). All of it is a
transcription-consistency check; the corpus is external model output not
held here.

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
