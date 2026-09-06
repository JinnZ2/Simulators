"""B4.1 items.py -- validate items.jsonl, refuse to mix arms.

Fields: item_id, source, text_verbatim, branches_stated, arm
arm in {hypothetical, documented}. One arm per output file: a mixed file
returns status=void and writes no output.

Command: python3 items.py ITEMS.jsonl --out ITEMS_VALID.jsonl
"""
import sys

from common import (parse_argv, usage_exit, ARMS, ITEM_FIELDS, Invalid, Run, Void, check_fields,
                    check_id, count_by, finish, nonempty_str, read_jsonl,
                    write_jsonl)


def validate(rows):
    probs, seen = [], set()
    for n, r in enumerate(rows, 1):
        where = "row %d" % n
        probs += check_fields(r, ITEM_FIELDS, where)
        if probs:
            continue
        probs += check_id(r["item_id"], where)
        if r["item_id"] in seen:
            probs.append("%s: duplicate item_id %r" % (where, r["item_id"]))
        seen.add(r["item_id"])
        if not nonempty_str(r["source"]):
            probs.append("%s: source must be non-empty text" % where)
        if not nonempty_str(r["text_verbatim"]):
            probs.append("%s: text_verbatim must be non-empty text" % where)
        b = r["branches_stated"]
        if isinstance(b, bool) or not isinstance(b, int) or b < 1:
            probs.append("%s: branches_stated must be an integer >= 1" % where)
        if r["arm"] not in ARMS:
            probs.append("%s: arm must be one of %s" % (where, ARMS))
    if probs:
        raise Invalid("\n".join(probs))
    arms = sorted(set(r["arm"] for r in rows))
    if len(arms) > 1:
        raise Void("arms mixed in one file: %s" % arms)
    return rows


def main(argv=None):
    try:
        a = parse_argv(argv, __doc__, positional=("items",), options=("out", "runs"), required=("out",))
    except Invalid as e:
        return usage_exit(e)
    if a is None:
        return 0
    with Run("b4/items.py", vars(a), None, [a.items], a.out, a.runs) as run:
        try:
            rows = read_jsonl(a.items)
            if not rows:
                return finish(run, "empty", {"items": 0}, "no rows")
            rows = validate(rows)
        except Invalid as e:
            return finish(run, "error", notes=str(e))
        except Void as e:
            return finish(run, "void", notes=str(e))
        write_jsonl(a.out, rows)
        return finish(run, "ok", {"items": len(rows), "by_arm": count_by(rows, "arm")})


if __name__ == "__main__":
    sys.exit(main())
