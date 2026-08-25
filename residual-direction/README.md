# residual-direction

Reads a miss history and names the folded term.

Companion to the **fold detector** (`sheet-structure-scan/`), which finds
unbound numbers, and the **claim record** (`claim-record/`), which
defines a bound one.

Order in [`WORK_ORDER.md`](WORK_ORDER.md), verbatim. Findings in
[`CLAIM_TABLE.md`](CLAIM_TABLE.md).

```
python3 residual.py demo                              the four fixtures
python3 residual.py run S.json --claim UNF_GRID_IRAQ  coupling from the record
python3 naming.py --source .                          S6, over the folder
python3 residual.py --selftest
```

## The counterexample the whole design is for

A pooled sign test scores F1 as unbiased. It is not.

```
row     against              slope    se        standardized  lean
S2a     predicted magnitude  0.12     0.006317  0.8681        lean
S2b     unrelated            -0.8584  0.5204    -0.1501       .
S2c     time index           0.09999  0.005264  0.8681        lean
pooled  sign only            -        0.04564   -             .

pooled sign fraction positive: 0.5083  (one row, not the verdict)
```

Overprediction at low magnitude and underprediction at high magnitude
sum to symmetric. The sign test sees nothing; the conditional slope sees
it at 0.868.

## Three things the fixtures forced

**The ranking has to be on the standardized slope.** Raw slopes against
predictors with different units are not on one scale, and sorting them
would be a comparison across unlike objects — `G-DIM`, in the one place
a ranked list makes it easy to miss. Raw slopes are shown and not sorted
on.

**F1 cannot separate magnitude from time, and says so.** In F1 the
predicted values rise with the time index, which is the common real
shape — so the two axes carry *identical* standardized slopes and a
ranked list cannot say which the residual leans with. The order asks for
the term to be **named** rather than inferred, and naming one of a
collinear pair is picking. The report emits `NOT SEPARABLE` with the
group.

**A missing coupling is a fifth state, not "weak".** The 2x2 has four
cells; a coupling nobody supplied is none of them, and treating it as
weak would route a case to `LOG AND LEAVE` on an absence.

## S6, enforced and able to scan itself

The banned phrase is never written in this source: the patterns are
composed from tokens, so `naming.py --source .` scans its own directory
**including itself**, with no skipped region and no hand-broken loop.

One file is exempt and it is measured rather than assumed: the delivered
order has to name the phrase in order to ban it. The selftest checks
both that the tool is clean with the specification excluded *and* that
the specification is the **only** file that fires without the exclusion.

## Where S5 and S6 disagree

S5 names field 8's values `raw | corrected | unknown`. S6 replaces the
state vocabulary with `adjusted / unadjusted`. S6 governs — it is the
naming constraint — and both S5 spellings load as aliases, so a series
written to the letter of S5 still validates.

## The chain

```
coupling          0.8815  (claim record UNF_GRID_IRAQ, clock.coupling,
                           basis: measured by perturbation, +0.1% on the cell)
```

S3 says the coupling comes from the claim record. It is **imported**,
not reimplemented, so the number the discriminator responds to is the
same object the clock derives its shelf life from — and that number was
measured by perturbing a cell in a real workbook.

49 selftest checks across two modules.

CC0. Stdlib only. Parses under Python 3.9.
