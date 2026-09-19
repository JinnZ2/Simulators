#!/usr/bin/env python3
"""load_class.py -- the order's load-class test as arithmetic.

The reachable controller is a CONJUNCTION of assumed stabilities. The
order lists seven and attaches illustrative percentages to four. This
module computes what that compounding is and is not.

Under independence the chance that at least one of the assessed
factors fails is 1 - prod(1 - p). That is one point in a BAND: with the
factors perfectly positively correlated the union is max(p), and with
them mutually exclusive it is min(1, sum(p)). All three are printed and
none is picked, because the correlation among these factors is not a
number the order supplies. (The direction of that dependence is on
record in this tree: correlation lowers a conjunction's joint failure
and can only raise the union up to the sum.)

The RULE the order marks OBSERVED -- where a factor is unassessed,
engineer on the assumption it is NOT stable -- is implemented as a
refusal to propagate: an unassessed factor enters no arithmetic. It is
listed, and the verdict turns on whether each unassessed factor
declares a STRUCTURAL handling. The order's refinement (bound rather
than invert: worst credible condition plus margin) needs a declared
worst-credible value per factor; where none is declared the bound is
UNBOUNDED, never a default.

Applied to the order's own list: the illustrative compounding is
computed over 4 of 7 factors, so the number it produces is a FLOOR on
the union and the order's own RULE says the other three are not stable.
"""
import sys

# The order's seven, verbatim names; p is illustrative where the order gives one, None otherwise.
FACTORS = (
    {"name": "personnel availability under all conditions", "p": None},
    {"name": "environmental stability", "p": None},
    {"name": "governance continuity", "p": None},
    {"name": "economic continuity", "p": 0.01},
    {"name": "corporate continuity in the same operating form", "p": 0.02},
    {"name": "absence of an internal actor modifying internal access", "p": 0.03},
    {"name": "regional connectivity", "p": 0.04},
)
HANDLING = ("STRUCTURAL", "NONE", "UNDECLARED")


def union_band(ps):
    """Union of failure events over assessed probabilities. None on empty."""
    ps = [p for p in ps if p is not None]
    if not ps:
        return None
    if any(not (0.0 <= p <= 1.0) for p in ps):
        raise ValueError("probability outside [0,1]")
    indep = 1.0
    for p in ps:
        indep *= (1.0 - p)
    return {"n": len(ps), "independent": round(1.0 - indep, 6), "perfect_positive": max(ps),
            "mutually_exclusive": min(1.0, sum(ps)), "band": [max(ps), min(1.0, sum(ps))]}


def apply_rule(factor):
    """The order's RULE and refinement on one factor."""
    p = factor.get("p")
    if p is not None:
        return {"name": factor["name"], "assessed": True, "p": p, "assumed_stable": None, "bound": p}
    wc = factor.get("worst_credible")
    margin = factor.get("margin")
    bound = "UNBOUNDED" if wc is None or margin is None else round(wc + margin, 6)
    return {"name": factor["name"], "assessed": False, "p": None, "assumed_stable": False,
            "handling": factor.get("handling", "UNDECLARED"), "bound": bound}


def assess(factors):
    rows = [apply_rule(f) for f in factors]
    assessed = [r for r in rows if r["assessed"]]
    un = [r for r in rows if not r["assessed"]]
    band = union_band([r["p"] for r in assessed])
    unhandled = [r["name"] for r in un if r.get("handling") != "STRUCTURAL"]
    if not rows:
        state = "EMPTY"
    elif unhandled:
        state = "NOT_FLIGHT_RATED"
    else:
        state = "ASSESSED_OR_HANDLED"
    return {"state": state, "rows": rows, "n_assessed": len(assessed), "n_unassessed": len(un),
            "assessed_share": (len(assessed) / len(rows)) if rows else None, "union": band,
            "union_is_floor": bool(un), "unhandled": unhandled}


def factor_of_safety(design_load, anticipated_load):
    """Structural practice designs to a multiple of estimated load. None
    when the anticipated load is not positive."""
    if design_load is None or anticipated_load is None or anticipated_load <= 0:
        return None
    return round(design_load / anticipated_load, 6)


def render(factors=None):
    a = assess(FACTORS if factors is None else factors)
    lines = ["load_class -- the order's compounding as arithmetic",
             "  state %s  assessed %d of %d (share %s)  union_is_floor %s" % (
                 a["state"], a["n_assessed"], a["n_assessed"] + a["n_unassessed"],
                 "%.3f" % a["assessed_share"] if a["assessed_share"] is not None else None, a["union_is_floor"])]
    for r in a["rows"]:
        if r["assessed"]:
            lines.append("    assessed    p=%.2f  %s" % (r["p"], r["name"]))
        else:
            lines.append("    unassessed  assumed_stable=%s handling=%s bound=%s  %s" % (r["assumed_stable"], r["handling"], r["bound"], r["name"]))
    u = a["union"]
    if u:
        lines.append("  union of the %d assessed failures: independent %.4f  perfect-positive %.2f  mutually-exclusive %.2f  band %s" % (
            u["n"], u["independent"], u["perfect_positive"], u["mutually_exclusive"], u["band"]))
    lines.append("  factor of safety, designed to the anticipated threat exactly: %s" % factor_of_safety(1.0, 1.0))
    lines.append("  reading: the number is a floor over the assessed subset; the unassessed factors enter no")
    lines.append("           arithmetic and the verdict turns on whether each declares a structural handling")
    return "\n".join(lines)


def main(argv):
    if "--selftest" in argv:
        print("load_class.py refuses --selftest; run: python3 selftest.py")
        return 2
    print(render())
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
