#!/usr/bin/env python3
"""
QRNG PAIR SEARCH
Candidate axes for two-source joint keying. Stdlib only. CC0.

The unit of search is (source, bath_set), not (source, name). Two sources
coupled to different baths beats two sources with different names. This is
`category-weld/` pointed the other way: a weld fuses quantities that are
independent in the world into one handle, and here the shared bath is the
welder. The audit is the same instrument, run to establish independence
rather than to expose its absence.

THREE CORRECTIONS TO THE DELIVERED TABLE, each carried in the data below.

1. A BATH SET ASSIGNED TO THE SOURCE IS NOT THE BATH SET OF THE LEG. Alpha
   decay is genuinely near-immune to substrate temperature and rail drift;
   the nucleus does not care. The DETECTOR cares. A PIN diode has leakage
   that doubles every ~7 C, a PMT or Geiger tube needs a high-voltage rail,
   and both sit on the board with everything else. Pricing `decay_alpha` at
   baths={"COS"} prices the physics and drops the readout chain -- so the
   delivered `decay_alpha x rtd_tunnel -> CLEAN, overlap {}` verdict is
   false as fielded. Every source below therefore carries `source_baths` and
   `readout_baths` separately, and pair verdicts use the union.

2. THE CORRELATION RULE IS NOT WHERE ENTROPY HIDES. "The correlation rule is
   where you can hide the actual entropy" is security through obscurity: the
   rule is an algorithm, and Kerckhoffs's principle says price it as public.
   Hiding the combiner adds no min-entropy. What the two-source structure
   actually buys is that a two-source extractor needs NO seed and NO secrecy
   -- it needs independence, which is the thing this module measures. The
   security sits in the min-entropy of the legs, not in the rule.

3. MIN-ENTROPY, NOT SHANNON. Correlated drift attacks the min-entropy far
   harder than it attacks the average. A pair whose Shannon entropy is
   barely dented can have its min-entropy halved by a bath excursion that
   pushes both legs the same way at the same time.
"""

import argparse
import itertools
import math
import sys


BATHS = {
    "TH": "thermal phonon / substrate temperature",
    "EM": "ambient EM field, RF pickup",
    "PWR": "shared power rail, bias drift",
    "MECH": "vibration, acoustic, strain",
    "OPT": "shared pump laser / optical path",
    "COS": "cosmic ray + ambient ionizing background",
}

QUANTUM = "QUANTUM"        # indeterminacy is in the physics
PARTIAL = "PARTIAL"        # quantum floor, classical gain stage on top
CLASSICAL = "CLASSICAL"    # no quantum indeterminacy; never a leg


SOURCES = {
    "decay_alpha": dict(
        mechanism="nuclear tunneling, per-nucleus indeterminate",
        quantum=QUANTUM,
        # The nucleus is not listening to the board.
        source_baths={"COS"},
        # The detector is. Bias rail, leakage current, and the substrate it
        # is mounted on. This is the correction that kills the CLEAN verdict.
        readout_baths={"TH", "PWR", "EM"},
        rate_hz=(1e1, 1e5),
        footprint="cm, needs shielding",
        gate="isotope licensing; rate fixed by half-life, not tunable",
    ),
    "photon_split": dict(
        mechanism="which-path at a 50/50 beamsplitter",
        quantum=QUANTUM,
        source_baths={"OPT"},
        readout_baths={"TH", "PWR", "EM"},
        rate_hz=(1e6, 1e9),
        footprint="mm-cm, alignment-sensitive",
        gate="pump laser is a shared bath if reused across legs",
    ),
    "avalanche_diode": dict(
        mechanism="shot noise with avalanche multiplication",
        quantum=PARTIAL,
        source_baths={"TH"},
        readout_baths={"TH", "PWR", "EM"},
        rate_hz=(1e6, 1e8),
        footprint="chip",
        gate="cheapest to field, worst bath overlap, gain stage is classical",
    ),
    "vacuum_homodyne": dict(
        mechanism="vacuum field quadrature fluctuation",
        quantum=QUANTUM,
        source_baths={"OPT"},
        readout_baths={"TH", "PWR", "EM"},
        rate_hz=(1e8, 1e10),
        footprint="benchtop to chip photonics",
        gate="local oscillator laser is a shared bath",
    ),
    "rtd_tunnel": dict(
        mechanism="resonant tunneling current fluctuation",
        quantum=QUANTUM,
        source_baths={"TH"},
        readout_baths={"TH", "PWR", "EM"},
        rate_hz=(1e6, 1e9),
        footprint="chip",
        gate="strong thermal coupling at the source, not only the readout",
    ),
    "nv_spin": dict(
        mechanism="NV-centre spin projection readout",
        quantum=QUANTUM,
        source_baths={"EM", "OPT"},
        readout_baths={"TH", "PWR", "EM", "OPT"},
        rate_hz=(1e3, 1e6),
        footprint="mm plus optics plus microwave",
        gate="microwave drive is the exposure surface; EM coupling by design",
    ),
    "johnson_noise": dict(
        mechanism="thermal resistor noise",
        quantum=CLASSICAL,
        source_baths={"TH"},
        readout_baths={"TH", "PWR", "EM"},
        rate_hz=(1e6, 1e9),
        footprint="chip",
        gate="EXCLUDED: classical. Do not use as either leg.",
    ),
}


# Which readout resources two legs share is a property of the DEPLOYMENT, not
# of either source. Assigning readout baths to a source makes them a constant
# across every pair -- measured: identical for all seven sources here -- and a
# constant cannot separate pairs. Assigning SHARING to the pair is what
# discriminates. Both the original table (baths on the source) and this
# folder's first correction (readout_baths on the source) put it on the wrong
# object.
READOUT_SHARING = {
    "board": {"TH"},          # one substrate, one temperature
    "rail": {"PWR"},          # one supply, one bias drift
    "clock": {"EM"},          # one oscillator, one pickup path
    "adc": {"EM", "PWR"},     # one converter carries both
}

# Compact single-board is the worst case and the case the squeeze is about.
FULLY_SHARED = frozenset(READOUT_SHARING)


def shared_readout_baths(shared):
    """Baths introduced by the readout elements two legs actually share."""

    unknown = set(shared) - set(READOUT_SHARING)
    if unknown:
        raise ValueError("unknown readout element(s): %s" % sorted(unknown))
    out = set()
    for element in shared:
        out |= READOUT_SHARING[element]
    return out


def effective_baths(name):
    """What the fielded leg actually couples to: source plus readout."""

    source = SOURCES[name]
    return set(source["source_baths"]) | set(source["readout_baths"])


def pair_score(a, b, shared=FULLY_SHARED):
    """Score a candidate pair on independence, admissibility and rate.

    Two overlaps are reported and they are not interchangeable.

      structural  the baths the SOURCES share. Irreducible without changing
                  the physics of one leg.
      fielded     structural, plus the baths introduced by the readout
                  elements the two legs actually share. `shared` is a
                  deployment choice, so this moves with the build -- which is
                  the whole point: it is the only part a designer controls.

    Passing shared=frozenset() prices two legs on fully separate chains. That
    is the bound, not a description of any real board.
    """

    A, B = SOURCES[a], SOURCES[b]
    structural = set(A["source_baths"]) & set(B["source_baths"])
    fielded = structural | shared_readout_baths(shared)
    return dict(
        pair=(a, b),
        admissible=A["quantum"] == QUANTUM and B["quantum"] == QUANTUM,
        structural_overlap=structural,
        fielded_overlap=fielded,
        independence=("clean" if not fielded
                      else "welded:" + ",".join(sorted(fielded))),
        separable=bool(fielded) and not structural,
        rate_cap_optimistic=min(A["rate_hz"][1], B["rate_hz"][1]),
        rate_floor_conservative=min(A["rate_hz"][0], B["rate_hz"][0]),
    )


def admissible_pairs(shared=FULLY_SHARED):
    """Every quantum-quantum pair, ordered by how little the legs share."""

    scored = [pair_score(a, b, shared)
              for a, b in itertools.combinations(sorted(SOURCES), 2)]
    scored = [s for s in scored if s["admissible"]]
    return sorted(scored, key=lambda s: (len(s["structural_overlap"]),
                                         len(s["fielded_overlap"]),
                                         s["pair"]))


# ------------------------------------------------------- entropy accounting

def xor_floor_bits(k1, k2):
    """Min-entropy guaranteed by XOR of two INDEPENDENT streams.

    XOR of independent sources has min-entropy at least that of the better
    leg. No extractor and no seed required. This is the floor to design to,
    because it survives one leg being fully compromised.
    """

    if k1 < 0 or k2 < 0:
        raise ValueError("min-entropies must not be negative")
    return max(k1, k2)


def two_source_target_bits(k1, k2, correlation_bits=0.0):
    """The k1 + k2 target a two-source extractor aims at, less any coupling.

    This is a BUDGET, not a bound. Reaching it requires a named two-source
    extractor with a stated error parameter and min-entropy requirement;
    which extractor is a design decision this module does not make. The
    `correlation_bits` term is the mutual information the independence
    measurement actually found -- not an assumed zero.
    """

    if k1 < 0 or k2 < 0 or correlation_bits < 0:
        raise ValueError("entropies and coupling must not be negative")
    return max(0.0, k1 + k2 - correlation_bits)


def samples_for_correlation(r_target, sigma=5.0, lags=1):
    """Samples needed to resolve a correlation of magnitude r_target.

    Under the null the standard error of Pearson r is ~1/sqrt(N), so
    detecting r at `sigma` significance needs N >= (sigma / r)**2. Scanning
    `lags` lags is a multiple-comparison problem, so the threshold is raised
    by the Bonferroni-equivalent normal quantile before the count is taken.

    This is the correction to "over >= 1e6 samples": 1e6 samples resolves
    r >= 5e-3 and is blind to anything smaller.
    """

    if not 0 < r_target < 1:
        raise ValueError("r_target must lie in (0, 1)")
    if sigma <= 0 or lags < 1:
        raise ValueError("sigma must be positive and lags at least 1")
    adjusted = sigma + math.log(lags) / sigma if lags > 1 else sigma
    return (adjusted / r_target) ** 2


def cross_correlation(xs, ys, lag):
    """Pearson correlation of xs against ys shifted by `lag`. Stdlib only."""

    if lag < 0:
        raise ValueError("lag must not be negative")
    n = min(len(xs), len(ys) - lag)
    if n < 2:
        raise ValueError("not enough overlapping samples")
    a = xs[:n]
    b = ys[lag:lag + n]
    mean_a = sum(a) / n
    mean_b = sum(b) / n
    da = [v - mean_a for v in a]
    db = [v - mean_b for v in b]
    num = sum(x * y for x, y in zip(da, db))
    den = math.sqrt(sum(x * x for x in da) * sum(y * y for y in db))
    return 0.0 if den == 0 else num / den


# --------------------------------------------------------------- protocols

MITIGATIONS = {
    "rate_extension":
        "the slow leg keys a namespace or partition layer; the fast leg "
        "carries payload entropy under it. Offset-as-namespace, not "
        "offset-as-key.",
    "bath_separation":
        "split the pump: independent lasers, independent rails, thermal "
        "isolation. This converts an OPT/TH/PWR overlap from structural to "
        "engineered -- and an engineered separation must then be MEASURED, "
        "not asserted. That is what separates `separable` from `clean`.",
    "not_a_mitigation":
        "keeping the combiner secret. The rule is an algorithm; price it as "
        "public. Secrecy of the combiner adds no min-entropy.",
}


INDEPENDENCE_PROTOCOL = (
    ("cross_corr",
     "XCF(a,b) at lags 0..L. Sample count set by samples_for_correlation() "
     "for the smallest r that would matter, NOT by a round number."),
    ("common_perturb",
     "sweep the suspected shared bath and watch both legs at once:"),
    ("  temp",
     "  ramp substrate 0->60 C, measure dP(bit=1) per leg, correlate"),
    ("  rail",
     "  sag and ripple the supply, same readout"),
    ("  mech",
     "  vibration sweep -- couples through alignment, not electronics"),
    ("  em",
     "  RF injection sweep across the readout band"),
    ("verdict",
     "coupling shows up under perturbation that is invisible at rest. A "
     "quiet-bench cross-correlation of zero is not evidence of "
     "independence; it is evidence the bath was not moving."),
)


def independence_protocol():
    return INDEPENDENCE_PROTOCOL


# ------------------------------------------------------------------ report

def report(stream=sys.stdout):
    write = stream.write
    write("QRNG PAIR SEARCH\n")
    write("unit of search = (source, bath_set), not (source, name)\n\n")

    write("SOURCES -- effective bath is source | readout\n")
    for name in sorted(SOURCES):
        src = SOURCES[name]
        flag = "" if src["quantum"] == QUANTUM else "  [%s]" % src["quantum"]
        write("  %-16s src=%-12s readout=%-18s eff=%s%s\n" % (
            name,
            ",".join(sorted(src["source_baths"])) or "-",
            ",".join(sorted(src["readout_baths"])) or "-",
            ",".join(sorted(effective_baths(name))) or "-",
            flag,
        ))

    write("\nREADOUT SHARING IS A DEPLOYMENT CHOICE, NOT A SOURCE PROPERTY\n")
    for label, shared in (("single board, one ADC", FULLY_SHARED),
                          ("split rail/clock/ADC, same board",
                           frozenset({"board"})),
                          ("fully separate chains", frozenset())):
        pairs = admissible_pairs(shared)
        clean = len([p for p in pairs if not p["fielded_overlap"]])
        write("  %-34s %d of %d pairs clean\n" % (label, clean, len(pairs)))
    write("  decay_alpha x rtd_tunnel is source-disjoint and welds at the ADC.\n")
    write("  Compactness forces sharing: that is the squeeze, priced.\n")

    write("\nADMISSIBLE PAIRS -- quantum on both legs, single shared board\n")
    write("  %-34s %-10s %-22s %s\n"
          % ("pair", "structural", "fielded", "rate cap"))
    for score in admissible_pairs():
        write("  %-34s %-10s %-22s %.0e\n" % (
            "%s x %s" % score["pair"],
            ",".join(sorted(score["structural_overlap"])) or "-",
            score["independence"],
            score["rate_cap_optimistic"],
        ))

    write("\n  On one shared board every pair welds at TH/PWR/EM. The pairs\n")
    write("  worth building are those with an EMPTY STRUCTURAL overlap, where\n")
    write("  the weld is an engineering fact rather than a physics one -- and\n")
    write("  where separating the chains is therefore both possible and\n")
    write("  measurable. A structural weld survives any chain separation.\n")

    separable = [s for s in admissible_pairs() if s["separable"]]
    write("\n  separable pairs (structural empty, fielded non-empty): %d of %d\n"
          % (len(separable), len(admissible_pairs())))

    write("\nSAMPLE COUNTS -- what a correlation sweep can actually resolve\n")
    for r in (5e-3, 1e-3, 1e-4):
        write("  r >= %-7.0e  needs %.2e samples at 5 sigma, 1 lag\n"
              % (r, samples_for_correlation(r)))
        write("  %-15s %.2e samples across 100 lags\n"
              % ("", samples_for_correlation(r, lags=100)))

    write("\nENTROPY -- min-entropy, not Shannon\n")
    write("  two legs at 0.8 and 0.6 bits per sample:\n")
    write("    XOR floor          %.2f bits  (guaranteed, needs independence)\n"
          % xor_floor_bits(0.8, 0.6))
    write("    two-source target  %.2f bits  (budget, needs a named extractor)\n"
          % two_source_target_bits(0.8, 0.6))
    write("    same, with 0.3 bits of measured coupling: %.2f\n"
          % two_source_target_bits(0.8, 0.6, 0.3))
    write("  Secrecy of the combiner appears in none of these lines, because\n")
    write("  it contributes to none of them.\n")


def protocol(stream=sys.stdout):
    stream.write("INDEPENDENCE PROTOCOL\n\n")
    for label, text in INDEPENDENCE_PROTOCOL:
        stream.write("  %-16s %s\n" % (label, text))
    stream.write("\nMITIGATIONS\n\n")
    for label, text in sorted(MITIGATIONS.items()):
        stream.write("  %-18s %s\n" % (label, text))


# ---------------------------------------------------------------- selftest

def _raises(fn, *args):
    try:
        fn(*args)
    except ValueError:
        return True
    return False


def selftest(stream=sys.stdout):
    checks = []

    def check(name, condition):
        checks.append((name, bool(condition)))

    check("classical source is never admissible",
          not pair_score("johnson_noise", "rtd_tunnel")["admissible"])
    check("partial-quantum source is never admissible",
          not pair_score("avalanche_diode", "rtd_tunnel")["admissible"])
    check("quantum pair is admissible",
          pair_score("decay_alpha", "rtd_tunnel")["admissible"])

    decay_rtd = pair_score("decay_alpha", "rtd_tunnel")
    check("decay x rtd has NO structural overlap",
          decay_rtd["structural_overlap"] == set())
    check("decay x rtd IS welded once readout is counted",
          decay_rtd["fielded_overlap"] == {"TH", "PWR", "EM"})
    check("the delivered CLEAN verdict does not survive",
          decay_rtd["independence"].startswith("welded"))
    check("decay x rtd is separable, not clean",
          decay_rtd["separable"])

    laser_pair = pair_score("vacuum_homodyne", "photon_split")
    check("shared-laser pair is structurally welded on OPT",
          laser_pair["structural_overlap"] == {"OPT"})
    check("a structurally welded pair is not separable",
          not laser_pair["separable"])

    check("effective bath is the union",
          effective_baths("decay_alpha") == {"COS", "TH", "PWR", "EM"})
    check("no admissible pair is clean on a single shared board",
          all(s["fielded_overlap"] for s in admissible_pairs()))
    check("separate chains make source-disjoint pairs clean",
          len([s for s in admissible_pairs(frozenset())
               if not s["fielded_overlap"]]) == 7)
    check("sharing only the board leaves TH and nothing else",
          pair_score("decay_alpha", "rtd_tunnel",
                     frozenset({"board"}))["fielded_overlap"] == {"TH"})
    check("a shared ADC welds a source-disjoint pair",
          pair_score("decay_alpha", "rtd_tunnel",
                     frozenset({"adc"}))["fielded_overlap"] == {"EM", "PWR"})
    check("sharing cannot clear a structural weld",
          pair_score("photon_split", "vacuum_homodyne",
                     frozenset())["fielded_overlap"] == {"OPT"})
    check("unknown readout element is rejected",
          _raises(shared_readout_baths, {"nonsense"}))
    check("some admissible pairs are separable",
          any(s["separable"] for s in admissible_pairs()))
    check("rate cap takes the slower leg",
          decay_rtd["rate_cap_optimistic"] == 1e5)
    check("conservative floor is below the optimistic cap",
          decay_rtd["rate_floor_conservative"]
          < decay_rtd["rate_cap_optimistic"])

    check("XOR floor is the better leg",
          xor_floor_bits(0.8, 0.6) == 0.8)
    check("XOR floor is symmetric",
          xor_floor_bits(0.6, 0.8) == xor_floor_bits(0.8, 0.6))
    check("two-source target is the sum when uncoupled",
          abs(two_source_target_bits(0.8, 0.6) - 1.4) < 1e-12)
    check("measured coupling is subtracted",
          abs(two_source_target_bits(0.8, 0.6, 0.3) - 1.1) < 1e-12)
    check("target never goes negative",
          two_source_target_bits(0.2, 0.2, 5.0) == 0.0)
    check("target is at least the XOR floor when uncoupled",
          two_source_target_bits(0.8, 0.6) >= xor_floor_bits(0.8, 0.6))
    check("negative entropy is rejected", _raises(xor_floor_bits, -1.0, 0.5))

    check("1e6 samples resolves 5e-3 and no better",
          abs(samples_for_correlation(5e-3) - 1e6) < 1e3)
    check("resolving 1e-3 costs 2.5e7 samples",
          abs(samples_for_correlation(1e-3) - 2.5e7) < 1e5)
    check("scanning lags raises the sample count",
          samples_for_correlation(1e-3, lags=100)
          > samples_for_correlation(1e-3, lags=1))
    check("r_target outside (0,1) is rejected",
          _raises(samples_for_correlation, 0.0))

    check("identical series correlate at 1",
          abs(cross_correlation([1, 2, 3, 4, 5], [1, 2, 3, 4, 5], 0) - 1.0)
          < 1e-12)
    check("inverted series correlate at -1",
          abs(cross_correlation([1, 2, 3, 4, 5], [5, 4, 3, 2, 1], 0) + 1.0)
          < 1e-12)
    check("a constant series correlates at 0",
          cross_correlation([1, 2, 3, 4], [7, 7, 7, 7], 0) == 0.0)
    check("lag shifts the comparison window",
          abs(cross_correlation([1, 2, 3], [9, 1, 2, 3], 1) - 1.0) < 1e-12)
    check("negative lag is rejected",
          _raises(cross_correlation, [1, 2, 3], [1, 2, 3], -1))

    check("obscurity is named as not a mitigation",
          "no min-entropy" in MITIGATIONS["not_a_mitigation"])
    check("protocol ends on the quiet-bench warning",
          "not evidence of" in INDEPENDENCE_PROTOCOL[-1][1])
    check("every bath key is documented",
          all(b in BATHS for s in SOURCES
              for b in effective_baths(s)))

    passed = sum(1 for _, ok in checks if ok)
    for name, ok in checks:
        stream.write("  %s  %s\n" % ("ok  " if ok else "FAIL", name))
    stream.write("\nselftest %d/%d\n" % (passed, len(checks)))
    return passed == len(checks)


def main(argv=None):
    parser = argparse.ArgumentParser(description="qrng pair search")
    parser.add_argument("--protocol", action="store_true",
                        help="print the independence measurement protocol")
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args(argv)
    if args.selftest:
        return 0 if selftest() else 1
    if args.protocol:
        protocol()
        return 0
    report()
    return 0


if __name__ == "__main__":
    sys.exit(main())
