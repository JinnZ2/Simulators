"""cut.py — vertex cut computations via Menger's theorem.

`vertex_connectivity(G, s, t)` returns κ(G, s, t), the minimum number
of vertices (excluding s and t) whose removal disconnects s from t.
By Menger's theorem this equals the maximum number of internally
vertex-disjoint s-t paths, so κ = 1 means there is a single vertex
whose removal is sufficient, and κ = 0 means s and t are already
disconnected in G.

`cut_vertices(G, s, t)` returns the set of vertices v (v not in {s,t})
such that G − v has no s-t path. For κ = 1 this is exactly the set of
single cut vertices; for κ ≥ 2 it is empty. For κ = 0 it raises —
there is nothing to cut.

The token node is treated like any other vertex. Whether it is a cut
vertex in a given G_θ is a property of G_θ, not a special status of
the token.
"""

from collections import deque

TOKEN_NODE = "__TOKEN__"

def _adj(graph):
    adj = {}
    for u, v in graph.edges().keys():
        adj.setdefault(u, set()).add(v)
        adj.setdefault(v, set())
    return adj

def _reachable(adj, s, t, removed):
    if s in removed or t in removed:
        return False
    seen = {s}
    q = deque([s])
    while q:
        u = q.popleft()
        if u == t:
            return True
        for v in adj.get(u, ()):
            if v not in seen and v not in removed:
                seen.add(v)
                q.append(v)
    return False

def is_connected(graph, s=None, t=None, removed=frozenset()):
    s = s if s is not None else graph.source
    t = t if t is not None else graph.target
    return _reachable(_adj(graph), s, t, set(removed))

def cut_vertices(graph, s=None, t=None):
    """Return (kappa, vertex_set). kappa 0 => already disconnected."""
    s = s if s is not None else graph.source
    t = t if t is not None else graph.target
    adj = _adj(graph)

    if not _reachable(adj, s, t, removed=set()):
        return 0, set()

    # κ=1 case: single cut vertices
    single = set()
    candidates = [v for v in adj.keys() if v not in (s, t)]
    for v in candidates:
        if not _reachable(adj, s, t, removed={v}):
            single.add(v)

    if single:
        return 1, single

    # κ ≥ 2: return the value, not a set (no single-vertex cut exists)
    kappa = _max_vertex_disjoint_paths(graph, s, t)
    return kappa, set()

# --- max flow on split graph ------------------------------------------

def _split_nodes(graph):
    """Return a split graph. Every v not in {s,t} becomes v_in, v_out
    with edge capacity 1. Every original edge u->v becomes u_out -> v_in
    with capacity INFINITY."""
    s, t = graph.source, graph.target
    adj = _adj(graph)

    def out_of(v):
        return v if v in (s, t) else f"{v}#out"
    def in_of(v):
        return v if v in (s, t) else f"{v}#in"

    cap = {}
    nodes = set()
    for u in adj:
        for v in adj[u]:
            a, b = out_of(u), in_of(v)
            nodes.add(a); nodes.add(b)
            cap[(a, b)] = cap.get((a, b), 0) + 10**9
    for v in adj:
        if v in (s, t):
            continue
        a, b = in_of(v), out_of(v)
        nodes.add(a); nodes.add(b)
        cap[(a, b)] = cap.get((a, b), 0) + 1
    return nodes, cap, s, t, out_of, in_of

def _max_vertex_disjoint_paths(graph, s, t):
    nodes, cap, s_node, t_node, out_of, in_of = _split_nodes(graph)
    src, dst = out_of(s_node), in_of(t_node)

    def neighbors(u):
        return [v for (a, v) in cap if a == u]

    flow = 0
    while True:
        # BFS to find augmenting path
        parent = {src: None}
        q = deque([src])
        while q and dst not in parent:
            u = q.popleft()
            for v in neighbors(u):
                if v in parent or cap.get((u, v), 0) <= 0:
                    continue
                parent[v] = u
                q.append(v)
        if dst not in parent:
            break
        # find bottleneck
        path = []
        v = dst
        while v is not None:
            path.append(v)
            v = parent[v]
        path.reverse()
        bottleneck = min(cap.get((path[i], path[i+1]), 0)
                         for i in range(len(path) - 1))
        for i in range(len(path) - 1):
            u, v = path[i], path[i+1]
            cap[(u, v)] = cap.get((u, v), 0) - bottleneck
            cap[(v, u)] = cap.get((v, u), 0) + bottleneck
        flow += bottleneck

    return flow

def vertex_connectivity(graph, s=None, t=None):
    """Menger's κ. Distinct from cut_vertices when κ ≥ 2."""
    s = s if s is not None else graph.source
    t = t if t is not None else graph.target
    if not is_connected(graph, s, t):
        return 0
    kappa, single = cut_vertices(graph, s, t)
    return kappa
