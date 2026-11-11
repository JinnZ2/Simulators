"""The experiment runner. It never changes when the equation does.

run(config) integrates one model over one configuration and returns a record
holding the twelve outputs. Unknown parameters stop the run; nothing is filled.
"""
import os
from ..equations import base as eq
from ..reporting import provenance, results
from .. import l0

REQUIRED = ("run_id", "system", "boundary", "model", "relationships", "controls", "environment",
            "parameters", "initial", "t_end", "dt", "observations", "budgets")


class Config(dict):
    def __init__(self, **kw):
        missing = [k for k in REQUIRED if k not in kw]
        if missing:
            raise ValueError("config fields %s dropped (write None with a reason in notes)" % missing)
        super().__init__(**kw)

    def with_changes(self, **kw):
        c = dict(self)
        c.update(kw)
        return Config(**c)

    def describe(self):
        s, b = self["system"], self["boundary"]
        return dict(run_id=self["run_id"], system=s.as_dict(), boundary=b.as_dict() if b else None,
                    model=self["model"], relationships=self["relationships"].as_dict() if self["relationships"] else None,
                    controls=self["controls"].as_dict() if self["controls"] else None,
                    environment=self["environment"].as_dict(), parameters=self["parameters"].as_dict(),
                    initial=self["initial"].as_dict(), t_end=self["t_end"], dt=self["dt"])


def _axpy(state, rates, h):
    out = dict(state)
    for k, r in rates.items():
        out[k] = out.get(k, 0.0) + h * r
    return out


def _extra_rates(out, cfg):
    """Quantities integrated beside the state: the boundary accumulators of the L0 gate."""
    return l0.flux_keys(out, cfg["budgets"])


def _eval(model, state, t, dt, cfg, params):
    envd = dict(cfg["environment"].at(t))
    envd.update(t=t, dt=dt, rng=cfg["environment"].rng)
    out = model(state, envd, cfg["relationships"], cfg["controls"], params)
    rates = dict(out.state_changes)
    rates.update(_extra_rates(out, cfg))
    return rates, out


def integrate(model, cfg, params, state):
    dt, n = cfg["dt"], int(round(cfg["t_end"] / cfg["dt"]))
    times, states, outs = [0.0], [dict(state)], []
    pert = (cfg["controls"].get("perturbation") if cfg["controls"] else None) or None
    for i in range(n):
        t = i * dt
        if model.kind == "rate":
            k1, out = _eval(model, state, t, dt, cfg, params)
            k2, _ = _eval(model, _axpy(state, k1, 0.5 * dt), t + 0.5 * dt, dt, cfg, params)
            k3, _ = _eval(model, _axpy(state, k2, 0.5 * dt), t + 0.5 * dt, dt, cfg, params)
            k4, _ = _eval(model, _axpy(state, k3, dt), t + dt, dt, cfg, params)
            comb = {k: (k1[k] + 2 * k2.get(k, 0.0) + 2 * k3.get(k, 0.0) + k4.get(k, 0.0)) / 6.0 for k in k1}
            state = _axpy(state, comb, dt)
        else:
            delta, out = _eval(model, state, t, dt, cfg, params)
            state = _axpy(state, delta, 1.0)
            if out.new_config is not None:
                state["_config"] = out.new_config
        if pert and abs((t + dt) - pert["at"]) < 0.5 * dt:
            state = _apply_kick(state, pert, cfg["budgets"])
        times.append(t + dt)
        states.append(dict(state))
        outs.append(out)
    return times, states, outs


def _apply_kick(state, pert, budgets):
    """A kick moves quantity across the boundary, so it is booked there."""
    state = dict(state)
    m = pert["magnitude"]
    state[pert["target"]] += m
    for b in budgets.values():
        if b.live and pert["target"] in b.pools:
            k = ("_in|%s|perturbation" if m >= 0 else "_out|%s|perturbation") % b.name
            state[k] = state.get(k, 0.0) + abs(m)
    return state


def _finish(record, cfg, model, times, states, outs):
    """Additions append their sections here."""
    rows, crossings = l0.audit(cfg["budgets"], states[0], states[-1])
    record["l0_budgets"], record["boundary_audit"] = rows, crossings
    record["status"], record["status_reason"] = l0.run_status(rows)
    record["expiry"] = dict(parameters=cfg["parameters"].expiry_report(), initial=cfg["initial"].expiry_report())
    from .. import known_answer_gate as gate
    t = gate.trust(model.name)
    record["model_trust"] = "TRUSTED: " + t["evidence"] if t["trusted"] else "UNTRUSTED: " + t["evidence"]
    if not t["trusted"]:
        record["status"] = "INCOMPLETE"
        record["status_reason"] += "; model not through the known-answer gate"
    return record


def run(cfg, code_paths=()):
    model = eq.get(cfg["model"])
    params = cfg["parameters"].resolve()          # raises on an unknown
    state = cfg["initial"].resolve()
    times, states, outs = integrate(model, cfg, params, state)
    numeric = lambda s: {k: v for k, v in s.items() if not k.startswith("_")}
    obs = cfg["observations"]
    record = dict(
        run_id=cfg["run_id"], status="PENDING L0",
        configuration_record=cfg.describe(),
        equation=model.ident(),
        boundary_specification=cfg["boundary"].as_dict() if cfg["boundary"] else "NONE DECLARED",
        control_specification=cfg["controls"].as_dict() if cfg["controls"] else "NONE DECLARED",
        parameter_values=cfg["parameters"].as_dict(),
        initial_conditions=cfg["initial"].as_dict(),
        observations_and_predictions=dict(observations=obs if obs is not None else "NONE SUPPLIED",
                                          final_state=numeric(states[-1]), n_steps=len(times) - 1),
        uncertainty_propagation=results.NOT_RUN,
        perturbation_response=results.NOT_RUN,
        continuity_and_transitions=results.NOT_RUN,
        applicability_region=results.NOT_RUN,
        known_limitations=list(model.limitations),
        model_uncertainty=outs[-1].uncertainty if outs else eq.NOT_APPLICABLE,
        boundary_behavior_last=outs[-1].boundary_behavior if outs else eq.NOT_APPLICABLE,
        energy_changes_last=outs[-1].energy_changes if outs else eq.NOT_APPLICABLE,
        provenance=provenance.stamp(cfg.describe(), list(code_paths) + [os.path.abspath(__file__)]),
    )
    record = _finish(record, cfg, model, times, states, outs)
    record["_trajectory"] = dict(times=times, states=[numeric(s) for s in states])
    return results.check(record)
