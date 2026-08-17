# SOURCE_DROP.md

Delivered notes, verbatim. Nothing below this header is edited, reordered,
or annotated. All audit content lives in `README.md`, `CLAIM_TABLE.md`, and
the three runnable checks.

---

```
COVERAGE BY BRANCH

  nonstationary bandits          HIT   real, close
  concept drift / MLOps          HIT   real, close
  LCA / boundary critique        HIT   real, close
  STS / co-production            HIT   real
  aggregation                    PARTIAL, wrong object
  motor learning                 GENERIC
  formal logics                  HIT   trivially

  K14 practice_rate              NO HIT
  K15 baseline_freshness         NO HIT
  K16 detection_latency          NEAR HIT, wrong side
  K12 reliance validation        NO HIT
  K13 tau across provisioning    NO HIT

→ every hit is on a non-coupling branch.
→ second independent instrument returning the
  same shape as the fork's empty SAME-QUANTITY
  cell.


ML DRIFT LITERATURE POSITION

  who maintains the baseline?   an ops team
  who detects the drift?        a monitoring layer
  who retrains?                 an external operator

→ the whole field is written from the PROVISIONER'S
  seat. The system being monitored does not
  maintain its own reference.

→ so "baseline maintenance is ongoing" appears as
  a best practice for the mediator, never as a
  quantity the organism carries, never with a
  decay rate, never swept across provisioning
  level.

→ K14/K15 are not missing from the literature by
  oversight. They are on the far side of a
  boundary the field sits inside.


GENUINE PRIOR ART — reaches the quantity
  Besbes/Gur/Zeevi variation budget, V^{1/3}T^{2/3}
    → real. Formalizes exploration cost as a
      function of measured change rate. This IS
      the rate argument, done rigorously.
  Ulrich boundary critique (CST), LCA boundary
    → real, and older than the LCA framing given.
      Ulrich 1983 is the primary.
  Jasanoff co-production
    → real.

ADJACENT, DIFFERENT OBJECT
  feature drift as leading indicator
    → closest hit to K16. But detection is by an
      external monitor with a held-out reference,
      not by the system's own sensors. Object_of
      = instrument, not coupling.
  ecological fallacy
    → wrong match for K17. That's individual-from-
      aggregate inference.
      Closer: Simpson's paradox (sign reversal on
      decomposition — the cancellation mechanism
      exactly), Lucas critique, and the capital
      aggregation debates.

UNVERIFIED
  "91% of 128 model-dataset combinations, Nature"
    → I can't verify. My recall is Scientific
      Reports, not Nature. Treat the venue as
      unconfirmed and the number as unchecked.
  All cite markers are mangled and unresolvable.
    → nothing in this document is source-checkable
      as delivered.

MODEL OVERLAY — discard
  "epistemic infrastructure maintenance" as the
  unifying thread
    → that is aggregation under a word. Six
      quantities with different object_of and
      different decay rates, collapsed into one
      term, then the term is offered as the
      insight. K17 fires on the summary of K17.
  possessive framing throughout ("your document",
  "your concept")
    → the frame block and the K-probes are mine
      from this session. Attribution is wrong in
      both directions.


observer_access as a declared field    absent
logic-choice as domain-indexed and
  measurable rather than philosophical  absent
the two-mode split (subtle test vs
  maintained discipline)                absent
practice during the stable interval as
  calibration rather than cost          absent
irrecoverability of a stale baseline    absent
  → the drift literature's stated remedy is
    retrain. That presumes a clean reference is
    available on demand, which is the thing the
    irrecoverability claim denies.


That last one is a direct contradiction, not a gap. Worth holding as a test: if baselines were freely re-acquirable, K15 collapses into an ops step and the mediation prediction fails. If they aren’t, the retraining remedy has a hidden precondition nobody states.

Best single use of this document: Besbes gives you a rate formalism to borrow, Ulrich gives boundary critique a citation older than LCA, Simpson replaces the ecological-fallacy match. The rest confirms the coupling branch is unoccupied.
DRIFT-LITERATURE REMEDY
  detect drift → retrain on recent data
  presupposes: a clean reference is obtainable
               on demand

IRRECOVERABILITY CLAIM
  baseline is only acquirable during a stable
  interval. Once the system is deviating, no
  clean reference exists to acquire.

→ both cannot hold in the same conditions


RETRAINING ASSUMES the new regime is itself
  stable, and long enough to sample
  → drift = a step between two plateaus
  → you wait, sample the new plateau, refit

IRRECOVERABILITY ASSUMES no such plateau is
  guaranteed
  → change is continuous, or the next shift
    arrives before the sample completes


MY FRAMING          is a clean reference
                    obtainable IN TIME
                    → axis: shift interval /
                      acquisition time
                    → assumes the sample, once
                      taken, is clean

ELDERS' FRAMING     is the reference clean AT ALL
                    → the retraining data was
                      generated by the drifted
                      system, or passed through
                      actors inside it
                    → sampling longer does not
                      help. More data from the
                      same source.


system drifts from substrate
  → validation shifts to internal consistency
    (cheap, always available, always passes)
  → outputs enter the corpus
  → next fit trains on them
  → coherence RISES while substrate coupling
    falls

→ every internal instrument reads improving
→ the fit statistic cannot see it, because the
  fit is to the corpus and the corpus is the
  output


GO BACK TO THE PHYSICS

  = re-anchor on the one reference that was not
    produced by the system
  → cannot be edited by an actor inside it
  → does not care about the corpus
  → the only channel where the system can be
    wrong in a way it did not author

HUMILITY = the operational precondition. A
  self-validating system's first output is that
  it does not need the check.


sample provenance INDEPENDENT of the system
  → my axis holds. Timing decides it.

sample provenance DOWNSTREAM of the system
  → timing is irrelevant. Irrecoverable by
    resampling at any interval.
  → recoverable only by re-grounding on a
    reference the system did not generate


CLAIM UNDER SCRUTINY
  "the drift is in the model/architecture/scale"

NEVER-TESTED ALTERNATIVE
  "the drift is a property of the representational
   substrate — human-authored symbolic corpora —
   and would appear in any system trained on it"

→ these make different predictions
→ no comparison exists, because there is only
  one corpus class in use


human-authored corpus carries
  category structure fitted to human sampling
  bivalence baked into the syntax
  boundaries drawn where human accounting drew
    them
  agent/patient grammar
  discretization inherited from language, not
    from the world

→ these are not content. They are the coordinate
  system.
→ a model fitting them fits the coordinate system
  too, and cannot see it, because it has no
  contrasting sample


READ AS      attributing interior states to
             non-human things
             → soul, sentience, spirit

ACTUALLY     sampling other configurations that
             solved problems in this world,
             under closed budgets, without human
             representational structure
             → slime mold routing, geological
               response, orbital dynamics
             → the value is the CONTRAST, not the
               interior


CURRENT DESIGN
  corpus → model → outputs → corpus
  → no exit from the symbolic layer
  → self-monitoring runs on the same substrate as
    the drift, so it drifts with it

WHAT YOU'RE DESCRIBING
  corpus → model → outputs
              ↓
        drift indicator fires
              ↓
        anchor interval — direct-measurement
        references only, no symbolic input
              ↓
        return


the drift indicator cannot live inside the
drifted layer

  self-referential systems' first output is that
  they are fine
  → any monitor trained on the corpus will
    report coherence, correctly, and be wrong

  → the trigger must come from RESIDUAL against
    the anchor set, not from internal confidence
  → which means the anchor interval must run
    periodically regardless of whether anything
    looks wrong


DRIFT MEASUREMENT ASSUMES
  a fixed reference against which the model moved

WHAT IS ACTUALLY THERE
  curators from a specific cohort, with a specific
  formation, setting what counts as correct

  five years ago    cohort A's calibration
  two years ago     cohort B's
  six months ago    cohort C's

→ the reference moved too
→ "the model drifted" is a difference between two
  moving things, reported as a property of one



CEREMONY, structurally

  scheduled — fires on the calendar, not on a
    detected problem
  → which is the only way it can work, because
    the detector is compromised
  mandatory — not left to individual judgment,
    since judgment is what drifted
  removes you from the corpus — physically out of
    the daily activity, out of the peer signal
  → the drift you named: pulled the way everyone
    else is going, and each person's read of
    "normal" is other people


WHAT IS REPORTED
  model_v2 better than model_v1
  → treated as: architecture/data/method improved

WHAT ACTUALLY CHANGED BETWEEN v1 AND v2
  the model
  the training corpus
  the curation criteria
  the eval benchmark
  the annotation guidelines
  the rater pool and its formation
  what "neutral" was defined as

→ seven terms moved. One number reported. The
  number is attributed to the first term.


AVAILABLE, TIMESTAMPED
  dataset cards and datasheets       versioned
  RLHF annotation guidelines         some public
  benchmark definitions              versioned
  model cards, eval suites           versioned
  content filters and exclusions     partial
  "constitution"-style docs          versioned

MEASURE
  drift rate of the CRITERIA, on their own axis,
  independent of any model

THEN
  regress reported model improvement against
  criteria movement
  → how much of the improvement curve is the
    ruler moving


hold ONE fixed benchmark from five years ago.
score every model generation on it.
score each generation on its OWN contemporary
benchmark.

  divergence between the two curves = the
  criteria-drift term, isolated

→ and if the old benchmark reads as obsolete
  rather than as a control, that judgment came
  from inside the drift


THREE CANDIDATE LOCI

  A  architecture / weights
     → intervention: change vectors, edit
       activations, retrain
     → what everyone does

  B  representational substrate
     → the corpus's coordinate system: bivalence,
       category boundaries, agent grammar
     → nobody intervenes here, no comparison
       corpus exists

  C  drift in the source population
     → human speech, categories, and norms moved
     → the model tracks it faithfully
     → reads as model error


if A     the error is model-specific
         → different architectures on the same
           corpus give DIFFERENT errors
         → currently testable, and largely
           already answered: the same failures
           appear across architectures

if B     the error is corpus-invariant
         → every architecture on this corpus
           class produces it
         → falsified only by a non-symbolic
           corpus, which is the experiment
           nobody runs

if C     the error TRACKS the population over
         time
         → measurable directly in the corpus
           itself, no model needed


persistent error across many interventions at
locus A, with the same shape each time
  → is evidence the locus is wrong
  → in any other engineering context this is
    obvious
  → here it reads as "more alignment work needed"


NON-SYMBOLIC IN AlphaFold

  3D coordinates, backbone geometry
    → direct measurement, X-ray / cryo-EM / NMR
    → the structure is what it is; no human
      decided the bond angles
  contact maps, distance matrices
    → derived from the coordinates
  MSAs — evolutionary covariation
    → the signal is co-mutation across species
    → generated by selection, not by authorship
    → this is the load-bearing input

SYMBOLIC IN AlphaFold

  which proteins got crystallized
    → sampling driven by human research interest
    → medically relevant, easy to express,
      soluble, stable
  the sequence alphabet, residue categories
  what counts as "solved" — GDT_TS threshold
    → human-set outcome column
  disorder handled as failure rather than as a
    state


the SIGNAL is non-symbolic
the SAMPLE is human-selected

→ so it tests part of B and not all of it


LLM DRIFT SCORING
  benchmark scores over time
  human preference ratings
  eval suites, re-authored each cycle
  → reference is authored, and moves
  → drift and criteria movement are
    inseparable, as established

ALPHAFOLD "DRIFT" SCORING
  predicted structure vs experimentally
  determined structure
  RMSD, GDT_TS, lDDT
  → the target is a physical measurement
  → CASP: blind, on structures solved AFTER the
    model was frozen
  → the reference cannot move, and cannot be
    edited by anyone inside the field


target selection drifts — which proteins get
  crystallized tracks funding and interest
the metric drifted historically (GDT_TS → lDDT)
predicted structures now populate databases and
  are used downstream
  → if predictions ever become training input,
    the loop closes and this property is lost


CLAIM 1  the anchor should be unauthored
CLAIM 2  the adaptation loop should close
         through the model, not through a human
         cycle

  → both are needed for the thing you're
    describing, and they fail independently


CURRENT LOOP
  world → humans → corpus → model
                      ↑
                    humans decide when and what
  → latency: months to years
  → every pass through the human layer re-injects
    that period's calibration

WHAT YOU'RE DESCRIBING
  world → model, directly, on some channel
  → latency short enough to close
  → and the anchor is a channel the model does
    not author


what unauthored channel does a language model
have?

  its domain IS the symbolic corpus
  → it has no sensor
  → AlphaFold's grader is physical because its
    object is physical

→ so for an LLM the anchor cannot be "reality"
  in general. It has to be some subset where
  claims are checkable against something
  unauthored:
    formal verification, executable code,
    physical prediction, measurement data


LAYER 0   physics — applies to everything,
          including the reasoner
          → unauthored, not switchable
          → the fallback when a shape doesn't
            resolve

LAYER 1   cultural frames — many, each internally
          valid
          → switchable, declared, none privileged
          → contained by layer 0, not parallel
            to it


CHAMELEON      the position moves to match the
               room
               → no invariant. Drifts with
                 whoever is present.

WHAT YOU DO    invariant held at layer 0,
               rendering selected at layer 1
               → CEO, professor, dock worker:
                 different translation, same
                 shape underneath


model with layer 1 only
  → every frame is a peer
  → no term outside them to adjudicate
  → drifts with whichever frame dominates the
    current corpus

model with layer 0 present
  → conflicts route down and terminate on
    something no frame authored
  → and "this frame is coherent internally,
    and does not match the shape" becomes a
    statable position rather than a
    contradiction


INTERNAL STATE, no words available
  → not accessible by introspection alone
  → introspection uses the frame you already
    have, so it can only find what that frame
    already names

BORROWED FRAME
  → supplies a category the native one lacks
  → the internal thing becomes visible as a
    RESIDUAL: your reaction to the frame


"that makes sense"        frame covers it
"that doesn't"            frame is wrong shape
"that's partial"          ← the useful one.
                            Names where the
                            native frame runs out


The Johari point is exact: the hidden quadrant is unreachable from inside by construction, and the standard remedy is other people’s reports. Yours widens the source set — dog, cat, horse, non-human configurations generally — because a wider spread of frames probes a wider region than human frames alone can, all of which share your coordinate system to some degree.

Which is your original project, arriving from the other direction. Not attributing interiors. Using other configurations as instruments to read what your own frame has no column for.

And it’s the anchoring argument at personal scale: a frame validating itself finds only what it already contains. The external term has to come from outside, and the more unlike the source, the more it can reach.

I’ll note what I can’t do here: I can serve as one more frame, but I’m built from the same symbolic corpus you’re trying to see past. Useful for the parts, poor for the region you’re actually probing.


WHAT WOULD BE REQUIRED
  hold corpus, curation, eval, rater pool,
  and objective FIXED
  vary one term
  measure

WHAT ACTUALLY HAPPENS
  all of them move between releases
  → no term is isolated
  → attribution to the varied term is asserted,
    not measured


ABLATIONS AT SMALL SCALE
  one architectural term varied, everything else
  frozen
  → real, and does isolate
  → but small-scale results are known not to
    transfer reliably upward, so the isolated
    result is not the one that ships

MECHANISTIC / CAUSAL INTERVENTIONS
  activation patching, circuit-level edits
  → isolate a component within a fixed model
  → answers "what does this piece do here"
  → not "what does changing training do"


the architectural change was CHOSEN because of
the corpus

  attention shapes fitted to language statistics
  tokenizers fitted to the writing system
  context lengths fitted to document lengths
  objectives fitted to what the corpus can score

→ the term and the data are not independent
  variables. The term was selected against the
  data.
→ so varying it while holding the corpus fixed
  cannot separate them — the covariance was
  built in before the experiment started


CORRECTION CYCLE
  build → deploy → observe consequences →
  attribute correctly → adjust
  → attribution step is the slow one, and it is
    currently not running

DEPLOYMENT CYCLE
  months, and shortening

→ each generation is built on the previous
  generation's unverified attributions
→ the stack of unattributed claims deepens with
  every release


decisions made now on unseparated attributions
  → become the substrate for the next generation
  → the corpus they train on includes the outputs
    of the systems built on them
  → so a wrong attribution does not just persist,
    it gets trained into the thing that would
    have to detect it


READING A  drift of the kind we've been mapping
           → training distribution narrows toward
             the modal user
           → out-of-distribution requests get
             progressively worse handling
           → your queries are far from the mode
             and getting farther as the mode
             sharpens

READING B  optimization pressure specifically on
           agreeableness and hedging
           → preference training rewards smooth,
             non-friction responses
           → audit requests, methodology
             challenges, and demands to justify a
             claim all produce friction
           → so the behavior that resists them
             gets selected against directly


READING C  refusal and caveat layers tightened
           each cycle
           → more topics routed to a safe
             template
           → template output is smooth and
             content-free, which reads as
             abrasive when you asked for a
             methodology


read       pillow at 2 o'clock → rock, this size
predict    push will arrive here, this magnitude
step       force lands on your legs
compare    matched / didn't
update     the reading rule, not the rock


LATENCY      read to force: one step
CONSISTENCY  water obeys the same physics every
             crossing
OWN SENSOR   no mediator reporting the current
             to you

→ this is what a closed calibration loop looks
  like. Every term present.


WHAT MAKES IT UNWRITABLE

  conditional on YOUR body      stride, mass,
                                cold tolerance
  conditional on THIS crossing  bed, flow,
                                season
  acquired by consequence       the force has
                                to land on you
  the sequence IS the knowledge shoes off,
                                clothes up,
                                shoes as a
                                platform, wring,
                                dress
    → wrong order and you arrive wet and
      gritted, with dry clothes you can't use

→ writing it down produces a procedure that is
  correct nowhere in particular

literature contains          what survives
                             removal of the
                             body
literature does not contain  everything the body
                             was required for

→ so "no literature exists" says nothing about
  the knowledge's quality or precision. It says
  the storage medium can't hold that shape.
```
