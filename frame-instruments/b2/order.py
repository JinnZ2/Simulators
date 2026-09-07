"""B2.2 order.py -- counterbalance condition order across readers.
Readers are taken in blocks of four; each block receives a fresh seeded
4x4 WILLIAMS square (the n=4 row-complete Latin square, relabelled by a
seeded permutation of A,B,C,D), so every condition sits in every position
once per block AND every ordered successor pair occurs exactly once per
block -- a cyclic square balances position only and confounds carryover.
Readers past the last full block receive a seeded permutation each, and
the shortfall is stated in the run record notes. Seed written into every
row.

Command: python3 order.py --readers N --seed S --out ASSIGNMENT.jsonl
"""
import os
import random
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ficommon import Invalid, Run, finish, parse_argv, usage_exit, write_jsonl  # noqa: E402

CONDITIONS = ["A", "B", "C", "D"]


WILLIAMS_4 = ((0, 1, 3, 2), (1, 2, 0, 3), (2, 3, 1, 0), (3, 0, 2, 1))


def latin_square(rng):
    base = list(CONDITIONS)
    rng.shuffle(base)
    return [[base[k] for k in row] for row in WILLIAMS_4]


def assign(n_readers, seed):
    rng = random.Random(seed)
    rows, k = [], 0
    while k + 4 <= n_readers:
        for order in latin_square(rng):
            k += 1
            rows.append({"reader_id": "r%03d" % k, "order": order, "seed": seed,
                         "block": (k - 1) // 4 + 1, "latin_square": True})
    while k < n_readers:
        k += 1
        order = list(CONDITIONS)
        rng.shuffle(order)
        rows.append({"reader_id": "r%03d" % k, "order": order, "seed": seed, "block": None, "latin_square": False})
    return rows, n_readers % 4


def main(argv=None):
    try:
        a = parse_argv(argv, __doc__, options=("readers", "seed", "out", "runs"), required=("readers", "seed", "out"))
    except Invalid as e:
        return usage_exit(e)
    if a is None:
        return 0
    try:
        n, seed = int(a.readers), int(a.seed)
    except ValueError:
        return usage_exit("--readers and --seed must be integers")
    with Run("b2/order.py", vars(a), seed, [], a.out, a.runs) as run:
        if n < 1:
            return finish(run, "empty", {"readers": n}, "no readers")
        rows, short = assign(n, seed)
        write_jsonl(a.out, rows)
        notes = ("shortfall: %d reader(s) beyond the last full Latin block carry seeded permutations" % short
                 if short else "")
        return finish(run, "ok", {"readers": n, "latin_blocks": n // 4, "shortfall": short}, notes)


if __name__ == "__main__":
    sys.exit(main())
