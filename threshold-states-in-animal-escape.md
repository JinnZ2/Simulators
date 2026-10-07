# threshold-states-in-animal-escape.md

Instrument. CC0 -- No Rights Reserved. Dated 2026-10-05.
Tags: OBSERVED (measured in the literature named) / DERIVED (follows from
the observed by a stated step) / PROPOSED (a reading offered here, testable,
not established) / PROXY_AVAILABLE, UNRUN (a measurable proxy for the
quantity exists in a named paper; nothing here has run it).
Companion to `sense_as_match.py` (repo root) and to the state definitions in
`notes/memory-export/files/unnamed-instruments.md` (lines 230-238).
One file. Loads whole. Readers: people and other models.
Revised 2026-10-07: section 0 added. It governs every later section.
Revised 2026-10-07 (second pass): literature checked chat-side by the
operator; results applied in sections 0, 2, 3, 5 and 8.

---

## 0. Definition of NEW (read first; T-1..T-6 are read under it)

Supplied by the operator, 2026-10-07:

```text
NEW := absent after a DECLARED search {corpus, query set, date},
       with the search logged in this file.
A search that is not declared and logged  -> status UNRATED, not NEW.
```

The rule applies to every absence claim in this file, not only to the state
label. "Not found" counts only when this log holds the search that did not
find it. Otherwise the claim reads UNRATED.

### 0a. Search log

```text
id   corpus                          query set (regex, case-insens.)   date        hits  define NEW state
---  ------------------------------  --------------------------------  ----------  ----  ----------------
S-1  JinnZ2/Simulators @ 0c0d53a,    "new *:="                         2026-10-07     0  0
     git grep, all tracked files,    "NEW state|state NEW"                            5  0
     this file excluded              "(UN)?COALESCED.*NEW|                            0  0
                                      NEW.*(UN)?COALESCED"
S-2  this file, section 1 state      "distance fled"                   2026-10-07     0  --
     table (3 rows)
S-3  JinnZ2/Simulators @ 243a773     "narrow watching|watching is      2026-10-07     0  --
     and branch                       costly" (whole word)
     claude/human-sensing-prior      "RESONANT" (whole word)                          5  0 define a
     @ c3578c8, this file excluded                                                       sensing class
```

S-3 RESONANT hits are all other senses: `fragility-cascade/homeostasis_kernel.py:69`
and its sample (3 lines), damping; `qrng-pair-search/qrng_pair_search.py:100`,
tunnelling. The S-3 phrases were supplied with the 2026-10-07 literature
check as cross-link targets. Neither target was located (section 8).
S-3 stands as run. S-4 relocates both targets from pointers the operator
supplied afterward. "narrow watching is costly" was a chat paraphrase, not
file text, so S-3 could not have found it.

```text
id   corpus                                  query (whole word,  date        hits
                                             case-insensitive)
---  --------------------------------------  ------------------  ----------  ----
S-4  JinnZ2/Simulators, human-sensing-prior/ "monitoring"        2026-10-07     0
     human-sensing-prior.md                  "vigilance"                        0
     @ c3578c8 (branch claude/human-sensing-prior)
     same file @ c9715a0 (branch             "monitoring"                       7
     claude/human-sensing-prior-cc0-cbm411)  "vigilance"                        2
     JinnZ2/Polyhedral-Intelligence,         file present?                   0 / 1
     ontology/relation_classes.json
     @ 1d477cf (main) / @ 7387230
     (branch claude/glyph-as-compression)
     same file @ 7387230                     class id == RESONANT            1
```

The operator named the branch `claude/human-sensing-prior`. That branch
has no section 7 and no hit. Both hits are on `-cc0-cbm411`. The
relation-class file is on the glyph branch, not on main. Recorded, not
resolved.

S-1 hits, read by hand. All 5 use "new state" in its ordinary sense of
"next state". None defines a processing state:
`claim-record/CLAIM_TABLE.md:410`, `fragility-cascade/nautilus_architecture.py`
(lines 9, 67, 166), `fragility-cascade/thermo_synth.py:81`.
Not searched: any other repository, any literature corpus. Publisher hosts
refuse CONNECT from this environment.

### 0b. T-1..T-6 under this rule

```text
item  absence claim?                         search   status
----  -------------------------------------  -------  ---------------------------
T-1   yes: no NEW definition in tree          S-1      absence holds @ 0c0d53a;
                                                       definition now in this
                                                       section (operator-supplied)
T-2   no: kinds of freeze, carried            --       not gated; CARRIED
T-3   no: FID-as-ratio reading, carried       --       not gated; CARRIED
T-4   no: starting-distance effect, carried   --       not gated; CARRIED
T-5   yes, if read as "monitoring is not      none     UNRATED
        general"
T-6a  yes: distance fled has no state         S-2      absence holds in the
                                                       section 1 state table
T-6b  yes: NEW has no stage                   none     UNRATED (literature
                                                       stage lists not searched)
```

At the animal level a stimulus is NEW only relative to the animal's own
search. That search state has measurable proxies (chat-side check,
2026-10-07):

```text
proxy                                   source
--------------------------------------  ------------------------------------
attentive immobility + bradycardia      Roelofs & Dayan 2022: freezing is an
                                        evidence-gathering state; bradycardia
                                        is its marker
alert distance (AD)                     Blumstein 2010, FEAR (section 2b)
```

Status of the NEW -> detection/alert mapping: PROXY_AVAILABLE, UNRUN
(was PROPOSED). No measurement in this file declares or logs the animal's
search, so any per-encounter NEW status still reads UNRATED.

---

## Posture

This file is written less hedged than institutional framing, by design.
A claim here says what it rests on and what would break it. Where it rests
on a measurement, it says so. Where it rests on a reading, it says so. It
does not soften a mapping that holds, and it does not hide one that is thin.
Thin points are marked in place as `THIN T-n`. Numbers the file needs and
does not have are marked `UNRATED`, for a human with the papers to fill.
No figure in this file was invented.

---

## 1. The three processing states

Definitions taken from `notes/memory-export/files/unnamed-instruments.md`:

```text
HELD-UNCOALESCED   a probability field; live hypotheses that have not formed
                   a shape. Rides as an overlay.                  [in-tree]
COALESCED          a shape; the field has resolved into one form. [in-tree]
NEW                named in the work order for this file. Defined in
                   section 0 (operator-supplied). No definition in
                   this tree before that (search S-1).            THIN T-1
```

`THIN T-1`: the order names three states, but only two are defined anywhere
in this repository. Section 2 maps the order's three transitions to
measured quantities. The labels COALESCED and NEW are attached to stages
there as PROPOSED, not as found. NEW is now PROXY_AVAILABLE, UNRUN
(section 0).

---

## 2. Core mapping: state to measured quantity

```text
state / transition         measured quantity                     tag
-------------------------  ------------------------------------  ---------
HELD-UNCOALESCED,          FREEZE (attentive immobility): the    OBSERVED
  sub-threshold            animal stops and assesses while the   (freeze)
                           field is below the act-threshold.     DERIVED
                           Not shutdown.                         (mapping)

ACT-THRESHOLD CROSSED      FLIGHT INITIATION DISTANCE (FID):     OBSERVED
  (COALESCED -- PROPOSED)  the distance at which the animal      (FID)
                           breaks and flees.                     DERIVED
                                                                 (mapping)

FIELD RESOLVING            LATENCY TO RESUME normal behaviour,   OBSERVED
                           plus monitoring that continues DURING (latency,
                           escape. The held state outlasts the   monitoring)
                           action until the field clears.        DERIVED
                                                                 (mapping)
```

### 2a. Freeze is active assessment, not shutdown

OBSERVED: the "freeze for action" line of work treats freezing as a
preparatory state, not a collapse. It is attentive immobility, with
autonomic and perceptual changes that support assessment and readiness to
act (Roelofs and colleagues; human and animal work).

DERIVED: a state that gathers information below an act-threshold, and
ends in either staying frozen or bolting, has the structure of a
probability field that has not yet coalesced.

`THIN T-2`: "freeze" covers more than one state. Attentive immobility early
in an encounter is the one that maps here. TONIC IMMOBILITY, the last-resort
response to inescapable threat (circa-strike) in the defense-cascade
literature, is a different state. It is closer to shutdown and does NOT map to held-uncoalesced. A
reading that cites freeze without saying which kind cannot be scored.
Under `sense_as_match.py` it returns UNRATED.

### 2b. FID is the reserve made numeric

OBSERVED: FID is among the most measured quantities in escape behaviour.
There is a large literature across fish, birds, lizards and mammals,
summarised in the Stankowich and Blumstein meta-analysis of risk
assessment (2005). The group-size effect REVERSES in fish (chat-side check,
2026-10-07): the direction of a confound is taxon-dependent.

DERIVED: FID turns into a number how much uncertainty the animal tolerates
before acting.

`THIN T-3`: the economic-escape models (Ydenberg and Dill) read FID
differently. FID is the distance where the expected cost of staying
(predation risk) equals the cost of leaving (lost feeding, lost mating,
the energy of fleeing). On that reading FID moves when the COST OF FLEEING
moves, even if risk perception does not. So FID is a RATIO of tolerance to
cost, not uncertainty tolerance alone. Food density shifting FID (section
4) is this term showing itself. To read FID as "reserve", hold the cost of
fleeing fixed or measure it alongside FID.

`THIN T-4`: FID also correlates with the distance at which the approach
began (the starting-distance effect; Blumstein 2003). A FID taken without
the starting distance recorded mixes the threshold with the approach
geometry.

The stronger form is FEAR ("flush early and avoid the rush"; Blumstein
2010): FID rises with ALERT DISTANCE, because monitoring an approaching
predator has a cost. The key variable is AD, not starting distance.
Support, carried from the chat-side check: Samia et al. 2013, a
phylogenetic meta-analysis; Samia & Blumstein 2015, 178 species, FEAR fits
79%. A FID taken without AD recorded mixes the threshold with the cost of
watching.

Cross-link: the monitoring cost in FEAR is the animal-level form of the
single-channel monitoring cost in `human-sensing-prior/human-sensing-prior.md`,
an independent literature. Location (search S-4): branch
`claude/human-sensing-prior-cc0-cbm411` @ c9715a0.

- Section 7, F1, is the test: whole-field monitoring against forced
  single-channel focus, matched duration.
- The supporting row is in its section 6 scope-limits table: "Sustained
  forced single-channel monitoring IS costly", vigilance research, cited
  there from memory.

This link equates no mechanism. FEAR's cost is watching one approaching
predator. The human file's cost is a forced narrow task.

### 2c. The held state outlasts the action

OBSERVED: birds keep tracking the predator during flight. Return to normal
behaviour has its own measured latency after escape. Frid and Dill framed
human disturbance as predation risk, measured through these same responses.

DERIVED: if monitoring continues after the act, the act did not close the
field. Commitment (bolting) and resolution (field cleared) are separate
events, and the gap between them is measured as resume latency.

`THIN T-5`: monitoring during escape is OBSERVED for some taxa and
contexts. This file does not establish how general it is.

---

## 3. Why the sequence matters

CARRIED (the book is verified to exist; its sequence content was NOT
checked): older work often scored escape as one binary event (fled / did
not flee). The "integrated view" of escape decisions (Cooper and Blumstein,
edited volume, 2015) measures a SEQUENCE:

```text
detection -> alert latency -> FID -> distance fled -> resume latency
             (held)            (threshold)  (?)       (resolving)
```

DERIVED, conditional on the carried sequence: that sequence is the state
model measured. If the book's content matches, the held-uncoalesced state
sits on stages with published distributions behind them. Until it is
checked, this paragraph rests on the CARRIED line above.

`THIN T-6`: the sequence has more measured stages than the order has
states. DISTANCE FLED has no state assigned to it. NEW has no stage
assigned to it.

PROXY_AVAILABLE, UNRUN (section 0): NEW maps to detection or alert, the
moment a stimulus enters the field. DISTANCE FLED is a property of the act, not a state. Both
readings are open.

---

## 4. "Instinct" as a bin-word   [DERIVED]

"Instinct" bundles four things into one unexamined lump:

```text
  threshold logic          when to act          (section 2b, FID)
  probability-holding      acting while unsure  (section 2a, freeze)
  reserve-scaling          how much uncertainty is tolerated, by context
                                                (section 2b + section 5)
  sensory integration      what enters the field (detection, alert)
```

It then treats the lump as a primitive. It looks like an explanation, but
it ends the drill instead of enabling it. This is the same failure shape as
"brain chemistry" or "externality" used as a verdict.

The drill test (PROPOSED, mechanical): after the word "instinct", does the
text name at least one stage (alert, freeze, FID, distance fled, resume) or
one covariate (section 5)?

- If YES, the word is a label on a mechanism.
- If NO, the word is a bin, and it hides the measured stages above.

Under `sense_as_match.py`, a score that rests on "instinct" must declare
the sense it read the word in. A score that does not declare it returns
UNRATED. A declared `corpus_default` passes, but it passes as a finding
that a second party can dispute.

---

## 5. Confounds   [OBSERVED -- stated, not hidden]

```text
group size          shifts FID          (direction reverses in fish)
refuge distance     shifts FID
food density        shifts FID          (the cost term in THIN T-3)
starting distance   shifts FID          (THIN T-4; Blumstein 2003)
alert distance      shifts FID          (THIN T-4; FEAR, Blumstein 2010)
```

A single reading does not isolate the variable. Repeated observation in the
same context is NOT replication: one observer, one site and one context
share every confound above. Repeating it raises the count without raising
independence. Replication means a different observer, a different site, and
covariates recorded or varied.

---

## 6. Numbers this file needs and does not have

Every row is UNRATED. Fill each one from a paper with its citation and
locator, or leave it as it is.

```text
quantity                                          status
------------------------------------------------  --------
FID distribution, per taxon                       UNRATED
pooled effect sizes, Stankowich & Blumstein meta  UNRATED
attentive-freeze duration distribution            UNRATED
alert latency distribution                        UNRATED
distance fled distribution                        UNRATED
resume latency distribution                       UNRATED
FID shift per unit group size / refuge distance /
  food density / starting distance                UNRATED
share of escapes with monitoring during flight    UNRATED
alert-distance distribution                       UNRATED
FID slope per unit alert distance                 UNRATED
```

Rows 9 and 10 (added 2026-10-07). Source pointers, not values:
Samia et al. 2013, Biol Lett; Samia & Blumstein 2015, PLoS ONE (178 bird
species). Not filled from memory.

---

## 7. What this file does not claim

- It does not claim that animals hold probability fields. It claims that
  the measured stages have the STRUCTURE the state model names. Mechanism
  is open.
- It does not claim the mapping transfers to people or to models. Transfer
  is a separate test.
- It does not rank species, contexts or observers.

---

## 8. Sources (literature families; checked chat-side 2026-10-07)

Egress from the environment that wrote this file is an allowlist that
refuses publisher hosts. No source was opened from here. The operator
checked the list from a different environment on 2026-10-07. The statuses
below are that check, carried. No figure in this file comes from these
sources except the two the check supplied (Samia & Blumstein 2015, section
2b).

```text
status      meaning
----------  -----------------------------------------------------------
VERIFIED    citation and anchor claim checked (chat-side, 2026-10-07)
EXISTS      the work is verified to exist; the anchor content is not
CHECK       cited from memory; the primary was not opened
CANDIDATE   named; full citation not yet seen
```

```text
family / work                                           status
------------------------------------------------------  ----------
freeze as preparation
  Roelofs K 2017. Phil Trans R Soc B 372(1718):20160206 VERIFIED
  Roelofs K, Dayan P 2022. Nat Rev Neurosci.            VERIFIED
    doi 10.1038/s41583-022-00608-2. Freezing as an
    evidence-gathering state; bradycardia as marker.
defense cascade (tonic vs attentive; THIN T-2)
  Kozlowska K, Walker P, McLean L, Carrive P 2015.      VERIFIED
    Harv Rev Psychiatry 23(4):263-287
FID meta-analysis
  Stankowich T, Blumstein DT 2005. Proc R Soc B         VERIFIED
    272(1581):2627-2634. doi 10.1098/rspb.2005.3251
economic escape theory (THIN T-3)
  Ydenberg RC, Dill LM 1986. Adv Study Behav            CHECK
    16:229-249. The anchor matches the theory as
    restated in later literature.
starting-distance effect (THIN T-4)
  Blumstein DT 2003. Full citation not given.           CHECK
FEAR, alert distance (THIN T-4)
  Blumstein DT 2010. Behav Ecol 21(3):440-442.          VERIFIED
    doi 10.1093/beheco/arq030
  Samia et al. 2013. Biol Lett. Phylogenetic            CARRIED
    meta-analysis.
  Samia & Blumstein 2015. PLoS ONE. 178 species,        CARRIED
    FEAR fits 79%.
disturbance as predation
  Frid A, Dill LM 2002. Conservation Ecology 6(1):11    VERIFIED
integrated escape sequence (section 3)
  Cooper WE Jr, Blumstein DT (eds) 2015. Escaping From  EXISTS
    Predators. Cambridge University Press.
multimodal risk assessment
  2024 Nat Commun meta-analysis, uni- vs multimodal     CANDIDATE
    predation risk assessment in birds. Authors not
    seen. Models redundancy / enhancement / antagonism.
```

CANDIDATE mapping, PROPOSED (carried from the check): redundancy and
enhancement map to the RESONANT class, and antagonism maps to the open
antagonistic class.

The target enum is in JinnZ2/Polyhedral-Intelligence,
`ontology/relation_classes.json` @ 7387230, class `RESONANT` (search S-4).
Only the enum is matched; the damping and tunnelling senses are excluded.
The enum's measurand is `I = F(A,B) - [F(A) + F(B)]`, joint minus the SUM
of separate, with RESONANT iff I > 0.

CONTRADICTS_CLASS is not used here. That verdict is for a record that
asserts a class its own values rule out. A redundant response asserts no
class. It is REDUNDANT, not RESONANT. (Revised 2026-10-07; the previous
pass labelled it CONTRADICTS_CLASS.)

Two-reference test (DERIVED, operator-supplied 2026-10-07; precedence
operator-supplied the same day). Built and tested as
`threshold-states/interaction.py` (`test_interaction.py`, 24 checks).

```text
S   = sum of the separate (unimodal) responses
M   = the largest single (unimodal) response
tol = declared parameter; an undeclared tol returns UNRATED
I   = joint - S  (the measurand of the RESONANT enum)

step  condition                    relation
0     S - M <= 2*tol               BELOW_RESOLUTION
1     |joint - M| <= tol           REDUNDANT
2     |joint - S| <= tol           ADDITIVE              NEW: I ~ 0, independent
3     joint > S + tol              RESONANT
4     M + tol < joint < S - tol    ENHANCED_SUBADDITIVE
5     joint < M - tol              ANTAGONISTIC          OPEN class: boundary
                                                         proposed, definition
                                                         pending the enum's author
```

`THIN T-7` RESOLVED (2026-10-07). The earlier four rows overlapped once
`tol > 0`, and the overlaps came from two sources:

- REDUNDANT's band met its neighbours.
- With S - M small, the REDUNDANT band reached the sum.

Step 0 removes the second: when S - M <= 2*tol the bands [M-tol, M+tol] and
[S-tol, S+tol] touch, so the weaker cues sum to less than the instrument
resolves. With S - M > 2*tol, rows 1-5 are disjoint and exhaustive:

```text
(-inf, M-tol)  [M-tol, M+tol]  (M+tol, S-tol)  [S-tol, S+tol]  (S+tol, inf)
 ANTAGONISTIC    REDUNDANT      ENH_SUBADDITIVE    ADDITIVE       RESONANT
```

The module does not rely on that argument. It evaluates all five rows and
raises if anything other than exactly one holds. A sweep over five
(cues, tol) settings never raises and reaches every row.

Correction: joint = S is ADDITIVE, not ENHANCED_SUBADDITIVE. The earlier
row read `M < joint <= S` and put the sum itself in the subadditive row.

ADDITIVE is a class the target enum does not carry. It sits at I ~ 0, between
RESONANT (I > 0) and the subadditive rows, so cues that act independently
no longer fall into either.

Canonical module: `threshold-states/interaction.py`. The root
`interaction_class.py` (built separately the same day) is consolidated onto
it and only imports it; its checks in `test_interaction_class.py` run
against the canonical module.

2024 candidate: the reference the paper uses, S or M, is UNRATED until the
paper is seen.

- If the paper reports against M only, its "enhancement" means joint > M.
  That covers ENHANCED_SUBADDITIVE, ADDITIVE or RESONANT, and the three
  cannot be separated without S. RESONANT is undecidable from an M-only
  report.
- The carried mapping above (redundancy and enhancement -> RESONANT) does
  not survive this test as stated. Redundancy is REDUNDANT. Enhancement is
  RESONANT only above S + tol.

Cross-links:
`sense_as_match.py` (its module docstring names itself `sense_at_match.py`;
the file is `sense_as_match.py`. Recorded here, not edited there.)
`notes/memory-export/files/unnamed-instruments.md` (state definitions).
