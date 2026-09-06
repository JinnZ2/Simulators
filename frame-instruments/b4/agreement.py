"""B4.5 agreement.py -- agreement across reconstructors from an external
matches file. Does no matching itself.

The work order says this wraps B2's agree.py plus one field. B2 is not in
this tree (see ../BUILD_NOTES.md), so the B4.5 computation is implemented
here directly with the one field, `match_source`, on every row. When B2
lands, the intended form is a wrap and this body is what it must reproduce.

matches.jsonl: item_id, req_a, req_b, matched   (req = reconstructor_id/req_id)
Both refs must exist under item_id and belong to different reconstructors.

Per item:
  pairs            for each reconstructor pair (A,B): agreement =
                   (A reqs with a counterpart in B + B reqs with one in A)
                   / (|A| + |B|); 0 when no link; one-to-many links count
                   each requirement once.
  full_disagreement_pairs   pairs with agreement 0
  singletons       requirements with no matched link to ANY other
                   reconstructor -- printed in full, never dropped.
Items with one reconstructor: pairs empty, agreement null, singletons = all.

Command: python3 agreement.py REQS.jsonl --matches MATCHES.jsonl --match-source "who/what" --out AGREE.jsonl
"""
import argparse
import itertools
import sys

from common import (MATCH_FIELDS, REQ_FIELDS, Invalid, Run, check_fields,
                    finish, parse_ref, raise_if, read_jsonl, ref, write_jsonl)

DEFINITION = ("agreement(A,B) = (#A with counterpart in B + #B with counterpart in A) / (|A|+|B|); "
              "counterpart = a matched=true row in matches.jsonl")


def index(rows):
    by_item = {}
    for r in rows:
        by_item.setdefault(r["item_id"], {})[ref(r["reconstructor_id"], r["req_id"])] = r
    return by_item


def links(matches, by_item):
    """{item: set of frozenset({ref_a, ref_b})} for matched rows, validated."""
    probs, out = [], {}
    for n, m in enumerate(matches, 1):
        where = "match row %d" % n
        p = check_fields(m, MATCH_FIELDS, where)
        if p:
            probs += p
            continue
        if not isinstance(m["matched"], bool):
            probs.append("%s: matched must be true/false" % where)
            continue
        reqs = by_item.get(m["item_id"], {})
        for k in ("req_a", "req_b"):
            if m[k] not in reqs:
                probs.append("%s: %s %r not under item %r" % (where, k, m[k], m["item_id"]))
        if probs:
            continue
        if parse_ref(m["req_a"])[0] == parse_ref(m["req_b"])[0]:
            probs.append("%s: both refs belong to one reconstructor" % where)
            continue
        if m["matched"]:
            out.setdefault(m["item_id"], set()).add(frozenset((m["req_a"], m["req_b"])))
    raise_if(probs)
    return out


def score(rows, matches, match_source):
    probs = []
    for n, r in enumerate(rows, 1):
        probs += check_fields(r, REQ_FIELDS, "row %d" % n, exact=False)
    raise_if(probs)
    by_item = index(rows)
    linked = links(matches, by_item)
    out = []
    for item in sorted(by_item):
        reqs = by_item[item]
        recs = sorted(set(parse_ref(k)[0] for k in reqs))
        by_rec = {rid: [k for k in reqs if parse_ref(k)[0] == rid] for rid in recs}
        item_links = linked.get(item, set())
        partner = {}
        for pair in item_links:
            a, b = tuple(pair)
            partner.setdefault(a, set()).add(parse_ref(b)[0])
            partner.setdefault(b, set()).add(parse_ref(a)[0])
        pairs = []
        for a_id, b_id in itertools.combinations(recs, 2):
            na, nb = len(by_rec[a_id]), len(by_rec[b_id])
            ca = sum(1 for k in by_rec[a_id] if b_id in partner.get(k, ()))
            cb = sum(1 for k in by_rec[b_id] if a_id in partner.get(k, ()))
            pairs.append({"a": a_id, "b": b_id, "n_a": na, "n_b": nb,
                          "matched_a": ca, "matched_b": cb,
                          "agreement": round((ca + cb) / float(na + nb), 4)})
        singles = [{"ref": k, "reconstructor_id": reqs[k]["reconstructor_id"],
                    "requirement_text": reqs[k]["requirement_text"],
                    "settling_test": reqs[k]["settling_test"], "status": reqs[k]["status"]}
                   for k in sorted(reqs) if k not in partner]
        out.append({
            "item_id": item,
            "reconstructors": recs,
            "n_requirements": {rid: len(by_rec[rid]) for rid in recs},
            "pairs": pairs,
            "mean_pairwise_agreement": (round(sum(p["agreement"] for p in pairs) / len(pairs), 4)
                                        if pairs else None),
            "full_disagreement_pairs": sum(1 for p in pairs if p["agreement"] == 0),
            "n_matched_links": len(item_links),
            "singletons": singles,
            "n_singletons": len(singles),
            "agreement_definition": DEFINITION,
            "match_source": match_source,
        })
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("requirements")
    ap.add_argument("--matches", required=True)
    ap.add_argument("--match-source", required=True, help="who or what produced matches.jsonl")
    ap.add_argument("--out", required=True)
    ap.add_argument("--runs", default=None)
    a = ap.parse_args(argv)
    with Run("b4/agreement.py", vars(a), None, [a.requirements, a.matches], a.out, a.runs) as run:
        try:
            if not a.match_source.strip():
                raise Invalid("--match-source must be non-empty: the matcher is a frame entry point")
            rows = read_jsonl(a.requirements)
            if not rows:
                return finish(run, "empty", {"requirements": 0})
            out = score(rows, read_jsonl(a.matches), a.match_source)
        except Invalid as e:
            return finish(run, "error", notes=str(e))
        write_jsonl(a.out, out)
        return finish(run, "ok", {"items": len(out),
                                  "singletons": sum(o["n_singletons"] for o in out),
                                  "full_disagreement_pairs": sum(o["full_disagreement_pairs"] for o in out)})


if __name__ == "__main__":
    sys.exit(main())
