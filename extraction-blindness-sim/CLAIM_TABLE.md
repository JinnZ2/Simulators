# CLAIM_TABLE — extraction-blindness-sim

Every claim is refutable. **Refutation protocol: when a claim fails,
update the claim. Never retune constants to protect a favored result.**

All evidence below is from the pinned run at
`samples/experiments.sample.txt`, reproducible with
`python3 run_experiments.py`. The suite is deterministic; a test
asserts two consecutive runs are byte-identical.

## Status legend
`SUPPORTED` · `REFUTED` · `INSTRUCTIVE-NEGATIVE` (question was mal-posed) · `SCOPE-LIMITED`

---

## Core mechanism

| # | Claim | Status | Evidence |
|---|-------|--------|----------|
| **EBS_001** | An optimizer acting on a blinded observation reports high safety while the substrate collapses. Its confidence is derived from absence of an error signal, and blindness removes the error signal. | **SUPPORTED** | Fishery, full blindness stack: collapse at **step 7**, final stock **0.0000**, max safety–health gap **0.5630**. At the collapse step itself the optimizer still reported safety 0.3728 against true health 0.1755. |
| **EBS_002** | Decay-velocity indicators fire strictly before collapse, buying measurable lead time. | **SUPPORTED** | Passive panel against the unaltered blind trajectory. Fishery: first fire **step 1**, collapse **step 7**, lead **6**. Soil: first fire **step 31**, collapse **step 55**, lead **24**. |
| **EBS_006** | Temporal aliasing changes the outcome only where the perceived trend actually steers the controller *and* no effort ratchet overrides it. Blindness in a channel nothing acts on is cosmetic. | **SUPPORTED** | Three regimes. (a) trend not in loop: outcome delta **0.0000**. (b) trend steers, no ratchet: clear vision ends at **0.8798**, aliased at **0.0000** — delta **+0.8798**. (c) ratchet defending a target: delta **0.0000**, the ratchet dominates. |

**Refuted if:** the blind fishery run survives 60 steps; or any panel's
first-fire step lands at or after its collapse step; or regime (b) of
EBS_006 shows a delta below 0.5.

---

## Control-layer design

| # | Claim | Status | Evidence |
|---|-------|--------|----------|
| **EBS_003** | Where a threshold sits dominates what authority it carries. An earlier advisory signal outperforms a later non-negotiable floor. | **SUPPORTED** | Fishery. Advisory indicators: final stock **1.0000**, no collapse. Hard boundaries at the specification's stated values: final stock **0.3107**, extraction **3.4817**. Boundaries do beat blind operation (0.0000), but they park the system *inside* the depensation regime rather than preventing entry to it. |

This is the result that ran against the initial expectation. The
specification's fishery biomass floor is written at 50% of B_MSY —
which is **25% of pristine**, while depensation begins at **40% of
pristine**. The floor is therefore placed below the threshold it is
meant to defend. The boundary layer does exactly what it was told:
it defends 25%, permits maximal extraction down to that line, and
reports compliance throughout.

**Refuted if:** raising the biomass floor above the depensation
threshold fails to make the override outperform the advisory layer.
That experiment is not yet built and is the first thing to add.

---

## Source-specification contradictions

These are properties of the source material, reproduced rather than
repaired. `throughput.py` implements each formulation as written and
the demonstrations show where they disagree in **sign**, which is the
part that matters for governance.

| # | Claim | Status | Evidence |
|---|-------|--------|----------|
| **EBS_004a** | RT as written is inverted relative to its own governance rule: both prescribed remedies move RT *away* from its threshold. | **SUPPORTED** | `RT = Output/(Regen+Reinvest)`: baseline **0.9130**, reduce extraction → **0.7825**, increase reinvestment → **0.8077**. Both fall. Under `RT = (Regen+Reinvest)/Output`: baseline **1.0952** → **1.2780** and **1.2381**. Both rise. |
| **EBS_004b** | The additive caloric term in soil RT Version B masks depletion: RT rises while humified carbon falls. | **SUPPORTED** | 30% loss of humified carbon. Version B **0.6667 → 1.1833** (delta **+0.5167**, reports improvement). Mass-balance form **1.2500 → 0.1250** (delta **−1.1250**, reports the loss). |
| **EBS_005** | A fixed RT threshold produces both false alarms and missed detections, because healthy baseline RT is substrate-specific. | **SUPPORTED** | Low-RT substrate at its own healthy baseline 0.92: absolute(0.95) **fires** (false alarm), relative 2σ does not. High-RT substrate dropped 19% below a 1.30 baseline: absolute(0.95) **silent** (missed detection), relative 2σ **fires**. |

**EBS_004a is not in the source's own audit.** The source identifies
four problems (two irreconcilable RT_soil equations, a 10cm/20cm depth
conflict, the arbitrary 0.95 threshold, and the caloric sign error).
The orientation error is a fifth, found while implementing the
governance rule against the equation as written.

**Refuted if:** a reading of the source is produced under which
"reduce extraction" raises `Output/(Regen+Reinvest)`.

---

## Open — not claimed

Recorded so they are not mistaken for settled.

| # | Question | Why it is open |
|---|----------|----------------|
| **EBS_OPEN_1** | Which soil RT formulation is correct? | The source gives two mutually exclusive equations. Both are implemented; neither is endorsed. Deciding requires field data correlating each against the SOC floor. |
| **EBS_OPEN_2** | At what depth does the SOC floor belong? | The source says 10 cm in one place, 20 cm in another, and 30 cm in the boundary text. `boundaries.py` uses the 30 cm integrated value and flags the ambiguity. Resolving it needs a sliding-window integration across 0–10 / 10–20 / 20–30 cm to find which layer fails first. |
| **EBS_OPEN_3** | Are the `[MODEL]` constants in `profiles.py` defensible? | Every derived state variable (trophic level, F:B ratio, qCO2 …) is a deterministic function of stock depletion, not an independently simulated process. The *ordering* of threshold crossings is therefore partly assumed rather than derived. |
| **EBS_OPEN_4** | Does the blind-optimizer result survive a stochastic substrate? | The substrate is deterministic. Recruitment variability would let a blind optimizer occasionally get lucky, and the interesting quantity becomes the distribution of collapse times, not a single trajectory. |

---

## What would most change these conclusions

1. **A stochastic substrate.** EBS_001 and EBS_002 are single-trajectory
   results. Their honest form is a distribution over seeds.
2. **Independently simulated indicators.** EBS_002's lead times are
   partly a consequence of how the `[MODEL]` indicator functions were
   written. Indicators driven by their own dynamics would be a real
   test rather than a consistency check.
3. **A boundary-placement sweep.** EBS_003 currently reports a single
   pair of configurations. Sweeping the biomass floor across the
   depensation threshold would turn a comparison into a curve, and is
   the cheapest high-value addition to this folder.
