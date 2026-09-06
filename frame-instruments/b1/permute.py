"""B1.3 permute.py -- shuffle WHICH position carries which
(ent_i, gap_i, resync_D, div_D) tuple. Row count and every other field
preserved. [CHOICE] tuples are shuffled within each (model_id, D, L)
stratum, independently per stratum, so the sweep structure survives and
the top-decile sets at adjacent D or L are independent under the null.
The seed is written into every row as permute_seed.

Command: python3 permute.py SEPARATIONS.jsonl --seed N --out SEPARATIONS_PERMUTED.jsonl
"""
import os
import random
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ficommon import Invalid, Run, check_fields, finish, parse_argv, raise_if, read_jsonl, usage_exit, write_jsonl  # noqa: E402

TUPLE = ("ent_i", "gap_i", "resync_D", "div_D")
KEYS = ("case_id", "model_id", "i", "branch_rank", "D", "L")


def permute(rows, seed):
    probs = []
    for n, r in enumerate(rows, 1):
        probs += check_fields(r, KEYS + TUPLE, "row %d" % n, exact=False)
    raise_if(probs)
    rng = random.Random(seed)
    strata = {}
    for idx, r in enumerate(rows):
        strata.setdefault((r["model_id"], r["D"], r["L"]), []).append(idx)
    out = [dict(r) for r in rows]
    for key in sorted(strata, key=str):
        idxs = strata[key]
        tuples = [tuple(rows[i][k] for k in TUPLE) for i in idxs]
        rng.shuffle(tuples)
        for i, tup in zip(idxs, tuples):
            for k, v in zip(TUPLE, tup):
                out[i][k] = v
    for r in out:
        r["permute_seed"] = seed
    return out


def main(argv=None):
    try:
        a = parse_argv(argv, __doc__, positional=("separations",), options=("seed", "out", "runs"), required=("seed", "out"))
    except Invalid as e:
        return usage_exit(e)
    if a is None:
        return 0
    try:
        seed = int(a.seed)
    except ValueError:
        return usage_exit("--seed must be an integer")
    with Run("b1/permute.py", vars(a), seed, [a.separations], a.out, a.runs) as run:
        try:
            rows = read_jsonl(a.separations)
            if not rows:
                return finish(run, "empty", {"rows": 0})
            out = permute(rows, seed)
        except Invalid as e:
            return finish(run, "error", notes=str(e))
        write_jsonl(a.out, out)
        return finish(run, "ok", {"rows": len(out), "seed": seed})


if __name__ == "__main__":
    sys.exit(main())
