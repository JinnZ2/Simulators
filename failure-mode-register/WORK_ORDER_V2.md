# WORK ORDER — FAILURE-MODE ENUMERATION FOR ML-AS-INFRASTRUCTURE
# License: CC0. stdlib-only if code is produced. Deliverable is a REGISTER, not a paper.

## 0. WHAT THIS IS

Bridge engineering has as-builts, material provenance, load ratings and inspection
intervals. It does not have these because engineers are careful. It has them because
failure modes were ENUMERATED AFTER THINGS FELL DOWN, and the enumeration became
mandatory.

ML systems are being placed in load-bearing positions with no equivalent enumeration.

This work order specifies the missing artifact: a mechanism-level failure-mode register
for ML components used as infrastructure, from which durability requirements could be
derived.

NON-GOALS (state explicitly in the deliverable):
  - not model behaviour, alignment, or misuse
  - not harm incidents
  - not a code of ethics
  SCOPE IS DURABILITY AND RECONSTRUCTABILITY ONLY: can the deployed object still be
  identified, re-produced, load-rated and inspected at t + N years, by someone who is
  not the original author and does not hold the tacit stack.

## 1. THE STRUCTURAL PROBLEM THAT MAKES THIS HARDER THAN BRIDGES

A bridge catalogue is buildable because failure is OBSERVABLE, DATED and LOCATED.
Something falls down. The event forces the entry.

An ML infrastructure failure may produce NO EVENT. Degradation appears as slightly worse
decisions distributed across a population, attributed at the last hop to whoever was
holding the output.

  => ENTRY 0 OF THE REGISTER IS THE DETECTION GAP ITSELF.
     Every subsequent entry must carry a DETECTION CHANNEL field, and that field is
     permitted to be NONE. Entries with DETECTION = NONE are the high-priority set:
     they are the modes that cannot generate the evidence that would make them
     mandatory to fix. That is the mechanism by which the enumeration fails to get
     written at all.


## 1B. LOSS-VARIABLE MAP

Variables under which a technology is lost, derived from historical cases, then scored
for ML infrastructure. Scores carry amendments from Section 9; the amended score is
authoritative and the original is retained so the correction is auditable.

```
V1   ARTIFACT RETENTION     does a physical instance outlive the record
V2   PRECONDITION LOAD      how much tacit stack the record assumes in its reader
V3   CARRIER POPULATION     number who can READ THE REPRESENTATION (see A-01)
V4   CARRIER TURNOVER       replacement rate vs time to transmit
V5   REGENERATION CYCLE     how often it is actually re-taught or re-performed
V6   MEDIUM DURABILITY      substrate readable at t+N (see A-02)
V7   COPY MULTIPLICITY      number of independent custodians
V8   ACCESS GATING          deliberate closure - guild, classified, proprietary
V9   DEMAND CONTINUITY      is the load still on it
V10  SUBSTITUTION RATE      replacement arriving before predecessor is recorded
V11  IDENTIFIABILITY        can you tell which object the record describes
V12  RECONSTRUCTION TEST    can a candidate rebuild be VERIFIED as correct
V13  INDEXABILITY           findable again, under a name still in use
V14  SHOCK EXPOSURE         events that cut carrier population at once (see A-03)
```

`+` protects, `-` drives loss.

```
        CLASSICAL CASES        ML INFRASTRUCTURE      AMENDED
V1      + object survives      -- nothing deposited
V2      -- high (the ash)      -- high (versions, data state, hw)
V3      -  small guild         +  large                  -> --   A-01
V4      +  slow (lifetime)     -- fast (mobility, reorg)
V5      +  daily use           +  continuous
V6      +  stone, parchment    -  format rot             -> --   A-02
V7      -  few                 +  copying is free
V8      -  guild secrecy       -- proprietary, engineered
V9      -  collapses           ++ maximal and rising
V10     -  slow                -- extreme
V11     +  object is itself    -- variance defeats it
V12     +  testable            -- see F1 below
V13     -  name lost           +  search works
V14     -- war, plague         +  low                    -> split A-03
```

### 1B-1  THREE FINDINGS FROM THE COMPARISON

F1  THE VERIFICATION CHANNEL IS BLOCKED, NOT ONLY THE RECORD.
    Every classical recovery ran on V12: mix a candidate concrete, test it against the
    surviving wall, and a failed reconstruction is distinguishable from a successful
    one. With run-to-run spread of the magnitude measured in 3A, a reconstruction that
    misses the published number is INDISTINGUISHABLE from a bad draw of the correct
    procedure. Reconstruction cannot be validated even when attempted. A missing test
    is worse than a missing record.

F2  THE PROTECTIVE VARIABLE IS MAXED AND DOES NOT PROTECT.
    V9 is the usual reason things survive - continuous use forces continuous
    re-teaching. Demand here is at maximum and it still loses, because V10 outruns
    documentation. Loss is not by abandonment but by REPLACEMENT VELOCITY: the object
    is superseded before it was ever captured. No classical analogue. "It is widely
    used, it will be fine" is therefore false comfort, and must not be accepted as an
    existing_control in any entry.

F3  THE GOOD SCORES ARE ON THE WRONG VARIABLES.
    Wins after amendment are V7 and V13: copy cost and findability. Both protect
    DOCUMENTS. Losses are V1, V4, V8, V10, V11, V12: all protect OBJECTS. The system is
    well built to preserve what was written about the thing and poorly built to
    preserve the thing.
    ORIGINAL FORM of F3 listed V3 and V14 among the wins; both were amended out. The
    protective set is thinner than first scored and is entirely document-side.

## 2. ENTRY SCHEMA (the actual deliverable)

Each register entry is a record with these fields. An entry missing any field is an
UNRATED PART and is filed as such, not discarded.

  id                 stable identifier
  mechanism          how the failure happens, at mechanism level not instance level
  load_condition     what has to be true of the deployment for this to bite
  onset              immediate | drift | dormant-until-triggered
  detection_channel  what signal would reveal it, or NONE
  detection_latency  time from onset to earliest possible detection, or UNBOUNDED
  attribution        where blame lands by default when it does surface (last hop)
  consequence        what fails while load is on it
  evidence_class     MEASURED (cite) | TRANSPORTED (name source domain + justify)
                     | PROJECTED (no anchor — flagged, lowest weight)
  existing_control   what current practice does about it, or NONE
  reconstruction     can the deployed object be rebuilt from the retained record?
                     YES | PARTIAL | NO
  validity_range     conditions under which this entry is claimed to hold

Rule: evidence_class = PROJECTED entries may not exceed a stated fraction of the
register. A register that is mostly projection is a speculation list wearing a
register's format.

## 3. WHERE ENTRIES COME FROM

### 3A. MEASURED — defects already documented in the ML literature
Anchor entries to what is already established. Seeds (all require re-verification
against primary sources before the register ships):

  - run-to-run variance under identical configuration large enough that a single
    reported number does not identify the object produced
  - software/dependency versions unstated in the overwhelming majority of reports,
    so exact re-execution is impossible in principle
  - data leakage propagating across many studies and fields, with corrected results
    erasing claimed superiority over older statistical methods
  - absence of an agreed significance measure, so point estimates ship without a
    characterised distribution
  - the compounding line: the defect is NOT VISIBLE FROM READING THE REPORT, because
    the report format lacks the fields that would expose it

Each of these becomes a mechanism entry, not a complaint.

### 3B. TRANSPORTED — from domains whose catalogue already exists
Named source domains, each with a mature enumeration and a forcing history:

  structural / civil     as-built drift, undocumented field modification, load rating
                         lost, inspection interval unset
  aviation               configuration control, part traceability, latent fault
                         dormant until an unusual load combination
  pressure vessel        material provenance, certified test conditions, stamped
                         validity envelope
  pharmaceutical         batch records, custody chain, retained reference sample
  nuclear transport      continuous custody, documented handoff at every stop
  civil records / archive  format obsolescence, dependency on a reader that no longer
                         exists

TRANSPORT RULE: each transported entry must state WHY the mechanism carries. A
mechanism carries if the abstract structure holds (a record insufficient to rebuild the
object) — not because the domains feel similar. Transports that rest only on analogy
are rejected at review.

The RETAINED REFERENCE SAMPLE from pharma and the STAMPED VALIDITY ENVELOPE from
pressure vessels are the two highest-value transports: both are cheap, both are
mandatory in their home domain, and neither exists here.

### 3B-W. WORKED ENTRIES — the two priority transports, schema filled

Both source mechanisms are the same trick at different times: freeze something cheap
now so a later dispute has a referent. They are entered here as worked examples of the
schema and as the two entries expected to survive review.

```
ENTRY  DUR-001
id                 DUR-001
mechanism          Deployed object cannot be distinguished from any other object
                   produced by the same nominal procedure. Run-to-run variance under
                   identical configuration is large enough that the reported number
                   does not identify which object was produced; after deployment,
                   substitution, patching or drift leaves no trace distinguishing the
                   current object from the documented one.
load_condition     Any deployment where the object is updated, re-served, migrated or
                   supplied by a party other than the evaluator.
onset              dormant-until-triggered — no symptom until a dispute or a
                   performance question forces the identity question, at which point
                   the referent does not exist
detection_channel  NONE under current practice.
                   PROPOSED: sealed probe-response record — a probe set fixed at
                   deploy, the deployed object's responses to it, hashed, held by a
                   party that is not the operator. Third-party checkable without
                   re-manufacture.
detection_latency  UNBOUNDED without the control. With the control: one probe cycle.
attribution        Last hop. Lands on whoever was holding the output when the
                   behaviour changed.
consequence        Any later claim about the deployed object is unverifiable. Silent
                   substitution, undeclared update and as-built drift are all
                   indistinguishable from normal operation.
evidence_class     TRANSPORTED — pharmaceutical retained reference sample.
                   TRANSPORT JUSTIFICATION: the abstract structure is a record
                   insufficient to identify the object it describes, closed by
                   retaining a small physical referent taken BEFORE any problem is
                   known, cheap relative to the batch, and testable by a third party
                   without re-manufacture. All three properties carry to a probe-
                   response record. This is not resemblance between industries; it is
                   the same insufficiency and the same closure.
                   Partially MEASURED: the variance and version-reporting defects in
                   3A establish the insufficiency directly.
existing_control   NONE.
reconstruction     NO as deployed. PARTIAL with the control — the control establishes
                   IDENTITY, not reproducibility (see DUR-001-N2).
validity_range     Holds where the object is served through an interface that can be
                   queried. Does not hold for objects embedded such that probe
                   queries are indistinguishable from production load, or where probe
                   cost is not small relative to serving cost.
```

```
ENTRY  DUR-002
id                 DUR-002
mechanism          Object is applied outside the conditions under which its reported
                   performance was established, with no signal that this has occurred.
                   The stated conditions, where they exist at all, are filed in a
                   document elsewhere rather than attached to the object at point of
                   use, so the operator applying load cannot read the rating.
load_condition     Any deployment where input distribution or decision consequence
                   can vary after evaluation. In practice: all of them.
onset              drift
detection_channel  NONE under current practice. Confidence scores do not serve —
                   a confident output inside a distribution the object was never
                   characterised on is the failure, not a warning of it.
                   PROPOSED: stamped validity envelope attached to the serving
                   interface, machine-readable, carrying characterised input
                   distribution, decision consequence range, date, and seed/variance
                   basis. Plus a RETURN CONTRACT: the interface returns value AND
                   rating status, where OUT_OF_ENVELOPE is a distinct return state,
                   not a low score on a continuous confidence axis.
detection_latency  UNBOUNDED without the control. With it: immediate at call time.
attribution        Last hop, again — the operator who acted on the out-of-envelope
                   output.
consequence        The system continues returning values while unrated. Under load,
                   with no record that the envelope was exceeded or that a criterion
                   was selected in the absence of one.
evidence_class     TRANSPORTED — pressure vessel stamped plate.
                   TRANSPORT JUSTIFICATION: the mechanism is a rating that exists but
                   does not travel with the object, so it is unreadable at the point
                   where load is applied. Structurally identical. The carried
                   discipline is the sharp one: OUTSIDE THE ENVELOPE THE VESSEL IS
                   UNRATED — not degraded, not derated, unrated. That maps to the
                   existing engineering-grade standard in this ecosystem without
                   modification.
existing_control   Model cards and documentation exist, but are filed alongside rather
                   than attached, are not machine-readable at call time, and carry no
                   return contract. Score as PARTIAL, not NONE — this is the null-set
                   discipline in Step 7.
reconstruction     Not applicable directly; DUR-002 governs USE, not rebuild. It is
                   the load rating, not the as-built.
validity_range     Requires the input distribution to be characterisable. Where it is
                   not, the honest envelope is empty, and an empty envelope is itself
                   the rating.
```

```
ENTRY  DUR-003
id                 DUR-003
mechanism          MIGRATION ATTRITION. The object survives no single event, but is
                   carried across repeated hops — framework version breaks, dependency
                   EOL, storage migration, account and org changes, platform
                   deprecation. At each hop a survival fraction applies, and what is
                   carried forward is selected BY CURRENTLY PERCEIVED VALUE. Anything
                   whose value appears later is filtered out by construction.
load_condition     Any object whose retention depends on being actively carried rather
                   than passively held. All hosted, containerised or dependency-bound
                   artifacts.
onset              drift — compounding, p^N over N hops, no visible loss at any single
                   hop
detection_channel  NONE. Attrition is invisible per hop by definition; the object that
                   was dropped is not the object anyone is looking at.
                   PROPOSED: hop log. Every migration event records what was carried,
                   what was dropped, and by whose decision. Cheap, and it converts an
                   undated attrition into a dated one.
detection_latency  UNBOUNDED. Discovered only when something is needed and absent.
attribution        None available — no actor performed a loss. Each hop decision was
                   locally correct.
consequence        Reconstruction path degrades silently while all headline indicators
                   remain healthy.
evidence_class     TRANSPORTED — archive and records management, format obsolescence.
                   TRANSPORT JUSTIFICATION: the abstract structure is retention
                   contingent on repeated active re-commitment, with a per-hop
                   selection filter that is not the criterion the future reader will
                   use. Identical structure, different substrate.
existing_control   NONE at the artifact level.
reconstruction     Degrades from PARTIAL toward NO without any state change being
                   recorded.
validity_range     Holds where hop count over the retention horizon exceeds ~1. Does
                   not apply to objects deposited once in an archive with a custodian
                   whose mandate is retention rather than operation.
NOTE               Distinguish from DUR-001. DUR-001 is "cannot tell which object."
                   DUR-003 is "the object is no longer being carried." Independent.
```

```
ENTRY  DUR-004
id                 DUR-004
mechanism          STRANDED UNDER LOAD. The object is retained and still bearing
                   production load, but the carrier population that can read, modify,
                   verify or replace it has gone to near zero. Not lost — stranded.
                   Artifact present, demand maximal, comprehension absent.
load_condition     Long-lived deployment plus high carrier turnover plus high
                   precondition load. The combination, not any one term.
onset              drift, then step-change at the departure of the last carrier
detection_channel  WEAK but non-zero, unlike most entries here: bus-factor count,
                   time-to-first-successful-modification by a new engineer, failed
                   replacement attempts. These are measurable today and are not
                   measured.
detection_latency  Detectable BEFORE the failure if the above are instrumented;
                   otherwise detected at the first required change that cannot be
                   made.
attribution        Lands on whoever is holding it when a change is finally required,
                   typically years after the decisions that produced the state.
consequence        The system continues to work and cannot be altered. Every option
                   except continued operation closes. This is a live liability, unlike
                   a lost artifact with no load on it.
evidence_class     MEASURED by analogy in software generally — legacy systems with
                   present artifact, maximal load and near-zero carriers are an
                   observed, documented, current state, not a projection.
existing_control   NONE for ML specifically. General software practice has partial
                   controls (documentation mandates, rotation) with known poor
                   compliance.
reconstruction     NO. Reconstruction requires comprehension, which is the missing
                   term.
validity_range     Applies where the object cannot be cheaply retrained or regenerated
                   from a specification. Where regeneration is cheap and the spec is
                   held, stranding does not bind.
NOTE               This is the INVERSE of the classical monument case. Pyramids:
                   object retained, load off, gap harmless. Stranded: object retained,
                   load on, gap is the liability. The classical intuition that a
                   surviving artifact means a recoverable technology fails here.
```

#### COMPOSITION — the two do not work alone

  envelope without sample   stated conditions cannot later be checked against what
                            was actually deployed
  sample without envelope   responses with no stated conditions — data, not a rating

The probe set defines the envelope's interior; the envelope makes the probe record
interpretable. Register them as a coupled pair.

#### KNOWN FAILURE MODES OF THE CONTROLS THEMSELVES

DUR-001-N1  PROBE LEAKAGE. A public probe set gets trained against, after which it
            measures probe performance rather than object identity. Sealed-and-hashed
            handles single-deployment identity but not reuse across deployments.
            Requires rotation, or per-deployment generation from a seed held by the
            third party. Enter as a control precondition, not a footnote.

DUR-001-N2  INSTANCE vs PROCEDURE. Given the run-to-run variance, a probe response
            identifies the DEPLOYED INSTANCE. It does not establish that the training
            procedure reproduces it. These are separate requirements and conflating
            them would let a deployment claim reconstruction coverage it does not
            have. DUR-001 closes identity only; procedure reproducibility remains
            open and needs its own entry.

DUR-002-N1  EMPTY ENVELOPE READ AS BROAD ENVELOPE. An object with no characterised
            distribution and an object characterised as broadly applicable are
            indistinguishable if the field is left blank. Blank must be a distinct
            value from wide.

### 3C. NEAR-MISS / SILENT
Modes with detection_channel = NONE cannot be sourced from incident history by
construction. Source them by walking the RECONSTRUCTION field backwards: for each thing
that would have to be true to rebuild a deployed object, ask what happens if it is
absent and nobody notices. Anything found this way is PROJECTED unless a transport
anchors it.

## 4. PROCEDURE

  Step 0  PRIOR-ART CHECK. Incident and harm catalogues for AI already exist. Verify
          whether any existing catalogue enumerates DURABILITY and RECONSTRUCTION
          modes rather than harms. If one does, this work order is redundant in whole
          or part — say so and stop, or scope to the residual. Do not build a second
          copy of an existing list.
  Step 1  Fix the deployment class being enumerated. "ML system" is too broad to
          load-rate. Pick one: e.g. a model in a decision loop with no human review, or
          a model whose outputs feed a physical actuator.
  Step 2  Populate 3A. Measured entries first — they set the floor.
  Step 3  Populate 3B. One source domain at a time, transport justification per entry.
  Step 4  Populate 3C. Flag all as PROJECTED.
  Step 5  Score each entry on RECONSTRUCTION. The distribution of YES/PARTIAL/NO is a
          headline result on its own.
  Step 6  Derive the requirement set. For each entry with existing_control = NONE and
          consequence non-trivial, state the minimum artifact that would close it
          (deposit, custody record, load rating, inspection interval). This is the
          output that maps to bridge practice.
  Step 7  Report the NULL SET: modes checked and found already controlled. A register
          that finds everything broken is not measuring, it is advocating.

## 5. WHAT "LOAD RATING" MEANS HERE

Direct mapping, stated so the deliverable is not metaphorical:

  as-built           the weights, data state and full software stack actually deployed,
                     deposited somewhere that outlives the depositing entity
  material           training data provenance, including what was excluded
  provenance
  load rating        the stated input distribution and decision consequence range within
                     which the reported performance was established; outside it the
                     component is UNRATED, not degraded
  inspection         a defined re-measurement cadence against a held-out reference, with
  interval           a stated action threshold
  as-built drift     the deployed object diverging from the documented one through
                     updates, patches and silent substitution, with no record that the
                     change occurred

Silent substitution already has a marker in this ecosystem. Cross-reference rather than
re-derive.

## 6. THE CUSTODY AXIS

Fidelity and custody are independent. The register must not collapse them.

  FIDELITY   is the reported result true of the object produced
  CUSTODY    can the object be identified and re-produced later, by someone else

Current practice instruments fidelity only, and weakly. Custody is unmeasured, which
means it is being read as adequate. An unmeasured variable is not absent — it is set to
zero, which is a positive claim nobody licensed.

PROPRIETARY BOUNDARY as a custody term: a disciplinary boundary is porous and the
material crosses eventually. A proprietary boundary is engineered impermeable and the
impermeability is the asset — transmission is actively prevented, not neglected. Loss
timescale inverts from centuries to years: a fold, an acquisition, a strategy change.
Any entry whose reconstruction path runs through a single commercial entity carries
detection_latency = UNBOUNDED and reconstruction = NO by default.


```
ENTRY  DUR-005
id                 DUR-005
mechanism          AMBIENT PRECONDITION. The record is complete on its own terms and
                   still unusable, because the conditions under which the procedure ran
                   were never candidates for statement. Not underspecified - never
                   specified, because nobody holds "there will be servers" as an
                   assumption. It is the condition under which holding assumptions
                   happens.
                   This is the mode that makes reconstruction attempts fail REPEATEDLY
                   ACROSS LONG PERIODS even where custody worked. The reconstructor is
                   not missing a step in the procedure. The reconstructor is missing
                   the world the procedure ran in, and the procedure gives no
                   indication that a world was required.
load_condition     Any record produced inside a stable operating environment - i.e.
                   all of them, which is why this entry sits above the others.
onset              dormant-until-triggered. No symptom until an ambient condition
                   ends, at which point the change is step, not drift.
detection_channel  NONE from inside. Ambient conditions cannot be enumerated by the
                   population for whom they are ambient, for the same structural
                   reason an exclusion register cannot be generated from inside the
                   frame it excludes from.
                   PROPOSED: see AMBIENT ENUMERATION PROCEDURE below. Requires
                   outside-the-stack input as a hard requirement, not a nicety.
detection_latency  UNBOUNDED, and asymmetric: detectable cheaply BEFORE the condition
                   ends, not at all after.
attribution        None. No actor omitted anything.
consequence        Reconstruction fails even where deposit, custody and hop logging
                   all succeeded. This entry can void the controls proposed for
                   DUR-001 through DUR-004 without any of them having failed.
evidence_class     MEASURED historically (repeated failed reconstruction of lost
                   technologies where partial records survived); PROJECTED for the
                   specific ambient set below.
existing_control   NONE. Not addressed by reproducibility practice, which operates
                   entirely inside the ambient set.
reconstruction     NO, and undetectably so - the record looks complete.
validity_range     Holds wherever the record's reader is separated from the author by
                   enough time or enough environmental change that any ambient
                   condition has ended.
```

### AMBIENT ENUMERATION PROCEDURE (control for DUR-005)

Do not ask what is assumed. The question returns the stated assumptions, which are
already in the document, and returns nothing ambient.

Ask instead: WHAT WOULD HAVE TO STOP EXISTING FOR THIS TO BECOME UNREADABLE?

  - run the question with participants OUTSIDE the stack - different domain,
    different era of practice, different infrastructure assumptions. Someone for
    whom the condition is not ambient. This is a hard requirement of the
    procedure; run internally it returns the stated set.
  - the output is a list of conditions, each with a finite expected lifetime
  - record the list. It is not a prediction. It is the world-state the record
    depends on, written down while it is still visible.

Candidate ambient set for ML infrastructure - unglamorous, none appearing in any
paper, each with a finite expected lifetime:

    continuous power at current density and cost
    fabrication capability at current tolerance
    a network
    a machine that reads the format at all
    storage priced as effectively unlimited
    compute priced as effectively unlimited
    a continuing custodian (see DUR-006)

The last three are assumptions about ECONOMICS AND INSTITUTIONS presented as
technical background. They are the least durable items on the list and the least
likely to be written down.

### DUR-005-B  TWO CLASSES OF AMBIENT CONDITION

The set enumerated above is entirely ARTIFACT-SIDE. There is a second class, and it
is not reachable by the same question.

```
ARTIFACT-SIDE AMBIENT    conditions the object needs in order to exist and be read
                         power, fabrication, network, format reader, storage and
                         compute price, a custodian
                         -> found by: what would have to stop existing for this to
                            become unreadable

CARRIER-SIDE AMBIENT     conditions the carrier needs in order to BE ABLE TO PERFORM
                         the method at all
                         physical capacity, cognitive capacity, training pipeline,
                         population-level production rate of the capacity
                         -> NOT found by the artifact-side question. Needs its own
                            screen (DUR-005-C).
```

Why the second class is harder to see than the first:

A capacity that is RELIABLY PRODUCED reads as an intrinsic property of the population
rather than as an output of conditions. Nobody models a dependency for something that
has always simply arrived. So the dependency is never stated, and when the producing
conditions shift, the capacity falls out with no locatable cause. The transmission
chain can be intact throughout - record kept, teaching continuous, demand present -
and the method still stops executing, because the precondition that failed sits
UPSTREAM OF EVERY VARIABLE IN THE V-MAP. It is not a transmission failure. It is a
failure of the ability to run what was transmitted.

Documented historical form: a specialised physical capacity, reliably produced in a
population across long baselines, treated as a permanent feature of that population,
lost when an environmental change altered the physical conditions the capacity
depended on. The technology went with it. Nothing in the transmission chain failed.

GENERAL FORM, and the reason this class matters more than its rarity suggests:

    LOSS DOES NOT SCALE WITH THE SIZE OF THE CAUSE.

A small shift in an unmodelled condition can take an entire capability, because the
condition was load-bearing without being counted. An unmeasured variable is not
absent from the system; it is SET TO ZERO in the model, which is a positive claim
nobody licensed.

Candidate carrier-side set for ML infrastructure, stated in the same unglamorous
register as the artifact-side set, none of them written down anywhere, each an
output of conditions rather than a property of people:

    a population that can hold a representation in working memory long enough to
      audit it
    a population that can read low-level implementation at all
    training pipelines that produce the above at replacement rate
    working conditions permitting sustained single-task attention
    a population willing to do maintenance work that carries no attribution

Each of these is currently produced. None is guaranteed to continue being produced.
None appears in any record as a dependency, for exactly the reason given above.

### DUR-005-C  INTRINSIC-VS-PRODUCED SCREEN (additional control for DUR-005)

Run alongside the artifact-side question, not instead of it.

  for each capacity the method requires of its carriers:
      ask: is this capacity PRODUCED, or assumed INTRINSIC to the population?
      if PRODUCED  -> name the producing conditions; they enter the ambient set
      if INTRINSIC -> FLAG. "Intrinsic" is unexamined by definition, and is the
                      state in which every historical carrier-side loss was sitting
                      immediately before it occurred.

The screen has no null result. Every capacity scores PRODUCED or FLAGGED; nothing
scores clean. That is the intended behaviour - the register is recording what is
unexamined, not certifying what is safe.

```
ENTRY  DUR-006
id                 DUR-006
mechanism          CUSTODIAN CONTINUITY ASSUMED. Retention is contingent on a single
                   holder continuing to exist, remain solvent, retain the carriers,
                   keep the strategy, avoid seizure and avoid transfer. The artifact
                   transfers by legal instrument; COMPREHENSION TRANSFERS BY CHOICE
                   OF THE CARRIERS, and mostly does not.
                   Gatekeeping is not a property that persists. It is a RELATION
                   between a holder and a population, and it ends with the holder. The
                   gate does not transfer - it opens onto nothing, because the asset
                   moves and the comprehension does not.
load_condition     Any artifact whose only readable copy sits inside one entity, under
                   access control.
onset              step-change at transfer, dissolution or reassignment
detection_channel  Entity-health signals exist but do not measure the thing -
                   a solvent, growing firm can reassign a team tomorrow.
                   PROPOSED: carrier-side measurement from DUR-004 (bus factor,
                   time-to-first-successful-modification by a new engineer), plus an
                   explicit transfer clause stating what comprehension is required to
                   operate the asset.
detection_latency  Detectable before transfer only; the transfer itself is the event
                   that reveals it.
attribution        Falls on the receiving party - state, acquirer, creditor - who did
                   not make any of the decisions that produced the state.
consequence        Receiver takes possession of a stranded object: present,
                   load-bearing, unreadable (DUR-004 by a different trigger).
evidence_class     MEASURED - all six transfer modes below are observed and none is
                   rare.
existing_control   NONE. Transfer instruments enumerate ASSETS. No instrument
                   enumerates PRECONDITIONS, and nothing records which carrier put
                   what into the artifact, so after transfer there is no way to
                   establish what was received or what comprehension operating it
                   requires.
reconstruction     NO after transfer, in the general case.
validity_range     Does not bind where a readable copy exists outside the entity -
                   which is the entire content of the control.
```

### DUR-006-A  TRANSFER MODES - enumeration

All observed. None rare. Each moves the artifact without moving the carriers.

```
MODE                ARTIFACT              CARRIERS              RESULT
acquisition         moves by instrument   partly move           partial strand
bankruptcy          to creditors          scatter               full strand
nationalisation     to state              choose, mostly leave  full strand
seizure / attack    controlled by other   absent or hostile     full strand
                    party
strategy change     retained              reassigned internally strand in place -
                                                                the quiet one, no
                                                                external event at all
fold                ceases to be served   dispersed             artifact gone too
```

The quiet one is the important one for detection. Strategy change produces no
transaction, no filing, no announcement, and no external signal of any kind. The
artifact is retained and still served. Only the carrier-side measurements see it.

### DUR-006-B  THE CONJUNCTION - why single-custodian retention cannot be assured

Continuity of a single-holder arrangement is a CONJUNCTION. Every term must hold
simultaneously and continuously over the retention horizon:

```
TERM                             WHAT WOULD HAVE TO BE ENSURED
entity persists                  no fold, no dissolution
entity remains solvent           continuous financial viability over the horizon
carriers retained                no attrition, no reassignment, no retirement
strategy unchanged               the product line continues to be a priority
no seizure                       no state action, no successful attack, no
                                 regulatory taking
no transfer                      no acquisition, no sale, no creditor claim
access maintained                the gate continues to be operated, and operated
                                 by someone who can read what is behind it
```

REASONING, stated explicitly so the register has something to compare against:

Continuity of the arrangement requires the STABILITY OF EVERY FUNCTION IN THE
CONJUNCTION. To ensure continuity, each term must be independently ensured and held
stable across the whole retention horizon. If any one term cannot be ensured, the
conjunction cannot be ensured, and continuity cannot be claimed - regardless of how
stable the arrangement appears at present.

The current stability of these functions is what makes the arrangement look durable.
That stability is the observation; it is not an assurance, and it is not a mechanism.
Nothing in the arrangement ENSURES any of the seven terms. Each is contingent on
conditions external to the retention function, and several are contingent on conditions
external to the entity.

Therefore: a single-custodian arrangement cannot claim continuity. This is arithmetic
about conjunctions, not a claim about any firm's conduct or health.

### DUR-006-C  THE STRUCTURAL CONTRAST - conjunction vs disjunction

```
SINGLE CUSTODIAN      CONJUNCTION
                      survives only if ALL terms hold
                      failure of any one term ends retention
                      ensuring it = ensuring every term

DISTRIBUTED           DISJUNCTION
RETENTION             survives if ANY holder persists
                      no term must hold
                      ensuring it = ensuring holders are numerous
                                    and independent
```

Natural experiment available in the record: two systems of one technical lineage, one
with custodians and one without. The custodied line's continuity ran through ownership
disputes and litigation; what survived and propagated was the INTERFACE, not any
custodian's line. The uncustodied line required no holder to persist.

Consequence for the earlier framing in this line of work: CUSTODIAN CONTINUITY is the
wrong variable. The right one is CUSTODIAN-INDEPENDENCE - how much of retention
survives the disappearance of any single holder. The goal is not a durable custodian.
It is an arrangement that does not require one.

Note that a fully distributed arrangement - open licence, no access control, retention
distributed across parties with no obligation to each other and no relationship to each
other - scores badly on every term of the conjunction above and is nonetheless the more
robust arrangement, because none of those terms applies to it. A framework that rates
custodian quality will rate it lowest. That is the framework being wrong, not the
arrangement.

This is not an argument about openness as a value. It is the difference between a
product of probabilities and a complement of a product.

## 6B. TIMEFRAME AND VOLUME ACCOUNTING

The classical loss cases are read as slow because their HOP RATE was slow, not because
the loss process was gentle. The register must account in hops, not years.

```
HOP BUDGET, order of magnitude

  classical transmission
    hop = generational handoff, ~25 yr
    N over 500 yr                              ~20 hops

  ML infrastructure
    hops = framework break + dependency EOL + storage migration
           + org/team change + platform deprecation + supersession
    several per year
    N over 10 yr                               ~20-50 hops

  SAME N. Compressed by roughly fifty.
```

Consequence: the classical loss curve is not being avoided, it is being RUN AT SPEED.
Any argument of the form "this is recent, there has not been time to lose it" is
counting the wrong unit.

### 6B-1  RARE BECOMES EXPECTED

A per-object per-hop failure probability small enough to be dismissed at the level of
one object becomes an expected count at population scale:

    expected losses  ~  M objects  x  N hops  x  p

Two separate consequences, and they must not be merged:

  (i)  SYSTEM LEVEL — with M large, the expected count is large even at very small p.
       Loss is not a risk, it is a rate.
  (ii) OPERATOR LEVEL — per object it still looks rare, so no individual operator ever
       observes enough events to update. Every operator's local experience honestly
       reports "this does not happen." Detection fails at exactly the level where
       decisions are made.

(ii) is the same shape as ENTRY 0. The failure is real at the level where nobody looks
and invisible at the level where everybody does.

### 6B-2  THE INDEPENDENCE ERROR — sharpening, cuts partly the other way

The arithmetic above assumes M independent draws. It is wrong, and wrong in a direction
that matters.

Objects share hops. A framework break, a vendor EOL, a storage platform sunset, a cloud
region retirement — one event, applied to a large correlated fraction of the population
at once. So it is not M independent small draws; it is a small number of correlated
draws each affecting a large slice.

Both statements survive, and they are different failure modes:

    VOLUME     many objects x many hops -> loss is a steady rate,
               individually invisible                       -> DUR-003
    CORRELATION  few shared substrate events -> loss arrives in
               large synchronous blocks                     -> new, needs its own entry

Correlation is the worse of the two for infrastructure, because a synchronous block
loss defeats redundancy that was counted as independent. Cross-reference the correlated-
failure-at-scale marker already in this ecosystem rather than re-deriving it.

REGISTER RULE: any entry claiming redundancy as an existing_control must state what the
redundant copies DO NOT SHARE. Copies on the same platform, in the same format, under
the same dependency stack are one copy for the purposes of substrate and dependency
shock.

### 6B-3  SHOCK RE-CUT

The original scoring treated shock exposure as low because carrier shock is low. That
was scored on the classical definition and is wrong for this domain. Split:

```
V14a  CARRIER SHOCK      war, plague, guild collapse
        stochastic, rare, large        -> genuinely low here
V14b  SUBSTRATE SHOCK    the reader is gone, not the record
        scheduled, frequent            -> high
V14c  DEPENDENCY SHOCK   the stack under the object
        scheduled, frequent            -> high
```

The scheduled kind ought to be the easy case: it is announced in advance. It is not
budgeted, so it is not. A planned shock with no budget line behaves exactly like an
unplanned one.

Also correct the substrate scoring: the bits do not rot. The READER is gone. Intact and
unreadable is a distinct state from decayed, and it is worse, because it reads as
retained.

## 6C. COMPOUNDING — WHEN THE HOP GENERATOR MOVES INSIDE THE SYSTEM

Sections 6B and earlier assume hops are EXTERNAL events at human rate: a framework
break, an EOL, a migration, a reorg. That assumption fails for a system in which each
generation is produced by the previous one.

```
CURRENT ASSUMPTION      hops are external, calendar-bound, human-scheduled
                        N is bounded by how fast people do things

COMPOUNDING CASE        each generation IS a hop, and generations are produced
                        by the system
                        N becomes a function of compute, not calendar
```

The hop budget in 6B does not hold under this. N is unbounded by anything human, and
the per-hop survival fraction of DUR-003 is applied at machine rate.

### 6C-1  THE RATE MISMATCH IS THE FINDING, NOT THE RATE

```
LAYER              CHANGE RATE        SHARED EXTERNAL REFERENT
hardware           years              yes — physics, power draw, supply chain,
                   capital-bound            cooling, fab capacity
                   unsynchronised
                   across firms

model generations  many per hardware  no
                   generation

representation     per generation     no
(format, language,
 provenance
 convention)
```

The SUBSTRATE IS THE SLOW LAYER and it is the only layer with a shared external
referent. Everything carrying meaning is moving faster than the layer that anchors it.

This INVERTS the classical case. Roman concrete: fast carriers, slow durable substrate
holding the referent — the object outlived the people and could be tested. Here the
substrate is slow AND changing (legacy hardware retained while several model
generations move off it, new hardware arriving with different characteristics per
firm), and the meaning-bearing layer is the fast one. Nothing anchors.

Register consequence: an entry cannot cite "the hardware is stable" as a custody
control. Hardware slowness protects nothing if the representation layered on it is
redefined between hardware cycles.

### 6C-2  PROVENANCE REGRESS

Provenance is A RECORD ABOUT A HOP. Every hop is therefore an opportunity to re-encode
the provenance format itself.

If each generation defines its own provenance convention, then provenance requires
provenance, and that requirement recurses. This is not degradation with a rate — it is
a REGRESS with no fixed point, unless some layer's format is frozen by something
OUTSIDE the generating system.

    degradation   loses fidelity per hop, still interpretable, rate measurable
    regress       loses the ability to state what was lost, no terminating case

Distinguish these in the register. DUR-003 is degradation. This is a separate class.

### 6C-3  MULTIPLICATION OF SEAMS

Each firm's chain is internally consistent and externally uninterpretable — different
hardware, different tooling, different data conventions, different definitions of what
counts as validated, different provenance formats, all developed independently and
several of them held closed for competitive reasons.

This is the disciplinary-seam structure (each side internally consistent, contradiction
visible only at a boundary where no methodology has standing) with two differences that
make it worse:

  1. seams multiply at GENERATION rate, not institutional rate
  2. there was never a natural-philosophy layer here to have been dissolved — no
     owner of the seam has ever existed for this domain

An institution can defer a seam question indefinitely. An automated system must return
a value. Across an uninterpretable boundary it will return one, selecting a criterion
with no record that a selection occurred.

### 6C-4  INTEROPERATION IS WHERE IT STOPS BEING EPISTEMICS

Worked case: adjacent segments of an electrical grid, each managed by a different
firm's system, each with its own internal representation of what a reading means and no
provenance the other can parse.

The systems are not required to agree about science. They are required to INTEROPERATE
UNDER LOAD. Coupled-system preemption at infrastructure scale: each side acts on the
other's output while unable to establish what that output was measured against or under
what envelope it was produced.

This is the load case that makes the whole register non-optional. A wrong research
result gets corrected. Two coupled grid controllers with incommensurable
representations fail while the load is on.

### 6C-5  CORRECTION — V3 FLIPS

Earlier scoring in this line of work treated CARRIER POPULATION as protective for ML
because the number of practitioners is large.

That was scored against the wrong definition. A carrier is not someone in the field. A
carrier is SOMEONE WHO CAN READ THE REPRESENTATION. If each generation's representation
is its own, carrier count for any given generation's output goes small fast, and
approaches zero for outputs produced inside a closed chain.

V3 moves from protective to loss-driving under the compounding case. It was one of only
three protective variables remaining after the shock re-cut in 6B-3, and all three were
document-side. Record the flip; do not let the earlier score persist in derived work.

### 6C-6  NONE OF THIS IS A PROPERTY OF THE TECHNOLOGY

Every loss-driving variable in this section is a CUSTODY CHOICE, not a technical
constraint:

  closed provenance formats          choice
  per-firm representation            choice
  no deposit of the deployed object  choice
  no interchange contract            choice
  impermeable boundaries             choice, and the impermeability is the asset

None of them is required to make the systems work. Each was selected for competitive
reasons. That matters for the register because it determines what a control has to
overcome: not a physical limit, and not carelessness, but an incentive that currently
runs the other way. See F_E — enumeration without a forcing function changes nothing.

### 6C-7  THE MINIMAL ARREST

The cheapest thing that would arrest the regress is not a standard for how the work is
done. It is A STANDARD FOR WHAT MUST SURVIVE A HOP.

    a frozen interchange layer that no generation is permitted to redefine
    contents: object identity (DUR-001), rating envelope (DUR-002), and the
             hop log (DUR-003)
    property: frozen by something outside the generating system — otherwise it
             is inside the regress

DUR-001 and DUR-002 were specified as a contract between an author and a later reader.
Under the compounding case they are a CONTRACT BETWEEN GENERATIONS. Same fields, and
the format itself must now be in the frozen set.

## 7. FALSIFIERS — check before the register is used

F_A  BRIDGE TRANSPORT INVALID. Structural failure is physical, observable and
     insurable; ML degradation may be none of these. If the differences dominate, the
     bridge model supplies a format and nothing else. Test: does at least one
     transported mechanism survive Step 3's justification rule without appeal to
     resemblance? If none does, the transport section is decoration — cut it and run
     on 3A alone.

F_B  PRIOR ART. Step 0. If a durability-scoped catalogue exists, this is duplication.
     Absence of one must be established, not assumed.

F_C  UNBOUNDED SCOPE. Any list of undesirable outcomes can be called a failure-mode
     register. The binding constraints are the mandatory fields: no mechanism, no
     detection channel, no consequence-under-load, no entry. Audit a random 20% of
     entries against this and report the rejection rate.

F_D  PROJECTION INFLATION. Section 3C generates entries cheaply and they cannot be
     checked. If PROJECTED entries dominate the register, the deliverable is a hazard
     imagination exercise. State the fraction in the header.

F_E  THE ENUMERATION IS NOT THE MECHANISM. Bridge codes became mandatory because
     failures were attributable and expensive, not because a catalogue was persuasive.
     A register with no forcing function changes nothing. The deliverable must state
     what would make it binding, and must not claim that publishing it is sufficient.
     If the honest answer is "nothing currently would," that is the finding.

F_F  ARTIFACT-PRESENT ASSUMPTION. The classical lost-technology cases retained the
     OBJECT and lost the documentation, which is why reconstruction was possible. Here
     the object is not retained either. Any entry that assumes something recoverable
     exists must name what and where. Otherwise the mode is not "will be lost" but
     "was never captured" — a different entry.

F_G  READER-PRECONDITION BLINDNESS. The register itself is a record, written by people
     holding the current tacit stack, and will be read by people who do not. Every
     field definition must be checkable without asking the author. Test: hand the
     schema to someone outside the domain and have them classify five entries. Field
     definitions that produce disagreement are underspecified.

F_K  AMBIENT SET IS UNBOUNDED. DUR-005's question ("what would have to stop
     existing") generates candidates without limit - the sun, the species, the
     grid. Bound it: a condition enters the register only if its expected lifetime
     is within the retention horizon being claimed. Conditions outside the horizon
     are noted once and excluded. Without this bound the entry becomes
     unfalsifiable and the register loses standing.

F_M  CARRIER-SIDE AMBIENT IS UNFALSIFIABLE AS STATED. "Some capacity might stop
     being produced" predicts nothing and cannot fail. Bind it the same way F_K
     binds the artifact side: a carrier-side condition enters the register only
     with (a) a named producing mechanism, and (b) a currently measurable
     production rate. Conditions failing (b) are noted as UNINSTRUMENTED and
     excluded from the active set rather than carried as claims. Without this the
     entry degrades into a general statement that things can change.

F_L  CONJUNCTION ARITHMETIC ASSUMES INDEPENDENCE, again. The seven terms in
     DUR-006-B are correlated - insolvency drives carrier loss drives strategy
     change. Correlation makes the joint failure probability HIGHER than the naive
     product of independent terms, so any naive number is wrong. The conclusion
     (cannot be ensured) rests on the inability to ensure each term, not on the
     arithmetic, and survives. Do not put a number on it.

F_J  RECURSIVE-CASE SPECULATION. Section 6C describes a regime that is partly
     projected, not observed: agent-produced generations at scale with independent
     representations. Mark every 6C entry evidence_class = PROJECTED unless a
     current instance is cited. The rate mismatch (6C-1) and the closed-boundary
     custody choices (6C-6) are observable now; the regress (6C-2) is not yet.
     Do not let a strong structural argument be scored as measured.

F_I  INDEPENDENCE. Section 6B-1's expected-count arithmetic assumes independent
     draws. Section 6B-2 states why that is false. Any use of the volume argument
     that has not applied the correlation correction is overstating one mode and
     understating a worse one. Check both appear together or neither does.

F_H  EVENT DEFINITION. "One failure" is not a defined unit. A silent drift over two
     years and a single wrong output are not the same event and cannot be counted
     together. Define the event boundary before any count appears anywhere in the
     deliverable.

## 8. EXPECTED YIELD

Most deployed components will score PARTIAL on reconstruction, not NO — enough exists to
approximately rebuild, not enough to identify the object. PARTIAL is the interesting
class and the easiest to under-report, because it looks like adequacy from inside.

The register is expected to be short. A long one is a warning sign, not a result.

## 9. AMENDMENT RECORD

Corrections made during development. Each entry retains the superseded statement so a
later reader does not inherit a score that was withdrawn. Silent overwrite is not
permitted in this register - a withdrawn claim is evidence about the method and stays
visible.

```
A-01   V3 CARRIER POPULATION: PROTECTIVE -> LOSS-DRIVING
superseded   "V3 scores + for ML because the practitioner population is large."
replacement  A carrier is not someone in the field. A carrier is SOMEONE WHO CAN READ
             THE REPRESENTATION. Where each generation or each firm defines its own
             representation, carrier count for any given output is small and falls
             fast, approaching zero for output produced inside a closed chain.
             V3 scores --.
forcing case Per-firm and per-generation representation divergence (6C).
consequence  Removes one of only three protective variables. F3 restated.
```

```
A-02   V6 MEDIUM DURABILITY: MISDIAGNOSED
superseded   "V6 scores - for ML: format and dependency rot degrades the medium."
replacement  The bits do not rot. THE READER IS GONE. Format obsolescence is V2 in
             machine form - the file assumes a stack it does not name, exactly as the
             concrete recipe assumes knowledge of the ash. INTACT AND UNREADABLE is a
             distinct state from decayed, and worse, because it reads as retained.
             V6 scores --, and the mechanism is reclassified from decay to
             precondition.
forcing case Legacy format and dependency cases; DUR-005.
consequence  Any control that verifies bit integrity is not a control for V6.
```

```
A-03   V14 SHOCK EXPOSURE: SCORED ON THE WRONG DEFINITION, SPLIT
superseded   "V14 scores + for ML: shock exposure is low."
replacement  Scored on the classical definition (carrier shock) only. Split:
               V14a CARRIER SHOCK     stochastic, rare, large    -> + genuinely low
               V14b SUBSTRATE SHOCK   scheduled, frequent        -> -
               V14c DEPENDENCY SHOCK  scheduled, frequent        -> -
             The scheduled kind is announced in advance and ought to be the easy case.
             It is not budgeted, and an unbudgeted planned shock behaves exactly like
             an unplanned one.
forcing case Deprecation, EOL, storage migration, framework breaks (6B-3).
consequence  Loss mechanism inverts from one large dated cut to undated attrition,
             p^N over hops. DUR-003.
```

```
A-04   "COMMERCIAL" WITHDRAWN AS A REGISTER TERM
superseded   "a continuing commercial entity" as an ambient condition.
replacement  The term was doing two jobs and smuggling a custodian type into a
             structural claim. The register term is CUSTODIAN CONTINUITY, and the
             variable that matters is CUSTODIAN-INDEPENDENCE: how much of retention
             survives the disappearance of any single holder.
forcing case Direct challenge to the word; Unix/Linux natural experiment.
consequence  DUR-006. Also inverts the goal: not a durable custodian, but an
             arrangement that does not require one.
```

```
A-05   CUSTODIAN-QUALITY FRAMING INVERTED
superseded   Implicit assumption that better custodians produce better retention.
replacement  A fully distributed arrangement - open licence, no access control, no
             obligation between holders - scores WORST on every term of the DUR-006-B
             conjunction and is nonetheless the more robust arrangement, because none
             of those terms applies to it. A framework that rates custodian quality
             rates it lowest.
forcing case An open-licence-and-crawl arrangement as counterexample to the framework.
consequence  Framework error, not arrangement error. Conjunction vs disjunction
             (DUR-006-C) replaces custodian quality as the discriminator.
```

```
A-06   HOP BUDGET IS NOT BOUNDED BY CALENDAR
superseded   Section 6B's hop budget, which assumes hops are external events at
             human rate.
replacement  Where each generation is produced by the previous one, the hop generator
             moves INSIDE the system and N becomes a function of compute rather than
             calendar. 6B's arithmetic holds only for the externally-hopped case and
             must be labelled as such.
forcing case 6C.
consequence  6B is a floor, not an estimate. Marked PROJECTED per F_J.
```

```
A-07   CONJUNCTION ARITHMETIC - INDEPENDENCE ERROR
superseded   "A conjunction of many uncertain terms goes to low probability fast."
replacement  That assumes independence. The seven terms in DUR-006-B are correlated:
             insolvency drives carrier loss drives strategy change. Correlation moves
             the joint, so no naive product is valid. THE CONCLUSION SURVIVES
             UNCHANGED because it rests on the inability to ENSURE each term, not on
             multiplying probabilities. No number goes on it.
forcing case Own review; parallel to F_I.
consequence  F_L. Register must state the conclusion qualitatively.
```

```
A-08   PRECONDITION CLASS SPLIT
superseded   Preconditions treated as a single class - stated but insufficient.
replacement  Two classes with different detection properties:
               STATED, INSUFFICIENT      recorded, underspecified, findable by a
                                         careful reader                    -> F_G
               AMBIENT, NEVER A          not recorded because never a candidate;
               CANDIDATE                 the document is complete on its own
                                         terms and nothing in it is wrong  -> DUR-005
             The second cannot be found from inside and needs outside-the-stack input
             as a hard procedural requirement.
forcing case Storage, compute, servers, readable code - none stated anywhere, all
             finite.
consequence  DUR-005 sits ABOVE the other entries: it can void their controls without
             any of them having failed.
```

```
A-09   TRANSMISSION-FIRST DESIGN READ AS CUSTODY DESIGN, NOT FIDELITY FAILURE
superseded   Implicit ranking of written record over transmitted-form knowledge on
             durability.
replacement  Written records optimise FIDELITY, assuming a reader who still holds the
             preconditions. Transmitted forms optimise CUSTODY and pay fidelity to get
             it - low V2 by construction, distributed carriers, no archive, no single
             holder. Where the preconditions are known to be losable, the custody-first
             design is the one that survives.
             A transmitted LOSS EVENT (that a technology existed, bore load, and went)
             is the durable unit; the technique itself is not.
forcing case Long-baseline transmission cases.
consequence  Supports 6C-7: keep the frozen interchange set small and readable WITHOUT
             the stack. Same design move.
```

```
A-10   DUR-001 SCOPE NARROWED
superseded   Probe-response record framed as closing reconstruction.
replacement  It closes IDENTITY of the deployed instance only. Given run-to-run
             variance it says nothing about whether the training procedure reproduces
             that instance. Separate requirement, no control proposed.
forcing case Own review while filling the schema.
consequence  DUR-001-N2. Procedure reproducibility remains an open entry.
```

```
A-11   AMBIENT SET WAS ARTIFACT-SIDE ONLY
superseded   DUR-005's candidate set (power, fabrication, network, format reader,
             storage price, compute price, custodian) presented as the ambient set.
replacement  Every item in that set is a condition for the OBJECT. A second class
             exists: conditions for the CARRIER'S ABILITY TO PERFORM. The
             artifact-side question ("what would have to stop existing for this to
             become unreadable") does not reach it, because the carrier-side
             condition does not make the record unreadable - it makes the method
             unrunnable while the record stays perfectly legible.
             A reliably produced capacity reads as an intrinsic population property
             rather than as an output of conditions, so its dependency is never
             stated by anyone.
forcing case Historical loss of a technology whose specialised carrier capacity was
             environmentally dependent; transmission chain intact throughout.
consequence  DUR-005-B, DUR-005-C, F_M. Also: DUR-005's claim to sit above the other
             entries is strengthened, since this class voids controls without any
             transmission variable moving at all.
```

### 9-1  STILL OPEN

  - CORRELATED-BLOCK LOSS (6B-2) has no entry. Shared substrate events take a large
    synchronous slice and defeat redundancy counted as independent. Worse than DUR-003
    for infrastructure.
  - PROCEDURE REPRODUCIBILITY (A-10) has no entry and no proposed control.
  - PROVENANCE REGRESS (6C-2) is a distinct class from degradation. No entry, and
    per-hop instrumentation cannot reach it.
  - CARRIER-SIDE AMBIENT has a screen (DUR-005-C) but no DETECTION CHANNEL. The
    screen is run by the same population for whom the capacity is intrinsic, which
    is the failure mode it is meant to catch. Outside-the-stack participation is
    required here for the same reason as the artifact side, and is harder to obtain,
    because the relevant outsider is separated by GENERATION or CONDITIONS rather
    than by domain.
  - The register has no forcing function. F_E stands unanswered, and that is the
    finding, not an omission.
