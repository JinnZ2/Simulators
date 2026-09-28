# SPDX-License-Identifier: CC0-1.0
"""lag_count.py -- FWO-11. Cases where a system under direct constraint produced
a result and the funding-coupled system reached it late, partially, or not at
all. Output: a lag distribution, never an impossibility claim.

    python3 lag_count.py             the seed cases and the distribution
    python3 lag_count.py --choices   every [CHOICE n] in force
    python3 test_single_channel.py   the checks; this module refuses --selftest

EVERY OUTPUT HEADER STATES: the record is survivor-filtered (DERIVED, the order's).
Only what lasted or was recovered can be counted.  A lag distribution over the
counted cases is a distribution over survivors.

per case   produced, by (a population, never a person), approx_date, reach_date,
           reached in FULL / PARTIAL / NOT_REACHED / RECOVERED_NOT_REDISCOVERED / UNKNOWN,
           source, selector (not patented / not sold / not produced for revenue, each
           True / False / UNKNOWN), settlement_check (an FWO-5 reading or NOT_RUN)
lag_years  reach_date - approx_date, ONLY for FULL and PARTIAL with both dates; None
           otherwise; a reach before the production is REFUSED (NEGATIVE_LAG), which
           is the fail fixture
independence  CANDIDATE unless the selector passes on all three AND settlement_check
           reads INDEPENDENT; never marked independent from the selector alone (the
           order: check the settlement layer with FWO-5 first)
sources    every seed date below is UNSOURCED: recalled, no document reached (egress
           allowlist).  The order says verify, do not assume; nothing was verified.
           The distribution is printed over SOURCED rows (empty) and UNSOURCED rows
           (the seeds) APART, never merged.  Years are astronomical (negative = BCE),
           approximate, and read as such.

Stdlib only. Parses under Python 3.8. No network. CC0.
"""
import sys

REACHED = ("FULL", "PARTIAL", "NOT_REACHED", "RECOVERED_NOT_REDISCOVERED", "UNKNOWN")
LAGGED = ("FULL", "PARTIAL")
UNKNOWN = "UNKNOWN"
SURVIVOR_LINE = ("SURVIVOR-FILTERED (DERIVED): only what lasted or was recovered can be counted; "
                 "this is a lag distribution over survivors, not an impossibility claim")

CHOICES = {
    1: "lag is counted on FULL and PARTIAL only; the other three classes carry no reach date by definition",
    2: "a seed date recalled from memory is UNSOURCED; the sourced distribution is empty and printed as empty",
    3: "independence needs the selector on all three axes AND an FWO-5 settlement reading; the selector alone gives CANDIDATE",
    4: "where a case admits two measurands (device vs capability) the coded class follows the DEVICE and the other reading is carried in also_fits",
}


class LagError(ValueError):
    pass


def _tri(v, name):
    if v not in (True, False, UNKNOWN):
        raise LagError("%s is True, False or UNKNOWN" % name)
    return v


def case(cid, produced, by_population, approx_date, reach_date, reached, source,
         not_patented=UNKNOWN, not_sold=UNKNOWN, not_for_revenue=UNKNOWN,
         settlement_check="NOT_RUN", also_fits="", note=""):
    if reached not in REACHED:
        raise LagError("%s: reached must be one of %s" % (cid, REACHED))
    if not isinstance(source, dict) or source.get("kind") not in ("UNSOURCED", "CARRIED", "READ", "VERIFIED", "CONSTRUCTED"):
        raise LagError("%s: source is a dict with kind UNSOURCED/CARRIED/READ/VERIFIED/CONSTRUCTED" % cid)
    if reached in LAGGED and reach_date is None:
        raise LagError("%s: reached %s needs a reach_date; a lag with no date is not a lag" % (cid, reached))
    if reached not in LAGGED and reach_date is not None:
        raise LagError("%s: reach_date is recorded on FULL/PARTIAL only [CHOICE 1]" % cid)
    if approx_date is not None and reach_date is not None and reach_date < approx_date:
        raise LagError("%s: NEGATIVE_LAG: reach %s precedes production %s" % (cid, reach_date, approx_date))
    if not isinstance(by_population, str) or not by_population:
        raise LagError("%s: by_population is required and names a population" % cid)
    return {"id": cid, "produced": produced, "by": by_population, "approx_date": approx_date,
            "reach_date": reach_date, "reached": reached, "source": source,
            "selector": {"not_patented": _tri(not_patented, "not_patented"), "not_sold": _tri(not_sold, "not_sold"),
                         "not_for_revenue": _tri(not_for_revenue, "not_for_revenue")},
            "settlement_check": settlement_check, "also_fits": also_fits, "note": note}


def lag_years(approx_date, reach_date, reached):
    """None unless reached is FULL/PARTIAL and both dates exist; refuses a reach before production."""
    if reached not in LAGGED or approx_date is None or reach_date is None:
        return None
    if reach_date < approx_date:
        raise LagError("NEGATIVE_LAG")
    return reach_date - approx_date


def independence(c):
    s = c["selector"]
    if any(v is False for v in s.values()):
        return "NOT_INDEPENDENT_BY_SELECTOR"
    if any(v == UNKNOWN for v in s.values()):
        return "CANDIDATE"
    if c["settlement_check"] == "INDEPENDENT":
        return "INDEPENDENT"
    return "CANDIDATE"                                                    # [CHOICE 3]


def distribution(cases):
    sourced, unsourced = [], []
    by_reached = dict((r, 0) for r in REACHED)
    for c in cases:
        by_reached[c["reached"]] += 1
        lg = lag_years(c["approx_date"], c["reach_date"], c["reached"])
        if lg is None:
            continue
        (unsourced if c["source"]["kind"] == "UNSOURCED" else sourced).append((c["id"], lg))
    return {"cases": len(cases), "by_reached": by_reached,
            "sourced_lags": sorted(sourced, key=lambda t: t[1]),
            "unsourced_lags": sorted(unsourced, key=lambda t: t[1]),
            "unknown_reach_date": [c["id"] for c in cases if c["reached"] == UNKNOWN],
            "independence": dict((c["id"], independence(c)) for c in cases)}


def seed_cases():
    u = {"kind": "UNSOURCED", "note": "recalled in session; no document reached (egress allowlist); verify before use"}
    o = "CARRIED: the case is on the order's seed list (OBSERVED there); the dates are this session's recall"
    return [
        case("terra_preta", "anthropogenic dark earth: durable soil fertility from charcoal, bone and organic amendment",
             "pre-Columbian Amazon-basin agricultural populations", 500, 2006, "PARTIAL", u,
             not_patented=True, not_sold=UNKNOWN, not_for_revenue=UNKNOWN,
             note=o + "; approx_date is a midpoint of a span running roughly -450 to 950; the coupled system's "
                      "reach is the biochar research programme (mid-2000s), which reproduces the amendment and not "
                      "the soil's persistence, hence PARTIAL"),
        case("willow_bark", "salicylate analgesic and antipyretic from willow bark",
             "folk-medicine populations across several regions; a written clinical report in 1763",
             -400, 1897, "FULL", u, not_patented=True, not_sold=UNKNOWN, not_for_revenue=UNKNOWN,
             note=o + "; approx_date is the Hippocratic corpus; reach_date is acetylsalicylic acid synthesised "
                      "for a manufacturer; FULL with a chemical difference (the acetyl derivative, not salicin)"),
        case("antikythera", "geared astronomical calculator with epicyclic gearing",
             "a Hellenistic workshop tradition", -125, None, "RECOVERED_NOT_REDISCOVERED", u,
             not_patented=True, not_sold=UNKNOWN, not_for_revenue=UNKNOWN,
             also_fits="FULL at about 1350 on the CAPABILITY reading (astronomical clocks with comparable gearing); "
                       "the DEVICE was not rebuilt from within the coupled tradition and was recovered in 1901 [CHOICE 4]",
             note=o),
        case("aqueducts", "gravity-fed long-distance water conveyance (Roman aqueducts; qanats earlier)",
             "Roman state builders; Persian and Arabian qanat-digging communities", -312, None, "UNKNOWN", u,
             not_patented=True, not_sold=UNKNOWN, not_for_revenue=UNKNOWN,
             note=o + "; UNKNOWN because the producer of the named instance is a state, and whether that system "
                      "was 'direct constraint' or 'funding coupled' is not decidable from memory; the qanat "
                      "communities fit the direct-constraint reading and the coupled system's reach date does not "
                      "have a referent"),
        case("bamboo_gas_piping", "natural gas conveyed by bamboo pipe to brine-boiling works",
             "Sichuan salt-well communities", -100, 1821, "FULL", u,
             not_patented=True, not_sold=UNKNOWN, not_for_revenue=UNKNOWN,
             note=o + "; reach_date is the first piped natural-gas lighting in North America; the salt the gas "
                      "boiled was sold, so not_for_revenue is UNKNOWN rather than True"),
        case("machu_picchu", "hillside terracing with subsurface drainage layers",
             "Inca builders and the agricultural population that maintained it", 1450, 2000, "PARTIAL", u,
             not_patented=True, not_sold=UNKNOWN, not_for_revenue=UNKNOWN,
             note=o + "; reach_date is the modern geotechnical study that characterised the drainage; PARTIAL "
                      "because modern drainage engineering reached the function earlier by a route the memory "
                      "cannot date, and the specific design was characterised rather than reached"),
    ]


def fail_fixture():
    """CONSTRUCTED: reach precedes production; the constructor and lag_years both refuse it."""
    return dict(cid="z_fail_negative_lag", produced="fixture", by_population="fixture population",
                approx_date=1900, reach_date=1800, reached="FULL",
                source={"kind": "CONSTRUCTED", "note": "fail fixture"})


def check_expectations(cases):
    d = distribution(cases)
    by = dict((c["id"], c) for c in cases)
    full_dated = sum(1 for c in cases if c["reached"] == "FULL" and c["reach_date"] is not None)
    rows = [
        ("E11.1 antikythera reads RECOVERED_NOT_REDISCOVERED",
         "antikythera" in by and by["antikythera"]["reached"] == "RECOVERED_NOT_REDISCOVERED"),
        ("E11.2 at most two FULL with a dated reach; at least one UNKNOWN reach date",
         full_dated <= 2 and len(d["unknown_reach_date"]) >= 1),
        ("E11.3 sourced distribution empty; unsourced apart", d["sourced_lags"] == [] and len(d["unsourced_lags"]) > 0),
        ("E11.5 no seed reads INDEPENDENT", all(v != "INDEPENDENT" for v in d["independence"].values())),
    ]
    return [(l, "MATCH" if v else "MISMATCH") for l, v in rows]


def render(out=None):
    out = out or sys.stdout
    w = out.write
    cases = seed_cases()
    w("lag_count -- FWO-11; the seed cases and the lag distribution\n")
    w("%s\n" % SURVIVOR_LINE)
    w("every seed date UNSOURCED (recalled; the order says verify, nothing was verified)\n\n")
    w("%-18s %-8s %-8s %-28s %-6s %s\n" % ("case", "approx", "reach", "reached", "lag", "independence"))
    for c in cases:
        lg = lag_years(c["approx_date"], c["reach_date"], c["reached"])
        w("%-18s %-8s %-8s %-28s %-6s %s\n" % (
            c["id"], c["approx_date"], "--" if c["reach_date"] is None else c["reach_date"], c["reached"],
            "--" if lg is None else lg, independence(c)))
        w("   by: %s\n   produced: %s\n" % (c["by"], c["produced"]))
        if c["also_fits"]:
            w("   also fits: %s\n" % c["also_fits"])
    d = distribution(cases)
    w("\nby reached: %s\n" % ", ".join("%s=%d" % (k, d["by_reached"][k]) for k in REACHED))
    w("sourced lags (years):   %s\n" % (d["sourced_lags"] or "[] (no seed is sourced)"))
    w("unsourced lags (years): %s\n" % d["unsourced_lags"])
    w("unknown reach date: %s\n\n" % d["unknown_reach_date"])
    for l, v in check_expectations(cases):
        w("expected %-72s %s\n" % (l, v))
    try:
        case(**fail_fixture())
        w("fail fixture (CONSTRUCTED, reach before production): NOT REFUSED\n")
    except LagError as e:
        w("fail fixture (CONSTRUCTED, reach before production): refused -- %s\n" % e)
    w("choices in force: %s\n" % ", ".join("[CHOICE %d]" % k for k in sorted(CHOICES)))


def main(argv):
    if "--selftest" in argv:
        sys.stderr.write("library module; run: python3 route-independence/test_single_channel.py\n")
        return 2
    if "--choices" in argv:
        for k in sorted(CHOICES):
            print("[CHOICE %d] %s" % (k, CHOICES[k]))
        return 0
    render()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
