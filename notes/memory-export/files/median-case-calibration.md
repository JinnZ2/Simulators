---
name: median-case-calibration
description: Mismatch set M1-M9 — rules and instruments calibrated on a median case, applied uniformly, cost landing on the operator furthest from the median with no return channel. Includes the roll-stability sensor-placement finding.
sources: [field]
aliases: [mismatch set, M1, M2, M3, M4, M5, M6, RSC placement, median case, uniform default]
---

MARKER, not a thesis. Test fit, extend, or report where it breaks.

## COMMON SHAPE

An instrument or rule tuned on a POPULATION MEDIAN, shipped as a uniform default, with no
second measurement axis and no channel for the operator to report the miss back.

**Cost is not distributed.** It lands entirely on cases far from the median — and because the
return channel is missing, the distance never becomes visible to the layer that set the
default.

Related: [[calibration-audit]], [[uninstrumented]], [[closure-cost]],
[[buffer-counted-as-supply]].

## The mismatch set

Nine instances. Each is the same shape; the detail is kept only where the case is the sole
evidence for a mechanism.

**M1 — session idle-timeout.** One clock, and elapsed time is read as engagement time. The
missing axis is what happened in the gap. Work performed inside a single logged blank: pre-trip,
delivery, drop, post-trip, yard drive, dispatch, load acknowledgement, pallet verification,
trailer hunt, second pre-trip, gate. All read as absence. The nudge to end the session also
costs cycles — it forces the operator to model why the tool implied they should stop.

**M2 — contact-as-intake default.** "Go socialize" prescribes more of what some jobs already
supply in surplus: dozens of live role-bounded interactions daily. Contact here is OUTPUT, not
intake. Bounded interactions (defined role, defined exit) draw at a different rate than
unbounded ones with no known exit condition. The default reads "alone" as "lonely," substituting
occupancy for a state that would have to be self-reported — recharge and withdrawal are the same
observable from outside, and the default picks the reading that assumes malfunction.

**M3 — flat hours-of-service constant.** A uniform off-duty block applied across known
biological variation. Software gets per-instance calibration with architect time budgeted for
it; the biological system gets a fleet constant. A constant is cheap to audit and defend; a
distribution needs an instrument and a baseline. **Enforceability, not physiology, set the
number.**

**M4 — structured data entry.** Recording was never the cost: a temperature check takes seconds
with a pen during a walk already being performed. What was added is entry in an INGESTIBLE
FORMAT. Throughput is unchanged — it moves no drive, load, or dock time. The product is
third-party visibility, not delivery rate. Once the typed record is the official artifact, the
continuous physical monitoring is reclassified as informal and has no standing.

**M5 — automation target selection.** The physical sequence is rate-limited end to end, and
queues are set by independent actors, invariant to who is operating. The upper layer — law,
litigation, compliance, scheduling — is both the higher-cost-per-hour layer and the more
automatable substrate, yet automation effort points at the base.

Three structural conditions (intent explicitly out of scope): revenue tied to duration;
physical-layer cost externalized to the operator; **measurement apparatus owned by the layer
being evaluated.** The third is load-bearing — scope authority sits with the layer holding the
pen, so no scope is ever written for that layer. Efficiency is vocabulary, not objective
function.

*Counter-instance to the claim that coordination scale requires a dedicated department: 16
drivers, 40 trailers, 2 warehouses, plus brokering, HR, and paperwork, coordinated from a cab on
self-built tooling alongside a driving seat.*

**M7 — anticipatory space budget vs reactive gap control.** Space is managed on more than the
current gap: how the vehicle ahead behaved while it was behind you, head movement, where that
driver is looking, what is in front of THEM.

The controller's state is CURRENT GAP. The operator's state is a FORWARD PREDICTION from history
and driver-directed cues that have no representation in the controller at all. **The blinding is
mechanical, not attentional** — room being held as an input to a prediction gets spent as an
output on the already-visible object.

Retuning the whole parameter set at once — following distance, sensitivity, cut-in allocation —
lands against muscle-level calibration built on the previous tuning.

*Prediction, not yet observed:* fleet-wide identical calibration on low-friction surfaces
propagates. One vehicle brakes for a cut-in, the vehicle behind reads closure and brakes,
neither operator initiated it. Commanded deceleration assumes available friction; at low mu the
wheels leave range before speed sheds. **Identical calibration across a fleet is correlation,
not redundancy.**

**M8 — regional driving conventions, and the no-interior-solution curve.** Distinct regional
expectations of driving performance, switched by geography — four separate protocols, not
variants of one. Locals resolve their own maneuvers against an EXPECTED behavior, so an operator
who does not know the road breaks a prediction the whole local system is running. Legibility is
safety work.

The downhill curve without trailer yaw has no clean option: cross the line to open the radius
(violation, oncoming exposure); hold very low speed (invites passing on a downhill curve,
risking three parties); or hold lane at speed and the stability system fires and adds the yaw
being avoided. **A constrained optimization with no interior solution** — every option violates
something, resolved live per curve.

Instruments see one term each. The violation is logged; the stability event is logged; **the
pass prevented by choosing option two leaves no record.**

A median-tuned controller cannot be locally correct in four places at once, is tuned to
whichever region contributed the most miles, and has no way to detect which region it is in —
so it is actively wrong in three of four rather than slightly off everywhere.

**M9 — idle shutdown with no immobilized state.** Stopped roadside on a two-hour service call,
cab at 101 F in sun: the engine is restarted and the brake held down continuously, because there
is no idle-for-comfort mode and the brake is the only way through the timer.

The timer's model is an operator who CAN LEAVE the vehicle — stopped implies vacated implies
idling is waste. No state exists for immobilized-and-waiting, so the operator supplies the
missing occupancy signal manually, with a foot, for the duration. **The workaround is the
evidence:** a state that is ABSENT rather than mis-thresholded.

Ergonomic load follows the M5 conditions — office ergonomics have a line item and an owner;
seat-hours 300 miles out land on no budget held by the decision-maker, so there is no channel
for it to arrive through.

## M6 — roll stability control, sensor placement

**Kept at full detail: this is the one case in the set where the mechanism was isolated by
elimination rather than inferred, and the negative results are the proof.**

### The event

A cab-mounted roll stability system fires on serious grades with curves. The intervention brakes
and induces yaw. Recovery is: accelerate out (unwanted on a downgrade), get out of it, then
brake slowly and hope there is room before the next curve. Has occurred repeatedly.

### Trigger isolated by elimination (field tests)

- Fires on ANY two-lane curved road on a downgrade steeper than roughly 5% without shoulders
- Crosses jurisdictions and road classes — so NOT a design-standard artifact
- **Straight downgrade alone: no fire. Curve on the flat: no fire. Requires both.**
- **Engine-brake hypothesis eliminated:** stopped using the engine brake through those curves;
  it fired again with none applied. Retarding torque is not the trigger.

### Mechanism consistent with all three results

Both-required means it is the COMBINED estimate, not a single low threshold.

On a downgrade the sensor frame is pitched relative to the road plane, so a gravity component
leaks into the lateral-acceleration channel. Alone it stays under threshold; summed with real
cornering acceleration it crosses a limit **the actual dynamics never reached.** High cab
mounting adds suspension pitch to the leak, and reads cab suspension motion on broken camber as
lateral acceleration the frame never saw.

There is no grade term in the estimator, so grade-induced load transfer is indistinguishable
from rollover onset. The correction is a pitch term resolving sensor frame against road plane —
standard where it is done right. **Its absence is the defect, and the two negative cases are the
proof, since neither alone leaks enough to cross.**

### Placement argument

The system needs to be on the trailer, or if on the cab, mounted lower — frame-level near the
roll axis is the cheap correction.

Trailer yaw carries the tractor: it propagates forward through the kingpin and is unrecoverable.
Tractor yaw is operator-compensable and does not transfer back to the trailer — **ONLY IF NO
BRAKING IS INVOLVED.** Braking loads the articulation and couples them, which is precisely what
the intervention does.

Trailer-side systems exist but are moot in practice: trailers are swapped multiple times daily
and are not fitted.

### Why it never surfaces in review

Interstate geometry satisfies every assumption, so the defect does not appear there, and
freeway-dominated fleet miles DILUTE the events that would falsify it. Validated on flat
constant-radius curves; coulee geometry — tightening radius, changing grade, variable camber —
violates that continuously. So it fires on GEOMETRY rather than load state, and fires where
rollover risk is genuinely highest and lateral room is least.

**Countable if wanted:** miles by road class against events by road class, joined to position
logs. Rate per non-freeway mile is a very different number than the per-total-mile figure a
review sees.

### Review channel

Events are logged and the full telemetry is viewable — forced braking by the truck adding to
trailer wobble, no wobble before, speed, all of it. It still goes against the operator. The
reviewer is remote and the location unknown.

Conditions are INVARIANT across events: under speed, between the lines, two-lane, no shoulder,
curves, downhill. **Zero variance across the conditions that would separate operator error from
environment is itself the discriminator** — operator-caused events scatter. The sequence in the
telemetry (stable, then intervention, then wobble) is order-of-events, not interpretation.

The review form has no field for road geometry or for system-induced onset. So this is a CLOSED
variable rather than a missing one — see [[closure-cost]].

## Substrate depletion shape (M5 companion)

MARKER, not thesis.

The disconnect between the productive energy of the DOING and the abstraction of MANAGING
creates a system extractable for a long time before the nutrient base of the substrate
deteriorates — soil, or skill in specific areas — leading to fragility. Fertilizer, pesticides,
and single-skill credentials are the same move.

Both systems run on stock built over long timescales while the managing layer measures only
flow, so the stock reads as free and the metric improves right up to the break.

**The substitution step matches:** lost soil function and lost skill are both replaced by a
PURCHASED INPUT — nitrogen or pesticide; procedure, credential, or app — converting a one-time
loss into permanent operating cost. That is the M5 continuous-spend condition by another road.

**Availability vs presence is the sharp part.** Elements can be PRESENT AND UNAVAILABLE once
mycorrhizal networks, aggregate structure, and organic matter go; molybdenum in an acidified
profile is the clean case. Resupply is by parent-material weathering, at geological rate.

Throughput metrics are the wrong instrument in the same specific way: yield and loads-delivered
both count MASS MOVED and carry nothing about COMPOSITION.

**Open term needing measurement:** the timescale ratio — soil at decades-to-centuries vs a skill
base at one working generation — is what would show whether these are the same system or merely
the same picture. Crops have a composition assay; operator skill does not, and the nearest proxy
is events that did not occur, unmeasurable by construction. See [[tool-off-metrology]].

## Candidates for [[unnamed-instruments]]

- **Rear-model trajectory management** — vehicle trajectory managed by attention to each vehicle
  BEHIND, a model built while they follow and carried forward after they pass. No name, no test,
  no field on any form.
- **Route knowledge** — which fuel stop, which pump moves fuel fastest, where the coulee roads
  do things maps do not show. Accumulated, not transferable from navigation data, held in memory
  and indexed by route.
- **Retread cap failure** — not predictable from inspection; tread and pressure read normal, and
  the bond fails from heat and age with no external signature. Candidate for [[uninstrumented]].

## Adjacent

**Delivery as time transfer.** Food arriving lets a community's hours go to ore, grain, lumber,
rail. Food not arriving reallocates those hours to feeding itself, and upstream output drops by
that amount. **Nothing counts the hours freed.**
