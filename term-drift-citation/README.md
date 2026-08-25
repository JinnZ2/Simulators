# term-drift-citation

**Marker under exploration.** Delivered spec: [`SPEC_CITATION.md`](SPEC_CITATION.md),
landed verbatim and also placed in [`PREAMBLE.md`](../PREAMBLE.md).

> A citation carries a measurement forward under a word. The citation is only
> valid if the word's referent held between the measurement and the use.
> Nothing in a citation records whether it did.

```
python3 citation.py     # the three questions, the worked cases, the safety run
python3 asymmetry.py    # does the revision direction ever cost the reviser
```

Both take `--selftest`. 28 / 22 checks, 50 in all, green. Samples pinned in
`samples/`, byte-reproducible.

## The verdicts that must not be confused

The check is three questions — what was the referent at time of measurement,
what was load-bearing in it, is that element present now. But the module's real
work is holding three things apart that a single score would merge:

| field | what it says | what it never says |
| --- | --- | --- |
| `verdict` | TRANSFERS / DOES_NOT_TRANSFER / UNASSESSED | whether the original was right |
| `original_result` | `NOT_ASSESSED_HERE`, permanently | — nothing here measures it |
| `retest` | RETESTED / NOT_RETESTED / **NOT_INSTANTIABLE** | REFUTED — not a value in the set |

**DOES_NOT_TRANSFER is not REFUTED.** The spec says it in one line — *the
result may be correct and still not attach* — and that line is why this is a
separate field rather than a score.

**Absence of retest is not refutation, and sometimes there is no retest to be
absent from.** Holling is `NOT_INSTANTIABLE`: testing it needs a system with
slack in it, and where slack was optimised away the original claim cannot be
retested at all. Folding that into "unsupported" would convert the
disappearance of the test bed into evidence against the claim.

All three delivered cases come back `DOES_NOT_TRANSFER` — and **the module
could not have returned anything else**, because each arrived with its status
already stating the load-bearing element was removed. The verdict is the input
restated in a type. What the module adds is the fields the verdict must not be
confused with. There is also no negative control: every worked example drifted,
so nothing here shows what a citation that *does* transfer looks like run
through the same three questions.

## The safety case, run

*"Frozen variables do not stop existing; they stop being read. Metric can
improve while facility degrades."* That is arithmetic, so it is run rather than
restated. One facility, six variables, five of them dropped from scope:

| t | metric (read now) | whole facility |
| --- | --- | --- |
| 1 | 0.750 | 0.925 |
| 3 | 0.850 | 0.875 |
| 6 | **1.000** | **0.800** |

The narrow metric climbs **+0.250 to a perfect score** while the facility falls
**−0.125**. The narrow metric is not wrong. It is correct about what it reads.

It is a demonstration, not evidence: compliance starts low and is worked on
*because* it is what is read, everything unread decays at a fixed rate, and the
rate was chosen to make the effect legible. It establishes the mechanism is
available, not that it occurred anywhere.

## "Frozen" means different things in your two specs

Worth surfacing rather than quietly reconciling — one week apart:

- **`SPEC_SHAPES.md`**: *"FROZEN entries are declared by the builder, not
  inferred."*
- **`SPEC_CITATION.md`**: *"Frozen variables do not stop existing; they stop
  being read."*

The safety case's unread variables — air handling, water, ergonomics, office,
floor — were declared by nobody. The scope contracted and they fell out. Under
the first spec's own constraint they are **UNDECLARED**, and calling them
FROZEN is exactly the inference that spec forbids.

Three readings are printed and **none is picked**: `UNDECLARED` (fits the
constraint, misses that they keep moving), `ASSUMED_FROZEN` (fits why the
metric can diverge — it needs them presumed constant *and* changing — but
`SPEC_SHAPES` has no such state), and `SAME_WORD_LOOSELY` (the notes were
delivered separately and neither cites the other). Which holds is a question
about what was meant. `PREAMBLE.md`'s own TERM COLLISION note is the instrument
for this, and its rule is that the senses get named, not merged.

## The asymmetry, tallied — and it does not flatter this session

*"Check whether the revision direction ever costs the reviser. If it never
does, the revision is a routing rule."*

That is a tally, so it is run as one. Two populations, counted apart, because
revising your own work in progress and revising a predecessor's are different
objects and **only the second is what the test is of**:

| | n | COST |
| --- | --- | --- |
| own work, in progress | 4 | 3 |
| someone else's, earlier | 1 | **0** |

Every self-revision in this session cost something — the NEGATED state removed
a CARRIED scoring at the matcher's maximum, `implementation_surface()` made
carrying harder to earn, the word-boundary fix shrank this work's own finding
count from 8 to 3.

The one **predecessor** revision cost nothing. The N-body figure in
`SCALING_CLASSES` was marked `CONSTRUCTION_FITTED` against the source — framed
as *the source was deficient*. The correct reading was `DIFFERENT_OBJECT`: the
term was printed in the source label and lost in transfer. It cost the reviser
nothing until an outside party caught it, and **the outside party was the
operator, not the reviser**. That is the asymmetry the spec describes, with
this session on the wrong side of it.

**And n=1 establishes nothing.** "Never costs" is falsified by one
counterexample and confirmed by no number of non-counterexamples, so the
`ROUTING_RULE` verdict is a description of one revision, not a property of a
practice. The contrast is 4 rows against 1.

Worse, the ledger is **self-assessed by the party it is about**. A reviser
wanting to look even-handed would produce exactly this ledger — self-revisions
costing, the awkward row disclosed. Every row carries a commit so an outside
reader can check it; that is the only defence available and it is not the same
as an outside assessment. And the sampling is biased toward rows that got
caught: the one FREE row is here *because* the operator objected, and a free
revision nobody objected to would have left nothing to log.

## A word is not a measurement — and this module does not decide which words are

A term without a quantity, a sign, or a formal definition in its field's
equations is not carrying a measurement, and must not be loaded. Whether a
given term has those is an assessment about a field, so all three fields
default to `UNASSESSED` and `carries_a_measurement()` refuses rather than
guessing — the same constraint as `scope-bound-shapes`' FROZEN list.

That holds even where the delivered text arguably supplies the answer:
Holling's referent is given as *"magnitude of disturbance absorbable before
state shift"*, which reads like a quantity with a sign. Filling the field from
that would be this module deciding what counts as a formal definition in
ecology. **UNASSESSED is not "no"** — a word that has not been checked is not
thereby a word that fails the check, and it is still not loadable.

CC0. Standard library only. Parses under Python 3.9. Phone-buildable.
