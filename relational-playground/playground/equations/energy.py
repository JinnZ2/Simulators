"""Family D. dE/dt = P_in - P_out - P_diss, with P_out = demand while E > 0 and P_diss = k E."""
from .base import ModelOutput, from_transfers, register


def energy_store(state, env, rel, ctl, p):
    E = state["E"]
    p_in = env.get("P_in", p["P_in"])
    p_out = p["demand"] if E > 0 else 0.0
    p_diss = p["k_diss"] * max(E, 0.0)
    tr = [("P_in", None, "E", p_in), ("P_out", "E", None, p_out), ("P_diss", "E", None, p_diss)]
    return ModelOutput(from_transfers(tr, ["E"]), transfers=tr,
                       energy_changes=dict(P_in=p_in, P_out=p_out, P_diss=p_diss),
                       configuration_changes="operating" if E > 0 else "store empty: demand not met",
                       uncertainty="one store; dissipation proportional to stored energy")


register("energy_store", "energy", "0.1", energy_store, "rate", requires=("P_in", "demand", "k_diss"),
         limitations=("demand switches off abruptly at E = 0", "no spatial structure"))
