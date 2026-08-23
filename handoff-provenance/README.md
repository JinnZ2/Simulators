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
python3 provenance.py            # tags, the ordering rule, the re-read column
python3 diff.py                  # carried / dropped / added, matcher graded
python3 excluded_register.py     # the third category, counted two ways
python3 ledgers/seed.py          # the seed ledger, and what it cannot establish
python3 ledgers/spec_v0_2.py     # the v0.2 ledger, and the first real diff
```

Each takes `--selftest`. 38 / 40 / 15 / 20 / 25 checks, 138 in all, green.
Samples are pinned in `samples/` and are byte-reproducible.

## The four modules

### `provenance.py` — the tag, and the ordering rule enforced

Seven tags: `[K]` operator-stated, `[K~]` operator-stated with the
**translation flagged lossy at time of speaking** — shape present, English
suspect, `[K?]` operator-stated per the ledger but **not confirmed**, `[R]`
repo-derived with a path, `[C]` proposed and not objected to, `[A]` proposed
and explicitly accepted, `[X]` the downstream model's own addition.

`[K~]` requires the flag to be located. Without that, the entry records the
downstream model deciding the English looked shaky, which overrides the
operator's confidence rather than recording it.

`[C]` and `[A]` are separate because **silence is not acceptance** — the same
rule as `inverseminar/`'s `unprobed` verdict, which is logged as a miss and
never as a confirmation.

The spec says the ledger "is written BEFORE the spec prose, not extracted
after". That is enforced rather than stated: `seal()` freezes a ledger and
`add()` afterwards raises `SealError`. A ledger extracted from finished prose
cannot fail, which is why the ordering had to become a code path.

`entry()` refuses an `[R]` with no path and an `[A]` with no located
acceptance.

### `[K~]` split two axes the module had conflated

One constant, `GROUND_TRUTH`, was answering two different questions at once:
*is this confirmed to have been said?* and *can the matcher be trusted on it?*
For `[K]` and `[K?]` those answers move together, so a single constant worked
and the conflation never showed. `[K~]` separates them:

| | tags | what it is |
| --- | --- | --- |
| `STATED` | `[K]` `[K~]` | the population the channel loses things from |
| `MATCHER_SCORABLE` | `[K]` | what the matcher can be trusted on |

A `[K~]` that does not match cannot be read as DROPPED: *"the English was
wrong, so the stems miss code that does implement the shape"* is a live
alternative and nothing here separates it from absence. So `[K~]` entries are
refused rather than scored — the same repair as `NEGATED`, at the translation
layer instead of at the polarity of the sentence — while staying inside
`n_stated`, because they **were** said. **The gap between the two
denominators is the translation layer's footprint**, and it is the only
quantity here that measures it. It stays a count: a share over a handful of
entries reads as a precision it does not have.

The cost has no defence in the module and is printed anyway: flagging an
entry lossy removes it from the measurement, so an operator who flags
liberally shrinks `n_scorable` until the rate runs over almost nothing — and
that reads exactly like a clean channel. The footprint prints beside it.

### The re-read column — two entries, never summed

| | what changed | measures | effect on a diff already taken |
| --- | --- | --- | --- |
| `SHIFT` | the item reads differently; the observing position moved | **the station** | `STALE_NOT_WRONG` — a prior verdict was about a different item |
| `RETRANS` | the item reads the same; the English was wrong the first time | **the translation layer** | `POSSIBLY_FALSE_CARRIED` — a prior verdict was taken against wrong English |

Both produce **one** observable: the line's text changed. The discriminator is
whether the *shape* moved, and that is not in the text — so `reread()`
requires the kind to be operator-attributed and refuses to infer it. It also
refuses an unchanged re-read, which is a confirmation and not an event in this
column. Summing the two would give a number meaning "the ledger churned",
which answers neither question.

**`RETRANS` is the only route by which the spec's fourth failure mode ever
becomes visible here.** It is not detection — it is the operator noticing from
upstream and reporting back down — so a `RETRANS` count is a **lower bound** on
voice-layer mangling, never a measurement of it.

A `RETRANS` on a `[K~]` does **not** promote it to `[K]` unless the caller
passes `still_lossy=False`. The tempting default is to read a retranslation
offered without a fresh flag as no-longer-lossy — but that reads silence as
acceptance, which is the rule the `[C]`/`[A]` split exists to enforce. The
module applies its own rule to itself here, and the cost is that `[K~]`
entries accumulate.

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

### `ledgers/spec_v0_2.py` — the first real denominator, and it read wrong

`seed.py` had to tag every operator-stated line `[K?]`. This delivery is
in-session and quotable, so *"was this stated upstream"* is answerable here.
Eleven `[K]` entries, sealed, **committed in their own commit ahead of the
commit that implements them** — `Ledger.seal()` can only prove nothing was
added after `seal()` inside one process, so putting the ordering in git
history is the first artifact here an outside reader could use to falsify the
ordering claim. Evidence, not proof: history is rewritable.

Eleven entries cleared the ten-entry reportability floor. **The first
reportable drop rate this module ever produced was 0.09, and it was wrong.**

The single DROPPED item — `[K~] is a tag, added to the existing tag set` — is
plainly carried; `[K~]` is in `TAGS`. The matcher scored it on `added` and
`existing` alone, because `tag` and `set`, the two words carrying the claim,
are three letters and the length floor is four. Share 0.50 against a 0.55
threshold: **a false DROPPED by two hundredths**, and it cleared the floor
that makes a rate reportable.

`coverage()` now measures how much of an entry the floor eats, and `match()`
refuses the entry when most of its content words go — a share over the
minority that survived is not a reading of the entry. The line is a
**majority**, set as a principle and deliberately not at the value that
rescues the entry that exposed it; the eight-fixture matcher grade is
unchanged. None of that makes it a rule chosen before the data. Both numbers
print, side by side.

**It does not fix the blindness.** An entry losing one content word of four is
still scored, with that one unseen. `the doe performs partner selection` loses
only `doe` — so the spec's flagship DROPPED instance is a doe-choice arm, and
the instrument measuring it **cannot see the token**. Any three-letter subject
is in the same position: arm, gap, key, ice.

### A docstring can earn a CARRIED

The 0.09 run then stopped reproducing — because writing the report put the
ledger's own entries verbatim into `diff.py`. That instability exposed a
larger defect than the one it interrupted: **matched against raw source, a
ledger entry scores against any prose in the file that repeats it.** A module
documenting an item it never implemented reads as having carried it, and the
effect is strongest exactly where ledger and code come from one party in one
pass.

`implementation_surface()` strips docstrings, comments and the disclosure
functions (`report`, `selftest`, `breaks`, `confidence`, `main`, `_wrap` — the
uniform surface every module in this folder carries, and where entries get
quoted in order to be printed). String literals in expressions stay: a gloss
table mapping `SHIFT` to `"the station"` **is** the implementation of "SHIFT
is data about the station"; a docstring saying the same sentence is not.

On the stripped surface the v0.2 rate is 0.00 over ten scorable entries, and
the seed ledger's verdicts are **unchanged** — so nothing it carried had been
earned by prose. That is checked, not assumed. It still isn't a measurement of
the channel: a self-diff scores code written to satisfy the ledger. Read 0.00
as an upper bound on carriage.

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
  after `seal()` was called in this program. `spec_v0_2.py` is the first
  ledger here written before its implementation, and git history is the
  evidence.
- **Zero `[K~]` entries and zero re-reads on the seed ledger is
  `NOT_YET_OBSERVED`, not zero.** Nothing has been read a second time and
  nothing was flagged lossy when spoken, so both columns are empty for want of
  observation, not for want of loss.
- **`reread()` cannot check the attribution it requires.** A caller who labels
  every re-read `RETRANS` produces a clean-looking station and a filthy
  translation layer, and nothing here objects.

Confidence is a separate readout on every module and is not resolved, per the
spec.

CC0. Standard library only. Parses under Python 3.9. Phone-buildable.
