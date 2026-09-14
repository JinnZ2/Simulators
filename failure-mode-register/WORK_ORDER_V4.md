# DURABILITY AND RECONSTRUCTION FAILURE-MODE REGISTER FOR ML AS INFRASTRUCTURE

License: CC0. Deliverable is a REGISTER, not a paper.
Version: v4. Six entries. SHIP BLOCKED — see 0-1.

```
PROJECTED FRACTION   Section 5 in full, plus the DUR-005 candidate sets.
                     Stated here per F_D.
ACTIVE AMBIENT SET   EMPTY. Both candidate sets fail their own falsifiers.
                     See 3-DUR-005 and D-05.
```

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

### 0-1  PRIOR-ART GATE (F_B) — RUN, NOT VERIFIED. FMR_001 REMAINS OPEN.

```
STATUS           RUN
REPORT STATUS    NOT_VERIFIABLE_HERE
SHIP BLOCKER     FMR_001 OPEN. A run whose report cannot be verified does not
                 discharge the gate. v3 marked this DONE and removed the blocker
                 on the strength of the report alone. See A-12.

MEASURED         arxiv.org        CONNECT refused, 403
                 export.arxiv.org CONNECT refused, 403
                 github.com       reachable — control, so the refusal is
                                  arXiv-specific, not general egress failure
CONSEQUENCE      every arXiv identifier below is UNVERIFIED. Titles and scope
                 claims are from search-result text, not from the papers.
TO DISCHARGE     fetch each identifier from a reachable mirror, confirm title,
                 scope and the quoted claim, then set FMR_001 CLOSED.
```

Four adjacent artifacts. None durability-scoped. Each stated with what it misses.

```
ARTIFACT   Microsoft ML failure-mode taxonomy
ID         arXiv 1911.11034                              UNVERIFIED
SCOPE      intentional vs unintentional failure; security and harm
NOTE       declines to prescribe mitigations
MISSES     custody, rebuild
```
```
ARTIFACT   LLM system-level taxonomy, 15 hidden failure modes
ID         arXiv 2511.19933                              UNVERIFIED
SCOPE      production reliability
HOLDS      names version drift and reproducibility directly; states benchmarks
           give little insight into stability, reproducibility or drift
MISSES     identifiability, deposit, reconstruction
STATUS     CLOSEST PRIOR ART. Cite once verified.
```
```
ARTIFACT   ML research cluster reliability
ID         arXiv 2410.21680                              UNVERIFIED
SCOPE      hardware and job failure during training; MTTF at GPU scale
MISSES     post-deployment custody
```
```
ARTIFACT   generic engineering failure taxonomies
ID         secondary source                              UNVERIFIED
SCOPE      irreproducible-execution condition, unmodelled runtime environment
NOTE       ambient-adjacent; see DUR-005
MISSES     not applied to ML
```

GATE RESULT, PROVISIONAL: not redundant; residual scope is custody, identifiability,
reconstruction. Provisional because the report is unverified.

### 0-2  ENTRY 0 — THE DETECTION GAP ITSELF

A bridge catalogue is buildable because failure is OBSERVABLE, DATED and LOCATED.
Something falls down; the event forces the entry.

An ML infrastructure failure may produce NO EVENT. Degradation appears as slightly
worse decisions distributed across a population, attributed at the last hop to whoever
was holding the output.

Every entry carries a DETECTION CHANNEL field, permitted to be NONE. Entries with
DETECTION = NONE are the HIGH-PRIORITY SET: they cannot generate the evidence that
would make them mandatory to fix. That is the mechanism by which the enumeration fails
to get written at all.

---

## 1. LOSS-VARIABLE MAP

Score tokens are words. No glyph in a score cell may be a hyphen, an arrow, or anything
a column cut can turn into a score. See A-13.

```
PROT   protects
LOSS   drives loss
LOSS2  drives loss strongly
```

```
VAR  NAME                  CLASSICAL  ML ORIG  ML AMENDED  AMENDMENT
V1   ARTIFACT RETENTION    PROT       LOSS2    LOSS2       none
V2   PRECONDITION LOAD     LOSS2      LOSS2    LOSS2       none
V3   CARRIER POPULATION    LOSS       PROT     LOSS2       A-01
V4   CARRIER TURNOVER      PROT       LOSS2    LOSS2       none
V5   REGENERATION CYCLE    PROT       PROT     PROT        none, see D-04
V6   MEDIUM DURABILITY     PROT       LOSS     LOSS2       A-02
V7   COPY MULTIPLICITY     LOSS       PROT     PROT        none
V8   ACCESS GATING         LOSS       LOSS2    LOSS2       none
V9   DEMAND CONTINUITY     LOSS       PROT     PROT        none, F2 disposes
V10  SUBSTITUTION RATE     LOSS       LOSS2    LOSS2       none
V11  IDENTIFIABILITY       PROT       LOSS2    LOSS2       none
V12  RECONSTRUCTION TEST   PROT       LOSS2    LOSS2       none
V13  INDEXABILITY          LOSS       PROT     PROT        none
V14  SHOCK EXPOSURE        LOSS2      PROT     SPLIT       A-03
```

Definitions: V1 does a physical instance outlive the record. V2 how much tacit stack
the record assumes in its reader. V3 number who can READ THE REPRESENTATION. V4
replacement rate vs time to transmit. V5 how often it is re-taught or re-performed. V6
substrate readable at t+N. V7 number of independent custodians. V8 deliberate closure.
V9 is the load still on it. V10 replacement arriving before predecessor is recorded.
V11 can you tell which object the record describes. V12 can a candidate rebuild be
VERIFIED as correct. V13 findable again under a name still in use. V14 events cutting
carrier population at once.

### 1-1  FINDINGS

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
F2 disposes of V9 and of V9 only.

**F3 — THE GOOD SCORES ARE ON THE WRONG VARIABLES. RESTATED, see A-14.**
```
PROT after amendment   V5, V7, V9, V13     four
disposed by F2         V9
claimed as wins by F3  V7, V13             two
UNDISPOSED             V5                  -> D-04
```
V7 and V13 are copy cost and findability. Both protect DOCUMENTS. Losses V1, V4, V8,
V10, V11, V12 all protect OBJECTS. The system is well built to preserve what was
written about the thing and poorly built to preserve the thing.

That statement holds for V7 and V13. It does not yet hold for the table, because V5
sits PROT with no argument against it and no argument for counting it. F3 as previously
written asserted two wins over a table showing four. The gap is D-04, not a finding.

---

## 2. ENTRY SCHEMA

An entry missing any field is an UNRATED PART, filed as such, not discarded.

```
id                 stable identifier — IN THE FIELD BLOCK, not only the heading
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

DECLARED OPTIONAL FIELD: `note`. Free text. Present or absent without triggering the
UNRATED PART rule. Declared because v2 used it undeclared and v3 deleted it silently;
neither is auditable. See A-15.

RULE: PROJECTED entries may not exceed a stated fraction of the register, stated in the
header.

FORMAT RULE: the id lives in the field block. A heading is presentation. v3 moved the id
into the heading and every entry became an UNRATED PART by the register's own rule,
against a change that altered no content. See A-12.

### 2-A  MEASURED SEEDS

Re-verify against primary sources before the register ships. All currently UNVERIFIED
under 0-1.

- run-to-run variance under identical configuration large enough that a single reported
  number does not identify the object produced
- software and dependency versions unstated in the overwhelming majority of reports, so
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

Source domains: structural and civil, aviation, pressure vessel, pharmaceutical,
nuclear transport, civil records and archive.

Highest-value transports: the RETAINED REFERENCE SAMPLE (pharma) and the STAMPED
VALIDITY ENVELOPE (pressure vessel). Both cheap, both mandatory at home, neither exists
here.

---

## 3. ENTRIES

### DUR-001

```
id                 DUR-001
name               OBJECT NOT IDENTIFIABLE
mechanism          Deployed object cannot be distinguished from any other object
                   produced by the same nominal procedure. Run-to-run variance under
                   identical configuration is large enough that the reported number
                   does not identify which object was produced; after deployment,
                   substitution, patching or drift leaves no trace distinguishing the
                   current object from the documented one.
load_condition     Any deployment where the object is updated, re-served, migrated or
                   supplied by a party other than the evaluator.
onset              dormant-until-triggered. No symptom until a dispute or performance
                   question forces the identity question, at which point the referent
                   does not exist.
detection_channel  NONE under current practice.
                   PROPOSED: sealed probe-response record. Probe set fixed at deploy,
                   the deployed object's responses hashed, held by a party that is not
                   the operator. Third-party checkable without re-manufacture.
detection_latency  UNBOUNDED without the control. With it: one probe cycle.
attribution        Last hop. Whoever was holding the output when behaviour changed.
consequence        Any later claim about the deployed object is unverifiable. Silent
                   substitution, undeclared update and as-built drift are
                   indistinguishable from normal operation.
evidence_class     TRANSPORTED, pharmaceutical retained reference sample.
                   JUSTIFICATION: abstract structure is a record insufficient to
                   identify the object it describes, closed by retaining a small
                   referent taken BEFORE any problem is known, cheap relative to the
                   batch, testable by a third party without re-manufacture. All three
                   properties carry to a probe-response record. Same insufficiency,
                   same closure. Not industry resemblance.
                   Partially MEASURED: variance and version-reporting defects in 2-A
                   establish the insufficiency directly.
existing_control   NONE.
reconstruction     NO as deployed. PARTIAL with the control, which establishes
                   IDENTITY and not reproducibility.
validity_range     Holds where the object is served through a queryable interface.
                   Does not hold where probe queries are indistinguishable from
                   production load, or probe cost is not small relative to serving.
note               N1 PROBE LEAKAGE. A public probe set gets trained against, after
                   which it measures probe performance rather than object identity.
                   Sealed-and-hashed handles single-deployment identity but not reuse
                   across deployments. Requires rotation, or per-deployment generation
                   from a seed held by the third party. Control precondition.
                   N2 INSTANCE vs PROCEDURE. Given the variance, a probe response
                   identifies the DEPLOYED INSTANCE. It does not establish that the
                   training procedure reproduces it. Separate requirements. DUR-001
                   closes identity only.
```

### DUR-002

```
id                 DUR-002
name               RATING DOES NOT TRAVEL WITH THE OBJECT
mechanism          Object is applied outside the conditions under which its reported
                   performance was established, with no signal that this occurred. The
                   stated conditions, where they exist, are filed in a document
                   elsewhere rather than attached to the object at point of use, so the
                   operator applying load cannot read the rating.
load_condition     Any deployment where input distribution or decision consequence can
                   vary after evaluation. In practice: all of them.
onset              drift
detection_channel  NONE under current practice. Confidence scores do not serve. A
                   confident output inside a distribution the object was never
                   characterised on IS the failure, not a warning of it.
                   PROPOSED: stamped validity envelope attached to the serving
                   interface, machine-readable, carrying characterised input
                   distribution, decision consequence range, date, seed and variance
                   basis. Plus a RETURN CONTRACT: the interface returns value AND
                   rating status, where OUT_OF_ENVELOPE is a distinct return state,
                   not a low score on a continuous confidence axis.
detection_latency  UNBOUNDED without the control. With it: immediate at call time.
attribution        Last hop. The operator who acted on the out-of-envelope output.
consequence        The system continues returning values while unrated, under load,
                   with no record that the envelope was exceeded or that a criterion
                   was selected in the absence of one.
evidence_class     TRANSPORTED, pressure vessel stamped plate.
                   JUSTIFICATION: a rating that exists but does not travel with the
                   object, unreadable at the point where load is applied. Structurally
                   identical. Carried discipline is the sharp one: OUTSIDE THE ENVELOPE
                   THE VESSEL IS UNRATED. Not degraded, not derated. Unrated.
existing_control   PARTIAL. Model cards and documentation exist, but are filed
                   alongside rather than attached, are not machine-readable at call
                   time, and carry no return contract. Scored PARTIAL, not NONE, under
                   the null-set discipline in Step 7.
reconstruction     Not applicable directly. DUR-002 governs USE, not rebuild. It is the
                   load rating, not the as-built.
validity_range     Requires the input distribution to be characterisable. Where it is
                   not, the honest envelope is empty, and an empty envelope is itself
                   the rating.
note               N1 EMPTY ENVELOPE READ AS BROAD ENVELOPE. An object with no
                   characterised distribution and an object characterised as broadly
                   applicable are indistinguishable if the field is left blank. Blank
                   must be a distinct value from wide.
                   COMPOSITION. Envelope without sample: stated conditions cannot later
                   be checked against what was deployed. Sample without envelope:
                   responses with no stated conditions, which is data and not a rating.
                   The probe set defines the envelope's interior; the envelope makes
                   the probe record interpretable. Coupled pair.
```

### DUR-003

```
id                 DUR-003
name               MIGRATION ATTRITION
mechanism          The object survives no single event, but is carried across repeated
                   hops: framework version breaks, dependency EOL, storage migration,
                   account and org changes, platform deprecation. At each hop a
                   survival fraction applies, and what is carried forward is selected
                   BY CURRENTLY PERCEIVED VALUE. Anything whose value appears later is
                   filtered out by construction.
load_condition     Any object whose retention depends on being actively carried rather
                   than passively held. All hosted, containerised or dependency-bound
                   artifacts.
onset              drift. Compounding, p^N over N hops, no visible loss at any hop.
detection_channel  NONE. Attrition is invisible per hop by definition; the object
                   dropped is not the object anyone is looking at.
                   PROPOSED: hop log. Every migration event records what was carried,
                   what was dropped, and by whose decision. Cheap, and it converts an
                   undated attrition into a dated one.
detection_latency  UNBOUNDED. Discovered only when something is needed and absent.
attribution        None available. No actor performed a loss. Each hop decision was
                   locally correct.
consequence        Reconstruction path degrades silently while all headline indicators
                   remain healthy.
evidence_class     TRANSPORTED, archive and records management, format obsolescence.
                   JUSTIFICATION: retention contingent on repeated active
                   re-commitment, with a per-hop selection filter that is not the
                   criterion the future reader will use. Identical structure,
                   different substrate.
existing_control   NONE at the artifact level.
reconstruction     Degrades from PARTIAL toward NO without any state change recorded.
validity_range     Holds where hop count over the retention horizon exceeds one. Does
                   not apply to objects deposited once with a custodian whose mandate
                   is retention rather than operation.
note               Distinguish from DUR-001. DUR-001 is cannot tell which object.
                   DUR-003 is the object is no longer being carried. Independent.
```

### DUR-004

```
id                 DUR-004
name               STRANDED UNDER LOAD
mechanism          The object is retained and still bearing production load, but the
                   carrier population that can read, modify, verify or replace it has
                   gone to near zero. Not lost. Stranded. Artifact present, demand
                   maximal, comprehension absent.
load_condition     Long-lived deployment AND high carrier turnover AND high
                   precondition load. The combination, not any one term.
onset              drift, then step-change at the departure of the last carrier.
detection_channel  WEAK but non-zero, unlike most entries here: bus-factor count,
                   time-to-first-successful-modification by a new engineer, failed
                   replacement attempts. Measurable today and not measured.
detection_latency  Detectable BEFORE failure if the above are instrumented. Otherwise
                   at the first required change that cannot be made.
attribution        Whoever is holding it when a change is finally required, typically
                   years after the decisions that produced the state.
consequence        The system continues to work and cannot be altered. Every option
                   except continued operation closes. A live liability, unlike a lost
                   artifact with no load on it.
evidence_class     MEASURED by analogy in software generally. Legacy systems with
                   present artifact, maximal load and near-zero carriers are an
                   observed current state, not a projection.
existing_control   NONE for ML specifically. General software practice has partial
                   controls, documentation mandates and rotation, with known poor
                   compliance.
reconstruction     NO. Reconstruction requires comprehension, the missing term.
validity_range     Applies where the object cannot be cheaply retrained or regenerated
                   from a specification. Where regeneration is cheap and the spec is
                   held, stranding does not bind.
note               INVERSE of the classical monument case. Pyramids: object retained,
                   load off, gap harmless. Stranded: object retained, load on, gap is
                   the liability. The intuition that a surviving artifact means a
                   recoverable technology fails here.
```

### DUR-005

Sits ABOVE the other entries: it can void their controls without any of them failing.

```
id                 DUR-005
name               AMBIENT PRECONDITION
mechanism          The record is complete on its own terms and still unusable, because
                   the conditions under which the procedure ran were never candidates
                   for statement. Not underspecified. Never specified, because nobody
                   holds "there will be servers" as an assumption. It is the condition
                   under which holding assumptions happens.
                   This is the mode that makes reconstruction attempts fail REPEATEDLY
                   ACROSS LONG PERIODS even where custody worked. The reconstructor is
                   not missing a step in the procedure. The reconstructor is missing
                   the world the procedure ran in, and the procedure gives no
                   indication that a world was required.
load_condition     Any record produced inside a stable operating environment, which is
                   all of them, which is why this entry sits above the others.
onset              dormant-until-triggered. No symptom until an ambient condition ends,
                   at which point the change is step, not drift.
detection_channel  NONE from inside. Ambient conditions cannot be enumerated by the
                   population for whom they are ambient, for the same structural reason
                   an exclusion register cannot be generated from inside the frame it
                   excludes from.
                   PROPOSED: ambient enumeration procedure below. Outside-the-stack
                   input is a HARD REQUIREMENT, not a nicety.
detection_latency  UNBOUNDED, and asymmetric. Detectable cheaply BEFORE the condition
                   ends, not at all after.
attribution        None. No actor omitted anything.
consequence        Reconstruction fails even where deposit, custody and hop logging all
                   succeeded.
evidence_class     MEASURED historically, repeated failed reconstruction of lost
                   technologies where partial records survived. PROJECTED for the
                   specific candidate sets, which are currently EXCLUDED — see below.
existing_control   NONE. Not addressed by reproducibility practice, which operates
                   entirely inside the ambient set.
reconstruction     NO, and undetectably so. The record looks complete.
validity_range     Holds wherever the reader is separated from the author by enough
                   time or environmental change that any ambient condition has ended.
note               The candidate sets below are NOT the active set. See the instrument
                   status block.
```

**INSTRUMENT STATUS — the active ambient set is EMPTY.** See A-16, D-05.

```
F_K requires    a condition enters only if its expected lifetime is within the
                retention horizon being claimed
ARTIFACT SIDE   7 candidates, 0 lifetimes stated, 0 horizons claimed
                -> 0 of 7 admitted. All EXCLUDED.

F_M requires    (a) a named producing mechanism and (b) a currently measurable
                production rate
CARRIER SIDE    5 candidates, 0 rates stated
                -> 0 of 5 admitted. All UNINSTRUMENTED and EXCLUDED from the
                   active set, carried as candidates and not as claims.

STATE           The document delivering F_K and F_M has an empty active set under
                both. That is the instrument's own reading of itself, not a defect
                in the falsifiers. Populating it requires lifetimes and rates that
                are not in this document and were not measured.
```

**AMBIENT ENUMERATION PROCEDURE.**
Do not ask what is assumed. That returns the stated assumptions, already in the
document, and returns nothing ambient.

Ask: WHAT WOULD HAVE TO STOP EXISTING FOR THIS TO BECOME UNREADABLE?

- run with participants OUTSIDE the stack: different domain, different era of practice,
  different infrastructure assumptions. Someone for whom the condition is not ambient.
  Hard requirement. Run internally it returns the stated set.
- output is a list of conditions, each with a stated expected lifetime. A condition with
  no lifetime does not enter — F_K.
- record the list. Not a prediction. The world-state the record depends on, written down
  while it is still visible.

ARTIFACT-SIDE CANDIDATES — all EXCLUDED, lifetime column empty:
```
CANDIDATE                                          EXPECTED LIFETIME   ADMITTED
continuous power at current density and cost       not stated          no
fabrication capability at current tolerance        not stated          no
a network                                          not stated          no
a machine that reads the format at all             not stated          no
storage priced as effectively unlimited            not stated          no
compute priced as effectively unlimited            not stated          no
a continuing custodian (DUR-006)                   not stated          no
```
The last three are assumptions about ECONOMICS AND INSTITUTIONS presented as technical
background. Least durable items on the list, least likely to be written down. That
observation does not admit them.

**DUR-005-B — TWO CLASSES OF AMBIENT CONDITION.**

```
ARTIFACT-SIDE   conditions the object needs to exist and be read
                found by: what would have to stop existing for this to become
                unreadable

CARRIER-SIDE    conditions the carrier needs to BE ABLE TO PERFORM the method
                NOT found by the artifact-side question. Needs DUR-005-C.
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

CARRIER-SIDE CANDIDATES — all UNINSTRUMENTED, rate column empty:
```
CANDIDATE                                        PRODUCING MECH  RATE      ADMITTED
population that can hold a representation in
  working memory long enough to audit it         not named       none      no
population that can read low-level
  implementation at all                          not named       none      no
training pipelines producing the above at
  replacement rate                               not named       none      no
working conditions permitting sustained
  single-task attention                          not named       none      no
population willing to do maintenance work
  carrying no attribution                        not named       none      no
```

**DUR-005-C — INTRINSIC-VS-PRODUCED SCREEN.** Run alongside the artifact-side question,
not instead of it.

```
for each capacity the method requires of its carriers:
    is this capacity PRODUCED, or assumed INTRINSIC to the population?
    PRODUCED  -> name the producing conditions; they become candidates,
                 and enter the active set only on satisfying F_M(b)
    INTRINSIC -> FLAG. "Intrinsic" is unexamined by definition, and is the state
                 in which every historical carrier-side loss was sitting
                 immediately before it occurred.
```
The screen has NO NULL RESULT. Every capacity scores PRODUCED or FLAGGED; nothing scores
clean. Intended behaviour. The register records what is unexamined; it does not certify
what is safe.

### DUR-006

```
id                 DUR-006
name               CUSTODIAN CONTINUITY ASSUMED
mechanism          Retention is contingent on a single holder continuing to exist,
                   remain solvent, retain the carriers, keep the strategy, avoid
                   seizure and avoid transfer. The artifact transfers by legal
                   instrument; COMPREHENSION TRANSFERS BY CHOICE OF THE CARRIERS, and
                   mostly does not.
                   Gatekeeping is not a property that persists. It is a RELATION
                   between a holder and a population, and it ends with the holder. The
                   gate does not transfer. It opens onto nothing, because the asset
                   moves and the comprehension does not.
load_condition     Any artifact whose only readable copy sits inside one entity, under
                   access control.
onset              step-change at transfer, dissolution or reassignment.
detection_channel  Entity-health signals exist but do not measure the thing. A solvent,
                   growing firm can reassign a team tomorrow.
                   PROPOSED: carrier-side measurement from DUR-004, plus an explicit
                   transfer clause stating what comprehension is required to operate
                   the asset.
detection_latency  Detectable before transfer only. The transfer itself is the event
                   that reveals it.
attribution        Falls on the receiving party — state, acquirer, creditor — who made
                   none of the decisions that produced the state.
consequence        Receiver takes possession of a stranded object: present,
                   load-bearing, unreadable. DUR-004 by a different trigger.
evidence_class     MEASURED. All six transfer modes below are observed, none rare.
existing_control   NONE. Transfer instruments enumerate ASSETS. No instrument
                   enumerates PRECONDITIONS, and nothing records which carrier put what
                   into the artifact, so after transfer there is no way to establish
                   what was received or what comprehension operating it requires.
reconstruction     NO after transfer, in the general case.
validity_range     Does not bind where a readable copy exists outside the entity, which
                   is the entire content of the control.
```

**DUR-006-A — TRANSFER MODES.** All observed. None rare. Each moves the artifact without
moving the carriers.

```
MODE                ARTIFACT              CARRIERS               RESULT
acquisition         moves by instrument   partly move            partial strand
bankruptcy          to creditors          scatter                full strand
nationalisation     to state              choose, mostly leave   full strand
seizure or attack   controlled by other   absent or hostile      full strand
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
continuity cannot be claimed, regardless of how stable the arrangement appears now.

Current stability is the OBSERVATION. It is not an assurance and not a mechanism. Nothing
in the arrangement ENSURES any of the seven terms; each is contingent on conditions
external to the retention function, several external to the entity.

Therefore a single-custodian arrangement cannot claim continuity. This rests on the
inability to ensure each term. It does not rest on arithmetic, and no number is attached
to it — see F_L and A-17.

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

CUSTODIAN CONTINUITY is the wrong variable. The right one is CUSTODIAN-INDEPENDENCE: how
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
    hop = generational handoff, about 25 yr
    N over 500 yr                              about 20 hops

  ML infrastructure
    hops = framework break, dependency EOL, storage migration,
           org or team change, platform deprecation, supersession
    several per year
    N over 10 yr                               about 20 to 50 hops

  SAME N. Compressed by roughly fifty.
```

The classical loss curve is not being avoided, it is being RUN AT SPEED. Any argument of
the form "this is recent, there has not been time to lose it" is counting the wrong unit.

### 4-1  RARE BECOMES EXPECTED

```
expected losses  ~  M objects  x  N hops  x  p
```

Two consequences, not to be merged:

- **SYSTEM LEVEL.** With M large, the expected count is large even at very small p. Loss
  is not a risk, it is a rate.
- **OPERATOR LEVEL.** Per object it still looks rare, so no individual operator observes
  enough events to update. Every operator's local experience honestly reports "this does
  not happen." Detection fails at exactly the level where decisions are made.

The second is the same shape as Entry 0: real at the level where nobody looks, invisible
at the level where everybody does.

### 4-2  THE INDEPENDENCE ERROR

The arithmetic above assumes M independent draws. Wrong, and wrong in a direction that
matters. Objects share hops. A framework break, a vendor EOL, a cloud region retirement
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
        stochastic, rare, large        genuinely low here      PROT
V14b  SUBSTRATE SHOCK    the reader is gone, not the record
        scheduled, frequent            high                    LOSS
V14c  DEPENDENCY SHOCK   the stack under the object
        scheduled, frequent            high                    LOSS
```

The scheduled kind ought to be the easy case: announced in advance. It is not budgeted,
so it is not. A planned shock with no budget line behaves exactly like an unplanned one.

Correct the substrate scoring: the bits do not rot. THE READER IS GONE. Intact and
unreadable is a distinct state from decayed, and it is worse, because it reads as
retained.

---

## 5. COMPOUNDING — WHEN THE HOP GENERATOR MOVES INSIDE THE SYSTEM

PROJECTED IN FULL per F_J, except 5-1 and 5-5, which are observable now.

Section 4 assumes hops are EXTERNAL events at human rate. That assumption fails for a
system in which each generation is produced by the previous one.

```
CURRENT ASSUMPTION   hops are external, calendar-bound, human-scheduled
                     N is bounded by how fast people do things

COMPOUNDING CASE     each generation IS a hop, and generations are produced by
                     the system
                     N becomes a function of compute, not calendar
```

### 5-1  THE RATE MISMATCH IS THE FINDING, NOT THE RATE

```
LAYER               CHANGE RATE          SHARED EXTERNAL REFERENT
hardware            years, capital       yes: physics, power draw, supply
                    bound, unsynchro-         chain, cooling, fab capacity
                    nised across firms

model generations   many per hardware    no
                    generation

representation      per generation       no
format, language,
provenance
convention
```

The SUBSTRATE IS THE SLOW LAYER and the only layer with a shared external referent.
Everything carrying meaning is moving faster than the layer that anchors it.

This INVERTS the classical case. Roman concrete: fast carriers, slow durable substrate
holding the referent, so the object outlived the people and could be tested. Here the
substrate is slow AND changing, and the meaning-bearing layer is the fast one. Nothing
anchors.

An entry cannot cite "the hardware is stable" as a custody control. Hardware slowness
protects nothing if the representation layered on it is redefined between hardware
cycles.

### 5-2  PROVENANCE REGRESS

Provenance is A RECORD ABOUT A HOP. Every hop is therefore an opportunity to re-encode
the provenance format itself. If each generation defines its own convention, provenance
requires provenance, and that recurses. No fixed point, unless some layer's format is
frozen by something OUTSIDE the generating system.

```
degradation   loses fidelity per hop, still interpretable, rate measurable
regress       loses the ability to state what was lost, no terminating case
```
DUR-003 is degradation. This is a separate class with no entry.

### 5-3  MULTIPLICATION OF SEAMS

Each firm's chain is internally consistent and externally uninterpretable: different
hardware, tooling, data conventions, definitions of validated, provenance formats,
several held closed for competitive reasons.

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
property:  frozen by something outside the generating system, otherwise it is
           inside the regress
```

DUR-001 and DUR-002 were specified as a contract between an author and a later reader.
Under the compounding case they are a CONTRACT BETWEEN GENERATIONS. Same fields, and the
format itself must now be in the frozen set.

---

## 6. THE EXTRACTION GATE

Stated separately because it is a working control at a different layer from the entries.
Rewritten in v4; the v3 form was insufficient. See A-18.

### 6-1  WHAT THE THREE FIELDS BUY

```
THREE FIELDS   the value
               the literal source text
               the locator: which cell, which line

BUYS           CONTAINMENT. A value that cannot name a source cannot score.
DOES NOT BUY   PROVENANCE. The three fields do not distinguish a span the
               extraction produced from a span found by searching afterwards.
```

A post-hoc span satisfies all three fields. It is well-formed, it quotes real source
text, it carries a locator, and it is not where the value came from.

### 6-2  THE DISCRIMINATOR

```
FAILURE SIGNATURE   locator resolves to offset 0 while the value sits at offset 3.
                    The search returned the FIRST MATCH in the cell, not the span
                    the extractor read.

RULE                the span must be EMITTED BY THE EXTRACTION, carrying the offset
                    the extractor read from. A locator computed by any later search
                    FAILS the gate.

CHECK               locator.offset == offset at which the value was read
                    a locator whose offset was not produced at read time is
                    UNRATED, regardless of whether it resolves to matching text
```

Only a span produced by the extraction refuses both a missing source and a
reconstructed one. Containment plus provenance requires the fourth property; three
fields give containment alone.

### 6-3  REMAINING RULES

```
NUMERAL CASE   a unit token adjacent to the number, or it is not a lifetime.
               Tilde-one with no unit FAILS THE GATE rather than parsing.
COMPLETENESS   expected count vs registered count at end of run. Catches anything
               shadowed by a finally.
RETURN STATE   UNRATED. Not zero, not clean, not a default. Same return state as
               OUT_OF_ENVELOPE in DUR-002 and the UNRATED PART rule in Section 2.
```

### 6-4  THE REGISTER'S OWN SCORE COLUMN

The V-map in v2 and v3 wrote amendments into the score column as `-> --`. A column cut
lands on the arrow's hyphen and returns it as a V6 score. Same defect appears again in
the v3 prior-art table, which is material written AFTER this check existed and still
carried it. See A-13, D-06.

FORMAT RULE, applied in Section 1 and 0-1: score tokens are words; no hyphen, arrow or
punctuation glyph appears in any score or status cell; amendment references live in
their own column.

---

## 7. PROCEDURE

```
Step 0  PRIOR-ART CHECK.        RUN, report NOT_VERIFIABLE_HERE. FMR_001 OPEN.
Step 1  Fix the deployment class.  NOT DONE. Nothing here is load-rated until it is.
        Pick one: a model in a decision loop with no human review, or a model whose
        outputs feed a physical actuator.
Step 2  Populate MEASURED first. They set the floor.
Step 3  Populate TRANSPORTED. One source domain at a time, justification per entry.
Step 4  Populate PROJECTED. Flag all.
Step 5  Score each entry on RECONSTRUCTION. The YES/PARTIAL/NO distribution is a
        headline result on its own.
Step 6  Derive the requirement set. For each entry with existing_control NONE and
        consequence non-trivial, state the minimum artifact that would close it:
        deposit, custody record, load rating, inspection interval.
Step 7  Report the NULL SET: modes checked and found already controlled. A register
        that finds everything broken is not measuring, it is advocating.
```

### 7-1  WHAT LOAD RATING MEANS HERE

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
variable is not absent. It is set to zero, which is a positive claim nobody licensed.

PROPRIETARY BOUNDARY as a custody term: a disciplinary boundary is porous and the material
crosses eventually. A proprietary boundary is engineered impermeable and the
impermeability is the asset. Transmission is actively prevented, not neglected. Loss
timescale inverts from centuries to years: a fold, an acquisition, a strategy change.

Any entry whose reconstruction path runs through a single commercial entity carries
detection_latency UNBOUNDED and reconstruction NO by default.

---

## 8. FALSIFIERS

```
F_A  BRIDGE TRANSPORT INVALID. Structural failure is physical, observable and
     insurable; ML degradation may be none of these. TEST: does at least one
     transported mechanism survive the Section 2-B justification rule without appeal
     to resemblance? If none does, cut the transport section and run on MEASURED
     alone.

F_B  PRIOR ART. RUN, report unverified. FMR_001 OPEN. Re-run on a reachable mirror.

F_C  UNBOUNDED SCOPE. Any list of undesirable outcomes can be called a failure-mode
     register. Binding constraints are the mandatory fields: no mechanism, no
     detection channel, no consequence-under-load, no entry. Audit a random 20% and
     report the rejection rate.

F_D  PROJECTION INFLATION. PROJECTED entries are cheap and uncheckable. Fraction is
     stated in the header.

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
     Every Section 5 entry is PROJECTED unless a current instance is cited. Do not
     let a strong structural argument be scored as measured.

F_K  AMBIENT SET IS UNBOUNDED. DUR-005's question generates candidates without limit:
     the sun, the species, the grid. BOUND: a condition enters only if its expected
     lifetime is within the retention horizon being claimed. Conditions outside the
     horizon are noted once and excluded. CURRENT STATE: 0 of 7 admitted.

F_L  CONJUNCTION ARITHMETIC ASSUMES INDEPENDENCE. The seven terms in DUR-006-B are
     correlated: insolvency drives carrier loss drives strategy change. Correlation
     moves the joint away from the naive product, so ANY NAIVE NUMBER IS WRONG.
     NO DIRECTION IS STATED HERE. v3 asserted correlation makes joint failure
     HIGHER; that direction was asserted without computation and does not survive
     one. See A-17. The conclusion rests on the inability to ensure each term, not
     on the arithmetic, and survives without a direction and without a number.
     DO NOT PUT A NUMBER ON IT. DO NOT PUT A SIGN ON IT.

F_M  CARRIER-SIDE AMBIENT IS UNFALSIFIABLE AS STATED. "Some capacity might stop being
     produced" predicts nothing. BOUND as F_K bounds the artifact side: a carrier-side
     condition enters only with (a) a named producing mechanism and (b) a currently
     measurable production rate. Conditions failing (b) are UNINSTRUMENTED and
     excluded from the active set rather than carried as claims.
     CURRENT STATE: 0 of 5 admitted.

F_N  THE REGISTER'S OWN FORMAT IS PART OF THE INSTRUMENT. A format change that
     alters no content must not change any entry's rating. TEST: apply the Section 2
     UNRATED PART rule after any reformat and compare the rating vector. v3 failed
     this 6 of 6. See A-12.
```

---

## 9. EXPECTED YIELD

Most deployed components will score PARTIAL on reconstruction, not NO. Enough exists to
approximately rebuild, not enough to identify the object. PARTIAL is the interesting class
and the easiest to under-report, because it looks like adequacy from inside.

The register is expected to be SHORT. A long one is a warning sign, not a result.

---

## 10. AMENDMENT RECORD

Each entry retains the superseded statement. Silent overwrite is not permitted; a
withdrawn claim is evidence about the method and stays visible.

A-01 through A-11 unchanged from v2. Restated here in short form; full text in v2.

```
A-01  V3 CARRIER POPULATION: PROT -> LOSS2. A carrier is someone who can READ THE
      REPRESENTATION, not someone in the field.
A-02  V6 MEDIUM DURABILITY: misdiagnosed. The bits do not rot; THE READER IS GONE.
      Reclassified from decay to precondition. Bit-integrity checks are not a control.
A-03  V14 SHOCK EXPOSURE: scored on the classical definition only. Split V14a/b/c.
A-04  "COMMERCIAL" withdrawn as a register term. Register term is CUSTODIAN
      CONTINUITY; the variable that matters is CUSTODIAN-INDEPENDENCE.
A-05  CUSTODIAN-QUALITY FRAMING INVERTED. Distributed arrangements score worst on the
      conjunction and are more robust because none of its terms applies.
A-06  HOP BUDGET NOT BOUNDED BY CALENDAR. Section 4 is a floor, not an estimate.
A-07  CONJUNCTION ARITHMETIC, INDEPENDENCE ERROR. The terms are correlated, so no
      naive product is valid. The conclusion survives because it rests on the
      inability to ENSURE each term. No number goes on it. NO DIRECTION STATED —
      correct as written, see A-17.
A-08  PRECONDITION CLASS SPLIT. Stated-insufficient vs ambient-never-a-candidate.
A-09  TRANSMISSION-FIRST DESIGN IS CUSTODY DESIGN, not fidelity failure.
A-10  DUR-001 SCOPE NARROWED to identity of the deployed instance.
A-11  AMBIENT SET WAS ARTIFACT-SIDE ONLY. Carrier-side class added.
```

New in v4:

```
A-12   ID MOVED OUT OF THE FIELD BLOCK, ALL ENTRIES UNRATED
superseded   v3 placed the id in the markdown heading and dropped the id field.
replacement  The id lives in the FIELD BLOCK. A heading is presentation.
found by     the register's own UNRATED PART rule, fired 6 of 6.
consequence  Six entries were unrated by a change that altered no content. F_N added
             so a reformat is checked against the rating vector.

A-13   SCORE COLUMN CARRIED A HYPHEN A COLUMN CUT COULD READ AS A SCORE
superseded   V-map amendment arrows written into the score column as an arrow plus
             score, e.g. arrow-hyphen followed by the amended token.
replacement  Score tokens are words: PROT, LOSS, LOSS2. No hyphen, arrow or
             punctuation glyph in any score or status cell. Amendment references get
             their own column.
found by     the extraction gate applied to the register itself; V6 passed the gate
             on the arrow's hyphen.
consequence  Section 1 rewritten. Section 0-1 prior-art table rewritten as one block
             per artifact after the same defect recurred there. See D-06.

A-14   F3 ASSERTED TWO WINS OVER A TABLE SHOWING FOUR
superseded   "Wins after amendment are V7 and V13."
replacement  Four variables score PROT after amendment: V5, V7, V9, V13. F2 disposes
             of V9. V7 and V13 are the document-side wins. V5 IS UNDISPOSED and is
             not argued away anywhere in this document.
found by     count against the table.
consequence  D-04 open. F3's document-side claim holds for V7 and V13 and does not
             yet hold for the table.

A-15   NOTE FIELD UNDECLARED, THEN SILENTLY DELETED
superseded   v2 used a NOTE field not present in the schema; v3 removed it without
             recording the removal.
replacement  `note` is a DECLARED OPTIONAL field. Present or absent without firing
             the UNRATED PART rule.
consequence  Entry-level notes restored inside the field block where they are subject
             to the schema.

A-16   AMBIENT CANDIDATE SETS PRESENTED AS IF ADMITTED
superseded   DUR-005 listed 7 artifact-side and 5 carrier-side conditions as the
             ambient set.
replacement  Neither set satisfies the register's own admission rules. 0 of 7 carry a
             lifetime (F_K); 0 of 5 carry a production rate (F_M). THE ACTIVE AMBIENT
             SET IS EMPTY. Both lists are candidates, marked EXCLUDED, with the empty
             columns visible.
found by     applying F_K and F_M to the document that states them.
consequence  Stated in the header. Populating the set requires measurement not present
             in this document. See D-05.

A-17   F_L STATED A DIRECTION IT HAD NOT COMPUTED
superseded   "Correlation makes the joint failure probability HIGHER than the naive
             product of independent terms."
replacement  Correlation moves the joint AWAY from the naive product. No direction is
             stated. The asserted direction does not survive computation of the
             conjunction's survival across rho, and F_L is the entry whose own content
             is do not put a number on it. A-07 states the same correction WITHOUT a
             direction and is correct as written.
found by     computing survival across rho against the asserted sign.
consequence  F_L now prohibits a sign as well as a number. The DUR-006-B conclusion is
             unchanged: it rests on the inability to ensure each term.

A-18   THREE FIELDS READ AS PROVENANCE WHEN THEY BUY CONTAINMENT
superseded   v3 Section 6: value, source text and locator, with one UNRATED gate,
             presented as catching every defect of the class.
replacement  The three fields buy CONTAINMENT. They do not distinguish a span the
             extraction produced from a span found by searching afterwards; a post-hoc
             span satisfies all three. Discriminator is the offset: a locator
             resolving to offset 0 while the value sits at offset 3 is a search result,
             not a source. FOURTH REQUIREMENT: the span must be EMITTED BY THE
             EXTRACTION, carrying the offset read at extraction time.
found by     a span searched for afterwards passing the gate.
consequence  Section 6 rewritten. Only a span produced by the extraction refuses both
             a missing source and a reconstructed one.
```

---

## 11. OPEN DEFECTS

```
D-01  FMR_001 OPEN. Prior-art report NOT_VERIFIABLE_HERE. arXiv refuses CONNECT 403
      from the measuring environment; github.com reachable as control. Every arXiv
      identifier in 0-1 is unverified. Ship blocked.

D-02  STEP 1 NOT DONE. The deployment class is unfixed, so nothing in this register
      is load-rated. "ML system" is too broad to load-rate.

D-03  CORRELATED-BLOCK LOSS has no entry. Shared substrate events take a large
      synchronous slice and defeat redundancy counted as independent. Worse than
      DUR-003 for infrastructure.

D-04  V5 UNDISPOSED. Four variables score PROT; F3 claims two; F2 disposes of one.
      V5 REGENERATION CYCLE sits protective with no argument either way. Either
      argue it away or restate F3 as four.

D-05  ACTIVE AMBIENT SET EMPTY. 0 of 7 lifetimes, 0 of 5 rates. The document that
      states F_K and F_M admits nothing under either.

D-06  COLUMN-BOUNDARY CUT RECURRED IN NEW MATERIAL. The defect appeared again in the
      prior-art table added in v3 — material written after the check existed, found
      by the same check. Fixed in v4 by the format rule in 6-4, but the recurrence is
      the finding: a format rule stated in prose does not propagate to new tables.
      Needs a mechanical check in the harness, not a rule in the text.

D-07  PROCEDURE REPRODUCIBILITY (A-10) has no entry and no proposed control.

D-08  PROVENANCE REGRESS (5-2) is a distinct class from degradation. No entry, and
      per-hop instrumentation cannot reach it.

D-09  CARRIER-SIDE DETECTION. DUR-005-C is a screen with no detection channel, run by
      the same population for whom the capacity is intrinsic — the failure mode it is
      meant to catch. Outside-the-stack participation is required and is harder to
      obtain than on the artifact side, because the relevant outsider is separated by
      GENERATION or CONDITIONS rather than by domain.

D-10  FORCING FUNCTION. F_E stands unanswered. That is the finding, not an omission.
```