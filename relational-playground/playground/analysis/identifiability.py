"""Identifiability: can two parameters be told apart from this output?

Each parameter gets a sensitivity vector (change in the output trajectory per
relative nudge). Two parameters whose vectors are parallel cannot be separated
by this output. A zero vector reads NO EFFECT, which is not the same finding.
"""
import math
from ..experiments import runner
from ..experiments.sensitivity import _with_param


def pairs(cfg, output, names, rel_step=0.05, parallel_at=0.999):
    base = [s[output] for s in runner.run(cfg)["_trajectory"]["states"]]
    vec = {}
    for n in names:
        v = cfg["parameters"].values[n].value
        tr = [s[output] for s in runner.run(_with_param(cfg, n, v * (1 + rel_step)))["_trajectory"]["states"]]
        vec[n] = [a - b for a, b in zip(tr, base)]
    rows = []
    ns = sorted(names)
    for i in range(len(ns)):
        for j in range(i + 1, len(ns)):
            a, b = vec[ns[i]], vec[ns[j]]
            na, nb = math.sqrt(sum(x * x for x in a)), math.sqrt(sum(x * x for x in b))
            if na == 0 or nb == 0:
                rows.append(dict(pair=(ns[i], ns[j]), reading="NO EFFECT", which=[n for n, m in ((ns[i], na), (ns[j], nb)) if m == 0]))
                continue
            c = sum(x * y for x, y in zip(a, b)) / (na * nb)
            rows.append(dict(pair=(ns[i], ns[j]), cosine=c,
                             reading="NOT SEPARABLE by this output" if abs(c) >= parallel_at else "SEPARABLE"))
    return dict(output=output, parallel_at=parallel_at, rows=rows)
