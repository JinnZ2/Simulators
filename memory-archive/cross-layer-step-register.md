---
name: cross-layer-step-register
description: Register opened 2026-09-30 — joins small changes landing on different layers (statute, regulation, enforcement, staffing, funding) so a cumulative shift is visible. Two domains: disability/special-ed (Texas v. Kennedy seed); biodiesel blend seam vs hauling fleet + road infrastructure.
sources: [chat]
aliases: [step register, incrementalism register, layer register, cross-layer changes, quiet incremental change, statute intact capability gone, biodiesel blend seam, RFS blend cap, fuel tax bridge funding]
---

> FRAME FOR A COLD READER: a measurement register, direction-neutral.
> It records changes in ANY direction (removal or expansion) on any
> domain. Intent is not recorded — it is unmeasurable. The reading is
> the cumulative join, which no single report carries.

## ORIGIN (2026-09-30)

- [WITHHELD — memory only, per the originator's choice: two lines of her read on motive/pattern-of-power.]
- DERIVED (Claude): the shape is F2 in [[held-indicator-five-field-instrument]] — the reading holds (statute text, precedent formally intact) while the generator underneath (interpretation, regulation, enforcement, staffing, funding) changes. Each step lands on a different layer and is reported as a separate story; no report carries the sequence. Same structure as [[quiet-failure-as-missing-aggregation-function]]: signals reported, never joined.

## ROW SCHEMA

```
date | domain | layer | step | source | formally intact | capability still operating | status
layer ∈ statute, precedent, interpretation, regulation,
        oversight, enforcement, staffing, funding, data
status ∈ IN_EFFECT, BLOCKED, PROPOSED, REVERSED
direction recorded per row: CONTRACTS / EXPANDS capability
```

## SEED ROWS — domain: disability integration and special education (US)

```
2025-10   staffing     OSEP layoffs attempted; court blocked
                       (Disability Scoop, 2025-10-16)        BLOCKED
2025-01→  staffing     IES 187 -> 30 staff; NCES ~100 -> 11
 2026-02               (97-org letter, May 2026)             IN_EFFECT
2026-06-16 oversight   4 interagency agreements: OSERS/IDEA
                       admin, enforcement, monitoring -> HHS
                       (Administration on Disabilities); OCR
                       -> DOJ. ED keeps STATUTORY duty.
                       Govt: "students will not lose any
                       rights"; better alignment.            IN_EFFECT
2026-06-18 interpretation OLC memo (39 pp, Pettit): no statutory
                       integration mandate in 504/Title II;
                       Olmstead narrow; mandate would raise
                       constitutional concerns; HHS/DOJ regs
                       exceed authority, should be rescinded;
                       memo itself says its view is "out of
                       step" with federal courts. OLC memos
                       lack force of law (Bagenstos).        IN_EFFECT
2026-06-23 statute     Latonya Reeves Freedom Act introduced
                       (affirmative statutory integration
                       right) — EXPANDS, proposed            PROPOSED
2026-08-31 regulation  DOJ/HHS + TX, FL, AK propose vacating
                       integration provisions, HHS 504 rule  -> order
2026-09-23 regulation  N.D. Tex. (Lubbock) order implements
                       settlement; integration provisions
                       vacated (ACLU, 2026-09-24)            IN_EFFECT
2026-09-30 funding     IES FY25 funds lapse deadline (~180M
                       of ~289M unobligated as of Sep); some
                       reprogrammed (+28M special-ed research
                       grants); lawsuit filed Jun 30; govt
                       argues moot (OMB released most).
                       Outcome after deadline NOT FOUND
                       (searched 2026-10-01)                 CHECK
formally intact: Section 504 statute, ADA, Olmstead precedent,
  private Olmstead suits still available
EXPANDS rows, same domain: A.J.T. v. Osseo (2025-06, 9-0, lower bar
  for student discrimination claims); Perez (2023); LRFA (proposed)
NOTE: VOR (family org historically supporting facility options)
  also criticized the memo as weakening the legal floor — not a
  two-sided split along the usual line.
```

- SCOPE: rows sourced from reporting, advocacy statements and government statements as reported; OLC memo described via secondary sources (summaries consistent across ACB, ABA, STAT, VOR); full text at justice.gov/olc not read.

## SECOND DOMAIN — biodiesel blend seam vs the hauling fleet + road infrastructure (opened 2026-10-03)

> Same schema, different domain. Each layer is locally correct; the cracks live in the SEAMS between boxes, where no party holds the coupling. The originator's frame: "none of this was looked at under engineering specs for the engine and updated to current standards" — so bad numbers stack on already-out-of-date infrastructure = a compounding system with cracks in its foundation.

### The pressure build (both levers moved the SAME direction at once)
- [OBSERVED, web 2026-10-03] RFS "Set 2" final rule (EPA, Mar 27 2026): record-high mandate, ~60% increase in biodiesel + renewable diesel production/use vs 2025; highest volumes in program's 20-yr history; ~+1B RINs more once reallocated small-refinery exemptions fold in. (Trinity, Holland & Knight, Taxpayers for Common Sense, Crux.)
- [OBSERVED, web] Summertime E15 limit waived; dyed-diesel RFS exemption proposed by refiners as price relief (Bloomberg/AgBull). So: mandate forced UP while exempt outlets (dyed/off-road) pulled OUT from under it. Volume rising, sinks shrinking — relief valve being welded shut while pressure rises.

### The mechanism (how displaced volume lands on the seam)
- RFS obligation sits on the obligated party's TOTAL POOL as a percentage (RVO), met by blending OR buying RINs — NOT per physical gallon. So exempting dyed/off-road gallons shrinks the obligated pool while required RIN volume holds → the % per remaining gallon RISES → biodiesel concentrates HARDER into the on-road pool. Volume doesn't leave the system; it relocates to where the obligation still bites = the hauling fleet.
- [stated, originator] The biodiesel "has to go somewhere," and it goes into the vehicles that actually transport goods on the road — degrading the transportation layer, because the blend % exceeds what the installed engine was specced to hold ("out of bounds").

### WHERE the volume can go — four sinks, ranked by actual flow (DERIVED, for the instrument)
```
1. on-road #2 diesel blend %        ← primary sink = THE SEAM (seal/injector-relevant)
2. renewable diesel (drop-in HVO, not FAME) ← chemically different, no elastomer issue
3. export                           ← but RINs generate only on domestic use → weak sink
4. storage / RIN banking            ← defers, doesn't absorb
```
- Seal-relevant number: B20 (20% FAME) = long-standing fleet/OEM comfort ceiling for older material specs; above ~B20 is where elastomer swell, injector deposits, cold-gel risk climb for equipment specced to lower blends. Regulatory tell that >B20 behaves differently: the T90 distillation spec already grants B6–B20 a 5°C higher allowance (Energy & Fuels 4c00912).

### Rows
```
date     | layer        | step                                              | direction | status
2026-03-27 regulation   RFS Set 2: record-high mandate, +~60% BBD vs 2025   EXPANDS(volume) IN_EFFECT
2026       regulation   summertime E15 (ethanol/GASOLINE) limit waived      EXPANDS         IN_EFFECT
2025-01    exec action  EO 14156 "National Energy Emergency" §2(b): yr-round EXPANDS         IN_EFFECT
                        E15 provision (ethanol/gasoline side)
2026-05-13 statute      House passed permanent yr-round E15; Senate in Ag   EXPANDS         PROPOSED
                        Act 2026 §12501
2026       regulation   dyed-diesel RFS exemption proposed (price relief)   CONTRACTS(sink) PROPOSED
formally intact: engine OEM blend specs, B20 material limits, highway trust fund,
  E15-side seasonal RVP limit (now waived)
capability shifting: on diesel, actual on-road blend % pressured up by volume math
```

### CORRECTION (search 2026-10-03) — which cap was actually lifted, and on which fuel
- [OBSERVED, web] The confirmed cap removal is on the ETHANOL/GASOLINE side: EO 14156 (National Energy Emergency, Jan 2025) §2(b) year-round E15 provision + EPA 2026 summertime E15 waiver (lifts the seasonal RVP/volatility limit) + House-passed permanent year-round E15 (May 13 2026) / Senate Ag Act §12501. This IS the executive order the originator remembered and it DOES lift a cap — but the cap is E15 (ethanol in gasoline), the gasoline side.
- [OBSERVED, web] On the DIESEL/biodiesel side: searched, found NO EO or EPA waiver allowing on-road diesel above B20. What's real on diesel is the Set 2 VOLUME mandate (+60%), a volume push, not a per-gallon blend-cap removal.
- CONSEQUENCE for the two branches (keep separate — her rule): ETHANOL seam fails by RULE (seasonal cap struck). DIESEL seam fails by PRESSURE (B20 engineering limit still formally stands; volume mandate + shrinking exempt sinks concentrate biodiesel onto on-road via RIN math, pushing toward the limit without removing it). Different mechanisms, different next steps — do not merge.
- [OBSERVED, web] EPA's Set 2 "set authority" (CAA) REQUIRES EPA to consider "the impact of renewable fuels on the infrastructure of the United States, including deliverability of materials, goods, and products." So the infrastructure coupling the originator says nobody held is STATUTORILY supposed to be considered. Open question = whether it was actually run against current engine specs. (Her point restated in the statute's own language.)

### The compounding (the originator's foundation point — why this is worse than a fuel problem)
- [stated, originator] None of it was re-run against CURRENT engineering specs for the engine and updated to current standards. So you get a big mass of misinformation, gaps, judgment calls, and out-of-date infrastructure ADDED TO already-out-of-date infrastructure. Compounding system, cracks in the foundation.
- [stated, originator] "None of those taxes are going to go in toward actually building the bridges anymore" — the fuel-tax base that funds roads/bridges is eroding at the same time.
- DERIVED (the two converging erosions, for the instrument): (1) the trucks degrade from the fuel [blend % > spec]; (2) the roads/bridges degrade from defunding [fuel-tax base pulled out: exempt gallons, EVs, dyed exemption]. BOTH failures land on FREIGHT — the carrier layer everything else rides on. A cost taken to hold farmland/crop-demand asset value is paid by the distribution network that farmland itself depends on to reach a buyer. The instrument eats its own delivery system.
- DERIVED (why nobody caught it): each layer optimizes its own box with the couplings declared "none" — RFS office sizes a volume, farmland investor sizes an asset, refiner solves a RIN %, fleet buyer specs to LAST year's blend, nobody holds the seam where "volume must go somewhere" meets "somewhere is a seal rated for less." Every box locally correct; the system incoherent because the inter-box couplings were never anyone's job. Same object as the dyed-fuel automation stack ([[dyed-fuel-sensor-drift-differential]]) and the consciousness-paper misnames ([[no-anchor-information-mismanagement]]): a real coupling declared absent, cost comes due on whoever stands at the seam. Here the seam is the on-road truck; the person on it is the driver.

### THE DRIVER AS MISLABELED SEAM — commute leg counted as "consumer demand" (stated 2026-10-03)
- [stated, originator] A truck driver who drives a personal vehicle to the yard to pick up their truck is NOT technically a "consumer" of that commute fuel — without the personal vehicle they can't reach the truck, so the commute is a REQUIRED input to doing the work, not discretionary end-use.
- DERIVED (the category error): "consumer" assumes discretionary end-use (you could choose not to burn it; the demand is yours). The commute leg is non-discretionary INPUT to freight — no commute fuel → no freight. It's a cost of PRODUCTION of transportation, mislabeled as personal consumption only because it rides in a personal vehicle. The accounting sees the vehicle (whose car), not the function (enabling freight) — same box-edge error as the tree/oxygen case ([[corpus-as-sample-not-reality]]): measured by what's easy to see, not by what it's doing.
- [stated, originator] The ONLY drivers who can park the truck+trailer at/near home are those with land and permission to park it there — and that is very few rural truckers, who are FARMERS. Everyone else (city/suburb) MUST commute to a yard. So the commute-fuel cost is forced on the majority, and specifically on the NON-farmers.
- DERIVED (the sorting): the one group that does NOT pay the commute-fuel cost = farmers = the exact group the mandate is built to subsidize. The policy sorts the burden AWAY from the beneficiary and ONTO the carrier. Drivers eat it twice: E15 in the personal commute car (gasoline side, fails by rule) AND the higher biodiesel blend in the truck (diesel side, fails by pressure). Same human is the seam for BOTH levers.

### THE QUESTION TO RUN (the originator's framing — an empirical fork that decides severity)
- [stated, originator] HOW DOES THIS IMPACT THE INDUSTRY? It turns on one measurable split:
  * IF the majority of truck drivers DO have land/parking access (no personal vehicle needed to reach the truck) → one thing, limited impact.
  * IF the majority DON'T (must use a personal vehicle) → then degradation to their PERSONAL vehicle (from the E15 they're now forced to burn) removes their way of getting to work. 
- [stated, originator] CONSEQUENCE if the second branch holds: you have closed the door on an entire system that is structurally dependent for resource management, resource access, and transportation — without ever understanding that that is what happened. The fuel policy degrades the personal vehicle → driver can't reach the truck → freight access severed at the human-access layer, a layer the accounting never knew was load-bearing because it filed the driver under "consumer."
- DATA NEEDED to resolve the fork: share of US truck drivers who park at/near home (land+permission) vs must commute to a yard; rural vs urban/suburban split; what fraction of commute vehicles burn E15-range gasoline. This is the measurement that turns the instrument from argument into finding.

### FINDING (search 2026-10-03) — the LEGAL STRUCTURE confirms the second branch; headcount still unrun
- [OBSERVED, web] Residential semi-truck parking is PROHIBITED in most US cities/counties by local ordinance. "The most restrictive rules come from city and county ordinances"; residential zones prohibit tractor-trailers, allowed only in commercial/industrial/transportation zones; "spending a night is impossible" in residential; CA + most states make parking a semi on a residential street illegal. (TheTruckersReport, TruxParking, Truck Parking Club, RecNation.)
- DERIVED: park-at-home is legally possible ONLY where rural + land + loose/absent zoning enforcement — i.e. exactly the farmer-with-land case, and essentially nowhere else. So ZONING LAW does the sorting: everyone in a city/suburb is legally FORCED to use a yard → legally forced into the commute leg → forced to burn personal-vehicle fuel to reach work. Not a preference or convenience — a legal structure. And it ties the park-at-home exemption to exactly the subsidized group (landholders/farmers). The originator's second branch is the structurally-confirmed one.
- STILL UNRUN (the one remaining number): the HEADCOUNT — % of US drivers who commute to a yard vs park at home. FMCSA's "Quantifying the Benefits of Creating New Truck Parking Spaces" survey (Docket FMCSA-2025-0787, ~1,000 responses) is only PLANNED, not yet run — so the clean national split doesn't exist yet. NOTE: all existing national parking data measures MID-HAUL stops ("shortage of spaces along routes"), not the HOME-END question (where the driver starts / whether they commute to the rig). The question is unanswered because it was never framed as a thing to count — box-edge pattern again.
- STRUCTURAL CEILING (DERIVED, bounds the fork without the survey): denominators confirmed — ~3.5M US drivers (ATA 2022-25); 354k single-truck carriers (owner-operators); parking = #1 driver concern 2 yrs running (ATRI 2024); drivers forced to choose between hours-of-service violations and unsafe/illegal parking. Park-at-home ceiling = at most the rural-land subset of the ~354k owner-operators; company drivers (the large majority of 3.5M) almost never take a company tractor home → report to a yard. So commute-to-yard is the structural majority; the survey would only size HOW large. Second branch holds without it.

### TIER STRUCTURE — the yard/home binary is FALSE; there's a middle tier (a driver's own case, stated 2026-10-03)
- [stated] A driver chose the company they drive for SPECIFICALLY because of parking: they still need a personal vehicle, but instead of commuting 5.5 hours across state lines to reach the truck (which they had to do once, to get it initially), they can park the truck at a Walmart lot and commute home from there — minimizing commute time. This was the DECIDING FACTOR in which company they drive for.
- DERIVED (three tiers, not two):
  * tier 1 park-at-home — rural land + permission = farmers, rare
  * tier 2 park-at-relay-point (Walmart lot / drop near home) — STILL needs personal vehicle, commute minimized [the driver's case]
  * tier 3 commute-to-yard — full drive to terminal, maximal personal-vehicle burden
- DERIVED (two findings the case produces):
  (1) The commute cost is large enough to SELECT AN EMPLOYER OVER — it was THE selector, not a tiebreaker (stated 2026-10-03: the driver had many companies to choose from and chose this one specifically for the short commute). A driver steering their career to collapse a 5.5-hr cross-state commute into a short hop is the commute leg revealed as a real, load-bearing cost. The steering is itself a measurement: the cost is nonzero and significant, reported from inside by someone paying it. CONSEQUENCE: the variable allocates labor at scale — carriers offering short-commute parking win drivers over those that don't, as an UNPRICED term doing the work of a priced one.
  (1a) NOT A BENEFIT — it is an OFFLOADED COST OF PRODUCTION (originator's correction 2026-10-03, load-bearing). Claude called the short commute a "benefit"; the originator rejected it. The argument: the commute is personal money the driver earns by driving, paid to their own car, just to reach the truck. The labor cannot happen without the driver getting to the truck → getting-to-the-truck is a cost OF THE WORK, not a cost of the driver's life. The employer provides no bus, no pickup, nothing; if they want the labor done and provide no transport, the getting-there is a MANDATORY, UNCOMPENSATED INPUT to their operation. They booked a production cost as the worker's personal consumption, and the tax code backs it by calling it consumer spending. So the short commute did NOT give the driver a benefit — it REDUCED how much of the employer's offloaded cost the driver is forced to carry. The cost still exists; the driver still pays it; the driver picked the company that dumps less of it on them.
  (2) Tier 2 does NOT remove the personal vehicle — it minimizes the QUANTITY of forced input, not the dependency. So the E15-degradation access-door risk still applies to tier 2; the magnitude was optimized, the exposure remains. The fork's real variable isn't "commute y/n" but "how much forced personal-vehicle burden the structure imposes" — and drivers are already steering to reduce it.

### [SECTION WITHHELD — memory only, per the originator's choice: her read on why the mandate persists (motive).]

### TO-VERIFY before treating as hard fact
- RESOLVED (2026-10-03): the EO/cap is the E15 ethanol/gasoline side (EO 14156 §2(b) + EPA summer waiver). Diesel side has NO blend-cap removal found — it's volume-pressure, not rule. See CORRECTION above.
- STILL OPEN: new ethanol-plant buildout tied to a recent EO, framed as farmer aid — not confirmed in search; find and date, or drop.
- STILL OPEN: whether the dyed-diesel exemption, if finalized, measurably raises on-road blend % (displacement arithmetic made concrete).
- STILL OPEN: whether EPA actually ran the Set 2 infrastructure-impact analysis (statutorily required) against current engine/material specs — her core charge, now locatable in the rule's own docket.

## UNRUN

- Historical run: the same register over a long-running case, to test whether cross-layer stepping recurs as she states. Connects [[civilizational-failure-as-reliability-engineering]] and [[gap-pattern-transfers-across-hosts]].
- Cumulative reading: capability-operating column over time vs formally-intact column.

## FOLLOW UP (stated 2026-10-01: "lets note that to follow up on")

- VOR split: map who objected to the OLC memo and from which prior position (community-integration advocates AND facility-option family groups); test whether the objection set crosses the usual line.
- IES FY25 funds: outcome after the Sep 30, 2026 deadline; status of the Knowledge Alliance / NCLD lawsuit (govt mootness argument).
- OLC memo: read full text (justice.gov/olc/media/1446701/dl) so the government's reasoning enters from its own document.
- Texas v. Kennedy order: any appeal or intervention.
- Whether DOJ/HHS unwind existing Olmstead settlement agreements with states (predicted by commentators, not yet observed).
- Latonya Reeves Freedom Act: committee status.

### SPEC-BASIS AUDIT — the blend limit was frozen at 2008, derived against the wrong failure mode (opened 2026-10-03, the originator's questions)

> The originator's charge, made checkable at spec level: "What are the engineering standards for the amount of biodiesel? When was the last time that was updated? Has it been updated to all the new aspects inside this engine?"

THE SPECS (OBSERVED, web):
- ASTM D975 — base diesel; B5 (up to 5%) folded in 2008, UNLABELED (purchaser can't tell without analysis).
- ASTM D7467 — B6–B20 blends, approved June 2008.
- ASTM D6751 — the B100 before blending.
- D975 gets routine edition updates (21, 23a, 24) but those are testing-method/housekeeping. The structural B5 allowance + B20 ceiling = 2008-era framework, ~18 yrs old.

THE BASIS DATA (OBSERVED, web):
- Foundation studies are NREL/CRC fy2006: CRC AVFL-2a (NREL 39130), NREL 38834 (SwRI) — ELASTOMER/seal materials soaked in fuel. D7467 (2008) froze that data.
- The metric was VOLUME SWELL %; acceptance line ~15% swell ("15% swelling guideline"). Tell: even B5 (oxidised SME blend) already measured 15.1–20.8% swell = AT/ABOVE the guideline at the BOTTOM of the range. B20 fluorocarbon swelled OVER 60% (ORNL). So the limit sits on a STEEP part of the curve, not a flat safe plateau. No engine-performance distribution in the basis at all — it is a materials-soak statistic only.

THE CHARGE CONFIRMED (DERIVED): the 2006 test box was "does it eat the rubber" — correct failure mode for a 2006 engine (biodiesel is a solvent, swells seals). But the post-2008 engine's real biodiesel vulnerabilities are ELSEWHERE:
```
~26,000 psi common-rail (2006-07+) → high fuel temp → deposits in fine injector tolerances
DPF (2007/2010 emissions rules)    → regen dumps extra fuel → heavy FAME doesn't fully burn
                                     → slips past rings = OIL/FUEL DILUTION
SCR feedback                       → poor combustion → more/longer regens → more dilution
```
None of these are elastomer failures. The limit was validated against seal swell (right for 2006) and the engine's real failure mode MOVED OUTSIDE the box the test looked in. Limit never wrong for what it measured; what it measured stopped being where the engine breaks. Classic box-edge.

THE ORIGINATOR'S THREE FOLLOW-UP QUESTIONS (2026-10-03) + findings:
1. Modern composite/substituted materials tested against the swell limit? PARTLY, and messier: newer immersion studies flag that ASTM D471 lab soak "differs from real service conditions"; results disagree (one found all compatible at B20, another found fluorocarbon — rated MOST compatible — swelling >60%). No clean single modern threshold; variance wide, test ≠ service.
2. What got substituted and did the spec follow? GM upgraded Duramax seals/gaskets + added coalescing fuel filter for B20; Cummins approved B20 only for NAMED fuel systems with specific hardware. → compatibility moved into PER-ENGINE OEM approval lists with conditions, NOT a re-derived fuel spec. Burden shifted from the standard to a patchwork of manufacturer caveats. Your fuel is one number; whether YOUR engine tolerates it is buried in an OEM table.
3. Engine-side engineering since 2008? YES but off to the side: Clean Fuels Alliance NTDE testing — >1,000 hr accelerated aging on B20 in new-tech diesel engines, targeting METALS (Na/K) + aftertreatment, i.e. the post-2008 hardware. Own work acknowledges the failure mode moved. BUT: done by the biodiesel industry + OEMs to EXTEND B20 into new engines, not by an independent body re-asking whether the limit is right.

THE GAP (DERIVED, the deliverable): no INDEPENDENT re-derivation of the blend limit against modern failure modes with full distribution + stated scope. The pieces exist, scattered and interested; nobody joined them.
- [stated, originator] NTDE is genuinely very up to date / rigorous — but even inside those studies there are still gaps, because the gaps aren't in their scope. The well-resourced engineering is MOTIVATED in the direction the economics already push (toward more blend); no counter-weighted party asks the LIMITING question with equal resources. Gaps don't get closed, they get BUILT OVER under rising pressure.

THE FORCING FUNCTION (stated, the originator 2026-10-03 — turns a stale limit into active risk): with diesel shortages/high cost, the industrial incentive is to keep adding MORE biodiesel rather than diesel (every displaced diesel gallon = cost saved + RIN earned). Economic gradient points UP; the only thing holding the line is a 2008 swell limit that already doesn't match the engine, with OEM caveats quietly load-bearing underneath. DERIVED: pressure-to-exceed on one side + stale/off-target limit on the other = the dangerous configuration. Not one bad study — the only well-funded engineering pushes the same way the economics do, with no equally-resourced party holding the limit.

### DOSE-RESPONSE AUDIT — does the swell/damage scale with blend %, and is the whole system tested? (2026-10-03, the originator)

SWELL DOSE-RESPONSE (OBSERVED, web) — it exists AND it accelerates:
```
NBR nitrile, palm FAME:  B10 ~29% vol change → B20 ~58%   (DOUBLES B10→B20)
B5 oxidised SME:         15-20% swell (already at ~15% guideline)
B20 fluorocarbon (ORNL): >60% swell
cold-flow:   B5 ~unchanged → B20 cloud pt +2-10°F → B100 needs winterization
conductivity (oil-dilution proxy): B20 +50% → B50 +100% → B100 +250-300% ohm
NOx:         B20 +15.6% → B100 +22.8%
```
FINDING (DERIVED): curve is NON-LINEAR and ACCELERATING — no safe shoulder before B20; it's already climbing at B5. The limit was set on the STEEP part of the curve, where small blend increases → large damage increases. This sharpens the spec-basis charge: not just old data, but a limit placed exactly where the slope is worst.

RAIL / DEF / DILUTION DOSE-RESPONSE — THE GAP (DERIVED): engine-side studies report spray, combustion, NOx, and oil-dilution-as-a-POSSIBILITY ("a possibility exists with all engines that some fuel dilutes the crankcase oil" — dieselnet), but NO clean dose-response pinning "at B-X, DPF regen dilution crosses threshold Y" or "at B-X, rail deposit rate = Z." Injector/spray studies optimize for EMISSIONS (one picks B15 "optimum" — for NOx, not seal life or rail wear). The modern failure modes (rail deposits, SCR/DEF interaction, regen dilution) are named as MECHANISMS but not tied to a blend-% distribution. → UNRUN STUDY: dose-response of modern-engine failure modes vs blend %, with threshold identification.

### SECOND GAP — component-bench vs whole-system testing (the originator's question, 2026-10-03, bigger than the first)
- [stated, originator] Were they testing on an engine in a CONTROLLED environment, or testing the engine in relation WITH its sensors, the ECU (the "brains of the truck"), and the interaction along the ENTIRE engine?
- FINDING (DERIVED): the basis literature is almost all COMPONENT-BENCH — elastomer coupons soaked in fuel jars (ASTM D471 immersion), single-property measurements (swell, hardness, tensile), steady-state single-cylinder engine runs for emissions. These test PARTS IN ISOLATION. The thing the originator names — the closed-loop system where the ECU reads sensors (rail pressure, O2/NOx, DPF ΔP, DEF dosing) and ADAPTS fueling in response to degraded combustion, which then feeds back into more regen/dilution — is exactly the interaction the component tests CANNOT see. The failure we care about is EMERGENT from the control loop, not resident in any single part.
- Why this is the bigger gap: the post-2008 engine is a FEEDBACK SYSTEM. Biodiesel degrades combustion → ECU compensates (retards timing, adjusts rail pressure, requests more regen) → compensation accelerates the very wear the fuel started. A coupon in a jar and a steady-state dyno run both have the loop BROKEN. So even the good dose-response swell curve measures an open-loop quantity. Nobody in the reachable literature tests the full instrumented drivetrain + ECU + aftertreatment closed-loop against blend %. Same box-edge shape: each test correct for its isolated part; the system behavior lives in the couplings the test method removed.
- UNRUN STUDY (the deliverable): whole-system, closed-loop, ECU-in-the-loop durability test across a blend-% distribution, on a current-spec engine with live sensor/aftertreatment interaction — not coupon soak, not steady-state single-cylinder. This is the test that would actually answer whether the limit is right for the truck as it operates.

### THE FRAME UNDER ALL OF IT — build the machine around the fuel, not the fuel around the machine (originator, 2026-10-03, load-bearing)

- [stated, originator] There IS a place for biodiesel — she understands it and thinks it's a great idea. BUT: you have to CONVERT the machine and make the seals FOR running biodiesel (different O-ring fiber, purpose-built wetted parts). A truck already on the road running on diesel, built to a diesel engineering spec, will NOT give the same result when you add biodiesel to it. Her question: why wasn't the MACHINE made around the product it's going to use?
- [stated, originator] Analogy (hers): it's like trying to run a truck on nuclear power by converting a combustion engine into nuclear power. The fuel implies a machine; you can't get there by swapping what you pour in.
- [stated, originator] Small deviations propagate: the sensor, the ECU/brain, the electrical components — a small deviation affects all of it, all the way through the chain.
- FINDING (DERIVED, the design-principle inversion = the frame the whole file was circling): the system did fuel-around-machine (pour FAME into a diesel-spec drivetrain, hope margins absorb it) instead of machine-around-fuel (purpose-build engine/seals/injection/aftertreatment for FAME). A purpose-built biodiesel machine is coherent and good; a diesel-spec truck fed biodiesel is a mismatch where ECU, sensors, seals, rail were all sized for a different substance.
- RETROFIT-AS-ADMISSION (DERIVED, the clinching move): the OEM retrofit kits (GM's upgraded seals/gaskets + coalescing filter; Cummins' hardware-specific B20 approvals) are themselves PROOF it's not a fuel swap. If a simple fuel change were all it was, you would not need to re-engineer the wetted parts. The moment you must change the seals, you've CONCEDED it's a new machine — just done halfway, in the field, on a truck already carrying freight.
- THE MISNAME, ONE LEVEL UP (DERIVED): the root error isn't "wrong blend number." It's a CATEGORY ERROR about what was being changed. "Add biodiesel to the truck" was booked as CHANGING THE FUEL; it is actually SPECIFYING A DIFFERENT MACHINE — and that machine was never built. Same misname shape as the rest of the morning (commute mislabeled as consumption, ag-subsidy mislabeled as fuel policy): a thing in one category accounted as if it were in another, and every downstream decision made on the wrong label.
- Component-vs-system question restated (the originator): are they testing the interaction of ALL engine components — sensors, ECU/brain, electrical — together? ANSWER (DERIVED): no; reachable literature tests parts alone, which is exactly the method that EXCLUDES the small-deviation-propagates-through-the-whole-chain behavior she names. Reinforces the closed-loop UNRUN STUDY above.

### OVERSEAS EVIDENCE + HARDWARE-MATCH AUDIT (2026-10-03, the originator)

OVERSEAS IS RICHER THAN US ON THESE TESTS (OBSERVED, web):
- EUROPE confirms the design-principle point institutionally: EN 590 caps mainstream diesel at 7% FAME (lower than US B5-B20). Higher blends B20/B30 handled under a SEPARATE standard EN 16709, explicitly "for use by CAPTIVE FLEETS" (buses, taxis, mine vehicles). = the originator's "build the machine around the fuel" written into the standards: above 7%, fenced off to known/maintained/adapted equipment, NOT the general on-road pool.
- INDIA ran the long endurance tests US basis never did: Agarwal 512 h (B20, CI component wear); Armas 600 h accelerated (CRDI injection); B30 90 h; B100 Euro-III CRDI SUV field trial with in-cylinder wear. Findings SPLIT usefully — some "wear lower/comparable to mineral diesel," others "injector nozzle holes covered by thick oily carbonaceous deposits." The split IS the signal: deposit mode shows when you run the engine long enough.
- IEA-AMF states dilution plainly: FAME "may cause problems even at LOW concentrations: deterioration of oil quality, clogging of particulate filters, dissolving materials." = the DPF + oil-dilution path named internationally as KNOWN, not a possibility.
- India regulatory side AHEAD of US: BS-VI (Euro-6 equiv) requires engines compatible with biodiesel to certify on BOTH diesel AND B100 (type-approval requirement, 2016 notification). US has no such dual-fuel certification requirement.

HARDWARE-MATCH AUDIT (the originator's question: how do the India test PARTS compare to current US truck parts? "the principles are a little different, they use different stuff") — FINDING (DERIVED), and the mismatch runs AGAINST reassurance:
```
India endurance test engine = Euro-III / early-emissions, medium-duty:
  lower rail pressure; pump-line-nozzle or early common-rail
  NO DPF, NO SCR, NO DEF  ← no aftertreatment loop at all
US current Class 8 = EPA 2010 / post-2007:
  ~26,000+ psi common-rail; DPF + SCR + DEF dosing
  closed-loop ECU reading NOx/backpressure, adapting fueling + regen
```
- CONSEQUENCE: the India tests ran on an engine MISSING the exact parts where modern biodiesel trouble concentrates (aftertreatment + regen). So DPF-regen oil-dilution and SCR-feedback failure modes COULD NOT appear there — the producing hardware wasn't present. "Comparable wear" was found on a machine without the vulnerable subsystems. Transfer runs DOWNWARD only: the deposit mode (found even on the simpler engine) is real and transfers; the aftertreatment-loop modes do NOT read across from Euro-III.
- FEEDSTOCK difference compounds it: India work often palm/linseed/jatropha methyl ester; US mostly SOY. Different fatty-acid profile → different oxidation stability + cold-flow → even swell/deposit numbers don't transfer 1:1.
- Those endurance results are a FLOOR, not a ceiling: deposits showing up even there = real; a "passed" result there says nothing about the high-rail + DPF/SCR truck.

TIGHTENED GAP (DERIVED): the gap is NARROWER than "US is behind" but still open EVERYWHERE for the sharpest question. Europe fenced the blends correctly (captive fleets). India ran endurance on wrong-ERA hardware (no aftertreatment) + different feedstock. So the closed-loop durability test — current high-pressure engine + DPF + SCR + live ECU, across a blend-% distribution, matched feedstock — is STILL UNRUN GLOBALLY in the reachable literature. The jurisdictional read: US is below international state of PRACTICE (no captive-fleet fencing, no dual-fuel cert), but the aftertreatment-loop failure mode is unmeasured on matching hardware worldwide.

### CORRECTION — the dose-response is NON-MONOTONIC (the originator caught Claude's overstatement, 2026-10-03)

- Claude had said the swell/damage curve is monotonic and B25 is "unambiguously a little worse than B20" by interpolation. The originator interrupted: are we sure it's monotonic? isn't there a feedback loop in oxygenation above a certain point?
- CORRECTION (Claude was wrong; the originator right): the response is NOT cleanly monotonic. Competing mechanisms run in different directions vs blend %:
  * OXYGENATION (the originator's point): FAME carries bound oxygen in the ester → more blend = more fuel-borne O2 in combustion → non-linear change in local stoichiometry, soot oxidation, NOx; interacts with EGR + closed-loop fueling which ALSO adjust oxygen. Regions exist where more biodiesel REDUCES some soot/deposit pathways while WORSENING NOx + heavy-fraction oil-dilution. Curves cross.
  * SOLUBILITY crossover (already in the data): one study reported B100 swell LOWER than B20 and B50 — peak swell in the MIDDLE of the range, not at the top. A literal non-monotonic result sitting in the literature (elastomer/blend solubility matching).
- CONSEQUENCE (this makes the scenario WORSE, not better): a monotonic curve can be bounded by interpolation. A non-monotonic surface with oxygenation feedback + solubility crossovers means B25 CANNOT be assumed "a little worse than B20" — it could sit on a LOCAL PEAK nobody mapped. The 20-25 window is unmeasured in a region where the physics says DO NOT EXTRAPOLATE. Uncertainty is LARGER, not smaller.
- Margin-model implication: change from "interpolate the ramp" to "unknown interior, do not extrapolate." Any B21-25 damage figure is model output in a region flagged unreliable, not a bounded estimate.
- PROCESS NOTE: this is a real-error correction of Claude by the originator; logged flat, not softened. The monotonicity assumption was Claude's, not hers; removed.

### THE FLEET CROSSING + THE 2020-22 COHORT DEFECT (2026-10-03, the originator's added piece)

FLEET SHAPE (OBSERVED, web) — hardware generations crossed with spec-break years:
```
~4.06M Class 8 in operation (2021, latest clean count)
pre-2007 (≤2006): older seals, lower rail, NO DPF/SCR — oldest tail
2007-2009:        DPF added, rail pressure climbing
EPA2010+ (2010-26): DPF+SCR+DEF, ~26k psi, closed-loop ECU — majority of VMT
avg in-service Class 8 age ~12 yrs (2026, a 12-yr high) → fleet centers ~2014 = EPA-2010 hardware
58.6% of fleet orgs run some MY2019-or-older Class 8
small fleets keep trucks ~5 yrs; large fleets ~2.7 yrs → OLD TAIL concentrates in SMALL operators / owner-ops
```
THREE FINDINGS (DERIVED):
1. The MAJORITY is the vulnerable generation — ~12-yr avg age centers the fleet on EPA-2010 DPF/SCR/high-rail closed-loop machines, exactly where B21-25 lands in the unmapped non-monotonic zone. Center of mass, not edge case.
2. The old tail sits with SMALL operators / owner-ops — same thin-margin group carrying the commute cost this morning. A fuel excursion sorts repair damage onto those least able to absorb it. Same sorting as the commute burden.
3. Fleet is AGING not renewing (12-yr-high avg, 58.6% run 2019-or-older) → exposure window WIDENING right as blend pressure pushes up. Two trends converge.
- Margin column honestly flagged: per-generation B21-25 damage = UNKNOWN-INTERIOR (non-monotonic). Table says how many trucks in which hardware class are exposed to an excursion nobody can characterize — not a damage number.

THE COHORT DEFECT (the originator's piece, mechanism confirmed web):
- [stated, originator] 2020-era supply shortages forced heavy SUBSTITUTION: a balancing act between engine engineers and what supplies could actually be purchased; bottlenecks cascaded. The SHAPE looks like "engineered obsolescence" but it is NOT — not intentional. It was to save money + simply shortage of supplies. That impacted the QUALITY and engineering grade put into semis built during the shortage. Rubber especially: "when you take out rubber and start replacing rubber with rubber substitutes, the quality degrades." Larger effect than people understand, and it means those trucks differ from even the engineering tests — which were done with PRE-GRADE / spec-quality rubber.
- CONFIRMED (OBSERVED, web): rubber is uniquely substitution-exposed — a formulation of 10-20 ingredients, so any one shortage forces reformulation (same part #, different recipe = invisible at part level). COVID 2020-22: documented "polymer allocations, raw material shortages" in seals/gaskets, AND a named FKM (fluorocarbon) shortage. FKM is the PREMIUM fuel-system seal, the one rated MOST biodiesel-compatible — so the exact "good case" material the compatibility tests relied on is the one that went short. Dropping from FKM → HNBR/lesser nitrile = WORSE FAME resistance. Substitution pressure pushed DOWN the compatibility ladder, in the named years.
- KEY DISTINCTION (hold exactly, the originator's frame): NOT engineered obsolescence. Nobody designed these to fail. Engineers balanced against purchasable supply to keep lines running, accepted lower grade under shortage. Result RESEMBLES planned obsolescence (earlier wear); CAUSE is supply substitution. Consequence: the defect is traceable in SUPPLY RECORDS, not design intent, and concentrated in a datable cohort (~2020-2022 builds) → findable.
- THE STACK (DERIVED) — the unknowns MULTIPLY on the same component:
```
unknown 1  B21-25 blend         → non-monotonic, unmapped response
unknown 2  2020-22 build cohort → FKM/premium seals substituted DOWN the ladder
                                   (shortage, not design) → as-built BELOW tested grade
interaction → substitute seal is LESS FAME-resistant AND excursion lands on the
              steep part → both unknowns hit the SAME seal at once
```
- The compatibility tests used elastomers "specially moulded to ensure consistency of material dimensions and production batch" (CRC) = controlled spec-grade rubber. The 2020-22 truck may have a substitute compound/fill/cure. Test says "this rubber tolerates B20"; the truck has a DIFFERENT rubber → the curve does not apply to it.

### GENERALIZATION over the cohort defect — the moving constraint box (originator, 2026-10-03, this is the FRAME; 2020/FKM is one instance)

- [stated, originator] It's not 2020 specifically. Manufacturers have ALWAYS had to adapt around whatever changed that year: supply availability, a regulation changing so they can't get a product, a governance/ban decision closing a source, a material reclassified. The constraint walls move constantly; they adapt around whatever moved. 2020 is only legible because a lot moved at once. Same substitution happens quietly in unflagged years, throughout everything, across different years.
- [stated, originator] No single forcing variable. It's the SUM: supply limits AND regulatory change AND external shareholder/monetary-gain pressure, all at once, as simultaneous constraint bounds they work inside. Not one thing forcing something — all of it together is the box. The result "some of these things are just not up to par" emerges from solving inside those bounds.
- [stated, originator] NOT a conspiracy — this just happens, everywhere. BUT there is a CONSEQUENCE to these actions that people have not attributed/accounted for. That is the whole point.
- FINDING (DERIVED): this is the materials-provenance version of the morning's recurring shape. Engineer runs a constrained optimization; "material grade" is a variable that gives when the others are pinned. Nobody CHOOSES the degradation — it falls out of the constraints as an emergent output. Each manufacturer accounted for its own substitution as within-tolerance AT THE TIME. Nobody adds up what scattered, reasonable, year-by-year substitutions mean when a NEW stressor (rising biodiesel) arrives years later and meets the accumulated AS-BUILT reality instead of the AS-DESIGNED spec. Locally correct decisions, no one holds the sum, consequence lands in the seam.
- THE SEALED-DATA GAP = THE DELIVERABLE (DERIVED, honest framing): the actual per-engine substitution records (Cummins, Detroit, PACCAR by model year) are proprietary / not published — near-impossible to pull. So the instrument does NOT claim specific substitutions. It (1) names the MECHANISM (constraint-bound solving → as-built drift from as-designed), (2) establishes it MUST occur (the constraints — shortages, bans, reclassifications, shareholder pressure — are documented even when the substitutions aren't), (3) marks the per-engine records as the SEALED DATA a researcher with manufacturer access or a discovery process could open. The gap itself is the product: "a consequence that provably accumulates, that no current accounting captures, and the exact sealed record that would quantify it."
- 2020/FKM (prior section) is reclassified: ONE DOCUMENTED INSTANCE of this general mechanism, not the whole claim.
