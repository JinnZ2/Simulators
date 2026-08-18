# MECHANISM 09 — CATEGORY WELD

Ninth exclusion mechanism for `uninstrumented`. The first eight cover a
quantity that cannot be measured. This one covers a quantity that cannot
be *separated*: two or more independent quantities are welded into a
single category, so neither can vary on the record.

---

QUANTITY
: Each component quantity welded inside a single term, and the divergence
  between them.

EXCLUDED BY
: The category itself. Not the sensor, not the storage, not the budget
  boundary. The term admits one value where the world has several, so a
  component can move to any extreme without the record moving at all.

VISIBLE AS
: A term whose components are demonstrably independent in the field but
  have no separate handles in the language. Detected by naming divergence
  cases: instances where the components moved apart while the term stayed
  constant.

WOULD MEASURE
: Three readouts per term (see `weld.py`):
  - `n_cases` — how many divergence cases can be named
  - `max_spread` — largest ratio between component relative-changes in any
    one case
  - `bias` — how consistently the divergence runs in the same direction

CONFIDENCE
: Mechanism: high — the two seed terms each produce divergence cases on
  first attempt. Readouts: unvalidated, no term is quantified yet.

---

## Why the readouts are three numbers and not one

`n_cases` alone undercounts a term whose components diverge rarely but
enormously, and overcounts a term whose components wobble against each
other constantly by small amounts.

`bias` separates two different situations that produce identical case
counts:

- bias near 0 — divergence in random directions. The term is imprecise.
- bias near 1 — divergence always in the same direction. One component is
  systematically standing behind another. The term does directional work
  whether or not anyone arranged it that way.

Intent is not an input. A term with high `bias` behaves the same way
regardless of who is using it or why, which is what makes it testable at
all.

## Generation rule

Models are structurally prone to this one. A word's representation is a
summary of the contexts it occurs in, so when a corpus never separates the
components, nothing in training provides a gradient that would pull them
apart. The weld is not learned — it is the absence of anything that would
break it, and it reproduces identically across every corpus.

The same structure appears wherever a token is held without independent
access to its referent.

## Test

A term is welded if both hold:

1. At least one divergence case can be named — the components moved
   independently in the field.
2. The language provides no separate handle for the components that
   diverged.

Failing (1): the components may genuinely be one quantity.
Failing (2): the term is a summary, not a weld — the handles exist.
