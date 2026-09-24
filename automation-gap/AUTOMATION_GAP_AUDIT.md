# AUTOMATION GAP AUDIT — Where the Doer Is the Dependency
### Measured deployments only. Marketing and forecasts quarantined. Compiled 2026-09-24.

**Method note (corpus bias declared):** the written record on automation is produced
overwhelmingly by vendors, analysts, and desk-side institutions — the parties who sell or
forecast automation. This audit therefore weights **measured deployment outcomes** (failure
rates, downtime, intervention rates, productivity regressions) over demos, pilots described
by their vendors, and projections. Forecasts are labeled FORECAST. Vendor claims are labeled
VENDOR. Peer-reviewed or government numbers are labeled MEASURED.

---

## 1. ROBOTICS — road freight (Aurora, the best-case deployment)

MEASURED:
- May 1, 2025: first commercial driverless Class-8 service (Dallas–Houston). Within three
  weeks, OEM partner PACCAR requested a human back behind the wheel; Aurora moved the
  observer from sleeper to driver's seat.
- Rain is not validated: when the system judges itself out of scope (weather), it pulls
  over and ends the trip.
- A tire blowout or hands-on problem summons an Aurora team member to the truck.
- Deployment geography: fixed Sun Belt corridors (Dallas–Houston, Fort Worth–El Paso,
  Phoenix), validated lane by lane. 100,000+ driverless miles, zero attributed incidents —
  real, and achieved inside a validated envelope on fair-weather interstate.
- Second-gen reboot July 2026 targets 200 trucks by end of 2026; "roadside assistance
  specialist may sometimes sit in the back seat on longer routes."

THE GAP THE DOER FILLS: weather judgment outside the validated envelope, physical breakdown
response, and the last-mile/first-mile operations the corridor model excludes. The autonomy
is real *inside its envelope*; the envelope's edges are manned.

## 2. ROBOTICS — humanoids (the hype centroid)

MEASURED:
- Stanford research (via Fortune, May 2026): robots at ~90% success in controlled
  simulation complete ~**12% of real household/industrial tasks**.
- 1X NEO consumer humanoid (2026): launch autonomy estimated 60–70%; the rest is "Expert
  Mode" — a human teleoperator at HQ seeing into your home. VENDOR calls it a feature.
- Data bottleneck: 50–200 teleoperated demonstrations **per task**; a 20-task facility
  needs 1,000–4,000 demos (50–200 operator-hours) before deployment starts.
- Beijing World Humanoid Robot Games 2025: robots crashed into operators, missed boxing
  punches, needed constant staff intervention on the soccer pitch — after flawless demos.
- Figure's best public number: 47,000 packages / 38 hours — one task, one conveyor, one
  object type. Genuinely impressive; deliberately bounded.

THE GAP THE DOER FILLS: every un-rehearsed task, every environment that isn't the training
floor, and — structurally — **the training itself**: the robot's competence is distilled
human demonstration. The doer is upstream of the machine, not just beside it.

## 3. KINESTHETIC / DEXTERITY — agricultural harvesting

MEASURED (MDPI Agronomy, 77-study review, Nov 2025):
- Average robot harvest success rate: **76.1%** — "still far from meeting practical
  requirements."
- Only **5.1% of studies report damage rate** at all — the metric that decides whether the
  fruit is sellable is the metric the literature mostly doesn't publish. (A measurement-gap
  inside the automation literature itself.)
- Strawberry picking: machines found/picked ~50% of ripe berries vs 60–90% for human crews.
- Root causes named: occlusion, variable lighting, fruit-to-fruit variation, grip-force
  judgment on delicate skin. All kinesthetic-contextual.

THE GAP THE DOER FILLS: judgment-by-touch at speed — force, ripeness, damage avoidance —
on biological variability no two units of which match.

## 4. LOGISTICS INFRASTRUCTURE — automated container terminals

MEASURED (the strongest anti-hype dataset in this audit):
- McKinsey global survey: automated terminals cut opex 15–35% (vs 25–55% expected) and
  productivity **falls 7–15%**. Quay cranes: low-20s moves/hour automated vs high-30s
  conventional. ROI below industry norm by up to a full percentage point.
- Remote-controlled quay cranes: cycle times **20–30% longer** than manned cranes.
- 2025 Tobit regression across terminals (MDPI): automation coefficient **negative** in
  both models — more automation does not correlate with more efficiency.
- TRB/CIMNE 2023 benchmark: "no evidence automated container terminals are more productive."
- Credit where measured: truck turn times ARE consistently faster at the automated Long
  Beach terminal; safety and consistency gains are real.

THE GAP THE DOER FILLS: the final handling onto the vessel ("will always require
operational leadership from well-trained people" per terminal experts), density-sensitive
yard judgment, and the exceptions that desynchronize an automated terminal's choreography.

## 5. MINING — automation's genuine success story, with the fine print

MEASURED: Autonomous haulage (Komatsu FrontRunner-class) is the most proven full-autonomy
deployment anywhere — private roads, single operator, controlled terrain. It works.
And the fine print (MDPI Mining, Aug 2026):
- Control-room operators supervising fleets face **cognitive overload** at scale.
- Supervised autonomy produces **skill degradation and reduced situational awareness** —
  the human is kept for the exceptions while the system erodes the skills the exceptions
  require. (This is closure-cost's instrument branch in the wild.)
- Roles displace to maintenance, control rooms, data: the trucks don't fix themselves.

THE GAP THE DOER FILLS: maintenance of the automation, and the retained capacity to
intervene — which the automation itself is quietly consuming.

## 6. IMAGERY / COMPUTER VISION — inspection and defect detection

MEASURED:
- Field review of bridge-inspection AI: thermal+optical detected 4/7 delaminated areas with
  3 false positives; a human with a **chain drag** got 5/7 with 3/3 true negatives.
- Domain shift is documented and quantified: lighting drift, weathering, mixed defect
  types, and new suppliers degrade deployed CNNs; models trained on static annotated sets
  degrade in uncontrolled settings ("performance degradation and reduced generalization").
- Vendor claims of 97.8–99.7% accuracy are VENDOR; the field literature's own numbers are
  85–90% with material false-positive rates, and accuracy is "a misleading headline metric"
  where defects are rare (industry practitioner's own guidance).
- Drones genuinely win on speed, safety (91% fewer on-site accidents), and coverage —
  MEASURED. Detection judgment under real-world variability remains human-verified.

THE GAP THE DOER FILLS: verification, disposition ("is this crack structural?"), and the
cross-modal senses imagery lacks — sounding, touch, smell, the feel of a member under load.

## 7. MODELING / FORECASTING / SUPPLY-CHAIN AUTONOMY

FORECAST (labeled): Gartner, March 2026 — 60% of supply-chain disruptions "resolved without
human intervention by 2031." A prediction, from an analyst firm, five years out.
The tell inside the pitch: Gartner's own recommendations include "develop contingency plans
for failures in autonomous decisions, including **protocols for rapid human intervention**."
Even the autonomy sales deck keeps the doer as the failover system.

MEASURED pattern from sections 4–6: automation performs inside its data's envelope;
disruptions are by definition outside it. The exception queue is the human job description.

## 8. ENERGY — the arithmetic nobody puts in the keynote

MEASURED:
- Humanoid locomotion consumes **10–50× more energy per unit distance** than human walking.
- Humanoids are battery-constrained to ~1/8 of body mass (vs 1/3 tolerable in EVs); heavy
  dynamic duty can cut battery cycle life to ~200 cycles, eroding unit economics.
- Reference human: ~2.3 kWh/day chemical energy, self-refueling from food, all-terrain,
  with onboard repair and a 20 W general-purpose brain.
- Running Atlas-class hardware ≈ 3.7 kWh for ~1 hour of mixed physical work.

THE GAP THE DOER FILLS: the energy logistics themselves. A doer works all day on lunch and
sleeps it off. The robot needs a charge infrastructure, a battery supply chain, and a
replacement schedule — each of which is itself a doer-staffed dependency chain.

## 9. DEPENDENCY CHAINS / SUPPLY CHAINS — the macro numbers

MEASURED (BLS, ABC, McKinsey, July–Sept 2026):
- **580,000 manufacturing + 326,000 construction** job openings, July 2026 (BLS).
- Associated Builders and Contractors: construction needs ~**349,000 net new workers in
  2026**; 92% of firms report difficulty hiring qualified people.
- McKinsey: **130,000 additional electricians** needed 2023–2030 just for AI
  infrastructure buildout — the AI boom runs on the doer pool it is supposedly replacing.
- Projected cost of unfilled trade positions: **$325.6B in lost GDP by 2030** across seven
  core trades.

## 10. INFRASTRUCTURE / MAINTENANCE

MEASURED pattern: unfilled maintenance-technician positions translate directly into
equipment downtime and maintenance backlog (BLS-linked industry reporting, Sept 2026).
Every automated system surveyed above (robots, terminals, haul trucks, drones) has a
maintenance tail staffed by the same shrinking trades pool. Automation does not remove the
maintenance dependency; it concentrates it on scarcer, higher-skill technicians.

---

## SYNTHESIS — the shared-node analysis

Automation's measured wins share a shape: **structured environment, private terrain,
repetitive task, validated envelope** (mining haul, warehouse tote transfer, corridor
trucking, drone photo capture). Its measured failures share the opposite shape: weather,
biological variability, mixed defects, density, exceptions, breakdown.

The doer is the shared node across every failure cell:

1. **Exception handling** — autonomy's edges are manned everywhere we looked.
2. **Kinesthetic judgment** — force, ripeness, structural feel; unmeasured and unautomated.
3. **The training supply chain** — robot competence is distilled human demonstration.
4. **Maintenance of the automation itself** — concentrated, not removed.
5. **The energy/logistics tail** — batteries, parts, charging: doer-staffed end to end.
6. **The retained skill the automation erodes** — supervised autonomy consumes the very
   capability it depends on for its exceptions (mining finding; closure-cost, instrument
   branch).

In the repo's terms: nominal automation channels are many; **effective** channels collapse
onto one shared node — the doer — because weather, parts, terrain, and exceptions are one
node with many faces. N_nominal keeps rising. N_eff is still 1.

## FALSIFIERS (registered, so this audit can be wrong on evidence, not vibes)

```
AUT-F1  Humanoid real-task success: claimed ~12% (Stanford/Fortune 2026)
        Refutes if: an independent, non-vendor field study shows >60%
        unassisted task success across mixed real environments by 2028
AUT-F2  Terminal productivity: automated −7..−15% vs conventional (McKinsey 2017)
        Refutes if: post-2024 automated terminals show sustained moves/hour
        parity or better at equal volume, third-party measured
AUT-F3  Corridor trucking: validated-envelope-only (weather pull-over, human
        recovery summoned)
        Refutes if: driverless operations validated in precipitation and
        winter conditions on public northern routes by 2028
AUT-F4  Harvest success: 76.1% mean, damage rate mostly unreported
        Refutes if: field-deployed harvesters exceed 90% success with
        published damage rates <2% on soft fruit by 2028
```
