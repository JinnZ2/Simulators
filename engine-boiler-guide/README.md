# Engine & Boiler Fix Guide

Single-file offline mobile app for triaging engine and boiler problems
in the field. Four-screen decision flow: symptom → machine → era →
filtered checklist. No install, no server, no dependencies.

## What it covers

**Ten symptom paths** (Screen 1):
Won't start · Hard to start · Starts then dies · Runs rough or misses ·
Smoking (blue/black/white) · Overheating · No power / weak ·
Backfires or pops · Surges or hunts · Boiler / burner problem.

**Seven machine types** (Screen 2):
Tractor · Car/truck · Lawn mower · Boiler/furnace · Chainsaw/small ·
Pump/generator · Other engine.

**Four eras** (Screen 3):
Old iron (1800-1940) · Mid-century (1940-1980) ·
Emission era (1980-2000) · Modern (2000-now).

**Filtered checklist** (Screen 4): each symptom carries 8-14 checks,
each check tagged with which machine/era combinations it applies to.
Only checks that match the picked (machine, era) show. Tap to mark a
check green when confirmed.

Approximately 130 individual checks, each with a short *why* and *how*
line — written to be readable at arm's length in a shop with cold
hands.

## How to use

**On a phone:**
- Email `index.html` to yourself → open in browser → "Add to Home Screen"
- Or Bluetooth / USB the file to the phone → open with any browser
- Works offline once loaded; no network calls, no fonts, no images

**On a desktop:**
- Double-click `index.html`; opens in whatever browser is default

**On any device:**
- Copy the file to a USB stick, phone SD card, or shared folder
- The single file is the whole app; no other assets to bring along

## Design constraints (why it looks this way)

- **Single HTML file.** No CSS, JS, or image dependencies. One file is
  what survives being emailed, copied to a USB stick, or handed
  across a table on a phone.
- **Touch targets are ~44-80px.** Field use assumes gloves, cold
  hands, poor light. All buttons oversized on purpose.
- **No emoji, no color-only signals.** Reads on any browser including
  old feature-phone WebKit. Warnings use labeled tag chips, not just
  color.
- **No autocomplete, no forms, no state save.** Every session starts
  fresh; nothing persists. This is intentional — no leaking a shop
  session to a next user.
- **Progressive filtering.** Each screen narrows the possible set;
  Screen 4 shows only checks relevant to the picked machine + era
  combo. Modern-only checks don't clutter old-iron flows.

## Adding a checklist item

Edit `data` in the `<script>` block at the bottom. Each entry is:

```js
{t:'Check title', d:'What it means / how to check.', tags:['modern','tractor']}
```

Tags: `all` (always show), or any combination of machine keys
(`tractor`, `car`, `lawn`, `boiler`, `small`, `pump`, `other`) and
era keys (`old`, `mid`, `emission`, `modern`).

## What it is not

- **Not a diagnostic authority.** It is a memory-jog and structured
  triage tool. The mechanic is you.
- **Not a substitute for the shop manual.** Torque values, timing
  specs, and tolerances live in the machine's manual — this guide
  points you at *what* to check, not what the number should be.
- **Not a safety code.** Boiler pressure tests, gas leaks, and CO
  levels can kill. The guide flags known-dangerous conditions
  (puffback, LWCO trip, CO from bad burner) but assumes the operator
  knows their local safety rules.

CC0.
