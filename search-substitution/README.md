# SEARCH SUBSTITUTION

Marker under exploration. Not a position under defence.

Three organisms produce an answer without searching for it. None of them
enumerates candidates, and none of them pays an exponential. Each pays
something else instead, and the something else is different in all three
cases — which is the useful part, because it means the exponential was never
attached to the problem.

The finding, stated once: **the exponential is a property of the
representation, not of the system. Check which one you are pricing.**

CC0. Stdlib only.

```
python3 search_substitution.py            # full report
python3 search_substitution.py --sources  # where each figure came from
python3 search_substitution.py --selftest # 23/23
```

## THREE SUBSTITUTIONS

    physarum          occupies the whole space simultaneously, then retracts
                      where throughput is low. The surviving network is the
                      answer. Cost scales with the arena, not the candidates.

    corvid            stores the world in advance. On arrival the problem is
                      already solved. The cost sits in what had to be kept.

    ornithorhynchus   fuses an electrical and a pressure field and reads the
                      offset between their arrivals. The disagreement is the
                      range. Nothing intermediate is built.

They are not merged, because they substitute different resources — area held
over time, bits carried over an interval, and one multiplication at the
moment of use. A single "efficiency" story covering all three would be
describing the observer's surprise, not the biology.

## WHAT EACH ONE DOES NOT PAY

Tero 2010 ran Physarum over 36 food sources. The exact Steiner-tree dynamic
program carries a 3^k term: 3^36, about 1.5 x 10^17 subproblem splits. The
plasmodium's cost expression contains no k at all. It is arena, held for a
duration, and it does not move when terminals are added. That is the whole
observation — not that the organism searches faster, but that the term is
absent.

A corvid recovering 5,000 caches over 10,000 candidate sites would average
about 2.5 x 10^7 probes searching and 5 x 10^3 remembering. The factor of
5,000 is not a saving. It is a transfer: roughly 3 x 10^5 bits at 64 bits per
cache, carried continuously across the whole storage interval, and paid
whether or not any given cache is ever recovered.

A platypus at 100 mm reads an arrival offset of about 68 microseconds. Range
is one multiplication away. A map-then-locate approach over the same working
volume — a half-metre hemisphere at 1 mm — would carry about 2.6 x 10^8
cells. That is polynomial and affordable; the point is not that it is too
expensive but that it is an intermediate object with no use.

## WHERE THE CROSSOVERS SIT

The module reproduces the crossover arithmetic against a fixed ceiling of
10^120 operations (Lloyd 1999), so the biology above can be read against it:

    2^k   exceeds the ceiling at k = 399
    3^k   exceeds the ceiling at k = 252
    N^2   exceeds the ceiling at N = 10^60
    N^3   exceeds the ceiling at N = 10^40

Earth carries about 10^50 atoms, so N^2 fits and N^3 does not at the same N.
The exponent decides, not the size. None of the three organisms sits anywhere
near these lines, and that is the point: the lines belong to methods.

## THE CUT

Each of the three replaces a relation with something that is not a procedure.
The search was never in the problem — it entered when the problem was written
as a sequence of visits to candidates. Remove the sequence and the exponent
goes with it, without new physics and without a better algorithm.

This is a claim about pricing, not about capability. It does not say the
organisms are computing anything we cannot, and it does not say enumeration
is always avoidable. It says that when an exponential shows up, its
provenance is a question worth asking before its difficulty is.

## WHAT WOULD BREAK IT

Any one of the three turning out to enumerate after all — a hidden sequential
stage doing the work the substitution is credited with. For Physarum this
would be a demonstration that convergence time scales with terminal count
rather than arena size. See `CLAIM_TABLE.md` for the per-claim falsifiers and
`AUDIT_NOTES.md` for what is not established, which includes the platypus
range mechanism.

## SPECIES PRECISION

"Crow" is doing too much work in the informal version of this and the folder
does not repeat it. The tens-of-thousands-of-caches figure belongs to Clark's
nutcracker, *Nucifraga columbiana*. The what-where-when result belongs to the
western scrub-jay, *Aphelocoma californica*. Observer-conditioned re-caching
belongs to the common raven, *Corvus corax*. All three are corvids; only the
last is genus *Corvus*, and the three results were not obtained in one animal.
