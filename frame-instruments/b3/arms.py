"""B3.3 arms.py -- declare the arms and refuse to mix them in one file.

  single   one instance writes statement and key together (baseline)
  split    two instances, no shared context

Validates a cases.jsonl in B2's schema plus arm; every row must carry an
arm from the list and all rows one arm, else void. B2's conditions.py
carries the arm through; comparing condition-B agreement between arms is
the B3 result and is read from two agree.py outputs side by side.

Command: python3 arms.py CASES.jsonl --out CASES_VALID.jsonl
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ficommon import B3_ARMS, CASE_FIELDS, Invalid, Run, Void, check_fields, check_id, finish, nonempty_str, parse_argv, raise_if, read_jsonl, usage_exit, write_jsonl  # noqa: E402

FIELDS = CASE_FIELDS + ("arm",)


def validate(rows):
    probs, seen = [], set()
    for n, r in enumerate(rows, 1):
        w = "row %d" % n
        p = check_fields(r, FIELDS, w)
        if p:
            probs += p
            continue
        probs += check_id(r["case_id"], w)
        if r["case_id"] in seen:
            probs.append("%s: duplicate case_id %r" % (w, r["case_id"]))
        seen.add(r["case_id"])
        for k in CASE_FIELDS[1:]:
            if not nonempty_str(r[k]):
                probs.append("%s: %s must be non-empty text" % (w, k))
        if r["arm"] not in B3_ARMS:
            probs.append("%s: arm must be one of %s" % (w, B3_ARMS))
    raise_if(probs)
    arms = sorted(set(r["arm"] for r in rows))
    if len(arms) > 1:
        raise Void("arms mixed in one file: %s" % arms)
    return rows, arms[0]


def main(argv=None):
    try:
        a = parse_argv(argv, __doc__, positional=("cases",), options=("out", "runs"), required=("out",))
    except Invalid as e:
        return usage_exit(e)
    if a is None:
        return 0
    with Run("b3/arms.py", vars(a), None, [a.cases], a.out, a.runs) as run:
        try:
            rows = read_jsonl(a.cases)
            if not rows:
                return finish(run, "empty", {"cases": 0})
            rows, arm = validate(rows)
        except Invalid as e:
            return finish(run, "error", notes=str(e))
        except Void as e:
            return finish(run, "void", notes=str(e))
        write_jsonl(a.out, rows)
        return finish(run, "ok", {"cases": len(rows), "arm": arm})


if __name__ == "__main__":
    sys.exit(main())
