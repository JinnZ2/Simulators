<!--
SPDX-License-Identifier: CC0-1.0
-->

# SCALING_CLASSES — delivered, verbatim

Fourth audit of this folder from outside it, and the follow-on to
[`EARTH_TRANSITIONS.md`](EARTH_TRANSITIONS.md). Landed unmodified; the
response is in [`scaling_classes.py`](scaling_classes.py) and `SHB_031..036`
in [`CLAIM_TABLE.md`](CLAIM_TABLE.md).

```
ITEMIZED — where each class lands vs 1e120
  turbulence, one ocean, 1e8 yr        1e45   fits
  all Earth fluid dynamics, 4.5e9 yr   1e100  fits
  N-body accretion, 1e30 bodies        1e67   fits
  quantum many-body, N=100             1e30   fits
  quantum many-body, N=300             1e90   fits
  quantum many-body, N=1000            1e301  EXCEEDS 1e181
  ONE protein, exhaustive fold search  1e143  EXCEEDS 1e23
  nested phase transitions, 4 classes  1e152  EXCEEDS 1e32


the structural result
  everything polynomial FITS, with room:
    fluids, gravitation, continuum mechanics
  everything EXPONENTIAL blows the ceiling:
    quantum many-body (d^N)
    conformation search (3^n)
    critical phenomena (no scale to truncate at)
  => the cut is not size. it is SCALING CLASS.
```

> And the sharpest single line: one 300-residue protein, searched
> exhaustively, exceeds the universe's entire compute budget by twenty-three
> orders of magnitude. A cell folds thousands per second.
>
> So the physics isn't doing the search. That's Levinthal's paradox — and its
> resolution is that folding is funnelled, not searched. Which is the general
> answer: nature never pays the exponential. It's in a configuration where the
> exponential doesn't arise.
