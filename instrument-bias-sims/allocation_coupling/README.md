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

| link | contribution alone |
|---|---|
| M1 hours → M2 | −0.20 |
| M1 blocks → M2 | −1.26 |
| position → M4 writing | −0.00 |
| **sum of the three** | **−1.45** |
| **total effect** | **−0.81** |
| **RESIDUAL (interaction)** | **+0.64** |

**The residual is 79% of the total effect.** The three links sum to nearly
twice the actual difference. A table printed without the residual row would
assign that interaction to whichever link was listed last. Reported alongside,
never distributed.

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
- **And it cannot be fixed at the assessor.** Generation and writing
  probability are anti-correlated at **−0.99** in this mapping, so no scoring
  rule reading only the record can separate them. An identifiability limit of
  the same shape as S2's one-arm protocol: the fix is a second observable, not
  a better estimator.
- **M2's prediction is a parameter band, not a fact.** The fragmentation
  penalty is unmeasured, as the spec says. Swept, it turns out the two halves
  of the prediction fail for *different reasons*: deep types die from the
  **window requirement**, which doesn't involve the penalty exponent at all,
  while level survival is what the exponent controls.
- **M3's correlation sign is a property of the position list.** Wage runs
  against energy draw at −0.93 here; adding two high-wage high-expenditure
  positions flips it. What would settle it is the population weight of such
  positions, which nothing here represents.

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
