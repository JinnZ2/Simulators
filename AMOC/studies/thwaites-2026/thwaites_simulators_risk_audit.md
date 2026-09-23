# Thwaites Glacier September-2026 Papers × JinnZ2/Simulators
## Risk-management-weighted audit (worst-case planning, not conservative averaging)

All tools below were **actually cloned and run** from `github.com/JinnZ2/Simulators` (2026-09-23).
Where a tool takes structured inputs, each paper was encoded as an input file and executed.
"Risk-weighted" here follows the repo's own rule: report the band, plan against the short end;
treat committed loss as the floor, not the scenario.

---

## Results map

| Paper | Tools run | Headline output |
|---|---|---|
| Goldberg et al. (ice-sheet modeling) | `climate-modeling` audit suite; `declared-frame` | **7/7 built audits FAIL**: smooth models are blind to threshold+memory cascades |
| Killingbeck et al. (MT groundwater) | `closure-cost` (instrument branch); `declared-frame`; `measurement-fork` | Intermediary (resistivity) is the reading; pore pressure never sampled |
| Phạm (glacial earthquakes) | `instrument-bias-sims` S1; `declared-frame` | Event-sampled catalog has **null share 0.0000** — baseline reconstructed from events alone |
| Pierce et al. (radar bed) | `measurement-fork`; `declared-frame` | Radar/MT/seismic arms **share no quantity at all** — no cross-validation exists |
| Bradley et al. (committed loss) | `closure-cost` (event branch); `reservoir-chain-coupling`; `declared-frame` | "No melt → no loss" was a **closed variable**; coupled chain breaches **4/4 nodes** the per-node view clears |

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

Every failure mode the suite flags has a direct analogue in the Goldberg paper's own finding:
**initialization dominates the 21st century** = the model's near-term answer is set by an
inherited state, not by measured physics (the suite's Stationarity/Omitted-Variable failures);
**forcing dominates later** = the regime where the model is best validated is the regime that
matters least for people alive now.

The declared-frame check pins the framing:
- **horizon**: the headline "2.6 mm/yr by 2200" is scored 175 years out; the 2026–2100 window — the planning horizon of every living structure — is the initialization-dominated window the model is *least* informative in.
- **boundary**: modeled ice volume only; MICI-style cliff physics, subglacial hydrology feedbacks (the Killingbeck/Pierce territory), and the downstream WAIS buttressing chain are outside the accounting.
- **who_counts**: global mean SLE. No coastline, no time-of-arrival distribution; the aggregate absorbs the variance that risk management lives on.

**Risk read:** treat 2.6 mm/yr by 2200 as a *floor with a smooth-model bias*, not a ceiling.
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

On the paper itself, the declared-frame check flags the load-bearing sentence: "homogeneous
substrate under fast-moving western regions" is an **instrument-resolution statement that reads as
a property statement**. Smooth to radar at survey-line spacing ≠ smooth at the scale of basal
hydrology. The risk-relevant cell — the fast-moving region — is precisely the one with the least
resolved bed.

**Risk read:** the bed beneath the fastest ice is the least characterized; heterogeneity is the
finding where the ice is slow, homogeneity (read: resolution floor) where it is fast. Plan as if
the western region's basal conditions are *unknown*, not *favorable*.

---

## 5. Bradley et al. — mass loss continues without ocean melting

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

Then the chain. Bradley's 150-year committed loss *is* the antecedent pool in
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

1. **The committed pool is the load-bearing input.** Bradley supplies the antecedent state;
   Goldberg supplies the arriving wave; the operator swap says combining them by `max` instead of
   `sum` is the standard assessment error, and it never overstates.
2. **No instrument reads the controlling variable.** Radar (Pierce), MT (Killingbeck), seismic
   (Phạm) share no quantity (measurement-fork, run result) and none reads pore pressure. The
   fastest-flowing region has the least-resolved bed.
3. **The event record has no baseline.** Phạm's catalog is event-triggered (S1: null share 0.0000);
   calm in the record is not calm in the glacier.
4. **The smooth-model bias is measured, not conjectured.** 7/7 climate-modeling audits FAIL in the
   direction of understated cascade speed — plan on the short end of every band.
5. **The failure was closure, not information.** Closure-cost: availability ruled out the
   procedure-gap rival. The handling class for committed loss does not exist because the premise
   was closed, and it must now be built under time pressure.

## Drafted gap-markers entries (schema-conformant)

```
GAP_ID   THW-01
DOMAIN   glaciology / coastal adaptation
STATE    unowned
WHAT_EXISTS  committed-loss magnitude (Bradley 2026); SLR ensembles (Goldberg 2026)
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
inter-coder Cohen's kappa: 0.000
```

Run notes:
- This also closes a gap the repo's own audit found: the delivered `report()` never calls its
  own `cohen_kappa`, so the two-coder blind protocol had no representation. Here it was called.
- **κ = 0.000 is the finding, not a defect**: whether the monitoring system has any redundancy
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
- Flux arithmetic from the September papers: even Goldberg's 2.6 mm/yr SLE at 2200 is ≈ 0.030 Sv
  — well below the collapse threshold *as a magnitude*.

**The risk-weighted point is not magnitude, it is duration.** The framework's own
`divergence.py` rule: DISCOUNT analog recovery when loading is ocean-sourced and not finite.
The paleo analogs (8.2ka, Younger Dryas) recovered because their freshwater pulses were finite.
Bradley 2026 commits the source for 150+ years *under zero melt* — the off-ramp the paleo
record used does not exist this time. A sub-threshold flux applied indefinitely across a
bistable system's history-dependent band is a different risk class than a finite pulse, and the
tool's honest-gap protocol keeps the Southern-Ocean routing cell marked UNMEASURED rather than
filled.

## 8. Falsifier watch list (standing, from the measurement-fork spec)

Registered as watch items — each has a defined observation that would refute it:

| ID | Claim under watch | Refutes if |
|---|---|---|
| THW-F1 | Radar "homogeneous substrate" under the fast western region is resolution, not property | Higher-resolution or repeat radar still shows no basal structure there |
| THW-F2 | MT high-resistivity basin does not exclude a thin high-pressure water film | A borehole through the basin finds dry/low-pressure conditions at the interface |
| THW-F3 | Phạm's event-rate trend confounds glacier acceleration with network sensitivity | Trend survives recomputation per unit detection sensitivity |
| THW-F4 | Per-glacier assessment understates the WAIS chain (operator swap) | A coupled Thwaites→WAIS run on published data shows coupling not load-bearing |
| THW-F5 | Committed loss is policy-inert (closure persists post-Bradley) | Any national adaptation design code cites committed ice loss as minimum basis within 5 years |

F5 is the cheapest to watch and the most diagnostic of the closure-cost mechanism: the
information is now unmistakably present, so continued absence of the handling class is pure
prior-closure readout.
