# RESULT — cross-model replication of the SCOPE-DIFFERENT taxonomy

Attaches to: ADDENDUM 01 §2 (the taxonomy test)
Runs compared: Kimi Run 2 (gm + g2b, 19 cells / 13 distinct)
               Perplexity blind sort (same 19 cells, stripped)
Date: 2026-09-05

The test existed because Runs 1 and 2 shared a system, so their
agreement could not distinguish "converged" from "remembered."
Perplexity had no exposure to the K-list and no access to the repos.

---

## 1. HEADLINE — THE TWO TAXONOMIES ARE STRICTLY NESTED

Every Perplexity group is a subset of exactly one Kimi kind.
Zero cross-cutting. No record was grouped by one sorter with a record
the other sorter placed in a different kind.

```
Kimi kind                        distinct  Perplexity groups covering it
---------------------------------------------------------------------
K1  conversion exists                 4     G1 reference temperature
    (unit/convention difference)             G3 absolute vs relative rate
                                             G4 CV2 vs half-CV2
                                             G5 rate as Bernoulli p

K3  no conversion in principle        4     G2 proxy vs wall clock
    (homonym)                                G7 scale inferred from result

K2  boundary difference               1     G6 whole-storm vs component

K5  reference-class re-baseline       3     G8  raw vs covariate-adjusted
                                             G10 flag rate vs null stream
                                             G11 uniform vs adaptive baseline

unassigned straggler                  1     G9 frame-relative refutation
                                             -> Perplexity: NO NAME FOUND
```

This is a stronger outcome than agreement. A conflict would have
shown up as two records grouped together by one sorter and split by
the other. There are none. The disagreement is entirely about GRAIN.

---

## 2. WHAT REPLICATED, AND WHAT DID NOT

```
MEMBERSHIP        replicated. An independent sorter with no K-list
                  put the same records together.

ABSTRACTION LEVEL did not replicate. Kimi: 4 kinds over 13 distinct.
                  Perplexity: 11 groups over 13 distinct, six of them
                  singletons. That is close to an identity map — a
                  re-listing, not a sort.

K3 boundary       replicated with identical membership on its core
                  (the proxy/wall-clock cluster). Kimi called this
                  the sharpest discriminator; Perplexity independently
                  gave it the largest group. Strongest single result.

K5               membership replicated exactly, as three separate
                  groups. Perplexity did not see the shared structure
                  (wrong null/baseline/adjustment set) but found all
                  three members. Kind CONFIRMED at the record level,
                  NOT confirmed as a kind.

K4               zero members again. Two independent sorters, no K4
                  on this transform set. K4 remains Run-1-only and
                  single-folder concentrated; treat as a candidate
                  artifact of that repo or that sorter until it
                  appears somewhere else.

straggler        both sorters flagged the same record as anomalous,
                  on different criteria: unassignable to a kind
                  (Kimi) and unnamed in any literature (Perplexity).
                  Independent convergence on the odd one out.
```

### So the contamination question is answered, and it splits

```
came from the records   which records belong together
came from the sorter    how coarse the kinds are
```

Kimi's abstraction was not read back off a menu — the membership
survives a sorter that never saw the menu. But the grain is the
sorter's, and nothing in the records fixes it.

---

## 3. THE GRAIN QUESTION IS NOT A TIE

Kimi sorted by REPAIR TYPE — what fixes the mismatch (re-baseline,
re-measure, rescale, disambiguate). Perplexity sorted by SUBJECT
MATTER — temperature, energy, rates, benchmarks, epidemiology.

Criterion that separates them, stated so it can be argued with:

```
a kind earns its place if MEMBERSHIP PREDICTS SOMETHING NOT ALREADY
IN THE RECORD.
```

Under that test:
- K1 predicts that a closed-form conversion exists and will work.
  Perplexity's G1/G3/G4/G5 each predict only what their own record
  already states.
- K5 predicts that re-measurement will NOT help and a different
  comparison set is required. G8/G10/G11 predict nothing jointly,
  because they were never joined.
- G9 / F-TETRA-SCOPE predicts nothing under either, which is
  consistent with it being genuinely unsorted rather than
  mis-sorted.

Kimi's grain carries information. Perplexity's does not. That is a
judgement and it is open to attack — the counter-case would be a
record where Kimi's merge hides a repair that works for one member
and fails for another.

---

## 4. PERPLEXITY'S SORTING SIGNATURE — ERRORS IN BOTH DIRECTIONS

It sorted on surface features of the record text, which shows up
twice with opposite signs:

```
OVER-SPLIT   different subject matter, same repair
             -> K1 became four groups, K5 became three

OVER-MERGED  similar wording, different transform
             -> merged T09 (PerformanceTracker averageSpeedup,
                measured 0.48x/0.26x/0.31x against a uniform grid)
                into T10/T12 (geometric_speedup, adaptive path
                2x-50x slower).
                Different code paths, different measurements.
                Kimi kept them distinct and is right.
             -> collapse count 12 vs Kimi's 13. The one-record
                difference is this merge.
```

Both are the same behaviour. Not a reason to discard the run — the
membership result survives it, because surface features and repair
type correlate on this set. It is a reason not to use Perplexity's
grain.

---

## 5. TASK 2 — LITERATURE PASS, AUDITED

Useful, with one recurring defect.

```
DEFECT     source-class tags reappeared: [nih], [cancer], [arxiv],
           [matexcel +1]. The work order declared these missing
           citations in advance. They came back anyway.
           Where a real identifier IS given alongside, use that and
           discard the tag.

USABLE     arXiv:2101.00905 (baselines for feature attribution)
           arXiv:1911.12185 (confounding, DiD adjustment)
           PMC6107969 (correlation coefficients)
           ISBN 978-0073523262 (Law & Kelton)
           ISBN 978-1119254645 (Montgomery, SQC)

CHECK      "ISO 14044:2020" — the standard is 2006 with later
           amendments. Verify the designation before citing.

OVERCLAIM  G2 marked EXACT with "nothing does not carry over."
           The proxy-benchmark literature treats proxies as NOISY.
           It does not cover the ENG-3 case, where the proxy moves
           OPPOSITE in sign — reports 1.50x more speedup while
           taking 1.89x more wall clock. Anti-correlation is not
           in the cited sources. Downgrade to PARTIAL, and the
           uncovered remainder is the interesting part.

WEAK SRC   a blog post cited as the source for an EXACT match.
           Fine as a pointer, not as the citation.
```

### The one that matters

```
G9 / F-TETRA-SCOPE   NO NAME FOUND.
  Searched: frame-dependent refutation test measurement;
  component count refutation measurement;
  representation-dependent invariants measurement theory.

  Two frames agree on a shape invariant (TETRA) but define
  refutation by different component counts (!=4 vs !=3), so the
  same data refutes in one frame and satisfies the invariant in
  the other.

  Status: candidate genuine gap. It is the record neither sorter
  could place and no field could name. That co-occurrence is
  itself the reason to look harder, not a reason to close it.
  Next step is a second independent name-search, not a decision.
```

---

## 6. STANDING ANSWER ON THE OPEN QUESTION

```
Is SCOPE-DIFFERENT one thing or several?   SEVERAL.
  Three independent sorts, none returned one group.

How many?                                  UNSETTLED.
  4 (Kimi) vs 11 (Perplexity), nested, N=13 distinct.
  The count is a function of grain and the grain is not yet
  fixed by anything in the records.

What is fixed?                             MEMBERSHIP.
  Which records belong together replicated across a sorter with
  no shared memory.
```

Do not report a kind count as a finding until a grain criterion is
argued and adopted. Report membership.
