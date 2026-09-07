"""B1.4 summarise.py -- runs identically on the real and the permuted
file; no branching on which it got.

Per (D, L, model_id): n_rows, mean_div, resync_rate, top-decile count and
the top-decile position set (position = case_id/i/branch_rank; top decile
= the ceil(n/10) rows with the largest div_D, PLUS every row tied with the
cutoff value, so a saturated stratum reports the whole stratum and
n_tied_at_cutoff says so), and the separation set (positions with
resync_D == 0, the readout that depends on L).
STABILITY rows: Jaccard overlap between adjacent D at fixed L and adjacent
L at fixed D, for BOTH position sets (position_set = top_decile_div |
separation_resync0). div_D does not depend on L, so the top-decile set is
identical across L by construction; the separation set is what moves.
Summary rows carry n_rows; stability rows carry sweep_axis. One file.

Command: python3 summarise.py SEPARATIONS.jsonl --out SUMMARY.jsonl
"""
import math
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ficommon import Invalid, Run, check_fields, finish, mean, parse_argv, raise_if, read_jsonl, usage_exit, write_jsonl  # noqa: E402

NEEDED = ("case_id", "model_id", "i", "branch_rank", "D", "L", "ent_i", "gap_i", "resync_D", "div_D")


def pos(r):
    return "%s/%s/%s" % (r["case_id"], r["i"], r["branch_rank"])


def top_decile(rows):
    """ceil(n/10) rows by div_D descending, plus every row tied at the cutoff."""
    k = max(1, int(math.ceil(len(rows) / 10.0)))
    ranked = sorted(rows, key=lambda r: (-r["div_D"], pos(r)))
    cutoff = ranked[k - 1]["div_D"]
    chosen = [r for r in ranked if r["div_D"] >= cutoff]
    return sorted(set(pos(r) for r in chosen)), len(chosen) - k


def separation_set(rows):
    return sorted(set(pos(r) for r in rows if r["resync_D"] == 0))


def jaccard(a, b):
    a, b = set(a), set(b)
    u = a | b
    return round(len(a & b) / float(len(u)), 4) if u else None


def summarise(rows):
    probs = []
    for n, r in enumerate(rows, 1):
        probs += check_fields(r, NEEDED, "row %d" % n, exact=False)
    raise_if(probs)
    cells = {}
    for r in rows:
        cells.setdefault((r["model_id"], r["D"], r["L"]), []).append(r)
    summary, sets = [], {"top_decile_div": {}, "separation_resync0": {}}
    for (m, D, L) in sorted(cells):
        sub = cells[(m, D, L)]
        t, tied = top_decile(sub)
        sep = separation_set(sub)
        sets["top_decile_div"][(m, D, L)], sets["separation_resync0"][(m, D, L)] = t, sep
        summary.append({"model_id": m, "D": D, "L": L, "n_rows": len(sub),
                        "n_positions": len(set(pos(r) for r in sub)),
                        "mean_div": round(mean(r["div_D"] for r in sub), 6),
                        "resync_rate": round(mean(r["resync_D"] for r in sub), 6),
                        "mean_ent": round(mean(r["ent_i"] for r in sub), 6),
                        "mean_gap": round(mean(r["gap_i"] for r in sub), 6),
                        "top_decile_count": len(t), "n_tied_at_cutoff": tied, "top_decile_positions": t,
                        "separation_count": len(sep), "separation_positions": sep})
    models = sorted(set(k[0] for k in cells))
    Ds = sorted(set(k[1] for k in cells))
    Ls = sorted(set(k[2] for k in cells))
    stability = []
    for kind, top in sets.items():
        for m in models:
            for L in Ls:
                for d1, d2 in zip(Ds, Ds[1:]):
                    if (m, d1, L) in top and (m, d2, L) in top:
                        stability.append({"model_id": m, "position_set": kind, "sweep_axis": "D", "held": {"L": L},
                                          "from": d1, "to": d2, "jaccard": jaccard(top[(m, d1, L)], top[(m, d2, L)])})
            for D in Ds:
                for l1, l2 in zip(Ls, Ls[1:]):
                    if (m, D, l1) in top and (m, D, l2) in top:
                        stability.append({"model_id": m, "position_set": kind, "sweep_axis": "L", "held": {"D": D},
                                          "from": l1, "to": l2, "jaccard": jaccard(top[(m, D, l1)], top[(m, D, l2)])})
    return summary + stability


def main(argv=None):
    try:
        a = parse_argv(argv, __doc__, positional=("separations",), options=("out", "runs"), required=("out",))
    except Invalid as e:
        return usage_exit(e)
    if a is None:
        return 0
    with Run("b1/summarise.py", vars(a), None, [a.separations], a.out, a.runs) as run:
        try:
            rows = read_jsonl(a.separations)
            if not rows:
                return finish(run, "empty", {"rows": 0})
            out = summarise(rows)
        except Invalid as e:
            return finish(run, "error", notes=str(e))
        write_jsonl(a.out, out)
        return finish(run, "ok", {"cells": sum(1 for o in out if "n_rows" in o),
                                  "stability_rows": sum(1 for o in out if "sweep_axis" in o)})


if __name__ == "__main__":
    sys.exit(main())
