# Field Fabrication & Materials Reference

Single-file offline mobile app for making precision tools and processing
raw materials from scratch. Ten sections navigable from a two-column
menu. No install, no server, no dependencies.

## What it covers

**Ten sections**, each self-contained and pointer-navigable:

1. **Lime** — burning limestone (CaCO3 → CaO), slaking, three lime
   types (quicklime / putty / hydraulic), whitewash recipes,
   far-north cold-weather setting notes.
2. **Ammonia** — field production from urine or fermented waste,
   optional concentration by distillation, dilution ratios for
   cleaning / degreasing / paint stripping / pest deterrent.
3. **Aluminum Smelting** — scrap identification by source (cans →
   3004, pistons → hypereutectic Al-Si, rims → 356, ladders →
   don't cast wrought), furnace types (charcoal / propane / waste
   oil), crucibles, green sand / lost foam / investment mold
   procedures.
4. **Straight Rules** — the three-plate method for generating
   flatness from nothing, scraping tools, casting + scraping an
   aluminum straightedge, testing straightness without instruments.
5. **Squares** — 3-4-5 triangle and Thales' theorem for generating
   90° from scratch, building a try square, the flip test.
6. **Levels** — spirit-level construction (vial curvature matters),
   the water level (accurate to 1/8" over 100 ft, no calibration),
   plumb-bob level for vertical.
7. **Plumb Bobs** — casting from aluminum, center-of-mass tuning by
   filing, point sharpening, testing vertical, cold-shop tips.
8. **Sextants** — double-reflection principle, materials (front-
   surface mirror requirement, half-silvered horizon mirror),
   graduating the arc (~0.105"/degree at 6" radius), vernier scale,
   noon latitude sight reduction.
9. **Dividers & Calipers** — forging from scrap steel, spring
   joints, hardening points, transfer technique.
10. **Angles & Protractors** — generating any angle geometrically,
    building a protractor from a semicircle, bevel gauge
    construction, tangent method.

Each section carries: quick-reference data cards, procedure steps
with why/how notes, warning/tip/note callouts, and material tables
with tradeoffs.

## How to use

**On a phone:**
- Email `index.html` to yourself → open in browser → "Add to Home Screen"
- Or Bluetooth / USB the file to the phone → open with any browser
- Works offline once loaded; no network calls, no fonts, no images

**On a desktop:**
- Double-click `index.html`; opens in whatever browser is default

## Design constraints (why it looks this way)

- **Single HTML file, ~90KB.** Everything inline — CSS, JS, layout.
  Survives being emailed, copied to a USB stick, handed across.
- **No fonts, no images, no icons.** System font stack only. Every
  visual element (data cards, step markers, formulas) is HTML+CSS,
  no external assets.
- **Every claim is standalone.** No cross-references to "see the
  video" or "download the manual." The section you're on has what
  you need.
- **Standard viewport meta but scale is not locked.** Unlike the
  engine/boiler triage app, this one has denser text — the user
  needs to pinch-zoom on precision numbers.
- **No state saved.** Reset on each session; no progress or
  bookmarks stored. Straightforward on any device without
  permissions.

## Adding a new section

1. Add a button to the `.toc-grid` block:
   ```html
   <button class="toc-btn" onclick="showSection('my-new-section')">My Section</button>
   ```
2. Add the section container after the last `</div>` closing an
   existing `.section`:
   ```html
   <div class="section" id="my-new-section">
     <div class="back-bar"><button class="back-btn" onclick="showSection('toc')">Back to Menu</button></div>
     <div class="section-title">My Section Title</div>
     ...
   </div>
   ```
3. Available styling classes: `.data-grid`+`.data-card`,
   `.step`+`.step-num`+`.step-body`, `.formula`, `.note`,
   `.warning`, `.tip`, plain `<table>`, `<h3>`, `<h4>`.

## What it is not

- **Not a chemistry textbook.** Formulas are for orientation. A
  serious chemistry reference and safety training precede any
  ammonia distillation or acid work.
- **Not a metallurgy course.** Alloy identification uses common
  scrap sources and spark tests. For structural work, get real
  material specs.
- **Not a navigation manual.** The sextant section is enough to
  build one and take a latitude sight. Nautical almanac data and
  sight reduction come from other sources.
- **Not a substitute for shop safety training.** Molten metal, hot
  lime, ammonia vapor, and acid all appear here. The warnings are
  reminders, not full safety instruction.

CC0.
