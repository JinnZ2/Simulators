"""ADDITION 7. Family G, percolation: spread on a grid, with a spatial threshold.

Cells are flammable with probability p_flammable when grid == "RANDOM", or laid
out by an explicit L x L grid (0 bare, 1 fuel). Fire moves to the four nearest flammable neighbours each step. With
probability `spot` a burning cell also throws one ember to a cell chosen
uniformly on the whole grid; the ember ignites it if it is flammable and unburned.

State is cell counts (unassigned, unburned, burning, burned, bare); the grid
itself rides in state["_config"]. Every change of a cell's class is a transfer,
so the cell count is a closable budget. Step 0 lays the grid out and lights it.

Site percolation on the square lattice has its threshold near 0.593 for an
infinite grid; on a finite grid the transition is smeared and is located by a sweep.
"""
from .base import ModelOutput, from_transfers, register

POOLS = ("unassigned", "unburned", "burning", "burned", "bare")
BARE, FUEL, FIRE, ASH = 0, 1, 2, 3


def _layout(env, p):
    L = int(p["L"])
    if p["grid"] != "RANDOM":
        g = [list(row) for row in p["grid"]]
        if len(g) != L or any(len(r) != L for r in g):
            raise ValueError("explicit grid must be L x L")
        return g
    rng = env["rng"]
    return [[FUEL if rng.random() < p["p_flammable"] else BARE for _ in range(L)] for _ in range(L)]


def percolation(state, env, rel, ctl, p):
    L = int(p["L"])
    grid = state.get("_config")
    if grid is None:                                   # step 0: lay out and ignite
        g = _layout(env, p)
        if p["ignition"] == "left_edge":
            lit = [(i, 0) for i in range(L) if g[i][0] == FUEL]
        elif p["ignition"] == "centre":
            lit = [(L // 2, L // 2)] if g[L // 2][L // 2] == FUEL else []
        else:
            raise ValueError("ignition must be left_edge or centre")
        for i, j in lit:
            g[i][j] = FIRE
        fuel = sum(r.count(FUEL) for r in g)
        bare = sum(r.count(BARE) for r in g)
        tr = [("layout_fuel", "unassigned", "unburned", fuel), ("layout_bare", "unassigned", "bare", bare),
              ("layout_ignited", "unassigned", "burning", len(lit))]
        return ModelOutput(from_transfers(tr, POOLS), transfers=tr, new_config=dict(grid=g, front=lit),
                           configuration_changes="grid laid out; %d cells lit" % len(lit))
    g, front, rng = grid["grid"], grid["front"], env["rng"]
    new, n_local, n_spot = [], 0, 0
    for i, j in front:
        for a, b in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
            if 0 <= a < L and 0 <= b < L and g[a][b] == FUEL:
                g[a][b] = FIRE
                new.append((a, b))
                n_local += 1
        if p["spot"] > 0 and rng.random() < p["spot"]:
            a, b = rng.randrange(L), rng.randrange(L)
            if g[a][b] == FUEL:
                g[a][b] = FIRE
                new.append((a, b))
                n_spot += 1
    for i, j in front:
        g[i][j] = ASH
    tr = [("spread_local", "unburned", "burning", n_local), ("spread_spot", "unburned", "burning", n_spot),
          ("burn_out", "burning", "burned", len(front))]
    return ModelOutput(from_transfers(tr, POOLS), transfers=tr, new_config=dict(grid=g, front=new),
                       relationship_changes=dict(local_ignitions=n_local, spot_ignitions=n_spot),
                       configuration_changes="burning" if new else "out",
                       uncertainty="one grid, one seed: a replicate set is needed before reading a fraction")


register("percolation", "percolation", "0.1", percolation, "step",
         requires=("L", "p_flammable", "spot", "ignition", "grid"),
         limitations=("finite grid: the threshold is smeared over a band that narrows with L",
                      "four-neighbour spread only; no wind, no slope",
                      "an ember lands anywhere with equal chance: no distance kernel"))
