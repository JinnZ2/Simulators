"""
estimate.py -- withheld-demand estimates. CC0. Co-authored. Stdlib only.

  non_claimants = eligible_population - claimants
  three bins, kept separate, never merged and never summed into one figure:
    barrier_non_take_up | unaware | deliberate_withholding
  a bin is a directly reported count or None (UNKNOWN). deliberate_withholding
  is None unless directly reported. The part of non_claimants no bin accounts
  for is reported as unattributed and is assigned to no bin.

  peak and average load are reported separately, never combined.

  python3 estimate.py    # demo on constructed numbers (not data)
"""
import sys

BINS = ("barrier_non_take_up", "unaware", "deliberate_withholding")


def _num(x, name):
    if x is None:
        return None
    if isinstance(x, bool) or not isinstance(x, (int, float)):
        raise ValueError(f"{name} must be a number or None, got {x!r}")
    if x < 0:
        raise ValueError(f"{name} must be >= 0, got {x}")
    return x


def withheld_estimate(eligible_population=None, claimants=None,
                      barrier_non_take_up=None, unaware=None, deliberate_withholding=None):
    """Returns a dict. Never returns a merged or summed bin figure."""
    e = _num(eligible_population, "eligible_population")
    c = _num(claimants, "claimants")
    bins = {"barrier_non_take_up": _num(barrier_non_take_up, "barrier_non_take_up"),
            "unaware": _num(unaware, "unaware"),
            "deliberate_withholding": _num(deliberate_withholding, "deliberate_withholding")}
    out = {"eligible_population": e, "claimants": c, "bins": bins, "flags": []}
    if e is None or c is None:
        out["non_claimants"] = None
        out["unattributed"] = None
        out["flags"].append("NON_CLAIMANTS_UNKNOWN: eligible_population or claimants missing")
    else:
        nc = e - c
        out["non_claimants"] = nc
        if nc < 0:
            out["flags"].append("CLAIMANTS_EXCEED_ELIGIBLE: check the two counts share a population")
        known = [v for v in bins.values() if v is not None]
        if len(known) == len(BINS):
            out["unattributed"] = nc - sum(known)
        else:
            # the remainder cannot be computed without every bin; it is not
            # assigned to the missing bin(s)
            out["unattributed"] = None
            out["flags"].append("UNATTRIBUTED_UNKNOWN: one or more bins not reported")
        if known and sum(known) > nc:
            out["flags"].append("BINS_EXCEED_NON_CLAIMANTS: reported bins overlap or differ in population")
    if bins["deliberate_withholding"] is None:
        out["flags"].append("DELIBERATE_SHARE_UNKNOWN: not directly reported")
    return out


def peak_vs_average(rows):
    """rows: iterables of dicts {"load": number|None, "peak": bool|None}.
    Returns average over all known loads, peak mean, off-peak mean, and the
    count of rows whose peak status is unknown. None where there are no rows."""
    loads, peak, off, unknown_peak, unknown_load = [], [], [], 0, 0
    for r in rows:
        x = r.get("load")
        if x is None:
            unknown_load += 1
            continue
        _num(x, "load")
        loads.append(x)
        p = r.get("peak")
        if p is True:
            peak.append(x)
        elif p is False:
            off.append(x)
        else:
            unknown_peak += 1
    mean = lambda v: (sum(v) / len(v)) if v else None
    return {"average": mean(loads), "peak": mean(peak), "off_peak": mean(off),
            "n": len(loads), "n_peak": len(peak), "n_off_peak": len(off),
            "unknown_peak": unknown_peak, "unknown_load": unknown_load}


def render(est):
    lines = ["withheld estimate"]
    for k in ("eligible_population", "claimants", "non_claimants"):
        lines.append(f"  {k:<24} {est[k]}")
    for b in BINS:
        v = est["bins"][b]
        lines.append(f"  bin {b:<20} {'UNKNOWN' if v is None else v}")
    u = est["unattributed"]
    lines.append(f"  {'unattributed':<24} {'UNKNOWN' if u is None else u}")
    for f in est["flags"]:
        lines.append(f"  flag {f}")
    return "\n".join(lines)


def main(argv):
    if "--selftest" in argv:
        print("estimate.py has no selftest; run: python3 test_load_withheld.py")
        return 2
    print("CONSTRUCTED numbers, not data.")
    print(render(withheld_estimate(1000, 700, barrier_non_take_up=120, unaware=90)))
    print()
    pv = peak_vs_average([{"load": 3, "peak": False}, {"load": 4, "peak": False},
                          {"load": 11, "peak": True}, {"load": 9, "peak": True},
                          {"load": 5, "peak": None}, {"load": None, "peak": True}])
    print("peak vs average (constructed):")
    for k, v in pv.items():
        print(f"  {k:<14} {v}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
