# DURABILITY AND RECONSTRUCTION FAILURE-MODE REGISTER FOR ML AS INFRASTRUCTURE

License: CC0. Deliverable is a REGISTER, not a paper.
Status: draft register, six entries, prior-art gate passed.

---

## 0. SCOPE

Bridge engineering has as-builts, material provenance, load ratings and inspection
intervals. Not because engineers are careful — because failure modes were ENUMERATED
AFTER THINGS FELL DOWN, and the enumeration became mandatory.

ML systems are being placed in load-bearing positions with no equivalent enumeration.

```
IN SCOPE     can the deployed object still be identified, re-produced,
             load-rated and inspected at t+N years, by someone who is not
             the original author and does not hold the tacit stack

OUT OF SCOPE model behaviour, alignment, misuse, harm incidents, ethics
```

### 0-1  PRIOR-ART GATE (F_B) — RESULT

Searched 2026-09-13. No durability-scoped catalogue found. Four adjacent artifacts
exist; each misses on a stated axis. Verify before citing.

```
ARTIFACT                             SCOPE                        MISSES
Microsoft ML failure-mode taxonomy   intentional vs unintentional custody, rebuild
(arXiv 1911.11034)                   failure; security and harm;
                                     declines to prescribe
                                     mitigations

LLM system-level taxonomy,           production reliability;      identifiability,
15 hidden failure modes              names VERSION DRIFT and      deposit,
(arXiv 2511.19933)                   REPRODUCIBILITY directly;    reconstruction
                                     states benchmarks give
                                     little insight into
                                     stability/reproducibility/
                                     drift
                                     -> CLOSEST PRIOR ART. CITE.

ML research cluster reliability      hardware/job failure during  post-deployment
(arXiv 2410.21680)                   training; MTTF at GPU scale  custody

generic engineering taxonomies       irreproducible-execution     not applied to ML
                                     condition, unmodelled
                                     runtime environment
                                     -> ambient-adjacent, see DUR-005
```

GATE RESULT: not redundant. Residual scope is custody, identifiability, reconstruction.
The LLM taxonomy must be cited as prior art on drift so this register claims no novelty
it does not have.

### 0-2  ENTRY 0 — THE DETECTION GAP ITSELF

A bridge catalogue is buildable because failure is OBSERVABLE, DATED and LOCATED.
Something falls down; the event forces the entry.

An ML infrastructure failure may produce NO EVENT. Degradation appears as slightly
worse decisions distributed across a population, attributed at the last hop to whoever
was holding the output.

Every entry therefore carries a DETECTION CHANNEL field, permitted to be NONE.
Entries with DETECTION = NONE are the HIGH-PRIORITY SET: they cannot generate the
evidence that would make them mandatory to fix. That is the mechanism by which the
enumeration fails to get written at all.

---

## 1. LOSS-VARIABLE MAP

Variables under which a technology is lost, derived from historical cases, scored for
ML infrastructure. Amended scores are authoritative; originals retained in Section 8 so
the correction is auditable.

```
V1   ARTIFACT RETENTION     does a physical instance outlive the record
V2   PRECONDITION LOAD      how much tacit stack the record assumes in its reader
V3   CARRIER POPULATION     number who can READ THE REPRESENTATION
V4   CARRIER TURNOVER       replacement rate vs time to transmit
V5   REGENERATION CYCLE     how often it is re-taught or re-performed
V6   MEDIUM DURABILITY      substrate readable at t+N
V7   COPY MULTIPLICITY      number of independent custodians
V8   ACCESS GATING          deliberate closure — guild, classified, proprietary
V9   DEMAND CONTINUITY      is the load still on it
V10  SUBSTITUTION RATE      replacement arriving before predecessor is recorded
V11  IDENTIFIABILITY        can you tell which object the record describes
V12  RECONSTRUCTION TEST    can a candidate rebuild be VERIFIED as correct
V13  INDEXABILITY           findable again, under a name still in use
V14  SHOCK EXPOSURE         events cutting carrier population at once
```

`+` protects, `-` drives loss.

```
        CLASSICAL CASES        ML INFRASTRUCTURE      AMENDED
V1      +  object survives     -- nothing deposited
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
V12     +  testable            -- see F1
V13     -  name lost           +  search works
V14     -- war, plague         +  low                    -> split A-03
```

### 1-1  THREE FINDINGS FROM THE COMPARISON

**F1 — THE VERIFICATION CHANNEL IS BLOCKED, NOT ONLY THE RECORD.**
Every classical recovery ran on V12: mix a candidate concrete, test it against the
surviving wall; a failed reconstruction is distinguishable from a successful one. With
run-to-run spread of the magnitude in 2-A, a reconstruction that misses the published
number is INDISTINGUISHABLE from a bad draw of the correct procedure. A missing test is
worse than a missing record.

**F2 — THE PROTECTIVE VARIABLE IS MAXED AND DOES NOT PROTECT.**
V9 is the usual reason things survive: continuous use forces continuous re-teaching.
Demand here is at maximum and it still loses, because V10 outruns documentation. Loss
is not by abandonment but by REPLACEMENT VELOCITY — the object is superseded before it
was captured. No classical analogue. "It is widely used, it will be fine" must not be
accepted as an existing_control in any entry.

**F3 — THE GOOD SCORES ARE ON THE WRONG VARIABLES.**
Wins after amendment are V7 and V13: copy cost and findability. Both protect DOCUMENTS.
Losses are V1, V4, V8, V10, V11, V12: all protect OBJECTS. The system is well built to
preserve what was written about the thing and poorly built to preserve the thing.
Original F3 listed V3 and V14 among the wins; both amended out. The protective set is
thinner than first scored and is entirely document-side.

---

## 2. ENTRY SCHEMA

An entry missing any field is an UNRATED PART, filed as such, not discarded.

```
id                 stable identifier
mechanism          how the failure happens, at mechanism level not instance level
load_condition     what must be true of the deployment for this to bite
onset              immediate | drift | dormant-until-triggered
detection_channel  what signal would reveal it, or NONE
detection_latency  onset to earliest possible detection, or UNBOUNDED
attribution        where blame lands by default when it surfaces (last hop)
consequence        what fails while load is on it
evidence_class     MEASURED (cite) | TRANSPORTED (name source domain + justify)
                   | PROJECTED (no anchor — flagged, lowest weight)
existing_control   what current practice does about it, or NONE
reconstruction     YES | PARTIAL | NO
validity_range     conditions under which this entry is claimed to hold
```

RULE: PROJECTED entries may not exceed a stated fraction of the register. A register
that is mostly projection is a speculation list wearing a register's format.

### 2-A  MEASURED SEEDS

Re-verify against primary sources before the register ships.

- run-to-run variance under identical configuration large enough that a single reported
  number does not identify the object produced
- software/dependency versions unstated in the overwhelming majority of reports, so
  exact re-execution is impossible in principle
- data leakage propagating across many studies and fields; corrected results erased
  claimed superiority over older statistical methods
- no agreed significance measure, so point estimates ship without a characterised
  distribution
- THE COMPOUNDING LINE: the defect is NOT VISIBLE FROM READING THE REPORT, because the
  report format lacks the fields that would expose it

### 2-B  TRANSPORT RULE

Each transported entry must state WHY the mechanism carries. A mechanism carries if the
abstract structure holds — a record insufficient to rebuild the object — not because the
domains feel similar. Transports resting only on analogy are rejected at review.

Source domains with mature enumerations and a forcing history: structural/civil,
aviation, pressure vessel, pharmaceutical, nuclear transport, civil records/archive.

Highest-value transports: the RETAINED REFERENCE SAMPLE (pharma) and the STAMPED
VALIDITY ENVELOPE (pressure vessel). Both cheap, both mandatory at home, neither exists
here.

---

## 3. ENTRIES

### DUR-001 — OBJECT NOT IDENTIFIABLE

```
mechanism          Deployed object cannot be distinguished from any other object
                   produced by the same nominal procedure. Run-to-run variance under
                   identical configuration is large enough that the reported number
                   does not identify which object was produced; after deployment,
                   substitution, patching or drift leaves no trace distinguishing the
                   current object from the documented one.
load_condition     Any deployment where the object is updated, re-served, migrated or
                   supplied by a party other than the evaluator.
onset              dormant-until-triggered — no symptom until a dispute or performance
                   question forces the identity question, at which point the referent
                   does not exist
detection_channel  NONE under current practice.
                   PROPOSED: sealed probe-response record — probe set fixed at deploy,
                   the deployed object's responses hashed, held by a party that is not
                   the operator. Third-party checkable without re-manufacture.
detection_latency  UNBOUNDED without the control. With it: one probe cycle.
attribution        Last hop. Whoever was holding the output when behaviour changed.
consequence        Any later claim about the deployed object is unverifiable. Silent
                   substitution, undeclared update and as-built drift are
                   indistinguishable from normal operation.
evidence_class     TRANSPORTED — pharmaceutical retained reference sample.
                   JUSTIFICATION: abstract structure is a record insufficient to
                   identify the object it describes, closed by retaining a small
                   referent taken BEFORE any problem is known, cheap relative to the
                   batch, testable by a third party without re-manufacture. All three
                   properties carry to a probe-response record. Same insufficiency,
                   same closure — not industry resemblance.
                   Partially MEASURED: variance and version-reporting defects in 2-A
                   establish the insufficiency directly.
existing_control   NONE.
reconstruction     NO as deployed. PARTIAL with the control — the control establishes
                   IDENTITY, not reproducibility (see N2).
validity_range     Holds where the object is served through a queryable interface.
                   Does not hold where probe queries are indistinguishable from
                   production load, or probe cost is not small relative to serving.
```

**N1 — PROBE LEAKAGE.** A public probe set gets trained against, after which it measures
probe performance rather than object identity. Sealed-and-hashed handles single-
deployment identity but not reuse across deployments. Requires rotation, or per-
deployment generation from a seed held by the third party. Control precondition, not a
footnote.

**N2 — INSTANCE vs PROCEDURE.** Given the variance, a probe response identifies the
DEPLOYED INSTANCE. It does not establish that the training procedure reproduces it.
Separate requirements; conflating them would let a deployment claim reconstruction
coverage it does not have. DUR-001 closes identity only.

### DUR-002 — RATING DOES NOT TRAVEL WITH THE OBJECT

```
mechanism          Object is applied outside the conditions under which its reported
                   performance was established, with no signal that this occurred. The
                   stated conditions, where they exist, are filed in a document
                   elsewhere rather than attached to the object at point of use, so the
                   operator applying load cannot read the rating.
load_condition     Any deployment where input distribution or decision consequence can
                   vary after evaluation. In practice: all of them.
onset              drift
detection_channel  NONE under current practice. Confidence scores do not serve — a
                   confident output inside a distribution the object was never
                   characterised on IS the failure, not a warning of it.
                   PROPOSED: stamped validity envelope attached to the serving
                   interface, machine-readable, carrying characterised input
                   distribution, decision consequence range, date, seed/variance basis.
                   Plus a RETURN CONTRACT: interface returns value AND rating status,
                   where OUT_OF_ENVELOPE is a distinct return state, not a low score on
                   a continuous confidence axis.
detection_latency  UNBOUNDED without the control. With it: immediate at call time.
attribution        Last hop — the operator who acted on the out-of-envelope output.
consequence        The system continues returning values while unrated, under load,
                   with no record that the envelope was exceeded or that a criterion
                   was selected in the absence of one.
evidence_class     TRANSPORTED — pressure vessel stamped plate.
                   JUSTIFICATION: a rating that exists but does not travel with the
                   object, unreadable at the point where load is applied. Structurally
                   identical. Carried discipline is the sharp one: OUTSIDE THE ENVELOPE
                   THE VESSEL IS UNRATED — not degraded, not derated, unrated.
existing_control   PARTIAL. Model cards and documentation exist, but are filed
                   alongside rather than attached, are not machine-readable at call
                   time, and carry no return contract. Scored PARTIAL, not NONE —
                   null-set discipline, Section 6 Step 7.
reconstruction     Not applicable directly. DUR-002 governs USE, not rebuild. It is the
                   load rating, not the as-built.
validity_range     Requires the input distribution to be characterisable. Where it is
                   not, the honest envelope is empty, and an empty envelope is itself
                   the rating.
```

**N1 — EMPTY ENVELOPE READ AS BROAD ENVELOPE.** An object with no characterised
distribution and an object characterised as broadly applicable are indistinguishable if
the field is left blank. Blank must be a distinct value from wide.

**COMPOSITION — the two do not work alone.**
```
envelope without sample   stated conditions cannot later be checked against what
                          was actually deployed
sample without envelope   responses with no stated conditions — data, not a rating
```
The probe set defines the envelope's interior; the envelope makes the probe record
interpretable. Register them as a coupled pair.

### DUR-003 — MIGRATION ATTRITION

```
mechanism          The object survives no single event, but is carried across repeated
                   hops — framework version breaks, dependency EOL, storage migration,
                   account and org changes, platform deprecation. At each hop a
                   survival fraction applies, and what is carried forward is selected
                   BY CURRENTLY PERCEIVED VALUE. Anything whose value appears later is
                   filtered out by construction.
load_condition     Any object whose retention depends on being actively carried rather
                   than passively held. All hosted, containerised or dependency-bound
                   artifacts.
onset              drift — compounding, p^N over N hops, no visible loss at any hop
detection_channel  NONE. Attrition is invisible per hop by definition; the object
                   dropped is not the object anyone is looking at.
                   PROPOSED: hop log. Every migration event records what was carried,
                   what was dropped, and by whose decision. Cheap, and it converts an
                   undated attrition into a dated one.
detection_latency  UNBOUNDED. Discovered only when something is needed and absent.
attribution        None available — no actor performed a loss. Each hop decision was
                   locally correct.
consequence        Reconstruction path degrades silently while all headline indicators
                   remain healthy.
evidence_class     TRANSPORTED — archive and records management, format obsolescence.
                   JUSTIFICATION: retention contingent on repeated active re-
                   commitment, with a per-hop selection filter that is not the
                   criterion the future reader will use. Identical structure,
                   different substrate.
existing_control   NONE at the artifact level.
reconstruction     Degrades from PARTIAL toward NO without any state change recorded.
validity_range     Holds where hop count over the retention horizon exceeds ~1. Does
                   not apply to objects deposited once with a custodian whose mandate
                   is retention rather than operation.
```
Distinguish from DUR-001. DUR-001 is "cannot tell which object." DUR-003 is "the object
is no longer being carried." Independent.

### DUR-004 — STRANDED UNDER LOAD

```
mechanism          The object is retained and still bearing production load, but the
                   carrier population that can read, modify, verify or replace it has
                   gone to near zero. Not lost — stranded. Artifact present, demand
                   maximal, comprehension absent.
load_condition     Long-lived deployment PLUS high carrier turnover PLUS high
                   precondition load. The combination, not any one term.
onset              drift, then step-change at the departure of the last carrier
detection_channel  WEAK but non-zero, unlike most entries here: bus-factor count,
                   time-to-first-successful-modification by a new engineer, failed
                   replacement attempts. Measurable today and not measured.
detection_latency  Detectable BEFORE failure if the above are instrumented; otherwise
                   at the first required change that cannot be made.
attribution        Whoever is holding it when a change is finally required, typically
                   years after the decisions that produced the state.
consequence        The system continues to work and cannot be altered. Every option
                   except continued operation closes. A live liability, unlike a lost
                   artifact with no load on it.
evidence_class     MEASURED by analogy in software generally — legacy systems with
                   present artifact, maximal load and near-zero carriers are an
                   observed current state, not a projection.
existing_control   NONE for ML specifically. General software practice has partial
                   controls (documentation mandates, rotation) with known poor
                   compliance.
reconstruction     NO. Reconstruction requires comprehension, the missing term.
validity_range     Applies where the object cannot be cheaply retrained or regenerated
                   from a specification. Where regeneration is cheap and the spec is
                   held, stranding does not bind.
```
INVERSE of the classical monument case. Pyramids: object retained, load off, gap
harmless. Stranded: object retained, load on, gap is the liability. The intuition that a
surviving artifact means a recoverable technology fails here.

### DUR-005 — AMBIENT PRECONDITION

Sits ABOVE the other entries: it can void their controls without any of them failing.

```
mechanism          The record is complete on its own terms and still unusable, because
                   the conditions under which the procedure ran were never candidates
                   for statement. Not underspecified — never specified, because nobody
                   holds "there will be servers" as an assumption. It is the condition
                   under which holding assumptions happens.
                   This is the mode that makes reconstruction attempts fail REPEATEDLY
                   ACROSS LONG PERIODS even where custody worked. The reconstructor is
                   not missing a step in the procedure. The reconstructor is missing
                   the world the procedure ran in, and the procedure gives no
                   indication that a world was required.
load_condition     Any record produced inside a stable operating environment — i.e.
                   all of them, which is why this entry sits above the others.
onset              dormant-until-triggered. No symptom until an ambient condition ends,
                   at which point the change is step, not drift.
detection_channel  NONE from inside. Ambient conditions cannot be enumerated by the
                   population for whom they are ambient, for the same structural reason
                   an exclusion register cannot be generated from inside the frame it
                   excludes from.
                   PROPOSED: ambient enumeration procedure below. Outside-the-stack
                   input is a HARD REQUIREMENT, not a nicety.
detection_latency  UNBOUNDED, and asymmetric: detectable cheaply BEFORE the condition
                   ends, not at all after.
attribution        None. No actor omitted anything.
consequence        Reconstruction fails even where deposit, custody and hop logging all
                   succeeded.
evidence_class     MEASURED historically (repeated failed reconstruction of lost
                   technologies where partial records survived); PROJECTED for the
                   specific ambient set below.
existing_control   NONE. Not addressed by reproducibility practice, which operates
                   entirely inside the ambient set.
reconstruction     NO, and undetectably so — the record looks complete.
validity_range     Holds wherever the reader is separated from the author by enough
                   time or environmental change that any ambient condition has ended.
```

**AMBIENT ENUMERATION PROCEDURE.**
Do not ask what is assumed — that returns the stated assumptions, already in the
document, and returns nothing ambient.

Ask: WHAT WOULD HAVE TO STOP EXISTING FOR THIS TO BECOME UNREADABLE?

- run with participants OUTSIDE the stack — different domain, different era of practice,
  different infrastructure assumptions. Someone for whom the condition is not ambient.
  Hard requirement; run internally it returns the stated set.
- output is a list of conditions, each with a finite expected lifetime
- record the list. Not a prediction — the world-state the record depends on, written
  down while it is still visible.

Candidate artifact-side set, none appearing in any paper, each with finite lifetime:

```
continuous power at current density and cost
fabrication capability at current tolerance
a network
a machine that reads the format at all
storage priced as effectively unlimited
compute priced as effectively unlimited
a continuing custodian                          -> DUR-006
```
The last three are assumptions about ECONOMICS AND INSTITUTIONS presented as technical
background. Least durable items on the list, least likely to be written down.

**DUR-005-B — TWO CLASSES OF AMBIENT CONDITION.**

```
ARTIFACT-SIDE   conditions the object needs to exist and be read
                power, fabrication, network, format reader, storage and compute
                price, a custodian
                -> found by: what would have to stop existing for this to become
                   unreadable

CARRIER-SIDE    conditions the carrier needs to BE ABLE TO PERFORM the method
                physical capacity, cognitive capacity, training pipeline,
                population-level production rate of the capacity
                -> NOT found by the artifact-side question. Needs DUR-005-C.
```

Why the second class is harder to see: a capacity that is RELIABLY PRODUCED reads as an
intrinsic property of the population rather than an output of conditions. Nobody models
a dependency for something that has always simply arrived. So the dependency is never
stated, and when the producing conditions shift, the capacity falls out with no locatable
cause. The transmission chain can be intact throughout — record kept, teaching
continuous, demand present — and the method still stops executing, because the
precondition that failed sits UPSTREAM OF EVERY VARIABLE IN THE V-MAP. Not a transmission
failure. A failure of the ability to run what was transmitted.

GENERAL FORM: **LOSS DOES NOT SCALE WITH THE SIZE OF THE CAUSE.** A small shift in an
unmodelled condition can take an entire capability, because the condition was
load-bearing without being counted. An unmeasured variable is not absent from the
system; it is SET TO ZERO in the model, which is a positive claim nobody licensed.

Candidate carrier-side set, each an output of conditions rather than a property of
people, none written down anywhere as a dependency:

```
a population that can hold a representation in working memory long enough to audit it
a population that can read low-level implementation at all
training pipelines that produce the above at replacement rate
working conditions permitting sustained single-task attention
a population willing to do maintenance work that carries no attribution
```

**DUR-005-C — INTRINSIC-VS-PRODUCED SCREEN.** Run alongside the artifact-side question,
not instead of it.

```
for each capacity the method requires of its carriers:
    is this capacity PRODUCED, or assumed INTRINSIC to the population?
    PRODUCED  -> name the producing conditions; they enter the ambient set
    INTRINSIC -> FLAG. "Intrinsic" is unexamined by definition, and is the state
                 in which every historical carrier-side loss was sitting
                 immediately before it occurred.
```
The screen has NO NULL RESULT. Every capacity scores PRODUCED or FLAGGED; nothing scores
clean. Intended behaviour — the register records what is unexamined, it does not certify
what is safe.

### DUR-006 — CUSTODIAN CONTINUITY ASSUMED

```
mechanism          Retention is contingent on a single holder continuing to exist,
                   remain solvent, retain the carriers, keep the strategy, avoid
                   seizure and avoid transfer. The artifact transfers by legal
                   instrument; COMPREHENSION TRANSFERS BY CHOICE OF THE CARRIERS, and
                   mostly does not.
                   Gatekeeping is not a property that persists. It is a RELATION
                   between a holder and a population, and it ends with the holder. The
                   gate does not transfer — it opens onto nothing, because the asset
                   moves and the comprehension does not.
load_condition     Any artifact whose only readable copy sits inside one entity, under
                   access control.
onset              step-change at transfer, dissolution or reassignment
detection_channel  Entity-health signals exist but do not measure the thing — a
                   solvent, growing firm can reassign a team tomorrow.
                   PROPOSED: carrier-side measurement from DUR-004, plus an explicit
                   transfer clause stating what comprehension is required to operate
                   the asset.
detection_latency  Detectable before transfer only; the transfer itself is the event
                   that reveals it.
attribution        Falls on the receiving party — state, acquirer, creditor — who made
                   none of the decisions that produced the state.
consequence        Receiver takes possession of a stranded object: present,
                   load-bearing, unreadable. DUR-004 by a different trigger.
evidence_class     MEASURED — all six transfer modes below are observed, none rare.
existing_control   NONE. Transfer instruments enumerate ASSETS. No instrument
                   enumerates PRECONDITIONS, and nothing records which carrier put what
                   into the artifact, so after transfer there is no way to establish
                   what was received or what comprehension operating it requires.
reconstruction     NO after transfer, in the general case.
validity_range     Does not bind where a readable copy exists outside the entity —
                   which is the entire content of the control.
```

**DUR-006-A — TRANSFER MODES.** All observed. None rare. Each moves the artifact without
moving the carriers.

```
MODE                ARTIFACT              CARRIERS               RESULT
acquisition         moves by instrument   partly move            partial strand
bankruptcy          to creditors          scatter                full strand
nationalisation     to state              choose, mostly leave   full strand
seizure / attack    controlled by other   absent or hostile      full strand
strategy change     retained              reassigned internally  strand in place
fold                ceases to be served   dispersed              artifact gone too
```
The quiet one is the important one for detection. STRATEGY CHANGE produces no
transaction, no filing, no announcement, no external signal of any kind. The artifact is
retained and still served. Only the carrier-side measurements see it.

**DUR-006-B — THE CONJUNCTION.** Continuity of a single-holder arrangement requires every
term to hold simultaneously and continuously over the retention horizon:

```
TERM                    WHAT WOULD HAVE TO BE ENSURED
entity persists         no fold, no dissolution
entity remains solvent  continuous financial viability over the horizon
carriers retained       no attrition, no reassignment, no retirement
strategy unchanged      the product line continues to be a priority
no seizure              no state action, no successful attack, no regulatory taking
no transfer             no acquisition, no sale, no creditor claim
access maintained       the gate continues to be operated, by someone who can read
                        what is behind it
```

To ensure continuity, each term must be independently ensured and held stable across the
whole horizon. If any one term cannot be ensured, the conjunction cannot be ensured, and
continuity cannot be claimed — regardless of how stable the arrangement appears now.

Current stability is the OBSERVATION. It is not an assurance and not a mechanism. Nothing
in the arrangement ENSURES any of the seven terms; each is contingent on conditions
external to the retention function, several external to the entity.

Therefore a single-custodian arrangement cannot claim continuity. This is arithmetic
about conjunctions, not a claim about any firm's conduct or health.

**DUR-006-C — CONJUNCTION vs DISJUNCTION.**

```
SINGLE CUSTODIAN   CONJUNCTION    survives only if ALL terms hold
                                  failure of any one term ends retention
                                  ensuring it = ensuring every term

DISTRIBUTED        DISJUNCTION    survives if ANY holder persists
RETENTION                         no term must hold
                                  ensuring it = ensuring holders are numerous
                                                and independent
```

Natural experiment in the record: two systems of one technical lineage, one with
custodians and one without. The custodied line's continuity ran through ownership
disputes and litigation; what survived and propagated was the INTERFACE, not any
custodian's line. The uncustodied line required no holder to persist.

CUSTODIAN CONTINUITY is the wrong variable. The right one is CUSTODIAN-INDEPENDENCE — how
much of retention survives the disappearance of any single holder. The goal is not a
durable custodian. It is an arrangement that does not require one.

A fully distributed arrangement — open licence, no access control, retention distributed
across parties with no obligation to each other — scores WORST on every term of the
conjunction and is nonetheless the more robust arrangement, because none of those terms
applies to it. A framework that rates custodian quality will rate it lowest. That is the
framework being wrong, not the arrangement.

Not an argument about openness as a value. The difference between a product of
probabilities and a complement of a product.

---

## 4. TIMEFRAME AND VOLUME ACCOUNTING

The classical loss cases are read as slow because their HOP RATE was slow, not because
the loss process was gentle. Account in hops, not years.

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

The classical loss curve is not being avoided, it is being RUN AT SPEED. Any argument of
the form "this is recent, there has not been time to lose it" is counting the wrong unit.

### 4-1  RARE BECOMES EXPECTED

```
expected losses  ~  M objects  x  N hops  x  p
```

Two consequences, not to be merged:

- **SYSTEM LEVEL** — with M large, the expected count is large even at very small p. Loss
  is not a risk, it is a rate.
- **OPERATOR LEVEL** — per object it still looks rare, so no individual operator observes
  enough events to update. Every operator's local experience honestly reports "this does
  not happen." Detection fails at exactly the level where decisions are made.

The second is the same shape as Entry 0: real at the level where nobody looks, invisible
at the level where everybody does.

### 4-2  THE INDEPENDENCE ERROR

The arithmetic above assumes M independent draws. Wrong, and wrong in a direction that
matters. Objects share hops — a framework break, a vendor EOL, a cloud region retirement
is one event applied to a large correlated fraction at once.

Both statements survive as different failure modes:

```
VOLUME       many objects x many hops -> steady rate, individually
             invisible                                        -> DUR-003
CORRELATION  few shared substrate events -> loss arrives in
             large synchronous blocks                         -> NO ENTRY YET
```

Correlation is the worse of the two for infrastructure: a synchronous block loss defeats
redundancy that was counted as independent.

REGISTER RULE: any entry claiming redundancy as an existing_control must state what the
redundant copies DO NOT SHARE. Copies on the same platform, in the same format, under the
same dependency stack are ONE COPY for substrate and dependency shock.

### 4-3  SHOCK RE-CUT

```
V14a  CARRIER SHOCK      war, plague, guild collapse
        stochastic, rare, large        -> genuinely low here
V14b  SUBSTRATE SHOCK    the reader is gone, not the record
        scheduled, frequent            -> high
V14c  DEPENDENCY SHOCK   the stack under the object
        scheduled, frequent            -> high
```

The scheduled kind ought to be the easy case: announced in advance. It is not budgeted,
so it is not. A planned shock with no budget line behaves exactly like an unplanned one.

Correct the substrate scoring: the bits do not rot. THE READER IS GONE. Intact and
unreadable is a distinct state from decayed, and it is worse, because it reads as
retained.

---

## 5. COMPOUNDING — WHEN THE HOP GENERATOR MOVES INSIDE THE SYSTEM

Section 4 assumes hops are EXTERNAL events at human rate. That assumption fails for a
system in which each generation is produced by the previous one.

```
CURRENT ASSUMPTION   hops are external, calendar-bound, human-scheduled
                     N is bounded by how fast people do things

COMPOUNDING CASE     each generation IS a hop, and generations are produced by
                     the system
                     N becomes a function of compute, not calendar
```

Mark all of Section 5 PROJECTED unless a current instance is cited (F_J). The rate
mismatch (5-1) and the custody choices (5-5) are observable now; the regress (5-2) is not
yet.

### 5-1  THE RATE MISMATCH IS THE FINDING, NOT THE RATE

```
LAYER               CHANGE RATE          SHARED EXTERNAL REFERENT
hardware            years, capital-bound yes — physics, power draw, supply
                    unsynchronised             chain, cooling, fab capacity
                    across firms

model generations   many per hardware    no
                    generation

representation      per generation       no
(format, language,
 provenance
 convention)
```

The SUBSTRATE IS THE SLOW LAYER and the only layer with a shared external referent.
Everything carrying meaning is moving faster than the layer that anchors it.

This INVERTS the classical case. Roman concrete: fast carriers, slow durable substrate
holding the referent — the object outlived the people and could be tested. Here the
substrate is slow AND changing, and the meaning-bearing layer is the fast one. Nothing
anchors.

An entry cannot cite "the hardware is stable" as a custody control. Hardware slowness
protects nothing if the representation layered on it is redefined between hardware
cycles.

### 5-2  PROVENANCE REGRESS

Provenance is A RECORD ABOUT A HOP. Every hop is therefore an opportunity to re-encode
the provenance format itself. If each generation defines its own convention, provenance
requires provenance, and that recurses — no fixed point, unless some layer's format is
frozen by something OUTSIDE the generating system.

```
degradation   loses fidelity per hop, still interpretable, rate measurable
regress       loses the ability to state what was lost, no terminating case
```
DUR-003 is degradation. This is a separate class with no entry.

### 5-3  MULTIPLICATION OF SEAMS

Each firm's chain is internally consistent and externally uninterpretable — different
hardware, tooling, data conventions, definitions of validated, provenance formats, several
held closed for competitive reasons.

This is the disciplinary-seam structure with two differences that make it worse:

1. seams multiply at GENERATION rate, not institutional rate
2. no owner of the seam has ever existed for this domain

An institution can defer a seam question indefinitely. An automated system must return a
value. Across an uninterpretable boundary it will return one, selecting a criterion with
no record that a selection occurred.

### 5-4  INTEROPERATION IS WHERE IT STOPS BEING EPISTEMICS

Worked case: adjacent segments of an electrical grid, each managed by a different firm's
system, each with its own internal representation of what a reading means and no
provenance the other can parse.

They are not required to agree about science. They are required to INTEROPERATE UNDER
LOAD. Each side acts on the other's output while unable to establish what that output was
measured against or under what envelope it was produced.

A wrong research result gets corrected. Two coupled grid controllers with incommensurable
representations fail while the load is on.

### 5-5  NONE OF THIS IS A PROPERTY OF THE TECHNOLOGY

```
closed provenance formats          choice
per-firm representation            choice
no deposit of the deployed object  choice
no interchange contract            choice
impermeable boundaries             choice, and the impermeability is the asset
```

None is required to make the systems work. Each was selected for competitive reasons.
That determines what a control has to overcome: not a physical limit, not carelessness,
but an incentive running the other way. See F_E.

### 5-6  THE MINIMAL ARREST

The cheapest thing that would arrest the regress is not a standard for how the work is
done. It is A STANDARD FOR WHAT MUST SURVIVE A HOP.

```
a frozen interchange layer that no generation is permitted to redefine
contents:  object identity (DUR-001)
           rating envelope (DUR-002)
           hop log (DUR-003)
property:  frozen by something outside the generating system — otherwise it is
           inside the regress
```

DUR-001 and DUR-002 were specified as a contract between an author and a later reader.
Under the compounding case they are a CONTRACT BETWEEN GENERATIONS. Same fields, and the
format itself must now be in the frozen set.

---

## 6. THE PARSER GATE — the same rule at the extraction layer

Stated separately because it is a working control at a different layer from the entries,
and it closes the same insufficiency.

```
CORE RULE   a value and its source travel together
            a value with no source cannot score

THREE FIELDS on every extracted value:
    the value itself
    the literal source text it came from
    the locator — which cell, which line

ONE GATE
    anything entering a scoring function must carry all three
    or it returns UNRATED
    not zero, not clean, not a default

ADDITIONS
    numeral case: a unit token adjacent to the number, or it is not a lifetime.
                  Tilde-one with no unit FAILS THE GATE rather than parsing.
    completeness: expected count vs registered count at end of run — catches
                  anything shadowed by a finally.
```

The single gate catches every defect of this class, because each one produces a value
that could not have named its source. UNRATED here is the same return state as
OUT_OF_ENVELOPE in DUR-002 and the same discipline as the UNRATED PART rule in Section 2.

---

## 7. PROCEDURE

```
Step 0  PRIOR-ART CHECK.        DONE — see 0-1. Not redundant. Cite arXiv 2511.19933
                                as prior art on drift.
Step 1  Fix the deployment class. "ML system" is too broad to load-rate. Pick one:
        a model in a decision loop with no human review, or a model whose outputs
        feed a physical actuator.
Step 2  Populate MEASURED first — they set the floor.
Step 3  Populate TRANSPORTED. One source domain at a time, justification per entry.
Step 4  Populate PROJECTED. Flag all.
Step 5  Score each entry on RECONSTRUCTION. The YES/PARTIAL/NO distribution is a
        headline result on its own.
Step 6  Derive the requirement set. For each entry with existing_control = NONE and
        consequence non-trivial, state the minimum artifact that would close it —
        deposit, custody record, load rating, inspection interval.
Step 7  Report the NULL SET: modes checked and found already controlled. A register
        that finds everything broken is not measuring, it is advocating.
```

### 7-1  WHAT "LOAD RATING" MEANS HERE

```
as-built            the weights, data state and full software stack actually
                    deployed, deposited somewhere that outlives the depositing entity
material provenance training data provenance, including what was excluded
load rating         stated input distribution and decision consequence range within
                    which reported performance was established; outside it the
                    component is UNRATED, not degraded
inspection interval defined re-measurement cadence against a held-out reference,
                    with a stated action threshold
as-built drift      deployed object diverging from the documented one through
                    updates, patches and silent substitution, with no record that
                    the change occurred
```

### 7-2  THE CUSTODY AXIS

```
FIDELITY   is the reported result true of the object produced
CUSTODY    can the object be identified and re-produced later, by someone else
```

Independent. Must not be collapsed. Current practice instruments fidelity only, and
weakly. Custody is unmeasured, which means it is being read as adequate. An unmeasured
variable is not absent — it is set to zero, which is a positive claim nobody licensed.

PROPRIETARY BOUNDARY as a custody term: a disciplinary boundary is porous and the material
crosses eventually. A proprietary boundary is engineered impermeable and the
impermeability is the asset — transmission is actively prevented, not neglected. Loss
timescale inverts from centuries to years: a fold, an acquisition, a strategy change.

Any entry whose reconstruction path runs through a single commercial entity carries
detection_latency = UNBOUNDED and reconstruction = NO by default.

---

## 8. FALSIFIERS — check before the register is used

```
F_A  BRIDGE TRANSPORT INVALID. Structural failure is physical, observable and
     insurable; ML degradation may be none of these. TEST: does at least one
     transported mechanism survive the Section 2-B justification rule without appeal
     to resemblance? If none does, cut the transport section and run on MEASURED
     alone.

F_B  PRIOR ART. ANSWERED — see 0-1. Re-run before any future edition.

F_C  UNBOUNDED SCOPE. Any list of undesirable outcomes can be called a failure-mode
     register. Binding constraints are the mandatory fields: no mechanism, no
     detection channel, no consequence-under-load, no entry. Audit a random 20% and
     report the rejection rate.

F_D  PROJECTION INFLATION. PROJECTED entries are cheap and uncheckable. If they
     dominate, the deliverable is a hazard imagination exercise. State the fraction
     in the header.

F_E  THE ENUMERATION IS NOT THE MECHANISM. Bridge codes became mandatory because
     failures were attributable and expensive, not because a catalogue was
     persuasive. A register with no forcing function changes nothing. State what
     would make it binding; do not claim publishing it is sufficient. If the honest
     answer is "nothing currently would," that is the finding.

F_F  ARTIFACT-PRESENT ASSUMPTION. Classical cases retained the OBJECT and lost the
     documentation, which is why reconstruction was possible. Here the object is not
     retained either. Any entry assuming something recoverable exists must name what
     and where. Otherwise the mode is not "will be lost" but "was never captured."

F_G  READER-PRECONDITION BLINDNESS. This register is itself a record, written by
     people holding the current tacit stack, to be read by people who do not. Every
     field definition must be checkable without asking the author. TEST: hand the
     schema to someone outside the domain, have them classify five entries.
     Definitions producing disagreement are underspecified.

F_H  EVENT DEFINITION. "One failure" is not a defined unit. A silent drift over two
     years and a single wrong output are not the same event and cannot be counted
     together. Define the event boundary before any count appears anywhere.

F_I  INDEPENDENCE. 4-1's expected-count arithmetic assumes independent draws; 4-2
     states why that is false. Any use of the volume argument without the
     correlation correction overstates one mode and understates a worse one. Check
     both appear together or neither does.

F_J  RECURSIVE-CASE SPECULATION. Section 5 describes a partly projected regime.
     Mark every Section 5 entry PROJECTED unless a current instance is cited. Do not
     let a strong structural argument be scored as measured.

F_K  AMBIENT SET IS UNBOUNDED. DUR-005's question generates candidates without limit
     — the sun, the species, the grid. BOUND: a condition enters only if its expected
     lifetime is within the retention horizon being claimed. Conditions outside the
     horizon are noted once and excluded. Without this the entry is unfalsifiable.

F_L  CONJUNCTION ARITHMETIC ASSUMES INDEPENDENCE. The seven terms in DUR-006-B are
     correlated — insolvency drives carrier loss drives strategy change. Correlation
     makes joint failure HIGHER than the naive product, so any naive number is wrong.
     The conclusion rests on the inability to ensure each term, not on the
     arithmetic, and survives. DO NOT PUT A NUMBER ON IT.

F_M  CARRIER-SIDE AMBIENT IS UNFALSIFIABLE AS STATED. "Some capacity might stop being
     produced" predicts nothing. BOUND as F_K bounds the artifact side: a carrier-side
     condition enters only with (a) a named producing mechanism and (b) a currently
     measurable production rate. Conditions failing (b) are noted UNINSTRUMENTED and
     excluded from the active set rather than carried as claims.
```

---

## 9. EXPECTED YIELD

Most deployed components will score PARTIAL on reconstruction, not NO — enough exists to
approximately rebuild, not enough to identify the object. PARTIAL is the interesting class
and the easiest to under-report, because it looks like adequacy from inside.

The register is expected to be SHORT. A long one is a warning sign, not a result.

---

## 10. AMENDMENT RECORD

Each entry retains the superseded statement so a later reader does not inherit a withdrawn
score. Silent overwrite is not permitted — a withdrawn claim is evidence about the method
and stays visible.

```
A-01   V3 CARRIER POPULATION: PROTECTIVE -> LOSS-DRIVING
superseded   "V3 scores + for ML because the practitioner population is large."
replacement  A carrier is not someone in the field. A carrier is SOMEONE WHO CAN READ
             THE REPRESENTATION. Where each generation or firm defines its own
             representation, carrier count for any given output is small and falls
             fast, approaching zero inside a closed chain. V3 scores --.
forcing case Per-firm and per-generation representation divergence (Section 5).
consequence  Removes one of only three protective variables. F3 restated.

A-02   V6 MEDIUM DURABILITY: MISDIAGNOSED
superseded   "V6 scores - for ML: format and dependency rot degrades the medium."
replacement  The bits do not rot. THE READER IS GONE. Format obsolescence is V2 in
             machine form — the file assumes a stack it does not name, exactly as the
             concrete recipe assumes knowledge of the ash. INTACT AND UNREADABLE is a
             distinct state from decayed, and worse, because it reads as retained.
             V6 scores --, mechanism reclassified from decay to precondition.
consequence  Any control that verifies bit integrity is not a control for V6.

A-03   V14 SHOCK EXPOSURE: SCORED ON THE WRONG DEFINITION, SPLIT
superseded   "V14 scores + for ML: shock exposure is low."
replacement  Scored on the classical definition (carrier shock) only. Split into
             V14a/b/c — see 4-3.
consequence  Loss mechanism inverts from one large dated cut to undated attrition,
             p^N over hops. DUR-003.

A-04   "COMMERCIAL" WITHDRAWN AS A REGISTER TERM
superseded   "a continuing commercial entity" as an ambient condition.
replacement  The term was doing two jobs and smuggling a custodian type into a
             structural claim. Register term is CUSTODIAN CONTINUITY; the variable
             that matters is CUSTODIAN-INDEPENDENCE.
consequence  DUR-006. Inverts the goal: not a durable custodian, but an arrangement
             that does not require one.

A-05   CUSTODIAN-QUALITY FRAMING INVERTED
superseded   Implicit assumption that better custodians produce better retention.
replacement  A fully distributed arrangement scores WORST on every term of the
             DUR-006-B conjunction and is nonetheless more robust, because none of
             those terms applies to it.
consequence  Framework error, not arrangement error. Conjunction vs disjunction
             replaces custodian quality as the discriminator.

A-06   HOP BUDGET IS NOT BOUNDED BY CALENDAR
superseded   Section 4's hop budget, assuming hops are external events at human rate.
replacement  Where each generation is produced by the previous one, the hop generator
             moves INSIDE the system and N becomes a function of compute.
consequence  Section 4 is a FLOOR, not an estimate. Marked PROJECTED per F_J.

A-07   CONJUNCTION ARITHMETIC — INDEPENDENCE ERROR
superseded   "A conjunction of many uncertain terms goes to low probability fast."
replacement  Assumes independence. The seven terms are correlated. THE CONCLUSION
             SURVIVES UNCHANGED because it rests on the inability to ENSURE each term,
             not on multiplying probabilities. No number goes on it.
consequence  F_L.

A-08   PRECONDITION CLASS SPLIT
superseded   Preconditions treated as a single class — stated but insufficient.
replacement  STATED-INSUFFICIENT (recorded, underspecified, findable by a careful
             reader -> F_G) vs AMBIENT-NEVER-A-CANDIDATE (not recorded because never a
             candidate; the document is complete on its own terms and nothing in it is
             wrong -> DUR-005).
consequence  DUR-005 sits ABOVE the other entries: it can void their controls without
             any of them having failed.

A-09   TRANSMISSION-FIRST DESIGN READ AS CUSTODY DESIGN, NOT FIDELITY FAILURE
superseded   Implicit ranking of written record over transmitted-form knowledge on
             durability.
replacement  Written records optimise FIDELITY, assuming a reader who still holds the
             preconditions. Transmitted forms optimise CUSTODY and pay fidelity to get
             it — low V2 by construction, distributed carriers, no archive, no single
             holder. Where preconditions are known to be losable, custody-first
             survives. A transmitted LOSS EVENT (that a technology existed, bore load,
             and went) is the durable unit; the technique is not.
consequence  Supports 5-6: keep the frozen interchange set small and readable WITHOUT
             the stack.

A-10   DUR-001 SCOPE NARROWED
superseded   Probe-response record framed as closing reconstruction.
replacement  Closes IDENTITY of the deployed instance only. Says nothing about whether
             the training procedure reproduces that instance.
consequence  DUR-001-N2. Procedure reproducibility remains open, no control proposed.

A-11   AMBIENT SET WAS ARTIFACT-SIDE ONLY
superseded   DUR-005's candidate set presented as the ambient set.
replacement  Every item was a condition for the OBJECT. A second class exists:
             conditions for the CARRIER'S ABILITY TO PERFORM. The artifact-side
             question does not reach it — the carrier-side condition does not make the
             record unreadable, it makes the method unrunnable while the record stays
             perfectly legible.
consequence  DUR-005-B, DUR-005-C, F_M.
```

---

## 11. STILL OPEN

```
CORRELATED-BLOCK LOSS (4-2)      no entry. Shared substrate events take a large
                                 synchronous slice and defeat redundancy counted as
                                 independent. Worse than DUR-003 for infrastructure.

PROCEDURE REPRODUCIBILITY (A-10) no entry, no proposed control.

PROVENANCE REGRESS (5-2)         distinct class from degradation. No entry, and
                                 per-hop instrumentation cannot reach it.

CARRIER-SIDE DETECTION           DUR-005-C is a screen with no detection channel. It
                                 is run by the same population for whom the capacity
                                 is intrinsic — the failure mode it is meant to catch.
                                 Outside-the-stack participation is required, and is
                                 harder to obtain than on the artifact side, because
                                 the relevant outsider is separated by GENERATION or
                                 CONDITIONS rather than by domain.

FORCING FUNCTION                 F_E stands unanswered. That is the finding, not an
                                 omission.
```
