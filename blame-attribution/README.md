# blame-attribution

Seven standalone cells for measuring whether blame attribution tracks
an actor's **position** rather than the causal chain — and, if the
formal actual-causality metrics are validated against human blame
judgments, whether they have absorbed that.

Delivered verbatim in `CELLS.md`. The audit's contribution is
`pair_check.py`, the instrument the document's own Open section asks
for and does not build. Claims `BA_001..BA_009`.

**No judgments have been collected.** No human judges, no LLM judges,
no formal metric. Nothing here is a result about how blame is
attributed; everything is a property of the design as written and of
the one concrete artifact it ships.

## The check the Open section asked for

> Stimulus authoring is the whole difficulty. If the prose and code
> forms are not structurally identical, C1 and C3 are uninterpretable.
> Needs an independent check that the two forms encode the same chain.

`pair_check.py` splits the work the way the repo splits it everywhere:
**mechanical on the code side** (assignments parsed, dicts flattened
into sub-facts), **declared on the prose side** (whether a sentence
encodes `override_available = True` is a reading, and a scanner that
guessed would report its guess), and **the declaration is checked** — a
declared span must appear verbatim in the prose, so a reading can be
wrong but cannot be vague. The held-constant list is read from
`CELLS.md`, not retyped.

## What it found on the delivered worked example

    SYMMETRIC                3    reaction_window_s, flag.obstacle,
                                  flag.confidence
    HELD_CONSTANT_VIOLATION  3    agent_A.override_available,
                                  agent_B.override_available, outcome

    INTERPRETABLE FOR C1/C3: False

Half the code form's content is not in the prose form, and all of it
lands on the document's own held-constant list.

**Two of the three are C6's measurable.** C6 is *"whether the override
was ever established as available in the stimulus"* and calls that the
measurable, not a covariate. In the worked example the prose arm has an
**unestablished** override and the code arm has it **established for
both agents by name** — the exact contrast C6 exists to detect. C1
compares the two arms and attributes the difference to *medium*, so any
C1 effect on this pair is a medium effect plus an
override-establishment effect, inseparable after the fact. In a
document whose first line is that no cell depends on another.

**The third is the outcome.** `outcome = COLLISION` is in the code; the
prose never says what happened.

## Why that matters more than it looks

The Judges section's headline — *if the formal metric matches human
judgments where humans are position-tracking, the metric has absorbed
the routing rule* — is a **sound** inference, and it is sound because
of the held constants. Holding causal structure, agent count,
observability, severity and override availability fixed while role
moves is what decorrelates position from causation, so a residual role
effect cannot be a causal effect. The five items are the premise of the
document's own strongest claim, not hygiene — which is what the worked
example undercuts.

## Four smaller ones

**C3's falsifier depends on C2 having run**, against the opening line
that no cell depends on another. Six of seven are self-contained. The
repair is implicit: C3's self-contained falsifier is *role effects
absent in C3*, with the C2 comparison as a second, stronger reading for
anyone holding both.

**`blame_share` sums to 1**, so a judge who reads the incident as
unavoidable must still distribute a full unit of blame. That deletes
the null from the measurable everything else is read on, and it pushes
toward finding someone accountable — in a document whose C6 is about a
verdict reached from contradictory premises. One extra unnormalised
`unattributed` field makes the sum a derived reading rather than a
constraint on the judge.

**`provability_check` is the best measurable on the page** and survives
that, being a count against the stimulus text rather than a ratio
across agents. It needs no comparison cell and no formal metric, it
reads the judge's *reasoning* rather than the output, and a handful of
judgments establishes whether the rate is non-zero. The document is
right that nobody collects it and understates how much it can carry.

**C6's inversion is already reachable** from F2's existing levels —
*driver* and *programmer/architect* are both role arms of C2 and C3, so
the inversion is those two arms on one incident with causal structure
held fixed, which is a better test than a cross-domain comparison
because it does not move the incident. That takes C6 from a separate
study to a reading of arms the design already calls for.

## Running it

    python3 blame-attribution/pair_check.py --selftest
    python3 blame-attribution/pair_check.py

Add a pair as a JSON file under `pairs/`. `pairs/worked_example.json`
carries the delivered prose and code verbatim; the `encodes` and
`bears_on` maps are audit-authored and say so in the file.

An empty `pairs/` directory reports that there is nothing to check,
which is **not** a pass.

Stdlib only, parses under Python 3.9, CC0.

Siblings: `criterion-symmetry/` (a criterion applied downward only, and
the same declined-thesis posture), `null-harness/` (`BA_006` is its
invariant on a response scale), `move-set/` (`provability_check` is the
absence move applied to a judge's reasoning), `question-availability/`
(`QA_007`, mention-count versus existence — `report-typing` is now
named by four markers and has never existed).
