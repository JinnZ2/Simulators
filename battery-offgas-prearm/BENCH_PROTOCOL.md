# BENCH PROTOCOL: battery-offgas-prearm

PROPOSED. CC0. Repeat each run at least **3 times per chemistry and
geometry**, and record every run, including the ones that look wrong.

The protocol has two phases. **Phase A** involves no live chemistry and
can be done in a workshop. **Phase B** drives real cells toward runaway
and is outdoor, remote-only work. Phase A alone gives you a threshold and
`Q_remove`. Phase B is what turns `UNMEASURED` margins into numbers.

```
 PHASE A (safe)                        PHASE B (outdoor, remote, hazardous)
 A1 breathing log  -> threshold        B1 single cell to runaway -> Q_generate, lead_s
 A2 sensor step    -> T90, actuation   B2 2-3 cells at YOUR spacing -> propagation_s
 A3 heater dummy   -> Q_remove         B3 feed margins into prearm.py
```

Record format for anything with a sensor stream: CSV lines
`t_seconds,channel,value`. That is what `prearm.py --trace` reads.

---

## PHASE A: no live chemistry

### A1. Breathing log: setting the threshold

1. Install the sensors at the cluster on a **healthy** pack in its real
   enclosure. Burn in MOx heaters per the datasheet first.
2. Log every channel for **at least 7 days** of normal use: charge, load,
   day/night, the hottest afternoon you can get.
3. For each channel, compute the Theil-Sen slope over your chosen
   `window_s` at every sample (`prearm.slope` on a sliding window). Record
   the **maximum** breathing slope `s_max` and the slope distribution.
4. Declare `rate_threshold = margin x s_max`. Write the margin down; the
   margin is your choice, not a measured value.
5. Replay the whole log through `prearm.py --trace`. **Zero trips** is the
   pass condition. Any trip is a false-trip estimate: count them per day.

The threshold you get here is the number that `config.example.json`
leaves `null`.

### A2. Sensor step response: lead time you will not get

1. Put the sensor in a small closed volume (a jar). Introduce a step of
   test gas: a little isopropyl-alcohol vapour for MOx VOC, exhaled breath
   or a CO2 cartridge puff for NDIR. Use a safe gas for each sensor class.
2. Record the time from step to 90 % of the final reading: **T90**.
3. Measure controller loop time plus disconnect actuation time (scope the
   coil or the SSR output).
4. `actuation_s` = (T90 not already inside how you measure lead) +
   controller + relay.

### A3. Heater dummy: Q_remove

1. Build a **dummy cell**: same outside dimensions as your cell, with a
   thermal mass close to the cell's (aluminium or a filled can), a
   cartridge heater inside, and a thermocouple at the core and one on the
   surface.
2. Pack it exactly like your real cells: same PCM, matrix and spacing, and
   tier 2 nozzle if fitted.
3. Drive it with **power steps** P1 < P2 < ..., each held for the length
   of your onset window.
4. `Q_remove` = the highest step at which the core stays **below the knee
   temperature you declare** (pick it from your chemistry's first
   exotherm, ~80 C `[CARRIED]`) for the whole window.
5. Repeat without PCM, with PCM, and with PCM plus tier 2. The differences
   are what each tier is worth on your geometry.
6. Put a second dummy at your real cell spacing and log its temperature.
   This is the *thermal* half of propagation, with no chemistry involved.

---

## PHASE B: real cells (outdoor, remote, hazardous)

**Before anything:** outdoors, at a standoff distance, with remote trigger
and remote readout. Use fire-rated containment, keep the downwind side
clear, and have extinguishing water at standoff. Never do this indoors.
See the README hazards section. If you cannot meet these conditions, skip
Phase B and use published calorimetry data for `Q_generate` instead
(tagged `[CARRIED]` in your record).

### B1. Single cell to runaway

1. Instrument one cell: gas channels at the cell, a surface
   thermocouple, and a camera.
2. Abuse it reproducibly. Use an external heater ramp at a stated rate or
   an overcharge at a stated current. Write down which.
3. Define runaway onset up front, for example surface dT/dt above a
   declared rate. Declare it before the run, not after.
4. Record:
   - `t_gas` = when `prearm.py` replayed on the log first fires tier 0
   - `t_run` = runaway onset
   - **`lead_s = t_run - t_gas`**
   - self-heating rate in the onset window -> **`Q_generate`** (W) from the
     cell's heat capacity times dT/dt before the knee

### B2. Cells at your spacing: propagation

1. Place 2-3 cells at **the spacing you actually build**. Run B1 on cell 1
   only.
2. **`propagation_s`** = neighbour runaway onset minus cell 1 runaway
   onset. Record "no propagation" as its own result, not as a large
   number.

### B3. Feed the margins

```python
import prearm as P
P.heat_margin(q_remove_w, q_generate_w)            # HOLDS / SHORT
P.cascade_margin(lead_s, actuation_s, propagation_s)
#   FIRST_CELL_WINDOW / NEIGHBOURS_ONLY / MARGIN_TOO_SHORT
```

`MARGIN_TOO_SHORT` means increase the spacing or add barriers, rerun B2,
and keep the earlier run in the record.

---

## RECORD TEMPLATE (one per run)

```
date / place / who
chemistry, cell model, SOC at test
geometry: spacing, PCM (type, melt C, mass), matrix, tier 2 type
sensors: classes, positions, T90 (A2)
window_s / confirm_count / rate_threshold per channel / margin used (A1)
knee temperature declared / runaway onset definition declared
results: Q_remove, Q_generate, lead_s, actuation_s, propagation_s
verdicts: heat_margin, cascade_margin
anything that went wrong (keep it)
```
