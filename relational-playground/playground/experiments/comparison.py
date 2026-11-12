"""Side-by-side comparison. No winner: rank() raises, and rows come out in name order."""
from . import runner


def side_by_side(configs, output, agreement_window=None, window_declared_at=None):
    """agreement_window (ADDITION 8): half-width fixed before the outputs are seen.
    Any cross-family pair inside it opens a coincidence card."""
    from ..equations import base as eq
    from ..analysis import coincidence
    rows = []
    for cfg in sorted(configs, key=lambda c: c["model"]):
        try:
            rec = runner.run(cfg)
            rows.append(dict(model=cfg["model"], family=eq.get(cfg["model"]).family, run_id=cfg["run_id"], status=rec["status"],
                             output=rec["observations_and_predictions"]["final_state"].get(output, "MODEL HAS NO SUCH VARIABLE"),
                             limitations=rec["known_limitations"]))
        except Exception as e:
            rows.append(dict(model=cfg["model"], run_id=cfg["run_id"], status="MODEL FAILED", error="%s: %s" % (type(e).__name__, e)))
    return dict(output=output, rows=rows, note="no ranking; each row is read with its own applicability record",
                coincidence=coincidence.on_agreement(rows, agreement_window, window_declared_at))


def rank(*_a, **_k):
    raise RuntimeError("no automatic model ranking: read the applicability records")


class RegimeUndeclared(RuntimeError):
    pass


def cross_system(systems, output):
    """ADDITION 6. systems: {system name: [Config, ...]}. Refused until every
    system's three observer regimes are declared; an UNKNOWN regime is a declaration,
    UNDECLARED is not. The regimes are printed beside the rows, never folded in."""
    owed = {}
    for name, cfgs in systems.items():
        for c in cfgs:
            u = c["controls"].observer_undeclared() if c["controls"] else ["no control matrix"]
            if u:
                owed.setdefault(name, set()).update(u)
    if owed:
        raise RegimeUndeclared("no cross-system comparison: observer regime undeclared for %s"
                               % {k: sorted(v) for k, v in sorted(owed.items())})
    out = {}
    for name in sorted(systems):
        out[name] = dict(regimes=systems[name][0]["controls"].observer, table=side_by_side(systems[name], output))
    differ = len({str(sorted(v["regimes"].items())) for v in out.values()}) > 1
    return dict(systems=out, regimes_differ=differ,
                note="regimes differ across systems: the rows are not like for like" if differ else "regimes match as declared")
