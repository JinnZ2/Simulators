"""B2.3 lock.py -- condition D's commit lock as a process boundary.

  commit   python3 lock.py commit --reader R --case C --response RESP.json --commits COMMITS.jsonl
           RESP.json holds the A-stage response {"posed": ..., "target": ...}.
           Appends {reader_id, case_id, response, sha256} and exits. Reads no key.
  release  python3 lock.py release --reader R --case C --cases CASES.jsonl --commits COMMITS.jsonl --out RELEASED.jsonl
           Refuses (status void) unless a commit row exists for (reader, case).
           Appends {reader_id, case_id, condition: "D2", presented_text, commit_sha256}.

One invocation runs exactly one of the two; the commit path never opens
cases.jsonl and the release path never writes commits.jsonl.
"""
import hashlib
import json
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ficommon import Invalid, Run, Void, finish, nonempty_str, parse_argv, read_jsonl, usage_exit, write_jsonl  # noqa: E402
from conditions import key_text, validate_cases  # noqa: E402

RESPONSE_FIELDS = ("posed", "target")


def response_hash(resp):
    return hashlib.sha256(json.dumps(resp, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()


def load_response(path):
    with open(path, encoding="utf-8") as fh:
        resp = json.load(fh)
    if not isinstance(resp, dict) or set(resp) != set(RESPONSE_FIELDS):
        raise Invalid("response must be an object with exactly %s" % (RESPONSE_FIELDS,))
    if not all(nonempty_str(resp[k]) for k in RESPONSE_FIELDS):
        raise Invalid("response fields must be non-empty text")
    return resp


def find_commit(commits, reader, case):
    for c in commits:
        if c.get("reader_id") == reader and c.get("case_id") == case and c.get("sha256"):
            return c
    return None


def commit(argv):
    a = parse_argv(argv, __doc__, options=("reader", "case", "response", "commits", "runs"),
                   required=("reader", "case", "response", "commits"))
    if a is None:
        return 0
    with Run("b2/lock.py commit", vars(a), None, [a.response], a.commits, a.runs) as run:
        try:
            resp = load_response(a.response)
        except (Invalid, ValueError, OSError) as e:
            return finish(run, "error", notes=str(e))
        row = {"reader_id": a.reader, "case_id": a.case, "response": resp, "sha256": response_hash(resp)}
        write_jsonl(a.commits, [row], append=True)
        return finish(run, "ok", {"committed": 1, "sha256": row["sha256"][:12]})


def release(argv):
    a = parse_argv(argv, __doc__, options=("reader", "case", "cases", "commits", "out", "runs"),
                   required=("reader", "case", "cases", "commits", "out"))
    if a is None:
        return 0
    with Run("b2/lock.py release", vars(a), None, [a.cases, a.commits], a.out, a.runs) as run:
        try:
            commits = read_jsonl(a.commits) if os.path.exists(a.commits) else []
            c = find_commit(commits, a.reader, a.case)
            if c is None:
                raise Void("no commit for reader %r case %r: key not released" % (a.reader, a.case))
            cases, _ = validate_cases(read_jsonl(a.cases))
            match = [x for x in cases if x["case_id"] == a.case]
            if not match:
                raise Invalid("case %r not in %s" % (a.case, a.cases))
        except Invalid as e:
            return finish(run, "error", notes=str(e))
        except Void as e:
            return finish(run, "void", notes=str(e))
        row = {"reader_id": a.reader, "case_id": a.case, "condition": "D2",
               "presented_text": key_text(match[0]), "commit_sha256": c["sha256"]}
        write_jsonl(a.out, [row], append=True)
        return finish(run, "ok", {"released": 1, "commit_sha256": c["sha256"][:12]})


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    try:
        if not argv or argv[0] not in ("commit", "release"):
            raise Invalid("first argument must be commit or release")
        return {"commit": commit, "release": release}[argv[0]](argv[1:])
    except Invalid as e:
        return usage_exit(e)


if __name__ == "__main__":
    sys.exit(main())
