# handoff-provenance

**Marker under exploration. Continuous work in progress.** The delivered
spec is [`SPEC_V0_1.md`](SPEC_V0_1.md), landed verbatim. Everything else in
this folder is the audit of it: four stdlib modules that run, refuse, and
report where they break.

The object under test is **the channel between conversation and code**, not
either endpoint. Loss across it is currently silent: a variable stated aloud
and absent from the code is indistinguishable from a variable never stated.
Ground truth exists — the conversation is upstream, the code is downstream —
and nothing links them, so the drop is unlocatable after the fact.

```
python3 provenance.py            # the tags and the ordering rule
python3 diff.py                  # carried / dropped / added, matcher graded
python3 excluded_register.py     # the third category, counted two ways
python3 ledgers/seed.py          # the seed ledger, and what it cannot establish
```

Each takes `--selftest`. 16 / 25 / 15 / 17 checks, 73 in all, green. Samples are
pinned in `samples/` and are byte-reproducible.

## The four modules

### `provenance.py` — the tag, and the ordering rule enforced

Six tags: `[K]` operator-stated, `[K?]` operator-stated per the ledger but
**not confirmed**, `[R]` repo-derived with a path, `[C]` proposed and not
objected to, `[A]` proposed and explicitly accepted, `[X]` the downstream
model's own addition.

`[C]` and `[A]` are separate because **silence is not acceptance** — the same
rule as `inverseminar/`'s `unprobed` verdict, which is logged as a miss and
never as a confirmation.

The spec says the ledger "is written BEFORE the spec prose, not extracted
after". That is enforced rather than stated: `seal()` freezes a ledger and
`add()` afterwards raises `SealError`. A ledger extracted from finished prose
cannot fail, which is why the ordering had to become a code path.

`entry()` refuses an `[R]` with no path and an `[A]` with no located
acceptance. Only `[K]` is ground truth for the DROPPED measurement; `[K?]` is
excluded from it.

### `diff.py` — and the matcher is graded before it is trusted

CARRIED / DROPPED / ADDED, per the spec. Two things sit on top.

**The matcher is the instrument.** Deciding whether a ledger line is present
in delivered code is a text-matching judgement, and the same problem already
produced two opposite failures in this repo — `measurement-fork/`'s classifier
over-matched on one corpus and under-matched on another, with no single
threshold fixing both. So `match()` is graded on known-carried and
known-dropped fixtures and reports a `null-harness/` grade. A DROPPED count
from an ungraded matcher is not a measurement, and the grade prints beside the
count. The threshold sweep shows the grade moving, so 0.55 is a choice.

**CARRIED is split.** A `[K?]` entry that matches lands in
`CARRIED_UNCONFIRMED`, counted apart. This is the only handling available for
the spec's fourth failure mode: a mangled transcription produces a ledger
holding the wrong version, code implementing the wrong version, and a diff
reading CARRIED. No matcher can see that. The split does not detect it — it
refuses to count it as evidence.

### `excluded_register.py` — the third category, in one place

EXCLUDED-BY-CONSTRUCTION is not a handoff failure; it is the model's own
ontology refusing a case, and the diff cannot see it. The spec says log the
instances in one place rather than per-repo, so the register **imports**
`instrument-bias-sims/excluded_subject.py` rather than duplicating it.
Importing beats copying and it is not independence.

**The spec's count of three is reached by two different routes and they name
different instances.** Derivation-level exclusion gives S4, S9, S10.
Ontology-refusal gives S4, S10, S10/M4 — S9 drops out, because nothing filters
there by design and its empty slot is a correct representation rather than a
refusal. Both are printed. The register does not pick one: picking would
settle a question about what the category means by arithmetic.

### `ledgers/seed.py` — the seed data, and the one thing it cannot establish

The spec names S4's doe-choice arm as DROPPED, and DROPPED requires the item
to have been stated upstream. **This side of the channel has no access to the
conversation upstream of a delivered work order.** What is verifiable from
here is that the S4 work order as received contained no doe and the delivered
patch said "was missing entirely" — consistent with DROPPED and equally
consistent with never-stated, and the diff cannot tell those apart.

So every operator-stated seed entry lands as `[K?]`, the drop rate is `None`
rather than zero, and the fourth failure mode is instanced on the first real
data rather than avoided. One operator confirmation converts an entry;
nothing else does.

## The sixth entry broke the matcher

The seed ledger has six lines. One of them is `remove unused rng and
statistics import`. It matched the delivered S4 code at share **1.00** — the
matcher's maximum — while `import statistics` is **absent** from that file:
the words survive in the prose describing the removal.

For an entry asking that something be taken **out**, presence of its stems is
evidence the item was **dropped**. The matcher does not merely mis-score a
negated entry; it inverts it, and it does so at full confidence.

The entry was left unchanged and the instrument was changed instead.
`match()` now returns `matched=None` with state `NEGATED`, and `diff()` routes
those entries to `UNSCORABLE_NEGATED` — out of both counts and out of the rate
denominator. **`None` is not `False`**: "the instrument cannot read this
entry" is a different state from "the item is absent from the code". That is
the recurring repair this audit tracks across the repo — one value standing
for a measurement and for its absence — and the running count in
`docs/FOLDER_NOTES.md` had reached twelve before this one. Here it was forced
by one real ledger line out of six, after eight hand-written matcher fixtures
had all been positive entries.

The negation detector is itself graded on four negated and four positive
fixtures, because a detector that never fires would restore the inversion
silently. Its limit is stated in `breaks()`: it is a cue list, and *"the
module runs on two arms rather than a constant"* asks for a removal, contains
no cue, and gets scored as a positive entry. What the detector buys is that
the cases it catches are refused instead of counted backwards.

## What is not measured

Per the spec's own OPEN section, and not softened:

- **No baseline drop rate.** There are zero confirmed `[K]` entries, so there
  is no denominator. The spec says the first several runs *are* the baseline.
- **No measurement of whether tagging changes the drop rate.** That needs two
  arms and one has not been run.
- **`ADDED` is supplied by the caller, not detected.** Nothing scans delivered
  code for items with no ledger entry, so the `[X]` column is only as complete
  as whoever filled it in — and attribution creep is precisely the case where
  they did not.
- **The seed ledger was written after the code existed**, which is the
  opposite of the ordering rule. The seal proves only that nothing was added
  after `seal()` was called in this program.

Confidence is a separate readout on every module and is not resolved, per the
spec.

CC0. Standard library only. Parses under Python 3.9. Phone-buildable.
