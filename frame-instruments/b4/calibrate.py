"""B4.7 calibrate.py -- documented arm only. Compare each reconstructor's
requirement list against the causal factors the investigating body named.

factors.jsonl:        item_id, factor_id, factor_text, report_source
factor_matches.jsonl: item_id, factor_id, req, matched   (req = reconstructor_id/req_id)
Matching factor<->requirement is external; --match-source records it.

Per (item, reconstructor):
  recovered      factors with >= 1 matched requirement from this reconstructor
  missed         factors with none
  beyond_report  this reconstructor's requirements matched to no factor
                 -- printed, NOT scored as error, left uninterpreted.
An items file carrying any non-documented item -> void.

Command: python3 calibrate.py REQS.jsonl --items ITEMS_VALID.jsonl --factors FACTORS.jsonl \
             --factor-matches FMATCHES.jsonl --match-source "who/what" --out CALIB.jsonl
"""
import sys

from common import (parse_argv, usage_exit, REQ_FIELDS, Invalid, Run, Void, check_fields, finish,
                    parse_ref, raise_if, read_jsonl, ref, write_jsonl)

FACTOR_FIELDS = ("item_id", "factor_id", "factor_text", "report_source")
FM_FIELDS = ("item_id", "factor_id", "req", "matched")


def calibrate(rows, items, factors, fmatches, match_source):
    probs = []
    arms = sorted(set(i.get("arm") for i in items))
    if arms != ["documented"]:
        raise Void("calibration runs only on the documented arm; items carry %s" % arms)
    item_ids = set(i["item_id"] for i in items)
    for n, r in enumerate(rows, 1):
        probs += check_fields(r, REQ_FIELDS, "req row %d" % n, exact=False)
    for n, f in enumerate(factors, 1):
        probs += check_fields(f, FACTOR_FIELDS, "factor row %d" % n)
    raise_if(probs)
    reqs = {(r["item_id"], ref(r["reconstructor_id"], r["req_id"])): r for r in rows}
    facs = {(f["item_id"], f["factor_id"]): f for f in factors}
    for k in list(reqs) + list(facs):
        if k[0] not in item_ids:
            probs.append("item_id %r not in items file" % k[0])
    hit_f, hit_r = {}, set()
    for n, m in enumerate(fmatches, 1):
        where = "factor-match row %d" % n
        p = check_fields(m, FM_FIELDS, where)
        if p:
            probs += p
            continue
        if not isinstance(m["matched"], bool):
            probs.append("%s: matched must be true/false" % where)
        if (m["item_id"], m["factor_id"]) not in facs:
            probs.append("%s: unknown factor %r under item %r" % (where, m["factor_id"], m["item_id"]))
        if (m["item_id"], m["req"]) not in reqs:
            probs.append("%s: unknown requirement %r under item %r" % (where, m["req"], m["item_id"]))
        if probs:
            continue
        if m["matched"]:
            rid = parse_ref(m["req"])[0]
            hit_f.setdefault((m["item_id"], m["factor_id"]), set()).add(rid)
            hit_r.add((m["item_id"], m["req"]))
    raise_if(probs)
    out = []
    for item in sorted(item_ids):
        recs = sorted(set(k[1].split("/")[0] for k in reqs if k[0] == item))
        item_facs = sorted(fid for (iid, fid) in facs if iid == item)
        for rid in recs:
            mine = sorted(k[1] for k in reqs if k[0] == item and k[1].startswith(rid + "/"))
            rec_ = [f for f in item_facs if rid in hit_f.get((item, f), ())]
            miss = [f for f in item_facs if f not in rec_]
            beyond = [q for q in mine if (item, q) not in hit_r]
            out.append({"item_id": item, "reconstructor_id": rid,
                        "n_factors_named": len(item_facs), "n_requirements": len(mine),
                        "recovered": rec_, "n_recovered": len(rec_),
                        "missed": miss, "n_missed": len(miss),
                        "beyond_report": beyond, "n_beyond_report": len(beyond),
                        "beyond_report_note": "printed, not scored as error, left uninterpreted",
                        "report_source": sorted(set(facs[(item, f)]["report_source"] for f in item_facs)),
                        "match_source": match_source})
    return out


def main(argv=None):
    try:
        a = parse_argv(argv, __doc__, positional=("requirements",), options=("items", "factors", "factor_matches", "match_source", "out", "runs"), required=("items", "factors", "factor_matches", "match_source", "out"))
    except Invalid as e:
        return usage_exit(e)
    if a is None:
        return 0
    ins = [a.requirements, a.items, a.factors, a.factor_matches]
    with Run("b4/calibrate.py", vars(a), None, ins, a.out, a.runs) as run:
        try:
            if not a.match_source.strip():
                raise Invalid("--match-source must be non-empty")
            rows = read_jsonl(a.requirements)
            if not rows:
                return finish(run, "empty", {"requirements": 0})
            out = calibrate(rows, read_jsonl(a.items), read_jsonl(a.factors),
                            read_jsonl(a.factor_matches), a.match_source)
        except Invalid as e:
            return finish(run, "error", notes=str(e))
        except Void as e:
            return finish(run, "void", notes=str(e))
        write_jsonl(a.out, out)
        return finish(run, "ok", {k: sum(o[k] for o in out) for k in
                                  ("n_recovered", "n_missed", "n_beyond_report")})


if __name__ == "__main__":
    sys.exit(main())
