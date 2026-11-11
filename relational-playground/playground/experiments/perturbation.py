"""Perturbation response: the same run with and without one kick, differenced."""
from . import runner


def response(cfg, target, magnitude, at, tol_fraction=0.05):
    ctl = cfg["controls"]
    if ctl is None:
        raise ValueError("a perturbation needs a control matrix")
    base = runner.run(cfg)
    extra = dict(ctl.as_dict())
    extra["perturbation"] = dict(target=target, magnitude=magnitude, at=at)
    kicked = runner.run(cfg.with_changes(controls=type(ctl)(**extra), run_id=cfg["run_id"] + "+kick"))
    tb, tk = base["_trajectory"], kicked["_trajectory"]
    diff = [k[target] - b[target] for b, k in zip(tb["states"], tk["states"])]
    peak = max(abs(d) for d in diff)
    recovered = None
    for t, d in zip(tb["times"], diff):
        if t > at and peak > 0 and abs(d) <= tol_fraction * peak:
            recovered = t
            break
    return dict(target=target, magnitude=magnitude, at=at, peak_deviation=peak,
                final_deviation=diff[-1], recovered_at=recovered if recovered is not None else "NOT RECOVERED IN RUN",
                recovery_rule="|deviation| <= %g of peak" % tol_fraction, base=base, kicked=kicked)
