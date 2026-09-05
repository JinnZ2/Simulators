# RESULT — repair adjacency, and the grain question

Attaches to: ADDENDUM 01 §2, RESULT_taxonomy_crossmodel.md
Input: same 19 stripped records
Runs now compared: Kimi (sort), Perplexity (sort), DeepSeek (repair)
Date: 2026-09-05

---

## 1. THE GRAPH

DeepSeek's R3 adjacency, computed. Fully symmetric — zero asymmetric
edges, though asymmetry was explicitly permitted.

```
9 connected components over 19 records / 13 distinct transforms

C1  T01 T07 T13              pass the matching reference of two
                             co-present references
C2  T02 T09 T10 T12 T17      measure wall clock, drop the computed
                             proxy
C3  T03 T18                  normalize by the claim's own magnitude
C4  T04                      apply the 1/2 factor
C5  T05 T16                  p = 1 - exp(-rate*dt)
C6  T06                      compare component-wise, not aggregate
C7  T08 T14                  supply scale as an explicit parameter
C8  T11                      adjust for covariates
C9  T15 T19                  compare against a baseline, not raw
```

Against the decision rule written into the work order: the count
landed **near neither** prior grouping — not 4, not 11, but 9.
Under that rule this reads as "both prior groupings wrong, the count
is the finding." That reading is wrong, and the reason is better than
the rule.

---

## 2. THE ACTUAL FINDING — A STRICT HIERARCHY

The three groupings do not conflict. They nest, in one order:

```
Kimi  4 kinds + straggler
  |
  +-- DeepSeek repair graph   9 components
        |
        +-- Perplexity        11 groups
```

Every DeepSeek component is contained in one Kimi kind.
Every Perplexity group is contained in one DeepSeek component.
Seven of the nine components are IDENTICAL to a Perplexity group.

Perplexity differs from the repair graph in exactly two places, both
splits:

```
C1  T01 T07 | T13        Perplexity separated the straggler
C9  T15     | T19        Perplexity separated null-baseline from
                          adaptive-baseline
```

Nothing else. Three systems, three grains, zero cross-cutting.

**So grain was never a disagreement. It is a cut height on a tree
that all three independently found.** The records carry nested
structure; each sorter reported a different level of it.

---

## 3. WHAT THIS DOES TO EACH KIND

```
K1  conversion exists       SPLITS INTO FOUR (C1 C3 C4 C5).
                            Four members, four different repair
                            operations. K1 still predicts something
                            real — that re-measurement is NOT needed
                            — but it does not predict WHICH move.
                            Survives as a level, not as an operation.

K3  no conversion in        SPLITS 3 + 1. The speedup core holds as
    principle               one component. NLS-3 (scale-from-
                            correlation) leaves it.
                            *** Both external systems removed NLS-3
                            from this cluster independently.
                            Kimi's assignment of NLS-3 to K3 is a
                            correction candidate. ***

K2  boundary difference     one member, one component. Consistent.

K5  reference-class         SPLITS 2 + 1. T15/T19 (null baseline,
    re-baseline             adaptive baseline) stay together;
                            T11 (covariate adjustment) separates.
                            CONTESTABLE: adjusting for covariates is
                            arguably also a change of comparison set.
                            DeepSeek said NONE for T11 without
                            argument. Worth one more look.

K4  frame-relative          DEAD as a repair class. Its three Run-1
    referent                blind members land in three different
                            components (C1, C6, C7). Second
                            independent failure to replicate.
```

---

## 4. THE STRAGGLER GOT PLACED

F-TETRA-SCOPE (T13) was unassignable to Kimi and unnamed to
Perplexity. DeepSeek placed it, in C1, with the two-reference-
temperature record.

```
TMP-2   two reference temperatures co-present in one module;
        the wrong one is passed into the correction
T13     two frames both yield SHAPE.TETRA; refutation is defined by
        component count, which differs between them

shared repair: identify which of two co-present referents governs,
               and pass that one
```

This is the first cross-cutting event in the whole exercise — it
joins a K1 member to a record Kimi left outside every kind.

It also puts pressure on Perplexity's NO NAME FOUND. Perplexity
searched for a name for "frame-dependent refutation test." If
DeepSeek is right, the searchable object is reference disambiguation
with two co-present referents, which is named in several fields.

```
TEST, cheap and decisive:
  does T13 reduce to TMP-2's shape? i.e. can it be restated as
  "two referents present, the governing one not declared"?
  if YES  -> the candidate gap CLOSES and the record is C1
  if NO   -> name what T13 has that TMP-2 does not, and the gap
             stands with a sharper statement than before
```

Do not close it on DeepSeek's grouping alone. One system, one
placement, no argument given for it.

---

## 5. THE RECURRING EXTERNAL ERROR — THIRD INSTANCE

```
Kimi          kept docs/F1, ENG-1, ENG-3 as three distinct
              transforms
Perplexity    merged F1 into ENG-1/ENG-3
DeepSeek      declared ALL TEN pairs among the five speedup records
              mutual restatements
```

They are not. Different code paths, different measured numbers, and
ENG-3 is a SIGN INVERSION (reports 1.50x more speedup while taking
1.89x more wall clock) while the others are magnitude errors.

Three systems, three collapses, increasing severity, all driven by
similar wording. Kimi is right and is the only one that read the
transforms rather than the prose around them.

Note this does NOT affect the component structure: the five collapse
into one component either way. It affects the distinct count, and
it would affect any claim about how often this mismatch occurs.

---

## 6. STANDING ANSWER, UPDATED

```
one or several?      SEVERAL. Four sorts, none returned one.

how many?            depends on the cut height, and the tree is
                     now known:
                       4-5   repair CLASS (is a conversion
                             available at all)
                       9     repair OPERATION (which move)
                       11    operation + referent (which move,
                             on which referent)

which to report?     both endpoints, with the nesting stated.
                     A single number is a cut, and a cut with no
                     stated height is the thing the instrument
                     exists to catch.

what is fixed?       membership at every level. Nothing
                     cross-cuts.
```

## 7. WHAT WAS NOT TESTED

```
- asymmetric adjacency was permitted and never used. Either the
  relation really is symmetric here, or the permission went unused.
  Not separable from this run.
- CANNOT FALSIFY was permitted and never used. All 19 repairs got a
  falsifier. Spot-check a sample against the source records before
  treating that as a clean sweep.
- the tree is built from ONE repair reading. A second repair pass by
  another system would test whether the 9 is stable or is DeepSeek's
  grain the way 4 was Kimi's.
```
