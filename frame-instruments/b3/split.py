"""B3.1 split.py -- prompt files for two roles that never share context.

  case  python3 split.py case --case-ids c1,c2 --out DIR
        DIR/<case_id>.jsonl holding {"case_id": ...} only. The CASE role
        writes statements.jsonl (case_id, statement); nothing here names a
        key or says one will be written.
  key   python3 split.py key STATEMENTS.jsonl --out DIR
        DIR/<case_id>.jsonl holding {"statement": ...} only, built from
        statements.jsonl alone. A statements file carrying ANY field
        beyond case_id and statement is refused: that is the boundary.
        Every written file is re-read and asserted to carry the one key.
"""
import json
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ficommon import Invalid, Run, check_fields, check_id, finish, nonempty_str, parse_argv, raise_if, read_jsonl, usage_exit  # noqa: E402

STATEMENT_FIELDS = ("case_id", "statement")


def validate_statements(rows):
    probs, seen = [], set()
    for n, r in enumerate(rows, 1):
        w = "row %d" % n
        p = check_fields(r, STATEMENT_FIELDS, w)  # exact: any other field is context and is refused
        if p:
            probs += p
            continue
        probs += check_id(r["case_id"], w)
        if r["case_id"] in seen:
            probs.append("%s: duplicate case_id %r" % (w, r["case_id"]))
        seen.add(r["case_id"])
        if not nonempty_str(r["statement"]):
            probs.append("%s: statement must be non-empty text" % w)
    raise_if(probs)
    return rows


def write_one(path, obj, only_key):
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(json.dumps(obj, sort_keys=True, ensure_ascii=False) + "\n")
    with open(path, encoding="utf-8") as fh:
        back = [ln for ln in fh.read().split("\n") if ln.strip()]
    if len(back) != 1 or set(json.loads(back[0])) != {only_key}:
        raise AssertionError("%s: boundary check failed" % path)


def emit_case(ids, out_dir):
    probs = []
    for i in ids:
        probs += check_id(i, "case id")
    if len(set(ids)) != len(ids):
        probs.append("duplicate case ids")
    raise_if(probs)
    os.makedirs(out_dir, exist_ok=True)
    for i in ids:
        write_one(os.path.join(out_dir, i + ".jsonl"), {"case_id": i}, "case_id")
    return len(ids)


def emit_key(rows, out_dir):
    validate_statements(rows)
    os.makedirs(out_dir, exist_ok=True)
    for r in rows:
        write_one(os.path.join(out_dir, r["case_id"] + ".jsonl"), {"statement": r["statement"]}, "statement")
    return len(rows)


def run_case(argv):
    a = parse_argv(argv, __doc__, options=("case_ids", "out", "runs"), required=("case_ids", "out"))
    if a is None:
        return 0
    ids = [x.strip() for x in a.case_ids.split(",") if x.strip()]
    with Run("b3/split.py case", vars(a), None, [], a.out, a.runs) as run:
        try:
            if not ids:
                return finish(run, "empty", {"files": 0})
            n = emit_case(ids, a.out)
        except Invalid as e:
            return finish(run, "error", notes=str(e))
        return finish(run, "ok", {"files": n, "keys_per_file": 1})


def run_key(argv):
    a = parse_argv(argv, __doc__, positional=("statements",), options=("out", "runs"), required=("out",))
    if a is None:
        return 0
    with Run("b3/split.py key", vars(a), None, [a.statements], a.out, a.runs) as run:
        try:
            rows = read_jsonl(a.statements)
            if not rows:
                return finish(run, "empty", {"files": 0})
            n = emit_key(rows, a.out)
        except Invalid as e:
            return finish(run, "error", notes=str(e))
        return finish(run, "ok", {"files": n, "keys_per_file": 1})


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    try:
        if not argv or argv[0] not in ("case", "key"):
            raise Invalid("first argument must be case or key")
        return {"case": run_case, "key": run_key}[argv[0]](argv[1:])
    except Invalid as e:
        return usage_exit(e)


if __name__ == "__main__":
    sys.exit(main())
