#!/usr/bin/env python3
# CC0. Synthetic numbers only — invented to exercise the arithmetic.
# Nothing here is a reading from any real system.

import weld

SYNTH = {
    "term": "SYNTHETIC",
    "domain": "test fixture",
    "tracked_by_label": "a",
    "components": [
        {"id": "a", "name": "tracked", "unit": "x"},
        {"id": "b", "name": "untracked", "unit": "x"},
        {"id": "c", "name": "untracked 2", "unit": "x"}
    ],
    "divergences": [
        # a holds, b falls 10x  -> spread 10, direction -1 (b hidden below a)
        {"id": "s1", "readings": {
            "a": {"before": 100, "after": 100},
            "b": {"before": 100, "after": 10}}},
        # a holds, b falls 1000x -> spread 1000, direction -1
        {"id": "s2", "readings": {
            "a": {"before": 100, "after": 100},
            "b": {"before": 1000, "after": 1}}},
        # a holds, c rises 4x -> spread 4, direction +1
        {"id": "s3", "readings": {
            "a": {"before": 50, "after": 50},
            "c": {"before": 10, "after": 40}}},
        # no paired readings -> counts as a case, not quantified
        {"id": "s4", "readings": {}}
    ]
}


def check(label, got, want):
    ok = "ok " if got == want else "FAIL"
    print("%s %-22s got=%s want=%s" % (ok, label, got, want))
    return got == want


def main():
    s = weld.score(SYNTH)
    fails = 0
    fails += not check("n_cases", s["n_cases"], 4)
    fails += not check("n_quantified", s["n_quantified"], 3)
    fails += not check("n_unquantified", s["n_unquantified"], 1)
    fails += not check("max_spread", round(s["max_spread"], 6), 1000.0)
    # directions: -1, -1, +1  -> |sum|/n = 1/3
    fails += not check("bias", round(s["bias"], 4), round(1.0 / 3.0, 4))

    # all-same-direction case should read bias 1.0
    same = dict(SYNTH)
    same["divergences"] = SYNTH["divergences"][:2]
    s2 = weld.score(same)
    fails += not check("bias (aligned)", s2["bias"], 1.0)

    print()
    print("FAILURES: %d" % fails)
    return 1 if fails else 0


if __name__ == "__main__":
    raise SystemExit(main())
