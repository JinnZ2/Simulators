"""B4.3 requirements.py -- validate returned requirement rows.

Fields: item_id, reconstructor_id, req_id, requirement_text, status,
        settling_test, layer
status in {true,false,lapsed,partial,unknown,undifferentiated}.
A file using ONLY true/false across all rows -> status=void (the grading
was not run). Empty settling_test -> rejected. `layer` is free text,
counted downstream, never checked against a list.

Command: python3 requirements.py REQS.jsonl --items ITEMS_VALID.jsonl --out REQS_VALID.jsonl
"""
import argparse
import sys

from common import (REQ_FIELDS, STATES, Invalid, Run, Void, check_fields,
                    check_id, count_by, finish, nonempty_str, read_jsonl,
                    ref, write_jsonl)


def validate(rows, item_ids=None):
    probs, seen = [], set()
    for n, r in enumerate(rows, 1):
        where = "row %d" % n
        p = check_fields(r, REQ_FIELDS, where)
        if p:
            probs += p
            continue
        probs += check_id(r["item_id"], where) + check_id(r["reconstructor_id"], where)
        probs += check_id(r["req_id"], where)
        key = (r["item_id"], r["reconstructor_id"], r["req_id"])
        if key in seen:
            probs.append("%s: duplicate %s under item %s" % (where, ref(key[1], key[2]), key[0]))
        seen.add(key)
        if item_ids is not None and r["item_id"] not in item_ids:
            probs.append("%s: item_id %r not in items file" % (where, r["item_id"]))
        if not nonempty_str(r["requirement_text"]):
            probs.append("%s: requirement_text must be non-empty" % where)
        if r["status"] not in STATES:
            probs.append("%s: status %r not in %s" % (where, r["status"], STATES))
        if not nonempty_str(r["settling_test"]):
            probs.append("%s: settling_test is required and non-empty (a status with no test is rejected)" % where)
        if not isinstance(r["layer"], str):
            probs.append("%s: layer must be text" % where)
    if probs:
        raise Invalid("\n".join(probs))
    used = set(r["status"] for r in rows)
    if used <= {"true", "false"}:
        raise Void("only %s used across all rows: two-state return, grading not run" % sorted(used))
    return rows


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("requirements")
    ap.add_argument("--items", default=None, help="validated items file; item_ids are checked against it")
    ap.add_argument("--out", required=True)
    ap.add_argument("--runs", default=None)
    a = ap.parse_args(argv)
    with Run("b4/requirements.py", vars(a), None, [a.requirements, a.items], a.out, a.runs) as run:
        try:
            rows = read_jsonl(a.requirements)
            if not rows:
                return finish(run, "empty", {"requirements": 0})
            item_ids = set(r["item_id"] for r in read_jsonl(a.items)) if a.items else None
            rows = validate(rows, item_ids)
        except Invalid as e:
            return finish(run, "error", notes=str(e))
        except Void as e:
            return finish(run, "void", notes=str(e))
        write_jsonl(a.out, rows)
        return finish(run, "ok", {"requirements": len(rows), "by_status": count_by(rows, "status"),
                                  "reconstructors": len(set(r["reconstructor_id"] for r in rows))})


if __name__ == "__main__":
    sys.exit(main())
