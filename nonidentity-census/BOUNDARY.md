# BOUNDARY DECISIONS

Written before `t1_predicate_unit.py` was written and before anything was
run. Order of authorship is checkable in the commit: this file lands in the
same commit as the detector, and the detector imports its decisions from
here rather than restating them, so a decision changed after a run changes
the run.

The work order asks for these as a first-class result because they determine
the count. They do.

---

## D0 — the unit of classification

**Decision.** One classification per abstract, taken on the **subject of the
main causal claim**, not on the abstract's vocabulary and not on its topic.

**Main causal claim** is resolved in this order, first hit wins:

1. the last sentence containing a result verb in first person
   (`we find` / `we show` / `we demonstrate` / `we argue` / `results show`),
2. else the last sentence containing a causal verb
   (`causes` / `drives` / `increases` / `reduces` / `predicts` / `leads to`),
3. else the final sentence.

**Why an ordered rule and not a judgement.** Abstracts carry several claims.
Without a stated selection rule the classifier's answer is set by which
sentence the reader happened to weigh, which is unrecoverable afterwards.
The rule is arbitrary in its details and is not arbitrary in being written
down.

**Known cost.** Rule 3 fires on abstracts that state their result early and
close on implications. Those get classified on the implication. Recorded,
not corrected — correcting it means a second rule about which sentence is
"really" the result, and that regress is the thing the rule exists to stop.

---

## D1 — the test

A unit is **identity-bearing** iff all three hold:

- **individuated** — this one is distinguishable from another of its kind,
- **persistent** — it is the same one across the time the claim spans,
- **predicated on** — the claim attaches a property, interest, or continuity
  to it, rather than to something it does.

Failing any one makes the framing **non-identity**.

Not part of the test: whether the unit is human, alive, agentive, or
morally considerable. Valence is off, per the work order.

---

## D2 — the three borderlines the work order names

### population — **COUNTS as identity-bearing**

Individuated (this population, not that one), persistent (it has a size at
t and at t+1 and they are the size of the same thing), predicated on (`the
population declined`). All three hold.

**This is the decision that moves the count most, and it moves it against
the work order's own prediction.** T2 predicts non-identity framings appear
where the substrate forces it — naming ecology first. Ecology's most common
unit is the population. Under D2 that unit is identity-bearing, so ecology
does not get the score its substrate was expected to buy it. The decision is
kept because the test gives it, not because the outcome is wanted.

### niche — **DOES NOT COUNT: non-identity**

Persistent, arguably individuated, but a niche is a region of a condition
space, not a carrier. Claims attach to what occupies it (`the niche was
filled`), and the niche is the slot. Fails *predicated on*.

### market — **RESOLVED AT THE CLAIM, NOT AT THE NOUN**

`the labour market tightened` predicates a property on a persistent
individuated thing: identity-bearing. `prices allocate scarce goods`
predicates on a mechanism: non-identity. Same noun, two answers.

**This is the general result and not a special case for `market`.** Every
borderline the work order names is decidable at the claim and undecidable at
the word, which is why a lexical scan cannot do this job — the same reason
T1 exists. A word list would have to file `market` once, and either filing
is wrong half the time.

---

## D3 — the rest of the borderlines, decided in advance

Decided before running so that a case met during the run cannot be decided
by what it does to the count.

| unit | decision | which test decides it |
|---|---|---|
| firm, organization, institution | identity-bearing | all three hold |
| species, lineage | identity-bearing | all three hold |
| gene, replicator | identity-bearing | all three hold |
| cohort, generation | identity-bearing | as population, D2 |
| individual, agent, household | identity-bearing | all three hold |
| state, nation, jurisdiction | identity-bearing | all three hold |
| role, office, position | non-identity | fails *predicated on* — the holder is the carrier |
| process, practice, procedure | non-identity | fails *individuated* |
| flow, flux, throughput | non-identity | fails *individuated* |
| field (physics sense) | non-identity | no carrier; a function on a domain |
| equilibrium, steady state | non-identity | a state, not a thing in a state |
| feedback loop, coupling | non-identity | fails *individuated* |
| rate, gradient, elasticity | non-identity | fails *individuated* |
| norm, convention | **identity-bearing**, contested | persists, is individuated, and claims attach properties to it (`the norm eroded`). Recorded as the weakest call on this table |
| system, network | claim-level, as D2 `market` | a named persistent network is a carrier; `network effects` is a process |
| information, signal | non-identity | fails *individuated* |

---

## D4 — what counts as UNDECIDABLE

A third value, not a tie-break. The classifier returns `UNDECIDABLE` when
the main causal claim has no extractable subject, or when the subject is a
pronoun or determiner with no resolvable antecedent inside the abstract.

`UNDECIDABLE` is **not** counted toward either arm, and is reported as its
own proportion. Folding it into `identity-bearing` would inflate the
hypothesis under test; folding it into non-identity would inflate its
negation. Both are available and neither is taken.

This is the `unrecorded`-not-`absent` rule the register already runs on,
applied to a classifier output.

---

## D5 — what this file cannot decide

The test in D1 is applied to the claim as written. It does not reach the
framing the author held and did not write. A paper whose apparatus is
entirely relational and whose abstract closes on `firms respond to` is
scored identity-bearing here, correctly by the stated rule and possibly
wrongly by the question the work order asks.

That gap is not closable from abstracts. Naming it is not a hedge on the
result; it is the size of what the result is about.
