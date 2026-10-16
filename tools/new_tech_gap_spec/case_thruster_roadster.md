# WORKED CASE 1: THRUSTER-EQUIPPED ROAD CAR

Instrument: `spec.md`. This case applies the spec to a road car offered
with cold-gas thrusters that can lift it off the road surface. It is
not a finding about the product, its maker or its buyers.

Status tags: OBSERVED / DERIVED / PROPOSED / UNMEASURED.
Citation states: VERIFIED / CORRECTED / NOT FOUND (checked 2026-10-16,
through search-result text; primary pages were not opened).

---

## 0. REPORTED FACTS AND CITATION CHECK

| # | Reported line | State | What the sources say |
|---|---|---|---|
| R1 | Unveiled 2026-10-16 | CORRECTED | Unveiled 2026-10-15 at the SpaceX McGregor TX test site, livestreamed; moved from Oct 1 for weather [1][2][3] |
| R2 | SpaceX-derived cold-gas thrusters | VERIFIED | Reported as cold-gas thrusters; 10 thrusters on the demo car [1][2] |
| R3 | Short hover / hop | VERIFIED IN PART | Demo showed a ramp launch, a flip and a landing; no sustained hover shown [1][3] |
| R4 | Optional upgrade | VERIFIED | Trims reported as Performance ($50k reservation), Thrust ($250k reservation), Rocket (invite only, no price) [2] |
| R5 | Not road-approved | VERIFIED (one report) | Stated in one report; not confirmed by a regulator [2] |
| R6 | Production ~2028 | VERIFIED as a statement | A stated target, not a confirmed delivery date; one other secondary source (not listed here) gives 2H 2027 [2] |
| R7 | ~10,000 psi COPV tanks in rear-seat space | CORRECTED / CONFLICTING | The ~10,000 psi COPV in the rear-seat space is the 2018 option description [4]. The 2026 demo car is reported with ~600 L (159 gal) of rechargeable compressed air [3]; one secondary source gives ~150 L at 6,000-10,000 psi. Pressure of the 2026 tanks not confirmed |
| R8 | Spectators held back for noise | NOT FOUND | No source located for this line |

Sources:
1. https://theevreport.com/tesla-roadster-unveil-spacex-cold-gas-thrusters
2. https://thenextweb.com/news/tesla-roadster-reveal-thrusters-2028
3. https://www.foxbusiness.com/technology/teslas-new-roadster-makes-flying-debut-hitting-60-mph-under-second
4. electrek.co, 2018-06-10, SpaceX option package description (2018 statement, carried)

[DERIVED] Everything below treats the thruster function as: stored
compressed gas, released through nozzles, able to lift the car off the
road for a short time. Pressure, mass flow and hop height are
UNMEASURED on the public record.

---

## 1. HAZARDS AT THE VEHICLE

H1  [DERIVED] Hopping: a road vehicle leaves its contact patch, so
    braking, steering and stability control stop acting until landing.
H2  [UNMEASURED] COPV puncture: stored energy of a carbon-overwrapped
    pressure vessel in a crash or fire. Pressure not confirmed (R7).
H3  [DERIVED] Crash with thrust armed: a collision can trigger or
    prevent release; neither case is described in any source located.
H4  [UNMEASURED] Plume zones: the area around and below each nozzle
    where gas velocity throws debris or injures a person. Size unknown.

### 1.1 Traffic-jam case

[PROPOSED as the baseline scenario, per spec S4]

- Simultaneous hops: several owners hop out of one stopped queue.
- Landing gap closes mid-air: the gap in traffic taken at launch is
  filled before landing.
- Plume-driven debris: gravel, glass and road litter thrown into
  adjacent cars and people.
- Startle secondary crashes: drivers around the event brake or swerve.
- Copycat cascade: one hop seen live invites the next.
- Gate and fence bypass: docks, secure yards, military gates, rail
  crossings and toll barriers assume a vehicle stays on the ground.

---

## 2. AUTOMATION (INTERFACE 5)

A1  [UNMEASURED] AV and driver-assist perception has no reported
    training on airborne road vehicles. Two failure directions:
    - miss: the object is not classified and is driven under or into;
    - phantom brake: hard braking with a loaded rig behind.
A2  [DERIVED] Gaming: hopping in front of an AV to provoke a brake
    chain is cheap and repeatable.
A3  [OBSERVED, carried] An 80,000 lb loaded tractor-trailer needs far
    more distance to stop than a car; it cannot answer a sudden brake
    chain. Stopping distance figures are carried, not re-measured here.

### 2.1 DOT design controls (all PROPOSED)

- Thrust as a separate drive mode, selected and logged.
- Geofence: thrust disabled on public roads by default.
- Activation event log: time, location, duration, occupant.
- AV testing against airborne objects before thrust is allowed near
  automated traffic.
- Hazmat-style exterior placard for a vehicle carrying a high-pressure
  vessel.

---

## 3. INFRASTRUCTURE (INTERFACE 1)

I1  [UNMEASURED] Clearance: overpasses, sign gantries, bridge decks,
    parking structures, toll plazas and weigh stations are designed for
    vehicles at grade.
I2  [UNMEASURED] Landing loads on bridge decks and parking-structure
    slabs.

### 3.1 Roadbed and subsurface

All UNMEASURED:
- Plume and landing effects tested separately on concrete, asphalt and
  dirt/gravel.
- Embedded inductive loops and weigh-in-motion strips, and their
  sealant, under jet impingement (lift, scour).
- Subbase pumping from repeated pressure pulses.

Adjacent literatures to start from:
- [OBSERVED, carried] FAA jet-blast guidance for airport pavement.
- [OBSERVED, carried] Harrier/VTOL pad design.
- [OBSERVED, carried] NASA plume-surface interaction work.

[PROPOSED] Highway cost allocation studies assign damage per axle load.
A thrust damage factor SHALL be added before any thrust fee is set.

### 3.2 Underground

All UNMEASURED:
- Tunnels and voids under roads: transit and utility tunnels (New York,
  Los Angeles, Duluth), lava tubes, karst, paved-over streetcar
  infrastructure.

Records sources to search: transit maps, Sanborn fire-insurance maps,
municipal archives, geological survey void and karst maps.

[PROPOSED] Ground-penetrating radar survey of any corridor before it is
used as a hover lane.

---

## 4. USERS (INTERFACE 3, 4)

U1  [DERIVED] The buyer of a $250k thrust option is not the commuter
    the road rules were written for; the purchase is partly for the
    display.
U2  [PROPOSED] Design for deliberate misuse as the baseline (spec S4).
U3  [DERIVED] Stunt incentive: hops produce video, and video produces
    reach.
U4  [DERIVED] A recording mandate (5.1) doubles as content production.
U5  [PROPOSED] Surface-detection limit: thrust inhibited unless sensors
    confirm a permitted surface and clear surroundings.

### 4.1 Recording

[PROPOSED] Interior and exterior recording tied to thrust activation.
Open branch, no pick: record during thrust only (privacy-preserving,
misses the lead-up) vs continuous (complete, a standing surveillance
record).

---

## 5. FAA / DOT SEAM (INTERFACE 2, 8, 14)

J1  [DERIVED] Low hover between the road surface and navigable airspace
    is not defined as either a vehicle on a highway or an aircraft.
J2  [OBSERVED, carried] Earlier roadable aircraft (Terrafugia
    Transition, Samson Switchblade) pursued dual certification and
    switched modes at an airport. A thrust road car erases the airport
    mode switch: the transition happens in traffic.
J3  Options, no pick (all PROPOSED):
    - threshold rule (height, duration) above which FAA governs;
    - joint NHTSA/FAA rulemaking;
    - a new vehicle category;
    - a designated lead agency.
J4  [DERIVED] Enforcement gap: local police enforce traffic law, FAA
    enforces aviation law, and neither patrols the band in between.

### 5.1 Local authority

- [DERIVED] Localities absorb the cost of road damage, response and
  cleanup, which predicts local bans, enforced by geofence.
- [OBSERVED, carried] Precedents for local routing and load control:
  truck routes, posted weight limits, seasonal frost laws.
- [PROPOSED] Per-event location fee. Precedents: IFTA fuel-tax
  apportionment and Oregon's OReGO road-usage charge. Tokenized
  settlement is PROPOSED. The fee is blocked on the UNMEASURED damage
  factor (3.1).
- [PROPOSED] Interim shared hover lanes with in-road sensors, with
  sunset (spec D4).

---

## 6. LIABILITY AND MEDICAL (INTERFACE 3, 4, 11, 13)

- [DERIVED] Expected injury claims: eye injury, projectile injury,
  hearing damage to bystanders.
- [PROPOSED] Claims tied to the thrust log (2.1): the log is evidence.
- [PROPOSED] Responders need a visible, registered placard to know a
  pressure vessel is on scene.

Law table (spec 1.13), first pass:

| Body of law | State |
|---|---|
| tort / product | AMBIGUOUS (roadway vs aviation duty of care) |
| criminal | AMBIGUOUS (reckless driving vs unlawful flight) |
| privacy / wiretap | AMBIGUOUS (recording mandate, 4.1) |
| contract | FITS |
| insurance | AMBIGUOUS (auto policy vs aviation exclusion) |
| property | AMBIGUOUS (low overflight of private land) |
| 4th Amendment | AMBIGUOUS (access to thrust and video logs) |

[DERIVED] n_ambiguous = 6 of 7 on this first pass (a reading, not a
measurement).

---

## 7. LICENSING (PROPOSED)

- A Class C/D endorsement for thrust, modeled on the CDL hazmat (H)
  endorsement plus the air-brake restriction plus the motorcycle
  endorsement structure.
- The car will not arm thrust without a valid endorsement read at
  start.
- Background check, renewal, suspension, interstate compact.

---

## 8. REPAIR AND MAINTENANCE (INTERFACE 10)

- [PROPOSED] COPV hydrostatic test and recertification interval.
- [PROPOSED] Mandatory post-impact inspection of vessel and mounts.
- [DERIVED] No ASE certification category covers compressed-gas
  vehicle thrust systems; a shop certification is needed.
- [DERIVED] DIY and aftermarket work moves the vehicle outside the
  declared envelope (spec D5).
- [OBSERVED, carried] EV high-voltage technician certification is a
  template for a new hazard category in shops.

---

## 9. OPEN GAPS

- [DERIVED] Thrust-log tamper-proofing: the log carries enforcement,
  claims and fees, so it is a single point of failure (spec S3).
  [PROPOSED] An ELD-style tamper-evident standard.
- [UNMEASURED] Pavement damage factor.
- [UNMEASURED] AV retrofit cost for airborne-object perception.
- [UNMEASURED] Subsurface response.
- [DERIVED] Manufacturer liability for thrust-mode incidents is
  unassigned.
- [DERIVED] Aftermarket thrust kits for other cars.
- [DERIVED] Interstate uniformity.
- [DERIVED] No consumer vehicle has been placed in a hazmat class
  before.
