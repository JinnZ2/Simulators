"""ADDITION 7. Family H, branching process: generations of offspring, with early die-out.

Each active individual leaves a number of offspring and retires. offspring =
"poisson" draws Poisson(R) each (seeded); "fixed" gives exactly R each (R whole).
A line can die in its first few generations by chance even when R > 1; the chance
that it dies out at all is the smallest root of q = exp(R (q - 1)).

Ledger: births cross the boundary inward; active -> retired is a transfer.
"""
from .base import ModelOutput, from_transfers, register
from .branching_math import extinction_probability, _poisson

POOLS = ("active", "retired")


def branching(state, env, rel, ctl, p):
    n = int(round(state["active"]))
    if n > p["cap"]:
        return ModelOutput(from_transfers([], POOLS), transfers=[], configuration_changes="established: population over the cap, growth not followed")
    if p["offspring"] == "fixed":
        births = n * int(p["R"])
    elif p["offspring"] == "poisson":
        births = _poisson(env["rng"], n * p["R"]) if n else 0     # a sum of n Poisson(R) is Poisson(nR)
    else:
        raise ValueError("offspring must be poisson or fixed")
    tr = [("retire", "active", "retired", n), ("births", None, "active", births)]
    return ModelOutput(from_transfers(tr, POOLS), transfers=tr,
                       configuration_changes="extinct" if births == 0 else "alive",
                       uncertainty=dict(die_out_probability_per_founder=extinction_probability(p["R"]) if p["offspring"] == "poisson" else "not stochastic"))


register("branching", "branching", "0.1", branching, "step", requires=("R", "offspring", "cap"),
         limitations=("individuals do not compete: no depletion of what they spread through",
                      "over the cap the process is declared established and not followed",
                      "Poisson draws above mean 30 use a normal approximation"))
