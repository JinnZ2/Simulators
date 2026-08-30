# GAP 14 — MINING HYDROLOGY: Subsurface Alteration to Reservoir Loading

*Draft entry for `UNDERGRADUATE_RESEARCH_GAPS.md`. CC0.*

**Gap:** `SCOPE_BOUNDARY.md` places mining at the head of its own
example cascade — *"Mining destabilizes slopes -> heavy rain saturates
ground -> landslide enters reservoir -> displacement wave overtops dam"*
— but no gap in the agenda covers it. The subsurface effects are
quantified in the 2024-2025 literature. The term connecting them to
reservoir inflow or dam loading is not.

**Knowledge state:** NOT_STUDIED (the coupling term)
**Input knowledge states:** UNDER_STUDY (the subsurface parameters below)

This split is the whole point of the gap — but state it precisely. The
mining side is measured. The dam side is measured. And the Chinese
literature carries mining FURTHER than the English record does: through
to basin streamflow (Kuye River CWIM) and, separately, through to
dam-body stability (coal-mine underground reservoirs). What no record
carries is either of those to RESERVOIR POOL LOADING on a multi-dam
surface chain. The two carries stop one node short of each other, and
neither reaches a cascade. That remaining seam is a scope error under
`knowledge_state.py`, not an epistemic one.

---

## What is already quantified (do not re-derive)

| Quantity | Measured value | Source |
|---|---|---|
| Surface soil porosity, non-fissure unit | +7.42% vs undisturbed | Land Degradation & Development (Wiley, 2025) |
| Surface soil porosity, fissure unit | +19.25% vs undisturbed | same |
| Porosity driver | volume expansion of pores > 3 mm | same |
| Fracture zone height | 134-183 m, borehole-measured | Int. J. Mining Sci. & Tech. / ScienceDirect (2024) |
| Zone structure | caving / fracture / subsidence, distinct | same |
| Hydraulic conductivity | evolves spatio-temporally with the mining face | same |
| Fissure networks, hard vs weak rock | hard rock extends further vertically, denser interconnection, higher permeability coefficient | Scientific Reports (Nature, 2025) |
| Slope destabilization terms | three distinct: volumetric weight of slide body, strength softening, pore water pressure | Sci. Reports (2024), Thar Coalfield multi-aquifer open pit |
| Failure concentration | where the aquifer is exposed | same |
| Preferential flow | crack density / width / length / connectivity control vadose-zone paths | Water (MDPI, 2025), dual-domain crack-matrix model |

---

## What the basin-scale literature already carries (primary, not alternative)

The table above is the SUBSURFACE side. Separately, work that carries
mining THROUGH to basin hydrology and to dam stability already exists —
predominantly Chinese, because that is where the field has run longest
and where the 2025-2026 record is densest. Entered as peer sources, primary:

| Carry | What it establishes | Source |
|---|---|---|
| mining → basin streamflow / groundwater | InSAR-identified subsidence areas incorporated as a boundary condition in a coupled surface-water / groundwater model (CWIM) | Li, X. et al., J. Hydrol. 659:133243 (2025), 10.1016/j.jhydrol.2025.133243, Kuye River Basin |
| three-zone theory → groundwater impact | caving / fracture / subsidence zones used as the boundary condition feeding a groundwater calculation model | Li et al., River 4(1) (2025), 10.1002/rvr2.70000, Kuye |
| mining → streamflow reduction, quantified | statistical attribution of streamflow loss to mining, basin scale | Sci. China Tech. Sci., 10.1007/s11431-016-0393-4, Kuye |
| mining stress / seepage / fracture → DAM stability | multi-field coupled dam-damage evolution for coal-mine underground reservoir (CMUR) dams | Water 16(13):1856; Sustainability 16:10350 (Shigetai); 2026 review, Du T. et al. |

**CONFIGURATION NOTE — not a discount.** The dam in the CMUR work is a
coal-pillar dam INSIDE a mine, not a surface impoundment in a cascade.
The mechanism (stress / seepage / fracture coupling degrading a dam
body) transfers; the configuration does not. And Kuye is a semi-arid
loess basin with a depleting groundwater regime — the transfer to
Columbia hard-rock / gravel is a PHYSICS question about the two basins,
addressed in Method step 2. It is not a reason to rank these sources
below an English one.

**READ CEILING.** These are entered from English-language abstracts and
citation metadata. The CWIM boundary-condition formulation — the exact
thing that would plug into `mining_increment.py` — is not visible at
that depth. Retrieving the full text is a step in the method. This is a
capability limit on the audit, not an open question about the work.

---

## Governing equations (forms verified; two named citations are not)

**SLOPE STABILITY — Limit Equilibrium Method (LEM)**

    FoS = resisting / driving = (c·L + N_eff·tanφ) / (driving shear)
    inputs: cohesion c, unit weight γ, slope height H, friction angle φ,
            pore pressure u
    mining coupling: excavation/blasting raises pore pressure u
      → effective normal stress N_eff = N − u·L falls
      → FoS falls. this is the pore-pressure term the slope literature names.

Method family is textbook (Fellenius, Bishop-simplified, Janbu,
Morgenstern-Price, Spencer, Sarma) and needs no single citation.
Confirmed recent open-pit applications: non-coal open-pit LEM + FLAC3D
(2026); improved Sarma with nonhomogeneous hydraulic boundary conditions
(Sci. Rep. 2025, s41598-025-17972-5, Aynak open-pit copper).

**SUBSIDENCE — time function**

    canonical Knothe (CONFIRMED):
      dW/dt = c·(W₀ − W(t))   →   W(t) = W₀·(1 − e^(−c·t))
      W₀ max subsidence, c overburden mechanical coefficient
      [Zhang, Yan, Tan, Dong 2022, Sci. Rep. 12:18433,
       10.1038/s41598-022-23303-9, Barapukuria coal mine]

    sigmoidal / MMF family (alternative form, as supplied):
      Sₜ = W₀·t^b / (a + t^b)
      a,b geology-dependent; same asymptote Sₜ→W₀, same Sₜ(0)=0.
      one of the benchmarked family (MMF, Weibull, Usher, tanh,
      power-Knothe) in the InSAR time-function literature
      (Remote Sens. 2024, 16:1938)

**STRAIN INTEGRATION (subsidence from a vertical strain profile)**

    S = ∫[h₁→h₂] ε̄ dh
    mean vertical strain integrated over affected depth; dimensionally length.

**PROVENANCE FLAG — two citations could not be confirmed:**

    "Padhy et al. 2026, Springer" (LEM FoS)
      → no such author/paper surfaced. real 2026 open-pit LEM work
        exists; the FoS method is textbook and does not rest on it.
    "Piao et al. 2024, Nature"  (Sₜ = W₀·t^b/(a+t^b))
      → Piao C.D. is a real subsidence researcher (water-conducting
        fracture zones), but this specific paper/formula pairing did
        not surface. the Knothe form above IS confirmed — anchor on it,
        treat the MMF form as an alternative pending its real citation.

    same discipline as the ±10% breach figure: the math is sound, the
    two named attributions are not verified. resolve before a student
    cites them. do not publish "Padhy 2026" or "Piao 2024" as given.

---

**CITATION STATUS: UNVERIFIED-PROVENANCE.** The table rows above were located by
search, not drawn from the source set the module arithmetic was built
from. They confirm the mechanism is quantified; they are not asserted
to be the specific papers behind any equation in this repo. A student
opening this gap resolves the citations against the module arithmetic
as step zero.

**TRANSFER CAVEAT.** The subsurface rows are coal-basin work (China,
Pakistan); the basin-scale carries are loess / coal basins (Kuye). This
is a PHYSICS question about basin conditions — hard-rock and gravel
mining, different overburden, different aquifer structure — not a
discount on the sources. Establishing or refuting transfer is Method
step 2, part of the gap, not a precondition for it. The language of the
source carries no weight here; the geology of the basin carries all of it.

---

**Research question:** Does mining-induced subsurface alteration change
antecedent pool level, reservoir inflow timing, or reservoir-rim slope
stability enough to shift the breach set on the Columbia/Snake chain?

**Disciplines:** Mining engineering, hydrogeology, geomorphology,
geotechnical engineering, dam safety

**Data sources:**
- USGS Mineral Resources Data System (MRDS) — mine locations, commodity, status
- State mining permits and reclamation records (WA, OR, ID, MT, BC)
- USGS groundwater monitoring wells in mined watersheds
- InSAR subsidence products (Sentinel-1, ESA; USGS/JPL ARIA)
- NLCD land cover change over mined parcels
- USGS gage records for tributaries draining mined watersheds
- Reservoir rim stability assessments (USACE, BC Hydro, if published)
- The 2024-2025 subsurface literature above

**Method:**
1. Inventory mines in the Columbia/Snake contributing watersheds; classify
   by type (open pit, underground, placer, gravel), commodity, and status
2. Establish transfer or refute it: compare host-rock and overburden
   conditions against the coal-basin studies above. Where conditions
   differ materially, mark the imported parameter UNDEFINED rather than
   applying it
3. Measure subsidence extent from InSAR over each mined parcel; where
   subsidence is detected, apply the fissure/non-fissure porosity split
4. Propagate the porosity delta to a runoff-coefficient change via water
   balance. **Name the intermediate quantity explicitly** — do not let a
   subsurface storage change and a surface flow change share a variable
   name (see the stock/flow separation in Gap 1)
5. Convert to an antecedent pool increment using the same interface
   `contributing_inflow.py` uses for urban runoff:
   `pool_effective = pool_natural * (1 + increment_fraction)`
6. Separately, map mined parcels against reservoir rim slopes; flag
   parcels where the aquifer is exposed (the failure concentration
   condition), as candidate displacement-wave sources for Module F
7. Report the increment fraction and the rim-slope flag list with
   uncertainty bounds

**Expected deliverable:** A `mining_increment.py` module in the
`contributing_inflow.py` interface, supplying a mining-attributable
pool increment fraction per tributary watershed with uncertainty
bounds, plus a rim-slope candidate list keyed to node. Every parameter
carries a knowledge state and names what would move it.

**Falsifier:** The mining-attributable pool increment is < 1% for all
tributaries AND no mined parcel intersects a reservoir rim slope. Then
the mechanism is not load-bearing for this chain and the gap closes.

**Secondary falsifier (transfer):** The coal-basin porosity and
conductivity findings do not transfer to Columbia-basin host rock.
Then the imported parameters revert to UNDEFINED and the gap narrows to
a measurement problem: what IS the porosity delta for this rock?

---

## Why this gap is different from Gaps 1-13

Gaps 1-13 ask for a value that nobody has measured. This one asks for a
**connection between bodies of measurement that already exist**. The
mining literature does not stop at the aquifer — the Chinese work
carries it to basin streamflow and, separately, to dam-body stability.
But those two carries stop one node short of each other, and neither
reaches a multi-dam surface cascade. The discontinuity is at the
institutional boundary between mining hydrology and cascade dam safety,
which is precisely the condition `SCOPE_BOUNDARY.md` names as a scope
error rather than a knowledge state.

The omission of this gap from the original thirteen is itself an
instance of the mechanism the manifesto describes: *"If a variable is
not in the model, the model shows no sensitivity to it."* The agenda
dropped mining the same way standard breach models drop it. Recording
that here rather than silently patching it is the honest version, and
it is evidence for the thesis rather than against it.
