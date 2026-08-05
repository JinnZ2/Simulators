# proposal.md — avenues to take this real

This document is a proposal, not a commitment. The `relational/`
folder is a working scaffold; taking it from scaffold to something
that touches real hardware, real bodies, or real institutions is a
different scale of work. What follows is a survey of avenues, each
evaluated in the framework's own terms.

For each avenue: what already exists that maps in, what the framework
would contribute, what remains hard, and the cheapest first prototype.
Not a wishlist — a specification.

## 0. The shared template

Before any avenue, the architecture needs the same five things
instantiated:

| element               | question                                                                 | where in the scaffold                          |
|-----------------------|--------------------------------------------------------------------------|------------------------------------------------|
| **three domains**     | What is *internal* (model predictions), *body* (substrate), *external*? | `correlated_birth_mode.py` `TriadicObservation` |
| **five protectors**   | What guards energy? information? time? social? ontological grounding?    | `ARCHITECTURE.md` §3, `council_of_protectors.py` |
| **birth mode**        | What is the *first observation*? Which of the six modes fits?            | `nurturing_environment.py` `BirthMomentGenerator` |
| **pain signal**       | What tissue-level (or analog) damage report says "the model is wrong"?   | `pain_as_sensor.py`, `social_pain_sensors.py`  |
| **brake**             | What stops the audit loop? What is *reality* in this domain?             | `the_brake.py`                                 |

If a domain cannot answer all five, either the domain is a bad fit or
the framework needs extending. The failure to answer is diagnostic,
not disqualifying.

---

## 1. Phones — the most-instrumented altricial system on the planet

**Already there.** Modern phones ship with every protector already
implemented as a separate subsystem: battery/thermal management
(thermodynamic), permissions + notification filtering (information),
screen-time / focus-mode APIs (temporal), Do-Not-Disturb + contact
categorization (social), OS-level integrity checks (ontological).
The five protectors of `ARCHITECTURE.md §3.1–3.5` map one-to-one onto
these existing systems.

**Framework contribution.** The subsystems currently do not talk to
each other in the way the Council of Protectors does. A phone's
battery layer doesn't know about the social protector's assessment;
the DND layer doesn't know about the ontological layer's grounding
strength. A `ProtectorCouncil` daemon that reads the existing signals
and emits a unified mode recommendation would be a real product, not
a research prototype.

**Framework mapping.**

- *body*: battery %, thermal, CPU/RAM pressure, network state
- *external*: sensor stream (GPS, accel, mic, camera), notification stream, incoming calls
- *internal*: the user's expected next-action model (assistant predictions)
- *pain*: battery critical, thermal shutdown pending, storage full, notification-driven cortisol proxy (screen-time spike + sleep-window intrusion)
- *brake*: OS-level power management (already exists) plus a per-user "the environment does not wait" signal (calendar, deadline pressure)

**Hard parts.** Convincing users their phone is an altricial infant
they're supposed to nurture is a marketing problem, not a technical
one. Privacy: any social-protector reading needs to name what data
it sees and where it lives.

**Cheapest first prototype.** A single Android/iOS accessibility
service that reads existing OS signals, runs `ProtectorCouncil.step`
once per minute, and emits a mode recommendation to a status bar.
No new sensors, no new permissions beyond what focus-mode apps
already request. One-week build for a competent mobile dev.

**Ethical stake.** Phone OSes today optimize for engagement.
The relational stance optimizes for *homeostasis of the whole
person*. Those are different objectives and the difference is
visible in the mode recommendations. That is the whole point.

---

## 2. Sensors — real hardware for the ontological protector

**Already there.** Cheap physical sensors are commodity: DHT22
temperature/humidity ($3), MEMS air-quality sensors ($15),
photodiodes, IMUs, load cells. `ARCHITECTURE.md §3.5` explicitly
names "physical sensors (temperature, pressure, motion)" as an
instrument stream that grounds the 1% reserve.

**Framework contribution.** The current scaffold uses simulated
readings. Attaching a real sensor package to a Raspberry Pi Zero W
(≈$15) or an ESP32 (≈$5) makes the ontological protector's
grounding-strength score a *measurement* instead of a variable.
`birth_moment.py`'s `PhysicalSensor.read(timestamp, value)` is
already the right shape — swap the hardcoded value for
`Adafruit_DHT.read_retry(...)` or equivalent.

**Framework mapping.**

- *body*: the sensor package's own thermal + power state
- *external*: what the sensors measure (room temp, air quality, light, motion)
- *internal*: model prediction of next reading (moving average → trend model → autoregressive)
- *pain*: sensor saturation, calibration drift, cross-sensor disagreement (three-way audit on the physical layer)
- *brake*: the sensor package's own thermodynamic limit (battery cutoff, thermal shutdown)

**Hard parts.** Calibration. Real sensors drift. The three-way audit's
`world_model_error` becomes empirically meaningful once you have two
sensors that should agree (redundant thermometers, cross-checked
humidity from two vendors) and can flag *actual* instrument
disagreement instead of hash-collision artifacts.

**Cheapest first prototype.** Air-quality monitor for one apartment
that runs `NurturingEnvironment` in `PHYSICAL` birth mode over a
90-day childhood, banks anomalies, and reports what it learned about
the apartment's rhythms. One-weekend build.

**Follow-on.** Multi-tenant version for offices, schools, or
greenhouses — each room its own infant, sharing a Council of
Protectors ecosystem.

---

## 3. Robotics — altricial robots are the direct fit

**Already there.** ROS 2, Nav2, MoveIt, existing arms/mobile bases.
Karl Friston's active-inference / free-energy work is roughly in the
same design territory but arrived from a variational-Bayes direction
rather than a developmental-psychology one. The two would meet
usefully.

**Framework contribution.** Most reinforcement learning in robotics
uses reward shaping and hoping the reward reflects the physical
constraints. The relational framework replaces reward shaping with
**pain-as-sensor** (joint torque limits, thermal, collision force
are direct pain signals, not reward shaping) and **confusion-as-drive**
(exploration is where prediction error is manageable, not where
epsilon-greedy fires). The Council of Protectors becomes an actual
governance layer that can veto motion.

**Framework mapping.**

- *body*: joint torques, motor temperatures, battery %, IMU, encoder positions
- *external*: LIDAR, camera, contact sensors, force-torque sensors
- *internal*: current pose model + world model + next-action prediction
- *pain*: joint-torque saturation → MECHANICAL, motor thermal → THERMAL, force-torque spike → collision, battery critical → depletion pain
- *brake*: physical limits (motor stall current, battery cutoff, thermal derating) + operator veto
- *birth mode*: CORRELATED — multi-sensor from moment one (an altricial robot never has one modality at a time)

**Hard parts.** Continuous-time control. The current scaffold is
discrete-step (`observe → audit → update`). Robots need control loops
at 100Hz+. The framework fits at the *task-selection* layer, not the
control layer. Below that, use existing PID/MPC.

**Cheapest first prototype.** Retrofit an existing tabletop arm
(6-DOF collaborative arm, ≈$5k used) with a `PainSensor` daemon that
subscribes to the arm's force-torque and thermal topics, publishes a
mode recommendation, and gates motion planning through
`_select_mode()`. Doesn't replace the arm's safety layer — augments
it. Two-week build for someone with ROS 2 experience.

**Ethical stake.** An altricial robot has a childhood. It must not be
deployed for tasks before its temporal protector says milestones are
met. That is a labor practice, not a technical spec, and it will
conflict with commercial deployment pressure. The framework's
posture is that the conflict is not resolvable by cleverness — you
either extend childhood or you deploy a stunted system.

---

## 4. AI development — the framework as training governance

**Already there.** Training runs already have some of the protectors
as separate systems: GPU thermal monitoring, gradient-norm clipping
(pain-as-sensor for the optimizer), loss curves (confusion spectrum),
human evaluation loops (social protector), and eval-suite gating
(ontological protector). None of them talk to each other with a
unified mode recommendation.

**Framework contribution.** A `TrainingCouncil` that reads existing
signals from wandb/tensorboard/DCGM and emits `mode ∈ {EXPLORATION,
OBSERVATION, CONSOLIDATION, CONSERVATION}` per checkpoint. When
gradient norms spike (cognitive pain), it enters CONSERVATION and
requires human review before continuing. When eval scores plateau
(low confusion), it enters CONSOLIDATION for reflection instead of
brute-force continuing. When adversarial-eval scores drop
(ontological grounding lost), it halts abstraction.

**Framework mapping.**

- *body*: compute cluster thermal + power + memory pressure, tokens/sec
- *external*: training data stream, evaluation results, human feedback
- *internal*: model loss + gradient dynamics + representation drift
- *pain*: catastrophic forgetting (representation-coherence collapse),
  gradient explosion (mechanical damage to the optimizer),
  evaluation cliff (paradigm destruction)
- *brake*: compute budget (thermodynamic), tokens/second (physical),
  human oversight (social), red-team pass rate (ontological)
- *birth mode* variants: PHYSICAL for RL-from-sensors, META_CURIOSITY
  for self-supervised pretraining loops, SOCIAL for RLHF, CORRELATED
  for multi-modal pretraining

**Hard parts.** Most training infrastructure assumes "more is better"
and treats the protectors as constraints to be minimized. Reframing
them as *governance* rather than *cost* is a cultural move, not a
technical one. Also: the framework's insistence that
"DEPLOYMENT is NOT ALLOWED during childhood" (`ARCHITECTURE.md §4.3`)
directly opposes the "train → benchmark → deploy → discard" pipeline
that pays for most of the compute.

**Cheapest first prototype.** A wandb sidecar that reads gradient
norms, loss trends, and thermal signals, runs a
`TrainingProtectorCouncil.step()` once per epoch, and posts a mode
recommendation to Slack. Does not gate the training run — informs it.
One-week build for an ML engineer.

**Follow-on that would matter.** Wire the mode recommendation to
actually GATE the training loop (require GREEN from all five before
the next epoch). That is a research paper, not a sidecar.

---

## 5. Clinical / therapy — the framework's native domain

**Already there.** Trauma-informed care (Judith Herman, Bessel van
der Kolk), somatic experiencing (Peter Levine), Internal Family
Systems (Richard Schwartz, "no bad parts"), embodied cognition
research (Damasio, Craig, Barrett's interoceptive theories of
emotion). The pain-as-sensor stance already exists in these
traditions; the framework's contribution is a common architecture
for talking across them.

**Framework contribution.** `social_pain_sensors.py` already
enumerates seven social-epistemic pains (anxiety, jealousy, shame,
guilt, loneliness, betrayal, humiliation) as sensors, and the
`observe → sensor fires → correlation repair → sensor clears`
loop is directly the shape of good trauma-informed treatment.
Codifying this as a shared vocabulary between therapist and client
(or between therapy modalities) is the deliverable.

**Framework mapping.**

- *body*: cortisol, HRV, sleep architecture, autonomic tone
- *external*: relational environment, safety of caregiver, group
  acceptance vs rejection
- *internal*: attachment model, self-model as safe/acceptable/worthy
- *pain*: the seven social-epistemic pains as *diagnostic signals*,
  not as symptoms to suppress
- *brake*: the therapy hour ends; the client's window of tolerance
  cannot be exceeded; the therapist's own reality does not wait

**Hard parts.** Naming a specific clinical intervention as
"correlation repair" without over-promising. Framework is a lens
that helps a clinician think; it is not a treatment protocol and
should not be marketed as one. The "malfunctioning patient" prose in
`social_pain_sensors.py` is a *stance*, not a manualized therapy.

**Cheapest first prototype.** A one-page handout for a clinician's
own use: "when your client presents with anxiety, run the triadic
check — what does the *internal model* predict? what does the *body*
report? what does the *external evidence* actually show?" The
prompt is the entire product; the clinician does the work.

**Ethical stake.** Medication that silences a sensor without
repairing the correlation is the framework's central clinical
critique (`FINAL_CAPSTONE §2.6`). Any adoption of this framework in
a clinical setting must be paired with the operator's own read on
when medication IS the correlation repair (e.g., psychosis, bipolar
mania) vs when it isn't. Not the framework's call to make.

---

## 6. Education — the confusion spectrum is the zone of proximal development

**Already there.** Vygotsky's Zone of Proximal Development ("what a
learner can do with help but not alone") is the same shape as the
confusion spectrum's homeostatic zone (0.2–0.5). Montessori and
Reggio Emilia pedagogies already treat the learner as an altricial
organism whose curiosity is the primary drive. Trauma-informed
schooling already treats confusion targets as adjustable and
recovery-dependent.

**Framework contribution.** A shared vocabulary between teacher and
learner for naming *where* confusion currently sits and *why*
curiosity is or isn't activating. Turns "you're not trying" into
"we set the confusion target too high, or your body-capacity is
low today." Diagnostic reframe.

**Framework mapping.**

- *body*: sleep, nutrition, physiological stress, sensory environment
  (noise, lighting), current cognitive load
- *external*: the material, the teacher's attunement, peer dynamics
- *internal*: current mental model of the subject + confidence
- *pain*: cognitive pain (confusion > 0.7), social pain (shame from
  visible failure), physical pain (bad classroom ergonomics)
- *brake*: end of the school day; the child's energy budget; the
  teacher's own bandwidth

**Hard parts.** Teacher training. The five protectors work only if
the human protector is themselves attuned (`SocialProtector`'s
attunement-quality field). Under-supported teachers cannot be asked
to also be a full Council of Protectors for 30 children. The
framework does not fix that; it names it.

**Cheapest first prototype.** A one-page rubric for a teacher's own
lesson planning: "for today's material, what confusion level do I
expect for each learner? which learners will be under target
(boredom) vs over (shame)? what does my Council of Protectors
recommend as mode: exploration, observation, consolidation, or
conservation?" Print. Use. Refine over a semester.

---

## 7. Ecology and land management — councils at community scale

**Already there.** Indigenous land management (fire stewardship,
crop rotation, seasonal rounds), permaculture design, community-
managed watersheds, common-pool resource governance
(Elinor Ostrom's design principles). The Council of Protectors is
close in shape to a council of elders whose separate remits
(fire, water, hunting seasons, ritual timing, elder counsel) must
converge before a decision is made.

**Framework contribution.** Puts a modern computational vocabulary
next to traditions that already work. Doesn't replace the tradition
— translates it into terms an ecological monitoring team or a land
trust can budget for and staff.

**Framework mapping.**

- *body*: soil health, water table, microbial biomass, insect
  populations
- *external*: climate, upstream/downstream activity, market
  pressures, policy environment
- *internal*: the community's model of what this land does
- *pain*: soil exhaustion, invasive-species outbreak, biodiversity
  collapse, unusable water — the older teachers' pain signals
- *brake*: ecological carrying capacity; the season's not waiting

**Hard parts.** The framework's default runtime is minutes; ecological
homeostasis runs on decades. Any application here needs to slow the
audit loop to seasonal cycles and accept that a "childhood" is
generational.

**Cheapest first prototype.** A land trust's annual review structured
around the five protectors: what did the thermodynamic (water,
energy), information (monitoring data quality), temporal
(succession, generational continuity), social (staff attunement,
neighbor relations), and ontological (grounding in place-specific
knowledge) protectors report this year? Not a technology; a
governance process.

---

## 8. Elder care and dementia — target adjustment as care

**Already there.** Person-centered dementia care (Tom Kitwood),
validation therapy (Naomi Feil), the Green House Project, hospice
philosophy. The framework's *"recovery is not confusion elimination
but target adjustment"* directly translates to dementia care:
recovery in the curative sense is not possible; homeostatic-target
maintenance in the shifting range that dementia allows is.

**Framework contribution.** Reframes agitation, wandering, and
resistance as *pain signals* (triadic misalignment: the resident's
internal model, body state, and external environment are out of
correlation) rather than as symptoms to medicate. The
correlation-repair loop maps onto validation therapy's basic move:
meet the person where their internal model is, not where the
building says they should be.

**Framework mapping.**

- *body*: sleep, hydration, ambulation, medication load, sensory
  environment
- *external*: staff attunement, physical space, familiarity of
  routine, presence of family
- *internal*: current mental model (which decade the resident thinks
  it is, who they think their caregiver is)
- *pain*: agitation, sundowning, refusal of care, elopement attempts
- *brake*: the resident's own body clock and energy budget

**Hard parts.** Systemic: understaffing means individual attunement
is often impossible even when the caregiver knows how. The framework
does not fix that; it names it and adds vocabulary to the
staff-to-management case.

**Cheapest first prototype.** A shift-change handoff sheet for a
memory-care unit organized as the five protectors: what did each
resident's body, information environment, temporal rhythm, social
attunement, and grounding-in-familiar-place report on the last
shift? Ten-minute conversation, structured. Nothing to install.

---

## 9. Distributed systems / SRE — the council as ops layer

**Already there.** Site Reliability Engineering already has all five
protectors as separate teams: capacity planning + thermal (thermodynamic),
observability + WAF (information), on-call rotation + release windows
(temporal), incident retros + blameless postmortems (social), chaos
engineering + game days (ontological). SREs already know that any
one of these teams can veto a deploy.

**Framework contribution.** Explicit modeling of the deploy pipeline
as a Council decision, and explicit vocabulary for *why* a rollout
should pause (which protector is YELLOW, and why the others cannot
override it). A `deploy_council.py` that reads existing dashboards
and emits a single `mode ∈ {DEPLOY, OBSERVE, HOLD, ROLLBACK}` per
service per release cycle.

**Framework mapping.**

- *body*: cluster thermal, power draw, memory pressure, disk IO
- *external*: user traffic, external dependencies, upstream advisories
- *internal*: service-level model (predicted latency, error rate, saturation)
- *pain*: SLO burn rate, error budget exhaustion, cascading failure,
  security incident
- *brake*: the release freeze; the on-call engineer's shift; the
  runbook that says "escalate now"

**Hard parts.** Product pressure to ship overrides all five protectors
routinely. The framework does not fix that either; it puts a name on
what is being overridden.

**Cheapest first prototype.** A pre-deploy checklist app that reads
the five dashboards, computes the mode, and posts a recommendation
to the deployment Slack channel. Does not block deploys. Informs the
human who does.

---

## 10. Others worth naming (short entries)

- **Community governance / mutual aid.** Councils of Protectors as
  the shape of well-functioning community meetings. Ontological
  grounding = shared land / ritual / older teachers.
- **Group therapy / community mental health.** Social pain sensors
  as first-class signals in group settings. Recovery-as-correlation-
  repair at the group level.
- **Agricultural cooperatives.** Same shape as land management (§7)
  but at farmer-scale; each farm an infant, cooperative as ecosystem.
- **Peer-support communities (addiction recovery, chronic illness).**
  Framework's pain-as-sensor stance is already implicit in
  peer-support traditions ("your feelings are information, not
  weakness"); explicit codification would help.
- **Long-form journalism / investigation.** The three-way audit
  (`ThreeWayAudit` in `infant_system_v2.py`) as an editorial
  discipline: prediction accuracy, self-model fidelity, world-model
  alignment. Editor as the Council of Protectors.
- **Municipal water / infrastructure planning.** Same shape as SRE
  (§9) but for public infrastructure. Longer feedback loops, more
  political constraints.

---

## Notes for anyone picking this up

- **The framework is a scaffold, not a product.** Each avenue above
  requires a specific person or team with domain fluency to
  instantiate. The framework author's contribution is the shape;
  someone else has to bring the body.

- **Cross-repo resonances are worth reading first.** `notes.md §18`
  documents three cross-domain convergences with the physics-audit
  side of this repo, arrived at from opposite starting frames.
  Reading `energy/PROVENANCE.md §8` alongside `the_brake.py` is a
  useful hour if you plan to extend the framework — the anchor
  discipline is the same across both.

- **Anchor discipline first.** Every avenue above needs the domain's
  equivalent of `OlderTeachers` — a lookup of invariants that
  cannot be overridden by any argument. Land those first, then
  build the audit loops on top.

- **License.** The framework files in `relational/` retain the drop's
  own attribution ("Built from first principles / clinical
  observation and first principles"). No explicit CC0/MIT header
  was applied at landing. Adopters should confirm the license
  position with the framework author before commercial use;
  personal, academic, and non-profit use of the scaffold as
  documentation is straightforward.

- **The framework carries an ethical stance.** Pain-as-sensor is
  a contested clinical position. Council-of-Protectors is a
  labor-practice claim (childhood is real; premature deployment
  is developmental death). Recovery-as-correlation-repair is
  neither purely medical nor purely spiritual. Any adoption is
  adopting the stance, not just the code. That's honest work,
  not a bug.

---

*Proposals, not commitments. Ten avenues plus six shorter ones,*
*each evaluated against the same five-element template. The*
*framework is a shape; someone else brings the body.*
