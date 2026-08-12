# Far North Fuel Independence

Single-file offline mobile app for keeping engines and generators
running when the fuel supply chain stops. Seven sections covering
wood gasification, biodiesel production, waste-motor-oil filtering,
extreme-cold diesel operation (-40 to -60 F), alcohol fuels for gas
engines, and safety.

## The premise

Corporations don't deliver fuel to unprofitable places. Batteries fail
at -60 F and can burn a house down. A 1968 Case diesel with a
mechanical injection pump will run on things that destroy any modern
common-rail engine. The guide leans into that.

## What it covers

**Seven sections** navigable from a two-column menu:

1. **Decision Chart** — one-page overview: what you have + what
   engine → which solution.
2. **Wood Gasifier** — Imbert downdraft design dimensioned for a
   50-100 hp tractor. Fire tube, tuyere ring, reduction zone, grate,
   condensate trap, filter train. Operation on gas and diesel
   engines (dual-fuel with 10-20% pilot diesel). Stationary vs.
   tractor-mounted tradeoffs.
3. **Biodiesel (2-Stage)** — the acid-esterification stage that lets
   rancid oil (high FFA) become usable biodiesel instead of soap.
   Full recipes (5 g NaOH + 200 mL methanol per liter of oil),
   settling, water wash, drying, quality tests, and winterizing
   with kerosene blends.
4. **Waste Motor Oil** — settling / decant / bag-filter, plus a
   scrap-built drum-and-cone centrifuge. Blending ratios for summer
   diesel use; noting WMO is better used for heat in winter.
5. **Cold Diesel Ops** — the fuel-gelling table (why summer #2
   diesel becomes a solid brick at -60 F), coolant-loop tank
   heating, filter heating, starting aids, and the ether-lock
   warning that has broken pistons on high-compression tractors.
6. **Alcohol Fuels** — improved methanol from hardwood (birch beats
   spruce, retort dimensions, fractionation), ethanol by fermentation
   + distillation + drying, and carb / timing / lubrication changes
   needed to run a gas engine on alcohol.
7. **Safety** — CO from wood gas, methanol toxicity (ethanol is the
   antidote), ether pool-ignition risk, lithium battery thermal
   runaway (why "just use an electric tractor" is bad advice at
   -60 F), lye and acid handling for biodiesel.

## How to use

**On a phone:**
- Email `index.html` → open in browser → "Add to Home Screen"
- Or Bluetooth / USB to the phone → open in any browser
- Works fully offline; no fonts, no images, no network calls

**On a desktop:**
- Double-click `index.html`; opens in whatever browser is default

## Design constraints (why it looks this way)

- **Single HTML file.** ~50 KB. Survives being emailed or copied to
  a USB stick.
- **Same visual system as `../field-fabrication-guide/`**. Sections,
  data-cards, step-numbers, note/warning/tip callouts. If you build
  a new guide in this family, copy either file's `<style>` block.
- **Warnings before recipes**, not after. CO poisoning callout at the
  top of the gasifier section, ether-lock warning before the ether
  row in the starting-aids table.
- **Named benchmarks.** Numbers throughout — "kerosene cloud point
  -40 F," "wood gas 20-30% CO," "1 kg dry hardwood → 10-20 mL
  methanol" — so a reader can sanity-check whether their setup is
  in the expected range, not just "it should work."
- **No state saved.** Reset each session.

## Sister guides in this family

- `../engine-boiler-guide/` — mobile-first symptom → machine → era →
  filtered checklist for triaging engine/boiler problems in the
  field. Same offline-first pattern, different UX (four-screen
  decision flow rather than section navigation).
- `../field-fabrication-guide/` — offline reference for making
  precision tools and processing raw materials (lime, ammonia,
  aluminum smelting, sextants). Same visual system as this guide.

Together the three cover: **diagnose it** (engine-boiler) →
**make it** (fabrication) → **fuel it** (this guide).

## What it is not

- **Not a permit.** Wood gasifiers, home distillation of alcohol, and
  biodiesel processing all have regulatory statuses that vary by
  jurisdiction. This guide is technical reference, not legal advice.
- **Not a substitute for hands-on training.** Molten lye, sulfuric
  acid, ether spray, and CO from a bad gasifier can all kill quickly.
  The safety section is a reminder, not a full HSE course.
- **Not a promise the tractor will start at -60 F.** All the guide can
  do is name the failure modes and the mitigations. The mechanic in
  the cold shed is you.

CC0.
