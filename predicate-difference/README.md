# predicate-difference

**Marker under exploration.** Delivered method:
[`SPEC_METHOD.md`](SPEC_METHOD.md), landed verbatim. Findings:
[`FINDINGS.md`](FINDINGS.md).

**Status: instrument built and graded. No corpus acquired. No marker over
any real class is reported.**

The method is now specified enough to build against, which it was not
before. What follows is the harness, its grade, and the reproduction
commands. The findings row is empty and that is the size of the work done,
not a result.

---

## Reproduction

```
python3 predicate_diff.py --selftest     # 27 checks
python3 shape_index.py   --selftest      # 23 checks
python3 predicate_diff.py                # the graded instrument
python3 shape_index.py                   # the index, empty
```

---

## What the support rule buys

The set difference is trivial; the clause *"at a rate the corpus size can
support"* is the whole instrument. Two fixtures carrying the **same real
difference**:

| fixture | reference tokens | markers | NOT_ENOUGH_TEXT |
| --- | --- | --- | --- |
| signal | 20 000 | **3** | 0 |
| thin | 300 | **0** | 2 |

A plain set subtraction reports the same three markers for both, and returns
the subject class's entire vocabulary whenever the reference sample is thin
— which for these subject classes in these sources is the expected
condition, not an edge case.

Absence is assertable only when the predicate **would have been expected**
in the reference class at the subject class's own rate. `NOT_ENOUGH_TEXT` is
a distinct state from absence and is never folded into it.

```
MIN_EXPECTED = 3.0     # expected occurrences before an absence is a reading
MIN_OBSERVED = 5       # before a rate is established at all
```

Both are chosen floors, printed beside every readout. The result moves with
them and nothing here establishes which is right.

## Valence

Not switched off — **absent**. There is no valence field, no valence
argument, no valence attribute. `check_no_valence()` walks the module's own
AST over identifiers (not strings, so the word can appear in prose
explaining its absence) and fails the selftest if a channel appears.

Limit, disclosed: this prevents a valence *field*. A predicate taxonomy
whose category names carry the judgement passes untouched — and a contempt
taxonomy is exactly where that is tempting.

## The recurrence test

| fixture | bindings | vocabulary | verdict |
| --- | --- | --- | --- |
| FX_1 | 4 of 4 | disjoint | `STRUCTURAL_SIGNATURE` |
| FX_2 | 4 of 4 | one shared word | `SHARED_VOCABULARY` |
| FX_3 | 2 of 4 | disjoint | `NOT_ESTABLISHED` |
| FX_4 | 2 of 4 | 2 classes never checked | `NOT_ESTABLISHED` |

**FX_1 and FX_2 are both present in all four classes.** They differ only in
whether one word is common across bindings. A test that counts bindings
returns four-of-four for both — and shared vocabulary is consistent with the
four literatures being *one* literature, which is the hypothesis the
extension exists to rule out. So full presence with shared vocabulary is
weaker than partial presence with disjoint vocabulary, and the verdict says
so.

`FX_4` holds the case where a class was never checked: unchecked is reported
separately from absent, and never counted as absence.

## Corpus

| target | state |
| --- | --- |
| Freud | NOT_ACQUIRED |
| period psychology and medicine | NOT_ACQUIRED |
| household management texts | NOT_ACQUIRED |
| labor economics of the era | NOT_ACQUIRED |

Acquired: **0 of 4.** Naming a source is not holding it. Every readout over
real classes returns `NOT_RUN`, and the shape index contains zero shapes.

Naming the shapes from here would be easy — the categories a contempt
taxonomy would use are guessable — and it would be this module writing the
finding and then confirming it against its own fixtures.

## Task 1 (seed sets) — done

[`TASK1_SEEDS.md`](TASK1_SEEDS.md). Seed file landed verbatim at
[`seeds/dimension-words.txt`](seeds/dimension-words.txt), md5
`de5cdbb44650e9b88c015737b1170ce2`, from
`github.com/wenhaojiangsoc/devaluation @ c22a643`. All four requested sets
present. The `moral` dimension referenced in `embeddings.py` has **no seed
lists in the package** — the paper's "moral standing" is the `evaluation`
axis (good/bad, Osgood E). Task 2 is blocked: the embeddings live on
Dropbox, which the egress policy refuses, and the HistWords fallback host is
refused too.

## Two things needing your decision

1. **The shape-index format is inferred.** No such format exists in this
   repo. It is built from `scope-bound-shapes/`, where a shape is defined by
   its structure and not its materials — which fits
   same-shape-different-vocabulary closely. If the delivered format differs,
   the file shape is wrong and the contents transfer.
2. **No reference class is settled.** The predicate difference needs one per
   comparison, and the four subject classes as delivered are not defined
   against a stated reference. They also overlap — a disabled woman is in
   two.

CC0. Stdlib only. Parses under Python 3.9.
