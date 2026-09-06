"""B1 nulls N1-N5 from workorders/runner_up_trace.md section 7, each
evaluated to a number and a triggered flag. Not a command; imported by
report.py. Every threshold is an argument and is printed with the result.

  N1  separations land only on wording: resync high at every D
  N2  every traced (high-entropy) position separates at D >= sustained_d
  N3  results depend on D or N: adjacent-D / adjacent-L top-decile Jaccard
      low; N is not carried in separations.jsonl and is not evaluable here
  N4  permuted run clusters as well as the real run: permuted stability >=
      real stability; the permuted values are the transfer function
  N5  top-k truncation changes the entropy ordering: needs base rows under
      both entropy bases for the same positions
A null that cannot be evaluated from the inputs says so; it is never
reported as not triggered.
"""
import itertools

from ficommon import mean

DEFAULTS = {"n1_resync": 0.9, "n2_separate": 0.95, "n3_jaccard": 0.5, "n5_discordance": 0.1, "sustained_d": 64}


def _cells(summary):
    return [s for s in summary if "n_rows" in s]


def _stab(summary, axis):
    return [s for s in summary if s.get("sweep_axis") == axis and s["jaccard"] is not None]


def n1(summary, thr):
    per_L = {}
    for c in _cells(summary):
        per_L.setdefault(c["L"], []).append(c["resync_rate"])
    mins = {L: min(v) for L, v in per_L.items()}
    trig = bool(mins) and all(v >= thr for v in mins.values())
    return {"id": "N1", "number": {"min_resync_over_D_per_L": mins}, "threshold": thr, "triggered": trig,
            "note": "triggered when the minimum resync rate over D is >= threshold at every L"}


def n2(seps, thr, sustained_d):
    per_L = {}
    for r in seps:
        if r["D"] >= sustained_d:
            per_L.setdefault(r["L"], {}).setdefault((r["case_id"], r["model_id"], r["i"], r["branch_rank"]), []).append(r["resync_D"])
    rates = {L: round(mean(all(v == 0 for v in vals) for vals in pos.values()), 4) for L, pos in per_L.items()}
    if not rates:
        return {"id": "N2", "number": None, "threshold": thr, "triggered": None,
                "note": "no rows at D >= %d; not evaluable" % sustained_d}
    return {"id": "N2", "number": {"separation_rate_at_D>=%d_per_L" % sustained_d: rates}, "threshold": thr,
            "triggered": all(v >= thr for v in rates.values()),
            "note": "separates = resync 0 at every D >= %d; triggered when the rate is >= threshold at every L" % sustained_d}


def n3(summary, thr):
    d, l = _stab(summary, "D"), _stab(summary, "L")
    num = {"min_adjacent_D_jaccard": min(s["jaccard"] for s in d) if d else None,
           "min_adjacent_L_jaccard": min(s["jaccard"] for s in l) if l else None, "N": "not carried"}
    trig = None if not d else (num["min_adjacent_D_jaccard"] < thr or (l and num["min_adjacent_L_jaccard"] < thr))
    return {"id": "N3", "number": num, "threshold": thr, "triggered": trig,
            "note": "triggered when any adjacent-D or adjacent-L top-decile Jaccard is < threshold; "
                    "the N sweep (stage B) is not in separations.jsonl and is compared across runs at different N"}


def n4(real, perm):
    rd, pd = _stab(real, "D"), _stab(perm, "D")
    num = {"mean_adjacent_D_jaccard_real": round(mean(s["jaccard"] for s in rd), 4) if rd else None,
           "mean_adjacent_D_jaccard_permuted": round(mean(s["jaccard"] for s in pd), 4) if pd else None,
           "transfer_function_permuted": [{"model_id": s["model_id"], "held": s["held"], "from": s["from"],
                                           "to": s["to"], "jaccard": s["jaccard"]} for s in pd]}
    trig = None if (not rd or not pd) else num["mean_adjacent_D_jaccard_permuted"] >= num["mean_adjacent_D_jaccard_real"]
    return {"id": "N4", "number": num, "threshold": "permuted >= real", "triggered": trig,
            "note": "the permuted stability values are the method's transfer function and are printed either way"}


def n5(base_rows, thr):
    if base_rows is None:
        return {"id": "N5", "number": None, "threshold": thr, "triggered": None,
                "note": "no --base supplied; k sensitivity not evaluable"}
    by = {}
    for r in base_rows:
        by.setdefault((r["case_id"], r["model_id"], r["i"]), {})[r["entropy_basis"]] = r["entropy_i"]
    bases = sorted(set(b for v in by.values() for b in v))
    both = {k: v for k, v in by.items() if "full" in v and "topk" in v}
    if len(both) < 2:
        return {"id": "N5", "number": {"entropy_bases_present": bases, "positions_with_both": len(both)},
                "threshold": thr, "triggered": None,
                "note": "requires >= 2 positions carrying entropy under both bases; not evaluable"}
    pairs = list(itertools.combinations(sorted(both), 2))
    disc = sum(1 for a, b in pairs if (both[a]["full"] - both[b]["full"]) * (both[a]["topk"] - both[b]["topk"]) < 0)
    frac = round(disc / float(len(pairs)), 4)
    return {"id": "N5", "number": {"discordant_pair_fraction": frac, "positions_with_both": len(both)},
            "threshold": thr, "triggered": frac > thr,
            "note": "fraction of position pairs whose entropy ordering flips between full and top-k"}


def evaluate(seps, real, perm, base_rows, thr):
    return [n1(real, thr["n1_resync"]), n2(seps, thr["n2_separate"], thr["sustained_d"]),
            n3(real, thr["n3_jaccard"]), n4(real, perm), n5(base_rows, thr["n5_discordance"])]
