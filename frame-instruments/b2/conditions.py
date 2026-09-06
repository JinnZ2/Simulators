"""B2.1 conditions.py -- four presentation files from cases.jsonl.
Each row: case_id, condition, presented_text ONLY. Withheld fields never
appear, asserted on every row by field set and by substring.

  A  statement only        B  key only (posed + target + why, no statement)
  C  both, simultaneous    D  statement only; the key is released by lock.py
                              after a committed A-stage response
cases.jsonl: case_id, statement, key_posed, key_target, key_why [, arm]
An optional arm (single | split, from B3) is carried in the run record;
a file mixing arms is void. [CHOICE] key text is rendered as three
labelled lines; the same rendering is imported by lock.py.

Command: python3 conditions.py CASES.jsonl --out DIR
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ficommon import (B3_ARMS, CASE_FIELDS, Invalid, Run, Void, check_fields, check_id, finish,  # noqa: E402
                      nonempty_str, parse_argv, raise_if, read_jsonl, usage_exit, write_jsonl)

CONDITIONS = ("A", "B", "C", "D")
ROW_FIELDS = ("case_id", "condition", "presented_text")


def key_text(c):
    return "posed: %s\ntarget: %s\nwhy: %s" % (c["key_posed"], c["key_target"], c["key_why"])


def validate_cases(rows):
    probs, seen = [], set()
    for n, c in enumerate(rows, 1):
        w = "row %d" % n
        p = check_fields(c, CASE_FIELDS, w, exact=False)
        for k in c:
            if k not in CASE_FIELDS + ("arm",):
                p.append("%s: unexpected field %r" % (w, k))
        if p:
            probs += p
            continue
        probs += check_id(c["case_id"], w)
        if c["case_id"] in seen:
            probs.append("%s: duplicate case_id %r" % (w, c["case_id"]))
        seen.add(c["case_id"])
        for k in CASE_FIELDS[1:]:
            if not nonempty_str(c[k]):
                probs.append("%s: %s must be non-empty text" % (w, k))
        if "arm" in c and c["arm"] not in B3_ARMS:
            probs.append("%s: arm must be one of %s" % (w, B3_ARMS))
    raise_if(probs)
    arms = sorted(set(c.get("arm") for c in rows if "arm" in c))
    if len(arms) > 1:
        raise Void("arms mixed in one file: %s" % arms)
    return rows, (arms[0] if arms else None)


def present(c, cond):
    if cond == "A" or cond == "D":
        return c["statement"]
    if cond == "B":
        return key_text(c)
    return c["statement"] + "\n\n" + key_text(c)


def build(rows):
    files = {}
    for cond in CONDITIONS:
        out = []
        for c in rows:
            row = {"case_id": c["case_id"], "condition": cond, "presented_text": present(c, cond)}
            assert_no_leak(row, c)
            out.append(row)
        files[cond] = out
    return files


def assert_no_leak(row, c):
    """Field set exact; withheld text absent by substring."""
    if set(row) != set(ROW_FIELDS):
        raise Invalid("%s/%s: row fields %s, expected %s" % (c["case_id"], row["condition"], sorted(row), list(ROW_FIELDS)))
    withheld = {"A": ("key_posed", "key_target", "key_why"), "D": ("key_posed", "key_target", "key_why"),
                "B": ("statement",), "C": ()}[row["condition"]]
    for k in withheld:
        if c[k] in row["presented_text"]:
            raise Invalid("%s/%s: withheld field %r present in presented_text" % (c["case_id"], row["condition"], k))


def main(argv=None):
    try:
        a = parse_argv(argv, __doc__, positional=("cases",), options=("out", "runs"), required=("out",))
    except Invalid as e:
        return usage_exit(e)
    if a is None:
        return 0
    with Run("b2/conditions.py", vars(a), None, [a.cases], a.out, a.runs) as run:
        try:
            rows = read_jsonl(a.cases)
            if not rows:
                return finish(run, "empty", {"cases": 0})
            rows, arm = validate_cases(rows)
            files = build(rows)
        except Invalid as e:
            return finish(run, "error", notes=str(e))
        except Void as e:
            return finish(run, "void", notes=str(e))
        for cond, out in files.items():
            write_jsonl(os.path.join(a.out, "%s.jsonl" % cond), out)
        return finish(run, "ok", {"cases": len(rows), "files": len(files), "arm": arm})


if __name__ == "__main__":
    sys.exit(main())
