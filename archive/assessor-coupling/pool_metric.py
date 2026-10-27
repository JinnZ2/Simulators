"""WO-6 step 1, the pool-level independence metric, as arithmetic on a
CONSTRUCTED funding graph.

The order: what fraction of an assessor's funding originates from sources
that also fund, hold equity in, or are governed by parties holding equity
in, the assessed sector. Applied to ALL assessors in a field; the output
is a DISTRIBUTION, not an accusation.

Graph schema (every node an opaque id, no node a real party):
  sources:   {id: {"funds": {assessor_id: amount, ...}}}
  sector:    {"funded_by": [source ids], "equity_held_by": [source ids]}
  governance:{source_id: [ids of parties on its board]}   (second order)
An edge LABEL (grant / contract / fellowship / donation / salary) is
carried on the record and read by NOTHING: the order's structural claim
is that relabeling an outflow changes no coupling, and the metric shows
it as an invariance rather than stating it.

Real 990s and grant databases are egress-blocked (EGRESS below, measured).
Library module: refuses --selftest; the suite is selftest.py.
"""
import json
import sys

EGRESS = {"measured": "2026-09-19T22:00Z",
          "hosts": {"projects.propublica.org:443": "CONNECT 403",
                    "apps.irs.gov:443": "CONNECT 403",
                    "www.grants.gov:443": "CONNECT 403",
                    "github.com:443": "connects (control)"}}
GOVERNANCE_DEPTH = 2   # [CHOICE 1] second-order coupling followed two hops through boards
COUPLINGS = ("funds_sector", "holds_equity", "governed_by_equity_holder")


def coupled(source, sector, governance, depth=GOVERNANCE_DEPTH, _seen=None):
    """Which of the three couplings a funding source carries to the
    assessed sector. Empty tuple = none found; the label carries nothing."""
    _seen = _seen or set()
    out = []
    if source in sector.get("funded_by", []):
        out.append("funds_sector")
    if source in sector.get("equity_held_by", []):
        out.append("holds_equity")
    if depth > 0 and source not in _seen:
        for board in governance.get(source, []):
            if board in sector.get("equity_held_by", []) or coupled(board, sector, governance, depth - 1, _seen | {source}):
                out.append("governed_by_equity_holder")
                break
    return tuple(out)


def assessor_fraction(assessor, sources, sector, governance):
    """Fraction of one assessor's funding from coupled sources. None when
    the assessor has no recorded funding (absent, never 0); UNDECLARED
    when a source funds it with an undeclared amount."""
    total = 0.0
    coupled_amt = 0.0
    paths = {}
    for sid, src in sources.items():
        if assessor not in src.get("funds", {}):
            continue
        amt = src["funds"][assessor]
        if amt is None:
            return {"state": "UNDECLARED", "why": "source %s funds the assessor with an undeclared amount" % sid}
        total += amt
        c = coupled(sid, sector, governance)
        if c:
            coupled_amt += amt
            paths[sid] = c
    if total == 0.0:
        return {"state": "NO_RECORDED_FUNDING", "fraction": None}
    return {"state": "MEASURED", "fraction": round(coupled_amt / total, 6), "total": total, "paths": paths}


def field_distribution(field):
    """The metric over EVERY assessor in a field, sorted, no names ranked:
    the output is the sorted list of fractions plus the count of
    unmeasurable assessors, kept apart."""
    res = {a: assessor_fraction(a, field["sources"], field["sector"], field.get("governance", {}))
           for a in field["assessors"]}
    measured = sorted(r["fraction"] for r in res.values() if r["state"] == "MEASURED")
    return {"n_assessors": len(field["assessors"]), "measured": len(measured),
            "no_recorded_funding": sum(1 for r in res.values() if r["state"] == "NO_RECORDED_FUNDING"),
            "undeclared": sum(1 for r in res.values() if r["state"] == "UNDECLARED"),
            "distribution": measured, "per_assessor": res}


def relabel(field, label):
    """Rewrite every funding edge's label. The metric must not move."""
    out = json.loads(json.dumps(field))
    for src in out["sources"].values():
        src["label"] = label
    return out


def constructed_fields():
    """Three constructed fields, answers known in advance. No node is a
    real party."""
    single_pool = {"source": "CONSTRUCTED",
                   "assessors": ["A1", "A2", "A3"],
                   "sources": {"P": {"label": "grant", "funds": {"A1": 10, "A2": 5, "A3": 20}}},
                   "sector": {"funded_by": ["P"], "equity_held_by": []},
                   "governance": {}}
    disjoint = {"source": "CONSTRUCTED",
                "assessors": ["A1", "A2"],
                "sources": {"S1": {"label": "contract", "funds": {"A1": 10}},
                            "S2": {"label": "salary", "funds": {"A2": 7}}},
                "sector": {"funded_by": ["X"], "equity_held_by": ["Y"]},
                "governance": {}}
    mixed = {"source": "CONSTRUCTED",
             "assessors": ["A1", "A2", "A3", "A4"],
             "sources": {"S1": {"label": "grant", "funds": {"A1": 6, "A2": 2}},
                         "S2": {"label": "donation", "funds": {"A1": 4, "A3": 9}},
                         "S3": {"label": "fellowship", "funds": {"A2": 8}},
                         "S4": {"label": "contract", "funds": {"A4": None}}},
             "sector": {"funded_by": ["S1"], "equity_held_by": ["E"]},
             "governance": {"S2": ["E"]}}
    return {"single_pool": single_pool, "disjoint": disjoint, "mixed": mixed}


def render(fields=None):
    fields = fields or constructed_fields()
    lines = ["pool_metric -- WO-6 step 1, pool-level independence as arithmetic on CONSTRUCTED graphs",
             "  record hosts, measured %s: %s" % (EGRESS["measured"], "; ".join("%s %s" % kv for kv in EGRESS["hosts"].items())),
             "  governance depth %d is [CHOICE 1]; every field CONSTRUCTED; no node is a real party" % GOVERNANCE_DEPTH]
    for name, f in fields.items():
        d = field_distribution(f)
        lines.append("  %-12s assessors %d  measured %d  no_funding %d  undeclared %d  distribution %s"
                     % (name, d["n_assessors"], d["measured"], d["no_recorded_funding"], d["undeclared"], d["distribution"]))
        for a, r in d["per_assessor"].items():
            if r["state"] == "MEASURED":
                lines.append("      %-3s %.3f  via %s" % (a, r["fraction"], {k: "+".join(v) for k, v in r["paths"].items()} or "no coupled source"))
            else:
                lines.append("      %-3s %s" % (a, r["state"]))
        rl = field_distribution(relabel(f, "salary"))["distribution"]
        lines.append("      relabel every edge 'salary': distribution %s  moved=%s" % (rl, rl != d["distribution"]))
    lines.append("  reading: the label on the pipe enters no arithmetic, so relabeling an outflow moves no")
    lines.append("           fraction -- 'a pool cannot audit itself by relabeling its outflows' as an invariance.")
    lines.append("           Nothing here is a fraction for any real assessor; the records are not reachable.")
    return "\n".join(lines)


def main(argv):
    if "--selftest" in argv:
        sys.stderr.write("pool_metric.py is a library; run python3 selftest.py\n")
        return 2
    fields = None
    if "--field" in argv:
        f = json.load(open(argv[argv.index("--field") + 1]))
        fields = {"supplied": f}
    print(render(fields))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
