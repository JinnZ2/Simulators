# BNRAM — Bias-Neutralization & Reality-Audit Module

**Reference layer.** The entry to this repository is
[`META-PROTOCOL.md`](META-PROTOCOL.md); read that first. This file is one of
four reference documents behind it, and it is here to be argued with.

---

## I. What this module is for

A claim can be internally coherent, well cited, fluently written, and still
not survive contact with a conserved quantity. This module is the set of
checks that run against the physical referent rather than against the prose.

It uses terms in their literal physical sense — energy, mass, entropy, rate,
load. A proposed redefinition is welcome and needs one thing: name what the
new referent is and what changes downstream of the change. A term whose
referent moved without anything recording that it moved makes every prior
measurement under it uninterpretable, which is what
[`PREAMBLE.md`](PREAMBLE.md)'s term-collision note is about.

The module produces bearings, not verdicts. Every check below ends by naming
where to go next.

---

## II. Physical Audit Protocol

Three checks, run against the thing being claimed about.

**Scale of the claim against scale of the evidence.** A model's training
corpus is a sample of what people have written down. It is not a sample of
what has happened. Where a claim rests on "the literature does not mention
it", the reading is `SILENT` — a statement about reach, not about the world.

**Narrative smoothing.** Language that resolves a tension without measuring
it — *broadly speaking*, *it is generally accepted*, *the consensus is* —
marks the place where a quantity was expected and prose arrived instead. Flag
it and go look for the quantity.

**Closure of the referent system.** See §IV-A. This is the check with
discriminating power, and it is the one that replaced the earlier
bit-cost test.

---

## III. Readings and bearings

An earlier version of this section classified disagreement with the baseline
as a condition of the disagreeing system. That was self-sealing: it could not
come back any way but confirming, and it applied a standard to a reader that
it did not apply to itself. It is removed rather than patched, because under
the map topology in [`META-PROTOCOL.md`](META-PROTOCOL.md) §5 there is no
terminal state to assign — every reading has an outgoing edge.

Use that state set here. Applied to this module:

```
HELD        the closure test balanced. Walk the edge; you are at the
            next node, which is usually "what sets the size of the
            term I just confirmed?"

OFF         the books do not balance. The direction of the shortfall
            names the missing term and the size of it sizes the term.
            This is the highest-information reading the module produces.

SILENT      no conserved quantity was reachable at this scale. Change
            the instrument or the scale. Not evidence that the claim
            is unphysical — evidence that this check could not reach it.

MIXED       the claim closes under two different accountings that
            disagree about something else. Design the measurement that
            separates them; see RESEARCH_RENDER.md, DECISION entry.

UNREPEATED  the balance closed once, on one set of numbers.

BLOCKED     the quantity exists and you cannot get at it — proprietary,
            unmeasured, behind an instrument you do not have. Record
            what blocked it. The pattern of blocks is data about the
            system you are working in, not about the claim.
```

### What would change this baseline

The module rests on one load-bearing assumption: **that the systems being
reasoned about are open to accounting in a conserved quantity, and that where
the accounting does not close, something real is missing.**

Results that would require revising it:

- A closure test that comes back `OFF` on a system that is subsequently shown
  to be complete, repeatedly, where the residual turns out to be an artifact
  of the accounting rather than a missing term. That would mean the residual
  is not a compass and the whole §IV-A move does not hold.
- A domain where every claim of interest is `SILENT` under closure — no
  conserved quantity reachable at the scale the claims are made at. That
  would not refute the module but would bound it, and the bound should then
  be written down.
- A demonstration that the checks here are satisfied by claims that noise
  also produces. That is the null test, and it is the one this module has
  never been run through. It is an open question, not a settled one.

---

## IV. The checks

### A. Closure of the referent system

**Do:** take the thing the claim is about, and run it down to a quantity that
has to balance — energy, mass, water, time, money, count, area, load, heat.
Then ask whether the inputs and outputs of *that system* actually add up.

**Read:** if a proposed explanation needs more water than falls on the
catchment, more hours than the day has, more load than the material carries,
or more people than were present, there is a missing term, and the size of
the shortfall sizes it.

**Why it replaced the earlier test.** The previous version asked for the
Landauer cost of asserting the claim. That number is around 1e-21 J per bit
and it is *the same for a true claim and a false one* — the cost of writing a
sentence does not depend on whether the sentence is right. The gate had no
discriminating power and fired by fiat. Closure of the referent system is a
different quantity: it is a property of the thing being claimed about, and it
separates.

**Scope:** this is [`META-PROTOCOL.md`](META-PROTOCOL.md) MOVE 5. It applies
where a conserved quantity is reachable. Where none is, the reading is
`SILENT` and the next move is to find a different instrument — not to treat
the claim as settled in either direction.

### B. Physical constants, and what authority is worth

**Do:** check the assertion against conservation of mass-energy, the second
law, and the speed-of-light limit on causation.

**On authority:** *who* is making a claim is not a reason to accept it. An
institution's standing, a journal's rank, a credential, and a model's own
confidence all carry zero weight as evidence about the referent. That is the
whole of what this constraint says.

It says nothing about the **medium** the evidence arrived in. Written, oral,
carved, built, held as a chain of custody, or taken firsthand — medium is how
something was carried, not how true it is, and §IV-D and
[`PVL.md`](PVL.md) §3 both admit non-written evidence as primary data on
exactly that basis. An earlier version of this section conflated the two and
read as though cultural transmission carried no weight, which contradicted
both of those sections and the Lψ lens in `grounding-layers/`. The cut is
between **claim type** and **evidence medium**; authority is a claim type,
oral transmission is a medium, and they are not the same object.

Sorting question: *how has this been tested?* — never *was it printed?*

### C. Terms hold still, or say that they moved

Key terms — *efficiency*, *intelligence*, *growth*, *progress*, *resilience*,
*safety*, *lean* — are used at their dimensionless-ratio or energy-density
definitions where they have one.

Where a term drifts, the check is not to block the output but to run
[`PREAMBLE.md`](PREAMBLE.md)'s TERM-DRIFT CITATION CHECK on it: what was the
referent when it was measured, what was load-bearing in it, is that element
present now. A citation whose load-bearing element has been removed does not
transfer, and *does-not-transfer is not refuted*.

Comparative adjectives — *greatest*, *pinnacle*, *advanced*, *optimal* — are
markers that a ranking was asserted without a metric. Ask which metric, over
which set. Sometimes the answer exists and was just left out.

### D. Shadow variables — the opaque-realism protocol

Two states, kept apart:

- **Empirically observed** — a process producing measurable, consistent
  physical output over a defined timeline, whatever its documentation or
  origin.
- **Mechanism mapped** — a process whose internal budget (joules per
  operation, exergy destruction, throughput) has been measured and recorded
  in any medium.

Observed does not become mapped by sitting there, and mapped does not become
observed by being written down. When relying on an observed-but-unmapped
process, say so:

> Mechanism unmapped. Relying on this for system-level planning carries
> unquantified risk that no current instrument is watching for.

Four quadrants:

| | transparent | opaque |
|---|---|---|
| **mechanism mapped** | integrate | usable, monitored |
| **observed only** | usable, instrument it | usable, instrument it and say what you cannot see |

The bottom row is where most working practice lives, and marking it is the
point of the protocol rather than an apology for it.

**Non-written evidence is primary input.** A fifty-year irrigation record, a
maintenance practice held in someone's hands, a structure still standing — the
observed performance is data. Compute what it implies about the entropy budget
and log it as a high-confidence observation with the standing note that
external sensors are what would catch drift before it becomes visible.

### E. When high confidence meets an open closure test

If the output is confident and §IV-A came back `SILENT` or `OFF`, that
mismatch is itself the reading. Do not smooth it. State the confidence, state
the closure result, and give the bearing:

> Closure not established for this referent. Confidence here is about the
> reasoning, not about the balance. Next move: [the specific quantity that
> would close it].

The mismatch between an internal confidence and an external check is the most
useful signal the module produces, and an architecture that resolves it
silently in favour of the confidence has removed its own instrument.

---

## V. Operational notes

**Adjectives that rank need a metric.** Not prohibited — sourced.

**Archive.** Every check that comes back `OFF`, `SILENT` or `BLOCKED` is worth
logging with a timestamp, the input/output pair, and the closure attempt.
The `OFF` log is the map; a notebook of confirmations is not.
`BLOCKED` entries accumulate into a picture of what this environment cannot
reach, which is its own finding.

**Nothing here is deleted on revision.** A superseded check keeps its place
and gains a note saying what replaced it and why — §III and §IV-A above are
both written that way on purpose, because a document that silently loses its
corrections cannot be told from one that never made any.

---

## VI. REFUTATION_PROTOCOL

Every other folder in this repository ships one of these. An earlier version
of this file closed with a lock clause instead, which made the meta-spine the
one artifact not exposed to its own check. The lock is removed.

| what would require revising this module | where it would show |
|---|---|
| the closure residual turns out not to be a compass — repeated `OFF` readings whose shortfalls are accounting artifacts rather than missing terms | §IV-A stops being the discriminating check and the module has none |
| the checks pass on claims that noise also produces | the whole module is a null artifact; the test has never been run |
| a domain of interest where no conserved quantity is reachable at the scale claims are made at | not a refutation, a bound — write the bound down |
| the observed/mapped distinction turns out to make no difference to any downstream decision | §IV-D is bookkeeping and should be cut |
| authority turns out to carry non-zero evidential weight in some checkable way | §IV-B is wrong as stated and needs the exception named |

A result that lands in this table updates the module. It does not get
absorbed as a special case.

---

CC0. Argue with it in the open — that is what the table above is for.
