"""Family B. dx/dt = f(x, u, e, theta). One member: growth with an Allee threshold.

    dx/dt = r x (x/a - 1)(1 - x/K) - h x

Two stable states (0 and near K) and an unstable threshold at a.
"""
from .base import ModelOutput, from_transfers, register


def allee(state, env, rel, ctl, p):
    x = state["x"]
    g = p["r"] * x * (x / p["a"] - 1.0) * (1.0 - x / p["K"])
    tr = [("growth", None, "x", g)] if g >= 0 else [("decline", "x", None, -g)]
    tr.append(("harvest", "x", None, p["h"] * x))
    side = "above threshold" if x > p["a"] else "below threshold"
    return ModelOutput(from_transfers(tr, ["x"]), transfers=tr, configuration_changes=side,
                       uncertainty="threshold a and capacity K are parameters, not derived")


register("allee", "nonlinear", "0.1", allee, "rate", requires=("r", "a", "K", "h"),
         limitations=("well-mixed: one number for the whole system", "the threshold is put in by hand"))
