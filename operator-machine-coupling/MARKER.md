# RESEARCH GAP — operator-machine coupling as a measured variable

CC0. Public domain. No attribution wanted or needed.

Posted as a gap, not a finding. Everything below is either
observation, an existing institutional practice, or a proposed
measurement. Nothing here is a result.

---

## THE VARIABLE THAT IS NOT MEASURED

Machine operation is currently accounted for as: operator (with
credential and total experience) applied to machine (with class,
model, maintenance interval).

Missing: the coupling between a specific operator and a specific
unit. Not the machine class. The individual machine.

Operators who couple report reading the specific unit — sound,
vibration, resistance, feel — and adapting to what that unit needs
rather than running a generic model of the machine class. Different
units of the same model behave differently. Same airframe on floats
is a different machine. Same model chainsaw is a different machine.

This capacity is acknowledged informally everywhere and measured
nowhere.

---

## WHY IT MATTERS FOR CLASSIFICATION

### Operator error vs coupling failure

Current incident taxonomies have no bin for coupling failure, so
those events record as operator error. The two have different
signatures:

    operator error      wrong action, correctly executed
    coupling failure    correct action, executed against the
                        wrong machine model

Discriminator: coupling failure should correlate with
time-on-that-specific-unit, NOT with time-in-role. It should drop
sharply after familiarization with the individual machine while
total experience stays flat.

If this is right, some fraction of the operator-error category is
misattributed, and the remedy differs — assignment stability rather
than retraining or discipline.

### Procedure-following as the decoupling mechanism

A procedure runs on interval and specification. It does not run on
what this specific unit is signalling. An operator or maintainer
working strictly to procedure is therefore structurally decoupled
regardless of individual skill.

This predicts: machines under procedure-only regimes fail differently
and earlier than machines under a stable operator who reads them.

---

## FOUR MEASURABLES, NONE REQUIRING SELF-REPORT

All four use data that already exists in fleet, plant, or maintenance
systems. None requires asking anyone about their interior state.

### M0 — tool and equipment service life vs assignment structure
FIRST PASS ONLY. Replacement interval for identical tools/equipment
across sites with dedicated vs pooled assignment. Procurement systems
already record replacement frequency per tool type per site, so this
needs no new instrumentation.

Why it is attractive: service life is a hard number in currency and
needs no interpretation, unlike failure mode. Observation motivating
it — maintenance shops that once kept the same tool twenty years now
replace on a five-to-six month cycle.

Why it is NOT a headline test: dedicated assignment is necessary but
not sufficient for coupling. A positive result has at least four
things baked in — assignment stability, whether coupling is
permitted, whether hiring selected for the capacity at all, and
ordinary differences in duty cycle and site conditions. A large
effect justifies the closer look. It attributes nothing on its own.

### THE COST-BOUNDARY PROBLEM M0 EXPOSES
Interchangeability is cheap on the labor line and expensive on the
asset line. Reduced tool and equipment life lands in capital
replacement, procurement, and downtime — different budgets, different
reporting periods, frequently different decision-makers.

Neither line sees the trade, because nothing joins them. Any cost
analysis of staffing flexibility that stops at the labor line has
drawn its system boundary where the savings are and excluded where
the cost goes. That is a declared-boundary failure, not a finding
about flexibility.

### M1 — assignment structure vs failure mode
Dedicated unit assignment vs pooled assignment, against failure
mode, mean time between failures, and repair cost per hour of
operation. Assignment structure is already recorded.

### M2 — work-order lag and operator diagnostic accuracy
Where an operator identifies a fault but is not authorized to act:
lag between operator report and repair, and whether the
operator-identified fault matched what the eventual repair found.

### M3 — operator diagnostic accuracy vs certification status
Same accuracy measure, split by whether the person holds the formal
credential. Tests whether the credential predicts the competency it
claims to select for.

### M4 — convergence rate on an unfamiliar unit
Put a person on a machine they have never touched. Score diagnostic
accuracy against time-on-unit. Fast accurate convergence is the
proposed competency measure — transferable across machine types,
unlike procedure knowledge for a machine class.

---

## THE PERMISSION VARIABLE

Third condition, institutional and usually unrecorded:

    coupled + authorized       operator reads unit, acts on reading
    coupled + prohibited       operator reads unit, files report,
                               waits; signal dies in queue
    decoupled                  no reading to act on

The middle case is distinct and is the cleanest test case, because
the operator's diagnosis exists as a record and can be scored against
what the repair eventually found. The coupling is intact; the
authority is severed.

Any study that treats maintenance regime as a single variable
collapses these three.

Note the recording problem: the permission state is almost never in
any system, because nobody thought to write it down. Without it,
assignment structure alone carries permission, hiring selection, and
coupling capacity as unseparated confounds. Recording the three-state
variable prospectively costs one field and makes every other
measurable here attributable.

---

## CREDENTIALING MISALIGNMENT

Where certification tests written and symbolic processing but the work
is spatial and mechanical diagnosis, the filter selects on the wrong
axis. Populations strong on the axis that matters — dyslexic
practitioners among them — are excluded from the credential while
retaining the competency.

Downstream effect: once the filter is in place, a person who reads the
machine correctly has no standing against a person who holds the
paper. Machine-specific knowledge accumulated over decades is not
stored as a credential anywhere, so it does not transfer and its loss
does not appear in any account.

M3 above tests this directly.

---

## EXISTING INSTITUTIONAL ACKNOWLEDGMENTS

The variable is recognized in practice, in several fields, with no
cross-reference between them:

- aviation: type rating and hours-in-type tracked separately from
  total hours. Machine-specific competency treated as its own thing.
- maritime: per-vessel familiarization requirements.
- TPM / jishu hozen (autonomous maintenance): operator ownership of
  a specific unit written into the method. The machine is "wholly the
  domain of one person or team."
- German and Chinese manufacturing practice: machine control,
  maintenance, and repair held in ONE technical role rather than
  split between a reporting operator and an acting mechanic.
- historical US practice: per-aircraft ground crews under a named
  crew chief; locomotive assignment to specific engineers; machinist
  trade literature on a machine holding tolerance for its regular
  operator.

None of these have been analyzed against outcome data using
hours-on-the-individual-unit as the predictor.

---

## PHYSIOLOGICAL LITERATURE THAT EXISTS BUT IS NOT JOINED

Several fields describe the mechanism under different names:

- body schema / peripersonal space extension — tool use measurably
  remaps sensory boundaries to include the tool (primate and human
  recordings)
- incorporation / embodiment — prosthetics and human factors
- transparency, ready-to-hand — human factors design and
  phenomenology; the tool disappears from awareness when coupling
  holds and reappears as an object when it breaks
- extended mind / "the blind man's stick is part of the man"

None of this literature connects to maintenance outcomes, incident
classification, or certification design. That join is the gap.

---

## WHAT HAS BEEN CHECKED (2026-09-05)

- Aviation incident literature runs on TOTAL flight hours almost
  universally. The FAA fine-grained human-error study explicitly
  flags as undetermined whether accidents reflect lack of flight
  hours or inexperience with the particular aircraft.
- ONE exception located: gyroplane crashes, pilots with under 40
  hours in the same make and model were five times more likely to
  lose control and twice as likely to destroy the aircraft. Same
  make and model — still not the individual unit. Demonstrates the
  discriminator works when someone splits the hours.
- WWII per-aircraft records: AFHRA states maintenance information and
  crew member data were never entered on individual aircraft record
  cards; availability was reported at squadron/group level. Historical
  case study, not a usable dataset.
- US autonomous-maintenance implementations largely fail, with
  failure modes described as predictable. TPM gets imported as
  procedure, which does not reproduce the result.
- No study located comparing equipment outcomes across permission
  regimes.

---

## NON-HUMAN EVIDENCE (2026-09-05)

### Epistemic status of this section — read before citing it

What is established:
    - the neural remapping is real and measured (macaque, human)
    - individual-unit and pairing preferences are real in wild
      chimpanzees

What is NOT established:
    - that those two are the same phenomenon
    - that either connects to maintenance outcomes, incident rates,
      or operator performance on machines

Cross-species equivalence is an OPEN QUESTION here, not an
implication. The findings below are assembled because they are
suggestive enough to justify looking, not because they demonstrate a
common mechanism. If someone runs the join and finds no relation,
that is a result and should be posted.

### Measured remapping
Macaque parietal neurons responding to space around the hand begin
responding to space around a rake after the animal learns to use it,
and revert when the tool is set down (Iriki, Sakura and colleagues).
Electrophysiological, not inferred from behavior. This is the
mechanism for an operator sensing an impact to the machine as an
impact to self.

### Individual-unit preference, separated from class preference
Wild chimpanzee tool-composite study, five years of field data: 
specific stones were combined as hammer and anvil MORE OFTEN THAN
CHANCE even after controlling for preference for the individual
stones considered separately.

Two effects stacked, and they had to be statistically separated:
    (a) preference for particular individual units
    (b) preference for particular PAIRINGS of units

Effect (b) is the coupled-unit effect. It exists in wild chimpanzee
data and required deliberate statistical separation from (a) to see.
That separation is exactly what is missing from human operator data —
where assignment effects and individual-skill effects are never
split.

### Selection on mechanical property, not appearance
Chimpanzees select hammers and anvils by hardness, elasticity, and
rebound rather than by visual appearance — reading the specific unit's
mechanical behavior rather than matching a category. Harder stones for
hammers, softer for anvils.

### Long convergence curve
Stick tool use skill in wild western chimpanzees continues improving
into adulthood, past the point where strength and dexterity plateau.
A protracted convergence curve on a mechanically simple tool. This is
M4 above, observed on a decades-long timescale in a non-human species.

### The same effect under other names, in microbes and plants
Wherever a SPECIFIC individual partner outperforms an
equivalent-on-paper substitute, the effect is currently attributed to
genotype matching, local adaptation, or priority effects — all
category-level explanations for a unit-level effect.

Legume-rhizobium symbiosis has it measured and named. Common bean
studies report significant cultivar x strain interaction for nodule
number, chlorophyll index, and root dry mass, then run diallel
analysis to separate:

    general combining ability (GCA)   partner's average performance
    specific combining ability (SCA)  the PAIRING residual

SCA is the pairing effect. This is the same separation the chimpanzee
hammer-anvil study performed, executed independently in plant
breeding vocabulary, with no cross-reference. Reviews go as far as
"personalized genetic relationships," tracing strain x host genotype
specificity to allelic variation in single genes (bacA, LysM receptor
kinases, Sym2/Sym37).

### Discriminator: fixed advantage vs convergence curve
For microbes, genotype compatibility may be the entire explanation —
there is no learning and no within-pairing adaptation. That makes it
the ideal control case, and it yields a test that separates the two
mechanisms anywhere they might both apply:

    genotype matching   predicts a FIXED advantage, present from
                        first contact, flat over the pairing's life
    coupling            predicts a CONVERGENCE CURVE — advantage
                        accrues with time-in-pairing

Nobody has asked this of the symbiosis data, and the experimental
systems to ask it already exist. Same question, same shape, applies
to operator-machine data where time-on-unit is recorded.

### Framing note
The reason to look for this outside humans is not analogy. If the
pairing effect is real it should be substrate-general, and treating
it as a human skill — or as a human projection onto machines — is
what has kept six literatures from citing each other. Drop the
anthropomorphic framing in both directions and the variable becomes
measurable in all of them.

### Not claimed
Plant partner-specificity (root and mycorrhizal association) is
adjacent but is a different phenomenon — it belongs with coupling
capacity in symbiosis, not with tool incorporation. Do not fold them
together.

---

## THE JOIN NOBODY HAS MADE

Primate neurophysiology has the mechanism.
Primate field archaeology has the individual-unit and pairing effects,
statistically separated.
Aviation has hours-in-type as an institutional practice.
TPM has operator ownership as a method.
Industrial safety has an operator-error category with no coupling bin.
Human factors has transparency and ready-to-hand as concepts.

Six literatures, one variable, no cross-citation.

---

## WHERE IT IS RUNNABLE TODAY

Commercial vehicle fleets and manufacturing plants, where assignment
history and failure records both exist in the same system:

- fleet maintenance systems record unit, driver assignment, and
  repair events
- plant CMMS records machine, operator shift, work orders, and
  downtime
- NTSB data supports M1 at tail-number level for general aviation

The join is: assignment history x failure record x
hours-on-that-unit. All three fields exist. Nobody has joined them.

---

## CALL

Anyone with access to fleet or plant maintenance data can run M1.
It needs no new instrumentation and no interviews.

Raw results welcome, negative results especially. If assignment
stability shows no effect on failure mode, that is a finding and
should be posted.

---

## WHY THIS IS WORTH THE MONEY TO INVESTIGATE

Stated plainly, because the practical stake is what will get this
funded if anything does:

If assignment stability affects failure mode (M1), maintenance cost
and equipment life are being left on the table by pooled-assignment
policy, and the fix is a scheduling decision rather than capital
spend.

If operator diagnostic accuracy is real and currently unauthorized
(M2), then a detection capability already on the payroll is being
discarded at the work-order queue.

If coupling capacity is transferable and testable (M4), hiring and
certification can select for it directly, instead of treating every
operator as an interchangeable body and testing for procedure recall.

None of these require accepting any claim about interior experience,
in humans or anything else. They require measuring pairings instead
of averaging over them.

The engineering question for the next decades is where humans, machines,
and automated systems each actually fit. That is answerable by
measurement. It is currently being answered by assumption.
