"""Factorial sweep over the listed levels only. A failed point stays in the table."""
import itertools
from . import runner
from .sensitivity import _with_param


def sweep(cfg, levels, output):
    names = sorted(levels)
    rows = []
    for combo in itertools.product(*(levels[n] for n in names)):
        c = cfg
        for n, v in zip(names, combo):
            c = _with_param(c, n, v)
        point = dict(zip(names, combo))
        try:
            rec = runner.run(c.with_changes(run_id="%s@%s" % (cfg["run_id"], point)))
            rows.append(dict(point=point, status=rec["status"], output=rec["observations_and_predictions"]["final_state"][output]))
        except Exception as e:                       # kept: where a model fails is a result
            rows.append(dict(point=point, status="MODEL FAILED", error="%s: %s" % (type(e).__name__, e)))
    return dict(output=output, names=names, rows=rows)
