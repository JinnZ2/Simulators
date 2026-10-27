# FIELD LEDGER 001 — first live entries
### Ingested 2026-09-24. Source: 4 photos, transcribed to text via DeepSeek (upload failed).
### PROVENANCE FLAG ON ALL FOUR: field-observed, AI-transcribed, **pixels unverified**.
### The transcription is a derived record — an intermediary reading. Errors it made are
### invisible to this ledger until the photos themselves are checkable.

---

## ENTRY 001 — road condition, unpaved (logging road)
```
timestamp    2026-09-24 (ingest; photo date UNKNOWN)
unit/road    unnamed logging gravel road — wooded corridor
observation  reddish-brown unbound surface; deep parallel tire ruts from
             heavy vehicles / aggressive tread; surface soft enough to hold
             footprints; recently trafficked
context      clearing ahead with parked vehicles — active use
provenance   field-observed, AI-transcribed
expected     n/a (condition baseline, not a claim check)
confound     recent rain unknown; traffic composition unknown
```
**Ledger value:** a dated (pending photo metadata) unpaved-road condition point.
Deep rutting in soft surface = the exact physical regime from WP1 that no autonomy
stack has commercial miles on. If this road is on any route you run regularly, repeat
photos over time turn it into a **rut-growth series** — the roughness-rate number the
desk literature estimates and nobody on the ground measures.

## ENTRY 002 — road condition, paved (baseline + weather)
```
timestamp    2026-09-24 (ingest); registration sticker "May 2026" bounds photo date
unit/road    two-lane paved highway, good condition
observation  smooth pavement; solid yellow / dashed white markings present and legible;
             shelf cloud approaching (storm inbound)
provenance   field-observed, AI-transcribed
```
**Ledger value:** paved control point — markings present and legible (the
machine-readability standard from WP2 assumes this; here it holds). The shelf cloud is
a condition note: storm + driving is the operating state where the human ability the
fatigue regs protect gets exercised most.

## ENTRIES 003 + 004 — one incident record (parked-vehicle damage)
```
timestamp    2026-09-24 (ingest); incident date = "found on returning to truck"
unit         your truck — gate guard (bull bar), top curve of tubing
observation  deep scrape through black coating to substrate, with scuff marks
evidence     red/white-striped bumper-like object left on grass at the scene,
             beside a concrete curb — per your context, the DOT trailer bumper
             from whoever hit the guard
provenance   field-observed, AI-transcribed
```
**⚠ DISCREPANCY FLAG (the pipeline working as designed):** DeepSeek's readout
describes entry 004's object as a *concrete parking wheel stop with red/white
reflective stripes*. Your context calls it a *DOT trailer bumper*. Those are different
objects with different implications (parking-lot fixture vs. trailer hardware torn off
in the strike). One of the two descriptions is wrong, or the object is genuinely
ambiguous from the photo. **Held UNRESOLVED — not smoothed.** Resolution path: the
photo itself, or one glance from you.

**Ledger value:** this is the parallel-record principle in action, unprompted — scene
evidence photographed at discovery time: damage documented (003), the other party's
leavings documented (004). For any claim/dispute: dated photos of both the wound and
the weapon, in place, beat any after-the-fact statement.

---

## WHAT THE TEST EXPOSED (meta — worth more than the entries)

1. **The intermediary problem, live.** The photos couldn't reach me, so the record
   arrived through a second AI's readout. That made every entry *derived*, not raw —
   closure-cost's instrument branch in miniature: the transcription becomes the reading
   and the pixels stop being sampled. The discrepancy on entry 004 is exactly the failure
   this predicts. Mitigation until uploads work: provenance flag stays on, and any entry
   where the transcript smells wrong gets flagged rather than resolved by guessing.
2. **One-sentence discipline held.** Your context lines ("the scratch you found upon
   returning," "left behind by whoever") were the highest-value content in the whole
   dump — the transcription described objects; your words supplied the *event*. The
   worker's one sentence is doing more work than the image model's paragraph.
3. **Ledger grows by contrast, not volume:** one unpaved + one paved + one incident is
   already a usable shape — condition series, control point, custody record.

## ONE QUESTION (per spec, max one)
Is entry 004's object metal trailer hardware or a concrete wheel stop? One word settles it.

---

## RESOLUTION — ENTRY 004 (photo received 2026-09-24; direct pixel read)

The photo settles the object class and vindicates **both** descriptions in part:

- **DeepSeek was right about the object:** it is a *concrete* beam — aggregate texture,
  weathering, and a broken end showing a mounting-pin hole are all visible. Not metal
  trailer hardware. Wheel-stop class.
- **The operator was right about the tape:** the red/white alternating reflective bands
  are **DOT-C2 conspicuity tape** — trailer-spec marking. Ordinary wheel stops don't wear
  it. That's the detail that made "DOT trailer bumper" a reasonable field label, and the
  transcription read the tape as decoration rather than as the identity clue it is.
- **New observations from the pixels the transcript missed:** the right end is *broken*,
  with a visible pin hole — consistent with the beam being forcibly ripped from a mounted
  position (wheel stops are pinned into pavement).
- **POSITION CORRECTION (operator, 2026-09-24):** the grass location is NOT the incident
  scene. The beam was found **in front of the truck, in the traffic path** — a hazard to
  other vehicles — and the operator moved it to the grass before photographing. Scene
  altered before imaging, for public-safety reasons. Recorded as: *original position:
  travel lane/parking area in front of unit; photographed position: post-intervention.*
  The act is also ledger content on its own: an unpaid, unasked hazard removal by the
  person who had just discovered damage to their own equipment — the doer maintaining
  infrastructure the responsible party left dangerous.
- **Interaction chain, narrowed but not closed:** the beam ended up *in front of the
  truck in the travel way* — consistent with the striker dragging/carrying it there from
  its mount and leaving it, or the truck itself pushing it on arrival (operator's call on
  whether it was present before parking: UNKNOWN). Gate-guard scrape remains consistent
  with concrete-on-steel. Striker identity: not determinable from the two photos.

**Meta-lesson, recorded:** the intermediary transcription got the *object class* right and
missed the *salient evidence* (tape spec, break pattern, displacement). The operator's label
got the *evidence* right (DOT tape = trailer connection) and the object class wrong.
Neither record alone was sufficient; the disagreement between them is what forced the
pixel check. Two imperfect readings that disagree beat one smooth reading that doesn't —
the discrepancy flag did its job.

---

## ENTRY 005 — road condition, paved divided highway, active snow (DIRECT PIXELS)
```
timestamp    2026-09-24 (ingest; photo date UNKNOWN — no metadata extracted)
unit/road    divided highway, cab POV, active heavy snowfall
observation  lane markings fully buried under snow cover; visibility limited
             (few hundred feet to whiteout); wipers running, snow accumulation
             on wiper arms; treeline corridor both sides; no other vehicles
             visible; windshield sticker lower-left (unread at this resolution)
intervened   n/a — driving condition, not a scene
provenance   field-measured, direct pixels (no intermediary)
expected     n/a (condition record)
confound     timestamp unverified; location unrecorded; whether plows had
             passed recently unknown
```
**Ledger value:** first direct-pixel winter condition point. This is the WP2 finding
caught in the wild: the machine-visibility spec (markings 150mm wide, 150mcd
retroreflective, "maintained more stringently than for human-driven vehicles") is not
*degraded* here — the markings are *gone* under snow, on an ordinary working day, and
the human is driving it on judgment. Any autonomy claim for this corridor class has
to answer: what does the stack do for the hours the road looks like this? Nobody's
demo envelope includes it (demo corpus check #4: envelope declared — winter-obscured
markings appeared in zero of 16 records).

**Series potential:** if this is a regular run, dated repeats across the winter build
the *fraction-of-season markings unreadable* number — a quantity that exists nowhere
in the autonomy literature and directly prices the human-in-the-seat dependency.

## ENTRY 006 — equipment damage, trailer mudflap torn loose (DIRECT PIXELS)
```
timestamp    2026-09-24 (ingest; photo date UNKNOWN; "Galaxy A15 5G" watermark)
unit         trailer — rear axle area, curb side
observation  metal-reinforced rubber mudflap torn/detached at its upper mount,
             bent outward ~90°, lower end dragging toward pavement; DOT-C2
             red/white conspicuity tape on flap bracket still legible; chunks of
             broken ice on pavement directly below the flap; duals + tread visible,
             tread present, no obvious chunking at this angle
mechanism    consistent with ice buildup (frame/body ice) dropping or being
             flung into the flap and tearing it from the mount — classic cold-ops
             failure; alternative: strike by road debris. Ice chunks at scene
             favor buildup-drop.
intervened   UNKNOWN — photo shows flap still detached at capture; whether
             re-secured, zip-tied, or swapped later is not recorded
provenance   field-measured, direct pixels (no intermediary)
confound     flap age/condition before event unknown; mount hardware condition
             (corroded vs sound) not readable at this angle
```
**Ledger value:** first equipment-wear entry — and it lands on the wear-provenance
problem from the Komatsu unmeld. If this flap gets logged anywhere as "wear," the
cause (ice event, a winter-ops condition) is exactly the kind of variable that
disappears when a desk system aggregates "maintenance events per mile" without the
mechanism. One word at capture time ("ice tore it") is the whole difference between
a wear statistic and a lie.

Also the doer-as-sensor cell from the automation audit: no system on that trailer
detected or reported this. The detection channel is the human walking around the
vehicle — the same pretrip the AHS ledger counts as overhead to be eliminated.

## ONE QUESTION (per spec, max one)
Entry 006: did the flap get field-secured (zip-tie/wire) or swapped at a shop?
One word settles it — it decides whether this is a *field-repair* record or a
*deferred-to-shop* record, which changes what the entry proves about the dependency
chain.

---

## UPDATE 2026-09-24 (operator answers + new field knowledge)

**ENTRY 005 — series ACTIVATED.** Operator confirms: these are the regular roads.
Nice asphalt is a luxury, even in storms — meaning the buried-markings condition is
not an edge case on this corridor, it's the default winter state. The
*fraction-of-season markings unreadable* series is live: any future winter shots from
regular runs add points automatically, no extra work — snap if you think of it,
ignore if you don't. Entry 001's rut-growth series inherits the same activation if
the logging road is on a regular run (assumed yes pending contradiction).

**ENTRY 006 — MECHANISM CORRECTION (operator, supersedes the ice-drop reading):**
the flap was **clipped by someone while the truck was parked during a rural
delivery** — discovered on return to the unit. Third-party strike, no responsible
party identified. The ice reading was mine, not the operator's, and it's corrected:
the chunks on the pavement were read as mechanism; they were background.

**But the correction comes with a multiplier the desk model doesn't have:**
operator note — *ice gets heavy, and at -30°F (-34°C) it wears metal and rubber
differently than expectations.* Applied here: cold-soaked rubber doesn't flex, it
tears. A clip a flap would survive in summer takes it off the mount at -30°F. So
the corrected mechanism is two-part: **cause = parked strike; severity multiplier =
cold-brittle materials.** Neither part alone explains the damage state.

**ONE QUESTION — status: UNANSWERED, left open (not re-asked, zero-burden).**
Field-secured vs. shop-swapped stays UNKNOWN. If a future entry shows the repair,
it closes itself.

**PATTERN FLAG — parked-strike discovery is now 2 of 6 entries.** Entry 003/004
(gate guard, beam left in traffic path) and entry 006 (mudflap, clipped during rural
delivery) are the same event class: damage to a parked truck, discovered on return,
responsible party gone, cost lands on the operator. Two instances in one small batch
says this is a recurring exposure of rural delivery work, not bad luck. If a third
shows up, this becomes its own series with a count and a cost column — the number
that decides whether "driver should have checked" policies or lot-design complaints
have any ground to stand on.

## ENTRY 007 — field knowledge, materials behavior in extreme cold (operator statement)
```
timestamp    2026-09-24
type         field-knowledge note (experience-based, not yet quantified)
statement    ice accumulates heavy on equipment; at -30°F (-34°C), ice loading
             wears metal and rubber differently than expectations
source       operator, direct experience, regular cold-ops corridor
provenance   field-knowledge (operator testimony — highest tier of this ledger
             for mechanism claims; below measurement, above any desk estimate)
status       STANDING NOTE — attach to any future cold-weather equipment entry
```
**Why this gets its own entry:** this is exactly the knowledge class the whole
field layer exists to catch. Component datasheets rate rubber and steel to
temperature points from lab tests; nobody's spec sheet says "behavior changes at
-30°F *under ice load*," and nobody behind a desk is measuring it. It already
changed one entry's mechanism reading (006). It will change others — cold-brittle
rubber reframes what "wear" means for every winter component: flaps, air lines,
tire sidewalls, suspension bushings, gladhand seals.

**Cross-thread connection:** this is the wear-provenance problem (Komatsu unmeld,
U3) with the sign flipped — there, bundled surface upgrades inflated autonomy's
wear gains; here, unrecorded cold/ice conditions inflate the *baseline* wear that
gets attributed to operator or equipment quality. Same disease: mechanism missing
from the record. One word at capture time is the cure in both directions.
