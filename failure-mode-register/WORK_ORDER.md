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
