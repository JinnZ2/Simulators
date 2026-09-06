"""B1.1 schema.py -- validators for base.jsonl and traces.jsonl.
Rejects with file, line number and field name. No coercion, no defaults.

base.jsonl:   case_id, model_id, i, token_taken, logprob_taken,
              topk [[token, logprob], ...], entropy_i, entropy_basis ("full"|"topk")
traces.jsonl: case_id, model_id, i, branch_rank, forced_token,
              continuation [token...] (<=128), base_continuation (same length)

Command: python3 schema.py BASE.jsonl TRACES.jsonl --out CHECK.jsonl
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ficommon import (Invalid, Run, check_fields, finish, is_int, is_num,  # noqa: E402
                      parse_argv, raise_if, read_jsonl, usage_exit, write_jsonl)

BASE_FIELDS = ("case_id", "model_id", "i", "token_taken", "logprob_taken", "topk", "entropy_i", "entropy_basis")
TRACE_FIELDS = ("case_id", "model_id", "i", "branch_rank", "forced_token", "continuation", "base_continuation")
BASES = ("full", "topk")
MAX_CONT = 128


def _tokens_ok(v):
    return isinstance(v, list) and all(isinstance(t, str) for t in v)


def validate_base(rows, path="base.jsonl"):
    probs, seen = [], set()
    for n, r in enumerate(rows, 1):
        w = "%s:%d" % (path, n)
        p = check_fields(r, BASE_FIELDS, w)
        if p:
            probs += p
            continue
        for k in ("case_id", "model_id", "token_taken"):
            if not isinstance(r[k], str) or not r[k]:
                probs.append("%s: %s: must be non-empty string" % (w, k))
        if not is_int(r["i"]) or r["i"] < 0:
            probs.append("%s: i: must be integer >= 0" % w)
        if not is_num(r["logprob_taken"]) or r["logprob_taken"] > 0:
            probs.append("%s: logprob_taken: must be number <= 0" % w)
        tk = r["topk"]
        if (not isinstance(tk, list) or not tk or
                not all(isinstance(e, list) and len(e) == 2 and isinstance(e[0], str) and is_num(e[1]) for e in tk)):
            probs.append("%s: topk: must be non-empty list of [token, logprob]" % w)
        if not is_num(r["entropy_i"]) or r["entropy_i"] < 0:
            probs.append("%s: entropy_i: must be number >= 0" % w)
        if r["entropy_basis"] not in BASES:
            probs.append("%s: entropy_basis: must be one of %s, not inferred" % (w, BASES))
        key = (r["case_id"], r["model_id"], r["i"]) if isinstance(r["i"], int) else None
        if key in seen:
            probs.append("%s: i: duplicate position %s" % (w, key))
        seen.add(key)
    raise_if(probs)
    return rows


def base_index(base_rows):
    return {(r["case_id"], r["model_id"], r["i"]): r for r in base_rows}


def validate_traces(rows, index, path="traces.jsonl"):
    probs, seen = [], set()
    for n, r in enumerate(rows, 1):
        w = "%s:%d" % (path, n)
        p = check_fields(r, TRACE_FIELDS, w)
        if p:
            probs += p
            continue
        for k in ("case_id", "model_id", "forced_token"):
            if not isinstance(r[k], str) or not r[k]:
                probs.append("%s: %s: must be non-empty string" % (w, k))
        if not is_int(r["i"]) or r["i"] < 0:
            probs.append("%s: i: must be integer >= 0" % w)
        if not is_int(r["branch_rank"]) or r["branch_rank"] < 1:
            probs.append("%s: branch_rank: must be integer >= 1" % w)
        c, b = r["continuation"], r["base_continuation"]
        if not _tokens_ok(c) or len(c) > MAX_CONT:
            probs.append("%s: continuation: must be list of <= %d strings" % (w, MAX_CONT))
        if not _tokens_ok(b) or (_tokens_ok(c) and len(b) != len(c)):
            probs.append("%s: base_continuation: must be list of strings, same length as continuation" % w)
        if probs and probs[-1].startswith(w):
            continue
        key = (r["case_id"], r["model_id"], r["i"])
        base = index.get(key)
        if base is None:
            probs.append("%s: i: position %s not in base.jsonl" % (w, key))
        elif r["forced_token"] not in [t for t, _ in base["topk"]]:
            probs.append("%s: forced_token: %r not in topk at %s" % (w, r["forced_token"], key))
        full = key + (r["branch_rank"],)
        if full in seen:
            probs.append("%s: branch_rank: duplicate trace %s" % (w, full))
        seen.add(full)
    raise_if(probs)
    return rows


def load(base_path, traces_path):
    base = validate_base(read_jsonl(base_path), base_path)
    traces = validate_traces(read_jsonl(traces_path), base_index(base), traces_path)
    return base, traces


def main(argv=None):
    try:
        a = parse_argv(argv, __doc__, positional=("base", "traces"), options=("out", "runs"), required=("out",))
    except Invalid as e:
        return usage_exit(e)
    if a is None:
        return 0
    with Run("b1/schema.py", vars(a), None, [a.base, a.traces], a.out, a.runs) as run:
        try:
            base, traces = load(a.base, a.traces)
        except Invalid as e:
            return finish(run, "error", notes=str(e))
        if not base or not traces:
            return finish(run, "empty", {"base_rows": len(base), "trace_rows": len(traces)})
        row = {"base_rows": len(base), "trace_rows": len(traces),
               "case_ids": sorted(set(r["case_id"] for r in base)),
               "model_ids": sorted(set(r["model_id"] for r in base))}
        write_jsonl(a.out, [row])
        return finish(run, "ok", {"base_rows": len(base), "trace_rows": len(traces)})


if __name__ == "__main__":
    sys.exit(main())
