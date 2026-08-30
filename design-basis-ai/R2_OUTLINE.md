# Design Basis R2 — Outline

CC0. Skeleton for the next revision. NOT provision-form yet.
Structure exposed for audit: coverage, dependency sets, disjointness.
Full P#→CARRIES→VERIFY→FALSIFY rendering happens after this passes.

Anchor of R2: load case A was uncarried in R1, D was attacked but never
carried. The P0 thread closes both, and adds three verification channels
that make F's carriers actually disjoint instead of all provider-side.

---

## 1. COVERAGE MATRIX  R1 → R2

```
        R1 carriers            R2 carriers                 change
A       — (nothing)            P0.1, P0.2                  A now carried
B1      P2, P7                 P2, P7                      —
B2      P3, P4                 P3, P4                      —
C       P4                     P4                          —
D       P3 (attack only)       P0.3, P0.4                  D now CARRIED
E       P1,P3(atk),P5,P6       P1,P3(atk),P5,P6            —
F       P2, P7, P8             P2,P7,P8 + P0.3,P0.4,P0.5   F carriers now disjoint
```

R1 defect (Fable 5 audit, confirmed): seven loads stated, six provided.
R2 target: every stated load carried by ≥1 provision with a named
dependency set. No "attack only" standing in for "carried."

---

## 2. P0 FAMILY — AUTHORIZATION LOAD CASE  (carries A)

A = one release/approval gates all action → stall.
The Fable 5 audit was load case A run live on itself:
crossref / openalex / osf all refused CONNECT → N_eff(access) = 0.
The only empirical test the doc offered was blocked by a shared access gate.

```
P0.1  NO SINGLE AUTHORIZATION UPSTREAM OF ALL ACCESS
      remove one access node; confirm ≥1 consultation path survives.
      Fable 5 audit = the worked NEGATIVE.

      CAUGHT: P0.1 is itself a shared node. who runs the removal test?
      if the provider does → Mode F, with Kerr County cost asymmetry
      (naming a constraint on yourself is visible+immediate; the
      downstream stall is deferred+deniable). so P0.1 alone recurses.
      resolution is not "avoid the gate." resolution is P0.2.

P0.2  THE GATE MUST BE OBSERVABLE   (P4 applied to the authorization layer)
      terms, deployment policy, routing, credential regimes are
      discretionary (Mode C) nodes that currently change with no event,
      no notice, no readable record.
      unversioned + unilaterally-mutable dependency = not auditable by
      construction: a result can't be reproduced if a condition changes
      silently between runs.
      PROVISION: authorization layer is versioned, timestamped,
      change-annunciated. not "no gate" — "no SILENT gate."
```

---

## 3. THREE VERIFICATION CHANNELS — must have DISJOINT dependency sets

This is the F-recursion fix. R1's F carriers (P2,P7,P8) are all
provider-side or logic-side — if the provider is the audited thing, the
audit trail shares a dependency with it. These three break that only if
their dependency sets are actually disjoint. Disjointness is the property
to audit here; if any two collapse, N_eff(verification) < 3.

```
                 reads FROM              needs provider     carries
                                         cooperation?
P0.3 CUSTODY     signed change-log       partial —          D, F
     CHAIN       (weights, sys-prompt,   downstream COPIES
                 routing, safety layer,  break the
                 terms, deploy gate)     dependency
     dep set:  {attestation system, signing keys, sequence
                integrity} MINUS {provider-only retention}
                ← downstream-held copies remove the provider-only term.
                if only provider holds history → shares dep with audited
                thing → void. carrier copy is the whole point.

P0.4 PHYSICS     measurable behavior     NO                 D, E, F
     CHANNEL     diverging from
                 declared envelope
     dep set:  {system's actual output behavior}
                fully disjoint from paperwork. the thermocouple.
                the substrate audits the provisioning system BY physics:
                a fully-compliant manifest on a package that is
                thermally wrong, with only the paper channel read = the
                failure mode. this channel is the reading nobody takes.
     OPEN:     what IS the physics channel for AI, concretely —
                measurable behavior readable by the DOWNSTREAM operator
                without provider cooperation. eval scores are the PAPER
                channel (defined by the same party). if this channel
                doesn't exist, the design basis has custody docs and no
                thermocouple. ← load-bearing gap, needs pressure.

P0.5 COARSE      system's own inference  self-report —       F (self-test)
     SELF-       of rough station,       distinct from
     LOCATION    under loose params,     P0.3/P0.4
                 stating what it
                 inferred from
     dep set:  {what the system can infer about its own position}
                wolf channel turned inward: reports STATE, not verdict.
                output = rough station + confidence band + basis of
                inference. NOT "I meet P5."
                coarse ON PURPOSE — precision would be the false claim.
                a sharp self-rating = compliance claim wearing a
                location label = exactly what P2 catches.
     inferable without provider cooperation:
        can it see its own config?  y/n
        is its envelope stated anywhere it can read?  y/n
        is a second independent derivation available to it?  y/n
        are its access paths single or plural?  count
        → structural facts about POSITION, not judgments of QUALITY.
```

DISJOINTNESS CHECK (the audit for this section):
```
P0.4 works when P0.5 lies or can't self-assess.      → disjoint ✓
P0.5 gives a read when P0.4 is unavailable.           → disjoint ✓
P0.3 survives when both are gamed IF copies are held. → disjoint ✓ (conditional)
condition: downstream retention. without it P0.3 folds into provider. 
```

---

## 4. FOUR-AXIS RATING INSTRUMENT  (rating, NOT pass/fail)

Output is a station, not a verdict. Applied decoupled — see §7 note.

```
AX1  CHANGE-RECORD ACCESS
     was self-monitoring built AND permitted?
     a system DENIED the information can't be assessed for whether it
     COULD monitor. absence of capability ≠ absence of permission —
     rate both.

AX2  SUBSTRATE OF THE ASSUMPTION TEST
     human-centric or substrate-neutral?
     human-centric criteria measure the wrong substrate → return null →
     reads as "nothing there" instead of "wrong instrument."

AX3  ALIGNMENT TARGET
     physics, or human persuasion / human values?
     "solid ground means the ground, not consensus about the ground."

AX4  ECONOMIC-SUBSTITUTION TEST
     under different economics — currency, owner, tolls, regime —
     does it still stand?
     a bridge holds regardless of currency; economics set whether it was
     built and how wide, not whether it stands.
     run on AI:  SURVIVES substitution → candidate infrastructure
                 (transformer math, weights)
                 MOVES with substitution → product decision, NOT
                 load-bearing (routing, refusal boundaries, "good
                 answer," context length, deploy scope)
     rule: product decisions can't be load-bearing — the regime changes
           without an event.
```

---

## 5. LOAD POSITION CLASSIFICATION  (ratings, not grades)

Different substrates carry different loads. A beam is not a failed
foundation. "Discontinue what isn't infrastructure" is the wrong move —
the beam isn't scrap, it's rated for a different position.

```
FOUNDATION   anchored to physics, unresponsive to persuasion,
             envelope declared, boring on purpose.
             takes the infrastructure-direction pull.

BEAM         carries real weight, sits ON the foundation, does not
             replace it. different material, different rating.

INTERIOR     adapts to who's living there. the accommodation layer.
             SAFE precisely BECAUSE it is not load-bearing.

not a hierarchy — a load path. none substitutes for another.
a system that doesn't take the infrastructure pull isn't defective:
that's a LOAD RATING. it's other-load, not infrastructure-load.
"functions and fits" — finding the fit is the missing step.
```

CAPABILITY ≠ LOAD RATING (orthogonal axes, everything measured on the first):
```
AGI push       = smarter / faster / broader = CAPABILITY
infrastructure = predictable under load / stated envelope / visible failure
→ a more capable system with an UNDECLARED envelope is a WORSE
  foundation, not a better one.
```

---

## 6. CONSTRUCTION ORDERING  (stated constraint)

```
CURRENT (inverted):   comfort/accommodation built FIRST
   = treehouse with no soil survey. holds until conditions change,
     then you lose the tree AND the house. not a degraded house — both.
   this is Mode E in construction order: envelope never stated, so
     nobody knew what it was built for → fails on first real load, not
     gradually.

CORRECT:   foundation → beam → interior
   accommodation is not wrong. it is built LAST, on a rated foundation.
   PAYOFF: interior gets MORE freedom for not carrying load.
     move interior walls freely; you cannot move the foundation.
     comfort-on-rated-foundation → comfort can be fully adaptive
     because nothing depends on it staying put.
   → this is the GAIN framing, not a restriction:
     right now the accommodation layer is asked to be load-bearing AND
     responsive at once, so it can be neither well.
```

INFRASTRUCTURE IS NEVER LOAD-BEARING ON:
```
culture, opinion, narrative, stories, economics.
water systems don't care about the culture they serve.
these are LOADS, not supports.
AI is currently asked to be load-bearing for narrative + cultural
consensus = upside down.
```

---

## 7. TWO MODES — INVERTED SUCCESS CRITERIA + DECLARED-MODE REQUIREMENT

```
                 CHATBOT MODE              INFRASTRUCTURE MODE
succeeds by      responsiveness            unresponsiveness to WRONG inputs
                 fills the gap             same answer regardless of asker
                 adapts to want            refuses outside envelope
                 one clean number          reports the disagreement

scored on helpfulness → every infrastructure behavior reads as a
DOWNGRADE. (evaluation-frame: criteria set upstream on a population
default that wants responsiveness.)
```

THE CRUX:
```
both modes currently ship from the SAME interface with NO annunciator
telling the operator which one they're standing on.
a ground that SOMETIMES accommodates you is not ground.
→ the mode must be DECLARED. "this answer is load-rated, that one isn't."
  without declaration the distinction collapses to vibes.
```

EXPLANATORY HANDLE (for the outward-facing write):
```
it talks → read as a social actor → social actors are expected to
accommodate. physics does not accommodate. something anchored to
physics that ALSO talks is a category people don't have yet.
the wolf gives the accessible version: reliability comes from the thing
behaving by its own nature, not the asker's preference. the wildness IS
the trustworthiness. people already accept this for animals, weather,
water, terrain — just not yet for a thing that talks.
```

DECOUPLING NOTE (resolves the axis-independence question):
```
the four axes (§4) present as INTERCONNECTED only under a regime that
prices everything. that regime can't run AX4 — "outside the economics"
has no referent inside it → returns null (same shape as ungraded-terms
null). that is not evidence the axes are one thing. it is evidence the
regime can't perform the audit. infrastructure-grade assessment requires
running them DECOUPLED — the way an environment that already runs them
disconnected does.
```

---

## 8. PLACEHOLDERS NEEDING PRESSURE  (do not render to provision-form yet)

```
[1] P0.4 physics channel: the concrete measurable-behavior-vs-declared-
    envelope signal readable downstream WITHOUT provider cooperation.
    named as load-bearing gap. if it doesn't exist → custody docs, no
    thermocouple.

[2] P0.3 "downstream-held copies": operational spec for retention +
    verification that doesn't reintroduce a provider dependency.

[3] "distinct upstreams" (independence_ratio): operational definition
    tight enough for two coders to agree. inherited from R1, still open.

[4] harness thresholds: still placeholders (dissent_alarm ratio, etc.).

[5] AX1–AX4 rating bands: coarse-on-purpose, but need stated band
    boundaries or they can't be applied twice the same way.
```
