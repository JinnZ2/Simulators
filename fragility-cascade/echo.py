"""
echo.py -- independence by construction, not by declaration.
CC0. stdlib only.

Replaces the proxy test.

    OLD: two supports are independent if they used different modes.
    NEW: two supports are independent if their provenance paths share
         no interior node. Different modes fed by the same upstream
         source are ONE support wearing two hats.

Same structure, three dialects:

    graph          vertex-disjoint paths (Menger)      <- implemented here
    systematics    homology vs homoplasy               <- interpretation
    estimation     correlated-error fusion             <- warning label

    agreement traced to a shared ancestor is HOMOLOGY: inherited, not
    corroborating, weight 0. agreement arrived at through disjoint paths
    is HOMOPLASY: convergent, and the only kind that counts.

Menger's theorem does the work: the maximum number of vertex-disjoint
paths equals the minimum vertex cut. So one computation returns both
    support  -- how many independent ways this claim reaches ground
    cut      -- the smallest set of nodes whose loss disconnects it
The cut is the fragility set. Ordered by clock.freshness(), it is the
retest queue.

No verdicts. Counts, cuts, and LOUD flags.
"""

from dataclasses import dataclass, field
from collections import deque
from typing import Dict, List, Set, Optional, Tuple
import clock

INF = float("inf")

# ----------------------------------------------------------------- the graph

@dataclass
class Node:
    id: str
    kind: str                       # claim | mode | source | anchor
    as_of: Optional[str] = None     # anchors especially
    volatility: Optional[str] = None
    mode: Optional[str] = None      # which mode this node was read through
    label: str = ""


@dataclass
class ProvGraph:
    """
    Edges point DOWNSTREAM: anchor -> source -> mode -> claim.
    Traversal for support runs upstream, from the claim back to ground.
    PROV-compatible: this is wasDerivedFrom read in the reading direction.
    """
    nodes: Dict[str, Node] = field(default_factory=dict)
    edges: Dict[str, Set[str]] = field(default_factory=dict)   # up -> {down}

    def add(self, n: Node) -> Node:
        self.nodes[n.id] = n
        self.edges.setdefault(n.id, set())
        return n

    def link(self, upstream: str, downstream: str) -> None:
        for x in (upstream, downstream):
            if x not in self.nodes:
                raise KeyError(f"unknown node '{x}'")
        self.edges[upstream].add(downstream)

    def upstream_of(self, nid: str) -> Set[str]:
        return {u for u, ds in self.edges.items() if nid in ds}


# --------------------------------------------------- max-flow w/ node capacity

def _split(g: ProvGraph, claim: str) -> Tuple[dict, str, str]:
    """
    Node-splitting: every interior node becomes v_in -> v_out with capacity 1,
    so a unit of flow = one path that uses that node, and no path can reuse it.
    The claim itself and the super-sink are uncapped -- we are counting the
    paths BETWEEN them, not through them.
    """
    cap: Dict[str, Dict[str, float]] = {}

    def edge(u, v, c):
        cap.setdefault(u, {}).setdefault(v, 0)
        cap.setdefault(v, {}).setdefault(u, 0)
        cap[u][v] += c

    SRC, SINK = "__claim__", "__ground__"
    for nid, n in g.nodes.items():
        c = INF if nid == claim else 1.0
        edge(f"{nid}|i", f"{nid}|o", c)
        if n.kind == "anchor":
            edge(f"{nid}|o", SINK, INF)

    # walk upstream from the claim; reversed edges so flow runs claim -> ground
    for up, downs in g.edges.items():
        for dn in downs:
            edge(f"{dn}|i", f"{up}|i", 0)     # ensure keys exist
            edge(f"{dn}|o", f"{up}|i", INF)

    edge(SRC, f"{claim}|i", INF)
    return cap, SRC, SINK


def _maxflow(cap: dict, s: str, t: str) -> Tuple[float, dict]:
    """Edmonds-Karp. Graphs here are small; clarity over speed."""
    flow = 0.0
    while True:
        parent = {s: None}
        q = deque([s])
        while q and t not in parent:
            u = q.popleft()
            for v, c in cap.get(u, {}).items():
                if v not in parent and c > 0:
                    parent[v] = u
                    q.append(v)
        if t not in parent:
            return flow, parent          # parent == reachable set in residual
        # bottleneck
        b, v = INF, t
        while parent[v] is not None:
            u = parent[v]
            b = min(b, cap[u][v])
            v = u
        v = t
        while parent[v] is not None:
            u = parent[v]
            cap[u][v] -= b
            cap[v][u] += b
            v = u
        flow += b


# ------------------------------------------------------------------- reading

@dataclass
class Independence:
    claim: str
    support: int                    # vertex-disjoint paths to ground
    cut: List[str]                  # min vertex cut = fragility set
    anchors_reached: List[str]
    choke_points: List[str]         # nodes every path must use
    loud: List[str] = field(default_factory=list)


def independence(g: ProvGraph, claim: str) -> Independence:
    if claim not in g.nodes:
        raise KeyError(claim)
    cap, s, t = _split(g, claim)
    flow, reachable = _maxflow(cap, s, t)

    # Menger: min vertex cut = nodes with in-side reachable, out-side not
    cut = sorted(nid for nid in g.nodes
                 if f"{nid}|i" in reachable and f"{nid}|o" not in reachable)

    anchors = sorted(n.id for n in g.nodes.values() if n.kind == "anchor")
    reached = [a for a in anchors if _reaches(g, a, claim)]

    loud: List[str] = []
    n = int(flow) if flow != INF else 0
    if n == 0:
        loud.append("support 0 -- claim does not reach any anchor: "
                    "cannot be re-checked, only re-argued")
    apparent = len(g.upstream_of(claim))
    if apparent > n:
        loud.append(f"ECHO: {apparent} apparent supports collapse to {n} -- "
                    f"routes share interior node(s) {cut}; the agreement is "
                    "homologous (inherited), not convergent")
    choke = [c for c in cut] if n == 1 else []
    return Independence(claim, n, cut, reached, choke, loud)


def _reaches(g: ProvGraph, start: str, target: str) -> bool:
    seen, q = {start}, deque([start])
    while q:
        u = q.popleft()
        if u == target:
            return True
        for v in g.edges.get(u, ()):
            if v not in seen:
                seen.add(v)
                q.append(v)
    return False


def common_ancestors(g: ProvGraph, a: str, b: str) -> List[str]:
    """Homology test for two corroborating claims. Non-empty -> shared descent."""
    return sorted(_ancestors(g, a) & _ancestors(g, b))


def _ancestors(g: ProvGraph, nid: str) -> Set[str]:
    seen, q = set(), deque([nid])
    while q:
        u = q.popleft()
        for p in g.upstream_of(u):
            if p not in seen:
                seen.add(p)
                q.append(p)
    return seen


def agreement(g: ProvGraph, a: str, b: str) -> dict:
    shared = common_ancestors(g, a, b)
    return {
        "pair": (a, b),
        "shared_ancestors": shared,
        "reading": "HOMOLOGY -- inherited agreement, weight 0" if shared
                   else "HOMOPLASY -- convergent, counts as support",
    }


# ------------------------------------------------- fragility x clock = queue

def retest_queue(g: ProvGraph, claim: str, now: str,
                 mode_half_lives: Optional[Dict[str, float]] = None) -> List[dict]:
    """
    The cut set is what the claim stands on. Ordered by freshness, it is the
    order in which the claim will fall over. Staleest cut member first.
    """
    mh = mode_half_lives or {}
    ind = independence(g, claim)
    rows = []
    for nid in ind.cut:
        n = g.nodes[nid]
        f = clock.freshness(n.as_of, now,
                            mode_half_life_days=mh.get(n.mode),
                            volatility=n.volatility)
        rows.append({"node": nid, "kind": n.kind, "band": f.band,
                     "remaining": f.remaining, "loud": f.loud})
    rows.sort(key=lambda r: (r["remaining"] is not None,
                             r["remaining"] if r["remaining"] is not None else 0))
    return rows
