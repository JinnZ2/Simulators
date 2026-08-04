#!/usr/bin/env python3
"""
percolation_lens.py -- packing-vs-distinguishability lens.  stdlib only.

Reads the manifold graph payload and treats the "how many distinguishable
cosmologies" question (report Section 8: N ~ 4) as a percolation problem.

Nodes are parameter points (lambda, beta).  For any distinguishability
threshold theta on the observable-space distance, two nodes are connected
if their observables (w0, wa, fs8_ratio) are within theta sigma of each
other under the assumed measurement covariance.  As theta rises, the
graph goes from disconnected islands to a single spanning cluster.

The packing question is then: is the report's theta = 1 sigma choice
sitting on a plateau (stable count) or near the percolation transition
(unstable -- small covariance changes flip the count)?

The lens returns a curve, not a verdict:
  theta -> (n_components, giant_fraction, mean_component_size)

Bond percolation on a fixed node set. Union-find, stdlib only.  Uses
diagonal observation-space covariance (sigma_w0=0.04, sigma_wa=0.16,
sigma_fs8=0.02) matching payload_bridge's DESI_MU / SIG_FS8.

names_no: [intent, verdict].
"""

import json, os


# --- distance --------------------------------------------------------------

SIG_W0, SIG_WA, SIG_FS8 = 0.04, 0.16, 0.02


def _dist(a, b):
    dw = (a["w0"] - b["w0"]) / SIG_W0
    dw_a = (a["wa"] - b["wa"]) / SIG_WA
    df = (a["fs8_ratio"] - b["fs8_ratio"]) / SIG_FS8
    return (dw * dw + dw_a * dw_a + df * df) ** 0.5


# --- union-find ------------------------------------------------------------

class _UF:
    def __init__(self, n):
        self.p = list(range(n)); self.r = [0] * n; self.sz = [1] * n

    def find(self, i):
        while self.p[i] != i:
            self.p[i] = self.p[self.p[i]]
            i = self.p[i]
        return i

    def union(self, i, j):
        ri, rj = self.find(i), self.find(j)
        if ri == rj:
            return False
        if self.r[ri] < self.r[rj]:
            ri, rj = rj, ri
        self.p[rj] = ri
        self.sz[ri] += self.sz[rj]
        if self.r[ri] == self.r[rj]:
            self.r[ri] += 1
        return True


# --- read the graph payload ------------------------------------------------

def load(payload_path):
    """Load {node_id -> observables dict}. Skips singularity-flagged nodes."""
    obs = {}
    with open(payload_path) as f:
        for line in f:
            if not line.strip():
                continue
            r = json.loads(line)
            o = r.get("observables", {})
            if o.get("w0") is None or o.get("wa") is None:
                continue
            obs[r["node_id"]] = {"w0": float(o["w0"]),
                                 "wa": float(o["wa"]),
                                 "fs8_ratio": float(o["fs8_ratio"]),
                                 "lam": float(r["state_vector"]["lambda"]),
                                 "beta": float(r["state_vector"]["beta"])}
    return obs


def _components(obs, theta):
    """
    Number of connected components at threshold `theta` (sigma).
    Also the size of the largest and the mean component size.
    """
    ids = list(obs.keys())
    n = len(ids)
    if n == 0:
        return {"theta": theta, "n_components": 0, "giant_fraction": 0.0,
                "mean_size": 0.0, "n_nodes": 0}
    uf = _UF(n)
    for i in range(n):
        oi = obs[ids[i]]
        for j in range(i + 1, n):
            if _dist(oi, obs[ids[j]]) <= theta:
                uf.union(i, j)
    roots = {uf.find(i): uf.sz[uf.find(i)] for i in range(n)}
    sizes = list(roots.values())
    return {"theta": theta, "n_components": len(sizes),
            "giant_fraction": max(sizes) / n,
            "mean_size": sum(sizes) / len(sizes),
            "n_nodes": n}


def sweep(payload_path, thetas=None):
    """
    Full curve: for each theta, count components.  Percolation
    transition is where giant_fraction jumps from <~ 0.2 to > 0.5
    over a small theta range.
    """
    if thetas is None:
        thetas = [0.2, 0.3, 0.5, 0.7, 1.0, 1.5, 2.0, 3.0, 5.0]
    obs = load(payload_path)
    return [_components(obs, t) for t in thetas]


# --- self-test -------------------------------------------------------------

_PAYLOAD = os.path.join(os.path.dirname(__file__), "..", "figures",
                       "manifold_graph_payload.jsonl")


def _t_theta_zero_gives_n_singletons():
    obs = load(_PAYLOAD)
    r = _components(obs, 0.0)
    # each node is its own component at theta=0
    assert r["n_components"] == r["n_nodes"], (r["n_components"], r["n_nodes"])
    assert abs(r["giant_fraction"] - 1.0 / r["n_nodes"]) < 1e-9


def _t_large_theta_gives_one_component():
    obs = load(_PAYLOAD)
    r = _components(obs, 1e6)
    assert r["n_components"] == 1
    assert r["giant_fraction"] == 1.0


def _t_monotone_in_theta():
    obs = load(_PAYLOAD)
    prev = None
    for t in [0.1, 0.5, 1.0, 2.0, 5.0]:
        r = _components(obs, t)
        # more edges -> fewer components, giant grows or holds
        assert prev is None or r["n_components"] <= prev["n_components"]
        assert prev is None or r["giant_fraction"] >= prev["giant_fraction"] - 1e-9
        prev = r


def _run():
    for name, fn in sorted(globals().items()):
        if name.startswith("_t_"):
            fn(); print("ok", name)
    print("all pass\n")


def _demo():
    print("--- Percolation sweep on the 48-node manifold graph ---")
    print(f"{'theta':>7}{'n_comp':>9}{'giant_frac':>13}"
          f"{'mean_size':>12}{'n_nodes':>10}")
    curve = sweep(_PAYLOAD)
    for r in curve:
        print(f"{r['theta']:>7.2f}{r['n_components']:>9}"
              f"{r['giant_fraction']:>13.3f}{r['mean_size']:>12.2f}"
              f"{r['n_nodes']:>10}")
    print()
    # locate the transition: where giant_fraction crosses 0.5
    crossing = None
    for i in range(1, len(curve)):
        if curve[i - 1]["giant_fraction"] < 0.5 <= curve[i]["giant_fraction"]:
            crossing = (curve[i - 1]["theta"], curve[i]["theta"])
            break
    print(f"Report's threshold (theta = 1.0 sigma) -> {curve[thetas_index(curve, 1.0)]['n_components']} components,"
          f" giant_fraction = {curve[thetas_index(curve, 1.0)]['giant_fraction']:.3f}")
    if crossing:
        print(f"Percolation transition (giant_fraction crosses 0.5) "
              f"between theta = {crossing[0]} and {crossing[1]}")
        report_theta = 1.0
        if crossing[0] <= report_theta <= crossing[1]:
            print("  -> The report's 'N ~ 4 distinguishable' count sits ON the")
            print("     percolation transition. Small covariance changes will")
            print("     jump the count. The number is unstable, not the geometry.")
        else:
            print("  -> The report's threshold is off the transition. The count")
            print("     is stable under modest covariance rescaling.")
    else:
        print("No 0.5 crossing in this sweep range; extend theta.")


def thetas_index(curve, target):
    for i, r in enumerate(curve):
        if abs(r["theta"] - target) < 1e-9:
            return i
    return -1


if __name__ == "__main__":
    _run(); _demo()
