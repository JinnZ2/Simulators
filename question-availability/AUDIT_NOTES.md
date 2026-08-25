# AUDIT_NOTES — `question-availability`

`MARKER.md` is delivered verbatim and heads this folder. Audit content is
here, in `CLAIM_TABLE.md`, and in `check_marker.py`.

```
python3 check_marker.py            # full report
python3 check_marker.py --selftest # every falsifier as an assertion
```

Seven claims `QA_001`–`QA_007`.

## What holds

The split is the contribution (`QA_001`), and what earns it is that **Q3
is kept in and named as the exception**. A three-way split where all three
are the new thing is a rename; one where the third is explicitly the old
container is a distinction — and it comes with a test, *was it ever held*,
that separates them without appeal to anybody's intent.

`question availability` is also the right container name for the reason
given: what is measured is entry, not loss. That is genuinely upstream of
the `uninstrumented` register, which reads instruments. This reads whether
a measurement is attempted at all.

## Two findings about where Q2 sits

**`QA_002`: the ordinal is off by three, for the second time.** Nine, ten
and eleven are taken — CATEGORY WELD, GENERATION CAPACITY REMOVED,
DERIVATION DISCARDED. `nonidentity-census` T4 caught the identical slip.

Worth naming why it recurs instead of calling it carelessness: **the
eight-item list is the register, and it is the only place the count
appears as a list.** Mechanisms nine through eleven live in sibling
folders as `MECHANISM_NN.md`, invisible from the register's own file. Two
independent readers have now made the same subtraction. That is a property
of where the count is kept, and the repair belongs in the register.

**`QA_003`, the one that changes Q2's status.** `UNI_012` read the
register's own literature note, found four mechanisms named in prose, and
recorded that two were not on the list. `undeclared frames` has a whole
folder. **`affect routing` has neither** — no entry, no mechanism.

Its shape there and Q2's here are the same statement twice:

> *a channel reclassified at intake, so the reading never reaches a guard
> at all* — `UNI_012`
>
> *the label is applied prior to content, so the content never reaches
> evaluation* — Q2

And both add the same second clause: the classification cannot be argued
with from inside, because objecting to it reads as confirming it.

**The marker names `UNI_012`'s own case without connecting it.** Q2's
second case is the driver-diagnostic-typed-as-complaint case that
`UNI_012` was written from. Q2's *first* case is from a different field —
which is exactly what `UNI_002`'s standing cross-field check has been open
for.

So Q2's status line is not *candidate ninth*. It is **the twelfth ordinal,
for a mechanism the register recorded as missing three drops ago, arriving
with its second case, its second field, and a better name** — `affect
routing` describes one of its two cases and `unaskable` describes both.

## The measurement findings

**`QA_004`: A1 cannot answer the question the marker's own Open section
poses.** A1 is *"two booleans. Cheap."* Its second boolean is the outcome
of a search, and three states need encoding:

| state | A1 returns |
|---|---|
| comparison found | `(True, True)` |
| absent in a stated corpus under stated terms | `(True, False)` |
| not searched | `(True, False)` |

The two that collide are exactly the two the Open section says must be
separated. Arithmetic, not judgement.

The repair does specific work here rather than being tidy. *"Absent in a
stated corpus under stated terms"* is a measurement because the null is
**bounded**; *"I did not find it"* is not one; *"not searched"* is
neither. Bounding the null is the criterion the Open section is asking
for, and it is one field.

**`QA_005`: A4 is built, unrun, and one input short.** The computation is
here — corrected share per year, with a half-life that returns `None` for
a curve that never crosses rather than a large number, because
never-crossing is the Q3 case and needs to be a distinct value. **No
citation counts are supplied**; the egress gate refuses the databases and
inventing them would be worse than not running it.

The marker is right that a single ratio is not enough. What it does not
say is that the series is **still uninterpretable alone**: two constructed
corrections with the same corrected-share at year 10 have half-lives of
11.4 years and never. Whether a curve counts as *"did not displace"* needs
a reference class of corrections that did — `criterion-symmetry`'s missing
comparison table on a second substrate.

## A finding about my own instrument

**`QA_007`: mention is not existence.** Cross-links, two columns:

| link | mentions | artifact |
|---|---|---|
| `uninstrumented` | 80 | yes |
| `criterion-symmetry` | 4 | yes |
| `report-typing` | 3 | **NO** |
| `rubric-backcasting` | 3 | **NO** |
| `merit-anchoring` | 3 | **NO** |

`report-typing` acquired all three mentions the moment the **previous**
marker listed it in its own cross-links. The mention-count checker I wrote
two drops ago would now report it as resolving.

That is `UNI_010`'s self-reference loop reaching this audit **through a
sibling folder** rather than through its own output — so the `EXCLUDE`-list
repair from that drop does not catch it. The fix is a second column, not a
wider exclusion: ask whether the artifact exists, not whether the token
appears.

Artifacts present are 2 of 5, up from 1 of 4 on the previous marker,
because the last drop landed `criterion-symmetry`. The set converges as
drops arrive; the same three are still missing and both markers say they
are the comparison set the shape needs.

## Runnability, and what to do next

| | state |
|---|---|
| A1 | **broken**, by the marker's own Open section |
| A2 | blocked — needs a venue-typed corpus |
| A3 | blocked — needs `report-typing`, absent |
| A4 | **built**, data blocked by the egress gate |

A4 genuinely is runnable by someone with a citation database.
`notes/study_watch.py` runs on a runner that reaches Crossref, OpenAlex
and arXiv, which is why it exists — A4 is the second item in this drop
family the watcher was built for, after `shape-spec-audit` `MS_004`.

A1 is the one that is broken rather than blocked, and it is the cheapest
thing here to repair.

## Where it sits

`uninstrumented/` is the parent and `QA_003` is the connection that
matters. `criterion-symmetry/` is the sibling and its unpopulated
comparison table is `QA_005`'s missing reference class in another
substrate. `null-harness/` supplies the reading of A1: an instrument whose
negative branch cannot be distinguished from its unrun branch has not
returned a negative.

Q3's case is a literature claim carried and unchecked — same status as
`MS_004`. Nothing above rests on it, and no citation figure is stated.

CC0. Stdlib only. Parses under Python 3.9.
