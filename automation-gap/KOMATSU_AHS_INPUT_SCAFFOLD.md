# THE KOMATSU SCAFFOLD — AHS vs human-driven haulage, input by input
### The one deployment with a 17-year, third-party-documented ledger. Built 2026-09-24.

**Why this scaffold:** FrontRunner AHS is the only 6/6 record in the demo corpus audit.
Commercial since 2008, 1,000+ ultra-class trucks commissioned (April 2026), 11.5 billion
tonnes hauled. If the question "what does automation actually cost in inputs, against the
human it displaces?" can be answered anywhere on evidence, it is here. Every number below
carries its provenance. Constructed arithmetic is declared.

---

## THE INPUT LEDGER (per truck-year, ultra-class ~290 t truck, 88% availability)

| Input | Human-driven | AHS | Provenance |
|---|---|---|---|
| Usable hours/yr | 6,552 | 7,323 (+12%) | Whittle/Redwood model on Pilbara data; operator-reported +700..1,000 h/yr |
| **Diesel per tonne** | 1.00× | **1.00× — CLAIMED −13%, NOT MEASURED** | Vendor/operator channel claims reduction; independent WA financial model: "evidence of reduced diesel consumption was not found in practical usage." Held at parity, labeled CLAIMED-NOT-MEASURED |
| Tire & brake consumption | 1.00× | 0.71× (+40% life) | Operator-reported via vendor channel; tire replacement at 6,000–7,000 h vs 5,000 h |
| Maintenance inputs | 1.00× | 0.87× (−13%) | Operator-reported via vendor channel |
| Inspection events | every 12 h shift | every 48 h (~4× fewer) | Operator-reported |
| Direct human hours/truck | ~9,000 (≈4.5 drivers) | ~1,800 (control room + AHS tech share) | CONSTRUCTED, anchored to "less than one operator per truck" reporting |
| Mean speed | 1.00× | 0.94× in mixed fleets | Hatch 2024: −15% documented where AHS shares ground with manned equipment; safety-bubble stoppages |
| Throughput/truck-year | 1.00× | ~1.05× | constructed from hours × speed factor |
| **Human hours per unit throughput** | **1.37** | **0.26 (−81%)** | constructed from the above |
| New inputs AHS adds | — | telecom network, GPS base stations, servers, cybersecurity, OEM licensing, more frequent road grading (smaller road volume), AHS specialist roles | Hatch 2024, itemized |
| Unit haulage cost | 1.00× | 0.85× | Rio Tinto "Mine of the Future," company-reported; Whittle model agrees direction |

## WHAT THE SCAFFOLD SHOWS

**1. The energy advantage is NOT fuel.** The keynote claim (smoother driving = less diesel)
is not borne out in the independent WA record. The real energy saving per tonne is in
**machine wear** — tires, brakes, components: embodied energy and parts-logistics energy,
reduced ~13–29%. Consistent inputs beat skilled inputs *on a closed course*, and the saving
lands in the parts bin, not the fuel tank.

**2. The human input drops 81% per unit of throughput — and does not reach zero.**
It moves: drivers (abundant-ish, trainable) → control-room operators, AHS technicians,
cyber/telecom staff (scarce, and getting scarcer — see the trades-shortage ledger). The
scaffold's key transformation: **labor is not deleted, it is concentrated into fewer,
scarcer, harder-to-replace skill nodes.** That is the effective-redundancy finding wearing
a hard hat: N_nominal falls, and what remains shares one node — the specialist.

**3. The autonomy tax is infrastructure.** Telecom, servers, licensing, cybersecurity,
extra grading. These inputs are real, recurring, and doer-staffed. They are absent from
the "one operator per truck" headline because they live in other departments' budgets —
the boundary trick declared-frame exists to catch.

**4. Speed is sacrificed for consistency in mixed fleets.** −15% where manned and unmanned
share ground: the system stops for safety bubbles and unidentified obstacles a driver would
roll past. On a fully privatized site the penalty vanishes — which is the general law this
scaffold establishes: **automation's economics close only where the environment is owned,
structured, and re-engineered around the machine.** The mine works because the mine
rebuilt itself for the trucks (roads, comms, dispatch, multipath GPS). The public highway,
the farm, the job site, and the kitchen do not offer that deal.

**5. The retained-skill erosion is priced nowhere.** Control-room supervision of autonomous
fleets produces skill degradation and reduced situational awareness (MDPI Mining 2026) —
the capability the system depends on for exceptions is consumed by the arrangement.
Closure-cost's instrument branch, running in production. It appears in no ledger column.

## REUSE RULES (how to point this scaffold at another domain)

1. Demand the five ledger columns: fuel/energy, wear, human hours (all grades, not just
   the displaced one), new infrastructure, supervision overhead.
2. Label every cell by provenance: MEASURED-independent / operator-reported /
   vendor-claimed / FORECAST / CONSTRUCTED.
3. The fuel cell is the honesty test: if a domain's claimed savings exist only in vendor
   studies, hold it at parity until an independent measurement exists (as here).
4. Ask what the environment had to become for the numbers to close. The environment
   re-engineering cost belongs IN the ledger.
5. Ask where the human hours went, not whether they vanished — and whether what remains
   shares one scarce-skill node.

## Falsifiers

```
AUT-F7  AHS fuel parity: claimed -13% diesel, independent record shows none
        Refutes if: an independent (non-vendor, non-operator-PR) fuel
        measurement on production AHS fleets shows >5% diesel/tonne reduction
        at matched duty cycle
AUT-F8  Human-input floor: ~0.9 humans/truck-year-equivalent residual
        Refutes if: a production AHS site publishes a full ledger (incl.
        telecom, licensing, supervision, road crews) showing <0.25 human
        hours per unit throughput sustained 2 years
```

---

# V2 — UNMELD PASS (operator review, 2026-09-24)
### Four melded variables separated. Two confounds confirmed against the record, two held UNKNOWN.

## U1. The driver–maintenance overlap (scaffold error, corrected)

The v1 ledger listed "inspection events" as a separate line. Wrong. In manned operation,
pre-trip/post-trip inspection is **on-duty driver time** — a regulated, paid overlap
(DVIR, 15–30 min, counts against the duty window). The driver's paid hours already contain
the inspection.

Correction to the ledger:
- Manned case: inspection labor is **inside** the ~4.5 drivers/truck — no separate cost.
- AHS case: the drivers are gone, so inspection becomes **dedicated technician time** —
  which is *more* expensive per event, not less. The "inspections every 48 h instead of
  every 12 h" claim is therefore not a clean 4× labor saving; it is a transfer from
  embedded (already-paid) driver time to dedicated (newly-paid) tech time, at a reduced
  frequency that AHS itself requires because the daily human walkaround no longer exists.
- **The daily walkaround was also a sensor.** A driver on pre-trip finds the weeping hose,
  the soft tire, the cracked mount — by hand and eye, before the failure. AHS replaces this
  with scheduled telemetry + tech inspection at 48 h. What telemetry doesn't cover rides
  for two days. UNMEASURED in the public record: fault-detection latency, walkaround vs
  AHS telemetry.

## U2. Hours: regulation, not ability (decomposed)

v1's utilization delta (6,552 → 7,323 h/yr) melded four things. Decomposed:

| Component of manned "lost hours" | Nature |
|---|---|
| Fatigue-law rest (WA: max 12 h driving/24 h; breaks; 168 h/14 d cap) | **REGULATORY** — a human could physically drive more; the law forbids it |
| Shift change / crib breaks / hot-seat gaps | operational practice |
| Pre-trip/post-trip on-duty time | regulatory (and it is the U1 overlap) |
| Absenteeism / turnover / camp churn | HR quality |

The AHS utilization advantage is mostly **regulatory release plus no shift change** — the
machine isn't more capable per hour; it is *legal* for more hours. Which means: the honest
comparison is not "robot vs human ability" but "robot vs human-under-fatigue-law."
The regulation exists because fatigue kills; AHS deletes the fatigue hazard rather than
out-performing it. Credit where due — but the ledger must name what the advantage is *made of*.

## U3. The wear confound — CONFIRMED (surface investment is bundled into AHS)

The question was: did they repair/upgrade the surface only when going autonomous?
The 2026 mine-planning review answers it: AHS deployment **requires** "more consistent road
geometry, controlled gradients, reliable drainage, predictable speed zones, low rolling
resistance, and higher surface-condition reliability" — and rolling resistance directly
drives fuel burn, tire wear, and maintenance demand (Michelin: stabilized surfaces cut
hourly fuel 3–5%; 1% rolling-resistance change ≈ 10% speed change on ramps).

So the tire-life (+40%) and maintenance (−13%) deltas are **confounded by the surface
upgrade the AHS deployment itself triggered**. Some of that gain was available to the
manned fleet all along, for the price of grading — a management choice, not a robot virtue.
And a reverse feedback is documented: AHS trucks drive identical lines (**channelized
wheel loading**), concentrating pavement damage and *increasing* road-maintenance demand —
which partially eats the tire saving and is staffed by grader operators.

Residual UNKNOWN (not resolvable from the public record): how much of the manned-era wear
was deferred maintenance or poor hiring/driving discipline — i.e., how much of the "AHS
advantage" is measured against a degraded human baseline. Two named hypotheses held open:
(a) consistent throttle/braking genuinely reduces wear at matched surface; (b) the manned
baseline was maintenance-deferred and the comparison is inflated. Probably both; the split
is UNMEASURED.

## U4. The dependency chain, with humans per link (the part v1 waved at)

| Link | Humans required | Change under AHS |
|---|---|---|
| Fuel: refinery → transport → site farm → fuel truck | refinery workers, tanker drivers, fuel-truck operator | unchanged |
| Haul road: survey → grade → water → drainage | surveyors, **grader operators (increased frequency)**, water-truck drivers | INCREASED |
| Comms: LTE/radio network, GPS base stations | network techs, tower crews, NOC staff | NEW |
| Control room | AHS controllers, dispatchers, trainers | NEW (replaces cab drivers, fewer heads, scarcer skill) |
| IT/OT: servers, cybersecurity, software updates | sysadmins, OT security, OEM remote diagnostics | NEW |
| Maintenance: field + component rebuild | HD mechanics, tire techs, offsite rebuild-shop workers | shifted: less routine, more specialist; rebuild supply chain unchanged |
| OEM layer | licensing desk, field service reps, engineering support | NEW recurring |
| Camp/logistics | cooks, cleaners, flights | reduced (fewer drivers onsite) |
| Regulator/insurer | inspectors, auditors, underwriters parsing a novel risk | NEW-ish |

**The chain's shape:** every NEW or INCREASED link sits in the scarcest skill bands
(network techs, OT security, AHS controllers, HD mechanics) — the same bands sitting at
580k+ unfilled openings in the trades ledger. The deleted link (drivers) sat in the most
replaceable band. **AHS doesn't shorten the dependency chain; it re-grades it toward the
links with the longest replacement lead times.** And the chain has a new single point of
failure with no human workaround at production scale: the comms/autonomy layer itself —
when it drops, the fleet stops, and the drivers who could have kept it moving are gone.

## Corrected headline

v1 said: "human input drops ~81% per unit throughput." v2 correction: that figure is
**regulatory release + embedded-overlap transfer + confounded wear**, not capability
substitution. The honest statement: **AHS converts a regulated, distributed, generalist
human input into an unregulated, concentrated, specialist human-plus-infrastructure input,
on a rebuilt surface, with the wear comparison confounded by the rebuild.** It still works —
17 years and 11.5 billion tonnes say so — but what it proves is narrower than what it is
quoted as proving.

### V2.1 — U3 refined by operator input: unpaved confirmed, causality sharpened

Operator correction accepted: haul roads are unbound wearing courses (crushed rock/gravel
over sand sub-base); mines do not pave unless forced. "Upgrade" under AHS therefore means
**grading discipline, drainage, and rolling-resistance control on gravel** — not pavement.

The record then answers the provenance question directly:

- **The road work happened because of automation, in the operators' own words.** Suncor
  (E&MJ, Dec 2019): AHS trucks "run in exactly the same path every time. In the summer,
  when the roads are soft, they could dig themselves into a deeper and deeper rut" — so
  Suncor worked with the OEM on a multi-trajectory fix AND "on the design and layout of
  its haul roads to better suit autonomous operation." The same interview then reports
  "reduction in maintenance needs, better fuel consumption and tire life." **The confound
  in one quote:** road redesign + multi-trajectory + reported wear gains, bundled.
- **The manned-era baseline was often under-maintained.** NIOSH/Univ. of Pretoria haul-road
  work: mine road maintenance historically ran on "heavy reliance on local experience,"
  ad hoc or fixed-calendar blading, "inefficient means... with the potential to generate
  excessive costs resulting from over- or undermaintenance." So part of the AHS-era road
  improvement was simply *doing road maintenance properly for the first time* — a gain
  available to the manned fleet at any time.
- **The confound is roughly quantifiable.** Pilbara rule of thumb (industry reporting):
  every two weeks of un-graded corrugation costs 1–2% of fleet tire life; sites moving to
  condition-based grading alone — no autonomy involved — report **5–15% tire-life
  improvement**. Set that against the +40% tire-life figure attributed to AHS: a
  substantial fraction of the "automation gain" was a grading-practice gain wearing an
  automation badge.
- **The reverse feedback is now priced and staffed:** AHS stop events from dust, defects,
  and water-truck proximity run 3–5 minutes each and cascade through the queue; graders
  and water trucks on the road "complicate autonomous truck operations" to the point that
  Rio Tinto deployed autonomous *water trucks* at Gudai-Darri — automating the road crew
  because the autonomous haulers can't cope with humans maintaining the road they need.
  The dependency chain absorbs its own feedback: the machine needs the road maintained,
  can't tolerate the maintainers, so the maintainers get automated too.

**U3 final accounting:** the wear/fuel advantage decomposes into (a) consistent throttle
application — genuinely robotic, (b) surface improvement triggered by the deployment —
management practice, available without robots, (c) under-maintained baseline — HR/ops
history, (d) channelized-loading penalty — robot-specific, *negative*. Public record
cannot separate (a) from (b)+(c); it does document (d). The +40%/−13% figures ride on all
four at once.
