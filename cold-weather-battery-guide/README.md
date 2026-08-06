# Cold-Weather Battery Guide

Single-folder offline reference for building a Li-ion battery system
that survives both &minus;60 F winter mornings and 125 F sleeper-cab
summer sun. Covers cell chemistry, scrap-sourced solid-state ceramics,
solar-thermal kiln design, cell assembly, dry-box construction, an
Arduino BMS with solar-thermal preheating and a safety shutter, and
the full safety envelope.

## Files

- `index.html` — mobile-first HTML reference. Eleven sections
  navigable from a two-column menu, same visual system as the other
  three practical guides in this repo.
- `bms/bms_1s_basic.ino` — minimal Arduino BMS for a single ester
  cell (electrical protection + low-temperature charge lockout).
- `bms/bms_1s_merged.ino` — full-feature Arduino BMS with thermal
  state machine, sunrise predictor, and PIR safety shutter.
- `bms/README.md` — hardware pin table, wiring notes, calibration
  procedure, testing steps, notes on scaling to 4S.

## The eleven sections

1. **Overview & Failure Stack** — the cold-end failure hierarchy
   (electrolyte transport → SEI/Rct → Li plating → freeze-out) and
   the hot-end note that 125 F is a shade+emissivity problem, not
   a chemistry one.
2. **Chemistry Options** — decision matrix: liquefied gas (A, skip),
   LATP solid state (B), Mars-rover ester (C).
3. **Ester Electrolyte (Option C)** — 1 M LiPF6 in EC:DMC:EA (1:1:2)
   + 2-3% VC. Includes drying hardware-store ethyl acetate over
   3 Å sieves, LiPF6 handling safety, and the home-brew Fischer
   esterification side quest.
4. **LATP Solid State (Option B)** — target
   Li₁.₃Al₀.₃Ti₁.₇(PO₄)₃, scrap precursor stream table (cordierite
   from cat converters, spark plug alumina, ABC-powder phosphate,
   welding-flux TiO₂, pottery Li₂CO₃), and why other solid-state
   families are the wrong choice for this environment.
5. **Kiln** — Fresnel solar cavity with SiC susceptor + thermal
   mass, and the microwave + SiC backup for nights and overcast.
6. **Dry Box** — glove-bin build from a plastic storage tote, PVC
   gauntlet gloves, welding-gas purge, molecular sieve tray,
   cobalt-chloride humidity indicator.
7. **Cell Assembly** — pouch cell construction with LFP + graphite
   from harvested foils, vacuum wetting, tab welding.
8. **Formation Cycling** — five-stage first charge protocol
   (C/50 → C/20 → C/10 → CV → discharge) that tames the ester
   toward the graphite anode.
9. **Thermal Management** — solar block preheat, four-state
   machine (STANDBY / PREHEAT / CHARGE_WAIT / OVERHEAT_PROTECT),
   scrap actuator options, predictive sunrise.
10. **BMS Overview** — pointer to the two `.ino` files with pin
    table excerpt and analog-hack fallback.
11. **Safety** — HF from LiPF6, concentrated sunlight hazards
    (including the PIR shutter requirement), CO, methanol,
    ether pool ignition, lithium thermal runaway, caustic chemicals.

## Where this fits

Fourth guide in the family (**diagnose it → make it → fuel it → power it**):

- `../engine-boiler-guide/` — diagnose it (field-triage decision
  flow for engine and boiler problems)
- `../field-fabrication-guide/` — make it (lime, ammonia, aluminum
  smelting, straightedges, sextants, etc.)
- `../fuel-independence-guide/` — fuel it (wood gasifier, biodiesel,
  waste motor oil, extreme-cold diesel, alcohol fuels)
- `../cold-weather-battery-guide/` — power it (this guide)

Same visual system across the three HTML guides; a new sibling can
copy any of their `<style>` blocks.

## How to use

**On a phone:**
- Email `index.html` → open in browser → "Add to Home Screen"
- Or Bluetooth / USB the file to the phone → open in any browser
- Works fully offline; no fonts, no images, no network calls

**On the Arduino:**
- Open either `.ino` in the Arduino IDE
- Install libraries: `Adafruit_INA219`, `Servo` (bundled)
- Compile against Arduino Nano or Uno target
- Upload via USB
- Serial Monitor at 9600 (basic) or 115200 (merged) baud

## What this is not

- **Not a chemistry course.** The recipes are directional. Real
  battery chemistry needs a graduate lab or a mentor. Warnings
  here are reminders, not full HSE training.
- **Not a certified BMS.** No UN 38.3, no UL, no automotive
  qualification. Learning and testing rig only. A hardware fuse
  in the pack negative lead and a proper enclosure vent are
  required for anything closer to real use.
- **Not a substitute for a fume hood** when handling LiPF6, and
  not a substitute for a physical exclusion fence around the
  Fresnel array. The PIR shutter is a fallback, not a primary
  safety layer.
- **Not a promise the cell will hit &minus;60 F on the first
  build.** Expected performance is 20-30% of room-temperature
  capacity at &minus;60 F when everything works. The path to
  that number goes through the dry box, the formation cycle, and
  a lot of patience.

## Sourcing notes

The scrap-based precursor list (dead cat converters, spark plug
insulators, ABC fire extinguisher powder, welding rod flux, dead
LFP cells) is real but assumes you have access to a junkyard or
scrap yard. Cordierite honeycomb is the single highest-leverage
item — get it before you start anything else. If you cannot scrap-
source, pottery supply and lab supply both stock every precursor
at commodity prices.

## Provenance

Content assembled from a design conversation covering cold-cell
failure analysis, three chemistry paths, Fresnel + microwave kiln
design, dry-box build, cell assembly, formation cycling, BMS design
(1S basic + merged with thermal state machine + PIR shutter), and
safety. The go-kart incident that inspired the PIR shutter is real.
The singed jeans were paid tuition.

CC0.
