"""B1.2 score.py -- separations.jsonl, one row per (trace, D, L).

Row: case_id, model_id, i, branch_rank, D, L, ent_i, gap_i, resync_D, div_D
  gap_i    = logprob_taken - logprob of the forced branch at position i
  resync_D = 1 if the continuation rejoins the base within D tokens:
             some t, L <= t <= D, with continuation[t-L:t] == base[t-L:t]
             (aligned, exact, length >= L). L is swept and written per row.
  div_D    = Levenshtein distance over tokens, both truncated at D,
             divided by the longer truncated length (0.0 if both empty).
[CHOICE] continuation and base_continuation are the tokens AFTER the forced
token and the taken token respectively, compared position-aligned.

Command: python3 score.py BASE.jsonl TRACES.jsonl --out SEPARATIONS.jsonl [--D 8,16,32,64,128] [--L 2,4,8]
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ficommon import Invalid, Run, finish, parse_argv, usage_exit, write_jsonl  # noqa: E402
from schema import load  # noqa: E402

D_DEFAULT = "8,16,32,64,128"
L_DEFAULT = "2,4,8"


def levenshtein(a, b):
    """Token-level edit distance, two-row DP. Written here; no library."""
    if not a:
        return len(b)
    if not b:
        return len(a)
    prev = list(range(len(b) + 1))
    for i, ta in enumerate(a, 1):
        cur = [i]
        for j, tb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (0 if ta == tb else 1)))
        prev = cur
    return prev[-1]


def div(cont, base, D):
    a, b = cont[:D], base[:D]
    m = max(len(a), len(b))
    return round(levenshtein(a, b) / float(m), 6) if m else 0.0


def resync(cont, base, D, L):
    top = min(D, len(cont), len(base))
    for t in range(L, top + 1):
        if cont[t - L:t] == base[t - L:t]:
            return 1
    return 0


def gap(base_row, forced_token):
    lp = [p for t, p in base_row["topk"] if t == forced_token][0]
    return round(base_row["logprob_taken"] - lp, 6)


def sweep(base_rows, traces, Ds, Ls):
    index = {(r["case_id"], r["model_id"], r["i"]): r for r in base_rows}
    out = []
    for tr in traces:
        b = index[(tr["case_id"], tr["model_id"], tr["i"])]
        g = gap(b, tr["forced_token"])
        for D in Ds:
            dv = div(tr["continuation"], tr["base_continuation"], D)
            for L in Ls:
                out.append({"case_id": tr["case_id"], "model_id": tr["model_id"], "i": tr["i"],
                            "branch_rank": tr["branch_rank"], "D": D, "L": L,
                            "ent_i": b["entropy_i"], "gap_i": g,
                            "resync_D": resync(tr["continuation"], tr["base_continuation"], D, L),
                            "div_D": dv})
    return out


def parse_ints(s, name):
    try:
        vals = sorted(set(int(x) for x in s.split(",") if x.strip()))
    except ValueError:
        raise Invalid("--%s must be comma-separated integers" % name)
    if not vals or any(v < 1 for v in vals):
        raise Invalid("--%s must be positive integers" % name)
    return vals


def main(argv=None):
    try:
        a = parse_argv(argv, __doc__, positional=("base", "traces"), options=("out", "D", "L", "runs"),
                       required=("out",), defaults={"D": D_DEFAULT, "L": L_DEFAULT})
    except Invalid as e:
        return usage_exit(e)
    if a is None:
        return 0
    with Run("b1/score.py", vars(a), None, [a.base, a.traces], a.out, a.runs) as run:
        try:
            Ds, Ls = parse_ints(a.D, "D"), parse_ints(a.L, "L")
            base, traces = load(a.base, a.traces)
        except Invalid as e:
            return finish(run, "error", notes=str(e))
        if not traces:
            return finish(run, "empty", {"traces": 0})
        rows = sweep(base, traces, Ds, Ls)
        write_jsonl(a.out, rows)
        return finish(run, "ok", {"traces": len(traces), "rows": len(rows), "D": Ds, "L": Ls})


if __name__ == "__main__":
    sys.exit(main())
