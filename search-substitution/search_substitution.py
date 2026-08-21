#!/usr/bin/env python3
"""
SEARCH SUBSTITUTION
Three organisms that produce an answer without searching for it, priced
against the search they do not perform. Stdlib only. CC0.

The shape under test: an exponential in a solution method is a property of
the method, not of the problem. Each organism here pays a different substitute
cost -- occupancy, storage, or direct coupling -- and none of the three pays
an enumeration term. The exponential is what it costs to visit one candidate
at a time, and none of them visits candidates.

  physarum          occupies the entire space at once, then retracts where
                    throughput is low. The surviving network is the answer.
                    Cost scales with the arena, not with the candidate count.

  corvid            stores the world in advance. At recovery the problem is
                    already solved, so the cost sits in what had to be kept,
                    not in a search performed on arrival.

  ornithorhynchus   fuses an electrical and a pressure field and reads the
                    offset between their arrival times. The disagreement is
                    the range. No map is built and then queried.

WHAT THIS MODULE DOES NOT DO. It does not convert the three substitute costs
into a common unit with the search costs. They are not the same kind of
quantity -- one is an enumeration count, the others are area-seconds, stored
bits, and a single multiplication -- and inventing a shared unit to divide
them would manufacture a ratio the biology does not support. The module
reports the scaling of each side and the point where the search side exceeds
a stated ceiling. That is the comparison the evidence carries.
"""

import argparse
import math
import sys


# Lloyd 1999 (Phys Rev Lett 88:237901, "Ultimate physical limits to
# computation"): ~1e120 logical operations available to the observable
# universe since t=0. Used here only as a fixed ceiling to locate crossovers.
CEILING_LOG10 = 120.0

SOUND_SPEED_FRESHWATER = 1480.0  # m/s, ~20 C. Platypus forages in fresh water.


def crossover_exponential(base, ceiling_log10=CEILING_LOG10):
    """Smallest integer k with base**k > 10**ceiling_log10.

    Reproduces the crossover figures: base 2 -> 399, base 3 -> 252.
    """

    if base <= 1:
        raise ValueError("base must exceed 1")
    exact = ceiling_log10 / math.log10(base)
    k = int(math.floor(exact)) + 1
    return k


def crossover_polynomial(exponent, ceiling_log10=CEILING_LOG10):
    """Log10 of the N at which N**exponent exceeds the ceiling.

    Reproduces: exponent 2 -> 60, exponent 3 -> 40.
    """

    if exponent <= 0:
        raise ValueError("exponent must be positive")
    return ceiling_log10 / float(exponent)


# ---------------------------------------------------------------- physarum

def steiner_dp_terms(terminals):
    """Subproblem count in the Dreyfus-Wagner exact Steiner-tree DP.

    Dreyfus & Wagner 1971, Networks 1:195. The 3**k term dominates: it is the
    number of ways to split a terminal subset across a branch. This is the
    enumeration Physarum does not perform.
    """

    if terminals < 0:
        raise ValueError("terminals must not be negative")
    return 3 ** terminals


def physarum_occupancy(arena_cm2, hours):
    """Area-seconds the plasmodium must hold to run the whole space at once.

    There is no terminal count in this expression, and that is the finding.
    The organism's cost is set by the arena it occupies and how long it takes
    to prune, not by how many candidate networks exist inside it.
    """

    if arena_cm2 <= 0 or hours <= 0:
        raise ValueError("arena and duration must be positive")
    return arena_cm2 * hours * 3600.0


# ------------------------------------------------------------------ corvid

def recovery_probes_by_search(caches, sites):
    """Expected probes to recover every cache by searching, with no memory.

    Uniform random search without replacement over `sites` candidate
    locations averages (sites + 1) / 2 probes per cache.
    """

    if caches < 0 or sites <= 0:
        raise ValueError("caches must not be negative and sites must exceed 0")
    return caches * (sites + 1) / 2.0


def recovery_probes_by_memory(caches, probes_per_cache=1.0):
    """Probes to recover every cache when the location was stored."""

    if caches < 0 or probes_per_cache <= 0:
        raise ValueError("caches must not be negative and probes must exceed 0")
    return caches * probes_per_cache


def cache_ledger_bits(caches, bits_per_cache):
    """What had to be kept. This is where the cost moved to, not away."""

    if caches < 0 or bits_per_cache <= 0:
        raise ValueError("caches must not be negative and bits must exceed 0")
    return caches * bits_per_cache


# --------------------------------------------------------- ornithorhynchus

def arrival_offset_seconds(distance_m, sound_speed=SOUND_SPEED_FRESHWATER):
    """Delay between the electrical and the mechanical arrival.

    The electrical field arrives at effectively the speed of light over
    centimetre distances; the pressure wave arrives at the speed of sound in
    water. The offset is therefore distance / sound_speed to well within any
    biological timing resolution.
    """

    if distance_m <= 0:
        raise ValueError("distance must be positive")
    return distance_m / float(sound_speed)


def range_from_offset(offset_s, sound_speed=SOUND_SPEED_FRESHWATER):
    """The inverse: one multiplication, and the range is out.

    No occupancy grid is populated, no map is queried. The quantity the
    animal needs is the quantity the two channels' disagreement already is.
    """

    if offset_s <= 0:
        raise ValueError("offset must be positive")
    return offset_s * float(sound_speed)


def occupancy_grid_cells(radius_m, resolution_m, hemisphere=True):
    """Cells in the map a model-then-locate approach would have to carry.

    This is the representation the platypus does not build. It is polynomial,
    not exponential -- the point is not that it is unaffordable, but that it
    is an intermediate object the animal has no need of.
    """

    if radius_m <= 0 or resolution_m <= 0:
        raise ValueError("radius and resolution must be positive")
    volume = (4.0 / 3.0) * math.pi * radius_m ** 3
    if hemisphere:
        volume /= 2.0
    return volume / (resolution_m ** 3)


# ------------------------------------------------------------------ report

SOURCES = (
    ("physarum / maze",
     "Nakagaki, Yamada & Toth 2000, Nature 407:470. Plasmodium of Physarum "
     "polycephalum selects the shortest of several connecting paths."),
    ("physarum / network",
     "Tero et al. 2010, Science 327:439. Plasmodium over 36 food sources "
     "positioned as Tokyo-area stations; resulting network compared to rail."),
    ("steiner / enumeration",
     "Dreyfus & Wagner 1971, Networks 1:195. Exact Steiner-tree DP, the "
     "3**k term. Steiner tree in graphs is NP-hard (Karp 1972)."),
    ("corvid / cache volume",
     "Vander Wall & Balda 1977, Ecol Monogr 47:89; Vander Wall 1982, Anim "
     "Behav 30:84. Clark's nutcracker, NUCIFRAGA COLUMBIANA -- thousands of "
     "caches, tens of thousands of seeds. NOT genus Corvus."),
    ("corvid / what-where-when",
     "Clayton & Dickinson 1998, Nature 395:272. Western scrub-jay, "
     "APHELOCOMA CALIFORNICA. NOT genus Corvus."),
    ("corvid / observer tracking",
     "Bugnyar & Heinrich 2005, Proc R Soc B 272:1641; Bugnyar, Reber & "
     "Buckner 2016, Nat Commun 7:10506. Common raven, CORVUS CORAX -- "
     "re-caching conditioned on whether a competitor could observe."),
    ("platypus / receptors",
     "Scheich et al. 1986, Nature 319:401; Manger & Pettigrew 1995, Phil "
     "Trans R Soc B 347:423. Bill carries electroreceptors and "
     "mechanoreceptors in striped arrangement."),
    ("platypus / time-offset range",
     "Pettigrew 1999, J Exp Biol 202:1447 -- proposes range from the "
     "electrical/mechanical arrival difference. A MODEL, not a measured "
     "mechanism. See AUDIT_NOTES.md."),
    ("ceiling",
     "Lloyd 1999, Phys Rev Lett 88:237901. ~1e120 operations. Used here "
     "only to locate crossovers, not as a claim about any organism."),
)


def report(stream=sys.stdout):
    write = stream.write
    write("SEARCH SUBSTITUTION\n")
    write("ceiling: 1e%d operations (Lloyd 1999)\n\n" % int(CEILING_LOG10))

    write("CROSSOVERS -- where a method exceeds the ceiling\n")
    write("  2**k   exceeds at k = %d components\n" % crossover_exponential(2))
    write("  3**k   exceeds at k = %d residues\n" % crossover_exponential(3))
    write("  N**2   exceeds at N = 1e%d bodies\n" % crossover_polynomial(2))
    write("  N**3   exceeds at N = 1e%d bodies\n" % crossover_polynomial(3))
    write("  Earth carries ~1e50 atoms: N**2 fits, N**3 does not, at one N.\n")
    write("  The exponent decides, not the size.\n\n")

    write("PHYSARUM -- occupancy instead of enumeration\n")
    terminals = 36
    write("  Tero 2010 ran %d terminals.\n" % terminals)
    write("  Exact Steiner DP carries 3**%d = %.3g subproblem splits.\n"
          % (terminals, float(steiner_dp_terms(terminals))))
    write("  Plasmodium cost has no terminal term at all: it is arena held\n")
    write("  for a duration. A 100 cm2 arena for 26 h is %.3g cm2-seconds,\n"
          % physarum_occupancy(100.0, 26.0))
    write("  and that figure does not move when terminals are added.\n\n")

    write("CORVID -- storage instead of search\n")
    caches, sites = 5000, 10000
    searched = recovery_probes_by_search(caches, sites)
    remembered = recovery_probes_by_memory(caches)
    write("  %d caches over %d candidate sites.\n" % (caches, sites))
    write("  Recovered by search:   %.3g probes\n" % searched)
    write("  Recovered by memory:   %.3g probes\n" % remembered)
    write("  Ratio: %.3g. The cost did not vanish -- it moved to the ledger,\n"
          % (searched / remembered))
    write("  %.3g bits at 64 bits per cache, carried the whole interval.\n"
          % cache_ledger_bits(caches, 64))
    write("  Species are not interchangeable here; see --sources.\n\n")

    write("ORNITHORHYNCHUS -- coupling instead of representation\n")
    for distance in (0.05, 0.10, 0.20):
        write("  %4.0f mm of range  ->  %6.1f us of arrival offset\n"
              % (distance * 1000.0, arrival_offset_seconds(distance) * 1e6))
    cells = occupancy_grid_cells(0.5, 0.001)
    write("  Recovered by one multiplication: %.3f m from %.1f us.\n"
          % (range_from_offset(67e-6), 67.0))
    write("  A map-then-query approach would carry %.3g cells at 1 mm over\n"
          % cells)
    write("  a 0.5 m hemisphere. The animal carries none of them.\n\n")

    write("The exponential is a property of the representation, not of the\n")
    write("system. Check which one you are pricing.\n")


def sources(stream=sys.stdout):
    stream.write("SOURCES\n\n")
    for label, text in SOURCES:
        stream.write("  %s\n    %s\n\n" % (label, text))


# ---------------------------------------------------------------- selftest

def selftest(stream=sys.stdout):
    checks = []

    def check(name, condition):
        checks.append((name, bool(condition)))

    check("2**k crosses at 399", crossover_exponential(2) == 399)
    check("3**k crosses at 252", crossover_exponential(3) == 252)
    check("N**2 crosses at 1e60", abs(crossover_polynomial(2) - 60.0) < 1e-9)
    check("N**3 crosses at 1e40", abs(crossover_polynomial(3) - 40.0) < 1e-9)
    check("crossover is the FIRST integer over the ceiling",
          2 ** 399 > 10 ** 120 and 2 ** 398 < 10 ** 120)
    check("3**k crossover is tight",
          3 ** 252 > 10 ** 120 and 3 ** 251 < 10 ** 120)
    check("base must exceed 1", _raises(crossover_exponential, 1))

    check("steiner DP is 3**k", steiner_dp_terms(4) == 81)
    check("steiner DP at 36 terminals exceeds 1e17",
          steiner_dp_terms(36) > 1e17)
    check("occupancy carries no terminal term",
          physarum_occupancy(100.0, 26.0) == 100.0 * 26.0 * 3600.0)
    check("occupancy rejects a zero arena", _raises(physarum_occupancy, 0, 1))

    check("search recovery averages (sites+1)/2 per cache",
          recovery_probes_by_search(2, 9) == 10.0)
    check("memory recovery is one probe per cache",
          recovery_probes_by_memory(5000) == 5000.0)
    check("memory beats search at these magnitudes",
          recovery_probes_by_search(5000, 10000)
          > recovery_probes_by_memory(5000))
    check("ledger is caches times bits",
          cache_ledger_bits(5000, 64) == 320000)

    offset = arrival_offset_seconds(0.10)
    check("100 mm gives ~68 us offset", 6.5e-5 < offset < 7.0e-5)
    check("offset and range invert",
          abs(range_from_offset(arrival_offset_seconds(0.15)) - 0.15) < 1e-12)
    check("range scales linearly with offset",
          abs(range_from_offset(2e-4) - 2.0 * range_from_offset(1e-4)) < 1e-12)
    check("grid cells grow as the cube of resolution",
          abs(occupancy_grid_cells(0.5, 0.001)
              / occupancy_grid_cells(0.5, 0.002) - 8.0) < 1e-9)
    check("grid rejects a zero resolution",
          _raises(occupancy_grid_cells, 0.5, 0))

    check("every source carries a citation",
          all(len(text) > 20 for _, text in SOURCES))
    check("species caveat is carried in the sources",
          any("NOT genus Corvus" in text for _, text in SOURCES))
    check("platypus range is flagged as a model",
          any("MODEL, not a measured mechanism" in text for _, text in SOURCES))

    passed = sum(1 for _, ok in checks if ok)
    for name, ok in checks:
        stream.write("  %s  %s\n" % ("ok  " if ok else "FAIL", name))
    stream.write("\nselftest %d/%d\n" % (passed, len(checks)))
    return passed == len(checks)


def _raises(function, *args):
    try:
        function(*args)
    except ValueError:
        return True
    return False


def main(argv=None):
    parser = argparse.ArgumentParser(description="search substitution")
    parser.add_argument("--sources", action="store_true",
                        help="print where each figure came from")
    parser.add_argument("--selftest", action="store_true",
                        help="run internal checks")
    args = parser.parse_args(argv)

    if args.selftest:
        return 0 if selftest() else 1
    if args.sources:
        sources()
        return 0
    report()
    return 0


if __name__ == "__main__":
    sys.exit(main())
