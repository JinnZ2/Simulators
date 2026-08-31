# GAP 15 — BRIDGE HYDRAULICS: Debris Clog, Impoundment, and Release

*Draft entry for `UNDERGRADUATE_RESEARCH_GAPS.md`. CC0.*

**Gap:** `SCOPE_BOUNDARY.md`'s cascade has *"downstream bridge traps
debris"* as an explicit link. The bridge-scour and debris-scour
literature is quantified in the 2024-2025 record. The term the cascade
actually needs — the bridge as a **transient impoundment** that clogs,
ponds, fails, and releases — is not studied. It falls between
transportation engineering and dam safety, and neither field owns it.

**Knowledge state:** NOT_STUDIED (the impoundment/release term)
**Input knowledge states:** UNDER_STUDY (the scour and clogging inputs below)

The scour literature measures damage to a **standing** structure. The
cascade needs the structure's behavior as an **obstruction that fills,
holds water, and then gives way** — a dam-break problem wearing a
bridge's name.

---

## What is already quantified (do not re-derive)

| Quantity | Measured value | Source |
|---|---|---|
| Debris scour amplification, rectangular debris | +42–47% | Scientific Reports (Nature, 2025), s41598-025-34364-x |
| Debris scour amplification, semi-circular | +30–43% | same |
| Debris scour amplification, triangular | lower (upstream positioning partially shields the pier) | same |
| Abutment vs pier scour under debris | abutment scour consistently exceeds pier scour | same |
| Scour hole length increase (buried debris) | +~50% vs pier alone | ResearchGate, buried-debris scour-evolution study |
| Scour hole width increase (buried debris) | +~180% vs pier alone | same |
| Temporal behavior | prior work used fixed jam geometry; real jams grow during the event | J. Hydraulic Eng. (ASCE, 2024), 150(5) |
| Clogging threshold | pier spacing ≤ 10 m substantially increases clogging risk | Water Resources Research (Wiley, 2025), 2024WR039218, Belgium/Germany 2021 floods |
| Successive bridges | upstream bridge reduces downstream pier scour 30–40% (standing-structure case only) | J. Infrastructure Preservation & Resilience (Springer, 2025), s43065-025-00138-y, HEC-RAS |

**CITATION STATUS: located by search, not asserted as the source set the
module arithmetic was built from.** These confirm the mechanism is
quantified; matching them to the repo's equations is step zero for the
student who opens this gap.

---

## Instrumented cascade case and standing record (Norway)

The table above is standing-structure scour. The impoundment/release
term the gap actually needs has a MEASURED analogue — a moraine-dam
breach that produced a debris flow, with post-event morphology in hand:

| Case / record | What it gives | Source |
|---|---|---|
| moraine-dammed lake breach → 240,000 m³ debris flow, erosion and morphology measured | a measured instance of the chained-process shape (impoundment breach → debris flow), not a reconstruction — the same chain the bridge case needs | Breien, De Blasio, Elverhøi & Høeg (2008), Landslides 5(3):271–280, 10.1007/s10346-008-0118-3, Fjærland, western Norway, 8 May 2004 |
| NVE national GLOF event register — pre-1950 events (Liestøl 1956), GLACIORISK to 2003, referenced documentation to 2014, annual updates ("Glaciological investigations in Norway", e.g. Rapport 27/2022) | a continuous instrumented record maintained by the national water and energy directorate — long series is the instrument a slow debris/sediment rate requires | NVE, glacier.nve.no/Glacier/viewer/GLOF/en/ |

**INDEX-TERM NOTE.** The NVE register serves an English page and was
always reachable, but it does not rank on an English-language query
because the phenomenon indexes under `jøkullaup` / `skred` and the
institution under `NVE`. Reaching it required querying the native term
and the institution name directly. This is a retrieval barrier, not a
language barrier — the source is in English. Treat the register as a
DATA SOURCE (tier OPEN), not merely a citation.

**SIGN CAVEAT — carried from the standing-structure table.** The
successive-bridge finding (upstream bridge reduces downstream pier scour
30–40%) is a NEGATIVE interaction term and holds only for standing
structures under sustained flow. It must NOT be carried into the
release case, where the sign is expected to reverse: a failed upstream
impoundment loads the downstream structure rather than shielding it.

**SIGN CAVEAT — do not import the protective finding.** The "successive
bridges" result is a *negative* interaction term — upstream structure
shields downstream structure — which is the **opposite sign** from the
dam chain, where upstream failure amplifies downstream loading. It is
measured for the standing-structure, sustained-flow case only. It says
nothing about a bridge that clogs and fails, and must not be carried
into the release scenario. Testing the release case is the gap.

---

## The unstudied term

    scour literature has:        damage to A standing bridge        (measured)
                                 upstream bridge → downstream scour (measured, protective)
                                 clogging threshold (pier ≤ 10 m)   (measured)

    the cascade needs, and nobody owns:

        CLOG    debris from the upstream failure accumulates on the span
          ↓
        POND    backwater rises; upstream reach inundates
          ↓
        FAIL    span or foundation gives way (scour-driven or overtopping-driven)
          ↓
        RELEASE surge hydrograph + the bridge's own debris load
                delivered to the next downstream node

This is the `sediment-debris-biological-loop` marker applied to a built
obstruction. The debris that clogs the bridge is the **upstream
failure's output**, not an independent input — so the bridge does not
merely pass the cascade along. It **stores and re-releases** it, with
gain, because the jam grows during the event (the ASCE 2024 temporal
finding). A rate with gain, not a static offset.

---

**Research question:** Does a debris-clogged bridge act as a transient
impoundment whose failure changes the downstream breach set or the
exposure timing on the Columbia/Snake chain?

**Disciplines:** Hydraulic engineering, transportation/structural
engineering, dam safety, geomorphology

**Data sources:**
- National Bridge Inventory (NBI, FHWA) — location, pier spacing,
  waterway class, scour-critical rating
- USGS gage records and high-water marks (HWM)
- HEC-RAS 2D bridge routines (blocked-obstruction / perched-weir modes)
- Upstream debris supply sources: landslide inventories, mining rim-slope
  candidates (Gap 14), post-fire debris yield (Gap 2)
- USACE bridge scour and backwater studies
- The 2024-2025 debris-scour and clogging literature above

**Method:**
1. Inventory bridges on the Columbia/Snake mainstem and the tributaries
   below dam nodes; flag every span with pier spacing ≤ 10 m (the
   clogging threshold)
2. Estimate debris supply reaching each flagged bridge from upstream
   failure sources. **The debris that clogs is the cascade's output** —
   couple this to Gap 14 (rim slopes) and Gap 2 (post-fire yield), do not
   treat debris supply as an independent parameter
3. Model the clog state (partial → full blockage) and compute backwater
   rise using HEC-RAS bridge/obstruction routines
4. Model the impoundment: pond volume behind the clogged span and the
   upstream inundation footprint
5. Model the release: bridge failure produces a surge hydrograph plus a
   debris load. Feed it to the next downstream node as an **initiator, in
   the same interface a breach hydrograph uses** — this is the `CCC_007`
   comparability requirement (every initiator writes only a hydrograph;
   the routing engine downstream is identical)
6. Test the release case **independently** of the successive-bridge
   protective finding (sign caveat above)
7. Report: which bridges can clog, the backwater/pond envelope, and
   whether the release shifts the downstream breach set

**Expected deliverable:** A `bridge_impoundment.py` module supplying, per
candidate bridge: a clog-probability flag (pier-spacing based), a
backwater/pond envelope, and a release hydrograph in the Module F
initiator interface. Every parameter carries a knowledge state and names
what would move it.

**Falsifier:** No bridge on the chain has pier spacing ≤ 10 m, OR the
maximum clog-induced backwater is below every downstream crest AND the
release hydrograph never shifts the breach set. Then the bridge term is
not load-bearing for this chain and the gap closes.

**Secondary falsifier (coupling):** Debris supply from all upstream
sources is below the clog-forming threshold at every flagged bridge.
Then bridges pass the cascade without storing it, and the loop term
drops — which also tests the coupling to Gaps 2 and 14 directly.

---

## Why this gap is different from Gaps 1-13

Same shape as Gap 14: it connects two bodies of measurement that already
exist — debris-scour hydraulics on one side, dam-break routing on the
other — across the institutional boundary between transportation
engineering and dam safety. Neither field is incomplete on its own
terms. The discontinuity is the seam between them.

And the mechanism it models is the debris loop's own structure: an
obstruction that accumulates its load during the event and releases it
with gain. A bridge evaluated only against its own design flood is the
single-event evaluation error — the same operator swap Module F already
proves. Independent evaluation asks whether the bridge survives its
flood. Coupled evaluation asks what it does when it is already holding
the upstream failure's debris and constricting flow into the next pool.
