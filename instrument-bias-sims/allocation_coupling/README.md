<!--
SPDX-License-Identifier: CC0-1.0
-->

# allocation_coupling — S10

**Marker under exploration, not a thesis.** A module set with a single runner.
Four modules with declared interfaces, coupled in phases, so the runner can
report *how much comes from each link* rather than only that an outcome occurs.

Stdlib only. Phone-buildable. CC0.

## Agents, declared before any equation

| agent | capabilities |
|---|---|
| `holder` | works, earns, holds or loses tenure, may observe |
| `assessor` | scores contribution from available record |
| `land` | state changes on a slow clock; readable only by continuous presence |
| `not_representable` | **`[BLANK]`** |

The spec asked for the blank to be *listed explicitly* rather than left empty,
which is a stronger form of the folder rule than S9's single empty slot. Five
parties are named in `agents.NOT_REPRESENTABLE`. The load-bearing one is the
fourth: **presence is derived from tenure in M1, so a continuous observer
without tenure cannot exist in this model at all** — and that is the position
most likely to hold the knowledge the module set is about.

## Modules

- **M1 `tenure_budget.py`** — an accounting identity. Hours in the money
  economy required to meet a tenure obligation, and what is left. No moral term.
- **M2 `coupling_readout.py`** — `C` is not linear in total hours. Window length
  gates observation type: `level` needs 4 unbroken hours, `threshold` needs 320.
- **M3 `energy_ledger.py`** — compensation gradient vs metabolic gradient.
- **M4 `assessment_record.py`** — contribution scored from the record.
  **Imports S9's `p_write` rather than re-deriving it.**
- **`run_all.py`** — three phases, per-link attribution.

## The main result: per-link attribution can't hold the finding

The spec's own reason for splitting into modules is that *"the finding is in
the cross-terms"* — and a per-link table is exactly the object that cannot
represent a cross-term.

| | |
|---|---|
| **RESIDUAL (interaction)** | **+0.64** |
| as a share of the effect | **0.791** |
| total effect | −0.81 |
| per-link table | **REFUSED** |

**The residual is 79% of the total effect**, and the table is now **refused**
rather than annotated. Where `|residual|` exceeds any single link, no per-link
table prints — the residual comes first and the links appear only as unranked
magnitudes. An annotation under a table does not undo the table: the rows are
the claim.

Leave-one-in is also one decomposition among several — leave-one-out and
Shapley give different per-link numbers on the same model. None is more
correct; they answer different questions, and the spec doesn't say which.

## Other results

- **The coupled run has zero deep observations for every position.** Positions
  with hours left have them in many short blocks; positions with long blocks
  have no hours left. That is the spec's prediction, and it holds.
- **M4 doesn't return a writing-time gradient — it returns an *inverted merit*
  gradient.** Assessed contribution correlates **−0.85** with observations
  generated. Stronger than the spec predicted. *(A first version of that readout
  compared |r| only and reported "tracks generated observations" for a
  correlation of minus 0.85. The sign was the finding and the magnitude
  comparison lost it.)*
- **CORRECTED — the −0.99 was a constraint, not a correlation.** Checked
  against the separator: `p_write` is a function of supply assumption, station
  distance and reward, while generation is a function of wage and block count.
  Different inputs, so this is **not** S4's rank-dictionary defect. But both
  dictionaries were hand-assigned in one ordering, so **the mapping admits no
  position high on both** — and adding one (a resident who is also compensated
  to write; a station scientist) moves the correlation with generation from
  **−0.853 to +0.107**. The inversion was a property of which five rows were
  typed in. The row that breaks it is one the mapping had no slot for, which is
  the blank-agent shape one level down.
- **M2's prediction is a parameter band, not a fact.** The fragmentation
  penalty is unmeasured, as the spec says. Swept, the two halves fail for
  *different reasons*: deep types die from the **window requirement**, which
  doesn't involve the penalty exponent at all.
- **The zero-everywhere result now has a null.** Scaling the window
  requirement down, deep observations become nonzero at **scale 0.25** — so the
  window is meetable and the zero is a property of the setting, not a
  hard-coded gate. Grade `OK`, not `CONSTANT_SILENT`.
- **Equal-block splitting is now swept, not just disclosed — and it is what
  *produces* the zero.** At the same total hours and the same block count,
  putting a fraction into one long stretch makes `sequence` reachable at
  unevenness 0.25 and all four types at 0.95. Not a small bias toward the
  prediction; the mechanism behind it.
- **M3's correlation sign is a property of the position list**, and now says
  so on the same line as the number: **−0.883 (n=5, UNWEIGHTED)**. Adding two
  high-wage high-expenditure positions flips it. This is not a result about
  compensation; it is a result about which five positions were typed in. The
  fix is labelling, not modelling.

## Known gaps, left visible

- **M3 has no term for multi-channel sensory integration load under vibration
  and noise.** `SENSORY_INTEGRATION_LOAD` is `None` for **5 of 5** positions and
  renders as `[BLANK]`. The instrument exists and is field-deployable; the
  sampled occupations are sport and prestige — pianists, racing drivers, pilots,
  air traffic controllers. No farm, fabrication, animal handling or freight data
  located. Left `None` rather than estimated: an estimate would enter the
  correlation and could not be told apart from a measurement. The gap has the
  same shape as the thing the module set is about.
- **M2's fragmentation penalty is unmeasured.** Parameterized and swept.
- **M4's position mapping is the weakest link in the set** — five M1 positions
  hand-assigned three S9 axis values each, fifteen stipulated numbers that every
  downstream magnitude moves with.
- **M3 does not enter the decomposition.** Nothing in the spec routes energy
  into assessment, so it is a separate readout and is reported as one.

No module reads real data.
