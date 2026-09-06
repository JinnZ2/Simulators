"""B4.6 nullshuffle.py -- reassign requirement lists to the WRONG items.

A requirement list is one (item, reconstructor) group. For each
reconstructor, the items they reconstructed are deranged (no list stays
on its own item); counts and every other field are preserved. A
reconstructor with fewer than two items has no wrong item available and
the run is void.

The seed is written into every output row as `shuffle_seed` and into the
run record. grade.py and agreement.py run on the output unchanged; the
matcher must be run on the shuffled file too, blind to which file is
which, to produce its matches.jsonl.

Command: python3 nullshuffle.py REQS_VALID.jsonl --seed N --out REQS_SHUFFLED.jsonl
"""
import random
import sys

from common import (parse_argv, usage_exit, REQ_FIELDS, Invalid, Run, Void, check_fields, finish,
                    raise_if, read_jsonl, write_jsonl)


def derange(seq, rng):
    """Permutation of seq with no fixed point, drawn uniformly by rejection."""
    n = len(seq)
    if n < 2:
        raise Void("cannot reassign a single list to a wrong item")
    while True:
        perm = list(seq)
        rng.shuffle(perm)
        if all(a != b for a, b in zip(seq, perm)):
            return perm


def shuffle(rows, seed):
    probs = []
    for n, r in enumerate(rows, 1):
        probs += check_fields(r, REQ_FIELDS, "row %d" % n)
    raise_if(probs)
    rng = random.Random(seed)
    by_rec = {}
    for r in rows:
        by_rec.setdefault(r["reconstructor_id"], [])
        if r["item_id"] not in by_rec[r["reconstructor_id"]]:
            by_rec[r["reconstructor_id"]].append(r["item_id"])
    mapping = {}
    for rid in sorted(by_rec):
        items = sorted(by_rec[rid])
        for src, dst in zip(items, derange(items, rng)):
            mapping[(rid, src)] = dst
    out = []
    for r in rows:
        s = dict(r)
        s["item_id"] = mapping[(r["reconstructor_id"], r["item_id"])]
        s["shuffle_seed"] = seed
        out.append(s)
    return out, mapping


def main(argv=None):
    try:
        a = parse_argv(argv, __doc__, positional=("requirements",), options=("seed", "out", "runs"), required=("seed", "out"))
    except Invalid as e:
        return usage_exit(e)
    if a is None:
        return 0
    a.seed = int(a.seed)
    with Run("b4/nullshuffle.py", vars(a), a.seed, [a.requirements], a.out, a.runs) as run:
        try:
            rows = read_jsonl(a.requirements)
            if not rows:
                return finish(run, "empty", {"requirements": 0})
            out, mapping = shuffle(rows, a.seed)
        except Invalid as e:
            return finish(run, "error", notes=str(e))
        except Void as e:
            return finish(run, "void", notes=str(e))
        write_jsonl(a.out, out)
        moved = sum(1 for (rid, src), dst in mapping.items() if src != dst)
        return finish(run, "ok", {"requirements": len(out), "lists": len(mapping), "lists_moved": moved,
                                  "seed": a.seed})


if __name__ == "__main__":
    sys.exit(main())
