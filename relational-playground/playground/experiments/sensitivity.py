"""One-at-a-time sensitivity. Listed in parameter-name order, never by size."""
from . import runner
from ..uncertainty import Value, UncertaintyMatrix


def _with_param(cfg, name, value):
    vals = dict(cfg["parameters"].values)
    old = vals[name]
    vals[name] = Value(value, old.status, old.provenance + " (nudged)", old.interval)
    return cfg.with_changes(parameters=UncertaintyMatrix(vals), run_id="%s+%s" % (cfg["run_id"], name))


def one_at_a_time(cfg, output, rel_step=0.05, names=None):
    base = runner.run(cfg)
    y0 = base["observations_and_predictions"]["final_state"][output]
    rows = []
    for name in sorted(names or cfg["parameters"].values):
        v = cfg["parameters"].values[name]
        if not isinstance(v.value, (int, float)) or isinstance(v.value, bool):
            rows.append(dict(parameter=name, state="NOT NUDGEABLE", reason="not a single number"))
            continue
        if v.value == 0:
            rows.append(dict(parameter=name, state="NOT NUDGEABLE", reason="value is 0; a relative step is undefined"))
            continue
        y1 = runner.run(_with_param(cfg, name, v.value * (1 + rel_step)))["observations_and_predictions"]["final_state"][output]
        rows.append(dict(parameter=name, state="NUDGED", d_output=y1 - y0,
                         elasticity=((y1 - y0) / y0) / rel_step if y0 != 0 else "UNDEFINED (base output 0)"))
    return dict(output=output, base=y0, rel_step=rel_step, rows=rows)
