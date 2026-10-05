# threshold-states-in-animal-escape.md

Instrument. CC0 -- No Rights Reserved. Dated 2026-10-05.
Tags: OBSERVED (measured in the literature named) / DERIVED (follows from
the observed by a stated step) / PROPOSED (a reading offered here, testable,
not established).
Companion to `sense_as_match.py` (repo root) and to the state definitions in
`notes/memory-export/files/unnamed-instruments.md` (lines 230-238).
One file. Loads whole. Readers: people and other models.

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
NEW                named in the work order for this file. No definition
                   located in this tree.                          THIN T-1
```

`THIN T-1`: the order names three states, but only two are defined anywhere
in this repository. Section 2 maps the order's three transitions to
measured quantities. The labels COALESCED and NEW are attached to stages
there as PROPOSED, not as found.

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
in an encounter is the one that maps here. TONIC IMMOBILITY, the late,
contact-stage collapse in the defense-cascade literature, is a different
state. It is closer to shutdown and does NOT map to held-uncoalesced. A
reading that cites freeze without saying which kind cannot be scored.
Under `sense_as_match.py` it returns UNRATED.

### 2b. FID is the reserve made numeric

OBSERVED: FID is among the most measured quantities in escape behaviour.
There is a large literature across birds, lizards and mammals, summarised
in the Stankowich and Blumstein meta-analysis of risk assessment.

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
began (the starting-distance effect; Blumstein, "flush early and avoid the
rush"). A FID taken without the starting distance recorded mixes the
threshold with the approach geometry.

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

OBSERVED: older work often scored escape as one binary event (fled / did
not flee). The "integrated view" of escape decisions (Cooper and Blumstein,
edited volume) measures a SEQUENCE:

```text
detection -> alert latency -> FID -> distance fled -> resume latency
             (held)            (threshold)  (?)       (resolving)
```

DERIVED: that sequence is the state model measured. The held-uncoalesced
state is not a claim offered without support. It sits on stages with
published distributions behind them.

`THIN T-6`: the sequence has more measured stages than the order has
states. DISTANCE FLED has no state assigned to it. NEW has no stage
assigned to it.

PROPOSED: NEW maps to detection or alert, the moment a stimulus enters
the field. DISTANCE FLED is a property of the act, not a state. Both
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
group size          shifts FID
refuge distance     shifts FID
food density        shifts FID          (the cost term in THIN T-3)
starting distance   shifts FID          (THIN T-4)
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
```

---

## 7. What this file does not claim

- It does not claim that animals hold probability fields. It claims that
  the measured stages have the STRUCTURE the state model names. Mechanism
  is open.
- It does not claim the mapping transfers to people or to models. Transfer
  is a separate test.
- It does not rank species, contexts or observers.

---

## 8. Sources (literature families, named; none opened here)

Egress from the environment that wrote this file is an allowlist that
refuses publisher hosts. No source was opened. Names are given so a reader
can find them. Author names and titles are CARRIED (from the work order and
from general knowledge) and are not verified here. No figure is taken from
any of them.

```text
freeze as preparation       "freeze for action" (Roelofs and colleagues)
defense cascade             tonic vs attentive immobility (THIN T-2)
FID meta-analysis           Stankowich & Blumstein, risk assessment
economic escape theory      Ydenberg & Dill (THIN T-3)
starting-distance effect    Blumstein, "flush early and avoid the rush"
disturbance as predation    Frid & Dill
integrated escape sequence  Cooper & Blumstein, "Escaping from Predators:
                            an integrative view of escape decisions"
```

Cross-links:
`sense_as_match.py` (its module docstring names itself `sense_at_match.py`;
the file is `sense_as_match.py`. Recorded here, not edited there.)
`notes/memory-export/files/unnamed-instruments.md` (state definitions).
