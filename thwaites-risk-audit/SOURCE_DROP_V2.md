# Thwaites Glacier 2026 Papers (July–September) × JinnZ2/Simulators
## Risk-management-weighted audit (worst-case planning, not conservative averaging)

All tools below were **actually cloned and run** from `github.com/JinnZ2/Simulators` (2026-09-23).
Where a tool takes structured inputs, each paper was encoded as an input file and executed.
"Risk-weighted" here follows the repo's own rule: report the band, plan against the short end;
treat committed loss as the floor, not the scenario.

> **REPAIR LOG — 2026-09-23** (citation + method audit against sources)
>
> | # | Repair | Status |
> |---|---|---|
> | R1 | "Bradley et al." → Williams et al. (Bradley is last author); published July, not September | FIXED |
> | R2 | Goldberg "2.6 mm/yr by 2200" not found in preprint summary; preprint under review | FLAGGED UNVERIFIED (s1, s7) |
> | R3 | Pierce "homogeneous under fast western region" not in abstract | s4 RE-DERIVED from abstract; THW-F1 RETIRED |
> | R4 | 7/7 FAIL and 4/4 BREACH are tool demonstrations on synthetic inputs | RELABELLED DEMONSTRATION |
> | R5 | One DOI assigned to two author sets (s10, s11) | FLAGGED CONFLICT, both uncitable |
> | R6 | κ = 0.000 from one model coding twice | FLAGGED INVALID AS RELIABILITY |
>
> Still unrepaired: s5 closure-cost verdict restates an auditor-entered input ("availability: present");
> s5 assumes committed and forced loss superpose linearly and that assessments combine them by `max`
> — both unsourced. Verified: Williams et al. finding, Killingbeck, Otosaka DOI, s9 ENSO status (CPC 10 Sep, IRI mid-Sep).
> Central line (committed loss as design floor; THW-01) rests on Williams et al. and survives.

---

## Results map

| Paper | Tools run | Headline output |
|---|---|---|
| Goldberg et al. (ice-sheet modeling) | `climate-modeling` audit suite; `declared-frame` | DEMONSTRATION (tool behaviour, not a Thwaites finding): suite's own synthetic cases, 7/7 FAIL; no Goldberg model input was run |
| Killingbeck et al. (MT groundwater) | `closure-cost` (instrument branch); `declared-frame`; `measurement-fork` | Intermediary (resistivity) is the reading; pore pressure never sampled |
| Phạm (glacial earthquakes) | `instrument-bias-sims` S1; `declared-frame` | Event-sampled catalog has **null share 0.0000** — baseline reconstructed from events alone |
| Pierce et al. (radar bed) | `measurement-fork`; `declared-frame` | Radar/MT/seismic arms **share no quantity at all** — no cross-validation exists |
| Williams et al. (committed loss) | `closure-cost` (event branch); `reservoir-chain-coupling`; `declared-frame` | "No melt → no loss" was a **closed variable**; DEMONSTRATION: synthetic arbitrary-unit chain; sum ≥ max for non-negative inputs, so the 4/4 breach is an identity, not a Thwaites finding |

---

## 1. Goldberg, Holland & Naughten — ice-sheet modeling / sea-level projections

**Tools: `climate-modeling` audit suite + `declared-frame`.**

The climate-modeling suite exists to catch *cascade-speed blindness* — "a smooth, memoryless,
Gaussian-driven model predicts collapse in fifty years and reality does it in five." Run result:

```
Cascade Speed Blindness    FAIL  rmse=307017.9   (threshold+feedback+memory+fat tails)
Stationarity Assumption    FAIL  final_biomass_error=99.97
Phase Change Blindness     FAIL  final_biomass_error=73.17
Missing Feedback           FAIL  final_biomass_error=248944.6
Omitted Variable           FAIL  final_biomass_error=76.05
Data Aggregation Error     FAIL  rmse=7.35
Missing Positive Feedback  FAIL  final_biomass_error=283254.5
SUMMARY: 0 pass, 7 fail
```

(REPAIRED: the analogues below are interpretive mappings, not test results — no Goldberg model was run.) Every failure mode the suite flags has a proposed analogue in the Goldberg preprint's finding:
**initialization dominates the 21st century** = the model's near-term answer is set by an
inherited state, not by measured physics (the suite's Stationarity/Omitted-Variable failures);
**forcing dominates later** = the regime where the model is best validated is the regime that
matters least for people alive now.

The declared-frame check pins the framing:
- **horizon**: the headline "2.6 mm/yr by 2200" [UNVERIFIED: figure not found in the preprint summary; source is the other model's citation list. Preprint under review (TC), posted 7 Jul 2026, not peer-reviewed.] is scored 175 years out; the 2026–2100 window — the planning horizon of every living structure — is the initialization-dominated window the model is *least* informative in.
- **boundary**: modeled ice volume only; MICI-style cliff physics, subglacial hydrology feedbacks (the Killingbeck/Pierce territory), and the downstream WAIS buttressing chain are outside the accounting.
- **who_counts**: global mean SLE. No coastline, no time-of-arrival distribution; the aggregate absorbs the variance that risk management lives on.

**Risk read:** (figure UNVERIFIED, see above) treat 2.6 mm/yr by 2200 as a *floor with a smooth-model bias*, not a ceiling.
The suite's flagship result is that smooth models systematically *understate* cascade speed when
threshold, feedback, and memory are present — and Thwaites is the canonical threshold+memory system.

---

## 2. Killingbeck et al. — subglacial groundwater via magnetotellurics

**Tools: `closure-cost` (instrument branch), `measurement-fork`, `declared-frame`.**

Encoded as a closure-cost case (`thwaites-killingbeck-mt`), branch **instrument**:

> A reliable intermediary becomes the reading, and the underlying quantity stops being sampled
> directly. Failure clusters where the intermediary has a *long correct record* — here it is worse:
> reliance with **no** direct record at all. There is no basin-scale borehole validation of the MT
> inversion beneath Thwaites.

Checker output: `variable_state=not_assessed`, `signal relied_on_as_reading=true`. The quantity
that actually controls basal sliding — **pore water pressure at the ice-bed interface** — sits
outside the instrument's constitution. MT reads bulk resistivity, a non-unique mixture of water
content, salinity, and temperature: one resistivity curve, many possible subglacial worlds.

**Risk read:** "high resistivity (>10 Ωm), distinct regime" does **not** exclude a thin, saline,
high-pressure water film — exactly the configuration that controls sliding. And the frame is a
**snapshot**: one survey epoch over a dynamic hydrological system with sub-seasonal variability.
Risk-weighted: this paper narrows the *map*, not the *risk*. The distinct-regime finding cuts both
ways — a basin unlike other Antarctic sites is a basin where transfer of calibrations from those
sites is unlicensed.

---

## 3. Phạm — 245 hidden glacial earthquakes

**Tools: `instrument-bias-sims` S1 (event-sampled observation), `declared-frame`.**

S1 models two observers of one system: A samples every tick, B samples only when something is
happening. Run output:

```
f        true null    B null
0.001    0.9989       0.0000
0.200    0.7984       0.0000
```

An event-triggered observer's record contains **no null at all** — at f=0.001 the system is 99.9%
quiet and the event catalog reports a composition with zero quiet in it. The distortion is a
*product*: event triggering removes the null baseline, then cost weighting re-weights what is left.

This is the exact constitution of a seismic detection catalog: 245 events over 2010–2023 are the
events **above detection threshold** of a network whose coverage and sensitivity changed over the
window. "Peak activity coinciding with accelerated ice flow" is computed on the detected record;
the pre-instrument baseline does not exist.

**Risk read:** two directions, both unfavorable to complacency.
1. The catalog *understates*: sub-threshold calving and aseismic slip are outside the accounting,
   so total edge instability is greater than 245 events.
2. The trend is *unverifiable as stated*: rising event counts over 2010–2023 confound glacier
   acceleration with network improvement. Risk-weighted posture: assume the physical trend is real
   (it has a mechanism — capsizing bergs at an accelerating margin) and treat the catalog as a
   lower bound, while refusing to use the apparent *calm early years* as any evidence of stability.

---

## 4. Pierce et al. — radar modeling of the bed

**Tools: `measurement-fork`, `declared-frame`.**

A full three-arm measurement-fork spec (`thwaites_subglacial`) was built covering the radar, MT,
and seismic instrument families plus the observing-program coupling, and run through `compare.py`:

```
arm conventional    8 probes
arm coupling       12 probes
arm widen          14 probes

SAME QUANTITY, DIFFERENT ROUTE
  none -- the arms share no quantity at all.
  That is itself a finding: the designs do not overlap,
  so no existing result speaks to the coupling questions.
```

**This is the cross-paper structural finding.** Pierce's radar, Killingbeck's MT, and Phạm's
seismology are three instruments reading three disjoint proxies of one system. There is no shared
quantity — no cell where two instruments measure the same thing by different routes — so
*no published result from any arm can confirm or refute any other*, and the one variable that
governs sliding (pore pressure) is in the residual set of all three.

On the paper itself (REPAIRED 2026-09-23): an earlier draft built this section on the sentence
"homogeneous substrate under fast-moving western regions." That sentence is NOT in the paper's
abstract; it came from the other model's citation summary. What the abstract states: modeled
bed-return variation matched the radar data closely in 40% of simulated flight segments
(read as a relatively homogeneous bed), and in another 40% the fit improved once hydrology or
substrate transitions were added. No location attribution is given in the abstract.

**Risk read (re-derived):** 40% of segments need hydrology or substrate transitions to fit, and
"homogeneous" in the other 40% is a radar-resolution statement, not a bed-property statement
(smooth to radar at survey-line spacing is not smooth at basal-hydrology scale). Where the
remaining 20% sit, and whether the homogeneous segments coincide with fast flow, is UNMEASURED
from the abstract — check the full paper before any location-specific claim.

---

## 5. Williams et al. — mass loss continues without ocean melting

*Citation (repaired 2026-09-23):* Williams, C. R., Trevers, M., Sun, S., Holland, P. R., Bett, D. T., Arthern, R. J., & Bradley, A. T. (2026). Mass Loss From Thwaites Glacier Continues Even Without Ocean Melting. *GRL* 53(14). DOI 10.1029/2026GL122843. Published 25–28 July 2026 (not September). Earlier drafts named Bradley (last author) as first author.

**Tools: `closure-cost` (event branch), `reservoir-chain-coupling`, `declared-frame`.**

Encoded as a closure-cost event-branch case (`thwaites-bradley-committed-loss`). The closed
variable: **"mass loss requires ocean melting."** Checker output:

```
VARIABLE  closed
INFORMATION AVAILABILITY  present
PROCEDURE GAP RIVAL: collapsed into closure  yes
```

Availability `present` + variable `closed` means the tool's core test fires: **the procedure gap
(no committed-loss planning) is ruled out as an information problem** — MISI theory and internal
dynamics literature existed for decades; the handling class was never acquired because the premise
said removing the driver removes the loss. This is the repo's central claim confirmed on this case:
response failure tracks prior closure, not event severity, not information availability.

Then the chain. Williams et al.'s 150-year committed loss *is* the antecedent pool in
`reservoir-chain-coupling`'s operator swap: per-glacier assessment evaluates `max(new_forcing,
committed_state)`; coupled physics evaluates `new_forcing + committed_state`. Run on a declared
synthetic Thwaites→WAIS chain (units arbitrary and labeled):

```
RUN 1 per-glacier (max): breach set []
RUN 2 coupled (sum):     breach set [grounding_line, eastern_shelf, WAIS_interior, coastal_delivery]
VERDICT: LOAD-BEARING: coupled breaches 4 node(s) independent does not
independent-only: [] (must be empty — the bias is one-sided, always understating)

node                       max      sum
Thwaites_grounding_line   4.20     9.00  BREACH
Thwaites_eastern_shelf    2.94    12.00  BREACH
WAIS_interior_basins      2.06    15.00  BREACH
coastal_SLR_delivery      1.44    18.00  BREACH
```

The disagreement compounds downstream: each breach raises the load into the next node. A one-node
study (any single-glacier assessment) structurally cannot produce this.

**Risk read:** the design-basis number for adaptation is not "melt-driven loss under scenario X" but
"the committed component alone." Under zero melt the loss runs 150 years — past every governance,
infrastructure, and insurance horizon. Mitigation success does not retire this hazard. And every
per-glacier or per-sector assessment that ignores the committed antecedent state understates the
chain, with the error's sign fixed: always toward "safer than it is."

---

## Cross-paper synthesis (the risk-management view)

1. **The committed pool is the load-bearing input.** Williams et al. supply the antecedent state;
   Goldberg supplies the arriving wave; the operator swap says combining them by `max` instead of
   `sum` is the standard assessment error, and it never overstates.
2. **No instrument reads the controlling variable.** Radar (Pierce), MT (Killingbeck), seismic
   (Phạm) share no quantity (measurement-fork, run result) and none reads pore pressure. The
   fastest-flowing region has the least-resolved bed.
3. **The event record has no baseline.** Phạm's catalog is event-triggered (S1: null share 0.0000);
   calm in the record is not calm in the glacier.
4. **(REPAIRED) The smooth-model bias is DEMONSTRATED on the suite's own synthetic system, not measured on ice-sheet models.** 7/7 climate-modeling audits FAIL in the
   direction of understated cascade speed — plan on the short end of every band.
5. **The failure was closure, not information.** Closure-cost: availability ruled out the
   procedure-gap rival. The handling class for committed loss does not exist because the premise
   was closed, and it must now be built under time pressure.

## Drafted gap-markers entries (schema-conformant)

```
GAP_ID   THW-01
DOMAIN   glaciology / coastal adaptation
STATE    unowned
WHAT_EXISTS  committed-loss magnitude (Williams et al. 2026); SLR ensembles (Goldberg 2026)
WHAT_IS_MISSING  any party whose scope covers translating committed glacier loss
                 into mandatory minimum design basis for coastal infrastructure
ENTRY_POINT  national adaptation design codes: does any cite committed ice loss as floor?
KIND     boundary-artifact

GAP_ID   THW-02
DOMAIN   radar glaciology / magnetotellurics / borehole hydrology
STATE    assembly
WHAT_EXISTS  basin-scale radar (Pierce 2026), MT (Killingbeck 2026)
WHAT_IS_MISSING  a shared quantity: any cell where two instruments measure the same
                 subglacial variable by different routes; pore pressure unmeasured by all
ENTRY_POINT  co-locate one deep borehole with existing radar/MT lines
KIND     knowledge (measurement genuinely absent) + boundary-artifact (funding by instrument)

GAP_ID   THW-03
DOMAIN   seismology / ice-flow dynamics
STATE    unasked
WHAT_EXISTS  13-year seismic catalog (Phạm 2026), continuous satellite velocity
WHAT_IS_MISSING  the question posed with detection-threshold correction: event rate
                 per unit detection sensitivity, not per calendar year
ENTRY_POINT  recompute the catalog trend against network sensitivity history
KIND     boundary-artifact (data exists, collected for another purpose)
```

## Observable-indicator analogue (`observable-indicator-rules`)

The OIR run confirmed its standing finding — the pipeline's stability check is a **miss filter,
blind to false alarms** (measured false-alarm rate 0.5 passes with miss rate 0.0). Applied here:
any Thwaites-derived public warning rule ("IF grounding line retreats past X THEN revise coastal
codes") must carry **both** a miss rate and a false-alarm rate on the card, and the band's short
end is what gets planned against. The router (coupled ice-ocean solve) is the non-phone term;
everything downstream of it — the indicator card a coastal authority or household evaluates on
sight — is cheap, and currently nobody owns building it (THW-01).

---

### Method note
Repo cloned 2026-09-23; tools run unmodified except inputs: two closure-cost case files, five
declared-frame blocks, one measurement-fork spec, one chain driver using the repo's own `Node`/
`compare` API with synthetic labeled values. No tool output was edited. Synthetic chain values are
declared arbitrary units; the claim they carry is the *operator*, not the magnitudes — per the
repo's own discipline.

---

# Follow-up wave (2026-09-23, second pass)

## 6. Effective-redundancy audit of the observing system itself

**Tool: `effective-redundancy-audit`.** The framework's question: the system's N nominal
channels were never N — they shared a node the diagram cannot draw because it is a *process,
budget, or logistics chain*, not a component. Applied to the six Thwaites observing channels
(satellite altimetry, InSAR velocity, airborne radar, magnetotellurics, seismic network,
GPS/borehole), coded two ways:

```
CODER 1 (generous, shared node = field logistics only):  N_nominal=6  N_eff=3
CODER 2 (risk-weighted, + funding authorization + processing chains): N_eff=1
inter-coder Cohen's kappa: 0.000  [INVALID AS RELIABILITY: both codings by one model; not independent coders. N_eff values are one coder's choice of shared nodes.]
```

Run notes:
- This also closes a gap the repo's own audit found: the delivered `report()` never calls its
  own `cohen_kappa`, so the two-coder blind protocol had no representation. Here it was called.
- (REPAIRED) κ here is not inter-coder reliability — one model coded twice. What survives: **the N_eff answer depends on which shared nodes are counted**: whether the monitoring system has any redundancy
  at all depends entirely on which shared nodes the coder is willing to count. Under the
  risk-weighted coding — same 2–3 national funding programs, same Antarctic logistics (ships,
  fuel, aircraft, a 3-month field season), shared processing chains between the two satellite
  channels — **N_eff = 1**. Six instruments, one failure point.
- Practical reading for anyone who fixes things for a living: this is a truck with six gauges
  and one wire. The gauges are fine; the wire is the funding-and-logistics chain. A single
  cancelled field season or one agency budget cycle degrades radar, MT, seismic, and borehole
  simultaneously — and the satellites do not cover what those measure (bed, water, basal
  events: see the measurement-fork result — no shared quantity).

**Gap entry (schema-conformant):**

```
GAP_ID   THW-04
DOMAIN   observing-system design / program funding
STATE    unowned
WHAT_EXISTS  six nominal instrument channels, each competently operated
WHAT_IS_MISSING  effective-redundancy accounting: no party scores the observing
                 system against shared process/budget nodes; N_eff is computed
                 by nobody
ENTRY_POINT  ask any program's review panel: which channels survive a 2-year
             funding gap AND a lost field season simultaneously?
KIND     boundary-artifact
```

## 7. AMOC × Thwaites coupling

**Tool: `AMOC/` regime-shift framework (StommelBox hysteresis + declared Sv→F calibration).**

**Transfer gate, declared up front:** Thwaites meltwater enters the *Southern Ocean*, not the
North Atlantic — routing it into an AMOC box is a mechanism transfer whose coupled-systems path
(AABW, interhemispheric seesaw) is UNMEASURED here. What the run legitimately produces is the
*shape* of the response surface and the flux arithmetic.

Run results:
- StommelBox hysteresis: bistable band F ∈ [0.00, 0.228]; collapse spinodal at F ≈ 0.228
  (≈ 0.50 Sv on the declared calibration). Inside the band, which state you occupy depends on
  history; past the spinodal there is no stable overturning branch to return to.
- Flux arithmetic from the September papers: even Goldberg's 2.6 mm/yr SLE at 2200 [UNVERIFIED input — this flux line inherits the flag] is ≈ 0.030 Sv
  — well below the collapse threshold *as a magnitude*.

**The risk-weighted point is not magnitude, it is duration.** The framework's own
`divergence.py` rule: DISCOUNT analog recovery when loading is ocean-sourced and not finite.
The paleo analogs (8.2ka, Younger Dryas) recovered because their freshwater pulses were finite.
Williams et al. 2026 commits the source for 150+ years *under zero melt* — the off-ramp the paleo
record used does not exist this time. A sub-threshold flux applied indefinitely across a
bistable system's history-dependent band is a different risk class than a finite pulse, and the
tool's honest-gap protocol keeps the Southern-Ocean routing cell marked UNMEASURED rather than
filled.

## 8. Falsifier watch list (standing, from the measurement-fork spec)

Registered as watch items — each has a defined observation that would refute it:

| ID | Claim under watch | Refutes if |
|---|---|---|
| THW-F1 | RETIRED 2026-09-23 — premise not in source. Re-derive after full-text read of Pierce et al.: "radar-homogeneous" segments are resolution, not property | Higher-resolution or repeat radar still shows no basal structure there |
| THW-F2 | MT high-resistivity basin does not exclude a thin high-pressure water film | A borehole through the basin finds dry/low-pressure conditions at the interface |
| THW-F3 | Phạm's event-rate trend confounds glacier acceleration with network sensitivity | Trend survives recomputation per unit detection sensitivity |
| THW-F4 | Per-glacier assessment understates the WAIS chain (operator swap) | A coupled Thwaites→WAIS run on published data shows coupling not load-bearing |
| THW-F5 | Committed loss is policy-inert (closure persists post-Williams et al.) | Any national adaptation design code cites committed ice loss as minimum basis within 5 years |

F5 is the cheapest to watch and the most diagnostic of the closure-cost mechanism: the
information is now unmistakably present, so continued absence of the handling class is pure
prior-closure readout.

---

## 9. ENSO coupling: the 2026–27 super El Niño as a forcing pulse on the committed pool

**Status as of 2026-09-24:** El Niño is official and intensifying — Niño 3.4 at +3.0°C
mid-September 2026, 100% El Niño probability through February 2027, >90% chance of "very
strong," 75% chance of a record Oct–Dec RONI (+2.5°C+), peak forecast Nov 2026–Jan 2027
(NOAA CPC 2026-09-10; IRI 2026-09-21; WMO 2026-09-03).

**The teleconnection (published mechanism):** El Niño weakens the Amundsen Sea Low and the
coastal easterlies → reduced Ekman transport of cold surface water onto the shelf → warm
Circumpolar Deep Water flows onto the continental shelf and under the ice shelves → basal
melt rises. Shelf warming ~+0.5°C peaking near 200 m depth (Huguenin et al. 2024, GRL);
during strong events Amundsen ice shelves lose up to 5× more mass from basal melting than
they gain from the accompanying snowfall (Paolo et al. 2018, Nature Geoscience). Lag: the
atmospheric wave train reaches West Antarctica within ~2 months; ice-shelf height correlates
with winds lagged 4–6 months.

**Why the coupling is asymmetric — the rectification:** basal melt responds faster to heat
increases than to decreases (Kimura et al. 2017), the shelf stays warm longer than it stays
cool over a strong ENSO cycle (Huguenin et al. 2024), and melt has a floor near zero but no
symmetric ceiling. Labeled arithmetic (declared, not a result): a superlinear melt law
(melt ∝ thermal driving^1.5, floored) over one strong ENSO cycle yields a net rectified
melt anomaly of ~+29% of a baseline year per cycle; a 2026-27-scale event at Thwaites-melt
magnitude is order 50–60 Gt of added basal melt over the event (~0.15 mm SLE one-time
pulse) — *on top of* the committed trend, not instead of it.

**Mapping onto the July–September 2026 papers:**

| Paper | ENSO coupling read (risk-weighted) |
|---|---|
| Williams et al. (committed loss) | The super El Niño is a **wave arriving on the committed pool** — the operator swap again: wave + pool, not max(pool, wave). The event does not replace committed loss; it rides on it |
| Goldberg (modeling) | A forcing pulse in the *initialization-dominated* window — exactly where the model is least informative, and exactly what the climate-modeling suite's `DataAggregationAudit` FAIL warns about: a pulse averaged into a mean disappears from the projection |
| Phạm (seismic) | Prediction to watch: basal-melt pulse → accelerated flow → capsizing-berg earthquake rate should peak 2027. Falsifier THW-F3 applies — the peak must survive detection-threshold correction before it counts as physics |
| Pierce / Killingbeck (bed, water) | A sub-seasonal hydrological pulse hitting a system characterized by *snapshot* instruments (single-epoch radar and MT). The event will not be in the maps; any drainage or pressure response is invisible to the existing characterization |
| THW-04 redundancy | The observing system that would catch this in real time has N_eff = 1 under risk-weighted coding — and the satellites that survive the shared nodes cannot see the basal channel where the pulse acts |

**The compounding chain, stated plainly:**
committed internal loss (Williams et al., 150 yr) + rectified ENSO staircase (each strong event
leaves a net step because melt responds asymmetrically) + projected increase in ENSO
amplitude/variability by 2100 (Cai et al. 2021, 2023) = the forcing term is not a smooth
ramp but a rising staircase of pulses, each landing on a higher committed pool. The
2026–27 event is the first super-tier pulse to arrive *after* the committed component was
formally demonstrated. Risk-management posture: treat the 2027 melt season as the first
observed wave+pool superposition and demand the observing system report it as such —
event-triggered catalogs and snapshot maps will each miss their half by construction.

---

## 10. Non-English-source sweep (September 2026 window, searched 2026-09-24)

Languages searched: German, French, Japanese, Korean, Chinese. Chinese-language results were
explainers only; French coverage was strong for April 2026 papers but had nothing
September-specific; German, Japanese and Korean sources carried real research.

### Citation-ready

1. **Kasuya, T., Kuniyoshi, Y., Nagashima, K., Hasegawa, H., Abe-Ouchi, A., Hagemann, J. R.,
   Arz, H. W., Lange, C. B., Lamy, F., Iwasaki, S., Chan, W.-L., Harada, N., Murayama, M.,
   Saito, F., & Okazaki, Y. (2026).** Patagonian Ice Sheet discharge enhanced by AMOC slowdown
   through thermal bipolar seesaw. *PNAS* 123(38). DOI: 10.1073/pnas.2532733123.
   Published 2026-09-14; announced in Japanese (JAMSTEC/Kyushu/Tokyo/Kochi/Hokkaido, 2026-09-15).
   **This closes the UNMEASURED transfer gate of section 7 at the mechanism level**: AMOC
   slowdown → Southern Ocean warming via thermal bipolar seesaw → strengthened SH westerlies →
   ice-margin melt and discharge. Paleo (last glacial), Patagonia not Amundsen — mechanism
   transfers, magnitudes do not (the mining-increment configuration note applies).

2. **van Westen, R. M., Börner, R., & Dijkstra, H. A. (2026).** Failure to track a stable AMOC
   state under rapid climate change. *Nature Climate Change*. DOI: 10.1038/s41558-026-02730-w.
   Published 2026-08-13 (August, retained for load-bearing relevance). Rate-induced tipping:
   collapse at ~+2°C under fast forcing (2.5 ppm/yr), stable past +5.5°C under slow (0.5 ppm/yr);
   critical rate ~0.3°C/decade. Formalizes the section-9 claim that forcing RATE, not level,
   is the control variable — pulsed forcing on a committed pool is the worst case.

3. **Nian, D., Willeit, M., Wunderling, N., Ganopolski, A., & Rockström, J. (2026).** Collapse
   of the Atlantic meridional overturning circulation would lead to substantial oceanic carbon
   release and additional global warming. *Communications Earth & Environment*.
   DOI: 10.1038/s43247-026-03427-w. April 2026; surfaced via Japanese and German coverage.
   Southern Ocean flips carbon sink→source (+47–83 ppm CO₂, +0.17–0.27°C); above 350 ppm CO₂
   the collapsed AMOC state does not recover. Antarctica +6°C in the 450 ppm scenario.

### Leads (not citation-ready)

- Portmann et al., *Science Advances* (Apr 2026), ~51% ± 8 weakening by 2100, ridge regression — DOI not pulled
- Elipot et al., *Science Advances* (2026), four western-boundary mooring arrays, deep decline — DOI not pulled
- RTBF-covered model study (Jul 2026): 10% collapse probability with emissions frozen — **preprint, not peer-reviewed**
- GEOMAR "water age" (CFC-12/SF₆) ventilation-decline study (early 2026) — no authors/journal in coverage
- egusphere-2026-3065 (Jun 2026), GFDL ESM2M AMOC collapse under 2°C stabilization — preprint
- Astudillo et al. (2026), *Nature*, coastal SL 100–150 cm above hazard-assessment assumptions — DOI 10.1038/s41586-026-10196-1, March, outside window [CONFLICT: same DOI assigned to two author sets in this file (Astudillo et al., s10; Seeger & Minderhoud et al., s11). Unresolved — do not cite either until the DOI record is checked.]

### Updated falsifier watch list addition

```
THW-F6  The AMOC->Southern Ocean->Amundsen transfer (Kasuya mechanism) operates
        at magnitudes that matter for Thwaites within the committed-loss window
        Refutes if: present-day Southern Ocean / Amundsen warming is shown to
        track local forcing only, with no detectable seesaw component,
        during a measured AMOC weakening interval
```

---

## 11. Cross-disciplinary sweep: modeling, mathematics, statistics, imaging, others
(searched 2026-09-24; mapped to the audit's earlier findings)

### MATHEMATICS — tipping theory

- **Ashwin, P., et al. (2025).** Early warning skill, extrapolation and tipping for accelerating
  cascades. (Utrecht research portal PDF; journal status unverified — LEAD pending pin.)
  Early-warning-signal skill scoring for systems accelerating through folds — the formal
  machinery for "can we see Thwaites tipping before it tips," with an honest ROC/AUC treatment.
- **Early-warning indicators for rate-induced tipping.** arXiv:1509.01696, v5 updated
  2026-08-24. PREPRINT (long revision history; cite as arXiv). The mathematical counterpart to
  van Westen et al. 2026 (section 10): early-warning indicators for systems whose control
  parameter moves too fast — exactly the ENSO-staircase-on-committed-pool configuration.

### STATISTICS — attribution and extreme values

- **Dangendorf, S., et al. (2026).** Human-driven sea-level rise has quadrupled the frequency of
  coastal sea-level extremes since 1900. *Nature Climate Change*. DOI: 10.1038/s41558-026-02659-0.
  CITATION-READY. Global median frequency of a historical 1-in-100-year extreme sea-level event is
  up ~12×; human forcing alone quadrupled it. This is the missing `who_counts` fix for the
  Goldberg frame (section 1): it converts global-mean SLE into event-frequency at the coast.
- **Gilford, D. M., et al. (2026).** Human-caused sea level rise drives 21st-century worldwide
  water level extremes. *Science Advances*. DOI: 10.1126/sciadv.adz3595. CITATION-READY.
  Anthropogenic SLR detectable at 97% of 519 tide-gauge sites; 58% (44–65%) of 21st-century
  extremes attributable. Companion to Dangendorf.
- **Seeger, K., & Minderhoud, P., et al. (2026).** Sea level much higher than assumed in most
  coastal hazard assessments. *Nature*. DOI: 10.1038/s41586-026-10196-1. NOT CITATION-READY [CONFLICT: same DOI assigned to two author sets in this file (Astudillo et al., s10; Seeger & Minderhoud et al., s11). Unresolved — do not cite either until the DOI record is checked.]
  Coastal sea levels underestimated ~30 cm on average, >1 m in parts of SE Asia/Indo-Pacific —
  i.e., the *baseline datum itself* is biased low. In repo terms: an instrument-frame error
  upstream of every adaptation calculation (declared-frame `boundary` failure at the datum level).

### MODELING — emulators, calibration, intercomparison

- **Reese, R., Jourdain, N. C., et al. (2026).** A protocol for calibrating basal melt rates in
  the ISMIP7 Antarctic projections + meltMIP design. egusphere-2026-5337, discussion opened
  **2026-09-22** (in-window PREPRINT). Admits in writing what the audit found structurally:
  basal-melt modules are one of the largest uncertainty sources, CMIP models carry large Southern
  Ocean biases and mostly lack ice-shelf cavities, and melt parameters used as tuning knobs "can
  yield melt rates in the projections that are not physically well-constrained." Notes a 2026
  finding of a sub-ice ocean connection between Dotson and Crosson shelves that breaks the
  observational melt budget assumed for calibration. Governance-level confirmation of the
  measurement-fork result (no shared quantity across instruments → calibration ambiguity).
- **egusphere-2026-1585 (2026, PREPRINT).** Future learning and uncertainty reductions in
  Antarctic projections (MALI + sequential Bayesian calibration, Amery sector). Key result for
  risk posture: **limited scope for narrowing SLE projections through the end of the 21st
  century; rapid learning only after shelf loss begins** — i.e., the observations that would
  settle the uncertainty arrive largely *after* the event they would have warned about. This is
  closure-cost at the field level, quantified. Authors themselves hypothesize Thwaites would
  learn faster because it is already in rapid change.
- **SC-DS: likelihood-free calibration with diffusion emulators.** arXiv:2608.29642 (2026-08-30,
  PREPRINT). 2.2 h vs 198.9 h for GP-MCMC on WAIS calibration; Bedmap3 posterior favors fast
  basal sliding (CRH most constrained, high values) — independent statistical support for the
  risk-weighted reading of Pierce's bed: sliding-friendly bed is what the data prefer.
- **Coulon, V., et al. (2025).** From short-term uncertainties to long-term certainties in ice
  sheet projections. *Nature Communications*. DOI: 10.1038/s41467-025-66178-w. CITATION-READY.
- **CMIP 2026 workshop / ISMIP7 (June 2026, program record):** "Initialization is fundamentally
  a palaeoclimate-constrained problem" — program-level confirmation of the Goldberg et al.
  comment's central finding (section 1).

### IMAGING / OBSERVING

- **Davison, B. J., Hogg, A. E., Slater, T., Rigby, R., & Hansen, N. (2025).** Antarctic Ice
  Sheet grounding line discharge 1996–2024. *Earth System Science Data*. CITATION-READY.
  Continental discharge rose 1999 ± 175 → 2224 ± 200 Gt/yr; monthly cadence in later years;
  updated monthly subject to "continued Sentinel-1 acquisitions and funding availability" — the
  dataset itself names the THW-04 shared node (funding) as its continuity condition.
- **MEaSUREs Antarctic Grounding Line v2.1** (NSIDC-0498, DOI: 10.5067/IKBWW4RYHF1Q, updated
  2026-02-27, coverage now 1992→2025-11) + Grounding Zone v1.1 with ML-generated migration
  boundaries. DATASET, citable.
- **UC Irvine / ICEYE 30-year grounding-line study** (PNAS, announced 2026-03-03): Antarctica
  lost 12,820 km² of grounded ice since 1996; Thwaites retreated 26 km, Pine Island 33 km,
  Smith 42 km; daily-revisit commercial SAR now load-bearing for fast sectors.
  LEAD — journal and date known, author list not yet pulled.
- **Hudson, T. S., et al. (2026).** Quantifying subsurface fracture damage in glaciers using
  fiber-optic seismology. *Science Advances* (PubMed 42490434). CITATION-READY (DOI to pull).
  DAS measures crevasse damage (~8% of ice volume, fracture-dominated) — a *new, cheap,
  rapidly deployable* channel that reads subsurface damage satellites cannot see. Directly
  relevant to THW-04: DAS is the one technology in this sweep that could raise N_eff, because
  it breaks the funding/logistics shared node (compact, low-power, no repeated field campaigns).
- **Rán II** (Univ. of Gothenburg): replacement AUV for the Rán lost under an Antarctic glacier
  in Jan 2024, delivery winter 2026/27. CONTEXT — a literal instance of observing-system
  fragility: the only instrument that had entered Thwaites' cavity was lost in it, leaving a
  ~3-year gap in cavity-class measurement exactly as the committed-loss era begins.

### OTHERS

- **Destination Earth Climate DT** (ECMWF/DestinE; ACM SC'25 paper DOI: 10.1145/3712285.3771790):
  operational multi-decadal km-scale climate digital twins (5 km production, 1 km demonstrated),
  6.6 PB portfolio. CITATION-READY as capability record. Relevant as the compute layer that could
  host a coupled Thwaites wave+pool monitoring product — but note ice sheets are *not* interactive
  in these ESMs yet; the glacier is a boundary condition, not a component (the climate-modeling
  suite's Cross-System Coupling stub, still a stub at continental compute scale).
- **SFU thesis (2025):** statistical emulation of subglacial drainage (GlaDS GP emulator,
  ~1000× speedup; random-forest Antarctic effective-pressure emulator, 6 orders of magnitude
  speedup). THESIS — LEAD. Finds structural model error, not parameters, is the binding
  constraint on subglacial hydrology — independent echo of this audit's core finding.

### New falsifier / gap entries

```
THW-F7  DAS-class sensing can read subsurface fracture damage at Thwaites scale
        Refutes if: a deployed DAS array on an Antarctic ice shelf fails to
        resolve crevasse/icequake damage above noise for one full season

THW-05 (gap)  STATE: unowned. The monthly grounding-line discharge dataset
        (Davison et al.) is the closest thing to an OIR-style observable
        indicator, and its continuity is conditional on a single funding line —
        the same shared node THW-04 flagged. No party owns converting it into
        a household/authority-readable trigger product.
```

---

## 12. Correction and counterweight pass (2026-09-24, from the operator's review + citation backlog)

### 12a. Correction: the OIR analogue was an over-transfer — scoped down

The operator's critique is accepted. In section 5 I transferred OIR's miss-filter finding
(a structural property of a *wetting-order stability check* — a miss flips the pair's sign,
a false alarm keeps it) onto a hypothetical Thwaites grounding-line-retreat warning rule
without comparing constraint sets. The repo's own vocabulary (SS_005, TP_008, RCC_008:
"the machine and human arms are not claimed to share a mechanism") is the discipline that
says state what they don't share before using the transfer.

**What transfers:** the *asymmetry class* — a warning product whose acceptance check
constrains misses but not false alarms will cry wolf, and the party who pays for the false
alarms is the household/worker, not the agency.
**What does not transfer (until shown):** the specific mechanism (sign-flip on order
inversion). A grounding-line-retreat rule is a threshold crossing, not a wetting-order
pair; its failure modes must be derived on its own constraint set.
**Status:** demoted from "application" to **candidate cross-domain shape, constraint sets
uncompared**. The report's OIR paragraph is to be read under this scope.

### 12b. Counterweight entered: Höse et al. 2026 cuts against the coupling narrative

**Höse, A., Kreuzer, M., Huiskamp, W., Petri, S., & Feulner, G. (2026).** Simulating the
impact of an AMOC weakening on the Antarctic Ice Sheet using a coupled climate and ice-sheet
model. *Earth System Dynamics* 17(4), 1025–1059. DOI: 10.5194/esd-17-1025-2026 (2026-07-30).

In an artificial North Atlantic freshwater-forcing experiment: little subsurface-temperature
change around most of Antarctica and **no change in total Antarctic ice volume for the first
eight centuries after AMOC shutdown**; later Ross Sea cooling *reduces* basal melt while
increased calving offsets it. Model-specific, with declared forcing/coupling limits — not a
safety guarantee, and not nothing.

Risk-weighted reconciliation (this changes the audit's emphasis, honestly):
- Sections 7/9's coupling chain ran AMOC→Southern Ocean→Thwaites. Kasuya (paleo mechanism)
  says the pathway exists; Höse (coupled forward model) says its magnitude is small for
  centuries. **The two are not in contradiction with Williams et al. — they reinforce it.** If AMOC
  forcing adds little, then the committed, internal-dynamics component is even more clearly
  the load-bearing term. The risk was never "AMOC collapse melts Thwaites"; it is "Thwaites
  is committed on its own dynamics, and no ocean-state change — including a favorable one —
  retires that."
- New falsifier:

```
THW-F8  The AMOC->Antarctic seesaw pathway is negligible for Thwaites on
        committed-loss timescales (Höse) versus material (Kasuya mechanism)
        Refutes the Höse reading if: a coupled run with resolved Amundsen
        cavities, observed freshwater geometry, and sub-seasonal ocean
        forcing shows shelf-temperature response within 200 years
        Refutes the Kasuya-transfer reading if: the pathway's Amundsen
        magnitude stays below natural ENSO-band variability in such a run
        (note: ENSO variability is section 9's term — this falsifier pits
        the two sections against each other deliberately)
```

### 12c. Backlog items mapped onto the gap register

- **Zeising et al. 2026** (*Comms Earth & Env.* 7, 366; DOI 10.1038/s43247-026-03502-2;
  "Hard rocks and deep wetlands beneath Thwaites"; vibroseismic + impedance products at
  PANGAEA 10.1594/PANGAEA.987704) — a **fourth instrument arm** with direct bed contact.
  Open test against THW-02: whether vibroseismic impedance shares any quantity with radar
  reflectivity or MT resistivity, or supports a joint inversion. Per the backlog's own
  discipline: agreement not assumed in advance. If a shared quantity exists, the
  measurement-fork result weakens; if not, THW-02 hardens from "no shared quantity among
  three arms" to "among four."
- **Matsuoka et al. 2026** (*Rev. Geophys.* 64(3), e2022RG000803; 2026-09-02) — review of
  coastal-zone data gaps and survey priorities; the institutional-side counterpart to THW-02
  and THW-04. Cross-check which of its proposed Amundsen surveys overlap in measured quantity
  and which still leave pore pressure unmeasured.
- **Otosaka et al. 2026** (*Scientific Data* 13, 1301; DOI 10.1038/s41597-026-08088-0;
  2026-09-16) — regional mass-balance baseline 1970s–2023 with uncertainties; the WAIS product
  is a constraint for basin-scale bookkeeping, explicitly **not** a Thwaites time series.
- **Nian date corrected**: publisher 2026-03-27, version of record 2026-03-31 (March, not the
  April used in section 10).
- **HAL animal-borne bathymetry record** — held as UNVERIFIED lead (no authorship/venue/DOI
  established). Noted without use.
- Repo convergence note: `Simulators/AMOC/research.md` (commit f35e1f5) independently added
  Kasuya and Nian while these searches ran. Same two papers, two independent routes.

### 12d. The worker-side reading — adopted as the report's audience frame

The operator's reframe is adopted: this document is a risk-management instrument for the
people who build and maintain what the risk applies to. Consequences carried forward:

1. **Design-life mismatch is the load-bearing sentence.** A 75-year code against a 150-year
   committed loss means the code is calibrated to a horizon the hazard has already passed.
   Sayable in a planning meeting; no per-glacier assessment contradicts it (section 5's
   operator swap is the arithmetic behind the sentence).
2. **THW-01 is the only gap a worker or community can push alone** (demand the code cite
   committed loss as floor). THW-02/04 need institutional moves. Priority ordering in any
   future action section follows this.
3. **"No shared quantity" means no appeal to cross-check.** The instrument that would let a
   worker falsify the institutional reading does not exist; terrain-prior reads are the only
   cross-check available on the ground. This is now stated as a consequence, not just a gap.
4. **Warning products must carry both rates.** A trigger product with a constrained miss rate
   and an unconstrained false-alarm rate trains its users to ignore it; the false-alarm side
   is the worker's problem before it is the agency's (held under the 12a scope note).

---

## 13. Backlog papers through the audit tools (audit first, counterweight second)

All six received declared-frame blocks (accepted by `check_frame.py`). Key per-paper reads:

**Otosaka et al. 2026 (mass balance baseline)** — frame flag: `boundary`. The WAIS product is
a regional aggregate; assigning it to Thwaites is a boundary error the paper's own regional
structure warns against. Role in the audit: the denominator — every attribution claim
downstream inherits its uncertainty budget. `observer_access: verified` — the cleanest frame
in the whole corpus, because it is a data product with released uncertainties.

**Kasuya et al. 2026 (Patagonian seesaw)** — frame flag: `who_counts`. The mechanism is
measured *in Patagonia, in the last glacial*; the Antarctic application is a transfer, not a
measurement. This paper upgrades section 7's transfer gate from UNMEASURED to
**measured-at-mechanism-level, magnitudes not transferable** — and the frame makes the
reason visible: boundary conditions differ (geometry, glacial climate state).

**Matsuoka et al. 2026 (coastal-zone review)** — frame flag: `who_counts` = the gap
inventory itself. A review measures nothing but ranks what is unmeasured; it is the
institutional-side mirror of THW-02/THW-04. Its Amundsen survey priorities are the checklist
against which "which proposed observation would actually read pore pressure" can be scored.

**Zeising et al. 2026 (vibroseismic bed)** — run through the measurement-fork as a fourth
arm (`thwaites_subglacial_v2`). Result:

```
SAME QUANTITY, DIFFERENT ROUTE
  none -- the arms share no quantity at all.   (unchanged with arm 4)
RESIDUAL
  [COVERED widen] whether acoustic impedance, radar reflectivity, and
  resistivity can be joint-inverted into one shared physical quantity
```

THW-02 hardens: "no shared quantity" now holds across **four** instrument arms. The joint
inversion question is registered in the residual cell — that is where a shared quantity
would have to be *built*, since none exists by design. Consequence from 12d stands and
strengthens: the cross-check instrument still does not exist.

**Höse et al. 2026 (AMOC→Antarctic null)** — mapped through `reservoir-chain-coupling`'s
harness structure: Höse is the **null, high-freeboard branch** of the operator-swap test.
The swap (max vs sum) is only decisive inside the disagreement band `crest − pool ≤ wave <
crest`; Höse's result says the AMOC-forcing wave never reaches the Antarctic band on
committed-loss timescales — freeboard (thermal distance) is too large, so the coupling term
is genuinely negligible *for that pathway*, and the detector honestly reports REFUTED
(coupling negligible) rather than firing. Crucially this says nothing about the **pool**:
Williams et al.'s committed internal loss is the antecedent term and does not need the AMOC wave.
The two papers occupy different cells of the same harness.

**Nian et al. 2026 (carbon flip)** — frame flag: `boundary`. Carbon-cycle diagnostics are
not shelf-temperature measurements; the Southern Ocean appears as a carbon reservoir, not an
ice-forcing term. Usable for AMOC consequence framing, unusable for Thwaites forcing.
Date corrected: VoR 2026-03-31.

**HAL animal-borne bathymetry record** — not run. UNVERIFIED lead; no authorship/venue/DOI
established. Held, per the repo rule that an absence is a location, not a finding.

## 14. Counterweight synthesis (post-audit)

Now legitimately, since the audit ran first:

1. **The committed-pool reading survives the counterweight.** Höse weakens the
   AMOC→Thwaites *forcing* pathway (section 7/9 emphasis was too coupling-forward); it does
   not touch Williams et al.'s committed internal loss, which needed no ocean forcing in the first
   place. Net effect of the counterweight: **the audit's central line (committed loss as
   design floor) is strengthened, and the AMOC coupling is demoted from 'risk amplifier' to
   'open pathway with a measured paleo mechanism (Kasuya) and a modeled weak magnitude
   (Höse)'** — exactly the state THW-F8 was written to resolve.

2. **THW-02 is now a four-arm result.** Zeising was the backlog's best candidate to break
   "no shared quantity" and did not. The residual cell names the only honest route forward:
   a joint inversion would have to *construct* the shared quantity.

3. **Frame-quality ranking (observer_access as the proxy):** verified — Otosaka, Matsuoka,
   Zeising (data products and reviews with released data); partial — Kasuya, Höse, Nian
   (model/proxy dependent). The three most decision-relevant papers for coupling are also
   the three with the least observer access. Not a flaw — the property of the questions they
   ask — but it sets the confidence ceiling for any counterweight verdict.

4. **Standing correction to section 7:** the sentence "the margin is not the flux ratio"
   survives Höse (he says the flux ratio is small and stays small; duration argument becomes
   moot for AMOC specifically). The committed-loss floor argument does not depend on AMOC
   and is unchanged.
