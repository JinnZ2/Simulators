# category-weld

CC0. stdlib only. Phone-buildable.

Ninth exclusion mechanism for `uninstrumented`, plus a scorer.

A CATEGORY WELD is a term that fuses two or more independent quantities
into one handle. The components can move to opposite extremes without the
record moving at all, because the language admits one value where the
world has several.

This is a marker for a sensed shape that needs more exploration. It is not
a thesis and not a position under defense. Test whether it fits, extend it
into a domain it does not cover, or report where it breaks. A break goes
in `CLAIM_TABLE.md` as a measurement.

## Files

    MECHANISM_09.md   the mechanism, in uninstrumented case format
    weld.py           scorer
    test_weld.py      synthetic fixtures for the arithmetic
    CLAIM_TABLE.md    falsifiable claims
    welds/*.json      one file per term

## Use

    python3 weld.py                  # readouts for every term
    python3 weld.py --term capital   # components and cases for one term
    python3 weld.py --jsonl          # one score object per line
    python3 weld.py --new employed    > welds/employed.json
    python3 test_weld.py             # verify the arithmetic

## The three readouts

    n_cases      how many divergence cases can be named
    max_spread   largest ratio between component relative-changes in one case
    bias         how consistently the divergence runs one direction, 0..1

Three numbers rather than one, because case count alone cannot separate a
term whose components diverge rarely and enormously from one whose
components wobble constantly by small amounts, and cannot separate
imprecision (bias near 0) from a term that systematically hides one
component behind another (bias near 1).

Intent is not an input anywhere in the scorer. A term with high bias
behaves the same way regardless of who uses it or why. Dropping intent is
what makes the thing testable on the data alone — and it means
decomposing the category works without anyone's cooperation.

## Adding a term

1. Name the components you think are welded, with units.
2. Set `tracked_by_label` to the component the term is read off in
   practice. That is the one the others hide behind.
3. Name divergence cases: instances where the components moved
   independently in the field.
4. Attach paired `before`/`after` readings with a source where you have
   them. Leave them null where you do not — an unquantified case counts
   toward `n_cases` and is reported separately. A gap is marked, not
   filled.

## Seeds

`rural` — density welded to ownership distribution, functional diversity,
self-supporting capacity.

`capital` — legal title welded to decision authority, risk bearing,
revenue claim, input supply.

Both currently sit at four named cases, zero quantified.
