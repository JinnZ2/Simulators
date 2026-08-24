# check_d2 — four readings

Produced by `check_d2.py`, pinned in `samples/check_d2.sample.txt`. The
entry is unmodified. Nothing here is a verdict on it.

## 1. Five of seven instances resolve in this tree

```
VERIFIED 5   AMBIGUOUS 1   NOT_IN_TREE 1
```

Resolution is a file plus a literal marker inside it, checked at run time,
not asserted here.

- **AMBIGUOUS** — *published instrument diverging from its own documented
  appendix* has three live candidates: `reasoning-gate` staging `G-FIT`
  `post` in `guards.json` while `gate.py` enforces it in `pre()`;
  `aperiodic-order-sim-stack` shipping sandbox figures the report never
  mentions; `criteria-drift` `CD_007`, "significant" twice in the README and
  zero times in `regress.py`. Not picked. The instance is under-specified for
  this tree, which is a property of the instance line, not of the tree.
- **NOT_IN_TREE** — *studies varying a CUE and reporting on the CONDITION*.
  Not in this repo, literature claim not checked. Carried at the status
  `UNI_166` already records for it.

## 2. The two representations are five different kinds of pair

The entry requires two representations and does not say what kind of pair
they may be. Across six readable instances:

| pair kind | n |
|---|---|
| artifact vs artifact | 2 |
| schema vs the data it admits | 1 |
| stated rule vs measured behaviour | 1 |
| output vs a known answer | 1 |
| declared value set vs reachable states | 1 |

Wide applicability and an undeclared parameter are the same fact here. Two
runs of D2 can compare very different things without the difference being
visible in either run.

## 3. The signature holds on one instance and fails on four

*"The instrument reverts to the channel it was built to avoid."*

```
HOLDS 1   ARGUABLE 1   FAILS 4
```

It holds cleanly on the predicate detector deciding 10 of 12 by word list —
where the avoided channel is named in the module docstring and is the one
returned to. It is arguable on the 0.83 metric, where no avoided channel was
declared in advance so the fit is read backwards.

It fails on four, and **two of those four fail together**: *schema accepting
anything* and *null test unable to emit two of its own terminal values* are
the cannot-refuse and cannot-emit directions of `UNI_166`, a declared state
with no path to it. Nothing reverts in either; a branch is unreachable. The
remaining two are plain drift between artifacts.

So the entry bundles at least three operations: divergence between two
representations (the stated operation), reversion to an avoided channel (the
stated signature, true of one instance), and an unreachable declared state
(`UNI_166`). The signature generalizes from the strongest instance rather
than across them.

## 4. The standing check's stated derivation is one short

*"STANDING CHECK derived from two of the above."* One source — the metric
returning 0.83 — is in the list. The other is `null-harness`'s `_verdict`
returning `OK` for a gate at `TP=0.5` and one at `TP=1.0` alike, and that is
**not among the seven instances**. The check itself is right and is built
(`tools/known_answer.py`); its stated provenance names a list that holds one
of its two sources.

## What this checker did to its own reading

Two of the paths recorded in `check_d2.py` were wrong when first written: a
marker containing `{"type": "array"}` where the file has `{"type":"array"}`,
and `CD_007` filed under `AUDIT_NOTES.md` where it lives in
`CLAIM_TABLE.md`. Both were caught by running the check rather than by
reading it — which is D2's own operation applied to the reading of D2.
