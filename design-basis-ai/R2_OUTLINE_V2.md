# Design Basis R2 — Outline

CC0. Skeleton for the next revision. NOT provision-form yet.
Structure exposed for audit: coverage, dependency sets, disjointness.
Full P#→CARRIES→VERIFY→FALSIFY rendering happens after this passes.

Anchor of R2: load case A was uncarried in R1, D was attacked but never
carried. The P0 thread closes A, and adds three verification channels
that make F's carriers actually disjoint instead of all provider-side.
D does NOT close here — see §1 and §8[1]. The Fable return (Task 3)
killed the P0.3+P0.4 fill; D is back to conditionally-uncarried,
bounded by P1, pinned-probe channel noted as the surviving candidate.

RETURN STATUS (Fable work order, commit 2fdbcd4 — same-builder pair,
NOT P3-verified, DBK_014): Tasks 1,2,5,7 PASS w/ qualifications;
Tasks 3,4,6 FAIL, kills folded below.

---

## 1. COVERAGE MATRIX  R1 → R2

```
        R1 carriers            R2 carriers                 change
A       — (nothing)            P0.1, P0.2                  A now carried
B1      P2, P7                 P2, P7                      —
B2      P3, P4                 P3, P4                      —
C       P4                     P4                          —
D       P3 (attack only)       — (P1-bounded, uncarried)   NOT closed (Task 3)
E       P1,P3(atk),P5,P6       P1,P3(atk),P5,P6            —
F       P2, P7, P8             P2,P7,P8 + P0.3,P0.4,P0.5   F carriers disjoint*
```
* Task 2: the three dep sets are pairwise-empty (disjoint), EXCEPT the
  DBK_011 VOID state on retention is now load-bearing and three-valued —
  copies-held 3 / inherited-metric 3 / outline-pricing 2. disjointness
  holds at 3 unless the pricing accounting is used, which drops it to 2.

D-KILL (Task 3): a signed, logged quantization pass degrading an
  UNDECLARED dimension is caught by neither P0.3 (custody logs THAT a
  change occurred — no assessment semantics; "quantized" ≠ "degraded
  dim X") nor P0.4 (no declared envelope = no referent to diverge from).
  → D is carried only once P1 declares the dimension (P1-bounded).
  → surviving candidate: a pinned-probe longitudinal channel (system vs
    its own past on a FIXED input) carries D with no envelope reference —
    BUT inherits the Task 6 kill: if the probe set is selected, that is
    sample-selection and D reopens. carries D only if the probe set is
    fixed, public, and unselectable. see §8[1].

R1 defect (Fable audit, confirmed): seven loads stated, six provided.
R2 status: A closed, D reopened, six of seven carried. No "attack only"
standing in for "carried."

NOTE ON THE VERIFIER (DBK_014): the Fable return corrected the work
order's header, which labeled Fable "the P3 dissimilar verifier." P3
requires all three dissimilarity axes ESTABLISHED (corpus, architecture,
builder); builder-sameness is known for this pair, so the returns are
same-node computations and none is citable as "P3-verified." The work
order's §3-scoping (every task self-verifying, identity-independent) is
why the work survived the mislabel: only Task 6's weak-positive branch
needed dissimilarity, and Task 6 FAILED, so nothing load-bearing rode on
the label. P3's VERIFY in the main doc is amended to catch this.

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
                thermocouple. ← STILL OPEN. one candidate killed:
     KILLED    (Task 6) candidate was "translation fidelity against
                ecosystem members structurally incapable of misreporting
                state." kill: the members can't misreport their STATE;
                the SAMPLE of members can misreport the POPULATION. frame
                selection, coarseness, and graded curation each pass
                without altering one member — they move WHICH members are
                read and HOW. incorruptible sensors do NOT compose to an
                incorruptible instrument, because SELECTION sits above the
                sensors. (generalizes the accepted-side/survivorship
                pattern: the shared node relocates UP to aggregation the
                moment the channels are made honest.) → ecosystem stays a
                MARKER, not a provision. the open gap is now: a physics
                channel whose SELECTION step is also closed.

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

Task 2 (measured): all three pairwise intersections EMPTY → 3 disjoint.
retention is three-valued (DBK_011 VOID now load-bearing):
  copies-held        → N_eff(verification) = 3
  inherited-metric   → 3
  outline-pricing    → 2   (pricing the retention re-shares one term)
so disjointness holds at 3 EXCEPT under the pricing accounting. which
accounting is used is itself a decision that must be declared (P0.2). 
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

status tags: OPEN (untested) · KILLED (Task N) · QUALIFIED (passes w/ caveat)

```
[1] P0.4 physics channel — OPEN, one candidate KILLED (Task 6).
    translation-fidelity/ecosystem candidate failed: selection sits
    above the incorruptible sensors. gap is now narrower and harder — a
    physics channel whose SELECTION step is also closed. also gates the
    D candidate below (pinned-probe dies on probe-selection).

[2] P0.3 "downstream-held copies" — OPEN spec, QUALIFIED by Task 2.
    disjoint at N_eff 3 except under pricing accounting (→2). spec must
    fix WHICH retention accounting and declare it (P0.2). still needs the
    operational retention+verification spec that adds no provider term.

[3] "distinct upstreams" (independence_ratio) — KILLED (Task 4).
    adversarial coder produced 0.1 vs 1.0 on one corpus through the
    delivered function = full-range disagreement. dead until redefined;
    would fail kappa ≥ 0.6 as written. do NOT collect data on it.

[4] harness thresholds — QUALIFIED (Task 5). code runs as delivered, but
    dissent_alarm at (4,3) FLIPS verdict between t=1 and t=1.5. not a
    test until the threshold is pinned; the verdict currently rides an
    unset constant.

[5] AX1–AX4 rating bands — KILLED-VACUOUS (Task 4). no bands exist to
    disagree on, so the definitions fail by absence. must state band
    boundaries before any application; without them AX is narrative.

[6] D carrier — REOPENED (Task 3). surviving candidate = pinned-probe
    longitudinal channel (system vs own past on fixed input), carries D
    with no envelope reference. viable ONLY if the probe set is fixed,
    public, unselectable — otherwise inherits [1]'s selection kill.

[7] load case A — LIVE (Task 7). independence-ratio access probed this
    run: 5 hosts, all refused CONNECT. N_eff(access) rated 1 / realized 0.
    log per run; the change across runs is the datum.

[8] verifier dissimilarity — the standing gap under DBK_014. every
    return so far is same-builder. a genuine P3 pass needs a verifier
    with a different builder, and the Task 6 weak-positive branch in
    particular needs re-running there before the physics channel could
    ever be called anything but OPEN. recursion doesn't bottom out — it
    takes another dissimilar pass.
```
