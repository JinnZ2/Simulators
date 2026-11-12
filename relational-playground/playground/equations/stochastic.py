"""Family F. dx = f(x,t) dt + G(x,t) dW. One member: mean reversion with additive noise,
Euler-Maruyama, one step per call. The random stream is the environment's seeded one."""
import math
from .base import ModelOutput, from_transfers, register


def mean_reverting(state, env, rel, ctl, p):
    x, dt = state["x"], env["dt"]
    drift = p["theta"] * (p["mu"] - x) * dt
    noise = p["sigma"] * math.sqrt(dt) * env["rng"].gauss(0.0, 1.0)
    tr = []
    for name, v in (("drift", drift), ("noise", noise)):
        tr.append((name + "_in", None, "x", v) if v >= 0 else (name + "_out", "x", None, -v))
    return ModelOutput(from_transfers(tr, ["x"]), transfers=tr,
                       uncertainty=dict(stationary_sd=p["sigma"] / math.sqrt(2 * p["theta"]) if p["theta"] > 0 else "undefined"))


register("mean_reverting", "stochastic", "0.1", mean_reverting, "step", requires=("theta", "mu", "sigma"),
         limitations=("additive Gaussian noise only", "first-order step: dt must be small against 1/theta"))
