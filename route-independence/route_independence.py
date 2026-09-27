# SPDX-License-Identifier: CC0-1.0
"""route_independence.py -- two measures, not one.

FWO-2. Counting alternative routes to a need overstates independence when
every route must discharge its external obligations in one medium. This
instrument returns the route count AND, per route, whether the route can
settle its own obligations in its own medium. It merges nothing.

INPUT   routes.txt
    dominant: TOKEN                      required header
    need | route | settles_in | obligation_medium | permitted | source

    settles_in          the medium the route's own exchanges use
    obligation_medium   the medium its external obligations are paid in
                        (UNKNOWN is a value)
    permitted           yes | no | UNKNOWN. Carried through to the output
                        as its own field. It reaches no measure: a route
                        can be permitted and still unable to discharge
                        its obligations in its own medium, and a tool
                        that folded the two together would reproduce
                        the error it exists to catch (TEST OF THE TEST).
    source              empty -> the row is printed SYNTHETIC

PER ROUTE
    discharges_own_obligations
        True     settles_in == obligation_medium and obligation_medium
                 is not the dominant token
        False    either condition fails on stated media
        None     a medium is UNKNOWN; reported as UNKNOWN, never as False

PER NEED
    route_count          distinct routes
    independent_count    a point when every route is decided, else a band
                         [min, max] with UNKNOWN routes counted at the top
    independence_ratio   independent_count / route_count, point or band;
                         NOT_EVALUABLE when route_count == 0
    flag
        ENCLOSED_PLURALITY   route_count >= 2 and independent_count == 0
                             (certain: the band's max is 0)
        NOT_ENCLOSED         independent_count >= 1 (certain)
        SINGLE_ROUTE         route_count == 1
        UNKNOWN              the band straddles 0 and the flag cannot be read
        NOT_EVALUABLE        route_count == 0

CROSS-CHECK (prior instrument, imported not copied)
    effective-redundancy-audit/effective_redundancy.py already computes
    N_eff over channels sharing a node. Here the shared node is the
    obligation medium, and ENCLOSED_PLURALITY is that instrument's
    `n_nominal >= 2 and n_eff == 1` with the coder's boolean DERIVED from
    two stated fields instead of declared. The cross-check reports whether
    the two readings agree; when the sibling module is not beside this
    folder (a promoted copy), it reports PRIOR_ART_NOT_IMPORTED.

DERIVED note carried from the work order: household production is
genuinely outside but cannot scale or specialize; the boundary sits around
COORDINATION, not subsistence. Under this instrument's own rule the
household-production row reads NOT independent wherever a dollar-
denominated obligation attaches to it (property tax on held land), so
"genuinely outside" holds only where no such obligation attaches. That
tension is reported, not resolved.
"""

import importlib.util
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

ENCLOSED_PLURALITY = "ENCLOSED_PLURALITY"
NOT_ENCLOSED = "NOT_ENCLOSED"
SINGLE_ROUTE = "SINGLE_ROUTE"
UNKNOWN = "UNKNOWN"
NOT_EVALUABLE = "NOT_EVALUABLE"
FLAGS = (ENCLOSED_PLURALITY, NOT_ENCLOSED, SINGLE_ROUTE, UNKNOWN, NOT_EVALUABLE)

PERMITTED_VALUES = ("yes", "no", "UNKNOWN")

CHOICES = {
    1: "an UNKNOWN medium puts the route in the top of the independent band "
       "and never in the bottom; the flag is UNKNOWN when the band straddles 0",
    2: "media are compared as case-insensitive strings after stripping; two "
       "spellings of one medium read as two media (a word-list limit, stated)",
    3: "the prior-art cross-check is imported by file path from the sibling "
       "folder and reports PRIOR_ART_NOT_IMPORTED when absent",
}


def parse_routes(text):
    """Returns (dominant, rows, refusals)."""
    dominant = None
    rows = []
    refusals = []
    seen = set()
    for lineno, raw in enumerate(text.splitlines(), 1):
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        if line.lower().startswith("dominant:"):
            dominant = line.split(":", 1)[1].strip()
            continue
        parts = [p.strip() for p in line.split("|")]
        if len(parts) < 5:
            refusals.append(("MALFORMED_ROW", "line %d: %r" % (lineno, raw.strip())))
            continue
        need, route, settles, oblig, permitted = parts[:5]
        source = parts[5] if len(parts) > 5 else ""
        if permitted not in PERMITTED_VALUES:
            refusals.append(("INVALID_PERMITTED",
                             "line %d: %r not in %s" % (lineno, permitted, "/".join(PERMITTED_VALUES))))
            continue
        key = (need, route)
        if key in seen:
            refusals.append(("DUPLICATE_ROUTE", "%s / %s" % key))
            continue
        seen.add(key)
        rows.append({
            "need": need, "route": route,
            "settles_in": settles, "obligation_medium": oblig,
            "permitted": permitted,
            "source": source,
            "sourced": bool(source) and source.upper() != "SYNTHETIC",
            "line": lineno,
        })
    if dominant is None:
        refusals.append(("DOMINANT_UNDECLARED", "no `dominant:` header"))
    return dominant, rows, refusals


def load(path):
    with open(path, "r", encoding="utf-8") as handle:
        return parse_routes(handle.read())


def _norm(medium):
    return medium.strip().lower()


def discharges_own_obligations(settles_in, obligation_medium, dominant):
    """True / False / None. None when a medium is UNKNOWN."""
    if _norm(settles_in) == "unknown" or _norm(obligation_medium) == "unknown":
        return None
    return _norm(settles_in) == _norm(obligation_medium) and \
        _norm(obligation_medium) != _norm(dominant)


def independence_ratio(independent_count, route_count):
    """independent_count / route_count; None (NOT_EVALUABLE) when route_count == 0.

    Registered in tools/known_answer.py. None is not 0.0: a need with no
    routes has no independence to measure, and 0.0 would read as
    'measured, and none of them settle'.
    """
    if route_count == 0:
        return None
    return independent_count / float(route_count)


def flag_for(route_count, independent_min, independent_max):
    """The per-need flag from three counts. Reads no route field."""
    if route_count == 0:
        return NOT_EVALUABLE
    if route_count == 1:
        return SINGLE_ROUTE
    if independent_max == 0:
        return ENCLOSED_PLURALITY
    if independent_min >= 1:
        return NOT_ENCLOSED
    return UNKNOWN


def measure_need(rows, dominant):
    """Measures for one need's rows."""
    per_route = []
    certain = 0
    unknown = 0
    for r in rows:
        d = discharges_own_obligations(r["settles_in"], r["obligation_medium"], dominant)
        if d is None:
            unknown += 1
        elif d:
            certain += 1
        per_route.append({
            "route": r["route"],
            "settles_in": r["settles_in"],
            "obligation_medium": r["obligation_medium"],
            "discharges_own_obligations": d,
            "permitted": r["permitted"],
            "sourced": r["sourced"],
        })
    n = len(rows)
    lo, hi = certain, certain + unknown
    flag = flag_for(n, lo, hi)
    if lo == hi:
        ind_count = lo
        ratio = independence_ratio(lo, n)
    else:
        ind_count = (lo, hi)
        ratio = (independence_ratio(lo, n), independence_ratio(hi, n))
    return {
        "route_count": n,
        "independent_count": ind_count,
        "independence_ratio": ratio,
        "unknown_routes": [p["route"] for p in per_route
                           if p["discharges_own_obligations"] is None],
        "flag": flag,
        "routes": per_route,
        "synthetic_routes": [p["route"] for p in per_route if not p["sourced"]],
    }


def measure(rows, dominant):
    needs = []
    for r in rows:
        if r["need"] not in needs:
            needs.append(r["need"])
    return dict((need, measure_need([r for r in rows if r["need"] == need], dominant))
                for need in needs)


# ------------------------------------------------------------ prior art

def _load_prior_art():
    path = os.path.join(HERE, "..", "effective-redundancy-audit", "effective_redundancy.py")
    if not os.path.exists(path):
        return None
    spec = importlib.util.spec_from_file_location("effective_redundancy", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def cross_check(need_result):
    """Does the prior instrument's N_eff reading agree with the flag?

    Routes with an UNKNOWN medium cannot be coded as a boolean for the
    prior instrument, so the cross-check is NOT_EVALUABLE on a need with
    any; it never guesses a side.
    """
    mod = _load_prior_art()
    if mod is None:
        return {"status": "PRIOR_ART_NOT_IMPORTED",
                "detail": "effective-redundancy-audit/effective_redundancy.py not beside this folder"}
    if need_result["unknown_routes"]:
        return {"status": "NOT_EVALUABLE",
                "detail": "UNKNOWN routes cannot be coded as a boolean for n_eff: "
                          + ", ".join(need_result["unknown_routes"])}
    channels = [mod.Channel(p["route"], bool(p["discharges_own_obligations"]))
                for p in need_result["routes"]]
    case = mod.Case("need", "route", "held", set(), channels)
    prior_enclosed = case.n_nominal >= 2 and case.n_eff == 1
    here_enclosed = need_result["flag"] == ENCLOSED_PLURALITY
    return {"status": "AGREE" if prior_enclosed == here_enclosed else "DISAGREE",
            "n_nominal": case.n_nominal, "n_eff": case.n_eff,
            "prior_reads_enclosed": prior_enclosed, "here_reads_enclosed": here_enclosed}


# ------------------------------------------------------------ render

def _fmt(v):
    if v is None:
        return "NOT_EVALUABLE"
    if isinstance(v, tuple):
        return "[%s, %s]" % (_fmt(v[0]), _fmt(v[1]))
    if isinstance(v, float):
        return "%.3f" % v
    return str(v)


def render(results, dominant, with_cross_check=True):
    lines = ["dominant token: %s" % dominant, ""]
    for need, res in results.items():
        lines.append("need: %s" % need)
        for p in res["routes"]:
            d = p["discharges_own_obligations"]
            dtxt = "UNKNOWN" if d is None else ("settles" if d else "does not settle")
            flags = [] if p["sourced"] else ["SYNTHETIC"]
            lines.append("  %-22s settles_in=%-18s obligation=%-12s permitted=%-7s %-16s %s" % (
                p["route"], p["settles_in"], p["obligation_medium"], p["permitted"],
                dtxt, " ".join(flags)))
        lines.append("  route_count=%d  independent_count=%s  independence_ratio=%s  flag=%s" % (
            res["route_count"], _fmt(res["independent_count"]),
            _fmt(res["independence_ratio"]), res["flag"]))
        if res["unknown_routes"]:
            lines.append("  unknown medium on: %s" % ", ".join(res["unknown_routes"]))
        if with_cross_check:
            cc = cross_check(res)
            if cc["status"] in ("AGREE", "DISAGREE"):
                lines.append("  prior-art cross-check (effective_redundancy n_eff): %s  n_nominal=%d n_eff=%d"
                             % (cc["status"], cc["n_nominal"], cc["n_eff"]))
            else:
                lines.append("  prior-art cross-check: %s (%s)" % (cc["status"], cc["detail"]))
        lines.append("")
    lines.append("scope: `permitted` is carried and reaches no measure. A route can be")
    lines.append("       permitted and still unable to discharge its obligations in its")
    lines.append("       own medium; the two are separate fields on every row above.")
    lines.append("       Every named source is carried, not read, in this build.")
    return "\n".join(lines)


def render_refusals(refusals):
    lines = ["not evaluated, %d refusal(s)" % len(refusals)]
    for kind, detail in refusals:
        lines.append("  %-20s %s" % (kind, detail))
    return "\n".join(lines)


def main(argv):
    args = argv[1:]
    if args == ["--choices"]:
        for k in sorted(CHOICES):
            print("[CHOICE %d] %s" % (k, CHOICES[k]))
        return 0
    if args == ["--selftest"]:
        sys.stderr.write("library module; run: python3 route-independence/test_route.py\n")
        return 2
    if len(args) != 1:
        sys.stderr.write("usage: route_independence.py ROUTES.txt | --choices\n")
        return 2
    dominant, rows, refusals = load(args[0])
    if refusals:
        print(render_refusals(refusals))
        return 2
    print(render(measure(rows, dominant), dominant))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
