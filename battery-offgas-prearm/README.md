# battery-offgas-prearm

**A buildable spec for a DIY off-gas pre-arm on lithium-ion battery banks.**
Detect the gas a cell vents *before* thermal runaway, and act on that gas.
Waiting for heat or flame comes too late.

```
STATUS     PROPOSED. SELF-GRADED: the spec, prearm.py and test_prearm.py
           share one author, so passing the tests is a regression result,
           not a validation. No cell has been tested for this folder.
LICENSE    CC0. Build it, change it, sell it, no attribution needed.
SCOPE      Homestead battery banks, small solar shops, DIY packs, vans,
           sleeper cabs: the people commercial off-gas products do not
           reach on cost.
CODE       stdlib Python, parses under 3.9, runs on a phone.
           python3 battery-offgas-prearm/prearm.py --demo
           python3 battery-offgas-prearm/test_prearm.py
```

Every external fact below is tagged `[CARRIED]`: it was stated to this
build or comes from general knowledge, and this environment could not
fetch a source to check it. Verify each one for your chemistry and your
parts before you build on it.

---

## 1. PURPOSE and PRIOR ART

```
            cell abuse / defect
                    |
     [ off-gas vents ]  <-- signal exists here, minutes early
                    |
     [ first exotherm, self-heating ]
                    |
     [ separator melt, internal short ]
                    |
     [ THERMAL RUNAWAY ] --> neighbour cells --> cascade
```

**Off-gas detection already exists.** Commercial off-gas detection exists
(e.g. Li-ion Tamer). In DNV-GL third-party tests it gave **6.4 min** of
early warning, and stopping the charge on the signal avoided runaway
`[CARRIED]`. The physics is not new.

**The combination below is not found as an open, buildable stack.** It is
three tiers, all keyed off the off-gas signal and sized for DIY scale:

- per-cell or per-cluster fast disconnect
- phase-change material (PCM) tuned to the onset temperature
- local CO2 or directed cooling, fired at detection

That combination is the contribution. Commercial early warning is
access-locked by product cost and integration, not by physics.

*Prior-art search status:* carried from the relay, not re-run here (the
egress gate refuses publisher hosts). "Not found" is a search result, not a
proof of absence. If you know of an open stack like this, the folder wants
to cite it.

---

## 2. THE 3-TIER STACK (in firing order)

```
 gas sensor (at the cluster)
      |
      v
 prearm.py: rate of rise > declared threshold, N times in a row
      |
      +--> TIER 0  FAST DISCONNECT ........ cut feed, isolate   (latched)
      +--> TIER 1  PASSIVE PCM ............ already in place, no actuation
      +--> TIER 2  ACTIVE LOCAL COOLING ... CO2 mist / directed cooling
                                            (only if interlock satisfied)
```

### TIER 0: fast disconnect (first, always)

- **What:** opens the charge/load path to the cell or cluster and isolates it.
- **Trips on:** a confirmed rate-of-rise gust, a declared level ceiling, or
  a sensor fault when the fault policy is `TRIP`.
- **Device options:**

  | device | for | against |
  |---|---|---|
  | DC-rated contactor, normally open, held closed by its coil | fail-safe: controller dies -> coil drops -> opens | coil power; contacts must be DC-rated for the arc |
  | Solid-state relay (DC) | fast, no arc | leaks current, drops voltage, runs hot at current; NOT true isolation |
  | Pyro-fuse (pyrotechnic disconnect) | very fast, true isolation | one-shot; an explosive device with handling and legal limits |

- **Honest limit:** disconnect does **not** stop runaway once the cell's
  internal chemistry has lit. It removes external energy (charge current,
  external short paths). The energy already in the cell stays there. Tier 0
  buys margin; it does not cure the cell.
- **Latches:** nothing in the code recloses it. A person resets it after
  looking at the pack.

### TIER 1: passive PCM (always there, no actuation)

- **What:** a phase-change material packed around or between cells. It
  absorbs heat as latent heat while it melts, at a fixed temperature.
- **Tuned:** pick the melt point to sit **above** the pack's maximum normal
  operating temperature and **below** the first exotherm (section 5, and
  conflicts C1-C3 below).
- **Role:** soaks the first surge in the onset window. It is inert in
  normal operation if the melt point is chosen right.
- Sizing arithmetic is in the code: `pcm_mass_kg(energy_j, latent_j_per_kg)`.
  It uses latent heat only, which is the conservative side.

### TIER 2: active, gas-triggered local cooling

- **What:** a CO2 mist or directed cooling at the affected cell or cluster.
  It fires at **detection**, not at ignition.
- **Interlock in code:** tier 2 refuses to arm unless the discharge space
  is declared `VENTED` or `UNOCCUPIED_ENCLOSURE`. Tier 0 still fires either
  way.
- **What it is for:** **cooling**. Oxide cathodes (NMC, LCO) release their
  own oxygen as they decompose, so inerting the air around them does not
  stop the reaction `[CARRIED]`. The coolant choice is a bench result
  (conflict C4).

---

## 3. DIY PARTS LIST (hobby scale)

Sensors go **at the cell cluster**, not on the pack wall. Vent gas dilutes
with distance, and dilution eats your lead time.

| part | class | notes |
|---|---|---|
| H2 sensor | MOx (hobby H2 modules) | H2 is a major vent gas, LFP included `[CARRIED]`; MOx responds in seconds |
| VOC / electrolyte vapour | MOx VOC sensor | solvent vapour (DMC/EMC/DEC) is among the earliest vents `[CARRIED]`; cross-sensitive, which is fine for a rate rule |
| CO | electrochemical CO cell | slower, more specific; good confirm channel |
| CO2 | NDIR module | specific and stable; often **slow** (T90 tens of seconds to minutes `[CARRIED]`, read your datasheet); confirm, not primary |
| controller | any hobby microcontroller with ADC/I2C | runs the same rule as `prearm.py` (port it, or log to a phone/SBC running it) |
| disconnect | DC contactor (NO, coil-held) / DC SSR / pyro-fuse | see the tier 0 table; rate it for your pack's max DC current and voltage |
| PCM | paraffin of a chosen melt point, or a salt hydrate | conflicts C1-C3; pack it in a conductive matrix (aluminium fins/foam, expanded graphite) |
| tier 2 source | small CO2 cylinder + solenoid valve + nozzle at cluster | only into a declared VENTED or UNOCCUPIED space; or swap to a directed fan/water-mist design after your bench test |
| enclosure vent | ducted vent to outside | vent gas is flammable and toxic (CO, HF) `[CARRIED]`; the pre-arm does not make an unvented enclosure safe |

MOx sensors need a heater burn-in (often a day or more `[CARRIED]`) before
their baseline settles. Log breathing for a while before you set a
threshold.

---

## 4. TRIGGER RULE

```
fire  <=>  rate_of_rise(channel, last window_s)  >=  declared threshold
           for confirm_count consecutive evaluations
```

- **The signal is the gust, not the level.** Normal breathing does not
  fire: baseline drift, charge-cycle swing, a warm afternoon. A runaway
  ramp accelerates (dx/dt = k·x^a with a > 1), and an accelerating ramp
  crosses any fixed rate threshold early.
- **Slope estimator:** Theil-Sen, the median of all pairwise slopes. This
  was not the first choice; see BOP_005. Least squares was tried first and
  a single one-sample spike carried it through confirmation.
- **Threshold is declared config.** No value means `UNRATED`, and the
  module **refuses to arm**. `config.example.json` ships with every
  threshold `null` on purpose. The number comes from your bench run
  (BENCH_PROTOCOL.md), not from this folder.
- **Partial rating:** a channel with no threshold contributes nothing and
  is listed as unrated on every run. Rated channels still arm ([CHOICE 1]).
- **Sensor fault policy is declared:** `TRIP` (a dead sensor opens tier 0)
  or `ALARM` (alarm only). With no policy declared the module refuses to
  arm.
- **Slow leaks:** a rate rule cannot see a level that never gusts. Declare
  an optional `level_ceiling` per channel if you want one.
- **Spike boundary (BOP_010):** at a 60 s window and 5 s sampling, a 30 s
  step does not fire and a 35 s step does. Past about half the window, a
  step is a sustained rise, and rate alone cannot tell it from onset.

---

## 5. GATING MEASUREMENT (does it work on YOUR pack?)

Two numbers decide whether the stack helps your pack, or only reports what
is happening to it. Both are bench quantities per **chemistry and
geometry**:

```
 HEAT    Q_remove (PCM + tier 2, inside the onset window)
           vs
         Q_generate (cell self-heating inside the onset window)
         onset window: first exotherm ~80-120 C, accelerating to
         ~150-200 C  [CARRIED -- verify per chemistry]
         -> heat_margin():  HOLDS | SHORT | UNMEASURED

 TIME    lead_s       gas detection before first-cell runaway
         actuation_s  sensor lag not in lead + controller + relay
         propagation_s first-cell runaway -> neighbour runaway
         -> cascade_margin():
              FIRST_CELL_WINDOW  detection beats cell 1
              NEIGHBOURS_ONLY    too late for cell 1, ahead of neighbours
              MARGIN_TOO_SHORT   signal real, margin too short
              UNMEASURED
```

`MARGIN_TOO_SHORT` is a result, not a failure. It says the remedy is
**geometry**: cell spacing or thermal barriers between cells. A faster
relay will not fix it. In dense packs this is the expected outcome, and
spacing is cheap.

The repeatable protocol is in **BENCH_PROTOCOL.md**. Phase A is safe, uses
no live chemistry, and measures `Q_remove`. Phase B is outdoor and
remote-only, and measures `Q_generate`, `lead_s` and `propagation_s` with
real cells.

---

## 6. CONFLICTS and GAPS (the design tensions, stated)

| # | conflict | consequence | open measurement |
|---|---|---|---|
| C1 | PCM melt point: must sit above the max normal pack temperature (a hot cab or shed can pass 50 C) and below the first exotherm (~80 C `[CARRIED]`) | a narrow window; the wrong melt point is either always melting or never in time | max operating temperature of YOUR install, logged over a summer |
| C2 | Solid paraffin conducts heat poorly (~0.2 W/m·K `[CARRIED]`) | it insulates the cells in normal use, raising baseline temperature and wear | cell temperature with vs without PCM at normal load |
| C3 | Paraffin is fuel | past its latent capacity it can feed a fire; salt hydrates don't burn but corrode, supercool and separate `[CARRIED]` | PCM choice under Phase B conditions |
| C4 | CO2 cools weakly: sublimation ~0.57 MJ/kg vs water evaporation ~2.26 MJ/kg `[CARRIED]`, and inerting does not stop oxide cathodes | tier 2 as CO2 may move too few watts; water near high voltage is its own hazard | Phase A `Q_remove` per coolant |
| C5 | Disconnecting an off-grid bank cuts the house | false trips cost power; this is why `confirm_count` and Theil-Sen exist | false-trip rate over a logged breathing period |
| C6 | DC breaking arcs; SSRs leak and are not isolation; pyro-fuses are explosives | the cheapest disconnect is not the safest one | none; this is a choice to declare |
| C7 | The sensor sits in the event it reports; HF and heat can kill MOx sensors `[CARRIED]` | the sensor may die mid-event | set `on_sensor_fault: TRIP` and test it |
| C8 | Slow NDIR lag eats lead time | CO2 as the primary channel loses minutes | T90 per sensor in Phase A step tests |
| C9 | Rate-only misses slow leaks | a quiet high level never fires | optional `level_ceiling` |

---

## 7. HAZARDS (engineering facts, peer to peer)

- **CO2 asphyxiation.** 1 kg of CO2 is about 0.54 m³ of gas. Released into
  a 2 m³ closet that is about **24 % by volume**
  (`co2_fraction(1.0, 2.0)`). The NIOSH IDLH is 4 % (40,000 ppm)
  `[CARRIED]`. Never discharge into a space a person can be in. The code
  enforces this only as a *declared* interlock: it cannot see your room.
- **Vent gas** is flammable (H2, CO, hydrocarbons, solvent vapour) and
  toxic (CO, HF) `[CARRIED]`. Vent the enclosure to outside, and do not
  stand downwind of a venting pack.
- **High-current DC disconnects** draw arcs that AC-rated parts do not
  extinguish. Use parts rated for your DC voltage and current.
- **Pyro-fuses** are pyrotechnic devices. Storage, handling and legal
  status vary by place. Treat one like any other charge.
- **Phase B** of the bench protocol deliberately drives a real cell toward
  runaway. Do it outdoors only, at a standoff distance, with remote trigger
  and readout, and fire-rated containment. Never do it indoors or near
  anything you need.
- **This stack adds margin. It does not certify a pack.** It does not
  replace a BMS, fusing, correct charge limits, or spacing.

---

## 8. FILES

```
README.md            this spec
BENCH_PROTOCOL.md    Phase A (safe, no chemistry) + Phase B (outdoor, remote)
CLAIM_TABLE.md       BOP_001..BOP_011
prearm.py            trigger logic, margins, hazard arithmetic, fixtures
test_prearm.py       checks (count printed by the run, not stored here)
config.example.json  every threshold null -> refuses to arm as shipped
samples/demo.sample.txt  pinned demo output (CONSTRUCTED fixtures)
```

The fixtures are **CONSTRUCTED shapes**. The demo's "685 s lead" is a
property of a made-up ramp, not of any cell.
