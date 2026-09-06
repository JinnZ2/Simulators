"""B3.2 join.py -- join statements.jsonl and keys.jsonl into the cases.jsonl
schema B2 consumes, every row carrying its arm. Rows on one side with no
partner are DROPPED, and every drop is counted and listed in the run
record; nothing is dropped silently.

keys.jsonl: case_id, key_posed, key_target, key_why

Command: python3 join.py STATEMENTS.jsonl KEYS.jsonl --arm single|split --out CASES.jsonl
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ficommon import B3_ARMS, Invalid, Run, check_fields, check_id, finish, nonempty_str, parse_argv, raise_if, read_jsonl, usage_exit, write_jsonl  # noqa: E402
from split import validate_statements  # noqa: E402

KEY_FIELDS = ("case_id", "key_posed", "key_target", "key_why")


def validate_keys(rows):
    probs, seen = [], set()
    for n, r in enumerate(rows, 1):
        w = "key row %d" % n
        p = check_fields(r, KEY_FIELDS, w)
        if p:
            probs += p
            continue
        probs += check_id(r["case_id"], w)
        if r["case_id"] in seen:
            probs.append("%s: duplicate case_id %r" % (w, r["case_id"]))
        seen.add(r["case_id"])
        for k in KEY_FIELDS[1:]:
            if not nonempty_str(r[k]):
                probs.append("%s: %s must be non-empty text" % (w, k))
    raise_if(probs)
    return rows


def join(statements, keys, arm):
    if arm not in B3_ARMS:
        raise Invalid("arm must be one of %s" % (B3_ARMS,))
    validate_statements(statements)
    validate_keys(keys)
    s = {r["case_id"]: r for r in statements}
    k = {r["case_id"]: r for r in keys}
    joined = [{"case_id": i, "statement": s[i]["statement"], "key_posed": k[i]["key_posed"],
               "key_target": k[i]["key_target"], "key_why": k[i]["key_why"], "arm": arm} for i in sorted(set(s) & set(k))]
    drops = {"statements_without_key": sorted(set(s) - set(k)), "keys_without_statement": sorted(set(k) - set(s))}
    return joined, drops


def main(argv=None):
    try:
        a = parse_argv(argv, __doc__, positional=("statements", "keys"), options=("arm", "out", "runs"), required=("arm", "out"))
    except Invalid as e:
        return usage_exit(e)
    if a is None:
        return 0
    with Run("b3/join.py", vars(a), None, [a.statements, a.keys], a.out, a.runs) as run:
        try:
            joined, drops = join(read_jsonl(a.statements), read_jsonl(a.keys), a.arm)
        except Invalid as e:
            return finish(run, "error", notes=str(e))
        n_drop = sum(len(v) for v in drops.values())
        notes = ("dropped %d: %s" % (n_drop, drops)) if n_drop else ""
        if not joined:
            return finish(run, "empty", {"joined": 0, "dropped": n_drop}, notes)
        write_jsonl(a.out, joined)
        return finish(run, "ok", {"joined": len(joined), "dropped": n_drop, "arm": a.arm}, notes)


if __name__ == "__main__":
    sys.exit(main())
