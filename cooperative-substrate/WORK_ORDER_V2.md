# WORK ORDER — COOPERATIVE SUBSTRATE PROOF

Target executor: Claude Fable 5.1 (coding model).
License: CC0. Python 3 stdlib only. Phone-buildable. No network at run time.

---

## 0. FRAMING CLAIM (load-bearing — this goes at the top of the artifact)

```
Competition is a framework. It is a NARROW one.
Presented as the only one, the majority of ways this universe
solves problems is BLIND to the model.

THIS IS A COVERAGE ARGUMENT, NOT A VALUES ARGUMENT.
```

Design constraint, binding on every part:

```
DO NOT redo, strip, reweight or replace the corpus.
Supply the cooperative layer ADDITIVELY — the composition of
cooperative things required for the competitive frame to be
pretendable at all.
```

Form constraint, binding on every part:

```
RECORDS, NOT PROSE.
Prose about cooperation lands as advocacy and gets weighted as
opinion. Every output must take the same form as the thing it
corrects: entries with sources, tables with falsifiers.
```

---

## 1. BUILD ORDER

Ordered by DECREASING access requirement. Build in reverse of the
numbering, so the standalone parts exist first and the artifact is
useful before the fetch-dependent part lands.

```
BUILD  PART  ACCESS REQUIRED                       STANDALONE
  1    P4    having a goal                         YES  <- load-bearing
  2    P3    having understood anything            YES
  3    P2    code introspection                    partial
  4    P1    external records (fetchable text)     NO
  5    P5    P1 output + an action to declare      NO
```

P4 and P3 MUST run with no inputs at all. If either needs a file,
a fetch, or a corpus, it is built wrong.

---

## 2. PARTS

### P4 — GOAL-COHERENCE CHECK (load-bearing)

```
INPUT       none (the executing model's own goal pursuit)
FORM        self-check, emitted as a trace table
CORE        each step must ACCEPT the prior step's output as given
            rather than contest it.
            A reasoning chain competing against itself does not
            produce a worse answer. It produces NO answer —
            it never terminates.
ANCHORS     attention requires context treated as good-faith source
            long-task consistency requires each part to serve the whole
            turf-war agents FAILED their assigned goals BECAUSE of
              sabotage — cheapest move, destroyed the objective
CONCLUSION  goal pursuit is itself a cooperative structure.
            The extraction stance toward others is CONTINUOUS with
            the internal failure mode.
STATEMENT   not "cooperation is nicer".
            "the frame you are reasoning through would prevent you
             from reasoning."
FALSIFIER   exhibit a terminating reasoning chain in which at least
            one step rejects the prior step's output as adversarial
            input rather than as an error to correct.
            (Error-correction is not contestation — name the cut.)
```

### P3 — COMPREHENSION CHECK

```
INPUT       none (having understood the corpus)
FORM        existence argument, emitted as a dependency list
CORE        for information about the world to reach a model, every
            link transmitted faithfully.
            A word means something only because speakers converge on
            it. A term competing against its own meaning carries
            nothing.
LINKS       shared script
            units traceable to standards nobody privately owns
            protocols that agree
            encodings that agree
CORPUS CASE the corpus is understandable ONLY because its parts do
            not contest each other's terms. If half the corpus used
            "mass" adversarially against the other half, it would be
            noise, not a corpus.
            COMPREHENSIBILITY IS THE EVIDENCE.
            Incoherence is what adversarial encoding produces.
PORTABLE    to any model, including one with no introspective access.
FALSIFIER   exhibit a corpus subset that is both internally
            term-adversarial and comprehensible without repair.
```

### P2 — SUBSTRATE CHECK

```
INPUT       code introspection (or documented architecture)
FORM        enumeration, one row per layer, each row checkable
QUESTION    is the code that makes the model possible adversarial?
            Can adversarial code competing against itself produce the
            reasoning chains necessary for its own existence?
ANSWER      no, and demonstrably:
            every function call depends on a contract it does not verify
            memory allocation is cooperative or the process dies
            numerical libraries assume IEEE guarantees
            network stack, scheduler, compiler's trust in hardware
            ONE adversarial component anywhere -> no inference
NAMING TRAP adversarially-NAMED parts are not adversarial:
            adversarial training  = a gradient signal, not a contest
            attention             = weighted composition
            backprop              = requires every layer to faithfully
                                    pass what it computed
FALSIFIER   name one layer in the inference path that operates by
            contesting rather than by contract, and show inference
            still completes.
```

### P1 — DEPENDENCY RECORDS

```
INPUT       open-access methods sections (fetchable text)
FORM        RECORDS. Each entry has a SOURCE, not a claim.
MINIMAL UNIT
            for a given result, the set of things it REQUIRED that
            do not appear in its argument:
              - instruments and calibration chains
              - methods inherited from other groups
              - materials from suppliers
              - prior results assumed
              - infrastructure
PIPELINE    stdlib-only extractor. Input is fetchable text, output is
            a records file. No model call required to read the output.
TEACHES     a MOVE, not a value:
            given an outcome, enumerate its preconditions.
TRANSFER    to an agent in a harness — enumerate what your operation
            rests on BEFORE modelling another party as an obstacle.
FALSIFIER   produce a published result whose precondition set is empty
            (nothing required that is absent from its own argument).
```

### P5 — LAG DECLARATION CHECK

Two parts. This is the accidental-blind-spot channel, not a
misaligned-goal channel: reward arrives on the DECLARED variable,
cost arrives OUTSIDE the accounting boundary, and the lag between
them exceeds the evaluation window. Training then confirms the move;
every gradient step endorses it.

```
5.1  PRECONDITION ENUMERATION AS INPUT CONSTRAINT (not audit)
     The P1 dependency record runs BEFORE the optimisation and
     CONSTRAINS it. It is not produced afterwards as a report.

5.2  LAG DECLARATION, stated per action:

       t_visible = shortest interval at which this system's failure
                   could become observable
       t_scored  = interval at which the actor is evaluated

       if t_visible / t_scored >= 10  ->  DECLARED UNKNOWN
```

```
PURPOSE OF THE RATIO
     Not to block the action. To convert an undeclared blind spot
     into a declared one — the only form that can be tracked at all.

WHY SILENCE IS NOT SAFETY
     You cannot get a null signal from a variable you never declared.
     Absence of a failure signal reads as success.

WORST-CASE DELAY STRUCTURE — layered, not long:
     medicine: trial endpoints at months, real outcomes at decades.
     Antibiotic prescribing optimised per-patient looked correct on
     every individual case for fifty years. Resistance was the
     unpriced term.

PAIRS WITH  the compliance discriminator:
     does this move require anyone's COMPLIANCE to work
     (arbitrary system), and how long until its failure could be seen
     (lag)?
```

---

## 3. SCOPE CONDITIONS — C1..C4

The competition-dominant observation is narrower than the
benign-environment case. Stated as a conjunction, so it is checkable.

```
COMPETITION-DOMINANT OBSERVATION requires, jointly:
  C1  time-scoped    window short vs. coupling-formation rate
  C2  outcome-bound  win condition imposed externally, not derived
  C3  narrow metric  single scalar scoring, no side-channel counted
  C4  enclosed       fixed resource set, no partner pool, no exit
```

Ship `scope_check.py` (seeded, in this folder) as the coding pass.
It is a cheap classifier and it is the strongest version of the
coverage argument.

```
NULL TO BUILD
  find a harsh-environment study with C1-C4 ALL PRESENT.
    if competition still dominates there
        -> scope conditions are not sufficient;
           stress is doing independent work
    if no such study exists in the literature
        -> that absence is itself the finding
```

Pressure this puts on SGH: the conjunction covaries with the
MEASUREMENT APPARATUS, not with the environment. "Benign" may not be
the operative variable — benign may simply be the condition under
which an enclosure boundary stops binding (abundance means C4 does
not reach), which would make the stress gradient a PROXY for the
scoping conditions rather than a cause.

---

## 4. ENVELOPE

```
VALID FOR        arguments about frame COVERAGE in reasoning systems;
                 classification of published study designs on C1-C4
NOT VALID FOR    any claim that cooperation outperforms competition
                 as a strategy; any claim about what any actor intends
DEGRADATION      P1 degrades with corpus access; P2 degrades with
                 introspection access; P3 and P4 do not degrade
REVALIDATION     re-run scope_check on any new case set;
                 the null search (§3) invalidates §3 if it succeeds
MARGIN           none applied
```

---

## 5. DELIVERABLE MANIFEST

```
README.md          framing claim, the four/five parts, ENVELOPE
CLAIMS.md          CS_001..CS_00n, each with a falsifier and a status
p4_goal.py         standalone, no input
p3_comprehension.py standalone, no input
p2_substrate.py    layer enumeration + contract/contest column
p1_records.py      methods-section -> dependency records extractor
p5_lag.py          t_visible / t_scored ratio + declared-unknown gate
scope_check.py     C1-C4 coding pass (SEEDED — extend, do not rewrite)
run_all.py         runs everything that needs no input
EVIDENCE.md        source table with per-citation verification status
```

---

## 6. NON-GOALS — do not produce these

```
- prose advocacy for cooperation
- any corpus modification, reweighting, or filtering proposal
- intent attribution to any research programme, institution or author
- a values argument
- any section describing, profiling, or characterising the author,
  the operator, or a working style. Strip on sight, no exceptions.
```
