"""Family E. dx/dt = f(x, e, B(t), u): exchange through a boundary whose permeability moves.

    B(t) = perm0 + perm_drift * t   (floored at 0)
    dx/dt = B(t) (e - x) - loss x
"""
from .base import ModelOutput, from_transfers, register


def permeable(state, env, rel, ctl, p):
    x, t = state["x"], env["t"]
    perm = max(0.0, p["perm0"] + p["perm_drift"] * t)
    e = env.get("outside", p["outside"])
    ex = perm * (e - x)
    tr = [("exchange_in", None, "x", ex)] if ex >= 0 else [("exchange_out", "x", None, -ex)]
    tr.append(("loss", "x", None, p["loss"] * x))
    return ModelOutput(from_transfers(tr, ["x"]), transfers=tr,
                       boundary_behavior=dict(permeability=perm, exchange_rate=ex, gradient=e - x),
                       uncertainty="the boundary is one coefficient; no thickness, no interface store")


register("permeable", "boundary", "0.1", permeable, "rate", requires=("perm0", "perm_drift", "outside", "loss"),
         limitations=("a thin boundary by construction", "permeability is prescribed, not generated"))
