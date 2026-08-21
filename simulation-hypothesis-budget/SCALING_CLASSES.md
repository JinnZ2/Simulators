<!--
SPDX-License-Identifier: CC0-1.0
-->

# SCALING_CLASSES

*Opening replaced as delivered. The table and the audit pointers below are
unchanged; the response is in [`scaling_classes.py`](scaling_classes.py) and
`SHB_031..040` in [`CLAIM_TABLE.md`](CLAIM_TABLE.md), amended per the
delivered H1/H2/H3 corrections.*

---

**What this document is.** A price list, and one cut through it.

The ceiling is fixed: roughly ten to the one-twenty operations available to
the observable universe since the big bang, at Lloyd's 1999 bound. Every row
below prices one class of physical process against it.

**The cut:** everything that scales polynomially fits, with room. Everything
that scales exponentially exceeds the ceiling, and exceeds it by margins no
efficiency recovers. Four crossover points locate the boundary exactly. Two to
the N crosses at 399 components. Three to the n crosses at 252 residues. N
squared crosses at ten to the sixty bodies. N cubed at ten to the forty. Earth
has ten to the fifty atoms, which is why N squared fits and N cubed does not at
the same N — the exponent decides, not the size.

**The finding, stated once.** The exponential is a property of the
representation, not of the system. Check which one you are pricing.

Every row that exceeded the ceiling turned out to price a method rather than a
process. Exhaustive conformation search exceeds by twenty-three orders of
magnitude, and no protein performs it — folding is funnelled, so the search
does not occur. Exponential state-space cost binds a classical simulator
carrying volume-law entanglement, and does not bind area-law states, which are
polynomially representable in tensor-network form and cover most ground-state
chemistry and condensed matter. In both cases the cost was removed by changing
the representation, with the physics untouched.

So the reading is not that these processes are expensive. It is that our
coordinates carry variables the system does not.

**How to use it.** An exponential appearing in a formalism is a report about
the formalism. It says: variables are being stored that the process is not
using. Treat it as a provenance question — is this exponent in the physics, or
in the method — before treating it as a difficulty. Where the answer is
method, the exponent is removable and the removal does not require new physics,
only different coordinates.

**What this does not claim.** It does not claim the mathematics is wrong; every
procedure priced here is correct. It does not claim exponentials are always
artifacts — where the physical state is genuinely volume-law entangled, the
cost is real and a classical substrate is genuinely bounded. Entanglement
scaling is the discriminator, and it is measurable rather than assumed. It does
not settle whether the universe is simulated. It bounds what a substrate would
have to be.

**Status.** Marker under exploration. Crossover arithmetic is reproducible from
the printed terms; four rows verified, one row's transfer label truncated, one
row's event count drifted between drops and is unresolved. Nothing here is a
position under defense.

---

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
